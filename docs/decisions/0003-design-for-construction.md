---
doc_id: CTW-DDR-003
title: CityTwin design for construction
project: CityTwin
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the kiosk physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target, with cost question A1 replaced by the register's Value engineering section
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are Proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated build plan that shows how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of CTW-DDR-002 showed what the CityTwin kiosk does, where its parts sit and how big they are, but it was a massing model: the head, cabinet and hood touched the post with nothing holding them, the head was a sealed box with no way in, the screen and controller floated in the head, and several cable and conduit routes ran into solid walls.

Checking the model with build123d (intersections, volumes and distances between every pair of parts) found 14 problems, P1 to P14 below. The fixes keep what the kiosk does: the same post, base plate, head, window, screen position, buttons, notice plate, hood, cabinet, rails, gateway layout, antenna height and sun shield, the same mains and 12 V split, and the same sheltered pilot and outdoor site rules. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 244 constructability checks (`python cad/src/model.py --check`): no two parts overlap, the 50 pairs that must touch do touch, and the 10 pairs that must stay apart keep their gap. All 244 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The head and the cabinet touched the post with no fixing. The post is a closed 100 mm tube, so nothing can be reached inside it to hold a nut. | Eight M8 steel flush rivet nuts set in countersunk 11 mm holes in the post: four in the front wall (head, at 1,100 and 1,660 mm) and four in the back wall (cabinet, at 360 and 700 mm), 25 mm each side of the center line. The head and the cabinet are each held by four M8 button-head screws with 30 mm washers, put in from inside. | Rivet nuts are set from outside a closed tube; flush heads keep the head and cabinet flat on the post. Holes are drilled before galvanizing and the nuts set after coating, so the threads stay clean. The 30 mm washers spread the load on the 2 mm aluminum tray. |
| P2 | The display head was a closed 2 mm aluminum box: there was no way to fit or service anything inside it, and no way to make it as one folded part. | The head is now a folded tray (back, top, bottom, sides, 98 mm deep) with a 15 mm return flange round its front, closed by a separate 2 mm front panel on twelve M4 tamper-resistant screws into rivet nuts in the flange, with a gasket strip. Outside size unchanged at 460 x 100 x 680 mm. | A sheet metal shop can fold the tray; the front panel comes off for service and the screws resist tampering, as BOM item 3 already asked. |
| P3 | The window sat inside the front wall with no fixing. | The window is bonded inside the front panel with 1 mm acrylic glazing tape on its 8 mm lap. | The common way to glaze a kiosk; it also seals the window edge. |
| P4 | The e-paper panel floated 1 mm behind the window, and the controller floated on a block near the back wall. | New BOM item 20, a 2 mm aluminum display carrier, sits on 15 mm spacers over eight M4 clinch studs pressed into the front panel. It presses the e-paper panel onto a 1 mm foam gasket on the window and carries the driver board and the controller on M2.5 standoffs. | One plate holds the fragile glass panel evenly and keeps the electronics with the screen, so the whole display lifts out with the front panel. |
| P5 | The head had only a 12 V feed, but the controller needs 5 V, the button rings and the dimmed hood light need switching, and nothing let the front panel unplug. | BOM item 6 now includes a 12 V to 5 V converter, a 4-channel LED driver module and a pluggable 6-way terminal block with a 2 A fuse, all on the carrier. Item 6 rises from $42.00 to $55.00. | The controller rules of CTW-DDR-002 (LED ring on press, hood light dimmed to about 0.3 W) need these; the fuse protects the 12 V cable up the post. |
| P6 | Buttons were drawn as 24 mm cylinders in 24 mm holes. | 19.2 mm holes; each button's 24 mm bezel sits outside the panel and its own nut clamps it inside. | That is how a 19 mm vandal-resistant button mounts. |
| P7 | The notice plate had no fixing. | Four 4.5 mm holes and four M4 tamper-resistant screws with nyloc nuts inside the front panel. | Reachable once the front panel is off; tamper-resistant from the street. |
| P8 | The hood roof was a 14 mm solid block with no fixing, and the LED strip floated below it. | The hood is folded 1.5 mm sheet (roof, lip, cheeks) resting on the tray top, held by four M5 tamper-resistant screws into rivet nuts in the tray top. The LED strip sits on a 20 x 20 mm angle riveted under the roof behind the lip; its cable enters the head through a 13 mm grommet in the front panel, under the roof. | A real folded part with a real fixing. The head's leading edge drops from 1,734 to 1,722 mm, still inside the 685 to 2,030 mm zone. |
| P9 | DIN rails were drawn on the cabinet wall itself. | The rails sit on the cabinet's 340 x 390 mm mounting plate on 10 mm standoffs, as a stock cabinet supplies it. | Lets the cabinet screws go in first, then the plate; every device keeps at least 10 mm from the door. |
| P10 | The 16 x 60 mm cable slot in the post back met a solid cabinet wall, and there was no cable route from the post into the head. | A 25 mm hole through the post back wall and the cabinet wall at 735 mm (above the mounting plate), and a 25 mm hole through the post front wall and the tray back at 1,380 mm, each with rubber grommets. The 12 V cable, Ethernet and coax run up inside the post. | Round holes are simpler to make and seal than a slot; both routes stay inside the post, out of reach. |
| P11 | The mains conduit stopped on top of the base plate and on the cabinet floor with no holes. | A 40 mm hole in the base plate, 130 mm behind the post center, and a 32 mm conduit gland in the cabinet floor. | The feed comes up from the footing without passing through the post, keeping mains out of the post. |
| P12 | The anchors were fused to the base plate, and the post was a closed steel tube, which cannot safely be hot-dip galvanized. | 18 mm anchor holes, 34 mm washers and nuts; a 25 mm vent and drain hole in the base plate under the post; the cap's 20 mm coax hole vents the top. | Galvanizers need vent holes at both ends of a closed section; the bottom hole also drains condensation. |
| P13 | The antenna bracket was a solid 60 x 60 x 20 mm block. | A 60 x 60 x 6 mm aluminum plate with a 16.5 mm hole for the antenna's N-type bulkhead, held to the post cap by four M5 screws into tapped holes. The antenna base makes up the rest of the height, so the tip stays at 2.38 m. | A plate a small shop can make; the coax passes straight down into the post. |
| P14 | The sun shield's two hook tabs hooked onto nothing, and its "lift-off" back panel was one piece with the rest. | The shield (top and sides) sits on four 25 mm M6 standoffs bolted through the cabinet sides with sealing washers. A 15 mm flange folded inward at the back of each side carries a separate back panel, held by four M5 knurled thumb screws into rivet nuts. | The 25 mm air gap, open bottom and top vents are unchanged, so the thermal result stands. The back panel comes off by hand to reach the locked door. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| BOM | Lines 1 to 4, 6 to 10, 14, 15 and 19 respecified; line 6 repriced to $55.00; line 15 repriced to $26.00 (fixings moved out); new line 20 (display carrier, $8.00) and line 21 (fixings, tapes and gaskets, $22.00). 21 lines. | Parts added for construction. |
| Cost | Pilot kiosk $739.00 to $778.00 [J1], $28.00 over the $750 value-engineering target [J2]; outdoor kiosk $808.00; with the TwinKit gateway $1,068.00. R16 changes from met on paper to **over the value-engineering target by $28.00**. | See the Value engineering section of CTW-DEC-001. |
| Mass | 60.1 to 63.5 kg with the sun shield [H4]. Most of the rise is the cabinet's 2 mm steel mounting plate (2.1 kg), then the front panel and fixings. | Still a two-person or hoist lift. |
| Wind | The hood is now modeled as sheet, not a 14 mm block: 827 to 821 N, post stress 26.9 to 26.6 MPa, anchor tension 1.97 to 1.94 kN [H1, H2, H5]. R13 still met on paper. | Follows the model. |
| Thermal, power, radio, legibility | Unchanged. The window, screen gap, hood, cabinet and shield keep their sizes and positions. | |
| Drawing | CTW-DWG-001 Rev P4; making sketches CTW-DWG-101 to 111 added. | Follows the model. |
| Documents | CTW-CAL-001 v0.3, CTW-REQ-001 v0.5, CTW-PRC-001 v0.5 updated for cost, mass and wind. New CTW-BLD-001 and CTW-DEC-001. | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A2 | The sun shield standoff holes breach the cabinet's sides. | (a) drill them only on kiosks that get the shield; (b) drill every cabinet so a pilot kiosk can later move outdoors, with sealed blanking screws until then. | (a), so the sheltered pilot cabinet keeps its unbroken IP55 sides. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CTW-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open items are in the design decisions register CTW-DEC-001.
- Requirement status (CTW-CAL-001 v0.3): 2 not met (R18, R20), 1 over the value-engineering target (R16), 1 at risk (R1), 9 met on paper, 7 met by design. Before: 2 not met, 1 at risk, 10 met on paper, 7 met by design.
- The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` are made on Amish's Mac and still show the concept head and shield; they are stale where the shield back panel and standoffs, the hood's sheet edges and the front panel screws show. The concept media in `media/` were regenerated from the new model.
- The cabinet, its mounting plate, the e-paper panel's outline and cable exit, and the rivet nuts' grip range are bought parts to be confirmed when chosen at TRL 4 (CTW-DEC-001).
