import logging
import os
import requests
import json
from datetime import datetime, timedelta
import re

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

    def fetch_maximo_wo_details(self, wonum):
        """Fetch Work Order, Location, and Service Address Lat/Lon data."""
        print("base url = ",self.base_url)
        base_url = f"{self.base_url}/maximo/api/os/AGAPIWODETAILS"


        query_params = {
            "apikey": self.api_key,
            "lean": "1",
            "ignorecollectionref": "1",
            "oslc.select": "wonum,location,location.saddresscode",
            "oslc.where": f'wonum="{wonum}"'
        }

        response = requests.get(base_url, params=query_params, verify=False)

        print("data = ",response)
        if response.status_code == 200:
            data = response.json()
            if "member" in data and len(data["member"]) > 0:
                work_order = data["member"][0]
                location_details = work_order.get("location", {})
                saddresscode = location_details.get("saddresscode", "N/A")
                print("agapiwodetail response = ",location_details)

                # Fetch Service Address details
                service_address = self.fetch_service_address_details(saddresscode)

                result = {
                    "wonum": work_order.get("wonum", "N/A"),
                    "location": work_order.get("location", "N/A"),
                    "saddresscode": saddresscode,
                    "LONGITUDEX": service_address.get("LONGITUDEX", "N/A"),
                    "LATITUDEY": service_address.get("LATITUDEY", "N/A"),
                    "CITY":service_address.get("CITY", "N/A")
                }

                print("response from maximo APIS = ",result)

                return result
        # return {"error": "Failed to fetch data"}

    def fetch_service_address_details(self, saddresscode):
        """Fetch Latitude and Longitude from serviceaddress."""
        if saddresscode == "N/A":
            return {"LONGITUDEX": "N/A", "LATITUDEY": "N/A","CITY":"N/A"}

        service_address_url = f"{self.base_url}/maximo/api/os/MXAPISRVAD"

        query_params = {
            "apikey": self.api_key,
            "lean": "1",
            "ignorecollectionref": "1",
            "oslc.select": "ADDRESSCODE,LONGITUDEX,LATITUDEY,CITY",
            "oslc.where": f'ADDRESSCODE="{saddresscode}"'
        }

        response = requests.get(service_address_url, params=query_params, verify=False)
        print("serviceadrress api response = ",response)

        if response.status_code == 200:
            data = response.json()
            if "member" in data and len(data["member"]) > 0:
                service_address = data["member"][0]
                return {
                    "LONGITUDEX": service_address.get("longitudex", "N/A"),
                    "LATITUDEY": service_address.get("latitudey", "N/A"),
                    "CITY":service_address.get("city", "N/A")
                }
        return {"LONGITUDEX": "N/A", "LATITUDEY": "N/A","CITY":"N/A"}
    
    def get_workorder_url(self, wonum, siteid="BEDFORD"):
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

    def update_schedule(self, wonum,sched_start,sched_finish):
        url = self.get_workorder_url(wonum)
        print("workorder url : ",url)
        
        match = re.search(r'mxapiwodetail/([^/]+)', url)

        if match:
            id_value = match.group(1)
            print("Extracted ID:", id_value)
        else:
            print("ID not found in the URL.")

        if not url:
            return {"error": "Work order URL not found"}
        
        final_url = self.base_url + "maximo/api/os/mxapiwodetail/" + id_value + "?lean=1&ignorecollectionref=1"

        # sched_start = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        # sched_finish = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "apikey": self.api_key,
            "x-method-override": "PATCH",
            "properties": "*"
        }

        payload = json.dumps({"schedstart": sched_start, "schedfinish": sched_finish})
        response = requests.post(final_url, headers=headers, data=payload, verify=False)

        print("\nUpdate Schedule Status:", response.status_code)
        print("Update Response:", response.text[:300])

        if response.status_code in [200, 204]:
            return {"message": "Work Order schedule updated successfully!"}
        return {"error": f"Failed to update schedule: {response.text}"}