# ──────────────────────────────────────────────
# Store Tracker — Main Streamlit Application
# ──────────────────────────────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import os

# Resolve logo paths
from config import LOGO_FILENAME, FAVICON_FILENAME
base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, LOGO_FILENAME)
favicon_path = os.path.join(base_dir, FAVICON_FILENAME)

st.set_page_config(
    page_title="Store Tracker",
    page_icon=favicon_path if os.path.exists(favicon_path) else logo_path,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS (Minimalist Medical Theme) ───────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Inter:wght@400;500;600&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff;
    }

    /* Headers - Crisp & Professional */
    h1, h2, h3, h4, h5, h6 { 
        font-family: 'Montserrat', sans-serif !important;
        color: #1e293b !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 1rem !important;
    }

    /* Sidebar - Clean & Muted */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] * { color: #475569 !important; }

    /* Custom Navigation Buttons - Vector Icon Injection */
    .stSidebar [data-testid="stVerticalBlock"] > div:has(button) {
        margin-bottom: -15px;
    }
    .stSidebar button[kind="secondary"] {
        width: 100% !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        text-align: left !important;
        padding: 10px 18px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
        border-radius: 10px !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stSidebar button[kind="secondary"]:hover {
        background: #f1f5f9 !important;
        color: #10b981 !important;
        transform: translateX(4px);
    }
    
    /* Vector Icon Styling - Deep Dark Slate */
    .stSidebar button[kind="secondary"]::before {
        font-family: "Font Awesome 6 Free" !important;
        font-weight: 900 !important;
        margin-right: 12px !important;
        font-size: 1.1rem !important;
        width: 24px !important;
        text-align: center !important;
        display: inline-block !important;
        color: #1e293b !important; /* Dark Coloured Icons */
        flex-shrink: 0 !important;
    }

    /* Page-Specific Dark Icons */
    .stSidebar button:has(div:contains("Dashboard"))::before { content: "\f201"; }
    .stSidebar button:has(div:contains("Inventory"))::before { content: "\f466"; }
    .stSidebar button:has(div:contains("Add Stock"))::before { content: "\f055"; }
    .stSidebar button:has(div:contains("Requests"))::before { content: "\f46d"; }
    .stSidebar button:has(div:contains("Ledger"))::before { content: "\f02d"; }
    .stSidebar button:has(div:contains("Manage Users"))::before { content: "\f502"; }
    .stSidebar button:has(div:contains("Suppliers"))::before { content: "\f48b"; }
    .stSidebar button:has(div:contains("Stock Viewer"))::before { content: "\f06e"; }
    .stSidebar button:has(div:contains("Submit Request"))::before { content: "\f1d8"; }
    .stSidebar button:has(div:contains("My Requests"))::before { content: "\f0ae"; }
    .stSidebar button:has(div:contains("Analytics"))::before { content: "\f200"; }
    .stSidebar button:has(div:contains("PO Track"))::before { content: "\f570"; }
    .stSidebar button:has(div:contains("Logout"))::before { content: "\f2f5"; }


    /* Active Navigation State */
    .active-nav button {
        background: #f0fdf4 !important;
        color: #10b981 !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 0 10px 10px 0 !important;
        font-weight: 700 !important;
    }


    /* Metrics - Minimal Floating Cards */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: #10b981;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    [data-testid="stMetric"] label { 
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important; 
        color: #64748b !important; 
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }

    /* Buttons - Medical Emerald Primary */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        background-color: #ffffff;
        color: #475569;
        border: 1px solid #e2e8f0;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        border-color: #10b981;
        color: #10b981;
        background-color: #f0fdf4;
    }
    
    /* Primary buttons */
    div.stButton > button:first-child[kind="primary"] {
        background-color: #10b981;
        color: white;
        border: none;
    }
    div.stButton > button:first-child[kind="primary"]:hover {
        background-color: #059669;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }

    /* Data frames - Clean Sharp Container */
    .stDataFrame { 
        border-radius: 12px; 
        border: 1px solid #e2e8f0; 
        background: #ffffff;
        padding: 5px;
    }

    /* Custom Slim Sidebar Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    /* Form containers - Minimal */
    [data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* Tab styles - Minimal Underline */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: transparent;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        color: #10b981 !important;
        border-bottom-color: #10b981 !important;
        font-weight: 700 !important;
    }

    /* Info/Alert boxes - Subtle Medical Callouts */
    .stAlert {
        border-radius: 10px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #10b981;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Aesthetic Helper: Modern Status Colors ──────
STATUS_PALETTE = {
    "danger": {"bg": "#fef2f2", "text": "#991b1b"},
    "warning": {"bg": "#fffbeb", "text": "#92400e"},
    "success": {"bg": "#f0fdfa", "text": "#0f766e"},
    "info": {"bg": "#f0f9ff", "text": "#075985"}
}

def format_2_decimals(val):
    try:
        if val == "" or pd.isna(val):
            return val
        return f"{float(val):.2f}"
    except (ValueError, TypeError):
        return val

def _get_plotly_layout(title):
    """Consistent Modern Layout for Plotly Charts."""
    return dict(
        title=dict(text=title, font=dict(family="Montserrat, sans-serif", size=18, color="#111827")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#6b7280"),
        margin=dict(t=50, b=50, l=50, r=30),
        xaxis=dict(gridcolor="#f3f4f6", zerolinecolor="#e5e7eb"),
        yaxis=dict(gridcolor="#f3f4f6", zerolinecolor="#e5e7eb"),
    )

def _display_store_timings():
    """Display the store timings notice in a green medical-themed caution box."""
    st.markdown(f"""
    <div style="background-color: {STATUS_PALETTE['success']['bg']}; 
                color: {STATUS_PALETTE['success']['text']}; 
                padding: 16px; 
                border-radius: 10px; 
                border: 1px solid #10b981; 
                border-left: 5px solid #10b981;
                margin-bottom: 20px;
                font-family: 'Inter', sans-serif;">
        <span style="font-size: 1.2rem; margin-right: 8px;">⚠️</span>
        <b style="font-family: 'Montserrat', sans-serif;">Our store timings are 10:00–11:00 AM, 2:00–3:00 PM, and 5:00–6:00 PM.</b><br>
        <div style="margin-left: 28px; margin-top: 4px; font-size: 0.9rem; opacity: 0.9;">
            In case of any urgent requirement or emergency, please feel free to contact us at any time.<br>
            <i>Thank you for your understanding.</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Imports (after st.set_page_config) ──────────
import db
import auth
from config import DEPARTMENTS, ROLES, TRANSACTION_TYPES, PO_HEADERS, PO_UNITS

# ── Database init ───────────────────────────────
if "db_ready" not in st.session_state:
    # Check absolute location for credentials.json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(base_dir, "credentials.json")
    
    creds_exist = os.path.exists(creds_path)
    secrets_exist = "gcp_service_account" in st.secrets
    
    if not creds_exist and not secrets_exist:
        st.error("❌ **Credentials missing.** Please provide `credentials.json` in the app folder.")
        st.info(f"Searched at: `{creds_path}`")
        st.stop()
        
    ok, msg = db.initialize_database()
    if not ok:
        st.error("⚠️ **Database Initialization Failed**")
        st.markdown(msg)
        st.stop()
    st.session_state["db_ready"] = True

# ── Auth gate ───────────────────────────────────
auth.require_login()

# ── Sidebar ─────────────────────────────────────
role = auth.current_role()
email = auth.current_user()

# Sidebar Logo Integration
if os.path.exists(logo_path):
    # Centered logo with controlled width
    logo_l, logo_m, logo_r = st.sidebar.columns([1, 4, 1])
    with logo_m:
        st.image(logo_path, use_container_width=True)
    st.sidebar.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True) 
else:
    st.sidebar.title("📦 Store Tracker")

st.sidebar.markdown(f"""
<div style="background: white; padding: 16px; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 10px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
        <div style="background: #f1f5f9; padding: 8px; border-radius: 50%; font-size: 1rem;">👤</div>
        <div style="font-size: 0.85rem; font-weight: 700; color: #1e293b; word-break: break-all; font-family: 'Inter', sans-serif;">{email}</div>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <span style="background: #10b981; color: white; padding: 2px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; font-family: 'Montserrat', sans-serif;">
            {role}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()

# Role-specific navigation with icons (No Emojis)
if "page" not in st.session_state:
    st.session_state.page = "Dashboard" if role != "Scientist" else "Stock Viewer"

nav_items = []
if role == "Admin":
    nav_items = [
        ("Dashboard", "fa-solid fa-chart-line"),
        ("Inventory", "fa-solid fa-boxes-stacked"),
        ("Add Stock", "fa-solid fa-plus-circle"),
        ("Requests", "fa-solid fa-clipboard-check"),
        ("Ledger", "fa-solid fa-book"),
        ("PO Track", "fa-solid fa-file-invoice"),
        ("Manage Users", "fa-solid fa-users-gear"),
        ("Suppliers / Vendors", "fa-solid fa-truck-field")
    ]
elif role == "Scientist":
    nav_items = [
        ("Stock Viewer", "fa-solid fa-eye"),
        ("Submit Request", "fa-solid fa-paper-plane"),
        ("My Requests", "fa-solid fa-list-check")
    ]
elif role == "Management":
    nav_items = [
        ("Analytics Dashboard", "fa-solid fa-chart-pie"),
        ("Suppliers / Vendors", "fa-solid fa-truck-field")
    ]

# Custom Styled Navigation Menu
for label, icon in nav_items:
    is_active = st.session_state.page == label
    active_class = "active-nav" if is_active else ""
    
    with st.sidebar.container():
        st.markdown(f'<div class="{active_class}">', unsafe_allow_html=True)
        # Icons are now injected via CSS using the label as a selector
        if st.button(label, key=f"nav_{label}", use_container_width=True):
            st.session_state.page = label
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


page = st.session_state.page
st.sidebar.divider()
if st.sidebar.button("🚪 Logout", use_container_width=True):
    auth.logout()



# ════════════════════════════════════════════════
#  HELPER: Build inventory + stock merged table
# ════════════════════════════════════════════════
@st.cache_data(ttl=30)
def _load_inventory_with_stock():
    """Merge Inventory_Master with computed stock from ledger."""
    items = db.get_all_items()
    if items.empty:
        return items
    stock = db.compute_stock()
    if isinstance(stock, float):
        return items
    merged = items.merge(stock, on="Item_ID", how="left")
    merged["Available_Stock"] = pd.to_numeric(merged["Available_Stock"], errors="coerce").fillna(0)
    return merged


# ════════════════════════════════════════════════
#  ADMIN PAGES
# ════════════════════════════════════════════════

def admin_dashboard():
    st.title("📊 Admin Dashboard")

    inv = _load_inventory_with_stock()
    requests_df = db.get_requests()

    tab_kpi, tab_logbook = st.tabs(["KPI & Status", "Daily Logbook (Template View)"])

    with tab_kpi:
        # KPI row
        c1, c2, c3, c4 = st.columns(4)
        total = len(inv) if not inv.empty else 0
        low = 0
        out = 0
        if not inv.empty:
            min_stocks = pd.to_numeric(inv.get("Min_Stock", 5.0), errors="coerce").fillna(5.0)
            low = int((inv["Available_Stock"] <= min_stocks).sum())
            out = int((inv["Available_Stock"] <= 0).sum())
        pending = len(requests_df[requests_df["Status"] == "PENDING"]) if not requests_df.empty else 0

        c1.metric("Total Items", total)
        c2.metric("Low Stock (≤Threshold)", low)
        c3.metric("Out of Stock", out)
        c4.metric("Pending Requests", pending)

        st.divider()

        # Inventory table
        st.subheader("📋 Full Inventory")
        if not inv.empty:
            display_cols = ["Item_ID", "Unique_Name", "Material_Name", "CAS_No", "Grade_Purity", 
                            "Pack_Size", "Min_Stock", "Status", "Manufacturer", "Units", "Available_Stock"]
            display_df = inv[[c for c in display_cols if c in inv.columns]].copy()
            display_df.insert(0, "S.No", range(1, len(display_df) + 1))

            # Color-code stock row-wise
            def highlight_row(row):
                styles = [''] * len(row)
                if "Available_Stock" in row.index:
                    try:
                        avail = float(row["Available_Stock"])
                        min_val = row.get("Min_Stock", 5.0)
                        try:
                            min_stk = float(min_val)
                        except (ValueError, TypeError):
                            min_stk = 5.0
                        idx = row.index.get_loc("Available_Stock")
                        if avail <= 0:
                            styles[idx] = f"background-color: {STATUS_PALETTE['danger']['bg']}; color: {STATUS_PALETTE['danger']['text']}; border-left: 4px solid {STATUS_PALETTE['danger']['text']}; font-weight: 700;"
                        elif avail <= min_stk:
                            styles[idx] = f"background-color: {STATUS_PALETTE['warning']['bg']}; color: {STATUS_PALETTE['warning']['text']}; border-left: 4px solid {STATUS_PALETTE['warning']['text']}; font-weight: 700;"
                        else:
                            styles[idx] = f"background-color: {STATUS_PALETTE['success']['bg']}; color: {STATUS_PALETTE['success']['text']}; border-left: 4px solid {STATUS_PALETTE['success']['text']}; font-weight: 700;"

                    except Exception:
                        pass
                return styles


            styled = display_df.style.format({
                "Available_Stock": format_2_decimals,
                "Min_Stock": format_2_decimals,
                "Pack_Size": format_2_decimals
            }).apply(highlight_row, axis=1)
            st.dataframe(styled, use_container_width=True, height=500, hide_index=True)
        else:
            st.info("No items in inventory yet. Use **Inventory** page to add items.")

    with tab_logbook:
        st.subheader("Template Daily Format")
        target_date = st.date_input("Select Date", value=pd.Timestamp.today().date())
        
        if inv.empty:
            st.warning("No inventory data.")
        else:
            ledger = db.get_ledger()
            
            # Ledger agg
            opening_stock = pd.DataFrame(columns=["Item_ID", "Opening Stock"])
            rcv_agg = pd.DataFrame(columns=["Item_ID", "Received Qty"])
            wst_agg = pd.DataFrame(columns=["Item_ID", "Total Wastage Quantity (day wise)"])

            if not ledger.empty:
                ledger["DateTime"] = pd.to_datetime(ledger["DateTime"], errors='coerce')
                ledger["Quantity"] = pd.to_numeric(ledger["Quantity"], errors='coerce').fillna(0)
                
                before_mask = ledger["DateTime"].dt.date < target_date
                if before_mask.any():
                    opening_stock = ledger[before_mask].groupby("Item_ID")["Quantity"].sum().reset_index()
                    opening_stock.rename(columns={"Quantity": "Opening Stock"}, inplace=True)
                
                on_mask = ledger["DateTime"].dt.date == target_date
                ledger_on = ledger[on_mask]
                
                r_mask = ledger_on["Transaction_Type"] == "RECEIVED"
                if r_mask.any():
                    rcv_agg = ledger_on[r_mask].groupby("Item_ID")["Quantity"].sum().reset_index()
                    rcv_agg.rename(columns={"Quantity": "Received Qty"}, inplace=True)
                
                w_mask = ledger_on["Transaction_Type"] == "WASTAGE"
                if w_mask.any():
                    wst_agg = ledger_on[w_mask].groupby("Item_ID")["Quantity"].sum().reset_index()
                    wst_agg["Quantity"] = wst_agg["Quantity"].abs()
                    wst_agg.rename(columns={"Quantity": "Total Wastage Quantity (day wise)"}, inplace=True)

            req_agg = pd.DataFrame(columns=["Item_ID", "Requested Dept", "Requested Person", "Material Quantity", "Approved / issued by", "Remark/Note"])
            if not requests_df.empty:
                requests_df["Approval_Time"] = pd.to_datetime(requests_df["Approval_Time"], errors='coerce')
                req_on = requests_df[(requests_df["Approval_Time"].dt.date == target_date) & (requests_df["Status"] == "APPROVED")]
                if not req_on.empty:
                    req_on["Quantity"] = pd.to_numeric(req_on["Quantity"], errors='coerce').fillna(0)
                    req_agg = req_on.groupby("Item_ID").agg({
                        "Department": lambda x: ", ".join(x.dropna().astype(str).unique()),
                        "Requested_By": lambda x: ", ".join(x.dropna().astype(str).unique()),
                        "Quantity": "sum",
                        "Approved_By": lambda x: ", ".join(x.dropna().astype(str).unique()),
                        "Remarks": lambda x: " | ".join(x.dropna().astype(str).unique()),
                    }).reset_index()
                    req_agg.rename(columns={
                        "Department": "Requested Dept",
                        "Requested_By": "Requested Person",
                        "Quantity": "Material Quantity",
                        "Approved_By": "Approved / issued by",
                        "Remarks": "Remark/Note"
                    }, inplace=True)

            # Merge everything
            df_template = inv.copy()
            for agg_df in [opening_stock, rcv_agg, wst_agg, req_agg]:
                if not agg_df.empty:
                    df_template = df_template.merge(agg_df, on="Item_ID", how="left")

            for col in ["Opening Stock", "Received Qty", "Total Wastage Quantity (day wise)", "Material Quantity"]:
                if col not in df_template: df_template[col] = 0
                df_template[col] = df_template[col].fillna(0)

            df_template["Date"] = target_date.strftime("%Y-%m-%d")
            df_template["S.No"] = range(1, len(df_template) + 1)
            df_template["Available quantity/ stock"] = df_template["Opening Stock"] + df_template["Received Qty"]
            df_template["Remaining Stock/Quantity"] = df_template["Available quantity/ stock"] - df_template["Material Quantity"]
            df_template["Remaining Stock"] = df_template["Remaining Stock/Quantity"] - df_template["Total Wastage Quantity (day wise)"]
            df_template["Total consumed quantity (day wise)"] = df_template["Material Quantity"]
            
            df_template["Material Name.1"] = df_template.get("Material_Name", "")
            df_template["CAS no"] = df_template.get("CAS_No", "")
            df_template["manufacturer"] = df_template.get("Manufacturer", "")
            df_template["Updated by"] = df_template.get("Approved / issued by", "")

            rename_map = {
                "Unique_Name": "Unique Name", "Material_Type": "Material Type",
                "Material_Name": "Material Name", "Grade_Purity": "Grade/Purity",
                "CAS_No": "CAS No"
            }
            df_template.rename(columns=rename_map, inplace=True)

            final_columns = [
                'S.No', 'Date', 'Unique Name', 'Material Type', 'Material Name', 
                'Grade/Purity', 'CAS No', 'Manufacturer', 'Units', 
                'Opening Stock', 'Received Qty', 'Available quantity/ stock', 
                'Requested Dept', 'Requested Person', 'Material Name.1', 'CAS no', 
                'manufacturer', 'Material Quantity', 'Approved / issued by', 
                'Remaining Stock/Quantity', 'Total consumed quantity (day wise)', 
                'Total Wastage Quantity (day wise)', 'Remaining Stock', 'Updated by', 'Remark/Note'
            ]
            
            for c in final_columns:
                if c not in df_template.columns: df_template[c] = ""
                    
            df_final = df_template[final_columns].copy()
            format_cols = [
                'Opening Stock', 'Received Qty', 'Available quantity/ stock', 'Material Quantity',
                'Remaining Stock/Quantity', 'Total consumed quantity (day wise)', 
                'Total Wastage Quantity (day wise)', 'Remaining Stock'
            ]
            format_dict = {col: format_2_decimals for col in format_cols if col in df_final.columns}
            st.dataframe(df_final.style.format(format_dict), use_container_width=True, height=500, hide_index=True)
            
            csv = df_final.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Logbook (CSV Format)", data=csv, file_name=f"Daily_Logbook_{target_date}.csv", mime="text/csv")


def admin_inventory():
    st.title("🏗️ Inventory Management")

    tab_view, tab_add, tab_edit = st.tabs(["View Inventory", "Add New Item", "Edit Item"])

    with tab_view:
        inv = _load_inventory_with_stock()
        if not inv.empty:
            search = st.text_input("🔍 Search by name, CAS, or manufacturer", key="inv_search")
            if search:
                search = search.lower().strip()
                mask = (
                    inv["Unique_Name"].str.contains(search, case=False, na=False) |
                    inv["Material_Name"].str.contains(search, case=False, na=False) |
                    inv["CAS_No"].str.contains(search, case=False, na=False) |
                    inv["Manufacturer"].str.contains(search, case=False, na=False)
                )
                inv = inv[mask]
            
            display_inv = inv.copy()
            display_inv.insert(0, "S.No", range(1, len(display_inv) + 1))
            st.dataframe(
                display_inv.style.format({
                    "Available_Stock": format_2_decimals,
                    "Min_Stock": format_2_decimals,
                    "Pack_Size": format_2_decimals
                }), 
                use_container_width=True, 
                height=500,
                hide_index=True
            )
        else:
            st.info("Inventory is empty.")

    with tab_add:
        st.subheader("Add New Chemical / Material")
        with st.form("add_item_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            unique_name = c1.text_input("Unique Name *", placeholder="e.g. Acetone-99")
            material_name = c2.text_input("Full Material Name *", placeholder="e.g. Acetone 99% AR Grade")
            cas = c1.text_input("CAS Number", placeholder="e.g. 67-64-1")
            grade = c2.text_input("Grade / Purity", placeholder="e.g. 99%, AR Grade")
            units = c2.selectbox("Units", ["g", "mg", "kg", "mL", "L", "units", "pcs"])
            pack_size = c1.text_input("Pack Size", placeholder="e.g. 100ml, 500g")
            
            c3, c4 = st.columns(2)
            mat_type = c3.selectbox("Material Type", ["Solvents", "Chemicals", "Reagents", "Buffers", "Standards", "Lab Consumbles", "Others"])
            manufacturer = c4.text_input("Manufacturer", placeholder="e.g. SRL, HYMA")
            
            opening = st.number_input("Opening Stock", min_value=0.0, value=0.0, step=0.5)
            min_stock = st.number_input("Minimum Stock Alert Threshold", min_value=0.0, value=5.0, step=0.5)

            if st.form_submit_button("➕ Add Item", use_container_width=True):
                if not unique_name or not material_name:
                    st.error("Unique Name and Material Name are required.")
                else:
                    item_id = db.add_item(
                        unique_name=unique_name,
                        material_name=material_name,
                        cas_no=cas,
                        grade=grade,
                        manufacturer=manufacturer,
                        units=units,
                        pack_size=pack_size,
                        material_type=mat_type,
                        opening_stock=opening,
                        min_stock=min_stock,
                        updated_by=email,
                    )
                    st.success(f"✅ Item added: **{unique_name}** (ID: {item_id})")
                    _load_inventory_with_stock.clear()

    with tab_edit:
        inv = db.get_all_items()
        if inv.empty:
            st.info("No items to edit.")
        else:
            search_edit = st.text_input("🔍 Filter dropdown by Item ID, Name, or CAS", key="edit_search")
            if search_edit:
                mask = inv.apply(lambda r: search_edit.lower() in str(r).lower(), axis=1)
                inv = inv[mask]
                
            if inv.empty:
                st.warning("No items match your filter.")
            else:
                options = inv["Item_ID"].astype(str) + " — " + inv["Unique_Name"].astype(str)
                selected = st.selectbox("Select item to edit", options, key="edit_sel")
                sel_id = selected.split(" — ")[0] if selected else None
            if sel_id:
                item_row = inv[inv["Item_ID"] == sel_id].iloc[0]
                with st.form("edit_item_form"):
                    c1, c2 = st.columns(2)
                    new_name = c1.text_input("Unique Name", value=str(item_row.get("Unique_Name", "")))
                    new_mat = c2.text_input("Material Name", value=str(item_row.get("Material_Name", "")))
                    new_cas = c1.text_input("CAS Number", value=str(item_row.get("CAS_No", "")))
                    new_grade = c2.text_input("Grade/Purity", value=str(item_row.get("Grade_Purity", "")))
                    new_units = c2.text_input("Units", value=str(item_row.get("Units", "")))
                    new_pack_size = c1.text_input("Pack Size", value=str(item_row.get("Pack_Size", "")))
                    
                    MAT_TYPES = ["Solvents", "Chemicals", "Reagents", "Buffers", "Standards", "Lab Consumbles", "Others"]
                    c3, c4 = st.columns(2)
                    c_mat_type = str(item_row.get("Material_Type", "Others"))
                    if c_mat_type not in MAT_TYPES: c_mat_type = "Others"
                    new_type = c3.selectbox("Material Type", MAT_TYPES, index=MAT_TYPES.index(c_mat_type))
                    new_mfr = c4.text_input("Manufacturer", value=str(item_row.get("Manufacturer", "")))
                    
                    min_val = item_row.get("Min_Stock", 5.0)
                    try:
                        def_min = float(min_val)
                    except (ValueError, TypeError):
                        def_min = 5.0
                    new_min = st.number_input("Minimum Stock Alert Threshold", value=def_min)

                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        db.update_item(sel_id, {
                            "Unique_Name": new_name,
                            "Material_Name": new_mat,
                            "CAS_No": new_cas,
                            "Grade_Purity": new_grade,
                            "Manufacturer": new_mfr,
                            "Units": new_units,
                            "Material_Type": new_type,
                            "Pack_Size": new_pack_size,
                            "Min_Stock": new_min,
                        })
                        st.success("Item details updated!")
                        _load_inventory_with_stock.clear()

                # --- NEW: Deactivation / Activation ---
                st.markdown("---")
                st.subheader("⚙️ Item Management")
                current_status = str(item_row.get("Status", "Active"))
                
                c_status1, c_status2 = st.columns([2, 1])
                c_status1.write(f"Current Status: **{current_status}**")
                
                if current_status == "Active":
                    if c_status2.button("🚫 Deactivate Item", use_container_width=True):
                        db.update_item(sel_id, {"Status": "Inactive"})
                        st.warning(f"{item_row['Unique_Name']} has been deactivated.")
                        _load_inventory_with_stock.clear()
                        st.rerun()
                else:
                    if c_status2.button("✅ Reactivate Item", use_container_width=True):
                        db.update_item(sel_id, {"Status": "Active"})
                        st.success(f"{item_row['Unique_Name']} is now active!")
                        _load_inventory_with_stock.clear()
                        st.rerun()

                # --- NEW: Quick Stock Adjustment Section (shifted) ---
                st.markdown("---")
                st.subheader("⚖️ Quick Stock Adjustment")
                
                # Fetch fresh stock value
                current_stock = db.compute_stock(sel_id)
                st.metric("Current Available Stock", f"{current_stock} {item_row.get('Units', '')}")

                with st.expander("Update Quantity", expanded=False):
                    with st.form(f"quick_adj_{sel_id}", clear_on_submit=True):
                        st.caption("Enter a positive value to add, or a negative value to deduct.")
                        adj_val = st.number_input("Adjustment Quantity", step=0.1, key=f"quick_qty_{sel_id}")
                        adj_reason = st.text_input("Reason / Remark", placeholder="e.g. Physical count correction", key=f"quick_rem_{sel_id}")
                        
                        if st.form_submit_button("⚡ Apply Adjustment", use_container_width=True):
                            if current_stock + adj_val < 0:
                                st.error(f"Cannot adjust. Resulting stock would be negative ({current_stock + adj_val}).")
                            elif adj_val == 0:
                                st.warning("Please enter a non-zero value.")
                            else:
                                db.add_ledger_entry(sel_id, "ADJUSTMENT", adj_val, 
                                                    reference_id=adj_reason, updated_by=email.lower().strip())
                                st.success(f"Successfully adjusted stock by {adj_val}!")
                                _load_inventory_with_stock.clear()
                                st.rerun()

                # --- NEW: Danger Zone (Hard Deletion) ---
                st.markdown("---")
                with st.expander("⚠️ DANGER ZONE - Permanent Actions"):
                    st.error("Hard deletion is irreversible and will remove the item completely from the database.")
                    confirm = st.checkbox(f"I confirm that I want to PERMANENTLY delete **{item_row['Unique_Name']}**", key=f"del_conf_{sel_id}")
                    if st.button("🗑️ Permanently Delete Item", type="primary", use_container_width=True, disabled=not confirm):
                        ok, msg = db.delete_item(sel_id)
                        if ok:
                            st.success(msg)
                            _load_inventory_with_stock.clear()
                            st.rerun()
                        else:
                            st.error(msg)


def admin_add_stock():
    st.title("📥 Add / Adjust Stock")

    tab_add, tab_adjust, tab_wastage = st.tabs(["Receive Stock", "Stock Adjustment", "Record Wastage"])

    inv = db.get_all_items()
    if inv.empty:
        st.warning("No inventory items found. Add items first.")
        return

    search_stock = st.text_input("🔍 Filter dropdowns by Item ID, Name, or CAS", key="stock_search")
    if search_stock:
        mask = inv.apply(lambda r: search_stock.lower() in str(r).lower(), axis=1)
        inv = inv[mask]

    if inv.empty:
        st.warning("No matching items found.")
        return

    options = inv["Item_ID"].astype(str) + " — " + inv["Unique_Name"].astype(str)

    with tab_add:
        st.subheader("Record Stock Received")
        with st.form("receive_stock_form", clear_on_submit=True):
            selected = st.selectbox("Select Item", options, key="recv_item")
            qty = st.number_input("Quantity Received", min_value=0.1, step=0.5, key="recv_qty")
            if st.form_submit_button("📥 Add Stock", use_container_width=True):
                item_id = selected.split(" — ")[0]
                db.add_ledger_entry(item_id, "RECEIVED", qty, updated_by=email)
                st.success(f"✅ Added {qty} units to stock.")
                _load_inventory_with_stock.clear()

    with tab_adjust:
        st.subheader("Stock Adjustment (±)")
        st.caption("Use positive values to add, negative to deduct.")
        with st.form("adjust_stock_form", clear_on_submit=True):
            selected = st.selectbox("Select Item", options, key="adj_item")
            adj_qty = st.number_input("Adjustment Quantity", step=0.5, key="adj_qty")
            reason = st.text_input("Reason", placeholder="e.g. Spillage, count correction")
            if st.form_submit_button("⚖️ Apply Adjustment", use_container_width=True):
                item_id = selected.split(" — ")[0]
                current = db.compute_stock(item_id)
                if current + adj_qty < 0:
                    st.error(f"Cannot adjust. Current stock: {current}, adjustment: {adj_qty}. Stock cannot go negative.")
                else:
                    db.add_ledger_entry(item_id, "ADJUSTMENT", adj_qty,
                                        reference_id=reason, updated_by=email)
                    st.success(f"Adjustment of {adj_qty} applied.")
                    _load_inventory_with_stock.clear()

    with tab_wastage:
        st.subheader("Record Wastage")
        st.caption("Deducts from available stock and logs specifically as wastage.")
        with st.form("wastage_stock_form", clear_on_submit=True):
            selected = st.selectbox("Select Item", options, key="waste_item")
            wastage_qty = st.number_input("Wastage Quantity", min_value=0.1, step=0.5, key="waste_qty")
            reason = st.text_input("Reason / Note", placeholder="e.g. Expired, Spillage")
            if st.form_submit_button("🗑️ Record Wastage", use_container_width=True):
                item_id = selected.split(" — ")[0]
                current = db.compute_stock(item_id)
                if current - wastage_qty < 0:
                    st.error(f"Cannot record wastage. Current stock: {current}.")
                else:
                    db.add_ledger_entry(item_id, "WASTAGE", -wastage_qty,
                                        reference_id=reason, updated_by=email)
                    st.success(f"Wastage of {wastage_qty} recorded.")
                    _load_inventory_with_stock.clear()


def admin_requests():
    st.title("📋 Request Management")

    tab_pending, tab_all = st.tabs(["Pending Requests", "All Requests"])

    with tab_pending:
        pending = db.get_requests(status="PENDING")
        if pending.empty:
            st.info("🎉 No pending requests!")
        else:
            inv = db.get_all_items()
            for _, req in pending.iterrows():
                item_match = inv[inv["Item_ID"] == str(req["Item_ID"])]
                item_name = item_match.iloc[0]["Unique_Name"] if not item_match.empty else req["Item_ID"]
                avail = db.compute_stock(str(req["Item_ID"]))

                with st.expander(
                    f"🔸 {item_name} — Qty: {req['Quantity']} — by {req['Requested_By']} ({req['Department']})",
                    expanded=True,
                ):
                    c1, c2, c3 = st.columns([2, 1, 1])
                    c1.write(f"**Available Stock:** {avail}")
                    c1.write(f"**Submitted:** {req['Timestamp']}")
                    
                    remark = st.text_input("Remarks", key=f"rmk_{req['Request_ID']}", placeholder="Optional reason...")

                    if c2.button("✅ Approve", key=f"app_{req['Request_ID']}", use_container_width=True):
                        ok, msg = db.approve_request(req["Request_ID"], email, remarks=remark)
                        if ok:
                            st.success(msg)
                            _load_inventory_with_stock.clear()
                            st.rerun()
                        else:
                            st.error(msg)

                    if c3.button("❌ Reject", key=f"rej_{req['Request_ID']}", use_container_width=True):
                        ok, msg = db.reject_request(req["Request_ID"], email, remarks=remark)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

    with tab_all:
        all_req = db.get_requests()
        if not all_req.empty:
            status_filter = st.multiselect("Filter by Status", ["PENDING", "APPROVED", "REJECTED"],
                                           default=["PENDING", "APPROVED", "REJECTED"])
            filtered = all_req[all_req["Status"].isin(status_filter)]
            
            inv = db.get_all_items()
            if not inv.empty:
                filtered = filtered.merge(inv[["Item_ID", "Unique_Name"]], on="Item_ID", how="left")
            
            # Reorder columns to put Unique_Name first and drop internal IDs
            cols_to_drop = ["Request_ID", "Item_ID"]
            display_df = filtered.drop(columns=cols_to_drop, errors="ignore")
            
            # Attempt to move Unique_Name to the front if it exists
            if "Unique_Name" in display_df.columns:
                cols = ["Unique_Name"] + [c for c in display_df.columns if c != "Unique_Name"]
                display_df = display_df[cols]
            
            display_df.insert(0, "S.No", range(1, len(display_df) + 1))

            st.dataframe(display_df.style.format({"Quantity": format_2_decimals}), use_container_width=True, height=400, hide_index=True)
            st.download_button("📥 Export CSV", data=display_df.to_csv(index=False).encode('utf-8'), file_name="requests_export.csv", mime="text/csv")
        else:
            st.info("No requests yet.")


def admin_ledger():
    st.title("📒 Stock Ledger (Audit Trail)")

    ledger = db.get_ledger()
    if ledger.empty:
        st.info("Ledger is empty.")
        return

    inv = db.get_all_items()

    # Filters
    c1, c2, c3 = st.columns(3)
    txn_filter = c1.multiselect("Transaction Type", TRANSACTION_TYPES, default=TRANSACTION_TYPES)
    item_search = c2.text_input("Search by Item ID or name")
    sort_order = c3.selectbox("Sort", ["Newest First", "Oldest First"])

    filtered = ledger[ledger["Transaction_Type"].isin(txn_filter)]

    if item_search:
        if not inv.empty:
            item_search = item_search.lower().strip()
            mask_items = (
                inv["Unique_Name"].str.contains(item_search, case=False, na=False) |
                inv["Material_Name"].str.contains(item_search, case=False, na=False) |
                inv["Item_ID"].astype(str).str.contains(item_search, case=False, na=False)
            )
            matching_ids = inv[mask_items]["Item_ID"].tolist()
            filtered = filtered[filtered["Item_ID"].isin(matching_ids) |
                                filtered["Item_ID"].astype(str).str.contains(item_search, case=False, na=False)]
        else:
            filtered = filtered[filtered["Item_ID"].str.contains(item_search, case=False, na=False)]

    ascending = sort_order == "Oldest First"
    if "DateTime" in filtered.columns:
        filtered = filtered.sort_values("DateTime", ascending=ascending)

    # Merge item names for readability
    if not inv.empty and not filtered.empty:
        filtered = filtered.merge(
            inv[["Item_ID", "Unique_Name"]], on="Item_ID", how="left"
        )
        
    cols_to_show = ["DateTime", "Item_ID", "Unique_Name", "Transaction_Type", "Quantity", "Updated_By"]
    display_df = filtered[[c for c in cols_to_show if c in filtered.columns]].copy()
    display_df.insert(0, "S.No", range(1, len(display_df) + 1))

    st.dataframe(display_df.style.format({"Quantity": format_2_decimals}), use_container_width=True, height=500, hide_index=True)
    st.caption(f"Showing {len(filtered)} entries")
    st.download_button("📥 Export Ledger CSV", data=filtered.to_csv(index=False).encode('utf-8'), file_name="ledger_export.csv", mime="text/csv")


def admin_manage_users():
    st.title("👥 User Management")

    tab_view, tab_add = st.tabs(["View Users", "Add User"])

    with tab_view:
        users = db.get_users()
        if not users.empty:
            c1, c2 = st.columns([4, 1])
            display = users.drop(columns=["Password_Hash", "UserID"], errors="ignore").copy()
            display.insert(0, "S.No", range(1, len(display) + 1))
            c1.dataframe(display, use_container_width=True, hide_index=True)

            with c2.form("delete_user_form"):
                st.write("**Remove User**")
                # Dictionary mapping Label -> UserID for selection
                user_options = {f"{row['Email']} ({row['Role']})": row['UserID'] for _, row in users.iterrows()}
                target_label = st.selectbox("Select user to delete", list(user_options.keys()))
                
                if st.form_submit_button("❌ Delete", use_container_width=True):
                    target_id = user_options[target_label]
                    # Get the email from the label for comparison
                    target_email = target_label.split(" (")[0]
                    
                    if target_email == auth.current_user():
                        st.error("You cannot delete your own account.")
                    else:
                        ok, msg = db.delete_user(target_id)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
        else:
            st.info("No users found.")

    with tab_add:
        # Use a container for styling (mimics the form look)
        with st.container(border=True):
            c1, c2 = st.columns(2)
            new_email = c1.text_input("Email *", placeholder="name@morepenpdr.com", key="admin_add_email")
            new_pass = c2.text_input("Password *", type="password", key="admin_add_pass")
            new_role = c1.selectbox("Role", ROLES, key="admin_add_role")
            
            # Reactive behavior: Enabled selection for Scientists, Visible but locked for others.
            is_scientist = (new_role == "Scientist")
            new_dept = c2.selectbox(
                "Department" + (" *" if is_scientist else ""), 
                [""] + DEPARTMENTS, 
                index=0,
                disabled=not is_scientist,
                key="admin_add_dept"
            )

        if st.button("➕ Create User", use_container_width=True):
            if not new_email or not new_pass:
                st.error("Email and password are required.")
            elif not new_email.endswith("@morepenpdr.com"):
                st.error("Only @morepenpdr.com emails are allowed.")
            elif new_role == "Scientist" and not new_dept:
                st.error("Scientists must be assigned to a department.")
            else:
                existing = db.get_user(new_email)
                if existing is not None:
                    st.error("Email already exists.")
                else:
                    from auth import hash_password
                    db.add_user(new_email, hash_password(new_pass), new_role, new_dept)
                    st.success(f"User **{new_email}** created with role **{new_role}**.")
                    # Safe cleanup of session state keys
                    st.session_state.pop("admin_add_email", None)
                    st.session_state.pop("admin_add_pass", None)
                    st.session_state.pop("admin_add_dept", None)
                    st.rerun()

def admin_po_track():
    st.title("🛒 Purchase Order (PO) Tracking")
    st.caption("Admin-only access: Use 'Review Mode' for a highlighted overview or 'Edit Mode' to make changes.")

    df = db.get_po_track()
    
    # 1. Fill missing columns and ensure consistent data types
    for col in PO_HEADERS:
        if col not in df.columns:
            df[col] = None
    
    # 2. Reorder columns
    df = df[PO_HEADERS].copy()

    # 3. Type Conversion & Null Handling
    date_cols = ["PO Date", "Expected Delivery", "Follow-up Date", "Recived date"]
    num_cols = ["Ordered Qty(G)", "Days to deliver"]
    
    for col in df.columns:
        if col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif col in num_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
        else:
            # Everything else treated as string to avoid mixed-type blocks
            df[col] = df[col].astype(str).replace("None", "").replace("nan", "").replace("NaN", "")

    # 4. Final cleaning for the editor
    df = df.reset_index(drop=True)

    # Define row-level styling for the Review tab
    def style_po_rows(row):
        status = str(row.get("Status", ""))
        if "🟢 RECEIVED" in status:
            return ['background-color: #f0fdf4; color: #0f766e;'] * len(row) # Light Green
        elif "🟡 IN TRANSIT" in status:
            return ['background-color: #fffbeb; color: #92400e;'] * len(row) # Light Yellow
        elif "🔴 CANCELLED" in status:
            return ['background-color: #fef2f2; color: #991b1b;'] * len(row) # Light Red
        elif "🔵 PENDING" in status:
            return ['background-color: #f0f9ff; color: #075985;'] * len(row) # Light Blue/Sky Blue
        return [''] * len(row)

    tab_view, tab_edit = st.tabs(["🔍 Review Mode (Highlighted)", "✏️ Edit Spreadsheet"])

    with tab_view:
        if df.empty:
            st.info("No PO tracking data available. Switch to **Edit Spreadsheet** to add records.")
        else:
            # Search and Filter row
            c1, c2 = st.columns([2, 1])
            with c1:
                search_po = st.text_input("🔍 Search PO / PR / Material / CAS", placeholder="Enter search term...", key="po_search_input")
            with c2:
                status_options = ["🟡 IN TRANSIT", "🟢 RECEIVED", "🔴 CANCELLED", "🔵 PENDING"]
                filter_status = st.multiselect("Filter by Status", status_options, default=status_options, key="po_status_filter")
            
            display_df = df.copy()
            
            # 1. Apply Search Filter
            if search_po:
                mask = display_df.astype(str).apply(
                    lambda row: row.str.contains(search_po, case=False, na=False)
                ).any(axis=1)
                display_df = display_df[mask]
            
            # 2. Apply Status Filter
            if filter_status:
                display_df = display_df[display_df["Status"].isin(filter_status)]
            elif not filter_status:
                display_df = display_df.iloc[0:0] # Show nothing if no status selected

            # Apply styling and formatting for display
            styled_df = display_df.style.apply(style_po_rows, axis=1)
            
            # Format date columns for clean display
            fmt_dict = {col: lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else "" for col in date_cols}
            if "Ordered Qty(G)" in display_df.columns:
                fmt_dict["Ordered Qty(G)"] = format_2_decimals
            styled_df = styled_df.format(fmt_dict)
            
            st.dataframe(styled_df, use_container_width=True, height=600, hide_index=True)
            st.caption(f"Showing {len(display_df)} records. Rows are highlighted based on their current status.")

    with tab_edit:
        st.info("💡 **Tip:** Scroll to the bottom to add a new row. Remember to click **Save** after making changes.")
        # Editable Table
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            hide_index=True,
            column_config={
                "Unit": st.column_config.SelectboxColumn(
                    "Unit",
                    options=PO_UNITS,
                    default="GM"
                ),
                "PO Date": st.column_config.DateColumn("PO Date"),
                "Expected Delivery": st.column_config.DateColumn("Expected Delivery"),
                "Follow-up Date": st.column_config.DateColumn("Follow-up Date"),
                "Recived date": st.column_config.DateColumn("Received date"),
                "Ordered Qty(G)": st.column_config.NumberColumn("Ordered Qty(G)", step=0.01, format="%.2f"),
                "Days to deliver": st.column_config.NumberColumn("Days to deliver", min_value=0, step=1),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["🟡 IN TRANSIT", "🟢 RECEIVED", "🔴 CANCELLED", "🔵 PENDING"],
                    default="🔵 PENDING"
                )
            },
            key="po_track_editor"
        )

        if st.button("💾 Save PO Tracking Data", type="primary", use_container_width=True):
            ok, msg = db.save_po_track(edited_df)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

def admin_vendors(is_admin=True):
    st.title("🏢 Suppliers & Vendors")
    
    if is_admin:
        tab_view, tab_add = st.tabs(["View Suppliers", "Add Supplier"])
    else:
        tab_view = st.container()
        tab_add = None

    with tab_view:
        vendors = db.get_vendors()
        if not vendors.empty:
            display = vendors.copy()
            display = display.rename(columns={
                "Company_Name": "Suppliers / Company Name",
                "Contact_Number": "Contact Number", 
                "Email": "Email ID",
                "Notes": "Others"
            })
            
            cols_to_show = ["Vendor_ID", "Suppliers / Company Name", "Contact Number", "Email ID", "Others"]
            display = display[[c for c in cols_to_show if c in display.columns]].copy()
            display.insert(0, "S.No", range(1, len(display) + 1))
            
            if is_admin:
                st.subheader("Manage Active Vendors")
                c1, c2 = st.columns([4, 1])
                c1.dataframe(display, use_container_width=True, hide_index=True)
                
                with c2.form("del_vendor_form"):
                    st.write("**Remove Vendor**")
                    target = st.selectbox("Select to delete", display["Vendor_ID"])
                    if st.form_submit_button("❌ Delete"):
                        ok, msg = db.delete_vendor(target)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            else:
                st.dataframe(display, use_container_width=True, hide_index=True)
        else:
            st.info("No suppliers found.")

    if tab_add:
        with tab_add:
            with st.form("add_supplier_form", clear_on_submit=True):
                st.subheader("Register New Supplier")
                c1, c2 = st.columns(2)
                co_name = c1.text_input("Suppliers / Company Name *")
                spoc = c2.text_input("Contact Person (SPOC)")
                contact = c1.text_input("Contact Number *")
                email_id = c2.text_input("Email ID *")
                notes = st.text_area("Others (Notes)", placeholder="Extra details...", height=68)
                
                if st.form_submit_button("➕ Save Supplier", use_container_width=True):
                    if not co_name or not contact or not email_id:
                        st.error("Company Name, Contact, and Email are required.")
                    else:
                        db.add_vendor(co_name, spoc, contact, email_id, notes)
                        st.success(f"Supplier **{co_name}** added successfully.")
                        st.rerun()


# ════════════════════════════════════════════════
#  SCIENTIST PAGES
# ════════════════════════════════════════════════

def scientist_stock_viewer():
    st.title("🔬 Available Stock")
    
    _display_store_timings()

    inv = _load_inventory_with_stock()
    if inv.empty:
        st.info("No inventory data available.")
        return

    # Search
    search = st.text_input("🔍 Search chemicals by name, CAS, or manufacturer")
    display = inv[inv["Status"] == "Active"].copy()
    if search:
        search = search.lower().strip()
        mask = (
            display["Unique_Name"].str.contains(search, case=False, na=False) |
            display["Material_Name"].str.contains(search, case=False, na=False) |
            display["CAS_No"].str.contains(search, case=False, na=False) |
            display["Manufacturer"].str.contains(search, case=False, na=False)
        )
        display = display[mask]

    # Show table
    cols_to_show = ["Item_ID", "Unique_Name", "Material_Name", "CAS_No", "Grade_Purity",
                    "Pack_Size", "Min_Stock", "Status", "Manufacturer", "Units", "Available_Stock"]
    show_df = display[[c for c in cols_to_show if c in display.columns]].copy()
    show_df.insert(0, "S.No", range(1, len(show_df) + 1))

    def color_row(row):
        styles = [''] * len(row)
        if "Available_Stock" in row.index:
            try:
                avail = float(row["Available_Stock"])
                min_val = row.get("Min_Stock", 5.0)
                try:
                    min_stk = float(min_val)
                except (ValueError, TypeError):
                    min_stk = 5.0
                idx = row.index.get_loc("Available_Stock")
                if avail <= 0:
                    styles[idx] = f"background-color: {STATUS_PALETTE['danger']['bg']}; color: {STATUS_PALETTE['danger']['text']}; border-left: 4px solid {STATUS_PALETTE['danger']['text']}; font-weight: 700;"
                elif avail <= min_stk:
                    styles[idx] = f"background-color: {STATUS_PALETTE['warning']['bg']}; color: {STATUS_PALETTE['warning']['text']}; border-left: 4px solid {STATUS_PALETTE['warning']['text']}; font-weight: 700;"
                else:
                    styles[idx] = f"background-color: {STATUS_PALETTE['success']['bg']}; color: {STATUS_PALETTE['success']['text']}; border-left: 4px solid {STATUS_PALETTE['success']['text']}; font-weight: 700;"

            except Exception:
                pass
        return styles



    styled = show_df.style.format({
        "Available_Stock": format_2_decimals,
        "Min_Stock": format_2_decimals,
        "Pack_Size": format_2_decimals
    }).apply(color_row, axis=1)
    st.dataframe(styled, use_container_width=True, height=500, hide_index=True)
    st.caption(f"Showing {len(show_df)} items")


def scientist_submit_request():
    st.title("📝 Submit Material Request(s)")
    
    _display_store_timings()

    if "cart" not in st.session_state:
        st.session_state["cart"] = []

    inv = _load_inventory_with_stock()
    if inv.empty:
        st.warning("No inventory available.")
        return

    c1, c2 = st.columns([1, 1])

    with c1:
        st.subheader("1. Select Chemical & Quantity")
        search_req = st.text_input("🔍 Search chemical by Name, ID, or CAS", key="req_search")
        display_inv = inv[inv["Status"] == "Active"].copy()
        if search_req:
            search_req = search_req.lower().strip()
            mask = (
                display_inv["Unique_Name"].str.contains(search_req, case=False, na=False) |
                display_inv["Material_Name"].str.contains(search_req, case=False, na=False) |
                display_inv["CAS_No"].str.contains(search_req, case=False, na=False) |
                display_inv["Item_ID"].astype(str).str.contains(search_req, case=False, na=False)
            )
            display_inv = display_inv[mask]

        if not display_inv.empty:
            with st.form("add_cart_form", clear_on_submit=True):
                options = display_inv["Item_ID"].astype(str) + " — " + display_inv["Unique_Name"].astype(str) + " (Stock: " + display_inv["Available_Stock"].astype(str) + ")"
                selected = st.selectbox("Select Chemical / Material", options)
                dept = st.selectbox("Your Department", DEPARTMENTS)
                qty = st.number_input("Quantity Required", min_value=0.1, step=0.5)

                if st.form_submit_button("🛒 Add to Cart", use_container_width=True):
                    item_id = selected.split(" — ")[0] if selected else ""
                    avail = db.compute_stock(item_id)
                    already_in_cart = sum(i["qty"] for i in st.session_state["cart"] if i["item_id"] == item_id)
                    
                    if (qty + already_in_cart) > avail:
                        st.error(f"Cannot add {qty}. Only {avail} available. (You already have {already_in_cart} in cart).")
                    else:
                        item_name = selected.split(" — ")[1].split(" (Stock:")[0]
                        st.session_state["cart"].append({
                            "item_id": item_id,
                            "name": item_name,
                            "dept": dept,
                            "qty": qty
                        })
                        st.success(f"Added {qty} units of {item_name} to cart.")

    with c2:
        st.subheader("2. Review Cart & Submit")
        cart = st.session_state["cart"]
        if not cart:
            st.info("Cart is empty.")
        else:
            cart_df = pd.DataFrame(cart)
            cart_df.insert(0, "S.No", range(1, len(cart_df) + 1))
            st.dataframe(cart_df[["S.No", "name", "dept", "qty"]], use_container_width=True, hide_index=True)
            if st.button("🗑️ Clear Cart", use_container_width=True):
                st.session_state["cart"] = []
                st.rerun()
            
            st.divider()
            if st.button("📤 Submit All Requests", type="primary", use_container_width=True):
                success_count = 0
                for item in cart:
                    ok, msg = db.submit_request(item["item_id"], email, item["dept"], item["qty"])
                    if ok:
                        success_count += 1
                    else:
                        st.error(f"Failed to submit {item['name']}: {msg}")
                if success_count > 0:
                    st.success(f"Successfully submitted {success_count} requests.")
                    st.session_state["cart"] = []
                    _load_inventory_with_stock.clear()


def scientist_my_requests():
    st.title("📋 My Requests")

    reqs = db.get_requests(requested_by=email)
    if reqs.empty:
        st.info("You haven't submitted any requests yet.")
        return

    inv = db.get_all_items()
    if not inv.empty:
        reqs = reqs.merge(inv[["Item_ID", "Unique_Name"]], on="Item_ID", how="left")

    # Status badges
    def status_color(status):
        if status == "PENDING":
            return f"color: {STATUS_PALETTE['warning']['text']}; font-weight: bold;"
        elif status == "APPROVED":
            return f"color: {STATUS_PALETTE['success']['text']}; font-weight: bold;"
        elif status == "REJECTED":
            return f"color: {STATUS_PALETTE['danger']['text']}; font-weight: bold;"
        return "color: #374151;"


    cols = ["Unique_Name", "Quantity", "Department", "Status",
                        "Timestamp", "Remarks", "Approved_By", "Approval_Time"]
    req_cols = [c for c in cols if c in reqs.columns]
    display_reqs = reqs[req_cols].copy()
    display_reqs.insert(0, "S.No", range(1, len(display_reqs) + 1))
    styled = display_reqs.style.map(status_color, subset=["Status"]).format({"Quantity": format_2_decimals})
    st.dataframe(styled, use_container_width=True, height=400, hide_index=True)


# ════════════════════════════════════════════════
#  MANAGEMENT PAGES
# ════════════════════════════════════════════════

def management_dashboard():
    st.title("📊 Analytics Dashboard")

    inv = _load_inventory_with_stock()
    reqs = db.get_requests()
    ledger = db.get_ledger()

    # ── KPI row ──
    c1, c2, c3, c4 = st.columns(4)
    total_items = len(inv) if not inv.empty else 0
    total_reqs = len(reqs) if not reqs.empty else 0
    approved = len(reqs[reqs["Status"] == "APPROVED"]) if not reqs.empty else 0
    pending = len(reqs[reqs["Status"] == "PENDING"]) if not reqs.empty else 0

    c1.metric("Total Items", total_items)
    c2.metric("Total Requests", total_reqs)
    c3.metric("Approved", approved)
    c4.metric("Pending", pending)

    st.divider()

    if reqs.empty and ledger.empty:
        st.info("No data available for analytics yet. Requests and ledger entries will populate these charts.")
        return

    # ── Charts row 1 ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 Department-wise Consumption")
        if not reqs.empty:
            approved_reqs = reqs[reqs["Status"] == "APPROVED"].copy()
            if not approved_reqs.empty:
                approved_reqs["Quantity"] = pd.to_numeric(approved_reqs["Quantity"], errors="coerce")
                dept_data = approved_reqs.groupby("Department")["Quantity"].sum().reset_index()
                fig = px.bar(dept_data, x="Department", y="Quantity",
                             color="Department",
                             color_discrete_sequence=["#009688", "#00796b", "#4db6ac", "#b2dfdb"],
                             title="Total Quantity Issued per Department")
                fig.update_layout(_get_plotly_layout("Quantity per Department"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No approved requests to show.")
        else:
            st.info("No requests data.")

    with col_right:
        st.subheader("🔝 Top 10 Most Requested Chemicals")
        if not reqs.empty:
            approved_reqs = reqs[reqs["Status"] == "APPROVED"].copy()
            if not approved_reqs.empty and not inv.empty:
                approved_reqs["Quantity"] = pd.to_numeric(approved_reqs["Quantity"], errors="coerce")
                top_items = approved_reqs.groupby("Item_ID")["Quantity"].sum().nlargest(10).reset_index()
                top_items = top_items.merge(inv[["Item_ID", "Unique_Name"]], on="Item_ID", how="left")
                top_items["Label"] = top_items["Unique_Name"].fillna(top_items["Item_ID"])
                fig = px.bar(top_items, x="Quantity", y="Label", orientation="h",
                             color="Quantity",
                             color_continuous_scale="Viridis",
                             title="Top 10 by Total Quantity Issued")
                fig.update_layout(_get_plotly_layout("Top 10 Chemicals"))
                fig.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No approved requests to show.")
        else:
            st.info("No requests data.")

    st.divider()

    # ── Charts row 2 ──
    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.subheader("📈 Stock Inflow vs Outflow (Ledger)")
        if not ledger.empty:
            ledger_c = ledger.copy()
            ledger_c["Quantity"] = pd.to_numeric(ledger_c["Quantity"], errors="coerce")
            ledger_c["DateTime"] = pd.to_datetime(ledger_c["DateTime"], errors="coerce")
            ledger_c = ledger_c.dropna(subset=["DateTime"])
            if not ledger_c.empty:
                ledger_c["Date"] = ledger_c["DateTime"].dt.date
                inflow = ledger_c[ledger_c["Quantity"] > 0].groupby("Date")["Quantity"].sum().reset_index()
                inflow.columns = ["Date", "Inflow"]
                outflow = ledger_c[ledger_c["Quantity"] < 0].groupby("Date")["Quantity"].sum().abs().reset_index()
                outflow.columns = ["Date", "Outflow"]
                merged = pd.merge(inflow, outflow, on="Date", how="outer").fillna(0).sort_values("Date")

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=merged["Date"], y=merged["Inflow"],
                                         mode="lines+markers", name="Inflow",
                                         line=dict(color="#009688", width=3)))
                fig.add_trace(go.Scatter(x=merged["Date"], y=merged["Outflow"],
                                         mode="lines+markers", name="Outflow",
                                         line=dict(color="#991b1b", width=3)))
                fig.update_layout(_get_plotly_layout("Stock Movement Over Time"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No dated ledger entries.")
        else:
            st.info("Ledger is empty.")

    with col_right2:
        st.subheader("📊 Request Status Breakdown")
        if not reqs.empty:
            status_counts = reqs["Status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            colors = {"PENDING": STATUS_PALETTE["warning"]["text"], 
                      "APPROVED": STATUS_PALETTE["success"]["text"], 
                      "REJECTED": STATUS_PALETTE["danger"]["text"]}
            fig = px.pie(status_counts, names="Status", values="Count",
                         color="Status",
                         color_discrete_map=colors,
                         title="Request Status Distribution")
            fig.update_layout(_get_plotly_layout("Distribution of Request Status"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No requests data.")



# ════════════════════════════════════════════════
#  PAGE ROUTER
# ════════════════════════════════════════════════

if role == "Admin":
    if page == "Dashboard":
        admin_dashboard()
    elif page == "Inventory":
        admin_inventory()
    elif page == "Add Stock":
        admin_add_stock()
    elif page == "Requests":
        admin_requests()
    elif page == "Ledger":
        admin_ledger()
    elif page == "Manage Users":
        admin_manage_users()
    elif page == "PO Track":
        admin_po_track()
    elif page == "Suppliers / Vendors":
        admin_vendors(is_admin=True)

elif role == "Scientist":
    if page == "Stock Viewer":
        scientist_stock_viewer()
    elif page == "Submit Request":
        scientist_submit_request()
    elif page == "My Requests":
        scientist_my_requests()

elif role == "Management":
    if page == "Analytics Dashboard":
        management_dashboard()
    elif page == "Suppliers / Vendors":
        admin_vendors(is_admin=False)

else:
    st.warning("Unknown role. Contact admin.")
