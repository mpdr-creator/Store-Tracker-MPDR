# ──────────────────────────────────────────────
# Store Tracker — Excel → Google Sheets Importer
# ──────────────────────────────────────────────
"""
One-time script to import chemicals from the Excel file into:
  - Inventory_Master  (item details)
  - Stock_Ledger      (OPENING entries for initial quantities)

Usage:
    python import_data.py
"""
import re
import uuid
import datetime
import pandas as pd
import db
from config import WS_INVENTORY, WS_LEDGER, INVENTORY_HEADERS, LEDGER_HEADERS

EXCEL_PATH = "Chemicals & solvents inventory.xlsx"


def parse_quantity(qty_str):
    """Parse quantity strings like '500 g*2', '2.5 ltr', '250 ltrs' into (value, unit)."""
    if pd.isna(qty_str):
        return 0.0, "units"

    raw = str(qty_str).strip().lower()

    # Handle multipliers like '500 g*2'
    multiplier = 1
    mult_match = re.search(r"\*(\d+)", raw)
    if mult_match:
        multiplier = int(mult_match.group(1))
        raw = raw[: mult_match.start()].strip()

    # Handle patterns like '2 *25=50 ltrs'
    eq_match = re.search(r"=\s*([\d.]+)\s*([a-z]+)", raw)
    if eq_match:
        return float(eq_match.group(1)), eq_match.group(2).rstrip("s")

    # Extract number and unit
    match = re.search(r"([\d.]+)\s*([a-z]*)", raw)
    if match:
        value = float(match.group(1)) * multiplier
        unit = match.group(2).rstrip("s") or "units"
        # Normalise common units
        unit_map = {"ltr": "L", "ml": "mL", "gm": "g", "kg": "kg", "l": "L"}
        unit = unit_map.get(unit, unit)
        return value, unit

    return 1.0, "units"


def import_from_excel():
    print(f"Reading {EXCEL_PATH}...")
    df = pd.read_excel(EXCEL_PATH, header=4)
    print(f"  Loaded {len(df)} raw rows.")

    df = df.dropna(subset=["Chemical Name"])
    print(f"  {len(df)} rows after dropping empty names.")

    # Check for duplicates in existing inventory
    existing = db.get_all_items()
    existing_names = set()
    if not existing.empty:
        # Assuming Material_Name column exists in the output
        if "Material_Name" in existing.columns:
            existing_names = set(existing["Material_Name"].str.lower().str.strip())

    added = 0
    skipped = 0

    new_inventory_rows = []
    new_ledger_rows = []

    for _, row in df.iterrows():
        name = str(row.get("Chemical Name", "")).strip()
        if not name or name.lower() == "nan":
            continue

        if name.lower().strip() in existing_names:
            skipped += 1
            continue

        mat_type = str(row.get("Material Type", "")).strip()
        cas = str(row.get("CAS NO", "")).strip()
        if cas == "nan":
            cas = ""
        manufacturer = str(row.get("Manufacture", "")).strip()
        if manufacturer == "nan":
            manufacturer = ""

        qty_raw = row.get("Quantity")
        stock_val, unit = parse_quantity(qty_raw)

        # Use Available Quantity if present
        avail = row.get("Available Quantity")
        if pd.notna(avail):
            try:
                stock_val = float(str(avail).strip())
            except ValueError:
                pass

        # Build a short unique name
        unique = name.split("(")[0].strip()[:40]

        # Extract grade from name if present
        grade = ""
        grade_match = re.search(r"(\d+%)", name)
        if grade_match:
            grade = grade_match.group(1)

        item_id = str(uuid.uuid4())[:8]

        # Build dicts matching config headers
        inv_dict = {
            "Item_ID": item_id,
            "Unique_Name": unique,
            "Material_Name": name,
            "CAS_No": cas,
            "Grade_Purity": grade,
            "Manufacturer": manufacturer,
            "Units": unit,
        }
        
        new_inventory_rows.append([str(inv_dict.get(h, "")) for h in INVENTORY_HEADERS])

        if stock_val > 0:
            ledger_dict = {
                "Transaction_ID": str(uuid.uuid4())[:8],
                "Item_ID": item_id,
                "DateTime": datetime.datetime.now().isoformat(),
                "Transaction_Type": "OPENING",
                "Quantity": stock_val,
                "Reference_ID": "",
                "Updated_By": "import_script",
            }
            new_ledger_rows.append([str(ledger_dict.get(h, "")) for h in LEDGER_HEADERS])

        added += 1
        existing_names.add(name.lower().strip())

    if new_inventory_rows:
        print(f"Batch appending {len(new_inventory_rows)} records to Inventory_Master...")
        db._ws(WS_INVENTORY).append_rows(new_inventory_rows, value_input_option="USER_ENTERED")
        if new_ledger_rows:
            print(f"Batch appending {len(new_ledger_rows)} records to Stock_Ledger...")
            db._ws(WS_LEDGER).append_rows(new_ledger_rows, value_input_option="USER_ENTERED")
            
        print(f"\n✅ Import complete: {added} items added, {skipped} duplicates skipped.")
    else:
        print(f"\n✅ Import complete: No new items to add ({skipped} skipped).")


if __name__ == "__main__":
    print("Initialising database...")
    ok, msg = db.initialize_database()
    print(f"  {msg}")
    if ok:
        import_from_excel()
    else:
        print(f"  ❌ {msg}")
