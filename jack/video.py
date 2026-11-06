"""Vidéo : Jack, le babouin aiguilleur."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n', '/home/claude/g2n/jack']
import numpy as np
from world import *
from video_core import *
from scripts import JACK as LINES
import audio as A

HERE = '/home/claude/g2n/jack'
TIMING_FILE = os.path.join(HERE, 'timing.json')
timing = load_timing(TIMING_FILE) if os.path.exists(TIMING_FILE) else est_timing(LINES)
tl = Timeline(timing)
T = tl.T
WT = tl.word_t
SHOT_STARTS = {}


def add(name, t0, fn):
    SHOT_STARTS[name] = t0
    tl.add(t0, fn)


def S(name):
    return SHOT_STARTS[name]


# ------------------------------------------------------------------ personnages
JAMES = james()
JAMES_PEG = james(peg=True)


def crutches(P, at):
    ms = []
    for k in ('hand_l', 'hand_r'):
        h = at[k]
        p = h[:3, 3]
        foot = np.array([p[0], 0.0, p[2]]) + (h[:3, :3] @ np.array([0, 0, 0.25]))
        foot[1] = at['foot_l'][1, 3] - 0.47 + 0.0 if False else 0.0
        ms.append(strip_box(p + np.array([0, 0.25, 0]), foot, 0.035, (130, 95, 60)))
    return merge(ms)


def strip_box(a, b, w, col):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    L = np.linalg.norm(d)
    yaw = math.atan2(d[0], d[2])
    pitch = -math.asin(d[1] / L)
    return box(w, w, L, col).xf(M(trans((a + b) / 2 - np.array([0, w / 2, 0])), roty(yaw), rotx(pitch), trans(0, 0, -L / 2), trans(0, 0, L / 2)))


class JamesCrutch(Human):
    pass


JAMES_CR = james(peg=True)
JAMES_CR.extra = None


def james_crutch_mesh(pos, yaw, phase, y0=0.0, face='james'):
    """James sur béquilles qui avance"""
    s = math.sin(phase)
    pose = dict(la=(0.35 + 0.25 * s, 0.25, 0.1), ra=(0.35 + 0.25 * s, 0.25, 0.1), ll=(0.2 * -s, 0.1), rl=(0.2 * s, 0.1),
                face=face, lean=0.08)
    m = JAMES_CR.mesh(pos, yaw, pose)
    at = JAMES_CR.attach
    ms = [m]
    for k in ('hand_l', 'hand_r'):
        h = at[k]
        p = h[:3, 3]
        fwd = np.array([math.sin(yaw), 0, math.cos(yaw)])
        foot = np.array([p[0], y0, p[2]]) + fwd * 0.1 * s
        top = p + np.array([0, 0.32, 0]) - fwd * 0.05
        ms.append(strip_box(top, foot, 0.04, (130, 95, 60)))
        ms.append(box(0.06, 0.04, 0.2, (90, 65, 40)).xf(M(trans(top), roty(yaw))))
    return merge(ms)


# ------------------------------------------------------------------ décor gare
def station_world():
    g = grid(-120, -120, 160, 80, 14, 10, None, (255, 255, 255), 'karoo', 3.0)
    ms = [g, track(-120, 160, 0.0)]
    # embranchement + voie de garage
    ang = math.atan2(4.5, 22)
    ms.append(track(0, 22.5, 0).xf(M(trans(18, 0, 0), roty(-ang))))
    ms.append(track(40, 160, 4.5))
    ms.append(platform(-16, 16, -5.2, -1.65))
    ms.append(station_building().xf(trans(0, 0.9, -8.6)))
    ms.append(signal_box_ext().xf(trans(26, 0, -4.2)))
    ms.append(semaphore(0).xf(trans(38, 0, -2.3)))
    ms.append(hills(-180, 3))
    rr = np.random.default_rng(5)
    for i in range(40):
        x, z = rr.uniform(-100, 140), rr.uniform(-60, 60)
        if -10 < z < 10:
            continue
        if rr.random() < 0.4:
            ms.append(aloe(i, 1.2 + rr.random()).xf(trans(x, 0, z)))
        else:
            ms.append(bush(0.5 + rr.random() * 0.6, i).xf(trans(x, 0, z)))
    for i, x in enumerate((-40, -28, 45, 60)):
        ms.append(deciduous(9, 3, seed=i, col=(200, 220, 190)).xf(trans(x, 0, -18 - i * 3)))
    for i, x in enumerate((-30, -18, -6, 8, 22)):
        ms.append(cape_house((235, 225, 200) if i % 2 else (225, 215, 185)).xf(M(trans(x, 0, -30), roty(0))))
    ms.append(grass_tufts(-60, -25, 80, -6, 900, 3, col=(150, 140, 80)))
    ms.append(grass_tufts(-60, 7, 80, 30, 700, 4, col=(150, 140, 80)))
    return merge(ms)


STATION = station_world()
ENV_DAYC = ENV_DAY.copy(points=[((26, 4.2, -3.6), (255, 235, 200), 0.6, 4)])


def points_blades(pull):
    """lames d'aiguille qui bougent (x 18..21)"""
    off = 0.08 * (1 - pull)
    ms = []
    for s in (-1, 1):
        z = s * TRACK_G / 2 - s * 0.09 + (off if s < 0 else -off) * 0 + (0.09 * pull * -s if s > 0 else 0.09 * (1 - pull) * -s)
        ms.append(box(3.0, 0.1, 0.05, (200, 200, 200), 'metal').xf(trans(19.5, 0.1, z)))
    ms.append(box(0.08, 0.06, 1.8, (120, 120, 120)).xf(trans(18.2, 0.08, 0.6)))
    ms.append(points_lever(pull).xf(M(trans(18.2, 0, 1.9), roty(math.pi / 2))))
    return merge(ms)


def jack_at_lever(base, i, pull, cap=False, yaw=0.0, mouth=0.0, hy=0.0):
    """Jack debout, les deux mains sur la poignée du levier i (il recule en tirant)"""
    g = lever_grip(base, i, pull)
    body = np.array([g[0] + 0.02, base[1], g[2] - 0.52])
    lean = 1.05 + 0.3 * pull
    return JACK.mesh(tuple(body), yaw, bab_stand(pitch=lean, ik_l=g + np.array([-0.05, 0, 0]), ik_r=g + np.array([0.05, 0, 0]),
                                                  cap=cap, mouth=mouth, hy=hy, hp=-0.25))


def james_at_lever(base, i, pull, face='james'):
    g = lever_grip(base, i, pull)
    body = (g[0] + 0.02, base[1], g[2] - 0.62)
    return JAMES_PEG.mesh(body, 0.0, dict(ik_l=g + np.array([-0.06, 0, 0]), ik_r=g + np.array([0.06, -0.12, 0]), lean=0.1 + 0.15 * pull, face=face))


BOX_BASE = np.array([26.0, 2.5, -3.5])


def jack_in_box(lt, pull_i=None, pull=0.0, cap=False, face_cam=False):
    """Jack aux leviers vu de l'extérieur (cabine à x=26, z=-4.2 ; plancher y=2.5)"""
    pulls = [0] * 6
    i = pull_i if pull_i is not None else 2
    pulls[i] = pull
    ms = [lever_frame(pulls).xf(trans(BOX_BASE)), box(4.2, 0.04, 3.2, (140, 105, 70), 'planks').xf(trans(26, 2.5, -4.2)),
          box(4.2, 2.0, 0.1, (220, 212, 190), 'planks_white', faces='f').xf(trans(26, 2.5, -5.8)),
          clock_mesh(10, 10, 0.24).xf(trans(24.6, 3.95, -5.72))]
    ms.append(jack_at_lever(BOX_BASE, i, pull, cap=cap, hy=0.5 if face_cam else 0.0))
    return merge(ms)


def train_at(x, parts=('loco', 'tender', 'car', 'car', 'car'), z=0.0, wr=None):
    return train(list(parts), x=x, z=z, wheel_rot=-x / 0.75 if wr is None else wr)


def steam_puffs(base, lt, cam, n=6, size=0.8, rise=4.0, seed=0, alpha=0.75):
    return smoke_sprites(base, lt * 1.6, cam, n=n, size=size, rise=rise, seed=seed, col=(255, 255, 255), drift=(-1.5, 0, 0.1), alpha=alpha)


def puff_tex_sprites(base, lt, cam, n=6, size=0.8, rise=3.0, seed=0, drift=(-1.2, 0, 0)):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        life = (lt * 0.6 + rr.random()) % 1.0
        off = np.array(drift) * life * rise + np.array([(rr.random() - .5) * size, life * rise, (rr.random() - .5) * size])
        s = size * (0.5 + life * 1.5)
        ms.append(billboard(np.asarray(base) + off, s, s, cam, (255, 255, 255), 'puff', emis=0.4, alpha=0.9 * (1 - life)))
    return merge(ms)


# ------------------------------------------------------------------ 0 : accroche
def shot_hook(lt, dur, tg):
    x = 14 + lt * 7
    cam = cam_lerp(Cam((40, 1.6, 7.5), (24, 2.6, -2.0), 55), Cam((39, 1.7, 7.0), (25, 2.8, -2.5), 55), lt / dur)
    ms = [STATION, train_at(x), points_blades(0), jack_in_box(lt, 2, 0.5 + 0.5 * math.sin(lt * 2))]
    ms.append(puff_tex_sprites((x - 4.3 + 2.6, 3.9, 0), lt, cam, 7, 0.9, 4, 1))
    return merge(ms), cam, ENV_DAYC, {}


def shot_hook2(lt, dur, tg):
    pull = ease(min(1, lt / 0.9))
    cam = cam_lerp(Cam((24.9, 4.45, -5.2), (25.8, 3.5, -3.3), 58), Cam((24.95, 4.42, -5.1), (25.8, 3.5, -3.3), 58), lt / dur)
    ms = [STATION, jack_in_box(lt, 2, pull)]
    return merge(ms), cam, ENV_DAYC, {}


# ------------------------------------------------------------------ 1 : Jumper
def plains():
    g = grid(-300, -100, 300, 100, 12, 6, None, (255, 255, 255), 'karoo', 3.0)
    ms = [g, track(-300, 300, 0.0), hills(-160, 7)]
    rr = np.random.default_rng(8)
    for i in range(70):
        x, z = rr.uniform(-280, 280), rr.uniform(-80, 80)
        if abs(z) < 6:
            continue
        ms.append((aloe(i) if rr.random() < 0.4 else bush(0.6, i)).xf(trans(x, 0, z)))
    for i in range(30):
        x = -280 + i * 20
        ms.append(cyl(0.06, 0.05, 6, 5, (110, 85, 60)).xf(trans(x, 0, -4)))
    ms.append(grass_tufts(-150, -40, 150, -3, 1500, 9, col=(150, 140, 80)))
    ms.append(grass_tufts(-150, 3, 150, 40, 1500, 10, col=(150, 140, 80)))
    return merge(ms)


PLAINS = plains()
GOODS = ('loco', 'tender', 'van', 'van', 'van', 'open', 'van')


def goods_train(x):
    return train_at(x, GOODS)


# positions des fourgons (centres) relatifs à x de la loco
def van_x(xh, idx):
    L = {'loco': 8.6, 'tender': 4.0, 'car': 8.0, 'open': 5.0, 'van': 5.0}
    cx = xh
    for i, p in enumerate(GOODS):
        cx -= L[p] / 2
        if i == idx:
            return cx
        cx -= L[p] / 2 + 0.4


VAN_TOP = 3.22


def flag_mesh(col=(200, 30, 30)):
    return merge([cyl(0.012, 0.012, 0.6, 4, (120, 90, 60)), box(0.02, 0.25, 0.35, col).xf(trans(0, 0.35, 0.17))])


def lantern():
    return merge([box(0.14, 0.2, 0.14, (60, 60, 60)).xf(trans(0, -0.25, 0)), box(0.1, 0.12, 0.1, (255, 220, 140), emis=0.8).xf(trans(0, -0.21, 0)),
                  cyl(0.008, 0.008, 0.08, 4, (60, 60, 60)).xf(trans(0, -0.05, 0))])


def shot_jumper(lt, dur, tg):
    """James au travail : il longe le train de marchandises arrêté, vérifie les attelages et fait signe au mécanicien"""
    xh = -40.0
    v3, v4 = van_x(xh, 3), van_x(xh, 4)
    u = lt / dur
    jx = v4 + 3.5 - u * 0.5 + (v3 - v4) * min(1, u * 1.4)
    jx = v4 - 1.0 + u * 7.5
    cam = cam_lerp(Cam((v4 - 0.5, 1.7, 6.2), (v4 + 0.5, 1.1, 1.5), 55), Cam((v4 + 4.6, 1.7, 6.2), (v4 + 3.2, 1.1, 1.5), 55), u)
    ms = [PLAINS, goods_train(xh)]
    gap_x = v4 + 2.7  # entre deux fourgons : il vérifie l'attelage
    if u < 0.45:
        pose = walk_pose(lt * 5, 0.7, hy=-0.4, hand_r=lantern(), la=(0.1, 0.15, 0.2))
        ms.append(JAMES.mesh((jx, 0, 1.75), math.pi / 2, pose))
    elif u < 0.7:
        ms.append(JAMES.mesh((gap_x, 0, 1.6), math.pi, dict(lean=0.5, hp=0.3, ik_r=(gap_x - 0.05, 0.95, 0.75), ik_l=(gap_x + 0.15, 1.0, 0.8), face='james')))
    else:
        k = (u - 0.7) / 0.3
        ms.append(JAMES.mesh((gap_x + 0.2, 0, 1.7), math.pi / 2 + 0.3, dict(ra=(2.6 + 0.3 * math.sin(lt * 9), 0.5, 0.2), hand_r=flag_mesh(), hy=0.5, face='james_open')))
    ms.append(puff_tex_sprites((xh - 1.7, 3.9, 0), lt, cam, 6, 0.9, 3, 2, drift=(-0.3, 0, 0)))
    return merge(ms), cam, ENV_DAY, {}


def jump_arc(u, x0, x1, y0=3.16, h=1.0):
    return x0 + (x1 - x0) * u, y0 + 4 * h * u * (1 - u)


TRAIN_V = 5.0


RUN_V = 2.6


def roof_run_x(lt, x_take, t_take):
    return x_take - RUN_V * (t_take - lt)


def train_x(t_abs):
    return -40 + (t_abs - S('jumper')) * TRAIN_V


def roof_plan():
    """trajet de James sur les toits (coordonnée relative à la loco) : court sur le fourgon 4, saute sur le 3,
    court sur le 3, saute vers le 2… et rate"""
    t0 = S('jump')
    tj1 = WT(1, 'saute')
    ts = WT(2, 'chute…')
    fly = 0.55
    v2, v3, v4 = van_x(0, 2), van_x(0, 3), van_x(0, 4)
    return dict(t0=t0, tj1=tj1, l1=tj1 + fly, tj2=ts - fly, ts=ts, fly=fly,
                a=v4 - 2.2, b=v4 + 2.25, c=v3 - 2.25, d=v3 + 2.25, e=v2 - 2.6)


def james_roof(t):
    """renvoie (rel_x, y, z, pose, roll, slipped) au temps absolu t"""
    P = roof_plan()
    jump_pose = dict(ll=(1.1, 1.5), rl=(-0.5, 0.6), la=(1.0, 0.4, 0.5), ra=(-0.4, 0.4, 0.6), lean=0.35, face='james_open')
    if t < P['tj1']:
        u = (t - P['t0']) / (P['tj1'] - P['t0'])
        x = P['a'] + (P['b'] - P['a']) * max(0.0, u)
        return x, VAN_TOP, 0.0, run_pose(x * 2.6, lean=0.2), 0.0, False
    if t < P['l1']:
        u = (t - P['tj1']) / P['fly']
        return P['b'] + (P['c'] - P['b']) * u, VAN_TOP + 4 * 0.6 * u * (1 - u), 0.0, jump_pose, 0.0, False
    if t < P['tj2']:
        u = (t - P['l1']) / (P['tj2'] - P['l1'])
        x = P['c'] + (P['d'] - P['c']) * u
        return x, VAN_TOP, 0.0, run_pose(x * 2.6, lean=0.25, face='james_smile'), 0.0, False
    if t < P['ts']:
        u = (t - P['tj2']) / P['fly']
        return P['d'] + (P['e'] - P['d']) * u, VAN_TOP + 4 * 0.35 * u * (1 - u) - 0.1 * u, 0.0, jump_pose, 0.0, False
    d = t - P['ts']
    pose = dict(ll=(-0.4, 0.3), rl=(1.0, 0.8), la=(2.6, 0.9, 0.2), ra=(1.8, 1.1, 0.3), lean=-0.4, face='james_shout')
    z = min(1.7, 2.2 * d * d + 0.9 * d)
    y = VAN_TOP - 0.1 - 4.9 * max(0.0, d - 0.12) ** 2
    return P['e'] - 0.4 * min(d, 0.4), y, z, pose, min(1.3, d * 2.5), True


def roof_cam(t):
    P = roof_plan()
    tc = min(t, P['ts'])
    x, y, _, _, _, _ = james_roof(tc)
    px = train_x(tc) + x
    return Cam((px + 0.6, VAN_TOP + 1.3, 6.2), (px + 0.4, VAN_TOP + 0.7, 0), 60)


def roof_shot(lt, dur, tg):
    t = tg
    xh = train_x(t)
    x, y, z, pose, roll, slipped = james_roof(t)
    P = roof_plan()
    if slipped:
        # il garde l'élan du train en tombant, le train continue
        px = train_x(P['ts']) + x + TRAIN_V * 0.5 * (t - P['ts'])
    else:
        px = xh + x
    cam = roof_cam(t)
    ms = [PLAINS, goods_train(xh)]
    if y > 0.3:
        ms.append(JAMES.mesh((0, 0, 0), 0.0, pose).xf(M(trans(px, y, z), roty(math.pi / 2), rotx(-roll * 0.4), rotz(roll))))
    ms.append(puff_tex_sprites((xh - 1.7, 3.9, 0), lt, cam, 7, 1.0, 4, 3, drift=(-2.5, 0, 0)))
    fade = max(0.0, min(1.0, (t - P['ts'] - 0.45) / 0.15)) if slipped else 0.0
    return merge(ms), cam, ENV_DAY, dict(fade=fade)


def shot_jump(lt, dur, tg):
    return roof_shot(lt, dur, tg)


# ------------------------------------------------------------------ 2 : chute
def shot_fall(lt, dur, tg):
    return roof_shot(lt, dur, tg)


HOSPITAL = None


def hospital():
    ms = [box(10, 0.05, 8, (210, 205, 190), 'planks_grey', ts=1.0).xf(trans(0, -0.05, 0)),
          box(10, 3.2, 0.1, (230, 228, 215), 'plaster', ts=1.5, faces='f').xf(trans(0, 0, -2.0)),
          box(0.1, 3.2, 8, (230, 228, 215), 'plaster', ts=1.5, faces='r').xf(trans(-3.0, 0, 0))]
    for x in (-1.5, 1.6):
        ms.append(box(1.2, 1.6, 0.06, (255, 255, 255), 'window').xf(trans(x, 1.2, -1.94)))
    ms.append(bed().xf(trans(0, 0, 0)))
    ms.append(bed().xf(trans(-2.2, 0, 0)))
    ms.append(box(0.5, 0.6, 0.4, (180, 170, 150), 'planks').xf(trans(0.9, 0, -0.8)))
    ms.append(cyl(0.05, 0.05, 0.2, 6, (230, 230, 240), alpha=0.7).xf(trans(0.9, 0.6, -0.8)))
    return merge(ms)


HOSP = hospital()


def shot_hospital(lt, dur, tg):
    cam = cam_lerp(Cam((1.9, 1.7, 1.2), (0, 0.6, -0.1), 55), Cam((1.7, 1.6, 1.0), (0, 0.6, -0.1), 55), lt / dur)
    ms = [HOSP]
    # James couché (jambes amputées sous les genoux) : couverture épaisse jusqu'aux genoux, plate ensuite
    jm = JAMES_PEG.mesh((0, 0, 0), 0.0, dict(face='james_closed' if (lt % 3) < 1.2 else 'james', la=(0.0, 0.1, 0.2), ra=(0.0, 0.1, 0.2), hat=False))
    ms.append(jm.xf(M(trans(0, 0.63, 1.05), rotx(-math.pi / 2))))
    ms.append(box(1.02, 0.27, 0.9, (255, 255, 255), 'blanket').xf(trans(0, 0.5, 0.09)))
    ms.append(box(1.02, 0.2, 0.52, (255, 255, 255), 'blanket').xf(trans(0, 0.5, 0.79)))
    ms.append(doctor().mesh((-0.9, 0, 0.3), 1.2, dict(la=(0.3, 0.1, 1.4), hy=0.2)))
    return merge(ms), cam, ENV_IN.copy(points=[((0, 2.8, 0), (255, 240, 210), 0.5, 6)]), {}


# ------------------------------------------------------------------ 3 : poste d'aiguilleur
def shot_station(lt, dur, tg):
    cam = cam_lerp(Cam((13.5, 2.2, -0.6), (7.0, 1.9, -3.6), 55), Cam((13.0, 2.2, -0.8), (8.0, 1.9, -3.6), 55), lt / dur)
    x = 7.0 + lt * 0.7
    ms = [STATION, james_crutch_mesh((x, 0.9, -3.0), math.pi / 2, lt * 4, 0.9)]
    ms.append(vendor('vendor2', (200, 190, 160)).mesh((2, 0.9, -4.3), 0.4, dict()))
    ms.append(lady().mesh((-4, 0.9, -3.8), 0.9, dict()))
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 4/5 : marché
def market():
    g = grid(-60, -60, 60, 60, 10, 10, None, (255, 255, 255), 'karoo', 3.0)
    ms = [g, box(8, 0.08, 120, (190, 160, 120), 'dirt', ts=2.0, faces='u').xf(trans(0, 0.0, 0))]
    rr = np.random.default_rng(12)
    cols = [(200, 60, 50), (60, 110, 160), (220, 170, 50), (90, 140, 70), (170, 80, 150)]
    fruit = [(230, 130, 40), (200, 40, 40), (240, 210, 60), (110, 160, 60), (120, 60, 120)]
    for i, z in enumerate((-16, -11.5, -7, -2.5, 2, 6.5, 11)):
        for side, x in ((-1, -5.2), (1, 5.2)):
            zz = z + (0 if side < 0 else 2.2)
            ms.append(market_stall(cols[(i + (side > 0) * 2) % 5], i * 3 + side + 2).xf(M(trans(x, 0, zz), roty(-side * math.pi / 2))))
            xf = x - side * 1.0
            ms.append(crate(fill=fruit[(i + side) % 5]).xf(M(trans(xf, 0, zz - 1.0), roty(0.2 * side))))
            ms.append(basket(0.28, 0.32, fruit[(i * 2 + 1) % 5]).xf(trans(xf + side * 0.1, 0, zz + 1.0)))
            if (i + side) % 2:
                ms.append(pot(0.22, (165 + 10 * side, 90, 55)).xf(trans(x + side * 0.9, 0, zz + 1.6)))
                ms.append(pot(0.16, (150, 80, 50)).xf(trans(x + side * 1.2, 0, zz + 1.25)))
            else:
                ms.append(sack_pile(4, i).xf(trans(x + side * 0.5, 0, zz + 1.7)))
    for i, z in enumerate((-24, -14, -4, 6, 16)):
        ms.append(cape_house().xf(M(trans(-11, 0, z), roty(math.pi / 2))))
        ms.append(cape_house((225, 215, 185)).xf(M(trans(11, 0, z + 3), roty(-math.pi / 2))))
        ms.append(bunting((-8.0, 3.3, z + 1.5), (8.0, 3.3, z + 4.0), 16))
    ms.append(well().xf(trans(-1.8, 0, -20)))
    for x, z in ((-8.5, -9), (8.5, 1), (-8.5, 12)):
        ms.append(deciduous(7, 2.5, seed=int(z + 30), col=(220, 235, 200)).xf(trans(x, 0, z)))
    ms.append(hills(-150, 9))
    ms.append(grass_tufts(-9, -40, -7, 40, 150, 11, col=(150, 140, 80)))
    for k in range(6):
        ms.append(box(1.2, 0.02, 0.8, [(170, 50, 40), (60, 90, 150), (200, 170, 60)][k % 3], 'cloth').xf(trans(-3.6 + (k % 2) * 7.2, 0.92, -14 + k * 4.5)))
    return merge(ms)


MARKET = market()


def market_crowd(t):
    rr = np.random.default_rng(3)
    ms = []
    people = [vendor('vendor'), vendor('vendor2', (230, 220, 200)), vendor('vendor', (90, 120, 170)), vendor('vendor2', (200, 120, 60)),
              farmer(), lady(), vendor('vendor', (150, 60, 50)), farmer()]
    # vendeurs derrière leurs stands
    for i, z in enumerate((-16, -7, 2, 11)):
        ms.append(people[i % 4].mesh((-6.2, 0, z), math.pi / 2, dict(ra=(0.8 + 0.4 * math.sin(t * 2 + i), 0.2, 1.0))))
        ms.append(people[(i + 1) % 4].mesh((6.2, 0, z + 2.2), -math.pi / 2, dict(hy=0.3 * math.sin(t + i))))
    # passants
    for i in range(7):
        z0 = rr.uniform(-18, 12)
        sp = rr.uniform(0.6, 1.1) * (1 if i % 2 else -1)
        z = (z0 + t * sp + 30) % 32 - 18
        x = rr.uniform(-3.2, 3.2)
        if abs(x) < 1.6:
            x = 2.6 * (1 if x > 0 else -1)
        ms.append(people[4 + i % 4].mesh((x, 0, z), 0.0 if sp > 0 else math.pi, walk_pose(t * 5 + i, 0.8)))
    for i in range(5):
        ph = t * 1.3 + i
        ms.append(chicken((230, 225, 210) if i % 2 else (170, 100, 50), ph).xf(M(trans(-3.0 + i * 1.4 + 0.3 * math.sin(ph), 0, -4 + (i % 3) * 3.5), roty(ph))))
    ms.append(donkey(t * 2).xf(M(trans(3.3, 0, -9), roty(0.2))))
    return merge(ms)


CROWD = market_crowd(0.0)


def ox_team(z, phase, wr):
    return merge([ox(phase).xf(trans(-0.7, 0, z + 3.2)), ox(phase + 1.5).xf(trans(0.7, 0, z + 3.2)), ox_cart(wr).xf(trans(0, 0, z))])


def jack_driver(z, lt):
    pose = bab_sit(la=(1.1, 0.4), ra=(1.1 + 0.15 * math.sin(lt * 4), 0.4), hy=0.2 * math.sin(lt))
    m = JACK.mesh((0.0, 1.38, z + 0.75), 0.0, pose)
    # rênes
    rr = []
    for k in ('hand_l', 'hand_r'):
        p = JACK.attach[k][:3, 3]
        side = -0.7 if k == 'hand_l' else 0.7
        rr.append(strip_box(p, (side, 1.55, z + 4.2), 0.025, (60, 40, 25)))
    return merge([m] + rr)


def shot_market(lt, dur, tg):
    z = -9 + lt * 1.6
    cam = cam_lerp(Cam((-3.3, 1.8, 9.8), (0.6, 1.1, -1.0), 60), Cam((-3.2, 1.8, 9.6), (0.6, 1.1, 0.5), 60), lt / dur)
    ms = [MARKET, market_crowd(tg), ox_team(z, lt * 3, -lt * 2.2), jack_driver(z, lt)]
    ms.append(JAMES_CR.mesh((-2.6, 0, 6.0), math.pi / 2 + 0.6, dict(face='james_open', hy=-0.3, la=(0.3, 0.25, 0.1), ra=(0.3, 0.25, 0.1))))
    at = JAMES_CR.attach
    for k in ('hand_l', 'hand_r'):
        p = at[k][:3, 3]
        ms.append(strip_box(p + np.array([0, 0.32, 0]), (p[0], 0.0, p[2]), 0.04, (130, 95, 60)))
    return merge(ms), cam, ENV_DAY, {}


def shot_buy(lt, dur, tg):
    tj = WT(5, 'Jack.') - S('buy')
    zc = 4.0
    if lt < tj:
        cam = Cam((-0.3, 1.6, zc + 3.8), (-1.9, 1.1, zc + 0.3), 55)
    else:
        cam = cam_lerp(Cam((-1.0, 0.95, zc + 1.25), (-2.0, 0.72, zc + 0.15), 45), Cam((-1.1, 0.92, zc + 1.1), (-2.0, 0.72, zc + 0.15), 45), (lt - tj) / max(0.2, dur - tj))
    ms = [MARKET, market_crowd(tg), ox_team(zc - 4.0, 0, 0)]
    ms.append(JAMES_CR.mesh((-2.6, 0, zc + 0.6), 1.9, dict(face='james_smile', ra=(1.2, 0.0, 0.3), la=(0.3, 0.25, 0.1))))
    at = JAMES_CR.attach
    p = at['hand_l'][:3, 3]
    ms.append(strip_box(p + np.array([0, 0.32, 0]), (p[0], 0.0, p[2]), 0.04, (130, 95, 60)))
    ms.append(coins(5).xf(M(at['hand_r'], trans(0, -0.05, 0.05))))
    ms.append(farmer('farmer').mesh((-1.2, 0, zc + 0.1), -1.2, dict(ra=(1.0, 0.0, 0.4))))
    ms.append(JACK.mesh((-2.0, 0, zc + 0.15), 0.4 if lt < tj else 0.6, bab_sit(hy=-0.6 if lt < tj else 0.2, hp=0.3 if lt < tj else 0.15)))
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 6 : corvées
HOUSE_IN = house_interior()
HOUSE_EXT = merge([grid(-40, -40, 40, 40, 8, 8, None, (255, 255, 255), 'karoo', 3.0), cape_house().xf(trans(0, 0, 0)),
                   cape_house((225, 215, 185)).xf(trans(-9, 0, -1)), box(4, 0.02, 60, (190, 160, 120), 'dirt').xf(trans(0, 0, 9)).xf(M(roty(math.pi / 2), trans(0, 0, 0))),
                   aloe(3).xf(trans(4.5, 0, 6)), bush(0.7, 2).xf(trans(-4, 0, 5)), hills(-150, 4),
                   grass_tufts(-20, 4.5, 20, 15, 400, 12, col=(150, 140, 80))])


def shot_sweep(lt, dur, tg):
    """Jack balaie : les deux mains sur le manche, la brosse frotte le sol"""
    cam = cam_lerp(Cam((1.8, 1.4, 2.4), (-0.3, 0.6, -0.4), 55), Cam((1.6, 1.35, 2.1), (-0.4, 0.6, -0.4), 55), lt / dur)
    sw = math.sin(lt * 7)
    x = -0.2 + 0.3 * math.sin(lt * 1.5)
    yaw = 0.7
    fwd = np.array([math.sin(yaw), 0, math.cos(yaw)])
    side = np.array([math.cos(yaw), 0, -math.sin(yaw)])
    body = np.array([x, 0, -0.2])
    brush = body + fwd * 0.75 + side * 0.3 * sw
    top = body + fwd * 0.05 + side * 0.15 * sw + np.array([0, 1.15, 0])
    d = (top - brush) / np.linalg.norm(top - brush)
    h1 = brush + d * 0.55
    h2 = brush + d * 0.9
    ms = [HOUSE_IN, rod(brush, top, 0.02, (150, 110, 60))]
    m_, L_ = frame_along(brush, top)
    ms.append(merge([cyl(0.12, 0.06, 0.28, 6, (200, 170, 90))]).xf(M(m_, rotx(math.pi), trans(0, -0.02, 0))))
    ms.append(JACK.mesh(tuple(body), yaw, bab_stand(pitch=1.0, ik_l=h2, ik_r=h1, hp=0.4)))
    for i in range(6):
        ph = (lt * 1.3 + i / 6) % 1
        p = brush + fwd * (0.2 + ph * 0.4) + np.array([0, 0.05 + ph * 0.3, math.sin(i) * 0.1])
        ms.append(billboard(p, 0.12, 0.12, cam, (210, 190, 150), 'smoke', emis=0.3, alpha=0.5 * (1 - ph)))
    return merge(ms), cam, ENV_IN.copy(points=[((0, 2.5, 0), (255, 235, 200), 0.4, 6)]), {}


def shot_bin(lt, dur, tg):
    """Jack porte la poubelle à deux mains jusqu'au bord du chemin"""
    u = ease(lt / dur)
    cam = Cam((3.6, 1.3, 9.2), (1.0, 0.7, 4.8), 55)
    yaw = 0.5
    pos = np.array([0.0 + u * 1.8, 0.15 if u < 0.25 else 0.0, 2.9 + u * 3.0])
    fwd = np.array([math.sin(yaw), 0, math.cos(yaw)])
    side = np.array([math.cos(yaw), 0, -math.sin(yaw)])
    bc = pos + fwd * 0.45 + np.array([0, 0.35 + 0.03 * math.sin(lt * 16), 0])
    ms = [HOUSE_EXT, dustbin().xf(M(trans(bc), roty(yaw))), dustbin().xf(trans(-1.6, 0, 6.2))]
    hl = bc + side * 0.27 + np.array([0, 0.5, 0])
    hr = bc - side * 0.27 + np.array([0, 0.5, 0])
    ms.append(JACK.mesh(tuple(pos), yaw, bab_stand(pitch=1.15, ik_l=hr, ik_r=hl, ll=(0.25 + 0.3 * math.sin(lt * 8), 0.45), rl=(0.25 - 0.3 * math.sin(lt * 8), 0.45))))
    return merge(ms), cam, ENV_GOLD.copy(light=(-0.6, 0.6, 0.6)), {}


ROAD_STATION = merge([STATION])


def shot_push(lt, dur, tg):
    """James assis sur le siège du chariot, Jack derrière qui le pousse par les deux brancards"""
    z = 14.0
    x = -12 + lt * 1.3
    yaw = math.pi / 2
    cam = Cam((x + 1.6, 1.4, z + 4.6), (x - 0.5, 0.75, z), 55)
    T_ = M(trans(x, 0, z), roty(yaw))
    ms = [STATION, trolley(wheel_rot=-lt * 6.5).xf(T_)]
    jm = JAMES_PEG.mesh(tuple((T_ @ np.array([0, 0.0, -0.05, 1]))[:3]), yaw,
                        sit_pose(ll=(1.45, 1.0), rl=(1.45, 1.0), la=(0.5, 0.2, 0.9), ra=(0.5, 0.2, 0.9), face='james_smile', drop=0.4))
    gl = (T_ @ np.array([-0.32, TROLLEY_GRIP[0], TROLLEY_GRIP[1], 1]))[:3]
    gr = (T_ @ np.array([0.32, TROLLEY_GRIP[0], TROLLEY_GRIP[1], 1]))[:3]
    bpos = (T_ @ np.array([0, 0, TROLLEY_GRIP[1] - 0.55, 1]))[:3]
    jk = JACK.mesh(tuple(bpos), yaw, dict(pitch=1.0, hip=0.52, ik_l=gr, ik_r=gl, la=(1.3, 0.2), ra=(1.3, 0.2), hp=-0.4,
                                         ll=(0.45 * math.sin(lt * 7) + 0.35, 0.4), rl=(-0.45 * math.sin(lt * 7) + 0.35, 0.4)))
    ms += [jm, jk]
    return merge(ms), cam, ENV_GOLD.copy(light=(-0.7, 0.55, 0.3), sky_hor=(240, 200, 150)), {}


# ------------------------------------------------------------------ 7/8 : la cabine
SB_IN = signal_box_int()


CAB_BASE = np.array([0.0, 2.5, 0.9])


def cabin_scene(lt, lever_i=None, pull=0.0, jack_mode='watch', james_mode='lever', cap=False, extra=()):
    """intérieur cabine (repère local, plancher y=2.5, leviers à z=0.9)"""
    pulls = [0] * 6
    i = lever_i if lever_i is not None else 2
    pulls[i] = pull
    ms = [SB_IN, lever_frame(pulls).xf(trans(CAB_BASE))]
    ms.append(box(4.2, 1.2, 0.04, (150, 190, 210), alpha=0.18).xf(trans(0, 3.3, 1.62)))
    for x in np.linspace(-2.1, 2.1, 6):
        ms.append(box(0.08, 1.2, 0.08, (235, 232, 222)).xf(trans(x, 3.3, 1.62)))
    ms.append(box(4.2, 0.8, 0.1, (220, 212, 190), 'planks_white').xf(trans(0, 2.5, 1.62)))
    if james_mode == 'lever':
        ms.append(james_at_lever(CAB_BASE, i, pull))
    elif james_mode == 'chair':
        ms.append(box(0.5, 0.45, 0.5, (110, 75, 45), 'planks').xf(trans(1.5, 2.5, -0.6)))
        ms.append(box(0.5, 0.6, 0.06, (110, 75, 45), 'planks').xf(trans(1.5, 2.95, -0.85)))
        cup = merge([cyl(0.04, 0.035, 0.08, 6, (240, 240, 235)), box(0.02, 0.04, 0.03, (240, 240, 235)).xf(trans(0.05, 0.03, 0))])
        ms.append(JAMES_PEG.mesh((1.5, 2.5, -0.55), -0.5, sit_pose(ra=(1.4, 0.1, 1.5 + 0.2 * math.sin(lt)), la=(0.5, 0.1, 0.4),
                                                                  face='james_smile', hand_r=cup, drop=0.48)))
    elif james_mode == 'side':
        ms.append(JAMES_PEG.mesh((-1.6, 2.5, -0.4), 0.7, dict(face='james_smile')))
    if jack_mode == 'watch':
        ms.append(box(0.45, 0.6, 0.45, (110, 75, 45), 'planks').xf(trans(0.8, 2.5, -1.0)))
        ms.append(JACK.mesh((0.8, 3.1, -1.05), -0.3, bab_sit(hy=0.6 * math.sin(lt * 1.3) + 0.3, hp=0.1)))
    elif jack_mode == 'lever':
        ms.append(jack_at_lever(CAB_BASE, i, pull, cap=cap))
    ms += list(extra)
    return merge(ms)


ENV_CAB = ENV_IN.copy(points=[((0, 4.3, 0.5), (255, 235, 200), 0.5, 5), ((0, 3.3, 3.0), (255, 245, 220), 0.7, 5)])


def shot_observe(lt, dur, tg):
    cam = cam_lerp(Cam((-1.95, 4.35, 1.5), (0.45, 3.2, -0.6), 66), Cam((-1.9, 4.33, 1.45), (0.5, 3.2, -0.6), 66), lt / dur)
    return cabin_scene(lt, 2, 0.0), cam, ENV_CAB, {}


def shot_whistle(lt, dur, tg):
    x = 30 + lt * 2.0
    wx = x - 4.3 - 1.7
    cam = Cam((wx + 1.2, 3.3, 3.2), (wx, 2.85, 0), 45)
    ms = [STATION, train_at(x)]
    for k, t0 in enumerate((0.15, 0.95)):
        if lt > t0:
            ms.append(puff_tex_sprites((wx, 3.1, 0), lt - t0, cam, 5, 0.35, 1.6, 20 + k, drift=(-0.6, 0, 0)))
    return merge(ms), cam, ENV_DAY, {}


def shot_pull(lt, dur, tg):
    pull = ease(min(1, lt / 0.8))
    cam = Cam((1.2, 4.35, 1.5), (-0.25, 3.1, 0.2), 58)
    return cabin_scene(lt, 2, pull), cam, ENV_CAB, {}


def shot_points(lt, dur, tg):
    pull = ease(min(1, lt / 0.6))
    cam = Cam((22.0, 1.8, 4.5), (19.0, 0.2, 0.5), 55)
    return merge([STATION, points_blades(pull)]), cam, ENV_DAY, {}


def shot_jack_alone(lt, dur, tg):
    pull = 0.5 - 0.5 * math.cos(min(1, lt / 1.6) * math.pi)
    cam = cam_lerp(Cam((1.9, 4.35, 1.5), (-0.6, 3.0, -0.2), 64), Cam((1.8, 4.33, 1.4), (-0.5, 3.0, -0.2), 64), lt / dur)
    return cabin_scene(lt, 3, pull, 'lever', 'chair'), cam, ENV_CAB, {}


# ------------------------------------------------------------------ 9 : la passagère
def carriage_interior_view(lt, dur, tg):
    """vue de l'extérieur : la passagère, assise derrière la vitre, découvre le singe aux commandes"""
    xh = 21.0 + 17.4 + 2.5 * (lt - dur)
    cx = xh - 17.4
    cam = Cam((cx + 0.05, 2.4, -3.1), (cx + 0.05, 2.2, -0.6), 54)
    ms = [STATION, train_at(xh, ('loco', 'tender', 'car', 'car', 'car')).xf(trans(0, 0, 0)) if False else
          train(['loco', 'tender', 'car', 'car', 'car'], x=xh, wheel_rot=-xh / 0.75, glass_car=2), jack_in_box(lt, 2, 0.5 + 0.5 * math.sin(lt * 2))]
    shock = lt > dur * 0.5
    pose = sit_pose(drop=0.45, la=(0.6, 0.1, 0.5), ra=(0.6, 0.1, 0.5), hy=0.0, face='lady')
    if shock:
        pose.update(face='lady_shock', ra=(1.5, 0.15, 0.3), lean=0.25, hy=0.25)
    ms.append(lady().mesh((cx + 0.1, 1.17, -0.62), math.pi, pose))
    return merge(ms), cam, ENV_DAY.copy(points=[((cx + 0.1, 2.6, -0.3), (255, 240, 210), 1.0, 2.5)]), {}


def shot_lady_pov(lt, dur, tg):
    cam = Cam((29.5 - lt * 0.8, 3.7, 0.8), (25.8, 3.4, -4.0), 40)
    return merge([STATION, jack_in_box(lt, 2, 0.5 + 0.5 * math.sin(lt * 2.5))]), cam, ENV_DAYC, {}


def office():
    ms = [box(8, 0.05, 6, (150, 110, 70), 'planks', ts=0.8).xf(trans(0, -0.05, 0)),
          box(8, 3.2, 0.1, (200, 190, 160), 'planks_v', ts=1.0, faces='f').xf(trans(0, 0, -2.0)),
          box(3.0, 1.1, 0.6, (120, 85, 55), 'planks', ts=0.6).xf(trans(0, 0, -0.6)),
          box(3.1, 0.06, 0.7, (100, 70, 45)).xf(trans(0, 1.1, -0.6))]
    ms.append(box(1.6, 1.0, 0.04, (240, 235, 220), 'diagram').xf(trans(-1.6, 1.8, -1.94)))
    ms.append(cyl(0.25, 0.25, 0.06, 12, (240, 235, 220)).xf(M(trans(1.8, 2.3, -1.94), rotx(math.pi / 2))))
    for i in range(5):
        ms.append(box(0.3, 0.04, 0.22, (240, 235, 215)).xf(trans(0.8, 1.13 + i * 0.04, -0.6)))
    return merge(ms)


OFFICE = office()


def shot_complaint(lt, dur, tg):
    cam = cam_lerp(Cam((2.2, 1.7, 2.6), (0.0, 1.3, -0.4), 50), Cam((2.0, 1.7, 2.3), (0.0, 1.3, -0.4), 50), lt / dur)
    wag = math.sin(lt * 9)
    ms = [OFFICE, make_clerk().mesh((0.1, 0, -1.3), 0.0, dict(face='clerk', hp=0.05)),
          lady('lady_shock').mesh((0.0, 0, 0.3), math.pi, dict(ra=(1.6, 0.0, 0.6 + 0.3 * wag), la=(0.9, 0.0, 1.0)))]
    letter = box(0.2, 0.28, 0.01, (245, 240, 225)).xf(M(rotx(-0.3)))
    ms.append(letter.xf(M(trans(0.25, 1.14, -0.4), rotx(-math.pi / 2))))
    return merge(ms), cam, ENV_IN.copy(points=[((0, 2.8, 0), (255, 240, 210), 0.5, 6)]), {}


def make_clerk():
    return Human('clerk', skin=(230, 192, 160), shirt=(235, 232, 225), pants=(40, 40, 45), hair=(60, 45, 30), tie=(30, 30, 60),
                 jacket=None, hat=None)


# ------------------------------------------------------------------ 10 : inspecteur
INSP = inspector()


def shot_inspector(lt, dur, tg):
    tw = WT(10, 'réussit') - S('inspector') - 0.6
    pull = ease(min(1, max(0, (lt - tw) / 0.7)))
    cam = cam_lerp(Cam((1.9, 4.35, 1.5), (-0.4, 3.0, -0.6), 72), Cam((1.85, 4.33, 1.45), (-0.4, 3.0, -0.6), 72), lt / dur)
    nb = box(0.15, 0.2, 0.02, (60, 40, 30)).xf(M(rotx(-1.2)))
    pen = cyl(0.008, 0.008, 0.14, 4, (30, 30, 30)).xf(M(rotx(-0.5)))
    face = 'insp' if lt < tw + 0.8 else 'insp_smile'
    ims = INSP.mesh((-0.35, 2.5, -0.95), 0.55, dict(face=face, la=(1.1, 0.0, 1.2), ra=(1.0, -0.2, 1.4 + 0.2 * math.sin(lt * 8) * (lt > tw + 0.8)),
                                                    hand_l=nb, hand_r=pen, hp=0.25, hy=0.3))
    return cabin_scene(lt, 4, pull, 'lever', 'side', extra=[ims]), cam, ENV_CAB, {}


# ------------------------------------------------------------------ 11 : la paye
def shot_pay(lt, dur, tg):
    """l'inspecteur, de l'autre côté de la table, pose les pièces une à une ; puis Jack attrape sa bière"""
    tb = WT(11, 'demi-bouteille') - S('pay') - 0.2
    ms = [SB_IN, lever_frame().xf(trans(CAB_BASE))]
    n = 20 if lt >= tb else min(20, int(lt / max(0.3, tb) * 24))
    stack = lambda i: np.array([-1.6 + (i // 10) * 0.07, 3.356 + (i % 10) * 0.007, -1.05])
    for i in range(n):
        ms.append(cyl(0.025, 0.025, 0.006, 8, (205, 205, 210), 'metal').xf(trans(stack(i))))
    jp = np.array([-0.62, 2.5, -1.2])
    insp_pos = (-1.45, 2.5, -0.35)
    if lt < tb:
        u = lt / max(0.3, tb)
        cam = cam_lerp(Cam((0.6, 4.15, 0.5), (-1.2, 3.25, -0.9), 58), Cam((0.5, 4.1, 0.35), (-1.2, 3.25, -0.9), 58), u)
        ms.append(JACK.mesh(tuple(jp), -math.pi / 2, bab_stand(cap=True, hp=0.35, la=(0.5, 0.4), ra=(0.5, 0.4))))
        ms.append(beer_bottle(0.5).xf(trans(-1.2, 3.355, -1.32)))
        # la main va du gousset à la pile, pose la pièce, revient
        ph = (lt * 24 / max(0.3, tb)) % 1.0
        top = stack(min(n, 19)) + np.array([0, 0.06, 0.02])
        src = np.array([-1.25, 3.5, -0.55])
        k = math.sin(ph * math.pi)
        hand = src * (1 - k) + top * k
        coin = cyl(0.025, 0.025, 0.006, 8, (205, 205, 210), 'metal').xf(trans(0, -0.03, 0.03)) if n < 20 and ph < 0.5 else None
        ms.append(INSP.mesh(insp_pos, math.pi, dict(ik_r=hand, la=(0.2, 0.1, 0.3), hp=0.45, hand_r=coin, face='insp_smile' if n >= 20 else 'insp')))
    else:
        d = lt - tb
        cam = cam_lerp(Cam((0.5, 4.1, 0.5), (-0.9, 3.45, -1.15), 50), Cam((0.4, 4.05, 0.35), (-0.9, 3.5, -1.15), 50), d / max(0.2, dur - tb))
        ms.append(INSP.mesh(insp_pos, math.pi * 0.8, dict(face='insp_smile', la=(0.2, 0.1, 0.3), ra=(0.2, 0.1, 0.3))))
        b0 = np.array([-1.2, 3.355, -1.32])
        mouth = jp + np.array([-0.45, 1.12, 0.0])
        if d < 0.5:
            bp, tilt = b0, 0.0
        elif d < 1.2:
            u = ease((d - 0.5) / 0.7)
            mid = np.array([b0[0] + 0.1, 3.75, (b0[2] + mouth[2]) / 2])
            bp = (1 - u) ** 2 * b0 + 2 * (1 - u) * u * mid + u * u * (mouth + np.array([-0.05, -0.12, 0]))
            tilt = 0.0
        else:
            bp, tilt = mouth + np.array([-0.05, -0.12, 0]), min(1.6, (d - 1.2) * 2.0)
        Mb = M(trans(bp), rotz(-tilt))
        ms.append(beer_bottle(0.5).xf(Mb))
        grip = (Mb @ np.array([0, 0.1, 0, 1]))[:3]
        reach = grip if d >= 0.25 else (jp + np.array([-0.3, 1.0, 0.1])) * (1 - d / 0.25) + grip * (d / 0.25)
        ms.append(JACK.mesh(tuple(jp), -math.pi / 2, bab_stand(cap=True, hp=0.25 - 0.4 * min(1, max(0, d - 1.2)), ik_r=reach,
                                                               la=(0.5, 0.4), mouth=0.6 if d > 1.1 else 0.2)))
    return merge(ms), cam, ENV_CAB, {}


def shot_years(lt, dur, tg):
    u = lt / dur
    k = (lt * 0.7) % 1.0
    env = ENV_DAY.copy()
    phase = (lt / dur) * 3
    m = (math.sin(phase * math.pi * 2) + 1) / 2
    env = ENV_DAY.copy(sky_hor=tuple(np.array(ENV_DAY.sky_hor) * 255 * m + np.array(ENV_GOLD.sky_hor) * 255 * (1 - m)),
                       light=(-0.8 + 1.6 * ((phase) % 1), 0.5, 0.3))
    cam = cam_lerp(Cam((30.5, 3.2, 4.5), (26, 3.3, -3.6), 52), Cam((29.5, 3.3, 4.0), (26, 3.3, -3.6), 52), u)
    ms = [STATION, jack_in_box(lt, int(lt * 2) % 6, abs(math.sin(lt * 4)), cap=True)]
    # trains qui défilent à toute vitesse
    xt = -30 + (lt * 40) % 110
    parts = [('loco', 'tender', 'car', 'car'), ('loco', 'tender', 'van', 'van', 'open')][int(lt * 40 / 110) % 2]
    zt = 0.0
    if xt < 160:
        ms.append(train_at(xt, parts, z=zt))
    return merge(ms), cam, env.copy(points=ENV_DAYC.points), {}


# ------------------------------------------------------------------ 13 : fin
def shot_end(lt, dur, tg):
    cam = cam_lerp(Cam((26.0, 3.62, -2.6), (26.0, 3.55, -4.0), 50), Cam((26.0, 3.63, -2.75), (26.0, 3.58, -4.0), 50), lt / dur)
    ms = [STATION, lever_frame().xf(trans(BOX_BASE)), box(4.2, 0.04, 3.2, (140, 105, 70), 'planks').xf(trans(26, 2.5, -4.2)),
          box(4.2, 2.0, 0.1, (220, 212, 190), 'planks_white', faces='f').xf(trans(26, 2.5, -5.7)),
          clock_mesh(10, 10, 0.24).xf(trans(24.6, 3.95, -5.62)),
          JACK.mesh((26.0, 2.5, -4.0), 0.0, bab_stand(cap=True, hp=0.05, mouth=0.6 if lt > dur * 0.5 else 0.0, la=(0.4, 0.4), ra=(0.9, 1.0)))]
    return merge(ms), cam, ENV_DAYC, dict(fade=max(0, (lt - dur + 0.4) / 0.4))


# ------------------------------------------------------------------ montage
add('hook2', 0.0, shot_hook2)
add('hook', WT(0, 'pendant') - 0.1, shot_hook)
add('jumper', T(1), shot_jumper)
add('jump', WT(1, 'On') - 0.1, shot_jump)
add('fall', T(2), shot_fall)
add('hospital', WT(2, 'et') - 0.1, shot_hospital)
add('station', T(3), shot_station)
add('market', T(4), shot_market)
add('buy', T(5), shot_buy)
add('sweep', T(6), shot_sweep)
add('bin', WT(6, 'sort') - 0.1, shot_bin)
add('push', WT(6, 'pousse') - 0.25, shot_push)
add('observe', T(7), shot_observe)
add('whistle', WT(7, 'Chaque') - 0.1, shot_whistle)
add('pull', WT(7, 'correspond') - 0.1, shot_pull)
add('points', WT(7, 'aiguillage.') - 0.05, shot_points)
add('jack_alone', T(8), shot_jack_alone)
add('lady', T(9), carriage_interior_view)
add('lady_pov', WT(9, 'singe') - 0.15, shot_lady_pov)
add('complaint', WT(9, 'Elle') - 0.1, shot_complaint)
add('inspector', T(10), shot_inspector)
add('pay', T(11), shot_pay)
add('years', T(12), shot_years)
add('end', T(13), shot_end)

subs = Subs(timing)


def build_audio(path):
    mx = A.Mixer(tl.duration())
    dur = tl.duration()
    mx.add(A.wind(10), 0, 0.12, length=dur)
    mx.add(A.chuff(8, 3.5), S('hook'), 0.5, 0.2, 0.4, length=S('jumper') - S('hook'))
    mx.add(A.wheel_rattle(6), S('hook'), 0.35, 0.2, 0.4, length=S('jumper') - S('hook'))
    mx.add(A.steam_whistle(1.0, 560), S('hook') + 0.3, 0.4)
    mx.add(A.ratchet(), 0.4, 0.5)
    mx.add(A.monkey(), 1.2, 0.4)
    mx.add(A.chuff(10, 2.2), S('jumper'), 0.45, 0.3, 0.2, length=S('hospital') - S('jumper'))
    mx.add(A.wheel_rattle(10), S('jumper'), 0.4, 0.3, 0.2, length=S('hospital') - S('jumper'))
    tj = WT(1, 'saute')
    mx.add(A.whoosh(0.6), tj, 0.4)
    mx.add(A.thwack(), tj + 0.7, 0.4)
    mx.add(A.whoosh(0.9), WT(2, 'chute…'), 0.6)
    mx.add(A.steam_whistle(1.2, 620), WT(2, 'chute…') + 0.1, 0.3)
    mx.add(A.tick(), S('hospital') + 0.3, 0.2)
    mx.add(A.birds(5), S('station'), 0.35, 0.2, 0.3, length=S('market') - S('station'))
    mx.add(A.crowd(8), S('market'), 0.45, 0.3, 0.3, length=S('sweep') - S('market'))
    mx.add(A.wheel_rattle(6), S('market'), 0.3, 0.2, 0.3, length=S('buy') - S('market'))
    mx.add(A.monkey(), S('market') + 1.5, 0.35)
    mx.add(A.clank(0.4), S('buy') + 0.3, 0.25)
    mx.add(A.monkey(), WT(5, 'Jack.'), 0.45)
    mx.add(A.sweep_broom(2.5), S('sweep'), 0.45, length=S('bin') - S('sweep'))
    mx.add(A.clank(0.3), S('bin') + 0.4, 0.3)
    mx.add(A.footsteps(2, 4), S('bin'), 0.3, length=S('push') - S('bin'))
    mx.add(A.wheel_rattle(4), S('push'), 0.35, 0.1, 0.3, length=S('observe') - S('push'))
    mx.add(A.tick(), S('observe') + 0.5, 0.25)
    mx.add(A.tick(), S('observe') + 1.5, 0.25)
    mx.add(A.steam_whistle(0.6, 560), S('whistle') + 0.15, 0.55)
    mx.add(A.steam_whistle(0.6, 560), S('whistle') + 0.95, 0.55)
    mx.add(A.chuff(4, 2), S('whistle'), 0.3, length=S('pull') - S('whistle'))
    mx.add(A.ratchet(), S('pull') + 0.1, 0.55)
    mx.add(A.clank(), S('points') + 0.4, 0.55)
    mx.add(A.ratchet(), S('jack_alone') + 0.3, 0.55)
    mx.add(A.chuff(6, 3), S('lady'), 0.35, 0.2, 0.3, length=S('complaint') - S('lady'))
    mx.add(A.wheel_rattle(6), S('lady'), 0.35, 0.2, 0.3, length=S('complaint') - S('lady'))
    mx.add(A.thwack(), S('complaint') + 0.6, 0.3)
    mx.add(A.thwack(), S('complaint') + 1.1, 0.3)
    tw = WT(10, 'réussit') - 0.6
    mx.add(A.steam_whistle(0.6, 560), tw - 0.9, 0.4)
    mx.add(A.ratchet(), tw, 0.55)
    mx.add(A.sting(), tw + 0.8, 0.4)
    for i in range(6):
        mx.add(A.clank(0.12), S('pay') + 0.2 + i * 0.3, 0.2)
    mx.add(A.monkey(), WT(11, 'demi-bouteille') + 0.8, 0.45)
    mx.add(A.chuff(6, 6), S('years'), 0.3, 0.2, 0.3, length=S('end') - S('years'))
    for i in range(4):
        mx.add(A.steam_whistle(0.4, 600), S('years') + 0.4 + i * 1.4, 0.25)
    mx.add(A.monkey(), S('end') + 1.0, 0.45)
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
        contact_sheet(tl, times[:36], os.path.join(HERE, 'sheet1.png'), subs, cols=6, scale=0.18)
        contact_sheet(tl, times[36:], os.path.join(HERE, 'sheet2.png'), subs, cols=6, scale=0.18)
    elif len(sys.argv) > 1 and sys.argv[1] == '--at':
        for s in sys.argv[2:]:
            frame(tl, float(s), subs).resize((540, 960)).save(os.path.join(HERE, f'at_{s}.png'))
    else:
        build_audio(os.path.join(HERE, 'sfx.wav'))
        mix_voice(os.path.join(HERE, 'voix.wav'), os.path.join(HERE, 'sfx.wav'), os.path.join(HERE, 'mix.wav'))
        render_video(tl, os.path.join(HERE, 'jack.mp4'), os.path.join(HERE, 'mix.wav'), subs)
