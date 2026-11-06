"""Vidéo : Phineas Gage, la barre de fer dans le crâne."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n', '/home/claude/g2n/gage']
import numpy as np
from world import *
from video_core import *
from scripts import GAGE as LINES
import audio as A
import common2 as C2

HERE = '/home/claude/g2n/gage'
TIMING_FILE = os.path.join(HERE, 'timing.json')
timing = load_timing(TIMING_FILE) if os.path.exists(TIMING_FILE) else est_timing(LINES, cps=16.5, gap=0.25)
tl = Timeline(timing)
T = tl.T
WT = tl.word_t
SHOT_STARTS = {}


def add(name, t0, fn):
    SHOT_STARTS[name] = t0
    tl.add(t0, fn)


def S(name):
    return SHOT_STARTS[name]


# ------------------------------------------------------------------ éléments
CUT = rail_cut()
HILLS = hills(1, -220, 900, (255, 255, 255), 'grass', 14)
FOREST = forest(-80, -120, 80, -20, 50, 2, avoid=lambda x, z: abs(x) < 30 and z > -14)
SITE = merge([CUT, HILLS, FOREST, blast_hole()])
HOTEL = hotel()
BEDROOM = bedroom()
SALOON = saloon()
DESK = desk_scene()
ANDES = andes()
ROAD = chile_road()
MUSEUM = museum_case()

G = gage()
G_SMILE = gage('gage_smile')
G_OPEN = gage('gage_open')
G_SHOUT = gage('gage_shout')
G_CLOSED = gage('gage_closed')
GB = gage('gage_b', hat=False)
GB_SMILE = gage('gage_b_smile', hat=False)
GB_BAND = gage('gage_b', hat=False, bandage=True)
GB_FEVER = gage('gage_b_fever', hat=False, bandage=True)
GB_COAT = gage('gage_b_smile', coat=True)
GB_COAT_N = gage('gage_b', coat=True, hat=False)
G_RAG = gage('gage_b_shout', ragged=True)
G_RAG_N = gage('gage_b', ragged=True)
W1, W2 = worker(0), worker(1)
W1S, W2S = worker(0, 'worker1_shock'), worker(1, 'worker2_shock')
DOC, DOC_S = doctor(), doctor('doctor_shock')
HARLOW = harlow()

GAGE_POS = np.array([0.0, 0.05, 0.36])   # debout face au trou (regarde -z)


def site_env(lt=0.0):
    return ENV_DAY


def workers_bg(tg, n=4):
    ms = []
    spots = ((-6, 0.05, -2.5, 0.4), (-9, 0.05, 1.5, 1.2), (7, 0.05, -2.0, -0.6), (11, 0.05, 1.0, -1.4))
    for i in range(n):
        x, y, z, yaw = spots[i]
        w = W1 if i % 2 == 0 else W2
        ph = tg * 4 + i
        ms.append(w.mesh((x, y, z), yaw, dict(ra=(1.6 + 0.6 * math.sin(ph), 0.1, 0.6), la=(1.2, 0.1, 0.8), lean=0.4, hp=0.4,
                                              hand_r=sledge().xf(M(rotx(-1.6), trans(0, -0.1, 0))))))
    return merge(ms)


def iron_in_hole(depth=0.45):
    return IRON.xf(trans(HOLE[0], HOLE[1] - depth, HOLE[2]))


def gage_tamp(who, phase, look_back=0.0):
    """Gage penché sur le trou, deux mains sur la barre, qui tasse (phase) ; look_back = tourne la tête"""
    lift = 0.12 * max(0.0, math.sin(phase))
    depth = 0.3 - lift
    gl = HOLE + np.array([0.0, 0.92 - depth, 0.0])
    pose = dict(lean=0.45, hp=0.35 - 0.6 * look_back, hy=1.1 * look_back, ik_l=gl + np.array([-0.03, -0.12, 0.02]), ik_r=gl + np.array([0.03, 0.02, 0.02]))
    return merge([who.mesh(tuple(GAGE_POS), math.pi, pose), iron_in_hole(depth)])


def IRON_TOP(depth):
    return 1.1 - depth


# ------------------------------------------------------------------ 0 : accroche
GRID = box(6, 6, 0.05, (255, 255, 255), 'xgrid', ts=0.25).xf(trans(0, -3, -1.0))


def xray_frame(lt, tg, prog, yaw, fov=34, dist=0.75):
    """crâne radiographique + barre incandescente qui le traverse (prog 0..1)"""
    a, b = iron_path()
    d = (b - a) / np.linalg.norm(b - a)
    L = 0.55
    start = a - d * 0.45
    head = start + d * (prog * 0.8)
    tail = head - d * L
    seg = merge([rod(tail, head, 0.008, (255, 170, 60))])
    seg.emis[:] = 1.0
    seg2 = rod(tail, head, 0.016, (255, 160, 60))
    seg2.emis[:] = 1.0
    seg2.alpha[:] = 0.35
    Ry = roty(yaw)
    ms = [SKULL_X.xf(Ry), seg.xf(Ry), seg2.xf(Ry), GRID]
    # points d'entrée / sortie qui s'allument
    for p, t0 in ((a, 0.45), (b, 0.75)):
        if prog > t0:
            k = min(1.0, (prog - t0) * 6)
            ms.append(billboard((Ry @ np.append(p, 1))[:3], 0.05 * k, 0.05 * k, Cam((0, 0, dist), (0, 0, 0)), (255, 230, 120), 'spark', emis=1.0))
    cam = Cam((math.sin(0.25) * dist, 0.05, math.cos(0.25) * dist), (0, 0.02, 0), fov)
    return merge(ms), cam, ENV_XRAY


def shot_hook_xray(lt, dur, tg):
    prog = min(1.0, lt / max(0.9, dur * 0.8))
    m, cam, env = xray_frame(lt, tg, ease(prog), -0.5 + lt * 0.5, fov=lerp(44, 34, ease(lt / dur)), dist=1.0)
    cam = C2.shake(cam, 0.01 * C2.decay(lt, 0.4, 4), tg)
    return m, cam, env, dict(flash=0.6 * C2.decay(lt, 0.0, 12))


PORCH_SEAT = np.array([1.2, 0.3, 5.5])


def porch(lt, tg, gage_face='gage_b_smile', talk=False, doc_z=8.0, doc_walk=False, crowd=True):
    who = GB_SMILE if gage_face == 'gage_b_smile' else (GB if gage_face == 'gage_b' else gage(gage_face, hat=False))
    hand = 0.4 * math.sin(tg * 5) if talk else 0.0
    pose = sit_pose(drop=0.45, la=(0.6, 0.15, 0.6), ra=(0.9 + hand, 0.3, 1.0 + hand), hp=-0.05, hy=0.15 * math.sin(tg * 2.5) if talk else 0.0)
    ms = [HOTEL, grid(-40, -40, 40, 40, 6, 6, None, (255, 255, 255), 'dirt', 3.0), HILLS, chair().xf(trans(PORCH_SEAT + np.array([0, 0, -0.05]))),
          who.mesh(tuple(PORCH_SEAT + np.array([0, -0.03, 0.0])), 0.0, pose)]
    dp = (PORCH_SEAT[0] - 0.3, 0, doc_z)
    ms.append((DOC_S if not doc_walk and talk else DOC).mesh(dp, math.pi, walk_pose(tg * 5, 0.8) if doc_walk else dict(ra=(0.2, 0.1, 0.3),
                                                                                                                         hand_r=box(0.35, 0.25, 0.15, (50, 30, 20)).xf(trans(0, -0.15, 0)))))
    if crowd:
        for i, (x, z, yaw) in enumerate(((-2.5, 8.5, 2.6), (-3.5, 9.6, 2.9), (4.5, 9.0, -2.7), (5.2, 7.8, -2.2))):
            ms.append((W1 if i % 2 else W2).mesh((x, 0, z), yaw, dict(hp=0.1)))
    return ms


def shot_hook_talk(lt, dur, tg):
    ms = porch(lt, tg, 'gage_b_smile', talk=True, doc_z=7.4)
    head = PORCH_SEAT + np.array([0, 1.15, 0])
    cam = cam_lerp(Cam(tuple(head + np.array([-1.0, 0.1, 2.0])), tuple(head + np.array([0.2, -0.2, 0])), 48),
                   Cam(tuple(head + np.array([-0.8, 0.1, 1.6])), tuple(head + np.array([0.2, -0.2, 0])), 45), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 1-2 : le chantier
def shot_vermont(lt, dur, tg):
    u = lt / max(dur, 0.1)
    cam = Cam((40 - u * 15, 22 - u * 5, 55 - u * 10), (0, 1, -3), 50)
    ms = [SITE, workers_bg(tg), G.mesh(tuple(GAGE_POS + np.array([1.5, 0, 1.5])), math.pi - 0.4, dict(ra=(0.4, 0.1, 0.3)))]
    ms.append(Mesh())
    return merge(ms), cam, ENV_DAY, {}


def shot_gage_intro(lt, dur, tg):
    """Gage, contremaître, fait signe à ses ouvriers"""
    p = np.array([2.0, 0.05, 2.5])
    pose = dict(ra=(1.9 + 0.3 * math.sin(tg * 4), 0.6, 0.4), la=(0.3, 0.1, 0.4), hy=-0.4 + 0.3 * math.sin(tg * 1.3))
    cam = cam_lerp(Cam((p[0] - 1.6, 1.65, p[2] + 2.4), (p[0], 1.45, p[2]), 45), Cam((p[0] - 1.2, 1.6, p[2] + 1.9), (p[0], 1.5, p[2]), 42), lt / dur)
    ms = [SITE, workers_bg(tg), G_SMILE.mesh(tuple(p), -0.45, pose)]
    return merge(ms), cam, ENV_DAY, {}


def blast_far(lt, tg, t0=0.25, pos=(-14, 0.5, -5)):
    cam_ = None
    return t0, pos


def shot_blast_demo(lt, dur, tg):
    """plan fixe et large : une charge saute dans la paroi, les ouvriers se protègent les oreilles"""
    cam = Cam((2, 2.2, 10), (-12, 2.0, -5), 50)
    t0 = 0.6
    ms = [SITE, workers_bg(tg, 2)]
    from lib import smoke_sprites
    if lt > t0:
        a = lt - t0
        for i in range(8):
            rr = np.random.default_rng(i)
            v = rr.normal(size=3) * np.array([3, 0, 3]) + np.array([0, 9, 0])
            p = np.array([-14, 1.0, -5]) + v * a + np.array([0, -4.9 * a * a, 0])
            if p[1] > 0:
                ms.append(box(0.4, 0.3, 0.35, (130, 125, 115), 'ledge').xf(M(trans(p), rotx(a * 7 + i))))
        ms.append(smoke_sprites((-14, 1.0, -5), a, cam, n=10, size=4.5, rise=8, seed=4, col=(170, 165, 155), drift=(0.4, 0, 0.1), alpha=max(0.0, 0.9 - a * 0.2)))
        if a < 0.2:
            ms.append(billboard((-14, 1.5, -5), 5 * (1 - a * 4), 5 * (1 - a * 4), cam, (255, 255, 255), 'fire', emis=1.0))
    for i, x in enumerate((3, 5)):
        ms.append((W1 if i else W2).mesh((x, 0.05, 6), -0.9, dict(la=(2.5, 0.3, 1.8), ra=(2.5, 0.3, 1.8))))
    return merge(ms), cam, ENV_DAY, dict(flash=0.3 * C2.decay(lt, t0, 10))


# ------------------------------------------------------------------ 3 : creuser, poudre, tasser
def shot_drill(lt, dur, tg):
    """plan fixe : un ouvrier tient le foret, l'autre frappe à la masse (on creuse le trou)"""
    hit = (tg * 1.6) % 1.0
    up = math.sin(hit * math.pi)
    hold = HOLE + np.array([0, 0.62, 0])
    ms = [SITE, drill_bit().xf(trans(HOLE - np.array([0, 0.1, 0]))),
          W2.mesh((0.0, 0.05, 0.55), math.pi, dict(lean=0.7, hp=0.4, drop=0.4, ll=(1.2, 1.9), rl=(1.2, 1.9),
                                                 ik_l=hold + np.array([-0.02, 0, 0.03]), ik_r=hold + np.array([0.02, -0.08, 0.03])))]
    ms.append(W1.mesh((0.9, 0.05, -0.1), -math.pi / 2, dict(ra=(0.6 + 2.0 * up, -0.1, 0.4), la=(0.6 + 2.0 * up, 0.1, 0.4), lean=0.15,
                                                          hand_r=sledge().xf(M(rotx(-1.5), trans(0, -0.2, 0))))))
    cam = Cam((2.8, 1.5, 2.6), (0.3, 0.6, 0.1), 45)
    return merge(ms), cam, ENV_DAY, {}


# --- vue en coupe : le trou dans la roche, ouvert comme un schéma


SEC_DEPTH = 0.9


def section_rock():
    """moitié arrière d'un bloc de roche coupé : on voit le trou en demi-cylindre (6 cm, 90 cm de profondeur) au centre"""
    R = (150, 145, 135)
    ms = [box(0.6, 1.4, 0.6, R, 'ledge', ts=0.3).xf(trans(-0.33, -1.4, -0.3)),
          box(0.6, 1.4, 0.6, R, 'ledge', ts=0.3).xf(trans(0.33, -1.4, -0.3)),
          box(0.06, 1.4, 0.57, (95, 90, 85), 'ledge', ts=0.3).xf(trans(0, -1.4, -0.315)),
          box(0.06, 1.4 - SEC_DEPTH, 0.6, R, 'ledge').xf(trans(0, -1.4, -0.3))]
    # face de coupe : bande plus claire autour du trou + traits rouges de schéma
    for x in (-0.33, 0.33):
        ms.append(box(0.6, 1.4, 0.004, (185, 178, 165), 'ledge', ts=0.3).xf(trans(x, -1.4, 0.002)))
    ms.append(box(1.4, 0.012, 0.01, (200, 40, 40)).xf(trans(0, -0.006, 0.006)))
    return merge(ms)


SECTION = section_rock()


POWDER_TOP = -SEC_DEPTH + 0.22


def section_scene(powder=1.0, sand=0.0, iron_y=None, spark=0.0, cam=None, flask=0.0, tg=0.0):
    ms = [SECTION, box(6, 0.05, 6, (255, 255, 255), 'dirt').xf(trans(0, -0.05, -3.4))]
    h = 0.22 * powder
    if h > 0:
        ms.append(box(0.058, h, 0.03, (30, 28, 26), 'powder').xf(trans(0, -SEC_DEPTH, -0.015)))
    if iron_y is not None:
        ms.append(IRON.xf(M(trans(0, iron_y + 1.1, -0.012), rotx(math.pi))))
    if flask > 0:
        ms.append(powder_flask().xf(M(trans(0.07, 0.18, 0.02), rotz(2.3))))
        for i in range(16):
            a = (tg * 2.2 + i / 16) % 1.0
            y = 0.12 - a * (0.12 - (-SEC_DEPTH + h))
            ms.append(box(0.014, 0.014, 0.014, (30, 30, 30)).xf(trans(0.005, y, 0.0)))
    if spark > 0 and cam is not None:
        p = np.array([0, POWDER_TOP + 0.01, 0.0])
        ms.append(billboard(p, 0.12 * spark, 0.12 * spark, cam, (255, 220, 120), 'spark', emis=1.0))
        rr = np.random.default_rng(4)
        for i in range(8):
            v = rr.normal(size=3) * np.array([0.08, 0.05, 0.02]) + np.array([0, 0.06, 0])
            ms.append(billboard(p + v * spark, 0.03, 0.03, cam, (255, 230, 150), 'spark', emis=1.0))
    return merge(ms)


SEC_CAM = Cam((0.3, -0.2, 1.7), (0, -0.4, -0.05), 44)


def shot_powder(lt, dur, tg):
    """schéma en coupe : on verse la poudre noire au fond du trou"""
    pw = min(1.0, lt / max(0.4, dur * 0.8))
    ms = [section_scene(pw, flask=1.0, tg=tg)]
    return merge(ms), SEC_CAM, ENV_DAY.copy(points=[((0.4, 0.3, 1.2), (255, 240, 210), 0.5, 3)]), {}


def shot_tamp(lt, dur, tg):
    """plan fixe de profil : Gage, penché au-dessus du trou, tasse doucement avec sa barre"""
    ms = [SITE, workers_bg(tg, 2), gage_tamp(G, tg * 4.0)]
    cam = Cam((3.0, 1.45, 0.7), (0, 0.95, 0.2), 48)
    return merge(ms), cam, ENV_DAY, {}


def shot_iron_hero(lt, dur, tg):
    """la barre posée sur une planche, la caméra la longe ; mesure 1,10 m / 6 kg"""
    board = box(1.5, 0.05, 0.4, (170, 140, 100), 'planks')
    ir = IRON.xf(M(trans(-0.55, 0.075, 0), rotz(-math.pi / 2)))
    u = ease(lt / max(dur, 0.1))
    cam = Cam((lerp(-0.6, 0.5, u), 0.35, 0.55), (lerp(-0.4, 0.55, u), 0.07, 0.0), 40)
    ms = [box(4, 0.05, 4, (255, 255, 255), 'dirt').xf(trans(0, -0.05, 0)), board, ir]
    return merge(ms), cam, ENV_DAY.copy(points=[((0, 1.2, 0.6), (255, 240, 210), 0.6, 3)]), {}


# ------------------------------------------------------------------ 4 : l'inattention
def shot_lookback(lt, dur, tg):
    """quelqu'un l'appelle derrière lui : Gage tourne la tête… la barre au-dessus du trou"""
    lb = min(1.0, lt / 0.6)
    ms = [SITE, gage_tamp(G, 0.0, ease(lb)), W1.mesh((-3.0, 0.05, 2.6), 2.4, dict(ra=(2.4, 0.4, 0.5)))]
    cam = Cam((3.0, 1.5, 1.4), (-0.3, 1.05, 0.4), 50)
    return merge(ms), cam, ENV_DAY, {}


def shot_strike(lt, dur, tg):
    """schéma en coupe : la barre descend dans le trou, frappe la roche… étincelle dans la poudre"""
    t_hit = min(0.6, dur * 0.4)
    k = min(1.0, lt / t_hit)
    y = 0.15 - (0.15 - (POWDER_TOP - 0.02)) * k * k
    sp = 0.0 if lt < t_hit else min(1.0, (lt - t_hit) * 5) * (1 + 0.3 * math.sin(lt * 40))
    cam = C2.shake(SEC_CAM, 0.01 * C2.decay(lt, t_hit, 6), tg)
    ms = [section_scene(1.0, iron_y=y, spark=sp, cam=cam)]
    env = ENV_DAY.copy(points=[((0.4, 0.3, 1.2), (255, 240, 210), 0.5, 3)] + ([((0, POWDER_TOP, 0.2), (255, 170, 60), 2.0 * min(1, sp), 0.8)] if sp > 0 else []))
    return merge(ms), cam, env, dict(flash=0.25 * C2.decay(lt, t_hit, 12))


def shot_spark(lt, dur, tg):
    """au ralenti : une étincelle jaillit au fond du trou"""
    ms = [SITE, iron_in_hole(0.3), blast_hole()]
    cam = cam_lerp(Cam(tuple(HOLE + np.array([0.18, 0.12, 0.2])), tuple(HOLE + np.array([0, 0.0, 0])), 40),
                   Cam(tuple(HOLE + np.array([0.12, 0.09, 0.14])), tuple(HOLE + np.array([0, 0.0, 0])), 36), lt / dur)
    rr = np.random.default_rng(4)
    for i in range(10):
        a = (lt * 0.35 + i * 0.03)
        v = rr.normal(size=3) * 0.15 + np.array([0, 0.25, 0])
        p = HOLE + np.array([0.03, 0.0, 0.03]) + v * a
        s = 0.02 * (1 - min(1, a * 1.5))
        if s > 0:
            ms.append(billboard(p, s, s, cam, (255, 220, 120), 'spark', emis=1.0))
    ms.append(billboard(HOLE + np.array([0.02, 0.02, 0.02]), 0.06, 0.06, cam, (255, 200, 80), 'spark', emis=1.0, alpha=0.8))
    env = ENV_DAY.copy(points=[(tuple(HOLE + np.array([0, 0.05, 0])), (255, 180, 80), 1.5, 0.6)])
    return merge(ms), cam, env, {}


# ------------------------------------------------------------------ 5 : boum, radiographie
def shot_boom(lt, dur, tg):
    """la poudre explose : la barre jaillit du trou et traverse la tête de Gage penché au-dessus ; il bascule"""
    cam = Cam((4.2, 1.8, 2.4), (0, 1.3, 0.3), 55)
    k = C2.decay(lt, 0.0, 4)
    cam = C2.shake(cam, 0.2 * k, tg)
    a = lt
    ms = [SITE, workers_bg(tg, 2)]
    fall = min(1.0, max(0.0, (a - 0.25) / 0.5))
    ang = ease(fall) * math.pi / 2
    gm = G_SHOUT.mesh((0, 0, 0), 0.0, dict(ll=(ang, 0.1), rl=(ang, 0.2), la=(2.2, 0.6, 0.4), ra=(2.0, 0.6, 0.3), lean=0.45 * (1 - fall), hp=0.35 * (1 - fall)))
    ms.append(gm.xf(M(trans(GAGE_POS + np.array([0, 0.17 * fall + 0.93 * (1 - fall), 0.5 * fall])), roty(math.pi), rotx(-ang), trans(0, -0.93, 0))))
    p = HOLE + np.array([0, 0.6 + 20 * a, 0.1 + 2 * a])
    ms.append(IRON.xf(M(trans(p), rotx(-0.08))))
    ms.append(strip([HOLE + np.array([0, 0.2, 0]), p], 0.04, cam, (255, 230, 180), emis=1.0, alpha=0.45))
    ms.append(smoke_sprites(HOLE + np.array([0, 0, -0.6]), a + 0.1, cam, n=6, size=1.0, rise=3, seed=2, col=(150, 145, 135), drift=(-0.3, 0, -0.4), alpha=max(0.0, 0.6 - a * 0.3)))
    if a < 0.25:
        ms.append(billboard(HOLE + np.array([0, 0.4, 0]), 1.2 * (1 - a * 3), 2.0 * (1 - a * 3), cam, (255, 255, 255), 'fire', emis=1.0))
    return merge(ms), cam, ENV_DAY, dict(flash=0.9 * C2.decay(lt, 0.0, 8))


def shot_xray(lt, dur, tg):
    prog = min(1.0, lt / (dur * 0.85))
    m, cam, env = xray_frame(lt, tg, prog, -0.9 + lt * 0.35, fov=38, dist=1.0)
    return m, cam, env, {}


# ------------------------------------------------------------------ 6 : 25 mètres
LAND = np.array([24.0, 0.05, 6.0])


def shot_flight(lt, dur, tg):
    Tf = min(1.5, dur * 0.6)
    a = min(lt, Tf)
    p0 = HOLE + np.array([0, 3.0, 0])
    v = (LAND - p0 + np.array([0, 4.9 * Tf * Tf, 0])) / Tf
    p = p0 + v * a + np.array([0, -4.9 * a * a, 0])
    vel = v + np.array([0, -9.8 * a, 0])
    m, _ = frame_along(p - vel / np.linalg.norm(vel) * 1.1, p)
    if lt >= Tf:
        m, _ = frame_along(LAND + np.array([-0.5, 0.75, -0.15]), LAND + np.array([0.0, -0.3, 0.0]))
        wob = 0.03 * math.sin((lt - Tf) * 30) * math.exp(-(lt - Tf) * 4)
        m = M(trans(LAND), rotz(wob), trans(-LAND)) @ m
    ms = [SITE, IRON.xf(m)]
    tgt = p if lt < Tf else LAND + np.array([0, 0.35, 0])
    cam = Cam(tuple(tgt + np.array([-2.5, 0.6, 4.5])), tuple(tgt), 50)
    if lt < Tf:
        trail = [p0 + v * b + np.array([0, -4.9 * b * b, 0]) for b in np.linspace(max(0, a - 0.35), a, 6)]
        ms.append(strip(trail, 0.06, cam, (255, 240, 200), emis=1.0, alpha=0.35))
    if lt >= Tf:
        ms.append(smoke_sprites(LAND, lt - Tf, cam, n=5, size=0.6, rise=0.8, seed=6, col=(180, 160, 130), alpha=max(0, 0.8 - (lt - Tf))))
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 7 : il se relève, la charrette
def lying_to_sit(who, pos, k, pose_extra=None, yaw=0.0):
    """k=0 couché sur le dos (tête vers -z du repère local), k=1 assis par terre"""
    a = (1 - k) * math.pi / 2
    pose = dict(ll=(math.pi / 2 - a, 0.05), rl=(math.pi / 2 - a, 0.05), la=(0.3 + 0.5 * k, 0.2, 0.5), ra=(0.3 + 0.5 * k, 0.2, 0.5))
    if pose_extra:
        pose.update(pose_extra)
    m = who.mesh((0, 0, 0), 0.0, pose)
    return m.xf(M(trans(pos), roty(yaw), trans(0, 0.17, 0), rotx(-a), trans(0, -0.93, 0)))


def shot_getup(lt, dur, tg):
    k = ease(min(1.0, max(0.0, (lt - 0.2) / 0.8)))
    p = np.array([0.3, 0.05, 2.0])
    who = GB if lt < 0.8 else gage('gage_b_shout', hat=False)
    ms = [SITE, lying_to_sit(who, p, k, yaw=math.pi + 0.3)]
    ms.append(W1S.mesh((1.6, 0.05, 0.9), -0.6, run_pose(tg * 9) if lt < 0.6 else dict(lean=0.4, la=(0.9, 0.1, 0.4), ra=(0.9, 0.1, 0.4))))
    ms.append(W2S.mesh((-1.0, 0.05, 0.9), 0.6, run_pose(tg * 9 + 1) if lt < 0.6 else dict(lean=0.3, hp=0.4)))
    cam = cam_lerp(Cam((2.6, 1.2, 4.4), (0.3, 0.6, 2.0), 50), Cam((2.2, 1.0, 3.8), (0.3, 0.7, 2.0), 48), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_speaks(lt, dur, tg):
    """assis par terre, Gage parle à ses ouvriers médusés"""
    p = np.array([0.3, 0.05, 2.0])
    talk = int(tg * 6) % 2
    who = GB if not talk else gage('gage_b_shout', hat=False)
    ms = [SITE, lying_to_sit(who, p, 1.0, dict(ra=(1.0 + 0.3 * math.sin(tg * 6), 0.3, 0.8), hp=-0.1), yaw=math.pi + 0.3)]
    ms.append(W1S.mesh((1.3, 0.05, 1.0), -0.8, dict(lean=0.4, la=(0.9, 0.1, 0.4), ra=(0.9, 0.1, 0.4))))
    ms.append(W2S.mesh((-1.2, 0.05, 1.3), 0.8, dict(lean=0.3, hp=0.4)))
    head = p + np.array([0, 0.9, 0])
    cam = Cam(tuple(head + np.array([-0.4, 0.15, -1.3])), tuple(head + np.array([0, 0.05, 0])), 45)
    return merge(ms), cam, ENV_DAY, {}


def shot_cart(lt, dur, tg):
    """Gage assis bien droit sur la charrette tirée par un bœuf"""
    x = -6 + lt * 1.4
    cm = M(trans(x, 0.05, 8), roty(math.pi / 2))
    ms = [SITE, cart(lt * 2).xf(cm), ox(tg * 4).xf(M(cm, trans(0, 0, 4.2)))]
    seat = (cm @ np.array([0, 0.97, -0.3, 1]))[:3]
    gm = GB.mesh((0, 0, 0), 0.0, dict(ll=(math.pi / 2, 0.05), rl=(math.pi / 2, 0.05), drop=0.0, la=(0.5, 0.2, 0.6), ra=(0.5, 0.2, 0.6)))
    ms.append(gm.xf(M(trans(seat), roty(math.pi / 2), trans(0, 0.17, 0), trans(0, -0.93, 0))))
    for i, dz in enumerate((-1.6, 1.8)):
        ms.append((W1 if i else W2).mesh((x - 0.5 - i, 0.05, 8 + dz), math.pi / 2, walk_pose(tg * 5 + i, 0.8)))
    cam = Cam((x + 4.0, 1.6, 13.5), (x, 1.3, 8), 50)
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 8 : « Docteur, voilà du travail »
def shot_doctor(lt, dur, tg):
    z = 13.0 - lt * 1.6
    ms = porch(lt, tg, 'gage_b_smile', False, doc_z=z, doc_walk=True)
    cam = cam_lerp(Cam((-4, 2.2, 16), (1.0, 1.2, 7), 50), Cam((-3.5, 2.0, 14.5), (1.0, 1.2, 7), 48), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_line(lt, dur, tg):
    """gros plan : Gage, tout sourire, lance sa réplique ; le médecin reste bouche bée"""
    ms = porch(lt, tg, 'gage_b_smile', talk=True, doc_z=7.4)
    head = PORCH_SEAT + np.array([0, 1.15, 0])
    cam = cam_lerp(Cam(tuple(head + np.array([-0.5, 0.05, 1.4])), tuple(head + np.array([0.1, -0.05, 0])), 40),
                   Cam(tuple(head + np.array([-0.4, 0.05, 1.1])), tuple(head + np.array([0.1, -0.05, 0])), 38), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_cta(lt, dur, tg):
    ms = porch(lt, tg, 'gage_b_smile', talk=True, doc_z=7.4)
    cam = cam_lerp(Cam((6, 3.0, 15), (1.0, 1.5, 5), 50), Cam((5, 2.6, 13), (1.0, 1.4, 5), 48), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_bizarre(lt, dur, tg):
    ms = porch(lt, tg, 'gage_b', talk=False, doc_z=7.4)
    head = PORCH_SEAT + np.array([0, 1.15, 0])
    u = ease(lt / max(dur, 0.1))
    cam = Cam(tuple(head + np.array([0.15, 0.02, lerp(1.5, 0.55, u)])), tuple(head + np.array([0, 0.02, 0])), 45)
    return merge(ms), cam, ENV_EVE, {}


# ------------------------------------------------------------------ 11 : œil, infection, guérison
BED_BODY = np.array([0.0, 0.72, -0.25])


def in_bed(who, extra=None):
    pose = dict(la=(0.15, 0.15, 0.2), ra=(0.15, 0.15, 0.2))
    if extra:
        pose.update(extra)
    m = who.mesh((0, 0, 0), 0.0, pose)
    return m.xf(M(trans(BED_BODY), rotx(-math.pi / 2), trans(0, 0.0, -0.12)))


QUILT = box(1.12, 0.12, 1.4, (255, 255, 255), 'quilt').xf(trans(0, 0.7, -0.75))


def shot_eye(lt, dur, tg):
    ms = [BEDROOM, in_bed(GB_BAND), QUILT, HARLOW.mesh((-0.95, 0, -1.55), math.pi / 2, dict(lean=0.4, hp=0.5, ik_r=(-0.2, 0.95, -1.9)))]
    cam = cam_lerp(Cam((1.1, 1.35, -1.2), (0, 0.8, -1.9), 45), Cam((0.95, 1.25, -1.35), (0, 0.8, -1.95), 42), lt / dur)
    return merge(ms), cam, ENV_ROOM.copy(points=[((0.95, 0.95, -2.05), (255, 190, 100), 1.2, 3.5)]), {}


def shot_fever(lt, dur, tg):
    sway = 0.2 * math.sin(tg * 3)
    ms = [BEDROOM, in_bed(GB_FEVER, dict(hy=sway)), QUILT]
    cam = Cam((0.7, 1.1, -1.55), (0, 0.8, -2.0), 40)
    cam = C2.shake(cam, 0.01, tg, 5)
    return merge(ms), cam, ENV_ROOM.copy(points=[((0.95, 0.95, -2.05), (255, 150, 80), 0.9, 3)], amb=0.35), dict(post_pil=C2.tint((255, 160, 120), 0.25))


def shot_recover(lt, dur, tg):
    """guéri : Gage se lève et sort de la chambre, bandeau sur la tête"""
    u = min(1.0, lt / dur)
    p = (1.0 - u * 0.5, 0, -0.6 + u * 1.5)
    ms = [BEDROOM, GB_BAND.mesh(p, 0.3, walk_pose(lt * 5, 0.7, face='gage_b_smile')), HARLOW.mesh((-1.2, 0, 0.2), 1.0, dict(ra=(0.4, 0.2, 0.6)))]
    cam = Cam((-0.5, 1.6, 2.6), (0.6, 1.2, 0), 50)
    return merge(ms), cam, ENV_ROOM.copy(points=[((0, 2.5, 0), (255, 230, 190), 0.6, 6)]), {}


# ------------------------------------------------------------------ 12 : « Ce n'est plus Gage »
def shot_friends(lt, dur, tg):
    p = np.array([0.0, 0.05, 2.0])
    ms = [SITE, GB.mesh(tuple(p + np.array([-3, 0, -2])), 0.4, dict(hat=False)),
          W1.mesh((2.0, 0.05, 2.8), 0.83, dict(hy=0.35 * math.sin(tg * 6), la=(0.4, 0.2, 1.4), ra=(0.4, 0.2, 1.4))),
          W2.mesh((3.0, 0.05, 2.0), 0.46, dict(hy=-0.3 * math.sin(tg * 5 + 1), hp=0.2))]
    cam = cam_lerp(Cam((4.6, 1.6, 5.2), (1.5, 1.4, 1.8), 45), Cam((4.3, 1.55, 4.7), (1.5, 1.4, 1.8), 43), lt / dur)
    return merge(ms), cam, ENV_EVE, {}


def shot_friend_close(lt, dur, tg):
    ms = [SITE, W1.mesh((2.0, 0.05, 2.8), -2.4, dict(hy=0.3 * math.sin(tg * 5), la=(0.4, 0.2, 1.4), ra=(0.4, 0.2, 1.4))),
          W2.mesh((3.0, 0.05, 2.0), -2.0, dict(hp=0.2))]
    head = np.array([2.0, 1.75, 2.8])
    d = np.array([-math.sin(2.4 - math.pi), 0, math.cos(2.4 - math.pi)])
    cam = Cam(tuple(head + np.array([-0.55, -0.02, -0.85])), tuple(head + np.array([0, -0.05, 0])), 42)
    return merge(ms), cam, ENV_EVE, {}


# ------------------------------------------------------------------ 13 : la légende
LEGEND = C2.chain(C2.tint((255, 70, 40), 0.55), lambda im: C2.vignette(im, 0.8))


def shot_legend(lt, dur, tg):
    """légende : un Gage furieux, les poings levés, filmé en contre-plongée"""
    ms = [SALOON, G_RAG.mesh((0, 0, 0), 0.0, dict(la=(1.7, 0.3, 1.9), ra=(1.7 + 0.4 * math.sin(tg * 8), 0.3, 1.9), lean=0.15))]
    cam = cam_lerp(Cam((0.4, 0.6, 2.2), (0, 1.5, 0), 55), Cam((0.3, 0.55, 1.8), (0, 1.55, 0), 52), lt / dur)
    return merge(ms), cam, ENV_ROOM.copy(points=[((0, 2.4, 1.0), (255, 140, 90), 1.0, 5)]), dict(post_pil=LEGEND)


def shot_brawl(lt, dur, tg):
    k = (lt * 3.0) % 1.0
    punch = math.sin(min(1.0, k * 2.5) * math.pi)
    ms = [SALOON, G_RAG.mesh((0, 0, 0.5), math.pi / 2, dict(ra=(1.55, 0.05, 1.8 - 1.7 * punch), la=(1.4, 0.1, 2.0), lean=0.2 + 0.15 * punch)),
          W1S.mesh((0.9, 0, 0.5), -math.pi / 2, dict(hy=0.5 * punch, lean=-0.2 * punch, la=(0.8, 0.4, 1.0), ra=(0.8, 0.4, 1.0)))]
    cam = Cam((0.45, 1.5, 2.6), (0.45, 1.3, 0.5), 50)
    cam = C2.shake(cam, 0.04 * punch, tg)
    return merge(ms), cam, ENV_ROOM.copy(points=[((0, 2.4, 1.0), (255, 140, 90), 1.0, 5)]), dict(post_pil=LEGEND)


def shot_drunk(lt, dur, tg):
    p = np.array([0.0, 0.0, -1.9])
    mouth = p + np.array([0, 1.62, 0.2])
    ms = [SALOON, G_RAG_N.mesh(tuple(p), 0.0, dict(ik_r=mouth + np.array([0.04, 0.0, 0.12]), hp=-0.35, la=(0.4, 0.1, 1.2), lean=-0.05)),
          bottle().xf(M(trans(mouth + np.array([0.04, 0.02, 0.14])), rotx(2.1)))]
    cam = Cam((0.9, 1.5, 0.2), (0, 1.45, -1.9), 45)
    return merge(ms), cam, ENV_ROOM.copy(points=[((0, 2.4, -0.5), (255, 140, 90), 1.0, 5)]), dict(post_pil=LEGEND)


def shot_vagabond(lt, dur, tg):
    x = -2 + lt * 1.2
    ms = [HOTEL.xf(trans(0, 0, -12)), grid(-40, -40, 40, 40, 6, 6, None, (255, 255, 255), 'dirt', 3.0),
          G_RAG_N.mesh((x, 0, 2), math.pi / 2, walk_pose(lt * 4, 0.6, hp=0.5, lean=0.25))]
    cam = Cam((x + 4, 1.4, 6), (x, 1.1, 2), 50)
    ms.append(C2.rain_mesh(cam, tg, 120, 8, 3))
    return merge(ms), cam, ENV_NIGHT, dict(post_pil=LEGEND)


# ------------------------------------------------------------------ 14 : le problème
def shot_book(lt, dur, tg):
    """le livre de 1868 tombe sur le bureau et s'ouvre"""
    t_hit = 0.3
    y = 0.84 + max(0.0, 1 - lt / t_hit) * 0.5
    op = min(1.0, max(0.0, (lt - t_hit - 0.3) / 0.3))
    ms = [DESK, book(op).xf(trans(0.0, y, 0.1))]
    cam = Cam((0.0, 1.45, 0.75), (0.0, 0.86, 0.05), 45)
    cam = C2.shake(cam, 0.03 * C2.decay(lt, t_hit, 6), tg)
    return merge(ms), cam, ENV_ROOM.copy(points=[((0.9, 1.1, -0.3), (255, 200, 120), 1.0, 3)]), {}


# ------------------------------------------------------------------ 15 : la réalité, le Chili
SC_SEAT = np.array([0, 2.2, 1.45])


def coach_scene(lt, tg, z0=-60.0, speed=7.0):
    z = z0 + lt * speed
    cm = M(trans(0, 0, z))
    ms = [ROAD, ANDES, stagecoach(lt * speed / 0.7).xf(cm)]
    for i, (hx, hz) in enumerate(((-0.55, 3.6), (0.55, 3.6), (-0.55, 6.0), (0.55, 6.0))):
        ms.append(horse(tg * 9 + i * 0.7, 1.0).xf(M(cm, trans(hx, 0, hz))))
    seat = (cm @ np.append(SC_SEAT, 1))[:3]
    gm = GB_COAT.mesh((0, 0, 0), 0.0, dict(ll=(math.pi / 2, 0.9), rl=(math.pi / 2, 0.9), la=(0.9, 0.15, 0.5), ra=(0.9, 0.15, 0.5), hp=-0.05))
    ms.append(gm.xf(M(trans(seat), trans(0, 0.12, 0), trans(0, -0.93, 0))))
    hands = [GB_COAT.attach['hand_l'], GB_COAT.attach['hand_r']]
    for h, (hx, hz) in zip(hands, ((-0.55, 6.0), (0.55, 6.0))):
        hp = (M(trans(seat), trans(0, 0.12, 0), trans(0, -0.93, 0)) @ h)[:3, 3]
        ms.append(rod(hp, (cm @ np.array([hx, 1.9, hz + 0.6, 1]))[:3], 0.012, (60, 40, 25), n=3))
    return ms, z, seat


def shot_chile(lt, dur, tg):
    ms, z, seat = coach_scene(lt, tg)
    cam = Cam((7, 3.0, z + 16), (0, 1.8, z + 2), 50)
    ms.append(smoke_sprites((0, 0.2, z - 1.5), tg, cam, n=6, size=1.8, rise=1.5, seed=5, col=(210, 185, 150), drift=(0.2, 0, -3), alpha=0.6))
    return merge(ms), cam, ENV_CHILE, {}


def shot_chile_close(lt, dur, tg):
    ms, z, seat = coach_scene(lt + 3.0, tg)
    head = seat + np.array([0, 0.85, 0.05])
    cam = Cam(tuple(head + np.array([0.9, 0.0, 1.5])), tuple(head + np.array([0, -0.05, 0])), 42)
    cam = C2.shake(cam, 0.015, tg, 9)
    return merge(ms), cam, ENV_CHILE, {}


# ------------------------------------------------------------------ 16 : mort, Harvard
def shot_sunset(lt, dur, tg):
    ms = [grid(-200, -200, 200, 30, 8, 8, lambda x, z: 4 * math.exp(-((x) ** 2 + (z + 5) ** 2) / 900), (255, 255, 255), 'grass_dry', 4.0),
          box(2000, 0.1, 2000, (255, 255, 255), 'sea', ts=10).xf(trans(0, -0.5, -1050))]
    ms.append(box(0.1, 1.0, 0.1, (220, 215, 200)).xf(trans(0, 4.0, -5)))
    ms.append(box(0.5, 0.1, 0.1, (220, 215, 200)).xf(trans(0, 4.7, -5)))
    cam = cam_lerp(Cam((3, 5.5, 5), (0, 4.6, -5), 45), Cam((2.4, 5.3, 2), (0, 4.6, -5), 45), lt / dur)
    return merge(ms), cam, ENV_SUNSET, {}


def shot_harvard(lt, dur, tg):
    ms = [MUSEUM, SKULL_BONE.xf(M(trans(-0.25, 1.02, 0.0), roty(0.6))), IRON.xf(M(trans(-0.5, 0.94, 0.12), rotz(-math.pi / 2), rotx(0.15)))]
    cam = cam_lerp(Cam((1.0, 1.7, 2.0), (0, 1.05, 0), 45), Cam((0.6, 1.5, 1.3), (-0.1, 1.05, 0), 42), lt / dur)
    return merge(ms), cam, ENV_MUSEUM.copy(points=[((0, 2.4, 0.3), (255, 235, 200), 1.6, 3)]), {}


# ------------------------------------------------------------------ 17 : le portrait
PORTRAIT = C2.chain(C2.tint((255, 220, 170), 0.15, sepia=True), lambda im: C2.vignette(im, 0.95, (40, 28, 18)))


def shot_portrait(lt, dur, tg):
    """daguerréotype : Gage, élégant, tient sa barre de fer"""
    pose = dict(ik_l=(-0.3, 0.98, 0.3), la=(0.2, 0.1, 0.3), ra=(0.15, 0.1, 0.2), hp=0.05)
    ms = [GB_COAT_N.mesh((0, 0, 0), 0.0, pose), IRON.xf(trans(-0.3, 0.05, 0.33)),
          box(4, 3, 0.1, (150, 140, 125), 'cloth').xf(trans(0, 0, -1.2)), box(4, 0.05, 4, (110, 90, 70), 'planks').xf(trans(0, -0.05, 0))]
    u = ease(lt / max(dur, 0.1))
    cam = Cam((0.1, 1.45, lerp(2.4, 1.3, u)), (0, 1.25, 0), 45)
    fade = max(0.0, (lt - dur + 0.6) / 0.6)
    return merge(ms), cam, ENV_MUSEUM.copy(points=[((1.0, 2.2, 1.5), (255, 240, 210), 1.0, 5)]), dict(post_pil=PORTRAIT, fade=fade)


# ------------------------------------------------------------------ montage
add('hook_xray', 0.0, shot_hook_xray)
add('hook_talk', WT(0, 'et') - 0.05, shot_hook_talk)
add('vermont', T(1), shot_vermont)
add('gage_intro', WT(1, 'Phineas') - 0.05, shot_gage_intro)
add('blast_demo', T(2), shot_blast_demo)
add('drill', T(3), shot_drill)
add('powder', T(3, 4) - 0.15, shot_powder)
add('tamp', WT(3, 'tasse') - 0.25, shot_tamp)
add('iron_hero', WT(3, 'mètre') - 0.35, shot_iron_hero)
add('lookback', T(4), shot_lookback)
add('strike', WT(4, 'La') - 0.1, shot_strike)
add('boom', T(5), shot_boom)
add('xray', WT(5, 'sous') - 0.1, shot_xray)
add('flight', T(6), shot_flight)
add('getup', T(7), shot_getup)
add('cart', WT(7, 'assoit') - 0.25, shot_cart)
add('doctor', T(8), shot_doctor)
add('line', WT(8, 'Docteur,') - 0.15, shot_line)
add('cta', T(9), shot_cta)
add('bizarre', T(10), shot_bizarre)
add('eye', T(11), shot_eye)
add('fever', WT(11, 'Une') - 0.1, shot_fever)
add('recover', WT(11, 'Mais') - 0.1, shot_recover)
add('friends', T(12), shot_friends)
add('friend_close', WT(12, 'disaient') - 0.1, shot_friend_close)
add('legend', T(13), shot_legend)
add('brawl', WT(13, 'Bagarreur.') - 0.1, shot_brawl)
add('vagabond', WT(13, 'Vagabond.') - 0.1, shot_vagabond)
add('book', T(14), shot_book)
add('chile', T(15), shot_chile)
add('chile_close', WT(15, 'Pas') - 0.1, shot_chile_close)
add('sunset', T(16), shot_sunset)
add('harvard', WT(16, 'Son') - 0.1, shot_harvard)
add('portrait', T(17), shot_portrait)

tl.overlay = C2.overlays(
    C2.hook_title(['1 BARRE DE FER', 'DANS LE CRÂNE.'], 0.0, T(1) - 0.05, y=250, accent=1),
    C2.badge('1,10 m  ·  6 kg', S('iron_hero') + 0.15, S('lookback') - S('iron_hero') - 0.2),
    C2.badge('25 m', S('flight') + 1.0, S('getup') - S('flight') - 1.1),
    C2.badge('LA LÉGENDE', S('legend') + 0.1, S('book') - S('legend') - 0.15, col=(255, 110, 90)),
    C2.badge('PUBLIÉ EN 1868', S('book') + 0.35, S('chile') - S('book') - 0.4),
    C2.badge('LA RÉALITÉ', S('chile') + 0.1, S('chile_close') - S('chile') - 0.1, col=(120, 230, 140)),
    C2.cta(T(9) - 0.1, max(2.6, T(10) - T(9) + 0.1)),
)

subs = Subs(timing)


def build_audio(path):
    dur = tl.duration()
    mx = A.Mixer(dur)
    mx.add(C2.impact(), 0.0, 0.8)
    mx.add(C2.heartbeat(2.0, 90), 0.1, 0.5)
    mx.add(C2.riser(0.8), 0.0, 0.3)
    mx.add(A.birds(8), S('hook_talk'), 0.35, length=S('vermont') - S('hook_talk'))
    # chantier
    mx.add(A.birds(10), S('vermont'), 0.35, 0.3, 0.3, length=S('drill') - S('vermont'))
    mx.add(A.wind(10), S('vermont'), 0.2, length=S('boom') - S('vermont'))
    for i in range(int((S('powder') - S('vermont')) * 2.5)):
        mx.add(A.clank(0.3), S('vermont') + i * 0.4, 0.12 if S('vermont') + i * 0.4 < S('drill') else 0.3)
    mx.add(A.explosion(2.5), S('blast_demo') + 0.3, 0.7)
    mx.add(C2.impact(), S('blast_demo') + 0.3, 0.4)
    for i in range(int((S('iron_hero') - S('powder')) / 0.07)):
        mx.add(A.tick(), S('powder') + i * 0.07, 0.12 if S('powder') + i * 0.07 < S('tamp') else 0.0)
    for i in range(int((S('iron_hero') - S('tamp')) * 7 / (2 * math.pi)) + 1):
        mx.add(A.thwack(), S('tamp') + 0.2 + i * 2 * math.pi / 7, 0.4)
    mx.add(C2.ding(), S('iron_hero') + 0.15, 0.4)
    mx.add(C2.riser(1.4), S('lookback'), 0.5)
    mx.add(A.clank(0.5), S('strike') + 0.25, 0.8)
    mx.add(A.zap(0.6), S('strike') + min(0.6, (S('boom') - S('strike')) * 0.4), 0.5)
    mx.add(C2.heartbeat(1.5, 120), S('strike') + 0.6, 0.5)
    mx.add(A.explosion(3), S('boom'), 1.0)
    mx.add(C2.impact(), S('boom'), 0.9)
    mx.add(C2.whoosh_(1.0) if hasattr(C2, 'whoosh_') else A.whoosh(1.0), S('boom') + 0.1, 0.6)
    mx.add(C2.heartbeat(3.0, 70), S('xray'), 0.6)
    mx.add(C2.riser(0.8), S('xray'), 0.25)
    mx.add(A.whoosh(1.2), S('flight') + 0.1, 0.5)
    mx.add(A.thwack(), S('flight') + min(1.5, (S('getup') - S('flight')) * 0.6), 0.8)
    mx.add(C2.ding(), S('flight') + 1.0, 0.35)
    mx.add(A.crowd(4), S('getup'), 0.3, 0.2, 0.3, length=S('cart') - S('getup'))
    mx.add(A.wheel_rattle(4), S('cart'), 0.5, length=S('doctor') - S('cart'))
    mx.add(A.footsteps(4, 2.2), S('doctor'), 0.4, length=S('line') - S('doctor'))
    mx.add(A.birds(8), S('doctor'), 0.3, length=S('eye') - S('doctor'))
    mx.add(C2.pop(), T(9) + 0.05, 0.5)
    mx.add(C2.ding(), T(9) + max(2.6, T(10) - T(9) + 0.1) * 0.62, 0.45)
    mx.add(C2.riser(1.2), S('bizarre'), 0.5)
    mx.add(C2.impact(), S('eye'), 0.4)
    mx.add(C2.heartbeat(3, 100), S('fever'), 0.5, length=S('recover') - S('fever'))
    mx.add(A.footsteps(3, 2), S('recover'), 0.4, length=S('friends') - S('recover'))
    mx.add(A.wind(6), S('friends'), 0.25, length=S('legend') - S('friends'))
    mx.add(C2.impact(), S('legend'), 0.7)
    mx.add(A.crowd(4), S('legend'), 0.25, length=S('vagabond') - S('legend'))
    mx.add(A.thwack(), S('brawl') + 0.25, 0.7)
    mx.add(A.thwack(), S('brawl') + 0.58, 0.7)
    mx.add(A.rain(5), S('vagabond'), 0.4, length=S('book') - S('vagabond'))
    mx.add(C2.record_scratch(), S('book') - 0.05, 0.7)
    mx.add(A.thwack(), S('book') + 0.3, 0.8)
    mx.add(C2.gallop(6), S('chile'), 0.6, 0.2, 0.5, length=S('sunset') - S('chile'))
    mx.add(A.wheel_rattle(5), S('chile'), 0.3, length=S('sunset') - S('chile'))
    mx.add(A.waves(6), S('sunset'), 0.3, 0.4, 0.3, length=S('harvard') - S('sunset'))
    mx.add(C2.ding(), S('harvard') + 0.2, 0.3)
    mx.add(C2.heartbeat(3, 60), S('portrait'), 0.4)
    C2.music_bed(mx, S('vermont'), S('lookback'), 'tense', 100, 0.15, 1)
    C2.music_bed(mx, S('xray'), S('legend'), 'tense', 112, 0.14, 2)
    C2.music_bed(mx, S('legend'), S('book'), 'epic', 90, 0.22, 3)
    C2.music_bed(mx, S('chile'), S('sunset'), 'hope', 120, 0.2, 4)
    C2.music_bed(mx, S('sunset'), dur, 'sad', 64, 0.18, 5)
    C2.cut_sounds(mx, list(SHOT_STARTS.values()), 0.1)
    mx.save(path)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--part':
        part_main(tl, subs, sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == '--sheet':
        ts = sorted(SHOT_STARTS.values())
        times = []
        for i, t0 in enumerate(ts):
            t1 = ts[i + 1] if i + 1 < len(ts) else tl.duration()
            times += [t0 + 0.05, (t0 + t1) / 2, t1 - 0.1]
        for k in range(0, len(times), 36):
            contact_sheet(tl, times[k:k + 36], os.path.join(HERE, f'sheet{k // 36 + 1}.png'), subs, cols=6, scale=0.18)
    elif len(sys.argv) > 1 and sys.argv[1] == '--at':
        for s in sys.argv[2:]:
            frame(tl, float(s), subs).resize((540, 960)).save(os.path.join(HERE, f'at_{s}.png'))
    elif len(sys.argv) > 1 and sys.argv[1] == '--draft':
        build_audio(os.path.join(HERE, 'sfx.wav'))
        render_video(tl, os.path.join(HERE, 'gage_draft.mp4'), os.path.join(HERE, 'sfx.wav'), subs)
    else:
        build_audio(os.path.join(HERE, 'sfx.wav'))
        mix_voice(os.path.join(HERE, 'voix.wav'), os.path.join(HERE, 'sfx.wav'), os.path.join(HERE, 'mix.wav'))
        render_video(tl, os.path.join(HERE, 'Gage_Good2No.mp4'), os.path.join(HERE, 'mix.wav'), subs)
