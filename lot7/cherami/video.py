"""Ép. 26 — Cher Ami, le pigeon du « bataillon perdu » (Les animaux héros) : Argonne, octobre 1918."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n/lot7']
from props7 import *
from video_core import *

HERE = '/home/claude/g2n/lot7/cherami'
timing = load_timing(os.path.join(HERE, 'timing.json'))
tl = Timeline(timing)
T, WT = tl.T, tl.word_t
END = timing[-1]['t1'] + 0.3
tl.duration = lambda: END
cut = Cut(tl)

# ------------------------------------------------------------------ personnages
FACES = [('gi1', (226, 186, 150), (90, 65, 40), False), ('gi2', (200, 155, 120), (40, 30, 25), True), ('gi3', (232, 196, 165), (150, 110, 60), False),
         ('gi4', (150, 105, 75), (25, 20, 18), False), ('gi5', (220, 178, 140), (60, 45, 30), True)]
for n, sk, hc, mu in FACES:
    make_face(n, skin=sk, hair_col=hc, mustache=mu)
make_face('major', skin=(228, 192, 160), hair_col=(70, 55, 40))
make_face('ger', skin=(225, 185, 150), mustache=True, hair_col=(140, 110, 70))
make_face('medic', skin=(230, 192, 160), hair_col=(100, 75, 50))
make_face('sci', skin=(215, 170, 135), hair_col=(40, 30, 25))
make_face('visit', skin=(235, 200, 175), hair_col=(160, 110, 60))
OD = (255, 255, 255)


def gi(i, helmet=True):
    n, sk, hc, _ = FACES[i % len(FACES)]
    return Human(n, skin=sk, shirt=OD, shirt_tex='olive', pants=OD, pants_tex='olive', hair=hc, shoes=(70, 50, 35), belt=(120, 95, 60),
                 hat='brodie' if helmet else None, hat_col=(88, 92, 60))


GIS = [gi(i) for i in range(5)]
MAJOR = Human('major', skin=(228, 192, 160), shirt=OD, shirt_tex='olive', pants=OD, pants_tex='olive', hair=(70, 55, 40), belt=(110, 80, 50),
              hat='brodie', hat_col=(88, 92, 60), jacket=(95, 92, 62), tie=(70, 60, 40))
GER = Human('ger', skin=(225, 185, 150), shirt=OD, shirt_tex='feldgrau', pants=OD, pants_tex='feldgrau', hair=(140, 110, 70), hat='stahl', hat_col=(100, 105, 95),
            belt=(40, 35, 30), shoes=(30, 28, 26))
HANDLER = gi(2, helmet=False)
MEDIC = Human('medic', skin=(230, 192, 160), shirt=(235, 232, 220), pants=OD, pants_tex='olive', hair=(100, 75, 50), jacket=(238, 236, 228))
SCI = Human('sci', skin=(215, 170, 135), shirt=(200, 210, 230), pants=(50, 55, 70), hair=(40, 30, 25), jacket=(245, 245, 242))
VISIT = Human('visit', skin=(235, 200, 175), shirt=(150, 60, 70), pants=(50, 60, 90), hair=(160, 110, 60), robe=(140, 55, 65), extra=C2.woman_extra('bun', hair=(160, 110, 60)))

# ------------------------------------------------------------------ ambiances
ENV_FOREST = Env(sky_top=(120, 130, 140), sky_hor=(185, 180, 165), fog=(150, 145, 130), fog_near=10, fog_far=110, amb=0.55, light=(-0.4, 0.8, 0.3), light_col=(240, 225, 200))
ENV_SMOKE = ENV_FOREST.copy(fog=(120, 112, 100), fog_near=5, fog_far=70, amb=0.5, sky_hor=(150, 140, 120))
ENV_SKY = Env(sky_top=(80, 115, 170), sky_hor=(200, 200, 195), fog=(185, 185, 180), fog_near=60, fog_far=700, amb=0.55, light=(-0.4, 0.8, 0.4))
ENV_DUSK = Env(sky_top=(60, 60, 110), sky_hor=(240, 150, 90), fog=(200, 140, 100), fog_near=40, fog_far=500, amb=0.5, light=(-0.6, 0.4, -0.6), light_col=(255, 190, 130))
ENV_TENT = Env(sky_top=(70, 66, 55), sky_hor=(70, 66, 55), fog=(60, 56, 48), fog_near=8, fog_far=35, amb=0.62, light=(0.3, 0.85, 0.4), light_col=(255, 235, 200))
ENV_ARCH = Env(sky_top=(50, 48, 45), sky_hor=(50, 48, 45), fog=(45, 42, 38), fog_near=6, fog_far=26, amb=0.55, light=(0.2, 0.9, 0.3), light_col=(255, 230, 190))
ENV_MUSEUM = Env(sky_top=(70, 72, 78), sky_hor=(70, 72, 78), fog=(60, 62, 68), fog_near=10, fog_far=40, amb=0.6, light=(0.2, 0.9, 0.3),
                 points=[((0, 2.6, 0), (255, 245, 225), 0.6, 4)])
ENV_LAB = Env(sky_top=(60, 70, 85), sky_hor=(60, 70, 85), fog=(50, 58, 70), fog_near=8, fog_far=30, amb=0.6, light=(0.3, 0.9, 0.3), light_col=(230, 240, 255))


# ------------------------------------------------------------------ la forêt d'Argonne (ravin de Charlevaux)
def hground(x, z):
    """ravin : fond à y=0 le long de z, pentes de part et d'autre"""
    return 0.06 * x * x + 0.3 * math.sin(z * 0.2) * 0.3


def forest(seed=1, emu=False):
    rr = np.random.default_rng(seed)
    ms = [grid(-40, -60, 40, 60, 24, 30, hground, (255, 255, 255), 'mud', 3.0)]
    for i in range(70):
        x, z = rr.uniform(-38, 38), rr.uniform(-58, 58)
        if abs(x) < 2.0 and -12 < z < 12:
            continue
        y = hground(x, z)
        if rr.random() < 0.65:
            ms.append(deciduous(rr.uniform(7, 11), rr.uniform(2.2, 3.4), int(rr.integers(0, 99)), (255, 255, 255), 'leaves_autumn').xf(trans(x, y - 0.1, z)))
        else:
            ms.append(deciduous(rr.uniform(6, 9), rr.uniform(0.6, 1.2), int(rr.integers(0, 99)), (120, 100, 70), 'bark').xf(trans(x, y - 0.1, z)))   # arbres déchiquetés
    for i in range(30):   # troncs couchés, rochers, souches
        x, z = rr.uniform(-12, 12), rr.uniform(-25, 25)
        y = hground(x, z)
        if i % 3 == 0:
            ms.append(cyl(0.18, 0.15, rr.uniform(2, 4), 6, (110, 80, 50), 'bark').xf(M(trans(x, y + 0.15, z), rotz(math.pi / 2), roty(rr.uniform(0, 3)))))
        else:
            ms.append(rock(rr.uniform(0.3, 0.8), i, (150, 140, 125)).xf(trans(x, y - 0.1, z)))
    ms.append(grass_tufts(-14, -30, 14, 30, 160, 3, hfun=hground, col=(130, 110, 60), h=0.3))
    # trous individuels (« foxholes ») : bourrelets de terre sur la pente
    for (x, z) in HOLES:
        y = hground(x, z)
        ms.append(box(1.4, 0.25, 0.35, (95, 75, 52), 'mud').xf(M(trans(x, y, z + 0.6), roty(0.1))))
        ms.append(box(0.35, 0.22, 1.2, (95, 75, 52), 'mud').xf(trans(x + 0.6, y, z)))
    if emu:   # l'émeu à chapeau, planté entre deux arbres sur la pente
        ms.append(emu_mesh((3.8, hground(3.8, -4) - 0.05, -4), -0.6, peck=0.0, look=0.3))
    return merge(ms)


HOLES = [(-2.4, 2.0), (-3.0, -1.5), (2.6, 1.0), (3.2, -2.5), (-2.0, 5.5), (2.4, 5.0), (-3.4, -5.0)]
FOREST = forest(1)
FOREST_EMU = forest(1, emu=True)


def on_ground(x, z):
    return (x, hground(x, z), z)


def crouch(**kw):
    p = dict(drop=0.45, ll=(1.6, 2.3), rl=(1.2, 2.0), lean=0.35, la=(0.9, 0.15, 1.0), ra=(0.9, 0.15, 1.0))
    p.update(kw)
    return p


def soldiers_in_ravine(tg, duck=0.0):
    ms = []
    for k, (x, z) in enumerate(HOLES):
        yaw = math.atan2(-x, 0.5) if k % 2 else math.atan2(-x, -0.3)
        ms.append(GIS[k % 5].mesh(on_ground(x, z), yaw, crouch(hp=0.4 * duck - 0.2, lean=0.35 + 0.4 * duck, hy=0.3 * math.sin(tg * 0.7 + k))))
    return merge(ms)


def shell_fx(pos, age, cam, size=1.0, seed=0):
    """explosion d'obus : éclair + gerbe de terre + fumée"""
    if age < 0 or age > 2.2:
        return Mesh()
    rr = np.random.default_rng(seed)
    p = np.asarray(pos, float)
    ms = []
    if age < 0.15:
        ms.append(billboard(p + np.array([0, 1.0 * size, 0]), 3 * size, 3 * size, cam, (255, 220, 140), 'fire', emis=1.0))
    k = min(1.0, age / 0.4)
    for i in range(12):
        o = rr.normal(size=3) * np.array([1.2, 0, 1.2]) * size
        yy = (5 * k * rr.uniform(0.4, 1.0) - max(0, age - 0.6) * 3) * size
        if yy < 0:
            continue
        s = (1.2 + rr.random()) * size
        ms.append(billboard(p + o + np.array([0, yy, 0]), s, s, cam, (110, 90, 70), 'puff', emis=0.2, alpha=0.9 * max(0, 1 - age / 2.2)))
    return merge(ms)


def shells(lt, cam, t0s, spots):
    return merge([shell_fx(spots[i % len(spots)], lt - t0, cam, 1.0, i) for i, t0 in enumerate(t0s)])


def pigeon_flying(tg, pos, yaw, pitch=0.0, hurt=False, scale_=1.0):
    return pigeon(tg * 22, leg_hurt=hurt).xf(M(trans(pos), roty(yaw), rotx(-pitch), scale(scale_)))


# ------------------------------------------------------------------ 0. accroche
def shot_hook(lt, dur, tg, p=None):
    """gros plan : Cher Ami vole à travers la fumée, la patte blessée, la capsule pend"""
    p = lt if p is None else p
    z = 5.0 * p
    pos = np.array([0.0, 3.2 + 0.08 * math.sin(tg * 6), z])
    cam = Cam(tuple(pos + np.array([0.75, 0.15, 0.6])), tuple(pos + np.array([0, 0.02, 0.05])), 48)
    ms = [FOREST.xf(trans(0, 0, 0)), pigeon_flying(tg, pos, 0.0, 0.05, hurt=True)]
    ms.append(smoke_sprites((0.6, 2.4, z + 2), tg, cam, n=5, size=1.5, rise=2, seed=3, col=(150, 140, 125), drift=(0.6, 0, 0), alpha=0.6))
    ms.append(shell_fx((3.0, hground(3, z - 6), z - 6), (lt % 1.6), cam, 1.0, 1))
    fl = C2.decay(lt % 1.6, 0.0, 6)
    return merge(ms), C2.shake(cam, 0.03 + 0.05 * fl, tg), ENV_SMOKE, dict(flash=0.25 * fl, flash_col=(255, 210, 150))


def shot_hook_soldiers(lt, dur, tg):
    """au fond du ravin, les soldats lèvent les yeux vers le pigeon"""
    cam = Cam((0.5, 1.3, 7.5), (0, 1.6, 0), 55)
    ms = [FOREST, soldiers_in_ravine(tg), pigeon_flying(tg, (0.4, 5 + lt * 2, 1 - lt * 3), math.pi, 0.4, scale_=1.6),
          shells(lt, cam, [0.3], [(-5, hground(-5, -6), -6)])]
    return merge(ms), C2.shake(cam, 0.03, tg), ENV_SMOKE, {}


# ------------------------------------------------------------------ 1. Cher Ami, pigeon voyageur
def loft_m():
    """colombier mobile de l'armée : caisse sur roues, toit à deux pans, planche d'envol"""
    ms = [box(5.0, 2.2, 2.2, (255, 255, 255), 'planks_green', ts=1.5).xf(trans(0, 0.8, 0)),
          Mesh([[(-2.6, 3.0, -1.2), (2.6, 3.0, -1.2), (2.6, 3.8, 0)], [(-2.6, 3.0, -1.2), (2.6, 3.8, 0), (-2.6, 3.8, 0)],
                [(-2.6, 3.8, 0), (2.6, 3.8, 0), (2.6, 3.0, 1.2)], [(-2.6, 3.8, 0), (2.6, 3.0, 1.2), (-2.6, 3.0, 1.2)]], C((120, 70, 50)))]
    ms.append(Mesh([[(-2.5, 3.0, -1.1), (-2.5, 3.0, 1.1), (-2.5, 3.75, 0)], [(2.5, 3.0, -1.1), (2.5, 3.75, 0), (2.5, 3.0, 1.1)]], C((90, 110, 75))))
    ms.append(box(4.6, 0.06, 0.5, (150, 120, 80)).xf(trans(0, 2.35, 1.3)))       # planche d'envol
    for x in np.arange(-2.0, 2.1, 0.8):
        ms.append(box(0.4, 0.35, 0.05, (30, 28, 25)).xf(trans(x, 2.42, 1.11)))  # trappes
    ms.append(box(0.9, 1.4, 0.05, (255, 255, 255), 'door').xf(trans(-1.8, 0.85, 1.11)))
    ms.append(box(0.5, 0.5, 0.05, (230, 230, 225)).xf(trans(1.6, 1.4, 1.11)))   # croix rouge -> non : plaque blanche
    for x in (-1.8, 1.8):
        for s in (-1, 1):
            ms.append(wheel(0.45, 0.2).xf(M(trans(x, 0.45, s * 1.2))))
    return merge(ms)


LOFT = loft_m()


def camp():
    rr = np.random.default_rng(4)
    ms = [ground(-60, -60, 60, 60, 'grass_dry', ts=4.0), LOFT]
    for i in range(14):
        ms.append(deciduous(rr.uniform(7, 10), rr.uniform(2.4, 3.2), i, (255, 255, 255), 'leaves_autumn').xf(trans(rr.uniform(-40, 40), 0, rr.uniform(-45, -12))))
    ms.append(box(4, 2.2, 3, (150, 140, 110), 'cloth').xf(trans(8, 0, -3)))               # tente
    for k in range(6):
        ms.append(box(0.6, 0.45, 0.4, (150, 120, 80)).xf(trans(4 + (k % 3) * 0.65, (k // 3) * 0.45, 2.5)))
    ms.append(pigeon_basket(2).xf(trans(2.2, 0, 2.0)))
    return merge(ms)


CAMP = camp()


def shot_intro(lt, dur, tg):
    """un soldat tient Cher Ami à deux mains devant le colombier, face à la caméra"""
    c = np.array([2.6, 0.0, 4.2])
    hold = c + np.array([0, 1.22, 0.4])
    pose = dict(ik_l=tuple(hold + np.array([-0.08, -0.03, 0])), ik_r=tuple(hold + np.array([0.08, -0.03, 0])), hp=0.2)
    bird = pigeon(pose='stand', capsule=True).xf(M(trans(hold + np.array([0, 0.03, 0.02])), roty(0.3 * math.sin(tg * 1.5))))
    cam = cam_lerp(Cam(tuple(c + np.array([0.7, 1.45, 2.3])), tuple(hold + np.array([0, 0.05, 0])), 44), Cam(tuple(c + np.array([0.5, 1.4, 1.7])), tuple(hold + np.array([0, 0.05, 0])), 40), lt / dur)
    return merge([CAMP, HANDLER.mesh(tuple(c), 0.0, pose), bird]), cam, ENV_SKY, {}


def shot_loft(lt, dur, tg):
    """le colombier mobile de l'armée, des pigeons tournent autour"""
    cam = cam_lerp(Cam((6, 2.0, 9), (0, 2.2, 0), 50), Cam((5.2, 2.0, 8), (0, 2.3, 0), 48), lt / dur)
    ms = [CAMP]
    for k in range(5):
        a = tg * 1.2 + k * 1.25
        ms.append(pigeon_flying(tg + k * 0.3, (3.5 * math.cos(a), 4.0 + 0.5 * math.sin(a * 2), 2 + 3.5 * math.sin(a)), -a, 0.0, scale_=1.4))
    for k in range(4):
        ms.append(pigeon(pose='stand', capsule=False).xf(M(trans(-1.5 + k * 0.9, 2.38, 1.3), roty(0.3 * k))))
    return merge(ms), cam, ENV_SKY, {}


# ------------------------------------------------------------------ 2-5. encerclés, pas de radio
def shot_forest(lt, dur, tg):
    """la forêt d'Argonne en octobre : brouillard, arbres déchiquetés (un émeu à chapeau traîne entre les arbres)"""
    u = lt / max(dur, 0.1)
    cam = Cam((-6 + 3 * u, 4.5, 16 - 2 * u), (2, 2.0, -6), 50)
    leaves = C2.particles((0, 4, 4), tg, cam, 30, (8, 5, 8), 0.8, 0.12, (190, 120, 50), seed=2, spin=True)
    return merge([FOREST_EMU, soldiers_in_ravine(tg), leaves]), cam, ENV_FOREST, {}


def ger_line(tg, aim=False):
    ms = []
    for k, (x, z) in enumerate([(9.5, -3), (10.5, 1), (-10, 0), (-9.5, 4), (9.8, 5), (-10.5, -4)]):
        yaw = math.atan2(-x, 0)
        pose = dict(ik_r=None) if not aim else dict(ra=(1.5, 0.0, 0.1), la=(1.4, -0.3, 0.4), hp=0.2)
        ms.append(GER.mesh(on_ground(x, z), yaw, pose))
        if aim:
            ms.append(rifle().xf(M(trans(x, hground(x, z), z), roty(yaw), trans(0.15, 1.42, 0.35))))
    return merge(ms)


def rifle():
    return merge([box(0.05, 0.08, 1.1, (90, 65, 40)), box(0.03, 0.03, 0.5, (50, 50, 52)).xf(trans(0, 0.05, 0.45))])


def shot_encircled(lt, dur, tg):
    """vue plongeante : le bataillon au fond du ravin, les Allemands sur les crêtes des deux côtés"""
    u = lt / max(dur, 0.1)
    cam = Cam((0, 16 - 2 * u, 14), (0, 0, -1), 50)
    return merge([FOREST, soldiers_in_ravine(tg), ger_line(tg)]), cam, ENV_FOREST, {}


def shot_basket(lt, dur, tg):
    """pas de radio : le major griffonne un message ; à côté, la cage des pigeons"""
    c = np.array([-2.4, hground(-2.4, 2.0), 2.0])
    pose = crouch(hp=0.6, ik_r=tuple(c + np.array([0.15, 0.62, 0.45])), ik_l=tuple(c + np.array([-0.15, 0.62, 0.45])))
    note = box(0.2, 0.01, 0.14, (255, 255, 255), 'note').xf(M(trans(c + np.array([0, 0.6, 0.45])), rotx(-0.3)))
    bk = pigeon_basket(3).xf(trans(c + np.array([0.9, 0.0, 0.5])))
    cam = cam_lerp(Cam(tuple(c + np.array([1.6, 1.3, 2.4])), tuple(c + np.array([0.4, 0.5, 0.3])), 48), Cam(tuple(c + np.array([1.4, 1.2, 2.1])), tuple(c + np.array([0.4, 0.5, 0.3])), 46), lt / dur)
    return merge([FOREST, MAJOR.mesh(tuple(c), 0.0, pose), note, bk]), cam, ENV_FOREST, {}


def shot_name(lt, dur, tg):
    """gros plan sur Cher Ami dans sa cage (retiens son nom)"""
    c = np.array([-1.5, hground(-1.5, 2.5), 2.5])
    bk = pigeon_basket(0).xf(trans(c))
    p = pigeon(pose='stand', capsule=False).xf(M(trans(c + np.array([0, 0.52, 0.05])), roty(0.5 + 0.2 * math.sin(tg * 1.7))))
    cam = cam_lerp(Cam(tuple(c + np.array([0.45, 0.75, 0.85])), tuple(c + np.array([0, 0.55, 0.05])), 40), Cam(tuple(c + np.array([0.32, 0.7, 0.62])), tuple(c + np.array([0, 0.55, 0.05])), 38), lt / dur)
    return merge([FOREST, bk, p]), cam, ENV_FOREST, dict(post_pil=lambda im: C2.vignette(im, 0.6))


# ------------------------------------------------------------------ 6-7. les obus… américains
SPOTS = [(-2, hground(-2, 0), 0.5), (3, hground(3, 3), 3), (-1, hground(-1, -4), -4), (2, hground(2, -1), -1)]


def shot_shells(lt, dur, tg):
    cam = Cam((5, 3.0, 11), (0, 1, 0), 52)
    ms = [FOREST, soldiers_in_ravine(tg, duck=1.0), shells(lt, cam, [0.15, 0.7, 1.2, 1.7], SPOTS)]
    fl = max([C2.decay(lt, t, 7) for t in (0.15, 0.7, 1.2, 1.7)])
    return merge(ms), C2.shake(cam, 0.12 * fl, tg), ENV_SMOKE, dict(flash=0.4 * fl, flash_col=(255, 210, 150))


def field_gun(recoil=0.0):
    ms = [cyl(0.06, 0.06, 2.4, 8, (70, 74, 60)).xf(M(trans(0, 1.0, -0.3 - recoil), rotx(math.pi / 2 - 0.25))),
          box(1.4, 1.0, 0.06, (80, 84, 66)).xf(M(trans(0, 0.8, 0.1), rotx(-0.1))), box(0.3, 0.3, 1.6, (75, 78, 62)).xf(M(trans(0, 0.35, -1.2), rotx(0.15)))]
    for s in (-1, 1):
        ms.append(wheel(0.6, 0.12, 0.0, rim=(110, 90, 60), tyre=(80, 60, 40)).xf(trans(s * 0.75, 0.6, 0)))
    return merge(ms)


def shot_artillery(lt, dur, tg):
    """à des kilomètres, une batterie de canons américains tire… sur leurs propres hommes"""
    ms = [ground(-80, -80, 80, 80, 'grass_dry', ts=4.0)]
    cam = Cam((-6, 1.8, 7), (2, 1.2, -2), 50)
    for k in range(3):
        t_f = 0.2 + k * 0.45
        rec = 0.35 * C2.decay(lt, t_f, 8) if lt > t_f else 0
        x = k * 4.0
        ms.append(field_gun(rec).xf(trans(x, 0, 0)))
        ms.append(GIS[k].mesh((x + 1.0, 0, -1.2), -0.3, dict(ra=(0.3, 0.1, 0.2), la=(1.4, 0.3, 1.6))))
        if 0 <= lt - t_f < 0.12:
            ms.append(billboard((x, 1.6, 2.0), 2.0, 2.0, cam, (255, 220, 140), 'fire', emis=1.0))
        if lt > t_f:
            ms.append(smoke_sprites((x, 1.4, 2.0), tg, cam, n=4, size=1.5, rise=2, seed=k, col=(190, 185, 175), drift=(0.5, 0, 0.3), alpha=0.6))
    for k in range(5):
        ms.append(box(0.3, 0.3, 0.6, (150, 120, 80)).xf(trans(-2 + k * 0.35, 0, -2)))
    fl = max([C2.decay(lt, 0.2 + k * 0.45, 9) if lt > 0.2 + k * 0.45 else 0 for k in range(3)])
    return merge(ms), C2.shake(cam, 0.08 * fl, tg), ENV_SKY.copy(sky_hor=(200, 190, 170)), {}


# ------------------------------------------------------------------ 8-11. les pigeons abattus, le dernier
def release_shot(lt, dur, tg, seed):
    """un soldat lâche un pigeon ; il monte… et tombe, abattu"""
    t_hit = WT(8 if seed == 0 else 9, 'Abattu') - cut['rel1' if seed == 0 else 'rel2'] + 0.05
    c = np.array([2.6, hground(2.6, 1.0), 1.0])
    rel = min(1.0, lt / 0.25)
    pose = crouch(ra=(2.8, 0.2, 0.1), la=(2.6, 0.2, 0.1), lean=0.0, hp=-0.6)
    up = max(0.0, lt - 0.1)
    if lt < t_hit:
        pp = c + np.array([0.1, 2.1 + up * 3.5, -up * 1.5])
        bird = pigeon_flying(tg, pp, math.pi, 0.6)
    else:
        f = lt - t_hit
        top = c + np.array([0.1, 2.1 + (t_hit - 0.1) * 3.5, -(t_hit - 0.1) * 1.5])
        pp = top + np.array([0.3 * f, -4.5 * f * f, 0])
        pp[1] = max(pp[1], hground(pp[0], pp[2]) + 0.05)
        bird = pigeon(tg * 8, pose='fall', capsule=True).xf(M(trans(pp), roty(1.0), rotz(f * 7)))
    feathers = []
    cam = Cam(tuple(c + np.array([-2.6, 1.0, 4.6])), tuple(c + np.array([0, 2.6, -0.5])), 55)
    if lt >= t_hit and lt - t_hit < 0.5:
        feathers.append(billboard(top + np.array([0, 0.1, 0]), 0.9, 0.9, cam, (230, 230, 235), 'puff', emis=0.6, alpha=1 - (lt - t_hit) * 2))
    ms = [FOREST, GIS[1 + seed].mesh(tuple(c), math.pi, pose), bird] + feathers
    return merge(ms), cam, ENV_SMOKE, {}


def shot_rel1(lt, dur, tg):
    return release_shot(lt, dur, tg, 0)


def shot_rel2(lt, dur, tg):
    return release_shot(lt, dur, tg, 1)


def shot_last(lt, dur, tg):
    """le major tient Cher Ami à deux mains, face à la caméra (lente poussée)"""
    c = np.array([-0.5, hground(-0.5, 0.5), 0.5])
    hold = c + np.array([0, 1.25, 0.42])
    pose = crouch(ik_l=tuple(hold + np.array([-0.08, -0.03, 0])), ik_r=tuple(hold + np.array([0.08, -0.03, 0])), lean=0.1, drop=0.3, hp=0.15)
    bird = pigeon(pose='stand', capsule=False).xf(M(trans(hold + np.array([0, 0.03, 0.02])), roty(0.15 * math.sin(tg * 2))))
    cam = cam_lerp(Cam(tuple(c + np.array([0.6, 1.4, 2.6])), tuple(hold + np.array([0, 0.1, 0])), 46), Cam(tuple(c + np.array([0.35, 1.35, 1.6])), tuple(hold + np.array([0, 0.1, 0])), 42), lt / dur)
    return merge([FOREST, MAJOR.mesh(tuple(c), 0.0, pose), bird]), cam, ENV_SMOKE, dict(post_pil=lambda im: C2.vignette(im, 0.6))


def shot_message(lt, dur, tg):
    """le message roulé glisse dans la capsule, sur la patte"""
    c = np.array([0.0, 1.0, 0.0])
    roll = min(1.0, lt / 1.6)
    bird = pigeon(pose='stand', capsule=True).xf(M(trans(c), roty(math.pi / 2)))
    note = box(0.18 * (1 - roll) + 0.012, 0.004 + 0.01 * roll, 0.12 * (1 - 0.6 * roll), (255, 255, 255), 'note').xf(trans(0.05, 0.93 + 0.02 * roll, 0.12 - 0.05 * roll))
    table = box(1.2, 0.05, 0.8, (110, 80, 50), 'planks').xf(trans(0, 0.88, 0))
    cam = Cam((0.5, 1.3, 0.75), (0.0, 0.97, 0.02), 40)
    return merge([FOREST, table, bird, note]), cam, ENV_FOREST, dict(post_pil=lambda im: C2.vignette(im, 0.5))


# ------------------------------------------------------------------ 12-16. l'envol, touché, il repart, 40 km
def shot_cta(lt, dur, tg):
    u = lt / max(dur, 0.1)
    pos = np.array([0, 12, -20 + 6 * lt])
    cam = Cam(tuple(pos + np.array([3 - u, 0.8, 3])), tuple(pos), 50)
    return merge([FOREST, pigeon_flying(tg, pos, 0.0, 0.0, hurt=False, scale_=1.0), sun_disc((-200, 60, -500), 25, (255, 190, 120))]), cam, ENV_DUSK, {}


def shot_takeoff(lt, dur, tg):
    """Cher Ami s'envole du ravin ; sur la crête, les Allemands tirent ; il est touché"""
    t_fire = WT(13, 'tirent.') - cut['takeoff'] - 0.3
    t_hit = WT(13, 'touché…') - cut['takeoff']
    c = np.array([0.0, 0.0, 0.0])
    if lt < t_hit:
        pp = c + np.array([0.0, 1.5 + lt * 2.4, -lt * 1.2])
        bird = pigeon_flying(tg, pp, math.pi, 0.5, scale_=1.3)
    else:
        f = lt - t_hit
        top = c + np.array([0.0, 1.5 + t_hit * 2.4, -t_hit * 1.2])
        pp = top + np.array([0.2 * f, -5.0 * f * f, -0.3 * f])
        pp[1] = max(pp[1], hground(pp[0], pp[2]) + 0.1)
        bird = pigeon(tg * 8, pose='fall', capsule=True, leg_hurt=True).xf(M(trans(pp), roty(0.8), rotz(f * 6), scale(1.3)))
    ms = [FOREST, soldiers_in_ravine(tg), ger_line(tg, aim=True), bird]
    cam = Cam((-4.5, 1.6, 8.5), (1.5, 3.5, -2), 55)
    if lt > t_fire:
        for k, (x, z) in enumerate([(9.5, -3), (10.5, 1), (9.8, 5)]):
            if ((tg * 7 + k * 0.37) % 1.0) < 0.25:
                ms.append(billboard((x - 0.9, hground(x, z) + 1.45, z), 0.8, 0.8, cam, (255, 230, 150), 'spark', emis=1.0))
    if lt >= t_hit and lt - t_hit < 0.5:
        ms.append(billboard(top, 1.2, 1.2, cam, (235, 235, 240), 'puff', emis=0.6, alpha=1 - (lt - t_hit) * 2))
    return merge(ms), C2.shake(cam, 0.03, tg), ENV_SMOKE, {}


def shot_again(lt, dur, tg):
    """au sol, blessé… il bat des ailes et repart"""
    c = np.array([1.0, hground(1.0, -3.0), -3.0])
    up = max(0.0, lt - 0.35)
    pp = c + np.array([0, 0.12 + up * up * 3.0 + up * 0.8, -up * 0.6])
    bird = pigeon(tg * (10 if up == 0 else 24), pose='fly', leg_hurt=True).xf(M(trans(pp), roty(math.pi * 0.8), rotx(-0.3 if up else 0.0), scale(1.2)))
    cam = Cam(tuple(c + np.array([0.9, 0.35, 1.2])), tuple(c + np.array([0, 0.25 + up * 1.2, 0])), 48)
    return merge([FOREST, bird]), cam, ENV_SMOKE, {}


def countryside():
    rr = np.random.default_rng(6)
    ms = [grid(-1500, -1500, 1500, 1500, 24, 24, None, (255, 255, 255), 'patchwork', 160.0)]
    for i in range(60):
        ms.append(deciduous(rr.uniform(12, 18), rr.uniform(4, 6), i, (255, 255, 255), 'leaves_autumn').xf(trans(rr.uniform(-400, 400), 0, rr.uniform(-600, 200))))
    for i in range(8):
        x, z = rr.uniform(-300, 300), rr.uniform(-500, 0)
        ms.append(box(8, 6, 10, (230, 220, 200), 'plaster_old').xf(trans(x, 0, z)))
        ms.append(box(9, 0.5, 11, (150, 70, 50), 'roof_red').xf(trans(x, 6, z)))
    return merge(ms)


COUNTRY = countryside()


def shot_flight(lt, dur, tg):
    """il file au-dessus de la campagne"""
    pos = np.array([0, 60, 100 - lt * 25])
    cam = Cam(tuple(pos + np.array([-1.0, 0.35, 1.6])), tuple(pos + np.array([0.3, -0.4, -2])), 55)
    return merge([COUNTRY, pigeon_flying(tg, pos, math.pi, 0.05, hurt=True)]), C2.shake(cam, 0.01, tg), ENV_SKY.copy(fog_far=900), {}


def shot_arrive(lt, dur, tg):
    """il se pose sur la planche du colombier, touché à la poitrine, la patte presque arrachée, la capsule pend"""
    t_land = 0.7
    land = np.array([0.3, 2.42, 1.3])
    if lt < t_land:
        f = 1 - lt / t_land
        bird = pigeon_flying(tg, land + np.array([1.5 * f, 1.2 * f, 2.5 * f]), math.pi + 0.5, -0.2, hurt=True)
    else:
        bird = pigeon(pose='stand', leg_hurt=True, capsule=True).xf(M(trans(land + np.array([0, 0.07, 0])), roty(0.6), rotz(0.15)))
    blood = box(0.05, 0.04, 0.01, (120, 35, 35)).xf(M(trans(land + np.array([0.05, 0.1, 0.06])), roty(0.6))) if lt >= t_land else Mesh()
    hand = HANDLER.mesh((1.3, 0, 2.5), -0.9, dict(ik_l=(0.6, 2.3, 1.6), ra=(0.2, 0.1, 0.3), hp=-0.4)) if lt > t_land + 0.4 else Mesh()
    cam = cam_lerp(Cam((1.4, 2.7, 2.6), tuple(land + np.array([0, 0.1, 0])), 42), Cam((1.1, 2.62, 2.2), tuple(land + np.array([0, 0.1, 0])), 38), lt / dur)
    return merge([CAMP, bird, blood, hand]), cam, ENV_SKY, {}


# ------------------------------------------------------------------ 17-19. sauvés, soignés, décoré
def tent():
    ms = [box(7, 0.05, 6, (255, 255, 255), 'planks'), box(7, 2.8, 0.05, (150, 140, 110), 'cloth').xf(trans(0, 0, -2.8)),
          box(0.05, 2.8, 6, (150, 140, 110), 'cloth').xf(trans(-3.2, 0, 0)), box(0.05, 2.8, 6, (150, 140, 110), 'cloth').xf(trans(3.2, 0, 0))]
    ms.append(bench_table(2.0, 1.0, 0.85, (255, 255, 255), 'wood_dark').xf(trans(0, 0, -0.8)))
    ms.append(box(1.4, 0.01, 0.8, (255, 255, 255), 'map_old').xf(trans(0, 0.86, -0.8)))
    ms.append(gas_lamp(True).xf(trans(0.8, 0.86, -1.1)))
    for k in range(4):
        ms.append(box(0.5, 0.4, 0.4, (150, 120, 80)).xf(trans(-2.6, k * 0.4, -2.2)))
    ms.append(box(0.4, 0.25, 0.3, (60, 60, 55)).xf(trans(2.5, 0.86, -1.0)))    # téléphone de campagne
    return merge(ms)


TENT = tent()


def shot_hq(lt, dur, tg):
    """au QG, deux officiers lisent le message sur la carte"""
    note = box(0.16, 0.005, 0.1, (255, 255, 255), 'note').xf(trans(0.0, 0.87, -0.5))
    ms = [TENT, note, MAJOR.mesh((-0.5, 0, 0.0), math.pi, dict(lean=0.35, hp=0.5, ra=(1.1, 0.1, 0.4), la=(0.6, 0.1, 0.4))),
          GIS[3].mesh((0.6, 0, 0.1), math.pi + 0.3, dict(lean=0.3, hp=0.5, ra=(1.6, 0.5, 1.6)))]
    cam = cam_lerp(Cam((0.6, 1.75, -2.3), (0, 1.1, 0.0), 52), Cam((0.5, 1.7, -2.2), (0, 1.1, 0.0), 50), lt / dur)
    return merge(ms), cam, ENV_TENT, {}


def shot_rescued(lt, dur, tg):
    """les survivants sortent de la forêt, en file"""
    ms = [FOREST]
    for k in range(9):
        z = -14 + k * 2.2 + lt * 1.1
        x = 0.4 * math.sin(k * 1.7)
        ms.append(GIS[k % 5].mesh(on_ground(x, z), 0.0, walk_pose(tg * 4.5 + k, 0.6, hp=0.2, lean=0.1)))
    cam = Cam((2.5, 1.8, 10 + lt * 0.8), (0, 1.2, 0), 52)
    return merge(ms), cam, ENV_FOREST.copy(fog_far=80), {}


def infirmary():
    ms = [box(7, 0.05, 6, (255, 255, 255), 'planks'), box(7, 2.8, 0.05, (230, 228, 220), 'plaster').xf(trans(0, 0, -2.5)),
          box(0.05, 2.8, 6, (225, 222, 215), 'plaster').xf(trans(-3, 0, 0))]
    ms.append(bench_table(1.4, 0.8, 0.9, (255, 255, 255), 'planks_white').xf(trans(0, 0, -1.0)))
    ms.append(box(0.8, 0.01, 0.5, (240, 240, 235)).xf(trans(0, 0.91, -1.0)))
    ms.append(box(0.6, 0.6, 0.05, (255, 255, 255), 'redcross').xf(trans(0, 1.8, -2.45)) if 'redcross' in TEXB else box(0.5, 0.15, 0.04, (200, 40, 40)).xf(trans(0, 1.9, -2.45)))
    for k in range(5):
        ms.append(bottle(0.18, 0.04, [(200, 220, 230), (110, 70, 40), (60, 90, 60)][k % 3], alpha=0.8).xf(trans(-0.5 + k * 0.12, 0.91, -1.3)))
    ms.append(shelf(1.4, 1.8, 0.35, 3).xf(M(trans(-2.8, 0, -1.2), roty(math.pi / 2))))
    return merge(ms)


INF = infirmary()


def shot_medic(lt, dur, tg, wood=False):
    """à l'infirmerie : le médecin soigne Cher Ami posé sur la table"""
    bird = pigeon(pose='stand', capsule=False, leg_hurt=not wood, wood_leg=wood).xf(M(trans(0.0, 0.98, -0.9), roty(0.5)))
    band = box(0.1, 0.05, 0.13, (245, 245, 240)).xf(M(trans(0.0, 1.02, -0.9), roty(0.5)))
    ms = [INF, bird, band, MEDIC.mesh((0.0, 0, -0.1), math.pi, dict(ik_l=(-0.12, 1.05, -0.8), ik_r=(0.13, 1.05, -0.82), hp=0.6, lean=0.25))]
    if wood:
        cam = cam_lerp(Cam((0.55, 1.12, -0.3), (0.0, 1.0, -0.9), 40), Cam((0.45, 1.08, -0.4), (0.0, 1.0, -0.9), 38), lt / dur)
        ms = [INF, bird, MEDIC.mesh((0.0, 0, -0.1), math.pi, dict(ra=(0.4, 0.1, 0.3), la=(0.4, 0.1, 0.3), hp=0.6))]
    else:
        cam = cam_lerp(Cam((1.4, 1.6, 0.6), (0.0, 1.0, -0.8), 48), Cam((1.2, 1.55, 0.4), (0.0, 1.0, -0.8), 46), lt / dur)
    return merge(ms), cam, ENV_TENT, {}


def shot_woodleg(lt, dur, tg):
    return shot_medic(lt, dur, tg, wood=True)


def shot_medal(lt, dur, tg):
    """la croix de guerre accrochée près de Cher Ami"""
    m = croix_de_guerre().xf(M(trans(0.1, 1.08, -0.85), roty(0.4 * math.sin(tg * 1.2)), scale(1.6)))
    bird = pigeon(pose='stand', capsule=False, wood_leg=True).xf(M(trans(-0.07, 0.98, -0.95), roty(0.5)))
    cam = cam_lerp(Cam((0.35, 1.15, -0.45), (0.03, 1.04, -0.9), 38), Cam((0.28, 1.12, -0.55), (0.03, 1.04, -0.9), 34), lt / dur)
    return merge([INF, m, bird]), cam, ENV_TENT, dict(post_pil=lambda im: C2.vignette(im, 0.5))


# ------------------------------------------------------------------ 20-23. le doute, le nom, l'ADN
def archives():
    rr = np.random.default_rng(3)
    ms = [box(10, 0.05, 10, (255, 255, 255), 'planks_grey')]
    for row in range(3):
        for k in range(3):
            ms.append(shelf(1.8, 2.4, 0.5, 5).xf(trans(-2.2 + k * 2.2, 0, -1.5 - row * 2.2)))
            for lv in range(5):
                for j in range(5):
                    ms.append(box(0.28, 0.32, 0.4, (180, 160, 120) * np.array([rr.uniform(0.8, 1.05)] * 3)).xf(trans(-2.2 + k * 2.2 - 0.66 + j * 0.33, lv * 0.47 + 0.02, -1.5 - row * 2.2)))
    ms.append(bench_table(1.6, 0.8, 0.8, (255, 255, 255), 'wood_dark').xf(trans(0, 0, 1.2)))
    for k in range(4):
        ms.append(box(0.3, 0.02, 0.22, (235, 228, 205), 'note').xf(M(trans(-0.4 + k * 0.25, 0.81 + k * 0.004, 1.2), roty(k * 0.4))))
    ms.append(gas_lamp(True).xf(trans(0.6, 0.8, 1.0)))
    return merge(ms)


ARCH = archives()


def shot_archives(lt, dur, tg):
    """les archives de l'armée : rien ne prouve que c'est lui"""
    cam = cam_lerp(Cam((0.8, 1.6, 3.4), (0, 1.0, 0.0), 50), Cam((0.6, 1.5, 2.8), (0, 1.0, 0.0), 48), lt / dur)
    dust = C2.particles((0, 1.5, 1.5), tg, cam, 25, (2, 1.5, 2), 0.1, 0.03, (230, 220, 190), seed=4, alpha=0.6)
    return merge([ARCH, dust]), cam, ENV_ARCH, {}


def _ledger(d, n):
    d.rectangle([0, 0, n, n], fill=(235, 225, 195))
    d.line([n // 2, 0, n // 2, n], fill=(150, 130, 100))
    for y in range(3, n - 2, 3):
        d.line([2, y, n // 2 - 3, y], fill=(90, 90, 110))
        d.line([n // 2 + 3, y, n - 3, y], fill=(90, 90, 110))
    d.ellipse([n // 2 + 4, 13, n - 4, 21], outline=(200, 30, 30))


tex_draw('ledger', _ledger)


def shot_ledger(lt, dur, tg):
    """le registre de l'armée : la case « femelle » entourée"""
    book = merge([box(0.6, 0.03, 0.42, (90, 40, 30)), box(0.58, 0.01, 0.4, (255, 255, 255), 'ledger').xf(trans(0, 0.03, 0))]).xf(trans(0, 0.81, 1.2))
    cam = cam_lerp(Cam((0.15, 1.45, 1.55), (0.1, 0.83, 1.2), 45), Cam((0.15, 1.25, 1.4), (0.12, 0.83, 1.2), 40), lt / dur)
    return merge([ARCH, book]), cam, ENV_ARCH, {}


def shot_name2(lt, dur, tg):
    """Cher Ami… ou chère amie ? Gros plan, il tourne la tête"""
    bird = pigeon(pose='stand', capsule=False, wood_leg=True).xf(M(trans(0, 0.98, -0.9), roty(0.6 * math.sin(tg * 1.4))))
    cam = Cam((0.2, 1.15, -0.25), (0.0, 1.06, -0.9), 40)
    return merge([INF, bird]), cam, ENV_TENT, {}


def museum():
    ms = [box(12, 0.05, 10, (255, 255, 255), 'tile_lab', ts=1.5), box(12, 4, 0.1, (60, 62, 70)).xf(trans(0, 0, -3.5)),
          box(0.1, 4, 10, (65, 67, 75)).xf(trans(-4, 0, 0))]
    ms.append(box(0.9, 1.0, 0.7, (40, 40, 45)).xf(trans(0, 0, -1.5)))                                  # socle
    ms.append(box(0.5, 0.08, 0.3, (130, 90, 55)).xf(trans(0, 1.0, -1.5)))                               # planchette en bois
    ms.append(pigeon(pose='stand', capsule=False, wood_leg=True).xf(M(trans(0, 1.17, -1.5), roty(0.4))))
    ms.append(box(0.8, 0.7, 0.6, (200, 225, 235), alpha=0.25).xf(trans(0, 1.0, -1.5)))                 # vitrine
    ms.append(box(0.3, 0.12, 0.02, (220, 210, 180)).xf(M(trans(0.25, 0.85, -1.14), rotx(-0.3))))         # cartel
    ms.append(box(1.0, 1.3, 0.04, (90, 80, 60)).xf(trans(-2.2, 1.6, -3.4)))
    ms.append(box(0.9, 1.2, 0.05, (255, 255, 255), 'map_old').xf(trans(-2.2, 1.6, -3.37)))
    ms.append(box(1.4, 0.9, 0.05, (255, 255, 255), 'flag_us').xf(trans(2.2, 1.9, -3.4)))
    return merge(ms)


MUSEUM = museum()


def shot_museum(lt, dur, tg):
    """aujourd'hui : Cher Ami empaillé, dans sa vitrine du musée Smithsonian"""
    ms = [MUSEUM, VISIT.mesh((-1.3, 0, -0.7), 2.1, dict(hy=0.2, ra=(0.2, 0.1, 0.3)))]
    cam = cam_lerp(Cam((1.0, 1.6, 1.4), (-0.2, 1.1, -1.4), 48), Cam((0.8, 1.5, 0.9), (-0.1, 1.1, -1.5), 44), lt / dur)
    return merge(ms), cam, ENV_MUSEUM, {}


def lab():
    ms = [box(8, 0.05, 8, (255, 255, 255), 'tile_lab', ts=1.0), box(8, 3, 0.1, (220, 228, 235)).xf(trans(0, 0, -2.5)),
          bench_table(2.4, 0.8, 0.9, (235, 238, 240)).xf(trans(0, 0, -1.6))]
    for k in range(8):
        ms.append(cyl(0.015, 0.015, 0.12, 6, [(230, 90, 120), (80, 150, 230)][k % 2], alpha=0.8).xf(trans(-0.8 + k * 0.07, 0.95, -1.5)))
    ms.append(box(0.6, 0.12, 0.25, (210, 212, 215)).xf(trans(-0.85, 0.9, -1.55)))      # porte-tubes
    ms.append(box(0.5, 0.4, 0.4, (230, 232, 235)).xf(trans(0.7, 0.9, -1.8)))           # machine PCR
    ms.append(box(0.3, 0.1, 0.02, (60, 200, 120), emis=0.9).xf(trans(0.7, 1.15, -1.59)))
    ms.append(monitor().xf(trans(0.0, 1.35, -2.0)))
    return merge(ms)


LAB = lab()


def shot_dna(lt, dur, tg):
    """2021 : test ADN au labo ; une double hélice tourne"""
    ms = [LAB, SCI.mesh((-0.4, 0, -0.9), math.pi, dict(ik_r=(-0.6, 1.0, -1.5), la=(0.4, 0.1, 0.3), hp=0.4)), dna_helix(tg * 1.5, 18, 1.3, 0.18).xf(trans(0.6, 0.95, -1.1))]
    cam = cam_lerp(Cam((1.6, 1.6, 0.8), (0.3, 1.4, -1.2), 48), Cam((1.3, 1.6, 0.4), (0.4, 1.45, -1.2), 45), lt / dur)
    return merge(ms), cam, ENV_LAB, {}


def shot_question(lt, dur, tg):
    pos = np.array([0, 8, 8 - lt * 4])
    cam = Cam(tuple(pos + np.array([2.5, 0.8, 3.0])), tuple(pos + np.array([0, -1.0, -1])), 52)
    return merge([FOREST, soldiers_in_ravine(tg), pigeon_flying(tg, pos, math.pi, 0.0, hurt=True, scale_=1.6)]), cam, ENV_FOREST, {}


def shot_loop(lt, dur, tg):
    return shot_hook(lt, dur, tg, p=lt - dur)


# ------------------------------------------------------------------ montage
cut.add('hook', 0.0, shot_hook)
cut.add('hook_soldiers', WT(0, 'sauvé') - 0.1, shot_hook_soldiers)
cut.add('intro', T(1), shot_intro)
cut.add('loft', WT(1, 'pigeon') - 0.1, shot_loft)
cut.add('forest', T(2), shot_forest)
cut.add('encircled', T(3), shot_encircled)
cut.add('basket', T(4), shot_basket)
cut.add('name', T(5), shot_name)
cut.add('shells', T(6), shot_shells)
cut.add('artillery', T(7) + 0.3, shot_artillery)
cut.add('shells2', WT(7, 'bombarde') - 0.1, shot_shells)
cut.add('rel1', T(8), shot_rel1)
cut.add('rel2', T(9), shot_rel2)
cut.add('last', T(10), shot_last)
cut.add('message', T(11), shot_message)
cut.add('cta', T(12), shot_cta)
cut.add('takeoff', T(13), shot_takeoff)
cut.add('again', T(14), shot_again)
cut.add('flight', T(15), shot_flight)
cut.add('arrive', T(16), shot_arrive)
cut.add('hq', T(17), shot_hq)
cut.add('rescued', WT(17, 'Quelques') - 0.1, shot_rescued)
cut.add('medic', T(18), shot_medic)
cut.add('woodleg', WT(18, 'sculptent') - 0.1, shot_woodleg)
cut.add('medal', T(19), shot_medal)
cut.add('archives', T(20), shot_archives)
cut.add('name2', T(21), shot_name2)
cut.add('ledger', T(22), shot_ledger)
cut.add('museum', T(23), shot_museum)
cut.add('dna', WT(23, 'ADN') - 0.15, shot_dna)
cut.add('question', T(24), shot_question)
cut.add('loop', T(25), shot_loop)

tl.overlay = C2.overlays(
    C2.hook_title(['UN PIGEON', 'CONTRE UNE ARMÉE'], 0.0, 2.6, y=250, accent=1),
    emu_pastille(3.3, 3.2, y=300),
    C2.badge('CHER AMI', WT(1, 'Cher') - 0.05, 1.8, y=700),
    C2.badge('ARGONNE, OCTOBRE 1918', T(2), 2.4, y=700),
    C2.badge('+ DE 500 SOLDATS ENCERCLÉS', T(3), 2.4, y=700),
    retiens(T(5) - 0.1, max(2.2, T(6) - T(5)), y=300),
    C2.badge('TIRS AMÉRICAINS', T(7) + 0.3, 1.8, y=700, col=(255, 110, 90)),
    C2.badge('PIGEON 1', T(8) + 0.1, 1.2, y=700),
    C2.badge('PIGEON 2', T(9), 1.2, y=700),
    C2.cta(T(12) - 0.1, max(1.6, T(13) - T(12) + 0.05)),
    C2.badge('40 KM', WT(15, '40') - 0.1, 1.3, y=700),
    C2.badge('25 MIN', WT(15, '25') - 0.1, 1.2, y=780),
    C2.badge('194 SURVIVANTS', WT(17, '194') - 0.1, 1.9, y=700),
    C2.badge('CROIX DE GUERRE', T(19), 1.6, y=700),
    C2.badge('AUCUNE PREUVE', WT(20, 'archives') - 0.1, 1.9, y=700, col=(255, 110, 90)),
    C2.badge('CHER AMI ?', WT(21, 'Cher') - 0.05, 1.2, y=700),
    C2.badge('CHÈRE AMIE ?', WT(21, 'chère') - 0.05, 1.3, y=780),
    C2.badge('FEMELLE', WT(22, 'femelle.') - 0.1, 1.3, y=700),
    C2.badge('2021 : MÂLE', WT(23, 'mâle.') - 0.1, 1.6, y=700),
    end_card(T(24), T(25) - T(24)),
)

subs = Subs(timing)


def build_audio(path):
    mx = A.Mixer(END)
    S = cut
    mx.add(A.wind(END), 0, 0.2)
    mx.add(C2.impact(), 0.0, 0.5)
    mx.add(A.explosion(2.0), 0.05, 0.4)
    mx.add(A.explosion(2.0), 1.65, 0.35)
    mx.add(A.whoosh(0.8), 0.4, 0.4)
    mx.add(A.birds(4), S['intro'], 0.3, length=S['forest'] - S['intro'])
    mx.add(A.whoosh(0.5), S['loft'] + 0.3, 0.3)
    mx.add(A.cannon(2.5), S['forest'] + 0.8, 0.25)
    mx.add(A.cannon(2.5), S['encircled'] + 1.2, 0.25)
    mx.add(A.footsteps(1.5, 1.5), S['basket'], 0.2)
    mx.add(C2.riser(1.2), T(5) - 0.4, 0.3)
    mx.add(C2.ding(), T(5) + 0.1, 0.4)
    for t in (0.15, 0.7, 1.2, 1.7):
        mx.add(A.explosion(2.0), S['shells'] + t, 0.6)
        mx.add(A.explosion(2.0), S['shells2'] + t, 0.6)
    for k in range(3):
        mx.add(A.cannon(2.0), S['artillery'] + 0.2 + k * 0.45, 0.7)
    for n, w in (('rel1', 8), ('rel2', 9)):
        mx.add(A.whoosh(0.6), S[n] + 0.1, 0.4)
        mx.add(A.thwack(0.3), WT(w, 'Abattu'), 0.8)
    mx.add(C2.heartbeat(2.0, 70), S['last'], 0.4)
    mx.add(A.ratchet(0.4), S['message'] + 1.2, 0.3)
    mx.add(C2.pop(), T(12) + 0.05, 0.5)
    mx.add(C2.ding(), T(12) + max(1.6, T(13) - T(12)) * 0.62, 0.4)
    mx.add(A.whoosh(0.8), S['takeoff'] + 0.1, 0.4)
    for k in range(6):
        mx.add(A.thwack(0.2), WT(13, 'tirent.') - 0.3 + k * 0.16, 0.5)
    mx.add(A.thwack(0.3), WT(13, 'touché…'), 0.9)
    mx.add(A.whoosh(1.0), S['again'] + 0.35, 0.5)
    mx.add(A.wind(3), S['flight'], 0.5)
    mx.add(A.birds(4), S['arrive'], 0.25)
    mx.add(A.tick(), S['hq'] + 0.5, 0.3)
    mx.add(A.footsteps(4, 2.0), S['rescued'], 0.35)
    mx.add(A.crowd(3), S['rescued'] + 0.5, 0.15)
    mx.add(A.clank(0.3), S['medic'] + 0.4, 0.2)
    mx.add(C2.ding(), S['medal'] + 0.2, 0.4)
    mx.add(A.sting(1.0), S['archives'], 0.3)
    mx.add(C2.record_scratch(), S['ledger'] + 0.1, 0.2)
    mx.add(C2.riser(1.0), S['dna'] - 0.3, 0.3)
    mx.add(C2.ding(), WT(23, 'mâle.'), 0.5)
    mx.add(A.wind(4), S['question'], 0.25)
    mx.add(A.explosion(2.0), END - 1.4, 0.3)
    C2.cut_sounds(mx, list(cut.st.values()), 0.08)
    mx.save(path)


if __name__ == '__main__':
    run(tl, subs, HERE, 'Good2No_ep26_Cher_Ami', build_audio, sys.argv)
