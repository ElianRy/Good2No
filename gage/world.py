"""Décors et personnages : Phineas Gage (Cavendish, Vermont, 1848 ; Chili 1852-1859)."""
import sys, math
sys.path[:0] = ['/home/claude/g2n']
import numpy as np
from lib import *
from common2 import *

build_base_textures()

tex_noise('ledge', (120, 115, 108), (150, 145, 135), seed=301, octaves=4, speck=0.08, speck_col=(95, 90, 85))
tex_noise('vest', (60, 50, 40), (75, 62, 50), seed=302, octaves=1)
tex_noise('shirt_w', (225, 222, 210), (240, 238, 228), seed=303, octaves=1)
tex_noise('linen', (200, 185, 150), (215, 200, 168), seed=304, octaves=1)
tex_noise('rag', (90, 80, 65), (115, 100, 80), seed=305, octaves=2, speck=0.2, speck_col=(60, 55, 45))
tex_noise('andes', (120, 105, 95), (150, 135, 120), seed=306, octaves=4)
tex_noise('dust', (190, 160, 120), (215, 185, 145), seed=307, speck=0.08, speck_col=(170, 140, 100))
tex_noise('quilt', (170, 60, 60), (200, 180, 150), seed=308, octaves=1, speck=0.3, speck_col=(60, 80, 140))
tex_noise('wallboard', (200, 185, 155), (220, 205, 175), seed=309, octaves=1)
tex_noise('fur_ox', (140, 90, 55), (170, 120, 80), seed=15, octaves=3, speck=0.08)
tex_noise('powder', (25, 25, 25), (50, 48, 45), seed=310, speck=0.3, speck_col=(90, 90, 90))
tex_noise('xray_grid', (8, 20, 45), (12, 30, 62), seed=311, octaves=1)


def _book(d, n):
    d.rectangle([0, 0, n, n], fill=(110, 40, 35))
    d.rectangle([2, 2, n - 3, n - 3], outline=(200, 170, 80))
    d.rectangle([6, 8, n - 7, 12], fill=(200, 170, 80))
    d.rectangle([9, 15, n - 10, 16], fill=(200, 170, 80))


tex_draw('book_cover', _book)


def _pages(d, n):
    d.rectangle([0, 0, n, n], fill=(232, 222, 195))
    d.line([n // 2, 0, n // 2, n], fill=(150, 140, 120))
    for y in range(4, n - 3, 3):
        d.line([3, y, n // 2 - 3, y], fill=(70, 60, 50))
        d.line([n // 2 + 3, y, n - 3 - (y * 5 % 7), y], fill=(70, 60, 50))


tex_draw('pages', _pages)


def _sign(d, n):
    d.rectangle([0, 0, n, n], fill=(235, 225, 200))
    d.rectangle([1, 1, n - 2, n - 2], outline=(90, 60, 35))
    for y in (10, 18):
        d.line([5, y, n - 6, y], fill=(40, 30, 25), width=2)


tex_draw('hotel_sign', _sign)


def _grid(d, n):
    d.rectangle([0, 0, n, n], fill=(6, 18, 40))
    d.line([0, 0, n, 0], fill=(30, 90, 140))
    d.line([0, 0, 0, n], fill=(30, 90, 140))


tex_draw('xgrid', _grid)


# ---------------------------------------------------------------- visages
SKIN_G = (232, 192, 160)
HAIR_G = (55, 38, 25)
make_face('gage', skin=SKIN_G, brow_col=(55, 38, 25), eye_col=(60, 70, 90))
make_face('gage_smile', skin=SKIN_G, brow_col=(55, 38, 25), eye_col=(60, 70, 90), mouth='smile')
make_face('gage_open', skin=SKIN_G, brow_col=(55, 38, 25), eye_col=(60, 70, 90), mouth='open')
make_face('gage_shout', skin=SKIN_G, brow_col=(55, 38, 25), eye_col=(60, 70, 90), mouth='shout')
make_face('gage_closed', skin=SKIN_G, brow_col=(55, 38, 25), eyes_closed=True)


def make_face_onebad(name, skin, mouth='neutral', soot=0.0, fever=False):
    """visage de Gage après l'accident : œil gauche fermé (aveugle), paupière tombante"""
    sk = np.asarray(skin)

    def fn(d, n):
        d.rectangle([0, 0, n, n], fill=tuple(sk))
        d.rectangle([0, 0, n, 3], fill=tuple((sk * 0.85).astype(int)))
        ey = 13
        # œil droit du personnage = à gauche de l'image (x=8), œil gauche = à droite (x=19)
        d.rectangle([8, ey, 12, ey + 3], fill=(245, 245, 240))
        d.rectangle([9, ey, 11, ey + 3], fill=(60, 70, 90))
        d.point([10, ey + 1], fill=(250, 250, 250))
        d.line([19, ey + 2, 23, ey + 3], fill=(60, 35, 30))
        d.rectangle([18, ey - 1, 24, ey + 1], fill=tuple((sk * 0.75).astype(int)))
        for ex in (8, 19):
            d.rectangle([ex - 1, ey - 3, ex + 5, ey - 2], fill=(55, 38, 25))
        d.rectangle([14, 16, 17, 21], fill=tuple((sk * 0.82).astype(int)))
        d.rectangle([14, 21, 17, 22], fill=tuple((sk * 0.65).astype(int)))
        d.rectangle([20, 19, 24, 20], fill=tuple((sk * 0.7).astype(int)))   # cicatrice sous la pommette
        if mouth == 'smile':
            d.line([11, 25, 13, 27, 18, 27, 20, 25], fill=(120, 50, 45), width=1)
        elif mouth == 'open':
            d.rectangle([12, 25, 19, 28], fill=(70, 20, 20))
        elif mouth == 'shout':
            d.ellipse([12, 24, 19, 30], fill=(70, 20, 20))
        else:
            d.rectangle([12, 26, 19, 26], fill=(130, 60, 55))
        if fever:
            for (x, y) in ((5, 8), (25, 9), (6, 20)):
                d.rectangle([x, y, x + 1, y + 2], fill=(200, 225, 240))
    return tex_draw(name, fn)


make_face_onebad('gage_b', SKIN_G)
make_face_onebad('gage_b_smile', SKIN_G, 'smile')
make_face_onebad('gage_b_shout', SKIN_G, 'shout')
make_face_onebad('gage_b_fever', (215, 190, 170), 'open', fever=True)
make_face('worker1', skin=(225, 180, 145), brow_col=(140, 70, 40), mustache=True, hair_col=(150, 75, 40))
make_face('worker1_shock', skin=(225, 180, 145), brow_col=(140, 70, 40), mustache=True, hair_col=(150, 75, 40), mouth='open')
make_face('worker2', skin=(215, 170, 135), brow_col=(50, 40, 30), beard=True, hair_col=(50, 40, 30))
make_face('worker2_shock', skin=(215, 170, 135), brow_col=(50, 40, 30), beard=True, hair_col=(50, 40, 30), mouth='open')
make_face('doctor', skin=(232, 195, 165), brow_col=(120, 110, 100), beard=True, hair_col=(130, 120, 110))
make_face('doctor_shock', skin=(232, 195, 165), brow_col=(120, 110, 100), beard=True, hair_col=(130, 120, 110), mouth='open')
make_face('harlow', skin=(232, 195, 165), brow_col=(70, 55, 40), mustache=True, hair_col=(70, 55, 40))


def gage(face='gage', hat=True, bandage=False, coat=False, ragged=False):
    def ex(P, at):
        ms = []
        if bandage:
            h = at['head']
            ms.append(box(0.27, 0.09, 0.27, (248, 248, 244)).xf(M(h, trans(0, 0.21, 0))))                 # bande sur le haut du crâne
            ms.append(box(0.34, 0.045, 0.275, (248, 248, 244)).xf(M(h, trans(0.02, 0.19, 0), rotz(-0.42))))  # sangle en diagonale
            ms.append(box(0.085, 0.075, 0.02, (248, 248, 244)).xf(M(h, trans(0.065, 0.155, 0.128))))     # pansement sur l'œil gauche seulement
        return merge(ms)
    if ragged:
        return Human(face, skin=SKIN_G, shirt=(95, 85, 70), pants=(70, 62, 52), hair=HAIR_G, hat='flatcap' if hat else None,
                     hat_col=(60, 55, 48), shirt_tex='rag', pants_tex='rag', extra=ex)
    if coat:
        return Human(face, skin=SKIN_G, shirt=(230, 228, 218), pants=(50, 45, 42), hair=HAIR_G, hat='bowler' if hat else None,
                     hat_col=(35, 30, 28), jacket=(60, 45, 35), tie=(30, 30, 30), extra=ex)
    return Human(face, skin=SKIN_G, shirt=(228, 225, 212), pants=(70, 62, 52), hair=HAIR_G, hat='bowler' if hat else None,
                 hat_col=(40, 34, 30), shirt_tex='shirt_w', belt=(50, 35, 25), extra=merge_extra(vest_extra, ex))


def merge_extra(*fs):
    def f(P, at):
        return merge([g(P, at) for g in fs])
    return f


def vest_extra(P, at):
    t = at['torso']
    return merge([box(0.44, 0.42, 0.26, (60, 50, 40), 'vest', faces='blrud').xf(M(t, trans(0, 0.12, 0))),
                  box(0.12, 0.42, 0.26, (60, 50, 40), 'vest', faces='f').xf(M(t, trans(-0.15, 0.12, 0))),
                  box(0.12, 0.42, 0.26, (60, 50, 40), 'vest', faces='f').xf(M(t, trans(0.15, 0.12, 0)))])


def worker(i=0, face=None):
    if i % 2 == 0:
        return Human(face or 'worker1', skin=(225, 180, 145), shirt=(150, 60, 50), pants=(70, 70, 85), hair=(150, 75, 40),
                     hat='flatcap', hat_col=(80, 70, 55), sleeves='long')
    return Human(face or 'worker2', skin=(215, 170, 135), shirt=(110, 120, 140), pants=(80, 65, 50), hair=(50, 40, 30),
                 hat='bowler', hat_col=(50, 45, 40), belt=(50, 35, 25))


def doctor(face='doctor'):
    return Human(face, skin=(232, 195, 165), shirt=(235, 235, 230), pants=(30, 28, 28), hair=(130, 120, 110),
                 hat='bowler', hat_col=(25, 22, 22), jacket=(35, 32, 32), tie=(20, 20, 20))


def harlow(face='harlow'):
    return Human(face, skin=(232, 195, 165), shirt=(235, 235, 230), pants=(40, 38, 36), hair=(70, 55, 40), jacket=(50, 45, 42), tie=(120, 30, 30))


# ---------------------------------------------------------------- objets
def tamping_iron(L=1.1, r=0.016):
    """barre à bourrer : 1,10 m, pointe effilée sur 30 cm (axe +y, base y=0)"""
    return merge([cyl(r, r, L - 0.3, 6, (175, 175, 180), 'metal'), cyl(r, 0.003, 0.3, 6, (175, 175, 180), 'metal').xf(trans(0, L - 0.3, 0))])


IRON = tamping_iron()


def iron_glow():
    return merge([cyl(0.045, 0.045, 0.8, 6, (255, 140, 40), emis=1.0), cyl(0.045, 0.01, 0.3, 6, (255, 140, 40), emis=1.0).xf(trans(0, 0.8, 0))])


def sledge():
    return merge([cyl(0.02, 0.02, 0.8, 5, (130, 95, 60)), box(0.18, 0.08, 0.08, (60, 60, 65), 'metal').xf(trans(0, 0.8, 0))])


def drill_bit():
    return cyl(0.015, 0.015, 0.7, 5, (110, 110, 115), 'metal')


def powder_flask():
    return merge([sphere(0.09, 7, 4, (110, 75, 40), sy=1.2), cyl(0.015, 0.012, 0.12, 5, (180, 150, 70)).xf(trans(0, 0.1, 0))])


def bucket():
    return merge([cyl(0.15, 0.17, 0.3, 8, (120, 90, 60), 'planks_v', caps=False), cyl(0.15, 0.15, 0.02, 8, (190, 170, 130), 'sand').xf(trans(0, 0.22, 0))])


def skull_mesh(col=(160, 230, 255), alpha=0.9, emis=0.9):
    """crâne stylisé façon radiographie (face vers +z)"""
    c = C(col)
    ms = [sphere(0.11, 10, 7, c, sy=1.0).xf(M(trans(0, 0.04, -0.01), scale(0.95, 1.05, 1.15))),
          box(0.15, 0.08, 0.1, c).xf(trans(0, -0.07, 0.05)),
          box(0.12, 0.04, 0.07, c).xf(trans(0, -0.12, 0.06))]
    for s in (-1, 1):
        ms.append(box(0.045, 0.035, 0.02, (10, 30, 50), emis=1.0).xf(trans(s * 0.042, 0.0, 0.118)))
        ms.append(box(0.03, 0.05, 0.08, c).xf(trans(s * 0.07, -0.06, 0.03)))   # pommettes
    ms.append(box(0.025, 0.03, 0.02, (10, 30, 50), emis=1.0).xf(trans(0, -0.045, 0.125)))
    for k in range(6):
        ms.append(box(0.012, 0.018, 0.01, (230, 250, 255), emis=1.0).xf(trans(-0.03 + k * 0.012, -0.098, 0.105)))
    out = merge(ms)
    out.alpha[:] = alpha
    out.emis[:] = emis
    return out


SKULL_X = skull_mesh()
SKULL_BONE = skull_mesh((225, 215, 190), 1.0, 0.0)


def iron_path():
    """entrée sous la pommette gauche, derrière l'œil, sortie au sommet (repère du crâne, gauche du personnage = +x)"""
    a = np.array([0.055, -0.075, 0.07])
    b = np.array([0.0, 0.16, -0.02])
    return a, b


def ox(phase=0.0, col=(255, 255, 255)):
    F = 'fur_ox'
    ms = [box(0.7, 0.7, 1.6, col, F).xf(trans(0, 0.75, 0)), sphere(0.4, 7, 4, col, F).xf(M(trans(0, 1.35, 0.55), scale(0.9, 0.6, 0.8)))]
    head = M(trans(0, 1.15, 0.95), rotx(0.4))
    ms.append(box(0.32, 0.38, 0.5, col, F).xf(M(head, trans(0, -0.15, 0.1))))
    ms.append(box(0.24, 0.18, 0.12, (70, 50, 40)).xf(M(head, trans(0, -0.18, 0.38))))
    for s in (-1, 1):
        ms.append(box(0.5, 0.06, 0.06, (230, 220, 190)).xf(M(head, trans(s * 0.32, 0.15, 0.1), rotz(s * 0.4))))
        ms.append(box(0.04, 0.04, 0.02, (15, 12, 10)).xf(M(head, trans(s * 0.12, 0.0, 0.36))))
    for (x, z, ph) in ((-0.25, 0.65, 0), (0.25, 0.65, math.pi), (-0.25, -0.65, math.pi), (0.25, -0.65, 0)):
        lg = M(trans(x, 0.8, z), rotx(0.35 * math.sin(phase + ph)))
        ms.append(box(0.16, 0.8, 0.18, col, F).xf(M(lg, trans(0, -0.8, 0))))
        ms.append(box(0.17, 0.08, 0.2, (30, 25, 20)).xf(M(lg, trans(0, -0.82, 0.01))))
    return merge(ms)


def cart(wheel_rot=0.0):
    """charrette à bœufs, timon vers +z ; plateau à y=0.97"""
    ms = [box(1.4, 0.12, 2.2, (150, 110, 70), 'planks', ts=0.6).xf(trans(0, 0.85, 0))]
    for s in (-1, 1):
        ms.append(box(0.08, 0.45, 2.2, (140, 100, 62), 'planks', ts=0.6).xf(trans(s * 0.68, 0.97, 0)))
        ms.append(wheel(0.75).xf(M(trans(s * 0.85, 0.75, -0.2), rotz(math.pi / 2), roty(wheel_rot))))
    ms.append(box(1.4, 0.45, 0.08, (140, 100, 62), 'planks', ts=0.6).xf(trans(0, 0.97, -1.08)))
    ms.append(box(0.12, 0.12, 2.6, (130, 95, 60)).xf(trans(0, 0.85, 2.3)))
    ms.append(box(1.6, 0.1, 0.12, (130, 95, 60)).xf(trans(0, 1.45, 3.15)))
    return merge(ms)


def stagecoach(wheel_rot=0.0):
    """diligence (mail coach), timon vers +z"""
    ms = [box(1.7, 1.4, 2.4, (150, 40, 35), 'maroon' if 'maroon' in TEXB else 0).xf(trans(0, 1.1, 0))]
    ms.append(box(1.8, 0.1, 2.6, (40, 30, 25)).xf(trans(0, 2.5, 0)))
    for s in (-1, 1):
        ms.append(box(0.02, 0.5, 0.8, (60, 70, 80)).xf(trans(s * 0.86, 1.7, 0)))
        ms.append(box(0.03, 0.06, 2.4, (200, 170, 70)).xf(trans(s * 0.86, 1.15, 0)))
        for z in (-0.9, 0.9):
            ms.append(wheel(0.65 if z > 0 else 0.8).xf(M(trans(s * 0.95, 0.65 if z > 0 else 0.8, z), rotz(math.pi / 2), roty(wheel_rot))))
    # siège du cocher en hauteur à l'avant
    ms.append(box(1.4, 0.1, 0.5, (90, 60, 40)).xf(trans(0, 2.2, 1.45)))
    ms.append(box(1.4, 0.5, 0.08, (90, 60, 40)).xf(trans(0, 2.3, 1.2)))
    ms.append(box(1.2, 0.08, 0.6, (90, 60, 40)).xf(trans(0, 1.6, 1.95)))
    # malles sur le toit
    ms.append(box(1.2, 0.4, 1.4, (110, 80, 50), 'planks').xf(trans(0, 2.6, -0.3)))
    ms.append(box(0.1, 0.1, 3.4, (110, 80, 55)).xf(trans(0, 0.9, 3.2)))
    return merge(ms)


def hills(seed=0, cz=-160, w=700, col=(255, 255, 255), tex='grass', n=12, hmin=30, hmax=70):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        x = -w / 2 + i * w / n + rr.uniform(-20, 20)
        r = rr.uniform(60, 110)
        ms.append(sphere(r, 9, 5, col, tex, sy=rr.uniform(hmin, hmax) / r).xf(trans(x, -5, cz + rr.uniform(-30, 30))))
    return merge(ms)


def forest(x0, z0, x1, z1, n=40, seed=0, avoid=None):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        x, z = rr.uniform(x0, x1), rr.uniform(z0, z1)
        if avoid and avoid(x, z):
            continue
        if rr.random() < 0.55:
            ms.append(pine(rr.uniform(6, 11), rr.uniform(1.6, 2.4), i).xf(trans(x, 0, z)))
        else:
            ms.append(deciduous(rr.uniform(6, 9), rr.uniform(2.2, 3.0), i).xf(trans(x, 0, z)))
    return merge(ms)


def rail_cut():
    """chantier : tranchée dans la roche (paroi au fond z<-4), sol rocheux, plateforme de travail"""
    ms = [grid(-60, -60, 60, 60, 10, 10, None, (255, 255, 255), 'dirt', 3.0)]
    ms.append(box(40, 0.25, 8, (150, 145, 135), 'ledge', ts=2.0).xf(trans(0, -0.2, -1)))   # dalle de roche
    for i in range(7):
        rk = rock(1.0, 60 + i, (255, 255, 255), 'ledge')
        rk.uv = rk.uv * 5.0
        ms.append(rk.xf(M(trans(-18 + i * 6, 0, -6.5), scale(4.5, 5.5, 3))))
    ms.append(box(60, 7, 3, (140, 135, 125), 'ledge', ts=2.5).xf(trans(0, 0, -9)))
    # traverses empilées, brouettes, piquets
    for k in range(5):
        ms.append(box(2.4, 0.18, 0.22, (110, 80, 55)).xf(trans(9, k * 0.18, 2.5 + (k % 2) * 0.05)))
    for x in (-8, 12):
        ms.append(box(0.6, 0.35, 1.0, (120, 90, 60), 'planks').xf(trans(x, 0.3, 3.5)))
        ms.append(wheel(0.25, 0.06, 6).xf(M(trans(x, 0.25, 4.1), rotz(math.pi / 2))))
    for x in np.arange(-25, 26, 5):
        ms.append(box(0.08, 1.0, 0.08, (180, 150, 100)).xf(trans(x, 0, 6)))
    return merge(ms)


HOLE = np.array([0.0, 0.05, 0.0])


def blast_hole():
    return merge([cyl(0.05, 0.05, 0.02, 8, (10, 10, 10)).xf(trans(HOLE)), cyl(0.12, 0.12, 0.01, 8, (90, 85, 80)).xf(trans(HOLE - np.array([0, 0.005, 0])))])


def hotel():
    """hôtel de Cavendish : maison à étage, véranda (piazza) devant (+z)"""
    ms = [box(12, 6.5, 8, (240, 236, 225), 'planks_white', ts=1.0)]
    rt = [[(-6.4, 6.5, 4.4), (6.4, 6.5, 4.4), (6.4, 9.5, 0)], [(-6.4, 6.5, 4.4), (6.4, 9.5, 0), (-6.4, 9.5, 0)],
          [(6.4, 6.5, -4.4), (-6.4, 6.5, -4.4), (-6.4, 9.5, 0)], [(6.4, 6.5, -4.4), (-6.4, 9.5, 0), (6.4, 9.5, 0)]]
    ms.append(Mesh(rt, C((90, 90, 95)), [[(0, 1), (6, 1), (6, 0)], [(0, 1), (6, 0), (0, 0)]] * 2, TEXB['roof_tin']))
    for s in (-1, 1):
        ms.append(Mesh([[(s * 6, 6.5, 4.0), (s * 6, 6.5, -4.0), (s * 6, 9.5, 0)]], C((240, 236, 225)), [[(0, 1), (2, 1), (1, 0)]], TEXB['planks_white']))
    for x in (-4, -1.5, 1.5, 4):
        for y in (1.0, 4.0):
            ms.append(box(1.0, 1.4, 0.06, (255, 255, 255), 'window').xf(trans(x, y, 4.02)))
    ms.append(box(1.2, 2.2, 0.06, (255, 255, 255), 'door').xf(trans(0, 0.3, 4.02)))
    # véranda
    ms.append(box(12.4, 0.3, 3.0, (170, 140, 100), 'planks', ts=0.8).xf(trans(0, 0, 5.5)))
    ms.append(box(12.8, 0.15, 3.4, (120, 120, 120), 'roof_tin').xf(trans(0, 3.2, 5.6)))
    for x in np.linspace(-6, 6, 6):
        ms.append(box(0.15, 2.9, 0.15, (240, 236, 225)).xf(trans(x, 0.3, 6.85)))
    ms.append(box(2.4, 0.6, 0.06, (255, 255, 255), 'hotel_sign').xf(trans(0, 3.4, 7.3)))
    return merge(ms)


def chair():
    ms = [box(0.45, 0.05, 0.45, (110, 75, 45)).xf(trans(0, 0.45, 0)), box(0.45, 0.55, 0.05, (110, 75, 45)).xf(trans(0, 0.5, -0.2))]
    for x in (-0.2, 0.2):
        for z in (-0.2, 0.2):
            ms.append(box(0.04, 0.45, 0.04, (90, 60, 35)).xf(trans(x, 0, z)))
    return merge(ms)


def bedroom():
    ms = [box(6, 0.05, 5, (130, 95, 60), 'planks', ts=0.7).xf(trans(0, -0.05, 0)),
          box(6, 2.8, 0.1, (255, 255, 255), 'wallboard', ts=1.0).xf(trans(0, 0, -2.5)),
          box(0.1, 2.8, 5, (255, 255, 255), 'wallboard', ts=1.0).xf(trans(-3, 0, 0))]
    # lit (tête contre le mur du fond, oreiller à z=-2)
    ms.append(box(1.2, 0.45, 2.1, (110, 75, 45), 'planks').xf(trans(0, 0, -1.3)))
    ms.append(box(1.1, 0.15, 2.0, (235, 230, 215), 'cloth').xf(trans(0, 0.45, -1.3)))
    ms.append(box(1.25, 1.1, 0.08, (110, 75, 45), 'planks').xf(trans(0, 0, -2.35)))
    ms.append(box(0.6, 0.12, 0.35, (245, 245, 240)).xf(trans(0, 0.6, -2.05)))
    # table de nuit, bougie, bassine
    ms.append(box(0.5, 0.7, 0.4, (100, 70, 40), 'planks_v').xf(trans(1.0, 0, -2.0)))
    ms.append(cyl(0.04, 0.04, 0.15, 6, (240, 235, 210)).xf(trans(0.95, 0.7, -2.05)))
    ms.append(box(0.04, 0.06, 0.04, (255, 200, 90), emis=1.0).xf(trans(0.95, 0.88, -2.05)))
    ms.append(cyl(0.16, 0.12, 0.08, 8, (200, 200, 205), 'metal').xf(trans(1.1, 0.7, -1.9)))
    ms.append(box(0.8, 1.0, 0.04, (255, 255, 255), 'window').xf(trans(-1.6, 1.2, -2.44)))
    return merge(ms)


def saloon():
    ms = [box(10, 0.05, 8, (120, 85, 55), 'planks', ts=0.7).xf(trans(0, -0.05, 0)),
          box(10, 3.2, 0.1, (255, 255, 255), 'planks_v', ts=1.0).xf(trans(0, 0, -3.5))]
    ms.append(box(6, 1.1, 0.7, (90, 55, 35), 'planks_v').xf(trans(0, 0, -2.6)))
    ms.append(box(6.2, 0.08, 0.8, (70, 45, 30)).xf(trans(0, 1.1, -2.6)))
    for i in range(10):
        ms.append(cyl(0.05, 0.05, 0.25, 6, (60, 110, 60) if i % 2 else (130, 70, 40), alpha=0.85).xf(trans(-2.5 + i * 0.55, 1.6, -3.3)))
    ms.append(box(6, 0.05, 0.3, (90, 60, 40)).xf(trans(0, 1.55, -3.3)))
    for x in (-3, 2.5):
        ms.append(cyl(0.45, 0.45, 0.05, 8, (100, 70, 45)).xf(trans(x, 0.75, 0.5)))
        ms.append(cyl(0.05, 0.05, 0.75, 5, (80, 55, 35)).xf(trans(x, 0, 0.5)))
    for x in (-3.5, 3.5):
        ms.append(box(0.3, 0.4, 0.3, (255, 210, 120), emis=0.8).xf(trans(x, 2.4, -3.3)))
    return merge(ms)


def bottle():
    return merge([cyl(0.04, 0.04, 0.2, 6, (60, 100, 50), alpha=0.9), cyl(0.04, 0.015, 0.06, 6, (60, 100, 50)).xf(trans(0, 0.2, 0)),
                  cyl(0.016, 0.016, 0.06, 5, (60, 100, 50)).xf(trans(0, 0.26, 0))])


def desk_scene():
    ms = [box(3, 0.08, 1.5, (90, 60, 35), 'planks').xf(trans(0, 0.8, 0)),
          box(8, 0.05, 8, (110, 80, 55), 'planks').xf(trans(0, -0.05, 0)),
          box(8, 3.5, 0.1, (255, 255, 255), 'wallboard').xf(trans(0, 0, -1.5))]
    ms.append(cyl(0.03, 0.03, 0.12, 6, (240, 235, 210)).xf(trans(0.9, 0.88, -0.3)))
    ms.append(box(0.03, 0.05, 0.03, (255, 200, 90), emis=1.0).xf(trans(0.9, 1.02, -0.3)))
    ms.append(cyl(0.04, 0.04, 0.08, 6, (30, 30, 50)).xf(trans(-0.8, 0.88, -0.2)))
    return merge(ms)


def book(open_=0.0):
    """livre (1868) : couverture rouge, s'ouvre (open_ 0..1)"""
    ms = [box(0.24, 0.035, 0.32, (255, 255, 255), 'book_cover')]
    if open_ > 0:
        ms.append(box(0.46, 0.01, 0.32, (255, 255, 255), 'pages').xf(trans(0.11, 0.035, 0)))
    return merge(ms)


def andes(seed=0):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(14):
        x = -500 + i * 75 + rr.uniform(-20, 20)
        h = rr.uniform(140, 260)
        z = -420 + rr.uniform(-60, 60)
        ms.append(cyl(rr.uniform(70, 110), 0, h, 6, (140, 125, 110), 'andes').xf(M(trans(x, 0, z), roty(rr.random()))))
        ms.append(cyl(rr.uniform(70, 110) * 0.28, 0, h * 0.28, 6, (245, 245, 250)).xf(M(trans(x, h * 0.72, z), roty(rr.random()))) if h > 180 else Mesh())
    return merge(ms)


def chile_road():
    ms = [grid(-200, -200, 200, 200, 8, 8, None, (255, 255, 255), 'dust', 4.0)]
    ms.append(box(6, 0.02, 400, (200, 175, 135), 'dust', ts=3).xf(trans(0, 0.01, 0)))
    rr = np.random.default_rng(3)
    for i in range(40):
        x = rr.uniform(-120, 120)
        if abs(x) < 6:
            x += 12 * np.sign(x)
        z = rr.uniform(-200, 200)
        if rr.random() < 0.5:
            ms.append(rock(rr.uniform(0.6, 2.0), i, (255, 255, 255), 'rock').xf(trans(x, 0, z)))
        else:
            ms.append(sphere(rr.uniform(0.6, 1.2), 6, 3, (110, 120, 60), 'scrub' if 'scrub' in TEXB else 'leaves', sy=0.7).xf(trans(x, 0.3, z)))
    return merge(ms)


def museum_case():
    ms = [box(10, 0.05, 10, (60, 45, 35), 'planks').xf(trans(0, -0.05, 0)),
          box(10, 4, 0.1, (70, 60, 55)).xf(trans(0, 0, -2.5))]
    ms.append(box(1.4, 0.9, 0.7, (60, 40, 30), 'planks_v').xf(trans(0, 0, 0)))
    ms.append(box(1.35, 0.8, 0.65, (200, 225, 235), alpha=0.22).xf(trans(0, 0.9, 0)))
    ms.append(box(1.4, 0.04, 0.7, (60, 40, 30)).xf(trans(0, 1.7, 0)))
    ms.append(box(0.9, 0.03, 0.25, (200, 190, 160)).xf(trans(0, 0.9, 0.18)))
    return merge(ms)


def frame_portrait(d, n):
    d.rectangle([0, 0, n, n], fill=(60, 40, 25))


ENV_DAY = Env(sky_top=(80, 130, 200), sky_hor=(205, 215, 215), fog=(185, 200, 205), fog_near=60, fog_far=450,
              light=(-0.45, 0.8, 0.4), amb=0.55, light_col=(255, 245, 225))
ENV_EVE = Env(sky_top=(70, 80, 140), sky_hor=(240, 170, 110), fog=(210, 160, 120), fog_near=40, fog_far=380,
              light=(-0.7, 0.4, 0.4), amb=0.5, light_col=(255, 200, 150))
ENV_ROOM = Env(sky_top=(30, 25, 22), sky_hor=(30, 25, 22), fog=(20, 16, 14), fog_near=5, fog_far=25,
               light=(0.4, 0.7, 0.6), amb=0.45, light_col=(255, 210, 160))
ENV_XRAY = Env(sky_top=(4, 12, 30), sky_hor=(10, 30, 60), fog=(6, 18, 40), fog_near=3, fog_far=12,
               light=(0.3, 0.8, 0.5), amb=0.6, light_col=(200, 230, 255))
ENV_CHILE = Env(sky_top=(50, 110, 200), sky_hor=(215, 210, 195), fog=(205, 195, 175), fog_near=100, fog_far=900,
                light=(0.5, 0.75, 0.4), amb=0.55, light_col=(255, 240, 215))
ENV_NIGHT = Env(sky_top=(10, 12, 25), sky_hor=(30, 32, 48), fog=(22, 24, 36), fog_near=8, fog_far=60,
                light=(0.3, 0.8, 0.5), amb=0.45, light_col=(150, 160, 200))
ENV_MUSEUM = Env(sky_top=(25, 20, 18), sky_hor=(25, 20, 18), fog=(18, 14, 12), fog_near=5, fog_far=22,
                 light=(0.2, 0.9, 0.4), amb=0.45, light_col=(255, 230, 190))
ENV_SUNSET = Env(sky_top=(60, 60, 120), sky_hor=(250, 150, 80), fog=(230, 150, 100), fog_near=60, fog_far=600,
                 light=(-0.8, 0.25, 0.4), amb=0.5, light_col=(255, 180, 120))
