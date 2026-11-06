"""Vidéo : la guerre de 38 minutes (Zanzibar, 1896)."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n', '/home/claude/g2n/zanzibar']
import numpy as np
from world import *
from video_core import *
from scripts import ZAN as LINES
import audio as A

HERE = '/home/claude/g2n/zanzibar'
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


# ------------------------------------------------------------------ disposition
HOW_POS = np.array([-42.0, 0, -22.0])      # House of Wonders (façade z=-14, galerie -11)
PAL_POS = np.array([12.0, 0, -18.0])       # palais (façade z=-11)
LIGHT_POS = np.array([-17.0, 0, -8.0])
GER_POS = np.array([75.0, 0, -42.0])
FLAG_WORLD = PAL_POS + np.array(PALACE_FLAG_POS)
CLOCK_WORLD = HOW_POS + np.array(CLOCK_POS)

# navires (proue vers -x après rotation, canons vers la côte -z)
SHIPS = [('gunboat', np.array([20.0, -0.9, 70.0])), ('gunboat', np.array([-30.0, -0.9, 85.0])), ('gunboat', np.array([70.0, -0.9, 95.0])),
         ('cruiser', np.array([-10.0, -0.9, 200.0])), ('cruiser', np.array([110.0, -0.9, 230.0]))]


YACHT_POS = np.array([40.0, -0.9, 45.0])


AIM = PAL_POS + np.array([0, 6.0, 7.0])


def ground():
    g1 = grid(-200, -160, 200, -11, 10, 8, None, (255, 255, 255), 'dirt', 3.0)
    # front de mer : esplanade au niveau de la ville, plage qui descend jusqu'à l'eau
    # sable seulement devant l'esplanade : plus aucune surface superposée au même niveau
    g2 = grid(-200, 2.0, 200, 12, 12, 3, lambda x, z: max(-1.8, -0.3 * (z - 2.0)), (255, 255, 255), 'sand', 3.0)
    esplanade = box(400, 0.3, 13.0, (215, 200, 170), 'stone_block', ts=1.2, faces='u').xf(trans(0, -0.3, -4.5))
    quay = merge([box(70, 1.6, 1.2, (220, 210, 185), 'stone_block', ts=1.0).xf(trans(10, -1.6, 2.4)),
                  box(70, 0.15, 0.4, (200, 190, 165)).xf(trans(10, 0.0, 2.0))])
    jetty = merge([box(3.0, 0.15, 22, (150, 120, 85), 'deck_planks', ts=1.0).xf(trans(-5, -0.15, 13))] +
                  [cyl(0.12, 0.12, 2.2, 5, (110, 80, 55)).xf(trans(-5 + s * 1.3, -2.1, z)) for s in (-1, 1) for z in range(4, 24, 3)])
    return merge([g1, g2, esplanade, quay, jetty])


def static_town():
    ms = [ground(), house_of_wonders(9, 0).xf(trans(HOW_POS)) if False else Mesh(), lighthouse().xf(trans(LIGHT_POS)),
          stone_town(1, -170, 170, -110, -30, 55, avoid=[(-75, -5, -45, -5), (-25, 45, -45, -5), (55, 95, -55, -25)])]
    rr = np.random.default_rng(2)
    for i in range(14):
        x = rr.uniform(-160, 160)
        if -75 < x < 45:
            continue
        ms.append(palm(7 + rr.random() * 3, i).xf(trans(x, 0, rr.uniform(-12, -6))))
    for x in (-62, -58, -20, 40, 48):
        ms.append(palm(8, int(abs(x))).xf(trans(x, 0, -9)))
    return merge(ms)


TOWN_BASE = static_town()
TOWN = merge([TOWN_BASE, german_consulate().xf(trans(GER_POS))])
HOW_CACHE = {}


def how(hour, minute):
    k = (hour, int(minute))
    if k not in HOW_CACHE:
        HOW_CACHE[k] = house_of_wonders(hour, minute).xf(trans(HOW_POS))
    return HOW_CACHE[k]


PAL_CACHE = {}


def pal(burn):
    k = round(burn, 1)
    if k not in PAL_CACHE:
        PAL_CACHE[k] = palace(k).xf(trans(PAL_POS))
    return PAL_CACHE[k]


def ship_matrix(p):
    return M(trans(p), roty(math.pi))


def aim_yaws(kind, p, u=1.0):
    """orientation de chaque tourelle pour viser le palais (u : 0 = repos, 1 = pointée)"""
    Ms = ship_matrix(p)
    out = []
    for (gx, ty, glen, gh) in turrets(kind):
        tw = (Ms @ np.array([gx, ty + gh, 0, 1]))[:3]
        d = AIM - tw
        g = math.atan2(d[2], -d[0])
        if g > math.pi:
            g -= 2 * math.pi
        out.append(g * u)
    return out


def barrel_tips(kind, p, u=1.0):
    Ms = ship_matrix(p)
    tips = []
    for (gx, ty, glen, gh), g in zip(turrets(kind), aim_yaws(kind, p, u)):
        tips.append((Ms @ M(trans(gx, ty, 0), roty(g)) @ np.array([glen + 0.3, gh, 0, 1]))[:3])
    return tips


def fleet(t, gun_yaw=0.0):
    u = min(1.0, abs(gun_yaw) / 0.6)
    ms = []
    for i, (kind, p) in enumerate(SHIPS):
        ms.append(warship(kind, t + i, gun_yaws=aim_yaws(kind, p, u)).xf(ship_matrix(p)))
    return merge(ms)


def fleet_smoke(t, cam):
    ms = []
    for i, (kind, p) in enumerate(SHIPS):
        L = WARSHIP_DIMS[kind][0]
        h = (9 if kind == 'cruiser' else 6) + WARSHIP_DIMS[kind][2] * 0.4 + 2.6
        ms.append(smoke_sprites(p + np.array([L * 0.03, h, 0]), t, cam, n=4, size=2.0, rise=8, seed=i, col=(90, 88, 85), drift=(0.8, 0, 0.2), alpha=0.6))
    return merge(ms)


def defenders(t, n=90, panic=0.0):
    """~3 000 défenseurs : on en montre une foule armée devant, sur les barricades et aux balcons"""
    rr = np.random.default_rng(4)
    ms = [barricade(16, 1).xf(trans(PAL_POS[0], 0, -2.6)), barricade(12, 2).xf(trans(PAL_POS[0] - 20, 0, -2.8)),
          barricade(10, 3).xf(trans(PAL_POS[0] + 22, 0, -3.0))]
    for cx in (-6, 0, 7):
        ms.append(old_cannon().xf(M(trans(PAL_POS[0] + cx, 0, -5.4), roty(-math.pi / 2))))
    types = [askari('askari'), askari('askari2'), askari('askari', (150, 35, 30)), civilian(), civilian(col=(215, 205, 180)), civilian(col=(230, 225, 210))]
    for i in range(n):
        h = types[i % len(types)]
        if i < 60:
            x = PAL_POS[0] - 30 + rr.random() * 60
            z = -3.5 - rr.random() * 7.0
            y = 0.0
        else:  # aux balcons du palais
            x = PAL_POS[0] - 10 + rr.random() * 20
            z = PAL_POS[2] + 8.2
            y = 4.65 if i % 2 else 8.65
        ph = t * 2 + i
        r = rifle().xf(M(rotx(-1.45), trans(0, 0, -0.35)))
        k = rr.random()
        if k < 0.55:  # fusil à l'épaule, en joue vers la mer
            pose = dict(ra=(1.45, 0.05, 0.25), la=(1.35, -0.3, 0.6), hand_r=r, hy=0.1 * math.sin(ph * 0.3))
        elif k < 0.8:  # fusil levé, crie
            pose = dict(ra=(2.7 + 0.2 * math.sin(ph), 0.2, 0.2), hand_r=rifle().xf(rotx(-0.3)), face='askari' if i % 2 else None)
        else:  # porte des munitions
            pose = dict(ra=(0.8, 0.1, 1.4), la=(0.8, -0.1, 1.4), hand_r=box(0.4, 0.25, 0.3, (120, 90, 60), 'planks').xf(trans(0.15, -0.1, 0.1)))
        if pose.get('face') is None:
            pose.pop('face', None)
        ms.append(h.mesh((x, y, z), rr.uniform(-0.25, 0.25), pose))
    return merge(ms)


DEF_CACHE = {}


def defenders_c(tk):
    k = int(tk * 4) % 8
    if k not in DEF_CACHE:
        DEF_CACHE[k] = defenders(k / 4.0)
    return DEF_CACHE[k]


def harbor_scene(t, cam, hour=9, minute=0, burn=0.0, yacht_state=(0, 0), flag_up=True, gun_yaw=0.0, show_def=True):
    ms = [TOWN, how(hour, minute), pal(burn), sea(t=t), fleet(t, gun_yaw), fleet_smoke(t, cam)]
    if yacht_state is not None:
        tilt, sink = yacht_state
        if sink < 9:
            ms.append(yacht(t, tilt, sink).xf(M(trans(YACHT_POS), roty(math.pi * 0.95))))
    if flag_up:
        ms.append(flagpole('red_cloth', 7, t, 3.2, 2.0).xf(trans(FLAG_WORLD)))
    if show_def:
        ms.append(defenders_c(t))
    for i in range(3):
        ms.append(dhow(t, i).xf(M(trans(-90 + i * 25, -1.1, 30 + i * 12), roty(0.3 * i))))
    return ms


# ------------------------------------------------------------------ 0 : accroche
def shot_hook(lt, dur, tg):
    # un seul navire au premier plan qui tire sur le palais en feu
    kind, p = SHIPS[0]
    cam = cam_lerp(Cam((p[0] + 34, 7, p[2] + 30), (p[0] - 14, 5, -8), 50), Cam((p[0] + 31, 6.5, p[2] + 27), (p[0] - 14, 5, -8), 50), lt / dur)
    ms = [TOWN, how(9, 15), pal(0.6), sea(t=tg), warship(kind, tg, gun_yaws=aim_yaws(kind, p, 1.0)).xf(ship_matrix(p)),
          flagpole('red_cloth', 7, tg, 3.2, 2.0).xf(trans(FLAG_WORLD))]
    fl, kf = gun_flashes(lt + 0.5, cam, period=0.9, ships=(0,))
    ms.append(fl)
    ex = []
    for k, (te, pos) in enumerate(((0.3, (6, 10, -11)), (1.1, (18, 6, -11)), (1.9, (0, 12, -12)), (2.7, (24, 9, -10)), (3.4, (-8, 7, -11)))):
        ex.append(explosion(pos, lt - te, cam, 5, k))
    ms += ex
    ms.append(big_smoke(PAL_POS + np.array([0, 13, 0]), tg, cam, 10, 7, 25, 3))
    ms.append(fire_sprites(PAL_POS + np.array([-6, 13, 5]), tg, cam, 6, 2.5, 3, 4))
    ms.append(fire_sprites(PAL_POS + np.array([6, 13, 5]), tg, cam, 6, 2.5, 3, 5))
    env = ENV_SMOKE.copy(points=[(tuple(PAL_POS + np.array([0, 8, 8])), (255, 140, 60), 1.0, 40)])
    return merge(ms), cam, env, {}


def shot_watch(lt, dur, tg):
    """montre à gousset : 9 h 02 -> 9 h 40 en accéléré"""
    u = min(1, lt / max(0.1, dur - 0.3))
    minute = 2 + 38 * ease(u)
    sec = (lt * 600) % 60
    cam = Cam((0, 2.3, 0.6), (0, 0, 0.05), 45)
    hand = merge([box(0.8, 0.25, 1.3, (232, 195, 165)).xf(trans(0, -0.3, 0.45)), box(0.9, 0.3, 1.0, (240, 238, 228)).xf(trans(0, -0.35, 1.4))])
    ms = [pocket_watch(minute, sec, 9, 1.0), hand, box(6, 0.05, 6, (220, 210, 190), 'deck_planks').xf(trans(0, -0.9, 0))]
    return merge(ms), cam, ENV_ROOM.copy(points=[((0.5, 2, 0.5), (255, 230, 190), 0.6, 4)], fog_near=4, fog_far=12), {}


# ------------------------------------------------------------------ 1 : l'île
ISLAND = island_map()


def shot_island(lt, dur, tg):
    u = ease(lt / dur)
    st = STONE_TOWN_GEO
    cam = Cam(lerpv((70, 150, 120), (st[0] + 18, 28, st[1] + 30), u), lerpv((-10, 0, 0), (st[0] + 2, 0, st[1]), u), 55)
    ms = [ISLAND, sea(-1000, -1000, 1000, 1000, tg, -0.1, 'ocean', 30, 4)]
    ms.append(cloud_bank(0, 40, 0, 120, 7, (245, 245, 245), 10, 8))
    # point qui marque Stone Town
    ms.append(cyl(0.9, 0.9, 1.2, 8, (200, 40, 40), emis=0.8).xf(trans(st[0], 0.6, st[1])))
    return merge(ms), cam, ENV_MORNING.copy(fog_near=200, fog_far=1500), {}


def shot_town(lt, dur, tg):
    cam = cam_lerp(Cam((-80, 25, 120), (-10, 8, -20), 55), Cam((-60, 18, 95), (-10, 8, -20), 55), lt / dur)
    ms = harbor_scene(tg, cam, 8, 0, show_def=False)
    return merge(ms), cam, ENV_MORNING, {}


# ------------------------------------------------------------------ 2 : mort du sultan
def bedroom():
    ms = [box(10, 0.05, 8, (255, 255, 255), 'rug', ts=3.0).xf(trans(0, -0.05, 0)),
          box(10, 4, 0.1, (240, 232, 210), 'plaster', ts=1.5, faces='f').xf(trans(0, 0, -3.0)),
          box(0.1, 4, 8, (240, 232, 210), 'plaster', ts=1.5, faces='r').xf(trans(-4.0, 0, 0)),
          box(0.1, 4, 8, (240, 232, 210), 'plaster', ts=1.5, faces='l').xf(trans(4.0, 0, 0))]
    ms.append(box(1.4, 2.0, 0.06, (255, 255, 255), 'shutter').xf(trans(-2.0, 1.0, -2.94)))
    # lit à baldaquin
    ms.append(box(2.0, 0.6, 2.4, (240, 235, 220), 'cloth').xf(trans(0, 0, -1.5)))
    ms.append(box(2.1, 0.15, 2.5, (110, 70, 40), 'wood_dark').xf(trans(0, 0.0, -1.5)))
    for (x, z) in ((-1.0, -2.7), (1.0, -2.7), (-1.0, -0.3), (1.0, -0.3)):
        ms.append(cyl(0.06, 0.06, 2.6, 6, (110, 70, 40)).xf(trans(x, 0, z)))
    ms.append(box(2.2, 0.1, 2.6, (150, 30, 35), 'red_cloth').xf(trans(0, 2.6, -1.5)))
    ms.append(box(0.8, 0.15, 0.4, (250, 248, 240)).xf(trans(0, 0.6, -2.5)))
    # lampe à huile
    ms.append(box(0.5, 0.7, 0.5, (110, 70, 40), 'wood_dark').xf(trans(1.6, 0, -2.4)))
    ms.append(sphere(0.12, 6, 3, (255, 210, 120), emis=0.9).xf(trans(1.6, 0.85, -2.4)))
    # porte sculptée
    ms.append(box(1.6, 2.8, 0.08, (255, 255, 255), 'carved_door').xf(M(trans(3.95, 0, 1.5), roty(-math.pi / 2))))
    return merge(ms)


BEDROOM = bedroom()
ENV_BED = ENV_ROOM.copy(points=[((1.6, 1.0, -2.4), (255, 190, 110), 0.6, 4)], amb=0.45)


def shot_sultan(lt, dur, tg):
    cam = cam_lerp(Cam((1.5, 1.9, -0.6), (0, 0.85, -2.1), 45), Cam((1.3, 1.8, -0.9), (0, 0.85, -2.15), 45), lt / dur)
    sm = sultan().mesh((0, 0, 0), 0.0, dict(hat=False, la=(0.0, 0.1, 0.2), ra=(0.0, 0.1, 0.2)))
    ms = [BEDROOM, sm.xf(M(trans(0, 0.73, -0.45), rotx(-math.pi / 2)))]
    ms.append(box(1.8, 0.2, 1.1, (235, 228, 210), 'cloth').xf(trans(0, 0.6, -1.4)))
    ms.append(box(1.8, 0.5, 0.75, (235, 228, 210), 'cloth').xf(trans(0, 0.6, -0.55)))
    ms.append(servant().mesh((-1.6, 0, -1.2), 1.4, dict(hp=0.4, la=(0.9, 0.2, 1.5), ra=(0.9, -0.2, 1.5))))
    return merge(ms), cam, ENV_BED, {}


def shot_khalid_door(lt, dur, tg):
    cam = cam_lerp(Cam((0.2, 1.72, 0.6), (3.5, 1.6, 1.5), 45), Cam((0.5, 1.72, 0.7), (3.5, 1.65, 1.5), 45), lt / dur)
    face = 'khalid' if lt < dur * 0.6 else 'khalid_angry'
    k = khalid(face).mesh((3.5, 0, 1.5), -math.pi / 2, dict(hy=-0.2, ra=(0.6, 0.2, 1.6), la=(0.0, 0.1, 0.2)))
    env = ENV_BED.copy(points=[((1.6, 1.0, -2.4), (255, 190, 110), 1.0, 5), ((3.2, 2.0, 1.5), (255, 170, 90), 0.4, 3)], amb=0.35)
    return merge([BEDROOM, k]), cam, env, {}


# ------------------------------------------------------------------ 3 : trône, consul
def throne_room():
    ms = [box(14, 0.05, 12, (255, 255, 255), 'rug', ts=3.0).xf(trans(0, -0.05, 0)),
          box(14, 6, 0.1, (240, 232, 210), 'plaster', ts=2.0, faces='f').xf(trans(0, 0, -5.0)),
          box(0.1, 6, 12, (240, 232, 210), 'plaster', ts=2.0, faces='r').xf(trans(-6.0, 0, 0)),
          box(0.1, 6, 12, (240, 232, 210), 'plaster', ts=2.0, faces='l').xf(trans(6.0, 0, 0))]
    ms.append(box(3.0, 0.4, 2.0, (150, 30, 35), 'red_cloth').xf(trans(0, 0, -3.8)))
    ms.append(box(1.4, 0.6, 0.9, (200, 170, 70), 'metal').xf(trans(0, 0.4, -3.9)))
    ms.append(box(1.4, 1.6, 0.2, (200, 170, 70), 'metal').xf(trans(0, 0.4, -4.4)))
    ms.append(box(1.2, 0.15, 0.8, (150, 30, 35), 'red_cloth').xf(trans(0, 1.0, -3.9)))
    for x in (-0.8, 0.8):
        ms.append(box(0.2, 0.9, 0.9, (200, 170, 70), 'metal').xf(trans(x, 0.4, -3.9)))
    for x in (-4.5, -2.0, 2.0, 4.5):
        ms.append(cyl(0.3, 0.3, 6, 8, (235, 228, 210)).xf(trans(x, 0, -2.0)))
    for x in (-3.2, 3.2):
        ms.append(box(1.6, 3.0, 0.08, (255, 255, 255), 'shutter').xf(trans(x, 1.4, -4.94)))
    ms.append(flagpole('red_cloth', 3.5, 0, 1.4, 0.9, (200, 170, 70)).xf(trans(1.8, 0, -4.5)))
    return merge(ms)


THRONE = throne_room()


THRONE_SEAT = np.array([0.0, 1.15, -3.85])


def shot_throne(lt, dur, tg):
    """Khalid traverse la salle, monte sur l'estrade, se retourne et s'assoit sur le trône"""
    u = lt / dur
    if u < 0.5:
        k = ease(u / 0.5)
        pos, yaw, pose = (0, 0, lerp(1.5, -2.45, k)), math.pi, walk_pose(lt * 5, 0.8)
    elif u < 0.62:
        k = (u - 0.5) / 0.12
        pos = (0, 0.4 * min(1, k * 1.6), lerp(-2.45, -3.35, k))
        pose = walk_pose(lt * 5, 1.0, ll=(0.9 * (1 - k), 0.8 * (1 - k)))
        yaw = math.pi
    elif u < 0.74:
        k = (u - 0.62) / 0.12
        pos, yaw, pose = (0, 0.4, -3.35), math.pi * (1 - ease(k)), dict()
    else:
        k = min(1, (u - 0.74) / 0.1)
        drop = 0.3 * k
        pos = (0, 0.4 + (THRONE_SEAT[1] - 0.63 - 0.4) * k, lerp(-3.35, THRONE_SEAT[2], k))
        yaw = 0.0
        pose = sit_pose(drop=drop, ll=(1.5 * k, 1.5 * k), rl=(1.5 * k, 1.5 * k), la=(0.5, 0.2, 0.4), ra=(0.5, 0.2, 0.4),
                        face='khalid' if k < 1 else 'khalid_angry')
    km = khalid().mesh(pos, yaw, pose)
    cam = cam_lerp(Cam((3.8, 2.2, 1.5), (0, 1.3, -2.5), 55), Cam((3.0, 2.0, 0.4), (0, 1.4, -3.5), 55), lt / dur)
    ms = [THRONE, km]
    for i, x in enumerate((-2.6, 2.6)):
        ms.append(askari('askari2' if i else 'askari').mesh((x, 0, -2.8), 0.0, dict(hand_r=rifle().xf(rotx(-1.5)), ra=(0.2, 0.0, 0.2))))
    for i, x in enumerate((-3.5, -1.5, 1.5, 3.5)):
        ms.append(civilian(col=[(235, 232, 220), (215, 205, 180)][i % 2]).mesh((x, 0, 1.5 + (i % 2)), math.pi + (0.2 if x < 0 else -0.2), dict(hp=0.2)))
    return merge(ms), cam, ENV_ROOM.copy(points=[((0, 4, -2), (255, 225, 170), 0.8, 9)]), {}


def consul_office():
    ms = [box(10, 0.05, 8, (150, 110, 70), 'planks', ts=0.8).xf(trans(0, -0.05, 0)),
          box(10, 3.6, 0.1, (220, 215, 200), 'plaster', ts=1.5, faces='f').xf(trans(0, 0, -2.5)),
          box(0.1, 3.6, 8, (220, 215, 200), 'plaster', ts=1.5, faces='r').xf(trans(-3.5, 0, 0))]
    ms.append(box(2.2, 0.08, 1.1, (90, 60, 35), 'wood_dark').xf(trans(0, 0.8, -1.2)))
    for (x, z) in ((-1.0, -0.75), (1.0, -0.75), (-1.0, -1.65), (1.0, -1.65)):
        ms.append(box(0.08, 0.8, 0.08, (80, 55, 35)).xf(trans(x, 0, z)))
    ms.append(box(1.4, 1.0, 0.04, (255, 255, 255), 'union_jack').xf(trans(-1.6, 2.0, -2.44)))
    ms.append(box(1.2, 0.9, 0.04, (255, 255, 255), 'diagram' if 'diagram' in TEXB else 'ledger').xf(trans(1.4, 2.0, -2.44)))
    ms.append(box(0.3, 0.02, 0.4, (255, 255, 255), 'letter').xf(trans(0.2, 0.89, -1.1)))
    ms.append(cyl(0.05, 0.05, 0.12, 6, (30, 30, 30)).xf(trans(-0.6, 0.88, -1.3)))
    ms.append(box(1.2, 1.8, 0.06, (255, 255, 255), 'shutter').xf(trans(3.0, 1.0, -2.44)))
    return merge(ms)


OFFICE = consul_office()


CONSUL = consul('cave')


CONSUL_A = consul('cave_angry')


def shot_consul(lt, dur, tg):
    """le consul britannique lit la nouvelle, document tenu à deux mains, et secoue la tête"""
    cam = cam_lerp(Cam((1.6, 1.7, 1.8), (0, 1.3, -1.4), 50), Cam((1.3, 1.65, 1.4), (0, 1.35, -1.5), 50), lt / dur)
    angry = lt > dur * 0.4
    body = np.array([0.0, 0, -2.0])
    pc = body + np.array([0, 1.28, 0.38])
    Mp = M(trans(pc), rotx(-0.45))
    paper = box(0.26, 0.34, 0.006, (255, 255, 255), 'letter').xf(M(Mp, trans(0, -0.17, 0)))
    gl = (Mp @ np.array([-0.13, 0.0, 0.0, 1]))[:3]
    gr = (Mp @ np.array([0.13, 0.0, 0.0, 1]))[:3]
    who = CONSUL_A if angry else CONSUL
    pose = dict(hp=0.25 if not angry else 0.05, hy=0.35 * math.sin(lt * 10) if angry and lt < dur * 0.8 else 0.0,
                ik_l=gl, ik_r=gr, hat=False)
    ms = [OFFICE, who.mesh(tuple(body), 0.0, pose), paper]
    ms.append(hat_mesh('pith', (240, 238, 228)).xf(trans(-0.7, 0.88, -1.0)))
    return merge(ms), cam, ENV_ROOM.copy(points=[((0, 3, 0), (255, 240, 210), 0.6, 6)]), {}


# ------------------------------------------------------------------ 4 : ultimatum
def shot_ultimatum(lt, dur, tg):
    """l'ultimatum britannique : papier à en-tête de la Couronne, signature, cachet de cire"""
    cam = cam_lerp(Cam((0.2, 1.55, -0.55), (0.2, 0.88, -1.15), 45), Cam((0.2, 1.38, -0.75), (0.2, 0.88, -1.15), 45), lt / dur)
    ms = [OFFICE]
    ms.append(box(0.36, 0.004, 0.48, (255, 255, 255), 'ultimatum').xf(trans(0.2, 0.882, -1.15)))
    ms.append(box(0.08, 0.004, 0.06, (255, 255, 255), 'union_jack').xf(trans(0.07, 0.887, -1.33)))
    sign = math.sin(lt * 10) * 0.04
    if lt < dur * 0.6:
        ms.append(box(0.08, 0.06, 0.12, (235, 200, 175)).xf(trans(0.28 + sign, 0.9, -1.0)))
        ms.append(box(0.12, 0.1, 0.5, (238, 236, 228)).xf(trans(0.33 + sign, 0.92, -0.7)))
        ms.append(cyl(0.006, 0.004, 0.2, 4, (240, 240, 230)).xf(M(trans(0.26 + sign, 0.9, -1.03), rotz(0.4))))
    else:
        ms.append(cyl(0.035, 0.035, 0.008, 10, (170, 20, 20)).xf(trans(0.3, 0.887, -0.98)))
    return merge(ms), cam, ENV_ROOM.copy(points=[((0, 3, 0), (255, 240, 210), 0.6, 6)]), {}


def shot_clock8(lt, dur, tg):
    cw = CLOCK_WORLD
    cam = cam_lerp(Cam((cw[0] + 2, cw[1] - 6, cw[2] + 16), tuple(cw), 40), Cam((cw[0] + 1.5, cw[1] - 4, cw[2] + 11), tuple(cw), 40), lt / dur)
    minute = 55 + lt * 0.8
    ms = [TOWN, how(8, int(minute)), pal(0.0), sea(t=tg), flagpole('red_cloth', 7, tg, 3.2, 2.0).xf(trans(FLAG_WORLD))]
    return merge(ms), cam, ENV_MORNING, {}


# ------------------------------------------------------------------ 5 : refus, défenseurs
def shot_refuse(lt, dur, tg):
    bal = PAL_POS + np.array([0, 8.4 + 0.25, 7.8])
    cam = cam_lerp(Cam((bal[0] + 2.0, bal[1] + 1.4, bal[2] + 4.0), (bal[0], bal[1] + 1.4, bal[2]), 45),
                   Cam((bal[0] + 1.6, bal[1] + 1.5, bal[2] + 3.2), (bal[0], bal[1] + 1.5, bal[2]), 45), lt / dur)
    shake = math.sin(lt * 9) * 0.5 if lt > dur * 0.2 and lt < dur * 0.7 else 0.0
    km = khalid('khalid_angry').mesh(tuple(bal), 0.0, dict(hy=shake, la=(0.4, -0.5, 2.2), ra=(0.4, -0.5, 2.2)))
    ms = [TOWN, pal(0.0), km, flagpole('red_cloth', 7, tg, 3.2, 2.0).xf(trans(FLAG_WORLD)), sea(t=tg), fleet(tg)]
    for i, dx in enumerate((-2.0, 2.0)):
        ms.append(askari('askari' if i else 'askari2').mesh((bal[0] + dx, bal[1], bal[2] - 0.5), 0.0, dict(hand_r=rifle().xf(rotx(-1.5)), ra=(0.2, 0.0, 0.2))))
    return merge(ms), cam, ENV_MORNING, {}


def shot_threat(lt, dur, tg):
    """« sinon, leurs navires ouvriront le feu » : les servants chargent un obus dans le canon du croiseur"""
    kind, p = SHIPS[3]
    tips = barrel_tips(kind, p, 1.0)
    Ms = ship_matrix(p)
    gx, ty, glen, gh = turrets(kind)[0]
    tw = (Ms @ np.array([gx, ty, 0, 1]))[:3]
    cam = cam_lerp(Cam((tw[0] + 6, tw[1] + 3.2, tw[2] + 7), (tw[0] - 1, tw[1] + 0.8, tw[2] - 2), 55),
                   Cam((tw[0] + 5, tw[1] + 2.8, tw[2] + 6), (tw[0] - 1, tw[1] + 0.8, tw[2] - 2), 55), lt / dur)
    ms = [TOWN, how(8, 58), pal(0.0), sea(t=tg), fleet(tg, 0.6)]
    sh = cyl(0.17, 0.0, 0.25, 8, (110, 110, 115), 'metal').xf(trans(0, 0.55, 0))
    shell = merge([cyl(0.17, 0.17, 0.55, 8, (200, 170, 70), 'metal'), sh])
    deck_y = tw[1]
    for i, dx in enumerate((2.5, 3.5)):
        s = sailor()
        pos = (tw[0] + dx, deck_y, tw[2] + 1.6 + i * 0.8)
        u = (lt * 0.6 + i * 0.5) % 1
        c = np.array([tw[0] + dx - 0.5, deck_y + 0.9, tw[2] + 1.2 + i * 0.8])
        ms.append(shell.xf(M(trans(c), rotz(math.pi / 2))))
        ms.append(s.mesh(pos, -1.8, dict(ik_l=c + np.array([0, 0.1, 0.15]), ik_r=c + np.array([0.3, 0.1, -0.15]), lean=0.3)))
    return merge(ms), cam, ENV_MORNING, {}


def shot_defenders(lt, dur, tg):
    cam = cam_lerp(Cam((PAL_POS[0] + 20, 4.0, 1.5), (PAL_POS[0] - 2, 2.5, -9.0), 60), Cam((PAL_POS[0] + 16, 3.6, 0.5), (PAL_POS[0] - 4, 2.5, -9.0), 60), lt / dur)
    ms = [TOWN, how(8, 50), pal(0.0), defenders_c(tg), flagpole('red_cloth', 7, tg, 3.2, 2.0).xf(trans(FLAG_WORLD)), sea(t=tg)]
    return merge(ms), cam, ENV_MORNING, {}


# ------------------------------------------------------------------ 6 : la flotte
def shot_fleet(lt, dur, tg):
    yaw = -0.6 * ease(min(1, lt / (dur * 0.7)))
    cam = cam_lerp(Cam((-60, 30, 20), (30, 0, 150), 55), Cam((-50, 26, 25), (30, 0, 150), 55), lt / dur)
    ms = harbor_scene(tg, cam, 8, 55, gun_yaw=yaw, show_def=False)
    return merge(ms), cam, ENV_MORNING, {}


def shot_gun_close(lt, dur, tg):
    """gros plan : la tourelle de la canonnière pivote jusqu'à viser le palais"""
    kind, p = SHIPS[0]
    u = ease(min(1, lt / (dur * 0.8)))
    Ms = ship_matrix(p)
    gx, ty, glen, gh = turrets(kind)[0]
    tw = (Ms @ np.array([gx, ty, 0, 1]))[:3]
    d = AIM - tw
    d /= np.linalg.norm(d)
    side = np.cross(d, (0, 1, 0))
    cam = Cam(tuple(tw - d * 6 - side * 2.0 + np.array([0, 2.6, 0])), tuple(tw + d * 25), 52)
    ms = [TOWN, how(8, 58), pal(0.0), sea(t=tg), fleet(tg, 0.6 * u), flagpole('red_cloth', 7, tg, 3.2, 2.0).xf(trans(FLAG_WORLD))]
    ms.append(sailor().mesh(tuple(tw + np.array([2.0, 0, 2.0])), math.pi * 1.2, dict(hp=0.1)))
    return merge(ms), cam, ENV_MORNING, {}


# ------------------------------------------------------------------ 7 : 9 h, feu
def shot_clock9(lt, dur, tg):
    cw = CLOCK_WORLD
    t902 = WT(7, '9') if False else None
    jump = WT(7, 'À') - S('clock9')
    minute = 0 if lt < jump else 2
    cam = Cam((cw[0] + 1.0, cw[1] - 1.5, cw[2] + 8), tuple(cw), 35 if lt < jump else 28)
    ms = [TOWN, how(9, minute), pal(0.0), flagpole('red_cloth', 7, tg, 3.2, 2.0).xf(trans(FLAG_WORLD))]
    return merge(ms), cam, ENV_MORNING, {}


def gun_flashes(lt, cam, period=0.7, seed=0, ships=(0, 1, 2, 3, 4)):
    """flash de lumière au bout de CHAQUE canon qui tire + fumée de poudre"""
    ms = []
    k_tot = 0
    for i in ships:
        kind, p = SHIPS[i]
        for j, tip in enumerate(barrel_tips(kind, p, 1.0)):
            ph = (lt + i * 0.23 + j * 0.37) % period
            k = max(0.0, 1 - ph / 0.15)
            size = 8 if kind == 'cruiser' else 5
            ms.append(muzzle(tip, k, cam, size))
            k_tot = max(k_tot, k)
            ms.append(smoke_sprites(tip, lt * 1.2 + i + j, cam, n=3, size=size * 0.6, rise=4, seed=10 + i * 3 + j, col=(220, 220, 215), drift=(0.3, 0, -0.8), alpha=0.6))
    return merge(ms), k_tot


def shot_fire(lt, dur, tg):
    cam = cam_lerp(Cam((48, 8, 105), (14, 4, 30), 55), Cam((45, 7.5, 100), (14, 4, 30), 55), lt / dur)
    ms = harbor_scene(tg, cam, 9, 2, gun_yaw=-0.7, show_def=False)
    fl, k = gun_flashes(lt, cam)
    ms.append(fl)
    for j in range(6):
        ms.append(explosion(PAL_POS + np.array([-10 + j * 4, 6 + (j % 3) * 3, 7]), lt - 0.4 - j * 0.45, cam, 5, 20 + j))
    env = ENV_MORNING.copy(points=[(tuple(SHIPS[0][1] + np.array([0, 5, -5])), (255, 200, 120), 1.2 * k, 30)])
    return merge(ms), cam, env, {}


# ------------------------------------------------------------------ 8 : palais en feu, yacht coulé
def shot_burn(lt, dur, tg):
    cam = cam_lerp(Cam((PAL_POS[0] + 25, 6, 30), (PAL_POS[0], 9, -12), 55), Cam((PAL_POS[0] + 20, 7, 25), (PAL_POS[0], 10, -12), 55), lt / dur)
    burn = min(1.0, 0.3 + lt / dur)
    ms = [TOWN, how(9, 10), pal(burn), sea(t=tg), flagpole('red_cloth', 7, tg, 3.2, 2.0).xf(trans(FLAG_WORLD)), barricade(14, 1).xf(trans(PAL_POS[0], 0, -6.5))]
    for k, dx in enumerate((-9, -3, 3, 9)):
        ms.append(fire_sprites(PAL_POS + np.array([dx, 9 + (k % 2) * 3, 7.6]), tg + k, cam, 7, 2.6, 2.5, 30 + k))
        ms.append(fire_sprites(PAL_POS + np.array([dx, 2 + (k % 2) * 2, 7.4]), tg + k * 2, cam, 5, 2.0, 2, 40 + k))
    ms.append(big_smoke(PAL_POS + np.array([0, 13, 0]), tg, cam, 12, 8, 30, 3))
    for j in range(3):
        ms.append(explosion(PAL_POS + np.array([-6 + j * 6, 5 + j * 2, 7]), lt - 0.3 - j * 0.9, cam, 5, 50 + j))
    env = ENV_SMOKE.copy(points=[(tuple(PAL_POS + np.array([0, 8, 10])), (255, 140, 60), 1.2, 30)])
    return merge(ms), cam, env, {}


def shot_yacht(lt, dur, tg):
    th = 0.4
    d = max(0, lt - th)
    tilt = min(0.35, d * 0.25)
    sink = d * 1.6
    cam = cam_lerp(Cam((YACHT_POS[0] + 50, 9, YACHT_POS[2] + 40), tuple(YACHT_POS + np.array([0, 3, 0])), 50),
                   Cam((YACHT_POS[0] + 44, 8, YACHT_POS[2] + 34), tuple(YACHT_POS + np.array([0, 2, 0])), 50), lt / dur)
    ms = [TOWN, how(9, 15), pal(0.7), sea(t=tg), fleet(tg, -0.4)]
    ms.append(yacht(tg, tilt, sink).xf(M(trans(YACHT_POS), roty(math.pi * 0.95))))
    ms.append(explosion(YACHT_POS + np.array([0, 4, 0]), lt - th, cam, 6, 61))
    ms.append(explosion(YACHT_POS + np.array([12, 3, 2]), lt - th - 0.8, cam, 5, 62))
    if d > 0:
        ms.append(fire_sprites(YACHT_POS + np.array([0, 5 - sink, 0]), tg, cam, 6, 2.5, 3, 63))
        ms.append(big_smoke(YACHT_POS + np.array([0, 6 - sink, 0]), tg, cam, 8, 5, 18, 64, (60, 58, 55)))
        # écume
        for i in range(10):
            ph = (lt * 1.5 + i * 0.1) % 1
            ms.append(billboard(YACHT_POS + np.array([math.cos(i) * 30 * ph * 0.3 + (i - 5) * 5, 0.5, math.sin(i * 2) * 3]), 2.5, 1.5 * (1 - ph), cam,
                                (240, 245, 245), 'puff', emis=0.5, alpha=0.8 * (1 - ph)))
    return merge(ms), cam, ENV_SMOKE, {}


# ------------------------------------------------------------------ 9 : fuite
def street():
    ms = [grid(-30, -30, 30, 30, 6, 6, None, (255, 255, 255), 'dirt', 2.5)]
    rr = np.random.default_rng(9)
    cols = [(240, 232, 210), (230, 215, 185), (220, 200, 165), (245, 240, 228)]
    for i, z in enumerate(range(-24, 24, 9)):
        ms.append(stone_house(8, 8, 9.9, cols[i % 4], i).xf(M(trans(-7.5, 0, z), roty(math.pi / 2))))
        ms.append(stone_house(8, 8, 13.2, cols[(i + 2) % 4], i + 20).xf(M(trans(7.5, 0, z + 4), roty(-math.pi / 2))))
    return merge(ms)


STREET = street()


def shot_flee(lt, dur, tg):
    """Khalid s'enfuit par la porte du palais en flammes et longe le front de mer"""
    door = PAL_POS + np.array([0, 0, 7.4])
    u = lt / dur
    p = door + np.array([u * 22.0, 0, 2.5 * min(1, u * 4)])
    cam = Cam((p[0] + 6.0, 2.2, p[2] + 6.5), (p[0] - 2.0, 2.4, p[2] - 2.5), 58)
    ms = [TOWN, how(9, 20), pal(0.8), sea(t=tg), barricade(16, 1).xf(trans(PAL_POS[0], 0, -6.5))]
    ms.append(khalid('khalid_shout').mesh(tuple(p), math.pi / 2 - 0.2, run_pose(lt * 11)))
    for i, (dx, dz) in enumerate(((-1.4, 0.8), (-2.4, -0.6), (-3.2, 0.5))):
        ms.append(askari('askari' if i % 2 else 'askari2').mesh(tuple(p + np.array([dx, 0, dz])), math.pi / 2 - 0.2,
                                                                 run_pose(lt * 11 + i, hand_r=rifle().xf(rotx(-1.0)))))
    for k, dx in enumerate((-9, -3, 3, 9)):
        ms.append(fire_sprites(PAL_POS + np.array([dx, 9 + (k % 2) * 3, 7.6]), tg + k, cam, 6, 2.4, 2.5, 30 + k))
    ms.append(big_smoke(PAL_POS + np.array([0, 13, 0]), tg, cam, 10, 7, 25, 3))
    env = ENV_SMOKE.copy(points=[(tuple(PAL_POS + np.array([0, 8, 10])), (255, 140, 60), 1.0, 30)])
    return merge(ms), cam, env, {}


def shot_consulate(lt, dur, tg):
    g = GER_POS
    cam = cam_lerp(Cam((g[0] + 9, 2.2, g[2] + 22), (g[0], 5.5, g[2] + 4), 58), Cam((g[0] + 7, 2.1, g[2] + 19), (g[0], 5.8, g[2] + 4), 58), lt / dur)
    u = min(1, lt / (dur * 0.75))
    z = g[2] + 18 - u * 12.5
    ms = [TOWN_BASE, german_consulate(tg, gate=min(1.0, max(0.0, (u - 0.45) / 0.3))).xf(trans(g))]
    if u < 1:
        ms.append(khalid('khalid_shout').mesh((g[0], 0, z), math.pi, run_pose(lt * 11)))
    # deux marins allemands gardent le portail
    for s in (-1, 1):
        ms.append(sailor().mesh((g[0] + s * 2.7, 0, g[2] + 9.8), 0.0, dict(hand_r=rifle().xf(rotx(-1.5)), ra=(0.2, 0.0, 0.2))))
    ms.append(big_smoke((g[0] - 60, 15, -10), tg, cam, 8, 10, 20, 9))
    return merge(ms), cam, ENV_SMOKE, {}


# ------------------------------------------------------------------ 10 : le drapeau tombe
def shot_flag(lt, dur, tg):
    th = 0.6
    fw = FLAG_WORLD
    cam = Cam((fw[0] + 10, fw[1] + 2, fw[2] + 22), (fw[0], fw[1] + 4, fw[2]), 45)
    ms = [TOWN, pal(0.9), sea(t=tg)]
    fp = flagpole('red_cloth', 7, tg, 3.2, 2.0)
    if lt < th:
        ms.append(fp.xf(trans(fw)))
    else:
        d = lt - th
        ang = min(math.pi / 2 * 0.95, d * d * 3.0)
        ms.append(fp.xf(M(trans(fw), rotz(-ang))))
    ms.append(explosion(fw + np.array([0, 3.0, 0]), lt - th, cam, 3, 71))
    ms.append(big_smoke(PAL_POS + np.array([0, 13, 0]), tg, cam, 10, 7, 25, 3))
    for k, dx in enumerate((-9, -3, 3, 9)):
        ms.append(fire_sprites(PAL_POS + np.array([dx, 10, 7.6]), tg + k, cam, 5, 2.4, 2.5, 30 + k))
    return merge(ms), cam, ENV_SMOKE, {}


def shot_clock940(lt, dur, tg):
    cw = CLOCK_WORLD
    cam = cam_lerp(Cam((cw[0] + 1.0, cw[1] - 1.5, cw[2] + 8), tuple(cw), 30), Cam((cw[0] + 1.0, cw[1] - 1.8, cw[2] + 10), tuple(cw), 32), lt / dur)
    ms = [TOWN, how(9, 40), pal(0.9)]
    ms.append(big_smoke(PAL_POS + np.array([0, 13, 0]), tg, cam, 8, 7, 25, 3, alpha=0.5))
    return merge(ms), cam, ENV_SMOKE, {}


# ------------------------------------------------------------------ 11 : bilan
def shot_ruins(lt, dur, tg):
    cam = cam_lerp(Cam((PAL_POS[0] - 8, 4, 22), (PAL_POS[0], 6, -12), 55), Cam((PAL_POS[0] - 4, 5, 20), (PAL_POS[0], 7, -12), 55), lt / dur)
    ms = [TOWN, how(10, 0), pal(1.0), sea(t=tg), barricade(14, 1).xf(trans(PAL_POS[0], 0, -6.5))]
    rr = np.random.default_rng(5)
    for i in range(25):
        ms.append(box(rr.uniform(0.5, 1.5), rr.uniform(0.3, 0.8), rr.uniform(0.5, 1.5), (90, 80, 70), 'scorch').xf(M(trans(PAL_POS[0] + rr.uniform(-12, 12), 0, -10.5 + rr.uniform(-1, 2)), roty(rr.random() * 3))))
    ms.append(big_smoke(PAL_POS + np.array([0, 8, 0]), tg, cam, 10, 7, 25, 3, alpha=0.6))
    for k, dx in enumerate((-8, 5)):
        ms.append(fire_sprites(PAL_POS + np.array([dx, 1, 7.5]), tg + k, cam, 4, 1.4, 2, 80 + k))
    return merge(ms), cam, ENV_SMOKE.copy(sky_hor=(170, 160, 150)), {}


def shot_wounded(lt, dur, tg):
    p = SHIPS[3][1]
    L, B, H = WARSHIP_DIMS['cruiser']
    deck = p + np.array([-L * 0.19, H * 0.4, -3.0])
    cam = cam_lerp(Cam((deck[0] - 0.4, deck[1] + 1.6, deck[2] + 3.6), (deck[0] + 0.6, deck[1] + 0.9, deck[2] + 0.2), 50),
                   Cam((deck[0] - 0.3, deck[1] + 1.55, deck[2] + 3.2), (deck[0] + 0.6, deck[1] + 0.9, deck[2] + 0.2), 50), lt / dur)
    ms = [TOWN, sea(t=tg), fleet(tg, -0.7)]
    bandage = box(0.13, 0.12, 0.14, (250, 250, 248))
    ms.append(sailor('sailor_ow').mesh(tuple(deck), -0.5, sit_pose(drop=0.45, la=(1.0, 0.3, 1.6), ra=(0.6, 0.1, 0.8))))
    at = sailor().attach if False else None
    ms.append(box(0.15, 0.25, 0.16, (250, 250, 248)).xf(trans(deck[0] + 0.25, deck[1] + 0.95, deck[2] + 0.1)))
    ms.append(box(0.6, 0.45, 0.6, (120, 90, 60), 'planks').xf(trans(deck[0], deck[1], deck[2] - 0.1)))
    ms.append(sailor().mesh((deck[0] + 1.2, deck[1], deck[2] + 0.6), -1.7, dict(la=(0.6, 0.0, 1.0), hp=0.3)))
    return merge(ms), cam, ENV_SMOKE.copy(sky_hor=(200, 190, 175)), {}


# ------------------------------------------------------------------ 12 : la facture
def bill_table():
    ms = [box(4, 0.08, 2.0, (90, 60, 35), 'wood_dark').xf(trans(0, 0.8, 0)), box(10, 0.05, 10, (150, 110, 70), 'planks').xf(trans(0, -0.05, 0)),
          box(10, 4, 0.1, (220, 215, 200), 'plaster', faces='f').xf(trans(0, 0, -3.0))]
    ms.append(box(0.7, 0.03, 0.5, (255, 255, 255), 'ledger').xf(trans(0.6, 0.88, 0.1)))
    ms.append(box(1.4, 1.0, 0.04, (255, 255, 255), 'union_jack').xf(trans(1.6, 2.0, -2.94)))
    # douilles d'obus
    for i in range(4):
        ms.append(cyl(0.08, 0.08, 0.45, 8, (200, 170, 70), 'metal').xf(trans(-1.4 + i * 0.22, 0.84, -0.4)))
        ms.append(cyl(0.075, 0.0, 0.18, 8, (110, 110, 115), 'metal').xf(trans(-1.4 + i * 0.22, 1.29, -0.4)))
    return merge(ms)


BILL = bill_table()


def shot_bill(lt, dur, tg):
    u = min(1, lt / (dur * 0.8))
    cam = cam_lerp(Cam((2.4, 2.0, 1.2), (-0.3, 0.95, 0.0), 50), Cam((2.1, 1.9, 1.0), (-0.3, 0.95, 0.0), 50), lt / dur)
    ms = [BILL]
    ms.append(box(0.36, 0.004, 0.48, (255, 255, 255), 'facture').xf(trans(0.15, 0.882, 0.0)))
    n = int(6 + u * 30)
    for i in range(n):
        col = i % 6
        ms.append(cyl(0.04, 0.04, 0.012, 8, (210, 210, 215), 'metal').xf(trans(-0.6 + col * 0.1 - (1 - u) * 0.8 * (i > n - 6), 0.882 + (i // 6) * 0.013, 0.35)))
    ms.append(civilian().mesh((-0.3, 0, 1.0), math.pi, dict(ra=(1.2, 0.0, 0.3), la=(1.2, 0.0, 0.3), hp=0.4)))
    ms.append(consul('cave').mesh((0.3, 0, -1.0), 0.0, dict(ik_r=(0.2, 0.92, -0.05), hp=0.4, hat=False)))
    return merge(ms), cam, ENV_ROOM.copy(points=[((0, 3, 0), (255, 240, 210), 0.6, 6)]), {}


# ------------------------------------------------------------------ 13 : fin
def shot_end(lt, dur, tg):
    cam = cam_lerp(Cam((30, 12, 70), (5, 8, -15), 55), Cam((40, 18, 95), (5, 8, -15), 55), lt / dur)
    ms = harbor_scene(tg, cam, 10, 0, burn=1.0, yacht_state=None, flag_up=False, gun_yaw=-0.7, show_def=False)
    ms.append(big_smoke(PAL_POS + np.array([0, 10, 0]), tg, cam, 10, 7, 25, 3, alpha=0.6))
    return merge(ms), cam, ENV_SUNSET, dict(fade=max(0, (lt - dur + 0.4) / 0.4))


# ------------------------------------------------------------------ montage
add('hook', 0.0, shot_hook)
add('watch', WT(0, '38') - 0.1, shot_watch)
add('island', T(1), shot_island)
add('town', WT(1, 'sous') - 0.1, shot_town)
add('sultan', T(2), shot_sultan)
add('khalid_door', WT(2, 'Certains') - 0.1, shot_khalid_door)
add('throne', T(3), shot_throne)
add('consul', WT(3, 'Problème') - 0.1, shot_consul)
add('ultimatum', T(4), shot_ultimatum)
add('clock8', WT(4, 'avant') - 0.1, shot_clock8)
add('threat', WT(4, 'sinon,') - 0.1, shot_threat)
add('refuse', T(5), shot_refuse)
add('defenders', WT(5, 'Près') - 0.1, shot_defenders)
add('fleet', T(6), shot_fleet)
add('gun_close', WT(6, 'pointent') - 0.2, shot_gun_close)
add('clock9', T(7), shot_clock9)
add('fire', WT(7, 'les') - 0.15, shot_fire)
add('burn', T(8), shot_burn)
add('yacht', WT(8, 'yacht') - 0.3, shot_yacht)
add('flee', T(9), shot_flee)
add('consulate', WT(9, 'réfugie') - 0.2, shot_consulate)
add('flag', T(10), shot_flag)
add('clock940', WT(10, 'La') - 0.1, shot_clock940)
add('ruins', T(11), shot_ruins)
add('wounded', T(11, 7) - 0.1, shot_wounded)
add('bill', T(12), shot_bill)
add('end', T(13), shot_end)

subs = Subs(timing)


def build_audio(path):
    mx = A.Mixer(tl.duration())
    dur = tl.duration()
    mx.add(A.waves(12), 0, 0.25, length=dur)
    mx.add(A.gulls(8), S('island'), 0.4, 0.3, 0.3, length=S('sultan') - S('island'))
    for k, te in enumerate((0.3, 1.1, 1.9, 2.7, 3.4)):
        mx.add(A.explosion(2.5), te, 0.6)
        mx.add(A.cannon(2), te - 0.25, 0.45)
    mx.add(A.fire_crackle(6), 0, 0.3, length=S('watch'))
    for i in range(int((S('island') - S('watch')) / 0.1)):
        mx.add(A.tick(), S('watch') + i * 0.1, 0.25)
    mx.add(A.tick(), S('sultan') + 0.3, 0.15)
    mx.add(A.crowd(5), S('throne'), 0.25, 0.3, 0.3, length=S('consul') - S('throne'))
    mx.add(A.bell(2.5, 330), S('clock8') + 0.3, 0.4)
    mx.add(A.crowd(6), S('defenders'), 0.4, 0.3, 0.3, length=S('fleet') - S('defenders'))
    mx.add(A.ratchet(1.5), S('fleet') + 0.5, 0.3)
    mx.add(A.ratchet(1.2), S('gun_close') + 0.2, 0.4)
    for i in range(9):
        mx.add(A.bell(2.0, 392), S('clock9') + 0.1 + i * 0.08 * 0, 0.0)
    mx.add(A.bell(3.0, 392), S('clock9') + 0.2, 0.5)
    mx.add(A.tick(), WT(7, 'Rien'), 0.4)
    mx.add(A.tick(), WT(7, 'bouge.'), 0.4)
    for i in range(int((S('burn') - S('fire')) / 0.7) + 1):
        for j in range(3):
            mx.add(A.cannon(2), S('fire') + i * 0.7 + j * 0.23, 0.45)
    for j in range(6):
        mx.add(A.explosion(2), S('fire') + 0.4 + j * 0.45, 0.4)
    mx.add(A.fire_crackle(8), S('burn'), 0.55, 0.2, 0.4, length=S('flee') - S('burn'))
    for j in range(3):
        mx.add(A.explosion(2.5), S('burn') + 0.3 + j * 0.9, 0.5)
    mx.add(A.explosion(3), S('yacht') + 0.4, 0.7)
    mx.add(A.explosion(3), S('yacht') + 1.2, 0.5)
    mx.add(A.splash(1.5), S('yacht') + 1.5, 0.6)
    mx.add(A.footsteps(5, 6), S('flee'), 0.5, length=S('flag') - S('flee') - 0.5)
    mx.add(A.cannon(2), S('flee') + 0.5, 0.25)
    mx.add(A.cannon(2), S('flee') + 1.6, 0.25)
    mx.add(A.thwack(), S('consulate') + (S('flag') - S('consulate')) * 0.75, 0.4)
    mx.add(A.explosion(2), S('flag') + 0.6, 0.6)
    mx.add(A.splinter(), S('flag') + 0.7, 0.5)
    mx.add(A.bell(3.0, 392), S('clock940') + 0.2, 0.4)
    mx.add(A.fire_crackle(6), S('ruins'), 0.35, 0.3, 0.3, length=S('bill') - S('ruins'))
    for i in range(8):
        mx.add(A.clank(0.15), S('bill') + 0.3 + i * 0.5, 0.2)
    mx.add(A.waves(5), S('end'), 0.3, length=dur - S('end'))
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
        contact_sheet(tl, times[:39], os.path.join(HERE, 'sheet1.png'), subs, cols=6, scale=0.18)
        contact_sheet(tl, times[39:], os.path.join(HERE, 'sheet2.png'), subs, cols=6, scale=0.18)
    elif len(sys.argv) > 1 and sys.argv[1] == '--at':
        for s in sys.argv[2:]:
            frame(tl, float(s), subs).resize((540, 960)).save(os.path.join(HERE, f'at_{s}.png'))
    else:
        build_audio(os.path.join(HERE, 'sfx.wav'))
        mix_voice(os.path.join(HERE, 'voix.wav'), os.path.join(HERE, 'sfx.wav'), os.path.join(HERE, 'mix.wav'))
        render_video(tl, os.path.join(HERE, 'zanzibar.mp4'), os.path.join(HERE, 'mix.wav'), subs)
