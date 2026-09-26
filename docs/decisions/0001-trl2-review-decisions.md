---
doc_id: CTW-DDR-001
title: CityTwin TRL 2 review decisions
project: CityTwin
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review recommendations adopted for TRL 3 work and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for D1 to D11. On 2026-09-25 Amish accepted all recommendations ("i accept all your recommendations, go with them across all repos"), so D1 to D11 are decided by Amish, 2026-09-25: go with recommendation. Item O1 had no recommendation and remains "Proposed, awaiting Amish". What changed in the repo is recorded in CTW-DDR-002.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed ten items as "Proposed, awaiting Amish", and the design precis (CTW-PRC-001 v0.2, Key design choices) gave a recommendation for most of them. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Under that instruction, every item that carries a recommendation is adopted as recommended for TRL 3 work, open for his review. Items without a recommendation stay open. v0.1 of this record left the recommended `budget_usd` figure unapplied. Later on 2026-09-25 Amish accepted all recommendations, which v0.2 records; the resulting changes are in CTW-DDR-002.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in CTW-PRC-001 v0.2, Key design choices. D11 is an interface proposal made in this session from the sibling repos' TRL 3 reviews.

## Decision

*Table 1. Items decided.*

| # | Item | Decided choice | Status |
| --- | --- | --- | --- |
| D1 | Budget | Option (b): the budget covers the kiosk only (items 1 to 12, 14 and 15); the TwinKit gateway is costed in the TwinKit repo. `budget_usd` is raised from $600 to $750 (CTW-DDR-002). R17 is redefined as a reported figure, not a budget target. | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Display | 13.3 in color e-paper for the street kiosk, with an indoor LCD variant for libraries and city hall lobbies (variant not modeled or costed at TRL 3). | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Climate range | Sheltered or indoor siting for the pilot, then a heater study at TRL 3. R12 is redefined as the pilot range (sheltered site, air 0 to 40 °C, no direct sun on the window); the outdoor range of -20 to +45 °C moves to a new R20 as the target after the pilot. The heater study is CTW-CAL-001 section F. | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Gateway location | TwinKit gateway in the kiosk cabinet for the pilot, on the upper DIN rail laid out as in TWK-DWG-001, with a coax lead to the post-top antenna; rooftop gateway for a full neighborhood. | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Power | Mains, with a solar head-only variant for sites without power (variant not modeled or costed at TRL 3). | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Privacy settings | Small-count threshold of 5 per hour; raw records kept two years; hourly aggregates kept indefinitely (sized for 10 years in CTW-CAL-001). | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Open data license | CC BY 4.0. | Decided by Amish, 2026-09-25: go with recommendation |
| D8 | Controls | Three push buttons rather than a touch screen, with the QR code handing richer use to the visitor's phone. | Decided by Amish, 2026-09-25: go with recommendation |
| D9 | Reference neighborhood | The 46-node reference neighborhood is kept for sizing. Reporting intervals now follow the sibling repos' TRL 3 figures (LoadZone 124 uplinks a day, not 64); CrossSafe's hourly summary remains a CityTwin assumption. | Decided by Amish, 2026-09-25: go with recommendation |
| D10 | Architecture | One-way publishing (no inbound connections to the gateway) and privacy rules enforced at the gateway as well as in the nodes (CTW-PRC-001 v0.2, Key design choices). | Decided by Amish, 2026-09-25: go with recommendation |
| D11 | Upload paths for PotholeLog and DockHub (new, from the sibling TRL 3 reviews) | The gateway pulls, by outbound HTTPS, the fleet operator's published daily PotholeLog segment files and DockHub's per-dock hourly aggregates from its back end. This keeps D10, because the gateway still accepts no inbound connection. Formats to be agreed with both repos (cross-repo action in `docs/REVIEW.md`); neither was edited. | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner city or neighborhood for co-design and a pilot site. No recommendation was made. | Proposed, awaiting Amish |

No reworded pitch or problem line was recommended, so `project.yaml` and `README.md` keep the existing wording.

## Consequences

- `project.yaml`: the TRL fields and evidence change; `budget_usd` was raised from $600 to $750 under CTW-DDR-002.
- CTW-PRB-001, CTW-PRC-001 and CTW-REQ-001 are revised to v0.3. The design choices in D1 to D10 are recorded as decided by Amish on 2026-09-25 (v0.4 of each). R12 and R17 are redefined, R20 is added and R1 is restated for the pull paths (D11).
- CTW-CAL-001 finds R10 (button response), R16 (kiosk cost against $600), R18 (backup in the worst case) and R20 (street climate) not met, and R1 and R12 at risk. New proposals from those findings are listed in `docs/REVIEW.md` and are not applied.
- Cross-repo: the gateway cost is taken from TwinKit's TRL 3 BOM ($290.00), matching TwinKit's own O1. CrossSafe defines no LoRaWAN uplink (its radio runs LoRa point to point between the two sides), so CityTwin's CrossSafe layer depends on an interface that CrossSafe has not yet defined. LoadZone's sign option needs class C downlinks from the TwinKit network server. See `docs/REVIEW.md`.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
