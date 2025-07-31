from beeai_framework.tools import StringToolOutput, tool
import requests
import os

class MaximoCraftTool:

    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")

    def get_all_crafts(self) -> str:
        base_url = f"{self.base_url}/maximo/api/os/MXAPICRAFT"

        query_params = {
            "apikey": self.api_key,
            "lean": "1",
            "ignorecollectionref": "1",
            "oslc.select": "craft,description"
        }

        try:
            response = requests.get(base_url, params=query_params, verify=False)

            if response.status_code == 200:
                data = response.json()

                if "member" in data and len(data["member"]) > 0:
                    all_crafts = [
                        f"{item.get('craft', 'N/A')}: {item.get('description', 'N/A')}"
                        for item in data["member"]
                    ]
                    return "\n".join(all_crafts)
                else:
                    return "No crafts found in Maximo."
            else:
                return f"Failed to fetch crafts. Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Request to Maximo failed: {str(e)}"


@tool
def get_craft_details() -> StringToolOutput:
    """
    Retrieve all craft codes and their descriptions from Maximo.

    Returns:
        str: A formatted string of craft codes and descriptions.
    """
    craft_tool = MaximoCraftTool()
    crafts_info = craft_tool.get_all_crafts()
    return crafts_info
