# Changelog

All notable changes to this project will be documented in this file.  
This project follows semantic-style versioning for development releases (0.x).

---

## [0.3] - 2025-11-19
### Added
- Full **broker management system** with normalized names, raw names, and analyst notes.
- Complete **relational listings model** with `broker_id` foreign key.
- Support for listing metadata including:
  - access type  
  - country  
  - privilege  
  - price  
  - description  
  - source  
  - post date (validated `YYYY-MM-DD`)  
  - sector (normalized)  
  - revenue (normalized)
- **Deduplication engine** to prevent accidental duplicate listings.
- **Edit listing** feature with full-field update support.
- **Delete listing** feature with ID validation.
- **Free-form multi-field search**, allowing keyword searches across all listing fields.
- **CSV export system** with support for:
  - all listings  
  - by broker  
  - by sector  
  - by free-form query
- **Basic analytics module**, providing:
  - total brokers  
  - total listings  
  - top brokers by activity  
  - sector distribution  
  - broker tier classification
- Expanded **normalization engine** for brokers, sectors, and revenue ranges.
- Much larger **sector mapping**, covering dozens of real-world industries.

### Changed
- Refactored CLI flows to support brokers + listings.
- Improved input validation and error handling.
- Standardized database schema with timestamps and foreign keys.

### Removed
- Tier calculation tied to broker listing count (moved to analytics context).

---

## [0.2] - 2025-11-14
### Added
- **SQLite backend** replacing the original CSV prototype.
- Auto table creation and persistent storage.
- Initial **IAB listings input workflow**.
- CLI menu for:
  - Adding listings  
  - Viewing listings  
  - Searching by broker  
  - Searching by tier  
  - Searching by sector  
- Normalization v1 for brokers, sectors, and revenue.
- Broker tier scoring (High, Medium, Low).
- Export directory structure preparation.

### Changed
- Improved input sanitation and whitespace handling.
- `listings.csv` removed in favor of database storage.

### Removed
- Manual CSV writing from main application.

---

## [0.1] - 2025-11-13
### Added
- First functional prototype of AXIS.
- Manual structured data entry:
  - broker name  
  - listing count  
  - target sector  
  - revenue range
- Normalization utilities (`normalize_broker_name`, `normalize_sector`, `normalize_revenue`).
- Tier calculation system based on broker listing count.
- CSV storage pipeline.
- Initial project structure and directory layout.

---

## Unreleased
(Reserved for upcoming development changes toward v0.4)
