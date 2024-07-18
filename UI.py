import streamlit as st
from Data import add_product, list_products, add_question, list_questions, add_steps, get_steps, list_steps, add_info, get_info, list_info, get_steps_private, get_info_private

st.set_page_config(layout="wide", page_title="NVCC Workflow", page_icon="https://store-images.s-microsoft.com/image/apps.20966.13599037783181022.b05b7adf-6b7a-44ae-9a70-9dc9370ea7e6.4cd88c60-6ff1-4b0f-aed6-8e2efa5629c1")
column_Alpha, column_Beta = st.columns(2)
def contextforemail():
    steps = st.multiselect("Steps", list_steps())
    message_block = st.text_area("Message Block",get_steps(steps))
    privatenotestepsrequest = get_steps_private(steps)
    newstep = st.text_input("Name of the Step")
    privatenotstep = st.text_input("Private Step")
    saveastemplate = st.button("Save As Template")
    if saveastemplate:
        if message_block.strip():
            if newstep.strip():
                result = add_steps(newstep,message_block, privatenotstep)
                st.warning(result)
            else:
                st.warning("Please enter the name of the template")
        else:
            st.warning("Please add the text in message block")
    pCheckbox = st.checkbox("Probing Questions")
    if pCheckbox:
        probingStatement =  "\n\nTo analyze the issue better and to determine the cause, I will need additional information:\n\n"
        probingQuestions = st.selectbox("Probing Questions for", list_products())
        newProduct = st.text_input("Add Product")
        addProduct = st.button("Add")
        if addProduct:
            if newProduct.strip():  # Check if input is not empty
                result = add_product(newProduct.strip())
                st.warning(result)
            else:
                st.warning("Please enter a product name!")
        selectedprobingQuestions = st.multiselect("Select Probing Questions", list_questions(probingQuestions))
        newQuestion = st.text_input("Question")
        addQuestion = st.button("Add Question")
        if addQuestion:
            if newQuestion.strip():  # Check if input is not empty
                result = add_question(probingQuestions,newQuestion.strip())
                st.warning(result)
            else:
                st.warning("Please enter a Question!")
    else:
        probingStatement = ""
        selectedprobingQuestions = ""
    requestinfo = st.multiselect("Request Information", list_info())
    request_information_block = st.text_area("Requested Information", get_info(requestinfo))
    privateinforeq = get_info_private(requestinfo)
    newiNFO = st.text_input("Name of the Information")
    privatenoteinfo = st.text_input("Private Information")
    saveastemplateInfo = st.button("Save Information")
    if saveastemplateInfo:
        if request_information_block.strip():
            if newiNFO.strip():
                result = add_info(newiNFO,request_information_block,privatenoteinfo)
                st.warning(result)
            else:
                st.warning("Please enter the name of the Information")
        else:
            st.warning("Please add the text in Information")

    exceptreply = st.checkbox("Except Reply")
    if exceptreply:
        replyStatement = "I look forward to your reply\n\n"
    else:
        replyStatement = ""

    return message_block,probingStatement,selectedprobingQuestions, request_information_block, replyStatement, privatenotestepsrequest, privateinforeq
with column_Alpha:
    column_A, column_B = st.columns(2)
    with column_A:
        template = st.selectbox("Template", ["New", "Updated", "RMA", "Follow-Up", "Feedback"])

    if template == "New":
        with column_Beta:
            subject = st.text_input("Subject")
        with column_B:
            type = st.selectbox("Type", ["Query", "Troubleshooting", "No-Information"])
        paraphrase = st.text_input("Paraphrase Text")
        if type == "Troubleshooting":
            appology = st.checkbox("Apology")
            if appology:
                statement = "I apologize for the inconvenience caused and please be assured that I will do my best to help you further."
            else:
                statement = ""
            message_blockfc, probingstatement, selectedprobingQuestions, request_information_block, exceptreply, privatestep, privateinfo = contextforemail()
            pQuestions = "\n".join(selectedprobingQuestions)
            emailTemplate = f"Hello,\n\nThank you for contacting NVIDIA Customer Care.\n\nThis is Santhoshsivan, assisting you in troubleshooting the issue you are experiencing.\n\nFrom the description, I understand that {paraphrase}.\n\n{statement}\n\n{message_blockfc}\n\n{probingstatement}{pQuestions}\n\n{request_information_block}\n\nPlease take your time and let me know the results at your earliest convenience. If there are any questions or concerns, feel free to contact me.\n\n{exceptreply}Best regards,\nSanthoshsivan,\nNVIDIA Customer Care "
            privatenote = f"Information (or) Troubleshooting:\n{privatestep}\n\nRequested Information:\n{privateinfo}"
        if type == "Query":
            steps = st.multiselect("Steps", list_steps())
            message_block = st.text_area("Message Block", get_steps(steps))
            privatenotestepsrequest = get_steps_private(steps)
            newstep = st.text_input("Name of the Step")
            privatenotstep = st.text_area("Private Step")
            saveastemplate = st.button("Save As Template")
            if saveastemplate:
                if message_block.strip():
                    if newstep.strip():
                        result = add_steps(newstep, message_block, privatenotstep)
                        st.warning(result)
                    else:
                        st.warning("Please enter the name of the template")
                else:
                    st.warning("Please add the text in message block")
            emailTemplate = f"Hello,\n\nThank you for contacting NVIDIA Customer Care.\n\nThis is Santhoshsivan, assisting you with the Query you have.\n\nFrom the description, I understand that {paraphrase}.\n\n{message_block}\n\nIf there are any questions or concerns, feel free to contact me.\n\nBest regards,\nSanthoshsivan,\nNVIDIA Customer Care"
            privatenote = f"Information (or) Troubleshooting:\n{privatenotestepsrequest}"
    if template == "Updated":
        with column_Beta:
            subject = st.text_input("Subject")
        steps_performed = st.multiselect("Steps Performed", list_steps())
        stepeperfomedprivate = get_steps_private(steps_performed)
        appology = st.checkbox("Apology")
        if appology:
            statement = "\n\nI am sorry the issue still persist, do not worry, I will help you with the issue you are experiencing.\n"
        else:
            statement = ""
        message_blockfc, probingstatement, selectedprobingQuestions, request_information_block, exceptreply, privatestep, privateinfo = contextforemail()
        pQuestions = "\n".join(selectedprobingQuestions)
        emailTemplate = f"Hello,\n\nThank you for taking the time to respond.{statement}\n{message_blockfc}{probingstatement}{pQuestions}\n\n{request_information_block}\nPlease take your time and let me know the results at your earliest convenience. If there are any questions or concerns, feel free to contact me.\n\n{exceptreply}Best regards,\nSanthoshsivan,\nNVIDIA Customer Care "
        privatenote = f"Steps Performed:\n{stepeperfomedprivate}\n\nInformation (or) Troubleshooting:\n{privatestep}\n\nRequested Information:\n{privateinfo}"
    if template == "RMA":
        reason = st.text_input("Reason")
        rmaid = st.text_input("RMA ID")
        complainid = st.text_input("Complaint ID")
        casenumber = st.text_input("Case Number")
        trackinddetails = st.checkbox("Tracking Details")
        if trackinddetails:
            trackimgnumber =f'Tracking Number: {st.text_input("Tracking Number")}\n'
            trackinglink = f'Tracking Link: {st.text_input("Tracking Link")}\n'
        else:
            trackinglink = ""
            trackimgnumber = ""
        emailTemplate = f"Hello Team,\n\n{reason}\n\nRMA ID: {rmaid}\nComplaint ID: {complainid}\nIncident/Case Number: {casenumber}\n\n{trackimgnumber}{trackinglink}\nBest Regards,\nSanthoshsivan Sundaramoorthy"
    if template == "Follow-Up":
        followup_type = st.selectbox("Follow-Up Type", ["Follow-Up 1", "Follow-Up 2"])
        if followup_type == "Follow-Up 1":
            typeFollowup = st.selectbox("Type", ["Query", "No-Information"])
            if typeFollowup == "Query":
                emailTemplate = f"Hello,\n\nThank you for contacting NVIDIA Customer Care.\n\nThis is a follow-up email in reference to your contact to NVIDIA.\n\nPlease let me know if the provided information was helpful and to your satisfaction.\n\nPlease feel free to let us know if you have any questions.\n\nLooking forward for your update. \n\nBest regards,\nSanthoshsivan\nNVIDIA Customer Care "
            if typeFollowup == "No-Information":
                emailTemplate = f"Hello,\n\nThank you for contacting NVIDIA Customer Care.\n\nThis is a follow-up email in reference to your contact to NVIDIA.\n\nI haven't received any updates from you. Kindly let me know if the issue has been resolved.\n\nPlease feel free to let us know if you have any questions.\n\nLooking forward for your update. \n\nBest regards,\nSanthoshsivan\nNVIDIA Customer Care "
        if followup_type == "Follow-Up 2":
            emailTemplate = f"Hello,\n\nThank you for contacting NVIDIA Customer care.\n\nThis is my second follow up to check the status of the issue you had contacted us for.\n\nPlease update us with the requested information so that your issue can be addressed as soon as possible.\n\nPlease note, our database is designed to auto close if we do not hear from you within 72 hours, the status will be changed to Solved.\n\nHence, if you find this case as Solved and if you need further assistance, please submit a new question by clicking the Ask A Question tab:  http://nvidia.custhelp.com/app/utils/login_form/redirect/ask \n\nAlso, once the case is closed the server will automatically trigger a survey to your email address with the subject 'NVIDIA support feedback' asking you to rate my service to you. The rating scale is 1 - 10, where 1 is the least and 10 the best.\n\nPlease participate in this short survey and survey rating below 8 indicates your dissatisfaction over the assistance that you have received by me.\n\nIf that's the case; please let me know and I shall help you troubleshoot further.\n\nI realize that your time is extremely valuable and I appreciate your feedback.\n\nRegards, \nSanthoshsivan,\nNVIDIA Customer Care "
    if template == "Feedback":
        emailTemplate = "Hello,\n\nThank you for your update, Glad to know that the issue you were having is fixed and we do appreciate your efforts in troubleshooting the issue.\n\nWe shall go ahead and move the case to Resolved with your consent.\n\nHowever, if in case you have any further queries in future you can always reply back to me over the e-mail and we will be happy to help you further.\n\nI would also like to inform you that shortly you will receive an email survey from NVIDIA asking you to rate our service on a scale of 1-10, rating 10 indicates that you were happy with the support and any rating below 8 indicates that you were not satisfied with the service.\n\nPlease take a minute and rate our service.\n\nThank you once again for contacting NVIDIA Customer Care and giving us an opportunity to serve you.\n\nHave a Nice Day!\n\nBest regards,\nSanthoshsivan,\nNvidia Customer Care"

with column_Beta:
    st.write("Email Template:")
    email = st.code( emailTemplate, language=None)

    if template == "Updated" or template == "New":
        st.write("Private Note:")
        operatingSystem = st.selectbox("Operating System", ["Other", "Windows", "Linux", "Android", "MacOS", "IOS"])
        product = st.selectbox("Product", list_products())
        status = st.selectbox("Status", ["Waiting", "Solved", "Unresolved", "Escalated - L1.5", "Researching"])
        note = st.code(
            f"Email:\n\n\nSubject: {subject}\n\nProduct: {product}\nOS: {operatingSystem}\n\n{privatenote}\n\n\nStatus: {status}",
            language=None)


