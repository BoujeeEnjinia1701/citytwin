"""CityTwin concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

CityTwin is mostly software. The physical part is the public kiosk: a steel post on a
base plate, a display head with a 13.3 in color e-paper screen at eye height, three
push buttons, a data notice plate and a sun and rain hood, and a lockable services
cabinet on the back of the post that holds the mains protection, a 12 V supply and the
TwinKit gateway. The LoRaWAN antenna sits on top of the post.

Axes: X across the kiosk face, Y front (-Y, the reading side) to back (+Y), Z up.
Units mm. Sidewalk surface at Z = 0.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
import concept
from concept import Part, render_all, human_figure, cutaway_parts  # noqa: F401


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def shell(x0, x1, y0, y1, z0, z1, t):
    """Closed hollow box with wall thickness t."""
    return box(x0, x1, y0, y1, z0, z1) - box(x0 + t, x1 - t, y0 + t, y1 - t, z0 + t, z1 - t)


# ---------------- key dimensions ----------------
POST = 100.0            # 100 x 100 x 4 mm square hollow section
POST_TOP = 1760.0
HEAD = (-230.0, 230.0, -150.0, -50.0, 1040.0, 1720.0)   # display head envelope
WIN = (-120.0, 120.0, 1300.0, 1620.0)                    # window opening (x0, x1, z0, z1)
SCREEN_Z = (1315.0, 1605.0)                              # 13.3 in e-paper, portrait, 285 x 209 mm outline
CAB = (-180.0, 180.0, 50.0, 210.0, 300.0, 760.0)         # services cabinet on the back of the post

STEEL = "#4B5563"
ALU = "#9CA3AF"
TEAL = "#0F766E"

# 1 Base plate with four anchors
base = box(-200, 200, -200, 200, 0, 12)
for x in (-150, 150):
    for y in (-150, 150):
        base = base + Pos(x, y, 22) * Cylinder(9, 20)

# 2 Post, square hollow section with cap
post = (box(-POST / 2, POST / 2, -POST / 2, POST / 2, 12, POST_TOP)
        - box(-POST / 2 + 4, POST / 2 - 4, -POST / 2 + 4, POST / 2 - 4, 12, POST_TOP - 6))

# 3 Display head enclosure, hollow, with window opening in the front face
head = shell(*HEAD, 3)
head = head - box(WIN[0], WIN[1], HEAD[2] - 1, HEAD[2] + 4, WIN[2], WIN[3])
for x in (-70, 0, 70):                                    # button holes
    head = head - Pos(x, HEAD[2] + 1, 1120) * Rot(90, 0, 0) * Cylinder(11, 8)
for i in range(6):                                        # vent slots in the underside
    x = -150 + i * 60
    head = head - box(x, x + 30, -135, -65, HEAD[4] - 1, HEAD[4] + 4)

# 4 Front window, 6 mm UV-stabilized polycarbonate
window = box(WIN[0] - 8, WIN[1] + 8, -147, -141, WIN[2] - 8, WIN[3] + 8)

# 5 E-paper display with driver board
display = box(-105, 105, -140, -133, *SCREEN_Z) + box(-33, 33, -133, -118, 1520, 1550)

# 6 Kiosk controller (single-board computer, Ethernet adapter, RTC) on a bracket
controller = box(-60, 40, -118, -96, 1400, 1460) + box(-60, 40, -96, -93, 1380, 1480)

# 7 Push buttons (three, stainless, LED ring)
buttons = None
for x in (-70, 0, 70):
    b = Pos(x, HEAD[2] - 3, 1120) * Rot(90, 0, 0) * Cylinder(12, 10)
    buttons = b if buttons is None else buttons + b

# 8 Data notice plate (sensor register summary, icons, QR code)
notice = box(-200, 200, HEAD[2] - 2, HEAD[2], 1165, 1265)

# 9 Sun and rain hood with LED front light
hood = (box(-250, 250, -240, -40, HEAD[5], HEAD[5] + 14)
        + box(-250, 250, -240, -228, HEAD[5] - 60, HEAD[5])          # front lip
        + box(-250, -238, -240, -150, HEAD[5] - 120, HEAD[5])        # side cheeks
        + box(238, 250, -240, -150, HEAD[5] - 120, HEAD[5]))
hood_light = box(-150, 150, -222, -208, HEAD[5] - 70, HEAD[5] - 56)
hood = hood + hood_light

# 10 Services cabinet, lockable steel, door on the back
cabinet = shell(*CAB, 2) + box(-120, -90, CAB[3], CAB[3] + 12, 500, 560)  # handle and lock

# 11 Mains protection: RCBO and surge protector on the DIN rail
rail_z = (560.0, 650.0)
protection = box(80, 150, 90, 150, *rail_z)

# 12 12 V DIN power supply
psu = box(10, 65, 90, 150, *rail_z)

# 13 TwinKit gateway (DIN enclosure) with its LiFePO4 backup pack below
gateway = box(-165, -5, 80, 150, *rail_z) + box(-150, 40, 70, 170, 320, 410)

# 14 LoRaWAN antenna on a post-top bracket (TwinKit item)
antenna = (box(-30, 30, -30, 30, POST_TOP, POST_TOP + 20)
           + Pos(0, 0, POST_TOP + 20 + 300) * Cylinder(10, 600))

# 15 Conduit and cabling: mains feed from the footing into the cabinet, data and 12 V up the post
conduit = (Pos(0, 130, 12 + 144) * Cylinder(16, 288)
           + box(-8, 8, 40, 50, 640, 700))

parts = [
    Part("Base plate and anchors", base, STEEL, 1, (0, 0, -260)),
    Part("Post, 100 mm square steel", post, "#374151", 2, (0, 0, 0)),
    Part("Display head enclosure", head, ALU, 3, (0, -220, 0)),
    Part("Front window, polycarbonate", window, "#BFDBFE", 4, (-80, -900, 420)),
    Part("E-paper display, 13.3 in color", display, "#1E3A8A", 5, (-40, -560, 210)),
    Part("Kiosk controller", controller, "#16A34A", 6, (-420, -300, 620)),
    Part("Push buttons (3)", buttons, "#D4A017", 7, (0, -760, -420)),
    Part("Data notice plate", notice, TEAL, 8, (0, -480, -200)),
    Part("Sun and rain hood with light", hood, "#6B7280", 9, (0, -260, 300)),
    Part("Services cabinet, lockable", cabinet, "#57534E", 10, (0, 1000, -150)),
    Part("Mains protection (RCBO, surge)", protection, "#DC2626", 11, (520, 420, 330)),
    Part("12 V DIN power supply", psu, "#7C3AED", 12, (260, 420, 520)),
    Part("TwinKit gateway with backup", gateway, "#C2410C", 13, (-60, 440, 80)),
    Part("LoRaWAN antenna (TwinKit)", antenna, "#111827", 14, (0, 0, 380)),
    Part("Conduit and cabling", conduit, "#0EA5E9", 15, (0, 330, -200)),
]

# Street context for the hero render only (grey, no BOM number)
sidewalk = box(-800, 1700, -1000, 600, -150, 0)
curb = box(-800, 1700, -1150, -1000, -300, 0)
road = box(-800, 1700, -1700, -1150, -300, -150)
context = [
    human_figure(1750.0, x=1150.0, y=-350.0, z=0.0),
    Part("sidewalk and curb", sidewalk + curb + road, "#D1D5DB", None),
]

# Reference neighborhood (proposed) for the data flow: (nodes, records per node per day)
REF = {
    "CurbCount": (8, 96), "CrossSafe": (4, 24), "LoadZone": (12, 64), "HeatMap Node": (6, 96),
    "FloodGauge": (4, 96), "AirStreet": (6, 288), "NoiseMap": (6, 96),
}
nodes = sum(n for n, _ in REF.values())
sent = sum(n * r for n, r in REF.values())
lost = round(sent * 0.03)
got = sent - lost
hourly = nodes * 24

render_all(
    parts, project="CityTwin", title="Public kiosk and data flow concept", dwg_no="CTW-DWG-010",
    key_figures=[f"Reference neighborhood: {nodes} LoRaWAN nodes, about {round(sent, -2):,.0f} records per day (est.)",
                 "13.3 in color e-paper, 1600 x 1200 px, screen center about 1.46 m",
                 "Buttons at about 1.12 m; about 20 s to redraw a layer",
                 "About 9 W average with TwinKit gateway; mains fed (est.)",
                 "Kiosk parts about $740; about $1,025 with TwinKit gateway (indicative)"],
    cut=False, scale_figure=False, context=context,
    flow={"title": f"data flow, records per day (estimates, {nodes}-node reference neighborhood)",
          "unit": "records/day",
          "stages": [("Node uplinks", sent), ("At gateway", got), ("Checked, stored", got),
                     ("Open export, hourly", hourly), ("Map and kiosk", "10 min redraw")],
          "losses": [(0, "Radio loss, about 3 %", lost), (2, "Rolled up to hourly", got - hourly)]},
)

# Cutaway: the reading-side layers (window, display, controller) only show in a side section,
# so cut on a vertical plane across X and look from +X, rather than the kit's default Y cut.
from build123d import Box as _Box
keep = Pos(-5000 + 10, 0, 0) * _Box(10000, 10000, 10000)
cut_parts = []
for p in parts:
    try:
        s = p.shape & keep
        if s.volume > 1e-6:
            cut_parts.append(Part(p.name, s, p.color, p.bom))
    except Exception:
        cut_parts.append(p)
concept._render(cut_parts, concept.ROOT / "media" / "cutaway.png", azim=12, elev=14,
                title="CityTwin: cutaway (section on the kiosk centerline, looking from the right)",
                note="Head: window (4), e-paper (5), controller (6). Cabinet: gateway (13), supply (12), protection (11).")

# Remove the renderer's temporary view folders
import shutil
for d in (concept.ROOT / "media").glob("_views*"):
    shutil.rmtree(d, ignore_errors=True)
print(f"nodes={nodes} sent={sent} lost={lost} got={got} hourly={hourly}")
