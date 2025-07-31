from beeai_framework.tools import StringToolOutput, tool
import requests
import ast
import os
from dotenv import load_dotenv
load_dotenv()

class MaximoItemTool:

    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")

    def filter_unique_items(self,items: list, keywords: list) -> list:
        """
        From a list of items, keep only the first matching item per functional type
        based on keywords found in the description.

        Args:
            items (list): List of item dicts with 'itemnum' and 'description'.
            keywords (list): List of functional keywords (e.g., ['motor', 'pump']).

        Returns:
            list: Filtered list with only first match for each keyword.
        """
        seen_categories = set()
        filtered_items = []

        for item in items:
            description = item.get("description", "").lower()

            for keyword in keywords:
                if keyword in description and keyword not in seen_categories:
                    filtered_items.append(item)
                    seen_categories.add(keyword)
                    break  # Stop after first match per item

        return filtered_items


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
                    results = []

                    for item in data["member"]:
                        itemnum = item.get("itemnum", "N/A")
                        description = item.get("description", "N/A")
                        results.append({"itemnum": itemnum, "description": description})

                    print("Response from Maximo get item detail API = ", results)

                    return results
                else:
                    print("No items found.")
                    return {"error": "No items found"}
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return {"error": f"Failed to fetch data, status code {response.status_code}"}
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {"error": "Request failed"}
        

    def get_store_location_list(self, item_list: list) -> list:
        """
        Fetch store locations for a list of items from Maximo Inventory.

        Args:
            item_list (list): A list of dicts with 'itemnum' and 'description' keys.

        Returns:
            list: A list of dicts with 'itemnum' and 'location' keys, for items found in inventory.
        """
        results = []

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "apikey": self.api_key
        }

        for item in item_list:
            itemnum = item.get("itemnum")
            if not itemnum:
                continue  # Skip if no itemnum

            try:
                url = f"{self.base_url}maximo/api/os/MXINVENTORY"
                query = f'?lean=1&ignorecollectionref=1&oslc.select=itemnum,location&oslc.where=itemnum="{itemnum}"'
                print(f"Calling: {url + query}")

                res = requests.get(url + query, headers=headers, verify=False)
                print(f"Response code: {res.status_code}")

                if res.status_code == 200:
                    data = res.json()
                    if "member" in data and len(data["member"]) > 0:
                        storeloc = data["member"][0].get("location", "N/A")
                        results.append({
                            "itemnum": itemnum,
                            "location": storeloc
                        })
                    else:
                        print(f"No inventory found for itemnum: {itemnum}")
                else:
                    print(f"Failed to fetch inventory for {itemnum}, status code: {res.status_code}")
            except Exception as e:
                print(f"Request failed for {itemnum}: {str(e)}")

        return results

            

@tool
def maximo_get_item_storelocation_details(inventory_response: str) -> StringToolOutput:
    """
    Retrieve Maximo item number and description using inventory response list.

    Args:
        inventory_response (str): A stringified list of item descriptions.

    Returns:
        str: A List containing the item numbers and corresponding storelocations.
    """
    maximo_tool = MaximoItemTool()
    item_info = maximo_tool.get_item_details(inventory_response)
    print("item info from maximo = ",item_info)
    filtered_items = maximo_tool.filter_unique_items(item_info,inventory_response)
    print("filtered items from items = ",filtered_items)
    store_location_info = maximo_tool.get_store_location_list(filtered_items)
    print("store locations for items = ",store_location_info)
    if len(store_location_info)>0 and "error" not in store_location_info:
        return store_location_info
    else:
        return item_info.get("error", "Unknown error occurred.")
    




# Input: a stringified list of item descriptions
# inventory_response = '["Motor", "Valve", "Pump"]'

# maximo_tool = MaximoItemTool()
# item_info = maximo_tool.get_item_details(inventory_response)

# # Print the result
# print(item_info)

# filtered = filter_unique_functional_items(item_info, inventory_response)

# store_location_info = maximo_tool.get_store_location_list(item_info)

# print("store location list = ",store_location_info)