from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd

@tool
def check_inventory_levels() -> list:
    """
    Checks hardcoded inventory levels and flags items that need restocking.

    Returns:
    - A list of dictionaries with keys:
        - 'sku'
        - 'current_stock'
        - 'reorder_level'
        - 'action' ('Restock' or 'OK')
    """
    data = {
        "sku": ["SKU001", "SKU002", "SKU003", "SKU004"],
        "current_stock": [5, 12, 2, 20],
        "reorder_level": [10, 10, 5, 15]
    }
    df = pd.DataFrame(data)
    df["action"] = df.apply(
        lambda row: "Restock" if row["current_stock"] <= row["reorder_level"] else "OK",
        axis=1
    )
    return df[["sku", "current_stock", "reorder_level", "action"]].to_dict(orient="records")
