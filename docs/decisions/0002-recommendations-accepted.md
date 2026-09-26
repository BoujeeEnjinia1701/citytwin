---
doc_id: CTW-DDR-002
title: CityTwin recommendations accepted
project: CityTwin
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the recommendations accepted by Amish on 2026-09-25, what changed in the repo and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below that carried a recommendation is decided by Amish, 2026-09-25: go with recommendation. Items with no recommendation stay "Proposed, awaiting Amish".

## Context

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Before that, CTW-DDR-001 (D1 to D11) recorded this repo's TRL 2 review choices as adopted for TRL 3 work and open for his review, and the TRL 3 review note (`docs/REVIEW.md`, session 2026-09-25: TRL 3) listed six further items with options and a recommendation. This record lists every item now decided, what changed in the repo because of it, and what remains open. Where a recommendation offered several options, the recommended option is the decision. Work that belongs to TRL 4 (build, test, measurement, purchasing, firmware beyond a sketch) is decided but on hold, because TRL 4 is on hold by Amish's instruction.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Budget scope (CTW-DDR-001) | Option (b): the budget covers the kiosk; the TwinKit gateway is costed in TwinKit | Status wording only; R17 stays a reported figure |
| D2 | Display | Color e-paper for the street kiosk, indoor LCD variant | Status wording; the indoor LCD variant is named in R10 and remains unmodeled at TRL 3 |
| D3 | Climate range | Sheltered or indoor pilot, heater study at TRL 3 | Status wording (range narrowed by N5 below) |
| D4 to D10 | Gateway in the cabinet; mains power with a solar variant; 5 per hour threshold and two years of raw data; CC BY 4.0; buttons; 46-node reference neighborhood; one-way publishing with privacy rules at the gateway | As recommended | Status wording in CTW-DDR-001 v0.2, CTW-PRB-001 v0.4, CTW-PRC-001 v0.4 and CTW-REQ-001 v0.4 |
| D11 | Pull paths for PotholeLog and DockHub | The gateway pulls published PotholeLog segment files and DockHub hourly aggregates by outbound HTTPS | Status wording; format agreement listed as a cross-repo action in `docs/REVIEW.md` |
| N1 | Budget figure | `budget_usd` raised to the recommended $750 | `project.yaml` `budget_usd` $600 to $750; R16 now **met on paper** for the pilot kiosk ($739.00, $11.00 under); README budget line updated |
| N2 | R10 button response | Option (a) for the street kiosk and (b) indoors: press acknowledged within 0.5 s by the button's LED ring and layer shown within 25 s; the indoor LCD variant keeps 5 s | R10 restated in CTW-REQ-001; firmware rule "LED ring lit from the press until the new image is drawn" added to CTW-PRC-001; CTW-CAL-001 [C2] checks both limits; R10 **not met** (19.8 s against 5 s) to **met on paper** (30 ms and 19.8 s against 0.5 s and 25 s) |
| N3 | R18 outage ride-through | Option (b): ask TwinKit for a larger pack in cabinet installs | CTW-CAL-001 [I1] now sizes the pack: at least 1.84 Ah against TwinKit's 1.5 Ah. Request listed as a cross-repo action; TwinKit not edited. R18 stays **not met** until TwinKit changes its pack |
| N4 | R20 street climate and the cabinet | A ventilated sun shield on the cabinet and a shaded screen orientation as site rules for any outdoor pilot; a panel heater only if the partner city has frost | New BOM item 19, cabinet sun shield (1.5 mm aluminum, 413 x 186 x 486 mm, 25 mm air gap, open bottom, top vents), $30.00, in `cad/src/model.py`, STEP and STL, CTW-DWG-001 Rev P2 and all media. CTW-CAL-001 v0.2: cabinet rise in sun 18.7 K without the shield, 7.2 K with it; the pack stays under its 45 °C charge limit in full sun up to 37.8 °C air. Site rules added to CTW-PRC-001. R20 stays **not met** (panel 45.1 °C shaded at 45 °C air) |
| N5 | R12 pilot margin | Define the pilot range as 0 to 35 °C air | R12 target 0 to 40 °C to 0 to 35 °C; panel 35.1 °C (4.9 K margin), pack 39.4 °C (5.6 K margin); R12 **at risk** to **met on paper** |
| N6 | Hood light (suggestion in the TRL 3 review note) | Dim the 2 W hood light to about 0.3 W, since 200 lx is enough | Controller rule in CTW-PRC-001; CTW-CAL-001 [D2, G1]: 219 lx at night, mains power 10.2 W to 9.2 W, 90 to 81 kWh a year |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner city or neighborhood for co-design and a pilot site. No recommendation was made. | Proposed, awaiting Amish |
| Q1 | Antenna height needed for the reference neighborhood with the gateway in the cabinet | Open question, no recommendation made |
| Q2 | Languages and scripts on the kiosk, and how residents ask questions or report a fault | Open question, no recommendation made; for co-design with the partner city (O1) |

## Consequences

- `project.yaml`: `budget_usd` $750. Pitch and problem unchanged: no rewording was recommended. `trl: 3` and `trl_target: 3` unchanged.
- Documents revised: CTW-PRB-001 v0.4, CTW-PRC-001 v0.4, CTW-REQ-001 v0.4, CTW-CAL-001 v0.2, CTW-DDR-001 v0.2; drawing CTW-DWG-001 Rev P2; `bom/bom.csv` (19 lines) and `bom/bom-notes.md`; `README.md`.
- Requirement status (CTW-CAL-001 v0.2): 2 not met (R18, R20), 1 at risk (R1), 10 met on paper, 7 met by design. Before: 4 not met, 2 at risk, 7 met on paper, 7 met by design.
- The sun shield adds 1.86 kg and 35 N of gust load: post stress 26.2 to 26.9 MPa, anchor tension 1.92 to 1.97 kN, mass 58.2 to 60.1 kg. All still met.
- Cross-repo actions (TwinKit pack, PotholeLog and DockHub pull formats, CrossSafe uplink) are listed in `docs/REVIEW.md`. No other repo was edited.
- On hold at TRL 4 by Amish's instruction: the panel heater (only for a frost site), the indoor LCD and solar variants beyond their mention, and every build, bench timing, climate chamber and outage test. Nothing in this record authorizes building or testing.
