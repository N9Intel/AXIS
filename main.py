import sys

from utils.normalize import normalize_broker_name, normalize_sector, normalize_revenue
from utils.scoring import calculate_tier
from db.database import create_tables, insert_listing, get_all_listings, find_by_broker, find_by_sector, search_query

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

    if not broker:
        print("\n[ERROR] Broker name is required and cannot be empty.\n")
        wait_for_enter()
        return

    if not sector:
        print("\n[ERROR] Sector is required and cannot be empty.\n")
        wait_for_enter()
        return

    if not revenue:
        print("\n[ERROR] Revenue is required and cannot be empty.\n")
        wait_for_enter()
        return

    
    if broker != normalize_broker_name(broker_raw):
        print(f"\n[INFO] Normalized broker name to: {broker}")

    try:
        insert_listing(broker, listings, tier, sector, revenue)
    except Exception as e:
        print(f"\n[ERROR] Failed to save listing to database: {e}\n")
        wait_for_enter()
        return


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
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Interrupted by user. Exiting.\n")
        sys.exit(0)
