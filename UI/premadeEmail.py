import streamlit as st

from Backend.template_editor_file import TemplateManager

def run(user_name,client):
    manager = TemplateManager(user_name, client)

    columna , columnb = st.columns(2)

    with columna:
        action = st.selectbox("Add/Modify", ["Add New", "Modify Existing"], key=f"action_{user_name}_pre_made")
        if action == "Add New":
            name_template = st.text_input("Name of the Email Template", width="stretch")
            with columnb:
                template = st.text_area("Template", width="stretch", height= 500)
            add_template_btn = st.button("Add Template", use_container_width=True)
            if add_template_btn:
                if not name_template.strip():
                    st.warning("Name of the Email Template is required.")
                elif not template.strip():
                    st.warning("Template is required.")
                else:
                    manager.add_pre_made_template(name_template, template)
                    st.success(" New Email Template Added Successfully")

        if action == "Modify Existing":

            stepnames = manager.list_pre_made_template()
            stepnames_names = [stepname["name"] for stepname in stepnames]
            steps = st.selectbox("Email Template", stepnames_names, width="stretch")
            if steps is not None:
                document = manager.get_pre_made_template(steps)
                with columnb:
                    message_block = st.text_area("Message Block", document["template"], width="stretch", height= 500)

            updatebtn1 = st.button("Update Email Template", use_container_width=True)
            deletebtn1 = st.button("Delete Email Template", use_container_width=True)
            if updatebtn1:
                manager.modify_pre_made_template(steps, message_block)
                st.success("Updated successfully")
            if deletebtn1:
                manager.delete_pre_made_template(steps)
                st.success(f"{steps} deleted Successfully")