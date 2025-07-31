from beeai_framework.tools import StringToolOutput, tool
import requests
import os

class MaximoLaborTool:

    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")

    def get_labor_by_craft(self, craft: str) -> str:
        url = f"{self.base_url}/maximo/api/os/MXAPILABOR"
        query = f'?lean=1&ignorecollectionref=1&oslc.select=laborcode&oslc.where=LABORCRAFTRATE.craft="{craft}"'

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "apikey": self.api_key
        }

        try:
            res = requests.get(url + query, headers=headers, verify=False)

            if res.status_code == 200:
                data = res.json()
                if "member" in data and len(data["member"]) > 0:
                    labor = data["member"][0].get("laborcode", "N/A")
                    return f"Labor code for craft '{craft}': {labor}"
                else:
                    return f"No labor records found for craft '{craft}'."
            else:
                return f"Failed to fetch labor data. Status code: {res.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Error while fetching labor info: {str(e)}"


@tool
def get_labor_for_craft(craft: str) -> StringToolOutput:
    """
    Retrieve labor code associated with the given craft from Maximo.

    Args:
        craft (str): The craft code (e.g., 'ELECT').

    Returns:
        str: The labor code corresponding to the craft.
    """
    labor_tool = MaximoLaborTool()
    labor_info = labor_tool.get_labor_by_craft(craft)
    return labor_info
