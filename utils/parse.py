import re
from utils.normalize import normalize_sector, normalize_revenue

# -----------------------------------------
#  ACCESS TYPE SUGGESTION
# -----------------------------------------

ACCESS_PATTERNS = {
    "rdp": r"\brdp\b",
    "vpn": r"\bvpn\b",
    "citrix": r"\bcitrix\b",
    "ssh": r"\bssh\b",
    "vnc": r"\bvnc\b",
    "owa": r"\bowa\b",
    "fortinet": r"\bforti",
}

def suggest_access_type(text: str) -> str:
    low = text.lower()
    for access, pattern in ACCESS_PATTERNS.items():
        if re.search(pattern, low):
            return access
    return ""


# -----------------------------------------
#  COUNTRY SUGGESTION
# -----------------------------------------

COUNTRY_CODES = {
    "us": ["usa", "united states", "america"],
    "gb": ["uk", "united kingdom", "england"],
    "es": ["spain", "españ", "spaña"],
    "fr": ["france"],
    "de": ["germany", "deutsch"],
    "ru": ["russia"],
}

def suggest_country(text: str) -> str:
    low = text.lower()

    # detect patterns like [ES]
    bracket = re.search(r"\[([A-Z]{2})\]", text)
    if bracket:
        return bracket.group(1)

    # detect based on keywords
    for code, keywords in COUNTRY_CODES.items():
        for kw in keywords:
            if kw in low:
                return code.upper()

    return ""


# -----------------------------------------
#  PRIVILEGE SUGGESTION
# -----------------------------------------

def suggest_privilege(text: str) -> str:
    low = text.lower()
    if "domain admin" in low or "da" in low:
        return "admin"
    if "admin" in low:
        return "admin"
    if "user" in low:
        return "user"
    return ""


# -----------------------------------------
#  PRICE SUGGESTION
# -----------------------------------------

def suggest_price(text: str) -> str:
    # Extract common START/STEP/BLITZ formats
    match = re.findall(r"(START\s*\d+|STEP\s*\d+|BLITZ\s*\d+|\$\s?\d+|\d+\s?USD)", text, flags=re.IGNORECASE)
    if match:
        return ", ".join(m.strip() for m in match)
    return ""


# -----------------------------------------
#  REVENUE SUGGESTION
# -----------------------------------------

def suggest_revenue(text: str) -> str:
    match = re.search(r"(\d+)\s?(M|MILLION|B|BILLION)", text, flags=re.IGNORECASE)
    if match:
        val, unit = match.groups()
        return normalize_revenue(f"{val}{unit}")
    return ""


# -----------------------------------------
#  SECTOR SUGGESTION
# -----------------------------------------

POSSIBLE_SECTORS = [
    "government", "education", "healthcare", "finance", "technology", "manufacturing",
    "energy", "logistics", "construction", "insurance", "retail", "e-commerce",
    "hospitality", "media", "agriculture", "legal", "accounting",
]

def suggest_sector(text: str) -> str:
    low = text.lower()
    for sector in POSSIBLE_SECTORS:
        if sector.lower() in low:
            return normalize_sector(sector)
    return ""


# -----------------------------------------
#  POST DATE SUGGESTION
# -----------------------------------------

def suggest_post_date(text: str) -> str:
    # Simple YYYY-MM-DD detection
    match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", text)
    if match:
        return match.group(1)
    return ""


# -----------------------------------------
#  FULL PARSER
# -----------------------------------------

def suggest_listing_fields(raw_title: str, raw_text: str) -> dict:
    combined = f"{raw_title}\n{raw_text}"

    return {
        "access_type": suggest_access_type(combined),
        "country": suggest_country(combined),
        "privilege": suggest_privilege(combined),
        "price": suggest_price(combined),
        "sector": suggest_sector(combined),
        "revenue": suggest_revenue(combined),
        "post_date": suggest_post_date(combined),
        "description": raw_title[:200],  # fallback
    }
