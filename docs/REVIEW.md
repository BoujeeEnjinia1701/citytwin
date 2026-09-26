# Review note: CityTwin

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Nothing here is recorded as decided or approved by Amish. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CTW-DDR-001 v0.1, status proposed): D1 to D10 adopted as recommended for TRL 3, open for Amish's review; D11 (pull paths for PotholeLog and DockHub) proposed in this session; O1 left open.
- `docs/04-calcs/01-sizing.md` (CTW-CAL-001 v0.1), `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: radio load and loss with the sibling repos' TRL 3 rates and LoadZone downlinks, storage and export, data age and button timing, legibility, night light and hood shading, accessibility geometry, head and cabinet thermal with a heater study, power and supply sizing, wind, weld, anchors and mass, backup, and cost, with a status for every requirement. The script imports the model's parameters and part volumes, reads the BOM and `project.yaml`, and prints every quoted number with a tag.
- `cad/src/model.py`: parametric build123d kiosk (base plate and anchors, post with cable entry, head with window, button holes and vents, window, e-paper, controller, buttons, notice plate, hood with light, cabinet with two TS35 rails, RCBO and SPD, 12 V supply, TwinKit gateway laid out as in TWK-DWG-001, antenna, conduit). Exports `cad/step/` and `cad/stl/` for `citytwin-kiosk-assembly`, `kiosk-head`, `services-cabinet` and `post-and-base`. A clash check finds only the intended wall penetrations of the conduit and cable entry.
- `cad/src/sheets.py` and `cad/drawings/CTW-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:20, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". CTW-DWG-001 was free because the concept blueprint is CTW-DWG-010.
- `bom/bom.csv` (18 lines, all priced with a supplier or supplier type) and `bom/bom-notes.md`. TwinKit now at its TRL 3 price, $290.00.
- `cad/src/concept_media.py` now builds from the model; all of `media/` re-rendered (hero, blueprint, cutaway, exploded, flow, `model.glb`, `viewer.html`) and every image checked; no `media/_views*` folders remain.
- CTW-PRB-001, CTW-PRC-001 and CTW-REQ-001 revised to v0.3; `README.md` (TRL badge and line, budget line, links, concept numbers, components, safety; the required sections keep their order and wording) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

### Requirement status (CTW-CAL-001, Table 2)

4 not met, 2 at risk, 7 met on paper, 7 met by design (R11's web page is not verifiable at TRL 3).

| ID | Status | Key number |
| --- | --- | --- |
| R10 Button response | **Not met** | 19.8 s against 5 s (0.79 s transfer plus 19 s full refresh) |
| R16 Kiosk cost | **Not met** | $739.00 against $600 (`budget_usd`); $11.00 under the recommended $750 |
| R18 Outage ride-through | **Not met** (worst case) | TwinKit backup 2.40 h new, 1.63 h aged at 0 °C, against 2 h |
| R20 Street climate (new) | **Not met** | Panel about 79 °C in low sun at 45 °C air; 13.5 W to hold an insulated panel bay at 0 °C in -20 °C air |
| R1 Ingest every type | At risk | Six LoRaWAN types on paper; PotholeLog and DockHub pull paths not agreed; CrossSafe has no LoRaWAN uplink |
| R12 Pilot climate (redefined) | At risk | Panel 40.1 °C at 40 °C air; cabinet pack 0.6 K under its 45 °C charge limit |
| R2, R8, R9, R11, R13, R15, R17 | Met on paper | 5,616 uplinks a day, 0.61 % lost; 25.9 min data age; 41 px capitals; 200 mm overhang; 26.2 MPa post, 1.92 kN per anchor; 10.2 W; $1,029.00 reported |
| R3 to R7, R14, R19 | Met by design | 7,128 export rows a day; 12 V peak 26.7 W on 60 W |

Corrections to TRL 2 figures: 5,616 uplinks a day, not 4,896 (LoadZone sends 124 a day, not 64); radio loss 0.61 %, not an assumed 3 %; storage 2.89 GB a year raw at TwinKit's conservative row size, not 350 MB; export 7,128 rows a day once PotholeLog segments are counted, not 1,100; power 10.2 W, not 9 W; post stress 26.2 MPa with post drag and the 1.5 factor, not 12 MPa; mass 58.2 kg, not 55 kg; gateway $290.00, not $285. The backup pack now sits inside TwinKit's UPS module, as TwinKit draws it.

### Decisions recorded (CTW-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: D1 budget option (b), the budget covers the kiosk and the gateway is costed in TwinKit (R17 redefined; `budget_usd` unchanged at $600, $750 recorded as awaiting Amish); D2 color e-paper with an indoor LCD variant; D3 sheltered or indoor pilot and a heater study at TRL 3 (R12 redefined to the pilot, R20 added); D4 gateway in the kiosk cabinet; D5 mains power with a solar head-only variant; D6 small-count threshold 5 per hour and two years of raw data; D7 CC BY 4.0; D8 buttons; D9 the 46-node reference neighborhood with the sibling TRL 3 rates; D10 one-way publishing and privacy rules at the gateway. No reworded pitch or problem line was recommended, so `project.yaml` and `README.md` keep the existing wording.

### Still awaiting Amish

1. **O1, first partner city or neighborhood** for co-design and a pilot site. No recommendation was made.
2. **Budget figure.** `budget_usd` stays $600; $750 is recommended (D1). The kiosk at $739.00 fits $750.
3. **New, D11 pull paths.** The gateway fetches PotholeLog's published segment files and DockHub's hourly aggregates by outbound HTTPS. Recommendation: adopt, and agree formats with both repos. Used for sizing; not agreed.
4. **New, R10.** Options: (a) restate R10 as "press acknowledged within 0.5 s by the LED ring and a first on-screen cue; layer shown within 25 s"; (b) keep 5 s and fit an LCD in the indoor variant only; (c) a smaller monochrome status panel for instant feedback. Recommendation: (a) for the street kiosk and (b) indoors. Not applied.
5. **New, R18.** Options: (a) restate R18 at 1.5 h; (b) ask TwinKit for a larger pack in cabinet installs; (c) keep 2 h and accept not met. Recommendation: (b), since winter cold in a street cabinet shortens the runtime further. Not applied.
6. **New, R20 and the cabinet.** Options for a street kiosk: a heated, insulated panel bay (13.5 W at -20 °C, not costed), a north-facing or shaded screen, a ventilated sun shield on the cabinet, or a wider-range panel if one exists. Recommendation: a sun shield on the cabinet and a shaded screen orientation as site rules for any outdoor pilot; a heater only if the partner city has frost. Not applied.
7. **New, R12 margin.** At 40 °C air the panel and pack have no margin. Recommendation: define the pilot range as 0 to 35 °C air. Not applied.

Suggestion only, not in the repo: dim the hood light to about 0.3 W (200 lx is enough), which would cut 0.9 W from the average.

### Cross-repo consistency

- **TwinKit (TRL 3):** gateway $290.00, 6.41 W, 20.6 W peak, 294 mm of rail, backup 2.40 h and 1.63 h worst, processor 69.1 °C at 40 °C, loss 1.02 % at 14,400 uplinks a day; all used as published. TwinKit's review asked for a separate thermal check of the street cabinet: this note finds the cabinet 4.4 K above ambient in shade and 18.8 K in sun, so TwinKit's 0 to 40 °C rating and the pack's 45 °C charge limit hold only on a sheltered site. The TwinKit whip is replaced by a coax lead to a post-top antenna; TwinKit's SMA bulkhead allows this. TwinKit's network server must support LoRaWAN class C for LoadZone's sign (LoadZone O5). TwinKit not edited.
- **PotholeLog (TRL 3):** uploads 112 kB a day per vehicle to the fleet operator's server and asked how CityTwin would receive the files given no inbound connections; D11 answers with an outbound pull. A publication date on a daily segment aggregate is compatible with PotholeLog's R13 if pass times stay unpublished. PotholeLog not edited.
- **DockHub (TRL 3):** syncs over LTE-M to its own back end and logs 1.28 kB a day; CityTwin assumes DockHub's back end publishes per-dock hourly aggregates for D11. DockHub names TwinKit only as a later suggestion. Not edited.
- **LoadZone (TRL 3):** 124 uplinks a day per puck of 12 B, and about 200 downlinks a day per sign; the downlinks cost 0.23 % of the gateway's receive time with six signs. No conflict.
- **CrossSafe (TRL 3), conflict:** its radio runs LoRa point to point between the two sides and no LoRaWAN uplink is defined, so CityTwin's CrossSafe layer has no interface yet. Noted here; CrossSafe not edited.
- **FloodGauge, CurbCount, HeatMap Node, AirStreet, NoiseMap (TRL 3):** rates and payloads as in their notes; NoiseMap's note confirms the 96 uplinks a day CityTwin assumed. FloodGauge's event mode is covered in the storm peak hour (0.94 % loss). CurbCount's and LoadZone's US915 payload packing does not change CityTwin's load.
- FieldNode, CellGuard, MotionCore, ThermaCart and CalRig are not used by CityTwin.

### Safety concerns

- Mains voltage in the cabinet: electrician installation, 30 mA RCBO, surge protection, earthing of all metal parts, locked door, only 12 V SELV in the head.
- LiFePO4 backup pack in a sealed steel cabinet: in sun the cabinet air reaches about 64 °C at 45 °C ambient, far above the pack's charge limit, and in frost it cannot charge. The UPS lockout must never be defeated; site the pilot out of direct sun.
- A 58 kg post beside a walkway: the footing and anchors need a structural design to the local code; vehicle impact is not covered by this note. The hood corners overhang the post by 200 mm at head height: round and pad them.
- Privacy: the schema check and small-count suppression at the gateway need review; outbound pulls must fetch only published aggregates, never raw PotholeLog tracks or DockHub logs.
- Over-reliance: CityTwin is not a flood or emergency warning system.

### Gaps and notes

- Citations: none were flagged as unchecked at TRL 2. The Access Board protruding-objects guide (685 to 2,030 mm, 305 mm overhang on posts) was checked by WebFetch on 2026-09-25 and is now cited. The Waveshare refresh time and temperature range were not re-fetched. WebSearch was not used.
- Assumptions only tests can settle: film coefficients and absorptance, panel heating through the window, controller and hood light power, supply efficiency at light load, anchor resistance, and bought-in masses.
- The kit's cutaway cuts on a Y plane near the parts' mean; as at TRL 2, `concept_media.py` makes its own X-plane section on the kiosk centerline with the kit's renderer. It works for this model without shifting it.
- In `media/exploded.png` the callouts for the small parts 7, 11 and 12 partly cover them.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. `electronics/` and `firmware/` are empty. No test, build or firmware material was created.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. The next step is Amish's review of CTW-DDR-001 (D1 to D11) and a choice on items 1 to 7 above, plus interface agreements with PotholeLog, DockHub and CrossSafe. For the record only, TRL 4 would need: a bench build of the kiosk head and cabinet with a TwinKit gateway; a lab test report (TST, `environment: lab`) covering button-to-layer timing, panel and cabinet temperatures in a climate chamber with a sun lamp, mains power draw, backup runtime with a cold pack, and ingest of recorded sibling payloads through the schema check; and build log entries. None of this has been started.

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
