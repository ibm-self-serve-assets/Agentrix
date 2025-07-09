from ibm_watsonx_orchestrate.agent_builder.tools import tool
from datetime import datetime, timedelta

@tool
def plan_deliveries(today: str = None) -> list:
    """
    Generate delivery ETA and priority based on procurement plan.
    
    Returns:
    - A list of dictionaries with:
        - 'sku'
        - 'supplier'
        - 'dispatch_date'
        - 'delivery_eta'
        - 'priority' (High if lead_time_days <= 3, else Normal)
    """
    try:
        # Simulated procurement plan (from previous step)
        procurement_plan = [
            {"sku": "SKU001", "supplier": "Supplier A", "lead_time_days": 3},
            {"sku": "SKU002", "supplier": "Supplier C", "lead_time_days": 5},
            {"sku": "SKU003", "supplier": "Supplier B", "lead_time_days": 2},  # Blocked
        ]

        # Only allow compliant suppliers
        approved_suppliers = {"Supplier A", "Supplier E"}  # From verify_compliance()

        base_date = datetime.strptime(today, "%Y-%m-%d") if today else datetime.today()
        schedule = []

        for row in procurement_plan:
            supplier = row.get("supplier")
            if supplier not in approved_suppliers:
                continue  # Skip blocked suppliers

            try:
                lead_time = int(row["lead_time_days"])
                eta = base_date + timedelta(days=lead_time)
                schedule.append({
                    "sku": row["sku"],
                    "supplier": supplier,
                    "dispatch_date": base_date.strftime("%Y-%m-%d"),
                    "delivery_eta": eta.strftime("%Y-%m-%d"),
                    "priority": "High" if lead_time <= 3 else "Normal"
                })
            except Exception as e:
                schedule.append({
                    "sku": row.get("sku", "Unknown"),
                    "supplier": supplier,
                    "error": f"Failed to calculate ETA: {str(e)}"
                })

        return schedule if schedule else [{"info": "No deliveries scheduled due to compliance filtering."}]

    except Exception as e:
        return [{"error": str(e)}]
