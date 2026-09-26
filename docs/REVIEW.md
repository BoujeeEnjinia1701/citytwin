# Review note: CityTwin

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (CTW-PRB-001 v0.2): problem, trust evidence, prior work (Sentilo, Civil IoT Taiwan, OGC SensorThings API, DTPR, AirQo), users, operating environment, a proposed 46-node reference neighborhood, constraints, out of scope, open questions; co-design checklist kept.
- `docs/03-requirements.md` (CTW-REQ-001 v0.2): 19 measurable requirements with targets and a status column against the concept estimates.
- `docs/02-concept.md` (CTW-PRC-001 v0.2): how it works (collect, check, store, privacy rules, publish, show), 18 numbered components, data load and kiosk estimates, design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of the public kiosk (post, base plate, display head, window, e-paper, controller, buttons, notice plate, hood, services cabinet with mains protection, 12 V supply and TwinKit gateway, antenna, conduit) in street context with a 1.75 m figure. The cutaway uses a custom section on the kiosk centerline, because the kit's default Y cut would slice across the screen instead of through the layers.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with callouts 1 to 15, `cutaway.png`, `flow.png` (data flow in records per day, estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 18 lines, numbered to match the exploded view (16 to 18 are software and documents with no callout); `bom/bom-notes.md` explains what is in and out of each cost.
- `README.md`: hero image and links line, expanded concept rationale, burning platform, where it could be used, what sparked the idea, concept, components and safety.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem still match the concept.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Reference neighborhood | 46 LoRaWAN nodes, about 4,900 records per day | R2 met (50 nodes, 10,000 per day) |
| Radio airtime | about 1 % of one channel, about 0.13 % over 8 | R2 met |
| Storage | about 350 MB per year | |
| Worst data age on screen | about 25 min | R8 met, thin margin (30 min) |
| Button to new layer | about 20 s | **R10 not met** (5 s) |
| Display operating range | 0 to 40 °C (maker's manual) | **R12 not met** (-20 to +45 °C) |
| Kiosk and gateway power | about 9 W, about 75 kWh per year | R15 met (15 W) |
| Post stress at 35 m/s gust | about 12 MPa | R13 met |
| Kiosk mass | about 55 kg | |
| Kiosk parts cost | about $740 | **R16 not met** ($600) |
| Kiosk plus TwinKit gateway | about $1,025 | **R17 not met** ($600 `budget_usd`) |

Requirements not met or at risk:

- **R10 not met:** the color e-paper has no partial refresh and takes about 19 s for a full refresh.
- **R12 not met:** the panel is rated 0 to 40 °C; a sunlit head in a 45 °C day or a Canadian winter falls outside that.
- **R16 and R17 not met:** kiosk about $740, about $1,025 with the gateway, against $600.
- **R1 at risk:** PotholeLog and DockHub upload paths into CityTwin are not defined in those repos.

### Proposed, awaiting Amish

1. **Budget.** Parts exceed `budget_usd` ($600). Options: (a) keep $600 and define it as the kiosk only, then cut about $140 (for example a steel head in place of aluminum, a cheaper cabinet, or a smaller 10 in class display); (b) raise `budget_usd` to about $750 for the kiosk, with the TwinKit gateway costed in TwinKit; (c) raise it to about $1,050 for kiosk and gateway. Recommendation: (b), because one gateway serves many nodes and is already budgeted in TwinKit. `project.yaml` is unchanged.
2. **Display.** Color e-paper (sun-readable, low power, slow, 0 to 40 °C), monochrome e-paper (faster, no color layers), or an outdoor LCD (instant, touch possible, costly and power-hungry). Recommendation: color e-paper, plus an indoor LCD variant.
3. **Climate range.** Thermostatic heater and more shading, a wider-range panel, or indoor or sheltered siting only for the first pilot. Recommendation: sheltered or indoor siting for the pilot, then a heater study at TRL 3.
4. **Gateway location.** In the kiosk cabinet (one site, low antenna) or on a rooftop (better range, second site). Recommendation: in the cabinet for the pilot.
5. **Power.** Mains, or a solar head-only variant for sites without power. Recommendation: mains.
6. **Privacy settings.** Small-count threshold (proposed 5 per hour) and raw data retention (proposed two years).
7. **Open data license.** CC BY 4.0, CC0 or ODbL. Recommendation: CC BY 4.0.
8. **Buttons rather than a touch screen**, with the QR code handing richer use to the visitor's phone.
9. **Reference neighborhood** of 46 nodes used for sizing, and the assumed intervals for CrossSafe, FloodGauge and LoadZone.
10. **First partner city or neighborhood** for co-design and a pilot site.

### Safety concerns

- Mains voltage in the services cabinet: electrician installation, 30 mA RCBO, surge protection, earthing of all metal parts, locked door, only 12 V SELV in the head.
- LiFePO4 backup pack in the TwinKit gateway inside a sealed cabinet that can get hot in the sun.
- A roughly 55 kg post beside a walkway: footing, wind and vehicle impact, sharp edges at head height, walkway clearance, two-person lift.
- Privacy: a changed node or a new node type could try to send more than counts and levels; the schema check at the gateway and small-count suppression address this but need review.
- Over-reliance: CityTwin must not be treated as a flood or emergency warning system.

### Problems and notes

- The kit's `cutaway_parts` cuts only on a Y plane; `concept_media.py` makes its own X-plane section with the kit's renderer. Worth adding an axis option to the kit (suggestion, not done here).
- Figures on the EU regulation and Brazil's data protection law were checked on the official texts; the EU application date (June 2024) comes from the EUR-Lex record.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 to 3. If approved, run `/advance-trl3` to check the data load, timing, thermal, wind and power estimates by calculation, and to agree the upload interfaces with PotholeLog, DockHub, CrossSafe, FloodGauge and LoadZone.
