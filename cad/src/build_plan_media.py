"""CityTwin prototype build plan pictures (CTW-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|holes|wiring ...]
A sheet, joint or step can be named alone, for example `sheets:101` or `steps:4`, to draw one
picture per process when memory is tight. With no argument it draws everything. Every picture
is drawn from cad/src/model.py (build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/CTW-DWG-101 to 111        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/post-holes.png      hole layout on the post faces (matplotlib)
    docs/05-build-plan/panel-holes.png     hole layout on the head front panel (matplotlib)
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import (PARAMS as P, build_components, derived, box, HEAD_PANEL_SCREWS, NOTICE_HOLES, STUDS,  # noqa: E402
                   LED_GROMMET)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P, shield=True)
P2 = P["post"] / 2

COL = {"base": "#4B5563", "post": "#374151", "anchors": "#6B7280", "cabinet": "#78716C", "mplate": "#A8A29E",
       "rails": "#9CA3AF", "protection": "#DC2626", "psu": "#7C3AED", "gateway": "#C2410C", "conduit": "#0EA5E9",
       "tray": "#9CA3AF", "hood": "#64748B", "led": "#FBBF24", "antenna": "#111827", "front_panel": "#CBD5E1",
       "buttons": "#D4A017", "window": "#93C5FD", "epd": "#1E3A8A", "carrier": "#0F766E", "modules": "#16A34A",
       "notice": "#0D9488", "shield": "#E2E8F0", "backpanel": "#CBD5E1", "fix": "#111827", "grommet": "#1F2937",
       "tape": "#F59E0B", "foam": "#F97316", "footing": "#D6D3D1"}


def _fuse(shapes):
    out = None
    for s in shapes:
        if s is not None:
            out = s if out is None else out + s
    return out


def S(*keys):
    return _fuse([C[k][2] for k in keys])


def crop(shape, x0=-1e4, x1=1e4, y0=-1e4, y1=1e4, z0=-1e4, z1=1e4):
    try:
        s = shape & box(x0, x1, y0, y1, z0, z1)
        return s if s.volume > 1e-3 else None
    except Exception:
        return None


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def cabinet_open():
    """The cabinet with its door left off, so the inside shows."""
    return crop(C["cabinet"][2], y1=D["cab_y1"] - P["cab_t"])


def footing():
    return box(-350, 350, -350, 350, -300, 0)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "base": part("Base plate", C["base"][2], COL["base"]),
        "post": part("Post with cap", S("post", "cap"), COL["post"]),
        "anchors": part("Anchors, nuts and washers", S("anchors", "anchor_nuts"), COL["anchors"]),
        "cabinet": part("Services cabinet, drilled", C["cabinet"][2], COL["cabinet"]),
        "mplate": part("Mounting plate and DIN rails", S("mplate", "rails"), COL["mplate"]),
        "protection": part("Mains protection (RCBO, surge)", C["protection"][2], COL["protection"]),
        "psu": part("12 V power supply", C["psu"][2], COL["psu"]),
        "gateway": part("TwinKit gateway", C["gateway"][2], COL["gateway"]),
        "conduit": part("Conduit and gland", C["conduit"][2], COL["conduit"]),
        "tray": part("Head tray", C["tray"][2], COL["tray"]),
        "hood": part("Hood with LED strip", S("hood", "led"), COL["hood"]),
        "antenna": part("Antenna bracket and antenna", S("ant_bracket", "antenna"), COL["antenna"]),
        "front_panel": part("Head front panel with studs", S("front_panel", "studs"), COL["front_panel"]),
        "buttons": part("Push buttons (3)", S("buttons", "button_nuts"), COL["buttons"]),
        "notice": part("Data notice plate", C["notice"][2], COL["notice"]),
        "window": part("Window and glazing tape", S("window", "tape"), COL["window"]),
        "epd": part("E-paper panel and foam gasket", S("epd", "foam"), COL["epd"]),
        "carrier": part("Display carrier with spacers", S("carrier", "spacers"), COL["carrier"]),
        "modules": part("Driver, controller, converter, LED driver, terminals", S("driver", "controller", "power_mods", "terminal", "standoffs"), COL["modules"]),
        "shield": part("Sun shield on standoffs (outdoor sites)", S("shield", "standoffs_sh"), COL["shield"]),
        "backpanel": part("Shield back panel (outdoor sites)", S("backpanel", "thumbs"), COL["backpanel"]),
    }


ORDER = ["base", "post", "anchors", "cabinet", "mplate", "protection", "psu", "gateway", "conduit", "tray", "hood",
         "antenna", "front_panel", "buttons", "notice", "window", "epd", "carrier", "modules", "shield", "backpanel"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"base": (0, 0, -300), "post": (0, 0, 0), "anchors": (0, 0, -520), "cabinet": (0, 380, -60),
           "mplate": (0, 700, -60), "protection": (-120, 980, -230), "psu": (120, 980, -120), "gateway": (0, 980, 60),
           "conduit": (0, 380, -420), "tray": (0, -200, 120), "hood": (0, -200, 420), "antenna": (0, 0, 520),
           "front_panel": (-1650, -200, 120), "buttons": (-1650, -350, -120), "notice": (-1650, -350, -120),
           "window": (-1300, -200, 120), "epd": (-1000, -200, 120), "carrier": (-700, -200, 120),
           "modules": (-700, -120, -430), "shield": (0, 1350, 60), "backpanel": (0, 1650, 60)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "CityTwin prototype kiosk: every component, pulled apart",
                       subtitle="Numbered in build order; 20 and 21 are fitted on outdoor sites only. Screws, rivet nuts and grommets not shown",
                       elev=16, azim=-40, size=(12, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="CityTwin", date=DATE)
    post_low = part("Post", crop(S("post", "cap"), z1=400), COL["post"])
    jobs = {}

    jobs[101] = lambda: bv.component_sheet(
        Part("Base plate", C["base"][2], COL["base"]), [post_low, part("a", S("anchors", "anchor_nuts"), "#999")],
        dwg_no="CTW-DWG-101", title="CityTwin base plate: making sketch", material="Steel plate 12 mm, S275 or S355 class",
        inset_view=(30, -50),
        notes=["Blank 400 x 400 mm, 12 mm steel; corners rounded about 10 mm.",
               "Positions from the plate center; the post sits on the center.",
               "Four anchor holes 18 mm on a 300 mm square (150 each way).",
               "Vent and drain hole 25 mm at the center, under the post:",
               "  the galvanizer needs it, and it lets condensation out.",
               "Conduit hole 40 mm on the center line, 130 mm toward the back",
               "  (the cabinet side), clear of the post by 64 mm.",
               "Weld: post square on the plate, 4 mm fillet all round,",
               "  before galvanizing (one weldment with the post).",
               "Deburr every hole; grind weld spatter off the top face.",
               "Check: the post stands square to the plate within 1 mm",
               "  over its height; anchor holes 300 mm apart both ways."], **base)

    def post_sheet():
        ps = S("post", "cap")
        flat = b.Rot(0, 90, 0) * ps         # lay the post down: its length along X
        return bv.component_sheet(
            Part("Post", ps, COL["post"]), [M["base"], M["cabinet"], M["tray"]],
            dwg_no="CTW-DWG-102", title="CityTwin post: making sketch", material="Steel SHS 100 x 100 x 4 mm and 6 mm cap plate",
            view_shape=flat, inset_view=(18, -40),
            notes=["Cut the tube 1,742 mm long, square ends; weld a 100 x 100 x 6",
                   "  cap on top (20 mm coax hole, four M5 tapped holes at 20 each way).",
                   "Heights below are from the sidewalk; the tube starts 12 mm up.",
                   "Front wall (head side): four 11 mm holes 25 mm each side of",
                   "  center at 1,100 and 1,660; one 25 mm cable hole at 1,380.",
                   "Back wall (cabinet side): four 11 mm holes 25 mm each side",
                   "  at 360 and 700; one 25 mm cable hole at 735.",
                   "Countersink the 11 mm holes 90 degrees for flush rivet nuts.",
                   "Weld to the base plate, then hot-dip galvanize and powder coat.",
                   "After coating: set eight M8 flush steel rivet nuts; clean",
                   "  the threads; deburr the cable holes and fit grommets.",
                   "Check: an M8 screw runs into every rivet nut by hand."], **base)
    jobs[102] = post_sheet

    jobs[103] = lambda: bv.component_sheet(
        Part("Head tray", C["tray"][2], COL["tray"]), [part("p", crop(S("post", "cap"), z0=900), "#999"), M["hood"]],
        dwg_no="CTW-DWG-103", title="CityTwin head tray: making sketch", material="Aluminum sheet 2 mm, 5052 class",
        inset_view=(20, -50),
        notes=["Folded tray 460 wide, 680 tall, 98 deep, open to the front.",
               "Back, top, bottom and sides from one blank; weld or rivet and",
               "  seal the four corners. 15 mm return flange round the front.",
               "Back wall: four 9 mm holes 25 mm each side of center at",
               "  60 and 620 mm up from the bottom edge; 25 mm cable hole at 340.",
               "Bottom: six vent slots 30 x 70 mm, 60 mm apart; glue insect",
               "  mesh inside them.",
               "Top: four 7 mm holes at 150 mm each side, 30 and 70 mm",
               "  behind the front panel line, for M5 rivet nuts (hood).",
               "Flange: twelve 6 mm holes for M4 rivet nuts (front panel):",
               "  three along the top and bottom, three down each side.",
               "Check: the flange is flat to 1 mm so the gasket seals."], **base)

    jobs[104] = lambda: bv.component_sheet(
        Part("Head front panel", S("front_panel", "studs"), COL["front_panel"]), [M["tray"], M["window"], M["buttons"], M["notice"]],
        dwg_no="CTW-DWG-104", title="CityTwin head front panel: making sketch", material="Aluminum sheet 2 mm, 5052 class, powder coated",
        inset_view=(20, -50),
        notes=["Blank 460 x 680 mm. Heights from the bottom edge.",
               "Window opening 240 wide x 320 tall, centered, 260 to 580 up.",
               "Three button holes 19.2 mm at 80 mm up: center and 70 each side.",
               "Notice plate holes 4.5 mm: 190 mm each side, 137 and 213 up.",
               "Screw holes 4.5 mm, 7.5 mm in from the edge, matching the",
               "  tray flange (twelve). LED grommet hole 13 mm, 140 mm right",
               "  of center, 645 up (under the hood).",
               "Press eight M4 x 25 clinch studs in from the back, 138 mm",
               "  each side and on the center line, 242, 420 and 598 up.",
               "Powder coat; mask the stud threads and the tape lap.",
               "Check: lay it on the tray; all twelve holes line up."], **base)

    jobs[105] = lambda: bv.component_sheet(
        Part("Display carrier", C["carrier"][2], COL["carrier"]), [M["front_panel"], M["epd"], M["modules"]],
        dwg_no="CTW-DWG-105", title="CityTwin display carrier: making sketch", material="Aluminum sheet 2 mm, 5052 class",
        inset_view=(20, 130),
        notes=["Blank 290 wide x 370 tall, corners rounded 5 mm.",
               "Eight 4.5 mm holes on the front panel studs: 138 mm each",
               "  side and on the center line, 7, 185 and 363 up.",
               "Ribbon slot 70 x 8 mm, centered, 49 to 57 mm below the",
               "  top edge; the e-paper panel's cable passes through it.",
               "Mark the board positions from the boards themselves and drill",
               "  2.7 mm for M2.5 standoffs: driver board top center,",
               "  controller lower left, converter and LED driver lower right,",
               "  terminal block bottom left.",
               "Fit: it sits on 15 mm spacers over the studs and presses the",
               "  e-paper panel onto its foam gasket on the window.",
               "Check: it drops over all eight studs without force."], **base)

    jobs[106] = lambda: bv.component_sheet(
        Part("Data notice plate", C["notice"][2], COL["notice"]), [M["front_panel"], M["buttons"]],
        dwg_no="CTW-DWG-106", title="CityTwin data notice plate: making sketch", material="Aluminum sheet 2 mm, printed or engraved",
        inset_view=(15, -60), view_shape=b.Rot(0, 90, 0) * C["notice"][2],
        notes=["Plate 400 x 100 mm, drawn standing on end; corners rounded",
               "  5 mm, edges deburred.",
               "Four 4.5 mm holes, 10 mm in from each end, 12 mm in from",
               "  the top and bottom edges (380 mm and 76 mm apart).",
               "Content by the sign maker: what is measured, who is",
               "  responsible, how long data is kept, QR code and short URL",
               "  to the sensor register; icons in the style of DTPR.",
               "Keep the QR code at least 25 mm square and clear of the holes.",
               "Fit: on the front panel, bottom edge 125 mm up, four M4",
               "  tamper-resistant screws with nyloc nuts inside.",
               "Check: the QR code scans from 1 m with a phone."], **base)

    jobs[107] = lambda: bv.component_sheet(
        Part("Hood", S("hood", "led"), COL["hood"]), [M["tray"], M["front_panel"], part("p", crop(S("post", "cap"), z0=1500), "#999")],
        dwg_no="CTW-DWG-107", title="CityTwin hood: making sketch", material="Aluminum sheet 1.5 mm, 5052 class; 20 x 20 x 1.5 angle",
        inset_view=(25, -50),
        notes=["Roof 500 wide x 240 deep, folded from one blank with a",
               "  60 mm front lip and two side cheeks 120 deep x 90 long;",
               "  notch the corners before folding, seal them with sealant.",
               "Four 5.5 mm holes in the roof at 150 mm each side, 30 and",
               "  70 mm in front of the back edge (over the tray rivet nuts).",
               "Round every exposed corner to at least 10 mm: the hood",
               "  is at head height.",
               "LED angle: 300 mm of 20 x 20 x 1.5 angle, riveted under the",
               "  roof 20 mm behind the lip, one leg facing the screen;",
               "  stick the LED strip on that leg.",
               "Fit: the roof sits on the tray top, back edge on the post.",
               "Check: the lip hides the LED strip from the sidewalk."], **base)

    jobs[108] = lambda: bv.component_sheet(
        Part("Antenna bracket", C["ant_bracket"][2], COL["antenna"]), [part("p", crop(S("post", "cap"), z0=1650), "#999"), part("a", crop(C["antenna"][2], z1=1900), "#999")],
        dwg_no="CTW-DWG-108", title="CityTwin antenna bracket: making sketch", material="Aluminum plate 6 mm, 6082 class",
        inset_view=(25, -50),
        notes=["Plate 60 x 60 mm, 6 mm, corners rounded 3 mm.",
               "Center hole 16.5 mm for the antenna's N-type bulkhead.",
               "Four 5.5 mm holes at 20 mm each way from center,",
               "  matching the M5 tapped holes in the post cap.",
               "Fit: on the cap with four M5 screws and a bead of sealant;",
               "  the bulkhead passes through the plate and the cap's",
               "  20 mm hole, nut underneath, coax down the post.",
               "Check: the antenna stands vertical within 2 degrees."], **base)

    def cab_sheet():
        return bv.component_sheet(
            Part("Services cabinet", C["cabinet"][2], COL["cabinet"]), [part("p", crop(S("post", "cap"), z1=1000), "#999"), M["shield"]],
            dwg_no="CTW-DWG-109", title="CityTwin services cabinet: drilling sketch", material="Bought steel cabinet 360 x 160 x 460 mm, IP55",
            inset_view=(20, 50),
            notes=["Remove the mounting plate before drilling; protect the inside.",
                   "Wall against the post (the face opposite the door), heights",
                   "  from the cabinet's bottom edge: four 9 mm holes 25 mm each",
                   "  side of center at 60 and 400; one 25 mm cable hole at 435.",
                   "Floor: one 32.5 mm gland hole on the center line, mid-depth.",
                   "Sides, outdoor sites only: two 6.5 mm holes each side at",
                   "  mid-depth, 120 and 380 up, for the sun shield standoffs.",
                   "Deburr; touch up the paint on every cut edge.",
                   "Check: with the cabinet held on the post, every 9 mm hole",
                   "  lines up with a rivet nut and the cable holes line up."], **base)
    jobs[109] = cab_sheet

    jobs[110] = lambda: bv.component_sheet(
        Part("Sun shield", C["shield"][2], COL["shield"]), [M["cabinet"], part("p", crop(S("post", "cap"), z1=1000), "#999")],
        dwg_no="CTW-DWG-110", title="CityTwin sun shield (outdoor sites): making sketch", material="Aluminum sheet 1.5 mm, 5052 class, powder coated light grey",
        inset_view=(20, 50),
        notes=["Top 413 x 186 mm with two sides folded down 90 degrees,",
               "  486 mm high overall; a 15 mm flange folded inward along",
               "  each side's back edge. Rivet or weld the top corners.",
               "Two 6.5 mm holes in each side at mid-depth, 120 and 380 mm",
               "  up from the bottom edge, for the standoff screws.",
               "In each flange, two 7 mm holes for M5 rivet nuts, 100 and",
               "  400 mm up, for the back panel's thumb screws.",
               "Fit: on four 25 mm standoffs on the cabinet sides; 25 mm",
               "  air gap at the top and sides; open at the bottom.",
               "Check: the gap is 25 mm, give or take 3, all round."], **base)

    jobs[111] = lambda: bv.component_sheet(
        Part("Shield back panel", S("backpanel"), COL["backpanel"]), [M["shield"], M["cabinet"]],
        dwg_no="CTW-DWG-111", title="CityTwin shield back panel (outdoor sites): making sketch", material="Aluminum sheet 1.5 mm, 5052 class, powder coated light grey",
        inset_view=(20, 50),
        notes=["Panel 413 wide x 485 tall, corners rounded 5 mm.",
               "Four vent slots 60 x 15 mm, 20 mm apart, 45 to 60 mm below",
               "  the top edge.",
               "Four 6.5 mm holes, 197.5 mm each side of center, 100 and",
               "  400 mm up, for M5 knurled thumb screws.",
               "Fit: on the shield's back flanges, over the cabinet door,",
               "  25 mm behind it. Undo four thumb screws to reach the door.",
               "Check: it comes off and goes back by hand in a minute."], **base)

    for k in sorted(jobs):
        if only is None or k in only:
            print("sheet", k, jobs[k]())


# ----------------------------------------------------------------- joints
def joints(only=None):
    jobs = {}
    cz = P["screen_cz"]
    bt = P["base"][2]

    def j1():
        z1 = 160
        ps = [part("Post (cut open)", crop(C["post"][2], z1=z1, x0=0), COL["post"]),
              part("Base plate", crop(C["base"][2], x0=0), COL["base"]),
              part("Anchor, washer and nut", crop(S("anchors", "anchor_nuts"), x0=0), COL["anchors"]),
              part("Conduit", crop(C["conduit"][2], z0=-40, z1=z1, x0=0), COL["conduit"]),
              part("Footing (site work)", crop(footing(), z0=-40, x0=0, x1=230, y0=-230, y1=230), COL["footing"])]
        return bv.joint(ps, OUT / "joint-01.png", "Joint 1: post foot, base plate and anchors",
                        subtitle="Cut on the center line, seen from the left. 4 mm fillet weld all round; 25 mm drain hole under the post",
                        elev=22, azim=-140, size=(8, 5.6))
    jobs[1] = j1

    def j2():
        sx = P["post_screw_x"]
        zc = P["cab_screw_z"][1]
        L = [(C["post"][2], "Post wall, 4 mm", COL["post"]), (C["cab_rivnuts"][2], "Flush M8 rivet nut", COL["fix"]),
             (C["cabinet"][2], "Cabinet back wall", COL["cabinet"]), (C["cab_screws"][2], "M8 screw and 30 mm washer", "#B45309"),
             (C["mplate"][2], "Mounting plate (fitted last)", COL["mplate"])]
        return section2d("joint-02.png", "Joint 2: cabinet on the post",
                         "True section through the upper right screw, seen from the right, to scale; the screw goes in from inside the cabinet",
                         L, "x", sx, 15, 95, zc - 30, zc + 60, left_label="inside the post", right_label="inside the cabinet")
    jobs[2] = j2

    def j3():
        sx = P["post_screw_x"]
        zc = P["head_screw_z"][1]
        L = [(C["post"][2], "Post wall, 4 mm", COL["post"]), (C["head_rivnuts"][2], "Flush M8 rivet nut", COL["fix"]),
             (C["tray"][2], "Head tray, back wall and top", COL["tray"]), (C["head_screws"][2], "M8 screw and 30 mm washer", "#B45309"),
             (C["hood"][2], "Hood roof", COL["hood"]), (C["hood_rivnuts"][2], "M5 rivet nut (hood)", COL["fix"])]
        return section2d("joint-03.png", "Joint 3: head tray on the post",
                         "True section through the upper right screw, seen from the right, to scale; screws go in from inside the tray",
                         L, "x", sx, -95, -15, zc - 30, zc + 70, left_label="street side (inside the head)", right_label="inside the post")
    jobs[3] = j3

    def j4():
        return section_stack()
    jobs[4] = j4

    def j5():
        x, z = HEAD_PANEL_SCREWS(P)[-2]
        L = [(C["front_panel"][2], "Front panel, 2 mm", COL["front_panel"]), (C["panel_screws"][2], "Tamper-resistant M4 screw", "#B45309"),
             (C["panel_rivnuts"][2], "M4 rivet nut", COL["fix"]), (C["tray"][2], "Tray return flange", "#57534E")]
        return section2d("joint-05.png", "Joint 5: front panel on the tray flange",
                         "True section through a right-hand side screw, seen from the right, to scale; the gasket strip goes on the flange",
                         L, "x", x, -160, -125, z - 15, z + 15, left_label="street", right_label="inside the head")
    jobs[5] = j5

    def j6():
        L = [(C["hood"][2], "Hood: roof and lip, 1.5 mm", COL["hood"]), (C["led"][2], "LED strip on its angle", COL["led"]),
             (C["hood_screws"][2], "M5 tamper-resistant screw", "#B45309"), (C["hood_rivnuts"][2], "M5 rivet nut", COL["fix"]),
             (C["tray"][2], "Head tray top", COL["tray"]), (C["front_panel"][2], "Front panel", "#0F766E"),
             (C["grommets"][2], "LED cable grommet (140 mm right)", "#0EA5E9")]
        return section2d("joint-06.png", "Joint 6: hood on the head top",
                         "True section through the right-hand hood screws, seen from the right, to scale; the lip hides the LED strip",
                         L, "x", 148, -300, -45, 1650, 1730, left_label="street", right_label="post", size=(12, 5.2),
                         anchors={"Front panel": (-149, 1662), "Head tray top": (-140, 1719), "Hood: roof and lip, 1.5 mm": (-289, 1690),
                                  "LED strip on its angle": (-268, 1706)})
    jobs[6] = j6

    def j7():
        L = [(C["buttons"][2], "Push button: bezel and body", COL["buttons"]), (C["button_nuts"][2], "Button nut", COL["fix"]),
             (C["front_panel"][2], "Front panel", COL["front_panel"]), (C["notice"][2], "Notice plate", COL["notice"]),
             (C["notice_fix"][2], "Notice plate screw and nut", "#B45309")]
        return section2d("joint-07.png", "Joint 7: push button and notice plate in the front panel",
                         "True section on the center line through the middle button, seen from the right, to scale",
                         L, "x", 0, -165, -105, P["btn_z"] - 20, P["notice_z0"] + 25, left_label="street", right_label="inside the head")
    jobs[7] = j7

    def j8():
        import build123d as b
        pt = P["post_top"]
        L = [(S("post", "cap"), "Post wall and 6 mm cap", COL["post"]),
             (C["ant_bracket"][2], "Antenna bracket, 6 mm", "#0EA5E9"),
             (C["antenna"][2], "Antenna base and bulkhead", COL["antenna"]),
             (b.Pos(-20, 0, 0) * C["ant_screws"][2], "M5 screws (behind the cut)", "#B45309")]
        return section2d("joint-08.png", "Joint 8: antenna bracket on the post cap",
                         "True section on the center line, seen from the right, to scale; the antenna cable runs down inside the post",
                         L, "x", 0, -60, 60, pt - 45, pt + 45, left_label="street side", right_label="cabinet side")
    jobs[8] = j8

    def j9():
        y, z = (P["post"] / 2 + P["cab_d"] / 2, 420.0)
        so = C["standoffs_sh"][2]
        L = [(C["cabinet"][2], "Cabinet side", COL["cabinet"]),
             (crop(so, x1=178), "M6 bolt and sealing washer (inside)", COL["fix"]),
             (crop(so, x0=178, x1=180), "", COL["fix"]),
             (crop(so, x0=180, x1=205), "25 mm standoff", "#B45309"),
             (crop(so, x0=205), "M6 screw (outside)", COL["fix"]),
             (C["shield"][2], "Sun shield side", "#94A3B8")]
        return section2d("joint-09.png", "Joint 9: sun shield standoff (outdoor sites)",
                         "True section through the lower right standoff, seen from the post side, to scale; sealing washer under the inside bolt",
                         L, "y", y, 160, 220, z - 30, z + 30, left_label="inside the cabinet", right_label="outside")
    jobs[9] = j9

    def j10():
        r = dict(x0=-15, x1=1e4, y0=-60, z0=270, z1=780)
        ps = [part("Post and cabinet, door off (cut)", crop(_fuse([S("post", "cap"), cabinet_open()]), **r), COL["cabinet"]),
              part("Mounting plate and rails", crop(S("mplate", "rails"), **r), COL["mplate"]),
              part("TwinKit gateway", crop(C["gateway"][2], **r), COL["gateway"]),
              part("12 V supply", crop(C["psu"][2], **r), COL["psu"]),
              part("Conduit gland: mains in", crop(C["conduit"][2], **r), COL["conduit"]),
              part("Grommet: 12 V, Ethernet and coax to the post", crop(C["grommets"][2], **r), "#0EA5E9")]
        return bv.joint(ps, OUT / "joint-10.png", "Joint 10: inside the cabinet, cable routes",
                        subtitle="Cut on the center line, seen from the left, door off. Mains stays in the cabinet; low-voltage cables go up the post",
                        elev=12, azim=-172, size=(8.5, 6))
    jobs[10] = j10

    for k in sorted(jobs):
        if only is None or k in only:
            print("joint", k, jobs[k]())


def section2d(out, title, sub, layers, axis, at, h0, h1, v0, v1, left_label="", right_label="", anchors=None, size=(9, 6.2)):
    """A true section through the model, drawn to scale with matplotlib.
    axis 'x': the plane x = at, Y across the page; axis 'y': the plane y = at, X across the page; Z up.
    layers: (shape, name, color). Each solid in the slice is drawn as its outline rectangle, so thin
    layers stay readable. Labels sit in columns left and right, ordered by height, so leaders do not cross."""
    import matplotlib.patches as mp
    fig, plt = _fig(title, sub, size=size)
    ax = fig.add_axes([0.27, 0.12, 0.46, 0.76]); ax.set_aspect("equal"); ax.axis("off")
    reg = dict(z0=v0, z1=v1)
    if axis == "x":
        reg.update(x0=at - 0.25, x1=at + 0.25, y0=h0, y1=h1)
    else:
        reg.update(y0=at - 0.25, y1=at + 0.25, x0=h0, x1=h1)
    items = []
    plane = at + 0.25
    for shape, name, col in layers:
        sh = crop(shape, **reg) if shape is not None else None
        if sh is None:
            continue
        best = None
        for f in sh.faces():
            c = f.center()
            n = f.normal_at()
            on = (abs(n.X) > 0.99 and abs(c.X - plane) < 1e-3) if axis == "x" else (abs(n.Y) > 0.99 and abs(c.Y - plane) < 1e-3)
            if not on:
                continue
            uv = lambda v: (v.Y, v.Z) if axis == "x" else (v.X, v.Z)  # noqa: E731

            def poly(w):
                pts = []
                for e in w.order_edges() if hasattr(w, "order_edges") else w.edges():
                    m = 2 if e.geom_type == "LINE" else 16
                    pts += [uv(e.position_at(t / m)) for t in range(m)]
                return pts
            outer = f.outer_wire()
            pts = poly(outer)
            ax.add_patch(mp.Polygon(pts, closed=True, fc=col, ec="#111827", lw=0.5))
            for w in f.inner_wires():
                ax.add_patch(mp.Polygon(poly(w), closed=True, fc="white", ec="#111827", lw=0.4))
            bb = f.bounding_box()
            u0, du = (bb.min.Y, bb.size.Y) if axis == "x" else (bb.min.X, bb.size.X)
            if best is None or f.area > best[2]:
                cu, cv = uv(f.center())
                # a point on the material: the face center if it lies inside, else the nearest boundary point
                from matplotlib.path import Path as _P
                if not _P(pts).contains_point((cu, cv)):
                    import numpy as _np
                    a_ = _np.array(pts)
                    k_ = int(_np.argmin(((a_ - (cu, cv)) ** 2).sum(1)))
                    cu, cv = a_[k_]
                best = (cu, cv, f.area)
        if best is None:
            continue
        if anchors and name in anchors:
            best = (*anchors[name], 0)
        if name:
            items.append((name, best[0], best[1]))
    ax.set_xlim(h0, h1); ax.set_ylim(v0, v1)
    mid = (h0 + h1) / 2
    for side in ("left", "right"):
        grp = sorted([it for it in items if (it[1] < mid) == (side == "left")], key=lambda it: -it[2])
        n = len(grp)
        for i, (name, u, z) in enumerate(grp):
            ty = v1 - (v1 - v0) * (0.08 + 0.84 * (i + 0.5) / max(n, 1))
            tx = h0 - 0.04 * (h1 - h0) if side == "left" else h1 + 0.04 * (h1 - h0)
            ax.annotate(name, xy=(u, z), xytext=(tx, ty), fontsize=8, va="center", annotation_clip=False,
                        ha="right" if side == "left" else "left",
                        arrowprops=dict(arrowstyle="-", color="#6B7280", lw=0.6),
                        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#6B7280", lw=0.5))
    span = h1 - h0
    bar = 10 if span < 120 else (50 if span < 500 else 100)
    ym = v0 - 0.06 * (v1 - v0)
    ax.plot([mid - bar / 2, mid + bar / 2], [ym, ym], color="#111827", lw=1, clip_on=False)
    ax.text(mid, ym - 0.015 * (v1 - v0), f"{bar} mm", fontsize=7, ha="center", va="top")
    if left_label:
        ax.text(h0, ym, left_label, fontsize=7.5, color="#C2410C", ha="right", va="center")
    if right_label:
        ax.text(h1, ym, right_label, fontsize=7.5, color="#C2410C", ha="left", va="center")
    out = OUT / out
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def section_stack():
    """Joint 4 as a true section on the center line (x = 0) through the top stud, drawn to scale
    from the model with matplotlib, so every thin layer can be named clearly."""
    import matplotlib.patches as mp
    cz = P["screen_cz"]
    zc = cz + P["stud_dz"]
    reg = dict(x0=-0.5, x1=0.5, z0=zc - 70, z1=zc + 25, y0=-160, y1=-115)
    layers = [("front_panel", "Front panel, 2 mm", COL["front_panel"]), ("tape", "Glazing tape, 1 mm", COL["tape"]),
              ("window", "Window, 6 mm polycarbonate", COL["window"]), ("foam", "Foam gasket, 1 mm", COL["foam"]),
              ("epd", "E-paper panel, 7 mm", COL["epd"]), ("carrier", "Display carrier, 2 mm", COL["carrier"]),
              ("spacers", "Spacer, 15 mm", "#9CA3AF"), ("studs", "M4 clinch stud", "#111827"), ("stud_nuts", "M4 nut", "#B45309")]
    fig, plt = _fig("Joint 4: window and screen stack at the top stud",
                    "True section on the center line, seen from the right, to scale; the street side is on the left", size=(9, 6.2))
    ax = fig.add_axes([0.05, 0.07, 0.62, 0.83]); ax.set_aspect("equal"); ax.axis("off")
    items = []
    for key, name, col in layers:
        sh = crop(C[key][2], **reg)
        if sh is None:
            continue
        for sol in sh.solids():
            bb = sol.bounding_box()
            ax.add_patch(mp.Rectangle((bb.min.Y, bb.min.Z), bb.size.Y, bb.size.Z, fc=col, ec="#111827", lw=0.5))
        bb = sh.bounding_box()
        items.append((name, bb))
    ax.set_xlim(-162, -112); ax.set_ylim(zc - 72, zc + 27)
    # labels in a column to the right; each leader ends at its own height band so none cross
    band = {"Front panel, 2 mm": 16, "M4 nut": 3, "M4 clinch stud": 0, "Spacer, 15 mm": -3, "Display carrier, 2 mm": -10,
            "Glazing tape, 1 mm": -14, "Window, 6 mm polycarbonate": -26, "Foam gasket, 1 mm": -35, "E-paper panel, 7 mm": -50}
    order = sorted(items, key=lambda it: -band[it[0]])
    n = len(order)
    for i, (name, bb) in enumerate(order):
        ty = zc + 22 - i * (92 / max(n - 1, 1))
        px = bb.min.Y + bb.size.Y / 2
        if name == "M4 clinch stud":
            px = bb.max.Y - 4
        ax.annotate(name, xy=(px, zc + band[name]), xytext=(-108, ty), fontsize=8, va="center", annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", color="#6B7280", lw=0.6),
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#6B7280", lw=0.5))
    ax.annotate("", xy=(-160, zc - 66), xytext=(-150, zc - 66), arrowprops=dict(arrowstyle="->", color="#C2410C", lw=1.2))
    ax.text(-160, zc - 69, "street", fontsize=7.5, color="#C2410C", va="top")
    ax.plot([-160, -150], [zc - 72, zc - 72], color="#111827", lw=1)
    ax.text(-155, zc - 74, "10 mm", fontsize=7, ha="center", va="top")
    out = OUT / "joint-04.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    G = lambda name, shape: part(name, shape, bv.GHOST)  # noqa: E731
    post_all = S("post", "cap")
    low = lambda s: crop(s, z1=860)   # noqa: E731
    high = lambda s: crop(s, z0=950)   # noqa: E731
    cab_done = [G("Post", low(post_all)), G("Base plate", C["base"][2])]
    jobs = {}

    def s(n, done, new, title, sub, ctx=(), elev=22, azim=-55, size=(8, 6), label_done=False):
        return bv.step(done, new, OUT / f"step-{n:02d}.png", title, sub, context=ctx, elev=elev, azim=azim,
                       size=size, label_done=label_done)

    jobs[1] = lambda: s(1, [G("Anchors in the footing", C["anchors"][2])],
                        [part("Post and base plate", S("post", "cap", "base"), COL["post"], (0, 0, 450))],
                        "Step 1: post onto the anchors", "Two people or a hoist. Plate on shims or a grout bed, post plumb; then washers and nuts on the anchors",
                        ctx=[part("Footing", footing(), COL["footing"])], elev=18)
    jobs[2] = lambda: s(2, cab_done, [part("Services cabinet (door shown off)", cabinet_open(), COL["cabinet"], (0, 300, 0))],
                        "Step 2: cabinet onto the post back", "Mounting plate out, door open; four M8 screws with washers from inside into the post rivet nuts",
                        elev=20, azim=50)
    cab_in = cab_done + [G("Cabinet (door off)", cabinet_open())]
    jobs[3] = lambda: s(3, cab_in, [part("Mounting plate and DIN rails", S("mplate", "rails"), COL["mplate"], (0, 350, 0))],
                        "Step 3: mounting plate and rails into the cabinet", "Onto the cabinet's four studs; earth lead to the earth stud",
                        elev=20, azim=50)
    cab_in2 = cab_in + [G("Mounting plate", S("mplate", "rails"))]
    jobs[4] = lambda: s(4, cab_in2, [part("RCBO and surge protector", C["protection"][2], COL["protection"], (0, 250, 0)),
                                    part("12 V power supply", C["psu"][2], COL["psu"], (0, 250, 0))],
                        "Step 4: mains protection and 12 V supply on the lower rail", "Clip on; the wiring is done by a qualified electrician only",
                        elev=20, azim=50)
    cab_in3 = cab_in2 + [G("Lower rail devices", S("protection", "psu"))]
    jobs[5] = lambda: s(5, cab_in3, [part("TwinKit gateway", C["gateway"][2], COL["gateway"], (0, 250, 0))],
                        "Step 5: TwinKit gateway on the upper rail", "Laid out as TwinKit draws it; backup pack fuse out until stop S4",
                        elev=20, azim=50)
    cab_in4 = cab_in3 + [G("Gateway", C["gateway"][2])]
    jobs[6] = lambda: s(6, cab_in4, [part("Conduit and gland", C["conduit"][2], COL["conduit"], (0, 0, -250)),
                                    part("Cable grommets", crop(C["grommets"][2], z1=1000), COL["grommet"], (0, 200, 0))],
                        "Step 6: conduit, gland and grommets", "Conduit up through the base plate into the floor gland; grommets in the cable hole",
                        elev=20, azim=50)
    head_done = [G("Post", high(post_all))]
    jobs[7] = lambda: s(7, head_done, [part("Head tray", C["tray"][2], COL["tray"], (0, -300, 0)),
                                      part("Four M8 screws and washers (from inside)", C["head_screws"][2], "#B45309", (0, -450, 0))],
                        "Step 7: head tray onto the post front", "Held level by a helper; four M8 screws into the post rivet nuts, from inside the tray",
                        elev=18, azim=-55)
    head2 = head_done + [G("Head tray", C["tray"][2])]
    jobs[8] = lambda: s(8, head2, [part("Hood with LED strip", S("hood", "led"), COL["hood"], (0, 0, 220)),
                                  part("Four M5 screws", C["hood_screws"][2], "#B45309", (0, 0, 330))],
                        "Step 8: hood onto the head top", "Roof on the tray top, back edge on the post; sealant under the roof; four M5 screws",
                        elev=24, azim=-55)
    jobs[9] = lambda: s(9, [G("Post top", crop(post_all, z0=1500)), G("Hood", crop(S("hood", "led"), z0=1500))],
                        [part("Antenna bracket", C["ant_bracket"][2], "#0EA5E9", (0, 0, 120)),
                         part("Antenna", crop(C["antenna"][2], z1=2000), COL["antenna"], (0, 0, 260))],
                        "Step 9: antenna bracket and antenna on the post cap", "Coax fed down the post first; four M5 screws with sealant; bulkhead nut under the cap",
                        elev=22, azim=-55)
    fp = [G("Head front panel", S("front_panel", "studs"))]
    jobs[10] = lambda: s(10, fp, [part("Push buttons (3)", S("buttons", "button_nuts"), COL["buttons"], (0, -120, 0)),
                                  part("Notice plate and screws", S("notice", "notice_fix"), COL["notice"], (0, -160, 0))],
                         "Step 10: buttons and notice plate onto the front panel", "On the bench. Button nuts inside; four M4 tamper-resistant screws, nyloc nuts inside",
                         elev=12, azim=-35)
    fp2 = [G("Front panel, seen from behind", S("front_panel", "studs", "buttons", "button_nuts", "notice"))]
    jobs[11] = lambda: s(11, fp2, [part("Glazing tape", C["tape"][2], COL["tape"], (0, 90, 0)),
                                   part("Window", C["window"][2], COL["window"], (0, 160, 0))],
                         "Step 11: window onto the front panel", "Panel face down, seen from behind. Clean, tape on the lap, window pressed on for 30 s",
                         elev=25, azim=125)
    fp3 = fp2 + [G("Window", S("window", "tape"))]
    jobs[12] = lambda: s(12, fp3, [part("Foam gasket", C["foam"][2], COL["foam"], (0, 90, 0)),
                                   part("E-paper panel", C["epd"][2], COL["epd"], (0, 170, 0))],
                         "Step 12: foam gasket and e-paper panel", "Gloves; the panel is glass. Gasket on the window, panel face down on it, cable to the top",
                         elev=25, azim=125)
    fp4 = fp3 + [G("E-paper panel", S("epd", "foam"))]
    jobs[13] = lambda: s(13, fp4, [part("Display carrier with boards", S("carrier", "driver", "controller", "power_mods", "terminal", "standoffs"), COL["carrier"], (0, 180, 0)),
                                   part("Spacers (8)", C["spacers"][2], COL["fix"], (0, 90, 0))],
                         "Step 13: display carrier onto the studs", "Spacers on the studs, carrier over them, panel cable through the slot; eight M4 nuts, snug",
                         elev=25, azim=125)
    full_panel = S("front_panel", "studs", "button_nuts", "notice_fix", "tape", "foam", "epd",
                   "carrier", "spacers", "stud_nuts", "driver", "controller", "power_mods", "terminal", "standoffs")
    jobs[14] = lambda: s(14, head2 + [G("Hood", S("hood", "led"))],
                         [part("Front panel with screen and carrier", full_panel, COL["front_panel"], (0, -350, 0)),
                          part("Window", C["window"][2], COL["window"], (0, -350, 0)),
                          part("Notice plate and buttons", S("notice", "buttons"), COL["notice"], (0, -350, 0)),
                          part("Twelve M4 tamper-resistant screws", C["panel_screws"][2], "#B45309", (0, -500, 0))],
                         "Step 14: front panel onto the head tray", "Plug the cables into the terminal block first; gasket on the flange; twelve M4 screws",
                         elev=16, azim=-55)
    sh_done = cab_done + [G("Cabinet", C["cabinet"][2])]
    jobs[15] = lambda: s(15, sh_done, [part("Standoffs (4)", C["standoffs_sh"][2], "#B45309", (0, 0, 0)),
                                      part("Sun shield", C["shield"][2], COL["shield"], (0, 0, 420))],
                         "Step 15: sun shield onto its standoffs (outdoor sites)", "Standoffs through the cabinet sides with sealing washers; shield down over them; four M6 screws",
                         elev=20, azim=50)
    jobs[16] = lambda: s(16, sh_done + [G("Sun shield", S("shield", "standoffs_sh"))],
                         [part("Shield back panel", S("backpanel", "thumbs"), COL["backpanel"], (0, 260, 0))],
                         "Step 16: shield back panel (outdoor sites)", "Over the cabinet door; four knurled thumb screws, finger tight",
                         elev=20, azim=50)
    for k in sorted(jobs):
        if only is None or k in only:
            print("step", k, jobs[k]())


# ----------------------------------------------------------------- 2D hole layouts and wiring (matplotlib)
def _fig(title, sub, size=(11, 7.5)):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=size, dpi=150)
    fig.text(0.02, 0.975, title, fontsize=11, fontweight="bold", color="#111827", va="top")
    fig.text(0.02, 0.94, sub, fontsize=8.5, color="#374151", va="top")
    fig.text(0.02, 0.015, bv.BANNER, fontsize=6.5, color="#B45309")
    rr = bv._repo()
    if rr:
        fig.text(0.98, 0.015, rr, fontsize=6.5, color="#0F766E", ha="right", family="monospace")
    return fig, plt


def holes():
    import matplotlib.patches as mp
    # post faces, laid side by side, heights from the sidewalk
    fig, plt = _fig("Post: holes in the front and back walls",
                    "Heights from the sidewalk; sideways from the center line of the face. Drill before galvanizing")
    bt, top = P["base"][2], P["post_top"]
    for i, (face, items) in enumerate((
            ("FRONT WALL (head side)", [(x, z, 11, "M8 rivet nut") for z in P["head_screw_z"] for x in (-25, 25)] + [(0, P["head_cable_z"], 25, "cable")]),
            ("BACK WALL (cabinet side)", [(x, z, 11, "M8 rivet nut") for z in P["cab_screw_z"] for x in (-25, 25)] + [(0, P["cab_cable_z"], 25, "cable")]))):
        ax = fig.add_axes([0.06 + i * 0.47, 0.07, 0.42, 0.83])
        ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(mp.Rectangle((-50, bt), 100, top - bt, fc="#E5E7EB", ec="#374151", lw=0.8))
        ax.plot([0, 0], [bt, top], color="#9CA3AF", lw=0.5, ls="-.")
        for x, z, d, _ in items:
            ax.add_patch(mp.Circle((x, z), d / 2, fc="white", ec="#111827", lw=0.8))
        zs = sorted({z for _, z, _, _ in items})
        tys, last = {}, -1e9
        for z in zs:                      # keep labels at least 45 mm apart
            tys[z] = max(z, last + 45)
            last = tys[z]
        for k, z in enumerate(zs):
            lab = [f"{d:.0f} mm {t}" for x, zz, d, t in items if zz == z]
            n = len(lab)
            txt = f"{z:,.0f} up: " + (f"{n} x {lab[0]}, 25 each side" if n > 1 else lab[0])
            ax.annotate(txt, xy=(50, z), xytext=(80, tys[z]), fontsize=7.5, va="center",
                        arrowprops=dict(arrowstyle="-", color="#6B7280", lw=0.5))
        ax.text(0, top + 60, face, ha="center", fontsize=8.5, fontweight="bold")
        ax.text(0, bt - 70, "100 wide; tube 12 to 1,754 up; cap to 1,760", ha="center", fontsize=7, color="#374151")
        ax.set_xlim(-120, 520); ax.set_ylim(-100, top + 120)
    fig.savefig(OUT / "post-holes.png", facecolor="white"); plt.close(fig)
    print("holes", OUT / "post-holes.png")

    # head front panel, seen from the front, positions from the bottom left corner
    fig, plt = _fig("Head front panel: holes and cut-out, seen from the front",
                    "Sizes from the bottom edge and the center line; 460 x 680 mm, 2 mm aluminum. Stud positions are on the back face", size=(11, 8))
    ax = fig.add_axes([0.04, 0.06, 0.92, 0.84]); ax.set_aspect("equal"); ax.axis("off")
    hw, z0, h = P["head_w"] / 2, P["head_z0"], P["head_z1"] - P["head_z0"]
    ax.add_patch(mp.Rectangle((-hw, 0), 2 * hw, h, fc="#F1F5F9", ec="#111827", lw=0.9))
    ww, wh, cz = P["win_w"] / 2, P["win_h"] / 2, P["screen_cz"] - z0
    ax.add_patch(mp.Rectangle((-ww, cz - wh), 2 * ww, 2 * wh, fc="white", ec="#111827", lw=0.9))
    ax.text(0, cz, "window opening\n240 x 320\n260 to 580 up", ha="center", va="center", fontsize=8)
    for i in (-1, 0, 1):
        ax.add_patch(mp.Circle((i * 70, P["btn_z"] - z0), P["btn_hole"] / 2, fc="white", ec="#111827", lw=0.8))
    ax.text(0, P["btn_z"] - z0 - 34, "3 x 19.2 buttons, 80 up, 70 apart", ha="center", fontsize=7.5)
    nz0 = P["notice_z0"] - z0
    ax.add_patch(mp.Rectangle((-200, nz0), 400, 100, fc="none", ec="#0D9488", lw=0.8, ls="--"))
    ax.text(0, nz0 + 50, "notice plate outline (125 to 225 up)", ha="center", va="center", fontsize=7, color="#0D9488")
    for x, z in NOTICE_HOLES(P):
        ax.add_patch(mp.Circle((x, z - z0), 2.25, fc="white", ec="#111827", lw=0.8))
    ax.annotate("4 x 4.5 notice holes,\n190 each side, 137 and 213 up", xy=(190, NOTICE_HOLES(P)[3][1] - z0), xytext=(300, 230),
                fontsize=7.5, arrowprops=dict(arrowstyle="-", color="#6B7280", lw=0.5))
    for x, z in HEAD_PANEL_SCREWS(P):
        ax.add_patch(mp.Circle((x, z - z0), 2.25, fc="white", ec="#111827", lw=0.8))
    ax.annotate("12 x 4.5 screw holes, 7.5 in from the edge:\ntop and bottom at center and 160 each side;\nsides at 120, 340 and 560 up",
                xy=(222.5, 560), xytext=(300, 470), fontsize=7.5, arrowprops=dict(arrowstyle="-", color="#6B7280", lw=0.5))
    for x, z in STUDS(P):
        ax.add_patch(mp.Circle((x, z - z0), 2.0, fc="#0F766E", ec="#0F766E"))
    ax.annotate("8 x M4 clinch studs (back face),\n138 each side and center,\n242, 420 and 598 up",
                xy=(-138, STUDS(P)[5][1] - z0), xytext=(-560, 600), fontsize=7.5, arrowprops=dict(arrowstyle="-", color="#6B7280", lw=0.5))
    lx, lz = LED_GROMMET
    ax.add_patch(mp.Circle((lx, lz - z0), 6.5, fc="white", ec="#111827", lw=0.8))
    ax.annotate("13 mm LED cable grommet,\n140 right, 645 up", xy=(lx, lz - z0), xytext=(300, 660), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", color="#6B7280", lw=0.5))
    ax.plot([0, 0], [-10, h + 10], color="#9CA3AF", lw=0.5, ls="-.")
    ax.text(0, -30, "460 wide; center line dash-dot", ha="center", fontsize=7.5)
    ax.text(-hw - 15, h / 2, "680 tall", rotation=90, ha="right", va="center", fontsize=7.5)
    ax.set_xlim(-600, 600); ax.set_ylim(-60, h + 30)
    fig.savefig(OUT / "panel-holes.png", facecolor="white"); plt.close(fig)
    print("holes", OUT / "panel-holes.png")


def wiring():
    import matplotlib.patches as mp
    import matplotlib.patheffects as pe
    fig, plt = _fig("Block-level wiring",
                    "Mains (red) stays in the cabinet; 12 V SELV (blue), data (green) and the antenna cable (black) go up the post. "
                    "Wire sizes in mm\u00b2 (AWG)", size=(12, 7.4))
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.86]); ax.axis("off"); ax.set_xlim(0, 120); ax.set_ylim(0, 68)
    gap = [pe.Stroke(linewidth=5, foreground="white"), pe.Normal()]

    def blk(x0, x1, y0, y1, t, fc="#F8FAFC", ec="#374151"):
        ax.add_patch(mp.FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.3", fc=fc, ec=ec, lw=0.9, zorder=3))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, t, ha="center", va="center", fontsize=7.5, zorder=4)

    def wire(pts, c, lab=None, at=None, ha="center"):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=c, lw=1.6, path_effects=gap, zorder=2, solid_capstyle="butt")
        if lab:
            ax.text(at[0], at[1], lab, fontsize=6.8, color=c, ha=ha, va="center", zorder=5,
                    bbox=dict(fc="white", ec="none", pad=0.6))
    ax.add_patch(mp.Rectangle((1, 2), 60, 56, fc="none", ec="#78716C", lw=1, ls="--"))
    ax.text(2, 59, "SERVICES CABINET (locked; mains work by an electrician)", fontsize=8, fontweight="bold", color="#78716C")
    ax.add_patch(mp.Rectangle((70, 2), 49, 56, fc="none", ec="#64748B", lw=1, ls="--"))
    ax.text(71, 59, "DISPLAY HEAD (on the front panel's carrier)", fontsize=8, fontweight="bold", color="#64748B")
    R, B, G, K, A, E = "#DC2626", "#2563EB", "#16A34A", "#111827", "#B45309", "#65A30D"
    blk(3, 14, 47, 54, "Mains feed\nin conduit", "#FEE2E2", R)
    blk(18, 29, 47, 54, "RCBO 6 A\n30 mA", "#FEE2E2", R)
    blk(33, 43, 47, 54, "Surge\nprotector", "#FEE2E2", R)
    blk(47, 59, 47, 54, "12 V 60 W\nsupply", "#EDE9FE", "#7C3AED")
    blk(22, 52, 26, 35, "TwinKit gateway\n(fused terminals, DC-DC converter,\nUPS with LiFePO4 pack)", "#FFEDD5", "#C2410C")
    blk(3, 15, 6, 12, "Earth stud", "#F1F5F9")
    blk(56, 70, 61, 66, "Antenna (post top)", "#F1F5F9", K)
    blk(74, 90, 47, 54, "Terminal block\n(2 A fuse, pluggable)", "#DBEAFE", B)
    blk(74, 90, 35, 42, "5 V converter", "#DCFCE7", G)
    blk(74, 90, 23, 30, "LED driver\n(4 channels)", "#DCFCE7", G)
    blk(74, 90, 8, 15, "3 button rings\nand switches", "#FEF3C7", A)
    blk(97, 117, 35, 42, "Controller\n(Pi Zero 2 W class)", "#DCFCE7", G)
    blk(97, 117, 23, 30, "E-paper driver\nand panel", "#DBEAFE", "#1E3A8A")
    blk(97, 117, 8, 15, "Hood LED strip\nand dusk sensor", "#FEF3C7", A)
    wire([(14, 50.5), (18, 50.5)], R, "1.5 (16)", (16, 52.6))
    wire([(29, 50.5), (33, 50.5)], R, "1.5", (31, 52.6))
    wire([(43, 50.5), (47, 50.5)], R, "1.5", (45, 52.6))
    wire([(8.5, 47), (8.5, 12)], E, "6 (10) green-yellow", (8.5, 30))
    wire([(15, 9), (66, 9), (66, 4.5), (70, 4.5)], E, "earth bonds to post, cabinet, head tray, front panel and hood, 4 (12)", (40, 9))
    wire([(53, 47), (53, 35)], B, "1.5 (16)", (56.5, 41))
    wire([(59, 50.5), (74, 50.5)], B, "12 V, 1.0 (18),\nup the post", (67.5, 50.5))
    wire([(82, 47), (82, 42)], B, "0.75", (84.5, 46.2), ha="left")
    wire([(90, 38.5), (97, 38.5)], B, "5 V", (93.5, 38.5))
    wire([(74, 48.5), (72, 48.5), (72, 26.5), (74, 26.5)], B, "12 V", (72, 32))
    wire([(107, 35), (107, 30)], G, "SPI", (110, 32.5))
    wire([(97, 36.5), (94, 36.5), (94, 27.5), (90, 27.5)], G, "control", (94, 32))
    wire([(82, 23), (82, 15)], A, "0.25 (24)", (85.5, 19))
    wire([(90, 25), (93, 25), (93, 11.5), (97, 11.5)], A, "0.5 (20)", (93, 18))
    wire([(52, 30.5), (66, 30.5), (66, 44.5), (112, 44.5), (112, 42)], G, "Ethernet, up the post", (101, 44.5))
    wire([(40, 35), (40, 43), (62, 43), (62, 61)], K, "antenna cable", (51, 43))
    fig.savefig(OUT / "wiring.png", facecolor="white"); plt.close(fig)
    print("wiring", OUT / "wiring.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "holes", "wiring"]
    for a in args:
        name, _, sel = a.partition(":")
        only = {int(v) for v in sel.split(",")} if sel else None
        {"overview": lambda: overview(), "sheets": lambda: sheets(only), "joints": lambda: joints(only),
         "steps": lambda: steps(only), "holes": holes, "wiring": wiring}[name]()
