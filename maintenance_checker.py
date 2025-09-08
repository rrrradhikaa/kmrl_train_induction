def check_maintenance_schedule(vehicle_data, threshold_km=10000):
    """
    Checks if a vehicle needs maintenance based on odometer reading.

    Args:
        vehicle_data (dict): Dictionary containing vehicle info.
            Example:
            {
                "vehicle_id": "V123",
                "odometer": 12500,
                "last_service_km": 3000
            }
        threshold_km (int): Distance threshold in kilometers for scheduling maintenance.

    Returns:
        dict: Maintenance status and details.
    """

    current_km = vehicle_data.get("odometer", 0)
    last_service_km = vehicle_data.get("last_service_km", 0)
    km_since_last_service = current_km - last_service_km

    needs_maintenance = km_since_last_service >= threshold_km

    return {
        "vehicle_id": vehicle_data.get("vehicle_id"),
        "current_km": current_km,
        "km_since_last_service": km_since_last_service,
        "maintenance_required": needs_maintenance
    }
