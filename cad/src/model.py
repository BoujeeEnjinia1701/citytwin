"""CityTwin parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    citytwin-kiosk-assembly   the whole public kiosk, BOM items 1 to 15
    kiosk-head                display head, window, e-paper, controller, buttons, notice plate, hood
    services-cabinet          cabinet with both DIN rails, mains protection, 12 V supply and TwinKit gateway
    post-and-base             post, base plate and anchors

CityTwin is mostly software. The physical part is the public kiosk: a steel post on a
base plate, a display head with a 13.3 in color e-paper screen at eye height, three push
buttons, a data notice plate and a sun and rain hood, and a lockable services cabinet on
the back of the post. The cabinet holds two TS35 DIN rails: the lower one carries the mains
protection and the 12 V supply; the upper one carries the TwinKit gateway exactly as
TwinKit lays it out (TWK-DWG-001: terminals and fuse, 9-module enclosure, 2-module DC-DC
converter, 4-module UPS with the LiFePO4 pack inside). The TwinKit whip is replaced by a
coax lead to the post-top antenna.

Axes: X across the kiosk face, Y from the reading side (-Y) to the back (+Y), Z up.
Units mm. Sidewalk surface at Z = 0. Main dimensions and interfaces only; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (CTW-CAL-001) and the GA sheet CTW-DWG-001.
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 base plate and anchors
    "base": (400.0, 400.0, 12.0), "anchor_pitch": 300.0, "anchor_d": 16.0, "anchor_proj": 40.0,
    # 2 post, square hollow section
    "post": 100.0, "post_t": 4.0, "post_top": 1760.0,
    # 3 display head enclosure (outer), wall thickness; mounted on the post front face
    "head_w": 460.0, "head_d": 100.0, "head_z0": 1040.0, "head_z1": 1720.0, "head_t": 2.0,
    # 4 window opening (width x height) and 6 mm polycarbonate
    "win_w": 240.0, "win_h": 320.0, "win_t": 6.0, "win_lap": 8.0,
    # 5 e-paper: active area 270.4 x 202.8 (portrait, so 202.8 wide), module outline and depth
    "epd_active": (202.8, 270.4), "epd_outline": (210.0, 290.0, 7.0), "screen_cz": 1460.0,
    # 6 controller board envelope
    "ctrl": (100.0, 22.0, 60.0),
    # 7 buttons: diameter, height of centers, spacing
    "btn_d": 24.0, "btn_z": 1120.0, "btn_pitch": 70.0,
    # 8 notice plate (w x h), bottom edge height
    "notice": (400.0, 100.0), "notice_z0": 1165.0,
    # 9 hood: width, forward reach from the post face, sheet, lip depth, cheek depth
    "hood_w": 500.0, "hood_reach": 240.0, "hood_t": 1.5, "hood_lip": 60.0, "hood_cheek": 120.0,
    # 10 services cabinet on the post back: width, depth, height, bottom, wall
    "cab_w": 360.0, "cab_d": 160.0, "cab_h": 460.0, "cab_z0": 300.0, "cab_t": 2.0,
    # DIN rails in the cabinet (TS35 x 7.5), height of rail centers
    "rail_len": 320.0, "rail_w": 35.0, "rail_h": 7.5, "rail_mains_z": 420.0, "rail_twk_z": 620.0,
    "module": 17.5,
    # 11 mains protection: RCBO 2 modules, type 2 SPD 2 modules; 12 12 V 60 W supply 3 modules
    "rcbo_mod": 2, "spd_mod": 2, "psu_mod": 3, "din_dev_h": 90.0, "din_dev_d": 60.0,
    # 13 TwinKit gateway per TWK-DWG-001: enclosure 9 modules x 90 x 60 above the rail,
    # DC-DC 2 modules, UPS 4 modules with a 60 x 60 x 40 pack inside
    "twk_enc_mod": 9, "twk_enc": (90.0, 60.0), "twk_psu_mod": 2, "twk_ups_mod": 4, "twk_tb_w": 25.4,
    # 14 antenna: bracket and whip length
    "ant_len": 600.0, "ant_d": 20.0,
    # 15 conduit
    "conduit_d": 32.0,
}


def derived(p=PARAMS):
    """Dimensions quoted by the calc note and the GA sheet, computed from PARAMS."""
    hy0 = -p["post"] / 2 - p["head_d"]          # head front face (reading side)
    head_area = 2 * (p["head_w"] * p["head_d"] + p["head_w"] * (p["head_z1"] - p["head_z0"])
                     + p["head_d"] * (p["head_z1"] - p["head_z0"])) / 1e6
    cab_area = 2 * (p["cab_w"] * p["cab_d"] + p["cab_w"] * p["cab_h"] + p["cab_d"] * p["cab_h"]) / 1e6
    m = p["module"]
    mains_used = (p["rcbo_mod"] + p["spd_mod"] + p["psu_mod"]) * m + 2 * 6.2
    twk_used = p["twk_tb_w"] + (p["twk_enc_mod"] + p["twk_psu_mod"] + p["twk_ups_mod"]) * m + 3 * 2.0
    return {
        "head_front_y": hy0,
        "head_front_area_m2": p["head_w"] * (p["head_z1"] - p["head_z0"]) / 1e6,
        "head_area_m2": head_area,
        "head_cz": (p["head_z0"] + p["head_z1"]) / 2,
        "hood_front_y": -p["post"] / 2 - p["hood_reach"],
        "hood_overhang": p["hood_reach"] - p["head_d"],      # beyond the head front face
        "win_area_m2": p["win_w"] * p["win_h"] / 1e6,
        "epd_active_area_m2": p["epd_active"][0] * p["epd_active"][1] / 1e6,
        "cab_area_m2": cab_area,
        "cab_y0": p["post"] / 2, "cab_y1": p["post"] / 2 + p["cab_d"],
        "cab_inner_w": p["cab_w"] - 2 * p["cab_t"],
        "mains_rail_used": mains_used, "twk_rail_used": twk_used,
        "antenna_tip_z": p["post_top"] + 20 + p["ant_len"],
        "head_side_overhang": p["head_w"] / 2 - p["post"] / 2,
        "hood_side_overhang": p["hood_w"] / 2 - p["post"] / 2,
    }


def _b():
    import build123d as b
    return b


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    b = _b()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def shell(x0, x1, y0, y1, z0, z1, t):
    """Closed hollow box with wall thickness t."""
    return box(x0, x1, y0, y1, z0, z1) - box(x0 + t, x1 - t, y0 + t, y1 - t, z0 + t, z1 - t)


def ycyl(x, y0, y1, z, r):
    """Cylinder along Y from y0 to y1."""
    b = _b()
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, abs(y1 - y0))


def zcyl(x, y, z0, z1, r):
    b = _b()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def build_parts(p=PARAMS):
    """Return [(bom, name, shape)] for BOM items 1 to 15."""
    D = derived(p)
    P2 = p["post"] / 2
    parts = []

    # 1 Base plate with four anchors
    bx, by, bt = p["base"]
    base = box(-bx / 2, bx / 2, -by / 2, by / 2, 0, bt)
    a = p["anchor_pitch"] / 2
    for x in (-a, a):
        for y in (-a, a):
            base = base + zcyl(x, y, bt, bt + p["anchor_proj"], p["anchor_d"] / 2) \
                + zcyl(x, y, bt, bt + 14, p["anchor_d"] * 0.9)          # nut and washer
    parts.append((1, "Base plate and anchors", base))

    # 2 Post: square hollow section with a cap
    t = p["post_t"]
    post = (box(-P2, P2, -P2, P2, bt, p["post_top"])
            - box(-P2 + t, P2 - t, -P2 + t, P2 - t, bt, p["post_top"] - 6)
            - box(-8, 8, P2 - t - 1, P2 + 1, 640, 700))                    # cable entry to the cabinet
    parts.append((2, "Post, 100 mm square steel", post))

    # 3 Display head: hollow, window opening, button holes, vents underneath
    hw, hy0, z0, z1 = p["head_w"] / 2, D["head_front_y"], p["head_z0"], p["head_z1"]
    head = shell(-hw, hw, hy0, -P2, z0, z1, p["head_t"])
    ww, wh, cz = p["win_w"] / 2, p["win_h"] / 2, p["screen_cz"]
    head = head - box(-ww, ww, hy0 - 1, hy0 + p["head_t"] + 1, cz - wh, cz + wh)
    for i in (-1, 0, 1):
        head = head - ycyl(i * p["btn_pitch"], hy0 - 1, hy0 + p["head_t"] + 1, p["btn_z"], p["btn_d"] / 2)
    for i in range(6):
        x = -150 + i * 60
        head = head - box(x, x + 30, hy0 + 15, -P2 - 15, z0 - 1, z0 + p["head_t"] + 1)
    parts.append((3, "Display head enclosure", head))

    # 4 Front window, inside the front wall, lapping the opening
    lap = p["win_lap"]
    wy0 = hy0 + p["head_t"]
    window = box(-ww - lap, ww + lap, wy0, wy0 + p["win_t"], cz - wh - lap, cz + wh + lap)
    parts.append((4, "Front window, polycarbonate", window))

    # 5 E-paper display module with driver board behind
    ow, oh, od = p["epd_outline"]
    ey0 = wy0 + p["win_t"] + 1
    display = (box(-ow / 2, ow / 2, ey0, ey0 + od, cz - oh / 2, cz + oh / 2)
               + box(-33, 33, ey0 + od, ey0 + od + 15, cz + 60, cz + 90))
    parts.append((5, "E-paper display, 13.3 in color", display))

    # 6 Kiosk controller on a bracket behind the display
    cw, cd, ch = p["ctrl"]
    cy0 = ey0 + od + 3
    controller = (box(-60, -60 + cw, cy0, cy0 + cd, cz - 60, cz)
                  + box(-60, -60 + cw, -P2 - p["head_t"] - 3, -P2 - p["head_t"], cz - 80, cz + 20))
    parts.append((6, "Kiosk controller", controller))

    # 7 Push buttons, proud of the front face
    buttons = None
    for i in (-1, 0, 1):
        s = ycyl(i * p["btn_pitch"], hy0 - 5, hy0 + 8, p["btn_z"], p["btn_d"] / 2)
        buttons = s if buttons is None else buttons + s
    parts.append((7, "Push buttons (3)", buttons))

    # 8 Data notice plate on the head front
    nw, nh = p["notice"]
    notice = box(-nw / 2, nw / 2, hy0 - 2, hy0, p["notice_z0"], p["notice_z0"] + nh)
    parts.append((8, "Data notice plate", notice))

    # 9 Hood: roof, front lip, side cheeks, LED strip under the lip
    hdw, ht = p["hood_w"] / 2, p["hood_t"]
    hf = D["hood_front_y"]
    hood = (box(-hdw, hdw, hf, -P2, z1, z1 + 14)
            + box(-hdw, hdw, hf, hf + ht * 8, z1 - p["hood_lip"], z1)
            + box(-hdw, -hdw + 12, hf, hf + p["hood_cheek"] - 30, z1 - p["hood_cheek"], z1)
            + box(hdw - 12, hdw, hf, hf + p["hood_cheek"] - 30, z1 - p["hood_cheek"], z1)
            + box(-150, 150, hf + 18, hf + 32, z1 - 70, z1 - 56))
    parts.append((9, "Sun and rain hood with light", hood))

    # 10 Services cabinet with back plate and both DIN rails; door handle and lock on the back
    cw2, cy_0, cy_1 = p["cab_w"] / 2, D["cab_y0"], D["cab_y1"]
    cz0, cz1 = p["cab_z0"], p["cab_z0"] + p["cab_h"]
    cab = shell(-cw2, cw2, cy_0, cy_1, cz0, cz1, p["cab_t"]) + box(-120, -90, cy_1, cy_1 + 12, 500, 560)
    ry0 = cy_0 + p["cab_t"]
    rl, rw, rh = p["rail_len"] / 2, p["rail_w"] / 2, p["rail_h"]
    for rz in (p["rail_mains_z"], p["rail_twk_z"]):
        cab = cab + box(-rl, rl, ry0, ry0 + rh, rz - rw, rz + rw)
    parts.append((10, "Services cabinet, lockable", cab))

    m = p["module"]
    dy0, dh, dd = ry0 + rh, p["din_dev_h"] / 2, p["din_dev_d"]
    rz = p["rail_mains_z"]
    x = -rl + 6
    protection = box(x, x + p["rcbo_mod"] * m, dy0, dy0 + dd, rz - dh, rz + dh)
    x += p["rcbo_mod"] * m + 2
    protection = protection + box(x, x + p["spd_mod"] * m, dy0, dy0 + dd, rz - dh, rz + dh)
    x += p["spd_mod"] * m + 4
    parts.append((11, "Mains protection (RCBO, surge)", protection))
    psu = box(x, x + p["psu_mod"] * m, dy0, dy0 + dd + 30, rz - dh, rz + dh)
    x += p["psu_mod"] * m + 4
    psu = psu + box(x, x + 12.4, dy0, dy0 + 45, rz - 25, rz + 25)             # 12 V terminals
    parts.append((12, "12 V DIN power supply", psu))

    # 13 TwinKit gateway on the upper rail, per TWK-DWG-001
    rz = p["rail_twk_z"]
    ed, eh = p["twk_enc"]
    x = -rl + 4
    gw = box(x, x + p["twk_tb_w"], dy0, dy0 + 45, rz - 25, rz + 25)              # terminals and fuse
    x += p["twk_tb_w"] + 2
    gw = gw + box(x, x + p["twk_enc_mod"] * m, dy0, dy0 + eh, rz - ed / 2, rz + ed / 2)
    x += p["twk_enc_mod"] * m + 2
    gw = gw + box(x, x + p["twk_psu_mod"] * m, dy0, dy0 + 55, rz - 45, rz + 45)
    x += p["twk_psu_mod"] * m + 2
    gw = gw + box(x, x + p["twk_ups_mod"] * m, dy0, dy0 + 65, rz - 45, rz + 45)
    parts.append((13, "TwinKit gateway with backup", gw))

    # 14 Antenna on a post-top bracket; coax runs down inside the post
    pt = p["post_top"]
    antenna = box(-30, 30, -30, 30, pt, pt + 20) + zcyl(0, 0, pt + 20, D["antenna_tip_z"], p["ant_d"] / 2)
    parts.append((14, "LoRaWAN antenna (TwinKit)", antenna))

    # 15 Conduit from the footing into the cabinet floor; cable entry from cabinet to post
    cr = p["conduit_d"] / 2
    conduit = zcyl(0, (cy_0 + cy_1) / 2, bt, cz0 + p["cab_t"], cr) + box(-8, 8, P2 - t, cy_0 + p["cab_t"], 640, 700)
    parts.append((15, "Conduit and cabling", conduit))
    return parts


GROUPS = {
    "citytwin-kiosk-assembly": list(range(1, 16)),
    "kiosk-head": [3, 4, 5, 6, 7, 8, 9],
    "services-cabinet": [10, 11, 12, 13],
    "post-and-base": [1, 2, 14, 15],
}


def assembly(p=PARAMS, items=None):
    from build123d import Compound
    items = items or GROUPS["citytwin-kiosk-assembly"]
    return Compound(children=[s for n, _, s in build_parts(p) if n in items])


if __name__ == "__main__":
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    for name, items in GROUPS.items():
        c = assembly(items=items)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"head front area {D['head_front_area_m2']:.3f} m2; cabinet area {D['cab_area_m2']:.3f} m2; "
          f"antenna tip {D['antenna_tip_z']:.0f} mm; mains rail used {D['mains_rail_used']:.0f} mm; "
          f"TwinKit rail used {D['twk_rail_used']:.0f} mm of {PARAMS['rail_len']:.0f}")
