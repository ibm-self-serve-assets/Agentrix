from beeai_framework.tools import StringToolOutput, tool
import requests
import os

class MaximoLaborAssignmentTool:

    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")

    def add_labor_to_work_order(self, labor: str, wonum: str, siteid: str) -> str:
        # Step 1: Get the Work Order href
        query_url = f'{self.base_url}/maximo/api/os/MXAPIWODETAIL'
        query = f'?lean=1&ignorecollectionref=1&oslc.select=wonum,description,siteid&oslc.where=wonum="{wonum}" and siteid="{siteid}"'

        headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key,
            "x-method-override": "patch"
        }

        try:
            res = requests.get(query_url + query, headers=headers, verify=False)

            if res.status_code == 200:
                href = res.json().get("member", [{}])[0].get("href")
                if not href:
                    return f"No href found for work order {wonum} at site {siteid}."

                # Fix href URL if pointing to localhost
                post_url = href.replace("http://localhost/", self.base_url) + "?lean=1"

                # Step 2: Prepare payload to add labor
                payload = {
                    "wonum": wonum,
                    "siteid": siteid,
                    "wplabor": {
                        "laborcode": labor
                    }
                }

                post_res = requests.post(post_url, json=payload, headers=headers, verify=False)

                if post_res.status_code == 204:
                    return f"Labor '{labor}' successfully added to work order '{wonum}'."
                else:
                    return f"Failed to add labor to work order. Status code: {post_res.status_code}"

            else:
                return f"Failed to retrieve work order. Status code: {res.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Request error while assigning labor: {str(e)}"


@tool
def assign_labor_to_work_order(labor: str, wonum: str, siteid: str) -> StringToolOutput:
    """
    Assign a labor code to a Maximo work order.

    Args:
        labor (str): The labor code to assign.
        wonum (str): The work order number.
        siteid (str): The site ID where the work order exists.

    Returns:
        str: Success or failure message.
    """
    labor_tool = MaximoLaborAssignmentTool()
    result = labor_tool.add_labor_to_work_order(labor, wonum, siteid)
    return result
