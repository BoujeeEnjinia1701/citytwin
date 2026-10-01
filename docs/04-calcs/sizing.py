"""CityTwin sizing calculations for CTW-CAL-001 v0.3 (TRL 3, CTW-DDR-002 and the constructable design of CTW-DDR-003).

Run from the repo root:  python docs/04-calcs/sizing.py
Imports the kiosk model's PARAMS and part volumes from cad/src/model.py, reads bom/bom.csv
and budget_usd from project.yaml, prints every number that CTW-CAL-001 quotes with a tag
such as [A2], and writes docs/04-calcs/results.csv. First-principles screening estimates
for a paper proof of concept; every assumption is stated below and in the note.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, build_parts  # noqa: E402
import yaml  # noqa: E402

D = derived(P)
OUT = []


def tag(t, text):
    print(f"[{t}] {text}")
    OUT.append((t, text))


# ---------------------------------------------------------------- A. radio load (R1, R2)
BW, CR, PREAMBLE, LW_OVERHEAD, CHANNELS = 125e3, 1, 8, 13, 8


def airtime(sf, payload):
    """Semtech time on air: explicit header, CRC on, low data rate optimize at SF11 and SF12."""
    de = 1 if sf >= 11 else 0
    ts = 2 ** sf / BW
    pl = payload + LW_OVERHEAD
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (CR + 4), 0)
    return (PREAMBLE + 4.25) * ts + n * ts


def aloha_loss(rate_per_s, t):
    return 1 - math.exp(-2 * rate_per_s * t)


# Reference neighborhood (CTW-DDR-001 D9): nodes, uplinks per node per day, payload bytes,
# values per record, source. Rates are the sibling repos' TRL 3 figures.
REF = {
    "CurbCount":    (8, 96, 14, 7, "CBC-CAL-001: 14 B per 15 min bin"),
    "CrossSafe":    (4, 24, 20, 4, "Assumed hourly summary; CrossSafe defines no LoRaWAN uplink"),
    "LoadZone":     (12, 124, 12, 5, "LDZ-CAL-001: 100 state changes plus 24 heartbeats, 12 B"),
    "HeatMap Node": (6, 96, 20, 11, "HMN-CAL-001: 20 B per 15 min"),
    "FloodGauge":   (4, 96, 20, 6, "FLG-CAL-001: 15 min normal mode; 1 min in events"),
    "AirStreet":    (6, 288, 20, 10, "AST-CAL-001: 20 B per 5 min"),
    "NoiseMap":     (6, 96, 22, 22, "NSM-CAL-001: 22 B per 15 min"),
}
SF = 9                      # all nodes at SF9: TwinKit's worst screening case
SIGNS, SIGN_DL, SIGN_DL_S = 6, 200, 33.0   # LoadZone sign option: one per two-puck bay; LDZ-CAL-001 [H5]
FLOOD_EVENT_PER_H = 60      # FloodGauge event mode, one uplink a minute
LDZ_PEAK = 3.0              # LoadZone peak-hour factor on its daily average (assumed)
nodes = sum(v[0] for v in REF.values())
recs = {k: v[0] * v[1] for k, v in REF.items()}
rec_day = sum(recs.values())
air_day = sum(v[0] * v[1] * airtime(SF, v[2]) for v in REF.values())
for k, v in REF.items():
    tag("A1", f"{k}: {v[0]} nodes x {v[1]} = {recs[k]:,} uplinks/day, {v[2]} B, {airtime(SF, v[2]) * 1000:.1f} ms at SF{SF}")
tag("A2", f"reference neighborhood: {nodes} LoRaWAN nodes, {rec_day:,} uplinks/day (TRL 2: 4,896); "
          f"airtime {air_day:.0f} s/day, {air_day / 86400 * 100:.2f} % of one channel, {air_day / 86400 / CHANNELS * 100:.3f} % per channel over {CHANNELS}")
mean_t = air_day / rec_day
loss_day = aloha_loss(rec_day / 86400 / CHANNELS, mean_t)
dl_s = SIGNS * SIGN_DL_S
blank = dl_s / 86400
tag("A3", f"collision loss {loss_day * 100:.2f} % (pure ALOHA, {CHANNELS} channels, all SF{SF}); sign downlinks "
          f"{SIGNS} x {SIGN_DL} = {SIGNS * SIGN_DL:,}/day, {dl_s:.0f} s/day of gateway transmit, blanking {blank * 100:.2f} % of uplinks; "
          f"total {(loss_day + blank) * 100:.2f} %")
# storm peak hour
per_h = {k: v[0] * v[1] / 24 for k, v in REF.items()}
per_h["FloodGauge"] = REF["FloodGauge"][0] * FLOOD_EVENT_PER_H
per_h["LoadZone"] *= LDZ_PEAK
peak_h = sum(per_h.values())
peak_air = sum(per_h[k] * airtime(SF, REF[k][2]) for k in REF)
loss_peak = aloha_loss(peak_h / 3600 / CHANNELS, peak_air / peak_h)
tag("A4", f"storm peak hour (FloodGauge event mode, LoadZone x{LDZ_PEAK:.0f}): {peak_h:.0f} uplinks/h, loss {loss_peak * 100:.2f} % "
          f"plus {blank * 100:.2f} % blanking")
# R2 capacity case: 50 nodes, 10,000 records a day, 20 B at SF9
t20 = airtime(9, 20)
loss_r2 = aloha_loss(10000 / 86400 / CHANNELS, t20)
cap = -math.log(0.99) / (2 * t20) * CHANNELS * 86400
tag("A5", f"R2 case 10,000 records/day of 20 B at SF9: loss {loss_r2 * 100:.2f} %; at most {cap:,.0f}/day under 1 % "
          f"(TwinKit R1 case 14,400/day gives 1.02 %)")
# Non-LoRaWAN sources (pulled by outbound HTTPS, CTW-DDR-001 D11)
PHL_BUSES, PHL_SEG_BUS, PHL_EV_BUS, PHL_KB = 3, 2000, 500, 112
phl_rows = min(PHL_BUSES * PHL_SEG_BUS, 6000)
dkh_rows = 24
tag("A6", f"PotholeLog: {PHL_BUSES} buses x {PHL_KB} kB = {PHL_BUSES * PHL_KB} kB/day of summaries on the operator's server; "
          f"CityTwin pulls at most {phl_rows:,} published segment rows/day; DockHub {dkh_rows} dock-hour rows/day")

# ---------------------------------------------------------------- B. storage and export (R2, R6)
B_VALUE = 90                # bytes per stored value, TWK-CAL-001 (conservative, uncompressed)
RAW_YEARS, AGG_YEARS, CARD_FREE_GB, TWK_OWN_GB = 2, 10, 56, 4.73
vals_day = sum(v[0] * v[1] * v[3] for v in REF.values()) + phl_rows * 6 + dkh_rows * 6
raw_gb_y = vals_day * 365 * B_VALUE / 1e9
agg_rows_day = nodes * 24 + dkh_rows + phl_rows
agg_vals_day = sum(v[0] * 24 * v[3] for v in REF.values()) + dkh_rows * 6 + phl_rows * 6
agg_gb_y = agg_vals_day * 365 * B_VALUE / 1e9
total_gb = raw_gb_y * RAW_YEARS + agg_gb_y * AGG_YEARS
tag("B1", f"{vals_day:,} values/day; raw {raw_gb_y:.2f} GB/yr uncompressed, {RAW_YEARS} years kept = {raw_gb_y * RAW_YEARS:.2f} GB; "
          f"hourly aggregates {agg_gb_y:.2f} GB/yr, {AGG_YEARS} years = {agg_gb_y * AGG_YEARS:.2f} GB; total {total_gb:.1f} GB")
tag("B2", f"with TwinKit's own R3 case ({TWK_OWN_GB} GB/yr for {RAW_YEARS} years) the card holds "
          f"{total_gb + TWK_OWN_GB * RAW_YEARS:.1f} GB of {CARD_FREE_GB} GB free")
CSV_ROW, GEO_ROW = 120, 400
exp_rows = agg_rows_day
tag("B3", f"open export: {nodes * 24:,} node-hour rows + {phl_rows:,} segment rows + {dkh_rows} dock rows = {exp_rows:,} rows/day; "
          f"{exp_rows * CSV_ROW / 1e6:.2f} MB CSV and {exp_rows * GEO_ROW / 1e6:.2f} MB GeoJSON a day, "
          f"{exp_rows * (CSV_ROW + GEO_ROW) * 365 / 1e9:.2f} GB/yr on the public host")

# ---------------------------------------------------------------- C. freshness and response (R8, R10)
NET_S, RENDER_S, REDRAW_MIN = 4.7, 30.0, 10.0
EPD_W, EPD_H, EPD_BPP, SPI_HZ, ETH_BPS, REFRESH_S = 1600, 1200, 4, 10e6, 80e6, 19.0
img_b = EPD_W * EPD_H * EPD_BPP / 8
fetch_s = img_b * 0.2 * 8 / ETH_BPS + img_b * 8 / SPI_HZ          # PNG about 20 % of raw over Ethernet
press_s = fetch_s + REFRESH_S
worst = 15 + REDRAW_MIN + (NET_S + RENDER_S + fetch_s + REFRESH_S) / 60
lost = worst + 15
tag("C1", f"worst data age on the kiosk, 15 min nodes: {worst:.1f} min (15 min interval + {REDRAW_MIN:.0f} min redraw + "
          f"{NET_S} s network + {RENDER_S:.0f} s render + {fetch_s:.2f} s transfer + {REFRESH_S:.0f} s refresh); "
          f"{lost:.1f} min if one uplink is lost ({loss_day * 100:.2f} % chance); web map {15 + (NET_S + RENDER_S) / 60:.1f} min")
ACK_POLL_S, ACK_DEBOUNCE_S = 0.010, 0.020   # firmware rule: LED ring lit on press until the new image is drawn
ack_s = ACK_POLL_S + ACK_DEBOUNCE_S
tag("C2", f"button to new layer: {fetch_s:.2f} s transfer ({img_b / 1e3:.0f} kB frame over SPI at {SPI_HZ / 1e6:.0f} MHz) + "
          f"{REFRESH_S:.0f} s refresh = {press_s:.1f} s against 25 s (R10 restated, CTW-DDR-002; TRL 2 target 5 s); "
          f"LED ring acknowledgment {ack_s * 1000:.0f} ms ({ACK_POLL_S * 1000:.0f} ms poll + {ACK_DEBOUNCE_S * 1000:.0f} ms debounce) against 0.5 s")

# ---------------------------------------------------------------- D. legibility, lighting, shading (R9)
CAP_MM, VIEW_M, PPI = 7.0, 1.5, EPD_W / (P["epd_active"][1] / 25.4)
arcmin = math.degrees(math.atan(CAP_MM / 1000 / VIEW_M)) * 60
px = CAP_MM / 25.4 * PPI
LM_W, UTIL, LED_W, LED_DIM_W = 100.0, 0.4, 2.0, 0.3   # 2 W strip dimmed to 0.3 W by the controller (CTW-DDR-002)
lux_full = LED_W * LM_W * UTIL / D["epd_active_area_m2"]
lux = LED_DIM_W * LM_W * UTIL / D["epd_active_area_m2"]
tag("D1", f"{PPI:.0f} px per inch; 7 mm cap height = {px:.0f} px; subtends {arcmin:.1f} arcmin at {VIEW_M} m, "
          f"{arcmin / 5:.1f} x a 20/20 letter (5 arcmin) and {arcmin / 10:.1f} x 20/40 (10 arcmin)")
tag("D2", f"night: {LED_W:.0f} W LED at {LM_W:.0f} lm/W with {UTIL:.0%} reaching the screen gives about {lux_full:,.0f} lx on "
          f"{D['epd_active_area_m2']:.4f} m2; 200 lx needs {200 / lux_full * LED_W:.2f} W; dimmed to {LED_DIM_W} W it gives {lux:,.0f} lx")
ov = D["hood_overhang"]
lip_z = P["head_z1"] - P["hood_lip"]
wz0, wz1 = P["screen_cz"] - P["win_h"] / 2, P["screen_cz"] + P["win_h"] / 2
for el in (30, 45, 60):
    zs = lip_z - ov * math.tan(math.radians(el))
    frac = min(max((wz1 - zs) / (wz1 - wz0), 0), 1)
    tag("D3", f"sun {el} deg high, facing the screen: hood shadow at z = {zs:.0f} mm, {frac * 100:.0f} % of the window shaded")

# ---------------------------------------------------------------- E. accessibility geometry (R11)
ADA_LO, ADA_HI, PROTRUDE_LO, PROTRUDE_HI, POST_OVERHANG = 380, 1220, 685, 2030, 305
tag("E1", f"buttons at {P['btn_z']:.0f} mm (reach range {ADA_LO} to {ADA_HI}); head leading edge {P['head_z0']:.0f} to "
          f"{P['head_z1'] + P['hood_t']:.0f} mm, in the {PROTRUDE_LO} to {PROTRUDE_HI} mm zone; overhang beyond the post "
          f"{D['head_side_overhang']:.0f} mm (head) and {D['hood_side_overhang']:.0f} mm (hood) sideways, "
          f"{P['hood_reach'] - P['post'] / 2:.0f} mm (hood) forward, against {POST_OVERHANG} mm; cabinet with sun shield "
          f"{D['shield_y1'] - P['post'] / 2:.1f} mm behind the post, bottom {P['cab_z0']:.0f} mm (below {PROTRUDE_LO}, cane-detectable)")

# ---------------------------------------------------------------- F. thermal (R12, R20)
H_OUT, H_IN, ALPHA, G_V, G_H = 10.0, 5.0, 0.5, 600.0, 1000.0
TAU_WIN, ALPHA_EPD = 0.85, 0.7
EPD_MAX, PACK_CHG_MAX, CPU_RISE, CPU_THROTTLE = 40.0, 45.0, 29.1, 85.0   # TWK-CAL-001 F2: 69.1 C at 40 C
# head internal heat
P_CTRL, P_LEDS, P_EPD_AVG, P_HOOD_AVG = 1.0, 0.1, 0.5 * REFRESH_S / (REDRAW_MIN * 60), LED_DIM_W * 12 / 24
PILOT_AIR = 35.0            # R12 pilot air range 0 to 35 C (CTW-DDR-002; was 0 to 40 C)
q_head = P_CTRL + P_LEDS + P_EPD_AVG
a_head = D["head_area_m2"] - P["post"] * (P["head_z1"] - P["head_z0"]) / 1e6
dt_head_shade = q_head / (H_OUT * a_head)
tag("F1", f"head: {q_head:.2f} W inside, {a_head:.3f} m2 exposed; shaded rise {dt_head_shade:.2f} K; at {PILOT_AIR:.0f} C air the panel is "
          f"at {PILOT_AIR + dt_head_shade:.1f} C against its {EPD_MAX:.0f} C rating ({EPD_MAX - PILOT_AIR - dt_head_shade:.1f} K margin); "
          f"at 40 C air {40 + dt_head_shade:.1f} C; limit for air {EPD_MAX - dt_head_shade:.1f} C")
# sunlit street case: front face in low sun, air node and panel node
a_front_opaque = D["head_front_area_m2"] - D["win_area_m2"]
q_sol_head = ALPHA * G_V * a_front_opaque
dt_air_sun = (q_sol_head + q_head) / (H_OUT * a_head)
u_front = 1 / (1 / (0.026 / 0.001) + 1 / (0.2 / P["win_t"] * 1000) + 1 / H_OUT)   # air gap, PC window, outside film
a_p = P["epd_outline"][0] * P["epd_outline"][1] / 1e6
q_panel = TAU_WIN * ALPHA_EPD * G_V * D["epd_active_area_m2"]
dt_panel = (q_panel + H_IN * a_p * dt_air_sun) / (u_front * a_p + H_IN * a_p)
tag("F2", f"street, sun {G_V:.0f} W/m2 on the face: head air +{dt_air_sun:.1f} K; panel absorbs {q_panel:.1f} W and sits "
          f"{dt_panel:.1f} K above ambient (front U {u_front:.1f} W/m2K); at 45 C air the panel reaches {45 + dt_panel:.0f} C")
# cold: heater for an insulated panel bay
BAY = (0.26, 0.34, 0.04); K_FOAM, T_FOAM = 0.035, 0.020
a_bay = 2 * (BAY[0] * BAY[1] + BAY[0] * BAY[2] + BAY[1] * BAY[2]) - D["win_area_m2"]
u_ins = 1 / (T_FOAM / K_FOAM + 1 / H_OUT)
g_bay = u_ins * a_bay + u_front * D["win_area_m2"]
heater = g_bay * 20
tag("F3", f"cold: whole uninsulated head needs {H_OUT * a_head * 20 - q_head:.0f} W to stay at 0 C in -20 C air; "
          f"a 20 mm foam panel bay needs {heater:.1f} W ({g_bay:.3f} W/K)")
# cabinet: sealed, wall node and air node
PSU_EFF = 0.85
p_head_dc = P_CTRL + P_LEDS + P_EPD_AVG + P_HOOD_AVG
TWK_W = 6.41
psu_loss = (TWK_W + p_head_dc) * (1 / PSU_EFF - 1)
q_cab = TWK_W + psu_loss + 0.2
a_cab = D["cab_area_m2"] - P["post"] * P["cab_h"] / 1e6
dt_cab_shade = q_cab / (H_OUT * a_cab) + q_cab / (H_IN * a_cab)
q_sol_cab = ALPHA * (G_V * P["cab_w"] * P["cab_h"] / 1e6 + G_H * P["cab_w"] * P["cab_d"] / 1e6)
dt_cab_sun = (q_cab + q_sol_cab) / (H_OUT * a_cab) + q_cab / (H_IN * a_cab)
SHIELD_RES = 0.2           # share of the sun still reaching the cabinet behind the ventilated shield (assumed)
q_sol_sh = SHIELD_RES * q_sol_cab
dt_cab_sh = (q_cab + q_sol_sh) / (H_OUT * a_cab) + q_cab / (H_IN * a_cab)
sh_air_max = PACK_CHG_MAX - dt_cab_sh
tag("F4", f"cabinet: {q_cab:.2f} W inside (TwinKit {TWK_W} W, supply loss {psu_loss:.2f} W, protection 0.2 W), "
          f"{a_cab:.3f} m2; air rise {dt_cab_shade:.1f} K shaded, {dt_cab_sun:.1f} K in sun ({q_sol_cab:.0f} W absorbed), "
          f"{dt_cab_sh:.1f} K in sun behind the sun shield ({q_sol_sh:.0f} W, {SHIELD_RES:.0%} residual); with the shield the pack "
          f"stays under {PACK_CHG_MAX:.0f} C in full sun up to {sh_air_max:.1f} C air")
for amb, rise, case in ((PILOT_AIR, dt_cab_shade, f"pilot {PILOT_AIR:.0f} C shaded"), (40, dt_cab_shade, "40 C shaded"),
                        (45, dt_cab_shade, "street 45 C shaded"), (45, dt_cab_sun, "street 45 C in sun, no shield"),
                        (PILOT_AIR, dt_cab_sh, f"outdoor {PILOT_AIR:.0f} C in sun with shield"),
                        (45, dt_cab_sh, "street 45 C in sun with shield")):
    air = amb + rise
    tag("F5", f"{case}: cabinet air {air:.1f} C; processor {air + CPU_RISE:.1f} C (throttle {CPU_THROTTLE:.0f}); "
              f"pack {air:.1f} C against {PACK_CHG_MAX:.0f} C charge limit ({PACK_CHG_MAX - air:+.1f} K)")
tag("F6", f"cold: at -20 C air the cabinet air is {-20 + dt_cab_shade:.1f} C, below the pack's 0 C charge limit")

# ---------------------------------------------------------------- G. power (R14, R15)
p_mains = (TWK_W + p_head_dc) / PSU_EFF + 0.2
tag("G1", f"head DC {p_head_dc:.2f} W (controller {P_CTRL}, hood light {P_HOOD_AVG:.1f} avg for 12 h a night, LEDs {P_LEDS}, "
          f"e-paper {P_EPD_AVG:.3f}); TwinKit {TWK_W} W; mains {p_mains:.1f} W average, {p_mains * 24 / 1000:.3f} kWh/day, "
          f"{p_mains * 8.76:.0f} kWh/yr")
p_heat = p_mains + heater / PSU_EFF
tag("G2", f"street variant with the panel heater on at -20 C: {p_heat:.1f} W while heating")
peak = 20.6 + 2.5 + 1.5 + LED_W + P_LEDS
tag("G3", f"12 V supply peak {peak:.1f} W (TwinKit 20.6, controller boot 2.5, e-paper 1.5, hood 2, LEDs 0.1); "
          f"{peak + heater:.1f} W with the heater; 60 W unit; mains current {p_mains / 230 * 1000:.0f} mA at 230 V")

# ---------------------------------------------------------------- H. structure and mass (R13)
RHO_AIR, V_GUST, LF = 1.25, 35.0, 1.5
q = 0.5 * RHO_AIR * V_GUST ** 2
hood_a = P["hood_w"] * (P["hood_lip"] + P["hood_t"]) / 1e6
loads = [("head and hood", 1.3, D["head_front_area_m2"] + hood_a, D["head_cz"] / 1000),
         ("cabinet and sun shield", 1.3, D["shield_w"] * D["shield_h"] / 1e6, (P["cab_z0"] + D["shield_h"] / 2) / 1000),
         ("post", 2.0, P["post"] * (P["post_top"] - P["base"][2]) / 1e6, P["post_top"] / 2000),
         ("antenna", 1.2, P["ant_d"] * P["ant_len"] / 1e6, (D["antenna_tip_z"] - P["ant_len"] / 2) / 1000)]
F_tot, M_tot = 0.0, 0.0
for name, cd, a, z in loads:
    F = q * cd * a
    F_tot += F; M_tot += F * z
    tag("H1", f"{name}: Cd {cd}, {a:.3f} m2, {F:.0f} N at {z:.2f} m")
b, t = P["post"], P["post_t"]
I = (b ** 4 - (b - 2 * t) ** 4) / 12
Z = I / (b / 2)
sig = M_tot * LF * 1000 / Z
tag("H2", f"q {q:.0f} Pa; {F_tot:.0f} N, base moment {M_tot:.0f} N m, x{LF} = {M_tot * LF:.0f} N m; SHS Z {Z:,.0f} mm3; "
          f"stress {sig:.1f} MPa against 355 MPa yield (factor {355 / sig:.1f})")
throat = 0.707 * 4
Zw = throat * (b * b + b * b / 3)
tag("H3", f"4 mm fillet weld all round: Zw {Zw:,.0f} mm3, {M_tot * LF * 1000 / Zw:.1f} MPa")
mass = {}
dens = {1: 7850, 2: 7850, 3: 2700, 4: 1200, 10: 7850, 19: 2700, 20: 2700}
fixed = {5: 1.2, 6: 0.25, 7: 0.15, 11: 0.5, 12: 0.3, 13: 1.2, 14: 0.5, 15: 1.0, 21: 0.6}
for n, name, s in build_parts():
    if n in dens:
        mass[n] = s.volume * 1e-9 * dens[n]
    elif n == 8:
        mass[n] = P["notice"][0] * P["notice"][1] * 2 * 1e-9 * 2700
    elif n == 9:
        area = (P["hood_w"] * (P["hood_reach"] - P["post"] / 2) + P["hood_w"] * P["hood_lip"]
                + 2 * P["hood_cheek"] * (P["hood_cheek"] - 30)) / 1e6
        mass[n] = area * P["hood_t"] * 2700 / 1000 + 0.1
    else:
        mass[n] = fixed[n]
m_tot = sum(mass.values())
W = m_tot * 9.81
pitch = P["anchor_pitch"] / 1000
T = M_tot * LF / (2 * pitch) - W / 4
tag("H4", f"mass {m_tot:.1f} kg (post {mass[2]:.1f}, base {mass[1]:.1f}, cabinet with rails {mass[10]:.1f}, head {mass[3]:.1f}, "
          f"hood {mass[9]:.2f}, window {mass[4]:.2f}, sun shield {mass[19]:.2f}; bought-in items assumed)")
tag("H5", f"anchor tension {T / 1000:.2f} kN per anchor (two in tension, {pitch * 1000:.0f} mm apart, less self-weight); "
          f"against an assumed 10 kN design resistance for an M16 anchor, factor {10000 / T:.1f}")
lever = (P["anchor_pitch"] - P["post"]) / 2 / 1000
Zp = P["base"][0] * P["base"][2] ** 2 / 6
tag("H6", f"base plate: {2 * T * lever:.0f} N m over {P['base'][0]:.0f} mm, {2 * T * lever * 1000 / Zp:.0f} MPa in the 12 mm plate")
Fh = loads[0][1] * q * loads[0][2]
defl = Fh * (D["head_cz"]) ** 3 / (3 * 200000 * I)
tag("H7", f"head deflection at {D['head_cz'] / 1000:.2f} m under the unfactored gust: {defl:.2f} mm")

# ---------------------------------------------------------------- I. backup (R18)
PACK_AH, T_NEW, T_WORST, T_REQ = 1.5, 2.40, 1.63, 2.0
tag("I1", f"TwinKit backup (TWK-CAL-001 E1): {T_NEW:.2f} h new, {T_WORST:.2f} h aged at 0 C, against {T_REQ:.0f} h; head not on backup, "
          f"e-paper keeps its last image and time stamp; a pack of at least {PACK_AH * T_REQ / T_WORST:.2f} Ah (now {PACK_AH} Ah) "
          f"would meet 2 h in the worst case, to be requested from TwinKit (CTW-DDR-002)")

# ---------------------------------------------------------------- J. cost (R16, R17)
pm = yaml.safe_load((ROOT / "project.yaml").read_text())
budget = float(pm["budget_usd"])
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = {int(r["item"].split()[0]): float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows}
kiosk = sum(v for k, v in cost.items() if k not in (13, 16, 17, 18, 19))   # items 1 to 12, 14, 15, 20, 21
outdoor = kiosk + cost[19]
priced = all((r["unit_cost_usd"] or "").strip() for r in rows)
tag("J1", f"{len(rows)} BOM lines, all priced: {priced}; pilot kiosk (1 to 12, 14, 15, 20, 21) ${kiosk:,.2f}; TwinKit ${cost[13]:,.2f}; "
          f"with gateway ${kiosk + cost[13]:,.2f}; outdoor kiosk with sun shield (19) ${outdoor:,.2f}")
tag("J2", f"pilot kiosk against budget_usd ${budget:,.0f} (was $600): {kiosk - budget:+,.2f}; outdoor kiosk {outdoor - budget:+,.2f}")

# ---------------------------------------------------------------- K. requirement status
STATUS = [
    ("R1", "Ingest every node type", "6 LoRaWAN types on paper; PotholeLog and DockHub by outbound pull (D11), not agreed; CrossSafe has no LoRaWAN uplink", "All 9 types", "At risk"),
    ("R2", "Capacity on one gateway", f"{nodes} nodes, {rec_day:,}/day, loss {loss_day * 100:.2f} %; 10,000/day gives {loss_r2 * 100:.2f} %", "50 nodes, 10,000/day", "Met on paper"),
    ("R3", "Counts and levels only", "Per-type schema at the decoder", "Reject out-of-schema fields", "Met by design"),
    ("R4", "Small-count suppression", "Threshold 5 per hour (D6)", "Fewer than 5 published as such", "Met by design"),
    ("R5", "No movement traces", "Segment per day; dock per hour", "No tracks, no card IDs", "Met by design"),
    ("R6", "Open data export", f"{exp_rows:,} rows/day, {exp_rows * CSV_ROW / 1e6:.2f} MB CSV", "Hourly CSV and GeoJSON, CC BY 4.0", "Met by design"),
    ("R7", "One map", "Layer per type, health, as-of time", "As stated", "Met by design"),
    ("R8", "Data freshness", f"{worst:.1f} min worst on the kiosk", "30 min", "Met on paper (thin margin)"),
    ("R9", "Readable day and night", f"7 mm = {px:.0f} px, {arcmin:.1f} arcmin; {lux:,.0f} lx at night (light dimmed to {LED_DIM_W} W)", "Sun and night at 1.5 m", "Met on paper"),
    ("R10", "Button response (restated)", f"LED ring {ack_s * 1000:.0f} ms; layer {press_s:.1f} s", "Acknowledged within 0.5 s; layer within 25 s", "Met on paper"),
    ("R11", "Accessible kiosk", f"Buttons {P['btn_z']:.0f} mm; overhang {D['hood_side_overhang']:.0f} mm", "380 to 1,220 mm; 305 mm; WCAG page", "Met on paper (web page not verifiable at TRL 3)"),
    ("R12", "Pilot climate (redefined)", f"Panel {PILOT_AIR + dt_head_shade:.1f} C and pack {PILOT_AIR + dt_cab_shade:.1f} C at {PILOT_AIR:.0f} C air", f"Sheltered site, air 0 to {PILOT_AIR:.0f} C", "Met on paper"),
    ("R13", "Wind", f"{sig:.1f} MPa with factor 1.5; anchors {T / 1000:.2f} kN", "35 m/s gust x 1.5, no yield", "Met on paper"),
    ("R14", "Electrical safety", f"Mains only in the cabinet; 12 V SELV; peak {peak:.1f} W of 60 W", "As stated", "Met by design"),
    ("R15", "Running power", f"{p_mains:.1f} W", "15 W", "Met on paper"),
    ("R16", "Pilot kiosk parts cost", f"${kiosk:,.2f} (outdoor with shield ${outdoor:,.2f})", f"${budget:,.0f} (budget_usd)", "Met on paper" if kiosk <= budget else f"Not met (${kiosk - budget:,.2f} over)"),
    ("R17", "Cost with gateway (redefined, D1)", f"${kiosk + cost[13]:,.2f}", "Reported; gateway costed in TwinKit", "Met on paper (reported)"),
    ("R18", "Honest in an outage", f"{T_NEW:.2f} h new, {T_WORST:.2f} h worst; {PACK_AH * T_REQ / T_WORST:.2f} Ah pack needed", "2 h ride-through", "Not met (worst case)"),
    ("R19", "Secure by default", "Outbound push and pull only", "No inbound connections", "Met by design"),
    ("R20", "Street climate (target after the pilot)", f"Panel {45 + dt_panel:.0f} C in sun, {45 + dt_head_shade:.1f} C shaded at 45 C; pack {45 + dt_cab_sh:.1f} C behind the shield; heater {heater:.1f} W at -20 C", "-20 to +45 C air", "Not met"),
]
counts = {}
for r in STATUS:
    key = r[4].split(" (")[0]
    counts[key] = counts.get(key, 0) + 1
tag("K1", "status counts: " + ", ".join(f"{v} {k.lower()}" for k, v in counts.items()))
with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "requirement", "value", "target", "status"])
    w.writerows(STATUS)
print("wrote docs/04-calcs/results.csv")
