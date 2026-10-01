---
doc_id: CTW-REQ-001
title: CityTwin requirements
project: CityTwin
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: "Initial scaffold"
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: "First measurable requirements for TRL 2, with status against the concept estimates"
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: "TRL 3 status from CTW-CAL-001; R12 and R17 redefined and R20 added per CTW-DDR-001; R1 restated for the pull paths (D11); reference rates from the sibling TRL 3 notes"
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: "Recommendations accepted by Amish (DDR-002)"
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: "Constructable design (CTW-DDR-003): R13 figures updated; R16 now not met ($778.00 against $750)"
---

# CityTwin requirements

The decisions in CTW-DDR-001 and CTW-DDR-002 (decided by Amish, 2026-09-25: go with recommendation) set these targets; the constructable design of CTW-DDR-003 (2026-10-01, open for Amish's review) changes no target. R12 covers the pilot on a sheltered site at 0 to 35 °C air (D3, narrowed from 0 to 40 °C by DDR-002), the outdoor range is R20, R17 is a reported figure because the gateway is costed in TwinKit (D1), R10 is restated for the e-paper street kiosk, and R16 is set against the new `budget_usd` of $750. The status column comes from the TRL 3 calculation note CTW-CAL-001 v0.3. Three requirements are **not met**: R16 (the parts added to make the kiosk buildable take it $28.00 over budget; an open decision in CTW-DEC-001), R18 (backup in the worst case, until TwinKit fits a larger pack) and R20 (street climate). R1 is **at risk**.

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
| R9 | Kiosk readable day and night | Readable in direct sun and at night at 1.5 m; key text cap height 7 mm or more | Met on paper: 41 px and 16.0 arcmin per capital; about 219 lx from the hood light dimmed to 0.3 W (1,459 lx at its full 2 W) | Mock-up viewed in sun and at night |
| R10 | Kiosk responds to a button (restated, CTW-DDR-002) | Street kiosk: press acknowledged within 0.5 s by the button's LED ring, which stays lit until the new image is drawn; selected layer shown within 25 s. Indoor LCD variant: selected layer within 5 s (the TRL 2 target) | Met on paper: LED ring in about 30 ms; layer in 19.8 s. The indoor LCD variant is not modeled at TRL 3 | Timed on a bench build |
| R11 | Accessible kiosk | Operable parts 380 to 1,220 mm above ground ([ADA forward reach](https://www.access-board.gov/ada/guides/chapter-3-operable-parts/)); overhang from the post no more than 305 mm between 685 and 2,030 mm ([protruding objects](https://www.access-board.gov/ada/guides/chapter-3-protruding-objects/)); same content on a web page that meets WCAG 2.1 AA, linked by QR code and short URL | Met on paper: buttons at 1,120 mm; overhang 200 mm (hood), 186.5 mm (cabinet with sun shield); web page not verifiable at TRL 3 | Accessibility audit of the web page and a site review |
| R12 | Pilot kiosk survives its climate (redefined, D3; range narrowed by CTW-DDR-002) | Sheltered or indoor site with no direct sun on the window; operate at 0 to 35 °C air; head IP54, cabinet IP55; panel within its 0 to 40 °C rating and the TwinKit pack within its 0 to 45 °C charge window | Met on paper: at 35 °C air the panel is at 35.1 °C (4.9 K margin) and the pack at 39.4 °C (5.6 K margin) | Temperature log in a climate chamber |
| R13 | Kiosk stands up to wind | 35 m/s gust with a factor of 1.5 without yield of post or anchors | Met on paper: post 26.6 MPa, 1.94 kN per anchor, with the sun shield | Structural design to the local code |
| R14 | Electrical safety | Mains only inside the locked cabinet, behind a 30 mA RCBO and a surge protector; only 12 V SELV in the head; all metal earthed | Met by design; 12 V peak 26.7 W on a 60 W supply | Inspection by a qualified electrician |
| R15 | Low running power | 15 W average or less including the TwinKit gateway | Met on paper: 9.2 W (81 kWh a year), with the hood light dimmed to 0.3 W | Energy meter on a bench build |
| R16 | Kiosk parts cost | Pilot kiosk (items 1 to 12, 14, 15, 20, 21) within `budget_usd` of $750 (raised from $600, CTW-DDR-002); the outdoor sun shield (item 19) is reported separately | **Not met:** $778.00 ($28.00 over) after the parts added for construction (CTW-DDR-003); $808.00 with the outdoor sun shield. Raising `budget_usd` to $800 is proposed, awaiting Amish (CTW-DEC-001) | Priced BOM |
| R17 | Cost with gateway (redefined, D1) | Kiosk plus TwinKit gateway reported; the gateway is costed and budgeted in the TwinKit repo | Met on paper (reported): $1,068.00 | Priced BOM |
| R18 | Honest in an outage | Screen keeps the last image with its timestamp when power fails; gateway rides through 2 h on its backup pack | **Not met in the worst case:** 2.40 h with a new pack, 1.63 h aged at 0 °C (TWK-CAL-001); a pack of at least 1.84 Ah (now 1.5 Ah) would meet 2 h and has been requested from TwinKit (CTW-DDR-002); the e-paper keeps its image by design | Outage test |
| R19 | Secure by default | No inbound connections from the internet to the gateway; open data pushed and sibling data pulled by outbound connections only; no exposed ports or USB on the kiosk | Met by design | Security review |
| R20 | Street kiosk climate (new, target after the pilot, D3) | Operate from -20 °C to +45 °C air in full sun | **Not met:** panel about 79 °C in low sun and 45.1 °C shaded at 45 °C air; a heated, insulated panel bay needs 13.5 W at -20 °C (fitted only where the partner city has frost); behind the sun shield the pack stays under 45 °C in full sun up to 37.8 °C air, and is at 52.2 °C at 45 °C air | Chamber and field tests |

## Assumptions

- Node types and reporting rates follow the sibling TRL 3 calculation notes: CurbCount, HeatMap Node, FloodGauge and NoiseMap 96 uplinks a day; AirStreet 288; LoadZone 124 (100 state changes and 24 heartbeats). CrossSafe's hourly activation summary is a CityTwin assumption; CrossSafe has not defined a LoRaWAN uplink.
- Radio loss is calculated (CTW-CAL-001 section A) rather than assumed; the TRL 2 figure of about 3 % was a placeholder.
- The pilot kiosk (R12) stands on a sheltered site; the street range (R20) is the target after the pilot. Any outdoor site uses the cabinet sun shield and a shaded screen orientation as site rules (CTW-DDR-002).
- 35 m/s design gust is an estimate for a first check; the local wind code governs any real installation.
