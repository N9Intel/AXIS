import sys

from utils.normalize import normalize_broker_name, normalize_sector, normalize_revenue
from utils.scoring import calculate_tier
from db.database import create_tables,insert_broker,get_all_brokers,find_broker_by_name,insert_listing,get_all_listings,find_listings_by_broker_name,find_listings_by_sector,search_query,find_duplicate_listings
from datetime import datetime

def validate_date(date_str: str) -> bool:
    """Return True if date is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def prompt(text: str) -> str:
    return input(text).strip()


def wait_for_enter() -> None:
    """Pause so the user can read output before returning to the menu."""
    input("Press ENTER to return to the menu...")


def print_brokers(rows):
    if not rows:
        print("\n[No brokers found]\n")
        return

    print()
    for broker_id, name, raw_name, notes, created_at in rows:
        display_name = raw_name or name
        print(f"[{broker_id}] {display_name} (normalized: {name})")
        if notes:
            preview = notes if len(notes) <= 80 else notes[:77] + "..."
            print(f"    Notes: {preview}")
        print(f"    Created: {created_at}")
        print()
    print()


def print_listings(rows):
    if not rows:
        print("\n[No listings found]\n")
        return

    print()
    for (
        listing_id,
        broker_name,
        access_type,
        country,
        privilege,
        price,
        description,
        source,
        post_date,
        sector,
        revenue,
        created_at,
    ) in rows:
        print(f"[{listing_id}] Broker: {broker_name}")
        print(
            f"    Access: {access_type or '-'} | Country: {country or '-'} | "
            f"Privilege: {privilege or '-'}"
        )
        print(f"    Price: {price or '-'} | Sector: {sector or '-'} | Revenue: {revenue or '-'}")
        print(f"    Source: {source or '-'} | Post date: {post_date or '-'}")
        if description:
            short_desc = description if len(description) <= 100 else description[:97] + "..."
            print(f"    Desc: {short_desc}")
        print(f"    Created: {created_at}")
        print()
    print()


def add_broker_flow() -> None:
    print("\n[Add broker]\n")

    raw_name = prompt("Broker name: ")
    notes = prompt("Notes (optional): ")

    normalized_name = normalize_broker_name(raw_name)

    if not normalized_name:
        print("\n[ERROR] Broker name cannot be empty.\n")
        wait_for_enter()
        return

    existing = find_broker_by_name(normalized_name)
    if existing:
        broker_id = existing[0]
        print(f"\n[WARN] Broker already exists with ID {broker_id}.")
        choice = prompt("Add duplicate broker anyway? (y/N): ").lower()
        if choice != "y":
            wait_for_enter()
            return

    created_id = insert_broker(normalized_name, raw_name, notes)
    print(f"\n[OK] Broker added with ID {created_id}\n")
    wait_for_enter()


def view_brokers_flow() -> None:
    print("\n[All brokers]\n")
    rows = get_all_brokers()
    print_brokers(rows)
    wait_for_enter()


def add_listing_flow() -> None:
    print("\n[Add listing]\n")

    broker_raw = prompt("Broker name (must already exist): ")
    broker_name = normalize_broker_name(broker_raw)

    if not broker_name:
        print("\n[ERROR] Broker name cannot be empty\n")
        wait_for_enter()
        return

    broker_row = find_broker_by_name(broker_name)
    if not broker_row:
        print(f"\n[ERROR] Broker '{broker_name}' not found. Add it first using option [1].\n")
        wait_for_enter()
        return

    broker_id = broker_row[0]

    access_type = prompt("Access type (rdp/vpn/etc): ").lower()
    country = prompt("Country (US/GB/RU/etc): ").upper()
    privilege = prompt("Privilege (admin/user, optional): ").lower()
    price = prompt("Price (e.g. START 700, STEP 200, BLITZ 1900 USD): ")
    description = prompt("Short description: ")
    source = prompt("Source forum (exploit/ramp/etc): ").lower()
    while True:
        post_date = prompt("Post date (YYYY-MM-DD): ").strip()
        if not post_date:
            print("\n[ERROR] Post date cannot be empty.\n")
            continue

        if validate_date(post_date):
            break
        else:
            print("\n[ERROR] Invalid date format. Use YYYY-MM-DD (e.g. 2025-09-10).\n")

    sector = normalize_sector(prompt("Sector (optional): "))
    revenue = normalize_revenue(prompt("Revenue (optional): "))

    if not access_type:
        print("\n[ERROR] Access type is required\n")
        wait_for_enter()
        return

    if not country:
        print("\n[ERROR] Country is required\n")
        wait_for_enter()
        return

    if not price:
        print("\n[ERROR] Price is required\n")
        wait_for_enter()
        return

    if not description:
        print("\n[ERROR] Description is required\n")
        wait_for_enter()
        return
    
    duplicates = find_duplicate_listings(
        broker_id=broker_id,
        access_type=access_type,
        country=country,
        price=price,
        description=description,
        source=source,
        post_date=post_date,
        sector=sector,
        revenue=revenue,
    )

    if duplicates:
        print("\n[WARN] Possible duplicate listing(s) found:\n")
        print_listings(duplicates)

        choice = prompt("Insert anyway? (y/N): ").lower()
        if choice != "y":
            print("\n[INFO] Listing was NOT saved.\n")
            wait_for_enter()
            return

    listing_id = insert_listing(
        broker_id,
        access_type,
        country,
        privilege,
        price,
        description,
        source,
        post_date,
        sector,
        revenue,
    )

    print(f"\n[OK] Added listing with ID {listing_id}\n")
    wait_for_enter()


def view_listings_flow() -> None:
    print("\n[All listings]\n")
    rows = get_all_listings()
    print_listings(rows)
    wait_for_enter()


def find_listings_by_broker_flow() -> None:
    print("\n[Find listings by broker]\n")
    broker_raw = prompt("Broker name: ")
    broker_name = normalize_broker_name(broker_raw)

    if not broker_name:
        print("\n[ERROR] Broker name cannot be empty\n")
        wait_for_enter()
        return

    rows = find_listings_by_broker_name(broker_name)
    print_listings(rows)
    wait_for_enter()


def find_listings_by_sector_flow() -> None:
    print("\n[Find listings by sector]\n")
    sector_raw = prompt("Sector: ")
    sector = normalize_sector(sector_raw)

    if not sector:
        print("\n[ERROR] Sector cannot be empty\n")
        wait_for_enter()
        return

    rows = find_listings_by_sector(sector)
    print_listings(rows)
    wait_for_enter()





def search_query_flow() -> None:
    print("\n[Search]\n")
    q = prompt("Query: ").lower().strip()

    if not q:
        print("\n[ERROR] Query cannot be empty\n")
        wait_for_enter()
        return
    
    rows = search_query(q)
    print_listings(rows)
    wait_for_enter()


def print_menu() -> None:
    print("AXIS v0.2 - IAB Listings")
    print("------------------------")
    print("[1] Add broker")
    print("[2] View brokers")
    print("[3] Add listing")
    print("[4] View listings ")
    print("[5] Find listings by broker")
    print("[6] Find listings by sector")
    print("[7] Search (query)")
    print("[0] Exit")
    print()

def main() -> None:
    create_tables()

    while True:
        print_menu()
        choice = prompt("> ")

        if choice == "1":
            add_broker_flow()
        elif choice == "2":
            view_brokers_flow()
        elif choice == "3":
            add_listing_flow()
        elif choice == "4":
            view_listings_flow()
        elif choice == "5":
            find_listings_by_broker_flow()
        elif choice == "6":
            find_listings_by_sector_flow()
        elif choice == "7":
            search_query_flow()
        elif choice == "0":
            print("\nGoodbye.\n")
            sys.exit(0)
        else:
            print("\n[ERROR] Invalid choice\n")
            wait_for_enter()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Interrupted by user. Exiting.\n")
        sys.exit(0)
