---
doc_id: CTW-REQ-001
title: CityTwin requirements
project: CityTwin
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from CTW-CAL-001; R12 and R17 redefined and R20 added per CTW-DDR-001; R1 restated for the pull paths (D11); reference rates from the sibling TRL 3 notes
---

# CityTwin requirements

Targets remain proposals for review. The adopted items in CTW-DDR-001 (adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review) change three rows: R12 now covers the pilot on a sheltered site (D3), the outdoor range moves to a new R20, and R17 becomes a reported figure because the gateway is costed in TwinKit (D1). The status column comes from the TRL 3 calculation note CTW-CAL-001. Four requirements are **not met**: R10 (button response), R16 (kiosk cost against `budget_usd`), R18 (backup in the worst case) and R20 (street climate). R1 and R12 are **at risk**.

Table 1. Requirements.

| ID | Requirement | Target | Status (CTW-CAL-001) | Verification (TRL 4 or later) |
| --- | --- | --- | --- | --- |
| R1 | Ingest every node type in the smart city set | All 9: seven over LoRaWAN through TwinKit; PotholeLog segment files and DockHub hourly aggregates pulled by outbound HTTPS from the operators' servers (D11) | **At risk:** six LoRaWAN types met on paper; the pull paths are proposed but not agreed with PotholeLog and DockHub; CrossSafe has no LoRaWAN uplink defined | Interface agreement with each sibling repo |
| R2 | Capacity on one TwinKit gateway | 50 nodes or more and 10,000 records per day or more | Met on paper: 46 nodes send 5,616 uplinks a day with 0.61 % lost (collisions and downlink blanking); 10,000 a day lose 0.71 % | Packet capture on a live gateway |
| R3 | Accept only counts and levels | Each node type has a payload schema; any field outside it is rejected and logged; no images or audio stored | Met by design | Schema review; fuzz test of the decoder |
| R4 | Suppress small counts in public outputs | People and vehicle counts below 5 per hour (D6) published as "fewer than 5" | Met by design | Review of export code |
| R5 | No movement traces in public outputs | PotholeLog published per road segment only, no vehicle tracks or times finer than one day; DockHub per dock per hour, no card IDs | Met by design | Review of export code |
| R6 | Open data export | Hourly CSV and GeoJSON with a documented schema, under CC BY 4.0 (D7), pushed to a public host | Met by design: 7,128 rows, 0.86 MB of CSV a day | Sample export checked against the schema |
| R7 | One map for all node types | One layer per node type, node health, and an "as of" timestamp on every view | Met by design | Review of dashboard mock-up |
| R8 | Data freshness | Map and kiosk show data no older than 30 min in normal operation | Met on paper, thin margin: 25.9 min worst on the kiosk, 15.6 min on the web map | Timing log on a live system |
| R9 | Kiosk readable day and night | Readable in direct sun and at night at 1.5 m; key text cap height 7 mm or more | Met on paper: 41 px and 16.0 arcmin per capital; about 1,459 lx from the hood light | Mock-up viewed in sun and at night |
| R10 | Kiosk responds to a button | Selected layer shown within 5 s of a press | **Not met:** 19.8 s; the button LED ring acknowledges the press at once | Timed on a bench build |
| R11 | Accessible kiosk | Operable parts 380 to 1,220 mm above ground ([ADA forward reach](https://www.access-board.gov/ada/guides/chapter-3-operable-parts/)); overhang from the post no more than 305 mm between 685 and 2,030 mm ([protruding objects](https://www.access-board.gov/ada/guides/chapter-3-protruding-objects/)); same content on a web page that meets WCAG 2.1 AA, linked by QR code and short URL | Met on paper: buttons at 1,120 mm; overhang 200 mm; web page not verifiable at TRL 3 | Accessibility audit of the web page and a site review |
| R12 | Pilot kiosk survives its climate (redefined, D3) | Sheltered or indoor site with no direct sun on the window; operate at 0 to 40 °C air; head IP54, cabinet IP55; panel within its 0 to 40 °C rating and the TwinKit pack within its 0 to 45 °C charge window | **At risk:** at 40 °C air the panel is at 40.1 °C and the pack at 44.4 °C (0.6 K margin) | Temperature log in a climate chamber |
| R13 | Kiosk stands up to wind | 35 m/s gust with a factor of 1.5 without yield of post or anchors | Met on paper: post 26.2 MPa, 1.92 kN per anchor | Structural design to the local code |
| R14 | Electrical safety | Mains only inside the locked cabinet, behind a 30 mA RCBO and a surge protector; only 12 V SELV in the head; all metal earthed | Met by design; 12 V peak 26.7 W on a 60 W supply | Inspection by a qualified electrician |
| R15 | Low running power | 15 W average or less including the TwinKit gateway | Met on paper: 10.2 W (90 kWh a year) | Energy meter on a bench build |
| R16 | Kiosk parts cost | Kiosk (items 1 to 12, 14, 15) within `budget_usd` of $600; $750 recommended under D1, awaiting Amish | **Not met** against $600: $739.00 ($11.00 under the recommended $750) | Priced BOM |
| R17 | Cost with gateway (redefined, D1) | Kiosk plus TwinKit gateway reported; the gateway is costed and budgeted in the TwinKit repo | Met on paper (reported): $1,029.00 | Priced BOM |
| R18 | Honest in an outage | Screen keeps the last image with its timestamp when power fails; gateway rides through 2 h on its backup pack | **Not met in the worst case:** 2.40 h with a new pack, 1.63 h aged at 0 °C (TWK-CAL-001); the e-paper keeps its image by design | Outage test |
| R19 | Secure by default | No inbound connections from the internet to the gateway; open data pushed and sibling data pulled by outbound connections only; no exposed ports or USB on the kiosk | Met by design | Security review |
| R20 | Street kiosk climate (new, target after the pilot, D3) | Operate from -20 °C to +45 °C air in full sun | **Not met:** panel about 79 °C in low sun at 45 °C air; a heated, insulated panel bay needs 13.5 W at -20 °C; cabinet pack out of its charge window in sun and in frost | Chamber and field tests |

## Assumptions

- Node types and reporting rates follow the sibling TRL 3 calculation notes: CurbCount, HeatMap Node, FloodGauge and NoiseMap 96 uplinks a day; AirStreet 288; LoadZone 124 (100 state changes and 24 heartbeats). CrossSafe's hourly activation summary is a CityTwin assumption; CrossSafe has not defined a LoRaWAN uplink.
- Radio loss is calculated (CTW-CAL-001 section A) rather than assumed; the TRL 2 figure of about 3 % was a placeholder.
- The pilot kiosk (R12) stands on a sheltered site; the street range (R20) is the target after the pilot.
- 35 m/s design gust is an estimate for a first check; the local wind code governs any real installation.
