# ──────────────────────────────────────────────
# Store Tracker — Configuration
# ──────────────────────────────────────────────

SPREADSHEET_NAME = "Store Tracker DB"
SHARE_EMAIL = "mpdr.services@gmail.com"
LOGO_FILENAME = "logo-2.png"

# Google API Scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Worksheet names
WS_INVENTORY = "Inventory_Master"
WS_LEDGER = "Stock_Ledger"
WS_REQUESTS = "Requests"
WS_USERS = "Users"
WS_VENDORS = "Suppliers"

# Inventory_Master headers
INVENTORY_HEADERS = [
    "Item_ID", "Unique_Name", "Material_Name",
    "CAS_No", "Grade_Purity", "Manufacturer", "Units", "Min_Stock", "Material_Type", "Pack_Size", "Status",
]

# Suppliers headers
VENDOR_HEADERS = [
    "Vendor_ID", "Company_Name", "Contact_Number", "Email", "Notes"
]

# Stock_Ledger headers
LEDGER_HEADERS = [
    "Transaction_ID", "Item_ID", "DateTime",
    "Transaction_Type", "Quantity", "Reference_ID", "Updated_By",
]

# Requests headers
REQUESTS_HEADERS = [
    "Request_ID", "Item_ID", "Requested_By", "Department",
    "Quantity", "Status", "Timestamp", "Approved_By", "Approval_Time", "Remarks",
]

# Users headers
USERS_HEADERS = [
    "UserID", "Email", "Password_Hash", "Role", "Department",
]

# Valid values
DEPARTMENTS = ["API", "CDMO", "MedChem", "AR&D", "SSD"]
ROLES = ["Admin", "Scientist", "Management"]
TRANSACTION_TYPES = ["OPENING", "RECEIVED", "ISSUED", "ADJUSTMENT"]
REQUEST_STATUSES = ["PENDING", "APPROVED", "REJECTED"]

# Categories for display grouping
CATEGORIES = ["Chemical", "Solvents", "Reagents", "Raw Materials",
              "Buffers", "Media", "Lab Supplies", "Stationery"]

# PO Tracking
WS_PO_TRACK = "PO_Tracking"
PO_HEADERS = [
    "S.No", "PO Date", "PO Number", "PR Number", "PR creator", "Depart", 
    "Material Name", "CAS number", "Manifacturer", "Supplier", "Ordered Qty(G)", 
    "Unit", "Days to deliver", "Expected Delivery", "Follow-up Date", "Status", 
    "Recived date", "Remark/Note"
]
PO_UNITS = ["KG", "GM", "MG", "Ltr", "ML", "Units", "Box", "Number's", "Packets", "others"]
