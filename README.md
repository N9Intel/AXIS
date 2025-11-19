# AXIS v0.3 — IAB Intelligence Collection & Analysis Framework

AXIS is a cyber intelligence framework designed for collecting, organizing, and analyzing data related to **Initial Access Broker (IAB)** activity across underground forums.  
Version **0.3** introduces a structured relational database, a refined data model for brokers and listings, advanced search capabilities, deduplication logic, and foundational analytics.

AXIS serves as a free, open-source foundation for analysts who track access brokers, compromised organizations, and access sale patterns on the dark web.

---

## Overview

AXIS provides a structured workflow for analysts to:

- Maintain a centralized catalog of **brokers** and their historical activity.
- Record and normalize **access listings** with consistent metadata.
- Query, search, and filter listings using multiple methods.
- Export structured intelligence for reporting or external analysis.
- Perform basic analytics to understand broker activity and sector distribution.

The system is built around **SQLite**, ensuring portability and reliability while keeping deployment simple.

---

## Key Features (v0.3)

### 1. Broker Management
- Add, view, and retrieve brokers.
- Normalization of broker names for consistency.
- Support for analyst notes per broker.
- Automatic timestamping.

---

### 2. Structured Listings Model
Each listing is linked to a broker and includes:

- Access type (e.g., RDP, VPN, Citrix)
- Country (ISO-like format)
- Privilege level (admin/user)
- Pricing data (start/step/blitz or fixed)
- Description of the access
- Source forum
- Post date (validated, `YYYY-MM-DD`)
- Sector (normalized)
- Revenue range (normalized)
- Automatic deduplication checks
- Automatic timestamping

---

### 3. Advanced Search (Free-Form Query Engine)
AXIS includes a multi-field search mechanism:

- Matches across all listing fields.
- Multiple-term matching (logical AND).


---

### 4. Deduplication Engine
AXIS detects potential duplicate listings using:

- Broker match  
- Access type  
- Country  
- Pricing  
- Description  
- Source  
- Post date  
- Sector  
- Revenue  

Users are warned before inserting duplicates.

---

### 5. Editing and Deleting Listings
- Update any field of an existing listing.
- Delete listings safely using the listing ID.

---

### 6. CSV Export System
Export listings to CSV with filtering options:

- All listings  
- By broker  
- By sector  
- By free-form query  

Exports are stored in `exports/`.

---

### 7. Basic Analytics
Provides statistical insight into IAB activity:

- Total brokers  
- Total listings  
- Top brokers by listing count  
- Broker tier classification (High / Medium / Low)  
- Sector distribution  

---

### 8. Enhanced Normalization Engine
Improved normalization for:

- Broker names  
- Revenue ranges  
- Sectors (including dozens of real-world industries)

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
[0] Exit

License
MIT License

Copyright (c) 2025 N9 Intelligence

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

