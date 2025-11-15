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
    # -----------------
    # Government / Public sector
    # -----------------
    "gov": "government",
    "govt": "government",
    "government": "government",
    "public sector": "government",
    "public administration": "government",
    "local government": "government",
    "state government": "government",
    "federal government": "government",
    "municipality": "government",
    "city council": "government",
    "ministry": "government",
    "agency": "government",
    "public service": "government",
    "civil service": "government",

    # -----------------
    # Education
    # -----------------
    "edu": "education",
    "education": "education",
    "school": "education",
    "schools": "education",
    "university": "education",
    "universities": "education",
    "college": "education",
    "colleges": "education",
    "k-12": "education",
    "k12": "education",
    "academy": "education",
    "academic": "education",
    "training": "education",
    "e-learning": "education",
    "elearning": "education",

    # -----------------
    # Healthcare / Life sciences
    # -----------------
    "health": "healthcare",
    "healthcare": "healthcare",
    "hospital": "healthcare",
    "hospitals": "healthcare",
    "clinic": "healthcare",
    "clinics": "healthcare",
    "med": "healthcare",
    "medical": "healthcare",
    "pharma": "pharmaceuticals",
    "pharmaceutical": "pharmaceuticals",
    "pharmaceuticals": "pharmaceuticals",
    "biotech": "biotech",
    "life sciences": "biotech",
    "laboratory": "healthcare",
    "lab": "healthcare",

    # -----------------
    # Finance / Banking / Insurance
    # -----------------
    "fin": "finance",
    "finserv": "finance",
    "finance": "finance",
    "financial": "finance",
    "financial services": "finance",
    "bank": "finance",
    "banking": "finance",
    "credit union": "finance",
    "investment": "finance",
    "asset management": "finance",
    "wealth management": "finance",
    "securities": "finance",
    "brokerage": "finance",
    "insurance": "insurance",
    "insurer": "insurance",
    "reinsurance": "insurance",
    "pension": "finance",
    "fintech": "finance",

    # -----------------
    # Technology / IT / Software
    # -----------------
    "tech": "technology",
    "technology": "technology",
    "information technology": "technology",
    "it services": "technology",
    "it service": "technology",
    "software": "technology",
    "software development": "technology",
    "saas": "technology",
    "cloud": "technology",
    "cloud services": "technology",
    "managed services": "technology",
    "msp": "technology",
    "it consulting": "technology",
    "hosting": "technology",
    "datacenter": "technology",
    "data center": "technology",
    "isp": "telecom",
    "cybersecurity": "technology",
    "security vendor": "technology",

    # -----------------
    # Telecom / Media / Entertainment
    # -----------------
    "telecom": "telecom",
    "telecommunications": "telecom",
    "telco": "telecom",
    "mobile operator": "telecom",
    "carrier": "telecom",
    "media": "media",
    "broadcasting": "media",
    "tv": "media",
    "television": "media",
    "streaming": "media",
    "entertainment": "entertainment",
    "gaming": "entertainment",
    "video game": "entertainment",

    # -----------------
    # Retail / E-commerce / Consumer
    # -----------------
    "retail": "retail",
    "retailer": "retail",
    "wholesale": "retail",
    "wholesaler": "retail",
    "ecommerce": "ecommerce",
    "e-commerce": "ecommerce",
    "online shop": "ecommerce",
    "online store": "ecommerce",
    "consumer goods": "retail",
    "fmcg": "retail",  # fast-moving consumer goods

    # -----------------
    # Manufacturing / Industrial / Engineering
    # -----------------
    "manufacturing": "manufacturing",
    "manufacturer": "manufacturing",
    "industrial": "industrial",
    "industry": "industrial",
    "engineering": "industrial",
    "plant": "industrial",
    "factory": "industrial",
    "factories": "industrial",
    "automotive": "automotive",
    "auto": "automotive",
    "car maker": "automotive",
    "aerospace": "aerospace_defense",
    "defense": "aerospace_defense",
    "defence": "aerospace_defense",
    "defense contractor": "aerospace_defense",

    # -----------------
    # Energy / Utilities / Natural resources
    # -----------------
    "energy": "energy",
    "oil": "oil_and_gas",
    "gas": "oil_and_gas",
    "oil & gas": "oil_and_gas",
    "oil and gas": "oil_and_gas",
    "petrochemical": "oil_and_gas",
    "power": "utilities",
    "electric": "utilities",
    "electricity": "utilities",
    "utility": "utilities",
    "utilities": "utilities",
    "water": "utilities",
    "water utility": "utilities",
    "waste management": "utilities",
    "mining": "mining",
    "minerals": "mining",
    "metals": "mining",

    # -----------------
    # Transport / Logistics / Travel
    # -----------------
    "transport": "transportation",
    "transportation": "transportation",
    "logistics": "logistics",
    "shipping": "logistics",
    "freight": "logistics",
    "supply chain": "logistics",
    "airline": "transportation",
    "airport": "transportation",
    "rail": "transportation",
    "railway": "transportation",
    "public transit": "transportation",
    "trucking": "transportation",
    "delivery": "logistics",
    "postal": "logistics",

    # -----------------
    # Construction / Real Estate / Infrastructure
    # -----------------
    "construction": "construction",
    "builder": "construction",
    "engineering & construction": "construction",
    "real estate": "real_estate",
    "property management": "real_estate",
    "realtor": "real_estate",
    "housing": "real_estate",
    "architecture": "construction",
    "infrastructure": "construction",

    # -----------------
    # Agriculture / Food / Beverage
    # -----------------
    "agriculture": "agriculture",
    "farming": "agriculture",
    "farm": "agriculture",
    "agro": "agriculture",
    "food": "food_and_beverage",
    "food & beverage": "food_and_beverage",
    "food and beverage": "food_and_beverage",
    "restaurant": "food_and_beverage",
    "restaurants": "food_and_beverage",
    "catering": "food_and_beverage",
    "hospitality": "hospitality",
    "hotel": "hospitality",
    "hotels": "hospitality",
    "resort": "hospitality",
    "travel": "hospitality",
    "tourism": "hospitality",

    # -----------------
    # Professional services / Legal / Consulting
    # -----------------
    "professional services": "professional_services",
    "consulting": "professional_services",
    "consultancy": "professional_services",
    "management consulting": "professional_services",
    "law": "legal",
    "law firm": "legal",
    "legal": "legal",
    "attorney": "legal",
    "accounting": "accounting",
    "accountant": "accounting",
    "audit": "accounting",
    "tax": "accounting",
    "hr services": "professional_services",
    "staffing": "professional_services",
    "recruitment": "professional_services",
    "outsourcing": "professional_services",
    "bpo": "professional_services",  # business process outsourcing

    # -----------------
    # Non-profit / NGO / Religion
    # -----------------
    "nonprofit": "nonprofit",
    "non-profit": "nonprofit",
    "ngo": "nonprofit",
    "charity": "nonprofit",
    "foundation": "nonprofit",
    "religious": "nonprofit",
    "church": "nonprofit",
    "ministry (religious)": "nonprofit",

    # -----------------
    # Other / Misc niche sectors
    # -----------------
    "media & entertainment": "entertainment",
    "sports": "entertainment",
    "casino": "gambling",
    "gambling": "gambling",
    "betting": "gambling",
    "lottery": "gambling",
    "crypto": "crypto",
    "cryptocurrency": "crypto",
    "blockchain": "crypto",
    "exchange": "finance",
    "stock exchange": "finance",
    "printing": "industrial",
    "publishing": "media",
}


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

