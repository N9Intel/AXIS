import csv
from pathlib import Path

from utils.normalize import normalize_broker_name, normalize_sector, normalize_revenue
from utils.scoring import calculate_tier

DATA_DIR = Path("data")
LISTINGS_FILE = DATA_DIR / "listings.csv"
CSV_FIELDS = ["broker", "listings", "tier", "sector", "revenue"]

def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def save_listing(broker: str, listings: int, sector: str, revenue: str) -> None:
    row = {
        "broker": broker,
        "listings": listings,
        "tier": calculate_tier(listings),
        "sector": sector,
        "revenue": revenue,
    }

    file_exists = LISTINGS_FILE.exists()

    with open(LISTINGS_FILE, "a", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


def main() -> None:
    ensure_data_dir()
    print("AXIS v0.1 input\n")

    broker_raw = input("Broker name: ").strip()
    listings_raw = input("Total broker listings: ").strip()
    sector_raw = input("Target sector: ").strip()
    revenue_raw = input("Revenue range (e.g. 10-25M): ").strip()

    try:
        listings = int(listings_raw)
        if listings < 0:
            raise ValueError
    except ValueError:
        print("\n[ERROR] Listings must be a whole number (0 or more)")
        return

    broker = normalize_broker_name(broker_raw)
    sector = normalize_sector(sector_raw)
    revenue = normalize_revenue(revenue_raw)

    save_listing(broker, listings, sector, revenue)

    print(f"\nSaved listing → {LISTINGS_FILE}")
    print(f"Broker: {broker}")
    print(f"Listings: {listings}  (Tier: {calculate_tier(listings)})")
    print(f"Sector: {sector}")
    print(f"Revenue: {revenue}")


if __name__ == "__main__":
    main()
