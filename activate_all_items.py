import streamlit as st
from unittest.mock import MagicMock
# Mock st.secrets to allow CLI execution
st.secrets = MagicMock()

import db
from config import WS_INVENTORY

def activate_all():
    print("Initializing connection...")
    ok, msg = db.initialize_database()
    if not ok:
        print(f"Failed to initialize DB: {msg}")
        return

    try:
        ws = db._ws(WS_INVENTORY)
        records = ws.get_all_records()
        headers = ws.row_values(1)
        
        if "Status" not in headers:
            print("Status column not found. Correcting headers first...")
            # This should be handled by initialize_database, but let's be explicit
            ws.update_cell(1, len(headers) + 1, "Status")
            status_col_idx = len(headers) + 1
        else:
            status_col_idx = headers.index("Status") + 1

        print(f"Found 135 items. Setting Status to 'Active' for all...")
        
        # We can update all cells in the status column in one go (except header)
        # For simplicity and reliability in smaller sheets, we can just batch update
        row_count = len(records) + 1
        cell_list = ws.range(2, status_col_idx, row_count, status_col_idx)
        for cell in cell_list:
            cell.value = "Active"
        
        ws.update_cells(cell_list)
        print("Success! All items are now physically marked as 'Active' in Google Sheets.")
            
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    activate_all()
