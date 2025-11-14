# AXIS – Access Exchange Intelligence Service   
### Version 0.2

AXIS is a lightweight cyber intelligence tool for tracking **Initial Access Brokers (IABs)** and their access listings.  
It provides an operator-friendly workflow for manually collecting, normalizing, and organizing intelligence from cybercrime forums.

> **AXIS v0.2 focuses on database migration, data hygiene, and a clean CLI workflow.**

---

# What’s New in v0.2

## SQLite Database Backend

AXIS now uses a dedicated `axis.db` SQLite datastore instead of CSV.

- automatic table creation  
- structured inserts  
- normalized schema  
- timestamps on every entry  
- `axis.db` is gitignored to protect real intelligence data  

This upgrade lays the foundation for analytics, automation, and ingestion in later versions.

---

## Interactive CLI Interface

AXIS v0.2 introduces a simple, operator-friendly menu:

[1] Add listing
[2] View all listings
[3] Find listings by broker
[4] Find listings by tier
[5] Find listings by sector
[0] Exit


The tool is optimized for manual HUMINT-style collection of broker information.

---

## Normalization v2

To ensure cleaner, more reliable intelligence, AXIS v0.2 includes strong normalization for all key fields.

---

### **Broker Name Normalization**

- lowercase + trimmed  
- junk characters removed (emojis, symbols, punctuation)  
- preserves `.`, `_`, `-`  
- collapses extra spaces  

**Examples:**  
- `"SSR-market🔥"` → `ssr-market`  
- `"xx_dead@crew_xx"` → `xx_deadcrew_xx`

---

### **Sector Mapping (Canonical Sectors)**

Common sector labels are normalized and mapped:

| Input Variants | Canonical |
|----------------|-----------|
| gov, govt, public sector | government |
| edu, school, university | education |
| health, medical, hospital | healthcare |
| fin, bank, banking | finance |
| tech, it | technology |

Unknown sectors remain normalized but unmapped.

---

### **Revenue Normalization**

Strong parsing of messy revenue formats:

- removes `$`, `USD`, `US$`  
- `MILLION → M`  
- `THOUSAND → K`  
- `BILLION → B`  
- normalizes separators:
  - `10 - 25m` → `10-25M`
  - `$10 TO 25m` → `10-25M`
  - `300 thousand` → `300K`

---

## Tier Classification

AXIS categorizes brokers based on total listing count:

| Listings | Tier |
|----------|------|
| ≥ 50 | High |
| 10–49 | Medium |
| 0–9 | Low |

This allows for structured filtering and basic capability assessment.

---

# Validation & Error Handling

AXIS v0.2 includes improved input safety:

- broker, sector, and revenue fields must not be empty  
- listing count must be a non-negative integer  
- invalid tier searches return clean errors  
- database issues handled gracefully  
- Ctrl+C clean exit support  


# 🪜 Installation & Usage

### Clone the Repository

```bash
git clone https://github.com/N9Intel/AXIS.git
cd AXIS

Run AXIS

python3 main.py

AXIS will automatically set up the database on first launch.
Roadmap – v0.3 and Beyond

Planned improvements:

    Query Search (freeform search across all fields)

    Edit / Update Existing Listings

    Duplicate Detection

    Raw vs Normalized Field Tracking

    Basic Analytics (tier / sector breakdown)

    Initial structure for real listing ingestion

    Export results to CSV

    Delete listings

    

AXIS v0.2 is the foundation for deeper intelligence automation coming in v0.3+.


MIT License — see the LICENSE file for full terms.

Progress updates & discussions posted on Twitter/X:
(@N9intel)



