def calculate_compliance(detected_ppe, required_ppe):

    detected_ppe = set(detected_ppe)
    required_ppe = set(required_ppe)

    present = detected_ppe.intersection(required_ppe)

    compliance = (len(present) / len(required_ppe)) * 100

    missing = list(required_ppe - detected_ppe)

    return round(compliance), missing