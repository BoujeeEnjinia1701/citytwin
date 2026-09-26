---
doc_id: CTW-CAL-001
title: CityTwin sizing calculations
project: CityTwin
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (radio load, storage and export, freshness and button response, legibility and shading, accessibility geometry, head and cabinet thermal with a heater study, power, wind and mass, backup, cost) with a status for every requirement
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# CityTwin sizing calculations

On paper, CityTwin meets 17 of its 20 requirements (10 by calculation, 7 by design), has 1 at risk and misses 2. This v0.2 applies Amish's decisions of 2026-09-25 (CTW-DDR-002): `budget_usd` of $750, R10 restated, the pilot range narrowed to 0 to 35 °C air, a ventilated sun shield on the cabinet for outdoor sites, the hood light dimmed to 0.3 W, and a larger TwinKit pack requested. **R18 is not met in the worst case**: TwinKit's backup pack rides through 2.40 h when new but only 1.63 h when aged and at 0 °C, against 2 h; a pack of at least 1.84 Ah would meet it. **R20 is not met**: in a street kiosk the panel would reach about 79 °C in low sun at 45 °C air, 45.1 °C even in shade, and needs about 13.5 W of heat at -20 °C. R1 (ingest of every node type) is at risk. R10 (LED ring in about 30 ms, layer in 19.8 s against 0.5 s and 25 s), R12 (about 5 K of margin at 35 °C air) and R16 ($739.00 against $750) are now met on paper. The radio and data side has ample margin: the 46-node reference neighborhood sends 5,616 uplinks a day and loses 0.61 % to collisions and downlink blanking. Several TRL 2 figures were corrected, and v0.2 changes are listed in the last sections. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A2], is the line of that script's output that carries it.

> **Safety:** These are first-principles screening estimates for a paper proof of concept. They do not replace the electrician's check of the mains installation, a structural design of the footing and anchors to the local code, or a privacy impact assessment. See CTW-PRC-001, Safety.

## Scope and method

The note checks every requirement in CTW-REQ-001 v0.4 against the design in CTW-PRC-001 v0.4, the decisions in CTW-DDR-001 and CTW-DDR-002 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, derived dimensions and part volumes, so the head, window, hood, cabinet, post and rail dimensions used here are the ones in the STEP files and in drawing CTW-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes the requirement table to `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is the reference neighborhood of CTW-DDR-001 D9 on one TwinKit gateway in the kiosk cabinet (D4), a pilot kiosk on a sheltered site in air of 0 to 35 °C (D3, CTW-DDR-002 N5), and a street kiosk case with the cabinet sun shield for R20.

## Assumptions

*Table 1. Main assumptions. Sibling figures are from those repos' TRL 3 calculation notes.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Node traffic | CurbCount 8 x 96 uplinks a day, 14 B; CrossSafe 4 x 24, 20 B; LoadZone 12 x 124, 12 B; HeatMap Node 6 x 96, 20 B; FloodGauge 4 x 96, 20 B (60 an hour in events); AirStreet 6 x 288, 20 B; NoiseMap 6 x 96, 22 B | CBC, LDZ, HMN, FLG, AST and NSM CAL-001; the CrossSafe rate is a CityTwin assumption |
| Radio | 13 B of LoRaWAN overhead, 125 kHz, CR 4/5, 8-symbol preamble; every node at SF9; pure ALOHA over 8 channels; no capture effect | TWK-CAL-001 method, conservative |
| Downlinks | LoadZone sign option on all 6 two-puck bays, 200 downlinks and 33 s of transmit a day each; the gateway cannot receive while it transmits | LDZ-CAL-001 [H5] |
| Peak hour | FloodGauge in event mode on all 4 gauges; LoadZone at 3 times its daily mean | Assumed storm and rush hour together |
| Pulled data | PotholeLog: 3 buses, 112 kB of summaries a bus-day, at most 6,000 published segment rows a day; DockHub: 24 dock-hour rows a day | PHL-PRC-001 v0.3; D11 |
| Storage | 90 B per stored value, uncompressed; values per record: CurbCount 7, CrossSafe 4, LoadZone 5, HeatMap 11, FloodGauge 6, AirStreet 10, NoiseMap 22, pulled rows 6; 56 GB free on the card, shared with TwinKit's own 4.73 GB a year | TWK-CAL-001; payload descriptions in the sibling notes |
| Timing | Network 4.7 s worst (TWK-CAL-001); layer render 30 s; kiosk redraw every 10 min; 1600 x 1200 frame at 4 bits per pixel over SPI at 10 MHz; PNG at 20 % of raw over 80 Mbit/s Ethernet; full refresh 19 s | Waveshare manual for the refresh; the rest assumed |
| Light | LED 100 lm/W; 40 % of the light reaches the screen; the 2 W strip runs dimmed to 0.3 W (CTW-DDR-002 N6) | Assumed |
| Thermal | Outside film 10 W/m²K, inside film 5 W/m²K; solar absorptance 0.5 (grey paint); sun 600 W/m² on a vertical face, 1,000 W/m² on a horizontal one; window transmits 0.85, panel absorbs 0.7; 1 mm air gap and 6 mm polycarbonate in front of the panel; TwinKit processor 29.1 K above the air around it at light load (69.1 °C at 40 °C) and throttles at 85 °C; pack charges only at 0 to 45 °C; the ventilated sun shield lets 20 % of the sun's heat reach the cabinet | TWK-CAL-001 F2; handbook ranges; to be measured |
| Power | Controller 1.0 W; button LEDs 0.1 W; e-paper 0.5 W while refreshing; hood light 0.3 W for 12 h a night (2 W at peak); TwinKit 6.41 W; 12 V supply 85 % efficient at light load; protection 0.2 W | TWK-CAL-001 D1; typical figures |
| Wind | 35 m/s gust, air 1.25 kg/m³, load factor 1.5; drag coefficient 1.3 for the head, hood and cabinet with its sun shield, 2.0 for the square post, 1.2 for the antenna; all areas loaded at once; S355 post, 355 MPa yield; M16 anchor design tension 10 kN | Screening values; the local wind code and the anchor maker's data govern |
| Mass | Steel 7,850, aluminum 2,700, polycarbonate 1,200 kg/m³ on the model volumes; bought-in items by estimate (display 1.2 kg, TwinKit 1.2 kg) | Model; estimates |

## A. Radio load and capacity (R1, R2)

- **Traffic.** The reference neighborhood of 46 LoRaWAN nodes sends 5,616 uplinks a day (TRL 2: 4,896), mainly because LoadZone's TRL 3 note sets 124 uplinks a day per puck, not 64 [A1, A2]. At SF9 the uplinks take 1,309 s a day, 1.52 % of one channel, or 0.189 % of each of 8 channels [A2].
- **Loss.** Collisions lose 0.38 % of uplinks. With the LoadZone sign option on all six bays, 1,200 downlinks take 198 s of gateway transmit a day, during which the gateway hears nothing: another 0.23 %, for 0.61 % in all [A3]. In a storm hour with every FloodGauge in event mode and LoadZone at three times its mean, the gateway sees 582 uplinks an hour and loses 0.94 % plus the same blanking [A4].
- **Capacity (R2).** 10,000 records a day of 20 B at SF9 lose 0.71 %; one gateway takes up to 14,075 a day before loss reaches 1 %, consistent with TwinKit's 1.02 % at 14,400 [A5]. **R2 is met on paper.**
- **Pulled sources (R1).** PotholeLog uploads its daily summaries (3 buses x 112 kB) to the fleet operator's server, not to CityTwin, and DockHub syncs its logs over LTE-M to its own back end. Under D11 the gateway fetches the published PotholeLog segment files (at most 6,000 rows a day) and DockHub's 24 dock-hour rows a day by outbound HTTPS, so it still accepts no inbound connection [A6]. CrossSafe's radio runs LoRa point to point between the two sides of a crossing and has no LoRaWAN uplink defined; the 24 summaries a day assumed here depend on CrossSafe adding one. **R1 is at risk**: met on paper for six LoRaWAN types, with the PotholeLog and DockHub paths proposed but not agreed and the CrossSafe uplink undefined.

## B. Storage and open export (R2, R6)

- **Store.** 87,936 values a day take 2.89 GB a year uncompressed. Two years of raw records (D6) are 5.78 GB and ten years of hourly aggregates 15.14 GB, 20.9 GB in all [B1]. With TwinKit's own two-year case the card holds 30.4 GB of 56 GB free [B2].
- **Export (R6).** Each day the export carries 1,104 node-hour rows, up to 6,000 road segment rows and 24 dock rows: 7,128 rows, 0.86 MB as CSV and 2.85 MB as GeoJSON, or 1.35 GB a year on the public host [B3]. PotholeLog segments dominate; the TRL 2 figure of 0.2 MB a day left them out. **R6 is met by design**; the sizes confirm that one-way pushes of this volume are trivial.

## C. Freshness and button response (R8, R10)

- **Data age (R8).** For a 15 min node, the newest value can be 15 min old when the next uplink arrives, and the kiosk may then wait up to 10 min for its next redraw. With 4.7 s of network time, 30 s to render the layer, 0.79 s to move the image and 19 s to refresh, the worst age on the kiosk is 25.9 min; if one uplink is lost (0.38 % chance) it is 40.9 min. The web map shows data at most 15.6 min old [C1]. **R8 is met on paper**, with a margin of about 4 min.
- **Button (R10).** A press starts a 960 kB frame transfer (0.79 s) and a full refresh (19 s): 19.8 s against the restated 25 s (CTW-DDR-002 N2; the TRL 2 target was 5 s). The controller lights the pressed button's LED ring after a 10 ms poll and 20 ms debounce, about 30 ms against 0.5 s, and keeps it lit until the new image is drawn [C2]. **R10 is met on paper** for the street kiosk. The indoor LCD variant keeps the 5 s target and is not modeled at TRL 3.

## D. Legibility, night light and shading (R9)

- **Text.** The panel has 150 pixels per inch, so 7 mm capitals are 41 px tall and subtend 16.0 arcmin at 1.5 m: 3.2 times the 5 arcmin of a 20/20 letter and 1.6 times the 10 arcmin of 20/40 [D1].
- **Night.** At its full 2 W the hood light gives about 1,459 lx on the 0.0548 m² screen; 200 lx needs only 0.27 W, so under CTW-DDR-002 N6 it runs dimmed to 0.3 W, which gives about 219 lx [D2].
- **Sun.** The hood reaches 140 mm beyond the head. With the sun facing the screen, its shadow covers 13 % of the window at 30°, 31 % at 45° and 63 % at 60° elevation [D3]. The hood shades the screen at midday but not in low morning or evening sun, which matters for R20 below.
- **R9 is met on paper**: reflective e-paper reads in sun by design, and the text size and night light have margin.

## E. Accessibility geometry (R11)

The buttons sit at 1,120 mm, inside the 380 to 1,220 mm reach range. The head's leading edge runs from 1,040 to 1,734 mm, inside the 685 to 2,030 mm zone (27 to 80 in) where objects on posts may overhang no more than 305 mm (12 in) ([U.S. Access Board, protruding objects](https://www.access-board.gov/ada/guides/chapter-3-protruding-objects/), checked 2026-09-25). The head overhangs the post by 180 mm sideways and the hood by 200 mm sideways and 190 mm forward. The cabinet with its sun shield projects 186.5 mm behind the post, and its bottom, at 300 mm, is below 685 mm and within cane reach [E1]. **R11 is met on paper** for the kiosk; the WCAG 2.1 AA web page is not verifiable at TRL 3. The screen center at 1.46 m is high for a seated reader; the web page and the QR code carry the same content.

## F. Thermal: head, heater study and cabinet (R12, R20)

- **Pilot head (R12).** The head holds 1.12 W of electronics and loses heat from 0.786 m², a rise of 0.14 K in shade. At 35 °C air, the top of the pilot range under CTW-DDR-002 N5, the panel sits at 35.1 °C, 4.9 K under its 40 °C rating; at 40 °C air it would be 40.1 °C, and the limit for air is 39.9 °C [F1].
- **Street head in sun (R20).** With 600 W/m² of low sun on the face, the head air rises 9.2 K, and the panel, which absorbs 19.6 W through the window, sits 33.6 K above the air outside: about 79 °C at 45 °C air [F2]. Only orientation or shading of the face can fix this, which is why a shaded screen orientation is a site rule (N4); the hood does not shade low sun. Even in shade the panel is at 45.1 °C in 45 °C air.
- **Heater study (R20).** Holding the panel at 0 °C in -20 °C air takes 156 W if the whole head is heated, but only 13.5 W if the panel sits in a bay lined with 20 mm of foam and the heater warms only that bay [F3]. Under N4 the heater is fitted only where the partner city has frost.
- **Cabinet.** The sealed cabinet holds 7.96 W (TwinKit 6.41 W, supply loss 1.35 W, protection 0.2 W). Its air rises 4.4 K in shade and 18.7 K in sun, when it absorbs 78 W. Behind the ventilated sun shield (item 19, N4) it absorbs about 16 W and rises 7.2 K, so the pack stays under its 45 °C charge limit in full sun up to 37.8 °C air [F4]. In the pilot case (35 °C shaded) the cabinet air is 39.4 °C, the TwinKit processor 68.5 °C against 85 °C, and the pack 5.6 K below its charge limit; at 40 °C in shade the margin is only 0.6 K. Outdoors at 35 °C in sun with the shield the cabinet air is 42.2 °C (2.8 K margin). At 45 °C the pack is over the limit in every case: 49.4 °C shaded, 52.2 °C in sun with the shield and 63.7 °C without it, when the processor reaches 92.8 °C, above its throttle point [F5]. At -20 °C air the cabinet is at -15.6 °C, too cold to charge the pack [F6].
- **Status.** **R12 is met on paper** with about 5 K of margin for the panel and the pack. **R20 is not met.**

## G. Power (R14, R15)

- **Average (R15).** The head draws 1.27 W of 12 V DC (controller 1.0 W, hood light 0.15 W averaged over 12 h a night at 0.3 W, button LEDs 0.1 W, e-paper 0.016 W). With TwinKit's 6.41 W and an 85 % supply, the kiosk takes 9.2 W from the mains: 0.222 kWh a day, 81 kWh a year [G1]. **R15 is met on paper.** A street kiosk with the panel heater running at -20 °C would take 25.1 W while heating [G2], above 15 W; how long it runs depends on the site's climate.
- **Supply (R14).** The 12 V peak is 26.7 W (TwinKit 20.6 W, controller boot 2.5 W, e-paper 1.5 W, hood 2 W, LEDs 0.1 W), or 40.2 W with the heater, within the 60 W supply. The mains current is 40 mA at 230 V [G3], far below the 6 A RCBO rating. **R14 is met by design** and the supply size is confirmed.

## H. Wind, structure and mass (R13)

- **Loads.** At 35 m/s the dynamic pressure is 766 Pa. The head and hood take 348 N at 1.38 m, the cabinet with its sun shield 200 N at 0.54 m, the post 268 N at 0.88 m and the antenna 11 N at 2.08 m [H1]: 827 N and a base moment of 848 N·m, or 1,271 N·m with the 1.5 load factor [H2].
- **Post and weld.** The 100 x 100 x 4 mm section (47,268 mm³) is stressed to 26.9 MPa, a factor of 13.2 on yield [H2]. A 4 mm fillet weld all round the post base sees 33.7 MPa [H3].
- **Anchors and plate.** Each anchor on the tension side carries 1.97 kN, a factor of 5.1 on the assumed 10 kN [H5]. The 12 mm base plate sees 41 MPa [H6]. The head moves 0.65 mm under the unfactored gust [H7].
- **Mass.** The kiosk weighs 60.1 kg with the sun shield (post 21.4, base 15.5, cabinet with rails 10.7, head 4.1, sun shield 1.86 kg) [H4], 58.2 kg without it. The TRL 2 figure was about 55 kg.
- **R13 is met on paper.** The TRL 2 figure of 12 MPa left out the post's own drag and the load factor. Vehicle impact is not covered; the footing and anchors are site design.

## I. Outage behavior (R18)

TwinKit's backup runs the gateway for 2.40 h with a new pack and 1.63 h with an aged pack at 0 °C, against the 2 h of R18. The head is not on the backup; the bistable e-paper keeps its last image and time stamp [I1]. Scaling TwinKit's 1.5 Ah pack by 2 h over 1.63 h, a pack of at least 1.84 Ah would meet R18 in the worst case; under CTW-DDR-002 N3 TwinKit is asked for it [I1]. **R18 is not met in the worst case** until TwinKit changes its pack. A cold cabinet in winter (section F) would shorten the runtime further.

## J. Cost (R16, R17)

All 19 BOM lines are priced. The pilot kiosk (items 1 to 12, 14 and 15) costs $739.00; the TwinKit gateway $290.00 from TwinKit's TRL 3 BOM; together $1,029.00. The outdoor sun shield (item 19) adds $30.00, for $769.00 [J1]. Against `budget_usd`, raised from $600 to $750 under CTW-DDR-002 N1, the pilot kiosk is $11.00 under and the outdoor kiosk $19.00 over [J2]. **R16 is met on paper** for the pilot kiosk. **R17**, redefined by D1 as a reported figure with the gateway costed in TwinKit, is met on paper.

## Results

*Table 2. Requirement status (also in `docs/04-calcs/results.csv`).*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Ingest every node type | 6 LoRaWAN types on paper; PotholeLog and DockHub by outbound pull (D11), not agreed; CrossSafe has no LoRaWAN uplink | All 9 types | **At risk** |
| R2 | Capacity on one gateway | 46 nodes, 5,616 a day, 0.38 % loss; 10,000 a day gives 0.71 % | 50 nodes, 10,000 a day | Met on paper |
| R3 | Counts and levels only | Schema per node type at the decoder | Out-of-schema fields rejected | Met by design |
| R4 | Small-count suppression | Threshold 5 per hour (D6) | Fewer than 5 published as such | Met by design |
| R5 | No movement traces | Segment per day; dock per hour | No tracks or card IDs | Met by design |
| R6 | Open data export | 7,128 rows a day, 0.86 MB CSV | Hourly CSV and GeoJSON, CC BY 4.0 | Met by design |
| R7 | One map | Layer per type, node health, as-of time | As stated | Met by design |
| R8 | Data freshness | 25.9 min worst on the kiosk | 30 min | Met on paper (thin margin) |
| R9 | Readable day and night | 41 px, 16.0 arcmin; 219 lx at night (light dimmed to 0.3 W) | Sun and night at 1.5 m | Met on paper |
| R10 | Button response (restated) | LED ring 30 ms; layer 19.8 s | Acknowledged within 0.5 s; layer within 25 s | Met on paper |
| R11 | Accessible kiosk | Buttons 1,120 mm; overhang 200 mm | 380 to 1,220 mm; 305 mm; WCAG page | Met on paper (web page not verifiable at TRL 3) |
| R12 | Pilot climate (redefined) | Panel 35.1 °C and pack 39.4 °C at 35 °C air | Sheltered site, 0 to 35 °C air | Met on paper |
| R13 | Wind | 26.9 MPa with the 1.5 factor; 1.97 kN per anchor | 35 m/s x 1.5, no yield | Met on paper |
| R14 | Electrical safety | Mains only in the cabinet; 12 V SELV; peak 26.7 W of 60 W | As stated | Met by design |
| R15 | Running power | 9.2 W | 15 W | Met on paper |
| R16 | Pilot kiosk parts cost | $739.00 (outdoor with sun shield $769.00) | $750 (`budget_usd`) | Met on paper |
| R17 | Cost with gateway (redefined, D1) | $1,029.00 | Reported; gateway costed in TwinKit | Met on paper (reported) |
| R18 | Honest in an outage | 2.40 h new, 1.63 h worst; 1.84 Ah pack needed | 2 h ride-through | **Not met** (worst case) |
| R19 | Secure by default | Outbound push and pull only | No inbound connections | Met by design |
| R20 | Street climate (target after the pilot) | Panel about 79 °C in sun and 45.1 °C shaded at 45 °C; pack 52.2 °C behind the sun shield; heater 13.5 W at -20 °C | -20 to +45 °C air | **Not met** |

Summary: 2 not met, 1 at risk, 10 met on paper, 7 met by design [K1]. The script counts R11 and R17 under "met on paper". Before v0.2: 4 not met, 2 at risk, 7 met on paper, 7 met by design.

## Changes from the TRL 2 estimates

*Table 3. TRL 2 figures checked against v0.1 of this note; later changes are in Table 4.*

| Quantity | TRL 2 (CTW-PRC-001 v0.2) | TRL 3 (v0.1) | Result |
| --- | --- | --- | --- |
| Records a day | About 4,896 | 5,616 | LoadZone rate from LDZ-CAL-001 |
| Radio airtime | About 900 s a day, 1 % of a channel, 0.13 % over 8 | 1,309 s, 1.52 %, 0.189 % | Corrected |
| Radio loss | About 3 % (assumed) | 0.61 % with downlink blanking | Calculated |
| Storage | About 350 MB a year | 2.89 GB a year raw, uncompressed | TwinKit's conservative 90 B per value |
| Open export | About 1,100 rows, 0.2 MB a day | 7,128 rows, 0.86 MB CSV a day | PotholeLog segments added |
| Worst data age | About 25 min | 25.9 min | Stands |
| Button to new layer | About 20 s | 19.8 s | Stands; R10 still not met |
| Kiosk and gateway power | About 9 W, 75 kWh a year | 10.2 W, 90 kWh a year | Hood light for 12 h, supply at 85 % |
| Post stress | About 12 MPa | 26.2 MPa with the 1.5 factor | Post drag and factor added; still met |
| Anchor tension | About 1 kN | 1.92 kN | As above |
| Mass | About 55 kg | 58.2 kg | From the model |
| Kiosk parts | About $740 | $739.00 | Stands |
| Kiosk and gateway | About $1,025 | $1,029.00 | TwinKit now $290.00 |
| Backup pack | Separate pack in the cabinet | Pack inside TwinKit's UPS module (TWK-DWG-001) | Model follows TwinKit |

## Changes in v0.2 (CTW-DDR-002)

*Table 4. Figures changed by the decisions of 2026-09-25.*

| Quantity | v0.1 | v0.2 | Cause |
| --- | --- | --- | --- |
| `budget_usd` | $600 | $750 | N1 |
| R10 target | Layer within 5 s | LED ring within 0.5 s, layer within 25 s | N2; status not met to met on paper |
| R12 pilot air range | 0 to 40 °C | 0 to 35 °C | N5; panel margin 4.9 K, pack 5.6 K; status at risk to met on paper |
| Hood light | 2 W, 1,459 lx | 0.3 W, 219 lx | N6 |
| Mains power | 10.2 W, 90 kWh a year | 9.2 W, 81 kWh a year | N6 |
| Cabinet rise in sun | 18.8 K | 18.7 K bare, 7.2 K with the sun shield | N4; lower head power trims the bare figure |
| Wind at the base | 792 N, 826 N·m; 26.2 MPa; 1.92 kN per anchor | 827 N, 848 N·m; 26.9 MPa; 1.97 kN per anchor | Sun shield area |
| Mass | 58.2 kg | 60.1 kg with the sun shield | N4 |
| Outdoor kiosk cost | Not costed | $769.00 | N4 |
| TwinKit pack for R18 | Not sized | At least 1.84 Ah | N3 |
