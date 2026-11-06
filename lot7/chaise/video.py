"""Ép. 22 — Larry Walters, l'homme sur une chaise de jardin (2 juillet 1982)."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n/lot7']
from props7 import *
from video_core import *

HERE = '/home/claude/g2n/lot7/chaise'
timing = load_timing(os.path.join(HERE, 'timing.json'))
tl = Timeline(timing)
T, WT = tl.T, tl.word_t
END = timing[-1]['t1'] + 0.3
tl.duration = lambda: END
cut = Cut(tl)

# ------------------------------------------------------------------ personnages
make_face('larry', skin=(228, 184, 148), hair_col=(85, 60, 38))
make_face('larry_closed', skin=(228, 184, 148), eyes_closed=True)
make_face('kid', skin=(232, 190, 155))
make_face('officer', skin=(215, 170, 135), mustache=True, hair_col=(50, 40, 30))
make_face('pilot', skin=(222, 178, 140))
make_face('pilot2', skin=(150, 105, 75), mustache=True, hair_col=(30, 25, 20))
make_face('rep1', skin=(225, 182, 150))
make_face('rep2', skin=(170, 120, 90))
make_face('rep3', skin=(232, 196, 165))
LARRY = Human('larry', skin=(228, 184, 148), shirt=(70, 108, 165), pants=(255, 255, 255), pants_tex='denim', hair=(85, 60, 38), shoes=(70, 50, 35))
KID = Human('kid', skin=(232, 190, 155), shirt=(200, 70, 60), pants=(255, 255, 255), pants_tex='denim', hair=(110, 75, 45), height=0.62, build=0.85)
OFFICER = Human('officer', skin=(215, 170, 135), shirt=(70, 95, 140), pants=(55, 75, 115), hair=(50, 40, 30), hat='kepi', hat_col=(55, 75, 115),
                tie=(30, 35, 50))
PILOT = Human('pilot', skin=(222, 178, 140), shirt=(235, 235, 238), pants=(30, 35, 55), hair=(90, 70, 50), tie=(30, 35, 55))
PILOT2 = Human('pilot2', skin=(150, 105, 75), shirt=(235, 235, 238), pants=(30, 35, 55), hair=(30, 25, 20), tie=(30, 35, 55))
CTRL = Human('rep1', skin=(225, 182, 150), shirt=(220, 215, 190), pants=(80, 70, 60), hair=(60, 45, 30))
REPS = [Human('rep1', skin=(225, 182, 150), shirt=(200, 190, 160), pants=(80, 70, 60), hair=(60, 45, 30), jacket=(120, 95, 70)),
        Human('rep2', skin=(170, 120, 90), shirt=(240, 240, 235), pants=(40, 40, 50), hair=(30, 25, 20), tie=(150, 40, 40)),
        Human('rep3', skin=(232, 196, 165), shirt=(170, 60, 70), pants=(50, 50, 60), hair=(170, 120, 60))]
FAA = Human('officer', skin=(215, 170, 135), shirt=(240, 240, 235), pants=(45, 45, 55), hair=(50, 40, 30), jacket=(50, 55, 70), tie=(120, 30, 30))


def gun_m():
    """pistolet à plombs (petit, jamais en gros plan dans la main)"""
    return merge([cyl(0.014, 0.014, 0.3, 5, (55, 55, 60)).xf(M(trans(0, 0.03, -0.02), rotx(math.pi / 2))),
                  box(0.04, 0.06, 0.16, (40, 40, 42)).xf(trans(0, 0.0, -0.06)),
                  box(0.04, 0.13, 0.06, (120, 75, 40)).xf(M(trans(0, -0.11, -0.1), rotx(0.35))),
                  box(0.01, 0.03, 0.04, (40, 40, 42)).xf(trans(0, -0.04, -0.03))])


GUN_HAND = gun_m().xf(M(rotx(-math.pi / 2)))
AIRLINER = airliner()

# ------------------------------------------------------------------ décors
ENV_DAY = Env(sky_top=(70, 130, 210), sky_hor=(200, 215, 230), fog=(200, 210, 222), fog_near=60, fog_far=420, amb=0.5, light=(-0.4, 0.85, 0.3))
ENV_SKY = Env(sky_top=(30, 70, 165), sky_hor=(160, 190, 230), fog=(170, 195, 230), fog_near=150, fog_far=1800, amb=0.55, light=(-0.4, 0.8, 0.4))
ENV_COLD = ENV_SKY.copy(light_col=(200, 220, 255), amb=0.5)
ENV_ROOM = Env(sky_top=(60, 58, 55), sky_hor=(60, 58, 55), fog=(50, 48, 45), fog_near=10, fog_far=40, amb=0.62, light=(0.3, 0.8, 0.5))
ENV_DESERT = Env(sky_top=(80, 140, 215), sky_hor=(230, 215, 190), fog=(225, 210, 185), fog_near=80, fog_far=900, amb=0.55)


def yard():
    """jardin de San Pedro : pelouse, maison, palissade, palmiers, barbecue, jeep, bouteilles d'hélium"""
    ms = [ground(-60, -60, 60, 60, 'lawn', ts=3.0), suburb_house(11, 8, 3.0).xf(trans(0, 0, -12)),
          suburb_house(10, 8, 3.0, roof=(140, 90, 70)).xf(M(trans(-18, 0, -8), roty(0.3)))]
    for x in np.arange(-14, 15, 2.0):
        ms.append(box(2.0, 1.8, 0.1, (255, 255, 255), 'fence').xf(trans(x, 0, 9)))
    for z in np.arange(-6, 9, 2.0):
        ms.append(box(0.1, 1.8, 2.0, (255, 255, 255), 'fence').xf(trans(14, 0, z)))
        ms.append(box(0.1, 1.8, 2.0, (255, 255, 255), 'fence').xf(trans(-14, 0, z)))
    ms += [palm(9, 1).xf(trans(-9, 0, -4)), palm(10, 2).xf(trans(10, 0, 5)), palm(8, 3).xf(trans(18, 0, -20)), palm(11, 4).xf(trans(-20, 0, 14))]
    # barbecue, table de jardin, tuyau d'arrosage, massif de fleurs
    ms.append(cyl(0.35, 0.3, 0.3, 8, (40, 40, 42)).xf(trans(-5, 0.7, -5)))
    ms.append(rod((-5, 0, -5), (-5, 0.7, -5), 0.03, (40, 40, 42), n=4))
    ms.append(bench_table(1.6, 1.0, 0.75, (255, 255, 255), 'planks_white').xf(trans(-6, 0, 2)))
    ms.append(grass_tufts(-13, -7, 13, 8.5, 160, 2, col=(70, 125, 50), h=0.25, flowers=0.15))
    ms.append(jeep().xf(M(trans(4.5, 0, -2.5), roty(-0.4))))
    for i in range(4):
        ms.append(cyl(0.12, 0.12, 1.5, 6, (90, 110, 90)).xf(trans(-2.6 + i * 0.3, 0, -3.2)))
        ms.append(cyl(0.05, 0.05, 0.12, 5, (180, 180, 180)).xf(trans(-2.6 + i * 0.3, 1.5, -3.2)))
    return merge(ms)


YARD = yard()
EMU_DECO = merge([cyl(0.3, 0.35, 0.18, 8, (180, 178, 170), 'concrete'), emu_mesh((0, 0.18, 0), 0, scale_=0.7)])   # nain de jardin version émeu


def suburb_aerial():
    rr = np.random.default_rng(5)
    ms = [ground(-400, -400, 400, 400, 'lawn', ts=6.0)]
    # routes nettement au-dessus du sol (pas de scintillement vu de haut) ; les croisements sont décalés en hauteur
    for z in np.arange(-300, 300, 40):
        ms.append(box(800, 0.1, 8, (255, 255, 255), 'asphalt', ts=8).xf(trans(0, 0.35, z)))
    for x in np.arange(-300, 300, 60):
        ms.append(box(8, 0.1, 800, (255, 255, 255), 'asphalt', ts=8).xf(trans(x, 0.6, 0)))
    for z in np.arange(-300, 300, 40):
        for x in np.arange(-300, 300, 15):
            if x % 60 < 10:
                continue
            for side in (-1, 1):
                ms.append(suburb_house(rr.uniform(8, 11), 8, 3.0, roof=[(160, 70, 50), (140, 90, 70), (110, 110, 115)][rr.integers(0, 3)]).xf(
                    trans(x + rr.uniform(-1, 1), 0, z + side * 11)))
            if rr.random() < 0.3:
                ms.append(palm(rr.uniform(8, 12), int(rr.integers(0, 99))).xf(trans(x + 5, 0, z + 5)))
    return merge(ms)


AERIAL = suburb_aerial()


def sky_world(seed=0):
    """vue en altitude : mer de nuages et sol très loin en dessous"""
    rr = np.random.default_rng(seed)
    ms = [grid(-6000, -6000, 6000, 6000, 6, 6, None, (255, 255, 255), 'patchwork', 400.0).xf(trans(0, -1500, 0))]
    for i in range(60):
        x, z = rr.uniform(-900, 900), rr.uniform(-900, 900)
        r = rr.uniform(40, 90)
        ms.append(sphere(r, 8, 4, (255, 255, 255), 'cloudtop', sy=0.35).xf(trans(x, -160 + rr.uniform(-15, 10), z)))
    for i in range(6):
        ms.append(sphere(rr.uniform(15, 25), 7, 4, (255, 255, 255), 'cloudtop', sy=0.4).xf(trans(rr.uniform(-200, 200), rr.uniform(-30, 30), rr.uniform(-300, -120))))
    return merge(ms)


SKYW = sky_world()


def highway():
    ms = [ground(-300, -300, 300, 300, 'desert', ts=8.0), box(600, 0.1, 14, (255, 255, 255), 'asphalt', ts=6).xf(trans(0, 0.04, 0))]
    for x in np.arange(-300, 300, 6):
        ms.append(box(3, 0.04, 0.15, (240, 220, 80)).xf(trans(x, 0.14, 0)))
    rr = np.random.default_rng(3)
    for i in range(40):
        x, z = rr.uniform(-280, 280), rr.uniform(-200, -12) if rr.random() < 0.5 else rr.uniform(12, 200)
        ms.append(rock(rr.uniform(0.5, 2.5), i, (220, 190, 150)).xf(trans(x, 0, z)))
    for i in range(12):
        ms.append(cyl(rr.uniform(30, 60), 0, rr.uniform(40, 90), 7, (170, 140, 110)).xf(trans(rr.uniform(-500, 500), 0, rr.uniform(-600, -300))))
    for x in np.arange(-280, 280, 40):
        ms.append(power_pole(9).xf(trans(x, 0, -10)))
    return merge(ms)


HIGHWAY = highway()


def desert():
    rr = np.random.default_rng(8)
    ms = [ground(-800, -800, 800, 800, 'desert', ts=12.0)]
    for i in range(40):
        ms.append(cyl(rr.uniform(20, 70), 0, rr.uniform(20, 70), 7, (190, 150, 115)).xf(trans(rr.uniform(-700, 700), 0, rr.uniform(-800, -200))))
    for i in range(60):
        ms.append(rock(rr.uniform(0.5, 2.0), i, (210, 185, 150)).xf(trans(rr.uniform(-200, 200), 0, rr.uniform(-200, 100))))
    return merge(ms)


DESERT = desert()


def office():
    ms = [box(8, 0.05, 8, (255, 255, 255), 'planks_grey').xf(trans(0, 0, 0)), box(8, 3, 0.1, (210, 205, 190)).xf(trans(0, 0, -3)),
          box(0.1, 3, 8, (205, 200, 185)).xf(trans(-3, 0, 0)), box(0.1, 3, 8, (205, 200, 185)).xf(trans(3.5, 0, 0))]
    ms.append(bench_table(1.8, 0.9, 0.78, (255, 255, 255), 'wood_dark').xf(trans(0, 0, -1.6)))
    ms.append(box(0.6, 0.8, 0.02, (255, 255, 255), 'eyechart').xf(trans(-1.6, 1.2, -2.94)))
    ms.append(box(0.9, 0.6, 0.02, (255, 255, 255), 'poster_af').xf(trans(1.2, 1.4, -2.94)))
    ms.append(box(0.5, 1.1, 0.5, (90, 95, 100), 'metal').xf(trans(2.6, 0, -2.5)))
    ms.append(box(0.4, 0.1, 0.3, (240, 238, 228)).xf(trans(0.3, 0.78, -1.6)))
    ms.append(cyl(0.02, 0.02, 1.6, 4, (60, 60, 60)).xf(trans(-2.6, 0, -2.6)))
    return merge(ms)


def _eyechart(d, n):
    from PIL import ImageFont
    d.rectangle([0, 0, n, n], fill=(245, 245, 240))
    y = 0
    for txt, sz in (('E', 12), ('FP', 8), ('TOZ', 6), ('LPED', 5)):
        f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', sz)
        d.text((n / 2, y + sz / 2 + 1), txt, font=f, fill=(15, 15, 15), anchor='mm')
        y += sz + 1


tex_draw('eyechart', _eyechart, bg=(245, 245, 240))


def _poster_af(d, n):
    d.rectangle([0, 0, n, n], fill=(40, 60, 110))
    d.polygon([(4, 20), (28, 14), (16, 18), (12, 24)], fill=(230, 230, 235))
    d.rectangle([2, 26, n - 3, 29], fill=(200, 40, 45))
    d.ellipse([20, 3, 28, 11], fill=(240, 240, 245))
    d.ellipse([22, 5, 26, 9], fill=(200, 40, 45))


tex_draw('poster_af', _poster_af, bg=(40, 60, 110))
OFFICE = office()


def street():
    """rue de Long Beach : maisons, poteaux, câbles, voitures, feu de circulation"""
    rr = np.random.default_rng(12)
    ms = [ground(-120, -120, 120, 120, 'lawn', ts=4.0), box(240, 0.1, 10, (255, 255, 255), 'asphalt', ts=6).xf(trans(0, 0.04, 0)),
          box(240, 0.15, 2, (200, 198, 190), 'concrete', ts=3).xf(trans(0, 0, 6)), box(240, 0.15, 2, (200, 198, 190), 'concrete', ts=3).xf(trans(0, 0, -6))]
    for x in np.arange(-100, 100, 14):
        ms.append(suburb_house(rr.uniform(8, 11), 8, 3.0, roof=[(160, 70, 50), (140, 90, 70), (110, 110, 115)][rr.integers(0, 3)]).xf(M(trans(x, 0, -14), roty(math.pi))))
        ms.append(suburb_house(rr.uniform(8, 11), 8, 3.0, roof=[(160, 70, 50), (140, 90, 70), (110, 110, 115)][rr.integers(0, 3)]).xf(trans(x + 6, 0, 14)))
        if rr.random() < 0.5:
            ms.append(palm(rr.uniform(9, 12), int(rr.integers(0, 99))).xf(trans(x + 3, 0, 8)))
    poles = [(x, 7.5) for x in np.arange(-96, 100, 24)]
    for (x, z) in poles:
        ms.append(power_pole(10).xf(trans(x, 0, z)))
    ms.append(wires(poles, 10, 0.6))
    for i, x in enumerate((-30, -12, 18, 34)):
        c = [(170, 40, 40), (60, 90, 150), (220, 210, 190), (50, 110, 70)][i]
        ms.append(merge([box(1.8, 0.7, 4.4, c).xf(trans(0, 0.35, 0)), box(1.6, 0.55, 2.2, c).xf(trans(0, 1.05, -0.2)),
                         box(1.5, 0.45, 0.05, (120, 150, 170)).xf(trans(0, 1.05, 0.92))]).xf(M(trans(x, 0, 3.2 if i % 2 else -3.2), roty(math.pi / 2))))
    return merge(ms), poles


STREET, POLES = street()
LANDING = np.array([POLES[4][0] + 9.0, 0, 7.5])   # entre deux poteaux


def traffic_light(on=True):
    ms = [cyl(0.1, 0.1, 4.2, 6, (60, 60, 62)), box(0.4, 1.1, 0.35, (40, 40, 40)).xf(trans(0, 4.2, 0))]
    for i, c in enumerate(((220, 40, 40), (230, 180, 40), (40, 200, 90))):
        on_c = on and i == 0
        ms.append(box(0.22, 0.22, 0.05, c if on_c else (50, 50, 50), emis=1.0 if on_c else 0.0).xf(trans(0, 4.97 - i * 0.33, 0.18)))
    return merge(ms)


def tower():
    """tour de contrôle (LAX) + piste"""
    ms = [ground(-800, -800, 800, 800, 'grass_dry', ts=10.0), box(1500, 0.05, 45, (255, 255, 255), 'asphalt', ts=10).xf(trans(0, 0.02, 60))]
    for x in np.arange(-700, 700, 30):
        ms.append(box(12, 0.06, 0.8, (240, 240, 240)).xf(trans(x, 0.03, 60)))
    ms.append(cyl(5, 4, 36, 8, (230, 228, 220), 'concrete', ts=4).xf(trans(0, 0, 0)))
    ms.append(cyl(8, 9, 5, 8, (40, 70, 90), alpha=1.0).xf(trans(0, 36, 0)))
    ms.append(cyl(9.5, 8, 1.5, 8, (220, 220, 215)).xf(trans(0, 41, 0)))
    ms.append(cyl(0.2, 0.2, 6, 4, (200, 200, 200)).xf(trans(0, 42.5, 0)))
    ms.append(box(60, 12, 30, (215, 210, 200), 'concrete', ts=5).xf(trans(-60, 0, -40)))
    return merge(ms)


TOWER = tower()


def cockpit():
    ms = [box(3.0, 0.1, 3.0, (60, 60, 65)).xf(trans(0, -0.1, 0.0)), box(3.0, 1.0, 0.6, (45, 48, 52)).xf(trans(0, 0, 1.4))]
    for x in np.arange(-1.2, 1.3, 0.2):
        for y in (0.65, 0.85):
            ms.append(box(0.12, 0.1, 0.02, (30, 30, 30)).xf(trans(x, y, 1.1)))
            ms.append(box(0.06, 0.06, 0.03, (90, 220, 120) if (x * 10 + y * 7) % 3 > 1.5 else (240, 180, 60), emis=1.0).xf(trans(x, y + 0.01, 1.1)))
    # montants du pare-brise
    for x in (-1.5, -0.5, 0.5, 1.5):
        ms.append(box(0.08, 1.2, 0.08, (50, 52, 56)).xf(M(trans(x * 0.9, 1.0, 1.6), rotx(-0.4))))
    ms.append(box(3.0, 0.15, 0.6, (50, 52, 56)).xf(trans(0, 2.05, 1.2)))
    for s in (-1, 1):
        ms.append(box(0.6, 0.9, 0.15, (70, 60, 50)).xf(trans(s * 0.65, 0.3, -0.5)))
        ms.append(box(0.6, 0.15, 0.6, (70, 60, 50)).xf(trans(s * 0.65, 0.3, -0.15)))
    return merge(ms)


COCKPIT = cockpit()

# ------------------------------------------------------------------ chaise volante
_FC = {}


def fchair(popped=()):
    k = tuple(sorted(popped))
    if k not in _FC:
        _FC[k] = flying_chair(popped)
    return _FC[k]


def larry_sit(tg, **kw):
    p = sit_pose(drop=0.47, la=(0.35, 0.15, 0.7), ra=(0.35, 0.15, 0.7), hy=0.25 * math.sin(tg * 0.7), lean=-0.1)
    p.update(kw)
    return p


def chair_in_sky(tg, popped=(), pose=None, sway=True, y=0.0):
    sw = 0.04 * math.sin(tg * 1.1) if sway else 0.0
    m = merge([fchair(popped), LARRY.mesh((0, 0, -0.08), 0.0, pose or larry_sit(tg))])
    return m.xf(M(trans(0, y, 0), roty(0.3 * math.sin(tg * 0.15)), rotz(sw)))


def plane_at(p, z=-55, y=6.0, x0=-55.0, speed=48.0, dirx=1):
    x = x0 + p * speed
    return AIRLINER.xf(M(trans(x * dirx, y, z), roty(math.pi / 2 * dirx)))


def shot_hook(lt, dur, tg, p=None):
    """0 : Larry sur sa chaise au-dessus des nuages, un avion de ligne passe derrière lui"""
    p = lt if p is None else p
    cam = Cam((2.2 + 0.2 * p, 1.4, 4.6 - 0.15 * p), (0.0, 1.3 + 0.03 * p, -0.2), 52)
    pose = larry_sit(tg, hy=-0.6 - 0.25 * min(1.0, max(0.0, p + 0.5)), la=(0.9, 0.3, 0.3))
    ms = [SKYW, chair_in_sky(tg, pose=pose), plane_at(p)]
    return merge(ms), cam, ENV_SKY, {}


def shot_hook_low(lt, dur, tg):
    """contre-plongée sous la chaise : les ballons, et l'avion qui passe au-dessus"""
    cam = Cam((0.8, -2.5, 2.2), (0.0, 3.5, -1.0), 62, roll=0.1)
    ms = [SKYW, chair_in_sky(tg), plane_at(lt + 0.4, z=-40, y=30, x0=-40, speed=55)]
    return merge(ms), C2.shake(cam, 0.03, tg), ENV_SKY, {}


def shot_hook_wide(lt, dur, tg):
    """très large : un point minuscule au-dessus des nuages"""
    u = lt / max(dur, 0.1)
    cam = Cam((40 - 6 * u, 8, 55 - 8 * u), (0, 3, 0), 45)
    ms = [SKYW, chair_in_sky(tg), plane_at(lt + 1.5, z=-90, y=15, x0=-120, speed=60)]
    return merge(ms), cam, ENV_SKY, {}


# ------------------------------------------------------------------ présentation
def shot_intro(lt, dur, tg):
    """dans son jardin, Larry à côté de sa chaise, il fait coucou"""
    wave = 2.6 + 0.35 * math.sin(tg * 9)
    ms = [YARD, lawn_chair().xf(M(trans(1.2, 0, 0.5), roty(-0.5))), LARRY.mesh((0, 0, 0.5), 0.4, dict(ra=(wave, 0.35, 0.3), hy=0.1))]
    cam = cam_lerp(Cam((1.8, 1.6, 5.5), (0.4, 1.3, 0.3), 48), Cam((1.5, 1.6, 4.6), (0.4, 1.35, 0.3), 45), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_aerial(lt, dur, tg):
    u = lt / max(dur, 0.1)
    cam = Cam((-60 + 30 * u, 70, 120), (20 * u, 0, 0), 55)
    return AERIAL, cam, ENV_DAY.copy(fog_near=150, fog_far=700), {}


def shot_truck(lt, dur, tg):
    """chauffeur routier : le camion file sur l'autoroute"""
    x = -30 + lt * 22
    tr = truck(roll=lt * 22 / 0.55).xf(M(trans(x, 0, -3.5), roty(math.pi / 2)))
    larry = LARRY.mesh((x + 6.6, 2.0, -2.75), math.pi / 2, sit_pose(drop=0.45, la=(1.2, 0.0, 0.4), ra=(1.2, 0.0, 0.4)))
    cam = Cam((x + 15, 2.4, 11), (x + 6.0, 2.0, -3.5), 48)
    return merge([HIGHWAY, tr, larry]), C2.shake(cam, 0.02, tg), ENV_DESERT, {}


def shot_dream(lt, dur, tg):
    """petit, il fait l'avion dans le jardin pendant qu'un avion passe"""
    run = (lt * 2.0) % 8
    pk = np.array([-3 + lt * 1.6, 0, 1.5])
    kid = KID.mesh(tuple(pk), math.pi / 2, run_pose(tg * 9, la=(0.2, 1.5, 0.0), ra=(0.2, 1.5, 0.0), lean=0.15))
    plane = AIRLINER.xf(M(trans(-80 + lt * 30, 120, -150), roty(math.pi / 2)))
    cam = Cam(tuple(pk + np.array([1.5, 0.6, 4.5])), tuple(pk + np.array([1.0, 1.5, 0])), 55)
    return merge([YARD, kid, plane]), cam, ENV_DAY.copy(fog_far=900), dict(post_pil=C2.chain(C2.tint((255, 210, 150), 0.35), lambda im: C2.vignette(im, 0.6)))


def shot_office(lt, dur, tg):
    """armée de l'air : l'officier secoue la tête"""
    no = 0.45 * math.sin(tg * 9) * min(1.0, lt / 0.3)
    ms = [OFFICE, OFFICER.mesh((0.0, 0, -2.3), 0.0, sit_pose(drop=0.45, la=(1.2, 0.1, 0.6), ra=(1.2, 0.1, 0.6), hy=no)),
          box(0.5, 0.45, 0.5, (90, 70, 50)).xf(trans(0, 0, -2.4)), LARRY.mesh((0.2, 0, 0.0), math.pi, dict(hp=0.1))]
    cam = cam_lerp(Cam((1.6, 1.6, 0.9), (-0.2, 1.1, -2.1), 50), Cam((1.4, 1.55, 0.6), (-0.2, 1.1, -2.1), 48), lt / dur)
    return merge(ms), cam, ENV_ROOM, {}


def shot_eyechart(lt, dur, tg):
    cam = cam_lerp(Cam((-1.6, 1.5, -1.6), (-1.6, 1.55, -2.94), 50), Cam((-1.6, 1.55, -2.0), (-1.6, 1.6, -2.94), 50), lt / dur)
    return OFFICE, cam, ENV_ROOM, dict(post_pil=lambda im: C2.vignette(im, 0.8))


def boxes_pile(n_open=0):
    rr = np.random.default_rng(2)
    ms = []
    for i in range(14):
        x, z = (i % 4) * 0.62 - 1.0, (i // 4 % 2) * 0.62 - 0.3
        y = (i // 8) * 0.45
        ms.append(box(0.6, 0.45, 0.6, (190, 150, 100) * np.array([rr.uniform(0.9, 1.05)] * 3)).xf(M(trans(x, y, z), roty(rr.uniform(-0.1, 0.1)))))
        ms.append(box(0.62, 0.02, 0.1, (170, 140, 90)).xf(trans(x, y + 0.45, z)))
    return merge(ms)


BOXES = boxes_pile()


def shot_boxes(lt, dur, tg):
    """il achète 42 ballons météo : pile de cartons livrés dans le jardin"""
    ms = [YARD, BOXES.xf(trans(-1.5, 0, -1.0)), LARRY.mesh((0.8, 0, 0.6), -0.6, dict(la=(0.0, 0.1, 1.9), ra=(0.0, 0.1, 1.9), hy=-0.3))]
    cam = cam_lerp(Cam((2.8, 1.4, 4.5), (-0.6, 0.8, -0.6), 50), Cam((2.3, 1.3, 3.6), (-0.6, 0.8, -0.6), 46), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_inflate(lt, dur, tg):
    """gonflage : les ballons grossissent un à un, attachés à la chaise ; l'émeu (nain de jardin) est caché près des fleurs"""
    k = min(1.0, lt / max(dur, 0.1))
    rr = np.random.default_rng(1)
    ms = [YARD, lawn_chair().xf(trans(0, 0, 0)), EMU_DECO.xf(M(trans(-1.6, 0, -6.6), roty(0.5)))]
    for i in range(9):
        s = min(1.0, max(0.15, k * 1.6 - i * 0.08))
        p = np.array([math.cos(i * 0.7) * 1.0, 1.4 + i * 0.35 * s, math.sin(i * 0.7) * 1.0 - 0.6])
        ms.append(sphere(0.55 * s, 7, 5, (236, 226, 200), sy=1.15).xf(trans(p)))
        ms.append(rod((0, 0.95, -0.38), p - np.array([0, 0.55 * s, 0]), 0.006, (230, 230, 230), n=3))
    ms.append(rod((-2.15, 1.5, -3.2), (0.4, 1.0, -0.5), 0.02, (40, 40, 40), n=4))   # tuyau d'hélium
    ms.append(LARRY.mesh((0.9, 0, -0.9), -0.9, dict(ik_r=(0.45, 1.05, -0.55), la=(0.3, 0.1, 0.4), hp=-0.3)))
    cam = cam_lerp(Cam((-1.0, 1.5, 6.0), (0.0, 1.6, -0.3), 52), Cam((-0.6, 1.5, 5.2), (0.0, 1.7, -0.3), 50), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_tied(lt, dur, tg):
    """la chaise est prête, retenue au sol par une corde attachée à la jeep"""
    ms = [YARD, fchair(), rod((0, 0.4, 0.1), (3.8, 0.45, -1.0), 0.035, (215, 200, 160), n=5)]
    cam = cam_lerp(Cam((-6, 1.2, 9), (0, 4, 0), 55), Cam((-5, 1.0, 8), (0, 4.2, 0), 55), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


# inventaire sur l'assise
def sandwich():
    return merge([box(0.14, 0.03, 0.14, (225, 195, 140)), box(0.15, 0.015, 0.15, (90, 160, 70)).xf(trans(0, 0.03, 0)), box(0.14, 0.03, 0.14, (225, 195, 140)).xf(trans(0, 0.045, 0))])


def beer():
    return merge([cyl(0.033, 0.033, 0.12, 8, (200, 180, 60)).xf(trans(dx, 0, 0)) for dx in (-0.04, 0.04)] + [cyl(0.033, 0.033, 0.12, 8, (200, 180, 60)).xf(trans(0, 0, 0.07))])


def radio_m():
    return merge([box(0.12, 0.2, 0.06, (35, 35, 38)), cyl(0.006, 0.006, 0.25, 3, (30, 30, 30)).xf(trans(0.04, 0.2, 0)), box(0.06, 0.04, 0.01, (90, 200, 120), emis=0.8).xf(trans(0, 0.13, 0.031))])


ITEMS = [('sandwichs', sandwich(), (-0.14, 0.43, 0.12)), ('bières', beer(), (0.13, 0.43, 0.15)), ('radio', radio_m().xf(rotx(-math.pi / 2)), (-0.12, 0.45, -0.1)),
         ('pistolet', gun_m().xf(M(rotx(-math.pi / 2), rotz(0.4), roty(0))), (0.1, 0.46, -0.08))]
GUN_ON_SEAT = gun_m().xf(M(trans(0, 0.022, 0), roty(0.7), rotz(math.pi / 2), scale(1.3)))


def shot_bags(lt, dur, tg):
    """vue de dessus de l'assise : les objets apparaissent un à un"""
    ms = [YARD, lawn_chair()]
    for name, m, p in ITEMS:
        t_w = WT(6, name) - cut['bags']
        if lt >= t_w - 0.05:
            drop = max(0.0, 0.15 - (lt - t_w) * 1.2)
            mm = GUN_ON_SEAT if name == 'pistolet' else m
            ms.append(mm.xf(trans(p[0], 0.43 + drop, p[2])))
    cam = Cam((0.0, 1.55, 0.35), (0.0, 0.42, 0.02), 50)
    return merge(ms), cam, ENV_DAY, {}


def shot_detail(lt, dur, tg):
    """le pistolet à plombs, posé sur l'assise : on s'approche lentement"""
    ms = [YARD, lawn_chair()]
    for name, m, p in ITEMS:
        ms.append((GUN_ON_SEAT if name == 'pistolet' else m).xf(trans(p[0], 0.43, p[2])))
    g = np.array([0.1, 0.45, -0.08])
    cam = cam_lerp(Cam(tuple(g + np.array([0.45, 0.95, 0.75])), tuple(g), 42), Cam(tuple(g + np.array([0.32, 0.7, 0.55])), tuple(g), 40), lt / dur)
    return merge(ms), cam, ENV_DAY, dict(post_pil=lambda im: C2.vignette(im, 0.75))


# ------------------------------------------------------------------ le plan
PLAN = C2.chain(C2.tint((170, 200, 255), 0.4), lambda im: C2.vignette(im, 0.5))


def shot_plan_up(lt, dur, tg):
    """le plan (imaginé) : monter doucement au-dessus du quartier"""
    y = 2 + lt * 6
    ms = [AERIAL, chair_in_sky(tg, y=y)]
    cam = Cam((10, y + 4, 22), (0, y + 2, 0), 50)
    return merge(ms), cam, ENV_DAY.copy(fog_near=150, fog_far=700), dict(post_pil=PLAN)


def shot_plan_desert(lt, dur, tg):
    ms = [DESERT, chair_in_sky(tg, y=60)]
    cam = Cam((14 - lt * 2, 64, 20), (0, 62, 0), 50)
    return merge(ms), cam, ENV_DESERT, dict(post_pil=PLAN)


def shot_plan_pop(lt, dur, tg):
    n = min(6, int(lt / 0.25))
    pops = tuple(range(0, n * 6, 6))
    y = 30 - lt * 3
    ms = [DESERT, chair_in_sky(tg, popped=pops, y=y)]
    if n:
        ms.append(billboard((0.6, y + 4.5, 0.3), 1.2 * max(0, 1 - (lt % 0.25) / 0.2), 1.2, Cam((8, y + 3, 14), (0, y + 3, 0)), (255, 255, 255), 'puff', emis=0.6, alpha=0.8))
    cam = Cam((8, y + 3, 14), (0, y + 3, 0), 52)
    return merge(ms), cam, ENV_DESERT, dict(post_pil=PLAN)


# ------------------------------------------------------------------ la corde casse
def shot_rope(lt, dur, tg):
    t_snap = WT(9, 'casse') - cut['rope'] + 0.15
    snapped = lt > t_snap
    rise = max(0.0, lt - t_snap)
    a = np.array([0, 0.4 + rise * 3, 0.1])
    b = np.array([3.8, 0.45, -1.0])
    ms = [YARD, fchair().xf(trans(0, rise * 3, 0))]
    if not snapped:
        ms.append(rod(a, b, 0.035 + 0.006 * math.sin(tg * 40), (215, 200, 160), n=5))
    else:
        mid = (a + b) / 2
        ms.append(rod(a, a + (mid - a) * 0.5 + np.array([0, -0.5, 0]), 0.035, (215, 200, 160), n=5))
        ms.append(rod(b, b + np.array([-0.4, 0.2 - min(0.6, rise), 0.2]), 0.035, (215, 200, 160), n=5))
    cam = Cam((1.9, 1.6, 5.6), (1.9, 0.7, -0.45), 60)
    return merge(ms), C2.shake(cam, 0.06 * C2.decay(lt, t_snap, 6), tg), ENV_DAY, dict(flash=0.3 * C2.decay(lt, t_snap, 12))


def shot_rocket(lt, dur, tg):
    """la chaise part comme une fusée : vue du sol, elle rapetisse dans le ciel"""
    y = 2 + 6 * lt + 9 * lt * lt
    ms = [YARD, chair_in_sky(tg, y=y)]
    cam = Cam((3.0, 1.0, 5.0), (0, y * 0.9 + 3, 0), 62)
    return merge(ms), C2.shake(cam, 0.03, tg), ENV_DAY.copy(fog_far=900), {}


# ------------------------------------------------------------------ altitude
def shot_climb(lt, dur, tg):
    u = lt / max(dur, 0.1)
    ms = [SKYW.xf(trans(0, -200 * (1 - u), 0)), chair_in_sky(tg)]
    cam = Cam((7 - 2 * u, 2.5, 9 - 2 * u), (0, 2.5, 0), 55)
    return merge(ms), cam, ENV_SKY, {}


def shot_cold(lt, dur, tg):
    """il gèle : bras croisés, il grelotte, du givre tombe"""
    shiver = 0.04 * math.sin(tg * 45)
    pose = larry_sit(tg, la=(1.1, -0.6, 1.9), ra=(1.1, -0.6, 1.9), side=shiver, hp=0.15)
    ms = [SKYW, chair_in_sky(tg, pose=pose, sway=False)]
    cam = cam_lerp(Cam((1.2, 1.5, 2.6), (0, 1.2, -0.1), 48), Cam((1.0, 1.45, 2.2), (0, 1.25, -0.1), 45), lt / dur)
    ms.append(C2.particles((0, 1.5, 0.5), tg, cam, 50, (2, 2, 2), 0.8, 0.04, (235, 245, 255), 4))
    return merge(ms), cam, ENV_COLD, dict(post_pil=C2.tint((180, 210, 255), 0.35))


def shot_planes(lt, dur, tg):
    """deux avions de ligne le croisent"""
    ms = [SKYW, chair_in_sky(tg), plane_at(lt - 0.2, z=-30, y=4, x0=-70, speed=70), plane_at(lt - 0.8, z=-160, y=25, x0=90, speed=55, dirx=-1)]
    cam = Cam((3.0, 1.0, 7.0), (-1.0, 3.0, -15), 60)
    return merge(ms), C2.shake(cam, 0.05 * C2.decay(lt, 0.8, 2), tg), ENV_SKY, {}


def shot_cockpit(lt, dur, tg):
    """dans le cockpit : devant, un homme sur une chaise de jardin"""
    ms = [COCKPIT, PILOT.mesh((-0.65, 0.0, -0.45), 0.0, sit_pose(drop=0.45, la=(1.2, 0.1, 0.6), ra=(1.4, 0.4, 0.4), hy=0.2)),
          PILOT2.mesh((0.65, 0.0, -0.45), 0.0, sit_pose(drop=0.45, ra=(2.2, 0.3, 0.6) if lt > 0.6 else (1.2, 0.1, 0.6), la=(1.2, 0.1, 0.6), hy=-0.2)),
          SKYW.xf(trans(0, 0, 0)), chair_in_sky(tg).xf(trans(-6 + lt * 3, -1.2, 45 - lt * 10))]
    cam = Cam((0.0, 1.75, -1.6), (0.0, 1.4, 3.0), 62)
    return merge(ms), C2.shake(cam, 0.01, tg), ENV_SKY, {}


def shot_tower(lt, dur, tg):
    ms = [TOWER, AIRLINER.xf(M(trans(-300 + lt * 60, 120, 200), roty(math.pi / 2)))]
    cam = cam_lerp(Cam((35, 4, 70), (0, 38, 0), 55), Cam((30, 6, 62), (0, 39, 0), 52), lt / dur)
    return merge(ms), cam, ENV_DAY.copy(fog_far=1500), {}


def shot_wave(lt, dur, tg):
    """Larry fait coucou aux avions"""
    pose = larry_sit(tg, ra=(2.6 + 0.4 * math.sin(tg * 9), 0.4, 0.3), hy=-0.5)
    ms = [SKYW, chair_in_sky(tg, pose=pose)]
    cam = cam_lerp(Cam((-2.2, 1.6, 3.5), (0, 1.5, 0), 50), Cam((-1.9, 1.6, 3.0), (0, 1.5, 0), 48), lt / dur)
    return merge(ms), cam, ENV_SKY, {}


def shot_cta(lt, dur, tg):
    u = lt / max(dur, 0.1)
    ms = [SKYW, chair_in_sky(tg), sun_disc((-300, 260, -800), 30)]
    cam = Cam((-10 + 4 * u, 4, 14 - 2 * u), (0, 4, 0), 55)
    return merge(ms), cam, ENV_SKY, {}


# ------------------------------------------------------------------ la descente
def shot_gun_up(lt, dur, tg):
    pose = larry_sit(tg, ra=(2.9, 0.15, 0.1), hp=-0.5, hy=0.0, hand_r=GUN_HAND)
    ms = [SKYW, chair_in_sky(tg, pose=pose, sway=False)]
    cam = cam_lerp(Cam((1.8, 0.8, 2.8), (0, 2.2, -0.2), 55), Cam((1.6, 0.7, 2.4), (0, 2.4, -0.2), 55), lt / dur)
    return merge(ms), cam, ENV_SKY, {}


POP_TIMES = []


def shot_pop(lt, dur, tg):
    """Pan. Pan. Les ballons éclatent, la chaise descend"""
    t1 = WT(15, 'Pan.') - cut['pop']
    t2 = tl.timing[15]['words'][1][1] - cut['pop']
    pops = []
    if lt > t1 + 0.05:
        pops += [3, 17, 30]
    if lt > t2 + 0.05:
        pops += [8, 22, 38, 41]
    desc = max(0.0, lt - t2 - 0.3)
    pose = larry_sit(tg, ra=(2.9, 0.15, 0.1), hp=-0.5, hand_r=GUN_HAND)
    ms = [SKYW.xf(trans(0, desc * 6, 0)), chair_in_sky(tg, popped=tuple(pops), pose=pose)]
    cam = Cam((4.5, 2.0, 6.5), (0, 3.0, 0), 55)
    for tp in (t1, t2):
        if 0 <= lt - tp < 0.25:
            k = (lt - tp) / 0.25
            ms.append(billboard((0.8, 4.6, 0.4), 1.6 * k + 0.5, 1.6 * k + 0.5, cam, (255, 255, 255), 'puff', emis=0.7, alpha=1 - k))
    fl = max(C2.decay(lt, t1, 14), C2.decay(lt, t2, 14))
    return merge(ms), C2.shake(cam, 0.08 * fl, tg), ENV_SKY, dict(flash=0.25 * fl)


POPPED = (3, 17, 30, 8, 22, 38, 41)


def shot_drop_gun(lt, dur, tg):
    """le pistolet glisse et tombe dans le vide"""
    t0 = 0.35
    f = max(0.0, lt - t0)
    pose = larry_sit(tg, ra=(1.0, 0.6, 0.2), la=(0.8, 0.5, 0.2), hp=0.6, lean=0.25)
    ms = [SKYW, chair_in_sky(tg, popped=POPPED, pose=pose, sway=False)]
    g = np.array([0.45, 0.7 - 2.2 * f * f, 0.5 + f * 0.3])
    ms.append(gun_m().xf(M(trans(g), rotx(f * 5), rotz(f * 3), scale(1.5))))
    cam = Cam((1.9, 0.9, 2.4), (0.4, -0.9, 0.4), 58)
    return merge(ms), cam, ENV_SKY, {}


def shot_wires(lt, dur, tg):
    """Long Beach : la chaise descend et se prend dans les câbles électriques"""
    t_hit = 1.0
    y = 10.4 + max(0.0, (t_hit - lt)) * 4.0
    m = fchair(POPPED).xf(M(trans(LANDING[0], y - 1.8, 7.5), rotz(0.25 * min(1.0, max(0.0, lt - t_hit) * 2))))
    ms = [STREET, m, LARRY.mesh((LANDING[0], y - 1.8, 7.42), 0.0, larry_sit(tg, la=(2.4, 0.4, 0.4), ra=(2.4, 0.4, 0.4), hp=-0.2)).xf(trans(0, 0, 0))]
    cam = Cam((LANDING[0] + 7, 4, 22), (LANDING[0], 9.5, 7.5), 55)
    sp = []
    if lt > t_hit:
        for k in range(3):
            ph = (tg * 3 + k * 0.33) % 1.0
            sp.append(billboard((LANDING[0] - 1 + k, 9.8, 7.5), 0.8 * (1 - ph), 0.8 * (1 - ph), cam, (255, 255, 255), 'spark', emis=1.0))
    return merge(ms + sp), C2.shake(cam, 0.1 * C2.decay(lt, t_hit, 5), tg), ENV_DAY, dict(flash=0.4 * C2.decay(lt, t_hit, 10), flash_col=(200, 220, 255))


def blackout_street(on):
    return traffic_light(on).xf(trans(LANDING[0] - 14, 0, 5.8))


def shot_blackout(lt, dur, tg):
    """le feu tricolore et les maisons s'éteignent"""
    t_off = 0.5
    on = lt < t_off
    ms = [STREET, blackout_street(on), fchair(POPPED).xf(M(trans(LANDING[0], 8.6, 7.5), rotz(0.25)))]
    cam = Cam((LANDING[0] - 22, 2.0, 1.5), (LANDING[0] - 8, 4.5, 6.5), 55)
    env = ENV_DAY if on else ENV_DAY.copy(amb=0.42, light_col=(225, 220, 215))
    return merge(ms), cam, env, dict(flash=0.3 * C2.decay(lt, t_off, 12), flash_col=(0, 0, 0))


def shot_safe(lt, dur, tg):
    """Larry, debout sur le trottoir, indemne"""
    ms = [STREET, fchair(POPPED).xf(M(trans(LANDING[0], 8.6, 7.5), rotz(0.25))),
          LARRY.mesh((LANDING[0] + 1.2, 0.15, 4.6), math.pi - 0.2, dict(ra=(2.7, 0.3, 0.2), la=(2.7, 0.3, 0.2)))]
    cam = cam_lerp(Cam((LANDING[0] - 0.5, 1.5, 0.6), (LANDING[0] + 1.2, 3.0, 6.5), 58), Cam((LANDING[0] - 0.3, 1.5, 1.2), (LANDING[0] + 1.2, 3.1, 6.5), 55), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def mic():
    return merge([cyl(0.015, 0.015, 0.2, 4, (30, 30, 30)), sphere(0.035, 5, 3, (60, 60, 60)).xf(trans(0, 0.2, 0))])


def shot_press(lt, dur, tg):
    """les journalistes l'entourent, flashs"""
    c = np.array([LANDING[0] + 1.5, 0.15, 5.6])
    ms = [STREET, LARRY.mesh(tuple(c), 0.3, dict(la=(0.4, 0.2, 0.4), ra=(0.9, 0.3, 1.0), hy=0.2 * math.sin(tg * 2)))]
    for i, (dx, dz) in enumerate(((1.0, 1.2), (-0.9, 1.1), (0.2, 1.5))):
        p = c + np.array([dx, 0, dz])
        yaw = math.atan2(c[0] - p[0], c[2] - p[2])
        ms.append(REPS[i].mesh(tuple(p), yaw, dict(ra=(1.6, 0.0, 0.3), lean=0.1, hand_r=mic().xf(rotx(math.pi / 2)))))
    cam = Cam(tuple(c + np.array([-1.5, 1.6, 3.6])), tuple(c + np.array([0, 1.4, 0])), 50)
    fl = (tg * 3.7) % 1.0 < 0.06
    return merge(ms), cam, ENV_DAY, dict(flash=0.45 if fl else 0.0)


def shot_fine(lt, dur, tg):
    c = np.array([LANDING[0] + 1.5, 0.15, 5.6])
    ms = [STREET, LARRY.mesh(tuple(c), 0.0, dict(la=(0.2, 0.1, 0.3), ra=(0.2, 0.1, 0.3), hp=0.2)),
          FAA.mesh(tuple(c + np.array([0, 0, 1.1])), math.pi, dict(ra=(1.2, 0.1, 0.4), hy=0.1))]
    cam = cam_lerp(Cam(tuple(c + np.array([2.4, 1.6, 0.6])), tuple(c + np.array([0, 1.3, 0.55])), 50), Cam(tuple(c + np.array([2.1, 1.6, 0.6])), tuple(c + np.array([0, 1.3, 0.55])), 48), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_question(lt, dur, tg):
    u = lt / max(dur, 0.1)
    ms = [SKYW, chair_in_sky(tg), sun_disc((-300, 260, -800), 30)]
    cam = Cam((9 - 3 * u, 3.0, 11 - 3 * u), (0, 3.2, 0), 55)
    return merge(ms), cam, ENV_SKY, {}


def shot_loop(lt, dur, tg):
    """fin en boucle : on rejoint exactement le premier plan"""
    return shot_hook(lt, dur, tg, p=lt - dur)


# ------------------------------------------------------------------ montage
cut.add('hook', 0.0, shot_hook)
cut.add('hook_low', WT(0, 'croise') - 0.05, shot_hook_low)
cut.add('hook_wide', WT(0, 'mètres') - 0.3, shot_hook_wide)
cut.add('intro', T(1), shot_intro)
cut.add('aerial', WT(1, 'Californie,') - 0.05, shot_aerial)
cut.add('truck', T(2), shot_truck)
cut.add('dream', WT(2, 'depuis') - 0.05, shot_dream)
cut.add('office', T(3), shot_office)
cut.add('eyechart', WT(3, 'vue') - 0.1, shot_eyechart)
cut.add('boxes', T(4), shot_boxes)
cut.add('inflate', T(5), shot_inflate)
cut.add('tied', WT(5, 'attache') - 0.05, shot_tied)
cut.add('bags', T(6), shot_bags)
cut.add('detail', T(7), shot_detail)
cut.add('plan_up', T(8), shot_plan_up)
cut.add('plan_desert', WT(8, 'flotter') - 0.05, shot_plan_desert)
cut.add('plan_pop', WT(8, 'éclater') - 0.05, shot_plan_pop)
cut.add('rope', T(9), shot_rope)
cut.add('rocket', WT(9, 'Et') - 0.05, shot_rocket)
cut.add('climb', T(10), shot_climb)
cut.add('cold', WT(10, 'gèle.') - 0.05, shot_cold)
cut.add('planes', T(11), shot_planes)
cut.add('cockpit', T(12), shot_cockpit)
cut.add('tower', WT(12, 'tour') - 0.1, shot_tower)
cut.add('wave', WT(12, 'homme…') - 0.05, shot_wave)
cut.add('cta', T(13), shot_cta)
cut.add('gun_up', T(14), shot_gun_up)
cut.add('pop', T(15), shot_pop)
cut.add('drop_gun', T(16), shot_drop_gun)
cut.add('wires', T(17), shot_wires)
cut.add('blackout', T(18), shot_blackout)
cut.add('safe', T(19), shot_safe)
cut.add('press', T(20), shot_press)
cut.add('fine', T(21), shot_fine)
cut.add('question', T(22), shot_question)
cut.add('loop', T(23), shot_loop)


def altitude_counter():
    t0, t1 = cut['climb'], cut['cold']

    def ov(img, t):
        if t0 <= t < t1 + 0.6:
            u = min(1.0, (t - t0) / (t1 - t0))
            n = int(round(5000 * u ** 1.4 / 50) * 50)
            C2.badge(f'{n:,} M'.replace(',', ' '), t0, t1 - t0 + 0.6, y=700)(img, t)
    return ov


tl.overlay = C2.overlays(
    C2.hook_title(['IL VOLE SUR UNE', 'CHAISE DE JARDIN'], 0.0, 2.6, y=250, accent=1),
    emu_pastille(3.3, 3.2, y=300),
    C2.badge('CALIFORNIE, 1982', WT(1, 'Californie,') - 0.05, 1.6, y=700),
    C2.badge('42 BALLONS MÉTÉO', WT(4, '42') - 0.1, 1.9, y=700),
    retiens(T(7) - 0.1, max(2.0, T(8) - T(7)), y=300),
    altitude_counter(),
    C2.cta(T(13) - 0.1, max(1.8, T(14) - T(13) + 0.05)),
    C2.badge('45 MINUTES PLUS TARD', T(14), 1.6, y=700),
    C2.badge('LONG BEACH', T(18), 1.3, y=700),
    C2.badge('20 MIN SANS COURANT', WT(18, '20') - 0.1, 1.6, y=700),
    C2.badge('AMENDE : 1 500 $', WT(21, '1') - 0.1, 2.0, y=700),
    end_card(T(22), T(23) - T(22)),
)

subs = Subs(timing)


def build_audio(path):
    mx = A.Mixer(END)
    S = cut
    mx.add(A.wind(END), 0, 0.22, length=S['intro'])
    mx.add(A.engine_hum(3, 70), 0.0, 0.35)
    mx.add(A.whoosh(1.2), 0.6, 0.45)
    mx.add(C2.impact(), 0.0, 0.5)
    mx.add(A.whoosh(1.0), S['hook_low'] + 0.2, 0.4)
    mx.add(A.birds(8), S['intro'], 0.3, length=S['truck'] - S['intro'])
    mx.add(A.engine_hum(4, 50), S['truck'], 0.4, length=S['dream'] - S['truck'])
    mx.add(A.birds(4), S['dream'], 0.25, length=S['office'] - S['dream'])
    mx.add(A.engine_hum(3, 90), S['dream'], 0.12, length=S['office'] - S['dream'])
    mx.add(A.tick(), S['office'] + 0.3, 0.3)
    mx.add(C2.record_scratch(), WT(3, 'refusé') - 0.1, 0.25)
    mx.add(A.birds(6), S['boxes'], 0.25, length=S['rope'] - S['boxes'])
    mx.add(A.clank(0.3), S['boxes'] + 0.2, 0.3)
    mx.add(C2.water_rush(2.5), S['inflate'], 0.25, length=S['tied'] - S['inflate'])
    for name, _, _ in ITEMS:
        mx.add(C2.pop(), WT(6, name), 0.4)
    mx.add(C2.riser(1.2), T(7) - 0.4, 0.3)
    mx.add(C2.ding(), T(7) + 0.1, 0.4)
    mx.add(A.wind(4), S['plan_up'], 0.15, length=S['rope'] - S['plan_up'])
    mx.add(C2.pop(), S['plan_pop'] + 0.1, 0.3)
    mx.add(A.thwack(0.3), WT(9, 'casse') + 0.1, 0.8)
    mx.add(C2.impact(), WT(9, 'casse') + 0.1, 0.4)
    mx.add(A.whoosh(1.4), S['rocket'], 0.6)
    mx.add(A.wind(10), S['climb'], 0.35, length=S['planes'] - S['climb'])
    mx.add(A.engine_hum(3, 65), S['planes'], 0.45)
    mx.add(A.whoosh(1.2), S['planes'] + 0.5, 0.5)
    mx.add(A.engine_hum(4, 80), S['cockpit'], 0.25, length=S['tower'] - S['cockpit'])
    mx.add(A.tick(), S['cockpit'] + 0.6, 0.3)
    mx.add(A.wind(6), S['tower'], 0.2, length=S['gun_up'] - S['tower'])
    mx.add(C2.pop(), T(13) + 0.05, 0.5)
    mx.add(C2.ding(), T(13) + max(1.8, T(14) - T(13)) * 0.62, 0.4)
    mx.add(A.wind(8), S['gun_up'], 0.3, length=S['wires'] - S['gun_up'])
    for w in tl.timing[15]['words'][:2]:
        mx.add(A.thwack(0.3), w[1], 0.7)
        mx.add(C2.pop(), w[1] + 0.05, 0.6)
    mx.add(A.whoosh(0.8), S['drop_gun'] + 0.35, 0.4)
    mx.add(A.zap(0.6), S['wires'] + 1.0, 0.6)
    mx.add(A.arc_buzz(1.5), S['wires'] + 1.1, 0.4) if hasattr(A, 'arc_buzz') else None
    mx.add(C2.impact(), S['wires'] + 1.0, 0.4)
    mx.add(A.zap(0.4), S['blackout'] + 0.5, 0.4)
    mx.add(A.crowd(6), S['safe'], 0.25, length=S['question'] - S['safe'])
    for k in range(6):
        mx.add(A.tick(), S['press'] + 0.27 * k + 0.1, 0.3)
    mx.add(A.wind(8), S['question'], 0.2, length=END - S['question'])
    mx.add(A.engine_hum(3, 70), END - 1.6, 0.3)
    C2.cut_sounds(mx, list(cut.st.values()), 0.08)
    mx.save(path)


if __name__ == '__main__':
    run(tl, subs, HERE, 'Good2No_ep22_Larry_Walters', build_audio, sys.argv)
