from beeai_framework.tools import StringToolOutput, tool
import requests
import os
from dotenv import load_dotenv
load_dotenv()


class MaximoWorkOrderTool:

    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")

    def fetch_unplanned_workorder(self) -> dict:
        """
        Fetch unplanned Work Order details (work order number and description) from Maximo.

        Args:
            None.

        Returns:
            dict: A dictionary containing wonum and description, or an error message.
        """
        try:
            base_url = f"{self.base_url}/maximo/api/os/AGAPIWODETAILS"

            query_params = {
                "apikey": self.api_key,
                "lean": "1",
                "ignorecollectionref": "1",
                "oslc.select": "wonum,description,siteid",
                "oslc.where": 'status="WAPPR" and schedstart!="*" and schedfinish!="*" and FLOWCONTROLLED=true'
            }

            response = requests.get(base_url, params=query_params, verify=False)
            print("response = ",response)

            if response.status_code == 200:
                data = response.json()
                if "member" in data and len(data["member"]) > 0:
                    # work_order = data["member"][0]
                    # return {
                    #     "wonum": work_order.get("wonum", "N/A"),
                    #     "description": work_order.get("description", "N/A"),
                    #     "siteid": work_order.get("siteid", "N/A")
                    # }
                    results = []

                    for item in data["member"]:
                        wonum = item.get("wonum", "N/A")
                        description = item.get("description", "N/A")
                        siteid = item.get("siteid","N/A")
                        # results.append({"itemnum": itemnum, "description": description,"siteid":siteid})
                        results.append(wonum)
                        print("Response from Maximo get item detail API = ", results)
                        if len(results) == 5:
                            break
                    return results
                else:
                    return {"error": "No unplanned work order found."}
            else:
                return {"error": f"Failed to fetch unplanned work order details. Status code: {response.status_code}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}



@tool
def fetch_workorder() -> StringToolOutput:
    """
    Retrieve Unplanned Maximo Work Order Number and Description.

    Args:
        None.

    Returns:
        str: A string containing the work order number and its description.
    """
    maximo_tool = MaximoWorkOrderTool()
    work_order_info = maximo_tool.fetch_unplanned_workorder()
    if isinstance(work_order_info, dict) and "error" not in work_order_info:
        return (
            f"Work Order Number: {work_order_info['wonum']}\n"
            f"Description: {work_order_info['description']}\n"
            f"SiteId:{work_order_info['siteid']}"
        )
    else:
        return work_order_info.get("error", "Unknown error occurred.")
    


# maximo_tool = MaximoWorkOrderTool()
# work_order_info = maximo_tool.fetch_unplanned_workorder()
# print("work order infor = ",work_order_info)