def new_troubleshooting_template(
    name,
    paraphrase,
    apology,
    assurance,
    askToTrySteps,
    troubleshooting,
    persists,
    questions,
    escalation,
    probingQuestions,
    info_request,
    expectingreply
):
    # Conditional statements
    apologyStatement = "\n\nI apologise for the inconvenience caused." if apology else ""
    assuranceStatement = "\nPlease be assured that I will do my best to help you further." if assurance else ""
    askToTryStepsStatement = "\n\nPlease try the following steps and let me know the results:\n" if askToTrySteps else ""
    persistsStatement = "\nIf the issue persists, " if persists else ""
    questionsStatement = "To analyse the issue better and to determine the cause, I will need additional information:\n" if questions else ""
    escalationStatement = "To check this with our Team and to determine the cause, I will need additional information:\n" if escalation else ""
    expectingreplyStatement = "\n\nPlease take your time and let me know the results at your earliest convenience." if expectingreply else ""

    # Construct the full response
    response = (
        f"Hello,\n\n"
        f"Thank you for contacting NVIDIA Customer Care. This is {name}, and I'll be assisting with the issue you are experiencing.\n\n"
        f"From the description, I understand that {paraphrase}."
        f"{apologyStatement}"
        f"{assuranceStatement}"
        f"{askToTryStepsStatement}"
        f"{troubleshooting}"
        f"{persistsStatement}"
        f"{questionsStatement}"
        f"{escalationStatement}"
        f"{probingQuestions}\n"
        f"{info_request}"
        f"{expectingreplyStatement}\n\n"
        f"If there are any questions or concerns, feel free to contact me.\n\n"
        f"Best Regards,\n"
        f"{name}\n"
        f"NVIDIA Customer Care"
    )

    return response



