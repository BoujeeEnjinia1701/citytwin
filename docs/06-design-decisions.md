---
doc_id: CTW-DEC-001
title: CityTwin design decisions register
project: CityTwin
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the review note, the decision records and the build plan work
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Amish approved the recommendations for open items 1 to 7 on 2026-10-02 (shield holes only where fitted, sheltered pilot near Irving, antenna walk test, languages, R20 kept as post-pilot target, pull format, CrossSafe uplink request); moved to decisions made
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Design for construction (CTW-DDR-003, P1 to P14) accepted by Amish on 2026-10-02; moved from open for review to decisions made"
---

# CityTwin design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, CTW-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

*Table 2. Items to confirm against the chosen part.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The cabinet comes with a removable mounting plate of about 340 x 390 mm on studs that stand it at least 10 mm off the back wall, and a lockable door on the 360 x 460 mm face | The rails, the cabinet screws behind the plate and the 25 mm cable hole above the plate are placed for this | CTW-DDR-003, P9 |
| 2 | The e-paper panel's outline (210 x 290 x 7 mm assumed) and where its flat cable leaves the panel | Sets the foam gasket, the carrier's ribbon slot and the driver board position | CTW-DDR-003, P4 |
| 3 | The M8 steel flush rivet nuts' grip range covers the 4 mm post wall with its coating, and their countersink size | The head and cabinet screws depend on them | CTW-DDR-003, P1 |
| 4 | The buttons' LED rings run from 5 V or 12 V, and their nut size fits beside the notice plate | Sets the LED driver wiring and the clearance below the notice plate | CTW-DDR-003, P5, P6 |
| 5 | TwinKit fits a backup pack of at least 1.84 Ah for cabinet installs (now 1.5 Ah); until then R18 is not met in the worst case | The outage ride-through of 2 h | CTW-DDR-002, N3 |
| 6 | The hood light's LED strip and dusk sensor work from the 12 V supply through the LED driver, dimmed to about 0.3 W | Night lighting (R9) and running power (R15) | CTW-DDR-002, N6 |
| 7 | The anchor design resistance (10 kN per M16 anchor assumed) and the footing, from a structural design to the local code | Wind (R13) and the safety of a kiosk of about 64 kg beside a walkway | CTW-CAL-001, section H |

## Value engineering

Value-engineering target: USD 750 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 778 for the pilot kiosk (USD 28 over the target; the pilot site is sheltered, so no sun shield or frost heater, decided 2026-10-02); USD 808 with the outdoor sun shield, and USD 1,068 with the TwinKit gateway, which is costed in TwinKit.

- **Main cost drivers:** the parts added to make the kiosk buildable (display carrier USD 8, fixings USD 22, and USD 13 more for the head's converter, LED driver and terminal block, less USD 4 moved out of another item); the outdoor sun shield (USD 30), reported separately.
- **Savings worth trying:** a lower-cost cabinet; dropping the real-time clock; checking prices at purchase, since the figures are indicative.

## Decisions made

*Table 3. Decisions made, with the record that argues each one.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D11: budget covers the kiosk only; color e-paper with an indoor LCD variant; sheltered pilot; gateway in the kiosk cabinet; mains power; 5 per hour small-count threshold and two years of raw data; CC BY 4.0; buttons; 46-node reference neighborhood; one-way publishing; outbound pulls for PotholeLog and DockHub | Amish: "i accept all your recommendations, go with them across all repos." | [CTW-DDR-001](decisions/0001-trl2-review-decisions.md), [CTW-DDR-002](decisions/0002-recommendations-accepted.md) |
| 2026-09-25 | N1 to N6: `budget_usd` $750; R10 restated (LED ring within 0.5 s, layer within 25 s); larger TwinKit pack requested; cabinet sun shield and shaded screen as outdoor site rules, heater only for a frost city; pilot range 0 to 35 °C air; hood light dimmed to about 0.3 W | Amish, same instruction | [CTW-DDR-002](decisions/0002-recommendations-accepted.md) |
| 2026-10-01 | Design for construction, P1 to P14: rivet nuts in the post for the head and cabinet; folded head tray with a removable front panel; window bonded with glazing tape; display carrier on studs; 5 V converter, LED driver and terminal block in the head; button, notice plate and hood fixings; mounting plate in the cabinet; grommeted cable holes; conduit hole and gland; vent hole for galvanizing; antenna bracket plate; shield on standoffs with a thumb-screw back panel | Made under Amish's 2026-09-30 instruction to make the design physically buildable ("If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations."); the changes themselves were accepted on 2026-10-02 (below) | [CTW-DDR-003](decisions/0003-design-for-construction.md) |
| 2026-10-02 | Sun shield standoff holes: option (a), drilled only in cabinets that get the shield, so the sheltered pilot cabinet keeps its unbroken IP55 sides | Amish: "i approve your recommendations for all 555 open decisions." | [CTW-DDR-003](decisions/0003-design-for-construction.md), A2 |
| 2026-10-02 | First partner and pilot site: a city within easy reach of Irving, Texas, with an active open-data program, the kiosk in a sheltered public lobby such as a library or transit center; with a sheltered site the frost heater is not fitted. The city is chosen as the first candidate to approach, not yet agreed | Amish: "i approve your recommendations for all 555 open decisions." | [CTW-DDR-001](decisions/0001-trl2-review-decisions.md), O1; [CTW-DDR-002](decisions/0002-recommendations-accepted.md) |
| 2026-10-02 | Antenna: keep the post-top antenna at 2.38 m for the pilot and run a coverage walk test from the site at TRL 4; if nodes in the reference neighborhood fall short, move to a rooftop gateway, not a taller mast | Amish: "i approve your recommendations for all 555 open decisions." | [CTW-DDR-002](decisions/0002-recommendations-accepted.md), Q1 |
| 2026-10-02 | Languages: English plus the partner city's most widely spoken other language in its own script, with a QR code and a phone or text number on the notice plate for questions and fault reports; refined with the partner in co-design | Amish: "i approve your recommendations for all 555 open decisions." | [CTW-DDR-002](decisions/0002-recommendations-accepted.md), Q2 |
| 2026-10-02 | Street climate (R20): kept as a post-pilot target; outdoor sites only in permanent shade with the sun shield; a panel rated above 40 °C is sought at TRL 4, and the heated bay is fitted only for a frost city | Amish: "i approve your recommendations for all 555 open decisions." | CTW-PRC-001, open questions; CTW-REQ-001, R20 |
| 2026-10-02 | Pull paths: the outbound pull already decided (D11), with daily CSV files on a fixed HTTPS address at each operator, a published column list and a version field; the same format to be agreed in PotholeLog (its open item 6) | Amish: "i approve your recommendations for all 555 open decisions." | [CTW-DDR-001](decisions/0001-trl2-review-decisions.md), D11 |
| 2026-10-02 | CrossSafe uplink: ask CrossSafe to add an hourly LoRaWAN summary uplink from one side of the crossing; CityTwin shows no CrossSafe layer until it exists | Amish: "i approve your recommendations for all 555 open decisions." | CTW-REQ-001, R1 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P14, as made | Amish: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)" | [CTW-DDR-003](decisions/0003-design-for-construction.md), Table 1 |
