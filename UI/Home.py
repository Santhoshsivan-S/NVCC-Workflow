from Backend import temp_cache
from UI import tsinfoadder, premadeEmail, underdevelopment, readytouseemailtemplate, logger, viewer, manual_drafter




def run(user_name):
    import streamlit as st
    from pymongo import MongoClient

    uri = st.secrets['api_keys']['MONGO_URI1']

    client = MongoClient(uri)




    daily_tracker, email_drafter, template_editor, Case_notes_creator = st.tabs(
        ["Daily Tracker", "Email Drafter", "Template Editor", "Case Notes Generator"])

    with Case_notes_creator:
        underdevelopment.run()

    with email_drafter:
        Troubleshooting, Information, Probing, Pre_made = temp_cache.run(user_name,client)
        st.info("""IF YOU MAKE **ANY CHANGES** IN THE **TEMPLATE EDITOR**, PLEASE MAKE SURE TO PRESS **'🔄 Sync'** TO APPLY THE UPDATES.
        """)

        manual, automated, pre_made = st.tabs(["Manual Drafting", " Draft using AI", "Ready to Use Template"])
        with automated:
            underdevelopment.run()
        with pre_made:
            readytouseemailtemplate.run(Pre_made)
        with manual:
            manual_drafter.run(Troubleshooting, Information, Probing)
    with daily_tracker:
        add_data, view_data = st.tabs(["Logger", "Viewer"])
        with add_data:
            logger.run(user_name,client)
        with view_data:
            viewer.run(user_name, client)

    with template_editor:
        steps_adder, ready_template = st.tabs(["Information, Troubleshooting and Probing Template", "Ready to Use Email Template Editor"])

        with steps_adder:
            tsinfoadder.run(user_name, client)
        with ready_template:
            premadeEmail.run(user_name, client)
