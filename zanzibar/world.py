"""Décors et personnages : guerre anglo-zanzibarienne, 27 août 1896."""
import sys, math
sys.path.insert(0, '/home/claude/g2n')
import numpy as np
from lib import *

build_base_textures()

tex_noise('white_robe', (225, 222, 210), (242, 240, 230), seed=61, octaves=1)
tex_noise('bisht', (30, 28, 30), (45, 40, 42), seed=62, octaves=1)
tex_noise('navy_whites', (230, 230, 225), (245, 245, 240), seed=63, octaves=1)
tex_noise('hull_black', (25, 25, 28), (38, 38, 42), seed=64, octaves=1)
tex_noise('deck', (170, 140, 100), (195, 165, 120), seed=65, octaves=1)
tex_planks('deck_planks', (200, 170, 125), (165, 135, 95), seed=7)
tex_noise('red_cloth', (160, 25, 25), (190, 35, 30), seed=66, octaves=1)
tex_noise('wood_dark', (80, 55, 35), (100, 70, 45), seed=67, octaves=2)
tex_noise('ochre', (200, 165, 115), (225, 190, 140), seed=68, octaves=4, speck=0.08)
tex_noise('scorch', (40, 35, 32), (70, 62, 55), seed=69, octaves=3, speck=0.1, speck_col=(20, 18, 16))
tex_noise('land', (90, 120, 60), (120, 150, 75), seed=70, octaves=4, speck=0.1)
tex_noise('sacking', (170, 150, 110), (195, 175, 130), seed=47, octaves=1, speck=0.2)
tex_noise('ocean', (25, 90, 130), (40, 115, 150), seed=71, octaves=3, speck=0.02, speck_col=(200, 230, 240))


def flags():
    def uj(d, n):
        d.rectangle([0, 0, n, n], fill=(20, 40, 110))
        d.line([0, 0, n, n], fill=(240, 240, 240), width=6)
        d.line([0, n, n, 0], fill=(240, 240, 240), width=6)
        d.line([0, 0, n, n], fill=(200, 30, 40), width=2)
        d.line([0, n, n, 0], fill=(200, 30, 40), width=2)
        d.rectangle([n // 2 - 5, 0, n // 2 + 4, n], fill=(240, 240, 240))
        d.rectangle([0, n // 2 - 5, n, n // 2 + 4], fill=(240, 240, 240))
        d.rectangle([n // 2 - 3, 0, n // 2 + 2, n], fill=(200, 30, 40))
        d.rectangle([0, n // 2 - 3, n, n // 2 + 2], fill=(200, 30, 40))
    tex_draw('union_jack', uj)

    def ensign(d, n):
        d.rectangle([0, 0, n, n], fill=(240, 240, 240))
        d.rectangle([n // 2 - 2, 0, n // 2 + 2, n], fill=(200, 30, 40))
        d.rectangle([0, n // 2 - 2, n, n // 2 + 2], fill=(200, 30, 40))
        d.rectangle([0, 0, n // 2 - 4, n // 2 - 4], fill=(20, 40, 110))
        d.line([0, 0, n // 2 - 4, n // 2 - 4], fill=(240, 240, 240), width=2)
        d.line([0, n // 2 - 4, n // 2 - 4, 0], fill=(240, 240, 240), width=2)
        d.rectangle([n // 4 - 3, 0, n // 4, n // 2 - 4], fill=(200, 30, 40))
        d.rectangle([0, n // 4 - 3, n // 2 - 4, n // 4], fill=(200, 30, 40))
    tex_draw('white_ensign', ensign)

    def ger(d, n):
        d.rectangle([0, 0, n, n // 3], fill=(20, 20, 20))
        d.rectangle([0, n // 3, n, 2 * n // 3], fill=(240, 240, 240))
        d.rectangle([0, 2 * n // 3, n, n], fill=(200, 30, 30))
    tex_draw('german_flag', ger)

    def clock(d, n):
        d.ellipse([0, 0, n - 1, n - 1], fill=(240, 235, 215))
        d.ellipse([0, 0, n - 1, n - 1], outline=(40, 40, 40), width=2)
        for k in range(12):
            a = k / 12 * 2 * math.pi
            x0, y0 = n / 2 + math.sin(a) * n * 0.36, n / 2 - math.cos(a) * n * 0.36
            x1, y1 = n / 2 + math.sin(a) * n * 0.44, n / 2 - math.cos(a) * n * 0.44
            d.line([x0, y0, x1, y1], fill=(30, 30, 30), width=2 if k % 3 == 0 else 1)
    tex_draw('clock_face', clock, bg=(255, 0, 255))

    def shutter(d, n):
        d.rectangle([0, 0, n, n], fill=(40, 30, 25))
        d.rectangle([3, 2, n // 2 - 1, n - 3], fill=(60, 110, 85))
        d.rectangle([n // 2 + 1, 2, n - 4, n - 3], fill=(60, 110, 85))
        for y in range(5, n - 4, 3):
            d.line([4, y, n // 2 - 2, y], fill=(40, 80, 60))
            d.line([n // 2 + 2, y, n - 5, y], fill=(40, 80, 60))
    tex_draw('shutter', shutter)

    def carved_door(d, n):
        d.rectangle([0, 0, n, n], fill=(70, 45, 25))
        d.rectangle([3, 3, n - 4, n - 1], fill=(95, 62, 35))
        d.line([n // 2, 3, n // 2, n], fill=(55, 35, 20))
        for y in range(6, n, 6):
            for x in (6, n - 8):
                d.rectangle([x, y, x + 2, y + 2], fill=(200, 170, 80))
        d.arc([3, -8, n - 4, 14], 0, 180, fill=(55, 35, 20))
    tex_draw('carved_door', carved_door)

    def letter(d, n):
        d.rectangle([0, 0, n, n], fill=(235, 225, 195))
        for y in range(5, n - 8, 3):
            d.line([4, y, n - 5 - (y * 7 % 9), y], fill=(70, 60, 50))
        d.ellipse([n - 12, n - 11, n - 4, n - 3], fill=(160, 20, 20))
    tex_draw('letter', letter)

    def ledger(d, n):
        d.rectangle([0, 0, n, n], fill=(230, 222, 195))
        d.line([n // 2, 0, n // 2, n], fill=(150, 130, 100))
        for y in range(4, n, 3):
            d.line([3, y, n // 2 - 3, y], fill=(80, 70, 60))
            d.line([n // 2 + 3, y, n - 3 - (y * 5 % 7), y], fill=(80, 70, 60))
    tex_draw('ledger', ledger)

    def rug(d, n):
        d.rectangle([0, 0, n, n], fill=(140, 30, 35))
        d.rectangle([3, 3, n - 4, n - 4], outline=(210, 170, 70), width=2)
        d.polygon([(n // 2, 8), (n - 9, n // 2), (n // 2, n - 9), (9, n // 2)], fill=(30, 50, 100))
        d.polygon([(n // 2, 12), (n - 13, n // 2), (n // 2, n - 13), (13, n // 2)], fill=(210, 170, 70))
    tex_draw('rug', rug)


flags()


def _ultimatum(d, n):
    d.rectangle([0, 0, n, n], fill=(238, 230, 205))
    d.rectangle([n // 2 - 4, 1, n // 2 + 3, 7], fill=(170, 30, 30))      # armoiries de la Couronne
    d.rectangle([n // 2 - 2, 2, n // 2 + 1, 5], fill=(210, 170, 60))
    for y in range(10, n - 8, 3):
        d.line([4, y, n - 5 - (y * 7 % 9), y], fill=(60, 50, 45))
    d.line([n - 14, n - 6, n - 5, n - 7], fill=(30, 30, 60))
    d.ellipse([4, n - 9, 11, n - 2], fill=(160, 20, 20))


def _facture(d, n):
    d.rectangle([0, 0, n, n], fill=(238, 230, 205))
    d.rectangle([n // 2 - 4, 1, n // 2 + 3, 7], fill=(170, 30, 30))
    for y in range(10, n - 6, 3):
        d.line([4, y, n // 2, y], fill=(60, 50, 45))
        d.line([n - 10, y, n - 4, y], fill=(60, 50, 45))
    d.line([4, n - 5, n - 4, n - 5], fill=(30, 30, 30), width=2)


tex_draw('ultimatum', _ultimatum)
tex_draw('facture', _facture)

# ---------------------------------------------------------------- visages
make_face('khalid', skin=(180, 130, 95), brow_col=(25, 20, 15), beard=True, hair_col=(25, 20, 15), eye_col=(30, 20, 15))
make_face('khalid_angry', skin=(180, 130, 95), brow_col=(25, 20, 15), beard=True, hair_col=(25, 20, 15), eye_col=(30, 20, 15), mouth='open')
make_face('khalid_shout', skin=(180, 130, 95), brow_col=(25, 20, 15), beard=True, hair_col=(25, 20, 15), eye_col=(30, 20, 15), mouth='shout')
make_face('sultan', skin=(175, 128, 95), brow_col=(200, 200, 200), beard=True, hair_col=(210, 210, 205), eyes_closed=True)
make_face('cave', skin=(235, 200, 175), brow_col=(140, 110, 80), mustache=True, hair_col=(140, 110, 80))
make_face('cave_angry', skin=(235, 200, 175), brow_col=(140, 110, 80), mustache=True, hair_col=(140, 110, 80), mouth='open')
make_face('sailor', skin=(232, 190, 160), brow_col=(110, 80, 50))
make_face('sailor_ow', skin=(232, 190, 160), brow_col=(110, 80, 50), mouth='open')
make_face('askari', skin=(95, 62, 42), brow_col=(20, 15, 10), eye_col=(25, 18, 12))
make_face('askari2', skin=(110, 72, 50), brow_col=(20, 15, 10), eye_col=(25, 18, 12), mustache=True, hair_col=(20, 15, 10))
make_face('civil', skin=(120, 82, 58), brow_col=(20, 15, 10), eye_col=(25, 18, 12), beard=True, hair_col=(30, 25, 20))
make_face('servant', skin=(105, 70, 50), brow_col=(20, 15, 10), eye_col=(25, 18, 12))


def kofia_guard_extra(P, at):
    return Mesh()


def rifle():
    return merge([box(0.04, 0.04, 1.1, (90, 60, 35)).xf(trans(0, 0, 0.1)), box(0.02, 0.02, 0.5, (60, 60, 65)).xf(trans(0, 0.03, 0.6))])


def khalid(face='khalid'):
    def bisht(P, at):
        t = at['torso']
        return merge([box(0.5, 1.15, 0.3, (40, 36, 38), 'bisht', faces='blrud').xf(M(t, trans(0, -0.6, -0.01))),
                      box(0.1, 0.55, 0.02, (200, 160, 60)).xf(M(t, trans(-0.12, 0.0, 0.15))),
                      box(0.1, 0.55, 0.02, (200, 160, 60)).xf(M(t, trans(0.12, 0.0, 0.15))),
                      box(0.06, 0.2, 0.06, (200, 160, 60)).xf(M(t, trans(0, -0.05, 0.14), rotz(0.3)))])  # khanjar
    return Human(face, skin=(180, 130, 95), shirt=(235, 232, 220), pants=(235, 232, 220), robe=(235, 232, 220),
                 hair=(25, 20, 15), hat='turban', hat_col=(240, 238, 225), shirt_tex='white_robe', extra=bisht)


def sultan():
    return Human('sultan', skin=(175, 128, 95), shirt=(235, 232, 220), pants=(235, 232, 220), hair=(210, 210, 205),
                 hat='turban', hat_col=(240, 238, 225))


def askari(face='askari', coat=(170, 40, 35)):
    return Human(face, skin=(95, 62, 42) if face == 'askari' else (110, 72, 50), shirt=coat, pants=(235, 232, 220),
                 robe=(235, 232, 220), hair=(20, 15, 10), hat='kofia', hat_col=(170, 30, 30), belt=(60, 40, 25))


def civilian(face='civil', col=(235, 232, 220)):
    return Human(face, skin=(120, 82, 58), shirt=col, pants=col, robe=col, hair=(30, 25, 20), hat='kofia', hat_col=(240, 238, 228),
                 shirt_tex='white_robe')


def consul(face='cave'):
    return Human(face, skin=(235, 200, 175), shirt=(240, 240, 235), pants=(240, 240, 235), hair=(140, 110, 80),
                 hat='pith', hat_col=(240, 238, 228), jacket=(238, 236, 228), tie=(30, 30, 40), belt=(120, 90, 50))


def sailor(face='sailor'):
    return Human(face, skin=(232, 190, 160), shirt=(240, 240, 238), pants=(240, 240, 238), hair=(110, 80, 50),
                 hat='sailor', hat_col=(240, 240, 238), shirt_tex='navy_whites', tie=(20, 30, 70))


def servant():
    return Human('servant', skin=(105, 70, 50), shirt=(235, 232, 220), pants=(235, 232, 220), robe=(235, 232, 220),
                 hair=(20, 15, 10), hat='kofia', hat_col=(240, 238, 228))


# ---------------------------------------------------------------- bâtiments
def flag(tex, w=2.0, h=1.3, t=0.0, wave=0.15, segs=6):
    """drapeau qui flotte, hampe à x=0, flotte vers +x, coin bas à y=0"""
    tris, uvs = [], []
    for i in range(segs):
        x0, x1 = w * i / segs, w * (i + 1) / segs
        z0 = math.sin(t * 6 + i * 0.9) * wave * (i / segs)
        z1 = math.sin(t * 6 + (i + 1) * 0.9) * wave * ((i + 1) / segs)
        p = [(x0, 0, z0), (x1, 0, z1), (x1, h, z1), (x0, h, z0)]
        u = [(i / segs, 1), ((i + 1) / segs, 1), ((i + 1) / segs, 0), (i / segs, 0)]
        tris += [[p[0], p[1], p[2]], [p[0], p[2], p[3]]]
        uvs += [[u[0], u[1], u[2]], [u[0], u[2], u[3]]]
    return Mesh(tris, C((255, 255, 255)), uvs, TEXB[tex] if isinstance(tex, str) else tex)


def flagpole(tex, h=8.0, t=0.0, fw=2.4, fh=1.5, col=(240, 240, 235)):
    return merge([cyl(0.08, 0.06, h, 6, col), sphere(0.12, 6, 3, (200, 170, 70)).xf(trans(0, h, 0)),
                  flag(tex, fw, fh, t).xf(trans(0.06, h - fh - 0.1, 0))])


def windows_row(w, y, n, z, tex='shutter', ww=1.0, wh=1.6, col=(255, 255, 255)):
    ms = []
    for i in range(n):
        x = -w / 2 + (i + 0.5) * w / n
        ms.append(box(ww, wh, 0.08, col, tex).xf(trans(x, y, z)))
    return merge(ms)


def veranda_level(w, d, y, depth=3.0, n_cols=12, col=(240, 238, 230), rail=True):
    """galerie à colonnes de fonte tout autour (House of Wonders)"""
    ms = [box(w + 2 * depth, 0.3, d + 2 * depth, col).xf(trans(0, y - 0.3, 0))]
    W2, D2 = w / 2 + depth - 0.2, d / 2 + depth - 0.2
    for i in range(n_cols + 1):
        x = -W2 + 2 * W2 * i / n_cols
        for z in (-D2, D2):
            ms.append(cyl(0.12, 0.12, 4.0, 6, (230, 228, 220)).xf(trans(x, y, z)))
    for i in range(int(n_cols * d / w) + 1):
        z = -D2 + 2 * D2 * i / max(1, int(n_cols * d / w))
        for x in (-W2, W2):
            ms.append(cyl(0.12, 0.12, 4.0, 6, (230, 228, 220)).xf(trans(x, y, z)))
    if rail:
        for z in (-D2, D2):
            ms.append(box(2 * W2, 0.08, 0.08, (60, 60, 60)).xf(trans(0, y + 1.0, z)))
            ms.append(box(2 * W2, 0.9, 0.03, (60, 60, 60), alpha=0.4).xf(trans(0, y + 0.1, z)))
        for x in (-W2, W2):
            ms.append(box(0.08, 0.08, 2 * D2, (60, 60, 60)).xf(trans(x, y + 1.0, 0)))
            ms.append(box(0.03, 0.9, 2 * D2, (60, 60, 60), alpha=0.4).xf(trans(x, y + 0.1, 0)))
    return merge(ms)


def clock_hands(hour, minute, r=1.4):
    a_m = minute / 60 * 2 * math.pi
    a_h = ((hour % 12) + minute / 60) / 12 * 2 * math.pi
    k = r / 1.4
    ms = [box(0.12 * k, r * 0.85, 0.05 * k, (20, 20, 20)).xf(M(rotz(-a_m), trans(0, 0, 0.03 * k))),
          box(0.18 * k, r * 0.55, 0.05 * k, (20, 20, 20)).xf(M(rotz(-a_h), trans(0, 0, 0.06 * k))),
          cyl(0.1 * k, 0.1 * k, 0.1 * k, 6, (40, 40, 40)).xf(rotx(math.pi / 2))]
    return merge(ms)


def house_of_wonders(hour=9, minute=0):
    """Beit al-Ajaib : 4 niveaux de galeries + tour de l'horloge. Façade côté mer = +z"""
    w, d = 30.0, 16.0
    ms = [box(w, 18, d, (240, 238, 230), 'plaster', ts=3.0)]
    for k, y in enumerate((0.6, 5.0, 9.4, 13.8)):
        ms.append(windows_row(w, y, 10, d / 2 + 0.02, 'shutter', 1.4, 2.4))
        ms.append(windows_row(w, y, 10, -d / 2 - 0.02, 'shutter', 1.4, 2.4))
        if k > 0:
            ms.append(veranda_level(w, d, y - 0.4, 3.0, 12))
    ms.append(veranda_level(w, d, 0.0, 3.0, 12, rail=False))
    ms.append(box(w + 6.4, 0.5, d + 6.4, (235, 232, 222)).xf(trans(0, 18.0, 0)))
    # porte sculptée
    ms.append(box(2.4, 3.6, 0.1, (255, 255, 255), 'carved_door').xf(trans(0, 0, d / 2 + 0.05)))
    # tour de l'horloge
    tw = 4.5
    ms.append(box(tw, 9, tw, (240, 238, 230), 'plaster', ts=2.0).xf(trans(0, 18.5, 0)))
    ms.append(box(tw + 0.6, 0.4, tw + 0.6, (230, 228, 220)).xf(trans(0, 27.5, 0)))
    ms.append(cyl(tw * 0.75, 0, 3.0, 4, (120, 120, 115), 'roof_tin').xf(M(trans(0, 27.9, 0), roty(math.pi / 4))))
    ms.append(cyl(0.06, 0.06, 2.5, 4, (200, 170, 70)).xf(trans(0, 30.8, 0)))
    for s in range(4):
        r = roty(s * math.pi / 2)
        ms.append(quad((-1.6, -1.6, 0), (1.6, -1.6, 0), (1.6, 1.6, 0), (-1.6, 1.6, 0), (255, 255, 255), 'clock_face',
                       ((0, 1), (1, 1), (1, 0), (0, 0))).xf(M(r, trans(0, 24.0, tw / 2 + 0.03))))
        ms.append(clock_hands(hour, minute).xf(M(r, trans(0, 24.0, tw / 2 + 0.05))))
    return merge(ms)


CLOCK_POS = (0, 24.0, 2.25 + 0.05)  # relatif à la House of Wonders, face +z


def palace(burn=0.0):
    """Beit al-Hukm (palais du sultan), façade côté mer +z ; burn 0..1 noircissement"""
    w, d, h = 26.0, 14.0, 13.0
    col = np.array([238, 232, 215]) * (1 - 0.65 * burn) + np.array([60, 52, 46]) * 0.0
    tex = 'plaster_old' if burn < 0.5 else 'scorch'
    ms = [box(w, h, d, col, tex, ts=3.0)]
    for y in (0.8, 4.8, 8.8):
        ms.append(windows_row(w, y, 9, d / 2 + 0.02, 'shutter', 1.3, 2.2, (255, 255, 255) if burn < 0.5 else (90, 80, 70)))
    # balcons de bois sculpté
    for y in (4.4, 8.4):
        ms.append(box(w - 4, 0.25, 1.6, (110, 75, 45), 'wood_dark').xf(trans(0, y, d / 2 + 0.8)))
        ms.append(box(w - 4, 0.9, 0.08, (100, 68, 40), 'planks_v', alpha=0.85).xf(trans(0, y + 0.25, d / 2 + 1.55)))
        ms.append(box(w - 4, 0.15, 1.8, (90, 60, 35)).xf(trans(0, y + 2.6, d / 2 + 0.9)))
        for i in range(12):
            ms.append(box(0.1, 2.6, 0.1, (90, 60, 35)).xf(trans(-w / 2 + 2.5 + i * (w - 5) / 11, y, d / 2 + 1.6)))
    # créneaux
    for i in range(20):
        x = -w / 2 + 0.6 + i * (w - 1.2) / 19
        ms.append(box(0.6, 0.8, 0.6, col, tex).xf(trans(x, h, d / 2 - 0.3)))
        ms.append(box(0.6, 0.8, 0.6, col, tex).xf(trans(x, h, -d / 2 + 0.3)))
    ms.append(box(2.2, 3.4, 0.1, (255, 255, 255), 'carved_door').xf(trans(0, 0, d / 2 + 0.05)))
    # aile du harem (plus basse)
    ms.append(box(14, 9, 12, col, tex, ts=3.0).xf(trans(-w / 2 - 7.5, 0, -1)))
    ms.append(windows_row(14, 3.0, 5, 5.02, 'shutter', 1.2, 2.0).xf(trans(-w / 2 - 7.5, 0, 0)))
    return merge(ms)


PALACE_FLAG_POS = (6.0, 13.0, 0.0)


def lighthouse():
    return merge([cyl(1.4, 1.0, 22, 8, (245, 243, 235), 'plaster', ts=2.0), cyl(1.3, 1.3, 0.3, 8, (60, 60, 60)).xf(trans(0, 22, 0)),
                  cyl(0.9, 0.9, 1.8, 8, (230, 220, 170), emis=0.3, alpha=0.8).xf(trans(0, 22.3, 0)),
                  cyl(1.1, 0.2, 1.2, 8, (60, 60, 60)).xf(trans(0, 24.1, 0))])


def stone_house(w=8, d=8, h=10, col=(235, 225, 200), seed=0, tex='coral'):
    rr = np.random.default_rng(seed)
    ms = [box(w, h, d, col, tex, ts=2.5)]
    nf = int(h // 3.3)
    for f in range(nf):
        ms.append(windows_row(w, 0.8 + f * 3.3, max(1, int(w // 2.8)), d / 2 + 0.02, 'shutter', 1.0, 1.7))
    if rr.random() < 0.5:
        ms.append(box(w * 0.7, 0.2, 1.0, (100, 70, 45), 'wood_dark').xf(trans(0, 3.6, d / 2 + 0.5)))
        ms.append(box(w * 0.7, 0.8, 0.06, (100, 70, 45), 'planks_v').xf(trans(0, 3.8, d / 2 + 0.98)))
    ms.append(box(1.4, 2.4, 0.08, (255, 255, 255), 'carved_door').xf(trans(rr.uniform(-w / 4, w / 4), 0, d / 2 + 0.04)))
    ms.append(box(w + 0.2, 0.4, d + 0.2, np.asarray(col) * 0.95).xf(trans(0, h, 0)))
    return merge(ms)




def german_consulate(t=0.0, gate=0.0):
    """consulat de l'Empire allemand : façade à colonnes, balcon, armoiries à l'aigle, mur et portail, drapeau impérial"""
    ms = [stone_house(12, 10, 9.9, (232, 225, 205), 4)]
    # portique à colonnes + balcon
    for x in (-2.4, -0.8, 0.8, 2.4):
        ms.append(cyl(0.25, 0.22, 3.2, 8, (240, 236, 222)).xf(trans(x, 0, 5.8)))
    ms.append(box(6.0, 0.3, 1.8, (235, 230, 215)).xf(trans(0, 3.2, 5.6)))
    for k in range(13):
        ms.append(box(0.08, 0.8, 0.08, (235, 230, 215)).xf(trans(-2.9 + k * 0.48, 3.5, 6.4)))
    ms.append(box(6.0, 0.1, 0.12, (235, 230, 215)).xf(trans(0, 4.3, 6.4)))
    ms.append(box(1.8, 2.8, 0.12, (255, 255, 255), 'carved_door').xf(trans(0, 0, 5.06)))
    # armoiries : aigle noir sur écu doré
    ms.append(box(1.4, 1.4, 0.08, (210, 175, 60), 'metal').xf(trans(0, 5.0, 5.08)))
    ms.append(box(0.6, 0.6, 0.05, (20, 20, 20)).xf(trans(0, 5.4, 5.14)))
    for s in (-1, 1):
        ms.append(box(0.45, 0.25, 0.05, (20, 20, 20)).xf(M(trans(s * 0.35, 5.5, 5.14), rotz(-s * 0.4))))
    ms.append(box(0.2, 0.2, 0.05, (20, 20, 20)).xf(trans(0, 6.0, 5.14)))
    ms.append(box(0.25, 0.15, 0.05, (200, 160, 40)).xf(trans(0, 6.2, 5.16)))  # couronne
    # mur d'enceinte et portail
    for s in (-1, 1):
        ms.append(box(5.0, 2.0, 0.5, (225, 215, 190), 'plaster_old', ts=1.5).xf(trans(s * 4.5, 0, 9.0)))
        ms.append(box(0.8, 2.8, 0.8, (225, 215, 190), 'plaster_old').xf(trans(s * 1.8, 0, 9.0)))
        ms.append(sphere(0.35, 6, 3, (225, 215, 190)).xf(trans(s * 1.8, 3.0, 9.0)))
    # portail à deux battants qui pivotent sur leurs gonds (vers l'intérieur)
    for s in (-1, 1):
        leaf = [box(0.06, 2.4, 0.06, (30, 30, 30)).xf(trans(-s * (0.1 + k * 0.4), 0, 0)) for k in range(4)]
        leaf += [box(1.4, 0.08, 0.08, (30, 30, 30)).xf(trans(-s * 0.7, y, 0)) for y in (0.3, 2.3)]
        ms.append(merge(leaf).xf(M(trans(s * 1.4, 0, 9.0), roty(s * gate * 1.6))))
    # jardin
    for x in (-4.5, 4.5):
        ms.append(palm(6, int(x + 10)).xf(trans(x, 0, 7.3)))
    ms.append(flagpole('german_flag', 5.0, t, 2.2, 1.4, (80, 80, 80)).xf(trans(4.0, 9.9, 4.5)))
    return merge(ms)


def stone_town(seed=0, x0=-120, x1=120, z0=-80, z1=-25, n=40, avoid=()):
    rr = np.random.default_rng(seed)
    ms = []
    cols = [(240, 232, 210), (230, 215, 185), (220, 200, 165), (245, 240, 228), (215, 190, 150)]
    for i in range(n):
        x, z = rr.uniform(x0, x1), rr.uniform(z0, z1)
        if any(a0 < x < a1 and b0 < z < b1 for (a0, a1, b0, b1) in avoid):
            continue
        w, d, h = rr.uniform(6, 12), rr.uniform(6, 10), rr.choice([6.6, 9.9, 13.2])
        ms.append(stone_house(w, d, h, cols[rr.integers(0, len(cols))], i).xf(M(trans(x, 0, z), roty(rr.choice([0, 0, 0, 0.05, -0.05])))))
    return merge(ms)


# ---------------------------------------------------------------- navires
def hull(L, B, H, col=(255, 255, 255), tex='hull_black', deck_tex='deck_planks', stripe=None):
    """coque vers +x (proue). quille y=-H*0.6, pont à y=H*0.4"""
    y0, y1 = -H * 0.6, H * 0.4
    xb, xs = L / 2, -L / 2
    xp = L / 2 - B * 1.4
    pts_top = [(xs, y1, -B / 2 * 0.9), (xp, y1, -B / 2), (xb, y1, 0), (xp, y1, B / 2), (xs, y1, B / 2 * 0.9)]
    pts_bot = [(xs + 1, y0, -B / 2 * 0.6), (xp, y0, -B / 2 * 0.7), (xb - 1.0, y0, 0), (xp, y0, B / 2 * 0.7), (xs + 1, y0, B / 2 * 0.6)]
    tris, uvs = [], []
    n = len(pts_top)
    for i in range(n - 1):
        a, b, c, d_ = pts_bot[i], pts_bot[i + 1], pts_top[i + 1], pts_top[i]
        tris += [[a, b, c], [a, c, d_]]
        uvs += [[(0, 1), (L / 6, 1), (L / 6, 0)], [(0, 1), (L / 6, 0), (0, 0)]]
    # poupe
    tris += [[pts_bot[-1], pts_bot[0], pts_top[0]], [pts_bot[-1], pts_top[0], pts_top[-1]]]
    uvs += [[(0, 1), (1, 1), (1, 0)], [(0, 1), (1, 0), (0, 0)]]
    ms = [Mesh(tris, C(col), uvs, TEXB[tex])]
    # pont
    dt = [[pts_top[0], pts_top[1], pts_top[3]], [pts_top[0], pts_top[3], pts_top[4]], [pts_top[1], pts_top[2], pts_top[3]]]
    du = [[(0, 0), (L / 3, 0), (L / 3, 2)], [(0, 0), (L / 3, 2), (0, 2)], [(L / 3, 0), (L / 2.5, 1), (L / 3, 2)]]
    ms.append(Mesh(dt, C((255, 255, 255)), du, TEXB[deck_tex]))
    if stripe is not None:
        for s in (-1, 1):
            ms.append(box(L - B * 1.6, 0.25, 0.05, stripe).xf(trans(-B * 0.7, y1 - 0.5, s * (B / 2 + 0.02))))
    return merge(ms)


def funnel(h=6, r=0.9, col=(200, 170, 110)):
    return merge([cyl(r, r, h, 10, col), cyl(r + 0.05, r + 0.05, 0.5, 10, (30, 30, 30)).xf(trans(0, h - 0.5, 0))])


def mast(h=18, yard=True):
    ms = [cyl(0.25, 0.12, h, 6, (110, 80, 50), 'bark')]
    if yard:
        ms.append(box(0.15, 0.15, 6.0, (110, 80, 50)).xf(trans(0, h * 0.7, 0)))
        ms.append(cyl(0.8, 0.8, 0.6, 8, (90, 70, 45)).xf(trans(0, h * 0.55, 0)))
    return merge(ms)


def gun(L=5.0, r=0.25):
    return merge([cyl(r, r * 0.7, L, 8, (60, 62, 60), 'metal').xf(M(rotz(-math.pi / 2)))])


def turrets(kind):
    """(x local, hauteur pont, longueur canon, hauteur canon) des tourelles"""
    big = kind == 'cruiser'
    L, B, H = (95, 15, 9) if big else (50, 8, 6)
    y1 = H * 0.4
    xs = (L * 0.35, -L * 0.38) if big else (L * 0.32, -L * 0.33)
    return [(gx, y1, 7.0 if big else 4.0, 0.8 if big else 0.5) for gx in xs]


def warship(kind='cruiser', t=0.0, gun_yaw=0.0, fire=None, ensign=True, gun_yaws=None):
    """navire britannique vers +x ; gun_yaws = orientation de chaque tourelle (repère du navire)"""
    big = kind == 'cruiser'
    L, B, H = (95, 15, 9) if big else (50, 8, 6)
    ms = [hull(L, B, H, (255, 255, 255), 'hull_black', stripe=(200, 170, 80))]
    y1 = H * 0.4
    ms.append(box(L * 0.35, 2.6, B * 0.6, (240, 240, 235), 'navy_whites', ts=2.0).xf(trans(-L * 0.05, y1, 0)))
    ms.append(box(L * 0.12, 2.2, B * 0.5, (240, 240, 235), 'navy_whites', ts=2.0).xf(trans(L * 0.12, y1 + 2.6, 0)))
    for i in range(5):
        for s in (-1, 1):
            ms.append(box(L * 0.3 / 5 * 0.6, 0.6, 0.05, (40, 50, 60)).xf(trans(-L * 0.2 + i * L * 0.3 / 5, y1 + 1.3, s * (B * 0.3 + 0.03))))
    nf = 2 if big else 1
    for k in range(nf):
        ms.append(funnel(9 if big else 6, 1.4 if big else 0.9).xf(trans(-L * 0.03 - k * L * 0.1, y1 + 2.6, 0)))
    ms.append(mast(28 if big else 18).xf(trans(L * 0.25, y1, 0)))
    ms.append(mast(24 if big else 15).xf(trans(-L * 0.3, y1, 0)))
    # haubans
    for s in (-1, 1):
        ms.append(rod((L * 0.25, (28 if big else 18) * 0.85 + y1, 0), (L * 0.18, y1, s * B * 0.45), 0.04, (40, 40, 40), n=3))
        ms.append(rod((-L * 0.3, (24 if big else 15) * 0.85 + y1, 0), (-L * 0.24, y1, s * B * 0.45), 0.04, (40, 40, 40), n=3))
    # garde-corps
    for s in (-1, 1):
        ms.append(box(L * 0.8, 0.05, 0.05, (230, 230, 225)).xf(trans(-L * 0.05, y1 + 0.9, s * B * 0.47)))
    tur = turrets(kind)
    for k, (gx, ty, glen, gh) in enumerate(tur):
        yaw = gun_yaws[k] if gun_yaws is not None else gun_yaw
        r = 1.8 if big else 1.1
        t_ = merge([cyl(r, r, 1.6 if big else 1.0, 10, (230, 230, 225), 'navy_whites'),
                    box(r * 1.2, 1.2 if big else 0.8, r * 1.4, (225, 225, 220), 'navy_whites').xf(trans(r * 0.1, 0.2, 0)),
                    gun(glen, 0.35 if big else 0.22).xf(trans(0, gh, 0))])
        ms.append(t_.xf(M(trans(gx, ty, 0), roty(yaw))))
    nb = 6 if big else 3
    for i in range(nb):
        x = -L * 0.25 + i * L * 0.5 / max(1, nb - 1)
        ms.append(gun(2.5, 0.15).xf(M(trans(x, y1 - 1.5, B / 2 - 0.4), roty(-math.pi / 2))))
    if ensign:
        ms.append(flag('white_ensign', 4 if big else 3, 2.6 if big else 2, t).xf(M(trans(-L / 2 + 0.5, y1 + 4, 0), roty(math.pi))))
        ms.append(cyl(0.08, 0.08, 7 if big else 6, 4, (110, 80, 50)).xf(trans(-L / 2 + 0.5, y1, 0)))
    return merge(ms)


WARSHIP_DIMS = {'cruiser': (95, 15, 9), 'gunboat': (50, 8, 6)}


def yacht(t=0.0, tilt=0.0, sink=0.0):
    """HHS Glasgow : yacht royal blanc, vers +x"""
    L, B, H = 64, 9, 6
    ms = [hull(L, B, H, (245, 245, 240), 'plaster', stripe=(200, 170, 70))]
    y1 = H * 0.4
    ms.append(box(L * 0.4, 2.4, B * 0.6, (245, 245, 238), 'navy_whites', ts=2.0).xf(trans(-L * 0.05, y1, 0)))
    for i in range(8):
        ms.append(box(1.0, 0.8, 0.05, (40, 50, 60)).xf(trans(-L * 0.22 + i * 2.6, y1 + 1.0, B * 0.3 + 0.03)))
    ms.append(funnel(7, 1.0, (225, 190, 90)).xf(trans(-L * 0.02, y1 + 2.4, 0)))
    ms.append(mast(18).xf(trans(L * 0.22, y1, 0)))
    ms.append(mast(16).xf(trans(-L * 0.28, y1, 0)))
    ms.append(flag('red_cloth', 3, 2, t).xf(M(trans(-L / 2 + 0.5, y1 + 4.0, 0), roty(math.pi))))
    ms.append(cyl(0.08, 0.08, 6, 4, (110, 80, 50)).xf(trans(-L / 2 + 0.5, y1, 0)))
    return merge(ms).xf(M(trans(0, -sink, 0), rotx(tilt), rotz(-tilt * 0.4)))


def dhow(t=0.0, seed=0):
    rr = np.random.default_rng(seed)
    ms = [hull(14, 4, 2.5, (255, 255, 255), 'wood_dark', 'planks')]
    ms.append(cyl(0.15, 0.1, 10, 5, (110, 80, 50)).xf(trans(1.5, 1, 0)))
    sail = Mesh([[(1.6, 2.0, 0), (1.6, 10.5, 0), (-5.0, 3.0, 0)], [(1.6, 10.5, 0), (6.5, 9.0, 0), (1.6, 2.0, 0)]], C((235, 225, 200)))
    ms.append(sail.xf(M(trans(0, 0, 0.3), roty(0.2 + 0.05 * math.sin(t + seed)))))
    return merge(ms)


# ---------------------------------------------------------------- effets
def sea(x0=-600, z0=4.0, x1=600, z1=700, t=0.0, y=-0.9, tex='sea', ts=8.0, n=6):
    m = grid(x0, z0, x1, z1, n, n, lambda x, z: y, (255, 255, 255), tex, ts)
    m.uv = m.uv + np.array([t * 0.05, t * 0.02])
    return m


def muzzle(pos, k, cam, size=4.0):
    """flash de canon k (0..1 décroissant)"""
    if k <= 0:
        return Mesh()
    return merge([billboard(pos, size * (0.6 + k), size * (0.6 + k), cam, (255, 255, 255), 'spark', emis=1.0, alpha=min(1, k * 1.5)),
                  billboard(pos, size * 0.6 * (1 + k), size * 0.6 * (1 + k), cam, (255, 255, 255), 'fire', emis=1.0, alpha=k)])


def explosion(pos, age, cam, size=6.0, seed=0, debris=True):
    """explosion : boule de feu puis fumée, débris"""
    if age < 0:
        return Mesh()
    rr = np.random.default_rng(seed)
    ms = []
    pos = np.asarray(pos, float)
    if age < 0.6:
        k = age / 0.6
        for i in range(5):
            o = rr.normal(size=3) * size * 0.25
            s = size * (0.4 + k) * (0.7 + 0.4 * rr.random())
            ms.append(billboard(pos + o, s, s, cam, (255, 255, 255), 'fire', emis=1.0, alpha=1 - k * 0.6))
    if age < 4.0:
        for i in range(7):
            o = rr.normal(size=3) * size * 0.3 + np.array([0, age * size * 0.35, 0])
            s = size * (0.6 + age * 0.5) * (0.7 + 0.4 * rr.random())
            ms.append(billboard(pos + o, s, s, cam, (110, 105, 100), 'smoke', emis=0.2, alpha=max(0, 0.8 - age * 0.2)))
    if debris and age < 2.0:
        for i in range(10):
            v = rr.normal(size=3) * np.array([1, 0.6, 1]) * size + np.array([0, size * 1.2, 0])
            p = pos + v * age * 0.6 + np.array([0, -4.9 * age * age, 0])
            ms.append(box(0.4, 0.4, 0.4, (120, 100, 80)).xf(M(trans(p), rotx(age * 8 + i), rotz(age * 5))))
    return merge(ms)


def big_smoke(base, t, cam, n=10, size=8.0, rise=25.0, seed=0, col=(70, 66, 62), alpha=0.85):
    return smoke_sprites(base, t, cam, n=n, size=size, rise=rise, seed=seed, col=col, drift=(0.6, 0, -0.1), alpha=alpha)


def barricade(n=8, seed=0):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        x = i * 1.3 - n * 0.65
        if rr.random() < 0.5:
            ms.append(box(1.2, 0.8, 0.9, (150, 110, 70), 'planks').xf(M(trans(x, 0, rr.uniform(-0.2, 0.2)), roty(rr.uniform(-0.3, 0.3)))))
        else:
            ms.append(sphere(0.6, 6, 3, (255, 255, 255), 'sacking', sy=0.6).xf(trans(x, 0.3, 0)))
            ms.append(sphere(0.55, 6, 3, (255, 255, 255), 'sacking', sy=0.6).xf(trans(x + 0.3, 0.8, 0.1)))
    return merge(ms)


def old_cannon():
    return merge([gun(2.2, 0.18).xf(M(trans(-0.8, 0.75, 0))), wheel(0.5, 0.1, 8, (100, 70, 40)).xf(M(trans(0, 0.5, 0.45), rotx(math.pi / 2))),
                  wheel(0.5, 0.1, 8, (100, 70, 40)).xf(M(trans(0, 0.5, -0.55), rotx(math.pi / 2))), box(1.4, 0.3, 0.6, (100, 70, 40)).xf(trans(-0.4, 0.3, 0))])


def pocket_watch(minute=0.0, second=0.0, hour=9, open_=1.0):
    ms = [cyl(0.5, 0.5, 0.12, 14, (200, 170, 70), 'metal'),
          quad((-0.43, 0.125, 0.43), (0.43, 0.125, 0.43), (0.43, 0.125, -0.43), (-0.43, 0.125, -0.43), (255, 255, 255), 'clock_face',
               ((0, 1), (1, 1), (1, 0), (0, 0))),
          cyl(0.08, 0.08, 0.15, 6, (200, 170, 70)).xf(M(trans(0, 0.06, -0.53), rotx(math.pi / 2))),
          cyl(0.12, 0.12, 0.04, 8, (200, 170, 70), caps=False).xf(M(trans(0, 0.06, -0.68), rotx(math.pi / 2)))]
    hands = clock_hands(hour, minute, 0.45).xf(M(trans(0, 0.13, 0), rotx(-math.pi / 2)))
    sec = box(0.012, 0.36, 0.01, (180, 20, 20)).xf(M(trans(0, 0.15, 0), rotx(-math.pi / 2), rotz(-second / 60 * 2 * math.pi)))
    lid = cyl(0.5, 0.5, 0.05, 14, (210, 180, 80), 'metal').xf(M(trans(0, 0, -0.5), rotx(-open_ * 2.0), trans(0, 0.12, 0.5)))
    return merge(ms + [hands, sec, lid])


def _earclip(poly):
    """triangulation d'un polygone simple (liste de (x, z)) par oreilles"""
    pts = [tuple(p) for p in poly]
    area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    if area < 0:
        pts = pts[::-1]
    idx = list(range(len(pts)))
    tris = []

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def inside(p, a, b, c):
        return cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0
    guard = 0
    while len(idx) > 3 and guard < 10000:
        guard += 1
        n = len(idx)
        for k in range(n):
            i0, i1, i2 = idx[(k - 1) % n], idx[k], idx[(k + 1) % n]
            a, b, c = pts[i0], pts[i1], pts[i2]
            if cross(a, b, c) <= 1e-9:
                continue
            if any(inside(pts[j], a, b, c) for j in idx if j not in (i0, i1, i2)):
                continue
            tris.append((a, b, c))
            idx.pop(k)
            break
        else:
            break
    if len(idx) == 3:
        tris.append(tuple(pts[i] for i in idx))
    return tris


# contour approximatif d'Unguja (lon, lat) : pointe nord étroite, presqu'île de Stone Town à l'ouest, baie de Chwaka à l'est


UNGUJA = [(39.295, -5.722), (39.27, -5.78), (39.245, -5.86), (39.225, -5.93), (39.205, -6.01), (39.19, -6.08), (39.175, -6.14),
          (39.185, -6.17), (39.2, -6.21), (39.23, -6.26), (39.255, -6.31), (39.30, -6.37), (39.36, -6.42), (39.42, -6.46), (39.47, -6.485),
          (39.52, -6.44), (39.545, -6.36), (39.53, -6.28), (39.555, -6.21), (39.53, -6.14), (39.47, -6.16), (39.44, -6.12), (39.46, -6.06),
          (39.5, -6.0), (39.5, -5.93), (39.46, -5.87), (39.42, -5.82), (39.38, -5.77), (39.33, -5.73)]


AFRICA = [(38.95, -5.2), (38.98, -5.5), (38.96, -5.8), (38.92, -6.0), (38.88, -6.2), (38.92, -6.45), (39.05, -6.65), (39.1, -6.85),
          (39.25, -7.1), (38.0, -7.1), (38.0, -5.2)]


def geo(lon, lat):
    return ((lon - 39.37) * 110.0, -(lat + 6.1) * 110.0)


def island_map():
    """l'île d'Unguja et la côte africaine (1 unité = 1 km)"""
    ms = []
    for poly, h, tex in ((UNGUJA, 0.6, 'land'), (AFRICA, 0.8, 'land')):
        P = [geo(*p) for p in poly]
        tris = _earclip(P)
        ms.append(Mesh([[(a[0], h, a[1]), (b[0], h, b[1]), (c[0], h, c[1])] for a, b, c in tris], C((255, 255, 255)),
                       [[(a[0] / 8, a[1] / 8), (b[0] / 8, b[1] / 8), (c[0] / 8, c[1] / 8)] for a, b, c in tris], TEXB[tex]))
        # plage tout autour
        cx, cz = np.mean([p[0] for p in P]), np.mean([p[1] for p in P])
        bt = []
        for i in range(len(P)):
            a, b = np.array(P[i]), np.array(P[(i + 1) % len(P)])
            na = a + (a - np.array([cx, cz])) / (np.linalg.norm(a - np.array([cx, cz])) + 1e-9) * 1.2
            nb = b + (b - np.array([cx, cz])) / (np.linalg.norm(b - np.array([cx, cz])) + 1e-9) * 1.2
            bt.append([(a[0], h, a[1]), (b[0], h, b[1]), (nb[0], 0.0, nb[1])])
            bt.append([(a[0], h, a[1]), (nb[0], 0.0, nb[1]), (na[0], 0.0, na[1])])
        ms.append(Mesh(bt, C((225, 210, 170))))
    # quelques reliefs/forêts sur l'île
    rr = np.random.default_rng(4)
    for k in range(40):
        lon, lat = rr.uniform(39.22, 39.5), rr.uniform(-6.42, -5.78)
        x, z = geo(lon, lat)
        from matplotlib.path import Path as _P
        if _P([geo(*p) for p in UNGUJA]).contains_point((x, z)):
            ms.append(sphere(rr.uniform(1.2, 2.5), 6, 3, (255, 255, 255), 'leaves', sy=0.5).xf(trans(x, 0.6, z)))
    return merge(ms)


ENV_MORNING = Env(sky_top=(70, 130, 200), sky_hor=(220, 225, 220), fog=(200, 210, 210), fog_near=80, fog_far=900,
                  light=(0.4, 0.7, 0.55), amb=0.55, light_col=(255, 245, 225))
ENV_SMOKE = Env(sky_top=(90, 100, 110), sky_hor=(190, 170, 150), fog=(160, 145, 130), fog_near=60, fog_far=700,
                light=(0.4, 0.7, 0.55), amb=0.55, light_col=(255, 220, 180))
ENV_NIGHT = Env(sky_top=(15, 20, 40), sky_hor=(40, 45, 70), fog=(30, 32, 50), fog_near=10, fog_far=60,
                light=(0.3, 0.8, 0.5), amb=0.45, light_col=(160, 170, 220))
ENV_ROOM = Env(sky_top=(35, 28, 22), sky_hor=(35, 28, 22), fog=(28, 22, 18), fog_near=8, fog_far=40,
               light=(0.4, 0.7, 0.6), amb=0.55, light_col=(255, 230, 190))
ENV_SUNSET = Env(sky_top=(70, 70, 130), sky_hor=(250, 160, 90), fog=(220, 150, 100), fog_near=80, fog_far=800,
                 light=(-0.8, 0.3, 0.4), amb=0.5, light_col=(255, 190, 130))


STONE_TOWN_GEO = geo(39.19, -6.16)
