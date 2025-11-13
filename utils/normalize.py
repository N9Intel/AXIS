import re

def normalize_broker_name(name: str) -> str:
    
    if not name:
        return ""
    
    name = name.strip().lower()

    name = re.sub(r"\s+", " ", name)
    name = re.sub(r"[^a-z0-9 ._-]", "", name)
    name = re.sub(r"\s+", " ", name).strip()

    return name 

SECTOR_MAP = {
    # government
    "gov": "government",
    "govt": "government",
    "government": "government",
    "public sector": "government",
    "public": "government",

    # education
    "edu": "education",
    "education": "education",
    "school": "education",
    "university": "education",
    "college": "education",

    # healthcare
    "health": "healthcare",
    "healthcare": "healthcare",
    "hospital": "healthcare",
    "med": "healthcare",
    "medical": "healthcare",

    # finance
    "fin": "finance",
    "finance": "finance",
    "financial": "finance",
    "bank": "finance",
    "banking": "finance",

    # technology
    "tech": "technology",
    "technology": "technology",
    "it": "technology",

    # generic
    "retail": "retail",
    "energy": "energy",
    "manufacturing": "manufacturing",
    "telecom": "telecom",
} #update this


def normalize_sector(sector: str) -> str:
    if not sector:
        return ""
    
    sector = sector.strip().lower()
    sector = re.sub(r"\s+", " ", sector)

    if sector in SECTOR_MAP:
        return SECTOR_MAP[sector]
    
    for key, value in  SECTOR_MAP.items():
        if sector.startswith(key) or sector.endswith(key):
            return value
    
    return sector 

def normalize_revenue(revenue: str) -> str:
    if not revenue:
        return ""

    revenue = revenue.strip().upper()

    for junk in ("USD", "US$", "$"):
        revenue = revenue.replace(junk, "")

    revenue = revenue.replace("MILLION", "M")
    revenue = revenue.replace("THOUSAND", "K")
    revenue = revenue.replace("BILLION", "B")

    revenue = revenue.replace(" ", "")
    revenue = revenue.replace("_", "-")
    revenue = revenue.replace("TO", "-")

    revenue = re.sub(r"-{2,}", "-", revenue)

    return revenue

