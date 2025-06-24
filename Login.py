import streamlit as st
from pymongo import MongoClient
import bcrypt
from streamlit_cookies_manager import EncryptedCookieManager
from UI import sidebarUI, Home

def app(users, cookies):
    if cookies.get("authenticated") == "true":
        main_app(users, cookies)
    else:
        login_page()

@st.cache_resource
def get_client(uri):
    return MongoClient(uri)

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def login_page():
    st.html("""
            <div style="text-align: center;">
                <img src="https://www.nvidia.com/content/nvidiaGDC/us/en_US/about-nvidia/legal-info/logo-brand-usage/_jcr_content/root/responsivegrid/nv_container_392921705/nv_container/nv_image.coreimg.100.630.png/1703060329053/nvidia-logo-vert.png" alt="NVIDIA Logo" width="200"/>
                <h1 style="color: #76b900; font-family: 'Courier New', Courier, monospace;">Customer Care - WorkFlow</h1>
            </div>
        """)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        user = users.find_one({"email": email})
        if user and check_password(password, user["password"]):
            cookies["authenticated"] = "true"
            cookies["user_email"] = email
            cookies.save()
            st.rerun()
        else:
            st.error("Invalid email or password")

def main_app(users, cookies):
    try:
        user = users.find_one({"email": cookies["user_email"]})
        user_name = user.get("username")
        sidebarUI.run(user, users, cookies)
        Home.run(user_name=user_name)
    except:
        st.error("⚠️ Something went wrong!\n\n\nPlease contact Santhoshsivan.")


uri = st.secrets['api_keys']['MONGO_URI1']
client = get_client(uri)
db = client["NVCC"]
users = db["Users"]

st.set_page_config(layout="wide", page_title="NVCC Workflow", page_icon="https://store-images.s-microsoft.com/image/apps.20966.13599037783181022.b05b7adf-6b7a-44ae-9a70-9dc9370ea7e6.4cd88c60-6ff1-4b0f-aed6-8e2efa5629c1")
cookiepass = st.secrets['cookie']["pass"]

cookies = EncryptedCookieManager(prefix="login", password= cookiepass)
if not cookies.ready():
    st.stop()

app(users, cookies)