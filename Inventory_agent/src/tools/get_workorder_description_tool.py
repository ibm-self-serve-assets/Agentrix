from beeai_framework.tools import StringToolOutput, tool
import requests
import os

class MaximoWorkOrderTool:

    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")

    def fetch_workorder_description(self, wonum: str) -> dict:
        """
        Fetch Work Order details (work order number and description) from Maximo.

        Args:
            wonum (str): The Work Order Number to fetch.

        Returns:
            dict: A dictionary containing wonum and description, or an error message.
        """
        try:
            base_url = f"{self.base_url}/maximo/api/os/AGAPIWODETAILS"

            query_params = {
                "apikey": self.api_key,
                "lean": "1",
                "ignorecollectionref": "1",
                "oslc.select": "wonum,description",
                "oslc.where": f'wonum="{wonum}"'
            }

            response = requests.get(base_url, params=query_params, verify=False)

            if response.status_code == 200:
                data = response.json()
                if "member" in data and len(data["member"]) > 0:
                    work_order = data["member"][0]
                    return {
                        "wonum": work_order.get("wonum", "N/A"),
                        "description": work_order.get("description", "N/A")
                    }
                else:
                    return {"error": "No work order found with the given WONUM."}
            else:
                return {"error": f"Failed to fetch work order details. Status code: {response.status_code}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}

def fetch_workorder_description_tool(wonum: str) -> str:
    """
    Retrieve work order number and description from Maximo.

    Args:
        wonum (str): The Work Order Number.

    Returns:
        str: A formatted string summarizing the work order details.
    """
    try:
        maximo_tool = MaximoWorkOrderTool()
        result = maximo_tool.fetch_workorder_description(wonum)
        if "error" not in result:
            return (
                f"Work Order Number: {result['wonum']}\n"
                f"Description: {result['description']}"
            )
        else:
            return result["error"]
    except Exception as e:
        return (
            "An error occurred while invoking the tool fetch_workorder_description. "
            f"Logs: {str(e)}"
        )

@tool
def fetch_workorder_description(wonum: str) -> StringToolOutput:
    """
    Retrieve Maximo Work Order Number and Description using the WONUM.

    Args:
        wonum (str): The Work Order Number.

    Returns:
        str: A string containing the work order number and its description.
    """
    maximo_tool = MaximoWorkOrderTool()
    work_order_info = maximo_tool.fetch_workorder_description(wonum)
    if isinstance(work_order_info, dict) and "error" not in work_order_info:
        return (
            f"Work Order Number: {work_order_info['wonum']}\n"
            f"Description: {work_order_info['description']}"
        )
    else:
        return work_order_info.get("error", "Unknown error occurred.")
