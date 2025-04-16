import logging
import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

class AgentMaximo:
    def __init__(self) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get("LOGLEVEL", "INFO").upper())

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

        if response.status_code == 200:
            data = response.json()

            if "member" in data and len(data["member"]) > 0:
                work_order = data["member"][0]
                location_details = work_order.get("location", {})
                saddresscode = location_details.get("saddresscode", "N/A")

                # Fetch Service Address details
                service_address = self.fetch_service_address_details(saddresscode)

                result = {
                    "wonum": work_order.get("wonum", "N/A"),
                    "location": work_order.get("location", "N/A"),
                    "saddresscode": saddresscode,
                    "LONGITUDEX": service_address.get("LONGITUDEX", "N/A"),
                    "LATITUDEY": service_address.get("LATITUDEY", "N/A")
                }

                print("response from maximo APIS = ",result)

                return result
        # return {"error": "Failed to fetch data"}

    def fetch_service_address_details(self, saddresscode):
        """Fetch Latitude and Longitude from serviceaddress."""
        if saddresscode == "N/A":
            return {"LONGITUDEX": "N/A", "LATITUDEY": "N/A"}

        service_address_url = f"{self.base_url}/maximo/api/os/MXAPISRVAD"

        query_params = {
            "apikey": self.api_key,
            "lean": "1",
            "ignorecollectionref": "1",
            "oslc.select": "ADDRESSCODE,LONGITUDEX,LATITUDEY",
            "oslc.where": f'ADDRESSCODE="{saddresscode}"'
        }

        response = requests.get(service_address_url, params=query_params, verify=False)

        if response.status_code == 200:
            data = response.json()
            if "member" in data and len(data["member"]) > 0:
                service_address = data["member"][0]
                return {
                    "LONGITUDEX": service_address.get("longitudex", "N/A"),
                    "LATITUDEY": service_address.get("latitudey", "N/A")
                }
        return {"LONGITUDEX": "N/A", "LATITUDEY": "N/A"}

    def get_workorder_url(self, wonum, siteid="BEDFORD"):
        """Fetch full resource URL for a work order."""
        get_url = f"{self.base_url}/maximo/api/os/MXAPIWODETAIL"
        query = f'?lean=1&ignorecollectionref=1&oslc.select=wonum,description,siteid&oslc.where=wonum="{wonum}" and siteid="{siteid}"'

        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key,
            **self.cookies
        }

        response = requests.get(get_url + query, headers=headers, verify=False)

        if response.status_code == 200:
            data = response.json()
            if "member" in data and len(data["member"]) > 0:
                href = data["member"][0].get("href")
                if href:
                    return href + "?lean=1&ignorecollectionref=1"
        return None

    def update_maximo_wo_schedule(self, wonum, sched_start, sched_finish):
        """POST call using fetched WO URL to update schedule."""
        wo_url = self.get_workorder_url(wonum)

        if not wo_url:
            return {"error": f"Could not find resource URL for WONUM {wonum}"}

        headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key,
            "x-method-override": "PATCH",
            "properties": "*",
            **self.cookies
        }

        payload = json.dumps({
            "schedstart": sched_start,
            "schedfinish": sched_finish
        })

        response = requests.post(wo_url, headers=headers, data=payload, verify=False)

        if response.status_code in [200, 204]:
            print("Updated Sched_finsh date in Maximo",sched_finish)
            return {"message": "Work Order schedule updated successfully!"}
        else:
            return {"error": f"Failed to update schedule. Status: {response.status_code}, Response: {response.text}"}

