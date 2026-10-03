"""CityTwin general arrangement sheet CTW-DWG-001, Rev P4 (TRL 3, constructable design per CTW-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/CTW-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept blueprint in media/ is CTW-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-09-25"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.1, 400, INK, "middle", mono=True)]


def dim_h_out(x1, x2, y, text, side="right"):
    """Narrow horizontal dimension with the value set beside it instead of on top of it."""
    out = dim_h(x1, x2, y, "")[:3]
    if side == "right":
        out.append(_t(max(x1, x2) + 1.8, y + 0.8, text, 2.1, 400, INK, "start", mono=True))
    else:
        out.append(_t(min(x1, x2) - 1.8, y + 0.8, text, 2.1, 400, INK, "end", mono=True))
    return out


def dim_v(x, y1, y2, text, side=-1, cy=None):
    a = 1.4
    cx, cy = x + side * 1.0, ((y1 + y2) / 2 if cy is None else cy)
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.1, 400, INK, "middle", mono=True)}</g>']


def dim_v_top(x, y1, y2, text, side=-1):
    """Vertical dimension with the value set above its upper end, clear of other levels' extension lines."""
    a = 1.4
    cx = x + side * 1.0
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {y1 - 2.0:.2f})">{_t(cx, y1 - 2.0 + 0.7, text, 2.1, 400, INK, "start", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.0, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly()
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="CityTwin", title="General arrangement, public kiosk", dwg_no="CTW-DWG-001", rev="P5",
              author="Amish Chadha", date="2026-10-02", scale=1 / 25, theme="technical",
              material="Steel post and plate, aluminum head; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Cabinet sun shield (19) added; wind figures updated (CTW-DDR-002)", DATE, "AC"),
                         ("P3", "Layout and labels tidied", "2026-09-30", "AC"),
                         ("P4", "Constructable design: fixings, front panel, carrier, shield standoffs (CTW-DDR-003)", "2026-10-01", "AC"),
                         ("P5", "Shield standoff holes only on the shielded variant; notice plate layout (CTW-DEC-001)", "2026-10-02", "AC")])
    s.add_ortho(views, dims=False)
    k = s.scale
    c = ortho_cells(s, views)
    L = []

    # front view (from -Y): X right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    xl = X(bb.min.X) - 4
    levels = [(D["antenna_tip_z"], f"{D['antenna_tip_z']:.0f} ANTENNA TIP"), (P["post_top"], f"{P['post_top']:.0f}"),
              (P["head_z1"], f"{P['head_z1']:.0f}"), (P["screen_cz"], f"{P['screen_cz']:.0f} SCREEN C/L"),
              (P["btn_z"], f"{P['btn_z']:.0f} BUTTONS"), (P["head_z0"], f"{P['head_z0']:.0f}"),
              (P["cab_z0"] + P["cab_h"], f"{P['cab_z0'] + P['cab_h']:.0f}"), (P["cab_z0"], f"{P['cab_z0']:.0f}")]
    for i, (zz, label) in enumerate(levels):
        xd = xl - 5.5 * i
        L.append(ext(X(-P["post"] / 2), Z(zz), xd - 1, Z(zz)))
        if i == 0:   # nearest column: set the value in the clear stretch above the next level
            L += dim_v(xd, Z(zz), Z(0), label, side=-1, cy=(Z(zz) + Z(levels[1][0])) / 2)
        else:
            L += dim_v_top(xd, Z(zz), Z(0), label, side=-1)
    L.append(ext(X(bb.min.X), Z(0), xl - 5.5 * len(levels), Z(0)))
    L.append(_t(X(bb.max.X) + 2, Z(0) - 1.5, "SIDEWALK Z = 0", 1.9, 400, MUTED))
    L += leader(X(0), Z(P["notice_z0"] + 50), X(bb.max.X) + 4, Z(P["notice_z0"] + 40), "8")
    L += leader(X(P["win_w"] / 2 - 10), Z(P["screen_cz"] + 60), X(bb.max.X) + 4, Z(P["screen_cz"] + 80), "4, 5")
    L += leader(X(P["hood_w"] / 2 - 20), Z(P["head_z1"] + 7), X(bb.max.X) + 4, Z(P["head_z1"] + 160), "9")

    # top view (from +Z): X right, Y up
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    ya = Yt(bb.max.Y) - 4
    for (a, b_, lab, dy) in ((-P["head_w"] / 2, P["head_w"] / 2, f"{P['head_w']:.0f} HEAD", 0),
                             (-P["hood_w"] / 2, P["hood_w"] / 2, f"{P['hood_w']:.0f} HOOD", 6)):
        yy = ya - dy
        L += [ext(Xt(a), Yt(0), Xt(a), yy), ext(Xt(b_), Yt(0), Xt(b_), yy)]
        L += dim_h(Xt(a), Xt(b_), yy, lab)

    xd = Xt(bb.min.X) - 4
    L += [ext(Xt(bb.min.X), Yt(bb.max.Y), xd - 1, Yt(bb.max.Y)), ext(Xt(bb.min.X), Yt(bb.min.Y), xd - 1, Yt(bb.min.Y))]
    L += dim_v(xd, Yt(bb.max.Y), Yt(bb.min.Y), f"{bb.size.Y:.0f}", side=-1)

    # right view (from +X): Y right, Z up
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    zt = P["head_z1"] + 120
    hf, hy0 = D["hood_front_y"], D["head_front_y"]
    L += [ext(Yr(hf), Zr(P["head_z1"]), Yr(hf), Zr(zt) - 1), ext(Yr(-P["post"] / 2), Zr(P["head_z1"]), Yr(-P["post"] / 2), Zr(zt) - 1)]
    L += dim_h(Yr(hf), Yr(-P["post"] / 2), Zr(zt), f"{P['hood_reach']:.0f}")
    L += [ext(Yr(hy0), Zr(P["head_z0"]), Yr(hy0), Zr(P["head_z0"] - 80) + 1)]
    L += dim_h_out(Yr(hy0), Yr(-P["post"] / 2), Zr(P["head_z0"] - 80), f"{P['head_d']:.0f}", "left")
    zc = P["cab_z0"] - 70
    L += [ext(Yr(D["cab_y0"]), Zr(P["cab_z0"]), Yr(D["cab_y0"]), Zr(zc) + 1), ext(Yr(D["cab_y1"]), Zr(P["cab_z0"]), Yr(D["cab_y1"]), Zr(zc) + 1)]
    L += dim_h_out(Yr(D["cab_y0"]), Yr(D["cab_y1"]), Zr(zc), f"{P['cab_d']:.0f}", "right")
    L += leader(Yr(D["cab_y1"] - 20), Zr(P["rail_twk_z"]), Yr(D["cab_y1"]) + 5, Zr(P["rail_twk_z"] + 120), "13 TWINKIT RAIL")
    L += leader(Yr(D["cab_y1"] - 20), Zr(P["rail_mains_z"]), Yr(D["cab_y1"]) + 5, Zr(P["rail_mains_z"] - 60), "11, 12 MAINS RAIL")
    L += leader(Yr(D["shield_y1"]), Zr(P["cab_z0"] + P["cab_h"] - 40), Yr(D["shield_y1"]) + 5, Zr(P["cab_z0"] + P["cab_h"] + 60), "10 DOOR ON BACK, 19 SHIELD")

    s._layers += L
    s.add_svg(views["iso"], 276, 44, 140, 84, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"2 post {P['post']:.0f} x {P['post']:.0f} x {P['post_t']:.0f} SHS; 1 base {P['base'][0]:.0f} x {P['base'][1]:.0f} x {P['base'][2]:.0f}, 4 x M{P['anchor_d']:.0f} on {P['anchor_pitch']:.0f} sq",
        f"3 head {P['head_w']:.0f} x {P['head_d']:.0f} x {P['head_z1'] - P['head_z0']:.0f}, {P['head_t']:.0f} mm aluminum, IP54 target",
        f"4 window {P['win_w']:.0f} x {P['win_h']:.0f} opening, {P['win_t']:.0f} mm PC; 5 active area {P['epd_active'][0]} x {P['epd_active'][1]}",
        f"7 three 19 mm buttons at {P['btn_pitch']:.0f} pitch; reach range 380 to 1,220",
        f"Overhang beyond post {D['hood_side_overhang']:.0f} max (305 allowed on posts)",
        f"10 cabinet {P['cab_w']:.0f} x {P['cab_d']:.0f} x {P['cab_h']:.0f}, IP55; two TS35 rails {P['rail_len']:.0f} long",
        f"19 sun shield (outdoor sites; side holes drilled only then) {D['shield_w']:.0f} wide, {P['shield_t']} mm Al, {P['shield_gap']:.0f} gap",
        f"Upper rail: TwinKit per TWK-DWG-001, {D['twk_rail_used']:.0f} used; lower: RCBO, SPD, 12 V 60 W",
        "Mains only in the cabinet; 12 V SELV and Ethernet up the post, 25 mm grommeted holes",
        "14 coax from TwinKit SMA bulkhead to post-top antenna",
        "Wind 35 m/s x 1.5: post 26.6 MPa; 1.94 kN per anchor (CTW-CAL-001 v0.3)",
        "Third-angle; front view from -Y (reading side)",
    ], x=276, y=142, width=140)
    out = s.save(ROOT / "cad" / "drawings" / "CTW-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
