
def run(user_name,client):
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi
    import streamlit as st
    import pandas as pd

    st.warning("""
    ### ⚠️ Important

    You may **only view your data** here.  
    The data is **not loaded into your Daily Tracker Excel sheet**.

    📊 The data shown here is only used for **charts** and **follow-up reminders** for easy access.

    📋 You are expected to **copy and paste** this information at the end of the day for the internal team to see it.
    """)

    # DB and collections
    safe_user_name = user_name.replace(" ", "_")
    db_dailyTracker = client[f"NVCC_Daily_Tracker_{safe_user_name}"]
    collections_calls = db_dailyTracker["Calls"]
    collections_Emails = db_dailyTracker["Emails"]
    collections_Chats = db_dailyTracker["Chats"]
    collections_Misc = db_dailyTracker["Misc"]
    collections_Resolved = db_dailyTracker["Resolved"]
    collections_FollowUp = db_dailyTracker["FollowUp"]

    collection_dict = {
        "Calls": collections_calls,
        "Emails": collections_Emails,
        "Chats": collections_Chats,
        "Misc": collections_Misc,
        "Resolved": collections_Resolved,
        "FollowUp": collections_FollowUp,
    }

    selected_collection_name = st.selectbox("Select Collection", list(collection_dict.keys()))
    collection = collection_dict[selected_collection_name]

    # Desired column orders
    column_orders = {
        "Calls": ["Date", "Name", "Ref #", "Product", "Call Synopsis", "OS", "Status", "Send Survey Now",
                  "Vol Trend - CS/ TS"],
        "Emails": ["Date", "Name", "Ref #", "Product", "Call Synopsis", "OS", "Status", "Send Survey Now", "Source",
                   "Vol Trend - CS/ TS"],
        "Chats": ["Date", "Name", "Ref #", "Product", "Call Synopsis", "OS", "Status", "Send Survey Now", "Source",
                  "Vol Trend - CS/ TS"],
        "Misc": ["Date", "Name", "Ref #", "Product", "Call Synopsis", "OS", "Status", "Send Survey Now", "Source",
                 "Vol Trend - CS/ TS"],
        "Resolved": ["Date", "Name", "Ref #", "Product", "Call Synopsis", "OS", "Status", "Send Survey Now"],
        "Follow-up": ["Date", "Name", "Ref #", "Follow-Up 1 Date", "Follow-Up 2 Date", "Follow-Up 3 Date", "Status"]
    }

    # Filter option
    filter_type = st.radio("Select Filter Type", ["All", "By Date"])

    # Filter logic
    if filter_type == "By Date":
        selected_date = st.date_input("Select Date")
        d1 = f"{selected_date.day}-{selected_date.strftime('%b')}-{selected_date.strftime('%y')}"
        query = {"Date": d1}
    else:
        query = {}

    # Fetch data
    data = list(collection.find(query))
    for doc in data:
        doc.pop("_id", None)

    # Display
    if data:
        df = pd.DataFrame(data)

        # Apply column order if defined
        columns = column_orders.get(collection)
        if columns:
            for col in columns:
                if col not in df.columns:
                    df[col] = ""  # Add missing columns as empty
            df = df[columns]  # Reorder

        st.success(f"Showing {len(df)} record(s).")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data found.")
