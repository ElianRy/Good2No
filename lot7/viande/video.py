"""Ép. 23 — La pluie de viande du Kentucky (3 mars 1876, comté de Bath)."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n/lot7']
from props7 import *
from video_core import *

HERE = '/home/claude/g2n/lot7/viande'
timing = load_timing(os.path.join(HERE, 'timing.json'))
tl = Timeline(timing)
T, WT = tl.T, tl.word_t
END = timing[-1]['t1'] + 0.3
tl.duration = lambda: END
cut = Cut(tl)

# ------------------------------------------------------------------ personnages (1876)
make_face('crouch', skin=(232, 196, 168))
make_face('farmer1', skin=(220, 175, 140), beard=True, hair_col=(90, 65, 40))
make_face('farmer2', skin=(225, 182, 150), mustache=True, hair_col=(60, 45, 30))
make_face('nb1', skin=(215, 170, 135))
make_face('nb2', skin=(160, 115, 85))
make_face('doctor', skin=(228, 190, 160), mustache=True, hair_col=(120, 110, 100))
make_face('sci', skin=(230, 192, 160), beard=True, hair_col=(70, 60, 50))
make_face('boy', skin=(232, 190, 155))
make_face('visitor', skin=(200, 150, 115))
CROUCH = Human('crouch', skin=(232, 196, 168), shirt=(120, 70, 80), pants=(90, 60, 65), hair=(90, 60, 40), hat='bonnet', hat_col=(225, 215, 190),
               robe=(105, 65, 75), extra=C2.woman_extra('bun', apron=True, hair=(90, 60, 40)))
FARMER1 = Human('farmer1', skin=(220, 175, 140), shirt=(210, 200, 175), pants=(90, 75, 55), hair=(90, 65, 40), hat='ranger', hat_col=(150, 120, 75),
                belt=(60, 45, 30))
FARMER2 = Human('farmer2', skin=(225, 182, 150), shirt=(150, 60, 50), pants=(70, 70, 80), hair=(60, 45, 30), hat='bowler', hat_col=(50, 45, 40))
NB = [Human('nb1', skin=(215, 170, 135), shirt=(110, 120, 90), pants=(80, 65, 50), hair=(70, 50, 30), hat='flatcap', hat_col=(90, 80, 70)),
      Human('nb2', skin=(160, 115, 85), shirt=(200, 190, 160), pants=(60, 60, 65), hair=(30, 25, 20), hat='bowler', hat_col=(70, 55, 40)),
      Human('crouch', skin=(232, 196, 168), shirt=(70, 90, 120), pants=(60, 70, 90), hair=(120, 80, 40), robe=(60, 75, 100), hat='bonnet', hat_col=(200, 200, 210),
            extra=C2.woman_extra('bun', hair=(120, 80, 40)))]
DOCTOR = Human('doctor', skin=(228, 190, 160), shirt=(235, 232, 220), pants=(40, 38, 40), hair=(120, 110, 100), jacket=(40, 38, 45), tie=(30, 30, 30))
SCI = Human('sci', skin=(230, 192, 160), shirt=(235, 232, 220), pants=(50, 45, 45), hair=(70, 60, 50), jacket=(90, 70, 55), tie=(30, 30, 30))
BOY = Human('boy', skin=(232, 190, 155), shirt=(200, 195, 175), pants=(100, 80, 60), hair=(120, 80, 45), hat='flatcap', hat_col=(80, 70, 60), height=0.75, build=0.85)
VISITOR = Human('visitor', skin=(200, 150, 115), shirt=(60, 130, 170), pants=(50, 60, 90), hair=(30, 25, 20))

# ------------------------------------------------------------------ décors
ENV_DAY = Env(sky_top=(60, 125, 215), sky_hor=(195, 215, 235), fog=(200, 215, 230), fog_near=50, fog_far=380, amb=0.52, light=(-0.5, 0.85, 0.35))
ENV_ROOM = Env(sky_top=(50, 42, 35), sky_hor=(50, 42, 35), fog=(40, 34, 28), fog_near=8, fog_far=30, amb=0.6, light=(0.4, 0.8, 0.5),
               points=[((1.5, 2.2, 1.0), (255, 210, 150), 0.6, 6)])
ENV_MUSEUM = Env(sky_top=(30, 32, 38), sky_hor=(30, 32, 38), fog=(25, 26, 30), fog_near=8, fog_far=30, amb=0.5, light=(0.2, 0.9, 0.3),
                 points=[((0, 3.0, 0.5), (255, 245, 225), 1.2, 5)])
tex_noise('dirt_yard', (120, 95, 65), (150, 122, 88), seed=601, octaves=3, speck=0.1, speck_col=(95, 75, 50))
tex_noise('grass_march', (110, 120, 70), (140, 145, 90), seed=602, octaves=3, speck=0.1, speck_col=(160, 150, 100))


def bare_tree(h=7, seed=0):
    rr = np.random.default_rng(seed)
    ms = [cyl(0.22, 0.12, h * 0.6, 6, (100, 80, 60), 'bark', ts=1.0)]
    for k in range(6):
        a = rr.uniform(0, 6.28)
        b0 = np.array([0, h * rr.uniform(0.35, 0.6), 0])
        b1 = b0 + np.array([math.cos(a) * h * 0.3, h * rr.uniform(0.2, 0.4), math.sin(a) * h * 0.3])
        ms.append(rod(b0, b1, 0.07, (95, 75, 55), 'bark', 5))
        for j in range(2):
            a2 = a + rr.uniform(-0.8, 0.8)
            ms.append(rod(b1, b1 + np.array([math.cos(a2) * 1.0, rr.uniform(0.5, 1.2), math.sin(a2) * 1.0]), 0.035, (95, 75, 55), n=4))
    return merge(ms)


def log_cabin():
    ms = [box(8, 3.0, 6, (255, 255, 255), 'logwall', ts=2.0)]
    ms.append(Mesh([[(-4.3, 3.0, 3.3), (4.3, 3.0, 3.3), (4.3, 4.8, 0)], [(-4.3, 3.0, 3.3), (4.3, 4.8, 0), (-4.3, 4.8, 0)],
                    [(4.3, 3.0, -3.3), (-4.3, 3.0, -3.3), (-4.3, 4.8, 0)], [(4.3, 3.0, -3.3), (-4.3, 4.8, 0), (4.3, 4.8, 0)]], C((255, 255, 255)),
                   [[(0, 0), (3, 0), (3, 1)], [(0, 0), (3, 1), (0, 1)], [(0, 0), (3, 0), (3, 1)], [(0, 0), (3, 1), (0, 1)]], TEXB['shingle']))
    for s in (-1, 1):
        ms.append(Mesh([[(s * 4.0, 3.0, -3.0), (s * 4.0, 3.0, 3.0), (s * 4.0, 4.7, 0)]], C((140, 105, 70)), None, TEXB['logwall']))
    ms.append(box(1.1, 2.1, 0.08, (255, 255, 255), 'door').xf(trans(0.8, 0, 3.02)))
    ms.append(box(1.0, 0.9, 0.08, (255, 255, 255), 'window').xf(trans(-2.2, 1.2, 3.02)))
    ms.append(box(1.2, 5.6, 1.0, (150, 140, 130), 'stone_block', ts=1.0).xf(trans(-4.4, 0, 0)))   # cheminée en pierre
    ms.append(box(8.6, 0.12, 2.0, (255, 255, 255), 'planks').xf(trans(0, 0.3, 4.0)))           # galerie
    for x in (-4, 0, 4):
        ms.append(box(0.15, 2.6, 0.15, (110, 80, 55)).xf(trans(x, 0.3, 4.9)))
    ms.append(box(8.8, 0.1, 2.3, (255, 255, 255), 'shingle').xf(M(trans(0, 2.95, 4.1), rotx(0.15))))
    return merge(ms)


def barn():
    ms = [box(9, 4.5, 7, (150, 60, 45), 'planks_v', ts=2.5)]
    ms.append(Mesh([[(-4.8, 4.5, 3.8), (4.8, 4.5, 3.8), (0, 7.0, 3.8)], [(-4.8, 4.5, -3.8), (4.8, 4.5, -3.8), (0, 7.0, -3.8)]], C((150, 60, 45))))
    for s in (-1, 1):
        ms.append(quad((s * 4.9, 4.4, 3.9), (s * 4.9, 4.4, -3.9), (0, 7.1, -3.9), (0, 7.1, 3.9), (110, 100, 90), 'roof_tin'))
    ms.append(box(3, 3.2, 0.1, (120, 50, 38), 'planks_v').xf(trans(0, 0, 3.52)))
    return merge(ms)


def rail_fence(x0, z0, x1, z1, h=1.2):
    """clôture en zigzag (rails de bois) typique du Kentucky"""
    ms = []
    p0, p1 = np.array([x0, 0, z0]), np.array([x1, 0, z1])
    L = np.linalg.norm(p1 - p0)
    d = (p1 - p0) / L
    side = np.array([-d[2], 0, d[0]])
    n = int(L / 3)
    pts = [p0 + d * (i * L / n) + side * (0.4 if i % 2 else -0.4) for i in range(n + 1)]
    for a, b in zip(pts[:-1], pts[1:]):
        for y in (0.25, 0.6, 0.95):
            ms.append(rod(a + np.array([0, y, 0]), b + np.array([0, y + 0.12, 0]), 0.06, (130, 100, 70), 'bark', 4))
    return merge(ms)


def kettle(fire=True):
    ms = [cyl(0.42, 0.5, 0.55, 10, (35, 33, 32)).xf(trans(0, 0.35, 0)), cyl(0.5, 0.5, 0.04, 10, (50, 45, 40)).xf(trans(0, 0.9, 0)),
          cyl(0.45, 0.45, 0.01, 10, (170, 150, 110)).xf(trans(0, 0.86, 0))]
    for a in (0, 2.1, 4.2):
        ms.append(rod((math.cos(a) * 0.45, 0, math.sin(a) * 0.45), (math.cos(a) * 0.35, 0.45, math.sin(a) * 0.35), 0.03, (35, 33, 32), n=4))
    for k in range(6):
        a = k / 6 * 6.28
        ms.append(rod((math.cos(a) * 0.5, 0.05, math.sin(a) * 0.5), (math.cos(a + 1.5) * 0.25, 0.08, math.sin(a + 1.5) * 0.25), 0.05, (90, 65, 45), 'bark', 4))
    for k in range(8):
        a = k / 8 * 6.28
        ms.append(rock(0.12, k, (150, 140, 130)).xf(trans(math.cos(a) * 0.65, 0, math.sin(a) * 0.65)))
    return merge(ms)


def chicken(phase=0.0, col=(240, 236, 225)):
    pk = max(0, math.sin(phase)) * 0.5
    return merge([sphere(0.13, 6, 4, col, sy=0.85).xf(trans(0, 0.25, 0)), sphere(0.07, 5, 3, col).xf(M(trans(0, 0.36 - pk * 0.15, 0.12 + pk * 0.05))),
                  box(0.03, 0.04, 0.04, (220, 160, 40)).xf(trans(0, 0.36 - pk * 0.15, 0.2 + pk * 0.05)), box(0.04, 0.05, 0.03, (200, 40, 40)).xf(trans(0, 0.43 - pk * 0.15, 0.12)),
                  rod((0.04, 0.0, 0), (0.04, 0.14, 0), 0.01, (220, 160, 40), n=3), rod((-0.04, 0.0, 0), (-0.04, 0.14, 0), 0.01, (220, 160, 40), n=3)])


def farm():
    rr = np.random.default_rng(4)
    ms = [ground(-200, -200, 200, 200, 'grass_march', ts=4.0), grid(-12, -6, 12, 14, 4, 4, None, (255, 255, 255), 'dirt_yard', 3.0).xf(trans(0, 0.02, 0)),
          log_cabin().xf(trans(0, 0, -6)), barn().xf(M(trans(18, 0, -12), roty(-0.5))), rail_fence(-15, 14, 30, 14), rail_fence(30, 14, 30, -30),
          rail_fence(-15, -15, -15, 14)]
    for i in range(14):
        x, z = rr.uniform(-80, 80), rr.uniform(-90, -25)
        ms.append(bare_tree(rr.uniform(6, 10), i).xf(trans(x, 0, z)))
    for i in range(10):
        ms.append(pine(rr.uniform(8, 13), 2.5, i).xf(trans(rr.uniform(-120, 120), 0, rr.uniform(-150, -60))))
    for i in range(6):
        ms.append(cyl(rr.uniform(40, 90), 0, rr.uniform(20, 40), 9, (90, 110, 80)).xf(trans(rr.uniform(-300, 300), 0, rr.uniform(-400, -250))))
    ms.append(box(1.2, 0.8, 0.8, (255, 255, 255), 'planks').xf(trans(-6, 0, 2)))      # tonneau / caisse
    ms.append(cyl(0.35, 0.35, 0.9, 8, (140, 100, 60), 'planks_v').xf(trans(-5.0, 0, 3.0)))
    ms.append(box(2.4, 0.5, 0.5, (255, 255, 255), 'planks').xf(trans(4.5, 0, 3.5)))      # banc
    # corde à linge entre deux poteaux, loin de la marmite ; les draps sont pincés sur la corde
    L0, L1 = np.array([-11.0, 0, 4.5]), np.array([-6.0, 0, 7.5])
    for p in (L0, L1):
        ms.append(box(0.1, 1.9, 0.1, (110, 85, 60)).xf(trans(p)))
    ms.append(rod(L0 + np.array([0, 1.85, 0]), L1 + np.array([0, 1.85, 0]), 0.03, (200, 195, 185), n=3))
    d = (L1 - L0) / np.linalg.norm(L1 - L0)
    yaw_l = math.atan2(d[0], d[2]) - math.pi / 2
    for k, u in enumerate((0.15, 0.38, 0.62, 0.85)):
        p = L0 + (L1 - L0) * u
        ms.append(box(0.95, 0.9, 0.02, [(235, 230, 215), (210, 220, 235), (235, 230, 215), (230, 215, 200)][k]).xf(M(trans(p[0], 0.95, p[2]), roty(yaw_l))))
        for e in (-0.4, 0.4):
            q = p + d * e
            ms.append(box(0.04, 0.1, 0.04, (150, 120, 80)).xf(trans(q[0], 1.8, q[2])))
    ms.append(kettle().xf(trans(KET)))
    return merge(ms)


KET = np.array([1.5, 0.0, 6.5])
FARM = farm()
CHICKENS = [(np.array([-4 + i * 1.3, 0, 8 + (i % 2) * 1.5]), i * 1.7) for i in range(5)]


def chickens(tg, scatter=0.0):
    ms = []
    for p, ph in CHICKENS:
        q = p + np.array([math.sin(ph) * scatter, 0, math.cos(ph) * scatter])
        ms.append(chicken(tg * 5 + ph).xf(M(trans(q), roty(ph))))
    return merge(ms)


# ------------------------------------------------------------------ morceaux de viande
_CHUNKS = [rock(r, i, (255, 255, 255), 'meat').xf(scale(1, 0.55, 1)) for i, r in enumerate((0.09, 0.12, 0.08, 0.1, 0.13, 0.085))]


def meat_rain(p, center, radius=10.0, n=70, seed=0, period=3.0, h=22.0, lie=True, s=1.0):
    """pluie de morceaux : chacun tombe, s'écrase puis reste au sol, disparaît en fondu à la fin du cycle"""
    rr = np.random.default_rng(seed)
    ms = []
    c = np.asarray(center, float)
    for i in range(n):
        off = rr.uniform(0, period)
        ang, rad = rr.uniform(0, 6.28), radius * math.sqrt(rr.random())
        x, z = c[0] + math.cos(ang) * rad, c[2] + math.sin(ang) * rad
        u = (p + off) % period
        tf = math.sqrt(2 * h / 30.0)
        ch = _CHUNKS[i % len(_CHUNKS)].xf(scale(s))
        if u < tf:
            y = h - 15.0 * u * u
            ms.append(ch.xf(M(trans(x, y, z), rotx(u * 6 + i), roty(i))))
        elif lie:
            a = 1.0 - max(0.0, (u - (period - 0.4)) / 0.4)
            m = ch.xf(M(trans(x, 0.02, z), roty(i)))
            if a < 1:
                m = m.set(alpha=a)
            ms.append(m)
    return merge(ms)


def meat_ground(center, radius=10.0, n=60, seed=5, s=1.0):
    rr = np.random.default_rng(seed)
    c = np.asarray(center, float)
    ms = []
    for i in range(n):
        ang, rad = rr.uniform(0, 6.28), radius * math.sqrt(rr.random())
        ms.append(_CHUNKS[i % 6].xf(M(trans(c[0] + math.cos(ang) * rad, 0.02, c[2] + math.sin(ang) * rad), roty(i), scale(s))))
    return merge(ms)


GROUND_MEAT = meat_ground(KET + np.array([0, 0, -2]), 11, 90)


def crouch_soap(tg, look_up=0.0, step=0.0):
    pos = KET + np.array([-0.95 - step, 0, 0.35])
    stir = (1.2 + 0.25 * math.sin(tg * 3), 0.1, 0.6)
    pose = dict(ra=stir if look_up < 0.5 else (2.2, 0.4, 1.4), la=(0.9, 0.1, 0.8) if look_up < 0.5 else (2.2, 0.4, 1.4), hp=-0.9 * look_up + 0.3 * (1 - look_up), lean=0.2 * (1 - look_up))
    m = [CROUCH.mesh(tuple(pos), math.pi / 2 - 0.2, pose)]
    if look_up < 0.5:
        m.append(rod(pos + np.array([0.55, 1.15, 0.0]), KET + np.array([0.1, 0.6, 0.0]), 0.025, (120, 90, 60), n=4))   # spatule dans la marmite
    return merge(m)


def soap_fire(tg, cam):
    return merge([C2.fire_sprites(KET + np.array([0, 0.05, 0]), tg, cam, 6, 0.35, 0.2, 1), C2.smoke_sprites(KET + np.array([0, 0.95, 0]), tg, cam, 4, 0.5, 2.0, 2, (210, 210, 210), alpha=0.5)])


def shot_hook(lt, dur, tg, p=None):
    """0 : au ras du sol, des morceaux de viande crue s'écrasent dans la cour"""
    p = lt if p is None else p
    cam = Cam((KET[0] + 2.2 - 0.15 * p, 0.55, KET[2] + 2.8 - 0.2 * p), (KET[0] - 0.5, 1.0, KET[2] - 0.5), 58)
    ms = [FARM, GROUND_MEAT, meat_rain(p, KET + np.array([0.8, 0, 1.2]), 2.6, 90, 1, 1.6, 9), crouch_soap(tg, look_up=1.0), soap_fire(tg, cam), chickens(tg, 2.0)]
    return merge(ms), cam, ENV_DAY, {}


def shot_date(lt, dur, tg):
    """grand plan de la ferme du Kentucky sous un ciel bleu, la viande tombe"""
    u = lt / max(dur, 0.1)
    cam = Cam((-16 + 4 * u, 6, 28), (2, 3, 0), 55)
    ms = [FARM, GROUND_MEAT, meat_rain(lt + 5, KET + np.array([0, 0, -1]), 12, 90, 2, 3.0, 25), crouch_soap(tg, 1.0)]
    return merge(ms), cam, ENV_DAY, {}


def shot_soap(lt, dur, tg):
    """madame Crouch fabrique son savon devant la ferme (calme)"""
    cam = cam_lerp(Cam((KET[0] + 2.5, 1.6, KET[2] + 4.5), (KET[0] - 0.6, 1.0, KET[2]), 50), Cam((KET[0] + 2.0, 1.5, KET[2] + 3.6), (KET[0] - 0.6, 1.0, KET[2]), 48), lt / dur)
    ms = [FARM, crouch_soap(tg), soap_fire(tg, cam), chickens(tg)]
    return merge(ms), cam, ENV_DAY, {}


def shot_splat(lt, dur, tg):
    """soudain : les morceaux s'écrasent autour d'elle, elle recule"""
    k = min(1.0, lt / 0.6)
    cam = Cam((KET[0] - 4.5, 1.3, KET[2] + 2.8), (KET[0] - 0.8, 1.0, KET[2]), 52)
    ms = [FARM, crouch_soap(tg, look_up=k, step=0.6 * k), meat_rain(lt, KET + np.array([-1.0, 0, 0.5]), 3.0, 30, 3, 2.0, 15), soap_fire(tg, cam), chickens(tg, 2 * k)]
    return merge(ms), C2.shake(cam, 0.03, tg), ENV_DAY, {}


def shot_wide(lt, dur, tg):
    """plusieurs minutes, sur près de 100 m : vue d'en haut"""
    u = lt / max(dur, 0.1)
    cam = Cam((-30 + 6 * u, 42, 40), (2, 0, 2), 50)
    ms = [FARM, meat_ground(KET + np.array([3, 0, -4]), 22, 220, 9, s=3.0), meat_rain(lt + 3, KET + np.array([2, 0, -2]), 22, 160, 4, 3.0, 30, lie=False, s=3.0),
          crouch_soap(tg, 1.0, 0.6)]
    return merge(ms), cam, ENV_DAY, {}


def shot_sky(lt, dur, tg):
    """contre-plongée : ciel parfaitement bleu, pas un nuage, et ça tombe quand même"""
    cam = Cam((KET[0], 1.2, KET[2] + 2), (KET[0] + 0.5, 30, KET[2] - 4), 60, roll=0.15 * math.sin(lt * 0.6))
    ms = [FARM, meat_rain(lt, KET + np.array([0.3, 0, 0.8]), 3.5, 70, 6, 1.6, 14, lie=False, s=1.5), sun_disc((80, 200, -150), 8)]
    return merge(ms), cam, ENV_DAY, {}


def shot_neighbors(lt, dur, tg):
    """les voisins accourent à travers le champ ; l'émeu à chapeau traîne près de la grange"""
    ms = [FARM, GROUND_MEAT, meat_ground(KET + np.array([4, 0, 6]), 8, 40, 11), chickens(tg, 2.0), crouch_soap(tg, 1.0, 0.6)]
    runners = [(FARMER1, np.array([15, 0, -1]), 0.0), (FARMER2, np.array([17, 0, 1.5]), 1.5), (NB[0], np.array([19.5, 0, -2]), 3.0), (NB[1], np.array([21, 0, 0.5]), 0.7)]
    for who, p0, ph in runners:
        d = (KET + np.array([2, 0, 3]) - p0)
        d[1] = 0
        L = np.linalg.norm(d)
        p = p0 + d / L * min(L - 1.5, lt * 3.5)
        yaw = math.atan2(d[0], d[2])
        ms.append(who.mesh(tuple(p), yaw, run_pose(tg * 8 + ph)))
    ms.append(emu_mesh((15.5, 0, -6.5), -1.9, peck=0.5 + 0.5 * math.sin(tg * 2), look=0.3 * math.sin(tg)))
    cam = Cam((KET[0] - 3, 1.7, KET[2] + 6.5), (12, 1.3, 2), 50)
    return merge(ms), cam, ENV_DAY, {}


TASTE = KET + np.array([3.5, 0, 3.0])


TASTE_CHUNK = None
HY_T = 0.4


def tasters(tg, chew=0.0, sick=0.0, pick=1.0):
    """pick : 0 = la main ramasse le morceau au sol, 1 = le morceau est à la bouche"""
    global TASTE_CHUNK
    a = TASTE
    b = TASTE + np.array([0.9, 0, 0.3])
    ms = [GROUND_MEAT]
    chunk = _CHUNKS[1].xf(scale(0.75))
    if sick > 0:
        ms.append(FARMER1.mesh(tuple(a), 0.6, dict(lean=0.7 * sick, hp=0.4, la=(0.8, 0.2, 1.6), ra=(0.6, -0.1, 1.9))))
        ms.append(FARMER2.mesh(tuple(b), -0.9, dict(lean=0.3, la=(1.4, 0.3, 2.3), ra=(1.4, 0.3, 2.3), hp=-0.2)))
    else:
        base = dict(ll=(1.6, 2.2), rl=(1.2, 2.0), drop=0.55, lean=0.3, hp=0.1 + 0.4 * (1 - pick), la=(0.6, 0.1, 0.5), hy=HY_T * pick)
        FARMER1.mesh(tuple(a), 0.6, base)
        hm = FARMER1.attach['head']
        mouth = (hm @ np.array([0.0, 0.07, 0.2, 1.0]))[:3]
        fw = np.array([math.sin(0.6), 0, math.cos(0.6)])
        rt = np.array([math.cos(0.6), 0, -math.sin(0.6)])
        ground_pt = a + fw * 0.45 + rt * 0.12 + np.array([0, 0.05, 0])
        s = pick * pick * (3 - 2 * pick)
        mouth = mouth + fw * 0.1 + rt * 0.05 - np.array([0, 0.05, 0])
        tgt = ground_pt + (mouth - ground_pt) * s
        if chew > 0 and pick >= 1:
            tgt = tgt + np.array([0, 0.015 * math.sin(tg * 12), 0])
        pose = dict(base, ik_r=tgt)
        held = pick > 0.02
        if held:
            # la main n'atteint pas tout à fait la bouche : le morceau est tenu du bout des doigts, contre les lèvres
            FARMER1.mesh(tuple(a), 0.6, pose)
            hmx = FARMER1.attach['hand_r']
            loc = (np.linalg.inv(hmx) @ np.append(tgt, 1.0))[:3]
            if np.linalg.norm(loc) > 0.16:
                loc = loc / np.linalg.norm(loc) * 0.16
            pose['hand_r'] = chunk.xf(trans(loc * s))
        ms.append(FARMER1.mesh(tuple(a), 0.6, pose))
        if not held:
            ms.append(chunk.xf(trans(ground_pt - np.array([0, 0.05, 0]))))
        ms.append(FARMER2.mesh(tuple(b), -0.9, dict(ll=(1.6, 2.2), rl=(1.2, 2.0), drop=0.55, lean=0.45, la=(0.9, 0.1, 0.4), hp=0.5)))
    return merge(ms)


def shot_taste(lt, dur, tg):
    """deux hommes s'accroupissent… et goûtent"""
    t_g = WT(7, 'goûtent') - cut['taste']
    chew = 1.0 if lt > t_g else 0.0
    pick = min(1.0, max(0.0, (lt - (t_g - 0.8)) / 0.8))
    cam = cam_lerp(Cam(tuple(TASTE + np.array([0.9, 1.15, 2.4])), tuple(TASTE + np.array([0.15, 0.75, 0.25])), 50),
                   Cam(tuple(TASTE + np.array([0.8, 1.1, 2.0])), tuple(TASTE + np.array([0.15, 0.8, 0.25])), 46), lt / dur)
    ms = [FARM, tasters(tg, chew, 0.0, pick), NB[0].mesh(tuple(TASTE + np.array([-1.5, 0, -1.0])), 0.8, dict(hp=0.3, la=(0.2, 0.1, 0.4))),
          NB[2].mesh(tuple(TASTE + np.array([-0.8, 0, -1.8])), 0.4, dict(hp=0.3, ra=(0.9, 0.1, 1.9)))]
    return merge(ms), cam, ENV_DAY, {}


# animaux : mouton et chevreuil
def quadruped(kind, phase=0.0, amp=0.0, graze=0.0):
    if kind == 'sheep':
        bc, bt, hc, L, bw, bh = (255, 255, 255), 'wool', (40, 35, 32), 0.42, 0.55, 0.5
    else:
        bc, bt, hc, L, bw, bh = (255, 255, 255), 'fur_deer', (150, 105, 70), 0.72, 0.38, 0.42
    ms = [box(bw, bh, 1.0 if kind == 'sheep' else 1.1, bc, bt).xf(trans(0, L, 0))]
    nk = M(trans(0, L + bh * 0.7, 0.5), rotx(-0.5 + graze * 1.6))
    ms.append(box(0.16, 0.45 if kind == 'deer' else 0.25, 0.16, hc if kind == 'sheep' else bc, 0 if kind == 'sheep' else bt).xf(nk))
    hd = M(nk, trans(0, 0.42 if kind == 'deer' else 0.22, 0.05), rotx(0.9 - graze * 0.6))
    ms.append(box(0.17, 0.32 if kind == 'deer' else 0.28, 0.2, hc).xf(hd))
    for s in (-1, 1):
        ms.append(box(0.18, 0.06, 0.04, hc).xf(M(hd, trans(s * 0.13, 0.22, -0.02), rotz(s * 0.4))))
        ms.append(box(0.025, 0.04, 0.02, (15, 15, 15)).xf(M(hd, trans(s * 0.09, 0.2, 0.06))))
    for (x, z, ph) in ((-0.15, 0.4, 0), (0.15, 0.4, math.pi), (-0.15, -0.4, math.pi), (0.15, -0.4, 0)):
        lg = M(trans(x * bw / 0.4, L, z), rotx(0.5 * math.sin(phase + ph) * amp))
        ms.append(box(0.08, L, 0.08, hc if kind == 'sheep' else (130, 95, 65)).xf(M(lg, trans(0, -L, 0))))
    if kind == 'deer':
        ms.append(box(0.1, 0.16, 0.05, (240, 235, 225)).xf(M(trans(0, L + bh * 0.8, -0.56), rotx(-0.4))))
    return merge(ms)


PASTURE = merge([ground(-100, -100, 100, 100, 'grass_march', ts=4.0), rail_fence(-20, 6, 20, 6)] + [bare_tree(8, i).xf(trans(-30 + i * 9, 0, -18 - (i % 3) * 6)) for i in range(7)]
                + [pine(10, 2.6, i).xf(trans(-40 + i * 10, 0, -35)) for i in range(9)])


def shot_sheep(lt, dur, tg):
    ms = [PASTURE] + [quadruped('sheep', graze=0.6 + 0.4 * math.sin(tg * 2 + i)).xf(M(trans(-2 + i * 1.6, 0, -1 - (i % 2) * 1.5), roty(0.5 + i))) for i in range(4)]
    cam = cam_lerp(Cam((1.0, 1.0, 4.0), (0, 0.6, -1), 50), Cam((0.8, 0.95, 3.4), (0, 0.6, -1), 48), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_deer(lt, dur, tg):
    ms = [PASTURE, quadruped('deer', graze=max(0, 0.8 - lt)).xf(M(trans(0, 0, -6), roty(0.8)))]
    cam = cam_lerp(Cam((2.0, 1.2, 0.0), (0, 1.1, -6), 45), Cam((1.6, 1.2, -1.0), (0, 1.1, -6), 42), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_detail(lt, dur, tg):
    """retiens ce détail : gros plan lent sur le goûteur qui mâche"""
    cam = cam_lerp(Cam(tuple(TASTE + np.array([0.9, 1.0, 1.6])), tuple(TASTE + np.array([0.15, 0.85, 0.1])), 45),
                   Cam(tuple(TASTE + np.array([0.6, 0.95, 1.1])), tuple(TASTE + np.array([0.15, 0.85, 0.1])), 40), lt / dur)
    ms = [FARM, tasters(tg, 1.0)]
    return merge(ms), cam, ENV_DAY, dict(post_pil=lambda im: C2.vignette(im, 0.75))


# ------------------------------------------------------------------ les journaux, les savants
def town():
    ms = [ground(-80, -80, 80, 80, 'dirt_yard', ts=4.0)]
    for i, x in enumerate(np.arange(-30, 31, 8)):
        h = 5 + (i % 3)
        ms.append(box(7.5, h, 6, (255, 255, 255), ['planks_white', 'brick', 'planks_grey'][i % 3], ts=2.5).xf(trans(x, 0, -8)))
        ms.append(box(7.6, 0.8, 0.2, [(120, 50, 40), (60, 80, 60), (70, 60, 90)][i % 3]).xf(trans(x, h - 0.9, -4.9)))
        ms.append(box(1.2, 2.2, 0.06, (255, 255, 255), 'door').xf(trans(x, 0, -4.97)))
        ms.append(box(2.2, 1.4, 0.06, (255, 255, 255), 'window').xf(trans(x + 2.2, 1.0, -4.97)))
        ms.append(box(7.5, 0.12, 2.0, (255, 255, 255), 'planks').xf(trans(x, 0.2, -4.0)))
    for x in (-22, 6, 25):
        ms.append(cyl(0.12, 0.1, 3.5, 6, (40, 40, 40)).xf(trans(x, 0, -2.6)))
        ms.append(box(0.4, 0.5, 0.4, (255, 230, 170), emis=0.5).xf(trans(x, 3.5, -2.6)))
    ms.append(C2.horse(0.0).xf(M(trans(-12, 0, 0.0), roty(1.3))))
    return merge(ms)


TOWN = town()


def _headline(d, n):
    d.rectangle([0, 0, n, n], fill=(232, 226, 205))
    d.rectangle([1, 1, n - 2, 5], fill=(30, 30, 30))
    d.rectangle([2, 8, n - 3, 13], fill=(40, 40, 40))   # gros titre
    for y in range(16, n - 1, 2):
        d.line([2, y, 14, y], fill=(110, 105, 95))
        d.line([17, y, n - 3, y], fill=(110, 105, 95))
    d.rectangle([17, 16, n - 3, 24], fill=(150, 60, 55))   # gravure


tex_draw('paper_meat', _headline)


def shot_paper(lt, dur, tg):
    """dans la rue, un petit vendeur de journaux crie la nouvelle"""
    p = np.array([0, 0, -2.2])
    paper = box(0.42, 0.55, 0.01, (255, 255, 255), 'paper_meat')
    shout = 2.5 + 0.3 * math.sin(tg * 6)
    ms = [TOWN, BOY.mesh(tuple(p), 0.2, dict(ra=(shout, 0.2, 0.3), la=(1.3, 0.1, 1.2), hand_r=paper.xf(M(trans(0, 0.02, 0.05), rotx(-math.pi / 2), rotz(0.1)))))]
    for i, (dx, dz) in enumerate(((2.2, 1.5), (-2.0, 1.8), (3.5, -0.2))):
        q = p + np.array([dx, 0, dz])
        ms.append(NB[i % 3].mesh(tuple(q), math.atan2(p[0] - q[0], p[2] - q[2]), dict(hp=0.1)))
    cam = cam_lerp(Cam((0.8, 1.2, 1.8), (0, 1.5, -2.2), 55), Cam((0.6, 1.1, 1.3), (0, 1.5, -2.2), 52), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def jar(content=None, label=(235, 228, 205)):
    ms = [cyl(0.12, 0.12, 0.3, 10, (200, 225, 230), alpha=0.45), cyl(0.125, 0.125, 0.04, 10, (120, 100, 80)).xf(trans(0, 0.3, 0)),
          box(0.12, 0.08, 0.01, label).xf(trans(0, 0.12, 0.125)), cyl(0.11, 0.11, 0.2, 10, (230, 220, 170), alpha=0.35)]
    if content is not None:
        ms.append(content.xf(trans(0, 0.08, 0)))
    return merge(ms)


def lab():
    ms = [box(9, 0.05, 8, (255, 255, 255), 'planks').xf(trans(0, 0, 0)), box(9, 3.4, 0.15, (255, 255, 255), 'plaster_old', ts=2.5).xf(trans(0, 0, -3)),
          box(0.15, 3.4, 8, (255, 255, 255), 'plaster_old', ts=2.5).xf(trans(-3.5, 0, 0)), bench_table(2.4, 1.0, 0.85, (255, 255, 255), 'wood_dark').xf(trans(0, 0, -1.6)),
          shelf(2.0, 2.2, 0.35, 4).xf(trans(1.8, 0, -2.75)), box(1.0, 1.4, 0.06, (255, 255, 255), 'window').xf(trans(-1.3, 1.3, -2.92))]
    rr = np.random.default_rng(3)
    for k in range(4):
        for j in range(5):
            ms.append(bottle(0.25, 0.05, [(110, 70, 40), (60, 90, 60), (200, 200, 190), (70, 70, 120)][(k + j) % 4]).xf(trans(1.0 + j * 0.38, k * 0.55 + 0.03, -2.75)))
    ms.append(microscope().xf(trans(-0.6, 0.85, -1.7)))
    ms.append(cyl(0.15, 0.15, 0.25, 8, (60, 60, 60)).xf(trans(0.9, 0.85, -1.9)))
    ms.append(cyl(0.012, 0.012, 0.3, 4, (200, 200, 200)).xf(trans(0.9, 1.1, -1.9)))
    return merge(ms)


LAB = lab()
JAR_MEAT = [rock(0.065, 31, (255, 255, 255), 'meat').xf(scale(1, 0.7, 1)), rock(0.06, 32, (255, 255, 255), 'meat').xf(scale(1, 0.7, 1)).tint((1.2, 1.4, 1.4)),
            rock(0.07, 33, (255, 255, 255), 'meat').xf(scale(1, 0.7, 1)).tint((1.1, 0.8, 0.8))]
JARS = [jar(m) for m in JAR_MEAT]


def shot_lab(lt, dur, tg):
    ms = [LAB, SCI.mesh((-0.6, 0, -0.9), math.pi, dict(lean=0.45, hp=0.5, ra=(1.0, 0.1, 0.9), la=(1.0, 0.1, 0.9))),
          DOCTOR.mesh((0.9, 0, -0.6), math.pi + 0.6, dict(la=(0.3, 0.1, 1.6), ra=(0.3, 0.1, 1.6), hp=0.3))]
    for i, j in enumerate(JARS):
        ms.append(j.xf(trans(0.0 + i * 0.35, 0.85, -1.4)))
    cam = cam_lerp(Cam((1.8, 1.8, 1.2), (-0.1, 1.0, -1.5), 50), Cam((1.5, 1.7, 0.8), (-0.1, 1.0, -1.5), 48), lt / dur)
    return merge(ms), cam, ENV_ROOM, {}


def shot_jars(lt, dur, tg):
    """muscle, cartilage… poumon : les bocaux, un par un"""
    ms = [LAB]
    for i, j in enumerate(JARS):
        ms.append(j.xf(trans(0.0 + i * 0.35, 0.85, -1.4)))
    i = 0
    for k, w in enumerate(('muscle,', 'cartilage…', 'poumon.')):
        if lt + cut['jars'] >= WT(12, w) - 0.05:
            i = k
    tgt = np.array([0.0 + i * 0.35, 1.0, -1.4])
    cam = Cam(tuple(tgt + np.array([0.15, 0.25, 0.9])), tuple(tgt), 42)
    return merge(ms), cam, ENV_ROOM, {}


# ------------------------------------------------------------------ les vautours
def vulture(flap=0.0, fly=False, vomit=0.0):
    """urubu à tête rouge : corps noir, tête nue rouge, bec clair. Regarde +z"""
    ms = [sphere(0.25, 7, 4, (255, 255, 255), 'feath_dark', sy=0.8).xf(M(trans(0, 0.55, 0), scale(0.9, 1.0, 1.5)))]
    hd = M(trans(0, 0.72, 0.35), rotx(0.5 * vomit))
    ms.append(rod((0, 0.6, 0.25), hd[:3, 3], 0.05, (60, 50, 50), n=4))
    ms.append(sphere(0.07, 6, 4, (200, 70, 60)).xf(M(hd, scale(1, 0.9, 1.3))))
    ms.append(box(0.04, 0.04, 0.08, (235, 225, 200)).xf(M(hd, trans(0, -0.01, 0.1))))
    if fly:
        for s in (-1, 1):
            a = s * (0.25 * math.sin(flap))
            w = M(trans(s * 0.15, 0.6, 0.05), rotz(a))
            ms.append(Mesh([[(0, 0, 0.18), (s * 1.0, 0.05, 0.05), (s * 0.95, 0.05, -0.25)], [(0, 0, 0.18), (s * 0.95, 0.05, -0.25), (0, 0, -0.2)]],
                           C((35, 32, 34)), None, TEXB['feath_dark']).xf(w))
            ms.append(Mesh([[(s * 0.95, 0.05, 0.05), (s * 1.25, 0.05, -0.05), (s * 0.95, 0.05, -0.25)]], C((150, 150, 150))).xf(w))
        ms.append(box(0.2, 0.03, 0.3, (35, 32, 34)).xf(trans(0, 0.55, -0.45)))
    else:
        for s in (-1, 1):
            ms.append(box(0.08, 0.32, 0.55, (35, 32, 34), 'feath_dark').xf(M(trans(s * 0.2, 0.42, -0.05), rotx(0.3))))
            ms.append(rod((s * 0.08, 0.35, 0), (s * 0.08, 0.0, 0.05), 0.02, (200, 190, 175), n=3))
    return merge(ms)


def dead_tree():
    ms = [cyl(0.3, 0.15, 6, 6, (110, 100, 90), 'bark', ts=1.0)]
    for (a, y, L) in ((0.3, 3.5, 2.5), (2.4, 4.2, 2.2), (4.2, 5.0, 1.8), (1.2, 5.5, 1.5)):
        ms.append(rod((0, y, 0), (math.cos(a) * L, y + 0.6, math.sin(a) * L), 0.09, (110, 100, 90), 'bark', 5))
    return merge(ms)


PERCHES = [np.array([math.cos(a) * L * 0.75, y + 0.45, math.sin(a) * L * 0.75]) for (a, y, L) in ((0.3, 3.5, 2.5), (2.4, 4.2, 2.2), (4.2, 5.0, 1.8), (1.2, 5.5, 1.5))]
DEADTREE = dead_tree()
TREE_POS = np.array([-11, 0, 0])


def vomit_stream(base, t, period=1.0, n=8, seed=0, col=(170, 120, 90)):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        u = (t + i / n * period) % period
        p = np.asarray(base) + np.array([rr.uniform(-0.05, 0.05), -12.0 * u * u, 0.25 + u * 0.4])
        ms.append(_CHUNKS[i % 6].tint(np.asarray(C(col)) * 1.4).xf(M(trans(p), rotx(u * 8))))
    return merge(ms)


def shot_why(lt, dur, tg):
    """d'où ça vient ? le ciel au-dessus de la ferme"""
    cam = cam_lerp(Cam((KET[0] - 2, 1.5, KET[2] + 6), (KET[0], 6, KET[2] - 10), 55), Cam((KET[0] - 2, 1.4, KET[2] + 5), (KET[0], 8, KET[2] - 10), 55), lt / dur)
    ms = [FARM, GROUND_MEAT, crouch_soap(tg, 1.0, 0.6)]
    return merge(ms), cam, ENV_DAY, {}


BOARD = None


def _board(d, n):
    d.rectangle([0, 0, n, n], fill=(40, 55, 45))
    d.polygon([(4, 18), (14, 12), (16, 14), (28, 10), (20, 17), (14, 20)], outline=(230, 230, 220))
    d.ellipse([12, 10, 17, 15], outline=(230, 230, 220))
    d.line([20, 20, 22, 26], fill=(230, 230, 220))
    d.line([24, 22, 26, 28], fill=(230, 230, 220))


tex_draw('board_vulture', _board, bg=(40, 55, 45))


def shot_doctor(lt, dur, tg):
    ms = [LAB, box(1.6, 1.1, 0.05, (255, 255, 255), 'board_vulture').xf(trans(-1.4, 1.2, -2.85)), DOCTOR.mesh((-0.3, 0, -2.1), 0.4, dict(ra=(1.6, 0.4, 0.2), hy=0.6))]
    cam = cam_lerp(Cam((0.9, 1.6, 0.6), (-0.8, 1.5, -2.4), 50), Cam((0.7, 1.6, 0.2), (-0.8, 1.5, -2.4), 48), lt / dur)
    return merge(ms), cam, ENV_ROOM, {}


def flock(tg, center, n=7, r=9.0, h=18.0, vomit=False, seed=0):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        a = tg * 0.35 + i / n * 6.28 + rr.uniform(-0.2, 0.2)
        rad = r * rr.uniform(0.6, 1.1)
        p = np.asarray(center) + np.array([math.cos(a) * rad, h + rr.uniform(-2, 2), math.sin(a) * rad])
        yaw = math.atan2(-math.sin(a), math.cos(a))
        ms.append(vulture(tg * 4 + i, True).xf(M(trans(p), roty(yaw), rotz(0.25))))
        if vomit:
            ms.append(vomit_stream(p + np.array([0, 0.5, 0]), tg + i * 0.3, 1.4, 6, i))
    return merge(ms)


def shot_vultures_reveal(lt, dur, tg):
    """les vautours tournent dans le ciel"""
    cam = Cam((0, 1.6, 10), (0, 14, -2), 60)
    ms = [FARM, flock(tg, (0, 0, -2), 7, 8, 16)]
    return merge(ms), cam, ENV_DAY, {}


def shot_perch(lt, dur, tg):
    """un vautour perché, trop plein (ou effrayé) : il vomit pour s'alléger"""
    t_v = WT(16, 'vomit') - cut['perch']
    vo = min(1.0, max(0.0, (lt - t_v) / 0.2))
    p = TREE_POS + PERCHES[0]
    ms = [FARM, DEADTREE.xf(trans(TREE_POS)), vulture(vomit=vo).xf(M(trans(p), roty(0.9)))]
    if vo > 0:
        ms.append(vomit_stream(p + np.array([0.3, 0.75, 0.2]), lt, 1.2, 8, 1))
    cam = Cam(tuple(p + np.array([1.5, 0.5, 1.7])), tuple(p + np.array([0, 0.45, 0])), 45)
    return merge(ms), cam, ENV_DAY, {}


def shot_tree_chain(lt, dur, tg):
    """et les autres font pareil, un par un"""
    ms = [FARM, DEADTREE.xf(trans(TREE_POS))]
    t_e = WT(17, 'autres') - cut['tree_chain']
    for i, pp in enumerate(PERCHES):
        p = TREE_POS + pp
        tv = t_e + i * 0.45
        vo = min(1.0, max(0.0, (lt - tv) / 0.2))
        ms.append(vulture(vomit=vo).xf(M(trans(p), roty(0.9 + i * 0.6))))
        if vo > 0:
            ms.append(vomit_stream(p + np.array([0.2, 0.7, 0.2]), lt - tv, 1.2, 6, i))
    cam = cam_lerp(Cam(tuple(TREE_POS + np.array([6, 3.5, 7])), tuple(TREE_POS + np.array([0, 4.3, 0])), 50),
                   Cam(tuple(TREE_POS + np.array([5, 3.8, 6])), tuple(TREE_POS + np.array([0, 4.5, 0])), 48), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def shot_flock_farm(lt, dur, tg):
    """imagine : une bande de vautours qui vomit au-dessus de la ferme"""
    u = lt / max(dur, 0.1)
    cam = Cam((-22 + 5 * u, 5, 26), (2, 9, -2), 55)
    ms = [FARM, GROUND_MEAT, flock(tg, KET + np.array([0, 0, -3]), 8, 7, 16, True), crouch_soap(tg, 1.0, 0.6)]
    return merge(ms), cam, ENV_DAY, dict(post_pil=C2.tint((255, 230, 180), 0.25))


def shot_sick(lt, dur, tg):
    """et nos deux goûteurs ?… mauvaise nouvelle"""
    t_v = WT(19, 'vomi') - cut['sick'] - 0.2
    sick = min(1.0, max(0.0, (lt - t_v) / 0.3))
    cam = cam_lerp(Cam(tuple(TASTE + np.array([1.8, 1.6, 3.2])), tuple(TASTE + np.array([0.4, 1.0, 0])), 50),
                   Cam(tuple(TASTE + np.array([1.4, 1.5, 2.6])), tuple(TASTE + np.array([0.4, 1.0, 0])), 46), lt / dur)
    ms = [FARM, tasters(tg, 1.0 if sick == 0 else 0.0, sick)]
    return merge(ms), C2.shake(cam, 0.03 * sick, tg), ENV_DAY, dict(post_pil=C2.tint((150, 230, 120), 0.35 * sick))


def shot_hypo(lt, dur, tg):
    ms = [LAB, box(1.6, 1.1, 0.05, (255, 255, 255), 'board_vulture').xf(trans(-1.4, 1.2, -2.85)),
          DOCTOR.mesh((-0.3, 0, -1.9), 0.1, dict(la=(0.8, 0.9, 1.6), ra=(0.8, 0.9, 1.6), hp=-0.1, hy=0.2 * math.sin(tg * 3)))]
    cam = Cam((0.5, 1.6, 0.6), (-0.3, 1.4, -1.9), 45)
    return merge(ms), cam, ENV_ROOM, {}


def shot_witness(lt, dur, tg):
    """la seule témoin regarde le ciel : pas un oiseau"""
    cam = cam_lerp(Cam((KET[0] - 4, 0.8, KET[2] + 3), (KET[0] - 1.4, 1.7, KET[2] + 0.3), 45), Cam((KET[0] - 3.5, 0.8, KET[2] + 2.6), (KET[0] - 1.4, 1.7, KET[2] + 0.3), 42), lt / dur)
    ms = [FARM, GROUND_MEAT, crouch_soap(tg, 1.0, 0.6)]
    return merge(ms), cam, ENV_DAY, {}


def museum():
    ms = [box(10, 0.05, 10, (255, 255, 255), 'tile_lab', ts=1.0), box(10, 4, 0.1, (60, 62, 70)).xf(trans(0, 0, -3)),
          box(0.8, 1.0, 0.8, (230, 228, 220)).xf(trans(0, 0, -1)), box(0.82, 0.9, 0.82, (200, 225, 235), alpha=0.25).xf(trans(0, 1.0, -1)),
          box(1.2, 0.8, 0.04, (220, 210, 180)).xf(trans(1.6, 1.3, -2.92)), bench_table(1.8, 0.5, 0.45, (255, 255, 255), 'wood_dark').xf(trans(-1.5, 0, 2))]
    ms.append(jar(JAR_MEAT[0].tint((0.85, 0.75, 0.7))).xf(trans(0, 1.0, -1)))
    return merge(ms)


MUSEUM = museum()


def shot_museum(lt, dur, tg):
    """150 ans plus tard : un morceau dans un bocal, dans une vitrine"""
    ms = [MUSEUM, VISITOR.mesh((0.9, 0, 0.2), math.pi + 0.5, dict(hp=0.35, lean=0.15))]
    cam = cam_lerp(Cam((-1.6, 1.7, 2.8), (0, 1.2, -1), 48), Cam((-1.3, 1.6, 2.3), (0, 1.2, -1), 45), lt / dur)
    return merge(ms), cam, ENV_MUSEUM, {}


def shot_question(lt, dur, tg):
    u = lt / max(dur, 0.1)
    cam = Cam((-18 + 3 * u, 4.5, 24), (2, 3, 0), 55)
    ms = [FARM, GROUND_MEAT, meat_rain(lt + 7, KET + np.array([0, 0, -1]), 12, 70, 8, 3.0, 25), crouch_soap(tg, 1.0, 0.6)]
    return merge(ms), cam, ENV_DAY, {}


def shot_loop(lt, dur, tg):
    return shot_hook(lt, dur, tg, p=lt - dur)


# ------------------------------------------------------------------ montage
cut.add('hook', 0.0, shot_hook)
cut.add('date', T(1) - 0.05, shot_date)
cut.add('soap', T(2), shot_soap)
cut.add('splat', T(3), shot_splat)
cut.add('wide', T(4), shot_wide)
cut.add('sky', T(5), shot_sky)
cut.add('neighbors', T(6), shot_neighbors)
cut.add('taste', WT(7, 'Ils') - 1.2, shot_taste)
cut.add('sheep', WT(8, 'mouton…') - 0.15, shot_sheep)
cut.add('deer', WT(8, 'chevreuil.') - 0.15, shot_deer)
cut.add('detail', T(9), shot_detail)
cut.add('paper', T(10), shot_paper)
cut.add('lab', T(11), shot_lab)
cut.add('jars', T(12), shot_jars)
cut.add('cta', T(13), shot_vultures_reveal)
cut.add('why', T(14), shot_why)
cut.add('doctor', T(15), shot_doctor)
cut.add('reveal', WT(15, 'vautours.') - 0.15, shot_vultures_reveal)
cut.add('perch', T(16), shot_perch)
cut.add('tree_chain', T(17), shot_tree_chain)
cut.add('flock_farm', T(18), shot_flock_farm)
cut.add('sick', T(19), shot_sick)
cut.add('hypo', T(20), shot_hypo)
cut.add('witness', T(21), shot_witness)
cut.add('museum', T(22), shot_museum)
cut.add('question', T(23), shot_question)
cut.add('loop', T(24), shot_loop)


def shot_cta_override():
    pass


tl.overlay = C2.overlays(
    C2.hook_title(['IL A PLU', 'DE LA VIANDE'], 0.0, 2.6, y=250, accent=1),
    C2.badge('KENTUCKY, 1876', T(1) - 0.05, 2.0, y=700),
    emu_pastille(3.3, 3.2, y=300),
    C2.badge('≈ 100 MÈTRES'.replace('≈ ', '~ '), WT(4, '100') - 0.1, 1.6, y=700),
    C2.badge('MOUTON ?', WT(8, 'mouton…') - 0.1, 1.0, y=700),
    C2.badge('CHEVREUIL ?', WT(8, 'chevreuil.') - 0.1, 1.2, y=700),
    retiens(T(9) - 0.1, max(2.0, T(10) - T(9)), y=300),
    C2.badge('MUSCLE', WT(12, 'muscle,') - 0.05, 1.0, y=700),
    C2.badge('CARTILAGE', WT(12, 'cartilage…') - 0.05, 1.2, y=700),
    C2.badge('POUMON', WT(12, 'poumon.') - 0.05, 1.3, y=700),
    C2.cta(T(13) - 0.1, max(1.8, T(14) - T(13) + 0.05)),
    C2.badge('HYPOTHÈSE', T(20) + 0.6, 1.8, y=700, col=(255, 140, 90)),
    C2.badge('AUJOURD\'HUI', T(22), 1.6, y=700),
    end_card(T(23), T(24) - T(23)),
)

subs = Subs(timing)


def splats(mx, t0, t1, rate=6.0, gain=0.35, seed=0):
    rr = np.random.default_rng(seed)
    t = t0
    while t < t1:
        mx.add(A.thwack(0.2), t, gain * rr.uniform(0.5, 1.0))
        t += rr.uniform(0.5, 1.5) / rate
    return mx


def build_audio(path):
    mx = A.Mixer(END)
    S = cut
    mx.add(C2.impact(), 0.0, 0.5)
    splats(mx, 0.0, S['soap'], 7, 0.45)
    mx.add(A.fire_crackle(5), 0, 0.2, length=END)
    mx.add(A.birds(8), S['soap'], 0.25, length=S['splat'] - S['soap'])
    splats(mx, S['splat'] + 0.1, S['neighbors'], 6, 0.4, 1)
    mx.add(C2.riser(1.0), S['splat'] - 0.9, 0.3)
    mx.add(A.wind(4), S['sky'], 0.25, length=S['neighbors'] - S['sky'])
    mx.add(A.footsteps(4, 6), S['neighbors'], 0.4, length=S['taste'] - S['neighbors'])
    mx.add(A.crowd(4), S['neighbors'], 0.2, length=S['detail'] - S['neighbors'])
    mx.add(C2.record_scratch(), WT(7, 'goûtent') - 0.05, 0.3)
    mx.add(A.birds(4), S['sheep'], 0.3, length=S['detail'] - S['sheep'])
    mx.add(C2.ding(), S['sheep'] + 0.1, 0.3)
    mx.add(C2.ding(), S['deer'] + 0.1, 0.3)
    mx.add(C2.riser(1.2), T(9) - 0.4, 0.3)
    mx.add(C2.ding(), T(9) + 0.1, 0.4)
    mx.add(A.crowd(4), S['paper'], 0.35, length=S['lab'] - S['paper'])
    mx.add(A.bell(1.2, 880), S['paper'] + 0.2, 0.2)
    mx.add(A.tick(), S['lab'] + 0.3, 0.3)
    for w in ('muscle,', 'cartilage…', 'poumon.'):
        mx.add(C2.pop(), WT(12, w), 0.4)
        mx.add(A.glass(0.6), WT(12, w) + 0.05, 0.2)
    mx.add(C2.pop(), T(13) + 0.05, 0.5)
    mx.add(C2.ding(), T(13) + max(1.8, T(14) - T(13)) * 0.62, 0.4)
    mx.add(A.wind(6), S['why'], 0.3, length=S['doctor'] - S['why'])
    mx.add(A.wind(6), S['reveal'], 0.3, length=S['sick'] - S['reveal'])
    mx.add(C2.sting(), S['reveal'] + 0.05, 0.3) if hasattr(C2, 'sting') else mx.add(A.sting(), S['reveal'] + 0.05, 0.35)
    for t in (WT(16, 'vomit'), WT(17, 'autres'), WT(17, 'autres') + 0.45, WT(17, 'autres') + 0.9, WT(17, 'autres') + 1.35):
        mx.add(A.splash(0.5), t + 0.05, 0.3)
    splats(mx, S['flock_farm'] + 0.2, S['sick'], 6, 0.35, 2)
    mx.add(C2.record_scratch(), WT(19, 'vomi') - 0.1, 0.35)
    mx.add(A.tick(), S['hypo'] + 0.2, 0.3)
    mx.add(A.wind(4), S['witness'], 0.25, length=S['museum'] - S['witness'])
    mx.add(C2.ding(), S['museum'] + 0.2, 0.25)
    mx.add(A.birds(6), S['question'], 0.2, length=END - S['question'])
    splats(mx, S['loop'], END, 7, 0.4, 3)
    C2.cut_sounds(mx, list(cut.st.values()), 0.08)
    mx.save(path)


if __name__ == '__main__':
    run(tl, subs, HERE, 'Good2No_ep23_Pluie_de_viande', build_audio, sys.argv)
