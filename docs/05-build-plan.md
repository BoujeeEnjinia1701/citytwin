---
doc_id: CTW-BLD-001
title: CityTwin prototype build plan
project: CityTwin
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (CTW-DDR-003)
---

# CityTwin prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype of the CityTwin kiosk, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order; 20 and 21, the sun shield and its back panel, are fitted on outdoor sites only.*

The prototype is the physical part of CityTwin: a public kiosk about 2.4 m tall to the antenna tip. A 100 mm square steel post, welded to a base plate, stands on four anchors. On its street side it carries a folded aluminum display head with a 13.3 in color e-paper screen behind a polycarbonate window, three push buttons, a data notice plate and a hood with a night light. On its back it carries a locked steel cabinet holding the mains protection, a 12 V supply and the TwinKit gateway that runs the CityTwin software, with an antenna on the post top. Figure 1 shows the 21 components in the order you make or fit them. Ten are made: the base plate and post (one welded, galvanized part from a steel fabricator), the head tray, front panel, display carrier, hood, notice plate and antenna bracket (from a sheet metal shop and a sign maker), and the sun shield and its back panel for outdoor sites; the bought cabinet is drilled. Everything else is bought and fitted: the window, e-paper panel, controller and small modules, buttons, DIN rail devices, the TwinKit gateway, conduit, cables and fixings. The work in your own workshop is drilling, setting rivet nuts, bonding the window, fitting boards and low-voltage wiring; the mains wiring is done by a qualified electrician. The parts for the sheltered pilot kiosk cost about $778 from the bill of materials.

> **Safety:** The cabinet carries mains voltage (230 V or 120 V). Only a qualified electrician installs or checks the mains feed, the RCBO, the surge protector and the earthing, to local electrical code. The TwinKit gateway holds a lithium iron phosphate backup pack: keep its fuse out until safety stop S4. The kiosk weighs about 64 kg; lift the post with two people or a hoist. Cut steel and aluminum edges are sharp: deburr everything, and round every corner at head height.

## 2. What changed to make it buildable

The concept showed what the kiosk does; many of its parts touched with nothing holding them, and the head was a sealed box. Each change below keeps what the kiosk does, and all of them are recorded in decision record CTW-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Post | A closed tube touched by the head and cabinet, with no fixing | Eight M8 flush rivet nuts set in the post walls; the head and cabinet are each held by four M8 screws from inside (Figures 7 and 10) | A nut can be set in a closed tube from outside |
| Base plate and post | Anchors fused to the plate; a sealed tube | 18 mm anchor holes, washers and nuts; a 25 mm vent and drain hole under the post; a 40 mm conduit hole (Figure 3) | A closed tube cannot be safely galvanized; the mains feed needs a way in |
| Display head | A sealed 2 mm box with no way in | A folded tray with a return flange, closed by a removable front panel on twelve tamper-resistant screws (Figure 17) | It can be made by folding, and opened for service |
| Window and screen | Floating in the head | Window bonded inside the front panel with glazing tape; the screen pressed onto it by a new display carrier on eight studs (Figure 21) | The glass panel is held evenly and lifts out with the front panel |
| Head electronics | A 12 V feed only | A 5 V converter, an LED driver and a pluggable, fused terminal block on the carrier (Figure 22) | The controller needs 5 V; the button rings and hood light need switching; the front panel must unplug |
| Buttons and notice plate | 24 mm holes; no fixing for the plate | 19.2 mm holes with each button's own nut; four tamper-resistant screws for the plate (Figure 18) | How these parts really mount |
| Hood | A solid 14 mm block with no fixing | Folded 1.5 mm sheet on four screws into rivet nuts in the head top; the LED strip on an angle behind the lip (Figure 12) | A real folded part with a real fixing |
| Cabinet | Rails drawn on the wall; a cable slot that met a solid wall | Rails on the cabinet's mounting plate; 25 mm grommeted cable holes through the post and cabinet, and through the post and head; a conduit gland in the floor (Figure 8) | Cables stay inside the post; mains stays in the cabinet |
| Antenna bracket | A solid block | A 6 mm plate screwed to the post cap, with the antenna's bulkhead through it (Figure 14) | A plate a small shop can make |
| Sun shield | Hook tabs that hooked onto nothing; a one-piece "lift-off" back | Four 25 mm standoffs on the cabinet sides; a separate back panel on four thumb screws (Figure 24) | A fixing that holds the 25 mm air gap and comes off by hand |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimeters. Heights are from the sidewalk unless a step says "from the bottom edge". "Front" is the street side, where the screen faces; "left" and "right" are as seen standing in front of the kiosk. Workshop tolerance is 0.5 mm on holes and 1 mm on sheet sizes unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Base plate

![Figure 2. Making sketch of the base plate](../cad/drawings/CTW-DWG-101.png)

*Figure 2. Base plate making sketch (CTW-DWG-101).*

**What it is and what it is made from.** The square steel plate the post is welded to; it bolts to the footing. Steel plate 12 mm thick, S275 or S355 class, 400 x 400 mm. The base plate and the post are made as one welded part by a steel fabricator.

**How to make it.**

1. Cut the blank to 400 x 400 mm and round the corners to about 10 mm.
2. Mark the center and two center lines. The side toward the cabinet is the back.
3. Drill four 18 mm anchor holes on a 300 mm square: 150 mm each way from the center.
4. Drill a 25 mm hole at the center. It sits under the post: the galvanizer needs it to vent the tube, and it lets condensation drain.
5. Drill a 40 mm hole on the center line, 130 mm behind the center, for the mains conduit.
6. Deburr every hole.

**How it fits the parts next to it.**

![Figure 3. Joint 1: post foot, base plate and anchors](05-build-plan/joint-01.png)

*Figure 3. The post stands on the plate's center with a 4 mm fillet weld all round; the drain hole is inside the post; the conduit rises through its own hole behind the post.*

The post is welded square on the plate before galvanizing (section 3.2). The plate sits on the footing on steel shims or a grout bed. Each anchor passes up through its 18 mm hole and takes a 34 mm washer and a nut on top of the plate.

**Check before moving on.** The anchor holes are 300 mm apart both ways, measured center to center, and the post stands square to the plate within 1 mm over its height.

### 3.2 Post

![Figure 4. Making sketch of the post](../cad/drawings/CTW-DWG-102.png)

*Figure 4. Post making sketch (CTW-DWG-102), drawn lying down.*

![Figure 5. Holes in the post's front and back walls](05-build-plan/post-holes.png)

*Figure 5. Every hole in the front wall (head side) and back wall (cabinet side), with heights from the sidewalk.*

**What it is and what it is made from.** The 1.75 m column that carries the head, the hood, the cabinet and the antenna, and carries the low-voltage cables inside it. Square hollow steel section 100 x 100 x 4 mm, with a 6 mm steel cap plate on top.

**How to make it.**

1. Cut the tube 1,742 mm long with square ends. With the 12 mm base plate under it and the 6 mm cap on it, the top is 1,760 mm up.
2. Cap plate: 100 x 100 x 6 mm, with a 20 mm hole at the center for the antenna cable and four M5 tapped holes 20 mm each way from the center for the antenna bracket.
3. Front wall (street side), as Figure 5: four 11 mm holes 25 mm each side of the center line, at 1,100 and 1,660 mm up; one 25 mm cable hole on the center line at 1,380 mm up.
4. Back wall (cabinet side): four 11 mm holes 25 mm each side of the center line, at 360 and 700 mm up; one 25 mm cable hole on the center line at 735 mm up.
5. Countersink the eight 11 mm holes 90 degrees so the flush rivet nuts sit level with the wall.
6. Weld the cap on top and weld the tube to the base plate (section 3.1).
7. Send the welded part for hot-dip galvanizing, then powder coating.
8. After coating, set eight M8 flush steel rivet nuts in the 11 mm holes with a rivet nut tool, clean the threads and deburr the two cable holes.

**How it fits the parts next to it.** The head tray's back sits flat on the front wall, held by four M8 screws into the front rivet nuts (Figure 10). The cabinet's back wall sits flat on the back wall, held by four M8 screws into the back rivet nuts (Figure 7). The two cable holes line up with matching holes in the cabinet and the head tray, each with a rubber grommet. The antenna bracket sits on the cap (Figure 14).

**Check before moving on.** An M8 screw runs into every rivet nut by hand; each rivet nut is flush with the wall and does not spin.

### 3.3 Services cabinet, drilled

![Figure 6. Drilling sketch of the services cabinet](../cad/drawings/CTW-DWG-109.png)

*Figure 6. Services cabinet drilling sketch (CTW-DWG-109).*

**What it is and what it is made from.** A bought, lockable steel electrical cabinet, 360 wide, 160 deep and 460 mm tall, rated IP55, with its door on the face away from the post and a removable mounting plate inside. It holds every mains part and the TwinKit gateway.

**How to make it.**

1. Take out the mounting plate and protect the inside from swarf.
2. On the wall that goes against the post, with heights from the cabinet's bottom edge: four 9 mm holes 25 mm each side of the center line at 60 and 400 mm up, and a 25 mm cable hole on the center line at 435 mm up, above the mounting plate.
3. In the floor: a 32.5 mm hole on the center line at mid-depth for the conduit gland.
4. Outdoor sites only: two 6.5 mm holes in each side wall at mid-depth, 120 and 380 mm up, for the sun shield standoffs.
5. Deburr and touch up the paint on every cut edge.

**How it fits the parts next to it.**

![Figure 7. Joint 2: cabinet on the post](05-build-plan/joint-02.png)

*Figure 7. The cabinet's back wall sits flat on the post; an M8 screw with a 30 mm washer goes in from inside the cabinet into the flush rivet nut. The mounting plate goes in after the screws.*

The cabinet is 300 mm above the sidewalk, centered on the post. Four M8 button-head screws with 30 mm washers go in from inside the cabinet. The mounting plate then goes back on its four studs, 10 mm off the back wall, clear of the screw heads. The cable hole lines up with the post's 25 mm hole at 735 mm, with a grommet each side.

![Figure 8. Joint 10: inside the cabinet, cable routes](05-build-plan/joint-10.png)

*Figure 8. The mains feed enters through the conduit gland in the floor and stays in the cabinet; the 12 V cable, Ethernet cable and antenna cable leave through the grommet into the post.*

**Check before moving on.** Held on the post, every 9 mm hole lines up with a rivet nut and the cable holes line up.

### 3.4 Head tray

![Figure 9. Making sketch of the head tray](../cad/drawings/CTW-DWG-103.png)

*Figure 9. Head tray making sketch (CTW-DWG-103).*

**What it is and what it is made from.** The body of the display head: a box 460 wide, 680 tall and 98 mm deep, open at the front, which the front panel closes. Aluminum sheet 2 mm, 5052 class, folded by a sheet metal shop.

**How to make it.**

1. Fold the back, top, bottom and two sides from one blank, and weld or rivet and seal the four corners.
2. Fold a 15 mm return flange inward all round the open front.
3. Back wall, with heights from the bottom edge: four 9 mm holes 25 mm each side of the center line at 60 and 620 mm up; a 25 mm cable hole on the center line at 340 mm up.
4. Bottom: six vent slots 30 x 70 mm, 60 mm apart; glue stainless insect mesh inside them.
5. Top: four 7 mm holes 150 mm each side of the center line, 30 and 70 mm behind the front panel line; set M5 aluminum rivet nuts in them for the hood.
6. Flange: twelve 6 mm holes, three along the top, three along the bottom and three down each side, matching the front panel (Figure 16); set M4 aluminum rivet nuts in them.
7. Powder coat.

**How it fits the parts next to it.**

![Figure 10. Joint 3: head tray on the post](05-build-plan/joint-03.png)

*Figure 10. The tray's back wall sits flat on the post's front wall; an M8 screw with a 30 mm washer goes in from inside the tray into the flush rivet nut.*

The tray's bottom edge is 1,040 mm up and its top 1,720 mm up, centered on the post. The four screws go in from inside, before the front panel is fitted. The 30 mm washers spread the load on the 2 mm wall.

**Check before moving on.** The flange is flat within 1 mm so the gasket seals, and all twelve rivet nuts take an M4 screw by hand.

### 3.5 Hood

![Figure 11. Making sketch of the hood](../cad/drawings/CTW-DWG-107.png)

*Figure 11. Hood making sketch (CTW-DWG-107).*

**What it is and what it is made from.** The roof that shades the screen by day and hides the night light. Aluminum sheet 1.5 mm, 5052 class, and a 300 mm length of 20 x 20 x 1.5 mm aluminum angle.

**How to make it.**

1. Cut one blank and fold a roof 500 wide and 240 mm deep, a 60 mm lip down along the front edge, and two side cheeks 120 mm deep and 90 mm long. Notch the corners before folding and seal them after.
2. Drill four 5.5 mm holes in the roof, 150 mm each side of the center line, 30 and 70 mm in front of the back edge.
3. Round every exposed corner to at least 10 mm: the hood is at head height.
4. Rivet the angle under the roof, 20 mm behind the lip, with one leg hanging down and facing the screen. Stick the LED strip on that leg.
5. Powder coat before fitting the angle and strip.

**How it fits the parts next to it.**

![Figure 12. Joint 6: hood on the head top](05-build-plan/joint-06.png)

*Figure 12. The roof sits on the tray top with its back edge against the post; M5 tamper-resistant screws go into the rivet nuts in the tray top. The lip hides the LED strip from the sidewalk.*

The roof reaches 140 mm in front of the head and 20 mm past it at each side. Run a bead of sealant under the roof's back edge before fitting. The LED cable runs back under the roof and into the head through a 13 mm grommet in the front panel, above the window.

**Check before moving on.** Standing 1.5 m in front of the kiosk, the LED strip cannot be seen.

### 3.6 Antenna bracket

![Figure 13. Making sketch of the antenna bracket](../cad/drawings/CTW-DWG-108.png)

*Figure 13. Antenna bracket making sketch (CTW-DWG-108).*

**What it is and what it is made from.** A small plate that holds the TwinKit antenna on the post top. Aluminum plate 6 mm, 6082 class, 60 x 60 mm.

**How to make it.**

1. Cut 60 x 60 mm and round the corners to 3 mm.
2. Drill a 16.5 mm hole at the center for the antenna's N-type bulkhead.
3. Drill four 5.5 mm holes 20 mm each way from the center, matching the tapped holes in the cap.

**How it fits the parts next to it.**

![Figure 14. Joint 8: antenna bracket on the post cap](05-build-plan/joint-08.png)

*Figure 14. The bracket sits on the cap with four M5 screws; the antenna's bulkhead passes through the bracket and the cap's 20 mm hole, with its nut underneath.*

The antenna cable is fed down inside the post to the cabinet before the bracket goes on. The antenna tip is 2.38 m up.

**Check before moving on.** The antenna stands vertical within 2 degrees.

### 3.7 Head front panel

![Figure 15. Making sketch of the head front panel](../cad/drawings/CTW-DWG-104.png)

*Figure 15. Head front panel making sketch (CTW-DWG-104).*

![Figure 16. Holes and cut-out in the front panel](05-build-plan/panel-holes.png)

*Figure 16. Every hole and the window opening, seen from the front, measured up from the bottom edge and sideways from the center line.*

**What it is and what it is made from.** The removable face of the head that carries the window, the screen, the buttons and the notice plate. Aluminum sheet 2 mm, 5052 class, 460 x 680 mm, powder coated.

**How to make it.**

1. Cut the blank to 460 x 680 mm and mark the center line and the bottom edge.
2. Cut the window opening 240 wide and 320 mm tall, centered, from 260 to 580 mm up.
3. Drill three 19.2 mm button holes 80 mm up: one on the center line and one 70 mm each side.
4. Drill four 4.5 mm notice plate holes, 190 mm each side of the center line, at 137 and 213 mm up.
5. Drill twelve 4.5 mm screw holes 7.5 mm in from the edge, matching the tray flange (Figure 16).
6. Drill a 13 mm hole 140 mm right of the center line, 645 mm up, for the LED cable grommet.
7. Press eight M4 x 25 mm clinch studs in from the back: 138 mm each side of the center line and on it, at 242, 420 and 598 mm up.
8. Powder coat, masking the stud threads and the 8 mm band round the opening where the glazing tape goes.

**How it fits the parts next to it.**

![Figure 17. Joint 5: front panel on the tray flange](05-build-plan/joint-05.png)

*Figure 17. The panel sits on the tray's flange with a gasket strip between them; a tamper-resistant M4 screw goes through the panel into the rivet nut in the flange.*

![Figure 18. Joint 7: push button in the front panel](05-build-plan/joint-07.png)

*Figure 18. Each button's bezel sits on the outside of the panel and its own nut clamps it from inside. The notice plate lies flat on the outside above the buttons.*

The panel closes the tray's open front. The window and screen stack on its back (section 3.9), the buttons and notice plate on its front.

**Check before moving on.** Laid on the tray, all twelve holes line up with the rivet nuts.

### 3.8 Data notice plate

![Figure 19. Making sketch of the data notice plate](../cad/drawings/CTW-DWG-106.png)

*Figure 19. Data notice plate making sketch (CTW-DWG-106).*

**What it is and what it is made from.** The plate that tells a passer-by what is measured nearby, who is responsible, how long data is kept, and where to read more. Aluminum sheet 2 mm, 400 x 100 mm, printed or engraved by a sign maker.

**How to make it.**

1. Have the sign maker print or engrave the content: what is measured, who is responsible, how long data is kept, a QR code and a short web address for the sensor register, with icons in the style of the open DTPR standard.
2. Keep the QR code at least 25 mm square and clear of the holes.
3. Round the corners to 5 mm and drill four 4.5 mm holes, 10 mm in from each end and 12 mm in from the top and bottom edges.

**How it fits the parts next to it.** The plate lies flat on the front panel with its bottom edge 125 mm up, held by four M4 tamper-resistant screws with nyloc nuts inside the panel (Figure 18).

**Check before moving on.** The QR code scans from 1 m with a phone.

### 3.9 Display carrier, with the window and screen

![Figure 20. Making sketch of the display carrier](../cad/drawings/CTW-DWG-105.png)

*Figure 20. Display carrier making sketch (CTW-DWG-105).*

**What it is and what it is made from.** A flat plate on the front panel's studs that holds the e-paper panel against the window and carries the electronics of the head. Aluminum sheet 2 mm, 5052 class, 290 x 370 mm.

**How to make it.**

1. Cut 290 x 370 mm and round the corners to 5 mm.
2. Drill eight 4.5 mm holes on the stud positions: 138 mm each side of the center line and on it, at 7, 185 and 363 mm up from the bottom edge.
3. Cut a 70 x 8 mm slot on the center line, 49 to 57 mm below the top edge, for the e-paper panel's flat cable.
4. Lay the boards on the back face, as seen from behind with the slot at the top: the driver board just below the slot; the controller lower right; the 5 V converter and LED driver lower left; the terminal block at the bottom right. Mark their holes through the boards and drill 2.7 mm for M2.5 standoffs.

**How it fits the parts next to it.**

![Figure 21. Joint 4: window and screen stack at the top stud](05-build-plan/joint-04.png)

*Figure 21. From the street side: front panel, glazing tape, window, foam gasket, e-paper panel, carrier. The carrier sits on 15 mm spacers over the studs and its nuts press the panel onto the gasket.*

The window is 6 mm polycarbonate, 256 x 336 mm. It is bonded inside the front panel by a 1 mm acrylic glazing tape on its 8 mm lap round the opening. A 1 mm foam gasket strip runs round the e-paper panel's border, between the panel and the window, so the glass never touches the window directly. The 15 mm spacers set the stack: tape, window, gasket and panel add up to 15 mm, so the carrier just clamps the panel when the nuts are snug.

#### 3.9.1 Wiring

![Figure 22. Block-level wiring](05-build-plan/wiring.png)

*Figure 22. Block-level wiring with wire sizes. Mains (red) stays in the cabinet; only 12 V, data and the antenna cable go up the post.*

The low-voltage wiring in the head is yours to do; the mains wiring in the cabinet is the electrician's. Use stranded copper and a ferrule on every screw terminal.

1. Cabinet (electrician): mains feed through the conduit gland to the RCBO, then the surge protector, then the 12 V supply, in 1.5 mm² (16 AWG) wire; earth to the earth stud in 6 mm² (10 AWG).
2. Cabinet: 12 V supply output to the TwinKit gateway's fused terminals, 1.5 mm².
3. Up the post: one 2-core 1.0 mm² (18 AWG) cable from the 12 V supply to the head's terminal block; one outdoor Ethernet cable from the gateway to the controller; the antenna cable from the gateway's antenna socket to the antenna.
4. Head: terminal block (with its 2 A fuse) to the 5 V converter and the LED driver, 0.75 mm²; 5 V converter to the controller; driver board to the e-paper panel's flat cable.
5. Head: LED driver to the three button rings, 0.25 mm² (24 AWG), and to the hood LED strip, 0.5 mm² (20 AWG) through the front panel grommet; button switches and the dusk sensor to the controller's inputs.
6. Earth bonds from the cabinet's earth stud to the post, the head tray, the front panel and the hood, 4 mm² (12 AWG), by the electrician.

**Check before moving on.** With nothing powered, every wire continues end to end; the 12 V pair reads open between its cores; every wire is labelled; the cables to the front panel all pass through the pluggable terminal block, so the panel unplugs.

### 3.10 Sun shield (outdoor sites only)

![Figure 23. Making sketch of the sun shield](../cad/drawings/CTW-DWG-110.png)

*Figure 23. Sun shield making sketch (CTW-DWG-110).*

**What it is and what it is made from.** A light grey cover over the top and sides of the cabinet that keeps direct sun off it, fitted only on outdoor sites. Aluminum sheet 1.5 mm, 5052 class, powder coated light grey.

**How to make it.**

1. Fold a top 413 x 186 mm with two sides down 90 degrees, 486 mm high overall.
2. Fold a 15 mm flange inward along the back edge of each side, and rivet or weld the top corners.
3. Drill two 6.5 mm holes in each side at mid-depth, 120 and 380 mm up from the bottom edge.
4. Drill two 7 mm holes in each flange, 100 and 400 mm up, and set M5 rivet nuts in them.
5. Powder coat light grey.

**How it fits the parts next to it.**

![Figure 24. Joint 9: sun shield standoff](05-build-plan/joint-09.png)

*Figure 24. A 25 mm standoff is bolted through the cabinet side with a sealing washer under the bolt head inside; an M6 screw holds the shield side to it from outside.*

The shield stands 25 mm off the cabinet's top, sides and back, and is open at the bottom, so air rises through the gap.

**Check before moving on.** On a trial fit the gap is 25 mm, give or take 3 mm, all round.

### 3.11 Shield back panel (outdoor sites only)

![Figure 25. Making sketch of the shield back panel](../cad/drawings/CTW-DWG-111.png)

*Figure 25. Shield back panel making sketch (CTW-DWG-111).*

**What it is and what it is made from.** The removable part of the shield over the cabinet door. Aluminum sheet 1.5 mm, 5052 class, 413 x 485 mm, powder coated light grey.

**How to make it.**

1. Cut 413 x 485 mm and round the corners to 5 mm.
2. Cut four vent slots 60 x 15 mm, 20 mm apart, about 45 to 60 mm below the top edge.
3. Drill four 6.5 mm holes 197.5 mm each side of the center line, at 100 and 400 mm up.
4. Powder coat light grey.

**How it fits the parts next to it.** The panel lies on the shield's two back flanges, 25 mm behind the cabinet door, held by four M5 knurled thumb screws into the flange rivet nuts. Undo the thumb screws to reach the locked door.

**Check before moving on.** It comes off and goes back by hand in about a minute.

### 3.12 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Anchors (line 1).** Four M16 anchors with nuts and 34 mm washers, sized by the structural design of the footing; for the bench build, chemical anchors in a precast concrete block of about 700 x 700 x 300 mm.
- **Window (line 4).** 6 mm UV-stabilized, anti-glare polycarbonate cut to 256 x 336 mm, edges smooth.
- **E-paper display (line 5).** 13.3 in color E Ink Spectra 6 panel, 1600 x 1200 px, with its driver board; outline about 210 x 290 x 7 mm.
- **Controller and head modules (line 6).** Raspberry Pi Zero 2 W class board with an industrial microSD card, a USB Ethernet adapter and a real-time clock; a 12 V to 5 V, 3 A buck converter; a 4-channel low-side LED driver module; a pluggable 6-way terminal block with a 2 A fuse.
- **Push buttons (line 7).** Three 19 mm stainless vandal-resistant momentary buttons with LED rings, 24 mm bezel, IP65.
- **Hood light (line 9).** 12 V warm white LED strip of about 2 W, 300 mm long, and a dusk sensor.
- **Cabinet (line 10).** Lockable steel cabinet 360 x 160 x 460 mm, IP55, with a removable mounting plate on studs, two 320 mm TS35 DIN rails and an earth stud. Drill as section 3.3.
- **Mains protection (line 11).** A 6 A, 30 mA RCBO and a Type 2 surge protective device, two modules each.
- **12 V supply (line 12).** DIN rail supply, 60 W, 12 V certified SELV output, three modules.
- **TwinKit gateway (line 13).** Built from the TwinKit repository as its own drawing TWK-DWG-001 lays it out, with an antenna cable to the post-top antenna in place of its whip.
- **Antenna (line 14).** The TwinKit antenna with an N-type bulkhead base.
- **Conduit and cabling (line 15).** 32 mm conduit and a matching gland; 2-core 1.0 mm² outdoor cable; outdoor Ethernet cable; four rubber grommets for 25 mm holes in walls of 4 to 6 mm; earth bond leads.
- **Fixings, tapes and gaskets (line 21).** Stainless where outdoors: 8 M8 steel flush rivet nuts for a 4 mm wall; 8 M8 x 20 mm button-head screws with 30 mm washers; 16 M4 and 4 M5 aluminum rivet nuts; 12 M4 tamper-resistant screws (front panel); 4 M4 tamper-resistant screws with nyloc nuts (notice plate); 4 M5 tamper-resistant screws (hood); 4 M5 screws (antenna bracket); 8 M4 x 15 mm spacers and nuts; M2.5 standoffs; 1 mm acrylic glazing tape 8 mm wide; 1 mm foam gasket tape; EPDM gasket strip for the front panel flange; for outdoor sites, four M6 x 25 mm aluminum standoffs, M6 screws and bolts with sealing washers, and four M5 knurled thumb screws.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in color, with an arrow showing the way it goes in.

### Step 1: post onto the anchors

![Step 1](05-build-plan/step-01.png)

With two people or a hoist, lower the post and base plate over the anchors onto shims or a grout bed. Plumb the post with a level on two faces, then fit the washers and nuts and tighten them to the anchor maker's torque. **Hold point:** safety stop S1.

### Step 2: cabinet onto the post

![Step 2](05-build-plan/step-02.png)

Mounting plate out, door open. Hold the cabinet flat on the post's back wall, 300 mm up, and fit four M8 screws with 30 mm washers from inside into the rivet nuts. Tighten evenly.

### Step 3: mounting plate and rails into the cabinet

![Step 3](05-build-plan/step-03.png)

Fit the mounting plate with its two rails on its four studs and connect its earth lead to the earth stud.

### Step 4: mains protection and 12 V supply on the lower rail

![Step 4](05-build-plan/step-04.png)

Clip the RCBO, the surge protector and the 12 V supply onto the lower rail, in that order starting from the right as you face the open door. The electrician wires them (section 3.9.1, wire 1). **Hold point:** safety stop S2.

### Step 5: TwinKit gateway on the upper rail

![Step 5](05-build-plan/step-05.png)

Clip the gateway's parts onto the upper rail as TwinKit lays them out, with the backup pack's fuse out; it goes in only at safety stop S4. Connect the 12 V supply to its fused terminals.

### Step 6: conduit, gland and grommets

![Step 6](05-build-plan/step-06.png)

Fit the conduit gland in the cabinet floor and bring the conduit up through the base plate into it. Fit the grommets in the cable hole on both sides of the wall. Feed the 12 V cable, the Ethernet cable and the antenna cable up the post to the head and the post top. **Hold point:** safety stop S3 before the mains is first switched on.

### Step 7: head tray onto the post

![Step 7](05-build-plan/step-07.png)

With a helper holding the tray level, bottom edge 1,040 mm up, fit four M8 screws with 30 mm washers from inside the tray into the rivet nuts. Fit the grommet in the head's cable hole and pull the cables through.

### Step 8: hood onto the head top

![Step 8](05-build-plan/step-08.png)

Run sealant along the roof's back edge, set the roof on the tray top against the post, and fit four M5 tamper-resistant screws into the rivet nuts.

### Step 9: antenna bracket and antenna on the post cap

![Step 9](05-build-plan/step-09.png)

Pass the antenna cable up through the cap, connect it to the antenna's bulkhead, push the bulkhead through the bracket and the cap and fit its nut underneath. Fit the bracket with four M5 screws and a bead of sealant. **Hold point:** safety stop S5 before you climb.

### Step 10: buttons and notice plate onto the front panel

![Step 10](05-build-plan/step-10.png)

On the bench, with the panel face up. Fit each button through its hole and tighten its nut from behind. Fit the notice plate with four M4 tamper-resistant screws and nyloc nuts.

### Step 11: window onto the front panel

![Step 11](05-build-plan/step-11.png)

Turn the panel face down on a soft cloth. Clean the 8 mm band round the opening and the window's edge with isopropyl alcohol, lay the glazing tape on the band, peel its liner and press the window on for 30 seconds all round.

### Step 12: foam gasket and e-paper panel

![Step 12](05-build-plan/step-12.png)

Wearing clean gloves, lay the foam gasket round the window's back over the panel's border area, then lay the e-paper panel face down on it, centered, with its flat cable toward the top.

### Step 13: display carrier onto the studs

![Step 13](05-build-plan/step-13.png)

Slide a spacer onto each stud, pass the panel's flat cable through the carrier's slot and lower the carrier, with its boards already fitted and wired, over the studs. Fit eight M4 nuts snug, working across, so the panel is held but not stressed. Connect the flat cable to the driver board.

### Step 14: front panel onto the head tray

![Step 14](05-build-plan/step-14.png)

Plug the 12 V cable, the Ethernet cable and the LED cable into the terminal block and controller, lay the gasket strip on the tray flange, and fit the panel with twelve M4 tamper-resistant screws, tightened evenly. **Hold point:** safety stop S6.

### Step 15: sun shield onto its standoffs (outdoor sites only)

![Step 15](05-build-plan/step-15.png)

Bolt the four standoffs through the cabinet sides from inside, with a sealing washer under each bolt head. Lower the shield over them and fit four M6 tamper-resistant screws through its sides.

### Step 16: shield back panel (outdoor sites only)

![Step 16](05-build-plan/step-16.png)

Hold the back panel on the shield's back flanges and fit the four thumb screws finger tight. **Hold point:** safety stop S7.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of CTW-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Electrical installation | R14 | Electrician's inspection and tests to local code: earth continuity, insulation, RCBO trip time with its test button and a tester | All pass; only 12 V reaches the post and head |
| 12 V supply | R14 | Meter at the head's terminal block with the front panel open | 12 V, give or take 0.5 V; the 2 A fuse in place |
| Button response | R10 | Press each button and time the LED ring and the new layer | Ring lights within 0.5 s and stays lit; new layer within 25 s |
| Reach and overhang | R11 | Tape measure from the sidewalk and from the post faces | Buttons 1,120 mm up; nothing overhangs the post more than 305 mm between 685 and 2,030 mm |
| Night light | R9 | Cover the dusk sensor; read the screen at 1.5 m in a dark room | Light on, dimmed; 7 mm capitals readable |
| Running power | R15 | Energy meter on the mains feed over 24 h | 15 W average or less (9.2 W expected) |
| Outage | R18 | Switch the RCBO off for 30 min | The screen keeps its last image and time stamp; the gateway runs on its pack |
| Pilot climate | R12 | Temperature loggers in the head and the cabinet for a week on the pilot site | Panel under 40 °C and cabinet under 45 °C at the hottest hour |
| No exposed ports | R19 | Look over the closed kiosk | No socket, USB port or screw that opens the head without a special bit |
| Head seal | R12 | Gentle hose spray on the closed head for 5 min (the IP test comes later) | No water inside the head |
| Post plumb and anchors | R13 | Level on two faces; torque wrench on the anchor nuts | Plumb within 2 mm per meter; nuts at the maker's torque |
| Mass | Handling (CTW-CAL-001 [H4]) | Weigh the post assembly before lifting, or sum the parts | About 64 kg with the shield; a two-person or hoist lift |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the post is lifted.** The footing is cured and designed for the site (or the bench block is level and anchored); two people or a hoist are ready; the work area is closed to the public; gloves and safety boots are worn.
- **S2. Before any mains wiring.** The feed is isolated and locked off at its source by the electrician, who does or checks all mains work; the cabinet's earth stud is bonded to the post.
- **S3. Before mains is first switched on.** The electrician's tests in section 5 pass; the RCBO trips on its test button; no mains wire leaves the cabinet; the cabinet door closes and locks.
- **S4. Before the gateway's backup pack fuse goes in.** The pack's voltage is within its maker's range, it has its own protection board and fuse, it shows no swelling, and the cabinet is out of direct sun or under its shield. Never defeat the gateway's 0 to 45 °C charge lockout.
- **S5. Before working on the post top.** A stable ladder or platform and a second person; no work in wind or rain; nothing dropped on the walkway below.
- **S6. Before 12 V is switched on to the head.** The terminal block's polarity is checked with a meter; the 2 A fuse is in; the e-paper panel's flat cable is seated; no wire is pinched by the front panel.
- **S7. Before the kiosk is left unattended.** Every tamper-resistant screw is in; the cabinet is locked; no sharp edge or corner at head height; the hood corners are rounded; the area round the post is clear for a walkway as local rules require.

## 7. Tools, skills and workspace

**Tools.** Bench drill or a drill in a stand; drills 2.5 to 13 mm; step drill to 33 mm; hole saw or punch for 25 mm holes in 4 mm steel; 90 degree countersink; rivet nut setting tool for M4, M5 and M8, steel and aluminum; M5 tap; tamper-resistant driver bits to match the screws; torque wrench; spirit level; tape measure and steel rule; scriber; deburring tool and files; caulking gun and sealant; isopropyl alcohol and lint-free cloths; clean nitrile gloves; ferrule crimper and wire strippers; soldering iron; multimeter; a hoist or two people; a stable ladder. The steel fabricator welds, galvanizes and coats the post; the sheet metal shop folds and coats the sheet parts.

**Skills.** Metalwork with drills and rivet nut tools, careful handling of a thin glass display, low-voltage wiring and crimping. Welding of the post and base plate is done by a qualified welder at the fabricator. All mains wiring and testing is done by a qualified electrician; the rest of the build is extra-low voltage (12 V).

**Workspace.** A bench about 1.5 x 0.8 m for the front panel and display work, clean and free of metal chips; a separate metalwork corner; a floor area about 2 x 2 m with headroom of 3 m to stand the post on its test block; a dry, ventilated place for sealant and glazing tape to cure.

**Personal protective equipment.** Safety glasses for drilling and cutting; cut-resistant gloves for sheet metal; safety boots and gloves for lifting the post; clean gloves for the display; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/CTW-DWG-101` to `CTW-DWG-111`.
- General arrangement: `cad/drawings/CTW-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (CTW-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; wind and anchors [H1] to [H6], mass [H4], power [G1], timing [C2], cost [J1].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (CTW-DDR-003), with CTW-DDR-001 and CTW-DDR-002.
- Requirements: `docs/03-requirements.md` (CTW-REQ-001 v0.5).
