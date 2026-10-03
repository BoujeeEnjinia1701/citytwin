# Review note: CityTwin

## Session 2026-10-01: design for construction and the prototype build plan

On 2026-09-30 Amish approved the build plan format and asked for it across all repos, with open decisions kept in a separate register, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." Kit 1.7.0 was installed (`.kit/`, `.claude/commands/`, root `CLAUDE.md`) and `/build-plan` was carried out. Nothing was built or tested; TRL stays 3.

### Design changes made for construction (CTW-DDR-003, Draft, open for Amish's review)

Made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.

| # | Change |
| --- | --- |
| P1 | Eight M8 flush steel rivet nuts in the post; the head tray and the cabinet each held by four M8 screws with 30 mm washers from inside |
| P2 | Display head is a folded 2 mm tray with a 15 mm return flange, closed by a removable 2 mm front panel on twelve M4 tamper-resistant screws into rivet nuts, with a gasket |
| P3 | Window bonded inside the front panel with 1 mm glazing tape on its 8 mm lap |
| P4 | New display carrier (BOM 20) on eight clinch studs and 15 mm spacers presses the e-paper panel onto a 1 mm foam gasket and carries the driver board and controller |
| P5 | 12 V to 5 V converter, 4-channel LED driver and a pluggable fused terminal block added to BOM item 6 ($42.00 to $55.00) |
| P6 | Button holes 19.2 mm, bezel outside, nut inside |
| P7 | Notice plate held by four M4 tamper-resistant screws with nyloc nuts |
| P8 | Hood is folded 1.5 mm sheet on four M5 screws into rivet nuts in the head top; LED strip on an angle behind the lip; LED cable through a grommet in the front panel |
| P9 | DIN rails on the cabinet's mounting plate on 10 mm standoffs |
| P10 | 25 mm grommeted cable holes through post and cabinet (735 mm) and post and head (1,380 mm), replacing a slot that met a solid wall |
| P11 | 40 mm conduit hole in the base plate and a conduit gland in the cabinet floor |
| P12 | Anchor holes, washers and nuts; 25 mm vent and drain hole under the post so it can be galvanized |
| P13 | Antenna bracket is a 60 x 60 x 6 mm plate screwed to the cap |
| P14 | Sun shield on four 25 mm standoffs through the cabinet sides; separate back panel on four thumb screws |
| | New BOM line 21 (fixings, tapes and gaskets, $22.00); line 15 repriced to $26.00 |

The model runs 244 constructability checks (`python cad/src/model.py --check`), all passing: no overlaps, 50 contacts, 10 clearances.

### Key results (CTW-CAL-001 v0.3)

- **R16 is now over the value-engineering target by $28.00:** the estimated cost of the pilot kiosk is $778.00 against the $750 target (a hypothetical control target); $808.00 with the outdoor sun shield; $1,068.00 with the TwinKit gateway. `budget_usd` was not changed.
- Mass 63.5 kg with the sun shield (was 60.1 kg). Wind: 821 N, post 26.6 MPa, 1.94 kN per anchor (R13 still met on paper).
- Requirement status: 2 not met (R18, R20), 1 over the value-engineering target (R16), 1 at risk (R1), 9 met on paper, 7 met by design.
- Thermal, power, radio, timing and legibility are unchanged.

### What was made

- `cad/src/model.py`: constructable model with `build_components()`, the checks and STEP and STL exports (`cad/step/`, `cad/stl/`, four groups).
- `cad/src/sheets.py` and `cad/drawings/CTW-DWG-001` at Rev P4.
- `cad/src/build_plan_media.py`: overview, 11 making sketches (`cad/drawings/CTW-DWG-101` to `111`), 10 joint pictures (six of them true sections to scale), 16 step pictures, post and front panel hole layouts and a wiring diagram, in `docs/05-build-plan/`.
- `docs/05-build-plan.md` (CTW-BLD-001 v0.1) and `docs/06-design-decisions.md` (CTW-DEC-001 v0.1); `docs/decisions/0003-design-for-construction.md` (CTW-DDR-003 v0.1).
- Updated: `bom/bom.csv` (21 lines), `bom/bom-notes.md`, `docs/04-calcs/sizing.py`, `results.csv` and CTW-CAL-001 v0.3, CTW-REQ-001 v0.5, CTW-PRC-001 v0.5, CTW-PRB-001 v0.5, `README.md` (links line, components, figures, "Building the prototype"), `project.yaml` (`design_state: constructable`, evidence), concept media in `media/` regenerated from the new model, and the PDFs in `docs/pdf/`.

### Proposed, awaiting Amish (also in CTW-DEC-001)

1. **Shield standoff holes (A2).** Drill only kiosks that get the shield (recommended), or every cabinet with sealed blanking screws.
2. Still open from earlier: first partner city (O1), antenna height (Q1), languages and fault reporting (Q2), street climate panel (R20), PotholeLog and DockHub pull formats, CrossSafe uplink.

### Stale on Amish's Mac

The photoreal renders (`media/render-hero.png`, `media/render-detail.png`), `media/card.png` and `media/social-preview.png` show the concept head, hood and shield; the shield's standoffs and separate back panel, the front panel screws and the thinner hood edge now differ. They were not regenerated here (`media/render-hero.png` is also missing from this copy).

### Safety

No change to the safety case. The plan adds safety stops for lifting the post, mains work (electrician only), first switch-on, the gateway pack fuse, work at the post top, 12 V to the head, and leaving the kiosk unattended. The hood corners at head height are now specified as rounded to at least 10 mm.

### Recommended next step

Amish's review of CTW-DDR-003 and decision A2; the register's Value engineering section holds the $750 target, the $778.00 estimate and the savings worth trying. TRL 4 (building and testing to CTW-BLD-001) remains on hold.

## Session 2026-09-26: sources strengthened

Amish asked on 2026-09-26 to "Fix the weaker sources." README.md sections Concept rationale, Burning platform, Where it could be used and What sparked the idea were checked; every kept link was fetched and confirmed against its claim.

| Where | Old source | New source |
| --- | --- | --- |
| What sparked the idea (Amsterdam sensor register) | Cities Today (trade press) with the Sensorenregister site | The regulation itself, Verordening meldingsplicht sensoren ([Gemeenteblad 2021, 368183](https://zoek.officielebekendmakingen.nl/gmb-2021-368183.html)), with the Sensorenregister site |

The paragraph now states only what the regulation supports: in force December 1, 2021, advance reporting of what data a sensor collects, exemptions for private individuals and police or public order use, six months for sensors already in place, and a city register of the reports. The claims that the register map shows owner and personal data processing and that the city could remove unregistered sensors at the owner's expense rested on Cities Today alone and were removed. The inspiration event is unchanged; its line in INSPIRATIONS.md now names the Gemeenteblad source. docs/01-problem.md did not cite Cities Today and was not changed. No budget change.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Every item in this note and in CTW-DDR-001 that carried a recommendation is now **decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (CTW-DDR-002 v0.1). Items with no recommendation stay "Proposed, awaiting Amish". Nothing past TRL 3 was done.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| D1 to D11 (CTW-DDR-001) | Budget scope, color e-paper, sheltered pilot, gateway in the cabinet, mains power, privacy settings, CC BY 4.0, buttons, reference neighborhood, one-way publishing, outbound pulls | Adopted for TRL 3, open for review | Decided; status wording in CTW-DDR-001 v0.2, CTW-PRB-001 v0.4, CTW-PRC-001 v0.4, CTW-REQ-001 v0.4 |
| N1 budget figure | Recommended $750 | `budget_usd` $600; R16 not met ($139.00 over) | `budget_usd` $750; R16 met on paper ($11.00 under) |
| N2 R10 | Option (a) street, (b) indoor LCD | Layer within 5 s; 19.8 s, not met | LED ring within 0.5 s (about 30 ms) and layer within 25 s (19.8 s), met on paper; the indoor LCD variant keeps 5 s (not modeled) |
| N3 R18 | Option (b), larger TwinKit pack | Pack not sized | At least 1.84 Ah needed against 1.5 Ah; requested from TwinKit; R18 still not met |
| N4 R20 and cabinet | Cabinet sun shield and shaded screen as site rules; heater only for a frost city | Cabinet 18.8 K over ambient in sun; no shield | New BOM item 19 (1.5 mm aluminum, 25 mm air gap, $30.00) in the model, STEP, STL, CTW-DWG-001 Rev P2 and media; cabinet 7.2 K over ambient in sun behind the shield, pack under 45 °C up to 37.8 °C air; R20 still not met |
| N5 R12 margin | Pilot range 0 to 35 °C air | 0 to 40 °C; panel 40.1 °C, pack 0.6 K margin; at risk | Panel 35.1 °C (4.9 K margin), pack 39.4 °C (5.6 K margin); met on paper |
| N6 hood light | Dim to about 0.3 W | 2 W, 1,459 lx; mains 10.2 W, 90 kWh a year | 0.3 W, 219 lx; mains 9.2 W, 81 kWh a year |

Knock-on figures: the sun shield adds 1.86 kg and 35 N of gust load, so post stress rises from 26.2 to 26.9 MPa, anchor tension from 1.92 to 1.97 kN and mass from 58.2 to 60.1 kg; all still met. The outdoor kiosk with the shield costs $769.00, $19.00 over `budget_usd`; R16 is set on the sheltered pilot kiosk. The pitch and problem lines were not reworded because no rewording was recommended.

Files changed: `project.yaml` (`budget_usd`), `README.md` (budget line, concept numbers, components, BOM line, safety, "What sparked the idea"), `docs/01-problem.md` (v0.4), `docs/02-concept.md` (v0.4), `docs/03-requirements.md` (v0.4), `docs/04-calcs/01-sizing.md` (CTW-CAL-001 v0.2), `docs/04-calcs/sizing.py` and `results.csv`, `docs/decisions/0001-trl2-review-decisions.md` (v0.2), new `docs/decisions/0002-recommendations-accepted.md`, `bom/bom.csv` (19 lines) and `bom/bom-notes.md`, `cad/src/model.py`, `cad/step/`, `cad/stl/`, `cad/src/sheets.py` and `cad/drawings/CTW-DWG-001` (Rev P2), `cad/src/concept_media.py` and all of `media/`, and the PDFs in `docs/pdf/`. All generated files were rebuilt, so none still shows the old site address.

"What sparked the idea" in `README.md` no longer describes how the portfolio was assembled. It now traces the idea to Amsterdam's mandatory register of sensors in public space (in force December 2021), cited to Cities Today and the city's register.

### Requirement status (CTW-CAL-001 v0.2)

2 not met, 1 at risk, 10 met on paper, 7 met by design (before: 4 not met, 2 at risk, 7 met on paper, 7 met by design).

| ID | Status | Key number |
| --- | --- | --- |
| R18 Outage ride-through | **Not met** (worst case) | 1.63 h aged at 0 °C against 2 h; needs a pack of at least 1.84 Ah from TwinKit |
| R20 Street climate | **Not met** | Panel about 79 °C in low sun and 45.1 °C shaded at 45 °C air; pack 52.2 °C at 45 °C behind the sun shield; heater 13.5 W at -20 °C |
| R1 Ingest every type | At risk | PotholeLog and DockHub pull formats not agreed; CrossSafe has no LoRaWAN uplink |
| R2, R8 to R13, R15 to R17 | Met on paper | 0.61 % lost; 25.9 min data age; 219 lx; LED ring 30 ms and layer 19.8 s; panel 35.1 °C at 35 °C; 26.9 MPa; 9.2 W; $739.00 against $750 |
| R3 to R7, R14, R19 | Met by design | |

### Still awaiting Amish

1. **O1, first partner city or neighborhood** for co-design and a pilot site. No recommendation was made. Proposed, awaiting Amish. This also decides whether the frost heater is fitted (N4).
2. Open questions without a recommendation, kept in CTW-PRC-001: antenna height for the reference neighborhood with the gateway in the cabinet, and the kiosk's languages and fault reporting (for co-design with the O1 partner).

### Cross-repo actions

- **TwinKit:** fit a backup pack of at least 1.84 Ah (now 1.5 Ah) for cabinet installs, so R18 is met with an aged pack at 0 °C (N3). TwinKit's review also asked for a street cabinet thermal check: this note gives 4.4 K rise in shade, 18.7 K in sun, 7.2 K in sun behind CityTwin's sun shield. TwinKit not edited.
- **PotholeLog:** agree the published daily segment file format and host that the CityTwin gateway pulls by outbound HTTPS (D11). Not edited.
- **DockHub:** agree per-dock hourly aggregates published by its back end for the CityTwin pull (D11). Not edited.
- **CrossSafe:** define a LoRaWAN uplink (hourly summary assumed here) so CityTwin's CrossSafe layer has an interface (R1). Not edited.
- **LoadZone and TwinKit:** class C downlink support on TwinKit's network server for LoadZone's sign, as noted in the TRL 3 session. Not edited.

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl: 3` and `trl_target: 3` are unchanged. Decided but on hold because they are TRL 4 work: fitting and testing the frost heater, building the indoor LCD and solar variants, and every bench build, button timing, climate chamber, backup and outage test. No build, test, purchasing, PCB or firmware material was created.

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

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (now **decided by Amish, 2026-09-25: go with recommendation**, see CTW-DDR-002): D1 budget option (b), the budget covers the kiosk and the gateway is costed in TwinKit (R17 redefined; `budget_usd` unchanged at $600, $750 recorded as awaiting Amish); D2 color e-paper with an indoor LCD variant; D3 sheltered or indoor pilot and a heater study at TRL 3 (R12 redefined to the pilot, R20 added); D4 gateway in the kiosk cabinet; D5 mains power with a solar head-only variant; D6 small-count threshold 5 per hour and two years of raw data; D7 CC BY 4.0; D8 buttons; D9 the 46-node reference neighborhood with the sibling TRL 3 rates; D10 one-way publishing and privacy rules at the gateway. No reworded pitch or problem line was recommended, so `project.yaml` and `README.md` keep the existing wording.

### Still awaiting Amish

Status update: items 2 to 7 and the hood light suggestion below are now decided by Amish, 2026-09-25: go with recommendation (session "recommendations accepted" above). Item 1 stays Proposed, awaiting Amish.

1. **O1, first partner city or neighborhood** for co-design and a pilot site. No recommendation was made.
2. **Budget figure.** `budget_usd` stays $600; $750 is recommended (D1). The kiosk at $739.00 fits $750. **Decided by Amish, 2026-09-25: go with recommendation** (CTW-DDR-002).
3. **New, D11 pull paths.** The gateway fetches PotholeLog's published segment files and DockHub's hourly aggregates by outbound HTTPS. Recommendation: adopt, and agree formats with both repos. Used for sizing; not agreed. **Decided by Amish, 2026-09-25: go with recommendation** (CTW-DDR-002).
4. **New, R10.** Options: (a) restate R10 as "press acknowledged within 0.5 s by the LED ring and a first on-screen cue; layer shown within 25 s"; (b) keep 5 s and fit an LCD in the indoor variant only; (c) a smaller monochrome status panel for instant feedback. Recommendation: (a) for the street kiosk and (b) indoors. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (CTW-DDR-002).
5. **New, R18.** Options: (a) restate R18 at 1.5 h; (b) ask TwinKit for a larger pack in cabinet installs; (c) keep 2 h and accept not met. Recommendation: (b), since winter cold in a street cabinet shortens the runtime further. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (CTW-DDR-002).
6. **New, R20 and the cabinet.** Options for a street kiosk: a heated, insulated panel bay (13.5 W at -20 °C, not costed), a north-facing or shaded screen, a ventilated sun shield on the cabinet, or a wider-range panel if one exists. Recommendation: a sun shield on the cabinet and a shaded screen orientation as site rules for any outdoor pilot; a heater only if the partner city has frost. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (CTW-DDR-002).
7. **New, R12 margin.** At 40 °C air the panel and pack have no margin. Recommendation: define the pilot range as 0 to 35 °C air. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (CTW-DDR-002).

Suggestion only, not in the repo: dim the hood light to about 0.3 W (200 lx is enough), which would cut 0.9 W from the average. **Decided by Amish, 2026-09-25: go with recommendation** (CTW-DDR-002).

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

Status update: items 1 to 9 are decided by Amish, 2026-09-25: go with recommendation (CTW-DDR-001 v0.2 D1 to D9, CTW-DDR-002). Item 10 had no recommendation and stays Proposed, awaiting Amish. Item 6 carried proposed values (5 per hour, two years), which are the decision.

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

## Session 2026-09-26: photoreal renders

Amish asked on 2026-09-26 for photoreal renders across the portfolio, starting with the software and playbook repos (Group C). This repo has no new product model: the existing concept scene from `cad/src/concept_media.py` was rendered with Blender Cycles (`.kit/scene_export.py`, `.kit/photoreal.py`) on Amish's Mac and captioned with the project, repository and viewing direction.

- New: `media/render-hero.png`, `media/render-detail.png`. The README now leads with `media/render-hero.png`.
- Geometry, BOM, calculations and drawings are unchanged. `trl` stays 3; TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation written for each open decision in the design decisions register (CTW-DEC-001 v0.2). trl stays 3; no build or test work was done, and the model, BOM quantities and prices, and pictures are unchanged.

### Decisions recorded

Seven decisions, all moved to Decisions made in CTW-DEC-001, dated 2026-10-02:

1. Sun shield standoff holes: option (a), drilled only in cabinets that get the shield (CTW-DDR-003, A2 accepted).
2. First partner and pilot site: a city within easy reach of Irving, Texas, with an active open-data program, as the first candidate to approach; the kiosk in a sheltered public lobby such as a library or transit center; no frost heater.
3. Antenna: post-top at 2.38 m for the pilot, with a coverage walk test at TRL 4; a rooftop gateway rather than a taller mast if nodes fall short.
4. Languages: English plus the partner city's most widely spoken other language in its own script, with a QR code and a phone or text number on the notice plate; refined in co-design.
5. Street climate (R20): kept as a post-pilot target; outdoor sites only in permanent shade with the sun shield; a panel rated above 40 °C sought at TRL 4; the heated bay only for a frost city.
6. Pull paths: daily CSV files on a fixed HTTPS address at each operator, with a published column list and a version field; the same format to be agreed in PotholeLog.
7. CrossSafe: ask for an hourly LoRaWAN summary uplink from one side of the crossing; no CrossSafe layer until it exists.

### Documents changed

- `docs/06-design-decisions.md` (CTW-DEC-001 v0.3): open decisions moved to Decisions made; the value-engineering line notes the sheltered pilot.
- `docs/decisions/0003-design-for-construction.md` (CTW-DDR-003 v0.3, status Draft): A2 accepted. The Table 1 changes (P1 to P14) were not an open decision in the register and so stayed open for Amish's review; he accepted them later on 2026-10-02 (see the next session).
- `docs/decisions/0001-trl2-review-decisions.md` (CTW-DDR-001 v0.3): O1 recorded as decided.
- `docs/decisions/0002-recommendations-accepted.md` (CTW-DDR-002 v0.2): O1, Q1 and Q2 recorded as decided.
- `docs/02-concept.md` (CTW-PRC-001 v0.7): outdoor site rule (permanent shade) and the open questions answered.
- `docs/01-problem.md` (CTW-PRB-001 v0.6): partner question answered.
- `docs/03-requirements.md` (CTW-REQ-001 v0.7): outdoor sites only in permanent shade (R20 status unchanged, not met, target after the pilot).
- `bom/bom-notes.md`: heater note (sheltered pilot).

### Follow-up actions to carry approved decisions into the design

1. Decision 1 (model and drawings): show the shield standoff holes only on the shielded variant in `cad/src/model.py`, drawing CTW-DWG-001 and the build plan pictures (section 3.3), if they are now shown on every cabinet.
2. Decision 4 (drawings and pictures): lay out the notice plate with the two languages, the QR code and the phone or text number, and update the build plan picture of the plate.
3. Decision 5 (calculations): add the permanent-shade site rule to the R20 discussion in CTW-CAL-001 when it is next run.
4. Decision 6 (docs): publish the CSV column list and version field, and agree it with PotholeLog's open item 6 (cross-repo action).
5. Decision 7 (docs): raise the hourly LoRaWAN summary uplink as a cross-repo action in CrossSafe.

### Points found in the review

- The register listed CTW-DDR-003 under Decisions made (2026-10-01) while also calling it open for Amish's review, and there was no open item to accept it. Amish accepted it later on 2026-10-02 (see the next session).
- Decision 6 is the same interface as PotholeLog's open item 6; decide both together.
- `media/render-hero.png` is missing from this copy, and the remaining renders show the concept head, hood and shield.

## Session 2026-10-02: design-for-construction changes accepted

Amish, 2026-10-02: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)". This accepts the design-for-construction changes P1 to P14 in Table 1 of CTW-DDR-003, which were left open for his review when the open decisions were decided earlier the same day. No other item is decided by it. trl stays 3; no build or test work was done, and the model, BOM, calculations and pictures are unchanged.

### Documents changed

- `docs/decisions/0003-design-for-construction.md` (CTW-DDR-003 v0.4, status Draft): status line now "accepted" with Amish's words.
- `docs/06-design-decisions.md` (CTW-DEC-001 v0.4): Decisions made row added, dated 2026-10-02; the 2026-10-01 row no longer calls the changes open for review.
- `docs/05-build-plan.md` (CTW-BLD-001 v0.2): section 2 says CTW-DDR-003 is accepted.
- `docs/03-requirements.md` (CTW-REQ-001 v0.8): CTW-DDR-003 noted as accepted.
- `README.md` (not a controlled document): build plan paragraph says CTW-DDR-003 is accepted.
- PDFs regenerated.

### Recommended next step

No change: the follow-up actions of the previous session stand. TRL 4 remains on hold by Amish's instruction.

## Session 2026-10-02: approved follow-ups carried out

Amish approved on 2026-10-02 that every follow-up action from the open-decision sign-off be carried out. trl stays 3; nothing was built or tested.

### Follow-ups

1. Decision 1, model and drawings: done. The shield standoff holes are now cut in the cabinet only when the sun shield is fitted (`cad/src/model.py`, `shield` option); a new check confirms that the pilot cabinet has none. 245 constructability checks pass. General arrangement CTW-DWG-001 is Rev P5 and says the side holes are drilled only on outdoor sites; the build plan text for the cabinet says the sheltered pilot cabinet gets no side holes.
2. Decision 4, notice plate: done. New layout picture (`docs/05-build-plan/notice-plate.png`, Figure 19a): English, the partner city's second language in its own script, a 50 mm QR code and a phone or text number. Making sketch CTW-DWG-106 and BOM line 8 updated; the price stays $15.00 (sign-maker set-up time only, an estimate).
3. Decision 5, calculations: done. The permanent-shade rule is in the R20 discussion of CTW-CAL-001 (section F) and in the `sizing.py` R20 row; `results.csv` rerun. No number changed.
4. Decision 6, CSV column list: done here (version 1 column list and version field in CTW-PRC-001, step 5); the agreement with PotholeLog is a cross-repo action.
5. Decision 7, CrossSafe uplink: cross-repo action only.

### Requirement status changes

None. R20 stays not met (a post-pilot target for outdoor sites in permanent shade). Cost and mass are unchanged: pilot kiosk USD 778 against the USD 750 target (USD 28 over), 808 with the sun shield.

### Pictures regenerated

General arrangement CTW-DWG-001 (Rev P5), making sketch CTW-DWG-106, new notice plate layout. The model geometry of the shielded kiosk did not change, so the concept media, overview, joints and steps were not redrawn.

### Appearance model and render scene

CityTwin has no `cad/src/product_model.py` and the hero stays a scene render (the 2026-09-26 approach): the scene is built by `cad/src/concept_media.py` from `cad/src/model.py`, so it follows the model. It was exported with `.kit/scene_export.py` to `/home/claude/renders/citytwin/citytwin__hero.npz` and `.json`, with `citytwin__jobs.json`. `.kit/export_views.py` is not used because there is no product model. Photoreal images, `media/card.png` and `media/social-preview.png` are made on Amish's Mac.

### Cross-repo actions

- PotholeLog: agree the version 1 pull-path column list (CTW-PRC-001, step 5) with its open item 6; DockHub to use the same list for its hourly aggregates.
- CrossSafe: ask for an hourly LoRaWAN summary uplink from one side of the crossing; CityTwin shows no CrossSafe layer until it exists.

### Documents changed

CTW-CAL-001 v0.5, CTW-PRC-001 v0.8, CTW-BLD-001 v0.3, CTW-DDR-003 v0.5, CTW-DWG-001 Rev P5, CTW-DWG-106, `bom/bom.csv`, `bom/bom-notes.md`. PDFs re-rendered.

### Recommended next step

Make the photoreal renders on the Mac. TRL 4 remains on hold by Amish's instruction.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
