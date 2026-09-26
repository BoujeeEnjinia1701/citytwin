"""CityTwin concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Main dimensions and interfaces only; not for fabrication. Flow values come from CTW-CAL-001.

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
from build123d import Pos
import concept
from concept import Part, render_all, human_figure, cutaway_parts  # noqa: F401


sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import build_parts, box  # noqa: E402

# Colors and exploded-view offsets per BOM item; geometry comes from cad/src/model.py
STYLE = {
    1: ("Base plate and anchors", "#4B5563", (0, 0, -260)),
    2: ("Post, 100 mm square steel", "#374151", (0, 0, 0)),
    3: ("Display head enclosure", "#9CA3AF", (0, -220, 0)),
    4: ("Front window, polycarbonate", "#BFDBFE", (-80, -900, 420)),
    5: ("E-paper display, 13.3 in color", "#1E3A8A", (-40, -560, 210)),
    6: ("Kiosk controller", "#16A34A", (-420, -300, 620)),
    7: ("Push buttons (3)", "#D4A017", (0, -760, -420)),
    8: ("Data notice plate", "#0F766E", (0, -480, -200)),
    9: ("Sun and rain hood with light", "#6B7280", (0, -260, 300)),
    10: ("Services cabinet, lockable", "#57534E", (0, 1000, -150)),
    11: ("Mains protection (RCBO, surge)", "#DC2626", (520, 420, -260)),
    12: ("12 V DIN power supply", "#7C3AED", (260, 420, -330)),
    13: ("TwinKit gateway with backup", "#C2410C", (-60, 440, 180)),
    14: ("LoRaWAN antenna (TwinKit)", "#111827", (0, 0, 380)),
    15: ("Conduit and cabling", "#0EA5E9", (0, 330, -200)),
}
parts = [Part(STYLE[n][0], shape, STYLE[n][1], n, STYLE[n][2]) for n, _, shape in build_parts()]

# Street context for the hero render only (grey, no BOM number)
sidewalk = box(-800, 1700, -1000, 600, -150, 0)
curb = box(-800, 1700, -1150, -1000, -300, 0)
road = box(-800, 1700, -1700, -1150, -300, -150)
context = [
    human_figure(1750.0, x=1150.0, y=-350.0, z=0.0),
    Part("sidewalk and curb", sidewalk + curb + road, "#D1D5DB", None),
]

# Data flow for the reference neighborhood (CTW-CAL-001 sections A and B)
REF = {
    "CurbCount": (8, 96), "CrossSafe": (4, 24), "LoadZone": (12, 124), "HeatMap Node": (6, 96),
    "FloodGauge": (4, 96), "AirStreet": (6, 288), "NoiseMap": (6, 96),
}
LOSS = 0.0061            # collisions 0.38 % plus downlink blanking 0.23 % (CTW-CAL-001 [A3])
nodes = sum(n for n, _ in REF.values())
sent = sum(n * r for n, r in REF.values())
lost = round(sent * LOSS)
got = sent - lost
hourly = nodes * 24

render_all(
    parts, project="CityTwin", title="Public kiosk and data flow concept", dwg_no="CTW-DWG-010",
    key_figures=[f"Reference neighborhood: {nodes} LoRaWAN nodes, {sent:,} uplinks a day, 0.61 % lost",
                 "13.3 in color e-paper, 1600 x 1200 px, screen center 1.46 m",
                 "Buttons at 1.12 m; 19.8 s to redraw a layer (R10 not met)",
                 "10.2 W average from the mains with TwinKit; about 58 kg",
                 "Kiosk parts $739; $1,029 with TwinKit gateway (indicative)"],
    cut=False, scale_figure=False, context=context,
    flow={"title": f"LoRaWAN data flow, records per day (CTW-CAL-001 estimates, {nodes}-node reference neighborhood)",
          "unit": "records/day",
          "stages": [("Node uplinks", sent), ("At gateway", got), ("Checked, stored", got),
                     ("Open export, hourly", hourly), ("Map and kiosk", "10 min redraw")],
          "losses": [(0, "Collisions and downlink blanking, 0.61 %", lost), (2, "Rolled up to hourly", got - hourly)]},
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
