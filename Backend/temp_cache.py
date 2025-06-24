import streamlit as st
from pymongo import MongoClient


def run(user_name, client):

    @st.cache_data(show_spinner="Loading data...")
    def get_user_collection_data(user_name, collection_name):
        safe_user_name = user_name.replace(" ", "_")
        db_template = client[f"NVCC_Templates_{safe_user_name}"]
        collection = db_template[collection_name]
        return list(collection.find({}))

    if st.button("🔄 Sync", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


    data_ts = get_user_collection_data(user_name, "Troubleshooting_Templates")
    data_info = get_user_collection_data(user_name, "Information_Templates")
    data_product = get_user_collection_data(user_name, "ProbingQuestion_Templates")
    data_premade = get_user_collection_data(user_name, "Pre_Made_Template")



    return data_ts, data_info, data_product, data_premade
