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
        print("base url = ", self.base_url)
        base_url = f"{self.base_url}/maximo/api/os/MXAPIITEM"
        inventory_response_list = ast.literal_eval(inventory_response)
        # Properly format the search condition using each item from the response
        # Use single quotes for descriptions in the OSLC query
        search_condition = [f'"%{item}%"' for item in inventory_response_list]
        formatted_cond = f'[{",".join(search_condition)}]'
        word="description"
        formatted_string = f"{word} in {formatted_cond}"
        print("Search Condition: ", formatted_string)

        query_params = {
            "apikey": self.api_key,
            "lean": "1",
            "ignorecollectionref": "1",
            "oslc.select": "itemnum,description",
            "oslc.where": formatted_string
        }

        # Making the GET request to the Maximo API
        try:
            response = requests.get(base_url, params=query_params, verify=False)

            print("Response: ", response)
            if response.status_code == 200:
                data = response.json()
                print("Data = ", data)
                if "member" in data and len(data["member"]) > 0:
                    items = data["member"][0]  # Assuming you want the first match
                    desc_details = items.get("description", "N/A")
                    print("mxapiitem response = ", desc_details)

                    result = {
                        "itemnum": items.get("itemnum", "N/A"),
                        "description": desc_details
                    }

                    print("Response from Maximo API = ", result)
                    return result
                else:
                    print("No items found.")
                    return {"error": "No items found"}
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return {"error": f"Failed to fetch data, status code {response.status_code}"}
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {"error": "Request failed"}


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
