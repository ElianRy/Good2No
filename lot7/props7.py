"""Accessoires et décors partagés du lot 7."""
from g2n7 import *

build_base_textures()

tex_noise('asphalt', (70, 70, 72), (92, 92, 95), seed=501, octaves=2, speck=0.08, speck_col=(110, 110, 112))
tex_noise('lawn', (78, 128, 52), (112, 158, 66), seed=502, octaves=3, speck=0.08, speck_col=(140, 175, 80))
tex_noise('stucco', (225, 210, 180), (240, 228, 205), seed=503, octaves=2, speck=0.05)
tex_noise('stucco_w', (228, 228, 222), (245, 245, 240), seed=504, octaves=2, speck=0.05)
tex_noise('concrete', (165, 162, 155), (190, 187, 180), seed=505, octaves=2, speck=0.1, speck_col=(140, 138, 132))
tex_noise('denim', (55, 80, 125), (70, 95, 140), seed=506, octaves=1)
tex_noise('linen', (225, 222, 212), (240, 238, 230), seed=507, octaves=1)
tex_noise('labcoat', (232, 232, 228), (248, 248, 245), seed=508, octaves=1)
tex_noise('logwall', (120, 85, 55), (150, 110, 70), seed=509, octaves=1)
tex_noise('shingle', (95, 80, 70), (120, 100, 85), seed=510, octaves=1, speck=0.2, speck_col=(70, 60, 55))
tex_noise('meat', (150, 30, 35), (195, 70, 70), seed=511, octaves=3, speck=0.18, speck_col=(235, 200, 190))
tex_noise('wool', (225, 220, 205), (245, 242, 232), seed=512, octaves=4, speck=0.25, speck_col=(200, 195, 180))
tex_noise('fur_deer', (140, 95, 60), (165, 115, 75), seed=513, octaves=3)
tex_noise('feath_dark', (30, 28, 30), (55, 50, 52), seed=514, octaves=3, speck=0.1, speck_col=(15, 15, 15))
tex_noise('melon', (190, 170, 110), (215, 195, 135), seed=515, octaves=2, speck=0.3, speck_col=(160, 145, 95))
tex_noise('mold', (80, 140, 90), (190, 220, 190), seed=516, octaves=4, speck=0.2, speck_col=(240, 245, 235))
tex_noise('tile_lab', (210, 215, 205), (230, 235, 225), seed=517, octaves=1)
tex_noise('wood_dark', (75, 50, 32), (98, 68, 45), seed=518, octaves=2)
tex_noise('desert', (200, 175, 130), (225, 200, 155), seed=519, octaves=3, speck=0.06, speck_col=(170, 150, 110))
tex_noise('cloudtop', (225, 228, 235), (250, 251, 253), seed=520, octaves=4)
tex_planks('fence', (180, 150, 110), (140, 110, 80), horizontal=False, seed=11)
tex_bricks('brick_red', (140, 60, 45), (170, 160, 145), seed=12)
tex_bricks('brick_lon', (120, 70, 55), (150, 140, 125), rows=8, cols=4, seed=13)
tex_stripes('webbing', (70, 150, 90), (235, 235, 225), n=4, vertical=True)


def _patchwork(d, n):
    r = np.random.default_rng(9)
    for j in range(0, n, 4):
        for i in range(0, n, 4):
            c = [(90, 120, 70), (150, 140, 100), (120, 110, 95), (200, 195, 185), (110, 130, 85), (170, 160, 140)][r.integers(0, 6)]
            d.rectangle([i, j, i + 3, j + 3], fill=c)
    for k in range(0, n, 8):
        d.line([0, k, n, k], fill=(80, 80, 82))
        d.line([k, 0, k, n], fill=(80, 80, 82))


tex_draw('patchwork', _patchwork)


def _windows_plane(d, n):
    d.rectangle([0, 0, n, n], fill=(240, 240, 238))
    d.rectangle([0, 18, n, 22], fill=(200, 40, 45))
    for x in range(1, n, 4):
        d.rectangle([x, 11, x + 1, 14], fill=(40, 50, 70))


tex_draw('plane_side', _windows_plane)


# ------------------------------------------------------------------ objets
def lawn_chair(col_frame=(190, 192, 196)):
    """chaise de jardin pliante alu + sangles vertes et blanches. Assise à y≈0.42, dossier vers -z, regarde +z"""
    ms = []
    fr = col_frame
    for s in (-1, 1):
        ms.append(rod((s * 0.28, 0, 0.3), (s * 0.28, 0.42, 0.25), 0.015, fr, n=4))
        ms.append(rod((s * 0.28, 0, -0.3), (s * 0.28, 0.42, -0.2), 0.015, fr, n=4))
        ms.append(rod((s * 0.28, 0.42, 0.28), (s * 0.28, 0.42, -0.24), 0.015, fr, n=4))
        ms.append(rod((s * 0.28, 0.42, -0.24), (s * 0.28, 1.0, -0.42), 0.015, fr, n=4))
        ms.append(rod((s * 0.28, 0.62, 0.22), (s * 0.28, 0.62, -0.3), 0.015, fr, n=4))     # accoudoir
    ms.append(box(0.56, 0.02, 0.5, (255, 255, 255), 'webbing').xf(trans(0, 0.41, 0.02)))
    m, L = frame_along((0, 0.42, -0.24), (0, 1.0, -0.42))
    ms.append(box(0.56, L, 0.02, (255, 255, 255), 'webbing').xf(m))
    return merge(ms)


def balloon_cluster(n=42, popped=(), seed=3, r=0.55):
    """grappe de ballons météo (4 étages) au-dessus de l'origine. Retourne (mesh, points d'attache des ficelles)"""
    rr = np.random.default_rng(seed)
    ms, tops = [], []
    k = 0
    for tier in range(4):
        cnt = [9, 11, 12, 10][tier]
        for i in range(cnt):
            if k >= n:
                break
            a = i / cnt * 2 * math.pi + tier * 0.4
            rad = [1.0, 1.6, 1.9, 1.3][tier] + rr.uniform(-0.15, 0.15)
            p = np.array([math.cos(a) * rad, 3.0 + tier * 1.05 + rr.uniform(-0.2, 0.2), math.sin(a) * rad])
            if k not in popped:
                c = np.array((236, 226, 200)) * rr.uniform(0.92, 1.05)
                ms.append(sphere(r, 7, 5, c.clip(0, 255), sy=1.15).xf(trans(p)))
                tops.append(p - np.array([0, r * 1.1, 0]))
            k += 1
    return merge(ms), tops


def flying_chair(popped=(), strings=True, larry=None, larry_pose=None, sway=0.0):
    """chaise + ballons + ficelles (+ Larry assis). Origine = sol de la chaise."""
    bm, tops = balloon_cluster(popped=popped)
    ms = [lawn_chair(), bm]
    if strings:
        for i, p in enumerate(tops):
            if i % 2 == 0:
                anc = np.array([0.28 * (1 if p[0] > 0 else -1), 0.95, -0.38])
                ms.append(rod(anc, p, 0.006, (230, 230, 230), n=3))
    # bidons d'eau (lest) accrochés sous l'assise
    for s in (-1, 1):
        ms.append(box(0.16, 0.24, 0.16, (230, 235, 240)).xf(trans(s * 0.36, 0.05, 0.0)))
        ms.append(rod((s * 0.36, 0.29, 0), (s * 0.28, 0.42, 0), 0.005, (200, 200, 200), n=3))
    if larry is not None:
        ms.append(larry.mesh((0, 0, -0.05), 0.0, larry_pose or sit_pose(drop=0.5, la=(0.3, 0.2, 0.6), ra=(0.3, 0.2, 0.6))))
    m = merge(ms)
    if sway:
        m = m.xf(rotz(sway))
    return m


def airliner(livery=(200, 40, 45)):
    """avion de ligne low-poly ~40 m, nez vers +z"""
    ms = [cyl(1.9, 1.9, 34, 10, (255, 255, 255), 'plane_side', ts=4.0).xf(M(trans(0, 0, -17), rotx(math.pi / 2)))]
    ms.append(sphere(1.9, 10, 5, (240, 240, 238)).xf(M(trans(0, 0, 17), scale(1, 1, 1.8))))
    ms.append(box(0.6, 0.35, 0.2, (40, 50, 70)).xf(trans(0, 0.9, 19.5)))
    ms.append(frustum(3.8, 3.8, 0.6, 0.8, 6.0, (235, 235, 233), dy1=1.4).xf(trans(0, 0, -23)).xf(M(rotx(math.pi), trans(0, 0, 0))) if False else Mesh())
    ms.append(frustum(3.6, 3.6, 0.5, 0.6, 7.0, (238, 238, 236), dy1=1.2).xf(M(trans(0, 0, -17), roty(math.pi))))
    # ailes
    for s in (-1, 1):
        w = [[(s * 1.6, -0.6, 4), (s * 18, -0.1, -5), (s * 18, -0.1, -7.5)], [(s * 1.6, -0.6, 4), (s * 18, -0.1, -7.5), (s * 1.6, -0.6, -4.5)]]
        ms.append(Mesh(w, C((215, 215, 218))))
        ms.append(cyl(0.9, 0.9, 3.4, 8, (200, 200, 205)).xf(M(trans(s * 6.5, -1.6, 1.0), rotx(math.pi / 2))))
        ms.append(Mesh([[(s * 0.5, 0.6, -20), (s * 7, 0.9, -25), (s * 7, 0.9, -26.5)], [(s * 0.5, 0.6, -20), (s * 7, 0.9, -26.5), (s * 0.5, 0.6, -25)]], C((215, 215, 218))))
    ms.append(Mesh([[(0, 1.2, -19), (0, 7.5, -25.5), (0, 7.5, -27.5)], [(0, 1.2, -19), (0, 7.5, -27.5), (0, 1.5, -24.5)]], C(livery)))
    return merge(ms)


def jeep(col=(80, 95, 70)):
    ms = [box(1.6, 0.7, 3.4, col).xf(trans(0, 0.5, 0)), box(1.5, 0.35, 1.4, col * np.array([0.9, 0.9, 0.9]) if False else col).xf(trans(0, 1.2, 0.9)),
          box(1.4, 0.5, 0.06, (120, 150, 170)).xf(M(trans(0, 1.2, 0.25), rotx(-0.2)))]
    for x in (-0.8, 0.8):
        for z in (-1.1, 1.1):
            ms.append(cyl(0.38, 0.38, 0.28, 10, (30, 30, 32)).xf(M(trans(x, 0.38, z), rotz(math.pi / 2), trans(0, -0.14, 0))))
    ms.append(box(1.5, 0.2, 0.1, (60, 60, 62)).xf(trans(0, 0.45, -1.75)))
    return merge(ms)


def truck(col=(190, 60, 40)):
    """semi-remorque américain (cabine + remorque), avant vers +z"""
    ms = [box(2.4, 2.4, 2.6, col).xf(trans(0, 0.9, 6.5)), box(2.3, 1.2, 1.6, col * np.array([0.95, 0.95, 0.95]) if False else col).xf(trans(0, 0.9, 8.4)),
          box(2.2, 0.9, 0.06, (120, 150, 175)).xf(trans(0, 2.2, 7.82)), box(2.0, 0.8, 0.3, (190, 190, 195)).xf(trans(0, 0.6, 9.25)),
          box(2.5, 3.0, 11, (225, 225, 220)).xf(trans(0, 1.2, -0.5)), box(2.52, 0.3, 11.02, col).xf(trans(0, 2.2, -0.5))]
    for s in (-1, 1):
        ms.append(cyl(0.12, 0.12, 3.0, 6, (180, 180, 185)).xf(trans(s * 1.25, 1.5, 7.2)))
        for z in (8.4, 5.0, -3.5, -4.7):
            ms.append(cyl(0.5, 0.5, 0.3, 10, (25, 25, 28)).xf(M(trans(s * 1.1, 0.5, z), rotz(math.pi / 2), trans(0, -0.15, 0))))
    return merge(ms)


def suburb_house(w=9, d=8, h=3.0, col=(255, 255, 255), roof=(160, 70, 50), seed=0):
    """maison californienne de plain-pied : crépi, toit de tuiles, fenêtres, porte, garage"""
    ms = [box(w, h, d, col, 'stucco', ts=3.0)]
    ms.append(Mesh([[(-w / 2 - 0.4, h, d / 2 + 0.4), (w / 2 + 0.4, h, d / 2 + 0.4), (0, h + 1.6, 0)],
                    [(w / 2 + 0.4, h, -d / 2 - 0.4), (-w / 2 - 0.4, h, -d / 2 - 0.4), (0, h + 1.6, 0)],
                    [(-w / 2 - 0.4, h, -d / 2 - 0.4), (-w / 2 - 0.4, h, d / 2 + 0.4), (0, h + 1.6, 0)],
                    [(w / 2 + 0.4, h, d / 2 + 0.4), (w / 2 + 0.4, h, -d / 2 - 0.4), (0, h + 1.6, 0)]], C(roof), None, TEXB['roof_red']))
    for x in (-w / 4, w / 4):
        ms.append(box(1.4, 1.2, 0.06, (255, 255, 255), 'window').xf(trans(x, 1.0, d / 2 + 0.02)))
        ms.append(box(1.4, 1.2, 0.06, (255, 255, 255), 'window').xf(trans(x, 1.0, -d / 2 - 0.02)))
    ms.append(box(1.0, 2.1, 0.06, (255, 255, 255), 'door').xf(trans(0, 0, d / 2 + 0.03)))
    return merge(ms)


def palm_tree(h=9, seed=0):
    return palm(h, seed)


def power_pole(h=10.0):
    ms = [cyl(0.16, 0.13, h, 6, (105, 80, 55), 'bark', ts=1.0), box(2.6, 0.14, 0.14, (100, 78, 55)).xf(trans(0, h - 0.6, 0))]
    for x in (-1.1, 0, 1.1):
        ms.append(cyl(0.05, 0.05, 0.18, 5, (120, 160, 120)).xf(trans(x, h - 0.46, 0)))
    ms.append(cyl(0.3, 0.3, 0.8, 8, (130, 130, 135)).xf(trans(0.4, h - 2.2, 0.2)))   # transformateur
    return merge(ms)


def wires(p_list, h=10.0, sag=0.6):
    """câbles entre poteaux (liste de positions (x,z)), 3 conducteurs"""
    ms = []
    for a, b in zip(p_list[:-1], p_list[1:]):
        for x in (-1.1, 0, 1.1):
            pts = []
            for k in range(7):
                u = k / 6
                p = np.array([a[0] + (b[0] - a[0]) * u + x, h - 0.3 - sag * 4 * u * (1 - u), a[1] + (b[1] - a[1]) * u])
                pts.append(p)
            for i in range(6):
                ms.append(rod(pts[i], pts[i + 1], 0.02, (30, 30, 30), n=3))
    return merge(ms)


def bench_table(w=2.4, d=0.9, h=0.9, col=(255, 255, 255), tex='wood_dark'):
    ms = [box(w, 0.06, d, col, tex).xf(trans(0, h - 0.06, 0))]
    for x in (-w / 2 + 0.06, w / 2 - 0.06):
        for z in (-d / 2 + 0.06, d / 2 - 0.06):
            ms.append(box(0.07, h - 0.06, 0.07, np.asarray(C(col)) * 0.8, tex).xf(trans(x, 0, z)))
    return merge(ms)


def shelf(w=1.6, h=2.0, d=0.35, n=4, col=(255, 255, 255), tex='wood_dark'):
    ms = [box(w, h, 0.03, col, tex).xf(trans(0, 0, -d / 2))]
    for s in (-1, 1):
        ms.append(box(0.04, h, d, col, tex).xf(trans(s * w / 2, 0, 0)))
    for k in range(n + 1):
        ms.append(box(w, 0.03, d, col, tex).xf(trans(0, k * (h - 0.03) / n, 0)))
    return merge(ms)


def bottle(h=0.25, r=0.05, col=(120, 80, 40), alpha=1.0):
    return merge([cyl(r, r, h * 0.7, 6, col, alpha=alpha), cyl(r, r * 0.4, h * 0.15, 6, col, alpha=alpha).xf(trans(0, h * 0.7, 0)),
                  cyl(r * 0.4, r * 0.4, h * 0.15, 5, col, alpha=alpha).xf(trans(0, h * 0.85, 0))])


def petri(r=0.05, col=(235, 225, 170)):
    """boîte de Petri (base claire + gélose jaunâtre)"""
    return merge([cyl(r, r, 0.012, 10, (210, 225, 230), alpha=1.0), cyl(r * 0.94, r * 0.94, 0.006, 10, col).xf(trans(0, 0.004, 0))])


def petri_stack(n=4, r=0.05, seed=0):
    rr = np.random.default_rng(seed)
    ms = []
    for k in range(n):
        ms.append(petri(r).xf(trans(rr.uniform(-0.006, 0.006), k * 0.014, rr.uniform(-0.006, 0.006))))
    return merge(ms)


def microscope():
    ms = [box(0.14, 0.03, 0.18, (30, 30, 32)), box(0.04, 0.22, 0.04, (30, 30, 32)).xf(trans(0, 0.03, -0.06)),
          box(0.1, 0.02, 0.1, (40, 40, 42)).xf(trans(0, 0.1, 0.0))]
    m, L = frame_along((0, 0.14, 0.0), (0, 0.33, -0.07))
    ms.append(cyl(0.022, 0.022, L, 6, (40, 40, 45)).xf(m))
    ms.append(cyl(0.012, 0.012, 0.04, 5, (150, 150, 150)).xf(trans(0, 0.1, 0)))
    return merge(ms)


def melon(r=0.12, moldy=0.0, seed=0):
    ms = [sphere(r, 8, 5, (255, 255, 255), 'melon', sy=0.92)]
    if moldy > 0:
        rr = np.random.default_rng(seed)
        for k in range(int(5 * moldy) + 1):
            a, v = rr.uniform(0, 6.28), rr.uniform(0.2, 1.2)
            p = np.array([math.cos(a) * math.cos(v), math.sin(v) * 0.92, math.sin(a) * math.cos(v)]) * r
            ms.append(sphere(r * rr.uniform(0.3, 0.5), 6, 3, (255, 255, 255), 'mold', sy=0.5).xf(trans(p)))
    return merge(ms).xf(trans(0, r * 0.92, 0))


def sun_disc(pos, r=6, col=(255, 245, 210)):
    return sphere(r, 8, 4, col, emis=1.0).xf(trans(pos))


# ------------------------------------------------------------------ avion de ligne v2 (corrigé le 6 nov.)
def slab(pts, th, col, plane='xz', tex=0):
    """plaque épaisse à partir d'un polygone convexe 2D. plane='xz' (aile) ou 'zy' (dérive, x = épaisseur)"""
    def P(a, b, h):
        return (a, h, b) if plane == 'xz' else (h, b, a)
    tris = []
    n = len(pts)
    for s in (-th / 2, th / 2):
        for i in range(1, n - 1):
            tris.append([P(*pts[0], s), P(*pts[i], s), P(*pts[i + 1], s)])
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        tris.append([P(*a, -th / 2), P(*b, -th / 2), P(*b, th / 2)])
        tris.append([P(*a, -th / 2), P(*b, th / 2), P(*a, th / 2)])
    return Mesh(tris, C(col))


def _plane_side2(d, n):
    d.rectangle([0, 0, n, n], fill=(242, 242, 240))
    d.rectangle([0, 19, n, 21], fill=(200, 40, 45))
    d.rectangle([0, 22, n, 23], fill=(40, 60, 120))
    for x in range(0, n, 3):
        d.rectangle([x, 12, x + 1, 14], fill=(35, 45, 65))
    d.rectangle([0, 26, n, n], fill=(205, 208, 212))


tex_draw('plane_side2', _plane_side2)


def airliner(livery=(200, 40, 45)):
    """avion de ligne type biréacteur, ~42 m, nez vers +z : fuselage, cockpit vitré, ailes épaisses, réacteurs, empennage"""
    W_ = (240, 240, 238)
    ms = [cyl(1.95, 1.95, 30, 12, W_).xf(M(trans(0, 0, -15), rotx(math.pi / 2)))]
    for s in (-1, 1):      # bandes de la compagnie + rangée de hublots, sur les deux flancs
        ms.append(box(0.08, 0.28, 34, livery).xf(trans(s * 1.93, -0.45, -1.5)))
        ms.append(box(0.08, 0.12, 34, (40, 60, 120)).xf(trans(s * 1.93, -0.7, -1.5)))
        for z in np.arange(-15.5, 14.0, 0.95):
            ms.append(box(0.08, 0.32, 0.26, (35, 45, 65)).xf(trans(s * 1.93, 0.35, z)))
    ms.append(cyl(1.95, 0.4, 5.5, 12, W_).xf(M(trans(0, 0, 15), rotx(math.pi / 2), trans(0, 0, 0))))
    ms.append(sphere(0.42, 6, 4, W_).xf(trans(0, 0, 20.5)))
    for x in (-0.75, -0.25, 0.25, 0.75):        # vitres du cockpit
        ms.append(box(0.42, 0.32, 0.06, (25, 35, 55)).xf(M(trans(x, 0.95, 16.6), rotx(-0.75), roty(-x * 0.5))))
    ms.append(cyl(1.95, 0.5, 9, 12, W_).xf(M(trans(0, 0, -15), rotx(-math.pi / 2 + 0.12))))
    # porte avant + ventre gris
    ms.append(box(0.06, 1.5, 0.8, (180, 182, 188)).xf(trans(1.93, -0.4, 12.5)))
    ms.append(box(0.06, 1.5, 0.8, (180, 182, 188)).xf(trans(-1.93, -0.4, 12.5)))
    ms.append(box(3.2, 0.6, 9, (200, 202, 206)).xf(trans(0, -1.95, 0)))
    for s in (-1, 1):
        wing = slab([(1.5, 4.5), (17.5, -5.0), (17.5, -7.0), (1.5, -3.8)], 0.4, (215, 217, 222)).xf(M(trans(0, -1.1, 0), rotz(0.08)))
        if s < 0:
            wing = wing.xf(scale(-1, 1, 1))
        ms.append(wing)
        ms.append(slab([(0, 0), (1.8, -0.6), (1.8, -1.6), (0, -1.6)], 0.15, livery, plane='zy').xf(M(trans(s * 17.6, -0.4, -5.2), rotz(0), trans(0, 0, 0))).xf(M(scale(1, 1, 1))) if False else
                  box(0.15, 1.6, 1.4, livery).xf(trans(s * 17.45, 0.15, -6.1)))      # winglets
        # réacteurs sous les ailes
        ex = s * 6.2
        ms.append(cyl(1.05, 0.9, 4.4, 12, (225, 227, 232)).xf(M(trans(ex, -2.45, -1.2), rotx(math.pi / 2))))
        ms.append(cyl(0.85, 0.85, 0.08, 12, (30, 30, 34)).xf(M(trans(ex, -2.45, 3.18), rotx(math.pi / 2))))
        ms.append(cyl(0.25, 0.1, 0.4, 8, (190, 190, 195)).xf(M(trans(ex, -2.45, 3.0), rotx(math.pi / 2))))
        ms.append(cyl(0.6, 0.45, 1.0, 10, (120, 120, 125)).xf(M(trans(ex, -2.45, -2.1), rotx(math.pi / 2))))
        ms.append(box(0.3, 0.8, 2.6, (210, 212, 216)).xf(trans(ex, -1.85, 0.4)))
        stab = slab([(0.5, -19.5), (7.2, -24.0), (7.2, -25.4), (0.5, -23.6)], 0.25, (215, 217, 222)).xf(trans(0, 0.9, 0))
        if s < 0:
            stab = stab.xf(scale(-1, 1, 1))
        ms.append(stab)
    ms.append(slab([(-17.5, 1.4), (-23.6, 8.6), (-25.4, 8.6), (-24.2, 1.4)], 0.35, livery, plane='zy'))
    ms.append(slab([(-21.6, 6.0), (-22.6, 7.2), (-24.0, 7.2), (-23.2, 6.0)], 0.4, (245, 245, 245), plane='zy'))   # logo blanc
    return merge(ms)


def truck(col=(190, 60, 40), roll=0.0):
    """semi-remorque américain (cabine longue à capot, vitres, phares, roues qui tournent), avant vers +z. roll = angle des roues"""
    c = np.asarray(C(col))
    ms = [box(2.4, 1.3, 2.4, col).xf(trans(0, 1.0, 6.6)),                    # cabine (bas)
          box(2.4, 0.4, 2.4, col).xf(trans(0, 3.1, 6.6)),                    # toit de cabine
          box(2.4, 0.8, 0.1, col).xf(trans(0, 2.3, 5.45)),                   # paroi arrière
          box(1.0, 0.6, 1.0, (50, 45, 40)).xf(trans(0.4, 2.3, 6.4)),           # siège
          box(2.2, 0.3, 0.4, (40, 40, 42)).xf(trans(0, 2.3, 7.55)),            # tableau de bord
          box(0.1, 0.8, 1.0, col).xf(trans(1.15, 2.3, 5.9)), box(0.1, 0.8, 1.0, col).xf(trans(-1.15, 2.3, 5.9)),
          box(0.1, 0.8, 0.2, col).xf(trans(1.15, 2.3, 7.7)), box(0.1, 0.8, 0.2, col).xf(trans(-1.15, 2.3, 7.7)),
          box(2.3, 1.25, 2.2, col).xf(trans(0, 1.0, 8.9)),                    # capot
          box(1.9, 1.0, 0.08, (180, 182, 186)).xf(trans(0, 1.1, 10.02)),      # calandre chromée
          box(2.45, 0.35, 0.3, (190, 190, 195)).xf(trans(0, 0.6, 10.1)),      # pare-chocs
          box(2.3, 0.08, 2.2, c * 0.8).xf(trans(0, 2.25, 8.9)),
          box(2.2, 1.6, 2.0, c * 0.9).xf(trans(0, 3.5, 5.9)),                 # couchette (sleeper)
          box(2.5, 3.0, 12, (230, 230, 226), 'planks_white', ts=4.0).xf(trans(0, 1.3, -1.6)),
          box(2.52, 0.25, 12.02, col).xf(trans(0, 1.3, -1.6)),
          box(2.4, 0.25, 12, (60, 60, 64)).xf(trans(0, 1.05, -1.6))]
    # vitres : pare-brise, vitres latérales
    ms.append(box(2.1, 0.95, 0.06, (120, 160, 190), alpha=0.45).xf(M(trans(0, 2.25, 7.83), rotx(-0.12))))
    for s in (-1, 1):
        ms.append(box(0.06, 0.8, 1.2, (120, 160, 190), alpha=0.4).xf(trans(s * 1.22, 2.3, 7.0)))
        ms.append(box(0.06, 0.25, 0.6, (60, 60, 64)).xf(trans(s * 1.22, 1.15, 7.4)))     # marchepied
        ms.append(box(0.1, 0.5, 0.25, (40, 40, 40)).xf(trans(s * 1.45, 2.4, 8.0)))       # rétroviseurs
        ms.append(box(0.4, 0.25, 0.06, (255, 245, 210), emis=0.8).xf(trans(s * 0.85, 1.25, 10.07)))   # phares
        ms.append(cyl(0.12, 0.12, 3.2, 6, (190, 190, 195)).xf(trans(s * 1.25, 1.6, 6.0)))  # cheminées
        ms.append(cyl(0.35, 0.35, 1.4, 8, (190, 190, 195)).xf(M(trans(s * 1.3, 0.75, 8.0), rotx(math.pi / 2), trans(0, -0.7, 0))))  # réservoirs
        # garde-boue
        ms.append(box(0.4, 0.1, 1.4, (40, 40, 42)).xf(trans(s * 1.05, 1.15, 9.2)))
    # roues : pneu + jante + rayons (la rotation se voit)
    for z in (9.2, 5.2, 3.9, -5.6, -6.9):
        for s in (-1, 1):
            ms.append(wheel(0.55, 0.32, roll, rim=(200, 200, 205)).xf(trans(s * 1.12, 0.55, z)))
    return merge(ms)


def wheel(r, w, roll=0.0, rim=(200, 200, 205), tyre=(25, 25, 28)):
    """roue posée sur l'axe x : pneu, jante, 5 rayons visibles qui tournent avec roll"""
    ms = [cyl(r, r, w, 12, tyre).xf(M(rotz(math.pi / 2), trans(0, -w / 2, 0)))]
    ms.append(cyl(r * 0.6, r * 0.6, w + 0.02, 10, rim).xf(M(rotz(math.pi / 2), trans(0, -(w + 0.02) / 2, 0))))
    for k in range(5):
        a = roll + k * 2 * math.pi / 5
        for sx in (-1, 1):
            ms.append(box(0.03, r * 0.45, 0.07, (60, 60, 65)).xf(M(trans(sx * (w / 2 + 0.012), 0, 0), rotx(a), trans(0, r * 0.12, 0))))
    ms.append(cyl(r * 0.18, r * 0.18, w + 0.06, 6, (90, 90, 95)).xf(M(rotz(math.pi / 2), trans(0, -(w + 0.06) / 2, 0))))
    return merge(ms)


# ================================================================== lot du 6 nov. (soir) : Poon Lim, Cher Ami, rayons X
import lib as _lib

tex_noise('ocean', (28, 92, 128), (48, 122, 156), seed=601, octaves=3, speck=0.04, speck_col=(200, 230, 240))
tex_noise('ocean_storm', (40, 60, 70), (65, 85, 95), seed=602, octaves=3, speck=0.03, speck_col=(170, 185, 195))
tex_noise('ocean_dusk', (40, 60, 95), (80, 80, 110), seed=603, octaves=3, speck=0.05, speck_col=(240, 170, 120))
tex_noise('hull_grey2', (88, 92, 96), (108, 112, 116), seed=604, octaves=1, speck=0.05, speck_col=(70, 60, 55))
tex_noise('hull_rust', (60, 58, 58), (85, 70, 62), seed=605, octaves=3, speck=0.12, speck_col=(130, 70, 40))
tex_noise('uboat', (95, 100, 104), (115, 120, 124), seed=606, octaves=2)
tex_noise('shark', (110, 118, 126), (130, 138, 146), seed=607, octaves=2)
tex_noise('olive', (82, 85, 55), (98, 100, 66), seed=608, octaves=1)
tex_noise('feldgrau', (95, 100, 88), (112, 116, 104), seed=609, octaves=1)
tex_noise('mud', (78, 62, 45), (102, 84, 60), seed=610, octaves=3, speck=0.1, speck_col=(60, 48, 35))
tex_noise('leaves_autumn', (150, 90, 35), (190, 130, 50), seed=611, octaves=3, speck=0.15, speck_col=(110, 60, 25))
tex_noise('pigeon', (110, 118, 135), (135, 142, 158), seed=612, octaves=2, speck=0.1, speck_col=(70, 75, 90))
tex_noise('wallpaper_red', (120, 55, 50), (140, 70, 62), seed=613, octaves=1, speck=0.1, speck_col=(170, 120, 70))
tex_noise('dress_dark', (55, 35, 45), (72, 48, 60), seed=614, octaves=1)
tex_noise('suit_dark', (40, 40, 46), (54, 54, 62), seed=615, octaves=1)
tex_noise('hospital', (215, 225, 225), (232, 240, 240), seed=616, octaves=1)
tex_noise('straw', (200, 170, 100), (225, 195, 125), seed=617, octaves=2, speck=0.15, speck_col=(170, 140, 80))
tex_stripes('ribbon_cdg', (40, 120, 60), (200, 40, 40), n=8, vertical=True)


def _flag_us(d, n):
    d.rectangle([0, 0, n, n], fill=(240, 240, 240))
    for k in range(0, n, 5):
        d.rectangle([0, k, n, k + 2], fill=(180, 35, 45))
    d.rectangle([0, 0, n // 2, n // 2], fill=(40, 50, 110))
    for i in range(2, n // 2, 4):
        for j in range(2, n // 2, 4):
            d.point((i, j), fill=(255, 255, 255))


tex_draw('flag_us', _flag_us)


def _star_roundel(d, n):
    d.rectangle([0, 0, n, n], fill=(150, 155, 150))
    d.ellipse([3, 3, n - 4, n - 4], fill=(30, 45, 110))
    c, r = n / 2, n / 2 - 5
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts.append((c + rr * math.cos(a), c + rr * math.sin(a)))
    d.polygon(pts, fill=(245, 245, 245))


tex_draw('star_roundel', _star_roundel)


def _note_paper(d, n):
    d.rectangle([0, 0, n, n], fill=(238, 232, 210))
    for y in range(4, n - 2, 4):
        d.line([3, y, n - 4 - (y * 7) % 9, y], fill=(60, 60, 80))


tex_draw('note', _note_paper)


def _newspaper(d, n):
    d.rectangle([0, 0, n, n], fill=(225, 220, 200))
    d.rectangle([2, 2, n - 3, 6], fill=(30, 30, 30))
    d.rectangle([3, 9, 15, 25], fill=(70, 70, 70))
    d.ellipse([5, 11, 13, 22], fill=(200, 200, 200))
    for y in range(9, n - 3, 3):
        d.line([18, y, n - 3, y], fill=(110, 110, 105))
    for y in range(27, n - 2, 3):
        d.line([3, y, 15, y], fill=(110, 110, 105))


tex_draw('newspaper', _newspaper)


def _map_fr(d, n):
    d.rectangle([0, 0, n, n], fill=(220, 210, 175))
    for k in range(0, n, 6):
        d.line([k, 0, k + 4, n], fill=(200, 190, 150))
    d.line([4, 22, 14, 16, 22, 18, 28, 8], fill=(60, 90, 150), width=1)


tex_draw('map_old', _map_fr)


# ------------------------------------------------------------------ casques (14-18)
_old_hat_mesh = _lib.hat_mesh


def _hat_mesh8(kind, col):
    col = C(col)
    if kind == 'brodie':   # casque américain/anglais : bord large plat + petite coque
        return merge([cyl(0.3, 0.3, 0.02, 14, col), sphere(0.2, 10, 4, col, sy=0.55).xf(trans(0, 0.0, 0)),
                      cyl(0.302, 0.302, 0.02, 14, col * 0.75, caps=False).xf(trans(0, -0.005, 0))])
    if kind == 'stahl':    # casque allemand : coque haute + jupe évasée sur les côtés
        return merge([sphere(0.165, 10, 5, col, sy=0.95).xf(trans(0, 0.0, -0.01)), cyl(0.2, 0.165, 0.09, 12, col, caps=False).xf(trans(0, -0.09, -0.01))])
    if kind == 'straw':    # chapeau de paille des pêcheurs
        return merge([cyl(0.31, 0.31, 0.02, 12, col, 'straw'), cyl(0.17, 0.15, 0.13, 10, col, 'straw')])
    if kind == 'garrison':  # calot d'officier
        return box(0.26, 0.07, 0.25, col).xf(trans(0, 0.02, 0))
    if kind == 'sailor_cap':  # casquette d'officier de marine
        return merge([cyl(0.15, 0.17, 0.08, 10, (245, 245, 245)), box(0.22, 0.015, 0.11, (25, 25, 30)).xf(trans(0, -0.0, 0.15)),
                      cyl(0.151, 0.151, 0.03, 10, (25, 25, 40), caps=False)])
    return _old_hat_mesh(kind, col)


_lib.hat_mesh = _hat_mesh8


# ------------------------------------------------------------------ mer, radeau, navires
def ocean(t=0.0, tex='ocean', size=2500, y=-0.06, ts=10.0, cx=0.0, cz=0.0, swell=0.0):
    """mer plane (pas de scintillement) qui défile doucement ; swell>0 -> petites vagues"""
    hf = (lambda x, z: y + swell * (math.sin(x * 0.35 + t * 1.6) * 0.5 + math.sin(z * 0.27 - t * 1.1) * 0.5)) if swell else (lambda x, z: y)
    m = grid(cx - size, cz - size, cx + size, cz + size, 30, 30, hf, (255, 255, 255), tex, ts)   # maillage fin : pas de triangles géants mal découpés près de la caméra
    m.uv = m.uv + np.array([t * 0.03, t * 0.015])
    return m


def near_waves(t, cx=0.0, cz=0.0, r=20, y=0.0, tex='ocean', amp=0.18):
    """bout de mer finement maillé autour du radeau : vraies petites vagues"""
    hf = lambda x, z: y + amp * (math.sin(x * 0.9 + t * 1.8) + math.sin(z * 0.7 - t * 1.3 + x * 0.3)) * 0.5 - 0.02
    m = grid(cx - r, cz - r, cx + r, cz + r, 18, 18, hf, (255, 255, 255), tex, 3.0)
    m.uv = m.uv + np.array([t * 0.05, t * 0.02])
    return m


def raft(knots=0, tin=True, canvas=True, flashlight=True):
    """radeau de 2,4 m : plancher posé sur 4 bidons à moitié dans l'eau. Plancher à y=0.32. Centre (0,0,0)"""
    ms = [box(2.4, 0.1, 2.4, (255, 255, 255), 'planks', ts=1.2).xf(trans(0, 0.22, 0))]
    for x in (-0.8, 0.8):
        ms.append(box(0.12, 0.12, 2.5, (110, 80, 50)).xf(trans(x, 0.12, 0)))
    for x in (-0.75, 0.75):
        for z in (-0.75, 0.75):
            ms.append(cyl(0.28, 0.28, 0.9, 8, (150, 150, 145), 'metal').xf(M(trans(x, 0.05, z - 0.45), rotx(math.pi / 2))))
    for x in (-1.15, 1.15):    # piquets aux coins + corde le long du bord
        for z in (-1.15, 1.15):
            ms.append(cyl(0.03, 0.03, 0.5, 4, (110, 80, 50)).xf(trans(x, 0.32, z)))
    for a, b in (((-1.15, 0.75, -1.15), (1.15, 0.75, -1.15)), ((1.15, 0.75, -1.15), (1.15, 0.75, 1.15)), ((-1.15, 0.75, -1.15), (-1.15, 0.75, 1.15))):
        ms.append(rod(a, b, 0.035, (200, 180, 130), n=4))
    if tin:
        ms.append(cyl(0.14, 0.14, 0.4, 8, (170, 165, 150), 'metal').xf(trans(0.85, 0.32, 0.85)))       # bidon d'eau
        ms.append(box(0.35, 0.22, 0.25, (120, 100, 70)).xf(trans(0.75, 0.32, 0.4)))                    # caisse de biscuits
    if flashlight:
        ms.append(flashlight_m().xf(M(trans(-0.7, 0.36, 0.9), roty(0.6))))
    if canvas:
        ms.append(box(0.9, 0.04, 0.6, (200, 190, 160), 'cloth').xf(M(trans(-0.6, 0.33, -0.7), roty(0.2))))
    # corde à nœuds (calendrier) accrochée au piquet arrière gauche
    if knots:
        a, b = np.array([-1.15, 0.8, 1.15]), np.array([-1.15, 0.36, 0.3])
        ms.append(rod(a, b, 0.03, (215, 195, 140), n=4))
        for k in range(min(knots, 12)):
            p = a + (b - a) * (0.1 + 0.8 * k / 12)
            ms.append(sphere(0.05, 5, 3, (190, 165, 110)).xf(trans(p)))
    return merge(ms)


def flashlight_m():
    return merge([cyl(0.04, 0.04, 0.22, 6, (60, 70, 60)).xf(M(rotz(math.pi / 2), trans(0, -0.11, 0))),
                  cyl(0.06, 0.045, 0.06, 6, (180, 180, 170)).xf(M(rotz(-math.pi / 2), trans(0, 0.11, 0))),
                  cyl(0.05, 0.05, 0.01, 6, (255, 245, 200), emis=0.6).xf(M(rotz(-math.pi / 2), trans(0, 0.17, 0)))])


def spring_m(n=7, r=0.025, L=0.18, col=(200, 200, 205)):
    """ressort hélicoïdal (le long de x)"""
    ms = []
    pts = [(L * k / (n * 6), r * math.cos(k * math.pi / 3), r * math.sin(k * math.pi / 3)) for k in range(n * 6 + 1)]
    for a, b in zip(pts[:-1], pts[1:]):
        ms.append(rod(a, b, 0.006, col, n=3))
    return merge(ms)


def hook_m(col=(200, 200, 205)):
    """hameçon tordu à partir du ressort"""
    pts = [(0, 0.12, 0), (0, 0.0, 0), (0.01, -0.03, 0), (0.035, -0.04, 0), (0.055, -0.02, 0), (0.055, 0.01, 0)]
    return merge([rod(a, b, 0.008, col, n=3) for a, b in zip(pts[:-1], pts[1:])])


def _hull(stations, y0, y1, col, tex, deck_col=(150, 120, 85), deck_tex='planks', ts=4.0, stripe=None):
    """coque simple symétrique, proue vers +x. stations=(x, demi-largeur pont, demi-largeur quille)"""
    tris, uvs = [], []
    for i in range(len(stations) - 1):
        xa, wa, ba = stations[i]
        xb, wb, bb = stations[i + 1]
        for s in (-1, 1):
            p = [(xa, y0, s * ba), (xb, y0, s * bb), (xb, y1, s * wb), (xa, y1, s * wa)]
            u = [(xa / ts, (y1 - y0) / ts), (xb / ts, (y1 - y0) / ts), (xb / ts, 0), (xa / ts, 0)]
            tris += [[p[0], p[1], p[2]], [p[0], p[2], p[3]]]
            uvs += [[u[0], u[1], u[2]], [u[0], u[2], u[3]]]
    ms = [Mesh(tris, C(col), uvs, TEXB[tex] if tex else 0)]
    xa, wa, ba = stations[0]
    ms.append(quad((xa, y0, -ba), (xa, y0, ba), (xa, y1, wa), (xa, y1, -wa), np.asarray(C(col)) * 0.9))
    dt = []
    for i in range(len(stations) - 1):
        xa, wa, _ = stations[i]
        xb, wb, _ = stations[i + 1]
        dt += [[(xa, y1, -wa), (xb, y1, -wb), (xb, y1, wb)], [(xa, y1, -wa), (xb, y1, wb), (xa, y1, wa)]]
    ms.append(Mesh(dt, C(deck_col), [[(0, 0), (1, 0), (1, 1)], [(0, 0), (1, 1), (0, 1)]] * (len(dt) // 2), TEXB[deck_tex] if deck_tex else 0))
    if stripe is not None:
        for s in (-1, 1):
            for i in range(len(stations) - 1):
                xa, wa, _ = stations[i]
                xb, wb, _ = stations[i + 1]
                ms.append(quad((xa, y1 - 0.5, s * (wa + 0.02)), (xb, y1 - 0.5, s * (wb + 0.02)), (xb, y1 - 0.15, s * (wb + 0.02)), (xa, y1 - 0.15, s * (wa + 0.02)), stripe))
    return merge(ms)


def cargo_ship(smoke=False, lights=False, list_=0.0):
    """cargo à vapeur des années 1920-40 (~80 m), proue vers +x, flottaison y=0 : coque grise rouillée, château, cheminée, 2 mâts + mâts de charge"""
    st = [(-40, 6.0, 3.5), (-36, 6.8, 5.0), (25, 6.8, 5.5), (33, 4.5, 2.5), (40, 0.4, 0.2)]
    ms = [_hull(st, -6.0, 5.0, (255, 255, 255), 'hull_rust', ts=6.0, stripe=(150, 40, 35))]
    ms.append(box(80, 1.6, 12.8, (130, 40, 35)).xf(trans(-2, -1.6, 0)))   # œuvres vives rouges à la flottaison
    # château central + passerelle
    ms.append(box(14, 3.2, 11, (225, 222, 210), 'window', ts=2.0).xf(trans(-2, 5.0, 0)))
    ms.append(box(9, 2.6, 9, (225, 222, 210), 'window', ts=2.0).xf(trans(-1, 8.2, 0)))
    ms.append(box(4, 2.4, 12.5, (225, 222, 210)).xf(trans(2.5, 8.2, 0)))
    # cheminée noire à bande rouge
    ms.append(cyl(1.6, 1.6, 7.0, 10, (35, 35, 38)).xf(M(trans(-5, 10.8, 0), rotz(0.08))))
    ms.append(cyl(1.62, 1.62, 1.0, 10, (170, 40, 35), caps=False).xf(M(trans(-5, 15.0, 0), rotz(0.08))))
    # château arrière + gouvernail
    ms.append(box(10, 2.6, 10, (225, 222, 210), 'window', ts=2.0).xf(trans(-33, 5.0, 0)))
    # écoutilles + mâts + mâts de charge
    for x in (-20, -12, 14, 22):
        ms.append(box(5, 0.8, 6, (60, 70, 60)).xf(trans(x, 5.0, 0)))
    for mx in (18, -16):
        ms.append(cyl(0.35, 0.22, 18, 6, (180, 170, 150)).xf(trans(mx, 5.0, 0)))
        ms.append(box(0.3, 0.3, 4, (180, 170, 150)).xf(trans(mx, 13, 0)))
        ms.append(rod((mx, 6.5, 0), (mx + 7 * (1 if mx > 0 else -1), 11, 0), 0.14, (170, 160, 140), n=4))
    ms.append(rod((18, 23, 0), (40, 5.2, 0), 0.06, (50, 50, 50), n=3))
    ms.append(rod((18, 23, 0), (-16, 23, 0), 0.06, (50, 50, 50), n=3))
    ms.append(rod((-16, 23, 0), (-40, 5.2, 0), 0.06, (50, 50, 50), n=3))
    # bastingage
    for s in (-1, 1):
        ms.append(box(58, 0.9, 0.08, (200, 198, 190)).xf(trans(-6, 5.0, s * 6.6)))
    # canot de sauvetage sur le château
    for s in (-1, 1):
        ms.append(box(5, 0.9, 1.6, (235, 235, 230)).xf(trans(-2, 8.3, s * 4.8)))
    if lights:
        for x in np.arange(-30, 25, 6):
            ms.append(box(0.4, 0.4, 0.2, (255, 225, 150), emis=1.0).xf(trans(x, 6.3, 6.7)))
    return merge(ms).xf(rotx(list_)) if list_ else merge(ms)


def uboat():
    """sous-marin allemand type IX en surface (~76 m), proue vers +x, flottaison y=0"""
    ms = [sphere(1.0, 12, 6, (255, 255, 255), 'uboat').xf(M(trans(0, -0.6, 0), scale(38, 3.0, 3.6)))]
    ms.append(box(52, 0.25, 4.2, (90, 85, 75), 'planks_grey').xf(trans(-2, 1.75, 0)))          # pont
    ms.append(box(8, 2.6, 3.0, (255, 255, 255), 'uboat').xf(trans(-3, 1.9, 0)))                  # kiosque
    ms.append(box(5.5, 0.9, 3.2, (255, 255, 255), 'uboat').xf(trans(-3.5, 4.5, 0)))
    ms.append(cyl(0.12, 0.12, 4, 4, (60, 60, 62)).xf(trans(-2.5, 5.4, 0)))                       # périscope
    ms.append(cyl(0.18, 0.18, 6, 6, (70, 72, 74)).xf(M(trans(8, 2.6, 0), rotz(-math.pi / 2 + 0.15), trans(0, 0, 0))))  # canon de pont
    ms.append(box(1.2, 1.0, 1.0, (80, 82, 84)).xf(trans(8, 2.0, 0)))
    ms.append(rod((-3, 5.4, 0), (35, 1.9, 0), 0.04, (40, 40, 40), n=3))
    ms.append(rod((-3, 5.4, 0), (-35, 1.9, 0), 0.04, (40, 40, 40), n=3))
    ms.append(box(1.4, 0.5, 0.8, (240, 240, 235)).xf(trans(-3, 3.9, 1.55)))                     # numéro (plaque)
    return merge(ms)


def torpedo():
    return merge([cyl(0.27, 0.27, 6.5, 8, (70, 72, 70)).xf(M(rotz(-math.pi / 2), trans(0, -3.2, 0))), sphere(0.27, 6, 4, (70, 72, 70)).xf(trans(3.3, 0, 0)),
                  box(0.08, 0.8, 0.08, (60, 60, 60)).xf(trans(-3.3, 0, 0)), box(0.08, 0.08, 0.8, (60, 60, 60)).xf(trans(-3.3, 0, 0))])


def wake_fx(a, b, t, cam, n=14, w=1.2, alpha=0.7):
    """sillage blanc de bulles le long du segment a->b"""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ms = []
    for k in range(n):
        u = (k + (t * 3) % 1.0) / n
        p = a + (b - a) * u
        s = w * (0.6 + 0.6 * u)
        ms.append(billboard(p + np.array([0, 0.1, 0]), s, s * 0.5, cam, (235, 245, 248), 'puff', emis=0.4, alpha=alpha * (1 - u * 0.5)))
    return merge(ms)


def shark(bend=0.0, jaw=0.0):
    """requin ~2,2 m, nez vers +x, dos vers +y. bend = queue qui fouette"""
    g, wh = (255, 255, 255), (230, 232, 230)
    ms = [sphere(1.0, 10, 5, g, 'shark').xf(M(scale(1.1, 0.26, 0.3)))]
    ms.append(sphere(1.0, 8, 4, wh).xf(M(trans(0.1, -0.08, 0), scale(0.95, 0.15, 0.24))))     # ventre blanc
    ms.append(slab([(0.15, 0.2), (-0.05, 0.62), (-0.35, 0.55), (-0.3, 0.2)], 0.05, (110, 118, 126), plane='zy').xf(roty(math.pi / 2)) if False else
              Mesh([[(0.2, 0.2, 0), (-0.25, 0.62, 0), (-0.35, 0.22, 0)]], C((105, 112, 120))))
    ms.append(Mesh([[(0.2, 0.2, 0.01), (-0.35, 0.22, 0.01), (-0.25, 0.62, 0.01)]], C((105, 112, 120))))
    tail = M(trans(-1.0, 0, 0), roty(bend))
    ms.append(sphere(1.0, 6, 4, g, 'shark').xf(M(tail, trans(-0.25, 0, 0), scale(0.35, 0.12, 0.12))))
    for s in (1, -1):
        ms.append(Mesh([[(-0.5, 0, 0), (-0.85, 0.45 * s, 0), (-0.7, 0.0, 0)], [(-0.5, 0, 0), (-0.7, 0.0, 0), (-0.85, 0.45 * s, 0)]], C((100, 108, 116))).xf(tail))
    for s in (-1, 1):        # nageoires pectorales
        ms.append(Mesh([[(0.4, -0.08, s * 0.25), (0.05, -0.22, s * 0.7), (0.15, -0.08, s * 0.25)], [(0.4, -0.08, s * 0.25), (0.15, -0.08, s * 0.25), (0.05, -0.22, s * 0.7)]],
                       C((105, 112, 120))))
        ms.append(box(0.06, 0.06, 0.02, (10, 10, 10)).xf(trans(0.85, 0.06, s * 0.17)))           # yeux
    ms.append(box(0.18, 0.03 + jaw * 0.08, 0.2, (90, 40, 45)).xf(trans(0.85, -0.1, 0)))           # gueule
    return merge(ms)


def gull(flap=0.0):
    """mouette, regarde +x, ailes qui battent"""
    w = (245, 245, 242)
    ms = [sphere(0.12, 6, 4, w).xf(scale(1.8, 0.8, 0.8)), sphere(0.07, 5, 3, w).xf(trans(0.22, 0.06, 0)),
          box(0.07, 0.02, 0.02, (230, 180, 50)).xf(trans(0.31, 0.05, 0)), box(0.1, 0.02, 0.12, (90, 90, 95)).xf(trans(-0.25, 0.0, 0))]
    a = 0.6 * math.sin(flap)
    for s in (-1, 1):
        ms.append(box(0.16, 0.015, 0.45, (200, 202, 205)).xf(M(trans(0, 0.04, s * 0.05), rotx(s * a), trans(0, 0, s * 0.22))))
        ms.append(box(0.1, 0.016, 0.18, (40, 40, 45)).xf(M(trans(0, 0.04, s * 0.05), rotx(s * a), trans(-0.02, 0, s * 0.48))))
    return merge(ms)


def fish_m(col=(190, 200, 205), L=0.35):
    return merge([sphere(L / 2, 6, 4, col).xf(scale(1.0, 0.45, 0.22)),
                  Mesh([[(-L / 2, 0, 0), (-L * 0.8, L * 0.2, 0), (-L * 0.8, -L * 0.2, 0)], [(-L / 2, 0, 0), (-L * 0.8, -L * 0.2, 0), (-L * 0.8, L * 0.2, 0)]], C(col))])


def patrol_plane(prop=0.0):
    """hydravion de patrouille américain (type Catalina), nez vers +z, ~20 m"""
    gr = (150, 155, 150)
    ms = [sphere(1.0, 10, 5, gr).xf(M(scale(1.3, 1.5, 9.0)))]
    ms.append(box(2.0, 0.6, 9, (235, 235, 232)).xf(trans(0, -1.2, 1)))           # coque claire en dessous
    ms.append(box(1.4, 0.6, 1.4, (40, 55, 75)).xf(trans(0, 1.2, 5.0)))           # vitres cockpit
    for s in (-1, 1):
        ms.append(sphere(0.8, 6, 3, (120, 150, 170), alpha=0.6).xf(trans(s * 1.0, 0.6, -2.5)))   # bulles d'observation
    ms.append(box(2.0, 1.6, 2.6, gr).xf(trans(0, 1.6, 0.5)))                     # pylône
    wing = box(32, 0.35, 3.0, gr).xf(trans(0, 3.2, 0.5))
    ms.append(wing)
    for s in (-1, 1):
        ms.append(box(1.6, 0.05, 1.6, (255, 255, 255), 'star_roundel').xf(trans(s * 11, 3.4, 0.5)))
        ex = s * 4.0
        ms.append(cyl(0.75, 0.6, 4.0, 10, gr).xf(M(trans(ex, 3.0, -1.0), rotx(math.pi / 2))))
        for k in range(3):
            a = prop + k * 2 * math.pi / 3
            ms.append(box(0.18, 1.6, 0.06, (40, 40, 40)).xf(M(trans(ex, 3.0, 3.1), rotz(a), trans(0, 0.8, 0))))
        ms.append(box(0.3, 1.8, 0.8, gr).xf(trans(s * 14.5, 2.2, 0.5)))           # flotteurs de bout d'aile
        ms.append(box(0.6, 0.4, 2.0, gr).xf(trans(s * 14.5, 1.2, 0.5)))
    ms.append(cyl(0.6, 0.25, 7, 8, gr).xf(M(trans(0, 0.6, -8.0), rotx(-math.pi / 2 + 0.1))))
    ms.append(slab([(0, 0), (-2.0, 3.6), (-3.4, 3.6), (-3.0, 0)], 0.25, gr, plane='zy').xf(trans(0, 1.0, -12.5)))
    ms.append(box(8, 0.2, 1.6, gr).xf(trans(0, 1.4, -14.2)))
    return merge(ms)


def fishing_boat(sail=True, emu=False):
    """barque de pêcheurs brésiliens (~7 m) : coque en bois, mât et voile triangulaire. proue vers +x, flottaison y=0"""
    st = [(-3.4, 0.9, 0.5), (-2.6, 1.15, 0.6), (1.8, 1.15, 0.6), (3.2, 0.5, 0.2), (3.7, 0.05, 0.05)]
    ms = [_hull(st, -0.55, 0.65, (255, 255, 255), 'planks_green', deck_col=(130, 95, 60), ts=2.0, stripe=(200, 170, 60))]
    ms.append(box(0.25, 0.08, 2.2, (110, 80, 50)).xf(trans(-0.6, 0.7, 0)))     # banc
    ms.append(box(0.25, 0.08, 2.2, (110, 80, 50)).xf(trans(1.0, 0.7, 0)))
    ms.append(cyl(0.07, 0.05, 5.5, 5, (150, 115, 70)).xf(trans(0.6, 0.65, 0)))
    if sail:
        ms.append(Mesh([[(0.65, 1.0, 0.02), (0.65, 6.0, 0.02), (-2.6, 1.1, 0.02)], [(0.65, 1.0, 0.0), (-2.6, 1.1, 0.0), (0.65, 6.0, 0.0)]],
                       C((235, 225, 200)), [[(0, 1), (0, 0), (1, 1)]] * 2, TEXB['cloth']))
        ms.append(rod((0.6, 1.05, 0), (-2.7, 1.05, 0), 0.04, (150, 115, 70), n=3))
    ms.append(box(1.0, 0.25, 0.6, (110, 90, 60)).xf(trans(-2.4, 0.65, 0.2)))   # panier de poissons
    for k in range(4):
        ms.append(fish_m().xf(M(trans(-2.4 + k * 0.12 - 0.2, 0.9, 0.2), roty(k))))
    if emu:   # petite sculpture d'émeu en bois, clouée sur l'étrave
        ms.append(cyl(0.12, 0.14, 0.12, 6, (120, 85, 50)).xf(trans(3.0, 0.65, 0)))
        ms.append(emu_mesh((3.0, 0.77, 0), math.pi / 2, scale_=0.32, statue=(150, 105, 60)))
    return merge(ms)


def storm_rain(cam, t, n=160, area=16, col=(185, 195, 205)):
    return C2.rain_mesh(cam, t, n=n, area=area, col=col, slant=(0.3, 0, 0.1))


# ------------------------------------------------------------------ pigeons
def pigeon(flap=0.0, fly=True, leg_hurt=False, capsule=True, wood_leg=False, pose='fly', col=None):
    """pigeon voyageur ~0,33 m, regarde +z. flap = phase des ailes. pose : fly / stand / fall"""
    tex = 'pigeon' if col is None else 0
    c = (255, 255, 255) if col is None else col
    dark = (70, 75, 92) if col is None else np.asarray(col) * 0.6
    body = M(rotx(0.0 if pose != 'stand' else -0.35))
    ms = [sphere(0.09, 8, 5, c, tex).xf(M(body, scale(0.85, 0.85, 1.35)))]
    ms.append(sphere(0.07, 7, 4, (95, 130, 115) if col is None else c).xf(M(body, trans(0, 0.04, 0.09), scale(1, 1, 0.8))))   # gorge irisée
    ms.append(sphere(0.05, 7, 4, c, tex).xf(M(body, trans(0, 0.09, 0.14))))                                                    # tête
    ms.append(box(0.022, 0.018, 0.045, (40, 38, 40)).xf(M(body, trans(0, 0.085, 0.2))))                                       # bec
    ms.append(box(0.02, 0.012, 0.02, (235, 235, 225)).xf(M(body, trans(0, 0.098, 0.18))))                                     # cire
    for s in (-1, 1):
        ms.append(box(0.012, 0.018, 0.018, (200, 90, 40)).xf(M(body, trans(s * 0.045, 0.1, 0.16))))                           # yeux orange
    ms.append(box(0.09, 0.015, 0.14, dark).xf(M(body, trans(0, 0.0, -0.17), rotx(-0.1))))                                     # queue
    ms.append(box(0.092, 0.012, 0.03, (30, 30, 35)).xf(M(body, trans(0, 0.0, -0.23))))
    if pose == 'fly' or pose == 'fall':
        a = 0.9 * math.sin(flap) if pose == 'fly' else 0.4 + 0.3 * math.sin(flap * 2)
        for s in (-1, 1):
            sh = M(body, trans(s * 0.06, 0.04, 0.02), rotz(s * a))
            ms.append(box(0.17, 0.012, 0.12, c, tex).xf(M(sh, trans(s * 0.09, 0, 0))))
            ms.append(box(0.12, 0.012, 0.09, dark).xf(M(sh, trans(s * 0.22, 0, -0.01), rotz(s * a * 0.4))))
            ms.append(box(0.09, 0.014, 0.025, (35, 35, 40)).xf(M(sh, trans(s * 0.11, 0.002, -0.03))))                        # barre noire
    else:
        for s in (-1, 1):
            ms.append(box(0.025, 0.07, 0.17, c, tex).xf(M(body, trans(s * 0.075, 0.01, -0.03))))
            ms.append(box(0.027, 0.03, 0.06, (35, 35, 40)).xf(M(body, trans(s * 0.077, 0.0, -0.05))))
    # pattes : gauche normale, droite (porte la capsule) presque arrachée si leg_hurt
    legs = []
    for s in (-1, 1):
        hurt = leg_hurt and s > 0
        top = M(body, trans(s * 0.03, -0.07, 0.0))
        if pose == 'stand':
            if wood_leg and s > 0:   # petite patte de bois taillée par les soldats : cheville tournée, 2 bagues sculptées, pied rond
                legs.append(cyl(0.006, 0.011, 0.085, 6, (175, 130, 75)).xf(M(top, trans(0, -0.085, 0))))
                for yy in (-0.03, -0.055):
                    legs.append(cyl(0.0125, 0.0125, 0.006, 6, (120, 85, 45)).xf(M(top, trans(0, yy, 0))))
                legs.append(cyl(0.016, 0.016, 0.006, 8, (150, 110, 60)).xf(M(top, trans(0, -0.088, 0.004))))
            elif not hurt:
                legs.append(box(0.012, 0.07, 0.012, (200, 90, 90)).xf(M(top, trans(0, -0.07, 0))))
                for a_ in (-0.4, 0, 0.4):
                    legs.append(box(0.008, 0.006, 0.04, (200, 90, 90)).xf(M(top, trans(0, -0.07, 0), roty(a_), trans(0, 0, 0.02))))
        else:
            ang = 1.1 if not hurt else 2.2
            legs.append(box(0.012, 0.06, 0.012, (200, 90, 90)).xf(M(top, rotx(ang), trans(0, -0.03, 0))))
        if capsule and s > 0:
            ang = 1.1 if pose != 'stand' else 0.0
            if hurt:
                cp = M(top, trans(0, -0.08, -0.03))
                legs.append(rod((0, 0, 0), (0, -0.05, -0.02), 0.004, (200, 90, 90), n=3).xf(top))
            else:
                cp = M(top, rotx(ang), trans(0, -0.045, 0))
            legs.append(cyl(0.012, 0.012, 0.045, 6, (150, 155, 150)).xf(cp))
    return merge(ms + legs)


def pigeon_basket(n=2):
    ms = [box(0.6, 0.4, 0.4, (180, 150, 100), 'straw').xf(trans(0, 0, 0)), box(0.62, 0.04, 0.42, (140, 110, 70)).xf(trans(0, 0.4, 0))]
    for x in np.linspace(-0.25, 0.25, 6):
        ms.append(box(0.015, 0.25, 0.01, (90, 70, 40)).xf(trans(x, 0.1, 0.205)))
    for k in range(n):
        ms.append(pigeon(pose='stand', capsule=False).xf(M(trans(-0.15 + k * 0.28, 0.14, 0.05), scale(0.9))))
    return merge(ms)


def dna_helix(t=0.0, n=16, h=1.6, r=0.25):
    ms = []
    for k in range(n):
        a = t + k * 0.6
        y = k * h / n
        p1, p2 = np.array([r * math.cos(a), y, r * math.sin(a)]), np.array([-r * math.cos(a), y, -r * math.sin(a)])
        ms.append(sphere(0.045, 5, 3, (80, 150, 230), emis=0.5).xf(trans(p1)))
        ms.append(sphere(0.045, 5, 3, (230, 90, 120), emis=0.5).xf(trans(p2)))
        ms.append(rod(p1, p2, 0.015, [(240, 200, 60), (80, 200, 120)][k % 2], n=3))
    return merge(ms)


def _ribbon_cdg(d, n):
    """ruban de la croix de guerre 1914-1918 : vert, bords rouges, 7 fines raies rouges"""
    d.rectangle([0, 0, n, n], fill=(40, 125, 60))
    d.rectangle([0, 0, 1, n], fill=(200, 40, 40))
    d.rectangle([n - 2, 0, n, n], fill=(200, 40, 40))
    for k in range(7):
        x = 5 + k * 3.4
        d.line([x, 0, x, n], fill=(200, 40, 40))


tex_draw('ribbon_cdg2', _ribbon_cdg)


def croix_de_guerre():
    """croix de guerre 1914-1918 (~4 cm) : croix pattée en bronze, 2 épées croisées, médaillon central, anneau, ruban vert et rouge.
    face vers +z, centre de la croix à l'origine"""
    br, br2, br3 = (165, 120, 55), (205, 160, 80), (120, 85, 40)
    ms = []
    for k in range(4):     # 4 branches évasées (croix pattée)
        arm = slab([(-0.003, 0.003), (0.003, 0.003), (0.0085, 0.02), (-0.0085, 0.02)], 0.003, br, plane='xz')
        ms.append(arm.xf(M(rotz(k * math.pi / 2), rotx(-math.pi / 2))))
        ms.append(box(0.016, 0.002, 0.004, br3).xf(M(rotz(k * math.pi / 2), trans(0, 0.0185, 0.0))))   # liseré au bout
    for k in (1, 3):       # deux épées croisées entre les branches
        a = k * math.pi / 4 + (0 if k == 1 else math.pi / 2)
        ms.append(box(0.0022, 0.05, 0.0025, br2).xf(M(rotz(a), trans(0, -0.025, 0.0015))))
        for e in (-1, 1):
            ms.append(box(0.007, 0.002, 0.003, br3).xf(M(rotz(a), trans(0, e * 0.017, 0.002))))      # gardes
    ms.append(cyl(0.0075, 0.0075, 0.004, 12, br2).xf(M(rotx(math.pi / 2), trans(0, -0.001, 0))))      # médaillon (Marianne)
    ms.append(cyl(0.0052, 0.0052, 0.0045, 10, br3).xf(M(rotx(math.pi / 2), trans(0, -0.0015, 0))))
    ms.append(box(0.004, 0.005, 0.0042, br2).xf(trans(0, -0.003, 0.0012)))                             # profil
    # anneau + ruban
    for k in range(8):
        a0, a1 = k * math.pi / 4, (k + 1) * math.pi / 4
        ms.append(rod((0.004 * math.cos(a0), 0.0245 + 0.004 * math.sin(a0), 0), (0.004 * math.cos(a1), 0.0245 + 0.004 * math.sin(a1), 0), 0.0009, br2, n=3))
    ms.append(box(0.036, 0.042, 0.0015, (255, 255, 255), 'ribbon_cdg2').xf(trans(0, 0.029, -0.001)))
    ms.append(box(0.038, 0.004, 0.003, br2).xf(trans(0, 0.07, -0.001)))                                 # barrette
    return merge(ms)


# ------------------------------------------------------------------ rayons X (1895)
def crookes_tube(glow=0.0):
    """tube de Crookes en verre sur son support, axe le long de x"""
    ms = [box(0.4, 0.03, 0.2, (90, 60, 35)).xf(trans(0, 0, 0)), cyl(0.012, 0.012, 0.25, 4, (60, 60, 62)).xf(trans(0, 0.03, 0))]
    gc = (120 + 120 * glow, 200 + 55 * glow, 140 + 60 * glow)
    ms.append(sphere(0.09, 8, 5, gc, alpha=0.45, emis=0.3 + 0.6 * glow).xf(M(trans(0, 0.3, 0), scale(1.6, 1, 1))))
    for s in (-1, 1):
        ms.append(cyl(0.025, 0.02, 0.1, 6, gc, alpha=0.5).xf(M(trans(s * 0.15, 0.3, 0), rotz(-s * math.pi / 2))))
        ms.append(cyl(0.006, 0.006, 0.06, 3, (180, 160, 90)).xf(M(trans(s * 0.25, 0.3, 0), rotz(-s * math.pi / 2))))
    return merge(ms)


def black_box(w=0.42, h=0.26, d=0.24):
    """le carton noir qui cache le tube"""
    return box(w, h, d, (22, 22, 24)).xf(trans(0, 0.17, 0))


def induction_coil():
    """bobine de Ruhmkorff"""
    return merge([box(0.5, 0.05, 0.22, (100, 65, 40)), cyl(0.08, 0.08, 0.38, 10, (150, 90, 40)).xf(M(trans(-0.19, 0.13, 0), rotz(-math.pi / 2))),
                  cyl(0.082, 0.082, 0.05, 10, (40, 30, 25)).xf(M(trans(-0.2, 0.13, 0), rotz(-math.pi / 2))),
                  cyl(0.082, 0.082, 0.05, 10, (40, 30, 25)).xf(M(trans(0.15, 0.13, 0), rotz(-math.pi / 2))),
                  cyl(0.008, 0.008, 0.12, 3, (200, 180, 90)).xf(trans(0.1, 0.21, 0.05)), cyl(0.008, 0.008, 0.12, 3, (200, 180, 90)).xf(trans(-0.1, 0.21, 0.05))])


def hand_image(bones=True, ring=False, bg=(150, 220, 120), flesh=(120, 180, 95), bone=(45, 70, 40), ring_col=(15, 15, 15), fracture=False, coin=False):
    """image d'une main « aux rayons X » sur un plan (x,y), z=0 : silhouette + os + bague. ~0,22 m de haut"""
    ms = [box(0.26, 0.34, 0.004, bg, emis=0.9 if bg[1] > 180 else 0.0).xf(trans(0, -0.205, -0.004))]
    em = 0.6 if bg[1] > 180 else 0.0
    ms.append(box(0.1, 0.1, 0.004, flesh, emis=em).xf(trans(0, -0.07, 0)))                   # paume
    ms.append(box(0.06, 0.07, 0.004, flesh, emis=em).xf(trans(0, -0.13, 0)))                 # poignet
    fingers = [(-0.042, 0.075, 0.0), (-0.015, 0.09, 0.0), (0.013, 0.085, 0.0), (0.038, 0.068, 0.0)]
    for k, (x, L, a) in enumerate(fingers):
        ms.append(box(0.022, L, 0.004, flesh, emis=em).xf(trans(x, 0.03, 0.0)))
    ms.append(box(0.024, 0.075, 0.004, flesh, emis=em).xf(M(trans(-0.045, -0.06, 0.0), rotz(0.75))))   # pouce (part du bord de la paume)
    if bones:
        bz = 0.003
        for x in (-0.035, -0.012, 0.012, 0.034):
            ms.append(box(0.008, 0.07, 0.004, bone).xf(trans(x, -0.09, bz)))                    # métacarpes
        for k, (x, L, a) in enumerate(fingers):
            seg = L / 3.3
            for j in range(3):
                ms.append(box(0.009, seg * 0.85, 0.004, bone).xf(trans(x, 0.03 + j * seg * 1.05, bz)))
        ms.append(box(0.009, 0.03, 0.004, bone).xf(M(trans(-0.047, -0.058, bz), rotz(0.75))))
        ms.append(box(0.009, 0.03, 0.004, bone).xf(M(trans(-0.068, -0.037, bz), rotz(0.75))))
        ms.append(box(0.04, 0.022, 0.004, bone).xf(trans(0, -0.135, bz)))                       # carpes
        for x in (-0.012, 0.012):
            ms.append(box(0.01, 0.05, 0.004, bone).xf(trans(x, -0.17, bz)))                      # radius / cubitus
        if fracture:
            ms.append(box(0.012, 0.004, 0.005, bg).xf(M(trans(-0.012, -0.165, bz + 0.001), rotz(0.4))))
    if ring:
        ms.append(box(0.03, 0.012, 0.005, ring_col).xf(trans(0.013, 0.048, 0.005)))   # alliance sur la 1re phalange de l'annulaire
    if coin:
        ms.append(cyl(0.02, 0.02, 0.004, 8, (15, 15, 15)).xf(M(rotx(math.pi / 2), trans(0.0, 0.0, 0.07))))
    return merge(ms)


def xray_screen(lit=0.0, hand=False, bones=True):
    """écran fluorescent (platinocyanure de baryum) sur pied"""
    g = (40 + 130 * lit, 45 + 190 * lit, 30 + 100 * lit)
    ms = [box(0.04, 0.3, 0.04, (80, 55, 35)).xf(trans(0, 0, 0)), box(0.3, 0.02, 0.2, (80, 55, 35)).xf(trans(0, 0, 0)),
          box(0.34, 0.34, 0.03, (70, 48, 30)).xf(trans(0, 0.3, -0.02))]
    ms.append(box(0.3, 0.3, 0.01, g, emis=min(1.0, lit * 1.2)).xf(trans(0, 0.32, 0.0)))
    if hand and lit > 0.2:
        ms.append(hand_image(bones=bones, bg=g, flesh=(np.asarray(g) * 0.72), bone=(np.asarray(g) * 0.3)).xf(M(trans(0, 0.49, 0.012), scale(0.85))))
    return merge(ms)


def photo_plate(t_dev=1.0, ring=True):
    """plaque photo développée : la main d'Anna, os + bague (négatif tiré en positif)"""
    k = max(0.0, min(1.0, t_dev))
    bg = (190 * k + 40 * (1 - k),) * 3
    return merge([box(0.36, 0.44, 0.01, (60, 50, 40)).xf(trans(0, -0.26, -0.01)),
                  hand_image(True, ring, bg=bg, flesh=(150 * k + 40 * (1 - k),) * 3, bone=(70 * k + 40 * (1 - k),) * 3, ring_col=(10, 10, 10)).xf(M(trans(0, 0.0, 0.002), scale(1.15)))])


def gas_lamp(on=True):
    return merge([cyl(0.08, 0.1, 0.03, 8, (150, 120, 60)), cyl(0.015, 0.015, 0.2, 4, (150, 120, 60)),
                  sphere(0.08, 7, 4, (255, 230, 160) if on else (120, 110, 90), alpha=0.7, emis=0.9 if on else 0.0).xf(trans(0, 0.27, 0))])


def xray_machine():
    """appareil de radio moderne : table + bras + tête émettrice + écran"""
    ms = [box(2.0, 0.08, 0.8, (235, 238, 240)).xf(trans(0, 0.85, 0)), box(0.8, 0.85, 0.6, (200, 205, 210)).xf(trans(0, 0, 0)),
          box(0.12, 2.2, 0.12, (220, 222, 226)).xf(trans(-1.2, 0, -0.5)), box(1.3, 0.12, 0.12, (220, 222, 226)).xf(trans(-0.6, 2.1, -0.5)),
          box(0.5, 0.35, 0.45, (240, 240, 242)).xf(trans(0, 1.65, -0.3)), box(0.42, 0.04, 0.38, (60, 65, 70)).xf(trans(0, 1.63, -0.3)),
          box(0.5, 0.02, 0.4, (90, 100, 110)).xf(trans(0, 0.93, -0.05))]
    ms.append(box(0.06, 0.06, 0.06, (255, 200, 60), emis=1.0).xf(trans(0.2, 1.85, -0.08)))
    return merge(ms)


def monitor(img_mesh=None):
    ms = [box(0.7, 0.45, 0.05, (25, 25, 28)).xf(trans(0, 0, 0)), box(0.64, 0.39, 0.01, (15, 18, 22), emis=0.5).xf(trans(0, 0.03, 0.027)),
          box(0.06, 0.4, 0.06, (40, 40, 44)).xf(trans(0, -0.4, -0.02)), box(0.3, 0.03, 0.2, (40, 40, 44)).xf(trans(0, -0.4, -0.02))]
    if img_mesh is not None:
        ms.append(img_mesh.xf(M(trans(0, 0.24, 0.035), scale(1.1))))
    return merge(ms)
