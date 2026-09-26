---
doc_id: CTW-REQ-001
title: CityTwin requirements
project: CityTwin
doc_type: Requirements
version: "0.2"
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
---

# CityTwin requirements

These are first-pass requirements for the concept. Targets are proposals for review, awaiting Amish, and will be checked by calculation at TRL 3. The status column compares each target with the first-order estimates in the design precis (CTW-PRC-001). Four requirements are **not met** by the current concept: R10 (button response), R12 (display temperature range), R16 (kiosk cost) and R17 (cost with gateway). R1 is at risk.

Table 1. Requirements.

| ID | Requirement | Target | Status (TRL 2 estimate) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Ingest every node type in the smart city set | All 9: seven over LoRaWAN through TwinKit, PotholeLog by file upload over depot Wi-Fi, DockHub over LTE-M | At risk: LoRaWAN types met by design; PotholeLog and DockHub upload paths are not yet defined in those repos | Interface review with each sibling repo |
| R2 | Capacity on one TwinKit gateway | 50 nodes or more and 10,000 records per day or more | Met: reference neighborhood of 46 nodes sends about 4,900 records per day | Airtime and database load calculation |
| R3 | Accept only counts and levels | Each node type has a payload schema; any field outside it is rejected and logged; no images or audio stored | Met by design | Schema review; fuzz test of the decoder |
| R4 | Suppress small counts in public outputs | People and vehicle counts below a threshold (proposed 5 per hour) published as "fewer than 5" | Met by design; threshold awaiting Amish | Review of export code |
| R5 | No movement traces in public outputs | PotholeLog published per road segment only, no vehicle tracks or times finer than one day; DockHub per dock per hour, no card IDs | Met by design | Review of export code |
| R6 | Open data export | Hourly CSV and GeoJSON with a documented schema, under an open license, pushed to a public host | Met by design; OGC SensorThings API proposed | Sample export checked against the schema |
| R7 | One map for all node types | One layer per node type, node health, and an "as of" timestamp on every view | Met by design | Review of dashboard mock-up |
| R8 | Data freshness | Map and kiosk show data no older than 30 min in normal operation | Met, thin margin: about 25 min worst case for 15 min nodes | Timing calculation |
| R9 | Kiosk readable day and night | Readable in direct sun and at night at 1.5 m; key text cap height 7 mm or more | Met by design (reflective e-paper, hood light); unverified | Legibility calculation, later mock-up |
| R10 | Kiosk responds to a button | Selected layer shown within 5 s of a press | **Not met:** about 20 s full refresh of the color e-paper; the button LED ring acknowledges the press at once | Datasheet timing |
| R11 | Accessible kiosk | Operable parts 380 to 1,220 mm above ground ([ADA forward reach](https://www.access-board.gov/ada/guides/chapter-3-operable-parts/)); same content on a web page that meets WCAG 2.1 AA, linked by QR code and short URL | Met by design for reach (buttons at about 1.12 m); no audio output on the kiosk | Design review; accessibility audit of the web page |
| R12 | Kiosk survives the outdoor climate | Operate from -20 °C to +45 °C air temperature; head IP54, cabinet IP55 | **Not met:** display rated 0 to 40 °C; needs a heater, a different panel or indoor siting | Thermal calculation of the head |
| R13 | Kiosk stands up to wind | 35 m/s gust with a factor of 1.5 without yield of post or anchors | Met by estimate: post bending stress about 12 MPa | Structural calculation |
| R14 | Electrical safety | Mains only inside the locked cabinet, behind a 30 mA RCBO and a surge protector; only 12 V SELV in the head; all metal earthed | Met by design | Design review by a qualified electrician |
| R15 | Low running power | 15 W average or less including the TwinKit gateway | Met: about 9 W | Power budget calculation |
| R16 | Kiosk parts cost | $600 or less for the kiosk (items 1 to 12, 14, 15) | **Not met:** about $740 | Priced BOM |
| R17 | Cost with gateway | $600 or less for kiosk and TwinKit gateway together (`budget_usd`) | **Not met:** about $1,025 | Priced BOM |
| R18 | Honest in an outage | Screen keeps the last image with its timestamp when power fails; gateway rides through 2 h on its backup pack | Met by design (e-paper is bistable; TwinKit backup) | Design review |
| R19 | Secure by default | No inbound connections from the internet to the gateway; open data pushed one way; no exposed ports or USB on the kiosk | Met by design | Security review |

## Assumptions

- Node types and reporting intervals follow the sibling READMEs: CurbCount, HeatMap Node and NoiseMap every 15 min; AirStreet every 5 min. CrossSafe (hourly activation summary), FloodGauge (15 min status plus alerts) and LoadZone (about 64 state changes and heartbeats per puck per day) are CityTwin assumptions to be confirmed with those projects.
- LoRaWAN packet loss of about 3 % for a single gateway in a dense street (estimate).
- 35 m/s design gust is an estimate for a first check; the local wind code governs any real installation.
