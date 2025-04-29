from beeai_framework.tools import StringToolOutput, tool
import requests
import ast
import os

class MaximoItemTool:

    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")

    def get_item_details(self, inventory_response: str) -> dict:
        """
        Fetch item details from Maximo Inventory based on item descriptions.

        Args:
            inventory_response (str): A stringified list of item descriptions.

        Returns:
            dict: A dictionary containing item number and description, or an error.
        """
        try:
            base_url = f"{self.base_url}/maximo/api/os/MXAPIITEM"

            inventory_response_list = ast.literal_eval(inventory_response)
            search_condition = [f'"%{item}%"' for item in inventory_response_list]
            formatted_cond = f'[{",".join(search_condition)}]'
            formatted_string = f'description in {formatted_cond}'

            query_params = {
                "apikey": self.api_key,
                "lean": "1",
                "ignorecollectionref": "1",
                "oslc.select": "itemnum,description",
                "oslc.where": formatted_string
            }

            response = requests.get(base_url, params=query_params, verify=False)

            if response.status_code == 200:
                data = response.json()
                if "member" in data and len(data["member"]) > 0:
                    item = data["member"][0]  # Taking the first matching item
                    return {
                        "itemnum": item.get("itemnum", "N/A"),
                        "description": item.get("description", "N/A")
                    }
                else:
                    return {"error": "No matching items found."}
            else:
                return {"error": f"Failed to fetch data, status code {response.status_code}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}

def maximo_get_item_details_tool(inventory_response: str) -> str:
    """
    Retrieve item number and description from Maximo Inventory based on input descriptions.

    Args:
        inventory_response (str): A stringified list of item descriptions.

    Returns:
        str: A formatted string summarizing the item details.
    """
    try:
        maximo_tool = MaximoItemTool()
        result = maximo_tool.get_item_details(inventory_response)
        if "error" not in result:
            return (
                f"Item Number: {result['itemnum']}\n"
                f"Description: {result['description']}"
            )
        else:
            return result["error"]
    except Exception as e:
        return (
            "An error occurred while invoking the tool maximo_get_item_details. "
            f"Logs: {str(e)}"
        )

@tool
def maximo_get_item_details(inventory_response: str) -> StringToolOutput:
    """
    Retrieve Maximo item number and description using inventory response list.

    Args:
        inventory_response (str): A stringified list of item descriptions.

    Returns:
        str: A string containing the item number and description.
    """
    maximo_tool = MaximoItemTool()
    item_info = maximo_tool.get_item_details(inventory_response)
    if isinstance(item_info, dict) and "error" not in item_info:
        return (
            f"Item Number: {item_info['itemnum']}\n"
            f"Description: {item_info['description']}"
        )
    else:
        return item_info.get("error", "Unknown error occurred.")
