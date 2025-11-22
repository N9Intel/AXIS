# AXIS v0.4 — IAB Intelligence Processing & Raw Post Parser

AXIS is a cyber intelligence framework for collecting, structuring, and analyzing **Initial Access Broker (IAB)** listings from underground forums.  
Version **0.4** introduces the first major upgrade to AXIS’s ingestion pipeline, adding full **raw post parsing**, **parser-backed field suggestion**, and **raw data preservation** for improved analyst workflows.

AXIS continues to evolve into a powerful, analyst-focused platform for monitoring access brokers and compromised organization listings.

---

## Overview

AXIS v0.4 enhances the intelligence workflow by:

- Ingesting complete raw posts from forums.
- Extracting structured metadata via a parser suggestion engine.
- Preserving raw titles, raw text, and source URLs.
- Allowing analysts to review and correct parser suggestions before saving.
- Extending the schema to support raw + structured intelligence side-by-side.

This version solidifies AXIS as a proper **threat intelligence data processor**, not just a listing tracker.

---

## Key Features (v0.4)

### 1. Raw Post Ingestion (New)
Paste full underground forum listings exactly as posted:

- Multiline raw text input  
- Raw title  
- Optional source URL  
- Terminates input with `.`  
- Stored alongside structured fields for auditing and reprocessing  

**Command:** `Add listing from raw post` (Menu option **[12]**)

---

### 2. Parser Suggestion Engine (New)
Automatically extracts common IAB metadata from raw text:

- **Access type** (rdp, vpn, fortinet, citrix, rdweb, etc.)  
- **Country** (from GEO lines or text)  
- **Privilege** (DA/admin/user)  
- **Price** (START / STEP / BLITZ or raw numbers)  
- **Sector** (mapped using expanded SECTOR_MAP)  
- **Revenue** (supports kk, million/billion, shorthand)  
- **Description** (from title when possible)  
- **Post date** (if included in raw text)

Analysts can override any suggested field before saving.

---

### 3. Expanded Data Model (Updated Schema)

Each listing now contains:

#### Structured fields:
- broker_id  
- access type  
- country  
- privilege  
- price  
- description  
- source  
- validated post date  
- normalized sector  
- normalized revenue  

#### New raw fields (v0.4):
- `raw_title`  
- `raw_text`  
- `raw_url`

This preserves original source data for future reprocessing or QA.

---

### 4. Full Listing Detail View (Updated)

A dedicated detail viewer shows both structured and raw intelligence:

#### Structured
- Access  
- Country  
- Privilege  
- Price  
- Sector  
- Revenue  
- Source  
- Post date  
- Description  

#### Raw
- Full raw title  
- Full raw text  
- Optional source URL  

Menu option: **[13] View listing details**

---

### 5. Improved Normalization System
Includes:

- Significantly expanded **sector mapping** (60+ sectors)  
- Better revenue parsing  
- Better GEO → country normalization  
- Improved access/privilege detection  

---

### 6. Enhanced Price Parsing
Handles:

- START/STEP/BLITZ formats  
- `$1400`, `price is 1400`, `1400$`  
- Multi-price detection  
- Ignores noise like `code=1014` or `host=1000+`

---

### 7. Updated Core Functions
All major components now work with raw + structured data:

- Edit listings  
- Delete listings  
- Search (structured fields only)  
- CSV export  
- Analytics  

---

## Installation

### Requirements
- Python 3.10+

### Setup
```bash
git clone https://github.com/<youruser>/AXIS.git
cd AXIS
python3 main.py

[1] Add broker
[2] View brokers
[3] Add listing
[4] View listings
[5] Find listings by broker
[6] Find listings by sector
[7] Search (query)
[8] Edit listing
[9] Delete listing
[10] Export listings to CSV
[11] Basic analytics
[12] Add listing from raw post
[13] View listing details
[0] Exit
