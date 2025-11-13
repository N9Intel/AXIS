# AXIS  
**Access Exchange Intelligence**

AXIS is an open-source cyber threat intelligence engine focused on monitoring and analyzing Access Broker activity across dark-web forums, marketplaces, and communication channels.  
It transforms raw access listings into structured intelligence, providing early-warning signals of targeted intrusion activity before attackers escalate.

---

## Features (v0.1)

AXIS v0.1 includes:

### ✔ Manual Listing Input
Add raw access-broker listings (broker, sector, revenue range, access details, source).

### ✔ Normalization Engine  
Automatically cleans and standardizes inputs:
- lowercasing  
- whitespace removal  
- normalized dates  
- standardized fields  

### ✔ Deduplication  
Prevents duplicate brokers or listings from being stored.

### ✔ CSV Intelligence Database  
Listings, brokers, and metadata stored in clean CSV files:
- `data/brokers.csv`
- `data/listings.csv`

### ✔ Risk Scoring  
Simple logic-based scoring for early assessment.


