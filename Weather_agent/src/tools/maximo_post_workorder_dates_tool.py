from beeai_framework.tools import StringToolOutput, tool
import requests
import re
import json
import os

class MaximoTool:
    def __init__(self):
        self.api_key = os.getenv("MAXIMO_APIKEY", "")
        self.base_url = os.getenv("MAXIMO_BASE_URL", "")
        self.cookie = os.getenv("SESSION_COOKIE", "")


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

    def update_schedule(self, wonum: str, sched_start: str, sched_finish: str) -> str:
        url = self.get_workorder_url(wonum)
        print("workorder url:", url)

        if not url:
            return "Work order URL not found."

        match = re.search(r'mxapiwodetail/([^/]+)', url)
        if not match:
            return "Work order ID not found in URL."

        id_value = match.group(1)
        final_url = f"{self.base_url}/maximo/api/os/mxapiwodetail/{id_value}?lean=1&ignorecollectionref=1"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "apikey": self.api_key,
            "x-method-override": "PATCH",
            "properties": "*"
        }

        payload = json.dumps({
            "schedstart": sched_start,
            "schedfinish": sched_finish
        })

        response = requests.post(final_url, headers=headers, data=payload, verify=False)

        print("\nUpdate Schedule Status:", response.status_code)
        print("Update Response:", response.text[:300])

        if response.status_code in [200, 204]:
            return "Work Order schedule dates updated successfully in Maximo!"
        return f"Failed to update schedule dates : {response.text}"

    def update_workorder_tool(self, wonum: str, sched_start: str, sched_finish: str) -> str:
        return self.update_schedule(wonum, sched_start, sched_finish)

@tool
def update_workorder_tool(query: str) -> StringToolOutput:
    """
    Update the schedule of a Maximo work order by providing the work order number, 
    scheduled start time, and scheduled finish time in a comma-separated string.

    Args:
        query (str): A comma-separated string in the format 
        'WONUM,YYYY-MM-DDTHH:MM:SSZ,YYYY-MM-DDTHH:MM:SSZ'

    Returns:
        str: Status of the scheduling update.
    """
    try:
        wonum, sched_start, sched_finish = [part.strip() for part in query.split(",")]
        maximo = MaximoTool()
        return maximo.update_workorder_tool(wonum, sched_start, sched_finish)
    except Exception as e:
        return f"An error occurred while invoking update_workorder_tool. Logs: {str(e)}"
