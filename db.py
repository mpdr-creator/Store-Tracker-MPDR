# ──────────────────────────────────────────────
# Store Tracker — Database (Google Sheets) Layer
# ──────────────────────────────────────────────
import os
import random
import string
import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from config import (
    SCOPES, SPREADSHEET_NAME, SHARE_EMAIL,
    WS_INVENTORY, WS_LEDGER, WS_REQUESTS, WS_USERS, WS_VENDORS, WS_PO_TRACK,
    INVENTORY_HEADERS, LEDGER_HEADERS, REQUESTS_HEADERS, USERS_HEADERS, VENDOR_HEADERS, PO_HEADERS,
)

# ── Singleton-ish client cache ──────────────────
_client = None
_spreadsheet = None

def get_ist_now():
    """Return current time in Indian Standard Time."""
    ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    return datetime.datetime.now(ist)


def _get_client():
    global _client
    if _client is not None:
        return _client
    
    # 1. Try Streamlit Secrets (for Cloud Deployment)
    if "gcp_service_account" in st.secrets:
        try:
            creds_info = st.secrets["gcp_service_account"]
            creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
            _client = gspread.authorize(creds)
            return _client
        except Exception as e:
            print(f"[db] Error loading secrets: {e}")

    # 2. Try Local File (for Local Development)
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    if os.path.exists(creds_path):
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        _client = gspread.authorize(creds)
        return _client
        
    return None


def _get_spreadsheet():
    global _spreadsheet
    if _spreadsheet is not None:
        return _spreadsheet
    client = _get_client()
    if not client:
        return None
    _spreadsheet = client.open(SPREADSHEET_NAME)
    return _spreadsheet


def reset_connection():
    """Force reconnect on next call (useful after errors)."""
    global _client, _spreadsheet
    _client = None
    _spreadsheet = None


# ── Initialisation ─────────────────────────────
def _ensure_worksheet(sh, name, headers):
    """Create worksheet with headers if it doesn't exist."""
    existing = [ws.title for ws in sh.worksheets()]
    if name not in existing:
        # Rename Sheet1 for the first custom worksheet
        if name == WS_INVENTORY and "Sheet1" in existing:
            ws = sh.worksheet("Sheet1")
            ws.update_title(name)
        else:
            ws = sh.add_worksheet(title=name, rows=2000, cols=len(headers) + 2)
        ws = sh.worksheet(name)
        ws.append_row(headers)
    else:
        ws = sh.worksheet(name)
        # Ensure headers are present
        first_row = ws.row_values(1)
        if not first_row:
            ws.append_row(headers)
        else:
            missing = [h for h in headers if h not in first_row]
            if missing:
                try:
                    ws.add_cols(len(missing) + 2)
                except Exception:
                    pass
                for idx, m_head in enumerate(missing):
                    ws.update_cell(1, len(first_row) + idx + 1, m_head)
    return ws


def initialize_database():
    """Ensure spreadsheet + all 4 worksheets exist with correct headers."""
    client = _get_client()
    if not client:
        return False, "Could not initialise Google Sheets client. Check credentials.json."

    try:
        sh = client.open(SPREADSHEET_NAME)
    except gspread.SpreadsheetNotFound:
        try:
            sh = client.create(SPREADSHEET_NAME)
            try:
                sh.share(SHARE_EMAIL, perm_type="user", role="writer")
            except Exception:
                pass
        except Exception as e:
            # Try to get email for quota error message
            try:
                if "gcp_service_account" in st.secrets:
                    sa_email = st.secrets["gcp_service_account"].get("client_email", "the service account")
                else:
                    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
                    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
                    sa_email = getattr(creds, "service_account_email", "the service account")
            except Exception:
                sa_email = "the service account"

            if "quota" in str(e).lower():
                return False, (
                    f"Drive quota exceeded. Please manually create a Google Sheet "
                    f"named **{SPREADSHEET_NAME}**, share it with **{sa_email}** "
                    f"(Editor), and refresh."
                )
            return False, f"Failed to create sheet: {e}"

    global _spreadsheet
    _spreadsheet = sh

    _ensure_worksheet(sh, WS_INVENTORY, INVENTORY_HEADERS)
    _ensure_worksheet(sh, WS_LEDGER, LEDGER_HEADERS)
    _ensure_worksheet(sh, WS_REQUESTS, REQUESTS_HEADERS)
    _ensure_worksheet(sh, WS_USERS, USERS_HEADERS)
    _ensure_worksheet(sh, WS_VENDORS, VENDOR_HEADERS)
    _ensure_worksheet(sh, WS_PO_TRACK, PO_HEADERS)

    return True, "Database ready."


# ── ID Generator ────────────────────────────────
def generate_id(length=6):
    """Generate a random customized uppercase alphanumeric ID."""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))


# ── Generic helpers ─────────────────────────────
def _ws(name):
    """Get a worksheet handle."""
    sh = _get_spreadsheet()
    return sh.worksheet(name)


def _all_records(name):
    """Return all records from a worksheet as a DataFrame."""
    try:
        ws = _ws(name)
        data = ws.get_all_records()
        df = pd.DataFrame(data) if data else pd.DataFrame(columns=ws.row_values(1))
        
        # Force string types on identifiers to prevent numeric inference bugs
        str_cols = ["Item_ID", "Unique_Name", "Material_Name", "Request_ID", "Reference_ID", "UserID", "CAS_No"]
        for c in str_cols:
            if c in df.columns:
                df[c] = df[c].astype(str)
                
        return df
    except Exception as e:
        print(f"[db] Error reading {name}: {e}")
        return pd.DataFrame()


def _append(name, row_dict):
    """Append one row dict to a worksheet."""
    ws = _ws(name)
    headers = ws.row_values(1)
    row = [str(row_dict.get(h, "")) for h in headers]
    ws.append_row(row, value_input_option="USER_ENTERED")


def _update_cell_by_id(name, id_col, id_val, updates: dict):
    """Update one or more columns in the row matched by id_col == id_val."""
    ws = _ws(name)
    records = ws.get_all_records()
    headers = ws.row_values(1)
    for i, rec in enumerate(records):
        if str(rec.get(id_col)) == str(id_val):
            row_idx = i + 2  # +1 header, +1 zero-index
            for col_name, new_val in updates.items():
                if col_name in headers:
                    col_idx = headers.index(col_name) + 1
                    ws.update_cell(row_idx, col_idx, str(new_val))
            return True
    return False


# ── Suppliers ───────────────────────────────────
def get_vendors():
    return _all_records(WS_VENDORS)


def add_vendor(company_name, contact, email, notes):
    _append(WS_VENDORS, {
        "Vendor_ID": generate_id(6),
        "Company_Name": company_name,
        "Contact_Number": contact,
        "Email": email,
        "Notes": notes,
    })


def delete_vendor(vendor_id):
    ws = _ws(WS_VENDORS)
    try:
        records = ws.get_all_records()
        for idx, row in enumerate(records):
            if str(row.get("Vendor_ID")) == str(vendor_id):
                ws.delete_rows(idx + 2)
                return True, "Vendor deleted."
    except Exception as e:
         pass
    return False, "Vendor not found."


# ── Inventory Master ───────────────────────────
def get_all_items():
    df = _all_records(WS_INVENTORY)
    if not df.empty and "Unique_Name" in df.columns:
        df = df.sort_values(by="Unique_Name", key=lambda col: col.astype(str).str.lower()).reset_index(drop=True)
    return df


def add_item(unique_name, material_name, cas_no, grade, manufacturer, units,
             opening_stock=0.0, min_stock=5.0, material_type="", pack_size="", updated_by="system"):
    """Add item to Inventory_Master and create an OPENING ledger entry."""
    item_id = generate_id(6)
    _append(WS_INVENTORY, {
        "Item_ID": item_id,
        "Unique_Name": unique_name,
        "Material_Name": material_name,
        "CAS_No": cas_no,
        "Grade_Purity": grade,
        "Manufacturer": manufacturer,
        "Units": units,
        "Min_Stock": min_stock,
        "Material_Type": material_type,
        "Pack_Size": pack_size,
    })
    if opening_stock > 0:
        add_ledger_entry(item_id, "OPENING", opening_stock, updated_by=updated_by)
    return item_id


def update_item(item_id, updates: dict):
    """Update fields on an existing inventory item."""
    return _update_cell_by_id(WS_INVENTORY, "Item_ID", item_id, updates)


# ── Stock Ledger ───────────────────────────────
def get_ledger(item_id=None):
    df = _all_records(WS_LEDGER)
    if df.empty:
        return df
    if item_id:
        df = df[df["Item_ID"] == item_id]
    return df


def add_ledger_entry(item_id, txn_type, quantity, reference_id="", updated_by="system"):
    """Insert a single ledger transaction row."""
    _append(WS_LEDGER, {
        "Transaction_ID": generate_id(6),
        "Item_ID": item_id,
        "DateTime": get_ist_now().strftime("%Y-%m-%d %H:%M:%S"),
        "Transaction_Type": txn_type,
        "Quantity": quantity,
        "Reference_ID": reference_id,
        "Updated_By": updated_by,
    })


def compute_stock(item_id=None):
    """
    CORE FUNCTION — dynamically compute available stock from the ledger.
    Returns a DataFrame with columns [Item_ID, Available_Stock].
    If item_id is given, returns a single float.
    """
    df = _all_records(WS_LEDGER)
    if df.empty:
        if item_id:
            return 0.0
        return pd.DataFrame(columns=["Item_ID", "Available_Stock"])

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
    stock = df.groupby("Item_ID")["Quantity"].sum().reset_index()
    stock["Quantity"] = stock["Quantity"].round(2)
    stock.columns = ["Item_ID", "Available_Stock"]

    if item_id:
        row = stock[stock["Item_ID"] == str(item_id)]
        return round(float(row["Available_Stock"].iloc[0]), 2) if not row.empty else 0.0
    return stock


# ── Requests ───────────────────────────────────
def get_requests(status=None, requested_by=None):
    df = _all_records(WS_REQUESTS)
    if df.empty:
        return df
    if status:
        df = df[df["Status"] == status]
    if requested_by:
        df = df[df["Requested_By"] == requested_by]
    return df


def submit_request(item_id, requested_by, department, quantity):
    """Submit a new material request after validating stock."""
    available = compute_stock(item_id)
    if quantity > available:
        return False, f"Insufficient stock. Available: {available}"
    if quantity <= 0:
        return False, "Quantity must be positive."

    req_id = generate_id(6)
    _append(WS_REQUESTS, {
        "Request_ID": req_id,
        "Item_ID": item_id,
        "Requested_By": requested_by,
        "Department": department,
        "Quantity": quantity,
        "Status": "PENDING",
        "Timestamp": get_ist_now().strftime("%Y-%m-%d %H:%M:%S"),
        "Approved_By": "",
        "Approval_Time": "",
        "Remarks": "",
    })
    return True, f"Request {req_id} submitted."


def approve_request(request_id, approved_by, remarks=""):
    """
    Approve a request:
      1. Re-validate stock
      2. Insert ISSUED ledger entry (negative qty)
      3. Update request status
    """
    requests_df = get_requests()
    if requests_df.empty:
        return False, "No requests found."

    row = requests_df[requests_df["Request_ID"] == request_id]
    if row.empty:
        return False, "Request not found."
    row = row.iloc[0]

    if row["Status"] != "PENDING":
        return False, f"Request is already {row['Status']}."

    item_id = str(row["Item_ID"])
    qty = float(row["Quantity"])

    # Re-validate stock at approval time (concurrency safety)
    available = compute_stock(item_id)
    if qty > available:
        return False, f"Insufficient stock to approve. Available: {available}"

    # Insert ISSUED ledger entry
    add_ledger_entry(item_id, "ISSUED", -qty,
                     reference_id=request_id, updated_by=approved_by)

    # Update request
    now = get_ist_now().strftime("%Y-%m-%d %H:%M:%S")
    _update_cell_by_id(WS_REQUESTS, "Request_ID", request_id, {
        "Status": "APPROVED",
        "Approved_By": approved_by,
        "Approval_Time": now,
        "Remarks": remarks,
    })
    return True, "Request approved and stock deducted."


def reject_request(request_id, rejected_by, remarks=""):
    """Reject a pending request."""
    now = get_ist_now().strftime("%Y-%m-%d %H:%M:%S")
    ok = _update_cell_by_id(WS_REQUESTS, "Request_ID", request_id, {
        "Status": "REJECTED",
        "Approved_By": rejected_by,
        "Approval_Time": now,
        "Remarks": remarks,
    })
    return ok, "Request rejected." if ok else "Request not found."


# ── Users ──────────────────────────────────────
def get_users():
    return _all_records(WS_USERS)


def get_user(email):
    df = get_users()
    if df.empty:
        return None
    match = df[df["Email"] == email]
    return match.iloc[0] if not match.empty else None


def add_user(email, password_hash, role, department=""):
    _append(WS_USERS, {
        "UserID": generate_id(6),
        "Email": email,
        "Password_Hash": password_hash,
        "Role": role,
        "Department": department,
    })


def update_password(email, new_hash):
    """Update password hash for existing user."""
    return _update_cell_by_id(WS_USERS, "Email", email, {"Password_Hash": new_hash})


def delete_user(user_id):
    """Delete a user from the database."""
    ws = _ws(WS_USERS)
    try:
        records = ws.get_all_records()
        for idx, row in enumerate(records):
            if str(row.get("UserID")) == str(user_id):
                ws.delete_rows(idx + 2)  # +1 header, +1 zero-index
                return True, "User deleted."
    except Exception as e:
         return False, f"Error deleting user: {e}"
    return False, "User not found."


# ── PO Tracking ────────────────────────────────
def get_po_track():
    """Return all PO tracking records as a DataFrame."""
    return _all_records(WS_PO_TRACK)


def save_po_track(df):
    """Overwrite the PO tracking worksheet with the given DataFrame."""
    try:
        sh = _get_spreadsheet()
        if not sh:
            return False, "Could not connect to Google Sheets."
            
        # Ensure worksheet exists before saving
        from config import PO_HEADERS
        ws = _ensure_worksheet(sh, WS_PO_TRACK, PO_HEADERS)
        
        # Clear existing data
        ws.clear()
        
        # Prepare data: convert everything to string and handle NaN/NaT/None
        # because JSON serialiser (used by gspread) crashes on 'nan' floats.
        data_df = df.copy()
        
        # 1. Format dates specifically
        date_cols = [c for c in data_df.columns if pd.api.types.is_datetime64_any_dtype(data_df[c])]
        for col in date_cols:
            data_df[col] = data_df[col].dt.strftime('%Y-%m-%d')

        # 2. Fill all Nulls with empty string and convert whole DF to string
        data_df = data_df.fillna("")
        
        # 3. Create the row list and do a final safety pass on every cell
        headers = data_df.columns.tolist()
        body = data_df.values.tolist()
        
        cleaned_data = [headers]
        for row in body:
            clean_row = []
            for val in row:
                # Catch any remaining nan/NaT/None objects or strings
                s_val = str(val)
                if s_val.lower() in ["nan", "nat", "none", "<na>"]:
                    clean_row.append("")
                else:
                    clean_row.append(s_val)
            cleaned_data.append(clean_row)
        
        # Standard gspread update requires a range or a named parameter 'values'
        ws.update("A1", cleaned_data)
        return True, "PO Tracking data saved successfully."
    except Exception as e:
        return False, f"Error saving PO data: {e}"
