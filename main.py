import sys
from pathlib import Path
from utils.normalize import normalize_broker_name, normalize_sector, normalize_revenue
from utils.scoring import calculate_tier
from utils.parse import suggest_listing_fields
from db.database import create_tables,insert_broker,get_all_brokers,find_broker_by_name,insert_listing,get_all_listings,find_listings_by_broker_name,find_listings_by_sector,search_query,find_duplicate_listings,get_listing_by_id, update_listing,get_broker_by_id,delete_listing,get_summary_counts,get_broker_listing_counts,get_sector_counts
from datetime import datetime
import csv

EXPORTS_DIR = Path("exports")


def ensure_exports_dir() -> None:
    EXPORTS_DIR.mkdir(exist_ok=True)


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
    country = prompt("Country (US/UK/RU/etc): ").upper()
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
    q = prompt("Query: ").strip()

    if not q:
        print("\n[ERROR] Query cannot be empty\n")
        wait_for_enter()
        return
    
    rows = search_query(q)
    print_listings(rows)
    wait_for_enter()


def edit_listing_flow() -> None:
    print("\n[Edit listing]\n")

    listing_id_raw = prompt("Listing ID to edit: ").strip()
    if not listing_id_raw.isdigit():
        print("\n[ERROR] Listing ID must be a number.\n")
        wait_for_enter()
        return

    listing_id = int(listing_id_raw)
    row = get_listing_by_id(listing_id)

    if not row:
        print(f"\n[ERROR] Listing with ID {listing_id} not found.\n")
        wait_for_enter()
        return

    (
        _id,
        broker_id,
        current_access_type,
        current_country,
        current_privilege,
        current_price,
        current_description,
        current_source,
        current_post_date,
        current_sector,
        current_revenue,
        created_at,
    ) = row

    
    broker_row = get_broker_by_id(broker_id)
    if broker_row:
        broker_name = broker_row[1]
        print(f"\nEditing listing [{listing_id}] for broker: {broker_name}")
    else:
        print(f"\nEditing listing [{listing_id}] (broker_id={broker_id})")

    print(f"Created at: {created_at}\n")

    print("Press ENTER to keep existing value.\n")

    new_access_type = prompt(f"Access type [{current_access_type}]: ").strip().lower()
    if not new_access_type:
        new_access_type = current_access_type

    new_country = prompt(f"Country [{current_country}]: ").strip().upper()
    if not new_country:
        new_country = current_country

    new_privilege = prompt(f"Privilege [{current_privilege or 'none'}]: ").strip().lower()
    if not new_privilege:
        new_privilege = current_privilege

    new_price = prompt(f"Price [{current_price}]: ").strip()
    if not new_price:
        new_price = current_price

    new_description = prompt(f"Description [{current_description[:40]}...]: ").strip()
    if not new_description:
        new_description = current_description

    new_source = prompt(f"Source [{current_source}]: ").strip().lower()
    if not new_source:
        new_source = current_source

    # Date with validation
    while True:
        new_post_date = prompt(f"Post date [{current_post_date}] (YYYY-MM-DD): ").strip()
        if not new_post_date:
            new_post_date = current_post_date
            break

        if validate_date(new_post_date):
            break
        else:
            print("\n[ERROR] Invalid date format. Use YYYY-MM-DD.\n")

    new_sector_raw = prompt(f"Sector [{current_sector or 'none'}]: ").strip()
    if new_sector_raw:
        new_sector = normalize_sector(new_sector_raw)
    else:
        new_sector = current_sector

    new_revenue_raw = prompt(f"Revenue [{current_revenue or 'none'}]: ").strip()
    if new_revenue_raw:
        new_revenue = normalize_revenue(new_revenue_raw)
    else:
        new_revenue = current_revenue

    # Basic validation again
    if not new_access_type:
        print("\n[ERROR] Access type cannot be empty.\n")
        wait_for_enter()
        return

    if not new_country:
        print("\n[ERROR] Country cannot be empty.\n")
        wait_for_enter()
        return

    if not new_price:
        print("\n[ERROR] Price cannot be empty.\n")
        wait_for_enter()
        return

    if not new_description:
        print("\n[ERROR] Description cannot be empty.\n")
        wait_for_enter()
        return

    update_listing(
        listing_id=listing_id,
        access_type=new_access_type,
        country=new_country,
        privilege=new_privilege,
        price=new_price,
        description=new_description,
        source=new_source,
        post_date=new_post_date,
        sector=new_sector,
        revenue=new_revenue,
    )

    print(f"\n[OK] Updated listing [{listing_id}].\n")
    wait_for_enter()


def delete_listing_flow() -> None:
    print("\n[Delete listing]\n")

    listing_id_raw = prompt("Listing ID to delete: ").strip()
    if not listing_id_raw.isdigit():
        print("\n[ERROR] Listing ID must be a number.\n")
        wait_for_enter()
        return

    listing_id = int(listing_id_raw)
    row = get_listing_by_id(listing_id)

    if not row:
        print(f"\n[ERROR] Listing with ID {listing_id} not found.\n")
        wait_for_enter()
        return

    (
        _id,
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
        created_at,
    ) = row

    print("\nYou are about to delete this listing:\n")
    print(f"[{listing_id}] Broker ID: {broker_id}")
    print(
        f"    Access: {access_type or '-'} | Country: {country or '-'} | "
        f"Privilege: {privilege or '-'}"
    )
    print(f"    Price: {price or '-'} | Sector: {sector or '-'} | Revenue: {revenue or '-'}")
    print(f"    Source: {source or '-'} | Post date: {post_date or '-'}")
    if description:
        short_desc = description if len(description) <= 100 else description[:97] + "..."
        print(f"    Desc: {short_desc}")
    print(f"    Created: {created_at}\n")

    choice = prompt("Type 'delete' to confirm, or press ENTER to cancel: ").strip().lower()
    if choice != "delete":
        print("\n[INFO] Delete cancelled.\n")
        wait_for_enter()
        return

    delete_listing(listing_id)
    print(f"\n[OK] Listing [{listing_id}] deleted.\n")
    wait_for_enter()


def export_listings_to_csv(rows: list[tuple], filename: str | None = None) -> Path:
    ensure_exports_dir()

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"axis_listings_{timestamp}.csv"

    export_path = EXPORTS_DIR / filename

    fieldnames = [
        "id",
        "broker",
        "access_type",
        "country",
        "privilege",
        "price",
        "description",
        "source",
        "post_date",
        "sector",
        "revenue",
        "created_at",
    ]

    with export_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

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
            writer.writerow(
                {
                    "id": listing_id,
                    "broker": broker_name,
                    "access_type": access_type,
                    "country": country,
                    "privilege": privilege,
                    "price": price,
                    "description": description,
                    "source": source,
                    "post_date": post_date,
                    "sector": sector,
                    "revenue": revenue,
                    "created_at": created_at,
                }
            )

    return export_path



def export_listings_flow() -> None:
    print("\n[Export listings to CSV]\n")
    print("Choose export type:")
    print("  [1] All listings")
    print("  [2] By broker")
    print("  [3] By sector")
    print("  [4] By search query")
    print()

    choice = prompt("> ").strip()

    if choice == "1":
        rows = get_all_listings()
    elif choice == "2":
        broker_raw = prompt("Broker name: ")
        broker_name = normalize_broker_name(broker_raw)
        rows = find_listings_by_broker_name(broker_name)
    elif choice == "3":
        sector_raw = prompt("Sector: ")
        sector = normalize_sector(sector_raw)
        rows = find_listings_by_sector(sector)
    elif choice == "4":
        q = prompt("Query: ").strip()
        if not q:
            print("\n[ERROR] Query cannot be empty.\n")
            wait_for_enter()
            return
        rows = search_query(q)
    else:
        print("\n[ERROR] Invalid choice.\n")
        wait_for_enter()
        return

    if not rows:
        print("\n[INFO] No rows to export for this filter.\n")
        wait_for_enter()
        return

    filename_input = prompt("Filename (leave empty for auto): ").strip()
    filename = filename_input or None

    export_path = export_listings_to_csv(rows, filename)

    print(f"\n[OK] Exported {len(rows)} listing(s) to {export_path}\n")
    wait_for_enter()

def analytics_flow() -> None:
    print("\n[Basic analytics]\n")

    total_brokers, total_listings = get_summary_counts()
    print(f"Total brokers:  {total_brokers}")
    print(f"Total listings: {total_listings}\n")

    # Top brokers
    print("Top brokers by listings:")
    broker_rows = get_broker_listing_counts(limit=10)
    if not broker_rows:
        print("  [No brokers]\n")
    else:
        for broker_name, listing_count in broker_rows:
            tier = calculate_tier(listing_count)
            print(f"  - {broker_name}: {listing_count} listing(s) (Tier: {tier})")
        print()

    # Sector distribution
    print("Listings by sector:")
    sector_rows = get_sector_counts(limit=10)
    if not sector_rows:
        print("  [No listings]\n")
    else:
        for sector, count in sector_rows:
            print(f"  - {sector}: {count}")
        print()

    wait_for_enter()


def add_raw_listing_flow() -> None:
    print("\n[Add listing from raw post]\n")

    # --- Broker resolution ---
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

    # --- Raw fields ---
    raw_title = prompt("Raw title (as shown on forum): ")
    raw_url = prompt("Source URL (optional): ")

    print("\nPaste raw post text below.")
    print("End input with a single line containing only a single dot: '.'\n")

    raw_lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == ".":
            break
        raw_lines.append(line)

    raw_text = "\n".join(raw_lines).strip()

    if not raw_text:
        print("\n[ERROR] Raw post text cannot be empty.\n")
        wait_for_enter()
        return

    # --- Structured fields (manual for now) ---
        # --- Structured fields (parser suggestions + edit) ---
    print("\n[Parser suggestions]\n")
    suggested = suggest_listing_fields(raw_title, raw_text)
    for key, value in suggested.items():
        print(f"{key}: {value}")
    print()

    def ask(field: str, default: str = "") -> str:
        """
        Prompt with an optional default. If user presses ENTER, keep default.
        """
        if default:
            answer = prompt(f"{field} [{default}]: ")
            return answer if answer else default
        else:
            return prompt(f"{field}: ")

    access_type = ask("Access type (rdp/vpn/etc)", suggested.get("access_type", "")).lower()
    country = ask("Country (US/GB/RU/etc)", suggested.get("country", "")).upper()
    privilege = ask("Privilege (admin/user, optional)", suggested.get("privilege", "")).lower()
    price = ask("Price", suggested.get("price", ""))
    description = ask("Short description", suggested.get("description", ""))
    source = ask("Source forum (exploit/ramp/etc)").lower()

    # Post date with validation, using parser suggestion as default
    while True:
        post_date_input = ask("Post date (YYYY-MM-DD)", suggested.get("post_date", ""))
        post_date_input = post_date_input.strip()
        if not post_date_input:
            print("\n[ERROR] Post date cannot be empty.\n")
            continue

        if validate_date(post_date_input):
            post_date = post_date_input
            break
        else:
            print("\n[ERROR] Invalid date format. Use YYYY-MM-DD (e.g. 2025-09-10).\n")

    sector = normalize_sector(ask("Sector (optional)", suggested.get("sector", "")))
    revenue = normalize_revenue(ask("Revenue (optional)", suggested.get("revenue", "")))


    # --- Basic validation (same rules as normal add_listing_flow) ---
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

    # --- Deduplication check (uses structured fields) ---
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

    # --- Insert with raw fields ---
    listing_id = insert_listing(
        broker_id=broker_id,
        access_type=access_type,
        country=country,
        privilege=privilege,
        price=price,
        description=description,
        source=source,
        post_date=post_date,
        sector=sector,
        revenue=revenue,
        raw_title=raw_title,
        raw_text=raw_text,
        raw_url=raw_url,
    )

    print(f"\n[OK] Added listing with ID {listing_id} (raw + structured saved).\n")
    wait_for_enter()






def print_menu() -> None:
    print("AXIS v0.3 - IAB Listings")
    print("------------------------")
    print("[1] Add broker")
    print("[2] View brokers")
    print("[3] Add listing")
    print("[4] View listings ")
    print("[5] Find listings by broker")
    print("[6] Find listings by sector")
    print("[7] Search (query)")
    print("[8] Edit listing")
    print("[9] Delete listing")
    print("[10] Export listings to CSV")
    print("[11] Basic analytics")
    print("[12] Add listing from raw post")
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
        elif choice == "8":
            edit_listing_flow()
        elif choice == "9":
            delete_listing_flow()
        elif choice == "10":
            export_listings_flow()
        elif choice == "11":
            analytics_flow()
        elif choice == "12":
            add_raw_listing_flow()
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
