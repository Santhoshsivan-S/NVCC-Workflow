from http.client import responses


def newQueryTemplate(name,paraphrase,apology, assurance, askToTrySteps, troubleshooting):

    apology = apology
    if apology:
        apologyStatement = "\nI apologise for the inconvenience caused."
    else:
        apologyStatement = ""

    assurance = assurance
    if assurance:
        assuranceStatement = "Please be assured that I will do my best to help you further.\n"
    else:
        assuranceStatement = ""

    askToTrySteps = askToTrySteps
    if askToTrySteps:
        askToTryStepsStatement = "\nPlease try the following steps and let me know the results:\n"
    else:
        askToTryStepsStatement = ""
    responses = f"Hello,\n\nThank you for contacting NVIDIA Customer Care. This is {name}, and I'll be answering your Query.\n\nFrom the description, I understand that {paraphrase}{apologyStatement} {assuranceStatement}{askToTryStepsStatement}{troubleshooting}\nIf there are any questions or concerns, feel free to contact me.\n\nBest Regards,\n{name}\nNVIDIA Customer Care"

    return responses

def newtroubleshootingtemplate(name,paraphrase,apology, assurance, askToTrySteps, troubleshooting, persists, questions, escalation, probingQuestions, info_request, expectingreply):
    apology = apology
    if apology:
        apologyStatement = "\n\nI apologise for the inconvenience caused. "
    else:
        apologyStatement = ""

    assurance = assurance
    if assurance:
        assuranceStatement = "Please be assured that I will do my best to help you further.\n"
    else:
        assuranceStatement = ""

    askToTrySteps = askToTrySteps
    if askToTrySteps:
        askToTryStepsStatement = "\nPlease try the following steps and let me know the results:\n"
    else:
        askToTryStepsStatement = ""

    persists = persists
    if persists:
        persistsStatement = "\nIf the issue persists, "
    else:
        persistsStatement = ""

    questions = questions
    if questions:
        questionsStatement = "To analyse the issue better and to determine the cause, I will need additional information:\n"
    else:
        questionsStatement = ""
    escalation = escalation
    if escalation:
        escalationStatement = "To check this with our Team and to determine the cause, I will need additional information:\n"
    else:
        escalationStatement = ""

    if expectingreply:
        expectingreplyStatement = "\nPlease take your time and let me know the results at your earliest convenience.\n"
    else:
        expectingreplyStatement = ""

    responses = f"Hello,\n\nThank you for contacting NVIDIA Customer Care. This is {name}, and I'll be answering your Query.\n\nFrom the description, I understand that {paraphrase}{apologyStatement} {assuranceStatement}{askToTryStepsStatement}{troubleshooting}{persistsStatement}{questionsStatement}{escalationStatement}{probingQuestions}\n{info_request}{expectingreplyStatement}If there are any questions or concerns, feel free to contact me.\n\nBest Regards,\n{name}\nNVIDIA Customer Care"
    return responses


def Updatedtroubleshootingtemplate(name, apology, assurance, askToTrySteps, troubleshooting, persists,
                               questions, escalation, probingQuestions, info_request, expectingreply):
    apology = apology
    if apology:
        apologyStatement = "\n\nI am sorry the issue still persist. "
    else:
        apologyStatement = ""

    assurance = assurance
    if assurance:
        assuranceStatement = "Please be assured that I will do my best to help you further."
    else:
        assuranceStatement = ""

    askToTrySteps = askToTrySteps
    if askToTrySteps:
        askToTryStepsStatement = "\nPlease try the following steps and let me know the results:\n"
    else:
        askToTryStepsStatement = ""

    persists = persists
    if persists:
        persistsStatement = "\nIf the issue persists, "
    else:
        persistsStatement = ""

    questions = questions
    if questions:
        questionsStatement = "To analyse the issue better and to determine the cause, I will need additional information:\n"
    else:
        questionsStatement = ""
    escalation = escalation
    if escalation:
        escalationStatement = "To check this with our Team and to determine the cause, I will need additional information:\n"
    else:
        escalationStatement = ""

    if expectingreply:
        expectingreplyStatement = "\n\nPlease take your time and let me know the results at your earliest convenience."
    else:
        expectingreplyStatement = ""
    responses = f"Hello,\n\nThank you for taking the time to respond. {apologyStatement} {assuranceStatement}\n{askToTryStepsStatement}{troubleshooting}{persistsStatement}{questionsStatement}{escalationStatement}{probingQuestions}\n{info_request}{expectingreplyStatement}\n\nIf there are any questions or concerns, feel free to contact me.\n\nBest Regards,\n{name}\nNVIDIA Customer Care"
    return responses

def followupone(name,type):
    type = type
    if type == "Query" :
        typeStatement = "Please let me know if the provided information was helpful and to your satisfaction."
    if type == "No-Reply after Troubleshooting":
        typeStatement = "I haven't received any updates from you. Kindly let me know if the issue has been resolved."

    responses = f"Hello,\n\nThank you for contacting NVIDIA Customer Care.\n\nThis is a follow-up email in reference to your contact to NVIDIA.\n\n{typeStatement}\n\nPlease feel free to let us know if you have any questions.\nLooking forward for your update.\n\nBest regards,\n{name},\nNVIDIA Customer Care"
    return responses

def followuptwo(name):
    responses = f"Hello,\n\nThank you for contacting NVIDIA Customer care.\nThis is my second follow up to check the status of the issue you had contacted us for.\nPlease update us with the requested information so that your issue can be addressed as soon as possible.\nPlease note, our database is designed to auto close if we do not hear from you within 72 hours, the status will be changed to Solved.\nHence, if you find this case as Solved and if you need further assistance, please submit a new question by clicking the Ask A Question tab:  http://nvidia.custhelp.com/app/utils/login_form/redirect/ask\nAlso, once the case is closed the server will automatically trigger a survey to your email address with the subject 'NVIDIA support feedback' asking you to rate my service to you. The rating scale is 1 - 10, where 1 is the least and 10 the best.\nPlease participate in this short survey and survey rating below 8 indicates your dissatisfaction over the assistance that you have received by me.\nIf that's the case; please let me know and I shall help you troubleshoot further.\nI realize that your time is extremely valuable and I appreciate your feedback.\n\nRegards,\n{name},\nNVIDIA Customer Care"
    return responses


def feedback(name):
    responses = f"Hello,\n\nThank you for your update, Glad to know that the issue you were having is fixed and we do appreciate your efforts in troubleshooting the issue.\nWe shall go ahead and move the case to Resolved with your consent.\nHowever, if in case you have any further queries in future you can always reply back to me over the e-mail and we will be happy to help you further.\nI would also like to inform you that shortly you will receive an email survey from NVIDIA asking you to rate our service on a scale of 1-10, rating 10 indicates that you were happy with the support and any rating below 8 indicates that you were not satisfied with the service.\nPlease take a minute and rate our service.\nThank you once again for contacting NVIDIA Customer Care and giving us an opportunity to serve you.\nHave a Nice Day!\n\nRegards,\n{name},\nNVIDIA Customer Care"
    return responses

def rma(name, reason, rmaId, complaintId, casenumber, trackingdetail, trackingnumber, trackingLink):
    trackingdetail = trackingdetail
    if trackingdetail:
        trackinginfo = f"Tracking Number: {trackingnumber}\nTracking Link: {trackingLink}"
    else:
        trackinginfo = ""
    responses = f"Hello Team,\n\n{reason}\n\nRMA ID: {rmaId}\nComplaint ID: {complaintId}\nIncident/Case Number: {casenumber}\n\n{trackinginfo}\n\nBest Regards,\n{name}"

    return responses