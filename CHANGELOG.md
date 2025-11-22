# Changelog

All notable changes to this project will be documented in this file.  
This project follows semantic-style versioning for development releases (0.x).

---

## [0.4] - 2025-11-22
### Added
- **Raw Post Ingestion Pipeline**
  - New menu option: *Add listing from raw post*.
  - Collects raw title, multiline raw post text, and optional source URL.
  - Stores raw data in new DB fields: `raw_title`, `raw_text`, `raw_url`.

- **Parser Suggestion Engine**
  - Extracts structured metadata from raw posts:
    - access type  
    - country  
    - privilege  
    - prices (START/STEP/BLITZ and numeric formats)  
    - sector (using expanded sector map)  
    - revenue (supports kk, million/billion, shorthand)  
    - description (fallback from raw title)
    - post date (when present)
  - Analysts can revise suggested fields before saving.

- **Expanded Price Parsing Logic**
  - Supports multi-number prices while filtering noise (`code=1014`, `host=1000+`).
  - Recognizes `$1400`, `1400$`, `price is 1400`, etc.

- **Listing Detail Viewer**
  - New command to view full structured + raw data for any listing.
  - Clearly separates `[STRUCTURED]` and `[RAW]` sections.

- **Massively Expanded Sector Mapping**
  - Coverage for 60+ industries across government, healthcare, logistics, industrial, finance, energy, retail, etc.

### Changed
- **Database schema extended** to include raw fields (`raw_title`, `raw_text`, `raw_url`).
- `insert_listing` updated for backward compatibility with new schema.
- `get_all_listings` and `get_listing_by_id` updated to return raw fields.
- Improved normalization engine (sector, revenue, GEO, privilege, access type).
- Updated CSV export to remain structured-only (raw fields intentionally excluded).
- Updated CLI flows to support parser-backed intake.

### Removed
- Old single-source description model (now replaced by dual raw + structured system).
- Legacy assumptions around exact price formatting.

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
- **Free-form multi-field search** across all listing fields.
- **CSV export** system with multiple filters.
- **Basic analytics module**:
  - total brokers  
  - total listings  
  - top brokers  
  - sector distribution  
  - tier classification
- Expanded **normalization engine** for brokers, sectors, and revenue.
- Large **sector mapping expansion** (30+ sectors).

### Changed
- Refactored CLI flows.
- Improved validation and error handling.
- Unified database schema with normalized timestamps.

### Removed
- Tier system being directly attached to exporter/CSV views.

---

## [0.2] - 2025-11-14
### Added
- **SQLite backend** replacing CSV storage.
- Auto table creation.
- Initial structured listings workflow.
- CLI features for adding & viewing listings.
- First version of normalization for sector and revenue.
- Tier scoring model.
- Early export directory structure.

### Changed
- Input handling improvements.

### Removed
- CSV-only mode.

---

## [0.1] - 2025-11-13
### Added
- Initial prototype.
- Manual broker + listing entry.
- Normalization utilities.
- Tier classification logic.
- CSV storage pipeline.
- Initial file structure.

---

