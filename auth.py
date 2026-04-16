# ──────────────────────────────────────────────
# Store Tracker — Authentication Module
# ──────────────────────────────────────────────
import streamlit as st
import bcrypt
import os
import db


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(stored_hash: str, password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
    except Exception:
        return False


def login_page():
    """Render the login page. Returns True if user is now logged in."""

    # Centre the login card
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-1.png")
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)
        logo_l, logo_c, logo_r = st.columns([1.2, 2.2, 1.2])
        with logo_c:
            st.image(logo_path, width=210)
        st.markdown(
            """
            <div style="text-align:center; margin-top: 8px; margin-bottom: 20px;">
                <div style="font-family: 'Montserrat', sans-serif; color: #1e293b; margin-bottom:0; font-size: 2.2rem; font-weight: 700;">
                    Store Tracker
                </div>
                <p style="color: #64748b; font-family: 'Inter', sans-serif; font-size: 1.05rem; font-weight: 500;">
                    MPDR Chemical Inventory Management
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_login, tab_register, tab_forgot = st.tabs(["Login", "Register", "Forgot Password"])

        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email", placeholder="name@morepenpdr.com")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                email = email.lower().strip()
                if not email or not password:
                    st.error("Please enter both email and password.")
                    return False

                user = db.get_user(email)
                if user is not None and check_password(str(user["Password_Hash"]), password):
                    st.session_state["logged_in"] = True
                    st.session_state["email"] = email
                    st.session_state["role"] = user["Role"]
                    st.session_state["department"] = user.get("Department", "")
                    st.session_state["user_id"] = user["UserID"]
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
                    
        with tab_register:
            from config import ROLES, DEPARTMENTS
            
            reg_email = st.text_input("Choose Email *", placeholder="name@morepenpdr.com", key="reg_email_in")
            reg_pass = st.text_input("Choose Password *", type="password", key="reg_pass_in")
            reg_pass2 = st.text_input("Confirm Password *", type="password", key="reg_pass2_in")
            reg_role = st.selectbox("Select Role *", ROLES, key="reg_role_in")
            
            reg_dept = ""
            if reg_role == "Scientist":
                reg_dept = st.selectbox("Select Department *", [""] + DEPARTMENTS, key="reg_dept_in")
                
            if st.button("Complete Registration", use_container_width=True, key="reg_btn"):
                reg_email = reg_email.lower().strip()
                if not reg_email or not reg_pass:
                    st.error("Email and password are required.")
                elif not reg_email.endswith("@morepenpdr.com"):
                    st.error("Only @morepenpdr.com emails are allowed for registration.")
                elif reg_pass != reg_pass2:
                    st.error("Passwords do not match.")
                elif reg_role in ["Admin", "Management"] and reg_email.lower() != "admin@morepenpdr.com":
                    st.error("Only the designated email (admin@morepenpdr.com) can hold Admin privileges.")
                elif reg_role == "Scientist" and not reg_dept:
                    st.error("Scientists must select a department.")
                elif db.get_user(reg_email) is not None:
                    st.error(f"Email '{reg_email}' is already registered.")
                else:
                    # Direct registration without OTP
                    ok, res = db.add_user(reg_email, hash_password(reg_pass), reg_role, reg_dept)
                    if ok:
                        st.success("✅ Registration successful! You can now login.")
                    else:
                        st.error(f"Registration failed: {res}")

        with tab_forgot:
            st.info("### 🔑 Password Reset")
            st.write(
                "For security reasons, automated password resets are disabled. "
                "Please contact your **System Administrator** or the IT department "
                "to reset your credentials."
            )
            st.markdown("---")
            st.markdown("**Admin Contact:** admin@morepenpdr.com")
    return False


def require_login():
    """Call at top of app.py — blocks rendering until logged in."""
    if not st.session_state.get("logged_in"):
        login_page()
        st.stop()


def logout():
    st.session_state.clear()
    st.rerun()


def current_user():
    return st.session_state.get("email", "")


def current_role():
    return st.session_state.get("role", "")


def current_department():
    return st.session_state.get("department", "")
