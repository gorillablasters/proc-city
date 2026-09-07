PROCESS_BUILDING_TYPES = {
    "generic": "generic",
    "commercial": "commercial",
    "network_service": "network",
    "industrial": "industrial",
    "storage_service": "warehouse",
    "infrastructure": "infrastructure",
    "temporary": "temporary",
}


def get_building_type(process_category: str) -> str:

    return PROCESS_BUILDING_TYPES.get(process_category, "generic")
