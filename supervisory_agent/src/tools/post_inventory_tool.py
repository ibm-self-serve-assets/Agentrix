from beeai_framework.tools import StringToolOutput, tool
import requests
import os
import re
import json

class MaximoInventoryTool:

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


    
    def add_item(self, items_with_locations: list, wonum: str, siteid: str) -> bool:
        """
        Update multiple items with their locations to a Work Order in Maximo.

        Args:
            items_with_locations (list): List of dicts with 'itemnum' and 'location'.
            wonum (str): Work Order number.
            siteid (str): Site ID.

        Returns:
            bool: True if items added successfully, False otherwise.
        """
        try:
            if not items_with_locations:
                raise ValueError("No item-location pairs provided.")

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

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "apikey": self.api_key,
                "x-method-override": "PATCH",
                "properties": "*"
            }

            payload = {
                "wonum": wonum,
                "siteid": siteid,
                "status" : "APPR",
                "wpmaterial": items_with_locations
            }

            print("POST URL:", final_url)
            print("Payload:", payload)

            post_res = requests.post(final_url, json=payload, headers=headers, verify=False)
            print("POST Response:", post_res.status_code, post_res.text)

            # if post_res.status_code in [200, 201, 204]:
            #     return True

            # return False
            if post_res.status_code in [200, 201, 204]:
                return True, f"Inventory successfully updated for work order '{wonum}'."

            elif post_res.status_code == 400 :
                error_json = json.loads(post_res.text)
                if "Error" in error_json and "message" in error_json["Error"]:
                    message = error_json["Error"]["message"]
                    print("Message:", message)
                    if "BMXAA4605E - Work plan material and services editing not enabled for Work Order 1201 which has a status of APPR." in message:
                        return False, f"Work order '{wonum}' is not suitable for planning."
                return False, f"Bad request: Possible issues with item data or work order '{wonum}'."
            elif post_res.status_code == 401:
                return False, "Unauthorized: API key or authentication error."
            elif post_res.status_code == 403:
                return False, "Forbidden: You do not have permission to update inventory."
            elif post_res.status_code == 404:
                return False, f"Work order '{wonum}' not found or URL is invalid."
            elif post_res.status_code >= 500:
                return False, f"Server error ({post_res.status_code}): Maximo backend issue."
            else:
                return False, f"Unexpected error ({post_res.status_code}): {post_res.text}"
        except Exception as e:
            print(f"Error during add_item: {str(e)}")
            return False


# @tool
# def post_inventory(itemnum: str, wonum: str, siteid: str) -> StringToolOutput:
#     """
#     Post an inventory item to a Maximo work order by providing the item number, 
#     work order number, and site ID as input parameters.

#     This tool retrieves the store location of the item and adds the item to the specified work order in Maximo.

#     Args:
#         itemnum (str): The item number.
#         wonum (str): The Work Order number.
#         siteid (str): The site ID.

#     Returns:
#         str: Success or error message.
#     """
#     inventory_tool = MaximoInventoryTool()

#     # Step 1: Get the item's store location
#     item_info = inventory_tool.get_item_url(itemnum)
#     if "error" in item_info:
#         return f"Failed to retrieve item details: {item_info['error']}"

#     storeloc = item_info["storeloc"]

#     # Step 2: Add item to the work order
#     success = inventory_tool.add_item(itemnum=itemnum, location=storeloc, wonum=wonum, siteid=siteid)
#     if success:
#         return f"Successfully posted item '{itemnum}' with store location '{storeloc}' to work order '{wonum}' for site '{siteid}'."
#     else:
#         return "Failed to post inventory item to the Work Order."


@tool
def post_multiple_inventory(items_with_locations:list, wonum: str, siteid: str) -> StringToolOutput:
    """
    Update multiple inventory items with their locations to a Maximo work order.

    Args:
        items_with_locations (list): List of item numbers with Store Locations.
        wonum (str): Work Order number.
        siteid (str): Site ID.

    Returns:
        str: Success or error message.
    """
    inventory_tool = MaximoInventoryTool()

    success,message = inventory_tool.add_item(items_with_locations=items_with_locations , wonum=wonum, siteid=siteid)
    if success:
        return f"Successfully posted {len(items_with_locations)} item(s) to work order '{wonum}' at site '{siteid}'."
    else:
        return message

