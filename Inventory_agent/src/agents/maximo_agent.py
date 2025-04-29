# import logging
# import os
# import requests
# import json
# import ast
# from datetime import datetime, timedelta

# class AgentMaximo:
#     def __init__(self) -> None:
#         self._init_config()

#     def _init_config(self):
#         self.api_key = os.getenv("MAXIMO_APIKEY", "")
#         self.base_url = os.getenv("MAXIMO_BASE_URL", "")
#         self.cookie = os.getenv("SESSION_COOKIE","")
#         self.cookies = {
#             'Cookie': self.cookie
#         }

#     def getItemDetails(self, inventory_response):
#         """Fetch items"""
#         print("base url = ", self.base_url)
#         base_url = f"{self.base_url}/maximo/api/os/MXAPIITEM"
#         inventory_response_list = ast.literal_eval(inventory_response)
#         # Properly format the search condition using each item from the response
#         # Use single quotes for descriptions in the OSLC query
#         search_condition = [f'"%{item}%"' for item in inventory_response_list]
#         formatted_cond = f'[{",".join(search_condition)}]'
#         word="description"
#         formatted_string = f"{word} in {formatted_cond}"
#         print("Search Condition: ", formatted_string)

#         query_params = {
#             "apikey": self.api_key,
#             "lean": "1",
#             "ignorecollectionref": "1",
#             "oslc.select": "itemnum,description",
#             "oslc.where": formatted_string
#         }

#         # Making the GET request to the Maximo API
#         try:
#             response = requests.get(base_url, params=query_params, verify=False)

#             print("Response: ", response)
#             if response.status_code == 200:
#                 data = response.json()
#                 print("Data = ", data)
#                 if "member" in data and len(data["member"]) > 0:
#                     items = data["member"][0]  # Assuming you want the first match
#                     desc_details = items.get("description", "N/A")
#                     print("mxapiitem response = ", desc_details)

#                     result = {
#                         "itemnum": items.get("itemnum", "N/A"),
#                         "description": desc_details
#                     }

#                     print("Response from Maximo API = ", result)
#                     return result
#                 else:
#                     print("No items found.")
#                     return {"error": "No items found"}
#             else:
#                 print(f"Error: {response.status_code} - {response.text}")
#                 return {"error": f"Failed to fetch data, status code {response.status_code}"}
#         except requests.exceptions.RequestException as e:
#             print(f"Request failed: {e}")
#             return {"error": "Request failed"}
    
#     def fetch_maximo_wo_details(self, wonum):
#         """Fetch Work Order, description"""
#         print("base url = ",self.base_url)
#         base_url = f"{self.base_url}/maximo/api/os/AGAPIWODETAILS"


#         query_params = {
#             "apikey": self.api_key,
#             "lean": "1",
#             "ignorecollectionref": "1",
#             "oslc.select": "wonum,description",
#             "oslc.where": f'wonum="{wonum}"'
#         }

#         response = requests.get(base_url, params=query_params, verify=False)

#         print("data = ",response)
#         if response.status_code == 200:
#             data = response.json()
#             if "member" in data and len(data["member"]) > 0:
#                 work_order = data["member"][0]
#                 desc_details = work_order.get("description", {})
#                 print("agapiwodetail response = ",desc_details)

               

#                 result = {
#                     "wonum": work_order.get("wonum", "N/A"),
#                     "description": work_order.get("description", "N/A")
#                 }

#                 print("response from maximo APIS = ",result)

#                 return result
#         # return {"error": "Failed to fetch data"}

    
#     def get_item_url(self, itemnum):
#         url = f"{self.base_url}maximo/api/os/MXINVENTORY"
#         query = f'?lean=1&ignorecollectionref=1&oslc.select=itemnum,location&oslc.where=itemnum="{itemnum}"'

#         headers = {
#             "Content-Type": "application/json",
#             "Accept": "application/json",
#             "apikey": self.api_key
#         }

#         print(url+query)
#         res = requests.get(url + query, headers=headers, verify=False)
      
#         print("\nGet item URL Response:", res.status_code)

#         if res.status_code == 200:
#             print("Data = ", res)
#             data = res.json()
#             if "member" in data and len(data["member"]) > 0:
#                 items = data["member"][0]  # Assuming you want the first match
#                 storeloc = items.get("location", "N/A")
#                 print("mxapiitem response = ", storeloc)

#                 result = {
#                     "itemnum": items.get("itemnum", "N/A"),
#                     "storeloc": storeloc
#                 }

#                 print("Response from Maximo API = ", result)
#                 return result
#             else:
#                 print("No items found.")
#                 return {"error": "No items found"}
           
#         return None
    
#     def addItem(self, itemnum, location, wonum, siteid):
#         # Step 1: Get Work Order HREF
#         url = f"{self.base_url}/maximo/api/os/MXAPIWODETAIL"
#         query = f'?lean=1&ignorecollectionref=1&oslc.select=wonum,description,siteid&oslc.where=wonum="{wonum}" and siteid="{siteid}"'

#         headers = {
#             "Content-Type": "application/json",
#             "apikey": self.api_key,
#             "x-method-override":"patch"
#         }

#         res = requests.get(url + query, headers=headers, verify=False)
#         print("\nGet Workorder URL Response:", res.status_code)

#         if res.status_code == 200:
#             href = res.json().get("member", [{}])[0].get("href")
#             if href:
#                 hrefurl = href.replace("http://localhost/", self.base_url)
#                 post_url = f"{hrefurl}?lean=1"
#                 print("POST URL for WPMATERIAL:", post_url)

#                 # Step 2: Prepare payload to add item and location
#                 payload = {
#                     "wonum": wonum,
#                     "siteid": "BEDFORD",
#                     "wpmaterial":{
#                         "itemnum": itemnum,
#                         "location": location
                        
#                     }
#                 }

#                 print(payload,post_url)
#                 post_res = requests.post(post_url, json=payload, headers=headers, verify=False)
                
#                 print("POST Response Code:", post_res.status_code)
#                 return post_res.status_code == 204

        
import logging
import os
import requests
import json
import ast
from datetime import datetime, timedelta

class AgentMaximo:
    def __init__(self) -> None:
        self._init_config()

    def _init_config(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")
        self.cookie = os.getenv("SESSION_COOKIE","")
        self.cookies = {
            'Cookie': self.cookie
        }

    def getItemDetails(self, inventory_response):
        """Fetch items"""
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
    
    def fetch_maximo_wo_details(self, wonum):
        """Fetch Work Order, description"""
        print("base url = ",self.base_url)
        base_url = f"{self.base_url}/maximo/api/os/AGAPIWODETAILS"


        query_params = {
            "apikey": self.api_key,
            "lean": "1",
            "ignorecollectionref": "1",
            "oslc.select": "wonum,description",
            "oslc.where": f'wonum="{wonum}"'
        }

        response = requests.get(base_url, params=query_params, verify=False)

        print("data = ",response)
        if response.status_code == 200:
            data = response.json()
            if "member" in data and len(data["member"]) > 0:
                work_order = data["member"][0]
                desc_details = work_order.get("description", {})
                print("agapiwodetail response = ",desc_details)

               

                result = {
                    "wonum": work_order.get("wonum", "N/A"),
                    "description": work_order.get("description", "N/A")
                }

                print("response from maximo APIS = ",result)

                return result
        # return {"error": "Failed to fetch data"}

    
    def get_item_url(self, itemnum):
        url = f"{self.base_url}maximo/api/os/MXINVENTORY"
        query = f'?lean=1&ignorecollectionref=1&oslc.select=itemnum,location&oslc.where=itemnum="{itemnum}"'

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "apikey": self.api_key
        }

        print(url+query)
        res = requests.get(url + query, headers=headers, verify=False)
      
        print("\nGet item URL Response:", res.status_code)

        if res.status_code == 200:
            print("Data = ", res)
            data = res.json()
            if "member" in data and len(data["member"]) > 0:
                items = data["member"][0]  # Assuming you want the first match
                storeloc = items.get("location", "N/A")
                print("mxapiitem response = ", storeloc)

                result = {
                    "itemnum": items.get("itemnum", "N/A"),
                    "storeloc": storeloc
                }

                print("Response from Maximo API = ", result)
                return result
            else:
                print("No items found.")
                return {"error": "No items found"}
           
        return None
    
    def addItem(self, itemnum, location, wonum, siteid):
        # Step 1: Get Work Order HREF
        url = f"{self.base_url}/maximo/api/os/MXAPIWODETAIL"
        query = f'?lean=1&ignorecollectionref=1&oslc.select=wonum,description,siteid&oslc.where=wonum="{wonum}" and siteid="{siteid}"'

        headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key,
            "x-method-override":"patch"
        }

        res = requests.get(url + query, headers=headers, verify=False)
        print("\nGet Workorder URL Response:", res.status_code)

        if res.status_code == 200:
            href = res.json().get("member", [{}])[0].get("href")
            if href:
                hrefurl = href.replace("http://localhost/", self.base_url)
                post_url = f"{hrefurl}?lean=1"
                print("POST URL for WPMATERIAL:", post_url)

                # Step 2: Prepare payload to add item and location
                payload = {
                    "wonum": wonum,
                    "siteid": "BEDFORD",
                    "wpmaterial":{
                        "itemnum": itemnum,
                        "location": location
                        
                    }
                }

                print(payload,post_url)
                post_res = requests.post(post_url, json=payload, headers=headers, verify=False)
                
                print("POST Response Code:", post_res.status_code)
                return post_res.status_code == 204
    