from beeai_framework.tools import StringToolOutput, tool
import requests
import os
import re
import json
from dotenv import load_dotenv
load_dotenv()

class MaximoLaborAssignmentTool:

    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")

    def get_workorder_url(self, wonum: str, siteid: str = "BEDFORD") -> str:
        url = f"{self.base_url}/maximo/api/os/MXAPIWODETAIL"
        query = f'?lean=1&ignorecollectionref=1&oslc.select=wonum,description,siteid&oslc.where=wonum="{wonum}" and siteid="{siteid}"'

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "apikey": self.api_key
        }

        res = requests.get(url + query, headers=headers, verify=False)
        print("\nGet Workorder URL Response:", res.status_code)

        if res.status_code == 200:
            href = res.json().get("member", [{}])[0].get("href")
            return href + "?lean=1&ignorecollectionref=1" if href else None
        return None

    def add_labor_to_work_order(self, labor: str, wonum: str, siteid: str) -> str:
        # Step 1: Get the Work Order href
        # query_url = f'{self.base_url}/maximo/api/os/MXAPIWODETAIL'
        # query = f'?lean=1&ignorecollectionref=1&oslc.select=wonum,description,siteid&oslc.where=wonum="{wonum}" and siteid="{siteid}"'

       

        try:
            url = self.get_workorder_url(wonum)
            print("Work order URL:", url)

            if not url:
                print("Work order URL not found.")
                return False

            match = re.search(r'mxapiwodetail/([^/]+)', url)
            if not match:
                print("Work order ID not found in URL.")
                return False

            id_value = match.group(1)
            final_url = f"{self.base_url}/maximo/api/os/mxapiwodetail/{id_value}?lean=1&ignorecollectionref=1"

            # Step 2: Prepare payload to add labor
            payload = {
                "wonum": wonum,
                "siteid": siteid,
                "status" : "APPR",
                "wplabor": {
                    "laborcode": labor
                }
            }

            headers = {
                "Content-Type": "application/json",
                "apikey": self.api_key,
                "x-method-override": "patch"
            }

            post_res = requests.post(final_url, json=payload, headers=headers, verify=False)
            print("POST response = ",post_res.status_code,post_res.text)

            # if post_res.status_code == 204:
            #     return f"Labor '{labor}' successfully added to work order '{wonum}'."
            # else:
            #     return f"Failed to add labor to work order. Status code: {post_res.status_code}"
            if post_res.status_code == 204:
                return f"Labor '{labor}' successfully added to work order '{wonum}'."

            elif post_res.status_code == 400:
                # return f"Bad request: Please check the payload. Possible issues with labor code '{labor}'."
                error_json = json.loads(post_res.text)
                if "Error" in error_json and "message" in error_json["Error"]:
                    message = error_json["Error"]["message"]
                    print("Message:", message)
                    if "BMXAA4606E - Work plan labor editing not enabled for Work Order 1201 which has a status of APPR." in message:
                        return f"Work order '{wonum}' is not suitable for planning."
                # return False, f"Bad request: Possible issues with item data or work order '{wonum}'."
                return f"Labor is already assigned for work order '{wonum}'."

            elif post_res.status_code == 401:
                return "Unauthorized: Invalid API key or authentication error."

            elif post_res.status_code == 403:
                return "Forbidden: You do not have permission to perform this action."

            elif post_res.status_code == 404:
                return f"Work order '{wonum}' not found or URL is invalid."

            elif post_res.status_code >= 500:
                return f"Server error ({post_res.status_code}): Maximo backend is unavailable or encountered an error."

            else:
                return f"Unexpected error. Status code: {post_res.status_code}, Response: {post_res.text}"

        # except requests.exceptions.RequestException as e:
        #     return f"Network or request error while assigning labor: {str(e)}"

        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
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

# obj = MaximoLaborAssignmentTool()
# # url = obj.get_workorder_url(wonum="1201",siteid="BEDFORD")
# result = obj.add_labor_to_work_order(labor='SCHFER',wonum="1201",siteid="BEDFORD")
# print("result = ",result)


