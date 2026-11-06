"""Décors et personnages : Hachikō (Tokyo, Shibuya, 1924-1935 ; statues 1934, 1948, 2015)."""
import sys, math
sys.path[:0] = ['/home/claude/g2n']
import numpy as np
from lib import *
from common2 import *

build_base_textures()

tex_noise('wood_jp', (110, 75, 45), (135, 95, 60), seed=401, octaves=2)
tex_noise('tile_roof', (60, 62, 70), (80, 82, 92), seed=402, octaves=1)
tex_stripes('roof_tiles', (70, 72, 82), (50, 52, 60), n=6, vertical=True)
tex_noise('shoji', (235, 230, 210), (245, 242, 228), seed=403, octaves=1)
tex_noise('suit_grey', (70, 70, 75), (85, 85, 90), seed=404, octaves=1)
tex_noise('suit_brown', (85, 65, 50), (100, 78, 60), seed=405, octaves=1)
tex_noise('kimono1', (150, 60, 80), (175, 80, 100), seed=406, octaves=1, speck=0.15, speck_col=(240, 210, 220))
tex_noise('kimono2', (50, 70, 120), (70, 90, 140), seed=407, octaves=1, speck=0.15, speck_col=(230, 230, 240))
tex_noise('bronze', (95, 70, 45), (130, 98, 62), seed=408, octaves=3, speck=0.06, speck_col=(70, 110, 90))
tex_noise('granite', (150, 148, 145), (180, 178, 172), seed=409, octaves=2, speck=0.2, speck_col=(110, 108, 105))
tex_noise('cobble', (130, 125, 115), (160, 152, 140), seed=410, octaves=1, speck=0.15, speck_col=(100, 95, 90))
tex_noise('car_green', (70, 95, 70), (85, 112, 85), seed=411, octaves=1)
tex_noise('snow', (225, 230, 240), (245, 248, 252), seed=412, octaves=2)
tex_noise('tatami', (190, 180, 120), (210, 200, 140), seed=413, octaves=1)
tex_noise('blanket', (225, 222, 210), (242, 240, 232), seed=414, octaves=1)


def _shoji_panel(d, n):
    d.rectangle([0, 0, n, n], fill=(80, 55, 35))
    d.rectangle([2, 2, n - 3, n - 3], fill=(240, 235, 215))
    for x in range(2, n - 2, 7):
        d.line([x, 2, x, n - 3], fill=(90, 62, 40))
    for y in range(2, n - 2, 7):
        d.line([2, y, n - 3, y], fill=(90, 62, 40))


tex_draw('shoji_panel', _shoji_panel)


def _paper(d, n):
    d.rectangle([0, 0, n, n], fill=(225, 218, 195))
    for y in range(3, n - 2, 3):
        d.line([2, y, 12, y], fill=(60, 55, 50))
    d.rectangle([15, 4, n - 3, 20], fill=(180, 172, 150))
    d.polygon([(18, 18), (19, 9), (21, 12), (25, 12), (27, 9), (27, 18)], fill=(60, 55, 45))   # chien dessiné
    for y in range(23, n - 2, 3):
        d.line([15, y, n - 3, y], fill=(60, 55, 50))


tex_draw('newspaper', _paper)


def _calendar(d, n):
    d.rectangle([0, 0, n, n], fill=(240, 236, 225))
    d.rectangle([0, 0, n, 7], fill=(180, 40, 40))
    d.rectangle([9, 12, 22, 26], fill=(30, 30, 30))
    d.rectangle([12, 15, 19, 23], fill=(240, 236, 225))


tex_draw('calendar', _calendar)


def _sign_jp(d, n):
    d.rectangle([0, 0, n, n], fill=(240, 236, 225))
    d.rectangle([1, 1, n - 2, n - 2], outline=(40, 30, 25))
    for x in (6, 14, 22):
        d.rectangle([x, 8, x + 4, 22], fill=(30, 25, 20))
        d.line([x - 1, 14, x + 5, 14], fill=(240, 236, 225))


tex_draw('sign_jp', _sign_jp)

# ---------------------------------------------------------------- personnages
SKIN_J = (232, 200, 165)
make_face('ueno', skin=SKIN_J, brow_col=(30, 25, 20), eye_col=(30, 22, 18), mustache=True, hair_col=(40, 35, 30))
make_face('ueno_smile', skin=SKIN_J, brow_col=(30, 25, 20), eye_col=(30, 22, 18), mustache=True, hair_col=(40, 35, 30), mouth='smile')
make_face('ueno_closed', skin=SKIN_J, brow_col=(30, 25, 20), eyes_closed=True, mustache=True, hair_col=(40, 35, 30))
make_face('jp_m1', skin=(228, 195, 160), brow_col=(25, 20, 18), eye_col=(30, 22, 18))
make_face('jp_m2', skin=(220, 186, 150), brow_col=(25, 20, 18), eye_col=(30, 22, 18), mustache=True, hair_col=(25, 20, 18))
make_face('jp_w', skin=(238, 210, 180), brow_col=(25, 20, 18), eye_col=(30, 22, 18))
make_face('jp_w_smile', skin=(238, 210, 180), brow_col=(25, 20, 18), eye_col=(30, 22, 18), mouth='smile')
make_face('jp_angry', skin=(225, 190, 155), brow_col=(25, 20, 18), eye_col=(30, 22, 18), mouth='shout')
make_face('jp_vendor', skin=(215, 180, 145), brow_col=(25, 20, 18), eye_col=(30, 22, 18), mouth='smile')
make_face('girl', skin=(240, 212, 185), brow_col=(25, 20, 18), eye_col=(30, 22, 18), mouth='smile')

HAIR_JP = (25, 22, 20)


def ueno(face='ueno', hat=True):
    return Human(face, skin=SKIN_J, shirt=(235, 235, 230), pants=(70, 70, 75), shoes=(25, 20, 18), hair=(40, 35, 30),
                 hat='bowler' if hat else None, hat_col=(45, 42, 40), jacket=(70, 70, 75), tie=(60, 30, 30))


def salaryman(i=0):
    face = 'jp_m1' if i % 2 == 0 else 'jp_m2'
    j = [(70, 70, 75), (85, 65, 50), (40, 40, 48)][i % 3]
    return Human(face, skin=(228, 195, 160), shirt=(235, 235, 230), pants=j, hair=HAIR_JP, hat=['bowler', 'flatcap', None][i % 3],
                 hat_col=(50, 45, 40), jacket=j, tie=(40, 40, 60))


def kimono_woman(i=0, face='jp_w'):
    col = [(150, 60, 80), (50, 70, 120), (90, 110, 80)][i % 3]
    tex = ['kimono1', 'kimono2', None][i % 3]

    def obi(P, at):
        return box(0.4, 0.14, 0.26, (220, 190, 90)).xf(M(at['torso'], trans(0, 0.06, 0)))
    return Human(face, skin=(238, 210, 180), shirt=col, pants=col, robe=col, shirt_tex=tex, hair=HAIR_JP, hair_style='bald', build=0.85,
                 extra=merge_extra(woman_extra('bun', hair=HAIR_JP), obi))


def worker_jp(face='jp_angry'):
    return Human(face, skin=(225, 190, 155), shirt=(40, 45, 70), pants=(40, 45, 70), hair=HAIR_JP, hat='kepi', hat_col=(35, 40, 60), belt=(30, 25, 20))


def vendor_jp():
    def apron(P, at):
        return box(0.38, 0.5, 0.02, (240, 240, 235)).xf(M(at['torso'], trans(0, -0.1, 0.13)))
    return Human('jp_vendor', skin=(215, 180, 145), shirt=(60, 70, 90), pants=(60, 60, 60), hair=HAIR_JP, sleeves='short', extra=apron)


def girl():
    return Human('girl', skin=(240, 212, 185), shirt=(200, 70, 80), pants=(200, 70, 80), robe=(200, 70, 80), hair=HAIR_JP, height=0.75,
                 hair_style='bald', extra=woman_extra('bun', hair=HAIR_JP))


def merge_extra(*fs):
    def f(P, at):
        return merge([g(P, at) for g in fs])
    return f


HACHI = Dog(1.0)
HACHI_OLD = Dog(1.0, (235, 228, 215), ear_l_drop=1.0)
PUPPY = Dog(0.45)
BRONZE_COL = (190, 145, 95)


def bronze(mesh):
    m = mesh.copy()
    m.col[:] = C(BRONZE_COL)
    m.tex[:] = TEXB['bronze']
    return m


# ---------------------------------------------------------------- décors
def jp_house(w=8, d=7, h=3.0, seed=0):
    ms = [box(w, 0.5, d, (140, 130, 115), 'granite').xf(trans(0, 0, 0)),
          box(w, h, d, (255, 255, 255), 'wood_jp', ts=1.0).xf(trans(0, 0.5, 0))]
    for x in np.linspace(-w / 2 + 1, w / 2 - 1, int(w / 1.6)):
        ms.append(box(1.4, 1.9, 0.06, (255, 255, 255), 'shoji_panel').xf(trans(x, 0.7, d / 2 + 0.02)))
    # toit à 4 pans en tuiles
    ov = 0.9
    y0, y1 = 0.5 + h, 0.5 + h + 1.8
    A, B, Cc, D = (-w / 2 - ov, y0, d / 2 + ov), (w / 2 + ov, y0, d / 2 + ov), (w / 2 + ov, y0, -d / 2 - ov), (-w / 2 - ov, y0, -d / 2 - ov)
    r0, r1 = (-w / 4, y1, 0), (w / 4, y1, 0)
    tris = [[A, B, r1], [A, r1, r0], [Cc, D, r0], [Cc, r0, r1], [B, Cc, r1], [D, A, r0]]
    uv = [[(0, 1), (4, 1), (3, 0)], [(0, 1), (3, 0), (1, 0)]] * 2 + [[(0, 1), (2, 1), (1, 0)]] * 2
    ms.append(Mesh(tris, C((255, 255, 255)), uv, TEXB['roof_tiles']))
    ms.append(box(w / 2 + 0.4, 0.25, 0.3, (40, 42, 50)).xf(trans(0, y1, 0)))
    # véranda (engawa)
    ms.append(box(w, 0.1, 1.0, (150, 110, 70), 'planks', ts=0.6).xf(trans(0, 0.45, d / 2 + 0.5)))
    return merge(ms)


def railcar(lit=False, door_open=0.0, wheel_rot=0.0):
    """motrice électrique années 20, vers +x, plancher à 1,1 m"""
    L, Wd = 15.0, 2.7
    ms = [box(L, 2.5, Wd, (255, 255, 255), 'car_green', ts=2.0).xf(trans(0, 0.9, 0))]
    ms.append(box(L + 0.2, 0.3, Wd + 0.2, (60, 60, 62)).xf(trans(0, 3.4, 0)))
    for s in (-1, 1):
        for i in range(8):
            x = -L / 2 + 1.2 + i * 1.6
            if abs(x) < 1.0 or abs(x - 5) < 0.6 or abs(x + 5) < 0.6:
                continue
            ms.append(box(1.0, 0.8, 0.04, (255, 230, 160) if lit else (110, 130, 140), emis=0.8 if lit else 0.0).xf(trans(x, 2.0, s * (Wd / 2 + 0.01))))
        for dx in (-5, 5):
            ms.append(box(1.1, 2.0, 0.05, (60, 75, 60)).xf(trans(dx + (door_open * 0.9 if s > 0 else 0), 1.1, s * (Wd / 2 + 0.02))))
    # pantographe
    ms.append(box(1.2, 0.1, 1.2, (40, 40, 40)).xf(trans(4, 3.7, 0)))
    ms.append(rod((3.6, 3.8, 0), (4.4, 4.6, 0), 0.03, (40, 40, 40), n=3))
    ms.append(rod((4.4, 4.6, 0), (3.6, 5.3, 0), 0.03, (40, 40, 40), n=3))
    ms.append(box(0.1, 0.06, 1.6, (40, 40, 40)).xf(trans(3.6, 5.3, 0)))
    for x in (-5.5, -4.2, 4.2, 5.5):
        for s in (-1, 1):
            ms.append(cyl(0.42, 0.42, 0.12, 10, (40, 40, 42)).xf(M(trans(x, 0.42, s * 0.75), rotx(math.pi / 2), roty(wheel_rot))))
    ms.append(box(L - 2, 0.4, 2.0, (35, 35, 35)).xf(trans(0, 0.5, 0)))
    return merge(ms)


def track(x0, x1, z=0.0):
    L = x1 - x0
    ms = [box(L, 0.15, 3.0, (150, 140, 125), 'gravel', ts=1.2).xf(trans((x0 + x1) / 2, -0.12, z))]
    for i in range(int(L / 0.7)):
        ms.append(box(0.22, 0.08, 1.9, (100, 75, 50)).xf(trans(x0 + (i + 0.5) * 0.7, 0.0, z)))
    for s in (-1, 1):
        ms.append(box(L, 0.12, 0.07, (120, 115, 110), 'metal').xf(trans((x0 + x1) / 2, 0.08, z + s * 0.53)))
    return merge(ms)


def catenary(x0, x1, z=0.0, step=20):
    ms = []
    for x in np.arange(x0, x1, step):
        ms.append(box(0.25, 6.5, 0.25, (80, 70, 60), 'wood_jp').xf(trans(x, 0, z - 2.2)))
        ms.append(box(0.15, 0.15, 2.5, (80, 70, 60)).xf(trans(x, 6.0, z - 1.0)))
    ms.append(box(x1 - x0, 0.03, 0.03, (30, 30, 30)).xf(trans((x0 + x1) / 2, 5.35, z)))
    return merge(ms)


def station():
    """gare de Shibuya (années 20) : bâtiment en bois, sortie vers la place (+z), quai et voies derrière (-z)"""
    ms = [box(22, 4.5, 8, (255, 255, 255), 'wood_jp', ts=1.2).xf(trans(0, 0, -4))]
    ms.append(box(22, 0.6, 8, (230, 225, 210), 'plaster').xf(trans(0, 4.5, -4)))
    A, B, Cc, D = (-12, 5.1, 1.0), (12, 5.1, 1.0), (12, 5.1, -9.0), (-12, 5.1, -9.0)
    r0, r1 = (-8, 7.6, -4), (8, 7.6, -4)
    ms.append(Mesh([[A, B, r1], [A, r1, r0], [Cc, D, r0], [Cc, r0, r1], [B, Cc, r1], [D, A, r0]], C((255, 255, 255)),
                   [[(0, 1), (8, 1), (6, 0)], [(0, 1), (6, 0), (2, 0)]] * 2 + [[(0, 1), (3, 1), (1.5, 0)]] * 2, TEXB['roof_tiles']))
    # sortie (grande ouverture) + auvent
    ms.append(box(5, 3.0, 0.1, (25, 22, 20)).xf(trans(0, 0, 0.02)))
    ms.append(box(7, 0.15, 2.6, (60, 50, 40), 'wood_jp').xf(trans(0, 3.2, 1.3)))
    for x in (-3.2, 3.2):
        ms.append(box(0.18, 3.2, 0.18, (70, 50, 35)).xf(trans(x, 0, 2.5)))
    for x in (-8, -5, 5, 8):
        ms.append(box(1.6, 1.4, 0.06, (255, 255, 255), 'window').xf(trans(x, 1.2, 0.02)))
    ms.append(box(3.4, 0.9, 0.08, (255, 255, 255), 'sign_jp').xf(trans(0, 3.6, 2.62)))
    # quai et voies derrière
    ms.append(box(40, 1.0, 4, (190, 185, 175), 'stone_block', ts=1.0).xf(trans(0, 0, -10)))
    ms.append(track(-80, 80, -14.0))
    ms.append(catenary(-80, 80, -14.0))
    return merge(ms)


def plaza(snow=False):
    ms = [grid(-50, -2, 50, 60, 8, 8, None, (255, 255, 255), 'snow' if snow else 'cobble', 2.5)]
    rr = np.random.default_rng(3)
    for i, x in enumerate((-20, -12, 12, 20)):
        ms.append(jp_house(8, 7, 3.2, i).xf(M(trans(x, 0, 22), roty(math.pi))))
    for x in (-6, 6):
        ms.append(cyl(0.08, 0.08, 4, 6, (40, 40, 40)).xf(trans(x, 0, 6)))
        ms.append(box(0.4, 0.5, 0.4, (40, 40, 40)).xf(trans(x, 4, 6)))
        ms.append(box(0.3, 0.4, 0.3, (255, 230, 160), emis=0.7).xf(trans(x, 4.05, 6)))
    return merge(ms)


SPOT = np.array([4.6, 0.0, 4.4])   # là où Hachi attend, à droite de la sortie


def yatai(lit=True):
    """stand de yakitori : comptoir, toit, lanterne rouge"""
    ms = [box(1.8, 1.0, 0.8, (120, 85, 55), 'wood_jp'), box(2.1, 0.08, 1.2, (60, 45, 35)).xf(trans(0, 2.1, 0))]
    for x in (-0.85, 0.85):
        ms.append(box(0.08, 1.1, 0.08, (70, 50, 35)).xf(trans(x, 1.0, 0.35)))
    ms.append(sphere(0.18, 7, 4, (230, 50, 40), emis=0.8 if lit else 0.2, sy=1.3).xf(trans(0.6, 1.8, 0.55)))
    ms.append(box(1.2, 0.05, 0.4, (40, 40, 40), 'metal').xf(trans(0, 1.0, 0.1)))
    for i in range(5):
        ms.append(box(0.02, 0.02, 0.3, (190, 150, 90)).xf(trans(-0.4 + i * 0.2, 1.06, 0.1)))
    return merge(ms)


def skewer():
    return merge([box(0.012, 0.012, 0.28, (200, 170, 120)), box(0.04, 0.04, 0.12, (150, 80, 45)).xf(trans(0, 0, 0.05))])


def crate(open_=0.0):
    ms = [box(0.6, 0.05, 0.45, (170, 130, 85), 'planks')]
    for (w, d, x, z) in ((0.6, 0.04, 0, 0.2), (0.6, 0.04, 0, -0.2), (0.04, 0.45, 0.28, 0), (0.04, 0.45, -0.28, 0)):
        ms.append(box(w, 0.35, d, (170, 130, 85), 'planks').xf(trans(x, 0.05, z)))
    lid = box(0.62, 0.04, 0.47, (160, 120, 80), 'planks').xf(M(trans(0, 0.4, -0.22), rotx(-open_ * 1.8), trans(0, 0, 0.22)))
    ms.append(lid)
    return merge(ms)


def office():
    ms = [box(6, 0.05, 5, (140, 100, 65), 'planks', ts=0.7).xf(trans(0, -0.05, 0)),
          box(6, 3, 0.1, (230, 225, 210), 'plaster').xf(trans(0, 0, -2.5)),
          box(0.1, 3, 5, (230, 225, 210), 'plaster').xf(trans(-3, 0, 0))]
    ms.append(box(1.8, 0.06, 0.9, (100, 70, 45), 'wood_jp').xf(trans(0, 0.75, -1.2)))
    for x in (-0.8, 0.8):
        for z in (-0.8, -1.6):
            ms.append(box(0.06, 0.75, 0.06, (80, 55, 35)).xf(trans(x, 0, z)))
    for i in range(6):
        ms.append(box(0.1, 0.3, 0.22, [(150, 40, 40), (40, 60, 120), (60, 100, 60)][i % 3]).xf(trans(-0.7 + i * 0.12, 0.81, -1.5)))
    ms.append(box(0.3, 0.01, 0.4, (240, 236, 222)).xf(trans(0.1, 0.785, -1.1)))
    ms.append(box(1.4, 1.2, 0.05, (255, 255, 255), 'window').xf(trans(1.6, 1.3, -2.44)))
    ms.append(box(0.4, 0.5, 0.03, (255, 255, 255), 'calendar').xf(trans(-1.2, 1.6, -2.44)))
    ms.append(box(0.45, 0.45, 0.45, (80, 55, 35), 'wood_jp').xf(trans(0, 0, -0.4)))
    # porte-manteau
    ms.append(cyl(0.03, 0.03, 1.8, 5, (80, 55, 35)).xf(trans(-2.3, 0, -1.8)))
    return merge(ms)


def sakura(h=5.0, seed=0, bloom=True, snow=False, autumn=False):
    rr = np.random.default_rng(seed)
    ms = [cyl(0.22, 0.14, h * 0.5, 6, (90, 60, 50), 'bark', ts=1.0)]
    col = (245, 190, 205) if bloom else ((210, 120, 50) if autumn else ((240, 245, 250) if snow else (80, 120, 60)))
    for i in range(4):
        o = (rr.normal() * 1.0, h * 0.55 + rr.random() * h * 0.25, rr.normal() * 1.0)
        ms.append(sphere(1.6 * (0.7 + rr.random() * 0.3), 7, 4, col, 'leaves' if not (bloom or snow) else 0, sy=0.75).xf(trans(o)))
    return merge(ms)


def pedestal(h=1.2):
    return merge([box(1.4, h, 1.0, (255, 255, 255), 'granite'), box(1.6, 0.15, 1.2, (255, 255, 255), 'granite').xf(trans(0, h, 0))])


def statue_dog(old=True):
    d = (HACHI_OLD if old else HACHI).mesh((0, 0, 0), 0.0, dict(sit=1.0))
    return bronze(d)


def statue_reunion():
    """statue de 2015 (Université de Tokyo) : Ueno se penche, Hachi lui saute dessus"""
    u = ueno('ueno_smile').mesh((0, 0, 0), 0.0, dict(lean=0.25, ra=(1.3, 0.3, 0.7), la=(1.3, 0.3, 0.7), hp=0.4))
    d = HACHI.mesh((0, 0, 0.75), math.pi, dict(jump=1.0, mouth=1.0, tail=0.5))
    return bronze(merge([u, d]))


def alley():
    ms = [grid(-6, -20, 6, 20, 3, 6, None, (255, 255, 255), 'cobble', 2.0)]
    for s in (-1, 1):
        for z in range(-18, 20, 7):
            ms.append(box(4, 3.5, 6.5, (255, 255, 255), 'wood_jp', ts=1.0).xf(trans(s * 4.2, 0, z)))
            ms.append(box(4.6, 0.2, 7, (60, 62, 70)).xf(trans(s * 4.2, 3.5, z)))
    for i in range(4):
        ms.append(box(0.5, 0.8, 0.5, (130, 100, 70), 'planks').xf(trans(-1.7, 0, -3 + i * 0.6)))
    return merge(ms)


def furnace_glow():
    return merge([box(4, 3, 3, (60, 55, 50), 'brick'), box(1.5, 1.2, 0.1, (255, 140, 40), emis=1.0).xf(trans(0, 0.5, 1.52))])


def campus():
    ms = [grid(-40, -40, 40, 40, 6, 6, None, (255, 255, 255), 'grass', 3.0),
          box(30, 12, 10, (170, 120, 90), 'brick', ts=2.0).xf(trans(0, 0, -20))]
    for x in np.arange(-13, 14, 3.2):
        for y in (2, 6.5):
            ms.append(box(1.4, 2.4, 0.06, (255, 255, 255), 'window').xf(trans(x, y, -14.97)))
    for x in (-10, 10):
        ms.append(deciduous(7, 3, int(x + 20)).xf(trans(x, 0, -6)))
    ms.append(box(4, 0.02, 30, (190, 180, 160), 'gravel', ts=1.5).xf(trans(0, 0.01, 0)))
    return merge(ms)


def city_skyline(seed=0):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(40):
        x, z = rr.uniform(-200, 200), rr.uniform(-260, -60)
        h = rr.uniform(4, 9)
        ms.append(jp_house(rr.uniform(6, 10), rr.uniform(6, 9), h * 0.5, i).xf(M(trans(x, 0, z), roty(rr.choice([0, math.pi / 2])))))
    return merge(ms)


ENV_DAY = Env(sky_top=(90, 140, 205), sky_hor=(215, 220, 220), fog=(200, 205, 210), fog_near=40, fog_far=320,
              light=(-0.4, 0.8, 0.5), amb=0.55, light_col=(255, 245, 228))
ENV_EVE = Env(sky_top=(70, 80, 140), sky_hor=(245, 170, 110), fog=(215, 160, 120), fog_near=30, fog_far=260,
              light=(-0.8, 0.35, 0.5), amb=0.5, light_col=(255, 195, 140))
ENV_NIGHT = Env(sky_top=(10, 14, 30), sky_hor=(30, 36, 60), fog=(22, 26, 44), fog_near=10, fog_far=80,
                light=(0.3, 0.8, 0.5), amb=0.45, light_col=(150, 160, 210))
ENV_SNOW = Env(sky_top=(150, 160, 175), sky_hor=(210, 215, 222), fog=(200, 205, 215), fog_near=15, fog_far=140,
               light=(-0.3, 0.9, 0.4), amb=0.65, light_col=(235, 240, 255))
ENV_ROOM = Env(sky_top=(35, 30, 26), sky_hor=(35, 30, 26), fog=(25, 20, 18), fog_near=6, fog_far=30,
               light=(0.4, 0.7, 0.6), amb=0.5, light_col=(255, 225, 180))
ENV_DAWN = Env(sky_top=(70, 80, 120), sky_hor=(225, 180, 160), fog=(190, 170, 165), fog_near=10, fog_far=90,
               light=(-0.7, 0.3, 0.5), amb=0.5, light_col=(255, 210, 180))
ENV_WAR = Env(sky_top=(70, 70, 75), sky_hor=(150, 140, 125), fog=(130, 120, 110), fog_near=20, fog_far=200,
              light=(-0.3, 0.8, 0.4), amb=0.55, light_col=(230, 220, 200))
