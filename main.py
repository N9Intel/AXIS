import sys

from utils.normalize import normalize_broker_name, normalize_sector, normalize_revenue
from utils.scoring import calculate_tier
from db.database import create_tables, insert_listing, get_all_listings, find_by_broker, find_by_tier, find_by_sector, search_query

def prompt(text: str) -> str:
    return input(text).strip()


def wait_for_enter() -> None:
    """Pause so the user can read output before returning to the menu."""
    input("Press ENTER to return to the menu...")


def save_listing() -> None:
    print("\n [Add listing]\n")
    
    broker_raw = prompt("Broker name: ")
    listings_raw = prompt("Total broker listings: ")
    sector_raw = prompt("Target sector: ")
    revenue_raw = prompt("Revenue range (e.g. 10-25M): ")

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
    tier = calculate_tier(listings)

    insert_listing(broker, listings, tier, sector, revenue)

    print("\n[OK] Saved listing:")
    print(f"  Broker:   {broker}")
    print(f"  Listings: {listings} (Tier: {tier})")
    print(f"  Sector:   {sector}")
    print(f"  Revenue:  {revenue}\n")

    wait_for_enter()

def print_rows(rows: list[tuple]) -> None:
    if not rows:
        print("\n[No results]\n")
        return
    
    print()
    for row in rows:
        row_id, broker, listings, tier, sector, revenue, created_at = row
        print(f"[{row_id}] {broker} | {listings} listings | {tier}")
        print(f"     Sector: {sector} | Revenue: {revenue} | Created: {created_at}")
        print()
    print()
    


def view_all_listings() -> None:
    print("\n[All listings]")
    rows = get_all_listings()
    print_rows(rows)
    wait_for_enter()


def find_by_broker_flow() -> None:
    print("\n[Find by broker]\n")
    broker_raw = prompt("Broker name: ")
    broker = normalize_broker_name(broker_raw)
    rows = find_by_broker(broker)
    print_rows(rows)
    wait_for_enter()


def find_by_tier_flow() -> None:
    print("\n[Find by tier]\n")
    tier_raw = prompt("Tier (High / Medium / Low): ").strip().lower()

    mapping = {
        "high": "High",
        "h": "High",
        "medium": "Medium",
        "m": "Medium",
        "low": "Low",
        "l": "Low",
    }

    tier = mapping.get(tier_raw)
    if tier is None:
        print("\n[ERROR] Tier must be High, Medium, or Low\n")
        return

    rows = find_by_tier(tier)
    print_rows(rows)
    wait_for_enter()


def find_by_sector_flow() -> None:
    print("\n[Find by sector]\n")
    sector_raw = prompt("Sector: ")
    sector = normalize_sector(sector_raw)
    rows = find_by_sector(sector)
    print_rows(rows)
    wait_for_enter()

def search_query_flow() -> None:
    print("\n[Search]\n")
    q = prompt("Query: ").lower().strip()

    if not q:
        print("\n[ERROR] Query cannot be empty\n")
        return
    
    rows = search_query(q)
    print_rows(rows)
    wait_for_enter()


def print_menu() -> None:
    print("AXIS v0.2 - IAB Listings")
    print("------------------------")
    print("[1] Add listing")
    print("[2] View all listings")
    print("[3] Find listings by broker")
    print("[4] Find listings by tier")
    print("[5] Find listings by sector")
    print("[6] Search (query)")
    print("[0] Exit")
    print()

def main() -> None:
    create_tables()

    while True:
        print_menu()
        choice = prompt("> ")

        if choice == "1":
            save_listing()
        elif choice == "2":
            view_all_listings()
        elif choice == "3":
            find_by_broker_flow()
        elif choice == "4":
            find_by_tier_flow()
        elif choice == "5":
            find_by_sector_flow()
        elif choice == "6":
            search_query_flow()
        elif choice == "0":
            print("\nGoodbye.\n")
            sys.exit(0)
        else:
            print("\n[ERROR] Invalid choice\n")

if __name__ == "__main__":
    main()
