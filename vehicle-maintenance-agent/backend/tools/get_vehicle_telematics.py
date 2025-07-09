# tool.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_vehicle_telematics", description="Get vehicle telematics data", permission=ToolPermission.READ_ONLY)
def get_vehicle_telematics(vin_number: str) -> dict:
    """
    This tool fetches vehicle telematics data based on the VIN number.
    Args:
        vin_number (str): The Vehicle Identification Number (VIN) of the vehicle.
    Returns:
        dict: A JSON containing the telematics data.
    """
    # Simulated response
    
    return {
        "vin": "1HGBH41JXMN109186",
        "timestamp": "2025-05-05T14:23:45Z",
        "engine_status": "on",
        "engine_temperature_celsius": 104.2,
        "rpm": 3200,
        "vehicle_speed_kph": 62,
        "battery_voltage": 12.3,
        "fuel_level_percent": 47.5,
        "dtc_codes": ["P0301", "P0171"],
        "location": {
            "lat": 37.7749,
            "lon": -122.4194
        },
        "odometer_km": 61240,
        "last_service_km": 45000,
        "coolant_level_percent": 78,
        "oil_pressure_psi": 28,
        "throttle_position_percent": 18.5,
        "intake_air_temp_celsius": 38.0
    }