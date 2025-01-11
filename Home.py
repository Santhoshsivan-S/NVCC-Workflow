import os

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from troubleshooting import *
from products import *
from questions import *
from information import *
from template import *
st.set_page_config(layout="wide", page_title="NVCC Workflow", page_icon="https://store-images.s-microsoft.com/image/apps.20966.13599037783181022.b05b7adf-6b7a-44ae-9a70-9dc9370ea7e6.4cd88c60-6ff1-4b0f-aed6-8e2efa5629c1")
from yaml.loader import SafeLoader

file_path = 'config.yaml'
if not os.path.exists(file_path):
    config_data = {
        'cookie': {
            'expiry_days': 30,
            'key': 'JusticeSantz# Must be a string',
            'name': 'Santhoshsivansundaramoorthy'
        },
        'credentials': {
            'usernames': {
                'ADMIN': {
                    'email': 'admin',
                    'first_name': 'Santhoshsivan',
                    'last_name': 'Sundaramoorthy',
                    'logged_in': False,
                    'password': '$2b$12$YdetO4BKPfrYI6juawfYp.t89abBXt0QOFJnMiiL.8ZrlM2DddRKu',
                    'password_hint': 'Suhail',
                    'roles': ['User']
                }
            }
        },
        'pre-authorized': {
            'emails': None
        }
    }

    # Define the path where the YAML file will be saved

    # Write the data to the YAML file
    with open(file_path, 'w') as file:
        yaml.dump(config_data, file, default_flow_style=False)


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

def newuser():
    try:
        with st.sidebar:
            st.html("""<h1 style=" text-align: center; color: #76b900; font-family: 'Courier New', Courier, monospace;">Sign Up</h1>""")
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
            pre_authorized=config['pre-authorized']['emails'], location='sidebar', captcha=False, domains= ['nvidia.com'],fields={'Form name':'', 'Email':'Email', 'Username':'Username', 'Password':'Password', 'Repeat password':'Repeat password', 'Password hint':'Password hint', 'Captcha':'Captcha', 'Register':'Sign Up'}, roles= ["User"],merge_username_email=True,clear_on_submit=False,key= 'Register user' )
        if email_of_registered_user:
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


if not st.session_state['authentication_status'] :
    st.html("""
        <div style="text-align: center;">
            <img src="https://www.nvidia.com/content/nvidiaGDC/us/en_US/about-nvidia/legal-info/logo-brand-usage/_jcr_content/root/responsivegrid/nv_container_392921705/nv_container/nv_image.coreimg.100.630.png/1703060329053/nvidia-logo-vert.png" alt="NVIDIA Logo" width="200"/>
            <h1 style="color: #76b900; font-family: 'Courier New', Courier, monospace;">Customer Care - WorkFlow</h1>
        </div>
    """)

authenticator.login(fields={'Form name':'Sign In', 'Username':'Email', 'Password':'Password', 'Login':'Sign In', 'Captcha':'Captcha'},max_login_attempts=5)

if st.session_state['authentication_status']:
    name = st.session_state["name"].split()[0]
    with st.sidebar:
        st.html("""
                <div style="text-align: center;">
                    <img src="https://www.nvidia.com/content/nvidiaGDC/us/en_US/about-nvidia/legal-info/logo-brand-usage/_jcr_content/root/responsivegrid/nv_container_392921705/nv_container/nv_image.coreimg.100.630.png/1703060329053/nvidia-logo-vert.png" alt="NVIDIA Logo" width="200"/>
                    <h1 style="color: #76b900; font-family: 'Courier New', Courier, monospace; font-size: 15
                    px">Customer Care WorkFlow</h1>
                </div>
            """)
        st.write(f'Hey, **{st.session_state["name"]}**')
        settings = st.selectbox("Update/Modify", ["", "Account Details", "Security/Password"])
        if settings == "Account Details":
            if st.session_state['authentication_status']:
                try:
                    if authenticator.update_user_details(st.session_state['name'], fields={'Form name':'Account'}):
                        with open('config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        st.success('Entries updated successfully')
                except Exception as e:
                    st.error(e)
        if settings == "Security/Password":
            if st.session_state['authentication_status']:
                try:
                    if authenticator.reset_password(st.session_state['username']):
                        with open('config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        st.success('Password modified successfully')
                except Exception as e:
                    st.error(e)

        authenticator.logout()
    emailComposer,infoUpdater = st.tabs(["Email Generator", "Update/Add Information"])
    with emailComposer:
        def contextforemail():
            steps = st.multiselect("Steps", list_troubleshooting_names())
            message_block = st.text_area("Message Block", get_troubleshooting_steps(steps))

            presistant = st.checkbox("Issue Persists", help="If the issue persists, ")
            probingStatement = st.checkbox("Request Info Statement",
                                               help="To analyse the issue better and to determine the cause, I will need additional information:")
            escalationStatement = st.checkbox("Escalation Statement",
                                                  help="To check this with our Team and to determine the cause, I will need additional information:")
            probingQuestions = st.selectbox("Probing Questions for", list_products())
            selectedprobingQuestions = st.multiselect("Select Probing Questions", list_questions(probingQuestions))
            requestinfo = st.multiselect("Request Information", list_info_names())
            request_information_block = st.text_area("Requested Information", get_info(requestinfo))
            expectingreply = st.checkbox("Expecting Reply",
                                         help="Please take your time and let me know the results at your earliest convenience.")

            return message_block, presistant, escalationStatement, probingStatement, selectedprobingQuestions, request_information_block, expectingreply

        column_Alpha, column_Beta = st.columns(2)
        with column_Alpha:
            column_A, column_B = st.columns(2)
            with column_A:
                template = st.selectbox("Template", ["New", "Updated", "RMA", "Follow-Up", "Feedback"])

            if template == "New":
                email = st.text_area("Email for Paraphrasing:", help= "Paste the email for Paraphrasing.")
                with column_B:
                    type = st.selectbox("Type", ["Query", "Troubleshooting"])
                paraphrase = st.text_input("Paraphrase Text", email)
                if type == "Troubleshooting":
                    Charlie1, Charlie2, Charlie3 = st.columns(3)
                    with Charlie1:
                        apology = st.checkbox("Apology", help=f"SENTENCE: I apologise for the inconvenience caused.")
                    with Charlie2:
                        assurance = st.checkbox("Assurance", help="SENTENCE: Please be assured that I will do my best to help you further.")
                    with Charlie3:
                        askToTrySteps = st.checkbox("FTR", help="SENTENCE: Please try the following steps and let me know the results:")
                    troubleshooting, persists, escalation, questions ,probingquestions, inforequest, expectingreply= contextforemail()
                    pQuestions = "\n".join(f"{i + 1}. {q}" for i, q in enumerate(probingquestions))
                    emailTemplate = newtroubleshootingtemplate(name, paraphrase, apology, assurance, askToTrySteps, troubleshooting= troubleshooting,persists=persists,questions=questions,escalation=escalation,probingQuestions=pQuestions,info_request= inforequest,expectingreply=expectingreply)
                if type == "Query":
                    Charlie1, Charlie2, Charlie3 = st.columns(3)
                    with Charlie1:
                        apology = st.checkbox("Apology", help=f"SENTENCE: I apologise for the inconvenience caused.")
                    with Charlie2:
                        assurance = st.checkbox("Assurance",
                                                help="SENTENCE: Please be assured that I will do my best to help you further.")
                    with Charlie3:
                        askToTrySteps = st.checkbox("FTR",
                                                    help="SENTENCE: Please try the following steps and let me know the results:")
                    steps = st.multiselect("Steps", list_troubleshooting_names())
                    message_block = st.text_area("Edit or Modify the selected Steps", get_troubleshooting_steps(steps), help="Usage: The selected steps will be displayed here and can be adjusted as needed based on the Scenario.\n\nImportant Note: If a new step is chosen after modifying the existing ones, all previous modifications will be erased.")
                    emailTemplate = newQueryTemplate(name, paraphrase, apology, assurance, askToTrySteps, message_block)
            if template == "Updated":
                Charlie1, Charlie2, Charlie3 = st.columns(3)
                with Charlie1:
                    apology = st.checkbox("Apology", help=f"SENTENCE: I am sorry the issue still persist. ")
                with Charlie2:
                    assurance = st.checkbox("Assurance",
                                            help="SENTENCE: Please be assured that I will do my best to help you further.")
                with Charlie3:
                    askToTrySteps = st.checkbox("FTR",
                                                help="SENTENCE: Please try the following steps and let me know the results:")
                troubleshooting, persists, escalation, questions, probingquestions, inforequest, expectingreply = contextforemail()
                pQuestions = "\n".join(f"{i + 1}. {q}" for i, q in enumerate(probingquestions))
                emailTemplate = Updatedtroubleshootingtemplate(name, apology, assurance, askToTrySteps,
                                                           troubleshooting=troubleshooting, persists=persists,
                                                           questions=questions, escalation=escalation,
                                                           probingQuestions=pQuestions, info_request=inforequest,
                                                           expectingreply=expectingreply)
            if template == "RMA":
                reason = st.text_input("Reason")
                rmaid = st.text_input("RMA ID")
                complainid = st.text_input("Complaint ID")
                casenumber = st.text_input("Case Number")
                trackinddetails = st.checkbox("Tracking Details")
                if trackinddetails:
                    trackimgnumber = st.text_input("Tracking Number")
                    trackinglink = st.text_input("Tracking Link")
                else:
                    trackinglink = ""
                    trackimgnumber = ""
                emailTemplate = rma(name, reason,rmaid, complainid,casenumber, trackinddetails, trackimgnumber, trackinglink )
            if template == "Follow-Up":
                followup_type = st.selectbox("Follow-Up Type", ["Follow-Up 1", "Follow-Up 2"])
                if followup_type == "Follow-Up 1":
                    typeFollowup = st.selectbox("Type", ["Query", "No-Reply after Troubleshooting"])
                    if typeFollowup == "Query":
                        emailTemplate = followupone(name,typeFollowup)
                    if typeFollowup == "No-Reply after Troubleshooting":
                        emailTemplate = followupone(name,typeFollowup)
                if followup_type == "Follow-Up 2":
                    emailTemplate = followuptwo(name)
            if template == "Feedback":
                emailTemplate=feedback(name)
        with column_Beta:
            st.write("Email Template:")
            email = st.code(emailTemplate, language=None)


elif st.session_state['authentication_status'] is False:
    newuser()
    st.error('Email/password is incorrect')
elif st.session_state['authentication_status'] is None:
    newuser()



