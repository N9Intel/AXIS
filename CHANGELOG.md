# Changelog

All notable changes to AXIS will be documented here.

---

## **v0.2.0 — 2025-11-14**
### Added
- SQLite database backend (`axis.db`)
- Automatic table creation on startup
- Full CLI workflow with menu system
- Stronger normalization:
  - Broker name cleanup
  - Canonical sector mapping
  - Revenue normalization (M/K/B)
- Robust tier scoring (High/Medium/Low)
- Input validation & error handling
- Graceful Ctrl+C exit handling

### Improved
- Cleaner project structure
- More predictable data hygiene

### Notes
- `axis.db` is now gitignored and not shipped with the repository.

---

## **v0.1.0 — 2025-11-13
### Added
- CSV-based storage
- Basic normalization (v1)
- Tier scoring
- Simple manual data entry pipeline
