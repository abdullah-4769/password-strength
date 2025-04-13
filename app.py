import re
import random
import string
import streamlit as st

# Persistent Storage for Passwords
if 'password_diary' not in st.session_state:
    st.session_state['password_diary'] = {}

def check_password_strength(password):
    score = 0
    feedback = []

    # Length Check 
    if len(password) >= 8:
        score += 2
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1.5
    else:
        feedback.append("Include both uppercase and lowercase letters.")

    # Digit Check 
    if re.search(r"\d", password):
        score += 1.5
    else:
        feedback.append("Add at least one number (0-9).")

    # Special Character Check 
    if re.search(r"[!@#$%^&*]", password):
        score += 2
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")

    return score, feedback

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

COMMON_PASSWORDS = ["password", "123456", "qwerty", "password123", "admin", "letmein"]

def save_password(account, password):
    st.session_state['password_diary'][account] = password

# Streamlit UI Config
st.set_page_config(page_title="🔐 Password Strength Meter", layout="wide")

# 🔥 Add Custom CSS for Black-Red Theme
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;600;800&display=swap');
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(to top, #000000, #1a1a1a);
            color: #ffffff;
        }

        h1 {
            font-size: 3rem;
            color: #ff4d4d;
            text-align: center;
            margin-bottom: 30px;
        }

        .stButton > button {
            background-color: #e60000 !important;
            color: white !important;
            border-radius: 12px;
            padding: 10px 25px;
            font-size: 16px;
            border: none;
            transition: 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #cc0000 !important;
            transform: scale(1.05);
        }

        .stTextInput input, .stTextArea textarea {
            border-radius: 10px;
            padding: 10px;
            border: 2px solid #ff4d4d;
            background-color: #1f1f1f;
            color: #ffffff;
            box-shadow: 0 2px 5px rgba(255, 77, 77, 0.2);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(to top, #000000, #1a1a1a);
        }

        .stAlert, .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 10px;
            padding: 15px;
            background-color: #1f1f1f !important;
            border-left: 5px solid #e60000 !important;
            color: #ffffff !important;
        }

        .password-card {
            background-color: #2a2a2a;
            padding: 10px 15px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(255, 0, 0, 0.1);
            margin-bottom: 10px;
            color: #ffffff;
        }

        label.css-16huue1 {
            font-weight: bold;
            color: #ff4d4d;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🔐 Password Strength Meter")

# Sidebar Navigation
page = st.sidebar.radio("Navigation", ["Home", "📒 Password Diary"])

# Home Page
if page == "Home":
    account_name = st.text_input("🔹 Enter Account Name:")
    password = st.text_input("🔹 Enter Your Password:", type="password")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Check Strength"):
            if password.lower() in COMMON_PASSWORDS:
                st.error("❌ This password is too common. Please choose a more secure one.")
            elif password:
                score, feedback = check_password_strength(password)
                if score >= 6:
                    st.success("✅ Strong Password!")
                elif score >= 4:
                    st.warning("⚠️ Moderate Password - Consider adding more security features.")
                else:
                    st.error("❌ Weak Password - Improve it using the suggestions below.")
                    for tip in feedback:
                        st.write("-", tip)
            else:
                st.warning("Please enter a password to check.")

    with col2:
        if st.button("Generate Strong Password"):
            strong_password = generate_strong_password()
            st.write("🔑 Suggested Password:", strong_password)

    if account_name and password:
        if st.button("Save Password"):
            save_password(account_name, password)
            st.success(f"✅ Password for {account_name} saved successfully!")

# Diary Page
elif page == "📒 Password Diary":
    st.header("📒 Saved Passwords")
    if st.session_state['password_diary']:
        for account, saved_password in st.session_state['password_diary'].items():
            st.markdown(f"""
                <div class="password-card">
                    <strong>{account}</strong>: <code>{saved_password}</code>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No passwords saved yet.")
