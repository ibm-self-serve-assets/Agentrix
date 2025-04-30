from beeai_framework.tools import StringToolOutput, tool
import requests
import os

class MaximoLocationTool:

    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")

    def get_work_order_location(self, wonum: str) -> str:
        try:
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

                    service_address = self.get_service_address(saddresscode)

                    result = {
                        "wonum": work_order.get("wonum", "N/A"),
                        "location": work_order.get("location", "N/A"),
                        "saddresscode": saddresscode,
                        "LONGITUDEX": service_address.get("LONGITUDEX", "N/A"),
                        "LATITUDEY": service_address.get("LATITUDEY", "N/A"),
                        "CITY": service_address.get("CITY", "N/A")
                    }

                    return str(result)
                else:
                    return f"No work order found for WONUM {wonum}"
            else:
                return f"Failed to fetch work order details. Status code: {response.status_code}"
        except Exception as e:
            return f"Error occurred while fetching work order location: {str(e)}"

    def get_service_address(self, saddresscode: str) -> dict:
        if saddresscode == "N/A":
            return {"LONGITUDEX": "N/A", "LATITUDEY": "N/A", "CITY": "N/A"}

        service_url = f"{self.base_url}/maximo/api/os/MXAPISRVAD"

        query_params = {
            "apikey": self.api_key,
            "lean": "1",
            "ignorecollectionref": "1",
            "oslc.select": "ADDRESSCODE,LONGITUDEX,LATITUDEY,CITY",
            "oslc.where": f'ADDRESSCODE="{saddresscode}"'
        }

        response = requests.get(service_url, params=query_params, verify=False)

        if response.status_code == 200:
            data = response.json()
            if "member" in data and len(data["member"]) > 0:
                service = data["member"][0]
                return {
                    "LONGITUDEX": service.get("longitudex", "N/A"),
                    "LATITUDEY": service.get("latitudey", "N/A"),
                    "CITY": service.get("city", "N/A")
                }
        return {"LONGITUDEX": "N/A", "LATITUDEY": "N/A", "CITY": "N/A"}
    
def maximo_get_location_tool(wonum: str) -> str:
    """
    Retrieve Maximo work order location and service address details.

    Args:
        wonum (str): The Work Order Number for which to retrieve location and service address data.

    Returns:
        str: A string summarizing the work order's location, coordinates, and city.

    Example:
        wonum = "1201"
    """
    try:
        maximo_tool = MaximoLocationTool()
        result = maximo_tool.get_work_order_location(wonum)
        if result:
            return (
                f"Work Order: {result['wonum']}\n"
                f"Location: {result['location']}\n"
                f"Service Address Code: {result['saddresscode']}\n"
                f"City: {result['CITY']}\n"
                f"Latitude: {result['LATITUDEY']}, Longitude: {result['LONGITUDEX']}"
            )
        else:
            return "No data found for the given work order number."
    except Exception as e:
        return (
            "An error occurred while invoking the tool maximo_get_location. "
            f"Here is the log. Try analyzing it and retry with a different payload. Logs: {str(e)}"
        )


@tool
def maximo_get_location(wonum: str) -> StringToolOutput:
    """
    Retrieve Maximo work order location and coordinates using the work order number.

    Args:
        wonum (str): The work order number.

    Returns:
        str: A string containing the location, city, and coordinates of the work order.
    """
    maximo_tool = MaximoLocationTool()
    location_info = maximo_tool.get_work_order_location(wonum)
    return location_info
