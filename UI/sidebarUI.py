def run(user, users, cookies):
    import streamlit as st
    import bcrypt

    user_name = user.get("username")
    user_email = user.get("email")

    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    with st.sidebar:
        st.html("""
                <div style="text-align: center;">
                    <img src="https://www.nvidia.com/content/nvidiaGDC/us/en_US/about-nvidia/legal-info/logo-brand-usage/_jcr_content/root/responsivegrid/nv_container_392921705/nv_container/nv_image.coreimg.100.630.png/1703060329053/nvidia-logo-vert.png" alt="NVIDIA Logo" width="200"/>
                    <h1 style="color: #76b900; font-family: 'Courier New', Courier, monospace; font-size: 15
                    px">Customer Care WorkFlow</h1>
                </div>
            """)
        st.write(f'Hey, **{user_name}**.')
        settings = st.selectbox("Update/Modify", [ "Account Details", "Security/Password"])
        if settings == "Account Details":
            with st.form("Account"):
                st.subheader("Current Information:")
                st.write(f"User Name:\n**{user_name}**")
                st.write(f"Email Address:\n**{user_email}**")
                field = st.selectbox("Field", ["Email", "Username"])
                value = st.text_input("New Value")
                update_btn = st.form_submit_button("update")

                if update_btn:
                    if field == "Email":
                        result = users.update_one(
                            {"email": user_email},  # Filter
                            {"$set": {"email": value}}  # Update
                        )
                        if result.modified_count > 0:
                            st.success("Email updated successfully!")
                        else:
                            st.warning("No changes made or user not found.")

                    if field == "Username":
                        result = users.update_one(
                            {"email": user_email},  # Filter
                            {"$set": {"username": value}}  # Update
                        )
                        if result.modified_count > 0:
                            st.success("Username updated successfully!")
                        else:
                            st.warning("No changes made or user not found.")
        if settings == "Security/Password":
            with st.form("Update Password"):
                newpass = st.text_input("New Password", type="password")
                btn = st.form_submit_button("Update")

                if btn:
                    result = users.update_one(
                        {"email": user_email},  # Filter
                        {"$set": {"password": hash_password(newpass)}}  # Update
                    )

                    if result.modified_count > 0:
                        st.success("Password updated successfully!")
                    else:
                        st.warning("No changes made or user not found.")


        if st.button("Logout"):
            cookies["authenticated"] = "false"
            cookies["user_email"] = ""
            cookies.save()
            st.rerun()








