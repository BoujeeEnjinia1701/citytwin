---
doc_id: CTW-PRC-001
title: CityTwin design precis
project: CityTwin
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, privacy rules, kiosk massing model, first-order numbers, safety, open questions)
---

# CityTwin design precis

## Summary

CityTwin is open software that runs on a TwinKit gateway and brings the lab's smart city nodes onto one map, plus a public street kiosk that shows the same data to residents. Nodes send counts and levels over LoRaWAN; CityTwin checks every record against a schema, stores it, publishes hourly open data files and draws the map. The kiosk is a steel post with a 13.3 in color e-paper screen at eye height, three push buttons, a notice plate that says what is measured and by whom, and a locked cabinet that holds the mains protection and the gateway.

First-order estimates, to be checked at TRL 3: a 46-node reference neighborhood sends about 4,900 records a day, well within one gateway; the kiosk and gateway draw about 9 W from the mains; the kiosk parts cost about $740, or about $1,025 with the TwinKit gateway, above the $600 budget. The color e-paper takes about 20 s to redraw and is rated only 0 to 40 °C, so button response and the climate range are not met.

![Hero render](../media/hero.png)

*Figure 1. CityTwin kiosk on a sidewalk, with a 1.75 m person for scale. Massing model.*

## How it works

1. **Collect.** The seven LoRaWAN node types (CurbCount, CrossSafe, LoadZone, HeatMap Node, FloodGauge, AirStreet, NoiseMap) send small uplinks to the TwinKit gateway's concentrator. PotholeLog uploads daily road summaries over depot Wi-Fi, and DockHub reports over LTE-M; both need an upload path agreed with those projects (open question).
2. **Check.** A decoder for each node type turns the payload into named fields. Any field outside that type's schema is rejected and logged, so a changed or faulty node cannot push anything but counts and levels into the store.
3. **Store.** Records go into the TwinKit time-series database with node ID, location and time. Raw records are kept for a limited period (proposed two years, awaiting Amish); hourly aggregates are kept indefinitely.
4. **Apply the privacy rules.** Before anything is published, people and vehicle counts below a threshold (proposed 5 per hour) become "fewer than 5", PotholeLog data is published only per road segment and per day, and DockHub data only per dock per hour. No card IDs, vehicle tracks or node-level raw streams leave the gateway.
5. **Publish.** Every hour the gateway writes CSV and GeoJSON files with a documented schema and pushes them one way to a public host under an open license. An OGC SensorThings API endpoint on the public host is proposed for TRL 3.
6. **Show.** The web map has one layer per node type, a time slider, node health and an "as of" timestamp. The kiosk controller pulls a pre-rendered 1600 x 1200 image of the selected layer from the gateway every 10 min, or when a button is pressed, and writes it to the e-paper. Each image carries its timestamp, so a stale screen during an outage says so.

![Data flow](../media/flow.png)

*Figure 2. Data flow for the reference neighborhood, in records per day. All values are estimates: about 3 % radio loss, and about 4,750 stored records rolled up to about 1,100 hourly records for the open export.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 3.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Base plate and anchors | 400 x 400 x 12 mm galvanized plate, four M16 anchors | Into a footing or existing slab |
| 2 | Post | 100 x 100 x 4 mm square hollow section, 1.75 m | Carries head, hood, cabinet and antenna |
| 3 | Display head enclosure | Folded 2 mm aluminum, about 460 x 100 x 680 mm | IP54 target, vents underneath |
| 4 | Front window | 6 mm UV-stabilized polycarbonate, anti-glare | Replaceable if scratched |
| 5 | E-paper display | 13.3 in E Ink Spectra 6, 1600 x 1200 px, about 150 px per inch | [Waveshare 13.3inch e-Paper HAT+ (E)](https://www.waveshare.com/13.3inch-e-paper-hat-plus-e.htm): about 19 s full refresh, no partial refresh, 0 to 40 °C ([manual](https://www.waveshare.com/wiki/13.3inch_e-Paper_HAT+_(E)_Manual)) |
| 6 | Kiosk controller | Raspberry Pi Zero 2 W class, wired Ethernet to the gateway | Only pulls and draws images |
| 7 | Push buttons | Three 19 mm stainless buttons with LED rings, at about 1.12 m | Layer, time range, "about this sensor" |
| 8 | Data notice plate | 400 x 100 mm, icons in the style of the open [DTPR](https://dtpr.io/) standard, QR code and short URL | Says what is measured, who is responsible and for how long data is kept |
| 9 | Sun and rain hood with light | Folded aluminum, 2 W LED strip with dusk sensor | Shades the screen by day, lights it at night |
| 10 | Services cabinet | Lockable steel, IP55, DIN rail, door on the back | Only place with mains voltage |
| 11 | Mains protection | 6 A 30 mA RCBO and Type 2 surge protector | Installed or checked by an electrician |
| 12 | 12 V DIN power supply | 60 W, certified, SELV output | Feeds gateway and head |
| 13 | TwinKit gateway | TwinKit DIN gateway with LoRaWAN concentrator and LiFePO4 backup | Separate BOM (TwinKit); runs CityTwin software |
| 14 | LoRaWAN antenna | TwinKit antenna on a post-top bracket, top at about 2.4 m | Low for a gateway; see open questions |
| 15 | Conduit and cabling | Mains conduit into the cabinet; 12 V and Ethernet up the post | |
| 16 to 18 | Software and templates | Map dashboard, open data export, governance templates | MIT and CC licensed; no parts cost |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with BOM numbers.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section on the kiosk centerline, looking from the right: window (4), e-paper (5) and controller (6) in the head; gateway with backup pack (13), power supply (12) and mains protection (11) in the cabinet.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions are stated in each row and in CTW-REQ-001.

Table 2. Data load for the reference neighborhood (proposed).

| Node type | Nodes | Records per node per day | Records per day | Basis |
| --- | --- | --- | --- | --- |
| CurbCount | 8 | 96 | 768 | 15 min counts (CurbCount README) |
| CrossSafe | 4 | 24 | 96 | Hourly activation summary (assumption) |
| LoadZone | 12 | 64 | 768 | State changes and heartbeats (assumption) |
| HeatMap Node | 6 | 96 | 576 | 15 min means (HeatMap Node README) |
| FloodGauge | 4 | 96 | 384 | 15 min status plus alerts (assumption) |
| AirStreet | 6 | 288 | 1,728 | 5 min records (AirStreet README) |
| NoiseMap | 6 | 96 | 576 | 15 min records (NoiseMap README) |
| **Total** | **46** | | **4,896** | Within TwinKit's roughly 50 nodes (R2 met) |

Table 3. System and kiosk estimates.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Radio airtime | about 900 s per day, about 1 % of one channel, about 0.13 % over 8 channels | 4,896 uplinks of about 20 bytes at SF9, about 185 ms each | R2 met with wide margin |
| Records stored | about 4,750 per day | 3 % radio loss | |
| Storage | about 1 MB per day, about 350 MB per year | About 200 bytes per stored record with index | Fits the gateway's storage |
| Open export | about 1,100 hourly records per day, about 0.2 MB per day as CSV | 46 nodes x 24 h | R6 |
| Worst data age on screen | about 25 min | 15 min node interval plus 10 min kiosk redraw | R8 met, thin margin |
| Button to new layer | about 20 s | About 1 s to fetch the image plus about 19 s full refresh | R10 **not met** (5 s) |
| Screen resolution | about 150 px per inch; 7 mm cap height is about 41 px | 1,600 px over 270.4 mm | R9 by design |
| Kiosk power (head only) | about 1.8 W from the mains | Controller about 1.0 W, hood light 2 W for about 6 h a day (0.5 W average), button LEDs 0.1 W, e-paper refresh under 0.5 W for 19 s every 10 min (about 0.02 W), 88 % supply | |
| Kiosk and gateway | about 9 W, about 0.21 kWh per day, about 75 kWh per year | Adds TwinKit's about 6 W | R15 met |
| Wind on head and hood | about 350 N at about 1.4 m | 0.35 m² at 35 m/s gust, air 1.25 kg/m³, drag coefficient 1.3 | |
| Post base moment and stress | about 0.58 kN·m; about 12 MPa | Adds about 160 N on the cabinet; section modulus of 100 x 100 x 4 SHS about 47,000 mm³ | R13 met by a wide margin |
| Anchor tension | about 1 kN per anchor | Moment over 0.3 m lever, two anchors in tension | Well within M16 anchors |
| Mass | about 55 kg | Post 21, base plate 15, cabinet 7, head 4.6, contents 4, hood 1.5, display and window 2 kg | Two-person lift |
| Kiosk parts cost | about $740 | Indicative, `bom/bom.csv` | R16 **not met** ($600) |
| Kiosk and gateway | about $1,025 | Adds TwinKit's about $285 | R17 **not met** ($600) |

## Key design choices

All are proposed, awaiting Amish.

- **Color e-paper rather than an LCD.** E-paper is readable in direct sun, draws almost nothing between refreshes and keeps its image in an outage. A 1,000-nit outdoor LCD would respond instantly and allow touch, but costs more, draws tens of watts and needs cooling. A monochrome e-paper panel would refresh faster but lose the color layers. Recommendation: color e-paper for the first kiosk, with an indoor LCD variant for libraries and city hall lobbies.
- **Buttons, not a touch screen.** Three stainless buttons survive vandalism and weather and suit e-paper's slow refresh; the QR code hands richer use over to the visitor's phone. Recommendation: buttons.
- **Gateway inside the kiosk cabinet.** One site, one mains feed and one locked box for a pilot. The cost is a low antenna (about 2.4 m), which shortens LoRaWAN range. The alternative is a rooftop gateway with the kiosk on a network link. Recommendation: gateway in the cabinet for the pilot, rooftop gateway for a full neighborhood.
- **Mains power.** Kiosk and gateway need about 0.21 kWh a day. A solar kiosk would need roughly a 75 W panel and a battery of about 0.6 kWh for three dark days (estimate), which does not fit the budget. The head alone (about 45 Wh a day) could run on a panel of about 30 W. Recommendation: mains, with a solar head-only variant for sites without power.
- **One-way publishing.** The gateway pushes open data files out and accepts no inbound connections from the internet, which keeps TwinKit's advice to keep the gateway off public networks until it is hardened. Recommendation: one-way push.
- **Privacy rules in the gateway, not only in the nodes.** Nodes already send counts and levels only; enforcing a schema and small-count suppression again at the gateway protects against a changed node or a future node type that is less careful. Recommendation: both layers.
- **Open data license.** Options: CC BY 4.0 (attribution, widely used for government data), CC0 (no conditions) or ODbL (share-alike). Recommendation: CC BY 4.0.
- **Budget.** See the review note for options.

## Safety

> **Safety:** The services cabinet contains mains voltage (230 V or 120 V). The mains feed, RCBO, surge protector and earthing must be installed or checked by a qualified electrician and follow local electrical code. Keep the cabinet locked, fit an earth bond to the post, head and hood, and carry only 12 V SELV up to the head.

> **Safety:** The TwinKit gateway contains a LiFePO4 backup pack. Use a pack with a built-in BMS and fuse, charge it only through the TwinKit UPS module, and keep it within its temperature limits; a sealed cabinet in full sun can exceed them.

> **Safety:** The kiosk is a roughly 55 kg steel post beside a walkway. Install it only with the asset owner's permission and a permit, on a footing designed for local wind and impact loads, with no sharp edges or protruding corners at head height, and keep a clear walkway width around it as local rules require. Lift it with two people or a hoist.

> **Safety:** Privacy by design: no images, audio recordings or personal identifiers are taken in, stored or published; only aggregate counts or levels. Check local data protection law, and carry out a privacy impact assessment before any deployment. CityTwin is not a public warning system: do not rely on it for flood or emergency alerts.

## Open questions

- [ ] Upload paths for PotholeLog (depot Wi-Fi files) and DockHub (LTE-M): agree formats with those projects rather than change them here.
- [ ] Reporting intervals and payload fields for CrossSafe, FloodGauge and LoadZone, which are assumed here.
- [ ] Climate range: a thermostatic heater and sun shading for the head, a panel rated for a wider range, or indoor siting only (R12).
- [ ] Button response: accept about 20 s with an LED acknowledgment, use a faster monochrome panel for part of the screen, or use an LCD (R10).
- [ ] Small-count threshold, raw data retention and the open data license. Proposed, awaiting Amish.
- [ ] Gateway in the kiosk cabinet or on a rooftop, and the antenna height needed for the reference neighborhood.
- [ ] Which languages and scripts the kiosk shows, and how residents ask questions or report a fault.
- [ ] First partner city or neighborhood, and co-design sessions with residents on what the kiosk should show.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
