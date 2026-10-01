"""CityTwin parametric model (build123d), TRL 3, constructable design (CTW-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks (overlaps and contacts)

Exports:
    citytwin-kiosk-assembly   the whole public kiosk, BOM items 1 to 15 and 19 to 21
    kiosk-head                head tray, front panel, window, e-paper, carrier, controller, buttons, notice plate, hood
    services-cabinet          cabinet with mounting plate, rails, mains protection, 12 V supply, TwinKit gateway and sun shield
    post-and-base             post, base plate, anchors, antenna and conduit

CityTwin is mostly software. The physical part is the public kiosk: a steel post welded to a
base plate, a display head with a 13.3 in color e-paper screen at eye height, three push
buttons, a data notice plate and a sun and rain hood, and a lockable services cabinet on the
back of the post. The cabinet's mounting plate holds two TS35 DIN rails: the lower one carries
the mains protection and the 12 V supply; the upper one carries the TwinKit gateway exactly as
TwinKit lays it out (TWK-DWG-001). The TwinKit whip is replaced by a coax lead to the
post-top antenna. On outdoor sites a ventilated aluminum sun shield (item 19, CTW-DDR-002)
stands 25 mm off the cabinet on four standoffs, with a back panel held by thumb screws.

Design for construction (CTW-DDR-003): the head is a folded tray screwed to blind rivet nuts in
the post, closed by a removable front panel; the window is bonded inside the front panel and
the e-paper is held against it by a carrier plate on studs, which also carries the driver
board and the controller; the hood is folded sheet screwed to the head top; the cabinet is
screwed to rivet nuts in the post and its rails sit on a mounting plate; cables pass through
grommeted 25 mm holes; the post is vented for galvanizing.

Axes: X across the kiosk face, Y from the reading side (-Y) to the back (+Y), Z up.
Units mm. Sidewalk surface at Z = 0. The same PARAMS feed docs/04-calcs/sizing.py
(CTW-CAL-001), the GA sheet CTW-DWG-001 and the build plan pictures (CTW-BLD-001).
"""
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 base plate and anchors
    "base": (400.0, 400.0, 12.0), "anchor_pitch": 300.0, "anchor_d": 16.0, "anchor_proj": 40.0,
    "anchor_hole": 18.0, "drain_hole": 25.0, "conduit_hole": 40.0,
    # 2 post, square hollow section with a 6 mm cap welded on top
    "post": 100.0, "post_t": 4.0, "post_top": 1760.0, "cap_t": 6.0,
    "rivnut_hole": 11.0, "post_screw_x": 25.0, "cable_hole": 25.0,
    "head_screw_z": (1100.0, 1660.0), "head_cable_z": 1380.0,
    "cab_screw_z": (360.0, 700.0), "cab_cable_z": 735.0,
    # 3 display head: folded tray (outer) plus a removable 2 mm front panel
    "head_w": 460.0, "head_d": 100.0, "head_z0": 1040.0, "head_z1": 1720.0, "head_t": 2.0,
    "head_flange": 15.0,
    # 4 window opening (width x height) and 6 mm polycarbonate, bonded with 1 mm glazing tape
    "win_w": 240.0, "win_h": 320.0, "win_t": 6.0, "win_lap": 8.0, "tape_t": 1.0, "foam_t": 1.0,
    # 5 e-paper: active area 270.4 x 202.8 (portrait, so 202.8 wide), module outline and depth
    "epd_active": (202.8, 270.4), "epd_outline": (210.0, 290.0, 7.0), "screen_cz": 1460.0,
    # 20 display carrier plate (2 mm aluminum) on eight M4 studs
    "carrier": (290.0, 370.0, 2.0), "stud_x": 138.0, "stud_dz": 178.0,
    # 6 controller board envelope
    "ctrl": (100.0, 22.0, 60.0),
    # 7 buttons: mounting hole, bezel diameter, height of centers, spacing
    "btn_hole": 19.2, "btn_d": 24.0, "btn_z": 1120.0, "btn_pitch": 70.0,
    # 8 notice plate (w x h), bottom edge height
    "notice": (400.0, 100.0), "notice_z0": 1165.0,
    # 9 hood: width, forward reach from the post face, sheet, lip depth, cheek depth
    "hood_w": 500.0, "hood_reach": 240.0, "hood_t": 1.5, "hood_lip": 60.0, "hood_cheek": 120.0,
    # 10 services cabinet on the post back: width, depth, height, bottom, wall
    "cab_w": 360.0, "cab_d": 160.0, "cab_h": 460.0, "cab_z0": 300.0, "cab_t": 2.0,
    # mounting plate inside the cabinet, on 10 mm standoffs
    "mplate": (340.0, 390.0, 2.0), "mplate_z0": 320.0, "mplate_off": 10.0,
    # DIN rails on the mounting plate (TS35 x 7.5), height of rail centers
    "rail_len": 320.0, "rail_w": 35.0, "rail_h": 7.5, "rail_mains_z": 420.0, "rail_twk_z": 620.0,
    "module": 17.5,
    # 11 mains protection: RCBO 2 modules, type 2 SPD 2 modules; 12 12 V 60 W supply 3 modules
    "rcbo_mod": 2, "spd_mod": 2, "psu_mod": 3, "din_dev_h": 90.0, "din_dev_d": 60.0,
    # 13 TwinKit gateway per TWK-DWG-001: enclosure 9 modules x 90 x 60 above the rail,
    # DC-DC 2 modules, UPS 4 modules with a 60 x 60 x 40 pack inside
    "twk_enc_mod": 9, "twk_enc": (90.0, 60.0), "twk_psu_mod": 2, "twk_ups_mod": 4, "twk_tb_w": 25.4,
    # 14 antenna: bracket plate, whip length
    "ant_len": 600.0, "ant_d": 20.0, "ant_bracket": (60.0, 6.0),
    # 15 conduit
    "conduit_d": 32.0,
    # 19 cabinet sun shield for outdoor sites (CTW-DDR-002): folded aluminum over the top and
    # both sides on four 25 mm standoffs, plus a back panel over the door on thumb screws
    "shield_gap": 25.0, "shield_t": 1.5, "shield_flange": 15.0,
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
        "shield_w": p["cab_w"] + 2 * (p["shield_gap"] + p["shield_t"]),
        "shield_y1": p["post"] / 2 + p["cab_d"] + p["shield_gap"] + p["shield_t"],
        "shield_z1": p["cab_z0"] + p["cab_h"] + p["shield_gap"] + p["shield_t"],
        "shield_h": p["cab_h"] + p["shield_gap"] + p["shield_t"],
        "win_y0": hy0 + p["head_t"] + p["tape_t"],                       # window front face
        "epd_y0": hy0 + p["head_t"] + p["tape_t"] + p["win_t"] + p["foam_t"],
        "carrier_y0": hy0 + p["head_t"] + p["tape_t"] + p["win_t"] + p["foam_t"] + p["epd_outline"][2],
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


def xcyl(x0, x1, y, z, r):
    """Cylinder along X from x0 to x1."""
    b = _b()
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, abs(x1 - x0))


def zcyl(x, y, z0, z1, r):
    b = _b()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def ytube(x, y0, y1, z, ro, ri):
    return ycyl(x, y0, y1, z, ro) - ycyl(x, y0 - 1, y1 + 1, z, ri)


def _fuse(shapes):
    out = None
    for s in shapes:
        if s is not None:
            out = s if out is None else out + s
    return out


def _screw_y(x, z, y_face, sign, head_d=14.0, head_h=4.4, washer_d=0.0, washer_t=0.0, shank=12.0, d=8.0):
    """A screw on a face normal to Y: head (and washer) on the side `sign` (+1 = toward +Y) of
    y_face, shank going the other way. Returns (head_and_washer, shank)."""
    parts = []
    y = y_face
    if washer_t:
        parts.append(ycyl(x, y, y + sign * washer_t, z, washer_d / 2)); y += sign * washer_t
    parts.append(ycyl(x, y, y + sign * head_h, z, head_d / 2))
    return _fuse(parts), ycyl(x, y_face, y_face - sign * shank, z, d / 2)


# ------------------------------------------------------------------------------------------------
def build_components(p=PARAMS, shield=True):
    """Every component of the constructable kiosk as {key: (bom, name, shape)}."""
    D = derived(p)
    P2, t = p["post"] / 2, p["post_t"]
    C = {}

    def add(key, bom, name, shape):
        C[key] = (bom, name, shape)

    # ---- 1 base plate, anchors (projecting part), nuts and washers
    bx, by, bt = p["base"]
    a = p["anchor_pitch"] / 2
    plate = box(-bx / 2, bx / 2, -by / 2, by / 2, 0, bt)
    for x in (-a, a):
        for y in (-a, a):
            plate = plate - zcyl(x, y, -1, bt + 1, p["anchor_hole"] / 2)
    plate = plate - zcyl(0, 0, -1, bt + 1, p["drain_hole"] / 2)
    cy_mid = P2 + p["cab_d"] / 2
    plate = plate - zcyl(0, cy_mid, -1, bt + 1, p["conduit_hole"] / 2)
    add("base", 1, "Base plate", plate)
    anchors, nuts = [], []
    for x in (-a, a):
        for y in (-a, a):
            anchors.append(zcyl(x, y, 0, bt + p["anchor_proj"], p["anchor_d"] / 2))
            nuts.append(zcyl(x, y, bt, bt + 3, 17) + zcyl(x, y, bt + 3, bt + 16, 13) - zcyl(x, y, bt - 1, bt + 17, p["anchor_d"] / 2))
    add("anchors", 1, "Anchors (4)", _fuse(anchors))
    add("anchor_nuts", 1, "Anchor nuts and washers", _fuse(nuts))

    # ---- 2 post: tube, cap; rivet-nut holes, cable holes
    ztop = p["post_top"] - p["cap_t"]
    tube = box(-P2, P2, -P2, P2, bt, ztop) - box(-P2 + t, P2 - t, -P2 + t, P2 - t, bt - 1, ztop + 1)
    sx, rh = p["post_screw_x"], p["rivnut_hole"] / 2
    for z in p["head_screw_z"]:
        for x in (-sx, sx):
            tube = tube - ycyl(x, -P2 - 1, -P2 + t + 1, z, rh)
    for z in p["cab_screw_z"]:
        for x in (-sx, sx):
            tube = tube - ycyl(x, P2 - t - 1, P2 + 1, z, rh)
    tube = tube - ycyl(0, -P2 - 1, -P2 + t + 1, p["head_cable_z"], p["cable_hole"] / 2)
    tube = tube - ycyl(0, P2 - t - 1, P2 + 1, p["cab_cable_z"], p["cable_hole"] / 2)
    add("post", 2, "Post", tube)
    cap = box(-P2, P2, -P2, P2, ztop, p["post_top"]) - zcyl(0, 0, ztop - 1, p["post_top"] + 1, 10)
    for x in (-20, 20):
        for y in (-20, 20):
            cap = cap - zcyl(x, y, ztop - 1, p["post_top"] + 1, 2.1)       # M5 tapping holes
    add("cap", 2, "Post cap", cap)

    # ---- 3 display head: tray (back wall, top, bottom, sides, front return flange)
    hw, hy0, z0, z1, ht = p["head_w"] / 2, D["head_front_y"], p["head_z0"], p["head_z1"], p["head_t"]
    ty0 = hy0 + ht                                        # tray front plane (behind the front panel)
    tray = box(-hw, hw, ty0, -P2, z0, z1) - box(-hw + ht, hw - ht, ty0 - 1, -P2 - ht, z0 + ht, z1 - ht)
    f = p["head_flange"]
    flange = (box(-hw, hw, ty0, ty0 + ht, z0, z1) - box(-hw + f, hw - f, ty0 - 1, ty0 + ht + 1, z0 + f, z1 - f))
    tray = tray + flange
    for i in range(6):                                     # vent slots underneath
        x = -150 + i * 60
        tray = tray - box(x, x + 30, hy0 + 15, -P2 - 15, z0 - 1, z0 + ht + 1)
    for z in p["head_screw_z"]:
        for x in (-sx, sx):
            tray = tray - ycyl(x, -P2 - ht - 1, -P2 + 1, z, 4.5)
    tray = tray - ycyl(0, -P2 - ht - 1, -P2 + 1, p["head_cable_z"], p["cable_hole"] / 2)
    hood_pts = [(x, y) for x in (-150, 150) for y in (-120, -80)]
    for x, y in hood_pts:
        tray = tray - zcyl(x, y, z1 - ht - 1, z1 + 1, 3.5)          # M5 rivet nut holes, 7 mm
    fpos = HEAD_PANEL_SCREWS(p)
    for x, z in fpos:
        tray = tray - ycyl(x, ty0 - 1, ty0 + ht + 1, z, 3.0)        # M4 rivet nut holes, 6 mm
    add("tray", 3, "Head tray", tray)

    # front panel with window opening, button holes, notice plate holes, screw holes, studs
    ww, wh, cz = p["win_w"] / 2, p["win_h"] / 2, p["screen_cz"]
    fp = box(-hw, hw, hy0, ty0, z0, z1) - box(-ww, ww, hy0 - 1, ty0 + 1, cz - wh, cz + wh)
    for i in (-1, 0, 1):
        fp = fp - ycyl(i * p["btn_pitch"], hy0 - 1, ty0 + 1, p["btn_z"], p["btn_hole"] / 2)
    for x, z in NOTICE_HOLES(p):
        fp = fp - ycyl(x, hy0 - 1, ty0 + 1, z, 2.25)
    for x, z in fpos:
        fp = fp - ycyl(x, hy0 - 1, ty0 + 1, z, 2.25)
    fp = fp - ycyl(LED_GROMMET[0], hy0 - 1, ty0 + 1, LED_GROMMET[1], 6.5)   # LED cable grommet, 13 mm, under the hood
    add("front_panel", 3, "Head front panel", fp)
    studs = _fuse([ycyl(x, ty0, ty0 + 25, z, 2.0) for x, z in STUDS(p)])
    add("studs", 3, "Clinch studs M4 (8)", studs)

    # ---- 4 window bonded inside the front panel with glazing tape
    lap = p["win_lap"]
    wy0 = D["win_y0"]
    tape = box(-ww - lap, ww + lap, ty0, wy0, cz - wh - lap, cz + wh + lap) - box(-ww, ww, ty0 - 1, wy0 + 1, cz - wh, cz + wh)
    add("tape", 21, "Glazing tape", tape)
    window = box(-ww - lap, ww + lap, wy0, wy0 + p["win_t"], cz - wh - lap, cz + wh + lap)
    add("window", 4, "Front window", window)

    # ---- 5 e-paper panel behind a foam gasket; driver board on the carrier
    ow, oh, od = p["epd_outline"]
    ey0 = D["epd_y0"]
    foam = box(-ow / 2, ow / 2, ey0 - p["foam_t"], ey0, cz - oh / 2, cz + oh / 2) - box(-ow / 2 + 4, ow / 2 - 4, ey0 - 2, ey0 + 1, cz - oh / 2 + 4, cz + oh / 2 - 4)
    add("foam", 21, "Foam gasket", foam)
    add("epd", 5, "E-paper panel", box(-ow / 2, ow / 2, ey0, ey0 + od, cz - oh / 2, cz + oh / 2))

    # ---- 20 display carrier plate on the studs, with spacers
    cw_, ch_, ct = p["carrier"]
    cy0 = D["carrier_y0"]
    carrier = box(-cw_ / 2, cw_ / 2, cy0, cy0 + ct, cz - ch_ / 2, cz + ch_ / 2)
    for x, z in STUDS(p):
        carrier = carrier - ycyl(x, cy0 - 1, cy0 + ct + 1, z, 2.25)
    carrier = carrier - box(-35, 35, cy0 - 1, cy0 + ct + 1, cz + oh / 2 - 12, cz + oh / 2 - 4)   # ribbon slot
    add("carrier", 20, "Display carrier", carrier)
    add("spacers", 21, "Stud spacers (8)", _fuse([ytube(x, ty0, cy0, z, 4.0, 2.2) for x, z in STUDS(p)]))
    add("stud_nuts", 21, "Stud nuts (8)", _fuse([ytube(x, cy0 + ct, cy0 + ct + 3.2, z, 3.5, 2.0) for x, z in STUDS(p)]))
    by0 = cy0 + ct
    so = []
    drv = box(-33, 33, by0 + 5, by0 + 20, cz + 60, cz + 116)
    for x in (-28, 28):
        for z in (cz + 64, cz + 112):
            so.append(ycyl(x, by0, by0 + 5, z, 2.5))
    cw, cd, ch = p["ctrl"]
    ctrl = box(-60, -60 + cw, by0 + 5, by0 + 5 + cd, cz - 90, cz - 30)
    for x in (-55, 35):
        for z in (cz - 85, cz - 35):
            so.append(ycyl(x, by0, by0 + 5, z, 2.5))
    # 12 V to 5 V converter, LED driver module and pluggable terminal block beside the controller
    conv = box(55, 100, by0 + 5, by0 + 20, cz - 90, cz - 64)
    ledd = box(55, 100, by0 + 5, by0 + 17, cz - 56, cz - 30)
    term = box(-110, -70, by0, by0 + 18, cz - 150, cz - 130)
    for x in (60, 95):
        for z in (cz - 77, cz - 43):
            so.append(ycyl(x, by0, by0 + 5, z, 2.5))
    add("driver", 5, "E-paper driver board", drv)
    add("controller", 6, "Kiosk controller", ctrl)
    add("power_mods", 6, "5 V converter and LED driver", conv + ledd)
    add("terminal", 6, "Pluggable terminal block", term)
    add("standoffs", 21, "Board standoffs (12)", _fuse(so))

    # ---- 7 push buttons: bezel outside, body through the panel, nut inside
    bez, body, bnut = [], [], []
    for i in (-1, 0, 1):
        x = i * p["btn_pitch"]
        bez.append(ycyl(x, hy0 - 3, hy0, p["btn_z"], p["btn_d"] / 2))
        body.append(ycyl(x, hy0, ty0 + 35, p["btn_z"], 9.4))
        bnut.append(ytube(x, ty0, ty0 + 4, p["btn_z"], 13, 9.6))
    add("buttons", 7, "Push buttons (3)", _fuse(bez) + _fuse(body))
    add("button_nuts", 7, "Button nuts (3)", _fuse(bnut))

    # ---- 8 notice plate on the front panel, four M4 security screws with nuts inside
    nw, nh = p["notice"]
    notice = box(-nw / 2, nw / 2, hy0 - 2, hy0, p["notice_z0"], p["notice_z0"] + nh)
    for x, z in NOTICE_HOLES(p):
        notice = notice - ycyl(x, hy0 - 3, hy0 + 1, z, 2.25)
    add("notice", 8, "Data notice plate", notice)
    ns = []
    for x, z in NOTICE_HOLES(p):
        ns.append(ycyl(x, hy0 - 4.5, hy0 - 2, z, 3.8) + ycyl(x, hy0 - 2, ty0 + 8, z, 2.0) + ytube(x, ty0, ty0 + 5, z, 3.8, 2.0))
    add("notice_fix", 21, "Notice plate screws (4)", _fuse(ns))

    # ---- front panel screws into rivet nuts in the tray flange
    fs, fr = [], []
    for x, z in fpos:
        fs.append(ycyl(x, hy0 - 3, hy0, z, 3.8) + ycyl(x, hy0, ty0 + ht + 8, z, 1.95))
        fr.append(ytube(x, ty0, ty0 + ht, z, 3.0, 2.0) + ytube(x, ty0 + ht, ty0 + ht + 9, z, 3.0, 2.0))
    add("panel_screws", 21, "Front panel screws (12)", _fuse(fs))
    add("panel_rivnuts", 21, "Front panel rivet nuts (12)", _fuse(fr))

    # ---- head to post: four M8 screws with penny washers through the tray back into rivet nuts in the post
    hs, hr = [], []
    for z in p["head_screw_z"]:
        for x in (-sx, sx):
            w, _ = _screw_y(x, z, -P2 - ht, -1, washer_d=30, washer_t=3)
            hs.append(w + ycyl(x, -P2 - ht, -P2 + 14, z, 4.0))
            hr.append(ytube(x, -P2, -P2 + t + 11, z, rh - 0.01, 4.0))
    add("head_screws", 21, "Head screws and washers (4)", _fuse(hs))
    add("head_rivnuts", 21, "Post rivet nuts, head (4)", _fuse(hr))

    # ---- 9 hood: roof, front lip, cheeks, LED angle; four M5 screws into rivet nuts in the tray top
    hdw, hth = p["hood_w"] / 2, p["hood_t"]
    hf = D["hood_front_y"]
    roof = box(-hdw, hdw, hf, -P2, z1, z1 + hth)
    lip = box(-hdw, hdw, hf, hf + hth, z1 - p["hood_lip"], z1)
    cheeks = (box(-hdw, -hdw + hth, hf + hth, hf + p["hood_cheek"] - 30, z1 - p["hood_cheek"], z1)
              + box(hdw - hth, hdw, hf + hth, hf + p["hood_cheek"] - 30, z1 - p["hood_cheek"], z1))
    hood = roof + lip + cheeks
    for x, y in hood_pts:
        hood = hood - zcyl(x, y, z1 - 1, z1 + hth + 1, 2.75)
    add("hood", 9, "Hood", hood)
    led = (box(-150, 150, hf + 20, hf + 40, z1 - 1.5, z1) + box(-150, 150, hf + 20, hf + 21.5, z1 - 20, z1 - 1.5)
           + box(-145, 145, hf + 21.5, hf + 23, z1 - 15, z1 - 5))
    add("led", 9, "LED strip on its angle", led)
    hsc, hrn = [], []
    for x, y in hood_pts:
        hsc.append(zcyl(x, y, z1 + hth, z1 + hth + 3.5, 4.75) + zcyl(x, y, z1 - ht, z1 + hth, 2.5))
        hrn.append(zcyl(x, y, z1 - ht - 10, z1, 3.5) - zcyl(x, y, z1 - ht - 11, z1 + 1, 2.5))
    add("hood_screws", 21, "Hood screws (4)", _fuse(hsc))
    add("hood_rivnuts", 21, "Head top rivet nuts (4)", _fuse(hrn))

    # ---- 10 services cabinet (bought, drilled), mounting plate on standoffs, DIN rails
    cw2, cy_0, cy_1 = p["cab_w"] / 2, D["cab_y0"], D["cab_y1"]
    cz0, cz1, cbt = p["cab_z0"], p["cab_z0"] + p["cab_h"], p["cab_t"]
    cab = shell(-cw2, cw2, cy_0, cy_1, cz0, cz1, cbt) + box(-120, -90, cy_1, cy_1 + 12, 500, 560)
    for z in p["cab_screw_z"]:
        for x in (-sx, sx):
            cab = cab - ycyl(x, cy_0 - 1, cy_0 + cbt + 1, z, 4.5)
    cab = cab - ycyl(0, cy_0 - 1, cy_0 + cbt + 1, p["cab_cable_z"], p["cable_hole"] / 2)
    cab = cab - zcyl(0, cy_mid, cz0 - 1, cz0 + cbt + 1, 16.25)
    for xs in (-1, 1):
        for y, z in SHIELD_STANDOFFS(p):
            cab = cab - xcyl(xs * cw2 - 3, xs * cw2 + 3, y, z, 3.25)
    add("cabinet", 10, "Services cabinet", cab)
    mw, mh, mt = p["mplate"]
    my0 = cy_0 + cbt + p["mplate_off"]
    mz0 = p["mplate_z0"]
    mpl = box(-mw / 2, mw / 2, my0, my0 + mt, mz0, mz0 + mh)
    mso = _fuse([ycyl(x, cy_0 + cbt, my0, z, 5) for x in (-155, 155) for z in (mz0 + 15, mz0 + mh - 15)])
    ry0 = my0 + mt
    rl, rw, rh_ = p["rail_len"] / 2, p["rail_w"] / 2, p["rail_h"]
    rails = _fuse([box(-rl, rl, ry0, ry0 + rh_, rz - rw, rz + rw) for rz in (p["rail_mains_z"], p["rail_twk_z"])])
    add("mplate", 10, "Mounting plate", mpl + mso)
    add("rails", 10, "DIN rails (2)", rails)
    cs, cr = [], []
    for z in p["cab_screw_z"]:
        for x in (-sx, sx):
            w, _ = _screw_y(x, z, cy_0 + cbt, 1, washer_d=30, washer_t=3)
            cs.append(w + ycyl(x, P2 - 14, cy_0 + cbt, z, 4.0))
            cr.append(ytube(x, P2 - t - 11, P2, z, rh - 0.01, 4.0))
    add("cab_screws", 21, "Cabinet screws and washers (4)", _fuse(cs))
    add("cab_rivnuts", 21, "Post rivet nuts, cabinet (4)", _fuse(cr))

    m = p["module"]
    dy0, dh, dd = ry0 + rh_, p["din_dev_h"] / 2, p["din_dev_d"]
    rz = p["rail_mains_z"]
    x = -rl + 6
    prot = box(x, x + p["rcbo_mod"] * m, dy0, dy0 + dd, rz - dh, rz + dh)
    x += p["rcbo_mod"] * m + 2
    prot = prot + box(x, x + p["spd_mod"] * m, dy0, dy0 + dd, rz - dh, rz + dh)
    x += p["spd_mod"] * m + 4
    add("protection", 11, "Mains protection", prot)
    psu = box(x, x + p["psu_mod"] * m, dy0, dy0 + dd + 30, rz - dh, rz + dh)
    x += p["psu_mod"] * m + 4
    psu = psu + box(x, x + 12.4, dy0, dy0 + 45, rz - 25, rz + 25)
    add("psu", 12, "12 V power supply", psu)

    # ---- 13 TwinKit gateway on the upper rail, per TWK-DWG-001
    rz = p["rail_twk_z"]
    ed, eh = p["twk_enc"]
    x = -rl + 4
    gw = box(x, x + p["twk_tb_w"], dy0, dy0 + 45, rz - 25, rz + 25)
    x += p["twk_tb_w"] + 2
    gw = gw + box(x, x + p["twk_enc_mod"] * m, dy0, dy0 + eh, rz - ed / 2, rz + ed / 2)
    x += p["twk_enc_mod"] * m + 2
    gw = gw + box(x, x + p["twk_psu_mod"] * m, dy0, dy0 + 55, rz - 45, rz + 45)
    x += p["twk_psu_mod"] * m + 2
    gw = gw + box(x, x + p["twk_ups_mod"] * m, dy0, dy0 + 65, rz - 45, rz + 45)
    add("gateway", 13, "TwinKit gateway", gw)

    # ---- 14 antenna bracket plate on the cap (four M5 screws), antenna base and whip
    pt = p["post_top"]
    bw, bth = p["ant_bracket"]
    br = box(-bw / 2, bw / 2, -bw / 2, bw / 2, pt, pt + bth) - zcyl(0, 0, pt - 1, pt + bth + 1, 8.25)
    for xx in (-20, 20):
        for yy in (-20, 20):
            br = br - zcyl(xx, yy, pt - 1, pt + bth + 1, 2.75)
    add("ant_bracket", 14, "Antenna bracket", br)
    ant = zcyl(0, 0, pt + bth, pt + 20, 15) + zcyl(0, 0, pt + 20, D["antenna_tip_z"], p["ant_d"] / 2) \
        + zcyl(0, 0, pt - 14, pt + bth, 8.0)
    ant = ant + (zcyl(0, 0, pt - 20, pt - 14, 9.5) - zcyl(0, 0, pt - 21, pt - 13, 8.0))   # bulkhead nut under the cap
    add("antenna", 14, "Antenna", ant)
    add("ant_screws", 21, "Bracket screws (4)", _fuse([zcyl(xx, yy, pt + bth, pt + bth + 3.5, 4.75) + zcyl(xx, yy, pt - 4, pt + bth, 2.05)
                                                      for xx in (-20, 20) for yy in (-20, 20)]))

    # ---- 15 conduit through the base plate into a gland in the cabinet floor; grommets
    cr_ = p["conduit_d"] / 2
    conduit = zcyl(0, cy_mid, -60, cz0, cr_) + (zcyl(0, cy_mid, cz0 + cbt, cz0 + cbt + 10, 22) - zcyl(0, cy_mid, cz0, cz0 + cbt + 11, 16.25))
    add("conduit", 15, "Conduit and gland", conduit)
    gr = (ytube(0, cy_0 + cbt, cy_0 + cbt + 3, p["cab_cable_z"], 17, 9) + ytube(0, P2 - t - 3, P2 - t, p["cab_cable_z"], 17, 9)
          + ytube(0, -P2 - ht - 3, -P2 - ht, p["head_cable_z"], 17, 9) + ytube(0, -P2 + t, -P2 + t + 3, p["head_cable_z"], 17, 9))
    lx, lz = LED_GROMMET
    gr = gr + ((ycyl(lx, hy0 - 2, hy0, lz, 9) + ycyl(lx, hy0, ty0, lz, 6.5) + ycyl(lx, ty0, ty0 + 2, lz, 9))
               - ycyl(lx, hy0 - 3, ty0 + 3, lz, 3))
    add("grommets", 15, "Cable grommets (5)", gr)

    # ---- 19 sun shield (outdoor sites): hood piece on four standoffs, back panel on thumb screws
    if shield:
        st, sw = p["shield_t"], D["shield_w"] / 2
        sy1, sz1 = D["shield_y1"], D["shield_z1"]
        sfl = p["shield_flange"]
        top = box(-sw, sw, cy_0, sy1, sz1 - st, sz1)
        sides = box(-sw, -sw + st, cy_0, sy1 - st, cz0, sz1 - st) + box(sw - st, sw, cy_0, sy1 - st, cz0, sz1 - st)
        fl = box(-sw + st, -sw + st + sfl, sy1 - 2 * st, sy1 - st, cz0, sz1 - st) + box(sw - st - sfl, sw - st, sy1 - 2 * st, sy1 - st, cz0, sz1 - st)
        sh = top + sides + fl
        for xs in (-1, 1):
            for y, z in SHIELD_STANDOFFS(p):
                sh = sh - xcyl(xs * sw - 3, xs * sw + 3, y, z, 3.25)
            for z in BACKPANEL_Z:
                sh = sh - ycyl(xs * (sw - st - sfl / 2), sy1 - 2 * st - 1, sy1 - st + 1, z, 3.5)
        add("shield", 19, "Sun shield", sh)
        bp = box(-sw, sw, sy1 - st, sy1, cz0, sz1 - st)
        for i in range(4):
            xs_ = -150 + i * 80
            bp = bp - box(xs_, xs_ + 60, sy1 - st - 1, sy1 + 1, sz1 - 60, sz1 - 45)
        for xs in (-1, 1):
            for z in BACKPANEL_Z:
                bp = bp - ycyl(xs * (sw - st - sfl / 2), sy1 - st - 1, sy1 + 1, z, 3.25)
        add("backpanel", 19, "Shield back panel", bp)
        sto = []
        for xs in (-1, 1):
            for y, z in SHIELD_STANDOFFS(p):
                sto.append(xcyl(xs * cw2, xs * (sw - st), y, z, 5.0))
                sto.append(xcyl(xs * (sw + 3.5), xs * sw, y, z, 5.0))                  # screw heads outside
                sto.append(xcyl(xs * (cw2 - cbt - 4), xs * (cw2 - cbt), y, z, 5.0))     # bolt heads inside
                sto.append(xcyl(xs * (cw2 - cbt), xs * cw2, y, z, 3.0))                  # bolt shank in the wall
                sto.append(xcyl(xs * (sw - st), xs * sw, y, z, 3.0))                     # screw shank in the shield
        add("standoffs_sh", 19, "Shield standoffs (4)", _fuse(sto))
        th = []
        for xs in (-1, 1):
            for z in BACKPANEL_Z:
                xx = xs * (sw - st - sfl / 2)
                th.append(ycyl(xx, sy1, sy1 + 8, z, 7) + ycyl(xx, sy1 - 2 * st - 8, sy1, z, 2.5))
        add("thumbs", 19, "Thumb screws (4)", _fuse(th))
    return C


def HEAD_PANEL_SCREWS(p=PARAMS):
    hw, z0, z1, f = p["head_w"] / 2, p["head_z0"], p["head_z1"], p["head_flange"]
    out = [(x, z) for x in (-160, 0, 160) for z in (z0 + f / 2, z1 - f / 2)]
    out += [(x, z) for x in (-hw + f / 2, hw - f / 2) for z in (1160, 1380, 1600)]
    return out


def NOTICE_HOLES(p=PARAMS):
    nw, nh = p["notice"]
    return [(x, z) for x in (-nw / 2 + 10, nw / 2 - 10) for z in (p["notice_z0"] + 12, p["notice_z0"] + nh - 12)]


def STUDS(p=PARAMS):
    sx, dz, cz = p["stud_x"], p["stud_dz"], p["screen_cz"]
    return [(-sx, cz - dz), (0, cz - dz), (sx, cz - dz), (-sx, cz), (sx, cz), (-sx, cz + dz), (0, cz + dz), (sx, cz + dz)]


def SHIELD_STANDOFFS(p=PARAMS):
    """(y, z) of the two standoffs on each cabinet side, at mid-depth, low and high."""
    y = p["post"] / 2 + p["cab_d"] / 2
    return [(y, 420.0), (y, 680.0)]


BACKPANEL_Z = (400.0, 700.0)
LED_GROMMET = (140.0, 1685.0)        # x, z on the front panel, above the window, under the hood roof


def build_parts(p=PARAMS, shield=True):
    """Return [(bom, name, shape)], one entry per BOM item (used by the calc note and the concept media)."""
    names = {1: "Base plate and anchors", 2: "Post, 100 mm square steel", 3: "Display head enclosure",
             4: "Front window, polycarbonate", 5: "E-paper display, 13.3 in color", 6: "Kiosk controller",
             7: "Push buttons (3)", 8: "Data notice plate", 9: "Sun and rain hood with light",
             10: "Services cabinet, lockable", 11: "Mains protection (RCBO, surge)", 12: "12 V DIN power supply",
             13: "TwinKit gateway with backup", 14: "LoRaWAN antenna and bracket", 15: "Conduit and cabling",
             19: "Cabinet sun shield (outdoor sites)", 20: "Display carrier", 21: "Fixings, tapes and gaskets"}
    groups = {}
    for _, (n, _, s) in build_components(p, shield).items():
        groups.setdefault(n, []).append(s)
    return [(n, names[n], _fuse(groups[n])) for n in sorted(groups)]


GROUPS = {
    "citytwin-kiosk-assembly": list(range(1, 16)) + [19, 20, 21],
    "kiosk-head": [3, 4, 5, 6, 7, 8, 9, 20],
    "services-cabinet": [10, 11, 12, 13, 19],
    "post-and-base": [1, 2, 14, 15],
}


def assembly(p=PARAMS, items=None):
    from build123d import Compound
    items = items or GROUPS["citytwin-kiosk-assembly"]
    return Compound(children=[s for n, _, s in build_parts(p) if n in items])


# ------------------------------------------------------------------------------------------------
# Constructability checks (CTW-DDR-003): parts that must touch do touch, and no two parts overlap.
TOUCH = [
    ("base", "post", "post stands on the base plate (fillet weld all round)"),
    ("post", "cap", "cap welded on the post top"),
    ("anchor_nuts", "base", "anchor washers bear on the base plate"),
    ("cabinet", "post", "cabinet back on the post back face"),
    ("cab_screws", "cabinet", "cabinet screw washers bear on the cabinet back wall"),
    ("cab_rivnuts", "post", "rivet nuts set in the post back wall"),
    ("mplate", "cabinet", "mounting plate standoffs on the cabinet back wall"),
    ("rails", "mplate", "DIN rails on the mounting plate"),
    ("protection", "rails", "RCBO and surge protector clipped on the lower rail"),
    ("psu", "rails", "12 V supply clipped on the lower rail"),
    ("gateway", "rails", "TwinKit gateway clipped on the upper rail"),
    ("conduit", "cabinet", "conduit gland in the cabinet floor"),
    ("tray", "post", "head tray back on the post front face"),
    ("head_screws", "tray", "head screw washers bear on the tray back wall"),
    ("head_rivnuts", "post", "rivet nuts set in the post front wall"),
    ("hood", "tray", "hood roof sits on the tray top"),
    ("hood_screws", "hood", "hood screws bear on the roof"),
    ("hood_rivnuts", "tray", "rivet nuts set in the tray top"),
    ("led", "hood", "LED angle riveted under the roof"),
    ("front_panel", "tray", "front panel on the tray flange"),
    ("panel_screws", "front_panel", "panel screws bear on the front panel"),
    ("panel_rivnuts", "tray", "rivet nuts set in the tray flange"),
    ("studs", "front_panel", "studs pressed into the front panel"),
    ("tape", "front_panel", "glazing tape on the panel"),
    ("window", "tape", "window on the glazing tape"),
    ("foam", "window", "foam gasket on the window"),
    ("epd", "foam", "e-paper panel on the foam gasket"),
    ("carrier", "epd", "carrier presses the e-paper panel"),
    ("spacers", "front_panel", "spacers on the front panel"),
    ("spacers", "carrier", "carrier on the spacers"),
    ("stud_nuts", "carrier", "nuts clamp the carrier"),
    ("standoffs", "carrier", "board standoffs on the carrier"),
    ("driver", "standoffs", "driver board on its standoffs"),
    ("controller", "standoffs", "controller on its standoffs"),
    ("power_mods", "standoffs", "converter and LED driver on their standoffs"),
    ("terminal", "carrier", "terminal block on the carrier"),
    ("grommets", "front_panel", "LED cable grommet in the front panel"),
    ("buttons", "front_panel", "button bezels on the front panel"),
    ("button_nuts", "front_panel", "button nuts clamp the front panel"),
    ("notice", "front_panel", "notice plate on the front panel"),
    ("notice_fix", "notice", "notice screws bear on the plate"),
    ("ant_bracket", "cap", "antenna bracket on the cap"),
    ("ant_screws", "ant_bracket", "bracket screws bear on the bracket"),
    ("antenna", "ant_bracket", "antenna base on the bracket"),
    ("grommets", "cabinet", "grommet in the cabinet back wall"),
    ("grommets", "tray", "grommet in the tray back wall"),
    ("standoffs_sh", "cabinet", "shield standoffs on the cabinet sides"),
    ("standoffs_sh", "shield", "shield sides on the standoffs"),
    ("backpanel", "shield", "back panel on the shield flanges"),
    ("thumbs", "backpanel", "thumb screws bear on the back panel"),
]
CLEAR = [  # pairs that must stay apart by at least this gap (mm)
    ("shield", "cabinet", 20.0, "25 mm air gap round the cabinet"),
    ("backpanel", "cabinet", 10.0, "air gap behind the door handle"),
    ("hood", "buttons", 400.0, "hood well above the buttons"),
    ("carrier", "tray", 10.0, "carrier clear of the tray walls"),
    ("controller", "tray", 10.0, "controller clear of the tray"),
    ("gateway", "cabinet", 10.0, "gateway clear of the door"),
    ("psu", "cabinet", 10.0, "supply clear of the door"),
    ("conduit", "post", 20.0, "conduit clear of the post"),
    ("buttons", "notice", 20.0, "buttons clear of the notice plate"),
    ("led", "front_panel", 50.0, "LED strip clear of the screen"),
]


def check(p=PARAMS):
    C = build_components(p, shield=True)
    keys = list(C)
    fails, n = [], 0
    bbs = {k: C[k][2].bounding_box() for k in keys}

    def bbo(a, b, tol=0.5):
        A, B = bbs[a], bbs[b]
        return not (A.max.X < B.min.X - tol or B.max.X < A.min.X - tol or A.max.Y < B.min.Y - tol or
                    B.max.Y < A.min.Y - tol or A.max.Z < B.min.Z - tol or B.max.Z < A.min.Z - tol)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if not bbo(a, b):
                continue
            n += 1
            v = (C[a][2] & C[b][2]).volume
            if v > 0.5:
                fails.append(f"OVERLAP {a} / {b}: {v:.1f} mm3")
    for a, b, why in TOUCH:
        n += 1
        d = C[a][2].distance_to(C[b][2])
        if d > 0.05:
            fails.append(f"NO CONTACT {a} / {b} ({why}): gap {d:.2f} mm")
    for a, b, g, why in CLEAR:
        n += 1
        d = C[a][2].distance_to(C[b][2])
        if d < g:
            fails.append(f"TOO CLOSE {a} / {b} ({why}): {d:.1f} mm < {g} mm")
    for f_ in fails:
        print(f_)
    print(f"{n} constructability checks, {len(fails)} failed")
    return not fails


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(0 if check() else 1)
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    for name, items in GROUPS.items():
        c = assembly(items=items)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.5)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"head front area {D['head_front_area_m2']:.3f} m2; cabinet area {D['cab_area_m2']:.3f} m2; "
          f"antenna tip {D['antenna_tip_z']:.0f} mm; mains rail used {D['mains_rail_used']:.0f} mm; "
          f"TwinKit rail used {D['twk_rail_used']:.0f} mm of {PARAMS['rail_len']:.0f}")
