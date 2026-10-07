def entry_decision(compliance, missing_ppe):

    if compliance == 100 and len(missing_ppe) == 0:
        return "ENTRY ALLOWED"

    else:
        return "ENTRY DENIED"