"""Ép. 25 — Poon Lim, 133 jours seul sur un radeau (Les survivants impossibles) : 1942-1943."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n/lot7']
from props7 import *
from video_core import *

HERE = '/home/claude/g2n/lot7/poon'
timing = load_timing(os.path.join(HERE, 'timing.json'))
tl = Timeline(timing)
T, WT = tl.T, tl.word_t
END = timing[-1]['t1'] + 0.3
tl.duration = lambda: END
cut = Cut(tl)

# ------------------------------------------------------------------ personnages
SKIN = (222, 186, 140)
make_face('poon', skin=SKIN, hair_col=(25, 22, 20))
make_face('poon_closed', skin=SKIN, eyes_closed=True)
make_face('fisher1', skin=(170, 120, 85), mustache=True, hair_col=(30, 25, 20))
make_face('fisher2', skin=(190, 140, 100), hair_col=(40, 30, 25))
make_face('fisher3', skin=(150, 105, 75), hair_col=(25, 20, 18))
make_face('sailor', skin=(230, 195, 165), hair_col=(120, 90, 60))
make_face('officer', skin=(228, 190, 160), hair_col=(60, 45, 30))
make_face('doc', skin=(225, 185, 155), mustache=True, hair_col=(90, 80, 70))
STEWARD = Human('poon', skin=SKIN, shirt=(240, 240, 235), pants=(40, 40, 50), hair=(25, 22, 20), jacket=(245, 245, 240), build=0.9)
POON = Human('poon', skin=SKIN, shirt=(225, 222, 210), pants=(60, 60, 70), hair=(25, 22, 20), sleeves='short', build=0.85, shoes=SKIN)
POON_C = Human('poon_closed', skin=SKIN, shirt=(225, 222, 210), pants=(60, 60, 70), hair=(25, 22, 20), sleeves='short', build=0.85, shoes=SKIN)
POON_SUIT = Human('poon', skin=SKIN, shirt=(235, 235, 230), pants=(55, 55, 62), hair=(25, 22, 20), jacket=(70, 70, 80), tie=(120, 30, 40), build=0.9)
POON_BARE = Human('poon', skin=SKIN, shirt=(235, 235, 230), pants=(55, 55, 62), hair=(25, 22, 20), jacket=(70, 70, 80), tie=(120, 30, 40), build=0.9, shoes=SKIN)
FISH = [Human('fisher1', skin=(170, 120, 85), shirt=(200, 190, 160), pants=(90, 80, 60), hair=(30, 25, 20), hat='straw', hat_col=(220, 190, 120), sleeves='short', shoes=(170, 120, 85)),
        Human('fisher2', skin=(190, 140, 100), shirt=(80, 120, 160), pants=(200, 190, 170), hair=(40, 30, 25), hat='straw', hat_col=(220, 190, 120), sleeves='short', shoes=(190, 140, 100)),
        Human('fisher3', skin=(150, 105, 75), shirt=(230, 225, 210), pants=(70, 70, 80), hair=(25, 20, 18), sleeves='short', shoes=(150, 105, 75))]
SAILOR = Human('sailor', skin=(230, 195, 165), shirt=(60, 70, 100), pants=(50, 55, 75), hair=(120, 90, 60), hat='flatcap', hat_col=(50, 50, 60))
OFFICER = Human('officer', skin=(228, 190, 160), shirt=(240, 240, 240), pants=(30, 35, 60), hair=(60, 45, 30), jacket=(30, 35, 60), hat='sailor_cap', hat_col=(240, 240, 240), tie=(20, 20, 20))
DOC = Human('doc', skin=(225, 185, 155), shirt=(240, 240, 235), pants=(70, 70, 75), hair=(90, 80, 70), jacket=(238, 238, 232))

# ------------------------------------------------------------------ ambiances
ENV_DAY = Env(sky_top=(60, 120, 200), sky_hor=(195, 215, 230), fog=(185, 205, 222), fog_near=60, fog_far=900, amb=0.55, light=(-0.4, 0.8, 0.45))
ENV_NIGHT = Env(sky_top=(8, 12, 30), sky_hor=(30, 40, 65), fog=(20, 28, 48), fog_near=40, fog_far=500, amb=0.35, light=(0.3, 0.8, -0.3), light_col=(150, 170, 220))
ENV_DUSK = Env(sky_top=(50, 60, 120), sky_hor=(250, 160, 90), fog=(220, 150, 110), fog_near=60, fog_far=800, amb=0.5, light=(-0.6, 0.35, -0.7), light_col=(255, 190, 130))
ENV_STORM = Env(sky_top=(45, 50, 58), sky_hor=(95, 100, 108), fog=(85, 90, 98), fog_near=20, fog_far=260, amb=0.45, light=(0.3, 0.8, 0.2), light_col=(190, 195, 205))
ENV_HOT = Env(sky_top=(70, 130, 210), sky_hor=(235, 225, 200), fog=(225, 215, 195), fog_near=60, fog_far=900, amb=0.6, light=(-0.2, 0.95, 0.2), light_col=(255, 240, 210))
ENV_ROOM = Env(sky_top=(70, 68, 64), sky_hor=(70, 68, 64), fog=(60, 58, 54), fog_near=10, fog_far=40, amb=0.62, light=(0.3, 0.85, 0.5))
ENV_HOSP = Env(sky_top=(80, 85, 90), sky_hor=(80, 85, 90), fog=(70, 74, 78), fog_near=10, fog_far=40, amb=0.62, light=(0.4, 0.85, 0.4))
SEA_FAR = ocean(0.0)


# ------------------------------------------------------------------ radeau qui tangue (tout ce qui est dessus bouge avec lui)
def bob(tg, k=1.0):
    return M(trans(0, 0.05 * k * math.sin(tg * 1.7), 0), rotx(0.05 * k * math.sin(tg * 1.3)), rotz(0.06 * k * math.sin(tg * 1.1 + 1)))


def raft_world(tg, people=(), knots=0, extra=(), k=1.0, tin=True, flashlight=True, canvas=True):
    m = merge([raft(knots, tin=tin, flashlight=flashlight, canvas=canvas)] + list(people) + list(extra))
    return m.xf(bob(tg, k))


def sea_at(tg, tex='ocean', amp=0.18):
    return merge([ocean(tg, tex), near_waves(tg, tex=tex, amp=amp)])


SIT = dict(drop=0.62, ll=(1.5, 1.6), rl=(1.4, 1.5))     # assis en tailleur sur le plancher (bassin posé à y≈0.32)


def poon_sit(tg, **kw):
    p = sit_pose(**SIT)
    p.update(la=(0.5, 0.15, 0.6), ra=(0.5, 0.15, 0.6), hy=0.3 * math.sin(tg * 0.4))
    p.update(kw)
    return p


def poon_on(pos, yaw, pose, who=None):
    return (who or POON).mesh((pos[0], 0.27 + pos[1], pos[2]), yaw, pose)


# ------------------------------------------------------------------ 0. accroche
def shot_hook(lt, dur, tg, p=None):
    """Poon debout sur son radeau fait de grands signes ; la caméra recule vite : rien autour"""
    p = lt if p is None else p
    wave = 2.7 + 0.35 * math.sin(tg * 8)
    pose = dict(ra=(wave, 0.5, 0.2), la=(wave - 0.3, 0.5, 0.2), hy=0.2 * math.sin(tg * 2))
    u = max(0.0, p)
    d = 2.6 + 3.2 * u * u
    cam = Cam((1.4 + 0.25 * d, 1.0 + 0.5 * d, 1.6 + 0.8 * d), (0, 1.1 - 0.05 * d, 0), 50)
    ms = [sea_at(tg), raft_world(tg, [poon_on((0.1, 0, 0.1), 0.5, pose)])]
    return merge(ms), cam, ENV_DAY, {}


def shot_hook_top(lt, dur, tg):
    """vue du ciel : un point minuscule sur l'océan"""
    h = 14 + lt * 18
    cam = Cam((0.5, h, 1.0), (0, 0, 0), 55, roll=0.2 * lt)
    ms = [sea_at(tg), raft_world(tg, [poon_on((0.1, 0, 0.1), 0.5, dict(ra=(2.8, 0.5, 0.2), la=(2.6, 0.5, 0.2)))])]
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 1. steward sur le cargo
def deck():
    """pont arrière d'un cargo : planches, bastingage, treuil, cordages, écoutille, bouées"""
    ms = [box(14, 0.1, 9, (255, 255, 255), 'planks', ts=1.5).xf(trans(0, -0.1, 0)), box(14, 1.0, 0.1, (200, 198, 190)).xf(trans(0, 0, 4.4)),
          box(14, 3.0, 0.2, (225, 222, 210), 'window', ts=2.0).xf(trans(0, 0, -4.4))]
    for x in np.arange(-6.5, 7, 1.3):
        ms.append(cyl(0.04, 0.04, 1.0, 4, (190, 188, 180)).xf(trans(x, 0, 4.4)))
    ms.append(box(1.6, 0.8, 1.2, (60, 70, 60)).xf(trans(-3, 0, 0)))
    ms.append(cyl(0.35, 0.35, 1.2, 8, (80, 80, 82)).xf(M(trans(3.5, 0.6, -1.5), rotz(math.pi / 2), trans(0, -0.6, 0))))
    ms.append(cyl(0.6, 0.6, 0.3, 8, (230, 230, 225), caps=False).xf(trans(-5.5, 0.6, 4.3)))     # bouée
    ms.append(box(0.15, 0.15, 0.15, (190, 60, 50)).xf(trans(-5.5, 0.9, 4.35)))
    for k in range(5):
        ms.append(cyl(0.5 - k * 0.03, 0.5 - k * 0.03, 0.08, 10, (200, 180, 130), caps=False).xf(trans(1.0, k * 0.08, 2.5)))   # rouleau de corde
    ms.append(box(0.9, 0.7, 0.6, (140, 110, 70), 'planks').xf(trans(5.5, 0, 2.6)))
    return merge(ms)


DECK = deck()


def tray():
    ms = [box(0.45, 0.02, 0.3, (190, 190, 195), 'metal')]
    for x in (-0.12, 0.0, 0.12):
        ms.append(cyl(0.035, 0.03, 0.07, 6, (245, 245, 240)).xf(trans(x, 0.01, 0.03)))
    return merge(ms)


def shot_intro(lt, dur, tg):
    """Poon, steward en veste blanche, traverse le pont avec un plateau de tasses (à deux mains)"""
    x = -2.0 + lt * 0.9
    pos = (x, 0, 1.0)
    pose = walk_pose(tg * 6, 0.6, arm=0.0, ik_l=(x - 0.2, 1.08, 1.4), ik_r=(x + 0.2, 1.08, 1.4))
    ms = [DECK, STEWARD.mesh(pos, math.pi / 2 - 0.5, pose), tray().xf(trans(x, 1.08, 1.45)), SEA_FAR.xf(trans(0, -6, 0))]
    cam = cam_lerp(Cam((x + 2.6, 1.7, 5.4), (x, 1.15, 1.0), 48), Cam((x + 2.2, 1.65, 4.8), (x, 1.15, 1.0), 46), lt / dur)
    return merge(ms), C2.shake(cam, 0.01, tg), ENV_DAY.copy(fog_far=600), {}


def shot_intro_ship(lt, dur, tg):
    """le cargo britannique, seul en mer"""
    u = lt / max(dur, 0.1)
    cam = Cam((60 - 15 * u, 10, 70), (5 * u, 6, 0), 48)
    ms = [ocean(tg), cargo_ship().xf(trans(lt * 4, 0, 0)), smoke_sprites((-5 + lt * 4, 16, 0), tg, cam, n=5, size=4, rise=10, seed=3, col=(60, 58, 55), drift=(-2, 0, 0))]
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 2-3. torpille, naufrage
def shot_night(lt, dur, tg):
    cam = Cam((50, 6, 55), (0, 6, 0), 48)
    ms = [ocean(tg, 'ocean_dusk'), cargo_ship(lights=True).xf(trans(lt * 3, 0, 0))]
    return merge(ms), cam, ENV_NIGHT, {}


def shot_torpedo(lt, dur, tg):
    """sous l'eau : la torpille fonce vers la caméra"""
    z = -14 + lt * 15
    cam = Cam((1.6, -1.6, 5.0), (0, -2.2, -4), 55)
    hull = box(80, 8, 13, (50, 52, 55)).xf(trans(0, -6.0, -24))
    ms = [box(400, 0.1, 400, (60, 120, 140)).xf(trans(0, 0, 0)), hull, torpedo().xf(M(trans(0, -2.2, z), roty(-math.pi / 2)))]
    ms.append(bubbles_fx((0, -2.2, z - 3.5), tg, cam))
    env = Env(sky_top=(10, 45, 70), sky_hor=(20, 70, 95), fog=(15, 60, 85), fog_near=2, fog_far=40, amb=0.6, light=(0, 1, 0), light_col=(150, 200, 220))
    return merge(ms), C2.shake(cam, 0.02, tg), env, {}


def bubbles_fx(base, t, cam, n=10):
    rr = np.random.default_rng(2)
    ms = []
    for i in range(n):
        ph = (t * 1.5 + rr.random()) % 1.0
        p = np.asarray(base, float) + np.array([rr.uniform(-0.3, 0.3), ph * 1.2, -ph * 4])
        s = rr.uniform(0.1, 0.25)
        ms.append(billboard(p, s, s, cam, (200, 235, 245), 'puff', emis=0.6, alpha=0.7 * (1 - ph)))
    return merge(ms)


def shot_hit(lt, dur, tg):
    """la torpille frappe : explosion contre la coque"""
    t_hit = WT(2, 'frappe') - cut['hit']
    cam = Cam((38, 5, 34), (0, 3, 0), 50)
    age = lt - t_hit
    ms = [ocean(tg, 'ocean_dusk'), cargo_ship(lights=age < 0.3).xf(trans(lt * 3, 0, 0))]
    if age > 0:
        ms.append(water_burst((6 + lt * 3, 0, 6.6), age, cam))
        ms.append(fire_sprites(np.array([6 + lt * 3, 4.5, 6.4]), tg, cam, n=6, size=2.2, spread=1.5, seed=1, hgt=3))
    else:
        ms.append(wake_fx((6 + lt * 3, 0, 40), (6 + lt * 3, 0, 40 - 34 * min(1, lt / max(0.01, t_hit))), tg, cam, w=1.0))
    fl = C2.decay(lt, t_hit, 5) if age > 0 else 0
    return merge(ms), C2.shake(cam, 0.25 * fl, tg), ENV_NIGHT, dict(flash=0.6 * fl, flash_col=(255, 190, 120))


def water_burst(pos, age, cam, h=18.0):
    rr = np.random.default_rng(4)
    ms = []
    p = np.asarray(pos, float)
    k = min(1.0, age / 0.5)
    for i in range(14):
        o = rr.normal(size=3) * np.array([2.5, 0, 2.0])
        yy = h * k * rr.uniform(0.3, 1.0) - max(0, age - 1.0) * 8
        if yy < 0:
            continue
        s = 4 * (0.6 + rr.random() * 0.6)
        ms.append(billboard(p + o + np.array([0, yy, 0]), s, s, cam, (230, 235, 240), 'puff', emis=0.5, alpha=0.9 * max(0, 1 - age / 3)))
    return merge(ms)


def shot_sink(lt, dur, tg):
    """le cargo pique du nez et coule en deux minutes (accéléré)"""
    u = lt / max(dur, 0.1)
    m = cargo_ship().xf(M(trans(0, -4 - 22 * u * u, 0), rotz(-0.18 - 0.35 * u), rotx(0.08)))
    cam = Cam((45, 4, 48), (0, 0, 0), 48)
    ms = [ocean(tg, 'ocean_dusk'), m, fire_sprites(np.array([5, 3 - 18 * u * u, 6]), tg, cam, n=5, size=2, seed=2),
          smoke_sprites((0, 8, 0), tg, cam, n=6, size=6, rise=14, seed=5, col=(50, 48, 46), drift=(1, 0, 0))]
    return merge(ms), C2.shake(cam, 0.03, tg), ENV_NIGHT, {}


# ------------------------------------------------------------------ 4. il nage, trouve le radeau
def swimmer(tg, pos, yaw):
    """Poon dans l'eau jusqu'aux épaules, il nage la brasse (tête hors de l'eau)"""
    a = tg * 3.5
    sw = 0.35 * math.sin(a)
    pose = dict(lean=0.35, hp=-0.3, ra=(1.5 + sw, 0.5 - sw, 0.3), la=(1.5 + sw, 0.5 - sw, 0.3), ll=(0.4 + sw, 0.6), rl=(0.4 - sw, 0.6))
    return POON.mesh((pos[0], pos[1] - 1.28, pos[2]), yaw, pose)


def shot_swim(lt, dur, tg):
    z = 6 - lt * 1.1
    cam = Cam((1.1, 0.5, z - 3.0), (0, 0.35, z), 50)
    ms = [sea_at(tg, 'ocean_dusk', 0.22), swimmer(tg, (0, 0, z), math.pi), raft_world(tg, [], extra=()).xf(trans(0.5, 0, z - 4.5))]
    return merge(ms), cam, ENV_NIGHT.copy(sky_hor=(90, 80, 100), fog=(70, 70, 95), amb=0.42), {}


def shot_climb(lt, dur, tg):
    """il se hisse sur le radeau vide"""
    u = min(1.0, lt / 1.4)
    pose = dict(lean=0.9 - 0.6 * u, ra=(2.0, 0.2, 0.6), la=(2.0, 0.2, 0.6), ll=(1.2 * u, 1.5 * u), rl=(0.3, 0.6), drop=0.3 * (1 - u))
    p = poon_on((0, -0.8 * (1 - u), 1.0 - 0.6 * u), math.pi, pose)
    cam = Cam((2.4, 1.3, 3.2), (0, 0.5, 0.3), 50)
    return merge([sea_at(tg, 'ocean_dusk'), raft_world(tg, [p])]), cam, ENV_NIGHT.copy(sky_hor=(140, 110, 120), fog=(100, 90, 110), amb=0.45), {}


# ------------------------------------------------------------------ 5-6. ce qu'il y a sur le radeau
ITEM_POS = {"l'eau,": (0.85, 0.32, 0.85), 'biscuits,': (0.75, 0.32, 0.4), 'lampe': (-0.7, 0.36, 0.9)}


def shot_items(lt, dur, tg):
    """vue de dessus : bidon d'eau, biscuits, lampe de poche (chaque objet s'éclaire quand il est dit)"""
    cam = Cam((0.3, 4.6, 1.4), (0.0, 0.3, 0.1), 45)
    ms = [sea_at(tg), raft_world(tg, [poon_on((-0.4, 0, -0.5), 0.3, poon_sit(tg, ra=(0.8, 0.1, 0.8)))], k=0.4)]
    for i, (w, p) in enumerate(ITEM_POS.items()):
        t_w = WT(5, w) - cut['items']
        if 0 <= lt - t_w < 1.0:
            k = 1 - (lt - t_w)
            ms.append(billboard(np.array(p) + np.array([0, 0.45, 0]), 0.5 * k + 0.2, 0.5 * k + 0.2, cam, (255, 250, 200), 'spark', emis=1.0, alpha=0.7 * k))
    return merge(ms), cam, ENV_DAY, {}


def shot_flashlight(lt, dur, tg):
    """gros plan lent sur la lampe de poche (retiens ce détail)"""
    g = np.array([-0.7, 0.36, 0.9])
    cam = cam_lerp(Cam(tuple(g + np.array([0.6, 0.5, 0.7])), tuple(g), 40), Cam(tuple(g + np.array([0.35, 0.3, 0.45])), tuple(g), 38), lt / dur)
    ms = [sea_at(tg), raft_world(tg, [], k=0.3)]
    return merge(ms), cam, ENV_DAY, dict(post_pil=lambda im: C2.vignette(im, 0.7))


# ------------------------------------------------------------------ 7. les jours passent
def days_env(lt, dur):
    u = (lt / max(dur, 0.1) * 2) % 1.0
    a = u * math.pi
    sun = (-math.cos(a), math.sin(a) * 0.9 + 0.1, -0.4)
    day = max(0.0, math.sin(a))
    return ENV_DAY.copy(light=sun, amb=0.35 + 0.25 * day, sky_top=(20 + 40 * day, 30 + 90 * day, 60 + 140 * day),
                        sky_hor=(90 + 105 * day, 80 + 135 * day, 110 + 120 * day), fog=(80 + 105 * day, 80 + 125 * day, 110 + 112 * day))


def shot_days(lt, dur, tg):
    """accéléré : le soleil tourne, Poon fait un nœud par jour sur la corde"""
    n = 3 + int(lt / dur * 9)
    pose = poon_sit(tg, ik_r=(-1.0, 0.75, 0.75), ik_l=(-1.0, 0.7, 0.6), hy=-0.4)
    ms = [sea_at(tg * 3), raft_world(tg * 3, [poon_on((-0.45, 0, 0.55), -1.2, pose)], knots=n, k=0.6)]
    cam = Cam((-2.7, 1.1, 2.2), (-1.0, 0.6, 0.7), 45)
    return merge(ms), cam, days_env(lt, dur), {}


# ------------------------------------------------------------------ 8-9. les cargos passent, l'avion, la tempête
def shot_ship_pass(lt, dur, tg):
    """un cargo passe au loin ; Poon agite les bras"""
    wave = 2.8 + 0.4 * math.sin(tg * 9)
    pose = dict(ra=(wave, 0.6, 0.2), la=(wave, 0.6, 0.2))
    cam = Cam((2.2, 1.4, 3.4), (-6, 2.0, -60), 52)
    ms = [sea_at(tg), raft_world(tg, [poon_on((0.1, 0, -0.2), math.pi - 0.2, pose)]), cargo_ship().xf(M(trans(-45 + lt * 9, 0, -110), roty(0.0)))]
    return merge(ms), cam, ENV_DAY, {}


def shot_ship_deck(lt, dur, tg):
    """depuis le cargo : deux marins regardent le petit radeau… et le navire continue"""
    ms = [ocean(tg), DECK.xf(trans(0, 6, 0)), raft_world(tg, [poon_on((0, 0, 0), 0.4, dict(ra=(2.8, 0.6, 0.2), la=(2.8, 0.6, 0.2)))]).xf(trans(-6 - lt * 4, 0, 40)),
          SAILOR.mesh((-1, 6, 3.6), 0.0, dict(ra=(0.3, 0.1, 0.2), hy=0.3)), SAILOR.mesh((0.2, 6, 3.6), 0.0, dict(la=(1.6, -0.3, 1.8), ra=(1.6, 0.3, 1.8), hy=-0.2))]
    cam = Cam((-0.4, 9.0, -2.5), (-5, 1, 40), 48)
    return merge(ms), cam, ENV_DAY, {}


def shot_plane(lt, dur, tg):
    """un hydravion américain passe en rase-mottes et le repère"""
    x = -70 + lt * 45
    cam = Cam((2.0, 1.2, 3.5), (x * 0.4, 12, -8), 58)
    ms = [sea_at(tg), raft_world(tg, [poon_on((0, 0, 0), math.pi * 0.8, dict(ra=(2.9, 0.4, 0.1), la=(2.9, 0.4, 0.1)))]),
          patrol_plane(tg * 30).xf(M(trans(x, 30, -20), roty(math.pi / 2), rotz(-0.15)))]
    return merge(ms), C2.shake(cam, 0.02, tg), ENV_DAY, {}


def shot_storm(lt, dur, tg):
    """la tempête : vagues énormes, pluie, éclairs"""
    cam = Cam((3.0, 2.0, 4.5), (0, 0.4, 0), 52)
    pose = poon_sit(tg, la=(1.3, 0.3, 0.2), ra=(1.3, 0.3, 0.2), lean=0.4, hp=0.4)
    ms = [ocean(tg, 'ocean_storm', swell=0.0), near_waves(tg * 1.6, tex='ocean_storm', amp=0.6, r=18), raft_world(tg * 1.6, [poon_on((0, 0, 0), 0.5, pose)], k=4.0),
          storm_rain(cam, tg)]
    fl = 1.0 if (lt % 1.3) < 0.08 else 0.0
    if fl:
        ms.append(lightning_mesh(lightning_path((-30, 60, -80), (-25, 0, -70), seed=int(lt)), cam, width=0.8))
    return merge(ms), C2.shake(cam, 0.06, tg), ENV_STORM, dict(flash=0.5 * fl, flash_col=(220, 230, 255))


# ------------------------------------------------------------------ 10-11. plus rien à manger, la lampe devient hameçon
def shot_empty(lt, dur, tg):
    """jour 55 : la caisse de biscuits est vide, Poon tête basse"""
    pose = poon_sit(tg, hp=0.5, la=(0.3, 0.1, 0.3), ra=(0.3, 0.1, 0.3), lean=0.25, hy=0.0)
    cam = cam_lerp(Cam((1.6, 1.0, 2.0), (0.0, 0.7, 0.2), 48), Cam((1.4, 0.95, 1.7), (0.0, 0.7, 0.2), 45), lt / dur)
    ms = [sea_at(tg), raft_world(tg, [poon_on((0, 0, 0.0), 0.6, pose, POON_C)], knots=12, extra=[box(0.36, 0.02, 0.26, (90, 70, 45)).xf(trans(0.75, 0.55, 0.4))])]
    return merge(ms), cam, ENV_HOT, dict(post_pil=C2.tint((255, 220, 160), 0.25))


def shot_dismantle(lt, dur, tg):
    """il ouvre la lampe : le ressort sort, il le tord en hameçon (objets tenus à deux mains devant lui)"""
    t_hook = WT(11, 'transforme') - cut['dismantle']
    c = np.array([0.0, 0.0, 0.3])
    hold = (c[0], 0.95, c[2] + 0.45)
    pose = poon_sit(tg, ik_l=(hold[0] - 0.09, hold[1], hold[2]), ik_r=(hold[0] + 0.09, hold[1], hold[2]), hp=0.45)
    obj = flashlight_m().xf(M(trans(hold), roty(math.pi / 2 + 0.3))) if lt < t_hook else hook_m().xf(M(trans(hold[0], hold[1] + 0.02, hold[2] + 0.02), scale(1.6)))
    extra = [spring_m().xf(trans(0.35, 0.33, 0.6)) if lt < t_hook else Mesh(), flashlight_m().xf(M(trans(-0.4, 0.36, 0.6), roty(1.2))) if lt >= t_hook else Mesh()]
    people = [poon_on((c[0], 0, c[2]), 0.0, pose), obj]
    cam = Cam((0.9, 1.35, 2.3), (0.0, 0.8, 0.45), 42)
    ms = [sea_at(tg), raft_world(tg, people, extra=extra, flashlight=False, k=0.3)]
    return merge(ms), cam, ENV_HOT, {}


def shot_cta(lt, dur, tg):
    u = lt / max(dur, 0.1)
    cam = Cam((-9 + 3 * u, 2.5, 10 - 2 * u), (0, 0.8, 0), 50)
    ms = [sea_at(tg, 'ocean_dusk'), raft_world(tg, [poon_on((0, 0, 0), 0.3, poon_sit(tg))], knots=12), sun_disc((-200, 30, -700), 30, (255, 200, 120))]
    return merge(ms), cam, ENV_DUSK, {}


# ------------------------------------------------------------------ 13. pêche, mouettes, pluie
def shot_fishing(lt, dur, tg):
    """il remonte la ligne : un poisson frétille au bout"""
    up = min(1.0, lt / 1.2)
    fish_y = -0.6 + 1.6 * up
    c = (0.6, 0, 0.2)
    pose = dict(ra=(1.6 + 0.6 * up, 0.2, 0.4), la=(1.0 + 0.4 * up, 0.1, 0.6), lean=-0.1 * up)
    fp = np.array([1.5, fish_y, 0.9])
    ms = [sea_at(tg), raft_world(tg, [poon_on(c, 0.9, pose), rod((0.95, 1.35 + 0.3 * up, 0.55), fp, 0.012, (220, 220, 210), n=3),
                                       fish_m((200, 210, 215), 0.4).xf(M(trans(fp + np.array([0, -0.18, 0])), rotz(-math.pi / 2), roty(0.6 * math.sin(tg * 18))))])]
    cam = Cam((2.8, 1.2, 2.6), (0.9, 0.8, 0.5), 48)
    return merge(ms), cam, ENV_DAY, {}


def shot_gull(lt, dur, tg):
    """une mouette se pose sur le bord du radeau"""
    u = min(1.0, lt / 0.8)
    gp = np.array([1.0 + 2.0 * (1 - u), 0.76 + 1.5 * (1 - u), -1.15])
    ms = [sea_at(tg), raft_world(tg, [poon_on((-0.3, 0, 0.3), 2.2, poon_sit(tg, la=(1.0, 0.2, 0.6), ra=(1.0, 0.2, 0.6), lean=0.3)),
                                       gull(tg * 14 if u < 1 else 0.6).xf(M(trans(gp), roty(math.pi)))])]
    cam = Cam((-0.6, 1.3, 2.4), (0.8, 0.8, -1.1), 45)
    return merge(ms), cam, ENV_DAY, {}


def shot_rain(lt, dur, tg):
    """il tend la toile de son gilet pour récolter l'eau de pluie"""
    hold = [(-0.25, 1.2, 0.5), (0.25, 1.2, 0.5)]
    pose = poon_sit(tg, ik_l=hold[0], ik_r=hold[1], hp=-0.6)
    cam = Cam((1.8, 1.4, 2.4), (0, 0.9, 0.2), 48)
    canvas = box(0.62, 0.02, 0.45, (200, 190, 160), 'cloth').xf(trans(0, 1.2, 0.55))
    ms = [sea_at(tg, 'ocean_storm'), raft_world(tg, [poon_on((0, 0, 0), 0.0, pose), canvas], canvas=False), storm_rain(cam, tg, n=110)]
    return merge(ms), cam, ENV_STORM.copy(amb=0.5), {}


# ------------------------------------------------------------------ 14-15. le requin
def shot_shark(lt, dur, tg):
    """il hisse un requin sur le radeau ; le requin se débat et l'attaque"""
    t_att = WT(14, 'attaque.') - cut['shark'] - 0.2
    on = min(1.0, lt / 1.2)
    bend = 0.6 * math.sin(tg * 14) if on >= 1 else 0.2 * math.sin(tg * 8)
    sp = np.array([0.3 + 0.9 * (1 - on), 0.42 - 0.8 * (1 - on), 0.0])
    sh = shark(bend, jaw=0.5 + 0.5 * math.sin(tg * 10)).xf(M(trans(sp), roty(-0.4), rotx(0.15 * math.sin(tg * 12))))
    back = min(1.0, max(0.0, lt - t_att) * 3)
    pose = dict(ra=(1.4 - 0.6 * on, 0.4, 0.6), la=(1.4 - 0.6 * on, 0.4, 0.6), lean=-0.25 * back, ll=(0.3 * back, 0.3), rl=(-0.2 * back, 0.2))
    ms = [sea_at(tg), raft_world(tg, [poon_on((-0.7, 0, -0.3 + 0.0 * back), 1.2, pose), sh], tin=False)]
    cam = Cam((1.2, 1.4, 2.9), (-0.1, 0.7, 0), 50)
    return merge(ms), C2.shake(cam, 0.04 * back, tg), ENV_DAY, {}


def shot_fight(lt, dur, tg):
    """Poon lève le bidon d'eau à deux mains au-dessus du requin"""
    raise_ = 0.5 + 0.5 * math.sin(tg * 9)
    hy = 1.75 + 0.25 * raise_
    pose = dict(ik_l=(-0.82, hy, 0.15), ik_r=(-0.62, hy, 0.15), lean=0.15)
    tin = cyl(0.14, 0.14, 0.4, 8, (170, 165, 150), 'metal').xf(M(trans(-0.72, hy + 0.02, 0.15), rotz(math.pi / 2), trans(0, -0.2, 0)))
    sh = shark(0.5 * math.sin(tg * 15), 0.8).xf(M(trans(0.3, 0.42, 0.1), roty(-0.4)))
    ms = [sea_at(tg), raft_world(tg, [poon_on((-0.72, 0, -0.25), 0.9, pose), tin, sh], tin=False)]
    cam = Cam((0.4, 0.9, 2.6), (-0.3, 1.2, 0), 55)
    return merge(ms), C2.shake(cam, 0.05, tg), ENV_DAY, {}


def shot_fins(lt, dur, tg):
    """les ailerons sèchent au soleil, accrochés à la corde du radeau"""
    fins = []
    for k, x in enumerate((-0.6, -0.1, 0.4)):
        fins.append(Mesh([[(x, 0.7, -1.15), (x + 0.12, 0.42, -1.15), (x - 0.14, 0.45, -1.15)], [(x, 0.7, -1.16), (x - 0.14, 0.45, -1.16), (x + 0.12, 0.42, -1.16)]],
                         C((110, 116, 122))))
    pose = poon_sit(tg, la=(0.2, 0.1, 0.3), ra=(0.2, 0.1, 0.3), hy=0.6)
    cam = cam_lerp(Cam((-0.6, 1.0, 1.0), (-0.1, 0.55, -1.15), 45), Cam((-0.5, 0.95, 0.7), (-0.1, 0.55, -1.15), 42), lt / dur)
    ms = [sea_at(tg), raft_world(tg, fins, knots=12, tin=False, canvas=False), sun_disc((80, 300, -600), 25)]
    return merge(ms), cam, ENV_HOT, {}


# ------------------------------------------------------------------ 16-18. les pêcheurs brésiliens
BOAT_POS = np.array([7.0, 0, -2.0])


def boat_world(tg, x_off=0.0, people=None, yaw=math.pi):
    pos = BOAT_POS + np.array([x_off, 0, 0])
    ppl = people if people is not None else [
        FISH[0].mesh((0.9, 0.65, -0.3), -math.pi / 2, dict(ra=(1.7, 0.1, 0.2), hy=0.2)),
        FISH[1].mesh((-0.6, 0.65, 0.4), -math.pi / 2, dict(la=(2.6, 0.4, 0.4), hy=-0.2)),
        FISH[2].mesh((-2.2, 0.65, -0.1), -math.pi / 2 + 0.3, sit_pose(drop=0.45))]
    m = merge([fishing_boat(emu=True)] + ppl)
    return m.xf(M(trans(pos), roty(yaw), trans(0, 0.04 * math.sin(tg * 1.5), 0), rotx(0.03 * math.sin(tg * 1.2))))


def shot_fishermen(lt, dur, tg):
    """5 avril 1943 : une barque à voile approche, les pêcheurs le montrent du doigt"""
    xo = 4.0 - lt * 1.2
    cam = cam_lerp(Cam((-2.5, 1.5, 5.0), (6.5, 1.6, -2), 52), Cam((-2.2, 1.45, 4.6), (6.0, 1.6, -2), 50), lt / dur)
    ms = [sea_at(tg, amp=0.12), raft_world(tg, [poon_on((0, 0, 0), 1.3, poon_sit(tg, hp=0.2, ra=(1.2, 0.5, 0.3)), POON)], knots=12, k=0.6), boat_world(tg, xo)]
    return merge(ms), cam, ENV_DAY, {}


def shot_bow(lt, dur, tg):
    """la barque arrive tout près du radeau : les pêcheurs se penchent (petite sculpture d'émeu sur l'étrave)"""
    xo = -2.2 - lt * 0.5
    cam = cam_lerp(Cam((-1.0, 1.5, 2.8), (2.6, 1.0, -1.8), 55), Cam((-0.8, 1.45, 2.5), (2.6, 1.0, -1.8), 53), lt / dur)
    ms = [sea_at(tg, amp=0.12), raft_world(tg, [poon_on((0, 0, 0), 1.3, poon_sit(tg, hp=0.3, lean=0.2), POON_C)], knots=12, k=0.5), boat_world(tg, xo)]
    return merge(ms), cam, ENV_DAY, {}


def shot_carry(lt, dur, tg):
    """deux pêcheurs le portent, un bras sur chaque épaule"""
    c = np.array([0.0, 0.27, 0.3])
    weak = dict(drop=0.12, lean=0.2, hp=0.35, ll=(0.2, 0.4), rl=(-0.1, 0.3), la=(0.3, 1.45, 0.5), ra=(0.3, 1.45, 0.5))
    ppl = [POON_C.mesh(tuple(c), 0.0, weak),
           FISH[0].mesh(tuple(c + np.array([-0.55, 0, 0.05])), 0.0, dict(ik_r=tuple(c + np.array([-0.12, 0.95, 0.1])), la=(0.2, 0.1, 0.3))),
           FISH[1].mesh(tuple(c + np.array([0.55, 0, 0.05])), 0.0, dict(ik_l=tuple(c + np.array([0.12, 0.95, 0.1])), ra=(0.2, 0.1, 0.3)))]
    m = merge([raft(12, tin=False, flashlight=False, canvas=False)] + ppl).xf(bob(tg, 0.4))
    cam = cam_lerp(Cam((0.8, 1.5, 4.6), (0, 1.0, 0.3), 48), Cam((0.6, 1.5, 4.1), (0, 1.05, 0.3), 46), lt / dur)
    ms = [sea_at(tg, amp=0.1), m, boat_world(tg, -4.5, people=[FISH[2].mesh((0.9, 0.65, -0.3), -math.pi / 2, dict(ra=(1.8, 0.1, 0.2)))])]
    return merge(ms), cam, ENV_DAY, {}


# ------------------------------------------------------------------ 19-20. le record
def hosp():
    ms = [box(7, 0.05, 7, (255, 255, 255), 'tile_lab', ts=1.0), box(7, 3, 0.1, (230, 232, 225), 'hospital').xf(trans(0, 0, -2.8)),
          box(0.1, 3, 7, (225, 228, 220), 'hospital').xf(trans(-2.5, 0, 0)), box(1.0, 1.0, 0.05, (255, 255, 255), 'window').xf(trans(0.8, 1.4, -2.74))]
    ms.append(box(0.9, 0.5, 2.0, (200, 200, 205), 'metal').xf(trans(-0.6, 0, -1.6)))          # lit
    ms.append(box(0.88, 0.14, 1.95, (245, 245, 240)).xf(trans(-0.6, 0.5, -1.6)))               # matelas
    ms.append(box(0.9, 0.9, 0.06, (200, 200, 205), 'metal').xf(trans(-0.6, 0, -2.6)))
    ms.append(box(0.5, 0.15, 0.3, (250, 250, 248)).xf(trans(-0.6, 0.64, -2.35)))               # oreiller
    ms.append(box(0.45, 0.7, 0.4, (180, 160, 130)).xf(trans(0.3, 0, -2.3)))                    # table de nuit
    ms.append(bottle(0.2, 0.04, (200, 220, 230), alpha=0.6).xf(trans(0.3, 0.7, -2.3)))
    ms.append(box(1.2, 0.05, 0.6, (255, 255, 255), 'newspaper').xf(M(trans(0.9, 0.55, -1.0), roty(0.3))))
    ms.append(box(0.45, 0.45, 0.45, (120, 85, 55)).xf(trans(1.1, 0, -0.6)))                      # tabouret
    return merge(ms)


HOSP = hosp()


def shot_hospital(lt, dur, tg):
    """à l'hôpital : Poon, assis dans son lit, répond à un journaliste qui prend des notes"""
    pose = sit_pose(drop=0.08, ll=(1.5, 0.0), rl=(1.5, 0.0), lean=-0.1, ra=(0.8, 0.3, 0.6), la=(0.3, 0.1, 0.2), hy=0.5)
    bed_top = 0.64
    poon = POON.mesh((-0.6, bed_top + 0.1 - 0.85, -2.15), 0.0, pose)
    blanket = box(0.86, 0.12, 1.1, (200, 210, 225), 'cloth').xf(trans(-0.6, bed_top, -1.2))
    rep = DOC.mesh((0.6, 0, -0.9), -1.9, dict(ik_r=(0.4, 1.15, -0.65), ik_l=(0.45, 1.1, -0.8), hp=0.2))
    note = box(0.12, 0.16, 0.02, (245, 245, 240)).xf(M(trans(0.43, 1.12, -0.72), rotx(-0.8)))
    cam = cam_lerp(Cam((-1.9, 1.6, 0.6), (-0.3, 0.95, -1.6), 50), Cam((-1.7, 1.55, 0.4), (-0.3, 0.95, -1.6), 48), lt / dur)
    return merge([HOSP, poon, blanket, rep, note]), cam, ENV_HOSP, {}


def shot_record(lt, dur, tg):
    """le radeau vide, au coucher du soleil"""
    u = lt / max(dur, 0.1)
    cam = Cam((-5 + 2 * u, 1.5, 6 - u), (0, 0.6, 0), 48)
    ms = [sea_at(tg, 'ocean_dusk'), raft_world(tg, [], knots=12, tin=False, canvas=False, flashlight=False), sun_disc((-150, 25, -600), 26, (255, 190, 110))]
    return merge(ms), cam, ENV_DUSK, {}


# ------------------------------------------------------------------ 21-22. la marine le refuse
def office():
    ms = [box(8, 0.05, 8, (255, 255, 255), 'planks_grey'), box(8, 3, 0.1, (215, 210, 195), 'plaster').xf(trans(0, 0, -3)),
          box(0.1, 3, 8, (205, 200, 185), 'plaster').xf(trans(-3, 0, 0))]
    ms.append(bench_table(1.8, 0.9, 0.78, (255, 255, 255), 'wood_dark').xf(trans(0, 0, -1.6)))
    ms.append(box(1.2, 0.8, 0.03, (255, 255, 255), 'flag_us').xf(trans(1.3, 1.6, -2.94)))       # drapeau au mur
    ms.append(box(0.7, 0.9, 0.02, (40, 50, 100)).xf(trans(-1.3, 1.5, -2.94)))                     # affiche de recrutement
    ms.append(box(0.5, 0.25, 0.022, (240, 240, 240)).xf(trans(-1.3, 1.7, -2.93)))
    ms.append(box(0.3, 0.1, 0.4, (240, 238, 228)).xf(trans(0.3, 0.78, -1.6)))
    ms.append(cyl(0.04, 0.05, 0.12, 6, (120, 40, 40)).xf(trans(-0.4, 0.78, -1.5)))               # tampon
    ms.append(box(0.6, 0.02, 1.4, (200, 190, 160)).xf(trans(0.2, 0.03, 0.4)))                      # tapis de mesure des pieds
    for k in range(6):
        ms.append(box(0.6, 0.005, 0.01, (60, 60, 60)).xf(trans(0.2, 0.045, -0.2 + k * 0.24)))
    return merge(ms)


OFFICE = office()


def shot_navy(lt, dur, tg):
    """bureau de recrutement de la marine américaine : Poon en costume devant l'officier"""
    ms = [OFFICE, OFFICER.mesh((0.0, 0, -2.3), 0.0, sit_pose(drop=0.45, la=(1.2, 0.1, 0.6), ra=(1.2, 0.1, 0.6), hy=0.1)),
          box(0.5, 0.45, 0.5, (90, 70, 50)).xf(trans(0, 0, -2.4)), POON_SUIT.mesh((0.3, 0, -0.4), math.pi, dict(hp=-0.05))]
    cam = cam_lerp(Cam((-1.7, 1.6, 1.3), (0.1, 1.05, -1.3), 52), Cam((-1.5, 1.55, 1.1), (0.1, 1.05, -1.3), 50), lt / dur)
    return merge(ms), cam, ENV_ROOM, {}


def shot_feet(lt, dur, tg):
    """pieds nus sur le tapis de mesure ; l'officier tamponne « REFUSÉ »"""
    t_stamp = 0.35
    ms = [OFFICE, POON_BARE.mesh((0.2, 0.04, 0.4), math.pi, dict(hp=0.3))]
    cam = Cam((0.9, 0.38, 1.25), (0.2, 0.1, 0.4), 50)
    return merge(ms), C2.shake(cam, 0.05 * C2.decay(lt, t_stamp, 8), tg), ENV_ROOM, {}


def shot_question(lt, dur, tg):
    u = lt / max(dur, 0.1)
    cam = Cam((4 - 2 * u, 1.3, 4.5 - u), (0, 0.9, 0), 50)
    ms = [sea_at(tg), raft_world(tg, [poon_on((0, 0, 0), 2.6, dict(hp=-0.1, hy=0.3 * math.sin(tg)))], knots=12)]
    return merge(ms), cam, ENV_DAY, {}


def shot_loop(lt, dur, tg):
    return shot_hook(lt, dur, tg, p=lt - dur)


# ------------------------------------------------------------------ montage
cut.add('hook', 0.0, shot_hook)
cut.add('hook_top', WT(0, 'radeau') - 0.1, shot_hook_top)
cut.add('intro', T(1), shot_intro)
cut.add('intro_ship', WT(1, 'cargo') - 0.1, shot_intro_ship)
cut.add('night', T(2), shot_night)
cut.add('torpedo', WT(2, 'torpille') - 0.15, shot_torpedo)
cut.add('hit', WT(2, 'frappe') - 0.5, shot_hit)
cut.add('sink', T(3), shot_sink)
cut.add('swim', T(4), shot_swim)
cut.add('climb', WT(4, 'tombe') - 0.05, shot_climb)
cut.add('items', T(5), shot_items)
cut.add('flash', T(6), shot_flashlight)
cut.add('days', T(7), shot_days)
cut.add('ship_pass', T(8), shot_ship_pass)
cut.add('ship_deck', WT(8, 'Ils', ) - 0.05, shot_ship_deck)
cut.add('plane', T(9), shot_plane)
cut.add('storm', WT(9, 'tempête') - 0.15, shot_storm)
cut.add('empty', T(10), shot_empty)
cut.add('dismantle', T(11), shot_dismantle)
cut.add('cta', T(12), shot_cta)
cut.add('fishing', T(13), shot_fishing)
cut.add('gull', WT(13, 'attrape') - 0.05, shot_gull)
cut.add('rain', WT(13, 'boit') - 0.05, shot_rain)
cut.add('shark', T(14), shot_shark)
cut.add('fight', T(15), shot_fight)
cut.add('fins', WT(15, 'fait') - 0.05, shot_fins)
cut.add('fishermen', T(16), shot_fishermen)
cut.add('bow', T(17), shot_bow)
cut.add('carry', T(18), shot_carry)
cut.add('hospital', T(19), shot_hospital)
cut.add('record', T(20), shot_record)
cut.add('navy', T(21), shot_navy)
cut.add('feet', T(22), shot_feet)
cut.add('question', T(23), shot_question)
cut.add('loop', T(24), shot_loop)


def day_counter():
    t0, t1 = cut['days'], cut['ship_pass']

    def ov(img, t):
        if t0 <= t < t1:
            n = 1 + int((t - t0) / (t1 - t0) * 40)
            C2.badge(f'JOUR {n}', t0, t1 - t0, y=700)(img, t)
    return ov


def stamp_refuse(t0, dur=1.6):
    f = ImageFont.truetype(INTER, 120)

    def ov(img, t):
        if not (t0 <= t < t0 + dur):
            return
        k = min(1.0, (t - t0) / 0.12)
        s = 1.6 - 0.6 * k
        layer = Image.new('RGBA', (760, 230), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.rectangle([8, 8, 752, 222], outline=(210, 30, 30, 255), width=14)
        d.text((380, 118), 'REFUSÉ', font=f, fill=(210, 30, 30, 255), anchor='mm')
        layer = layer.rotate(-12, expand=True, resample=Image.NEAREST)
        layer = layer.resize((int(layer.size[0] * s * 0.9), int(layer.size[1] * s * 0.9)), Image.NEAREST)
        img.paste(layer, ((OW - layer.size[0]) // 2, 520 - layer.size[1] // 2), layer)
    return ov


tl.overlay = C2.overlays(
    C2.hook_title(['133 JOURS', 'SUR UN RADEAU'], 0.0, 2.6, y=250, accent=0),
    emu_pastille(3.3, 3.2, y=300),
    C2.badge('POON LIM, 24 ANS', WT(1, 'Poon') - 0.05, 1.8, y=700),
    C2.badge('23 NOVEMBRE 1942', T(2), 1.7, y=700),
    retiens(T(6) - 0.1, max(2.2, T(7) - T(6)), y=300),
    day_counter(),
    C2.badge('JOUR 55', T(10), T(11) - T(10), y=700),
    C2.cta(T(12) - 0.1, max(1.8, T(13) - T(12) + 0.05)),
    C2.badge('5 AVRIL 1943', T(16), 1.7, y=700),
    C2.badge('133 JOURS', T(17), 1.7, y=700),
    C2.badge('+ DE 1 000 KM', WT(17, 'dérivé') - 0.1, 1.8, y=700),
    C2.badge('RECORD : 133 JOURS', T(20), T(21) - T(20), y=700),
    stamp_refuse(T(22) + 0.3, 1.5),
    C2.badge('PIEDS PLATS', WT(22, 'pieds') - 0.05, 1.3, y=760),
    end_card(T(23), T(24) - T(23)),
)

subs = Subs(timing)


def build_audio(path):
    mx = A.Mixer(END)
    S = cut
    mx.add(A.waves(END), 0, 0.35)
    mx.add(C2.impact(), 0.0, 0.5)
    mx.add(A.whoosh(1.4), 0.3, 0.4)
    mx.add(A.gulls(4), 0.5, 0.25)
    mx.add(A.whoosh(0.8), S['hook_top'], 0.35)
    mx.add(A.footsteps(2.0, 2.4), S['intro'], 0.3)
    mx.add(C2.ship_horn(2.0), S['intro_ship'] + 0.1, 0.35)
    mx.add(A.engine_hum(5, 45), S['night'], 0.3, length=S['sink'] - S['night'])
    mx.add(C2.underwater(2.0), S['torpedo'], 0.5, length=S['hit'] - S['torpedo'])
    mx.add(A.explosion(3.0), WT(2, 'frappe'), 0.9)
    mx.add(C2.impact(), WT(2, 'frappe'), 0.6)
    mx.add(C2.metal_groan(2.5), S['sink'], 0.6)
    mx.add(A.splash(0.7), S['swim'] + 0.2, 0.4)
    for k in range(4):
        mx.add(A.splash(0.5), S['swim'] + 0.6 + k * 0.7, 0.25)
    mx.add(A.thwack(0.3), S['climb'] + 1.0, 0.4)
    for w in ITEM_POS:
        mx.add(C2.pop(), WT(5, w), 0.4)
    mx.add(C2.riser(1.2), T(6) - 0.4, 0.3)
    mx.add(C2.ding(), T(6) + 0.1, 0.4)
    for k in range(6):
        mx.add(A.tick(), S['days'] + 0.4 + k * 0.45, 0.3)
    mx.add(C2.ship_horn(2.5), S['ship_pass'] + 0.3, 0.4)
    mx.add(A.engine_hum(3, 70), S['plane'], 0.5)
    mx.add(A.rain(S['empty'] - S['storm']), S['storm'], 0.5)
    mx.add(A.thunder_close(4.0), S['storm'] + 0.2, 0.7)
    mx.add(A.wind(3), S['storm'], 0.5)
    mx.add(A.clank(0.3), S['dismantle'] + 0.4, 0.4)
    mx.add(A.ratchet(0.6), WT(11, 'transforme'), 0.4)
    mx.add(C2.pop(), T(12) + 0.05, 0.5)
    mx.add(C2.ding(), T(12) + max(1.8, T(13) - T(12)) * 0.62, 0.4)
    mx.add(A.splash(0.6), S['fishing'] + 1.1, 0.5)
    mx.add(A.gulls(2), S['gull'], 0.5)
    mx.add(A.rain(S['shark'] - S['rain']), S['rain'], 0.4)
    mx.add(A.splash(0.9), S['shark'] + 0.6, 0.7)
    mx.add(A.thwack(0.3), S['shark'] + 1.3, 0.6)
    for k in range(3):
        mx.add(A.thwack(0.3), S['fight'] + 0.25 + k * 0.7, 0.6)
    mx.add(A.gulls(3), S['fins'], 0.3)
    mx.add(A.wind(4), S['fishermen'], 0.25)
    mx.add(A.crowd(2.0), S['fishermen'] + 1.0, 0.15)
    mx.add(A.gulls(4), S['bow'], 0.3)
    mx.add(A.waves(S['hospital'] - S['carry']), S['carry'], 0.3)
    mx.add(A.tick(), S['hospital'] + 0.6, 0.2)
    mx.add(C2.record_scratch(), S['feet'] + 0.1, 0.25)
    mx.add(A.thwack(0.3), T(22) + 0.3, 0.9)
    mx.add(A.gulls(3), S['question'], 0.25)
    C2.cut_sounds(mx, list(cut.st.values()), 0.08)
    mx.save(path)


if __name__ == '__main__':
    run(tl, subs, HERE, 'Good2No_ep25_Poon_Lim', build_audio, sys.argv)
