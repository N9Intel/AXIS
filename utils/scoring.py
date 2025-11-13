def calculate_tier(listings: int) -> str:
    if listings >= 50:
        return "HIGH"
    elif listings >=10:
        return "MEDIUM"
    return "LOW"
    