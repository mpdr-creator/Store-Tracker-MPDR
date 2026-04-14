# ──────────────────────────────────────────────
# Store Tracker — Authentication Module
# ──────────────────────────────────────────────
import os
import random
import smtplib
from email.message import EmailMessage

import streamlit as st
import bcrypt
import db


def send_otp(to_email, otp_code, scope="global"):
    """Send OTP via SMTP. `scope` namespaces the dev-mode message key so
    Register and Forgot-Password tabs never share the same session state key."""
    sender = os.getenv("SMTP_EMAIL")
    pwd = os.getenv("SMTP_PASSWORD")
    try:
        if not sender and "SMTP_EMAIL" in st.secrets:
            sender = st.secrets["SMTP_EMAIL"]
        if not pwd and "SMTP_PASSWORD" in st.secrets:
            pwd = st.secrets["SMTP_PASSWORD"]
    except Exception:
        pass

    if not sender or not pwd:
        st.session_state[f"dev_otp_message_{scope}"] = (
            f"🔧 DEV MODE: SMTP not configured. Your OTP is: **{otp_code}**"
        )
        return True
    
    msg = EmailMessage()
    msg.set_content(f"Your Store Tracker Verification Code is: {otp_code}\n\nPlease do not share this code with anyone.")
    msg['Subject'] = 'Store Tracker - Verification Code'
    msg['From'] = sender
    msg['To'] = to_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, pwd)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email. Check SMTP configuration. Exception: {e}")
        return False


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
        st.markdown(
            """
            <div style="text-align:center; margin-top:40px; margin-bottom: 20px;">
                <div style="font-family: 'Montserrat', sans-serif; color: #1e293b; margin-bottom:0; font-size: 2.5rem; font-weight: 700;">
                    <span style="color: #10b981;">📦</span> Store Tracker
                </div>
                <p style="color: #64748b; font-family: 'Inter', sans-serif; font-size: 1.1rem; font-weight: 500;">
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
                if not email or not password:
                    st.error("Please enter both email and password.")
                    return False

                email_clean = email.strip().lower()
                user = db.get_user(email_clean)
                if user is not None and check_password(str(user["Password_Hash"]), password):
                    st.session_state["logged_in"] = True
                    st.session_state["email"] = email_clean
                    st.session_state["role"] = user["Role"]
                    st.session_state["department"] = user.get("Department", "")
                    st.session_state["user_id"] = user["UserID"]
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
                    
        with tab_register:
            from config import ROLES, DEPARTMENTS
            
            if "reg_state" not in st.session_state:
                st.session_state.reg_state = "input"
                
            if st.session_state.reg_state == "input":
                reg_email = st.text_input("Choose Email *", placeholder="name@morepenpdr.com", key="reg_email_in")
                reg_pass = st.text_input("Choose Password *", type="password", key="reg_pass_in")
                reg_pass2 = st.text_input("Confirm Password *", type="password", key="reg_pass2_in")
                reg_role = st.selectbox("Select Role *", ROLES, key="reg_role_in")
                
                reg_dept = ""
                if reg_role == "Scientist":
                    reg_dept = st.selectbox("Select Department *", [""] + DEPARTMENTS, key="reg_dept_in")
                    
                if st.button("Send Verification OTP", use_container_width=True, key="reg_btn"):
                    reg_email_clean = reg_email.strip().lower()
                    if not reg_email or not reg_pass:
                        st.error("Email and password are required.")
                    elif not reg_email_clean.endswith("@morepenpdr.com"):
                        st.error("Only @morepenpdr.com emails are allowed for registration.")
                    elif reg_pass != reg_pass2:
                        st.error("Passwords do not match.")
                    elif reg_role in ["Admin", "Management"] and reg_email_clean != "admin@morepenpdr.com":
                        st.error("Only the designated email (admin@morepenpdr.com) can hold Admin privileges.")
                    elif reg_role == "Scientist" and not reg_dept:
                        st.error("Scientists must select a department.")
                    elif db.get_user(reg_email_clean) is not None:  # BUG FIX: use normalized email
                        st.error(f"Email '{reg_email_clean}' is already registered.")
                    else:
                        otp = str(random.randint(100000, 999999))
                        if send_otp(reg_email, otp, scope="reg"):  # scoped key
                            st.session_state.reg_otp = otp
                            st.session_state.reg_data = {
                                "email": reg_email_clean, "pass": reg_pass, 
                                "role": reg_role, "dept": reg_dept
                            }
                            st.session_state.reg_state = "verify"
                            st.rerun()

            elif st.session_state.reg_state == "verify":
                if "dev_otp_message_reg" in st.session_state:
                    st.warning(st.session_state["dev_otp_message_reg"])
                st.info(f"An OTP has been sent to {st.session_state.reg_data['email']}")
                otp_input = st.text_input("Enter 6-digit OTP", key="reg_otp_in")
                col1, col2 = st.columns(2)
                verify_clicked = col1.button("Verify & Register", use_container_width=True, key="reg_verify_btn")
                cancel_clicked = col2.button("Cancel", key="reg_cancel_btn")

                if cancel_clicked:
                    st.session_state.reg_state = "input"
                    st.session_state.pop("reg_success", None)
                    st.session_state.pop("dev_otp_message_reg", None)
                    st.rerun()

                # Show success state (persists across re-runs via reg_success flag)
                if st.session_state.get("reg_success"):
                    st.success("✅ Registration successful! Switch to the **Login** tab to sign in.")
                    if st.button("Reset Registration Form", key="reg_done_btn"):
                        st.session_state.reg_state = "input"
                        st.session_state.pop("reg_success", None)
                        st.session_state.pop("dev_otp_message_reg", None)
                        st.rerun()
                elif verify_clicked:
                    if otp_input.strip() == st.session_state.reg_otp:
                        d = st.session_state.reg_data
                        try:
                            db.add_user(d["email"], hash_password(d["pass"]), d["role"], d["dept"])
                            st.session_state.reg_success = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to register: {e}")
                    else:
                        st.error("Invalid OTP.")

        with tab_forgot:
            if "forgot_state" not in st.session_state:
                st.session_state.forgot_state = "input"
                
            if st.session_state.forgot_state == "input":
                for_email = st.text_input("Registered Email", placeholder="name@morepenpdr.com", key="for_email")
                for_email_clean = for_email.strip().lower()
                if st.button("Send Reset OTP", use_container_width=True, key="for_btn"):
                    if not for_email:
                        st.error("Please enter your email.")
                    elif db.get_user(for_email_clean) is None:
                        st.error("Account not found in the system.")
                    else:
                        otp = str(random.randint(100000, 999999))
                        if send_otp(for_email_clean, otp, scope="forgot"):  # scoped key
                            st.session_state.forgot_otp = otp
                            st.session_state.forgot_email = for_email_clean
                            st.session_state.forgot_state = "verify"
                            st.rerun()
                            
            elif st.session_state.forgot_state == "verify":
                if "dev_otp_message_forgot" in st.session_state:
                    st.warning(st.session_state["dev_otp_message_forgot"])
                st.info(f"OTP sent to {st.session_state.forgot_email}")
                for_otp = st.text_input("Enter 6-digit OTP", key="for_otp_in")
                new_pass = st.text_input("New Password", type="password", key="for_pass")
                col1, col2 = st.columns(2)
                reset_clicked = col1.button("Reset Password", use_container_width=True, key="for_verify_btn")
                cancel_clicked = col2.button("Cancel", key="for_cancel_btn")

                if cancel_clicked:
                    st.session_state.forgot_state = "input"
                    st.session_state.pop("forgot_success", None)
                    st.session_state.pop("dev_otp_message_forgot", None)
                    st.rerun()

                # Show success state persisted across re-runs via forgot_success flag
                if st.session_state.get("forgot_success"):
                    st.success("✅ Password updated successfully! Switch to the **Login** tab to sign in.")
                    if st.button("Reset Form", key="for_done_btn"):
                        st.session_state.forgot_state = "input"
                        st.session_state.pop("forgot_success", None)
                        st.session_state.pop("dev_otp_message_forgot", None)
                        st.rerun()
                elif reset_clicked:
                    if for_otp.strip() != st.session_state.forgot_otp:
                        st.error("Invalid OTP.")
                    elif not new_pass:
                        st.error("New password required.")
                    else:
                        ok = db.update_password(st.session_state.forgot_email, hash_password(new_pass))
                        if ok:
                            st.session_state.forgot_success = True
                            st.rerun()
                        else:
                            st.error("Failed to update password. User record might be missing.")
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
