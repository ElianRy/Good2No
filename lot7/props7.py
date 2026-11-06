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
