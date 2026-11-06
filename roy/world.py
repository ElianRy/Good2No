"""Décors et personnages : Roy Sullivan (Shenandoah, années 1940-1970)."""
import sys, math
sys.path.insert(0, '/home/claude/g2n')
import numpy as np
from lib import *

build_base_textures()

SKIN = (226, 176, 140)
HAIR = (75, 55, 38)
make_face('roy', skin=SKIN, brow_col=(70, 50, 32))
make_face('roy_nobrow', skin=SKIN, brows=False, soot=0.5)
make_face('roy_shock', skin=SKIN, mouth='open', brow_col=(70, 50, 32))
make_face('roy_shock_nb', skin=SKIN, mouth='open', brows=False, soot=0.6)
make_face('roy_closed', skin=SKIN, brow_col=(70, 50, 32), eyes_closed=True)
make_face('roy_shout', skin=SKIN, mouth='shout', brow_col=(70, 50, 32))
make_face('roy_smile', skin=SKIN, mouth='smile', brow_col=(70, 50, 32))
make_face('col1', skin=(232, 190, 160), brow_col=(110, 80, 50), mustache=True, hair_col=(110, 80, 50))
make_face('col2', skin=(210, 160, 125), brow_col=(40, 30, 25))
make_face('col1_worry', skin=(232, 190, 160), brow_col=(110, 80, 50), mustache=True, hair_col=(110, 80, 50), mouth='open')

tex_noise('asphalt', (55, 55, 58), (80, 80, 82), seed=31, octaves=1, speck=0.1, speck_col=(100, 100, 100))
tex_noise('uniform', (150, 140, 105), (170, 160, 122), seed=32, octaves=1)
tex_noise('uniform_g', (62, 72, 48), (78, 88, 60), seed=33, octaves=1)
tex_noise('truck_green', (60, 95, 70), (72, 108, 80), seed=34, octaves=1)
tex_noise('ridge', (50, 80, 70), (70, 100, 85), seed=35, octaves=3)
tex_noise('ridge_trees', (40, 70, 50), (70, 105, 70), seed=36, octaves=4, speck=0.2, speck_col=(30, 55, 40))


def burnt_leg_tex():
    def f(d, n):
        d.rectangle([0, 0, n, n], fill=(70, 80, 55))
        d.rectangle([n // 2 - 3, 0, n // 2 + 2, n], fill=(40, 30, 25))
        d.rectangle([n // 2 - 1, 0, n // 2, n], fill=(150, 70, 50))
    return tex_draw('burnt_leg', f)


burnt_leg_tex()


def sign_tex():
    def f(d, n):
        from PIL import ImageFont
        d.rectangle([0, 0, n, n], fill=(95, 65, 40))
        d.rectangle([1, 1, n - 2, n - 2], outline=(60, 40, 25))
    tex_draw('sign_blank', f)


sign_tex()


def make_sign_tex(name, text, size=(128, 48), bg=(95, 65, 40), fg=(235, 215, 160)):
    """texture plus large pour un panneau lisible"""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new('RGB', size, bg)
    d = ImageDraw.Draw(im)
    d.rectangle([2, 2, size[0] - 3, size[1] - 3], outline=tuple(int(c * 0.6) for c in bg), width=2)
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 15)
    lines = text.split('\n')
    y = (size[1] - 17 * len(lines)) // 2
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((size[0] - w) / 2, y), ln, font=f, fill=fg)
        y += 17
    arr = np.asarray(im)
    # stocke en 32x32 : on garde la texture large dans un banc séparé via découpe -> on remplace par
    # une texture 32x32 « échantillonnée » : moins lisible, donc on garde la grande en tuiles
    tiles = []
    tw = size[0] // 32
    th = size[1] // 16
    return arr


def roy(face='roy', hat=True, hair_burn=False):
    hc = (40, 30, 25) if hair_burn else HAIR
    return Human(face, skin=SKIN, shirt=(170, 160, 122), pants=(70, 80, 55), shoes=(45, 32, 24), hair=hc,
                 hat='ranger' if hat else None, hat_col=(150, 118, 78), belt=(70, 48, 28), shirt_tex='uniform',
                 pants_tex='uniform_g')


def colleague(face='col1', shirt=(170, 160, 122)):
    return Human(face, skin=(232, 190, 160), shirt=shirt, pants=(70, 80, 55), hair=(110, 80, 50),
                 hat='ranger', hat_col=(140, 110, 72), belt=(70, 48, 28), shirt_tex='uniform', pants_tex='uniform_g')


# --------------------------------------------------------------- terrains
def ridges(cx=0, cz=-150, layers=4, width=600, seed=0, base_col=(255, 255, 255)):
    """chaînes de montagnes bleutées en fond (Blue Ridge)"""
    rr = np.random.default_rng(seed)
    ms = []
    for k in range(layers):
        z = cz - k * 60
        n = 26
        xs = np.linspace(cx - width / 2, cx + width / 2, n + 1)
        hs = 12 + 18 * k + rr.random(n + 1) * (10 + 6 * k)
        hs = np.convolve(hs, np.ones(3) / 3, mode='same')
        tris, uvs = [], []
        for i in range(n):
            p0, p1 = (xs[i], -5, z), (xs[i + 1], -5, z)
            p2, p3 = (xs[i + 1], hs[i + 1], z - 10), (xs[i], hs[i], z - 10)
            tris += [[p0, p1, p2], [p0, p2, p3]]
            uvs += [[(0, 1), (1, 1), (1, 0)], [(0, 1), (1, 0), (0, 0)]]
        ms.append(Mesh(tris, C(base_col) * (1 - k * 0.08), uvs, TEXB['ridge_trees']))
    return merge(ms)


def forest(x0, z0, x1, z1, n=40, seed=0, avoid=(), mix=0.3, hmin=5, hmax=9, hfun=None):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        x, z = rr.uniform(x0, x1), rr.uniform(z0, z1)
        if any((x - a) ** 2 + (z - b) ** 2 < r * r for (a, b, r) in avoid):
            continue
        y = hfun(x, z) if hfun else 0
        h = rr.uniform(hmin, hmax)
        if rr.random() < mix:
            ms.append(deciduous(h, h * 0.35, seed=i + seed * 100, col=(255, 255, 255) if rr.random() < .6 else (230, 240, 200)).xf(trans(x, y, z)))
        else:
            ms.append(pine(h, h * 0.27, seed=i + seed * 100).xf(trans(x, y, z)))
    return merge(ms)


# --------------------------------------------------------------- tour de guet
def lookout_tower(h=9.0, rod=False):
    ms = []
    leg = 3.2
    top = 2.2
    for sx in (-1, 1):
        for sz in (-1, 1):
            a = np.array([sx * leg / 2, 0, sz * leg / 2])
            b = np.array([sx * top / 2, h, sz * top / 2])
            d = b - a
            L = np.linalg.norm(d)
            # poutre inclinée
            ang_x = math.atan2(d[2], d[1])
            ang_z = -math.atan2(d[0], math.hypot(d[1], d[2]))
            ms.append(box(0.18, L, 0.18, (120, 90, 60), 'planks_v').xf(M(trans(a), rotx(ang_x), rotz(ang_z))))
    # croisillons
    for k in range(4):
        y0, y1 = h * k / 4, h * (k + 1) / 4
        w0 = leg + (top - leg) * k / 4
        w1 = leg + (top - leg) * (k + 1) / 4
        for side in range(4):
            r = roty(side * math.pi / 2)
            p0 = np.array([-w0 / 2, y0, w0 / 2])
            p1 = np.array([w1 / 2, y1, w1 / 2])
            d = p1 - p0
            L = np.linalg.norm(d)
            ms.append(box(L, 0.1, 0.08, (110, 82, 55)).xf(M(r, trans((p0 + p1) / 2 - np.array([0, 0.05, 0])), rotz(math.atan2(d[1], d[0])))))
            ms.append(box(w1, 0.1, 0.1, (110, 82, 55)).xf(M(r, trans(0, y1 - 0.05, w1 / 2))))
    # escalier zigzag
    for k in range(8):
        y = h * k / 8
        ms.append(box(0.7, 0.06, 1.2, (130, 100, 70), 'planks').xf(M(trans(0.3 * (1 if k % 2 else -1), y + 0.4, 0), roty(0))))
    # cabine
    cab = 3.0
    ms.append(box(cab + 0.4, 0.15, cab + 0.4, (120, 90, 60), 'planks').xf(trans(0, h, 0)))
    ms.append(box(cab, 1.0, cab, (150, 130, 100), 'planks_grey', ts=1.0).xf(trans(0, h + 0.15, 0)))
    # vitres (cadres + verre)
    for side in range(4):
        r = roty(side * math.pi / 2)
        ms.append(box(cab, 1.1, 0.04, (150, 190, 210), alpha=0.6).xf(M(r, trans(0, h + 1.15, cab / 2))))
        for k in range(5):
            ms.append(box(0.08, 1.1, 0.08, (220, 215, 200)).xf(M(r, trans(-cab / 2 + k * cab / 4, h + 1.15, cab / 2))))
    ms.append(box(cab, 0.1, cab, (220, 215, 200)).xf(trans(0, h + 2.25, 0)))
    # toit pyramidal
    rt = [[(-1.9, h + 2.35, -1.9), (1.9, h + 2.35, -1.9), (0, h + 3.3, 0)],
          [(1.9, h + 2.35, -1.9), (1.9, h + 2.35, 1.9), (0, h + 3.3, 0)],
          [(1.9, h + 2.35, 1.9), (-1.9, h + 2.35, 1.9), (0, h + 3.3, 0)],
          [(-1.9, h + 2.35, 1.9), (-1.9, h + 2.35, -1.9), (0, h + 3.3, 0)]]
    ms.append(Mesh(rt, C((90, 90, 95)), [[(0, 1), (1, 1), (.5, 0)]] * 4, TEXB['roof_tin']))
    if rod:
        ms.append(cyl(0.03, 0.02, 1.5, 4, (180, 180, 180)).xf(trans(0, h + 3.3, 0)))
    # porte de cabine (côté +z)
    ms.append(box(0.8, 1.9, 0.05, (110, 75, 45), 'door').xf(trans(0.9, h + 0.15, cab / 2 + 0.01)))
    return merge(ms)


# --------------------------------------------------------------- camion
def truck(col=(255, 255, 255), wheel_rot=0.0, door_open=0.0, window_open=True):
    """pick-up années 60 du National Park Service, avance vers +z. origine au sol, centre."""
    G = 'truck_green'
    ms = []
    body = (255, 255, 255)
    # chassis + caisse arrière
    ms.append(box(1.9, 0.55, 4.9, body, G).xf(trans(0, 0.45, -0.1)))
    # capot
    ms.append(box(1.85, 0.32, 1.5, body, G).xf(trans(0, 1.0, 1.5)))
    # calandre + phares
    ms.append(box(1.6, 0.4, 0.06, (200, 200, 195), 'metal').xf(trans(0, 0.65, 2.37)))
    for s in (-1, 1):
        ms.append(cyl(0.12, 0.12, 0.05, 8, (250, 245, 220), emis=0.6).xf(M(trans(s * 0.7, 0.9, 2.38), rotx(math.pi / 2))))
    ms.append(box(1.95, 0.15, 0.12, (190, 190, 190), 'metal').xf(trans(0, 0.42, 2.42)))
    # cabine
    ms.append(box(1.85, 0.35, 1.5, body, G).xf(trans(0, 1.0, 0.0)))
    # montants + toit (fenêtres ouvertes)
    for (x, z) in ((-0.88, 0.7), (0.88, 0.7), (-0.88, -0.72), (0.88, -0.72)):
        ms.append(box(0.08, 0.6, 0.08, (235, 235, 230)).xf(trans(x, 1.35, z)))
    ms.append(box(1.85, 0.08, 1.5, (235, 235, 230)).xf(trans(0, 1.95, 0.0)))
    # pare-brise
    ms.append(quad((-0.85, 1.35, 0.74), (0.85, 1.35, 0.74), (0.85, 1.93, 0.7), (-0.85, 1.93, 0.7), (140, 175, 190), alpha=0.45))
    # lunette arrière
    ms.append(quad((-0.85, 1.35, -0.74), (0.85, 1.35, -0.74), (0.85, 1.93, -0.74), (-0.85, 1.93, -0.74), (60, 70, 75)))
    # portes : bande blanche + logo
    for s in (-1, 1):
        ms.append(box(0.02, 0.1, 1.4, (235, 235, 230)).xf(trans(s * 0.935, 1.25, 0.0)))
        ms.append(box(0.02, 0.22, 0.3, (200, 170, 90)).xf(trans(s * 0.935, 0.95, 0.1)))
        if not window_open:
            ms.append(box(0.02, 0.58, 1.3, (140, 175, 190), alpha=0.4).xf(trans(s * 0.92, 1.35, 0)))
    # benne : rebords
    for s in (-1, 1):
        ms.append(box(0.08, 0.45, 2.3, body, G).xf(trans(s * 0.91, 1.0, -1.6)))
    ms.append(box(1.9, 0.45, 0.08, body, G).xf(trans(0, 1.0, -2.75)))
    ms.append(box(1.75, 0.04, 2.3, (60, 60, 60)).xf(trans(0, 1.0, -1.6)))
    # pare-chocs arrière + feux
    ms.append(box(1.95, 0.12, 0.12, (190, 190, 190), 'metal').xf(trans(0, 0.42, -2.6)))
    for s in (-1, 1):
        ms.append(box(0.15, 0.12, 0.04, (200, 30, 30), emis=0.5).xf(trans(s * 0.8, 1.1, -2.8)))
    # roues
    for (x, z) in ((-0.88, 1.45), (0.88, 1.45), (-0.88, -1.7), (0.88, -1.7)):
        w = merge([cyl(0.38, 0.38, 0.28, 10, (30, 30, 30), cap_col=(35, 35, 35)), cyl(0.2, 0.2, 0.3, 8, (170, 170, 165), 'metal').xf(trans(0, -0.01, 0))])
        ms.append(w.xf(M(trans(x + (0.14 if x > 0 else -0.14), 0.38, z), rotz(math.pi / 2), roty(wheel_rot), trans(0, -0.14, 0))))
    # sièges + volant (visibles par la fenêtre)
    ms.append(box(1.6, 0.5, 0.25, (110, 85, 60)).xf(trans(0, 1.1, -0.5)))
    ms.append(box(1.6, 0.12, 0.6, (110, 85, 60)).xf(trans(0, 1.05, -0.2)))
    ms.append(cyl(0.2, 0.2, 0.03, 8, (30, 30, 30)).xf(M(trans(0.45, 1.45, 0.45), rotx(-1.0))))
    return merge(ms)


def water_can():
    return merge([box(0.25, 0.32, 0.14, (180, 40, 30), 'metal'), box(0.06, 0.06, 0.06, (60, 60, 60)).xf(trans(0.08, 0.32, 0)),
                  box(0.14, 0.03, 0.03, (60, 60, 60)).xf(trans(-0.03, 0.36, 0))])


# --------------------------------------------------------------- maison / poteau
def house(w=7.0, d=6.0, h=2.8, col=(235, 232, 222)):
    ms = []
    ms.append(box(w, h, d, col, 'planks_white', ts=1.2))
    roof_h = 1.6
    rt = [[(-w / 2 - .3, h, d / 2 + .3), (w / 2 + .3, h, d / 2 + .3), (w / 2 + .3, h + roof_h, 0)],
          [(-w / 2 - .3, h, d / 2 + .3), (w / 2 + .3, h + roof_h, 0), (-w / 2 - .3, h + roof_h, 0)],
          [(w / 2 + .3, h, -d / 2 - .3), (-w / 2 - .3, h, -d / 2 - .3), (-w / 2 - .3, h + roof_h, 0)],
          [(w / 2 + .3, h, -d / 2 - .3), (-w / 2 - .3, h + roof_h, 0), (w / 2 + .3, h + roof_h, 0)]]
    ms.append(Mesh(rt, C((110, 60, 50)), [[(0, 1), (3, 1), (3, 0)], [(0, 1), (3, 0), (0, 0)]] * 2, TEXB['roof_red']))
    for s in (-1, 1):
        ms.append(Mesh([[(s * w / 2, h, d / 2), (s * w / 2, h, -d / 2), (s * w / 2, h + roof_h, 0)]], C(col), [[(0, 1), (1, 1), (.5, 0)]], TEXB['planks_white']))
    ms.append(box(1.0, 2.1, 0.06, (255, 255, 255), 'door').xf(trans(0, 0, d / 2 + 0.01)))
    for x in (-2.2, 2.2):
        ms.append(box(1.1, 1.1, 0.06, (255, 255, 255), 'window').xf(trans(x, 1.0, d / 2 + 0.01)))
    # porche
    ms.append(box(3.0, 0.2, 1.6, (130, 110, 90), 'planks').xf(trans(0, 0, d / 2 + 0.8)))
    ms.append(box(1.4, 1.2, 1.2, (150, 70, 60), 'brick').xf(trans(2.2, h + 0.5, -1.0)))
    return merge(ms)


def utility_pole(transformer=True, h=8.0):
    ms = [cyl(0.15, 0.12, h, 6, (110, 85, 60), 'bark', ts=1.0)]
    ms.append(box(2.0, 0.12, 0.12, (110, 85, 60)).xf(trans(0, h - 0.6, 0)))
    for x in (-0.9, 0, 0.9):
        ms.append(cyl(0.05, 0.04, 0.15, 5, (230, 230, 230)).xf(trans(x, h - 0.48, 0)))
    if transformer:
        ms.append(cyl(0.32, 0.32, 1.0, 8, (150, 155, 160), 'metal').xf(trans(0.0, h - 2.4, 0.35)))
        ms.append(box(0.1, 0.4, 0.1, (60, 60, 60)).xf(trans(0.0, h - 2.2, 0.15)))
        for x in (-0.12, 0.12):
            ms.append(cyl(0.04, 0.03, 0.2, 5, (230, 230, 230)).xf(trans(x, h - 1.4, 0.35)))
    return merge(ms)


def wires(p0, p1, sag=0.6, col=(30, 30, 30), n=8, w=0.03):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    ms = []
    for i in range(n):
        a, b = i / n, (i + 1) / n
        pa = p0 + (p1 - p0) * a - np.array([0, sag * 4 * a * (1 - a), 0])
        pb = p0 + (p1 - p0) * b - np.array([0, sag * 4 * b * (1 - b), 0])
        d = pb - pa
        L = np.linalg.norm(d)
        yaw = math.atan2(d[0], d[2])
        pitch = -math.asin(d[1] / L)
        ms.append(box(w, w, L, col).xf(M(trans((pa + pb) / 2 - np.array([0, w / 2, 0])), roty(yaw), rotx(pitch))))
    return merge(ms)


def fence(x0, z0, x1, z1, n=10, col=(240, 238, 230)):
    ms = []
    for i in range(n + 1):
        t = i / n
        x, z = x0 + (x1 - x0) * t, z0 + (z1 - z0) * t
        ms.append(box(0.1, 1.0, 0.1, col).xf(trans(x, 0, z)))
    L = math.hypot(x1 - x0, z1 - z0)
    yaw = math.atan2(x1 - x0, z1 - z0)
    for y in (0.4, 0.8):
        ms.append(box(0.05, 0.1, L, col).xf(M(trans((x0 + x1) / 2, y, (z0 + z1) / 2), roty(yaw))))
    return merge(ms)


# --------------------------------------------------------------- intérieur poste de garde
def ranger_station_interior():
    ms = []
    W_, D_, H_ = 5.0, 4.0, 2.7
    ms.append(box(W_, 0.05, D_, (140, 110, 80), 'planks', ts=1.0).xf(trans(0, -0.05, 0)))
    # murs (intérieur)
    ms.append(box(W_, H_, 0.1, (170, 140, 105), 'planks', ts=1.0, faces='f').xf(trans(0, 0, -D_ / 2)))
    ms.append(box(0.1, H_, D_, (170, 140, 105), 'planks', ts=1.0, faces='r').xf(trans(-W_ / 2, 0, 0)))
    ms.append(box(0.1, H_, D_, (170, 140, 105), 'planks', ts=1.0, faces='l').xf(trans(W_ / 2, 0, 0)))
    ms.append(box(W_, 0.05, D_, (150, 125, 95), 'planks_v', ts=1.0).xf(trans(0, H_, 0)))
    # fenêtre (orage dehors)
    ms.append(box(1.4, 1.1, 0.05, (60, 70, 90)).xf(trans(-1.0, 1.1, -D_ / 2 + 0.06)))
    ms.append(box(1.5, 0.08, 0.08, (220, 210, 190)).xf(trans(-1.0, 1.1, -D_ / 2 + 0.08)))
    ms.append(box(1.5, 0.08, 0.08, (220, 210, 190)).xf(trans(-1.0, 2.2, -D_ / 2 + 0.08)))
    ms.append(box(0.08, 1.1, 0.08, (220, 210, 190)).xf(trans(-1.0, 1.1, -D_ / 2 + 0.08)))
    for x in (-1.72, -0.28):
        ms.append(box(0.08, 1.2, 0.08, (220, 210, 190)).xf(trans(x, 1.05, -D_ / 2 + 0.08)))
    # carte au mur
    def mapf(d, n):
        d.rectangle([0, 0, n, n], fill=(225, 215, 170))
        d.line([2, 20, 10, 14, 18, 18, 30, 6], fill=(60, 110, 160), width=1)
        d.polygon([(4, 4), (14, 2), (16, 10), (6, 12)], fill=(120, 160, 90))
        d.polygon([(18, 20), (28, 16), (29, 28), (20, 29)], fill=(120, 160, 90))
        d.rectangle([0, 0, n - 1, n - 1], outline=(90, 70, 50))
    tex_draw('map', mapf)
    ms.append(box(1.2, 0.9, 0.03, (255, 255, 255), 'map').xf(trans(1.2, 1.3, -D_ / 2 + 0.07)))
    # bureau + chaise + radio + lampe
    ms.append(box(1.6, 0.06, 0.8, (120, 85, 55), 'planks').xf(trans(1.0, 0.75, -1.4)))
    for (x, z) in ((0.3, -1.05), (1.7, -1.05), (0.3, -1.75), (1.7, -1.75)):
        ms.append(box(0.06, 0.75, 0.06, (100, 70, 45)).xf(trans(x, 0, z)))
    ms.append(box(0.45, 0.3, 0.3, (70, 75, 70), 'metal').xf(trans(1.4, 0.81, -1.55)))
    ms.append(box(0.3, 0.02, 0.4, (240, 235, 220)).xf(trans(0.7, 0.81, -1.35)))
    # évier + robinet (il n'arrive pas à passer la tête dessous)
    ms.append(box(0.7, 0.85, 0.5, (200, 200, 195), 'metal').xf(trans(2.1, 0, 0.6)))
    ms.append(box(0.08, 0.3, 0.08, (180, 180, 185)).xf(trans(2.25, 0.85, 0.6)))
    ms.append(box(0.25, 0.06, 0.06, (180, 180, 185)).xf(trans(2.16, 1.12, 0.6)))
    # porte-manteau avec veste
    ms.append(cyl(0.03, 0.03, 1.8, 5, (90, 65, 40)).xf(trans(-2.1, 0, 1.3)))
    # étagère + boîtes
    ms.append(box(1.2, 0.05, 0.3, (120, 85, 55)).xf(trans(-1.7, 1.8, -D_ / 2 + 0.2)))
    for k, c in enumerate([(160, 50, 40), (60, 90, 140), (200, 180, 80)]):
        ms.append(box(0.25, 0.3, 0.22, c).xf(trans(-2.1 + k * 0.35, 1.85, -D_ / 2 + 0.2)))
    return merge(ms)


def ranger_station_exterior():
    ms = [box(5.2, 2.9, 4.2, (255, 255, 255), 'planks_grey', ts=1.0)]
    rt = [[(-3, 2.9, 2.5), (3, 2.9, 2.5), (3, 4.1, 0)], [(-3, 2.9, 2.5), (3, 4.1, 0), (-3, 4.1, 0)],
          [(3, 2.9, -2.5), (-3, 2.9, -2.5), (-3, 4.1, 0)], [(3, 2.9, -2.5), (-3, 4.1, 0), (3, 4.1, 0)]]
    ms.append(Mesh(rt, C((90, 95, 85)), [[(0, 1), (3, 1), (3, 0)], [(0, 1), (3, 0), (0, 0)]] * 2, TEXB['roof_tin']))
    for s in (-1, 1):
        ms.append(Mesh([[(s * 2.6, 2.9, 2.1), (s * 2.6, 2.9, -2.1), (s * 2.6, 4.1, 0)]], C((255, 255, 255)), [[(0, 1), (1, 1), (.5, 0)]], TEXB['planks_grey']))
    ms.append(box(1.0, 2.1, 0.06, (255, 255, 255), 'door').xf(trans(1.2, 0, 2.11)))
    ms.append(box(1.4, 1.1, 0.06, (255, 255, 255), 'window').xf(trans(-1.0, 1.1, 2.11)))
    ms.append(cyl(0.05, 0.04, 6.0, 5, (200, 200, 200)).xf(trans(-3.2, 0, 2.0)))
    return merge(ms)


# --------------------------------------------------------------- ruisseau, ours, poisson
def trout(col=(150, 140, 110)):
    body = sphere(0.16, 6, 4, col, sy=0.35).xf(scale(1, 1, 0.4)).xf(rotz(0))
    body = sphere(0.18, 6, 4, col, sy=0.4)
    body.tris = body.tris * np.array([1.0, 1.0, 0.35])
    tail = Mesh([[(0.16, 0, 0), (0.3, 0.07, 0), (0.3, -0.07, 0)]], C(col) * 0.8)
    spots = box(0.2, 0.02, 0.07, (190, 110, 120)).xf(trans(0, 0.0, 0.0))
    return merge([body, tail, spots])


def bear(phase=0.0, stand=0.0, yaw=0.0, head_turn=0.0, mouth=0.0, paws_up=None):
    """ours noir, face +z. stand 0..1 = se dresse sur ses pattes arrière, mouth 0..1 = gueule ouverte"""
    F = 'fur_bear'
    W = (255, 255, 255)
    ms = []
    paws_up = stand if paws_up is None else paws_up
    pivot = M(trans(0, 0.85, -0.5), rotx(-stand * 1.2))
    # corps : arrière-train, ventre, bosse d'épaule
    ms.append(sphere(0.52, 8, 5, W, F, sy=0.95).xf(M(pivot, trans(0, 0.05, 0.15), scale(1.0, 1.0, 1.05))))
    ms.append(sphere(0.5, 8, 5, W, F).xf(M(pivot, trans(0, 0.08, 0.7), scale(0.95, 1.0, 1.0))))
    ms.append(sphere(0.38, 7, 4, W, F).xf(M(pivot, trans(0, 0.38 - 0.1 * stand, 0.85 - 0.1 * stand))))
    ms.append(sphere(0.12, 5, 3, W, F).xf(M(pivot, trans(0, 0.15, -0.38))))  # queue
    # tête (contre-rotation pour regarder devant)
    head = M(pivot, trans(0, 0.3 * (1 - stand) - 0.32 * stand, 1.3 + 0.12 * stand), rotx(stand * 1.2 - 0.1 * (1 - stand)), roty(head_turn), rotx(0.25 * mouth))
    ms.append(box(0.46, 0.4, 0.42, W, F).xf(M(head, trans(0, -0.2, 0))))
    ms.append(box(0.5, 0.3, 0.3, W, F).xf(M(head, trans(0, -0.18, -0.12))))  # bajoues
    for x in (-0.18, 0.18):
        ms.append(box(0.12, 0.13, 0.06, W, F).xf(M(head, trans(x, 0.18, -0.08))))
        ms.append(box(0.06, 0.07, 0.02, (60, 45, 40)).xf(M(head, trans(x, 0.2, -0.05))))
        # yeux petits et brillants
        ms.append(box(0.06, 0.04, 0.02, (15, 10, 8)).xf(M(head, trans(x * 0.6, 0.0, 0.215))))
        ms.append(box(0.02, 0.02, 0.01, (230, 200, 120), emis=0.6).xf(M(head, trans(x * 0.6 + 0.01, 0.01, 0.225))))
    # museau fauve + truffe
    mz = M(head, trans(0, -0.14, 0.2))
    ms.append(box(0.22, 0.14, 0.26, (125, 95, 70)).xf(M(mz, trans(0, -0.02, 0.12))))
    ms.append(box(0.11, 0.07, 0.05, (15, 12, 12)).xf(M(mz, trans(0, 0.04, 0.26))))
    # mâchoire inférieure qui s'ouvre
    jaw = M(mz, trans(0, -0.08, 0.0), rotx(0.75 * mouth))
    ms.append(box(0.2, 0.06, 0.24, (110, 82, 60)).xf(M(jaw, trans(0, -0.06, 0.12))))
    if mouth > 0.1:
        ms.append(box(0.18, 0.02, 0.22, (150, 35, 40)).xf(M(jaw, trans(0, 0.0, 0.12))))
        ms.append(box(0.18, 0.1 * mouth, 0.2, (90, 20, 25)).xf(M(mz, trans(0, -0.08 - 0.05 * mouth, 0.12))))
        for s_ in (-1, 1):  # crocs
            ms.append(box(0.025, 0.06, 0.025, (245, 240, 225)).xf(M(mz, trans(s_ * 0.07, -0.11, 0.22))))
            ms.append(box(0.025, 0.05, 0.025, (245, 240, 225)).xf(M(jaw, trans(s_ * 0.07, 0.0, 0.21))))
    # pattes arrière (restent au sol)
    for x, ph in ((-0.3, 0.0), (0.3, math.pi)):
        sw = 0.4 * math.sin(phase + ph) * (1 - stand)
        hip = M(trans(x, 0.85, -0.45), rotx(sw))
        ms.append(box(0.28, 0.55, 0.34, W, F).xf(M(hip, trans(0, -0.55, 0))))
        kn = M(hip, trans(0, -0.5, 0))
        ms.append(box(0.24, 0.35, 0.26, W, F).xf(M(kn, trans(0, -0.35, 0.02))))
        ms.append(box(0.26, 0.08, 0.36, (30, 26, 24)).xf(M(kn, trans(0, -0.36, 0.08))))
    # pattes avant : au sol en marchant, levées griffes en avant quand il se dresse
    for x, ph in ((-0.3, math.pi), (0.3, 0.0)):
        sh = M(pivot, trans(x, -0.05, 1.0))
        walk = 0.45 * math.sin(phase + ph) * (1 - stand)
        lift = paws_up * (1.35 + 0.2 * math.sin(phase * 2 + ph))
        arm = M(sh, rotx(stand * 1.2 - lift + walk), rotz(x * 2.4 * paws_up))
        ms.append(box(0.26, 0.5, 0.3, W, F).xf(M(arm, trans(0, -0.5, 0))))
        el = M(arm, trans(0, -0.48, 0), rotx(-0.5 * paws_up))
        ms.append(box(0.22, 0.4, 0.26, W, F).xf(M(el, trans(0, -0.4, 0))))
        paw = M(el, trans(0, -0.42, 0))
        ms.append(box(0.26, 0.1, 0.3, (30, 26, 24)).xf(M(paw, trans(0, -0.05, 0.04))))
        for k in range(4):  # griffes
            ms.append(box(0.03, 0.03, 0.1, (225, 215, 195)).xf(M(paw, trans(-0.09 + k * 0.06, -0.08, 0.2))))
    return merge(ms).xf(roty(yaw))
def stream_bed(x0=-30, x1=30, w=4.0, z=0.0):
    ms = []
    ms.append(box(x1 - x0, 0.02, w, (255, 255, 255), 'water', ts=3.0).xf(trans((x0 + x1) / 2, -0.25, z)))
    ms.append(box(x1 - x0, 0.2, w + 0.2, (90, 75, 60), 'gravel', ts=2).xf(trans((x0 + x1) / 2, -0.55, z)))
    rr = np.random.default_rng(4)
    for i in range(30):
        x = rr.uniform(x0, x1)
        side = rr.choice([-1, 1])
        ms.append(rock(rr.uniform(0.3, 0.8), seed=i).xf(trans(x, -0.3, z + side * (w / 2 + rr.uniform(-0.3, 0.5)))))
    return merge(ms)


def stream_ground(x0, z0, x1, z1, zc=0.0, w=4.0):
    def h(x, z):
        d = abs(z - zc)
        if d < w / 2 + 0.3:
            return -0.6
        return min(0.0, -0.6 + (d - w / 2 - 0.3) * 1.2)
    return grid(x0, z0, x1, z1, 24, 24, h, (255, 255, 255), 'grass', 3.0)


def fishing_rod():
    return merge([cyl(0.015, 0.008, 2.2, 4, (120, 80, 40)), cyl(0.03, 0.03, 0.06, 6, (60, 60, 60)).xf(trans(0, 0.25, 0.03))])


def branch():
    return merge([cyl(0.04, 0.025, 1.4, 5, (110, 80, 50), 'bark'), cyl(0.02, 0.01, 0.4, 4, (110, 80, 50)).xf(M(trans(0, 0.9, 0), rotz(0.7)))])


# --------------------------------------------------------------- musée
def hat_case(burn=True):
    ms = [box(0.8, 1.0, 0.8, (60, 45, 35), 'planks'),
          box(0.75, 0.6, 0.75, (180, 210, 220), alpha=0.35).xf(trans(0, 1.0, 0)),
          box(0.8, 0.04, 0.8, (200, 190, 150)).xf(trans(0, 1.6, 0))]
    h = hat_mesh('ranger', (150, 118, 78)).xf(trans(0, 1.08, 0))
    ms.append(h)
    if burn:
        ms.append(box(0.08, 0.02, 0.1, (30, 25, 20)).xf(trans(0.05, 1.255, 0.02)))
    return merge(ms)


# --------------------------------------------------------------- ambiances
ENV_SUN = Env(sky_top=(70, 115, 190), sky_hor=(195, 210, 220), fog=(170, 190, 205), fog_near=40, fog_far=320,
              light=(-0.45, 0.8, 0.35), amb=0.55)
ENV_STORM = Env(sky_top=(28, 30, 40), sky_hor=(75, 80, 92), fog=(62, 66, 78), fog_near=15, fog_far=160,
                light=(-0.3, 0.8, 0.4), amb=0.5, light_col=(170, 175, 195))
ENV_INT = Env(sky_top=(30, 30, 35), sky_hor=(30, 30, 35), fog=(20, 20, 25), fog_near=8, fog_far=40,
              light=(0.3, 0.8, 0.5), amb=0.55, light_col=(255, 225, 180))
ENV_MUSEUM = Env(sky_top=(30, 25, 22), sky_hor=(30, 25, 22), fog=(25, 20, 18), fog_near=6, fog_far=30,
                 light=(0.2, 0.9, 0.4), amb=0.6, light_col=(255, 230, 190))


def flash_env(env, k, pos=None):
    """éclair : illumination globale"""
    if k <= 0:
        return env
    e = env.copy(amb=min(1.0, env.amb + 0.35 * k))
    e.sky_top = env.sky_top + (np.array([0.55, 0.58, 0.72]) - env.sky_top) * k
    e.sky_hor = env.sky_hor + (np.array([0.85, 0.87, 0.95]) - env.sky_hor) * k
    e.fog = env.fog + (np.array([0.6, 0.62, 0.72]) - env.fog) * k * 0.5
    if pos is not None:
        e.points = list(env.points) + [(pos, (190, 200, 255), 2.5 * k, 25)]
    return e


def rain_mesh(cam, t, n=140, area=14, seed=0, col=(170, 180, 200), slant=(0.1, 0, 0.05)):
    rr = np.random.default_rng(seed)
    cp = np.asarray(cam.pos)
    f = np.asarray(cam.at) - cp
    f /= np.linalg.norm(f)
    ms = []
    for i in range(n):
        o = np.array([rr.uniform(-area, area), 0, rr.uniform(-area, area)])
        o = o + f * area * 0.6
        if np.hypot(o[0], o[2]) < 3.0:
            o[0] += 3.0 * np.sign(o[0] + 1e-3)
            o[2] += f[2] * 3.0
        y = (rr.uniform(0, 12) - t * 18) % 12 - 2
        p = cp + o + np.array([0, y, 0])
        p[1] = cp[1] - 3 + ((rr.uniform(0, 12) - t * 18) % 12)
        ms.append(strip([p, p - np.array([slant[0], 0.7, slant[2]])], 0.025, cam, col, emis=0.6, alpha=0.6))
    return merge(ms)


def storm_clouds(cy=40, seed=0, w=300, col=(45, 47, 58), n=30, z=-40):
    return cloud_bank(0, cy, z, w, seed, col, n, sz=18)


def cliff_edge(x):
    """bord de la falaise (z) selon x — découpé, irrégulier"""
    return 0.7 * math.sin(0.31 * x + 0.4) + 0.45 * math.sin(0.83 * x + 1.7) + 0.25 * math.sin(1.9 * x) + 0.2 * math.sin(3.7 * x + 0.3)


CLIFF_DROP = 75.0


def cliff_scene():
    ms = []
    xs = np.arange(-60, 60.01, 1.5)
    rr = np.random.default_rng(8)
    # plateau qui suit le bord découpé
    zrows = [-140, -70, -35, -18, -8, -3]
    tris, uvs = [], []
    for i in range(len(xs) - 1):
        xa, xb = xs[i], xs[i + 1]
        za_e, zb_e = cliff_edge(xa), cliff_edge(xb)
        rows_a = zrows + [za_e - 0.6, za_e]
        rows_b = zrows + [zb_e - 0.6, zb_e]
        for k in range(len(rows_a) - 1):
            ya0 = -0.12 if k == len(rows_a) - 2 else 0.0
            ya1 = -0.25 if k + 1 == len(rows_a) - 1 else (-0.12 if k + 1 == len(rows_a) - 2 else 0.0)
            p0, p1 = (xa, ya0, rows_a[k]), (xb, ya0, rows_b[k])
            p2, p3 = (xb, ya1, rows_b[k + 1]), (xa, ya1, rows_a[k + 1])
            tris += [[p0, p1, p2], [p0, p2, p3]]
            u = [(xa / 3, rows_a[k] / 3), (xb / 3, rows_b[k] / 3), (xb / 3, rows_b[k + 1] / 3), (xa / 3, rows_a[k + 1] / 3)]
            uvs += [[u[0], u[1], u[2]], [u[0], u[2], u[3]]]
    ms.append(Mesh(tris, C((255, 255, 255)), uvs, TEXB['grass']))
    # paroi rocheuse : strates, surplomb sous le bord, éboulis en bas
    levels = [0.0, -0.25, -2.0, -6.0, -12.0, -20.0, -30.0, -42.0, -55.0, -66.0, -CLIFF_DROP]
    offs = {}
    for i, x in enumerate(xs):
        for k, y in enumerate(levels):
            if k <= 1:
                o = 0.0
            elif k == 2:
                o = -0.6 + rr.uniform(-0.2, 0.2)  # léger surplomb : la roche rentre sous le bord
            else:
                o = rr.uniform(-1.5, 1.5) + (k - 2) * 0.35 + (2.5 if k == len(levels) - 1 else 0)
            offs[(i, k)] = o
    tris, uvs, cols = [], [], []
    strata = [(150, 140, 125), (125, 115, 105), (160, 150, 135), (110, 102, 95), (140, 128, 112)]
    for i in range(len(xs) - 1):
        for k in range(1, len(levels) - 1):
            def P(ii, kk):
                return (xs[ii], levels[kk], cliff_edge(xs[ii]) + offs[(ii, kk)])
            p0, p1, p2, p3 = P(i, k), P(i + 1, k), P(i + 1, k + 1), P(i, k + 1)
            tris += [[p0, p1, p2], [p0, p2, p3]]
            u = [(xs[i] / 4, levels[k] / 4), (xs[i + 1] / 4, levels[k] / 4), (xs[i + 1] / 4, levels[k + 1] / 4), (xs[i] / 4, levels[k + 1] / 4)]
            uvs += [[u[0], u[1], u[2]], [u[0], u[2], u[3]]]
            c = C(strata[k % len(strata)]) * (0.9 + 0.2 * rr.random())
            cols += [c, c]
        # lèvre herbeuse (k=0..1)
        p0, p1 = (xs[i], -0.25, cliff_edge(xs[i])), (xs[i + 1], -0.25, cliff_edge(xs[i + 1]))
        p2, p3 = (xs[i + 1], levels[2], cliff_edge(xs[i + 1]) + offs[(i + 1, 2)]), (xs[i], levels[2], cliff_edge(xs[i]) + offs[(i, 2)])
        tris += [[p0, p1, p2], [p0, p2, p3]]
        uvs += [[(0, 0), (1, 0), (1, 1)], [(0, 0), (1, 1), (0, 1)]]
        cols += [C((95, 80, 60)), C((95, 80, 60))]
    ms.append(Mesh(tris, np.array(cols), uvs, TEXB['rock']))
    # vallée tout en bas : forêt, rivière, rochers
    ms.append(grid(-250, -10, 250, 400, 10, 10, lambda x, z: -CLIFF_DROP, (255, 255, 255), 'grass', 6.0))
    ms.append(forest(-150, 15, 150, 300, 90, seed=21, hfun=lambda x, z: -CLIFF_DROP, hmin=8, hmax=13))
    riv = []
    for k in range(40):
        z0, z1 = 25 + k * 8, 25 + (k + 1) * 8
        x0, x1 = 20 * math.sin(z0 * 0.02) - 30, 20 * math.sin(z1 * 0.02) - 30
        riv += [[(x0 - 4, -CLIFF_DROP + 0.1, z0), (x1 - 4, -CLIFF_DROP + 0.1, z1), (x1 + 4, -CLIFF_DROP + 0.1, z1)],
                [(x0 - 4, -CLIFF_DROP + 0.1, z0), (x1 + 4, -CLIFF_DROP + 0.1, z1), (x0 + 4, -CLIFF_DROP + 0.1, z0)]]
    ms.append(Mesh(riv, C((90, 130, 160))))
    for k in range(25):
        x = rr.uniform(-55, 55)
        ms.append(rock(rr.uniform(1.5, 4.0), seed=100 + k).xf(trans(x, -CLIFF_DROP, cliff_edge(x) + rr.uniform(6, 14))))
    # forêt et rochers sur le plateau, route qui passe derrière
    ms.append(forest(-60, -140, 60, -20, 60, seed=22, avoid=[(0.8, z, 4.0) for z in range(-60, 0, 3)] + [(x, -16, 4.5) for x in range(-60, 61, 4)]))
    ms.append(box(120, 0.02, 6.0, (255, 255, 255), 'asphalt', ts=3.0).xf(trans(0, 0.0, -16)))
    ms.append(box(120, 0.025, 0.12, (230, 220, 120), emis=0.2).xf(trans(0, 0.0, -16)))
    for x in (-6.5, -4.0, 4.2, 6.0, 9.5, -10.0):
        ms.append(rock(rr.uniform(0.4, 0.9), int(abs(x) * 10)).xf(trans(x, -0.15, cliff_edge(x) - 0.7)))
    ms.append(grass_tufts(-25, -14, 25, -1.0, 900, 6, avoid=lambda x, z: z > cliff_edge(x) - 0.5 or (abs(x - 0.8) < 1.1 and z > -13)))
    return merge(ms)


def can_frame(c, tilt=0.0, yaw=0.0):
    """repère du bidon : origine au fond, x = largeur (poignées de part et d'autre)"""
    return M(trans(c), roty(yaw), rotz(tilt))


def stream_h(x, z, zc=0.0, w=4.0):
    d = abs(z - zc)
    if d < w / 2 + 0.3:
        return -0.6
    return min(0.0, -0.6 + (d - w / 2 - 0.3) * 1.2)


def on_ground(x, z):
    return np.array([x, stream_h(x, z), z])


def bear_path(u):
    """l'ours sort de la forêt d'en face, traverse le ruisseau et arrive vers les truites"""
    pts = [np.array([3.5, 0, -8.0]), np.array([2.6, 0, -2.4]), np.array([2.0, 0, 0.6]), np.array([1.9, 0, 1.3])]
    u = min(max(u, 0.0), 1.0) * (len(pts) - 1)
    i = min(int(u), len(pts) - 2)
    f = u - i
    p = pts[i] * (1 - f) + pts[i + 1] * f
    p[1] = max(stream_h(p[0], p[2]), -0.6)
    return p




def station_scene():
    g = grid(-60, -60, 60, 60, 10, 10, None, (255, 255, 255), 'grass', 3.0)
    return merge([g, ranger_station_exterior(), box(4, 0.02, 30, (190, 170, 140), 'gravel', ts=1.5).xf(trans(1.2, 0, 17)),
                  forest(-50, -60, 50, -6, 45, seed=57), forest(-50, 12, 50, 40, 15, seed=58, avoid=[(1.2, z, 4) for z in range(0, 41, 3)]),
                  grass_tufts(-15, -5, 15, 15, 700, 9, avoid=lambda x, z: abs(x - 1.2) < 2.2 or (abs(x) < 3 and abs(z) < 2.5))])


STRINGER_POS = np.array([1.4, stream_h(1.4, 2.3) + 0.05, 2.3])
