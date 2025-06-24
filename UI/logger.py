


def run(user_name, client):
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi
    import streamlit as st
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta
    import plotly.graph_objects as go

    safe_user_name = user_name.replace(" ", "_")
    db_dailyTracker = client[f"NVCC_Daily_Tracker_{safe_user_name}"]
    collections_calls = db_dailyTracker["Calls"]
    collections_Emails = db_dailyTracker["Emails"]
    collections_Chats = db_dailyTracker["Chats"]
    collections_Misc = db_dailyTracker["Misc"]
    collections_Resolved = db_dailyTracker["Resolved"]
    collections_FollowUp = db_dailyTracker["FollowUp"]


    column1, column2, column3 = st.columns(3)

    def data(collection,date,mode):

        if "reset_form" in st.session_state and st.session_state.reset_form:
            st.session_state["n2"] = False
            st.session_state["i1"] = ""
            st.session_state["p1"] = 'GeForce graphics'
            st.session_state["s1"] = ""
            st.session_state["o1"] = 'Other'
            st.session_state["s2"] = 'Researching'
            st.session_state["s3"] = False
            st.session_state["s4"] = 'Self'
            st.session_state["v1"] = None
            st.session_state.reset_form = False

        if st.button("Clear Form"):
            st.session_state.reset_form = True
            st.rerun()


        with st.form("Daily Tracker Entry"):

            n1 = st.selectbox("Name:", [user_name])
            n2 = st.checkbox("New", key="n2")
            i1 = st.text_input("Incident ID:", key="i1")
            p1 = st.selectbox("Product:",
                              ['GeForce graphics', 'NVIDIA Branded GPU', 'Promo Code', 'DGX-1', 'GeForce Experience',
                               'NVIDIA App', 'GeForce NOW', 'SHIELD TV (2015/ 2017)', 'SHIELD TV (2019)',
                               'Shield Tablet', 'Shield Portable', 'Quadro graphics', 'GRID', 'Jetson', 'Tegra',
                               '3D Vision', '3DTV Play', 'Tesla', 'PureVideo Decoder', 'nForce', 'Other'], key="p1")
            s1 = st.text_input("Subject:", key= 's1')
            o1 = st.selectbox("Operating System:",
                              ['Win 11', 'Win XP', 'Win Vista', 'Win 7', 'Win 8', 'Win 10', 'Win Server', 'Other',
                               'MAC OSX', 'Android', 'Linux'], key= "01")
            s2 = st.selectbox("Status:",
                              ['Waiting', 'Resolved', 'Unresolved', 'Escalated-L1.5', 'Escalated-L2', 'Researching'],
                              key="s2")
            s3 = st.checkbox("Send Survey Now", key='s3')
            if mode != "Call":
                s4 = st.selectbox("Source:", ['Zendesk', 'Self', 'L1.5', 'Others'], key='s4')
            else:
                s4 = None
            v1 = st.selectbox("Volume Trend:", ["CS", "TS"], key="v1")
            submitted = st.form_submit_button("Add")
            if submitted:
                if not i1.strip():
                    st.warning("Incident ID is required.")
                elif not s1.strip():
                    st.warning("Subject is required.")
                elif not n1:
                    st.warning("Name must be selected.")
                elif not p1:
                    st.warning("Product must be selected.")
                elif not o1:
                    st.warning("Operating System must be selected.")
                elif not s2:
                    st.warning("Status must be selected.")
                elif not v1:
                    if p1 == "GeForce NOW":
                        st.warning("Volume Trend must be selected for GeForce Now.")
                else:
                    if s3:
                        s3 = "Yes"
                    else:
                        s3 = None

                    d1 = f"{date.day}-{date.strftime('%b')}-{date.strftime('%y')}"

                    entry = {
                        "Date": d1,
                        "Name": n1,
                        "Ref #": i1,
                        "Product": p1,
                        "Call Synopsis": s1,
                        "OS": o1,
                        "Status": s2,
                        "Send Survey Now": "Yes" if s3 else None,
                        "Vol Trend - CS/ TS": v1,
                    }
                    if s4 is not None:
                        entry["Source"] = s4

                    def format_date(d):
                        return f"{d.day}-{d.strftime('%b')}-{d.strftime('%y')}"

                    if n2:
                        if s2 in ["Waiting", "Researching"]:
                            date_dt = datetime.combine(date, datetime.min.time())

                            # Follow-up dates
                            Follow_Up_1 = date_dt + timedelta(days=2)
                            Follow_Up_2 = date_dt + timedelta(days=4)
                            Follow_Up_3 = date_dt + timedelta(days=6)

                            entry_FollowUp = {
                                "Date": d1,
                                "Name": n1,
                                "Ref #": i1,
                                "Follow-Up 1 Date": format_date(Follow_Up_1),
                                "Follow-Up 2 Date": format_date(Follow_Up_2),
                                "Follow-Up 3 Date": format_date(Follow_Up_3),
                                "Status": s2
                            }

                            collections_FollowUp.insert_one(entry_FollowUp)
                            st.success("Follow-up dates added")
                    elif collections_FollowUp.find_one({"Ref #": i1}):
                            if s2 in ["Waiting", "Researching"]:
                                if mode != "Misc":
                                    date_dt = datetime.combine(date, datetime.min.time())

                                    # Follow-up dates
                                    Follow_Up_1 = date_dt + timedelta(days=2)
                                    Follow_Up_2 = date_dt + timedelta(days=4)
                                    Follow_Up_3 = date_dt + timedelta(days=6)

                                    entry_FollowUp_Update = {
                                        "Date": d1,
                                        "Name": n1,
                                        "Ref #": i1,
                                        "Follow-Up 1 Date": format_date(Follow_Up_1),
                                        "Follow-Up 2 Date": format_date(Follow_Up_2),
                                        "Follow-Up 3 Date": format_date(Follow_Up_3),
                                        "Status": s2
                                    }
                                    collections_FollowUp.update_one({"Ref #": i1}, {"$set": entry_FollowUp_Update})
                                    st.success(f"Follow Up Modified for {i1}")


                    # Insert into main collection
                    collection.insert_one(entry)
                    st.success("Data added to the Tracker")


                    # Add to Resolved if needed
                    if s2 == "Resolved":
                        if not collections_Resolved.find_one({"Ref #": i1}):
                            collections_Resolved.insert_one(entry)
                            # Delete the corresponding FollowUp entry if it exists
                            if collections_FollowUp.find_one({"Ref #": i1}):
                                collections_FollowUp.delete_one({"Ref #": i1})
                                st.success(f"{i1} is removed from the Follow Up Tracker")
                            st.success("Added to Resolved")








    with column1:
        d1_obj = st.date_input("Date:")  # This is a datetime.date object
        m1 = st.selectbox("Mode:", ['Call', 'Email', 'Chat', 'Misc'])
        if m1 == 'Call':
            data(collections_calls, d1_obj, m1)
        elif m1 == 'Email':
            data(collections_Emails, d1_obj, m1)
        elif m1 == 'Chat':
            data(collections_Chats, d1_obj, m1)
        elif m1 == 'Misc':
            data(collections_Misc, d1_obj, m1)

    with column2:


        d1 = f"{d1_obj.day}-{d1_obj.strftime('%b')}-{d1_obj.strftime('%y')}"

        # Build regex patterns to match end of the string
        current_pattern = f"-{d1_obj.strftime('%b')}-{d1_obj.strftime('%y')}$"


        def count_by_month(collection, pattern):
            return collection.count_documents({"Date": {"$regex": pattern}})

        calls_current = count_by_month(collections_calls, current_pattern)
        emails_current = count_by_month(collections_Emails, current_pattern)
        chats_current = count_by_month(collections_Chats, current_pattern)
        resolved_current = count_by_month(collections_Resolved, current_pattern)

        total_current_month = calls_current + emails_current + chats_current

        if total_current_month != 0:
            current_resolution_rate = round((resolved_current / total_current_month) * 100, 2)
        else:
            current_resolution_rate = 0

        def count_by_date(collection, date_str):
            return collection.count_documents({"Date": date_str})

        call_count = count_by_date(collections_calls, d1)
        email_count = count_by_date(collections_Emails, d1)
        chat_count = count_by_date(collections_Chats, d1)
        misc_count = count_by_date(collections_Misc, d1)
        resolved_count = count_by_date(collections_Resolved, d1)

        total_production_day = call_count + email_count + chat_count
        if total_production_day != 0:
            resolution_rate_day = round((resolved_count / total_production_day) * 100, 2)
        else:
            resolution_rate_day = 0

        target_cases_per_day = 50
        resolved_case_per_day = 15

        fig = go.Figure(go.Indicator(
            domain={'x': [0.2, 0.8], 'y': [0.2, 0.8]},
            value=total_production_day,
            mode="gauge+number+delta",
            title={'text': "Daily Production"},
            delta={'reference': 40, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
            gauge={
                'axis': {'range': [None, target_cases_per_day], 'tickwidth': 1, 'tickcolor': "black"},
                'bar': {'color': '#f0fff4'},  # soft green bar
                'steps': [
                    {'range': [0, 35], 'color': '#ffcccc'},
                    {'range': [35, 40], 'color': '#ffe680'},
                    {'range': [40, 50], 'color': '#b6fcd5'}
                ],
                'threshold': {
                    'line': {'color': "#ff69b4", 'width': 8},  # Hot pink threshold for the drama
                    'thickness': 0.9,
                    'value': 40
                }
            }
        ))

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")  # separator line
        col1, col2= st.columns(2)
        col1.metric("🎯 Resolution Rate for the Day", f"{resolution_rate_day}%",
                    delta=round(resolution_rate_day - 30, 2), delta_color="normal")
        col2.metric("✅ Resolved Count", resolved_count,
                    delta=resolved_count - resolved_case_per_day, delta_color="normal")
        col2.metric("📊 Over All Production", total_current_month,
                    delta=total_current_month - 1000, delta_color="normal")

        st.markdown("<div style='text-align:center; padding-top: 1rem;'>", unsafe_allow_html=True)
        col1.metric("📈 Over All Resolution Rate", f"{current_resolution_rate}%",
                  delta=round(current_resolution_rate - 30, 2), delta_color="normal")
        st.markdown("</div>", unsafe_allow_html=True)

    with column3:

        fup1 = collections_FollowUp.find({"Follow-Up 1 Date": d1})
        fup2 = collections_FollowUp.find({"Follow-Up 2 Date": d1})
        fup3 = collections_FollowUp.find({"Follow-Up 3 Date": d1})

        fup1_ids = [doc["Ref #"] for doc in fup1]
        fup2_ids = [doc["Ref #"] for doc in fup2]
        fup3_ids = [doc["Ref #"] for doc in fup3]

        st.subheader(f"Follow-Ups Scheduled for Today", anchor=False)

        with st.expander(f"📌 Follow-Up 1 - Count: {len(fup1_ids)}"):
            if fup1_ids:
                for ref in fup1_ids:
                    st.markdown(f"- {ref}")
            else:
                st.write("No Follow-Up 1 scheduled.")

        with st.expander(f"📌 Follow-Up 2 - Count: {len(fup2_ids)}"):
            if fup2_ids:
                for ref in fup2_ids:
                    st.markdown(f"- {ref}")
            else:
                st.write("No Follow-Up 2 scheduled.")

        with st.expander(f"📌 Follow-Up 3 - Count: {len(fup3_ids)}"):
            if fup3_ids:
                for ref in fup3_ids:
                    st.markdown(f"- {ref}")
            else:
                st.write("No Follow-Up 3 scheduled.")

        st.info("""
        ### 📝 Note

        - 🔒 **Follow-Up dates will not be modified** when adding a case into *Misc* with status **Waiting** or **Researching**.  
          This ensures all three follow-ups are completed properly.

        - ✅ **Follow-Up incidents will be removed** when the status is **Marked as Resolved**.

        - ⚠️ **When adding a new follow-up case**, make sure to **check the 'New' checkbox**,  
          otherwise the case will **not** be added to the Follow-Up Tracker.

        - 🔄 **When working on others' updates or updating an existing follow-up**,  
          make sure to **uncheck the 'New' checkbox**, unless you intend to follow up on their update.
        """)





