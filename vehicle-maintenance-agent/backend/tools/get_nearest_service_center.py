# tool.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_nearest_service_center", description="Get nearest service center", permission=ToolPermission.READ_ONLY)
def get_nearest_service_center(lat: float, lon: float) -> list:
    """
    This tool fetches the nearest service center based on the provided latitude and longitude.
    Args:
        lat (float): The latitude of the user's location.
        lon (float): The longitude of the user's location.
    Returns:
        list: A list of dictionaries containing service center details.
    """
    # Simulated response
    
    service_centers = [
        {
            "name": "KHT Prime Jeep Domlur",
            "address": "92/93 Garden city Plaza Amar Jyothi Layout Domlur, Kormangala, Intermediate Ring Rd, Bengaluru, Karnataka 560071",
            "phone": "+91-9876543210",
            "distance_km": 2.5
        },
        {
            "name": "PPS Jeep HSR Layout",
            "address": "PPS JEEP, 142, Outer Ring Rd, Teacher's Colony, Jakkasandra, 1st Block Koramangala, HSR Layout 5th Sector, Bengaluru, Karnataka 560102",
            "phone": "+91-9786534210",
            "distance_km": 3.0
        },
        {
            "name": "PPS Jeep JP Nagar",
            "address": "G R Grand Plaza, Building No. 386/1/383/362/70, village, Kanakapura Main Rd, Jarganahalli, JP Nagar Phase 6, J. P. Nagar, Bengaluru, Karnataka 560078",
            "phone": "+91-9654321876",
            "distance_km": 4.0
        }
    ]

    return service_centers
