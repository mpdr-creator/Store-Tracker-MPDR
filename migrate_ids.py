import db
import string
import random

def gen_id():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

def migrate():
    print("Fetching data...")
    ws_inv = db._ws(db.WS_INVENTORY)
    inv_data = ws_inv.get_all_values()
    
    ws_ledger = db._ws(db.WS_LEDGER)
    ledger_data = ws_ledger.get_all_values()
    
    ws_req = db._ws(db.WS_REQUESTS)
    req_data = ws_req.get_all_values()
    
    ws_users = db._ws(db.WS_USERS)
    users_data = ws_users.get_all_values()
    
    item_map = {}
    
    print("Processing Inventory...")
    if inv_data and len(inv_data) > 1:
        item_id_idx = inv_data[0].index("Item_ID") if "Item_ID" in inv_data[0] else None
        if item_id_idx is not None:
            for i in range(1, len(inv_data)):
                old_id = str(inv_data[i][item_id_idx])
                # Only map if it doesn't look like a new ID already
                # New IDs are exactly 6 uppercase + digits. Old are 8 chars lowercase + digits.
                if len(old_id) == 8 or old_id.islower():
                    new_id = gen_id()
                    item_map[old_id] = new_id
                    inv_data[i][item_id_idx] = new_id
                else:
                    item_map[old_id] = old_id

    print("Processing Ledger...")
    if ledger_data and len(ledger_data) > 1:
        txn_id_idx = ledger_data[0].index("Transaction_ID") if "Transaction_ID" in ledger_data[0] else None
        l_item_id_idx = ledger_data[0].index("Item_ID") if "Item_ID" in ledger_data[0] else None
        for i in range(1, len(ledger_data)):
            if txn_id_idx is not None:
                old_txn = str(ledger_data[i][txn_id_idx])
                if len(old_txn) == 8 or old_txn.islower():
                    ledger_data[i][txn_id_idx] = gen_id()
            if l_item_id_idx is not None:
                old_id = str(ledger_data[i][l_item_id_idx])
                if old_id in item_map:
                    ledger_data[i][l_item_id_idx] = item_map[old_id]

    print("Processing Requests...")
    if req_data and len(req_data) > 1:
        req_id_idx = req_data[0].index("Request_ID") if "Request_ID" in req_data[0] else None
        r_item_id_idx = req_data[0].index("Item_ID") if "Item_ID" in req_data[0] else None
        for i in range(1, len(req_data)):
            if req_id_idx is not None:
                old_req = str(req_data[i][req_id_idx])
                if len(old_req) == 8 or old_req.islower():
                    req_data[i][req_id_idx] = gen_id()
            if r_item_id_idx is not None:
                old_id = str(req_data[i][r_item_id_idx])
                if old_id in item_map:
                    req_data[i][r_item_id_idx] = item_map[old_id]

    print("Processing Users...")
    if users_data and len(users_data) > 1:
        user_id_idx = users_data[0].index("UserID") if "UserID" in users_data[0] else None
        for i in range(1, len(users_data)):
            if user_id_idx is not None:
                old_usr = str(users_data[i][user_id_idx])
                if len(old_usr) == 8 or old_usr.islower():
                    users_data[i][user_id_idx] = gen_id()

    print("Uploading to Google Sheets...")
    
    if inv_data:
        ws_inv.clear()
        ws_inv.update(inv_data)
        print(" -> Inventory Master uploaded")
        
    if ledger_data:
        ws_ledger.clear()
        ws_ledger.update(ledger_data)
        print(" -> Stock Ledger uploaded")
        
    if req_data:
        ws_req.clear()
        ws_req.update(req_data)
        print(" -> Requests uploaded")
        
    if users_data:
        ws_users.clear()
        ws_users.update(users_data)
        print(" -> Users uploaded")

    print("\n✅ Migration complete!")

if __name__ == "__main__":
    _, msg = db.initialize_database()
    if msg == "Database ready.":
        migrate()
    else:
        print("Error initializing DB:", msg)
