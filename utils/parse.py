import re
from utils.normalize import normalize_sector, normalize_revenue, SECTOR_MAP

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
    """
    Try to extract pricing info from the text.

    Priority:
    1. START / STEP / BLITZ lines
    2. Lines explicitly mentioning 'price'
    We ignore random numbers on non-price lines (e.g. code=1014, host=+1000).
    """
    lines = text.splitlines()
    tiers: list[str] = []
    loose_prices: list[str] = []

    for line in lines:
        low = line.lower()

        # Skip empty / near-empty lines
        if not low.strip():
            continue

        # ---------------------------------
        # 1) START / STEP / BLITZ patterns
        # ---------------------------------
        if any(k in low for k in ("start", "step", "blitz")):
            start_match = re.search(r"start[:=\s]+\$?\s*([\d,]+)", low, flags=re.IGNORECASE)
            if start_match:
                tiers.append(f"START {start_match.group(1).replace(',', '')}")

            step_match = re.search(r"step[:=\s]+\$?\s*([\d,]+)", low, flags=re.IGNORECASE)
            if step_match:
                tiers.append(f"STEP {step_match.group(1).replace(',', '')}")

            blitz_match = re.search(r"blitz[:=\s]+\$?\s*([\d,]+)", low, flags=re.IGNORECASE)
            if blitz_match:
                tiers.append(f"BLITZ {blitz_match.group(1).replace(',', '')}")

            continue  # done with this line

        # ---------------------------------
        # 2) Generic "price" lines
        #    e.g. "price is 1400$", "price: 900 usd"
        # ---------------------------------
        if "price" in low:
            # find numbers on this line that look like prices
            candidates = re.findall(
                r"\$?\s*([\d][\d.,]*)\s*(usd)?",
                line,
                flags=re.IGNORECASE,
            )
            for num, _ in candidates:
                # check context around the number to avoid revenue-like "28m", "5 million"
                context_pattern = rf"{re.escape(num)}\s*(m|million|b|billion|k|thousand)"
                if re.search(context_pattern, line, flags=re.IGNORECASE):
                    continue  # looks more like revenue, skip

                cleaned = num.replace(",", "")
                loose_prices.append(cleaned)

    # If we got any tiered prices, return them joined
    if tiers:
        return ", ".join(tiers)

    # Otherwise, if we found price values from 'price' lines, return first few
    if loose_prices:
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for p in loose_prices:
            if p not in seen:
                seen.add(p)
                unique.append(p)
        return ", ".join(unique[:3])

    return ""



# -----------------------------------------
#  REVENUE SUGGESTION
# -----------------------------------------

def suggest_revenue(text: str) -> str:
    low = text.lower()

    kk_match = re.search(r"\b(\d+)\s*kk\b", low, flags=re.IGNORECASE)
    if kk_match:
        num = kk_match.group(1)
        return normalize_revenue(f"{num}M")

    rev_line = re.search(
        r"revenue\s*[:\-]*\s*[<\$\s]*([\d.,]+)\s*(M|MILLION|K|THOUSAND|B|BILLION)",
        text,
        flags=re.IGNORECASE,
    )
    if rev_line:
        num, unit = rev_line.groups()
        num = num.replace(",", "")
        return normalize_revenue(f"{num}{unit}")

    generic = re.search(
        r"([\d.]+)\s*(M|MILLION|K|THOUSAND|B|BILLION)",
        text,
        flags=re.IGNORECASE,
    )
    if generic:
        num, unit = generic.groups()
        num = num.replace(",", "")
        return normalize_revenue(f"{num}{unit}")

    return ""

# -----------------------------------------
#  SECTOR SUGGESTION
# -----------------------------------------

def suggest_sector(text: str) -> str:
    low = text.lower()

    # 1) Prefer explicit "Industry: ..." style hints
    industry_line = re.search(r"industry[:\s]+(.+)", low)
    if industry_line:
        industry_val = industry_line.group(1)
        for key in SECTOR_MAP.keys():
            if key in industry_val:
                return normalize_sector(key)

    # 2) Fallback: scan whole text for any sector keyword
    for key in SECTOR_MAP.keys():
        if key in low:
            return normalize_sector(key)

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
