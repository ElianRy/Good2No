"""Vidéo : Violet Jessop, la survivante des trois paquebots."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n', '/home/claude/g2n/violet']
import numpy as np
from world import *
from video_core import *
from scripts import VIOLET as LINES
import audio as A
import common2 as C2

HERE = '/home/claude/g2n/violet'
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


def nxt(name):
    ts = sorted(SHOT_STARTS.values())
    i = ts.index(SHOT_STARTS[name])
    return ts[i + 1] if i + 1 < len(ts) else tl.duration()


# ------------------------------------------------------------------ éléments communs
L_OLY = liner('olympic')
L_OLY_GASH = liner('olympic', gash=True)
L_TIT_DAY = liner('titanic')
L_TIT_NIGHT = liner('titanic', lights=1.0)
L_TIT_DARK = liner('titanic', lights=0.0)
L_BRIT = liner('britannic')
HAWKE = hawke()
ICEBERG = iceberg()
FLOES = ice_floes(40, 4, 260)
CORR = corridor()
QUAY = quay_set()
COTTAGE = cottage()
CEMETERY = cemetery()
DECK_DAY = deck_set('olympic')
DECK_NIGHT = deck_set('titanic', night=True)
DECK_BRIT = deck_set('britannic')
BOAT = lifeboat_mesh(8.5, 2.4, 1.1)
TUG = tug()

V_STEW = violet()
V_STEW_S = violet('violet_smile')
V_STEW_SH = violet('violet_shock')
V_COAT = violet('violet', 'coat')
V_COAT_SH = violet('violet_shock', 'coat')
V_COAT_C = violet('violet_closed', 'coat')
V_NURSE = violet('violet', 'nurse')
V_NURSE_SH = violet('violet_shout', 'nurse')
V_NURSE_SHOCK = violet('violet_shock', 'nurse')
V_NURSE_C = violet('violet_closed', 'nurse')
V_OLD = violet('violet_old', 'old')
V_OLD_SH = violet('violet_old_shock', 'old')
OFFICER = officer()
PASS = [passenger(i) for i in range(4)]
PASS_NB = [passenger(i, belt=False) for i in range(4)]
SOLDIER = soldier()
SOLDIER_H = soldier('soldier_hurt')

_LINER_CACHE = {}


def sinking_matrix(pitch, sink, roll=0.0):
    """navire qui sombre par la proue (+x) ; pitch en radians, sink en mètres"""
    return M(trans(0, -sink, 0), rotx(roll), rotz(-pitch))


def wake(t, cam, L=262, k=1.0):
    """écume derrière la poupe et le long des flancs"""
    if k <= 0:
        return Mesh()
    ms = []
    for i in range(14):
        ph = (t * 0.6 + i / 14) % 1.0
        x = -L / 2 - ph * 160
        w = 14 + ph * 50
        ms.append(quad((x - 6, 0.15, -w / 2), (x + 6, 0.15, -w / 2), (x + 6, 0.15, w / 2), (x - 6, 0.15, w / 2), (240, 245, 245), 'puff',
                       ((0, 0), (1, 0), (1, 1), (0, 1)), emis=0.3, alpha=0.45 * (1 - ph) * k))
    for s in (-1, 1):
        for i in range(6):
            ph = (t * 1.2 + i / 6) % 1.0
            x = L / 2 - 8 - ph * 40
            ms.append(billboard((x, 1.0, s * (14 + ph * 6)), 8, 3, cam, (240, 248, 250), 'puff', emis=0.4, alpha=0.6 * (1 - ph) * k))
    return merge(ms)


def lit_env(env, pts):
    return env.copy(points=list(env.points) + list(pts))


def carpathia(lights=True):
    st = [(-80, 7, 4), (60, 8, 6), (78, 0.5, 0.3)]
    ms = [C2_hull(st)]
    ms.append(box(70, 6, 13, (255, 255, 255), 'superwin_lit' if lights else 'superwin', ts=3).xf(trans(-5, 12, 0)))
    ms.append(cyl(3, 3, 16, 10, (200, 60, 30)).xf(trans(-5, 18, 0)))
    ms.append(cyl(3.05, 3.05, 3, 10, (20, 20, 20)).xf(trans(-5, 31, 0)))
    for mx in (50, -60):
        ms.append(cyl(0.4, 0.2, 35, 5, (180, 150, 100)).xf(trans(mx, 12, 0)))
    if lights:
        ms.append(box(0.8, 0.8, 0.8, (255, 255, 230), emis=1.0).xf(trans(50, 46, 0)))
    return merge(ms)


def C2_hull(st):
    from world import _hull_bands
    return _hull_bands(st, [(-7, 2.0), (2.0, 12.0)], lambda b: 'hull_black' if b == 0 else 'ports_lit', ts=4.0, emis=0.6)


CARPATHIA = carpathia()


# ------------------------------------------------------------------ 0 : accroche
def shot_hook(lt, dur, tg):
    """le Titanic sombre, la poupe se dresse ; caméra qui fonce au ras de l'eau"""
    pitch = 0.3 + lt * 0.03
    Ms = sinking_matrix(pitch, 6 + lt * 2)
    flick = 1.0 if (int(lt * 12) % 5) else 0.0
    ship = (L_TIT_NIGHT if flick else L_TIT_DARK).xf(Ms)
    u = ease(lt / max(dur, 0.1))
    cam = Cam(lerpv((-215, 4, 120), (-165, 7, 85), u), (-70, 28, 0), 56)
    cam = C2.shake(cam, 0.6, tg)
    stern = (Ms @ np.array([-128, 0, 0, 1]))[:3]
    ms = [ship, sea(tg, 'sea_night'), STARS, flare((40, 30, 0), lt - 0.1, cam), flare((-20, 30, 10), lt - 0.9, cam)]
    ms.append(C2.particles(stern + np.array([0, -10, 0]), tg, cam, n=30, area=(20, 20, 10), fall=-3, size=1.2, col=(220, 230, 240), seed=3, alpha=0.5))
    env = ENV_NIGHT_SEA.copy(points=[((20, 60, 0), (255, 250, 230), 1.4 * max(0, 1 - abs(lt - 0.9) * 2), 260)])
    return merge(ms), cam, env, {}


def ram_scene(lt, t_hit, tg, cam_mode='close'):
    """le Hawke (gris) arrive par tribord et enfonce de l'étrave le flanc arrière de l'Olympic, au niveau de la brèche (x=-92)"""
    z_hit = 14.0
    hit = lt >= t_hit
    approach = 18.0
    if not hit:
        z = z_hit + approach * (1 - ease(min(1.0, lt / max(t_hit, 0.01))) * 0.0) - approach * min(1.0, lt / max(t_hit, 0.01))
    else:
        z = z_hit - min(lt - t_hit, 0.25) * 2.0
    # étrave (x local 55) placée exactement sur la brèche
    Hm = M(trans(-92.0 + 13.75, 0, z + 53.35), roty(math.pi / 2 + 0.25))
    ms = [(L_OLY_GASH if hit else L_OLY), HAWKE.xf(Hm), sea(tg, 'sea_day')]
    return ms


def shot_hook_crash(lt, dur, tg):
    t_hit = 0.15
    cam = Cam((-160, 20, 44), (-95, 2, 18), 46)
    k = C2.decay(lt, t_hit, 4)
    cam = C2.shake(cam, 1.6 * k, tg)
    ms = ram_scene(lt, t_hit, tg) + [impact_fx(lt, t_hit, cam)]
    return merge(ms), cam, ENV_GREY_SEA, dict(flash=0.8 * C2.decay(lt, t_hit, 10))


def shot_hook_mine(lt, dur, tg):
    cam = C2.punch(Cam((260, 20, 210), (60, 18, 0), 45), lt, 0.3, 0.8)
    k = C2.decay(lt, 0.1, 3)
    cam = C2.shake(cam, 1.4 * k, tg)
    ms = [L_BRIT.xf(sinking_matrix(0.02 * lt, lt * 0.5)), sea(tg, 'sea_aegean'), water_column((112, 0, 18), lt - 0.08, cam, 70, 1)]
    ms.append(explosion((112, 8, 16), lt - 0.08, cam, 16, 3) if False else Mesh())
    return merge(ms), cam, ENV_AEGEAN, dict(flash=0.7 * C2.decay(lt, 0.08, 9))


# ------------------------------------------------------------------ 1 : Violet
def shot_intro(lt, dur, tg):
    """Violet marche vers nous sur le pont-promenade de l'Olympic, plateau en main, sourire"""
    z = 1.2
    x = 6.0 - lt * 1.1
    tr = tray().xf(M(rotx(-math.pi / 2), trans(0, 0.04, 0)))
    pose = walk_pose(lt * 6.0, 0.7, face='violet_smile')
    v = V_STEW_S.mesh((x, 0, z), -math.pi / 2, pose)
    cam = Cam((x - 2.8, 1.55, z + 0.6), (x, 1.35, z), 50)
    ms = [DECK_DAY, v, sea(tg, 'sea_day', y=-22)]
    for i, (px, pz, yaw) in enumerate(((-6, -2.6, 0.3), (-10, 2.6, 2.6))):
        ms.append(PASS_NB[i].mesh((px, 0, pz), yaw, dict(hp=0.1)))
    return merge(ms), cam, ENV_DAY_SEA, {}


def shot_intro_wide(lt, dur, tg):
    u = lt / max(dur, 0.1)
    a = 0.6 + u * 0.35
    cam = Cam((math.cos(a) * 330, 70 - u * 15, math.sin(a) * 330), (0, 20, 0), 45)
    Ms = np.eye(4)
    ms = [L_OLY, sea(tg, 'sea_day'), wake(tg, cam), funnel_smoke(Ms, tg, cam)]
    return merge(ms), cam, ENV_DAY_SEA, {}


# ------------------------------------------------------------------ 2 : Olympic 1911
CONTACT = np.array([-92.0, 1.5, 14.6])


def shot_southampton(lt, dur, tg):
    """l'Olympic quitte le quai de Southampton, remorqueurs, coup de sirène"""
    x = -lt * 3.0
    Ms = M(trans(x, 0, 45), roty(math.pi))
    cam = cam_lerp(Cam((-160, 8, -30), (0, 25, 45), 55), Cam((-150, 9, -26), (-10, 25, 45), 55), lt / dur)
    ms = [QUAY, L_OLY.xf(Ms), sea(tg, 'sea_day', y=-1.3), funnel_smoke(Ms, tg, cam, col=(60, 58, 55)),
          TUG.xf(M(trans(-150 + x, -1.3, 30), roty(math.pi + 0.2))), TUG.xf(M(trans(140 + x, -1.3, 75), roty(0.3)))]
    for i in range(8):
        ms.append(PASS_NB[i % 4].mesh((-170 + i * 3.5, 0, -3 - (i % 3)), math.pi * 0.55, dict(ra=(2.8, 0.3, 0.2) if i % 2 else (0, 0.1, 0.2))))
    return merge(ms), cam, ENV_GREY_SEA, {}


def shot_twins(lt, dur, tg):
    """les jumeaux côte à côte : plan large en hauteur, la caméra glisse le long des deux coques"""
    u = ease(lt / max(dur, 0.1))
    cam = Cam((lerp(330, 270, u), 95, lerp(260, 220, u)), (0, 10, 0), 48)
    ms = [L_OLY.xf(trans(0, 0, -36)), L_TIT_DAY.xf(trans(0, 0, 36)), sea(tg, 'sea_day'),
          funnel_smoke(trans(0, 0, -36), tg, cam), funnel_smoke(trans(0, 0, 36), tg, cam)]
    return merge(ms), cam, ENV_DAY_SEA, {}


# ------------------------------------------------------------------ 3 : la collision
def shot_wave(lt, dur, tg):
    """Violet salue du pont (bastingage), vue depuis l'extérieur"""
    v = V_STEW_S.mesh((0, 0, 3.6), 0.0, dict(ra=(2.7 + 0.25 * math.sin(lt * 9), 0.35, 0.3), la=(0.1, 0.1, 0.4), face='violet_smile'))
    cam = Cam((1.6, 1.6, 8.0), (0, 1.5, 3.6), 45)
    cam = cam_lerp(cam, Cam((1.2, 1.55, 6.8), (0, 1.5, 3.6), 42), lt / dur)
    ms = [DECK_DAY, v, PASS_NB[1].mesh((-1.4, 0, 3.5), 0.1, dict(ra=(2.6 + 0.3 * math.sin(lt * 8 + 1), 0.3, 0.2))),
          PASS_NB[0].mesh((1.5, 0, 3.4), -0.1, {}), sea(tg, 'sea_day', y=-22)]
    return merge(ms), cam, ENV_GREY_SEA, {}


def impact_fx(lt, t_hit, cam):
    a = lt - t_hit
    ms = []
    if a < 0:
        return Mesh()
    ms.append(splash_fx(CONTACT + np.array([0, -0.5, 1.0]), a, cam, 7, 1))
    ms.append(splash_fx(CONTACT + np.array([-4, -0.5, 1.5]), a - 0.12, cam, 5, 2))
    if a < 0.35:  # gerbe d'étincelles au point de contact
        k = 1 - a / 0.35
        ms.append(billboard(CONTACT, 9 * k, 9 * k, cam, (255, 255, 255), 'spark', emis=1.0, alpha=k))
    rr = np.random.default_rng(3)
    for i in range(12):  # éclats de tôle
        v = rr.normal(size=3) * np.array([4, 3, 3]) + np.array([0, 9, 6])
        p = CONTACT + v * a + np.array([0, -4.9 * a * a, 0])
        if p[1] > -0.5:
            ms.append(box(0.7, 0.25, 0.5, (40, 40, 44), 'metal').xf(M(trans(p), rotx(a * 9 + i), rotz(a * 5))))
    return merge(ms)


def shot_ram(lt, dur, tg):
    """vue en hauteur sur l'arrière : on voit l'étrave grise arriver et percuter le flanc"""
    t_hit = min(0.7, dur * 0.4)
    cam = Cam((-165, 22, 46), (-95, 2, 18), 46)
    k = C2.decay(lt, t_hit, 3)
    cam = C2.shake(cam, 1.4 * k, tg)
    ms = ram_scene(lt, t_hit, tg) + [impact_fx(lt, t_hit, cam)]
    return merge(ms), cam, ENV_GREY_SEA, dict(flash=0.7 * C2.decay(lt, t_hit, 9))


def shot_ram_wide(lt, dur, tg):
    cam = cam_lerp(Cam((-60, 14, 75), (-92, 2, 14), 42), Cam((-68, 12, 66), (-92, 2, 14), 42), lt / dur)
    cam = C2.shake(cam, 0.5 * C2.decay(lt, 0, 2), tg)
    ms = ram_scene(10, 0, tg)
    ms.append(splash_fx(CONTACT + np.array([0, -0.5, 1.0]), (lt * 0.8) % 1.4, cam, 3, 5))
    return merge(ms), cam, ENV_GREY_SEA, {}


# ------------------------------------------------------------------ 4 : personne ne meurt
def shot_corridor(lt, dur, tg):
    """dans la coursive, Violet se relève, tasses au sol ; un collègue l'aide"""
    u = min(1.0, lt / (dur * 0.7))
    k = ease(u)
    pose = dict(ll=(-0.1 * (1 - k), 1.57 * (1 - k)), rl=(-0.1 * (1 - k), 1.57 * (1 - k)), drop=0.46 * (1 - k), lean=0.3 * (1 - k),
                la=(0.6 * (1 - k), 0.2, 0.6), ra=(0.6 * (1 - k), 0.2, 0.6), face='violet_shock' if u < 0.6 else 'violet')
    v = (V_STEW_SH if u < 0.6 else V_STEW).mesh((0, 0, 0), math.pi / 2, pose)
    cam = Cam((3.0, 1.3, 0.8), (0, 0.9, -0.2), 50)
    cam = C2.shake(cam, 0.06 * C2.decay(lt, 0, 2), tg)
    ms = [CORR, v, tray(0).xf(M(trans(0.7, 0.01, 0.4), roty(0.6)))]
    for i in range(3):
        ms.append(cyl(0.035, 0.03, 0.06, 6, (250, 250, 250)).xf(M(trans(0.9 + i * 0.25, 0.035, 0.2 - i * 0.15), rotz(math.pi / 2), roty(i))))
    ms.append(officer().mesh((-1.2, 0, 0.3), math.pi / 2, dict(la=(0.7, 0.1, 0.4), lean=0.2, hp=0.3)))
    return merge(ms), cam, ENV_CORR, {}


def shot_gash(lt, dur, tg):
    cam = cam_lerp(Cam((-80, 3, 45), (-92, -1, 14), 45), Cam((-84, 3, 38), (-92, -1, 14), 45), lt / dur)
    ms = [L_OLY_GASH, sea(tg, 'sea_day'), splash_fx((-92, 0.5, 15.5), (lt * 0.8) % 1.2, cam, 2, 5)]
    return merge(ms), cam, ENV_GREY_SEA, {}


# ------------------------------------------------------------------ 5 : Titanic au quai
def shot_dock(lt, dur, tg):
    """Violet marche sur le quai vers le Titanic, valise à la main ; la caméra lève les yeux vers les cheminées"""
    Ms = M(trans(0, 0, 18))
    u = lt / max(dur, 0.1)
    pos = np.array([-20.0, 0.0, -8.0 + lt * 1.1])
    v = V_STEW.mesh(tuple(pos), 0.0, walk_pose(lt * 5.5, 0.8, ra=(0.0, 0.12, 0.05), hand_r=suitcase().xf(M(trans(0, -0.2, 0)))))
    a = ease(u)
    cam = Cam((pos[0] + 0.9, 1.1, pos[2] - 3.2), (pos[0] - 0.3, 1.4 + 38 * a, 14), 62)
    ms = [QUAY, L_TIT_DAY.xf(Ms), v, sea(tg, 'sea_day', y=-1.2), funnel_smoke(Ms, tg, cam)]
    for i in range(4):
        ms.append(PASS_NB[i].mesh((pos[0] - 3 + i * 2.2, 0, -1.5 - (i % 2) * 2 + lt * 0.8), 0.15 * i, walk_pose(lt * 5 + i, 0.7)))
    return merge(ms), cam, ENV_GREY_SEA, {}


# ------------------------------------------------------------------ 6 : la nuit, l'iceberg
def shot_night(lt, dur, tg):
    u = lt / max(dur, 0.1)
    cam = Cam((300 - u * 40, 55, 230 - u * 30), (20, 15, 0), 42)
    ms = [L_TIT_NIGHT, sea(tg * 2, 'sea_night'), STARS, wake(tg, cam, k=0.6), funnel_smoke(np.eye(4), tg, cam, col=(30, 30, 34), alpha=0.6)]
    return merge(ms), cam, ENV_NIGHT_SEA, {}


def shot_iceberg(lt, dur, tg):
    """vue de haut et de côté : l'iceberg frotte contre l'étrave tribord ; grincements, glace qui tombe"""
    ix = 150 - lt * 12
    cam = Cam((230, 85, 150), (100, 5, 22), 42)
    cam = C2.shake(cam, 0.6 + 0.4 * math.sin(lt * 7) ** 2, tg)
    ms = [L_TIT_NIGHT, sea(tg, 'sea_night'), STARS, ICEBERG.xf(trans(ix, -4, 36))]
    for i in range(14):
        a = (lt * 1.3 + i / 14) % 1.0
        p = np.array([ix - 12 + i * 1.8, 22 - a * 22, 15.5 + a * 1.5])
        ms.append(box(1.0, 0.8, 0.9, (230, 245, 255), 'ice').xf(M(trans(p), rotx(a * 5 + i))))
    ms.append(splash_fx((ix - 6, 0.2, 15.5), (lt * 0.9) % 1.4, cam, 3.5, 6, (220, 235, 245)))
    return merge(ms), cam, ENV_NIGHT_SEA.copy(amb=0.55), {}


# ------------------------------------------------------------------ 7 : canots
def shot_boats(lt, dur, tg):
    """pont des embarcations la nuit : passagers en gilets, Violet guide une mère et son enfant"""
    v = V_COAT.mesh((-0.5 + lt * 0.5, 0, 1.4), math.pi / 2 - 0.4, dict(ra=(1.6, 0.4, 0.2), la=(0.3, 0.1, 0.5), hy=-0.4))
    ms = [DECK_NIGHT, v, sea(tg, 'sea_night', y=-22)]
    mom = PASS[1].mesh((0.6 + lt * 0.5, 0, 2.2), math.pi / 2 - 0.3, walk_pose(lt * 5, 0.6))
    kid = Human('pass_w', skin=(236, 200, 178), shirt=(120, 60, 60), pants=(60, 60, 70), height=0.6, extra=lifebelt_extra())
    ms += [mom, kid.mesh((1.1 + lt * 0.5, 0, 2.8), math.pi / 2 - 0.3, walk_pose(lt * 7, 0.6))]
    for i, (x, z, yaw) in enumerate(((-3, 0.5, 1.2), (-4.2, 1.8, 1.4), (3.5, 0.0, -1.6), (-6, 2.5, 1.0), (5.5, 1.5, -1.8))):
        ms.append(PASS[i % 4].mesh((x, 0, z), yaw, walk_pose(lt * 4 + i, 0.3)))
    ms.append(OFFICER.mesh((4.8, 0, 3.4), -2.2, dict(ra=(1.4, 0.3, 0.1), hp=-0.1)))
    cam = cam_lerp(Cam((6.5, 1.7, 0.6), (0, 1.1, 1.6), 55), Cam((5.8, 1.65, 0.7), (0.4, 1.1, 1.6), 52), lt / dur)
    return merge(ms), cam, ENV_NIGHT_SEA.copy(points=[((0, 2.6, -3.8), (255, 220, 150), 0.8, 9)]), {}


def boat_people(lt, n=5, seed=0, start=0):
    """passagers assis dans un canot (repère du canot : proue +x, origine au centre)"""
    ms = []
    seats = [(-2.4, -0.55), (-2.4, 0.55), (-0.6, -0.55), (-0.6, 0.55), (1.2, -0.55), (1.2, 0.55), (2.6, 0.0)]
    for i in range(min(n, len(seats) - start)):
        sx, sz = seats[(i + start) % len(seats)]
        ms.append(PASS[(i + seed) % 4].mesh((sx, -0.33, sz), math.pi / 2 if sz <= 0 else -math.pi / 2,
                                           sit_pose(drop=0.45, la=(0.8, 0.3, 1.6), ra=(0.8, 0.3, 1.6), hp=0.15)))
    return merge(ms)


def shot_lower(lt, dur, tg):
    """le canot 16 descend le long de la coque illuminée"""
    y = 12 - lt * 3.0
    bm = M(trans(-40, y, 15.3))
    ms = [L_TIT_NIGHT, sea(tg, 'sea_night'), STARS, BOAT.xf(bm), boat_people(lt, 5).xf(bm)]
    ms.append(V_COAT.mesh((0.0, -0.33, 0.0), math.pi / 2, sit_pose(drop=0.45, hp=-0.5, la=(0.8, 0.2, 1.4), ra=(0.8, 0.2, 1.4))).xf(M(bm, trans(2.6, 0, 0.1))))
    for dx in (-3.6, 3.6):
        ms.append(rod((-40 + dx, y + 0.5, 15.3), (-40 + dx, LINER_DECK + 9.5, 15.0), 0.03, (200, 190, 160), n=3))
    cam = Cam((-20, y + 3.0, 32), (-40, y + 1.0, 15), 50)
    return merge(ms), cam, ENV_NIGHT_SEA.copy(points=[((-40, y + 6, 18), (255, 220, 150), 1.0, 20)]), {}


BABY = baby()


def shot_baby(lt, dur, tg):
    """l'officier, penché par-dessus le bastingage, tend un bébé à Violet debout dans le canot"""
    bpos = np.array([0.0, -0.6, 5.5])
    bm = M(trans(bpos), roty(math.pi / 2))
    u = min(1.0, lt / (dur * 0.6))
    hand_pt = np.array([0.0, 0.98, 4.72])
    off_hands = hand_pt + np.array([0, 0.05 + (1 - ease(u)) * 0.25, -0.15 * (1 - ease(u))])
    baby_pt = off_hands if u < 0.85 else hand_pt + np.array([0, -0.15 * ease((u - 0.85) / 0.15) if u < 1 else -0.15, 0.1])
    ms = [DECK_NIGHT, sea(tg, 'sea_night', y=-22), BOAT.xf(bm), boat_people(lt, 4, 1).xf(bm)]
    # l'officier
    off = OFFICER.mesh((0.0, 0, 3.95), 0.0, dict(lean=0.7, hp=0.3, ik_l=baby_pt + np.array([-0.1, 0.0, -0.05]), ik_r=baby_pt + np.array([0.1, 0.0, -0.05])) if u < 0.92
                       else dict(lean=0.5, hp=0.4, la=(0.6, 0.1, 0.4), ra=(0.6, 0.1, 0.4)))
    ms.append(off)
    # Violet debout dans le canot, bras tendus vers le haut
    vt = np.array([0.0, -0.9, 5.25])
    vpose = dict(hp=-0.6 if u < 0.9 else -0.1, ik_l=baby_pt + np.array([-0.1, -0.02, 0.05]), ik_r=baby_pt + np.array([0.1, -0.02, 0.05]))
    ms.append(V_COAT.mesh(tuple(vt), math.pi, vpose))
    ms.append(BABY.xf(M(trans(baby_pt + np.array([0, 0.0, 0.02])), roty(math.pi / 2), rotz(0.2))))
    cam = Cam((2.2, 0.2, 8.0), (0, 0.4, 4.8), 50)
    cam = cam_lerp(cam, Cam((1.6, 0.3, 7.2), (0, 0.5, 4.8), 48), lt / dur)
    return merge(ms), cam, ENV_NIGHT_SEA.copy(points=[((0, 2.6, 3.0), (255, 220, 150), 1.0, 8)]), {}


def shot_baby_close(lt, dur, tg):
    """gros plan : Violet serre le bébé contre elle et le regarde"""
    vt = np.array([0.0, -0.9, 0.0])
    hold = vt + np.array([0.0, 1.2, 0.22])
    v = V_COAT.mesh(tuple(vt), 0.0, dict(hp=0.45, ik_l=hold + np.array([-0.13, -0.03, -0.02]), ik_r=hold + np.array([0.12, -0.06, 0.02])))
    ms = [v, BABY.xf(M(trans(hold), roty(-math.pi / 2 + 0.5), rotx(-0.5))), BOAT.xf(M(trans(0, -0.6, 0), roty(math.pi / 2)))]
    ms += [sea(tg, 'sea_night', y=-1.5), L_TIT_NIGHT.xf(M(trans(30, 0, -60), roty(0.4)))]
    head = V_COAT.attach['head'][:3, 3]
    cam = cam_lerp(Cam(tuple(head + np.array([0.6, -0.1, 1.5])), tuple(head + np.array([0, -0.25, 0.1])), 45),
                   Cam(tuple(head + np.array([0.45, -0.1, 1.2])), tuple(head + np.array([0, -0.25, 0.1])), 42), lt / dur)
    return merge(ms), cam, ENV_NIGHT_SEA.copy(points=[(tuple(head + np.array([0.5, 0.6, 1.0])), (255, 220, 160), 0.7, 4)]), {}


# ------------------------------------------------------------------ 9 : le naufrage vu du canot
def shot_sinking(lt, dur, tg):
    u = lt / max(dur, 0.1)
    pitch = 0.25 + u * 0.55
    Ms = sinking_matrix(pitch, 10 + u * 60, 0.05)
    lights_on = u < 0.45 or (u < 0.5 and int(lt * 15) % 2)
    ship = (L_TIT_NIGHT if lights_on else L_TIT_DARK).xf(M(trans(0, 0, -380), Ms))
    bm = M(trans(0, 0.3, 0), roty(0.2))
    cam = Cam((-4, 2.0, 10), (0, 30, -380), 45)
    ms = [ship, sea(tg, 'sea_night'), STARS, BOAT.xf(bm), boat_people(lt, 5, 2, start=2).xf(bm), FLOES.xf(trans(0, 0, -150))]
    ms.append(V_COAT.mesh((0, -0.33, 0), math.pi, sit_pose(drop=0.45, hp=-0.25, la=(0.9, 0.3, 1.6), ra=(0.9, 0.3, 1.6))).xf(M(bm, trans(-2.4, 0, 0))))
    return merge(ms), cam, ENV_NIGHT_SEA, {}


def shot_cold(lt, dur, tg):
    """le canot dérive parmi la glace ; Violet serre le bébé contre elle, souffle qui fume"""
    bm = M(trans(0, 0.3, 0))
    a = 0.4 + lt * 0.08
    cam = Cam((math.cos(a) * 6.5, 3.0, math.sin(a) * 6.5), (0, 0.6, 0), 50)
    hold = np.array([-2.55, 0.62, 0.25])
    ms = [sea(tg, 'sea_night'), STARS, FLOES, BOAT.xf(bm), boat_people(lt, 5, 3, start=2).xf(bm)]
    vm = V_COAT.mesh((-2.55, -0.33, -0.1), 0.0, sit_pose(drop=0.45, hp=0.4, ik_l=hold + np.array([-0.1, 0, 0]), ik_r=hold + np.array([0.12, -0.05, 0.03])))
    ms += [vm.xf(bm), BABY.xf(M(bm, trans(hold + np.array([0, 0.03, 0.0])), roty(-math.pi / 2 + 0.2), rotz(0.4)))]
    br = (lt * 0.7) % 1.0
    ms.append(billboard((-2.55, 1.45 + br * 0.3, 0.3 + br * 0.4), 0.2 + br * 0.3, 0.2 + br * 0.3, cam, (230, 235, 240), 'puff', emis=0.3, alpha=0.5 * (1 - br)))
    return merge(ms), cam, ENV_NIGHT_SEA.copy(points=[((0, 6, 3), (150, 170, 220), 0.6, 15)]), {}


def shot_carpathia(lt, dur, tg):
    bm = M(trans(0, 0.3, 0), roty(-0.3))
    cam = cam_lerp(Cam((-9, 2.6, 4), (40, -40, -300), 45), Cam((-8, 2.5, 3.5), (40, -38, -300), 42), lt / dur)
    hold = np.array([-2.55, 0.62, 0.25])
    ms = [sea(tg, 'sea_night'), FLOES, BOAT.xf(bm), boat_people(lt, 5, 3, start=2).xf(bm), CARPATHIA.xf(M(trans(60, 0, -520 + lt * 8), roty(-1.3)))]
    vm = V_COAT_C.mesh((-2.55, -0.33, -0.1), 0.0, sit_pose(drop=0.45, hp=0.5, ik_l=hold + np.array([-0.1, 0, 0]), ik_r=hold + np.array([0.12, -0.05, 0.03])))
    ms += [vm.xf(bm), BABY.xf(M(bm, trans(hold + np.array([0, 0.03, 0.0])), roty(-math.pi / 2 + 0.2), rotz(0.4)))]
    return merge(ms), cam, ENV_DAWN, {}


def shot_notover(lt, dur, tg):
    """coup de zoom sur le visage de Violet qui relève la tête"""
    bm = M(trans(0, 0.3, 0), roty(-0.3))
    hold = np.array([-2.55, 0.62, 0.25])
    vm = V_COAT.mesh((-2.55, -0.33, -0.1), 0.0, sit_pose(drop=0.45, hp=-0.1, ik_l=hold + np.array([-0.1, 0, 0]), ik_r=hold + np.array([0.12, -0.05, 0.03])))
    head = (bm @ V_COAT.attach['head'])[:3, 3] + np.array([0, 0.12, 0])
    u = ease(lt / max(dur, 0.1))
    d = np.array([0.15, 0.05, 1.0])
    d /= np.linalg.norm(d)
    cam = Cam(tuple(head + d * lerp(2.6, 0.7, u)), tuple(head), 45)
    ms = [sea(tg, 'sea_night'), FLOES, BOAT.xf(bm), boat_people(lt, 5, 3, start=2).xf(bm), vm.xf(bm),
          BABY.xf(M(bm, trans(hold + np.array([0, 0.03, 0.0])), roty(-math.pi / 2 + 0.2), rotz(0.4)))]
    return merge(ms), cam, ENV_DAWN, {}


# ------------------------------------------------------------------ 12 : 1916, Britannic
def islands():
    ms = []
    for i, (x, z, s) in enumerate(((600, -900, 160), (-700, -1100, 220), (200, -1400, 260), (-200, 1200, 200))):
        ms.append(rock(1.0, 30 + i, (200, 180, 140), 'sand').xf(M(trans(x, -20, z), scale(s, s * 0.35, s * 0.8))))
    return merge(ms)


ISLANDS = islands()


def shot_brit_wide(lt, dur, tg):
    u = lt / max(dur, 0.1)
    cam = Cam((200 - u * 60, 45, 260), (0, 15, 0), 45)
    ms = [L_BRIT, sea(tg, 'sea_aegean'), ISLANDS, wake(tg, cam), funnel_smoke(np.eye(4), tg, cam, col=(80, 78, 75))]
    return merge(ms), cam, ENV_AEGEAN, {}


def shot_nurse(lt, dur, tg):
    """Violet infirmière s'occupe de soldats blessés sur le pont du Britannic"""
    ms = [DECK_BRIT, sea(tg, 'sea_aegean', y=-22)]
    for i, x in enumerate((-2.0, 0.4, 2.8)):
        ms.append(box(2.0, 0.08, 0.7, (240, 240, 235), 'cloth').xf(trans(x, 0.45, 2.6)))
        for dx in (-0.9, 0.9):
            ms.append(box(0.06, 0.45, 0.6, (120, 90, 60)).xf(trans(x + dx, 0, 2.6)))
        sm = (SOLDIER_H if i != 1 else SOLDIER).mesh((0, 0, 0), 0, dict(la=(0.1, 0.1, 0.2), ra=(0.1, 0.1, 0.2)))
        ms.append(sm.xf(M(trans(x - 0.95, 0.65, 2.6), rotx(-math.pi / 2), rotz(-math.pi / 2))))
    v = V_NURSE.mesh((0.6, 0, 1.6), 0.0, dict(lean=0.35, hp=0.4, ik_r=(0.75, 0.8, 2.45), la=(0.3, 0.1, 0.5)))
    ms.append(v)
    cam = cam_lerp(Cam((2.7, 1.7, 5.0), (0.4, 0.9, 2.0), 55), Cam((2.6, 1.6, 4.7), (0.4, 0.9, 2.0), 52), lt / dur)
    return merge(ms), cam, ENV_AEGEAN, {}


L_TIT_GHOST = L_TIT_DAY.set(alpha=0.35)


L_OLY_GHOST = L_OLY.set(alpha=0.3)


def shot_three(lt, dur, tg):
    """les trois frères : Olympic et Titanic en fantômes, seul le Britannic (celui de Violet en 1916) est bien réel"""
    u = ease(lt / max(dur, 0.1))
    cam = Cam((lerp(520, 470, u), 150, lerp(330, 290, u)), (0, 5, 0), 46)
    ms = [L_OLY_GHOST.xf(trans(0, 0, 90)), L_TIT_GHOST, L_BRIT.xf(trans(0, 0, -90)), sea(tg, 'sea_aegean'),
          funnel_smoke(trans(0, 0, -90), tg, cam, col=(80, 78, 75))]
    return merge(ms), cam, ENV_AEGEAN, {}


# ------------------------------------------------------------------ 13 : la mine
def shot_mine_under(lt, dur, tg):
    """sous l'eau : la mine au bout de sa chaîne, la coque blanche arrive au-dessus"""
    sx = -5 + 22 * (1 - lt / max(dur, 0.1))
    cam = Cam((128, -16, 14), (121, -10.5, 6), 60)
    ms = [L_BRIT.xf(trans(sx, 0, 0)), mine().xf(trans(122, -9, 8)), box(600, 0.05, 600, (60, 140, 160), 'underwater', ts=8).xf(trans(100, 0, 0))]
    for i in range(6):
        ms.append(strip([(100 + i * 9, 0, -20 + i * 5), (110 + i * 9, -35, -10 + i * 5)], 2.0, cam, (120, 200, 210), emis=1.0, alpha=0.15))
    ms.append(bubbles((122, -12, 8), tg, cam, 8, 1, 2.0, 6))
    return merge(ms), cam, ENV_UNDER.copy(fog_far=60), {}


def shot_mine_boom(lt, dur, tg):
    cam = Cam((230, 14, 120), (90, 15, 0), 45)
    k = C2.decay(lt, 0.0, 2.5)
    cam = C2.shake(cam, 2.0 * k, tg)
    ms = [L_BRIT.xf(sinking_matrix(0.01 + lt * 0.01, lt * 0.4)), sea(tg, 'sea_aegean'), ISLANDS,
          water_column((112, 0, 16), lt, cam, 75, 2), funnel_smoke(np.eye(4), tg, cam, col=(80, 78, 75))]
    ms.append(big_smoke_(lt, cam))
    return merge(ms), cam, ENV_AEGEAN, dict(flash=0.8 * C2.decay(lt, 0.0, 8))


def big_smoke_(lt, cam):
    if lt < 0.4:
        return Mesh()
    return smoke_sprites((112, 12, 14), lt, cam, n=8, size=14, rise=30, seed=8, col=(90, 85, 80), drift=(0.2, 0, 0.6), alpha=0.7)


# ------------------------------------------------------------------ 14 : 55 minutes
def shot_listing(lt, dur, tg):
    u = lt / max(dur, 0.1)
    Ms = sinking_matrix(0.08 + u * 0.06, 6 + u * 4, 0.12 + u * 0.08)
    cam = Cam((-60 - u * 30, 70, 260), (30, 0, 0), 45)
    ms = [L_BRIT.xf(Ms), sea(tg, 'sea_aegean'), ISLANDS, funnel_smoke(Ms, tg, cam, col=(80, 78, 75))]
    for i in range(6):
        ms.append(lifeboat_mesh(8.0, 2.2, 1.0, empty=False).xf(M(trans(-40 + i * 22, 0.3, 40 + (i % 2) * 12), roty(0.3 * i))))
    ms.append(smoke_sprites((100, 5, 14), tg, cam, n=8, size=12, rise=25, seed=8, col=(100, 95, 90), drift=(0.2, 0, 0.6), alpha=0.6))
    return merge(ms), cam, ENV_AEGEAN, {}


# ------------------------------------------------------------------ 15 : les hélices
BRIT_TILT = sinking_matrix(0.065, 1.0, 0.04)


PROP_C = None


def prop_scene(lt, tg, boat_pos):
    """le Britannic coule par l'avant : l'arrière se soulève, l'hélice tribord émerge et brasse l'eau"""
    rot = tg * 6
    ship = liner('britannic', prop_rot=rot)
    ms = [ship.xf(BRIT_TILT), sea(tg, 'sea_aegean')]
    bm = M(trans(boat_pos), roty(0.3))
    ms += [BOAT.xf(bm), boat_people(lt, 5, 0, start=0).xf(bm)]
    return ms, bm


def prop_world():
    return (BRIT_TILT @ np.array([-134, -6.5, 7.5, 1]))[:3]


def churn(tg, cam, n=14):
    p = prop_world()
    ms = []
    for i in range(n):
        ph = (tg * 1.6 + i / n) % 1.0
        a = i * 2.4
        q = np.array([p[0] + math.cos(a) * 3.5 * ph, 0.4 + ph * 1.5, p[2] + math.sin(a) * 3.5 * ph])
        ms.append(billboard(q, 2.5 + ph * 2.5, 1.8, cam, (240, 248, 250), 'puff', emis=0.4, alpha=0.8 * (1 - ph)))
    return merge(ms)


def boat_track(t_abs):
    """le canot est aspiré : il glisse vers l'hélice"""
    p = prop_world()
    u = min(1.0, max(0.0, t_abs / 4.5))
    start = p + np.array([-6.0, 0, 22.0])
    end = p + np.array([-1.0, 0, 7.5])
    q = start + (end - start) * ease(u)
    q[1] = 0.3
    return q


def shot_props(lt, dur, tg):
    """plan large : l'arrière dressé, l'hélice géante qui tourne à moitié hors de l'eau, le canot attiré vers elle"""
    bp = boat_track(lt)
    ms, bm = prop_scene(lt, tg, bp)
    vm = V_NURSE_SHOCK.mesh((0, -0.33, 0), math.pi / 2, sit_pose(drop=0.45, hp=-0.3, la=(1.0, 0.4, 0.8), ra=(1.0, 0.4, 0.8)))
    ms.append(vm.xf(M(bm, trans(-2.4, 0, -0.55))))
    p = prop_world()
    cam = Cam(tuple(p + np.array([-26, 7, 32])), tuple((p + bp) / 2 + np.array([0, 0.5, 0])), 50)
    cam = C2.shake(cam, 0.15, tg)
    ms.append(churn(tg, cam))
    return merge(ms), cam, ENV_AEGEAN, {}


def shot_jump(lt, dur, tg):
    """plus près : Violet se lève et saute par-dessus bord, côté opposé à l'hélice"""
    t_abs = S('jump') - S('props') + lt
    bp = boat_track(t_abs)
    ms, bm = prop_scene(lt, tg, bp)
    t_j = 0.45
    if lt < t_j:
        k = lt / t_j
        vm = V_NURSE_SH.mesh((0, -0.33 + 0.3 * k, 0), math.pi, dict(ll=(1.4 * (1 - k), 1.4 * (1 - k)), rl=(1.4 * (1 - k), 1.4 * (1 - k)), drop=0.45 * (1 - k),
                                                               la=(1.2 * k, 0.3, 0.3), ra=(1.2 * k, 0.3, 0.3)))
        ms.append(vm.xf(M(bm, trans(-2.4, 0, -0.55))))
    else:
        a = lt - t_j
        loc = np.array([-2.4, 2.2 * a - 4.9 * a * a, -0.55 - 1.8 * a])
        if loc[1] > -1.6:
            vm = V_NURSE_SH.mesh(tuple(loc), math.pi, dict(la=(2.8, 0.3, 0.2), ra=(2.8, 0.3, 0.2), ll=(0.3, 0.5), rl=(-0.2, 0.3), lean=0.3))
            ms.append(vm.xf(bm))
        tsp = (2.2 + math.sqrt(2.2 ** 2 + 4 * 4.9 * 1.0)) / (2 * 4.9)
        wp = (bm @ np.array([-2.4, 0, -0.55 - 1.8 * tsp, 1]))[:3]
    p = prop_world()
    c = (bm @ np.array([-2.4, 0.8, -1.0, 1]))[:3]
    cam = Cam(tuple(c + np.array([-5.5, 2.2, 8.5])), tuple(c + (p - c) * 0.25), 52)
    if lt >= t_j:
        ms.append(splash_fx((wp[0], 0.2, wp[2]), lt - t_j - tsp, cam, 1.6, 4))
    ms.append(churn(tg, cam))
    return merge(ms), cam, ENV_AEGEAN, {}


# ------------------------------------------------------------------ 16 : sous l'eau
def shot_under(lt, dur, tg):
    """Violet sous l'eau remonte et heurte la quille d'un canot : flash, secousse, tout s'assombrit"""
    t_hit = dur * 0.55
    y = -3.2 + min(lt, t_hit) * (2.0 / t_hit)
    if lt > t_hit:
        y = -1.2 - (lt - t_hit) * 0.5
    vm = (V_NURSE_SH if lt < t_hit else V_NURSE_C).mesh((0, 0, 0), 0.0, dict(la=(2.9, 0.4, 0.3), ra=(2.9, 0.4, 0.3), ll=(0.3 * math.sin(lt * 6), 0.4),
                                                                                                rl=(-0.3 * math.sin(lt * 6), 0.4), hp=-0.6))
    vm = vm.xf(M(trans(0, y, 0), rotx(0.25)))
    boat = BOAT.xf(M(trans(0.2, 0.3, 0.3), roty(0.3)))
    cam = Cam((1.6, -2.4, 3.0), (0, -0.6, 0), 60)
    k = C2.decay(lt, t_hit, 3)
    cam = C2.shake(cam, 0.25 * k, tg)
    ms = [vm, boat, box(60, 0.02, 60, (90, 170, 190), 'water', ts=4, alpha=0.6).xf(trans(0, 0.02, 0)), bubbles((0, y + 1.8, 0.1), tg, cam, 12, 2, 0.3, 2.5)]
    for i in range(5):
        ms.append(strip([(-3 + i * 1.5, 0, -2), (-2 + i * 1.5, -12, -1)], 0.8, cam, (130, 210, 220), emis=1.0, alpha=0.12))
    dark = min(0.85, max(0.0, (lt - t_hit) / (dur - t_hit)) * 0.85)
    return merge(ms), cam, ENV_UNDER, dict(flash=0.9 * C2.decay(lt, t_hit, 10), fade=dark,
                                           post_pil=(lambda im: C2.vignette(im, 0.6 + 0.3 * (lt > t_hit))))


# ------------------------------------------------------------------ 17 : elle survit
def shot_surface(lt, dur, tg):
    bm = M(trans(0, 0.3, 0), roty(0.2))
    rise = min(1.0, lt / 0.4)
    ms = [sea(tg, 'sea_aegean'), BOAT.xf(bm), boat_people(lt, 4, 2).xf(bm), ISLANDS]
    vpos = (bm @ np.array([0.0, -1.6 + rise * 0.55, 1.8, 1]))[:3]
    vm = V_NURSE_SHOCK.mesh(tuple(vpos), math.pi + 0.2, dict(la=(2.2, 0.2, 0.4), ra=(1.6, 0.1, 0.6), hp=-0.3))
    ms.append(vm)
    ms.append(splash_fx(vpos + np.array([0, 1.5, 0]), lt, Cam((4, 1.6, 6), (0, 0.4, 0), 50), 0.8, 7))
    cam = cam_lerp(Cam((3.5, 1.4, 6.5), tuple(vpos + np.array([0, 1.0, 0])), 50), Cam((5, 2.5, 9), tuple(vpos + np.array([0, 0.8, 0])), 55), lt / dur)
    return merge(ms), cam, ENV_AEGEAN, {}


# ------------------------------------------------------------------ 18 : le coup de fil
def lightning_k(tg, seed=0, period=3.1):
    ph = (tg + seed * 0.7) % period
    return max(0.0, 1 - ph / 0.12) + 0.6 * max(0.0, 1 - abs(ph - 0.22) / 0.06)


def house_ext():
    ms = [grid(-30, -30, 30, 30, 6, 6, None, (255, 255, 255), 'grass_night', 3.0)]
    ms.append(box(9, 4.5, 7, (220, 205, 180), 'plaster_old', ts=1.5))
    rt = [[(-4.8, 4.5, 3.8), (4.8, 4.5, 3.8), (4.8, 7.2, 0)], [(-4.8, 4.5, 3.8), (4.8, 7.2, 0), (-4.8, 7.2, 0)],
          [(4.8, 4.5, -3.8), (-4.8, 4.5, -3.8), (-4.8, 7.2, 0)], [(4.8, 4.5, -3.8), (-4.8, 7.2, 0), (4.8, 7.2, 0)]]
    ms.append(Mesh(rt, C((120, 60, 50)), [[(0, 1), (4, 1), (4, 0)], [(0, 1), (4, 0), (0, 0)]] * 2, TEXB['roof_red']))
    for s in (-1, 1):
        ms.append(Mesh([[(s * 4.5, 4.5, 3.5), (s * 4.5, 4.5, -3.5), (s * 4.5, 7.2, 0)]], C((220, 205, 180)), [[(0, 1), (2, 1), (1, 0)]], TEXB['plaster_old']))
    ms.append(box(1.6, 1.3, 0.06, (255, 220, 140), emis=0.9).xf(trans(-2.0, 1.2, 3.52)))
    ms.append(box(1.6, 1.3, 0.06, (40, 45, 60)).xf(trans(2.2, 1.2, 3.52)))
    ms.append(box(1.0, 2.1, 0.06, (255, 255, 255), 'door').xf(trans(0.2, 0, 3.52)))
    ms.append(box(0.8, 1.6, 0.8, (150, 140, 130), 'brick').xf(trans(3.0, 6.0, 0)))
    ms.append(rain_puddles())
    return merge(ms)


def rain_puddles():
    return Mesh()


HOUSE = house_ext()


def shot_storm_ext(lt, dur, tg):
    k = lightning_k(tg, 1)
    cam = cam_lerp(Cam((-6, 1.6, 14), (-1, 2.4, 0), 50), Cam((-5, 1.7, 11), (-1, 2.4, 0), 50), lt / dur)
    ms = [HOUSE, C2.rain_mesh(cam, tg, 160, 12, 1), cloud_bank(0, 40, -60, 200, 3, (30, 32, 42), 14, 20)]
    env = C2.flash_env(ENV_STORM, k, (0, 30, -20))
    return merge(ms), cam, env, dict(flash=0.25 * k)


def room_env(tg, base_k=0.0):
    k = lightning_k(tg, 2)
    e = ENV_ROOM.copy(points=[((-0.35, 1.1, -0.75), (255, 200, 130), 0.8, 4), ((1.4, 1.6, -3.5), (180, 200, 255), 2.2 * k, 6)])
    return e, k


def shot_ring(lt, dur, tg):
    """le téléphone sonne ; Violet âgée lève les yeux de son tricot et tend la main"""
    ring = 1.0
    u = lt / max(dur, 0.1)
    vm = V_OLD.mesh((-1.2, 0.0, -0.3), 0.0, sit_pose(drop=0.45, hp=0.2 - 0.4 * min(1, u * 2), hy=0.8 * min(1, u * 1.5),
                                                       ra=(0.6 + 0.6 * ease(u), 0.5 + 0.3 * ease(u), 0.5), la=(0.6, 0.1, 0.7)))
    ms = [COTTAGE, vm, phone(0, ring, tg).xf(trans(PHONE_POS))]
    cam = cam_lerp(Cam((1.3, 1.35, 1.8), (-0.6, 0.85, -0.45), 50), Cam((1.1, 1.3, 1.5), (-0.5, 0.85, -0.45), 46), u)
    e, k = room_env(tg)
    return merge(ms), cam, e, dict(flash=0.15 * k)


def shot_answer(lt, dur, tg):
    """gros plan : Violet décroche, l'écouteur à l'oreille ; son visage se fige"""
    shock = lt > WT(18, "C'était") - S('answer') - 0.1
    who = V_OLD_SH if shock else V_OLD
    who.mesh((-1.2, 0.0, -0.3), 0.0, sit_pose(drop=0.45, hp=0.0, hy=0.25))
    h0 = who.attach['head'][:3, 3]
    hd = who.attach['head'][:3, :3]
    ear = h0 + hd @ np.array([0.2, 0.1, 0.02])
    pose = sit_pose(drop=0.45, hp=0.0, hy=0.25, ik_r=ear + np.array([0, -0.08, 0]), la=(0.6, 0.1, 0.7))
    pose['hand_r'] = handset_mesh().xf(M(trans(0.0, 0.02, 0.0), rotz(math.pi / 2)))
    vm = who.mesh((-1.2, 0.0, -0.3), 0.0, pose)
    hand = who.attach['hand_r'][:3, 3]
    base = PHONE_POS + np.array([0.1, 0.1, 0.0])
    pts = [base + (hand - base) * s + np.array([0, -0.25 * math.sin(math.pi * s), 0]) for s in np.linspace(0, 1, 8)]
    ms = [COTTAGE, vm, phone(1, 0, tg).xf(trans(PHONE_POS)), strip(pts, 0.012, Cam((0, 1, 2), (0, 1, 0)), (25, 25, 25), emis=0.2)]
    head = who.attach['head'][:3, 3]
    cam = cam_lerp(Cam(tuple(head + np.array([0.8, 0.0, 1.15])), tuple(head + np.array([0, 0.02, 0])), 45),
                   Cam(tuple(head + np.array([0.6, 0.0, 0.85])), tuple(head + np.array([0, 0.02, 0])), 42), lt / dur)
    e, k = room_env(tg)
    return merge(ms), cam, e, dict(flash=0.15 * k)


# ------------------------------------------------------------------ 19 : le cimetière
def shot_grave(lt, dur, tg):
    k = lightning_k(tg, 3, 2.4)
    cam = cam_lerp(Cam((1.2, 1.2, 3.5), (0, 0.4, -3), 50), Cam((0.6, 0.9, 0.5), (0, 0.4, -3), 45), lt / dur)
    ms = [CEMETERY, C2.rain_mesh(cam, tg, 150, 10, 2), cloud_bank(0, 40, -80, 200, 5, (25, 28, 38), 12, 20)]
    env = C2.flash_env(ENV_STORM, k, (2, 20, -10))
    return merge(ms), cam, env, dict(flash=0.3 * k)


# ------------------------------------------------------------------ 20 : fin
def shot_end(lt, dur, tg):
    """le combiné pend au bout du fil et se balance ; éclairs"""
    sw = math.sin(tg * 2.2) * 0.35 * math.exp(-lt * 0.15)
    top = PHONE_POS + np.array([0.12, 0.02, 0.1])
    L = 0.5
    hp = top + np.array([math.sin(sw) * L, -math.cos(sw) * L, 0.05])
    pts = [PHONE_POS + np.array([0.1, 0.1, 0.0]), top + np.array([0, 0.05, 0]), hp]
    hs = handset_mesh().xf(M(trans(hp), rotz(math.pi / 2 + sw)))
    ms = [COTTAGE, phone(1, 0, tg).xf(trans(PHONE_POS)), hs, strip(pts, 0.012, Cam((0, 1, 2), (0, 1, 0)), (25, 25, 25), emis=0.2)]
    ms.append(box(0.9, 0.42, 0.8, (120, 70, 50), 'cloth').xf(trans(-1.2, 0, -0.3)) if False else Mesh())
    cam = cam_lerp(Cam((0.9, 0.7, 1.4), (0.0, 0.45, -0.4), 50), Cam((0.55, 0.6, 0.8), (0.05, 0.4, -0.4), 44), lt / dur)
    e, k = room_env(tg)
    fade = max(0.0, (lt - dur + 0.6) / 0.6)
    return merge(ms), cam, e, dict(flash=0.2 * k, fade=fade)


# ------------------------------------------------------------------ montage
add('hook', 0.0, shot_hook)
add('hook_crash', WT(0, 'et') - 0.05, shot_hook_crash)
add('hook_mine', WT(0, 'autres') - 0.05, shot_hook_mine)
add('intro', T(1), shot_intro)
add('intro_wide', WT(1, 'Hôtesse') - 0.1, shot_intro_wide)
add('southampton', T(2), shot_southampton)
add('twins', WT(2, 'jumeau') - 0.35, shot_twins)
add('wave', T(3), shot_wave)
add('ram', WT(3, 'boum') - 0.25, shot_ram)
add('ram_wide', WT(3, 'navire') - 0.05, shot_ram_wide)
add('corridor', T(4), shot_corridor)
add('gash', WT(4, 'Premier') - 0.1, shot_gash)
add('dock', T(5), shot_dock)
add('night', T(6), shot_night)
add('iceberg', WT(6, "L'iceberg.") - 0.25, shot_iceberg)
add('boats', T(7), shot_boats)
add('lower', T(8), shot_lower)
add('baby', WT(8, 'officier') - 0.1, shot_baby)
add('baby_close', WT(8, 'bras.') - 0.25, shot_baby_close)
add('sinking', T(9), shot_sinking)
add('cold', WT(9, 'Elle') - 0.05, shot_cold)
add('carpathia', T(10), shot_carpathia)
add('notover', T(11), shot_notover)
add('brit_wide', T(12), shot_brit_wide)
add('nurse', WT(12, 'Violet') - 0.05, shot_nurse)
add('three', WT(12, 'troisième') - 0.1, shot_three)
add('mine_under', T(13), shot_mine_under)
add('mine_boom', WT(13, 'explose.') - 0.05, shot_mine_boom)
add('listing', T(14), shot_listing)
add('props', T(15), shot_props)
add('jump', WT(15, 'Elle') - 0.1, shot_jump)
add('under', T(16), shot_under)
add('surface', T(17), shot_surface)
add('storm_ext', T(18), shot_storm_ext)
add('ring', T(18, 7) - 0.05, shot_ring)
add('answer', T(18, 10) - 0.05, shot_answer)
add('grave', T(19), shot_grave)
add('end', T(20), shot_end)

tl.overlay = C2.overlays(
    C2.hook_title(['3 NAUFRAGES.', '1 SURVIVANTE.'], 0.0, T(1) - 0.05, y=260, accent=1),
    C2.badge('ACCIDENT 1/3', WT(4, 'Premier') - 0.1, min(2.0, S('dock') - WT(4, 'Premier'))),
    C2.badge('ACCIDENT 2/3', S('iceberg') + 0.1, min(2.0, S('boats') - S('iceberg') - 0.1)),
    C2.badge('ACCIDENT 3/3', S('mine_boom') + 0.05, 2.2),
    C2.cta(T(10) - 0.1, max(2.6, T(11) - T(10) + 0.1)),
    C2.comment_bubble(WT(20, 'Dis-le') - 0.1, 3.5, y=330, text='Moi je pense que…', user='toi'),
)

subs = Subs(timing)


def build_audio(path):
    dur = tl.duration()
    mx = A.Mixer(dur)
    # accroche
    mx.add(C2.water_rush(3), 0, 0.5)
    mx.add(C2.metal_groan(2.5), 0.0, 0.5)
    mx.add(C2.impact(), 0.0, 0.7)
    mx.add(C2.crash_metal(), S('hook_crash') + 0.15, 0.8)
    mx.add(A.explosion(2.5), S('hook_mine') + 0.05, 0.8)
    mx.add(C2.impact(), S('hook_mine') + 0.05, 0.6)
    # Olympic
    mx.add(A.waves(10), S('intro'), 0.25, 0.3, 0.5, length=S('corridor') - S('intro'))
    mx.add(A.gulls(6), S('intro'), 0.3, length=S('wave') - S('intro'))
    mx.add(C2.ship_horn(2.2), S('southampton') + 0.2, 0.55)
    mx.add(A.crowd(4), S('southampton'), 0.25, 0.3, 0.3, length=S('twins') - S('southampton'))
    mx.add(C2.riser(1.0), S('ram') - 0.9, 0.4)
    mx.add(C2.crash_metal(2.5), S('ram') + 0.2, 0.9)
    mx.add(C2.impact(), S('ram') + 0.2, 0.6)
    mx.add(A.splash(1.2), S('ram') + 0.35, 0.5)
    mx.add(C2.metal_groan(2.0), S('ram_wide'), 0.3)
    for i in range(3):
        mx.add(A.clank(0.3), S('corridor') + 0.1 + i * 0.25, 0.3)
    mx.add(C2.ding(), S('gash') + 0.1, 0.4)
    # Titanic
    mx.add(A.crowd(4), S('dock'), 0.3, 0.3, 0.3, length=S('night') - S('dock'))
    mx.add(A.gulls(4), S('dock'), 0.3, length=S('night') - S('dock'))
    mx.add(A.waves(8), S('night'), 0.2, length=S('carpathia') - S('night'))
    mx.add(A.bell(1.5, 880), S('iceberg') - 0.3, 0.35)
    mx.add(A.bell(1.5, 880), S('iceberg') - 0.05, 0.35)
    mx.add(C2.metal_groan(3.0), S('iceberg') + 0.05, 0.7)
    mx.add(C2.impact(), S('iceberg'), 0.5)
    mx.add(C2.ding(), S('iceberg') + 0.1, 0.4)
    mx.add(A.crowd(4), S('boats'), 0.4, 0.2, 0.3, length=S('lower') - S('boats'))
    mx.add(A.ratchet(1.0), S('lower') + 0.2, 0.35)
    mx.add(A.ratchet(1.0), S('lower') + 1.2, 0.3)
    mx.add(C2.metal_groan(3.0), S('sinking'), 0.6)
    mx.add(C2.water_rush(3), S('sinking') + 0.5, 0.4)
    mx.add(A.wind(8), S('cold'), 0.3, 0.3, 0.5, length=S('brit_wide') - S('cold'))
    mx.add(C2.ship_horn(2.0), S('carpathia') + 0.6, 0.25)
    mx.add(C2.pop(), T(10) + 0.05, 0.5)
    mx.add(C2.ding(), T(10) + (max(2.6, T(11) - T(10) + 0.1)) * 0.62, 0.45)
    mx.add(C2.riser(1.0), S('brit_wide') - 1.0, 0.5)
    mx.add(C2.impact(), S('brit_wide'), 0.5)
    # Britannic
    mx.add(A.waves(10), S('brit_wide'), 0.25, length=S('mine_under') - S('brit_wide'))
    mx.add(A.gulls(5), S('brit_wide'), 0.3, length=S('three') - S('brit_wide'))
    mx.add(C2.underwater(2), S('mine_under'), 0.5)
    mx.add(A.explosion(3), S('mine_boom'), 0.9)
    mx.add(C2.impact(), S('mine_boom'), 0.7)
    mx.add(C2.ding(), S('mine_boom') + 0.05, 0.4)
    mx.add(C2.metal_groan(3), S('listing'), 0.5)
    mx.add(C2.water_rush(5), S('props'), 0.6, 0.2, 0.3, length=S('under') - S('props'))
    mx.add(A.chuff(4, 6), S('props'), 0.3, length=S('under') - S('props'))
    mx.add(A.splash(1.0), S('jump') + 0.75, 0.7)
    mx.add(C2.underwater(4), S('under'), 0.7, length=S('surface') - S('under'))
    mx.add(C2.impact(), S('under') + (S('surface') - S('under')) * 0.55, 0.8)
    mx.add(A.thwack(), S('under') + (S('surface') - S('under')) * 0.55, 0.6)
    mx.add(C2.heartbeat(2.0, 50), S('under') + (S('surface') - S('under')) * 0.6, 0.6)
    mx.add(A.splash(1.0), S('surface') + 0.1, 0.6)
    mx.add(A.waves(6), S('surface'), 0.3, length=S('storm_ext') - S('surface'))
    # l'orage, le téléphone
    mx.add(A.rain(12), S('storm_ext'), 0.35, 0.3, 1.0, length=dur - S('storm_ext'))
    for t0 in np.arange(S('storm_ext'), dur, 3.1):
        mx.add(A.thunder_close(4.0, int(t0)) if hasattr(A, 'thunder_close') else A.thunder(4), t0 + 0.05, 0.4)
    mx.add(C2.phone_ring(4.0), S('ring'), 0.6, length=S('answer') - S('ring') + 0.05)
    mx.add(A.clank(0.2), S('answer'), 0.25)
    mx.add(C2.riser(1.2), WT(18, "C'était") - 1.0, 0.35)
    mx.add(C2.impact(), WT(18, "C'était") - 0.05, 0.5)
    mx.add(C2.impact(), S('grave'), 0.4)
    mx.add(C2.heartbeat(3.0, 55), S('end'), 0.45)
    # musiques
    C2.music_bed(mx, S('intro'), S('cold'), 'tense', 104, 0.16, 1)
    C2.music_bed(mx, S('cold'), S('brit_wide'), 'sad', 70, 0.22, 2)
    C2.music_bed(mx, S('brit_wide'), S('storm_ext'), 'epic', 110, 0.2, 3)
    C2.music_bed(mx, S('storm_ext'), dur, 'sad', 60, 0.14, 4)
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
        n = len(times)
        for k in range(0, n, 36):
            contact_sheet(tl, times[k:k + 36], os.path.join(HERE, f'sheet{k // 36 + 1}.png'), subs, cols=6, scale=0.18)
    elif len(sys.argv) > 1 and sys.argv[1] == '--at':
        for s in sys.argv[2:]:
            frame(tl, float(s), subs).resize((540, 960)).save(os.path.join(HERE, f'at_{s}.png'))
    elif len(sys.argv) > 1 and sys.argv[1] == '--draft':
        build_audio(os.path.join(HERE, 'sfx.wav'))
        render_video(tl, os.path.join(HERE, 'violet_draft.mp4'), os.path.join(HERE, 'sfx.wav'), subs)
    else:
        build_audio(os.path.join(HERE, 'sfx.wav'))
        mix_voice(os.path.join(HERE, 'voix.wav'), os.path.join(HERE, 'sfx.wav'), os.path.join(HERE, 'mix.wav'))
        render_video(tl, os.path.join(HERE, 'Violet_Good2No.mp4'), os.path.join(HERE, 'mix.wav'), subs)
