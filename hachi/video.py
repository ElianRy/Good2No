"""Vidéo : Hachikō, le chien qui a attendu presque dix ans."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n', '/home/claude/g2n/hachi']
import numpy as np
from world import *
from video_core import *
from scripts import HACHI as LINES
import audio as A
import common2 as C2

HERE = '/home/claude/g2n/hachi'
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
STATION = station()
PLAZA = plaza()
PLAZA_SNOW = plaza(snow=True)
SKY = city_skyline()
HOUSE = jp_house(10, 8, 3.2)
GARDEN = merge([grid(-30, -30, 30, 30, 6, 6, None, (255, 255, 255), 'grass', 3.0), sakura(5, 3, bloom=False).xf(trans(5, 0, 8)),
                rock(0.8, 2).xf(trans(-4, 0, 7)), rock(0.5, 3).xf(trans(-3, 0, 8))])
OFFICE = office()
ALLEY = alley()
CAMPUS = campus()
YATAI = yatai()
TREE_SPRING = sakura(5.5, 1, bloom=True).xf(trans(7.5, 0, 6.5))
TREE_SUMMER = sakura(5.5, 1, bloom=False).xf(trans(7.5, 0, 6.5))
TREE_AUTUMN = sakura(5.5, 1, bloom=False, autumn=True).xf(trans(7.5, 0, 6.5))
TREE_SNOW = sakura(5.5, 1, bloom=False, snow=True).xf(trans(7.5, 0, 6.5))

UENO = ueno()
UENO_S = ueno('ueno_smile')
UENO_NH = ueno('ueno', hat=False)
UENO_NH_S = ueno('ueno_smile', hat=False)
UENO_C = ueno('ueno_closed', hat=False)
CROWD = [salaryman(i) for i in range(3)] + [kimono_woman(i) for i in range(3)]
WORKER = worker_jp()
VENDOR = vendor_jp()
GIRL = girl()

DOG_YAW = math.atan2(-SPOT[0], -SPOT[2])   # regarde la sortie de la gare
EXIT = np.array([0.0, 0.0, 0.6])
TAG_Y = 0.0
_STATUE = statue_dog(True)
STATUE_POS = np.array([-3.2, 0.0, 4.5])


def town(snow=False, tree=None):
    ms = [STATION, PLAZA_SNOW if snow else PLAZA, SKY]
    if tree is not None:
        ms.append(tree)
    return ms


LAST_CAM = None


def crowd_flow(tg, n=10, speed=1.3, seed=0, density=1.0, out=True, cam=None):
    """voyageurs qui sortent de la gare (ou y entrent) en s'éventaillant"""
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        ph = (tg * speed / 12 + rr.random()) % 1.0
        if rr.random() > density:
            continue
        ang = rr.uniform(-0.9, 0.9)
        d = ph * 12 if out else (1 - ph) * 12
        p = EXIT + np.array([math.sin(ang) * d, 0, 0.3 + math.cos(ang) * d])
        if p[0] > SPOT[0] - 3.5 and p[2] > SPOT[2] - 1.0 and p[0] < SPOT[0] + 1.0:   # jamais entre la caméra et Hachi
            continue
        if cam is not None and np.hypot(p[0] - cam[0], p[2] - cam[2]) < 3.5:
            continue
        if cam is None and LAST_CAM is not None and np.hypot(p[0] - LAST_CAM[0], p[2] - LAST_CAM[2]) < 3.0:
            continue
        yaw = ang if out else ang + math.pi
        ms.append(CROWD[i % len(CROWD)].mesh(tuple(p), yaw, walk_pose(tg * 6 + i, 0.8)))
    return merge(ms)


def dog_wait(dog=HACHI, tg=0.0, look=0.0, pos=SPOT, extra=None):
    pose = dict(sit=1.0, hy=look, tail=math.sin(tg * 2) * 0.2)
    if extra:
        pose.update(extra)
    return dog.mesh(tuple(pos), DOG_YAW, pose)


def wait_cam(lt, dur, d=4.0, h=1.0, side=1.0):
    """caméra face à Hachi, le chien bien au centre"""
    fwd = np.array([math.sin(DOG_YAW), 0, math.cos(DOG_YAW)])
    tgt = SPOT + fwd * 0.2 + np.array([0.0, 0.5, 0.0])
    off = {1.0: np.array([-0.95, 0, 0.0]), -1.0: np.array([-0.35, 0, -0.9]), 0.0: np.array([-0.85, 0, -0.45])}[float(side)]
    off = off / np.linalg.norm(off) * d * 0.75
    p0 = tgt + off + np.array([0, h * 0.6, 0])
    p1 = tgt + off * 0.85 + np.array([0, h * 0.55, 0])
    p0[2], p1[2] = max(p0[2], 1.3), max(p1[2], 1.3)
    c0 = Cam(tuple(p0), tuple(tgt), 45)
    c1 = Cam(tuple(p1), tuple(tgt), 43)
    global LAST_CAM
    LAST_CAM = p0
    return cam_lerp(c0, c1, lt / max(dur, 0.1))


# ------------------------------------------------------------------ 0 : accroche (accéléré)
HOOK_PHASES = [('day', None), ('eve', None), ('night', None), ('snow', TREE_SNOW), ('spring', TREE_SPRING), ('day', TREE_SUMMER),
               ('autumn', TREE_AUTUMN), ('night', None), ('snow', TREE_SNOW), ('eve', None)]


def phase_env(kind):
    return {'day': ENV_DAY, 'eve': ENV_EVE, 'night': ENV_NIGHT, 'snow': ENV_SNOW, 'spring': ENV_DAY, 'autumn': ENV_EVE}[kind]


def shot_hook(lt, dur, tg):
    global LAST_CAM
    LAST_CAM = np.array([5.0, 1.0, 7.5])
    """accéléré : les saisons et les foules défilent, Hachi ne bouge pas"""
    k = int(lt / 0.32) % len(HOOK_PHASES)
    kind, tree = HOOK_PHASES[k]
    ms = town(kind == 'snow', tree)
    ms.append(dog_wait(HACHI, tg))
    ms.append(crowd_flow(tg * 6, 14, 1.6, k))
    cam = cam_lerp(Cam((5.6, 1.1, 8.2), tuple(SPOT + np.array([-0.8, 0.8, -1.0])), 50), Cam((4.2, 0.9, 6.5), tuple(SPOT + np.array([-0.7, 0.6, -0.8])), 46), lt / dur)
    if kind == 'snow':
        ms.append(C2.particles(SPOT + np.array([0, 2, 0]), tg, cam, 60, (6, 5, 6), 1.2, 0.07, (255, 255, 255), 1))
    if kind == 'spring':
        ms.append(C2.particles(SPOT + np.array([0, 2, 0]), tg, cam, 50, (6, 5, 6), 0.8, 0.07, (250, 190, 210), 2, spin=True))
    if kind == 'autumn':
        ms.append(C2.particles(SPOT + np.array([0, 2, 0]), tg, cam, 40, (6, 5, 6), 1.0, 0.1, (210, 120, 50), 3, spin=True))
    return merge(ms), cam, phase_env(kind), dict(flash=0.25 * max(0, 1 - (lt % 0.32) / 0.08))


# ------------------------------------------------------------------ 1 : 1924, le chiot
def tokyo_city():
    """Tokyo des années 20 : maisons à toits de tuiles serrées, quelques immeubles en brique, poteaux, collines, mont Fuji au loin"""
    rr = np.random.default_rng(11)
    ms = []
    for i in range(140):
        x, z = rr.uniform(-260, 260), rr.uniform(-320, 160)
        if -40 < x < 40 and -30 < z < 40:
            continue
        if rr.random() < 0.12:
            h = rr.uniform(10, 22)
            w = rr.uniform(10, 18)
            b = box(w, h, rr.uniform(10, 14), (170, 120, 90) if rr.random() < 0.6 else (215, 210, 195), 'brick' if rr.random() < 0.6 else 'plaster', ts=2.5)
            for y in np.arange(2, h - 1, 3.2):
                b = merge([b, box(w * 0.9, 1.2, 0.08, (60, 70, 85)).xf(trans(0, y, rr.uniform(5, 7)))])
            ms.append(b.xf(M(trans(x, 0, z), roty(rr.choice([0, math.pi / 2])))))
        else:
            ms.append(jp_house(rr.uniform(6, 10), rr.uniform(6, 9), rr.uniform(2.6, 4.0), i).xf(M(trans(x, 0, z), roty(rr.choice([0, math.pi / 2, math.pi])))))
    for i in range(30):
        x, z = rr.uniform(-200, 200), rr.uniform(-250, 120)
        if -40 < x < 40 and -30 < z < 40:
            continue
        ms.append(deciduous(rr.uniform(6, 9), rr.uniform(2.5, 3.5), i).xf(trans(x, 0, z)))
    for x in np.arange(-120, 120, 18):
        ms.append(cyl(0.12, 0.1, 8, 5, (90, 70, 50)).xf(trans(x, 0, 30)))
    ms.append(grid(-400, -400, 400, 400, 8, 8, None, (255, 255, 255), 'cobble', 5.0).xf(trans(0, -0.02, 0)))
    ms.append(cyl(420, 0, 260, 10, (110, 120, 145)).xf(trans(-300, -10, -1600)))
    ms.append(cyl(150, 0, 92, 10, (240, 244, 250)).xf(trans(-300, 158, -1600)))
    return merge(ms)


TOKYO = tokyo_city()


def shot_tokyo(lt, dur, tg):
    global LAST_CAM
    LAST_CAM = None
    u = lt / max(dur, 0.1)
    cam = Cam((60 - u * 15, 34 - u * 6, 80 - u * 12), (0, 4, -12), 52)
    ms = town(tree=TREE_SUMMER) + [TOKYO, railcar(wheel_rot=tg * 4).xf(trans(-30 + lt * 9, 1.0, -14)), crowd_flow(tg, 10)]
    return merge(ms), cam, ENV_DAY.copy(fog_near=120, fog_far=2200, sky_hor=(200, 215, 230)), {}


def shot_puppy(lt, dur, tg):
    """devant la maison, Ueno ouvre la caisse : le chiot sort la tête"""
    op = min(1.0, lt / 0.6)
    pop = min(1.0, max(0.0, (lt - 0.4) / 0.4))
    ms = [HOUSE, GARDEN, crate(op).xf(trans(0, 0.0, 7.2))]
    ms.append(PUPPY.mesh((0, 0.05, 7.2), 0.3, dict(sit=1.0, tail=math.sin(tg * 14) * 0.6, mouth=1.0 * pop, hy=0.3 * math.sin(tg * 3))))
    ms.append(UENO_NH_S.mesh((0.2, 0, 8.2), math.pi, dict(ll=(0.0, 1.57), rl=(0.2, 1.4), drop=0.45, lean=0.4, hp=0.4,
                                                       la=(1.2, 0.3, 0.4), ra=(1.2, 0.3, 0.4))))
    cam = cam_lerp(Cam((1.3, 1.5, 5.2), (0.0, 0.45, 7.3), 45), Cam((1.1, 1.4, 5.6), (0.0, 0.45, 7.3), 42), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_pet(lt, dur, tg):
    """assis sur l'engawa, Ueno caresse le chiot : « Hachi »"""
    seat = np.array([0.5, 0.5, 4.7])
    pup = seat + np.array([0.55, 0.05, 0.1])
    ms = [HOUSE, GARDEN, UENO_NH_S.mesh(tuple(seat + np.array([0, -0.45, 0.25])), 0.2, sit_pose(drop=0.45, ik_r=pup + np.array([0, 0.33 + 0.03 * math.sin(tg * 4), 0.02]), la=(0.5, 0.1, 0.5))),
          PUPPY.mesh(tuple(pup), -0.5, dict(sit=1.0, tail=math.sin(tg * 12) * 0.6, hp=-0.3, mouth=0.6))]
    cam = cam_lerp(Cam((2.0, 1.2, 7.2), (0.6, 0.8, 4.9), 45), Cam((1.7, 1.15, 6.6), (0.6, 0.8, 4.9), 43), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 2 : la routine
def shot_morning(lt, dur, tg):
    global LAST_CAM
    LAST_CAM = None
    """le matin, Ueno et Hachi arrivent à la gare ; Ueno entre, Hachi s'assoit"""
    u = min(1.0, lt / (dur * 0.8))
    up = EXIT + np.array([0.6, 0, 9 - 9 * u])
    dp = up + np.array([1.0, 0, 0.4])
    if u >= 1:
        dp = SPOT
    walking = u < 1
    ms = town(tree=TREE_SPRING) + [UENO.mesh(tuple(up), math.pi, walk_pose(lt * 5.5, 0.8) if walking else dict()),
                                   HACHI.mesh(tuple(dp), math.pi if walking else DOG_YAW, dog_walk(lt * 7, 1.0, tail=math.sin(tg * 8) * 0.3) if walking else dict(sit=1.0))]
    ms.append(crowd_flow(tg, 6, 1.0, 3, out=False))
    cam = Cam((6.0, 1.6, 12.0), tuple(up + np.array([0, 1.0, 0])), 50)
    return merge(ms), cam, ENV_DAY, {}


def shot_evening(lt, dur, tg):
    global LAST_CAM
    LAST_CAM = None
    """le soir, Ueno sort de la gare ; Hachi bondit vers lui"""
    t_out = 0.35
    u = min(1.0, max(0.0, (lt - t_out) / 0.9))
    up = EXIT + np.array([0.3, 0, 0.2 + 2.0 * u])
    jump = max(0.0, min(1.0, (lt - t_out - 0.4) / 0.25)) * (1 - max(0.0, min(1.0, (lt - t_out - 1.3) / 0.3)))
    dpos = SPOT + (up - SPOT) * 0.55 * min(1.0, max(0.0, (lt - t_out - 0.3) / 0.6))
    dyaw = math.atan2(up[0] - dpos[0], up[2] - dpos[2])
    dog = HACHI.mesh(tuple(dpos), dyaw if lt > t_out + 0.2 else DOG_YAW,
                     dict(sit=1.0 * (1 - min(1.0, max(0.0, (lt - t_out) / 0.3))), jump=jump, mouth=1.0 if lt > t_out else 0.0, tail=math.sin(tg * 14) * 0.8))
    ms = town(tree=TREE_SUMMER) + [dog, crowd_flow(tg, 8, 1.3, 5)]
    if lt > t_out - 0.3:
        ms.append(UENO_S.mesh(tuple(up), math.atan2(dpos[0] - up[0], dpos[2] - up[2]) if lt > t_out + 0.6 else 0.0,
                              walk_pose(lt * 5, 0.6, la=(0.9, 0.3, 0.5), ra=(0.9, 0.3, 0.5)) if u < 1 else dict(la=(0.9, 0.3, 0.6), ra=(0.9, 0.3, 0.6), lean=0.3, hp=0.4)))
    cam = cam_lerp(Cam((4.2, 1.3, 7.5), (0.9, 0.9, 2.0), 50), Cam((3.8, 1.2, 6.8), (0.9, 0.9, 2.0), 48), lt / dur)
    return merge(ms), cam, ENV_EVE, {}


# ------------------------------------------------------------------ 3 : 21 mai 1925
def shot_office(lt, dur, tg):
    """Ueno travaille à son bureau… puis s'effondre doucement"""
    t_fall = (WT(3, 'Ueno') - S('office')) + 0.4
    k = ease(min(1.0, max(0.0, (lt - t_fall) / 0.6)))
    who = UENO_NH if k < 0.5 else UENO_C
    pen = (0.15 + 0.03 * math.sin(tg * 9) * (1 - k), 0.8, -1.05)
    pose = sit_pose(drop=0.45, lean=0.25 + 0.75 * k, hp=0.3 + 0.4 * k, ik_r=pen if k < 0.3 else None, la=(0.9, 0.2, 1.2), ra=(0.9 - 0.3 * k, 0.4, 0.4 + 1.0 * (1 - k)))
    if pose['ik_r'] is None:
        pose.pop('ik_r')
    ms = [OFFICE, who.mesh((0, 0, -0.4), math.pi, pose), hat_mesh('bowler', (45, 42, 40)).xf(trans(-2.3, 1.75, -1.8))]
    cam = cam_lerp(Cam((1.6, 1.4, -2.2), (0, 1.0, -0.8), 48), Cam((1.3, 1.3, -2.0), (0, 0.95, -0.8), 45), lt / dur)
    env = ENV_ROOM.copy(points=[((1.6, 1.8, -2.3), (255, 240, 210), 0.8, 5)])
    return merge(ms), cam, env, dict(fade=0.25 * k)


def calendar_page(day):
    name = f'cal_{day}'
    if name in TEXB:
        return name
    from PIL import ImageFont

    def f(d, n):
        d.rectangle([0, 0, n, n], fill=(245, 240, 228))
        d.rectangle([0, 0, n, 8], fill=(190, 35, 35))
        d.rectangle([3, 2, n - 4, 5], fill=(245, 240, 228))   # « MAI 1925 » stylisé
        fnt = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 17)
        d.text((n / 2, 20), str(day), font=fnt, fill=(25, 25, 25), anchor='mm')
    tex_draw(name, f, bg=(245, 240, 228))
    return name


DAYS = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
for _d in DAYS:
    calendar_page(_d)


def shot_empty(lt, dur, tg):
    """le calendrier du bureau s'effeuille : 21, 22, 23 mai… la chaise reste vide, le chapeau reste accroché"""
    i = min(len(DAYS) - 1, int(lt / max(0.25, dur / len(DAYS))))
    ph = (lt / max(0.25, dur / len(DAYS))) % 1.0
    cal_pos = np.array([-1.2, 1.6, -2.42])
    ms = [OFFICE, hat_mesh('bowler', (45, 42, 40)).xf(trans(-2.3, 1.75, -1.8))]
    ms.append(box(0.5, 0.6, 0.02, (255, 255, 255), calendar_page(DAYS[i])).xf(trans(cal_pos + np.array([0, -0.3, 0.0]))))
    if i + 1 < len(DAYS):
        ms.append(box(0.5, 0.6, 0.02, (245, 240, 228)).xf(
            M(trans(cal_pos + np.array([0, 0.3, 0.02])), rotx(-ph * 2.6), trans(0, -0.6, 0))) if ph > 0.55 else Mesh())
    for k in range(i):
        rr = np.random.default_rng(k)
        ms.append(box(0.5, 0.004, 0.6, (245, 240, 228)).xf(M(trans(-1.0 + rr.uniform(-0.5, 0.6), 0.005 + k * 0.004, -1.6 + rr.uniform(-0.3, 0.4)), roty(rr.uniform(-1, 1)))))
    cam = cam_lerp(Cam((-0.2, 1.45, -0.2), (-1.2, 1.3, -2.4), 50), Cam((0.2, 1.5, 0.4), (-1.0, 1.2, -2.4), 52), lt / dur)
    return merge(ms), cam, ENV_ROOM.copy(points=[((1.6, 1.8, -2.3), (255, 170, 110), 0.7, 5)], amb=0.4), {}


# ------------------------------------------------------------------ 4 : il attend
def shot_wait1(lt, dur, tg):
    look = 0.4 * math.sin(tg * 1.7)
    cam = wait_cam(lt, dur)
    ms = town(tree=TREE_SUMMER) + [dog_wait(HACHI, tg, look), crowd_flow(tg, 12, 1.3, 7)]
    return merge(ms), cam, ENV_EVE, {}


def shot_wait_night(lt, dur, tg):
    ms = town(tree=TREE_SUMMER) + [dog_wait(HACHI, tg, 0.0, extra=dict(hp=-0.15))]
    tgt = SPOT + np.array([0, 0.65, 0])
    f = np.array([math.sin(DOG_YAW - 0.5), 0, math.cos(DOG_YAW - 0.5)])
    cam = cam_lerp(Cam(tuple(tgt + f * 2.7 + np.array([0, 0.15, 0])), tuple(tgt), 42), Cam(tuple(tgt + f * 2.3 + np.array([0, 0.1, 0])), tuple(tgt), 40), lt / dur)
    env = ENV_NIGHT.copy(points=[((6, 4, 6), (255, 220, 150), 1.4, 9)])
    return merge(ms), cam, env, {}


def shot_next_day(lt, dur, tg):
    cam = wait_cam(lt, dur, 6, 2.5, -1.0)
    ms = town(tree=TREE_SUMMER) + [dog_wait(HACHI, tg, -0.3), crowd_flow(tg, 8, 1.0, 9, out=False)]
    return merge(ms), cam, ENV_DAY, {}


def shot_day_after(lt, dur, tg):
    global LAST_CAM
    LAST_CAM = None
    ms = town(tree=TREE_SUMMER) + [dog_wait(HACHI, tg, 0.3), crowd_flow(tg, 10, 1.4, 11)]
    tgt = SPOT + np.array([0, 0.5, 0])
    u = ease(lt / max(dur, 0.1))
    f = np.array([math.sin(DOG_YAW + 0.4), 0, math.cos(DOG_YAW + 0.4)])
    cam = Cam(tuple(tgt + f * lerp(5, 2.2, u) + np.array([0, 0.2, 0])), tuple(tgt), 45)
    return merge(ms), cam, ENV_EVE, {}


def shot_cta(lt, dur, tg):
    global LAST_CAM
    LAST_CAM = None
    ms = town(tree=TREE_SUMMER) + [dog_wait(HACHI, tg, 0.2 * math.sin(tg)), crowd_flow(tg, 12, 1.2, 13)]
    cam = cam_lerp(Cam((9, 4.5, 14), (1, 1.2, 2), 50), Cam((8, 4, 12.5), (1, 1.2, 2), 48), lt / dur)
    return merge(ms), cam, ENV_EVE, {}


# ------------------------------------------------------------------ 6 : les saisons, les gens
def shot_spring(lt, dur, tg):
    ms = town(tree=TREE_SPRING) + [dog_wait(HACHI, tg, 0.2)]
    cam = wait_cam(lt, dur, 3.5, 0.8)
    ms.append(C2.particles(SPOT + np.array([0, 2, 0]), tg, cam, 60, (5, 4, 5), 0.7, 0.07, (250, 190, 210), 2, spin=True))
    return merge(ms), cam, ENV_DAY, {}


def shot_snow(lt, dur, tg):
    ms = town(True, TREE_SNOW) + [dog_wait(HACHI, tg, -0.1)]
    ms.append(box(0.6, 0.06, 0.4, (245, 248, 252)).xf(trans(SPOT[0], 0.0, SPOT[2])))
    cam = wait_cam(lt, dur, 3.2, 0.9, -1)
    ms.append(C2.particles(SPOT + np.array([0, 2, 0]), tg, cam, 90, (5, 4, 5), 1.0, 0.06, (255, 255, 255), 1))
    return merge(ms), cam, ENV_SNOW, {}


def shot_chase(lt, dur, tg):
    """un employé de la gare le chasse avec un balai"""
    sw = math.sin(tg * 7)
    back = min(1.0, lt / 0.8)
    dp = SPOT + np.array([0.9, 0, 0.9]) * back
    ms = town(tree=TREE_SUMMER) + [HACHI.mesh(tuple(dp), DOG_YAW + 0.6, dict(hp=0.3, tail=-0.6, phase=lt * 8, amp=0.4 * (1 - back)))]
    ms.append(WORKER.mesh((SPOT[0] - 1.2, 0, SPOT[2] - 0.8), 0.9, dict(ra=(1.0 + 0.6 * sw, 0.2, 0.5), la=(0.9 + 0.6 * sw, -0.1, 0.6), lean=0.25,
                                                                     hand_r=broom_m().xf(M(rotx(-1.2), trans(0, -0.3, 0))))))
    cam = Cam((SPOT[0] + 1.6, 1.3, SPOT[2] + 3.4), (SPOT[0] - 0.3, 0.8, SPOT[2]), 50)
    return merge(ms), cam, ENV_DAY, {}


def broom_m():
    return merge([cyl(0.018, 0.018, 1.3, 5, (150, 110, 70)), box(0.25, 0.3, 0.06, (190, 160, 90)).xf(trans(0, 1.3, 0))])


def shot_feed(lt, dur, tg):
    """le vendeur de yakitori lui tend une brochette : Hachi la prend dans la gueule"""
    yp = SPOT + np.array([2.8, 0, 0.0])
    ms = town(tree=TREE_SUMMER) + [YATAI.xf(M(trans(yp), roty(-math.pi / 2)))]
    dyaw = math.pi / 2 + 0.2
    dm = HACHI.mesh(tuple(SPOT), dyaw, dict(sit=1.0, hp=0.15, mouth=0.6, tail=math.sin(tg * 10) * 0.5))
    mouth = HACHI.mouth
    sk_dir = np.array([math.sin(dyaw + math.pi), 0, math.cos(dyaw + math.pi)])   # la brochette part de la gueule vers le vendeur
    grip = mouth + sk_dir * 0.26 + np.array([0, 0.02, 0])
    ms.append(VENDOR.mesh((SPOT[0] + 0.95, 0, SPOT[2] + 0.1), -math.pi / 2 - 0.2, dict(lean=0.5, hp=0.4, ik_r=grip)))
    m_sk, L = frame_along(grip, mouth + sk_dir * -0.02)
    ms.append(merge([cyl(0.006, 0.006, L, 4, (200, 170, 120)), box(0.035, 0.1, 0.035, (150, 80, 45)).xf(trans(0, L - 0.07, 0))]).xf(m_sk))
    ms.append(dm)
    cam = Cam(tuple(SPOT + np.array([-1.0, 1.0, 2.6])), tuple(SPOT + np.array([0.4, 0.55, 0])), 45)
    return merge(ms), cam, ENV_EVE.copy(points=[(tuple(yp + np.array([0.6, 1.8, 0.5])), (255, 120, 80), 0.8, 4)]), {}


def shot_returns(lt, dur, tg):
    """en automne, Hachi revient au trot et se rassoit à sa place"""
    u = min(1.0, lt / (dur * 0.7))
    start = SPOT + np.array([7.0, 0, 6.0])
    p = start + (SPOT - start) * ease(u)
    walking = u < 1
    ms = town(tree=TREE_AUTUMN) + [HACHI.mesh(tuple(p), math.atan2(SPOT[0] - start[0], SPOT[2] - start[2]) if walking else DOG_YAW,
                                              dog_walk(lt * 9, 1.0, tail=0.3) if walking else dict(sit=1.0))]
    cam = Cam((SPOT[0] + 3.5, 1.4, SPOT[2] + 5.5), tuple(p + np.array([0, 0.5, 0])), 50)
    ms.append(C2.particles(SPOT + np.array([2, 2, 2]), tg, cam, 40, (6, 4, 6), 0.9, 0.1, (210, 120, 50), 3, spin=True))
    return merge(ms), cam, ENV_EVE, {}


# ------------------------------------------------------------------ 7 : 1932, le journal
def shot_paper(lt, dur, tg):
    """un homme lit le journal : la photo de Hachi en une"""
    p = np.array([0.0, 0.0, 0.0])
    hold = p + np.array([0, 1.25, 0.42])
    paper = box(0.42, 0.55, 0.004, (255, 255, 255), 'newspaper').xf(M(trans(hold), rotx(-0.35), trans(0, -0.05, 0)))
    ms = [STATION.xf(trans(0, 0, -6)), PLAZA, salaryman(0).mesh(tuple(p), 0.0, dict(ik_l=hold + np.array([-0.2, 0.0, 0]), ik_r=hold + np.array([0.2, 0.0, 0]), hp=0.35)), paper]
    cam = cam_lerp(Cam((0.35, 1.9, -0.55), tuple(hold + np.array([0, -0.08, 0])), 45), Cam((0.3, 1.85, -0.4), tuple(hold + np.array([0, -0.08, 0])), 42), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_visitors(lt, dur, tg):
    ms = town(tree=TREE_SPRING) + [dog_wait(HACHI_OLD, tg, 0.3 * math.sin(tg))]
    rr = np.random.default_rng(4)
    for i in range(9):
        a = DOG_YAW + math.pi + (-1.2 + i * 0.3)
        r = 1.3 + (i % 3) * 0.5
        p = SPOT + np.array([math.sin(a) * r, 0, math.cos(a) * r])
        who = CROWD[i % len(CROWD)] if i != 4 else GIRL
        yaw = math.atan2(SPOT[0] - p[0], SPOT[2] - p[2])
        pose = dict(hp=0.4, lean=0.15)
        if i in (2, 5):
            pose = dict(lean=0.7, hp=0.6, ik_r=SPOT + np.array([0.05, 0.75, 0.05]))
        ms.append(who.mesh(tuple(p), yaw, pose))
    cam = wait_cam(lt, dur, 4.2, 2.2, 0.0)
    return merge(ms), cam, ENV_DAY, {}


def shot_name(lt, dur, tg):
    ms = town(tree=TREE_SPRING) + [dog_wait(HACHI_OLD, tg, 0.15, extra=dict(hp=0.05))]
    head = SPOT + np.array([0.0, 0.8, 0.0])
    d = np.array([math.sin(DOG_YAW), 0, math.cos(DOG_YAW)])
    cam = cam_lerp(Cam(tuple(head + d * 3.0 + np.array([0.3, 0.1, 0])), tuple(head - np.array([0, 0.15, 0])), 42), Cam(tuple(head + d * 2.5 + np.array([0.25, 0.1, 0])), tuple(head - np.array([0, 0.15, 0])), 40), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 8 : 1934, la statue
CLOTH = box(0.9, 1.0, 1.2, (240, 238, 230), 'cloth')


def statue_m(cloth=0.0):
    ms = [pedestal(1.1).xf(trans(STATUE_POS)), _STATUE.xf(M(trans(STATUE_POS + np.array([0, 1.25, 0])), roty(DOG_YAW + math.pi)))]
    if cloth < 1:
        ms.append(CLOTH.xf(M(trans(STATUE_POS + np.array([0.0 + cloth * 1.2, 1.25 - cloth * 1.0, 0])), rotz(-cloth * 1.2))))
    return merge(ms)


def shot_unveil(lt, dur, tg):
    cl = ease(min(1.0, max(0.0, (lt - 0.6) / 0.6)))
    ms = town(tree=TREE_SPRING) + [statue_m(cl)]
    for i in range(10):
        a = -0.9 + i * 0.2
        p = STATUE_POS + np.array([math.sin(a) * 3.5, 0, math.cos(a) * 3.5])
        pose = dict(ra=(2.3, 0.3, 0.3), la=(2.3, 0.3, 0.3)) if cl > 0.5 and i % 2 else dict(hp=-0.2)
        ms.append(CROWD[i % len(CROWD)].mesh(tuple(p), math.atan2(STATUE_POS[0] - p[0], STATUE_POS[2] - p[2]), pose))
    ms.append(GIRL.mesh(tuple(STATUE_POS + np.array([-0.9, 0, 1.4])), math.pi - 0.6, dict(ra=(1.4, 0.2, 0.2))))
    cam = cam_lerp(Cam(tuple(STATUE_POS + np.array([1.6, 2.4, 3.2])), tuple(STATUE_POS + np.array([0, 1.6, 0])), 52),
                   Cam(tuple(STATUE_POS + np.array([1.4, 2.3, 2.8])), tuple(STATUE_POS + np.array([0, 1.6, 0])), 50), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def festival(tg, cam_pos=None):
    """fête de l'inauguration : guirlandes de lanternes, drapeaux, foule qui applaudit"""
    ms = []
    for k in range(14):
        x = STATUE_POS[0] - 6 + k * 0.95
        y = 3.6 - 0.5 * math.sin(math.pi * k / 13)
        ms.append(sphere(0.18, 6, 3, (230, 60, 50) if k % 2 else (245, 230, 210), emis=0.6, sy=1.3).xf(trans(x, y, STATUE_POS[2] - 1.2)))
    ms.append(rod((STATUE_POS[0] - 6, 3.6, STATUE_POS[2] - 1.2), (STATUE_POS[0] + 6.4, 3.6, STATUE_POS[2] - 1.2), 0.01, (40, 40, 40), n=3))
    for x in (-6.2, 6.6):
        ms.append(cyl(0.06, 0.06, 3.8, 5, (110, 80, 55)).xf(trans(STATUE_POS[0] + x, 0, STATUE_POS[2] - 1.2)))
    rr = np.random.default_rng(7)
    for i in range(14):
        a = math.pi * 1.05 + i * (math.pi * 0.9 / 13)
        r = 2.6 + (i % 3) * 0.6
        p = STATUE_POS + np.array([math.cos(a) * r * 1.3, 0, math.sin(a) * r * 0.9])
        if cam_pos is not None and np.hypot(p[0] - cam_pos[0], p[2] - cam_pos[2]) < 2.5:
            continue
        clap = math.sin(tg * 9 + i) * 0.25
        yaw = math.atan2(STATUE_POS[0] - p[0], STATUE_POS[2] - p[2])
        pose = dict(ra=(1.3, -0.3 + clap, 1.2), la=(1.3, -0.3 + clap, 1.2)) if i % 3 else dict(ra=(2.7, 0.3, 0.2), la=(0.2, 0.1, 0.3))
        ms.append(CROWD[i % len(CROWD)].mesh(tuple(p), yaw, pose))
    return merge(ms)


def shot_beside(lt, dur, tg):
    """plan large : Hachikō, vieux, regarde sa propre statue au milieu de la fête"""
    dp = STATUE_POS + np.array([1.4, 0, 1.6])
    look = math.atan2(STATUE_POS[0] - dp[0], STATUE_POS[2] - dp[2])
    cam_p = STATUE_POS + np.array([4.5 - lt * 0.2, 2.2, 6.5 - lt * 0.2])
    ms = town(tree=TREE_SPRING) + [statue_m(1.0), festival(tg, cam_p), HACHI_OLD.mesh(tuple(dp), look, dict(sit=1.0, hp=-0.35, tail=math.sin(tg * 4) * 0.4))]
    cam = Cam(tuple(cam_p), tuple(STATUE_POS + np.array([0.7, 1.0, 0.8])), 50)
    ms.append(C2.particles(STATUE_POS + np.array([0, 3, 1]), tg, cam, 50, (5, 3, 4), 0.8, 0.07, (250, 190, 210), 2, spin=True))
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 9 : 8 mars 1935
def shot_alley(lt, dur, tg):
    """à l'aube, couché dans une ruelle : il relève la tête une dernière fois… puis la laisse retomber, les yeux se ferment"""
    k = ease(min(1.0, max(0.0, (lt - 0.5) / 1.2)))
    ms = [ALLEY, HACHI_OLD.mesh((0.6, 0, 0.0), 2.0, dict(lie=1.0, hp=-0.45 + 1.05 * k, eyes=1.0 if k < 0.7 else 0.0))]
    hd = HACHI_OLD.head
    fwd = np.array([math.sin(2.0), 0, math.cos(2.0)])
    side = np.array([fwd[2], 0, -fwd[0]])
    cam = cam_lerp(Cam(tuple(hd + fwd * 1.2 + side * 0.5 + np.array([0, 0.25, 0])), tuple(hd - np.array([0, 0.12, 0])), 45),
                   Cam(tuple(hd + fwd * 1.0 + side * 0.4 + np.array([0, 0.18, 0])), tuple(hd - np.array([0, 0.15, 0])), 42), lt / dur)
    ms.append(C2.particles((0.5, 2.0, 0.5), tg, cam, 24, (3, 3, 3), 0.4, 0.06, (250, 200, 215), 5, spin=True))
    return merge(ms), cam, ENV_DAWN, dict(fade=0.3 * k)


def memorial():
    """petit mémorial à sa place : stèle en bois, fleurs, bâtons d'encens, bol"""
    ms = [box(0.7, 0.06, 0.4, (140, 135, 125), 'granite').xf(trans(0, 0, 0)),
          box(0.12, 0.75, 0.06, (175, 140, 95), 'wood_jp').xf(trans(0, 0.06, -0.08)),
          box(0.14, 0.04, 0.08, (60, 50, 40)).xf(trans(0, 0.81, -0.08))]
    for k in range(4):
        ms.append(box(0.012, 0.06, 0.003, (30, 25, 20)).xf(trans(-0.02, 0.6 - k * 0.1, -0.048)))
    ms.append(cyl(0.07, 0.05, 0.06, 8, (60, 60, 65), 'metal').xf(trans(0.18, 0.06, 0.06)))
    for i in range(3):
        ms.append(cyl(0.004, 0.004, 0.2, 3, (150, 60, 40)).xf(M(trans(0.18 + (i - 1) * 0.02, 0.1, 0.06), rotz((i - 1) * 0.15))))
    for i, c in enumerate(((240, 230, 90), (240, 240, 240), (230, 90, 120), (250, 180, 60))):
        x = -0.25 + i * 0.06
        ms.append(cyl(0.006, 0.006, 0.25, 3, (60, 120, 50)).xf(trans(x, 0.06, 0.08)))
        ms.append(sphere(0.035, 5, 3, c).xf(trans(x, 0.33, 0.08)))
    ms.append(cyl(0.06, 0.05, 0.09, 8, (210, 200, 180)).xf(trans(-0.17, 0.06, 0.08)))
    return merge(ms)


MEMORIAL = memorial()


def shot_empty_spot(lt, dur, tg):
    """sa place, vide : un petit mémorial, de l'encens, des passants qui s'inclinent"""
    global LAST_CAM
    LAST_CAM = None
    cam = wait_cam(lt, dur, 2.6, 0.9)
    yaw = DOG_YAW
    ms = town(tree=TREE_SPRING) + [crowd_flow(tg, 8, 0.8, 21), MEMORIAL.xf(M(trans(SPOT), roty(yaw)))]
    smoke = C2.particles(SPOT + np.array([0.0, 0.6, 0.0]), tg, cam, 6, (0.05, 0.6, 0.05), -0.25, 0.05, (220, 220, 225), 9, alpha=0.4)
    ms.append(smoke)
    for i, (dx, dz) in enumerate(((-1.2, 1.0), (-0.3, 1.5))):
        p = SPOT + np.array([dx, 0, dz])
        ms.append(CROWD[i + 3].mesh(tuple(p), math.atan2(SPOT[0] - p[0], SPOT[2] - p[2]), dict(lean=0.35, hp=0.4, la=(0.7, -0.2, 1.6), ra=(0.7, -0.2, 1.6))))
    return merge(ms), cam, ENV_DAWN, {}


# ------------------------------------------------------------------ 10 : la guerre, 1948
def shot_melt(lt, dur, tg):
    """1944 : la statue est descendue de son socle à la corde"""
    lift = ease(min(1.0, lt / (dur * 0.8)))
    sp = STATUE_POS + np.array([0, 1.25 + 0.8 * lift, 0])
    ms = town() + [pedestal(1.1).xf(trans(STATUE_POS)), _STATUE.xf(M(trans(sp + np.array([0.9 * lift, 0, 0])), roty(DOG_YAW + math.pi), rotz(-0.6 * lift)))]
    ms.append(box(0.3, 6.0, 0.3, (90, 70, 50)).xf(trans(STATUE_POS + np.array([0.9, 0, -0.9]))))
    ms.append(box(2.5, 0.25, 0.25, (90, 70, 50)).xf(trans(STATUE_POS + np.array([0.3, 6.0, -0.9]))))
    ms.append(rod(STATUE_POS + np.array([0.0, 6.0, -0.9]), sp + np.array([0.9 * lift, 0.6, 0]), 0.02, (60, 50, 40), n=3))
    for i, (dx, dz) in enumerate(((2.0, 1.4), (2.8, 0.4))):
        ms.append(WORKER.mesh(tuple(STATUE_POS + np.array([dx, 0, dz])), -1.9, dict(ra=(2.6, 0.1, 0.4), la=(2.4, -0.1, 0.5), lean=-0.15)))
    cam = cam_lerp(Cam(tuple(STATUE_POS + np.array([3.5, 1.5, 5.5])), tuple(STATUE_POS + np.array([0, 1.8, 0])), 50),
                   Cam(tuple(STATUE_POS + np.array([3.0, 1.4, 4.8])), tuple(STATUE_POS + np.array([0, 1.9, 0])), 48), lt / dur)
    return merge(ms), cam, ENV_WAR, dict(post_pil=C2.tint((200, 190, 170), 0.5))


def shot_new(lt, dur, tg):
    ms = town(tree=TREE_SPRING) + [statue_m(1.0), crowd_flow(tg, 10, 1.1, 31, cam=STATUE_POS + np.array([4.0, 0, 4.5]))]
    u = lt / max(dur, 0.1)
    cam = Cam(tuple(STATUE_POS + np.array([4.0 - u, 1.2, 4.5])), tuple(STATUE_POS + np.array([0, 1.6, 0])), 50)
    return merge(ms), cam, ENV_DAY, {}


def shot_today(lt, dur, tg):
    ms = town(tree=TREE_SUMMER) + [statue_m(1.0), crowd_flow(tg, 14, 1.4, 41, cam=STATUE_POS + np.array([-2.0, 0, 5.0]))]
    for i in range(3):
        p = STATUE_POS + np.array([1.6 + i * 0.7, 0, 1.8 + (i % 2) * 0.6])
        ms.append(CROWD[i + 2].mesh(tuple(p), math.atan2(STATUE_POS[0] - p[0], STATUE_POS[2] - p[2]), dict(ra=(1.5, 0.1, 1.0), la=(1.4, -0.1, 1.0))))
    cam = cam_lerp(Cam(tuple(STATUE_POS + np.array([-2.0, 1.0, 5.0])), tuple(STATUE_POS + np.array([0, 1.6, 0])), 50),
                   Cam(tuple(STATUE_POS + np.array([-1.6, 0.9, 4.2])), tuple(STATUE_POS + np.array([0, 1.6, 0])), 48), lt / dur)
    return merge(ms), cam, ENV_NIGHT.copy(points=[((-6, 4, 6), (255, 220, 150), 1.6, 12), ((6, 4, 6), (255, 220, 150), 1.6, 12)], amb=0.55), {}


# ------------------------------------------------------------------ 11 : 2015, les retrouvailles
REUNION = statue_reunion()


def shot_campus(lt, dur, tg):
    a = 0.3 + lt * 0.15
    ms = [CAMPUS, pedestal_big(), REUNION.xf(trans(0, 1.35, 0))]
    cam = Cam((math.sin(a) * 7.5, 2.8, math.cos(a) * 7.5), (0, 1.9, 0), 50)
    return merge(ms), cam, ENV_DAY, {}


def shot_reunion_close(lt, dur, tg):
    ms = [CAMPUS, pedestal_big(), REUNION.xf(trans(0, 1.35, 0))]
    cam = cam_lerp(Cam((3.4, 2.8, 3.4), (0, 2.2, 0.3), 45), Cam((3.0, 2.75, 3.0), (0, 2.2, 0.3), 43), lt / dur)
    return merge(ms), cam, ENV_EVE, {}


# ------------------------------------------------------------------ 12 : fin (souvenir)
WARM = C2.chain(C2.tint((255, 200, 140), 0.25), lambda im: C2.vignette(im, 0.6, (60, 30, 15)))


def pedestal_big():
    return merge([box(2.4, 1.2, 2.6, (255, 255, 255), 'granite').xf(trans(0, 0, 0.35)), box(2.7, 0.15, 2.9, (255, 255, 255), 'granite').xf(trans(0, 1.2, 0.35))])


def shot_final(lt, dur, tg):
    """souvenir : Ueno sort de la gare au coucher du soleil, s'accroupit, Hachi court et se dresse contre lui"""
    up = EXIT + np.array([0.6, 0, 1.6])
    k = ease(min(1.0, lt / 0.9))
    to_u = up - SPOT
    stop = up - to_u / np.linalg.norm(to_u) * 0.85
    dpos = SPOT + (stop - SPOT) * k
    dog = HACHI.mesh(tuple(dpos), math.atan2(up[0] - dpos[0], up[2] - dpos[2]), dict(jump=1.0 if k > 0.7 else 0.0, phase=lt * 9, amp=1.0 if k < 0.95 else 0.0,
                                                                                    mouth=1.0, tail=math.sin(tg * 14) * 0.8))
    u_pose = dict(ll=(0.0, 1.57), rl=(0.4, 1.3), drop=0.45, lean=0.3, la=(1.3, 0.4, 0.5), ra=(1.3, 0.4, 0.5), hp=0.2, face='ueno_smile')
    ms = town(tree=TREE_SPRING) + [UENO_S.mesh(tuple(up), math.atan2(dpos[0] - up[0], dpos[2] - up[2]), u_pose), dog]
    ms.append(C2.particles(SPOT + np.array([0, 2, 0]), tg, Cam((4, 1, 7), (1, 0.8, 2)), 40, (5, 4, 5), 0.6, 0.07, (250, 190, 210), 2, spin=True))
    c = (up + dpos) / 2 + np.array([0, 0.7, 0])
    side = np.array([-(up - dpos)[2], 0, (up - dpos)[0]])
    side = side / (np.linalg.norm(side) + 1e-9)
    if side[2] < 0:
        side = -side
    cam = cam_lerp(Cam(tuple(c + side * 3.4 + np.array([0, 0.35, 0])), tuple(c), 45), Cam(tuple(c + side * 2.8 + np.array([0, 0.3, 0])), tuple(c), 42), lt / dur)
    fade = max(0.0, (lt - dur + 0.7) / 0.7)
    return merge(ms), cam, ENV_EVE, dict(post_pil=WARM, fade=fade)


# ------------------------------------------------------------------ montage
add('hook', 0.0, shot_hook)
add('tokyo', T(1), shot_tokyo)
add('puppy', WT(1, 'chiot') - 0.25, shot_puppy)
add('pet', T(1, -4) - 0.1, shot_pet)
add('morning', T(2), shot_morning)
add('evening', WT(2, 'Et') - 0.05, shot_evening)
add('office', T(3), shot_office)
add('empty', WT(3, 'Il') - 0.05, shot_empty)
add('wait1', T(4), shot_wait1)
add('wait_night', T(4, 7) - 0.05, shot_wait_night)
add('next_day', T(4, 9) - 0.05, shot_next_day)
add('day_after', T(4, 12) - 0.05, shot_day_after)
add('cta', T(5), shot_cta)
add('spring', T(6), shot_spring)
add('snow', T(6, 3) - 0.05, shot_snow)
add('chase', T(6, 6) - 0.05, shot_chase)
add('feed', T(6, 9) - 0.05, shot_feed)
add('returns', T(6, 12) - 0.05, shot_returns)
add('paper', T(7), shot_paper)
add('visitors', T(7, 7) - 0.05, shot_visitors)
add('name', T(7, 12) - 0.05, shot_name)
add('unveil', T(8), shot_unveil)
add('beside', T(8, 12) - 0.1, shot_beside)
add('alley', T(9), shot_alley)
add('empty_spot', T(9, 13) - 0.05, shot_empty_spot)
add('melt', T(10), shot_melt)
add('new', T(10, 7) - 0.05, shot_new)
add('today', T(10, 13) - 0.05, shot_today)
add('campus', T(11), shot_campus)
add('reunion_close', T(11, 14) - 0.1, shot_reunion_close)
add('final', T(12), shot_final)


def day_counter():
    """« JOUR n » qui défile pendant les saisons, puis « 3 573 JOURS » au moment de sa mort"""
    t0, t1 = S('spring'), S('paper')

    def ov(img, t):
        if t0 <= t < t1:
            u = (t - t0) / (t1 - t0)
            n = int(2 + (2600 - 2) * u ** 1.6)
            C2.badge(f'JOUR {n:,}'.replace(',', ' '), t0, t1 - t0 + 0.01)(img, t)
    return ov


tl.overlay = C2.overlays(
    C2.hook_title(['9 ANS ET DEMI', 'À ATTENDRE.'], 0.0, T(1) - 0.05, y=250, accent=0),
    day_counter(),
    C2.badge('3 573 JOURS', S('empty_spot') + 0.1, S('melt') - S('empty_spot') - 0.15),
    C2.cta(T(5) - 0.1, max(2.6, T(6) - T(5) + 0.05)),
)

subs = Subs(timing)


def build_audio(path):
    dur = tl.duration()
    mx = A.Mixer(dur)
    # accroche : tic-tac accéléré, foule
    for i in range(int(T(1) / 0.16)):
        mx.add(A.tick(), i * 0.16, 0.35)
    mx.add(A.crowd(4), 0, 0.35, length=T(1))
    mx.add(C2.impact(), 0.0, 0.6)
    mx.add(C2.riser(1.2), T(1) - 1.2, 0.35)
    # 1924
    mx.add(A.crowd(5), S('tokyo'), 0.3, length=S('puppy') - S('tokyo'))
    mx.add(A.steam_whistle(1.0, 700), S('tokyo') + 0.3, 0.2)
    mx.add(A.wheel_rattle(3), S('tokyo'), 0.3, length=S('puppy') - S('tokyo'))
    mx.add(A.birds(8), S('puppy'), 0.35, length=S('morning') - S('puppy'))
    mx.add(A.clank(0.2), S('puppy') + 0.1, 0.3)
    mx.add(C2.pop(), S('puppy') + 0.5, 0.4)
    mx.add(A.crowd(8), S('morning'), 0.3, 0.3, 0.3, length=S('office') - S('morning'))
    mx.add(A.footsteps(3, 2.2), S('morning'), 0.4, length=S('evening') - S('morning'))
    mx.add(A.bell(1.5, 880), S('evening') + 0.2, 0.3)
    mx.add(C2.ding(), S('evening') + 0.75, 0.3)
    # 1925
    mx.add(A.tick(), S('office') + 0.2, 0.3)
    mx.add(C2.heartbeat(3, 64), S('office'), 0.4, length=S('empty') - S('office'))
    mx.add(C2.impact(), WT(3, 'Ueno') + 0.4, 0.4)
    mx.add(A.wind(5), S('empty'), 0.2, length=S('wait1') - S('empty'))
    mx.add(A.crowd(6), S('wait1'), 0.35, length=S('wait_night') - S('wait1'))
    mx.add(A.wind(4), S('wait_night'), 0.3, length=S('next_day') - S('wait_night'))
    mx.add(A.crowd(6), S('next_day'), 0.3, length=S('spring') - S('next_day'))
    mx.add(C2.pop(), T(5) + 0.05, 0.5)
    mx.add(C2.ding(), T(5) + max(2.6, T(6) - T(5) + 0.05) * 0.62, 0.45)
    # saisons
    mx.add(A.birds(4), S('spring'), 0.35, length=S('snow') - S('spring'))
    mx.add(A.wind(4), S('snow'), 0.4, length=S('chase') - S('snow'))
    mx.add(A.sweep_broom(1.5), S('chase') + 0.1, 0.5)
    mx.add(C2.pop(), S('feed') + 0.4, 0.3)
    mx.add(A.fire_crackle(3), S('feed'), 0.25, length=S('returns') - S('feed'))
    mx.add(A.footsteps(2, 4), S('returns'), 0.3, length=S('paper') - S('returns'))
    for i in range(int((S('paper') - S('spring')) / 0.25)):
        mx.add(A.tick(), S('spring') + i * 0.25, 0.12)
    mx.add(A.splinter(0.5), S('paper') + 0.1, 0.25)
    mx.add(A.crowd(6), S('visitors'), 0.35, length=S('name') - S('visitors'))
    mx.add(A.crowd(6), S('unveil'), 0.4, length=S('alley') - S('unveil'))
    mx.add(A.sting(), S('unveil') + 0.9, 0.5)
    mx.add(A.whoosh(0.8), S('unveil') + 0.6, 0.4)
    mx.add(A.wind(6), S('alley'), 0.25, length=S('melt') - S('alley'))
    mx.add(C2.metal_groan(2.5), S('melt'), 0.4)
    mx.add(A.ratchet(1.5), S('melt') + 0.4, 0.3)
    mx.add(A.crowd(6), S('new'), 0.3, length=S('campus') - S('new'))
    mx.add(A.birds(6), S('campus'), 0.35, length=S('final') - S('campus'))
    mx.add(C2.riser(1.2), S('reunion_close') - 1.0, 0.3)
    mx.add(A.bell(2.0, 660), S('final') + 0.2, 0.25)
    # musiques : koto discret puis émotion
    C2.music_bed(mx, S('tokyo'), S('office'), 'japan', 92, 0.22, 1)
    C2.music_bed(mx, S('office'), S('unveil'), 'sad', 66, 0.26, 2)
    C2.music_bed(mx, S('unveil'), S('alley'), 'japan', 92, 0.22, 3)
    C2.music_bed(mx, S('alley'), S('campus'), 'sad', 58, 0.26, 4)
    C2.music_bed(mx, S('campus'), dur, 'hope', 76, 0.26, 5)
    C2.cut_sounds(mx, list(SHOT_STARTS.values()), 0.08)
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
        render_video(tl, os.path.join(HERE, 'hachi_draft.mp4'), os.path.join(HERE, 'sfx.wav'), subs)
    else:
        build_audio(os.path.join(HERE, 'sfx.wav'))
        mix_voice(os.path.join(HERE, 'voix.wav'), os.path.join(HERE, 'sfx.wav'), os.path.join(HERE, 'mix.wav'))
        render_video(tl, os.path.join(HERE, 'Hachiko_Good2No.mp4'), os.path.join(HERE, 'mix.wav'), subs)
