import streamlit as st

def run(data):
    names = [item['name'] for item in data]
    selected_name = st.selectbox("Select the Template Name:", names)
    template = next((item['template'] for item in data if item['name'] == selected_name), None)
    st.write(f"Template for {selected_name}")
    st.code(template, language=None, height= 500)