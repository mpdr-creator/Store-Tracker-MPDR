import db
import string
import random

def gen_numeric_id(length=6):
    """Generate a random 6-digit numeric ID."""
    return "".join(random.choices(string.digits, k=length))

def migrate_to_6_digits():
    """
    Standardizes all Item IDs to exactly 6 digits.
    Updates all related worksheets: Inventory, Ledger, and Requests.
    """
    print("🚀 Starting ID Standardization Migration...")
    
    # 1. Fetch all worksheets
    sh = db._get_spreadsheet()
    if not sh:
        print("❌ Could not connect to Google Sheets.")
        return

    print("--- Fetching data from all worksheets ---")
    ws_inv = db._ws(db.WS_INVENTORY)
    inv_rows = ws_inv.get_all_values()
    
    ws_ledger = db._ws(db.WS_LEDGER)
    ledger_rows = ws_ledger.get_all_values()
    
    ws_req = db._ws(db.WS_REQUESTS)
    req_rows = ws_req.get_all_values()
    
    if not inv_rows:
        print("❌ No inventory data found.")
        return

    # 2. Map existing IDs to new 6-digit numeric IDs
    item_map = {}
    headers_inv = inv_rows[0]
    id_idx = headers_inv.index("Item_ID")
    
    print("--- Mapping Item IDs ---")
    for i in range(1, len(inv_rows)):
        old_id = str(inv_rows[i][id_idx]).strip()
        # If it's already 6 digits, keep it, otherwise generate a new one
        if len(old_id) == 6 and old_id.isdigit():
            item_map[old_id] = old_id
        else:
            new_id = gen_numeric_id()
            # Ensure uniqueness in the map
            while new_id in item_map.values():
                new_id = gen_numeric_id()
            item_map[old_id] = new_id
            inv_rows[i][id_idx] = new_id
            print(f"  Mapped: {old_id} -> {new_id}")

    # 3. Update Ledger references
    print("--- Updating Ledger references ---")
    if ledger_rows:
        headers_ledger = ledger_rows[0]
        l_id_idx = headers_ledger.index("Item_ID")
        for i in range(1, len(ledger_rows)):
            old_id = str(ledger_rows[i][l_id_idx]).strip()
            if old_id in item_map:
                ledger_rows[i][l_id_idx] = item_map[old_id]

    # 4. Update Request references
    print("--- Updating Request references ---")
    if req_rows:
        headers_req = req_rows[0]
        r_id_idx = headers_req.index("Item_ID")
        for i in range(1, len(req_rows)):
            old_id = str(req_rows[i][r_id_idx]).strip()
            if old_id in item_map:
                req_rows[i][r_id_idx] = item_map[old_id]

    # 5. Upload everything back
    print("--- Uploading new data ---")
    try:
        # Inventory
        ws_inv.clear()
        ws_inv.update(inv_rows)
        print("✅ Inventory Master updated.")
        
        # Ledger
        if ledger_rows:
            ws_ledger.clear()
            ws_ledger.update(ledger_rows)
            print("✅ Stock Ledger updated.")
            
        # Requests
        if req_rows:
            ws_req.clear()
            ws_req.update(req_rows)
            print("✅ Requests updated.")
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return

    print("\n🎉 Migration Complete! All Item IDs are now 6-digit numeric codes.")

if __name__ == "__main__":
    # Ensure DB is initialized (loads credentials)
    ok, msg = db.initialize_database()
    if ok:
        migrate_to_6_digits()
    else:
        print(f"❌ Database initialization failed: {msg}")
