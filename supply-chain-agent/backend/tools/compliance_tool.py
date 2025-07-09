from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(description="Verify supplier compliance based on certification, ESG adherence, and blacklist status.")
def verify_compliance() -> list:
    """
    Check whether suppliers are compliant based on certification, ESG status, and blacklist inclusion.

    Returns:
    - A list of dictionaries with:
        - 'supplier'
        - 'certified'
        - 'blacklisted'
        - 'esg_compliant'
        - 'status' (Approved or Blocked)
    """
    try:
        suppliers_data = [
            {"supplier": "Supplier A", "certified": "Yes", "blacklisted": "No", "esg_compliant": "Yes"},
            {"supplier": "Supplier E", "certified": "Yes", "blacklisted": "No", "esg_compliant": "Yes"},
        ]

        for row in suppliers_data:
            if row["certified"] != "Yes" or row["esg_compliant"] != "Yes" or row["blacklisted"] == "Yes":
                row["status"] = "Blocked"
            else:
                row["status"] = "Approved"

        return suppliers_data
    
    except Exception as e:
        return [{"error": str(e)}]
