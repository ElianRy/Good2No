"""Vidéo : Roy Sullivan, l'homme foudroyé 7 fois."""
import sys, os, math, json
sys.path[:0] = ['/home/claude/g2n', '/home/claude/g2n/roy']
import numpy as np
from world import *
from video_core import *
from scripts import ROY
import audio as A

HERE = '/home/claude/g2n/roy'
TIMING_FILE = os.path.join(HERE, 'timing.json')
timing = load_timing(TIMING_FILE) if os.path.exists(TIMING_FILE) else est_timing(ROY)
tl = Timeline(timing)
T = tl.T
WT = tl.word_t


# ------------------------------------------------------------------ outils éclair
def bolt_k(lt, th):
    d = lt - th
    if d < 0 or d > 0.55:
        return 0.0
    if d < 0.07:
        return 1.0
    if d < 0.11:
        return 0.25
    if d < 0.17:
        return 0.85
    return max(0.0, 0.85 * (1 - (d - 0.17) / 0.38))


def bolt_vis(lt, th):
    d = lt - th
    return 0 <= d < 0.2


def strike(cam, lt, th, target, top=None, seed=0, width=0.28):
    """renvoie (mesh, k)"""
    k = bolt_k(lt, th)
    target = np.asarray(target, float)
    if top is None:
        top = target + np.array([3.0, 45.0, -10.0])
    m = Mesh()
    if bolt_vis(lt, th):
        m = lightning_mesh(lightning_path(top, target, seed=seed, segs=22, jitter=0.05, branches=4), cam, width * 0.8)
    return m, k


def screen_flash(lt, th):
    d = lt - th
    if 0 <= d < 0.04:
        return 0.35
    if 0.1 <= d < 0.13:
        return 0.2
    return 0.0


def hit_pose(lt, th, base=None):
    """raidi par l'éclair"""
    d = lt - th
    p = dict(base or {})
    if 0 <= d < 0.35:
        j = math.sin(d * 90) * 0.06
        p.update(la=(0.2, 1.1 + j, 0.2), ra=(0.2, 1.1 - j, 0.2), hp=-0.25, lean=-0.1, face='roy_shock')
    elif 0.35 <= d < 1.1:
        p.update(la=(0.1, 0.5, 0.6), ra=(0.1, 0.5, 0.6), lean=0.15, drop=0.08, face='roy_shock')
    return p


STORM_CLOUDS = storm_clouds(55, seed=1, w=400, n=40, z=-60)
RIDGES = ridges(0, -160, 4, 700, seed=2)
RIDGES_S = ridges(0, -160, 4, 700, seed=2, base_col=(120, 130, 150))


def storm_env(k=0.0, hit=None):
    return flash_env(ENV_STORM, k, hit)


# ------------------------------------------------------------------ 0 : accroche
def summit_ground():
    def h(x, z):
        return -0.08 * (x * x + z * z) ** 0.9 / 10
    return grid(-40, -40, 40, 40, 16, 16, h, (255, 255, 255), 'rock', 2.0)


SUMMIT = merge([summit_ground(), rock(1.2, 3).xf(trans(-2.5, -0.3, -1.5)), rock(0.9, 4).xf(trans(2.8, -0.3, 0.5)),
                rock(0.7, 5).xf(trans(1.5, -0.2, -2.5)), STORM_CLOUDS, RIDGES_S,
                forest(-40, -40, 40, -12, 30, seed=3, hfun=lambda x, z: -0.08 * (x * x + z * z) ** 0.9 / 10)])
ROY_N = roy()
ROY_NB = roy('roy_nobrow', hair_burn=True)
ROY_NOHAT = roy(hat=False)
ROY_NOHAT_B = roy('roy_nobrow', hat=False, hair_burn=True)


def shot_hook(lt, dur, tg):
    th1 = WT(0, 'frapper') + 0.1
    th2 = WT(0, '7') + 0.2
    th3 = WT(0, 'foudre,') + 0.05
    cam = cam_lerp(Cam((0.9, 0.45, 5.6), (0, 2.3, 0), 58), Cam((0.6, 0.6, 4.4), (0, 2.0, 0), 58), lt / dur)
    ms = [SUMMIT]
    k = 0
    base = dict(la=(0, 0.1, 0.1), ra=(0, 0.1, 0.1), hy=0.2 * math.sin(lt * 0.8))
    pose = dict(base)
    hit = (0, 1.8, 0)
    m1, k1 = strike(cam, lt, th1, (0, 1.85, 0), seed=1)
    m2, k2 = strike(cam, lt, th2, (0, 1.85, 0), top=(-8, 45, -12), seed=2)
    m3, k3 = strike(cam, lt, th3, (0, 1.85, 0), top=(10, 45, -8), seed=3)
    ms += [m1, m2, m3]
    k = max(k1, k2, k3)
    for th in (th1, th2, th3):
        pose = hit_pose(lt, th, pose) if 0 <= lt - th < 1.1 else pose
    if lt > th1 + 0.3:
        ms.append(smoke_sprites((0, 1.9, 0), lt, cam, n=5, size=0.4, rise=2.0, seed=5, alpha=0.6))
    ms.append(ROY_N.mesh((0, 0, 0), 0.0, pose))
    ms.append(rain_mesh(cam, tg, 120, 12))
    fl = max(screen_flash(lt, th1), screen_flash(lt, th2), screen_flash(lt, th3))
    return merge(ms), cam, storm_env(k, hit), dict(flash=fl)


def shot_hook2(lt, dur, tg):
    """gros plan : il fume mais il est vivant"""
    cam = cam_lerp(Cam((0.4, 1.65, 2.0), (0, 1.62, 0), 45), Cam((0.3, 1.66, 1.6), (0, 1.64, 0), 45), lt / dur)
    blink = (lt % 2.2) < 0.12
    face = 'roy_closed' if blink else ('roy_smile' if lt > dur * 0.6 else 'roy')
    pose = dict(face=face, hy=0.0, ra=(0.5 if lt > dur * 0.5 else 0, 0.6 if lt > dur * 0.5 else 0.1, 1.9 if lt > dur * 0.5 else 0.1))
    ms = [SUMMIT, ROY_N.mesh((0, 0, 0), 0.0, pose),
          smoke_sprites((0, 1.92, 0), lt, cam, n=6, size=0.25, rise=1.5, seed=6, alpha=0.55),
          smoke_sprites((0.2, 1.4, 0.1), lt, cam, n=3, size=0.15, rise=0.8, seed=7, alpha=0.45),
          rain_mesh(cam, tg, 80, 6)]
    return merge(ms), cam, storm_env(0.15 * (1 + math.sin(lt * 3)) * 0), {}


# ------------------------------------------------------------------ 1 : Shenandoah
def trail_ground():
    def colf(x, z):
        return (190, 160, 120) if abs(x - 0.3 * math.sin(z * 0.15)) < 1.2 else (255, 255, 255)
    return grid(-50, -60, 50, 30, 20, 18, lambda x, z: 0.0, (255, 255, 255), 'grass', 3.0, colfun=colf)


def park_sign():
    ms = [box(2.6, 1.0, 0.12, (110, 75, 45), 'planks').xf(trans(0, 0.9, 0)),
          box(0.15, 1.5, 0.15, (90, 60, 35)).xf(trans(-1.1, 0, 0)), box(0.15, 1.5, 0.15, (90, 60, 35)).xf(trans(1.1, 0, 0)),
          box(2.8, 0.12, 0.3, (90, 60, 35)).xf(trans(0, 1.9, 0))]
    # lettres gravées (traits, pas de texte lisible)
    for i in range(9):
        ms.append(box(0.16, 0.25, 0.02, (230, 205, 150)).xf(trans(-1.0 + i * 0.25, 1.45, 0.07)))
    for i in range(6):
        ms.append(box(0.18, 0.12, 0.02, (230, 205, 150)).xf(trans(-0.65 + i * 0.26, 1.08, 0.07)))
    ms.append(box(0.5, 0.5, 0.02, (210, 180, 120)).xf(trans(0, 1.6, 0.07)).xf(trans(0, -0.45, 0)).xf(trans(10, 0, 0)))
    return merge(ms)


PARK = merge([trail_ground(), grass_tufts(-25, -40, 25, 15, 700, 1, avoid=lambda x, z: abs(x - 0.3 * math.sin(z * 0.15)) < 1.3, flowers=0.15), RIDGES, forest(-50, -60, 50, 25, 70, seed=4, avoid=[(0, -10, 3.0), (0, 0, 3), (0, 10, 3), (-3.5, 4, 2.5)]),
              park_sign().xf(M(trans(-3.5, 0, 4), roty(0.5))), cloud_bank(0, 70, -200, 300, 9, (240, 240, 245), 12, 14)])


def shot_park(lt, dur, tg):
    z = -6 + lt * 1.3
    cam = cam_lerp(Cam((1.8, 1.4, z + 5.5), (0, 1.5, z - 2), 55), Cam((1.6, 1.5, z + 4.8), (0, 1.6, z - 4), 55), lt / dur)
    ms = [PARK, ROY_N.mesh((0.3 * math.sin(z * 0.15), 0, z), 0.0, walk_pose(lt * 6.5, hy=0.2 * math.sin(lt)))]
    return merge(ms), cam, ENV_SUN, {}


# ------------------------------------------------------------------ 2 : tour 1942
def tower_scene():
    def h(x, z):
        return -0.05 * max(0, math.hypot(x, z) - 4) ** 1.3
    g = grid(-50, -50, 50, 50, 16, 16, h, (255, 255, 255), 'rock', 2.5)
    return merge([g, lookout_tower(9.0, rod=False), STORM_CLOUDS, RIDGES_S,
                  forest(-50, -50, 50, 50, 50, seed=7, avoid=[(0, 0, 9)], hfun=h)])


TOWER = tower_scene()


def roy_in_cab(lt):
    return ROY_N.mesh((0.5, 9.15, 0.3), 0.8 + 0.3 * math.sin(lt), dict())


def shot_tower(lt, dur, tg):
    # caméra qui monte de la base jusqu'au toit (pas de paratonnerre)
    u = lt / dur
    cam = Cam((7.0, 2.0 + u * 9.5, 9.0), (0, 2.0 + u * 10.5, 0), 55)
    ms = [TOWER, roy_in_cab(lt), rain_mesh(cam, tg, 120, 14)]
    k = 0.25 if (lt % 2.0) < 0.06 else 0.0
    return merge(ms), cam, storm_env(k), {}


def shot_tower_hit(lt, dur, tg):
    th = WT(2, 'foudre') - tl_start_of('tower_hit')
    run_z = 2.2 + lt * 2.6
    pos = (0.8, 0, min(run_z, 2.2 + th * 2.6))
    cam = Cam((3.2, 1.0, pos[2] + 4.6), (0.6, 2.2, pos[2] - 0.5), 58)
    if lt < th:
        pose = run_pose(lt * 9, face='roy_shout')
    else:
        pose = hit_pose(lt, th, dict(la=(0, 0.1, 0.1), ra=(0, 0.1, 0.1)))
    m, k = strike(cam, lt, th, (pos[0], 1.85, pos[2]), seed=11)
    ms = [TOWER, m, ROY_N.mesh(pos, 0.0, pose), rain_mesh(cam, tg, 120, 14)]
    if lt > th + 0.2:
        ms.append(smoke_sprites((pos[0], 0.3, pos[2]), lt, cam, n=5, size=0.25, rise=1.6, seed=12, alpha=0.6))
    return merge(ms), cam, storm_env(k, (pos[0], 2, pos[2])), dict(flash=screen_flash(lt, th))


ROY_BURNT_LEG = Human('roy', skin=SKIN, shirt=(170, 160, 122), pants=(70, 80, 55), shoes=(45, 32, 24), hair=HAIR,
                      hat='ranger', hat_col=(150, 118, 78), belt=(70, 48, 28), shirt_tex='uniform', pants_tex='burnt_leg')


def shot_leg(lt, dur, tg):
    cam = cam_lerp(Cam((0.42, 0.42, 0.8), (0.1, 0.1, 0.06), 55), Cam((0.36, 0.36, 0.68), (0.1, 0.08, 0.06), 55), lt / dur)
    ms = [TOWER.xf(trans(-0.8, 0, -4.0)), ROY_N.mesh((0, 0, 0), 0.0, dict())]
    # bande brûlée le long de la jambe droite (côté extérieur)
    ms.append(box(0.012, 0.8, 0.05, (25, 20, 18)).xf(trans(0.172, 0.1, 0.0)))
    ms.append(box(0.014, 0.75, 0.018, (170, 70, 45)).xf(trans(0.173, 0.12, 0.0)))
    # trou dans la chaussure droite
    ms.append(box(0.09, 0.012, 0.08, (15, 12, 10)).xf(trans(0.1, 0.085, 0.1)))
    ms.append(box(0.05, 0.014, 0.045, (225, 220, 205)).xf(trans(0.1, 0.086, 0.1)))
    ms.append(smoke_sprites((0.1, 0.1, 0.1), lt, cam, n=4, size=0.05, rise=0.4, seed=13, alpha=0.5))
    ms.append(rain_mesh(cam, tg, 60, 3))
    return merge(ms), cam, storm_env(0), {}


# ------------------------------------------------------------------ 3 : camion 1969
def road_scene(cliff=False):
    ms = []
    # route nord-sud (axe z)
    L, zc = (400, -100)
    ms.append(box(5.0, 0.02, L, (255, 255, 255), 'asphalt', ts=3.0).xf(trans(0, 0.0, zc)))
    ms.append(box(0.12, 0.025, L, (230, 220, 120), emis=0.2).xf(trans(0, 0.0, zc)))
    ms.append(grid(-60, -300, 60, 100, 10, 30, None, (255, 255, 255), 'grass', 3.0))
    ms.append(forest(-40, -300, 40, 100, 150, seed=23, avoid=[(0, z, 5.0) for z in range(-300, 101, 4)]))
    ms.append(grass_tufts(-18, -120, 18, 80, 1800, 5, avoid=lambda x, z: abs(x) < 2.8))
    return merge(ms)


ROAD = merge([road_scene(False), STORM_CLOUDS.xf(trans(0, 0, 0))])
ROAD_CLIFF = merge([cliff_scene(), cloud_bank(0, 40, 80, 300, 4, (60, 62, 72), 25, 16), cloud_bank(0, 35, -150, 300, 5, (50, 52, 62), 25, 16)])


HIT_TREE = deciduous(8, 2.6, seed=5)


def shot_truck_bolt(lt, dur, tg):
    """l'éclair frappe l'arbre puis entre au ralenti par la fenêtre ouverte"""
    th = WT(3, 'éclair') - T(3) + 0.05
    slow0, slow1, sf = th + 0.12, th + 1.3, 0.18

    def te_of(t):  # temps « ralenti »
        if t < slow0:
            return t
        if t < slow1:
            return slow0 + (t - slow0) * sf
        return slow0 + (slow1 - slow0) * sf + (t - slow1)
    te = te_of(lt)
    z = -20 + te * 9.0
    xt = 0.8
    zh = -20 + (slow0 + 0.08) * 9.0  # position du camion au moment de l'arc
    tree_pos = np.array([5.6, 0, zh + 0.8])
    win = np.array([xt + 0.95, 1.62, z + 0.05])
    head = np.array([xt + 0.45, 1.72, z + 0.1])
    if lt < th - 0.6:
        cam = Cam((7.5, 2.0, z + 7.0), (2.0, 1.6, z + 0.5), 55)
    else:
        cam = Cam((8.0, 2.3, zh - 8.0), (3.0, 2.5, zh + 0.2), 56)
    ms = [ROAD, HIT_TREE.xf(trans(tree_pos)), truck(wheel_rot=-te * 12).xf(trans(xt, 0, z))]
    face = 'roy' if lt < slow0 else 'roy_shock'
    ms.append(ROY_N.mesh((xt + 0.45, 0.5, z + 0.1), 0.0, sit_pose(la=(1.2, 0.1, 0.5), ra=(1.2, 0.1, 0.5), face=face,
                                                                   hy=0.0 if lt < th else 0.5)))
    k = 0.0
    # 1) l'éclair du ciel dans l'arbre
    if th <= lt < th + 0.18:
        top = tree_pos + np.array([3, 45, -10])
        ms.append(lightning_mesh(lightning_path(top, tree_pos + np.array([0, 7.5, 0]), seed=31, segs=22, jitter=0.05, branches=4), cam, 0.3))
        k = 1.0
    # 2) au ralenti : l'arc se propage de l'arbre jusqu'à la fenêtre et sa tête
    if slow0 <= lt < slow1:
        f = min(1.0, (lt - slow0) / ((slow1 - slow0) * 0.55))
        path = lightning_path(tree_pos + np.array([-0.3, 4.2, 0]), head, seed=32, segs=14, jitter=0.06, branches=0)[0]
        n = max(2, int(round(f * (len(path) - 1))) + 1)
        flick = 0.75 + 0.25 * math.sin(lt * 90)
        ms.append(lightning_mesh([path[:n]], cam, 0.12 * flick + 0.05))
        tip = path[n - 1]
        ms.append(billboard(tip, 0.5, 0.5, cam, (200, 220, 255), 'spark', alpha=0.9))
        k = 0.55 * flick
        if f >= 1.0:
            ms.append(billboard(head, 1.0, 1.0, cam, (220, 230, 255), 'spark', alpha=0.9))
            k = 0.9
    if lt > th:
        ms.append(fire_sprites(tree_pos + np.array([0, 5.5, 0]), te, cam, n=6, size=0.8, spread=0.6, seed=33))
        ms.append(smoke_sprites(tree_pos + np.array([0, 6.5, 0]), te, cam, n=5, size=1.2, rise=4, seed=34, alpha=0.5))
    if lt > slow1 - 0.3:
        ms.append(smoke_sprites(head + np.array([0, 0.2, 0]), lt, cam, n=5, size=0.18, rise=1.0, seed=35, alpha=0.6))
    ms.append(rain_mesh(cam, te + T(3), 120, 14))
    env = storm_env(k, tuple(head))
    if lt > th:
        env = env.copy()
        env.points = env.points + [(tuple(tree_pos + np.array([0, 5.5, 0])), (255, 150, 60), 1.2, 9)]
    fl = screen_flash(lt, th) + (0.25 if slow0 + (slow1 - slow0) * 0.55 <= lt < slow0 + (slow1 - slow0) * 0.55 + 0.05 else 0)
    return merge(ms), cam, env, dict(flash=fl)


def shot_truck_face(lt, dur, tg):
    """gros plan par la fenêtre ouverte : sourcils disparus"""
    cam = cam_lerp(Cam((3.1, 1.7, 0.6), (1.25, 1.66, 0.15), 45), Cam((2.8, 1.69, 0.5), (1.25, 1.66, 0.15), 45), lt / dur)
    ms = [ROAD, truck().xf(trans(0.8, 0, 0)),
          ROY_NB.mesh((1.25, 0.5, 0.1), 0.0, sit_pose(la=(1.2, 0.1, 0.5), ra=(1.2, 0.1, 0.5), hy=1.0 + 0.1 * math.sin(lt * 2),
                                                       face='roy_shock_nb' if lt < dur * 0.5 else 'roy_nobrow')),
          smoke_sprites((1.25, 1.95, 0.2), lt, cam, n=6, size=0.18, rise=1.0, seed=35, alpha=0.6)]
    return merge(ms), cam, storm_env(0), {}


def shot_cliff(lt, dur, tg):
    xt = 0.8
    z_stop = cliff_edge(xt) - 0.35 - 2.42
    u = ease(min(1, lt / (dur * 0.62)))
    zt = -24 + (z_stop + 24) * u
    late = max(0.0, lt - dur * 0.62)
    rock_ = math.sin(late * 14) * 0.035 * max(0, 1 - late * 1.6)
    # caméra « dans le vide » sous le bord : on voit la paroi et le camion qui s'arrête au ras du gouffre
    c0 = Cam((11.0, -0.5, 9.0), (0.8, -3.5, -2.5), 62)
    c1 = Cam((9.5, -1.5, 7.5), (0.8, -3.0, -2.5), 62)
    cam = cam_lerp(c0, c1, lt / dur)
    ms = [ROAD_CLIFF, truck(wheel_rot=-u * 30).xf(M(trans(xt, 0, zt), rotx(rock_)))]
    ms.append(ROY_NB.mesh((xt + 0.45, 0.5, zt + 0.1), 0.0, sit_pose(la=(1.2, 0.1, 0.5), ra=(1.2, 0.1, 0.5), face='roy_shock_nb')))
    # cailloux qui tombent du bord quand le camion s'arrête
    if late > 0:
        for i in range(6):
            d = late - i * 0.08
            if d > 0:
                x = xt - 0.6 + i * 0.25
                ms.append(box(0.15, 0.12, 0.15, (120, 110, 100), 'rock').xf(M(trans(x, -0.2 - 4.9 * d * d, cliff_edge(x) + 0.1 + d * 0.3), rotx(d * 6))))
    ms.append(rain_mesh(cam, tg, 80, 10))
    return merge(ms), cam, storm_env(0), {}


# ------------------------------------------------------------------ 4 : transformateur 1970
def yard_scene():
    ms = [grid(-40, -40, 40, 40, 10, 10, None, (255, 255, 255), 'grass', 3.0),
          house().xf(trans(-3, 0, -8)), utility_pole().xf(trans(4.5, 0, -2.0)), utility_pole(False).xf(trans(4.5, 0, -32)),
          utility_pole(False).xf(trans(4.5, 0, 28)),
          wires((5.4, 7.52, -2), (5.4, 7.52, -32)), wires((4.5, 7.52, -2), (4.5, 7.52, -32)), wires((3.6, 7.52, -2), (3.6, 7.52, -32)),
          wires((5.4, 7.52, -2), (5.4, 7.52, 28)), wires((4.5, 7.52, -2), (4.5, 7.52, 28)), wires((3.6, 7.52, -2), (3.6, 7.52, 28)),
          wires((4.5, 6.0, -1.7), (-1.0, 4.2, -5.0), sag=0.4),
          fence(-10, 6.5, 2, 6.5, 12), grass_tufts(-12, -6, 12, 6, 500, 4, avoid=lambda x, z: abs(x + 3) < 0.8, flowers=0.08), forest(-40, -40, 40, -14, 30, seed=41), STORM_CLOUDS, box(1.2, 0.02, 9, (190, 170, 140), 'gravel', ts=1.5).xf(trans(-3, 0, -0.5))]
    return merge(ms)


YARD = yard_scene()


def shot_transformer(lt, dur, tg):
    """1) la foudre frappe le transformateur  2) au ralenti, l'arc saute jusqu'à son épaule"""
    th = WT(4, 'frappe') - T(4) + 0.1
    tj = WT(4, 'saute') - T(4) - 0.2
    grow = 1.3   # durée de la propagation au ralenti
    rp = np.array([1.6, 0, -0.5])
    trans_pos = np.array([4.5, 5.9, -1.65])
    slow = tj <= lt < tj + grow + 0.4
    # temps ralenti pour la pluie et les étincelles
    if lt < tj:
        te = lt
    elif lt < tj + grow + 0.4:
        te = tj + (lt - tj) * 0.15
    else:
        te = tj + (grow + 0.4) * 0.15 + (lt - tj - grow - 0.4)
    cam = cam_lerp(Cam((-1.8, 1.4, 5.0), (3.0, 3.4, -1.2), 64), Cam((-1.4, 1.4, 4.4), (2.9, 3.2, -1.2), 64), lt / dur)
    ms = [YARD]
    pose = dict(hy=0.6, la=(0, 0.1, 0.1), ra=(0, 0.1, 0.1), face='roy')
    if th <= lt:
        pose.update(hy=0.75, hp=0.45, face='roy_shock')
    k = bolt_k(lt, th) * 0.8
    if bolt_vis(lt, th):
        ms.append(lightning_mesh(lightning_path(trans_pos + np.array([-4, 42, -10]), trans_pos + np.array([0, 0.8, 0]), seed=41, segs=22, jitter=0.05, branches=4), cam, 0.3))
    if lt > th:
        ms.append(fire_sprites(trans_pos + np.array([0, 0.9, 0]), te * 2, cam, n=4, size=0.35, spread=0.15, seed=42))
        for i in range(10):
            ph = (te * 1.5 + i * 0.13) % 1.0
            p = trans_pos + np.array([math.sin(i * 7) * ph * 1.2, 0.8 - ph * ph * 6, math.cos(i * 5) * ph * 1.2])
            ms.append(billboard(p, 0.1, 0.1, cam, (255, 255, 255), 'spark', alpha=1 - ph))
        # le transformateur grésille avant le saut
        if lt < tj + grow:
            for i in range(3):
                a = lt * 40 + i * 2.1
                ms.append(lightning_mesh(lightning_path(trans_pos + np.array([0, 0.3, 0.3]), trans_pos + np.array([0.5 * math.cos(a), -0.3, 0.5 * math.sin(a)]),
                                                        seed=int(lt * 30) + i, segs=4, jitter=0.2, branches=0), cam, 0.04))
    sh = rp + np.array([0.3 * math.cos(0.6) - 0.0, 1.45, -0.3 * math.sin(0.6)])
    if slow:
        f = min(1.0, (lt - tj) / grow)
        path = lightning_path(trans_pos + np.array([0, 0.1, 0.25]), sh, seed=43, segs=16, jitter=0.07, branches=0)[0]
        n = max(2, int(round(f * (len(path) - 1))) + 1)
        flick = 0.8 + 0.2 * math.sin(lt * 80)
        ms.append(lightning_mesh([path[:n]], cam, 0.11 * flick + 0.04))
        ms.append(billboard(path[n - 1], 0.45, 0.45, cam, (210, 225, 255), 'spark', alpha=0.95))
        k = max(k, 0.45 * flick)
        if f >= 1.0:
            ms.append(billboard(sh, 0.9, 0.9, cam, (220, 230, 255), 'spark', alpha=0.9))
            k = 0.9
    t_hit = tj + grow
    if lt >= t_hit:
        pose = hit_pose(lt, t_hit, pose)
        if lt > t_hit + 0.3:
            ms.append(smoke_sprites(sh, lt, cam, n=4, size=0.15, rise=0.8, seed=44, alpha=0.6))
            if lt > t_hit + 1.1:
                pose.update(la=(0.9, 0.6, 1.8), face='roy_shock')
    ms.append(ROY_N.mesh(tuple(rp), 0.6, pose))
    ms.append(rain_mesh(cam, te + T(4), 90, 12))
    fl = screen_flash(lt, th) + (0.3 if t_hit <= lt < t_hit + 0.05 else 0)
    return merge(ms), cam, storm_env(k, tuple(trans_pos)), dict(flash=fl)


# ------------------------------------------------------------------ 5 : cheveux 1972
INTERIOR = ranger_station_interior()
STATION_SCENE = merge([station_scene(), STORM_CLOUDS])
JACKET_HUNG = box(0.4, 0.6, 0.15, (150, 140, 105), 'uniform').xf(trans(-2.1, 1.1, 1.3))


def shot_hair_ext(lt, dur, tg):
    """le poste de garde sous l'orage : la foudre frappe l'antenne et le bâtiment"""
    th = WT(5, 'foudre') - T(5) + 0.05
    cam = cam_lerp(Cam((6.5, 2.3, 13.0), (-1.6, 3.6, 0.0), 60), Cam((5.8, 2.2, 12.0), (-1.6, 3.6, 0.0), 60), lt / dur)
    ms = [STATION_SCENE]
    ant = np.array([-3.2, 6.0, 2.0])
    m, k = strike(cam, lt, th, ant, top=ant + np.array([4, 40, -12]), seed=55, width=0.3)
    ms.append(m)
    # la décharge court le long du toit et rentre dans le bâtiment
    if th + 0.05 <= lt < th + 0.5:
        roof = [ant, np.array([-3.0, 4.0, 1.9]), np.array([-2.0, 3.6, 1.6]), np.array([-0.5, 3.4, 1.2]), np.array([-1.0, 1.7, 2.12])]
        ms.append(lightning_mesh([np.array(roof)], cam, 0.08))
    lit = (th <= lt < th + 0.5)
    if lit:
        ms.append(box(1.3, 1.0, 0.03, (200, 215, 255), emis=1.0).xf(trans(-1.0, 1.15, 2.13)))
    ms.append(rain_mesh(cam, tg, 120, 14))
    return merge(ms), cam, storm_env(k, tuple(ant)), dict(flash=screen_flash(lt, th))


def shot_hair(lt, dur, tg):
    th = 0.12
    cam = cam_lerp(Cam((-0.5, 1.6, 2.6), (0.7, 1.35, -1.0), 55), Cam((-0.3, 1.55, 2.2), (0.7, 1.4, -0.8), 55), lt / dur)
    ms = [INTERIOR, hat_mesh('ranger', (150, 118, 78)).xf(trans(-2.05, 1.85, 1.3))]
    k = bolt_k(lt, th) * 0.8
    env = ENV_INT.copy(points=[((0.0, 2.4, 0.0), (255, 230, 180), 0.4, 6)])
    if k > 0:
        env.points = env.points + [((-1.0, 1.6, -1.8), (200, 210, 255), 3.0 * k, 7)]
    pos = (0.8, 0, -0.75)
    if lt < th:
        pose = sit_pose(la=(1.2, 0.1, 0.6), ra=(1.2, 0.1, 0.6), hp=0.25, face='roy')
        ms.append(box(0.45, 0.45, 0.45, (110, 80, 50), 'planks').xf(trans(0.8, 0, -0.75)))
        ms.append(ROY_NOHAT.mesh(pos, math.pi, pose))
        ms.append(JACKET_HUNG)
    else:
        d = lt - th
        if bolt_vis(lt, th):
            ms.append(lightning_mesh(lightning_path((-1.0, 2.1, -1.95), (0.8, 1.7, -0.75), seed=56, segs=8, jitter=0.1, branches=1), cam, 0.06))
        jump = min(1, d / 0.3)
        pp = (0.8 - 0.3 * jump, 0, -0.75 + 1.2 * jump)
        flap = math.sin(d * 16)
        jk = box(0.35, 0.4, 0.04, (150, 140, 105), 'uniform').xf(M(rotx(1.2), trans(0, -0.1, 0)))
        pose = dict(la=(0.4, 0.3, 0.9), ra=(2.9 + 0.25 * flap, 0.2, 1.0 + 0.3 * flap), face='roy_shout', hp=-0.1)
        ms.append(ROY_NOHAT.mesh(pp, 0.25, dict(pose, hand_r=jk)))
        ms.append(box(0.45, 0.45, 0.45, (110, 80, 50), 'planks').xf(M(trans(0.8, 0, -0.75), rotz(min(1.4, d * 5)))))
        ms.append(fire_sprites((pp[0], 1.9, pp[2]), lt * 1.5, Cam(cam.pos, cam.at), n=7, size=0.28, spread=0.1, seed=51))
        ms.append(smoke_sprites((pp[0], 2.1, pp[2]), lt, cam, n=4, size=0.2, rise=0.6, seed=52, alpha=0.5))
        env.points = env.points + [((pp[0], 2.0, pp[2]), (255, 150, 60), 1.0, 3.5)]
    return merge(ms), cam, env, dict(flash=screen_flash(lt, th) * 0.4)


# ------------------------------------------------------------------ 6/7 : 1973
ROAD2 = merge([road_scene(False), cloud_bank(0, 32, -90, 160, 6, (32, 34, 42), 26, 16)])
ENV_HALF = Env(sky_top=(80, 110, 160), sky_hor=(170, 180, 190), fog=(150, 158, 170), fog_near=30, fog_far=220,
               light=(-0.4, 0.8, -0.5), amb=0.55)


def shot_flee(lt, dur, tg):
    z = lt * 11
    cam = Cam((-3.0, 2.2, z + 12.0), (0.5, 1.6, z - 4.0), 55)
    ms = [ROAD2, truck(wheel_rot=-lt * 14).xf(trans(0.8, 0, z)),
          ROY_N.mesh((1.25, 0.5, z + 0.1), 0.0, sit_pose(la=(1.2, 0.1, 0.5), ra=(1.2, 0.1, 0.5)))]
    return merge(ms), cam, ENV_HALF, {}


def shot_stop(lt, dur, tg):
    th = WT(6, 'trouve') - tl_start_of('stop')
    zt = 30.0
    cam = Cam((4.8, 1.5, zt + 4.0), (0.8, 1.7, zt - 1.5), 55)
    ms = [ROAD2, truck().xf(trans(0.8, 0, zt))]
    pos = np.array([2.3, 0, zt + 0.4])
    pose = dict(hy=1.2 if lt < th else 0, hp=0.4 if lt < th else 0, face='roy_smile' if lt < th else 'roy')
    if lt >= th:
        pose = hit_pose(lt, th, pose)
    m, k = strike(cam, lt, th, (pos[0], 1.85, pos[2]), top=(pos[0] + 6, 45, pos[2] - 25), seed=61)
    if lt < th:
        ms += [m, ROY_N.mesh(tuple(pos), 0.5, pose)]
    else:
        d = lt - th
        ms += [m, ROY_NOHAT.mesh(tuple(pos), 0.5, dict(pose, face='roy_shout' if d > 0.4 else pose.get('face')))]
        # cheveux en feu
        ms.append(fire_sprites(pos + np.array([0, 1.92, 0]), lt * 1.4, cam, n=6, size=0.26, spread=0.1, seed=63))
        # chapeau et chaussure qui volent
        hp_ = pos + np.array([0.5 * min(d, 0.9), 1.95 + 2.8 * d - 4.9 * d * d, 0.6 * min(d, 0.9)])
        hp_[1] = max(hp_[1], 0.02)
        ms.append(hat_mesh('ranger', (150, 118, 78)).xf(M(trans(hp_), rotz(min(d, 0.8) * 5))))
        sp = np.array([pos[0] + 0.1, 0.05 + 3.5 * d - 4.9 * d * d, pos[2] + 1.5 * d])
        sp[1] = max(sp[1], 0.05)
        ms.append(box(0.13, 0.08, 0.26, (45, 32, 24)).xf(M(trans(sp), rotx(d * 10))))
        ms.append(smoke_sprites((pos[0], 1.9, pos[2]), lt, cam, n=5, size=0.3, rise=1.4, seed=62, alpha=0.6))
    return merge(ms), cam, flash_env(ENV_HALF, k, (pos[0], 2, pos[2])), dict(flash=screen_flash(lt, th))


def shot_water(lt, dur, tg):
    """il prend le bidon à deux mains dans la benne, le lève au-dessus de sa tête et se verse l'eau dessus"""
    zt = 30.0
    pos = np.array([2.35, 0, zt - 1.6])   # à côté de la benne, côté conducteur, face au camion (-x)
    yaw = -math.pi / 2
    tp = WT(7, 'éteindre') - T(7) - 0.4
    ta, tb_ = tp * 0.3, tp * 0.85
    cam = cam_lerp(Cam((0.2, 2.5, zt - 4.4), (2.3, 1.75, zt - 1.6), 52), Cam((0.3, 2.45, zt - 4.0), (2.3, 1.85, zt - 1.6), 52), lt / dur)
    ms = [ROAD2, truck().xf(trans(0.8, 0, zt)), hat_mesh('ranger', (150, 118, 78)).xf(trans(3.4, 0.02, zt + 1.3))]
    head = pos + np.array([0, 1.75, 0])
    bed = np.array([1.35, 1.04, zt - 1.6])
    over = head + np.array([-0.3, 0.42, 0])
    # trajectoire du bidon
    if lt < ta:
        c, tilt = bed, 0.0
    elif lt < tb_:
        u = ease((lt - ta) / (tb_ - ta))
        mid = (bed + over) / 2 + np.array([0.2, 0.25, 0])
        c = (1 - u) ** 2 * bed + 2 * (1 - u) * u * mid + u * u * over
        tilt = 0.0
    else:
        c = over
        tilt = -min(1.0, (lt - tb_) / 0.5) * 1.9   # bascule vers la tête
    Mc = can_frame(c, tilt, 0.0)
    grip_a = (Mc @ np.array([0.0, 0.16, -0.15, 1]))[:3]
    grip_b = (Mc @ np.array([0.0, 0.16, 0.15, 1]))[:3]
    can = merge([box(0.14, 0.32, 0.25, (180, 40, 30), 'metal'), box(0.06, 0.06, 0.06, (60, 60, 60)).xf(trans(0.0, 0.32, 0.08)),
                 box(0.03, 0.03, 0.14, (60, 60, 60)).xf(trans(0, 0.36, -0.03))]).xf(Mc)
    ms.append(can)
    burning = lt < tp + 0.7
    face = 'roy_shout' if lt < tp else 'roy_closed'
    reach = lt < ta
    pose = dict(face=face, lean=0.35 if reach else 0.0)
    if reach:
        u = lt / max(ta, 0.1)
        pose['ik_l'] = (1 - u) * (pos + np.array([-0.25, 1.0, 0.3])) + u * grip_a
        pose['ik_r'] = (1 - u) * (pos + np.array([-0.25, 1.0, -0.3])) + u * grip_b
    else:
        pose['ik_l'], pose['ik_r'] = grip_a, grip_b
    if lt >= tb_:
        pose['hp'] = -0.2
    R_ = ROY_NOHAT if burning else ROY_NOHAT_B
    ms.append(R_.mesh(tuple(pos), yaw, pose))
    head = (R_.attach['head'] @ np.array([0, 0.2, 0, 1]))[:3]
    if burning:
        n = 6 if lt < tp else max(1, int(6 * (1 - (lt - tp) / 0.7)))
        ms.append(fire_sprites(head + np.array([0, 0.08, 0]), lt * 1.4, cam, n=n, size=0.26, spread=0.08, seed=71))
    if lt >= tb_ + 0.3:
        spout = (Mc @ np.array([0.0, 0.33, 0.08, 1]))[:3]
        d = lt - tb_ - 0.3
        for i in range(18):
            ph = (d * 2.2 + i / 18) % 1.0
            p = spout + np.array([0, -ph * 0.6, 0]) + np.array([math.sin(i * 1.7) * 0.05, 0, math.cos(i * 2.3) * 0.05]) * ph
            ms.append(billboard(p, 0.06, 0.12, cam, (160, 205, 255), 0, emis=0.6, alpha=0.75))
        for i in range(8):  # éclaboussures sur la tête et les épaules
            ph = (d * 2.5 + i / 8) % 1.0
            p = head + np.array([math.cos(i) * 0.25 * ph, 0.1 - ph * 0.9, math.sin(i) * 0.25 * ph])
            ms.append(billboard(p, 0.05, 0.08, cam, (170, 210, 255), 0, emis=0.6, alpha=0.7 * (1 - ph)))
    if lt >= tp:
        ms.append(smoke_sprites(head + np.array([0, 0.25, 0]), lt, cam, n=6, size=0.35, rise=1.8, seed=72, col=(240, 240, 240), alpha=0.7))
    return merge(ms), cam, ENV_HALF, {}


# ------------------------------------------------------------------ 8 : nuage 1976
CLOUD1 = cloud_bank(0, 0, 0, 10, 77, (45, 47, 55), 8, 4.5)
PARK2 = merge([trail_ground(), grass_tufts(-25, -40, 25, 15, 700, 1, avoid=lambda x, z: abs(x - 0.3 * math.sin(z * 0.15)) < 1.3, flowers=0.15), RIDGES, forest(-50, -60, 50, 25, 70, seed=4, avoid=[(0, -10, 3.0), (0, 0, 3), (0, 10, 3), (-3.5, 4, 2.5)])])


def shot_cloud_look(lt, dur, tg):
    cam = cam_lerp(Cam((1.7, 1.0, 3.6), (-0.3, 4.0, -3.0), 62), Cam((1.5, 0.9, 3.2), (-0.3, 4.6, -3.0), 62), lt / dur)
    ms = [PARK2, CLOUD1.xf(trans(-1 + lt * 0.6, 12, -6)), ROY_N.mesh((0, 0, 0), 0.4, dict(hp=0.55 * min(1, lt * 2), hy=-0.2, face='roy'))]
    env = ENV_SUN.copy(amb=0.5)
    return merge(ms), cam, env, {}


def shot_cloud_run(lt, dur, tg):
    th = WT(8, 'trop') - tl_start_of('cloud_run') + 0.05
    z = -lt * 4.2
    zz = min(z, -th * 4.2)
    cam = Cam((7.0, 1.4, zz + 8.0), (0, 5.0, zz - 1.0), 66)
    ms = [PARK2, CLOUD1.xf(trans(0.5 + (zz - z) * 0.0, 12, z - 1.5 + (lt * 0.3 if lt < th else th * 0.3)))]
    if lt < th:
        pose = run_pose(lt * 10, face='roy_shout')
        ms.append(ROY_N.mesh((0.3 * math.sin(z * 0.15), 0, z), math.pi, pose))
    else:
        pose = hit_pose(lt, th, dict())
        ms.append(ROY_N.mesh((0.3 * math.sin(zz * 0.15), 0, zz), math.pi, pose))
    m, k = strike(cam, lt, th, (0.3 * math.sin(zz * 0.15), 1.85, zz), top=(0.5, 11.5, zz - 1.5), seed=81)
    ms.append(m)
    if lt > th + 0.25:
        ms.append(fire_sprites((0.3 * math.sin(zz * 0.15), 1.95, zz), lt, cam, n=4, size=0.2, seed=82))
    return merge(ms), cam, flash_env(ENV_SUN.copy(amb=0.5), k, (0, 2, zz)), dict(flash=screen_flash(lt, th))


# ------------------------------------------------------------------ 9/10 : pêche 1977, ours
STREAM = merge([stream_ground(-40, -40, 40, 30, 0.0, 4.0), grass_tufts(-15, 3.2, 15, 15, 500, 2, flowers=0.1), grass_tufts(-15, -15, 15, -3.2, 400, 3), stream_bed(-40, 40, 4.0, 0.0),
                forest(-40, -40, 40, -6, 45, seed=91), forest(-40, 6, 40, 30, 15, seed=92), RIDGES])
ROD_LINE = None


def stringer_mesh(n=3, taken=0):
    ms = [cyl(0.01, 0.01, 0.5, 3, (200, 200, 200)).xf(M(rotz(math.pi / 2)))]
    for i in range(n - taken):
        ms.append(trout().xf(M(trans(-0.15 + i * 0.12, -0.15, 0), rotz(math.pi / 2))))
    return merge(ms)




def fishing_scene(lt, cam, roy_pose, roy_mesh_fn, rod=True, taken=0, darkness=0.0):
    ms = [STREAM]
    ms.append(box(0.4, 0.12, 0.3, (120, 110, 100), 'rock').xf(trans(STRINGER_POS[0], STRINGER_POS[1] - 0.1, STRINGER_POS[2])))
    ms.append(stringer_mesh(3, taken).xf(trans(STRINGER_POS + np.array([0, 0.2, 0]))))
    return ms


def shot_fish(lt, dur, tg):
    th = WT(9, 'éclair.') - T(9) - 0.25
    tb = WT(9, 'ours') - T(9) - 0.3
    cam = Cam((4.4, 1.1, 6.6), (0.9, 0.4, 0.8), 58)
    rp = on_ground(0.2, 2.6)
    rod = fishing_rod().xf(M(rotx(1.0)))
    dark = min(1.0, max(0, (lt - (th - 1.2)) / 1.0))
    env = ENV_SUN.copy()
    env.sky_top = ENV_SUN.sky_top * (1 - dark) + ENV_STORM.sky_top * dark
    env.sky_hor = ENV_SUN.sky_hor * (1 - dark) + ENV_STORM.sky_hor * dark
    env.fog = ENV_SUN.fog * (1 - dark) + ENV_STORM.fog * dark
    env.amb = 0.55 - 0.05 * dark
    env.light_col = ENV_SUN.light_col * (1 - dark) + ENV_STORM.light_col * dark
    ms = fishing_scene(lt, cam, None, None)
    if dark > 0:
        ms.append(STORM_CLOUDS.xf(trans(0, -10, 0)))
    if lt < th:
        pose = dict(ra=(0.9, 0.1, 0.4), la=(0.9, -0.1, 0.6), hy=0.0)
        ms.append(ROY_N.mesh(tuple(rp), math.pi * 0.95, dict(pose, hand_r=rod)))
    else:
        pose = hit_pose(lt, th, dict(ra=(0.9, 0.1, 0.4), la=(0.9, -0.1, 0.6)))
        if lt > tb + 0.6:
            pose.update(face='roy_shock', hy=0.5)
        ms.append(ROY_NOHAT.mesh(tuple(rp), math.pi * 0.95, dict(pose, hand_r=rod)))
        ms.append(fire_sprites(rp + np.array([0, 1.92, 0]), lt * 1.3, cam, n=6, size=0.24, spread=0.1, seed=91))
        d = lt - th
        hp_ = rp + np.array([0.6 * min(d, 1.5), 1.9 + 2.0 * min(d, 0.6) - 4.9 * min(d, 0.6) ** 2, 0.3 * min(d, 1.5)])
        hp_[1] = max(hp_[1], stream_h(hp_[0], hp_[2]) + 0.02)
        ms.append(hat_mesh('ranger', (150, 118, 78)).xf(M(trans(hp_), rotz(min(d, 0.9) * 4))))
    m, k = strike(cam, lt, th, rp + np.array([0, 1.85, 0]), seed=93)
    ms.append(m)
    if lt > tb:
        u = (lt - tb) / max(0.1, dur - tb)
        bp = bear_path(u * 0.92)
        nxt = bear_path(u * 0.92 + 0.02)
        yaw_b = math.atan2(nxt[0] - bp[0], nxt[2] - bp[2])
        ms.append(bear(phase=lt * 7, yaw=yaw_b, mouth=0.3 + 0.3 * math.sin(lt * 3)).xf(trans(bp)))
        if bp[2] < 1.6 and bp[2] > -1.6:  # éclaboussures dans le ruisseau
            for i in range(6):
                ph = (lt * 2 + i / 6) % 1
                ms.append(billboard(bp + np.array([math.cos(i * 2) * 0.6 * ph, 0.35 + ph * 0.4 - ph * ph * 0.8, math.sin(i * 2) * 0.6 * ph]), 0.15, 0.15, cam,
                                    (220, 235, 245), 'puff', emis=0.4, alpha=0.8 * (1 - ph)))
    return merge(ms), cam, flash_env(env, k, tuple(rp + np.array([0, 2, 0]))), dict(flash=screen_flash(lt, th))


def shot_bear_chase(lt, dur, tg):
    """l'ours se dresse et rugit, Roy recule un peu puis le chasse à coups de branche"""
    t_rear, t_fight = dur * 0.32, dur * 0.42
    cam = cam_lerp(Cam((4.6, 1.6, 7.6), (0.6, 1.0, 2.2), 62), Cam((4.3, 1.55, 7.2), (0.8, 1.0, 2.2), 62), lt / dur)
    ms = fishing_scene(lt, cam, None, None, taken=1)
    ms.append(STORM_CLOUDS.xf(trans(0, -10, 0)))
    flee = min(1, max(0, (lt - dur * 0.7) / (dur * 0.3)))
    bp0 = bear_path(0.92)
    if flee > 0:
        bp = bear_path(0.92 - flee * 0.9)
    else:
        bp = bp0
    rp = on_ground(-0.2 - 0.35 * min(1, lt / t_rear) + 0.7 * flee, 3.0 + 0.15 * min(1, lt / t_rear) - 0.3 * flee)
    face_b = math.atan2(rp[0] - bp[0], rp[2] - bp[2])
    if lt < t_fight:
        stand = min(1.0, lt / 0.4)
        ms.append(bear(phase=lt * 6, yaw=face_b, stand=stand, mouth=0.6 + 0.4 * math.sin(lt * 7)).xf(trans(bp)))
        # Roy recule, mains levées, un peu effrayé
        pose = dict(face='roy_shock', la=(1.3, 0.5, 1.6), ra=(1.3, 0.5, 1.6), lean=-0.15, hp=-0.2)
        if lt > t_rear:
            u = (lt - t_rear) / (t_fight - t_rear)
            pose = dict(face='roy_shout', lean=0.4 * u, ra=(0.3, 0.2, 0.2), la=(0.6, 0.4, 1.2))
            if u > 0.5:
                pose['ra'] = (2.2, 0.3, 0.3)
        ms.append(ROY_NOHAT_B.mesh(tuple(rp), math.atan2(bp[0] - rp[0], bp[2] - rp[2]), pose))
        if lt < t_rear + (t_fight - t_rear) * 0.5:
            ms.append(branch().xf(M(trans(rp + np.array([0.5, 0.03, -0.2])), rotz(math.pi / 2), roty(0.4))))
    else:
        swing = math.sin((lt - t_fight) * 9)
        br = branch().xf(M(rotx(1.4)))
        pose = dict(ra=(1.6 + 1.0 * swing, 0.3, 0.3 + 0.4 * max(0, swing)), la=(0.6, 0.4, 1.2), face='roy_shout', lean=0.15)
        ms.append(ROY_NOHAT_B.mesh(tuple(rp), math.atan2(bp[0] - rp[0], bp[2] - rp[2]), dict(pose, hand_r=br)))
        if flee <= 0:
            ms.append(bear(phase=lt * 6, yaw=face_b, stand=max(0, 1 - (lt - t_fight) * 2.5), mouth=0.8).xf(trans(bp)))
        else:
            nxt = bear_path(0.92 - flee * 0.9 - 0.03)
            yaw_r = math.atan2(nxt[0] - bp[0], nxt[2] - bp[2])
            ms.append(bear(phase=lt * 11, yaw=yaw_r, mouth=0.4).xf(trans(bp)))
            hd = bp + np.array([math.sin(yaw_r) * 1.45, 0.75, math.cos(yaw_r) * 1.45])
            ms.append(trout().xf(M(trans(hd), roty(yaw_r + math.pi / 2))))
    hd_ = (ROY_NOHAT_B.attach['head'] @ np.array([0, 0.28, 0, 1]))[:3]
    ms.append(fire_sprites(hd_, lt * 1.3, cam, n=6, size=0.24, spread=0.08, seed=101))
    env = ENV_STORM.copy(points=[(tuple(rp + np.array([0, 2.0, 0])), (255, 150, 60), 1.0, 4)])
    return merge(ms), cam, env, {}


# ------------------------------------------------------------------ 11 : collègues
def shot_colleagues(lt, dur, tg):
    tf = WT(11, "l'éviter") - T(11) - 0.2
    z = -lt * 1.2
    rz = z if lt < tf else -tf * 1.2
    cam = Cam((0.9, 1.6, rz - 6.0 - (lt - tf) * 0.2 * (lt > tf)), (0, 1.3, rz + 0.5), 55)
    ms = [PARK2, cloud_bank(-30, 45, -120, 120, 3, (70, 72, 82), 15, 14)]
    flash = (lt > tf - 0.4 and lt < tf - 0.3)
    if lt < tf:
        ms.append(ROY_N.mesh((0, 0, rz), math.pi, walk_pose(lt * 6)))
        ms.append(colleague('col1').mesh((1.0, 0, rz + 0.2), math.pi, walk_pose(lt * 6 + 1)))
        ms.append(colleague('col2', (165, 155, 118)).mesh((-1.0, 0, rz + 0.1), math.pi, walk_pose(lt * 6 + 2)))
    else:
        d = lt - tf
        ms.append(ROY_N.mesh((0, 0, rz), math.pi * 0.5 * min(1, d * 2) + math.pi * (1 - min(1, d * 2)) * 1.0, dict(face='roy', la=(0, 0.05, 0.05), ra=(0, 0.05, 0.05), hp=-0.1)))
        ms.append(colleague('col1_worry').mesh((1.0 + d * 2.6, 0, rz + 0.2 + d * 1.5), 2.2, walk_pose(d * 9, 1.2, hy=-0.9)))
        ms.append(colleague('col2', (165, 155, 118)).mesh((-1.0 - d * 2.8, 0, rz + 0.1 + d * 1.2), -2.0, walk_pose(d * 9 + 1, 1.2)))
    env = ENV_HALF.copy(sky_top=(70, 80, 100), sky_hor=(140, 145, 155), amb=0.5)
    if flash:
        env = flash_env(env, 0.5)
    if lt > tf - 0.4 and lt < tf - 0.32:
        ms.append(lightning_mesh(lightning_path((-30, 45, rz + 90), (-26, 5, rz + 90), seed=111, segs=10), cam, 0.6))
    return merge(ms), cam, env, {}


# ------------------------------------------------------------------ 12 : musée Guinness
def museum():
    ms = [box(14, 0.05, 10, (120, 30, 35), 'cloth', ts=2).xf(trans(0, -0.05, 0)),
          box(14, 4, 0.1, (40, 40, 60), faces='f').xf(trans(0, 0, -3)),
          box(0.1, 4, 10, (40, 40, 60), faces='r').xf(trans(-5, 0, 0)), box(0.1, 4, 10, (40, 40, 60), faces='l').xf(trans(5, 0, 0)),
          hat_case(True).xf(trans(-1.0, 0, -0.5)), hat_case(False).xf(trans(1.0, 0, -0.5))]
    # plaque dorée
    ms.append(box(1.2, 0.8, 0.05, (200, 170, 70), 'metal').xf(trans(0, 1.5, -2.92)))
    for i in range(4):
        ms.append(box(0.9 - i * 0.1, 0.05, 0.02, (90, 70, 30)).xf(trans(0, 2.05 - i * 0.12, -2.88)))
    # cordons
    for x in (-3, -1, 1, 3):
        ms.append(cyl(0.05, 0.05, 0.9, 6, (200, 170, 70), 'metal').xf(trans(x, 0, 1.2)))
    for x in (-2, 0, 2):
        ms.append(wires((x - 1, 0.85, 1.2), (x + 1, 0.85, 1.2), 0.15, (150, 20, 25), 6, 0.04))
    return merge(ms)


MUSEUM = museum()


def shot_museum(lt, dur, tg):
    cam = cam_lerp(Cam((-2.5, 1.6, 3.2), (-0.4, 1.2, -0.5), 50), Cam((2.0, 1.5, 2.6), (0.4, 1.15, -0.5), 50), lt / dur)
    env = ENV_MUSEUM.copy(points=[((-1, 3.2, -0.5), (255, 230, 180), 0.8, 4), ((1, 3.2, -0.5), (255, 230, 180), 0.8, 4)])
    return MUSEUM, cam, env, {}


# ------------------------------------------------------------------ 13 : fin
def shot_end(lt, dur, tg):
    th = WT(13, 'lui') - T(13)
    cam = cam_lerp(Cam((0.0, 1.6, 3.0), (0, 1.55, 0), 50), Cam((0.0, 1.62, 2.4), (0, 1.6, 0), 50), lt / dur)
    m, k = strike(cam, lt, th, (-4, 0, -12), top=(-6, 45, -30), seed=131, width=0.6)
    ms = [SUMMIT, m, ROY_N.mesh((0, 0, 0), 0.0, dict(face='roy_smile' if lt > 0.4 else 'roy', hp=0.0)), rain_mesh(cam, tg, 80, 8)]
    return merge(ms), cam, storm_env(k * 0.8, (-4, 3, -12)), dict(fade=max(0, (lt - dur + 0.4) / 0.4))


# ------------------------------------------------------------------ montage
SHOT_STARTS = {}


def add(name, t0, fn):
    SHOT_STARTS[name] = t0
    tl.add(t0, fn)


def tl_start_of(name):
    return SHOT_STARTS[name]


add('hook', 0.0, shot_hook)
add('hook2', WT(0, 'Cet') - 0.05, shot_hook2)
add('park', T(1), shot_park)
add('tower', T(2), shot_tower)
add('tower_hit', WT(2, 'La') - 0.1, shot_tower_hit)
add('leg', WT(2, 'brûle') - 0.05, shot_leg)
add('truck_bolt', T(3), shot_truck_bolt)
add('truck_face', WT(3, 'perd') - 0.15, shot_truck_face)
add('cliff', T(3, 17) - 0.1, shot_cliff)
add('transformer', T(4), shot_transformer)
add('hair_ext', T(5), shot_hair_ext)
add('hair', WT(5, 'Ses') - 0.1, shot_hair)
add('flee', T(6), shot_flee)
add('stop', WT(6, "s'arrête…") - 0.25, shot_stop)
add('water', T(7), shot_water)
add('cloud_look', T(8), shot_cloud_look)
add('cloud_run', WT(8, 'court…') - 0.2, shot_cloud_run)
add('fish', T(9), shot_fish)
add('bear', T(10), shot_bear_chase)
add('colleagues', T(11), shot_colleagues)
add('museum', T(12), shot_museum)
add('end', T(13), shot_end)

subs = Subs(timing)


# ------------------------------------------------------------------ audio
def build_audio(path):
    mx = A.Mixer(tl.duration())
    st = SHOT_STARTS
    tm = lambda name: st[name]
    rainx = A.rain(12)
    for a, b in (('hook', 'park'), ('tower', 'truck_face'), ('cliff', 'hair'), ('stop', 'water')):
        mx.add(rainx, tm(a), 0.3, 0.2, 0.3, length=tm(b) - tm(a))
    mx.add(A.wind(10), tm('hook'), 0.3, length=tm('park'))
    mx.add(A.birds(8), tm('park'), 0.6, 0.3, 0.4, length=tm('tower') - tm('park'))
    mx.add(A.footsteps(6, 2.2), tm('park'), 0.5, length=tm('tower') - tm('park'))
    # coups de foudre proches : claquement + boum + roulement
    hits = [WT(0, 'frapper') + 0.1, WT(0, '7') + 0.2, WT(0, 'foudre,') + 0.05, WT(2, 'foudre'), WT(3, 'éclair') + 0.05,
            WT(4, 'frappe') + 0.1, WT(5, 'foudre') + 0.05, WT(6, 'trouve'), WT(8, 'trop') + 0.05, WT(9, 'éclair.') - 0.25, WT(13, 'lui')]
    for i, h in enumerate(hits):
        mx.add(A.thunder_close(5.5, seed=i), h, 0.95 if i >= 3 else 0.8)
    mx.add(A.thunder_far(6, 1), tm('tower') + 0.3, 0.5)
    mx.add(A.thunder_far(6, 2), tm('flee') + 0.2, 0.45)
    mx.add(A.thunder_far(6, 3), WT(11, "l'éviter") - 0.6, 0.55)
    # arcs au ralenti
    mx.add(A.arc_buzz(1.4), WT(3, 'éclair') + 0.17, 0.6)
    mx.add(A.zap(), WT(3, 'éclair') + 0.17 + 1.18 * 0.55, 0.5)
    tj = WT(4, 'saute') - 0.2
    mx.add(A.arc_buzz(1.5), tj, 0.65)
    mx.add(A.zap(), tj + 1.3, 0.7)
    mx.add(A.zap(), tm('hair') + 0.12, 0.6)
    mx.add(A.engine_hum(8, 42), tm('truck_bolt'), 0.35, 0.2, 0.3, length=tm('transformer') - tm('truck_bolt') - 1.0)
    mx.add(A.fire_crackle(4), WT(4, 'frappe'), 0.35, 0, 0.5, length=tm('hair_ext') - WT(4, 'frappe') - 0.3)
    mx.add(A.fire_crackle(4), tm('hair') + 0.12, 0.5, 0, 0.3, length=tm('flee') - tm('hair'))
    mx.add(A.engine_hum(8, 50), tm('flee'), 0.4, 0.2, 0.4, length=tm('stop') - tm('flee') + 0.5)
    mx.add(A.fire_crackle(4), WT(6, 'trouve'), 0.45, 0, 0.3, length=WT(7, 'éteindre') - 0.4 + 0.6 - WT(6, 'trouve'))
    mx.add(A.clank(0.4), tm('water') + 0.4, 0.3)
    mx.add(A.splash(2.0), WT(7, 'éteindre') - 0.4, 0.7)
    mx.add(A.stream(10), tm('fish'), 0.4, 0.3, 0.3, length=tm('colleagues') - tm('fish'))
    mx.add(A.birds(4), tm('fish'), 0.4, 0.2, 0.5, length=2.5)
    mx.add(A.splash(0.8), WT(9, 'ours') + 0.4, 0.4)
    mx.add(A.growl(1.3), WT(9, 'ours') + 0.6, 0.6)
    mx.add(A.fire_crackle(4), WT(9, 'éclair.'), 0.35, 0, 0.3, length=tm('colleagues') - WT(9, 'éclair.'))
    mx.add(A.roar(1.8), tm('bear') + 0.15, 0.8)
    d_b = tm('colleagues') - tm('bear')
    for k in range(4):
        t0 = tm('bear') + d_b * 0.42 + k * 0.7
        mx.add(A.whoosh(0.3), t0 - 0.15, 0.3)
        mx.add(A.thwack(), t0, 0.55)
    mx.add(A.growl(1.0), tm('bear') + d_b * 0.7, 0.5)
    mx.add(A.splash(1.0), tm('bear') + d_b * 0.8, 0.4)
    mx.add(A.wind(6), tm('colleagues'), 0.25, 0.3, 0.3, length=tm('museum') - tm('colleagues'))
    mx.add(A.footsteps(4, 4), WT(11, "l'éviter") - 0.2, 0.4, length=2.0)
    mx.add(A.sting(), tm('museum') + 0.2, 0.5)
    mx.add(A.rain(5), tm('end'), 0.3, 0.2, 0.4, length=tl.duration() - tm('end'))
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
        contact_sheet(tl, times[:30], os.path.join(HERE, 'sheet1.png'), subs, cols=6, scale=0.18)
        contact_sheet(tl, times[30:], os.path.join(HERE, 'sheet2.png'), subs, cols=6, scale=0.18)
    elif len(sys.argv) > 1 and sys.argv[1] == '--at':
        for s in sys.argv[2:]:
            frame(tl, float(s), subs).resize((540, 960)).save(os.path.join(HERE, f'at_{s}.png'))
    else:
        build_audio(os.path.join(HERE, 'sfx.wav'))
        mix_voice(os.path.join(HERE, 'voix.wav'), os.path.join(HERE, 'sfx.wav'), os.path.join(HERE, 'mix.wav'))
        render_video(tl, os.path.join(HERE, 'roy.mp4'), os.path.join(HERE, 'mix.wav'), subs)
