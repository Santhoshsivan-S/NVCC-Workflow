from Backend import template

def run(Troubleshooting, Information, Probing):

    import streamlit as st

    ts = Troubleshooting
    info = Information
    product = Probing

    def list_all_troubleshooting_names(ts):
        return [item["name"] for item in ts]

    def list_all_product_names(product):
        return [item["name"] for item in product]
    def list_all_info_names(info):
        return [item["name"] for item in info]

    def contextforemail():
        selected_steps = st.multiselect("Select Query/FTR", list_all_troubleshooting_names(ts))
        templates = [item["template"] for item in ts if item["name"] in selected_steps]
        combined_template = "\n\n".join(templates)
        textblockforFTR = st.text_area("Query/FTR", combined_template, height=200,
                                       help="📍Selected Steps from Query or FTR will be added here.\n\n⚠️ Select all the Steps and Continue Editing, else the Editing will be lost.")
        issuepersistcheckbox = st.checkbox("Template[If the issue persists, ]",
                                           help=f"📍 Enable this to include ‘If the issue persists, ’ in the email template.")
        analysetheissuecheckbox = st.checkbox(
            "Template[To analyse the issue better and to determine the cause, I will need additional information:]",
            help="📍 Enable this if you are planning to ask Probing Questions or Requesting Logs")
        escalationStatement = st.checkbox(
            "Template[To check this with our Team and to determine the cause, I will need additional information:]",
            help="📍 Enable this if you are planning to Collect Information and Escalate")

        product_for_Questions = st.multiselect("Probing Questions for", list_all_product_names(product),
                                               help="📝 You have an Option to Select Multiple products to list the Questions")
        questions = [item["questions"] for item in product if item["name"] in product_for_Questions]
        merged_questions = [q for group in questions for q in group]
        probingquestions = st.multiselect("Probing Questions", merged_questions,
                                          help="📍 Select the Questions in the Order you want to ask, the Questions will be Numbered")
        editablequestions = st.text_area("Probing Questions:",
                                         "\n".join(f"{i + 1}. {q}" for i, q in enumerate(probingquestions)),
                                         help="📍 Here you can modify the Questions based on the User Issue")
        requestinfo = st.multiselect("Select the Logs:", list_all_info_names(info),
                                     help="📍 Select the Logs you need from the User to troubleshoot the issue further.")
        template_info = [item["Info"] for item in info if item["name"] in requestinfo]
        combined_template_info = "\n\n".join(f"{i + 1}. {q}" for i, q in enumerate(template_info))
        textareforInfo = st.text_area("Log Request", combined_template_info, height=200,
                                      help="📍Selected Logs from will be added here.\n\n⚠️ Select all the Logs and Continue Editing, else the Editing will be lost.")
        expectingreply = st.checkbox(
            "Template[Please take your time and let me know the results at your earliest convenience.]",
            help="📍 Select Only if you are excepting Reply from the User")

        return textblockforFTR,issuepersistcheckbox,analysetheissuecheckbox,escalationStatement,editablequestions,textareforInfo,expectingreply

    columnA, columnB = st.columns(2)
    with columnA:
        columnAA, columnBB = st.columns(2)
        with columnAA:
            user_name = st.text_input("User Name", help="📍 Enter the name you'd like to include in the signature and introduction.")
        with columnBB:
            template = st.selectbox("Template", ["New", "Updated", "RMA", "Follow-Up", "Feedback"])

        if template == "New":
            type = st.selectbox("Type", ["Query", "Troubleshooting"])
            paraphrase = st.text_input("Paraphrase the Email",
                                       help="📍 Paraphrasing of the email should be mentioned here.")

            if type == "Troubleshooting":
                apology = st.checkbox("Template[I apologise for the inconvenience caused.]",
                                      help=f"📍 Select if you believe User deserves an Apology")
                assurance = st.checkbox("Template[Please be assured that I will do my best to help you further]")
                askToTrySteps = st.checkbox("Template[Please try the following steps and let me know the results:]",
                                            help="📍 Select only if you are providing any steps for the Customer to Try.")
                textblockforFTR, issuepersistcheckbox, analysetheissuecheckbox, escalationStatement, editablequestions, textareforInfo, expectingreply = contextforemail()

                emailTemplate = template.new_troubleshooting_template(user_name, paraphrase, apology, assurance, askToTrySteps,
                                                           troubleshooting=textblockforFTR, persists=issuepersistcheckbox,
                                                           questions=analysetheissuecheckbox, escalation=escalationStatement,
                                                           probingQuestions=editablequestions, info_request=textareforInfo,
                                                           expectingreply=expectingreply)
                st.write(emailTemplate)

