from beeai_framework.tools import StringToolOutput, tool
import requests
import os

class MaximoInventoryTool:

    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")

    def get_item_url(self, itemnum: str) -> dict:
        """
        Fetch item number and store location from Maximo Inventory.

        Args:
            itemnum (str): Item number to search for.

        Returns:
            dict: A dictionary with itemnum and storeloc, or error.
        """
        try:
            url = f"{self.base_url}/maximo/api/os/MXINVENTORY"
            query = f'?lean=1&ignorecollectionref=1&oslc.select=itemnum,location&oslc.where=itemnum="{itemnum}"'

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "apikey": self.api_key
            }

            res = requests.get(url + query, headers=headers, verify=False)

            if res.status_code == 200:
                data = res.json()
                if "member" in data and len(data["member"]) > 0:
                    items = data["member"][0]
                    return {
                        "itemnum": items.get("itemnum", "N/A"),
                        "storeloc": items.get("location", "N/A")
                    }
                else:
                    return {"error": "No items found for the given item number."}
            else:
                return {"error": f"Failed to fetch item. Status code: {res.status_code}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}

    def add_item(self, itemnum: str, location: str, wonum: str, siteid: str) -> bool:
        """
        Add an item and location to a Work Order in Maximo.

        Args:
            itemnum (str): Item number to add.
            location (str): Store location.
            wonum (str): Work Order number.
            siteid (str): Site ID.

        Returns:
            bool: True if item added successfully, False otherwise.
        """
        try:
            url = f"{self.base_url}/maximo/api/os/MXAPIWODETAIL"
            query = f'?lean=1&ignorecollectionref=1&oslc.select=wonum,description,siteid&oslc.where=wonum="{wonum}" and siteid="{siteid}"'

            headers = {
                "Content-Type": "application/json",
                "apikey": self.api_key,
                "x-method-override": "patch"
            }

            res = requests.get(url + query, headers=headers, verify=False)

            if res.status_code == 200:
                href = res.json().get("member", [{}])[0].get("href")
                if href:
                    hrefurl = href.replace("http://localhost/", self.base_url)
                    post_url = f"{hrefurl}?lean=1"

                    payload = {
                        "wonum": wonum,
                        "siteid": siteid,
                        "wpmaterial": {
                            "itemnum": itemnum,
                            "location": location
                        }
                    }

                    post_res = requests.post(post_url, json=payload, headers=headers, verify=False)
                    return post_res.status_code == 204
            return False
        except Exception as e:
            print(f"Error during add_item: {str(e)}")
            return False

@tool
def post_inventory(itemnum: str, wonum: str, siteid: str) -> StringToolOutput:
    """
    Post an inventory item to a Maximo work order by providing the item number, 
    work order number, and site ID as input parameters.

    This tool retrieves the store location of the item and adds the item to the specified work order in Maximo.

    Args:
        itemnum (str): The item number.
        wonum (str): The Work Order number.
        siteid (str): The site ID.

    Returns:
        str: Success or error message.
    """
    inventory_tool = MaximoInventoryTool()

    # Step 1: Get the item's store location
    item_info = inventory_tool.get_item_url(itemnum)
    if "error" in item_info:
        return f"Failed to retrieve item details: {item_info['error']}"

    storeloc = item_info["storeloc"]

    # Step 2: Add item to the work order
    success = inventory_tool.add_item(itemnum=itemnum, location=storeloc, wonum=wonum, siteid=siteid)
    if success:
        return f"Successfully posted item '{itemnum}' with store location '{storeloc}' to work order '{wonum}' for site '{siteid}'."
    else:
        return "Failed to post inventory item to the Work Order."

