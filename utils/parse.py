import re
from datetime import datetime
from typing import Dict, Any

from utils.normalize import normalize_sector, normalize_revenue, SECTOR_MAP

ACCESS_PATTERNS: Dict[str, str] = {
    "rdp": r"\brdp\b|\b3389\b",
    "vpn": r"\bvpn\b|\banyconnect\b|\bopenvpn\b",
    "citrix": r"\bcitrix\b",
    "ssh": r"\bssh\b",
    "vnc": r"\bvnc\b",
    "owa": r"\bowa\b|\bwebmail\b",
    "fortinet": r"\bforti(gate|client)?\b",
    "rdweb": r"\brdweb\b|\bremote desktop\b",
    "hyperv": r"\bhyper[-\s]?v\b",
}

def suggest_access_type(text: str, title: str = "") -> str:
    def _match(scope: str) -> str:
        low = scope.lower()
        for access, pattern in ACCESS_PATTERNS.items():
            if re.search(pattern, low):
                return access
        return ""
    if title:
        hit = _match(title)
        if hit:
            return hit
    return _match(text)


ISO_COUNTRY_CODES = {
    "AF","AX","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM","AW","AU","AT","AZ",
    "BS","BH","BD","BB","BY","BE","BZ","BJ","BM","BT","BO","BQ","BA","BW","BV","BR",
    "IO","BN","BG","BF","BI","KH","CM","CA","CV","KY","CF","TD","CL","CN","CX","CC",
    "CO","KM","CD","CG","CK","CR","CI","HR","CU","CW","CY","CZ","DK","DJ","DM","DO",
    "EC","EG","SV","GQ","ER","EE","SZ","ET","FK","FO","FJ","FI","FR","GF","PF","TF",
    "GA","GM","GE","DE","GH","GI","GR","GL","GD","GP","GU","GT","GG","GN","GW","GY",
    "HT","HM","VA","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IM","IL","IT","JM",
    "JP","JE","JO","KZ","KE","KI","KP","KR","KW","KG","LA","LV","LB","LS","LR","LY",
    "LI","LT","LU","MO","MG","MW","MY","MV","ML","MT","MH","MQ","MR","MU","YT","MX",
    "FM","MD","MC","MN","ME","MS","MA","MZ","MM","NA","NR","NP","NL","NC","NZ","NI",
    "NE","NG","NU","NF","MP","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PN",
    "PL","PT","PR","QA","MK","RO","RU","RW","RE","BL","SH","KN","LC","MF","PM","VC",
    "WS","SM","ST","SA","SN","RS","SC","SL","SG","SX","SK","SI","SB","SO","ZA","GS",
    "SS","ES","LK","SD","SR","SJ","SE","CH","SY","TW","TJ","TZ","TH","TL","TG","TK",
    "TO","TT","TN","TR","TM","TC","TV","UG","UA","AE","GB","US","UM","UY","UZ","VU",
    "VE","VN","VG","VI","WF","EH","YE","ZM","ZW"
}

COUNTRY_ALIAS = {
    "US": ["usa", "u.s.", "u.s", "america", "american", "murica", "🇺🇸"],
    "GB": ["uk", "gb", "england", "britain", "brits", "🇬🇧"],
    "RU": ["ru", "russia", "russian", "rf", "rossiya", "🇷🇺"],
    "UA": ["ua", "ukraine", "ukrainian", "🇺🇦"],
    "CN": ["cn", "china", "prc", "🇨🇳"],
    "DE": ["de", "germany", "deutsch", "🇩🇪"],
    "FR": ["fr", "france", "french", "🇫🇷"],
    "ES": ["es", "spain", "españa", "spanish", "🇪🇸"],
    "IT": ["it", "italy", "italian", "🇮🇹"],
    "AU": ["au", "australia", "aussie", "🇦🇺"],
    "CA": ["ca", "canada", "canadian", "🇨🇦"],
    "BR": ["br", "brazil", "brasil", "🇧🇷"],
    "MX": ["mx", "mexico", "mexican", "🇲🇽"],
}

KEYWORD_COUNTRY_MAP = {
    "US": [
        "united states", "america", "american", "yanks", "yankee",
        "murica", "states"
    ],
    "GB": [
        "united kingdom", "britain", "great britain", "england",
        "scotland", "wales", "british", "uk"
    ],
    "NL": [
        "netherlands", "holland", "dutch"
    ],
    "DE": [
        "germany", "deutsch", "deutschland", "german"
    ],
    "FR": [
        "france", "french", "republique francaise"
    ],
    "ES": [
        "spain", "españa", "spanish"
    ],
    "IT": [
        "italy", "italian", "italia"
    ],
    "PL": [
        "poland", "polish"
    ],
    "SE": [
        "sweden", "swedish", "sverige"
    ],
    "NO": [
        "norway", "norwegian", "norge"
    ],
    "DK": [
        "denmark", "danish", "dansk"
    ],
    "FI": [
        "finland", "finnish", "suomi"
    ],
    "RU": [
        "russia", "russian", "rossiya", "rf", "moscow"
    ],
    "UA": [
        "ukraine", "ukrainian", "kyiv", "kiev"
    ],
    "BY": [
        "belarus", "belarussian", "belorussia"
    ],
    "RO": [
        "romania", "romanian"
    ],
    "BG": [
        "bulgaria", "bulgarian"
    ],
    "GR": [
        "greece", "greek", "hellas"
    ],
    "PT": [
        "portugal", "portuguese"
    ],
    "CZ": [
        "czech", "czechia"
    ],
    "SK": [
        "slovakia", "slovak"
    ],
    "HU": [
        "hungary", "hungarian", "magyar"
    ],
    "CH": [
        "switzerland", "swiss"
    ],
    "AT": [
        "austria", "austrian"
    ],
    "BE": [
        "belgium", "belgian"
    ],
    "IE": [
        "ireland", "irish", "eire"
    ],
    "IS": [
        "iceland", "icelandic"
    ],
    "CA": [
        "canada", "canadian"
    ],
    "MX": [
        "mexico", "mexican"
    ],
    "BR": [
        "brazil", "brasil", "brazilian"
    ],
    "AR": [
        "argentina", "argentinian"
    ],
    "CL": [
        "chile", "chilean"
    ],
    "CO": [
        "colombia", "colombian"
    ],
    "PE": [
        "peru", "peruvian"
    ],
    "VE": [
        "venezuela", "venezuelan"
    ],
    "EC": [
        "ecuador", "ecuadorian"
    ],
    "UY": [
        "uruguay", "uruguayan"
    ],
    "AU": [
        "australia", "aussie", "australian"
    ],
    "NZ": [
        "new zealand", "kiwi"
    ],
    "JP": [
        "japan", "japanese", "nippon"
    ],
    "KR": [
        "south korea", "korean", "republic of korea"
    ],
    "KP": [
        "north korea", "dprk"
    ],
    "CN": [
        "china", "chinese", "prc", "peoples republic of china"
    ],
    "TW": [
        "taiwan", "taiwanese", "roc"
    ],
    "SG": [
        "singapore", "singaporean"
    ],
    "IN": [
        "india", "indian", "bharat"
    ],
    "PK": [
        "pakistan", "pakistani"
    ],
    "BD": [
        "bangladesh", "bangladeshi"
    ],
    "LK": [
        "sri lanka", "ceylon"
    ],
    "PH": [
        "philippines", "filipino"
    ],
    "ID": [
        "indonesia", "indonesian"
    ],
    "MY": [
        "malaysia", "malaysian"
    ],
    "TH": [
        "thailand", "thai"
    ],
    "VN": [
        "vietnam", "vietnamese"
    ],
    "TR": [
        "turkey", "turkish", "türkiye"
    ],
    "AE": [
        "uae", "united arab emirates", "emirati", "dubai", "abu dhabi"
    ],
    "SA": [
        "saudi arabia", "saudi"
    ],
    "IR": [
        "iran", "persian", "tehran"
    ],
    "IQ": [
        "iraq", "iraqi"
    ],
    "IL": [
        "israel", "israeli"
    ],
    "EG": [
        "egypt", "egyptian"
    ],
    "ZA": [
        "south africa", "south african"
    ],
    "NG": [
        "nigeria", "nigerian"
    ],
    "KE": [
        "kenya", "kenyan"
    ],
    "UG": [
        "uganda", "ugandan"
    ],
    "TZ": [
        "tanzania", "tanzanian"
    ],
    "ET": [
        "ethiopia", "ethiopian"
    ],
    "GH": [
        "ghana", "ghanaian"
    ],
    "DZ": [
        "algeria", "algerian"
    ],
    "MA": [
        "morocco", "moroccan"
    ],
    "TN": [
        "tunisia", "tunisian"
    ],
    "LY": [
        "libya", "libyan"
    ],
}


def suggest_country(text: str, title: str = "") -> str:
    """
    Detect country as ISO alpha-2.
    Prefers title, then full text.
    Uses:
      - [US]/(GB)/{RU} style tags
      - standalone ISO tokens (US, DE, FR)
      - KEYWORD_COUNTRY_MAP (full names, demonyms, slang)
      - COUNTRY_ALIAS (slang, emojis, abbreviations)
    """

    def _scan_scope(raw: str) -> str:
        low = raw.lower()

        m = re.search(r"[\[\(\{]([A-Z]{2})[\]\)\}]", raw)
        if m:
            code = m.group(1)
            if code in ISO_COUNTRY_CODES:
                return code


        tokens = re.findall(r"\b([A-Z]{2})\b", raw)
        for tok in tokens:
            if tok in ISO_COUNTRY_CODES:
                return tok

        
        for code, words in KEYWORD_COUNTRY_MAP.items():
            for w in words:
                if w in low:
                    return code
                
        for code, aliases in COUNTRY_ALIAS.items():
            for a in aliases:
                if re.search(r"\W", a):
                    if a in raw:
                        return code
                else:
                    if re.search(rf"\b{re.escape(a.lower())}\b", low):
                        return code

        return ""

    if title:
        hit = _scan_scope(title)
        if hit:
            return hit

    return _scan_scope(text)


def suggest_privilege(text: str) -> str:
    low = text.lower()

    if re.search(r"\bno\s+(domain\s+admin|da|admin)\b", low):
        return ""

    privs: list[str] = []

    if re.search(r"\bdomain\s+admin\b", low) or re.search(r"\bda\b", low):
        privs.append("domain admin")

    if re.search(r"\blocal\s+admin\b", low):
        privs.append("local admin")

    if not any(p in ("domain admin", "local admin") for p in privs) and re.search(r"\badmin(istrator)?\b", low):
        privs.append("admin")

    if re.search(r"\buser\b", low):
        privs.append("user")

    seen = set()
    unique = []
    for p in privs:
        if p not in seen:
            seen.add(p)
            unique.append(p)

    return ", ".join(unique) if unique else ""

PRICE_NUMBER_RE = re.compile(
    r"\$?\s*([\d][\d.,]*)\s*(usd|eur|usd\.?|eur\.?)?",
    flags=re.IGNORECASE,
)

def _is_revenueish(num: str, line: str) -> bool:
    return bool(re.search(rf"{re.escape(num)}\s*(m|million|b|billion|k|thousand)", line, flags=re.IGNORECASE))

def suggest_price(text: str) -> str:
    lines = text.splitlines()
    tiers = []
    loose_prices = []

    TIER_KEYWORDS = ("start", "step", "blitz", "flash")

    for line in lines:
        low = line.lower().strip()
        if not low:
            continue

        # 1) START / STEP / BLITZ / FLASH
        if any(k in low for k in TIER_KEYWORDS):
            def _grab(label: str) -> None:
                m = re.search(
                    rf"{label}[:=\s]+\$?\s*([\d,]+)",
                    low,
                    flags=re.IGNORECASE,
                )
                if m:
                    amount = m.group(1).replace(",", "")
                    tiers.append(f"{label.upper()} {amount}")

            _grab("start")
            _grab("step")
            _grab("blitz")
            _grab("flash")
            continue

        # 2) Lines that mention “price”
        if "price" in low:
            for num, _cur in PRICE_NUMBER_RE.findall(line):
                if _is_revenueish(num, line):
                    continue
                cleaned = num.replace(",", "")
                loose_prices.append(cleaned)

    if tiers:
        return ", ".join(tiers)

    if loose_prices:
        seen = set()
        unique = []
        for p in loose_prices:
            if p not in seen:
                seen.add(p)
                unique.append(p)
        return ", ".join(unique[:3])

    return ""


def suggest_revenue(text: str) -> str:
    low = text.lower()

    kk_match = re.search(r"\b(\d+)\s*kk\b", low)
    if kk_match:
        num = kk_match.group(1)
        return normalize_revenue(f"{num}M")

    range_match = re.search(
        r"([\d.,]+)\s*[-–]\s*([\d.,]+)\s*(M|MILLION|K|THOUSAND|B|BILLION)",
        text,
        flags=re.IGNORECASE,
    )
    if range_match:
        lo, hi, unit = range_match.groups()
        lo_clean = lo.replace(",", "")
        hi_clean = hi.replace(",", "")
        unit_clean = unit.strip().upper()[0]
        return f"{lo_clean}-{hi_clean}{unit_clean}"

    single = re.search(
        r"(revenue|turnover|income)\s*[:\-]*\s*[<\$\s]*([\d.,]+)\s*(M|MILLION|K|THOUSAND|B|BILLION)",
        text,
        flags=re.IGNORECASE,
    )
    if single:
        _, num, unit = single.groups()
        num_clean = num.replace(",", "")
        return normalize_revenue(f"{num_clean}{unit}")

    generic = re.search(
        r"\b([\d.]+)\s*(M|MILLION|K|THOUSAND|B|BILLION)\b",
        text,
        flags=re.IGNORECASE,
    )
    if generic:
        num, unit = generic.groups()
        num_clean = num.replace(",", "")
        return normalize_revenue(f"{num_clean}{unit}")

    return ""



def suggest_sector(text: str, title: str = "") -> str:
    low_title = title.lower()
    low = text.lower()

    ind = re.search(r"(industry|sector)[:\s]+(.+)", low)
    if ind:
        val = ind.group(2)
        for key in SECTOR_MAP.keys():
            if key in val:
                return normalize_sector(key)

    for key in SECTOR_MAP.keys():
        if key in low_title:
            return normalize_sector(key)

    for key in SECTOR_MAP.keys():
        if key in low:
            return normalize_sector(key)

    return ""


def suggest_post_date(text: str) -> str:
    patterns = [
        (r"\b(20\d{2}-\d{2}-\d{2})\b", "%Y-%m-%d"),
        (r"\b(\d{2}\.\d{2}\.20\d{2})\b", "%d.%m.%Y"),
        (r"\b(20\d{2}/\d{2}/\d{2})\b", "%Y/%m/%d"),
    ]
    for regex, fmt in patterns:
        m = re.search(regex, text)
        if m:
            try:
                return datetime.strptime(m.group(1), fmt).strftime("%Y-%m-%d")
            except:
                pass
    return ""


def _build_description(title: str, text: str, max_len: int = 200) -> str:
    low = text.lower()

    access = ""
    if "rdp" in low: access = "RDP"
    elif "vpn" in low: access = "VPN"
    elif "ssh" in low: access = "SSH"

    country = ""
    m = re.search(r"\b([A-Z]{2})\b", text)
    if m:
        country = m.group(1)

    rev = ""
    m = re.search(r"([\d.]+)\s*(M|B|K)", text, flags=re.IGNORECASE)
    if m:
        rev = f"{m.group(1)}{m.group(2).upper()}"

    parts = [title.strip()]
    if access: parts.append(access)
    if country: parts.append(country)
    if rev: parts.append(rev)

    desc = " | ".join(parts)

    return desc[: max_len - 3] + "..." if len(desc) > max_len else desc


def suggest_listing_fields(raw_title: str, raw_text: str) -> Dict[str, Any]:
    combined = f"{raw_title}\n{raw_text}"
    country = suggest_country(combined, title=raw_title)

    return {
        "access_type": suggest_access_type(combined, title=raw_title),
        "country": country,
        "privilege": suggest_privilege(combined),
        "price": suggest_price(combined),
        "sector": suggest_sector(combined, title=raw_title),
        "revenue": suggest_revenue(combined),
        "post_date": suggest_post_date(combined),
        "description": _build_description(raw_title, raw_text),
    }
