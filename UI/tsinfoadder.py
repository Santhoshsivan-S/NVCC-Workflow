import streamlit as st
from Backend.template_editor_file import TemplateManager

def run(user_name,client):
    manager = TemplateManager(user_name, client)
    action = st.selectbox("Add/Modify", ["Add New", "Modify Existing"], key=f"action_{user_name}_ts")

    #Layout
    column_a , column_b = st.columns(2)
    column1 , column2 = st.columns(2)




    if action == "Add New":
        with column_a:
            st.subheader("Troubleshooting", anchor=False)
            name_ts = st.text_input("Name of the Troubleshooting Step", width="stretch")
            template = st.text_area("Template", width="stretch")
            add_ts_btn = st.button("Add T/S", use_container_width=True)
            if add_ts_btn:
                if not name_ts.strip():
                    st.warning("Name of the Troubleshooting Step is required.")
                elif not template.strip():
                    st.warning("Template is required.")
                else:
                    manager.add_new_troubleshooting(name_ts, template)
                    st.success(" New T/S Added Successfully")


        with column_b:
            st.subheader("Information", anchor=False)
            name_info = st.text_input("Name of the Information", width="stretch")
            template_info = st.text_area("Information", width="stretch")
            btninfo = st.button("Add Information", use_container_width=True)
            if btninfo:
                if not name_info.strip():
                    st.warning("Name of the Information is required.")
                elif not template_info.strip():
                    st.warning("Information is required.")

                else:
                    manager.add_new_information(name_info, template_info)
                    st.success(" New Information Added Successfully")

        with column1:
            st.subheader("Product", width="stretch", anchor=False)
            product_name = st.text_input("Name of the Product", width="stretch")
            add_product_btn = st.button("Add Product", use_container_width=True)
            if add_product_btn:
                if not product_name.strip():
                    st.warning("Name of the Product is required.")
                else:
                    manager.add_new_product(product_name)
                    st.success("Product added Successfully")

        with column2:
            st.subheader("Questions", width="stretch", anchor=False)
            product_names = manager.list_product()
            product_names_list = [product["name"] for product in product_names]
            product = st.selectbox("Product Name", product_names_list)
            questions = st.text_input("Probing Question")
            add_question = st.button("Add Question", use_container_width=True)
            if add_question:
                if not product.strip():
                    st.warning("Select the Product")
                elif not questions.strip():
                    st.warning("Probing Question is Required")
                else:
                    product_document = manager.find_questions(product)
                    if isinstance(product_document.get("questions", []), str):
                        questions_list = [q.strip() for q in product_document["questions"].split("\n") if q.strip()]
                        manager.add_questions_set(product, questions_list)
                    manager.add_questions_add_to_set(product, questions)
                    st.success("Question added successfully")



    if action == "Modify Existing":
        with column_a:
            st.subheader("Troubleshooting", anchor=False)
            stepnames = manager.list_ts_names()
            stepnames_names = [stepname["name"] for stepname in stepnames]
            steps = st.selectbox("T/S Name", stepnames_names, width="stretch")
            if steps is not None:
                document = manager.get_ts_template(steps)
                message_block = st.text_area("Message Block", document["template"], width="stretch")

            updatebtn1 = st.button("Update T/S", use_container_width=True)
            deletebtn1 = st.button("Delete T/S", use_container_width=True)
            if updatebtn1:
                manager.modify_troubleshooting(steps,message_block)
                st.success("Updated successfully")
            if deletebtn1:
                manager.delete_troubleshooting(steps)
                st.success(f"{steps} deleted Successfully")
        with column_b:
            st.subheader("Information", anchor=False)
            infoname = manager.list_info_names()
            stepnames_names = [stepname["name"] for stepname in infoname]
            steps = st.selectbox("Info Name", stepnames_names, width="stretch")
            if steps is not None:
                document = manager.get_info_template(steps)
                message_block = st.text_area("Message Block", document["Info"], width="stretch", key=f"message_block_{document['_id']}")

            updatebtn2 = st.button("Update Information", use_container_width=True)
            deletebtn2 = st.button("Delete Information", use_container_width=True)
            if updatebtn2:
                manager.modify_information(steps,message_block)
                st.success("Updated successfully")
            if deletebtn2:
                manager.delete_information(steps)
                st.success(f"{steps} deleted Successfully")
        with column1:
            st.subheader("Product", width="stretch", anchor=False)
            productnames = manager.list_product()
            productnames_names = [productnames["name"] for productnames in productnames]
            prod = st.selectbox("Product Name", productnames_names)
            deletebtn765 = st.button("Delete Product", use_container_width=True)
            if deletebtn765:
                manager.delete_product(prod)
        with column2:
            st.subheader("Questions", width="stretch", anchor=False)
            productnames = manager.list_product()
            productnames_names = [productnames["name"] for productnames in productnames]
            prod = st.selectbox("Product", productnames_names)
            product1 = manager.find_questions(prod)
            if product1 is not None:
                Que = st.selectbox("Questions List", product1["questions"])
            delQ = st.button("Delete the Question", use_container_width=True)

            if delQ:
                manager.delete_question(prod,Que)




