"""Bibliothèque commune : textures procédurales, personnages, décors génériques."""
import math
import numpy as np
from engine import *

RNG = np.random.default_rng(7)
T = TEX


def _noise(scale=1.0, seed=0, octaves=3):
    r = np.random.default_rng(seed)
    out = np.zeros((T, T))
    amp = 1.0
    for o in range(octaves):
        n = 2 ** (o + 2)
        g = r.random((n, n))
        # interpolation périodique
        xs = np.arange(T) / T * n
        i0 = np.floor(xs).astype(int) % n
        i1 = (i0 + 1) % n
        f = xs - np.floor(xs)
        f = f * f * (3 - 2 * f)
        a = g[i0][:, i0] * (1 - f)[None, :] + g[i0][:, i1] * f[None, :]
        b = g[i1][:, i0] * (1 - f)[None, :] + g[i1][:, i1] * f[None, :]
        out += amp * (a * (1 - f)[:, None] + b * f[:, None])
        amp *= 0.5
    out -= out.min()
    out /= out.max() + 1e-9
    return out


def _mix(c0, c1, t):
    c0, c1 = np.asarray(c0, float), np.asarray(c1, float)
    return (c0[None, None] * (1 - t[..., None]) + c1[None, None] * t[..., None]).clip(0, 255).astype(np.uint8)


def tex_noise(name, c0, c1, seed=0, octaves=3, speck=0.0, speck_col=None):
    n = _noise(seed=seed, octaves=octaves)
    img = _mix(c0, c1, n)
    if speck:
        r = np.random.default_rng(seed + 99)
        m = r.random((T, T)) < speck
        img[m] = speck_col if speck_col is not None else np.asarray(c0) * 0.7
    return TEXB.add(name, img)


def tex_planks(name, c0, c1, horizontal=True, n=4, seed=1):
    r = np.random.default_rng(seed)
    base = _noise(seed=seed, octaves=2) * 0.35
    img = np.zeros((T, T))
    w = T // n
    for i in range(n):
        tone = r.random() * 0.4
        if horizontal:
            img[i * w:(i + 1) * w, :] = tone
            img[i * w, :] = 1.2
        else:
            img[:, i * w:(i + 1) * w] = tone
            img[:, i * w] = 1.2
    # veines
    yy, xx = np.mgrid[0:T, 0:T]
    vein = (np.sin((xx if horizontal else yy) * 0.9 + base * 9) > 0.85) * 0.25
    t = np.clip(img + base + vein, 0, 1.3) / 1.3
    return TEXB.add(name, _mix(c1, c0, 1 - t))


def tex_bricks(name, brick, mortar, rows=8, cols=4, seed=2):
    r = np.random.default_rng(seed)
    img = np.zeros((T, T, 3), np.uint8)
    img[:] = mortar
    bh, bw = T // rows, T // cols
    for j in range(rows):
        off = (bw // 2) if j % 2 else 0
        for i in range(-1, cols + 1):
            x0 = i * bw + off + 1
            c = np.asarray(brick, float) * (0.85 + r.random() * 0.3)
            xa, xb = max(0, x0), min(T, x0 + bw - 1)
            if xb > xa:
                img[j * bh + 1:(j + 1) * bh, xa:xb] = c.clip(0, 255)
    return TEXB.add(name, img)


def tex_stripes(name, c0, c1, n=4, vertical=True):
    img = np.zeros((T, T, 3), np.uint8)
    w = T // (2 * n)
    for i in range(2 * n):
        c = c0 if i % 2 == 0 else c1
        if vertical:
            img[:, i * w:(i + 1) * w] = c
        else:
            img[i * w:(i + 1) * w, :] = c
    return TEXB.add(name, img)


def tex_draw(name, fn, bg=(255, 0, 255)):
    """fn(draw, T) via PIL, à 4x puis réduit (antialias limité) -> look pixel"""
    from PIL import Image, ImageDraw
    im = Image.new('RGB', (T, T), tuple(bg))
    d = ImageDraw.Draw(im)
    fn(d, T)
    return TEXB.add(name, np.asarray(im))


# ------------------------------------------------------------------ visages
SIMPLE_FACES = False   # règle Good2No : visages ultra simples (2 points), voir REGLES.md


def make_face(name, skin=(224, 172, 132), brows=True, brow_col=(60, 40, 25), mustache=False, beard=False,
              hair_col=(70, 50, 30), eye_col=(40, 30, 20), mouth='neutral', soot=0.0, fur=False, eyes_closed=False):
    sk = np.asarray(skin)

    def fn(d, n):
        d.rectangle([0, 0, n, n], fill=tuple(sk))
        if SIMPLE_FACES and not fur:
            for ex in (10, 19):
                if eyes_closed:
                    d.line([ex, 15, ex + 2, 15], fill=(35, 25, 20))
                else:
                    d.rectangle([ex, 14, ex + 2, 16], fill=(25, 20, 18))
            if beard or mustache:
                d.rectangle([4, 22, 27, 31] if beard else [10, 22, 21, 24], fill=tuple(hair_col))
            return
        # ombre joues
        d.rectangle([0, 0, n, 3], fill=tuple((sk * 0.85).astype(int)))
        # yeux
        ey = 13
        for ex in (8, 19):
            if eyes_closed:
                d.line([ex, ey + 2, ex + 4, ey + 2], fill=(40, 25, 20))
            else:
                d.rectangle([ex, ey, ex + 4, ey + 3], fill=(245, 245, 240))
                d.rectangle([ex + 1, ey, ex + 3, ey + 3], fill=tuple(eye_col))
                d.point([ex + 2, ey + 1], fill=(250, 250, 250))
            if brows:
                d.rectangle([ex - 1, ey - 3, ex + 5, ey - 2], fill=tuple(brow_col))
        # nez
        d.rectangle([14, 16, 17, 21], fill=tuple((sk * 0.82).astype(int)))
        d.rectangle([14, 21, 17, 22], fill=tuple((sk * 0.65).astype(int)))
        if beard:
            d.rectangle([4, 21, 27, 31], fill=tuple(hair_col))
            d.polygon([(2, 14), (5, 14), (5, 24), (2, 22)], fill=tuple(hair_col))
            d.polygon([(26, 14), (29, 14), (29, 22), (26, 24)], fill=tuple(hair_col))
        if mustache or beard:
            d.rectangle([10, 23, 21, 24], fill=tuple((np.asarray(hair_col) * 0.9).astype(int)))
        # bouche
        if mouth == 'open':
            d.rectangle([12, 25, 19, 28], fill=(70, 20, 20))
            d.rectangle([12, 25, 19, 25], fill=(240, 240, 235))
        elif mouth == 'smile':
            d.line([11, 25, 13, 27, 18, 27, 20, 25], fill=(120, 50, 45), width=1)
        elif mouth == 'shout':
            d.ellipse([12, 24, 19, 30], fill=(70, 20, 20))
        else:
            d.rectangle([12, 26, 19, 26], fill=(130, 60, 55))
        if soot > 0:
            r = np.random.default_rng(3)
            for _ in range(int(soot * 6)):
                x, y = r.integers(2, n - 6, 2)
                d.rectangle([int(x), int(y), int(x) + 3, int(y) + 1], fill=tuple((sk * 0.55).astype(int)))
    return tex_draw(name, fn)


# ------------------------------------------------------------------ textures de base
def build_base_textures():
    def clock(d, n):
        d.ellipse([0, 0, n - 1, n - 1], fill=(240, 235, 215))
        d.ellipse([0, 0, n - 1, n - 1], outline=(40, 40, 40), width=2)
        for k in range(12):
            a = k / 12 * 2 * math.pi
            x0, y0 = n / 2 + math.sin(a) * n * 0.34, n / 2 - math.cos(a) * n * 0.34
            x1, y1 = n / 2 + math.sin(a) * n * 0.44, n / 2 - math.cos(a) * n * 0.44
            d.line([x0, y0, x1, y1], fill=(30, 30, 30), width=2 if k % 3 == 0 else 1)
    tex_draw('clock_face', clock, bg=(255, 0, 255))
    tex_noise('grass', (70, 110, 45), (110, 150, 60), seed=1, speck=0.06, speck_col=(140, 170, 80))
    tex_noise('grass_dry', (130, 125, 70), (170, 160, 95), seed=2, speck=0.05, speck_col=(110, 100, 60))
    tex_noise('dirt', (110, 85, 60), (150, 120, 85), seed=3, speck=0.08, speck_col=(90, 70, 50))
    tex_noise('sand', (200, 180, 140), (225, 210, 170), seed=4, speck=0.05, speck_col=(180, 160, 120))
    tex_noise('rock', (105, 100, 95), (150, 145, 135), seed=5, octaves=4, speck=0.05, speck_col=(80, 75, 70))
    tex_noise('gravel', (120, 110, 100), (160, 150, 135), seed=6, octaves=1, speck=0.25, speck_col=(90, 85, 80))
    tex_noise('water', (40, 90, 120), (70, 130, 160), seed=7, speck=0.03, speck_col=(170, 210, 230))
    tex_noise('sea', (20, 120, 140), (50, 160, 170), seed=8, speck=0.03, speck_col=(190, 230, 230))
    tex_noise('plaster', (225, 220, 205), (245, 240, 228), seed=9, speck=0.04, speck_col=(200, 195, 180))
    tex_noise('plaster_old', (205, 195, 170), (235, 228, 210), seed=10, octaves=4, speck=0.06, speck_col=(170, 160, 140))
    tex_noise('metal', (120, 125, 130), (150, 155, 160), seed=11, octaves=1)
    tex_noise('rust', (110, 60, 35), (150, 90, 50), seed=12, speck=0.08)
    tex_noise('fur_baboon', (112, 102, 82), (135, 124, 100), seed=13, octaves=4, speck=0.07, speck_col=(95, 86, 70))
    tex_noise('fur_bear', (25, 22, 20), (50, 44, 38), seed=14, octaves=4, speck=0.1, speck_col=(15, 12, 10))
    tex_noise('fur_ox', (140, 90, 55), (170, 120, 80), seed=15, octaves=3, speck=0.08)
    tex_noise('bark', (80, 55, 35), (110, 80, 50), seed=16, octaves=2)
    tex_noise('needles', (30, 70, 40), (55, 100, 55), seed=17, speck=0.15, speck_col=(20, 50, 30))
    tex_noise('leaves', (55, 100, 40), (90, 140, 55), seed=18, speck=0.15, speck_col=(40, 80, 30))
    tex_noise('cloth', (200, 200, 200), (235, 235, 235), seed=19, octaves=1)
    tex_noise('ash', (60, 55, 50), (95, 88, 80), seed=20, speck=0.1)
    tex_noise('coral', (215, 205, 180), (240, 232, 210), seed=21, octaves=4, speck=0.1, speck_col=(180, 170, 145))
    tex_planks('planks', (150, 110, 70), (115, 80, 50))
    tex_planks('planks_v', (150, 110, 70), (115, 80, 50), horizontal=False)
    tex_planks('planks_grey', (150, 145, 135), (110, 105, 98), seed=4)
    tex_planks('planks_white', (235, 232, 222), (200, 195, 185), seed=5)
    tex_planks('planks_green', (80, 110, 70), (60, 85, 52), seed=6)
    tex_bricks('brick', (150, 70, 50), (190, 180, 160))
    tex_bricks('stone_block', (170, 160, 140), (120, 112, 100), rows=4, cols=2)
    tex_stripes('roof_tin', (150, 150, 145), (115, 115, 112), n=4)
    tex_stripes('roof_red', (160, 60, 45), (130, 45, 35), n=4)
    tex_stripes('awning', (230, 230, 220), (170, 40, 40), n=2)

    def rail(d, n):
        d.rectangle([0, 0, n, n], fill=(110, 100, 90))
        for i in range(0, n, 8):
            d.rectangle([0, i, n, i + 4], fill=(100, 70, 45))
    tex_draw('sleepers', rail)

    def window(d, n):
        d.rectangle([0, 0, n, n], fill=(60, 50, 40))
        d.rectangle([2, 2, n - 3, n - 3], fill=(90, 120, 140))
        d.line([n // 2, 2, n // 2, n - 3], fill=(60, 50, 40), width=2)
        d.line([2, n // 2, n - 3, n // 2], fill=(60, 50, 40), width=2)
        d.line([5, 5, 10, 10], fill=(170, 200, 210))
    tex_draw('window', window)

    def window_lit(d, n):
        d.rectangle([0, 0, n, n], fill=(60, 50, 40))
        d.rectangle([2, 2, n - 3, n - 3], fill=(240, 200, 110))
        d.line([n // 2, 2, n // 2, n - 3], fill=(60, 50, 40), width=2)
        d.line([2, n // 2, n - 3, n // 2], fill=(60, 50, 40), width=2)
    tex_draw('window_lit', window_lit)

    def door(d, n):
        d.rectangle([0, 0, n, n], fill=(95, 60, 35))
        d.rectangle([3, 3, n - 4, n // 2 - 2], outline=(70, 45, 25))
        d.rectangle([3, n // 2 + 2, n - 4, n - 4], outline=(70, 45, 25))
        d.rectangle([n - 8, n // 2, n - 6, n // 2 + 2], fill=(200, 170, 80))
    tex_draw('door', door)

    def fire(d, n):
        d.polygon([(n // 2, 0), (n - 4, n // 2), (n - 6, n - 1), (5, n - 1), (3, n // 2)], fill=(255, 140, 20))
        d.polygon([(n // 2, 8), (n - 9, n // 2 + 2), (n - 10, n - 1), (9, n - 1), (8, n // 2 + 2)], fill=(255, 210, 60))
        d.polygon([(n // 2, 17), (n - 13, n - 6), (n // 2, n - 1), (13, n - 6)], fill=(255, 250, 200))
    tex_draw('fire', fire)

    def smoke(d, n):
        for (x, y, r, c) in ((16, 18, 11, 95), (10, 14, 7, 105), (22, 12, 8, 110), (15, 10, 7, 125), (20, 20, 7, 100)):
            d.ellipse([x - r, y - r, x + r, y + r], fill=(c, c, c - 2))
    tex_draw('smoke', smoke)

    def puff(d, n):
        d.ellipse([1, 1, n - 2, n - 2], fill=(220, 220, 215))
        d.ellipse([6, 4, n - 8, n - 10], fill=(245, 245, 242))
    tex_draw('puff', puff)

    def spark(d, n):
        d.ellipse([4, 4, n - 5, n - 5], fill=(255, 200, 80))
        d.ellipse([10, 10, n - 11, n - 11], fill=(255, 255, 220))
    tex_draw('spark', spark)


# ------------------------------------------------------------------ personnages

# ------------------------------------------------------------------ cinématique inverse (mains qui saisissent)
_IK_CACHE = {}


def solve_arm(fk, target, x0, bounds, iters=60, key=None):
    """trouve les angles du bras pour que la main atteigne target (monde)."""
    from scipy.optimize import minimize
    tgt = np.asarray(target, float)
    lo, hi = np.array([b[0] for b in bounds]), np.array([b[1] for b in bounds])
    x0 = np.clip(np.asarray(x0, float), lo, hi)

    def f(a):
        d = fk(a) - tgt
        return float(d @ d) + 1e-4 * float(((a - x0) ** 2).sum())
    starts = []
    if key is not None and key in _IK_CACHE:
        starts.append(np.clip(_IK_CACHE[key], lo, hi))
    starts += [x0, (lo + hi) / 2]
    best = None
    for st in starts:
        r = minimize(f, st, method='L-BFGS-B', bounds=bounds, options=dict(maxiter=iters))
        if best is None or r.fun < best.fun:
            best = r
        if best.fun < 4e-4:
            break
    if key is not None:
        _IK_CACHE[key] = best.x
    return tuple(best.x)


def _human_hand(torso, side, tw, a):
    sp, sr, el = a
    sh = M(torso, trans(side * (tw / 2 + 0.06), 0.5, 0), rotx(-sp), rotz(side * sr))
    elb = M(sh, trans(0, -0.29, 0), rotx(-el))
    return M(elb, trans(0, -0.34, 0))[:3, 3]


def frame_along(a, b):
    """matrice dont l'axe +y va de a vers b (origine en a)"""
    a, b = np.asarray(a, float), np.asarray(b, float)
    y = b - a
    L = np.linalg.norm(y)
    y = y / (L + 1e-12)
    ref = np.array([0, 0, 1.0]) if abs(y[2]) < 0.9 else np.array([1.0, 0, 0])
    x = np.cross(y, ref)
    x /= np.linalg.norm(x)
    z = np.cross(x, y)
    m = np.eye(4)
    m[:3, 0], m[:3, 1], m[:3, 2], m[:3, 3] = x, y, z, a
    return m, L


def rod(a, b, r=0.02, col=(120, 85, 50), tex=0, n=5):
    m, L = frame_along(a, b)
    return cyl(r, r, L, n, col, tex).xf(m)


class Human:
    """humain low-poly articulé. Regarde vers +z. Taille ~1.78 m."""

    def __init__(self, face, skin=(224, 172, 132), shirt=(120, 120, 120), pants=(60, 60, 70), shoes=(40, 30, 25),
                 hair=(60, 45, 30), hat=None, hat_col=(150, 120, 80), sleeves='long', shirt_tex=None, pants_tex=None,
                 build=1.0, height=1.0, belt=None, robe=None, peg_legs=False, hair_style='short', extra=None,
                 tie=None, jacket=None):
        self.face = face
        self.skin, self.shirt, self.pants, self.shoes, self.hair = map(C, (skin, shirt, pants, shoes, hair))
        self.hat, self.hat_col = hat, C(hat_col)
        self.sleeves, self.shirt_tex, self.pants_tex = sleeves, shirt_tex, pants_tex
        self.build, self.height = build, height
        self.belt = C(belt) if belt is not None else None
        self.robe = C(robe) if robe is not None else None
        self.peg_legs = peg_legs
        self.hair_style = hair_style
        self.extra = extra  # fn(pose, attach dict) -> Mesh
        self.tie = C(tie) if tie is not None else None
        self.jacket = C(jacket) if jacket is not None else None

    def mesh(self, pos=(0, 0, 0), yaw=0.0, pose=None):
        P = dict(lean=0.0, side=0.0, hy=0.0, hp=0.0, la=(0, 0.08, 0.15), ra=(0, 0.08, 0.15),
                 ll=(0, 0), rl=(0, 0), drop=0.0, hair_fire=0, face=None, sit=False, hand_l=None, hand_r=None)
        if pose:
            P.update(pose)
        b, hs = self.build, self.height
        root = M(trans(pos), roty(yaw), scale(hs))
        ms = []
        tsh = TEXB[self.shirt_tex] if self.shirt_tex else 0
        tpa = TEXB[self.pants_tex] if self.pants_tex else 0
        hip_y = 0.93 - P['drop']
        pelvis = M(root, trans(0, hip_y, 0))
        attach = {}
        # bassin
        ms.append(box(0.36 * b, 0.16, 0.22 * b, self.pants, tpa).xf(M(pelvis, trans(0, -0.08, 0))))
        if self.belt is not None:
            ms.append(box(0.37 * b, 0.05, 0.23 * b, self.belt).xf(M(pelvis, trans(0, 0.0, 0))))
        # jambes
        for side, key in ((-1, 'll'), (1, 'rl')):
            hp, kn = P[key]
            hip = M(pelvis, trans(side * 0.1 * b, -0.04, 0), rotx(-hp))
            ms.append(box(0.15 * b, 0.46, 0.17 * b, self.pants, tpa).xf(M(hip, trans(0, -0.46, 0))))
            knee = M(hip, trans(0, -0.45, 0), rotx(kn))
            if self.peg_legs:
                ms.append(box(0.13 * b, 0.1, 0.15 * b, self.pants, tpa).xf(M(knee, trans(0, -0.1, 0))))
                ms.append(cyl(0.035, 0.025, 0.36, 6, (130, 95, 60)).xf(M(knee, trans(0, -0.45, 0))))
            else:
                ms.append(box(0.13 * b, 0.42, 0.15 * b, self.pants, tpa).xf(M(knee, trans(0, -0.42, 0))))
                ms.append(box(0.13 * b, 0.08, 0.26, self.shoes).xf(M(knee, trans(0, -0.47, 0.05))))
            attach['foot_' + ('l' if side < 0 else 'r')] = M(knee, trans(0, -0.47, 0.05))
        if self.robe is not None:
            # tunique longue (kanzu)
            ms.append(cyl(0.3 * b, 0.22 * b, 0.95, 8, self.robe, caps=False).xf(M(pelvis, trans(0, -0.86, 0))))
        # torse
        torso = M(pelvis, rotx(P['lean']), rotz(P['side']))
        tw, td = 0.42 * b, 0.24 * b
        ms.append(box(tw, 0.56, td, self.shirt, tsh).xf(M(torso, trans(0, 0.0, 0))))
        if self.jacket is not None:
            ms.append(box(tw + 0.02, 0.5, td + 0.02, self.jacket, faces='blrud').xf(M(torso, trans(0, 0.04, 0))))
            ms.append(box(0.12, 0.5, td + 0.02, self.jacket, faces='f').xf(M(torso, trans(-tw / 2 + 0.06, 0.04, 0))))
            ms.append(box(0.12, 0.5, td + 0.02, self.jacket, faces='f').xf(M(torso, trans(tw / 2 - 0.06, 0.04, 0))))
        if self.tie is not None:
            ms.append(box(0.05, 0.3, 0.02, self.tie).xf(M(torso, trans(0, 0.22, td / 2 + 0.01))))
        attach['torso'] = torso
        # cou + tête
        neck = M(torso, trans(0, 0.56, 0))
        ms.append(box(0.1, 0.08, 0.1, self.skin).xf(neck))
        head = M(neck, trans(0, 0.06, 0), roty(P['hy']), rotx(-P['hp']))
        attach['head'] = head
        face = P['face'] if P['face'] is not None else self.face
        # RÈGLE : avec un chapeau, le crâne s'arrête sous le chapeau -> rien ne peut transpercer
        hat_on = bool(self.hat) and P.get('hat', True)
        hh = 0.205 if hat_on else 0.27
        hb = box(0.24, hh, 0.25, self.skin, faces='blrud')
        vt = 1.0 - hh / 0.27
        hf = quad((-0.12, 0, 0.125), (0.12, 0, 0.125), (0.12, hh, 0.125), (-0.12, hh, 0.125), self.skin * 0 + 1,
                  TEXB[face], ((0, 1), (1, 1), (1, vt), (0, vt)))
        ms += [hb.xf(head), hf.xf(head)]
        if hat_on and self.hat != 'bonnet':
            # bandeau du chapeau qui ferme tout le dessus de la tête (coins compris)
            ms.append(box(0.262, 0.045, 0.272, self.hat_col * 0.85).xf(M(head, trans(0, 0.195, 0))))
        # oreilles
        for s in (-1, 1):
            ms.append(box(0.03, 0.07, 0.05, self.skin * 0.95).xf(M(head, trans(s * 0.13, 0.1, 0))))
        has_hat = bool(self.hat) and P.get('hat', True)
        if self.hair_style != 'bald' and P.get('hair', True):
            hc = self.hair
            if has_hat:
                # cheveux qui dépassent seulement sous le chapeau
                ms.append(box(0.255, 0.14, 0.05, hc).xf(M(head, trans(0, 0.07, -0.11))))
                ms.append(box(0.025, 0.1, 0.16, hc).xf(M(head, trans(-0.122, 0.11, -0.04))))
                ms.append(box(0.025, 0.1, 0.16, hc).xf(M(head, trans(0.122, 0.11, -0.04))))
            else:
                ms.append(box(0.26, 0.06, 0.27, hc).xf(M(head, trans(0, 0.25, -0.005))))
                ms.append(box(0.26, 0.18, 0.06, hc).xf(M(head, trans(0, 0.1, -0.11))))
                ms.append(box(0.03, 0.12, 0.2, hc).xf(M(head, trans(-0.125, 0.15, -0.03))))
                ms.append(box(0.03, 0.12, 0.2, hc).xf(M(head, trans(0.125, 0.15, -0.03))))
        if has_hat:
            hk = self.hat
            if hk in ('ranger', 'pith', 'bonnet'):
                ms.append(hat_mesh(hk, self.hat_col).xf(M(head, trans(0, 0.21, 0))))
                if hk != 'bonnet':
                    ms.append(box(0.27, 0.09, 0.28, self.hat_col).xf(M(head, trans(0, 0.2, 0))))
            else:
                # chapeau enfoncé sur la tête et assez large pour couvrir les coins du crâne
                ms.append(box(0.262, 0.04, 0.272, self.hat_col * 0.9).xf(M(head, trans(0, 0.205, 0))))
                # calotte pleine qui englobe tout le haut du crâne (aucun coin de tête ne dépasse)
                ms.append(box(0.27, 0.11, 0.28, self.hat_col).xf(M(head, trans(0, 0.2, 0))))
                ms.append(hat_mesh(hk, self.hat_col).xf(M(head, trans(0, 0.215, 0), scale(1.3, 1.0, 1.3))))
        # bras
        for side, key in ((-1, 'la'), (1, 'ra')):
            sp, sr, el = P[key]
            ik = P.get('ik_' + ('l' if side < 0 else 'r'))
            if ik is not None:
                sp, sr, el = solve_arm(lambda a, s=side: _human_hand(torso, s, tw, a), ik, (sp, sr, el),
                                       ((-1.2, 3.3), (-0.4, 1.7), (0.0, 2.7)), key=(id(self), side))
            sh = M(torso, trans(side * (tw / 2 + 0.06), 0.5, 0), rotx(-sp), rotz(side * sr))
            arm_col = self.shirt if self.sleeves in ('long', 'short') else self.skin
            ac = self.jacket if self.jacket is not None else arm_col
            ms.append(box(0.11 * b, 0.3, 0.12 * b, ac, tsh if self.jacket is None else 0).xf(M(sh, trans(0, -0.3, 0))))
            elb = M(sh, trans(0, -0.29, 0), rotx(-el))
            lc = self.shirt if self.sleeves == 'long' else self.skin
            if self.jacket is not None:
                lc = self.jacket
            ms.append(box(0.1 * b, 0.27, 0.11 * b, lc, tsh if (self.sleeves == 'long' and self.jacket is None) else 0).xf(M(elb, trans(0, -0.27, 0))))
            hand = M(elb, trans(0, -0.27, 0))
            ms.append(box(0.08, 0.1, 0.1, self.skin).xf(M(hand, trans(0, -0.1, 0))))
            attach['hand_' + ('l' if side < 0 else 'r')] = M(hand, trans(0, -0.07, 0))
        if self.extra:
            ms.append(self.extra(P, attach))
        for k in ('hand_l', 'hand_r'):
            if P[k] is not None:
                ms.append(P[k].xf(attach[k]))
        self.attach = attach
        return merge(ms)


def hat_mesh(kind, col):
    col = C(col)
    if kind == 'bonnet':  # capote victorienne : coque sur l'arrière de la tête, bord qui encadre le visage, ruban noué
        shell = merge([box(0.29, 0.13, 0.27, col).xf(trans(0, -0.07, -0.02)),
                       box(0.29, 0.26, 0.08, col).xf(trans(0, -0.27, -0.14)),
                       box(0.03, 0.26, 0.22, col).xf(trans(-0.145, -0.22, 0.0)),
                       box(0.03, 0.26, 0.22, col).xf(trans(0.145, -0.22, 0.0))])
        brim = merge([box(0.34, 0.05, 0.06, col * 1.1).xf(trans(0, 0.03, 0.12)),
                      box(0.05, 0.3, 0.06, col * 1.1).xf(trans(-0.17, -0.25, 0.1)),
                      box(0.05, 0.3, 0.06, col * 1.1).xf(trans(0.17, -0.25, 0.1))])
        ribbon = merge([box(0.012, 0.2, 0.02, (235, 225, 230)).xf(trans(-0.13, -0.4, 0.06)),
                        box(0.012, 0.2, 0.02, (235, 225, 230)).xf(trans(0.13, -0.4, 0.06)),
                        box(0.27, 0.02, 0.02, (235, 225, 230)).xf(trans(0, -0.41, 0.07)),
                        box(0.08, 0.05, 0.03, (235, 225, 230)).xf(trans(0.06, -0.43, 0.13))])
        flower = merge([box(0.05, 0.05, 0.05, (200, 80, 110)).xf(trans(0.12, 0.05, 0.02)), box(0.04, 0.03, 0.06, (90, 130, 70)).xf(trans(0.09, 0.04, -0.03))])
        return merge([shell, brim, ribbon, flower])
    if kind == 'ranger':  # chapeau de campagne (garde forestier)
        # calotte assez large pour englober le crâne (coins compris) et plus haute que lui
        brim = cyl(0.3, 0.3, 0.015, 14, col)
        crown = cyl(0.19, 0.15, 0.19, 10, col)
        band = cyl(0.195, 0.19, 0.035, 10, col * 0.45, caps=False)
        dent = [box(0.035, 0.03, 0.2, col * 0.8).xf(M(trans(0, 0.175, 0))), box(0.2, 0.03, 0.035, col * 0.8).xf(trans(0, 0.175, 0))]
        return merge([brim, crown, band.xf(trans(0, 0.015, 0))] + dent)
    if kind == 'cap':
        return merge([sphere(0.14, 8, 4, col, sy=0.6), box(0.18, 0.015, 0.12, col).xf(trans(0, 0.0, 0.16))])
    if kind == 'bowler':
        return merge([cyl(0.2, 0.2, 0.015, 10, col), sphere(0.135, 8, 4, col, sy=0.9).xf(trans(0, 0.04, 0))])
    if kind == 'kepi':  # casquette d'employé de chemin de fer
        return merge([cyl(0.135, 0.14, 0.11, 8, col), box(0.2, 0.015, 0.1, (25, 25, 25)).xf(trans(0, 0.0, 0.15)),
                      cyl(0.137, 0.137, 0.025, 8, (190, 160, 60), caps=False).xf(trans(0, 0.03, 0))])
    if kind == 'pith':  # casque colonial
        return merge([sphere(0.27, 10, 4, col, sy=0.18), sphere(0.19, 8, 4, col, sy=0.9).xf(trans(0, 0.03, 0))])
    if kind == 'sailor':
        return merge([cyl(0.14, 0.15, 0.06, 10, col), cyl(0.16, 0.16, 0.02, 10, col).xf(trans(0, 0.06, 0)),
                      cyl(0.141, 0.141, 0.02, 10, (20, 20, 30), caps=False).xf(trans(0, 0.0, 0))])
    if kind == 'turban':
        return merge([cyl(0.15, 0.16, 0.08, 10, col), sphere(0.16, 10, 4, col, sy=0.55).xf(trans(0, 0.06, 0))])
    if kind == 'kofia':  # bonnet brodé
        return merge([cyl(0.135, 0.135, 0.09, 10, col), cyl(0.137, 0.137, 0.03, 10, (180, 140, 60), caps=False).xf(trans(0, 0.03, 0))])
    if kind == 'flatcap':
        return merge([sphere(0.145, 8, 4, col, sy=0.45), box(0.2, 0.015, 0.1, col * 0.9).xf(trans(0, -0.005, 0.15))])
    return Mesh()


def walk_pose(phase, amp=1.0, arm=1.0, **kw):
    s = math.sin(phase)
    c = math.cos(phase)
    # le genou se plie quand la jambe passe vers l'avant (et non quand elle recule)
    p = dict(ll=(0.45 * s * amp, max(0, c) * 0.6 * amp + 0.05), rl=(-0.45 * s * amp, max(0, -c) * 0.6 * amp + 0.05),
             la=(-0.4 * s * amp * arm, 0.08, 0.25), ra=(0.4 * s * amp * arm, 0.08, 0.25), drop=abs(math.cos(phase)) * 0.03 * amp)
    p.update(kw)
    return p


def run_pose(phase, **kw):
    s, c = math.sin(phase), math.cos(phase)
    p = dict(ll=(0.8 * s + 0.15, max(0, c) * 1.5 + 0.2), rl=(-0.8 * s + 0.15, max(0, -c) * 1.5 + 0.2),
             la=(-0.9 * s, 0.1, 1.3), ra=(0.9 * s, 0.1, 1.3), lean=0.25, drop=0.05 + abs(c) * 0.05)
    p.update(kw)
    return p


def sit_pose(**kw):
    p = dict(ll=(1.5, 1.5), rl=(1.5, 1.5), drop=0.45, la=(0.6, 0.1, 0.5), ra=(0.6, 0.1, 0.5))
    p.update(kw)
    return p


# ------------------------------------------------------------------ décors
def pine(h=6.0, r=1.6, seed=0, snow=False, dead=False):
    rr = np.random.default_rng(seed)
    ms = [cyl(0.16 * h / 6, 0.1 * h / 6, h * 0.35, 6, (110, 80, 55), 'bark', ts=1.0)]
    layers = 3
    for i in range(layers):
        y = h * (0.22 + 0.24 * i)
        rad = r * (1 - i * 0.26) * (0.9 + rr.random() * 0.2)
        if dead:
            continue
        ms.append(cyl(rad, 0.0, h * 0.42, 7, (255, 255, 255), 'needles', ts=1.5).xf(M(trans(0, y, 0), roty(rr.random() * 3))))
    return merge(ms)


def deciduous(h=6.0, r=2.2, seed=0, col=(255, 255, 255), tex='leaves'):
    rr = np.random.default_rng(seed)
    ms = [cyl(0.2 * h / 6, 0.14 * h / 6, h * 0.55, 6, (110, 80, 55), 'bark', ts=1.0)]
    for i in range(3):
        o = (rr.normal() * r * 0.3, h * 0.55 + rr.random() * h * 0.25, rr.normal() * r * 0.3)
        ms.append(sphere(r * (0.7 + rr.random() * 0.3), 7, 4, col, tex, sy=0.8).xf(trans(o)))
    return merge(ms)


def palm(h=7.0, seed=0, lean=0.15):
    rr = np.random.default_rng(seed)
    ms = []
    seg = 6
    pos = np.zeros(3)
    ang = rr.random() * 6.28
    dirv = np.array([math.cos(ang) * lean, 1, math.sin(ang) * lean])
    dirv /= np.linalg.norm(dirv)
    for i in range(seg):
        rot = np.eye(4)
        # aligne cylindre sur dirv
        axis = np.cross([0, 1, 0], dirv)
        if np.linalg.norm(axis) > 1e-6:
            a = math.acos(min(1, dirv[1]))
            axis /= np.linalg.norm(axis)
            K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
            rot[:3, :3] = np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
        ms.append(cyl(0.2 - i * 0.015, 0.19 - i * 0.015, h / seg + 0.02, 6, (140, 110, 80), 'bark', ts=0.6).xf(M(trans(pos), rot)))
        pos = pos + dirv * h / seg
        dirv = dirv + np.array([math.cos(ang), 0, math.sin(ang)]) * 0.04
        dirv /= np.linalg.norm(dirv)
    for k in range(8):
        a = k / 8 * 6.28 + rr.random() * 0.3
        L = 2.6 + rr.random() * 0.6
        tip = (math.cos(a) * L, -1.0 - rr.random() * 0.6, math.sin(a) * L)
        mid = (math.cos(a) * L * 0.5, 0.35, math.sin(a) * L * 0.5)
        side = np.array([-math.sin(a), 0, math.cos(a)]) * 0.35
        p0 = pos
        t = [[p0, pos + np.array(mid) + side, pos + np.array(mid) - side],
             [pos + np.array(mid) + side, pos + np.array(tip), pos + np.array(mid) - side]]
        ms.append(Mesh(t, C((70, 120, 45)) * (0.85 + 0.3 * rr.random()), None, TEXB['leaves']))
    return merge(ms)


def rock(r=1.0, seed=0, col=(255, 255, 255), tex='rock'):
    rr = np.random.default_rng(seed)
    s = sphere(r, 6, 4, col, tex)
    t = s.tris.copy()
    # déformation cohérente par sommet
    keys = {}
    for i in range(t.shape[0]):
        for j in range(3):
            k = tuple(np.round(t[i, j], 4))
            if k not in keys:
                keys[k] = 0.75 + rr.random() * 0.5
            t[i, j] *= keys[k]
    t[:, :, 1] = np.maximum(t[:, :, 1], -0.1 * r)
    s.tris = t
    return s


def ground(x0, z0, x1, z1, tex='grass', col=(255, 255, 255), ts=3.0, n=8, hfun=None, colfun=None):
    return grid(x0, z0, x1, z1, n, n, hfun, col, tex, ts, colfun)


def cloud_bank(cx, cy, cz, w=40, seed=0, col=(70, 70, 80), n=10, sz=6.0):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        o = (cx + (rr.random() - 0.5) * w, cy + rr.random() * sz * 0.4, cz + (rr.random() - 0.5) * w * 0.4)
        ms.append(sphere(sz * (0.6 + rr.random() * 0.6), 7, 4, np.asarray(col) * (0.85 + 0.25 * rr.random()), sy=0.55).xf(trans(o)))
    return merge(ms)


def lightning_path(a, b, seed=0, segs=12, jitter=0.12, branches=2):
    """renvoie liste de polylignes (tronc + branches)"""
    rr = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = np.linalg.norm(b - a)
    pts = [a]
    for i in range(1, segs):
        t = i / segs
        p = a + (b - a) * t + rr.normal(size=3) * L * jitter * (1 - abs(t - 0.5))
        pts.append(p)
    pts.append(b)
    paths = [np.array(pts)]
    for k in range(branches):
        i = rr.integers(2, segs - 3)
        st = pts[i]
        d = (b - a) / segs
        bp = [st]
        for j in range(4):
            bp.append(bp[-1] + d * 0.8 + rr.normal(size=3) * L * 0.05)
        paths.append(np.array(bp))
    return paths


def lightning_mesh(paths, cam, width=0.25, core=(255, 255, 255), glow=(170, 190, 255), alpha=1.0):
    ms = []
    for i, p in enumerate(paths):
        w = width if i == 0 else width * 0.5
        ms.append(strip(p, w * 2.2, cam, glow, emis=1.0, alpha=0.5 * alpha))
        ms.append(strip(p, w, cam, core, emis=1.0, alpha=alpha))
    return merge(ms)


def fire_sprites(base, t, cam, n=5, size=0.35, spread=0.15, seed=0, hgt=1.0):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        ph = rr.random()
        life = (t * 1.8 + ph) % 1.0
        off = np.array([(rr.random() - 0.5) * spread * 2, life * size * 1.6 * hgt, (rr.random() - 0.5) * spread * 2])
        s = size * (1.0 - life * 0.6) * (0.8 + 0.4 * rr.random())
        ms.append(billboard(np.asarray(base) + off, s, s * 1.3, cam, (255, 255, 255), 'fire', emis=1.0,
                            alpha=1.0 - life * 0.5))
    return merge(ms)


def smoke_sprites(base, t, cam, n=6, size=1.0, rise=3.0, seed=0, col=(255, 255, 255), drift=(0.5, 0, 0.2), alpha=0.8):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        ph = rr.random()
        life = (t * 0.25 + ph) % 1.0
        off = np.array(drift) * life * rise + np.array([(rr.random() - .5) * size, life * rise, (rr.random() - .5) * size])
        s = size * (0.6 + life * 1.6)
        ms.append(billboard(np.asarray(base) + off, s, s, cam, col, 'smoke', emis=0.3, alpha=alpha * (1 - life)))
    return merge(ms)


def grass_tufts(x0, z0, x1, z1, n=200, seed=0, hfun=None, col=(80, 125, 50), h=0.35, avoid=None, flowers=0.0):
    """touffes d'herbe en croix (+ fleurs)"""
    rr = np.random.default_rng(seed)
    tris, cols = [], []
    for i in range(n):
        x, z = rr.uniform(x0, x1), rr.uniform(z0, z1)
        if avoid and avoid(x, z):
            continue
        y = hfun(x, z) if hfun else 0.0
        hh = h * (0.6 + rr.random() * 0.8)
        a = rr.random() * 3.14
        c = np.asarray(C(col)) * (0.8 + 0.4 * rr.random())
        for k in range(3):
            aa = a + k * 1.05
            dx, dz = math.cos(aa) * hh * 0.4, math.sin(aa) * hh * 0.4
            lean = (rr.random() - 0.5) * hh * 0.5
            tris.append([(x - dx, y, z - dz), (x + dx, y, z + dz), (x + lean, y + hh, z + lean * 0.5)])
            cols.append(c)
        if rr.random() < flowers:
            fc = C([(240, 230, 90), (240, 240, 240), (200, 120, 200), (230, 90, 70)][rr.integers(0, 4)])
            for k in range(2):
                aa = a + k * 1.57
                dx, dz = math.cos(aa) * 0.05, math.sin(aa) * 0.05
                tris.append([(x - dx, y + hh, z - dz), (x + dx, y + hh, z + dz), (x, y + hh + 0.08, z)])
                cols.append(fc)
    if not tris:
        return Mesh()
    return Mesh(tris, np.array(cols))


def wheel(r=0.7, w=0.1, spokes=8, col=(120, 85, 50)):
    ms = [cyl(r, r, w, 14, (90, 90, 95), 'metal', caps=False).xf(M(trans(0, -w / 2, 0))),
          cyl(r * 0.94, r * 0.94, w * 0.9, 14, col, caps=False).xf(trans(0, -w * 0.45, 0)),
          cyl(0.1, 0.1, w * 1.6, 8, col).xf(trans(0, -w * 0.8, 0))]
    for k in range(spokes):
        a = k / spokes * math.pi
        ms.append(box(0.05, 0.04, r * 1.9, col).xf(M(roty(a), trans(0, -0.02, 0))))
    return merge(ms)


def frustum(w0, h0, w1, h1, L, col=(255, 255, 255), tex=0, dy1=0.0):
    """boîte effilée le long de +z : section w0×h0 à z=0 -> w1×h1 à z=L (centrée en x, y)"""
    a = [(-w0 / 2, -h0 / 2, 0), (w0 / 2, -h0 / 2, 0), (w0 / 2, h0 / 2, 0), (-w0 / 2, h0 / 2, 0)]
    b = [(-w1 / 2, -h1 / 2 + dy1, L), (w1 / 2, -h1 / 2 + dy1, L), (w1 / 2, h1 / 2 + dy1, L), (-w1 / 2, h1 / 2 + dy1, L)]
    ms = [quad(b[0], b[1], b[2], b[3], col, tex), quad(a[1], a[0], a[3], a[2], col, tex)]
    for i in range(4):
        j = (i + 1) % 4
        ms.append(quad(a[i], a[j], b[j], b[i], col, tex))
    return merge(ms)


def clock_mesh(hour, minute, r=0.3, frame_col=(90, 60, 35)):
    """horloge murale face +z, aiguilles nettement devant le cadran"""
    ms = [cyl(r * 1.12, r * 1.12, 0.05, 14, frame_col).xf(rotx(math.pi / 2)).xf(trans(0, 0, -0.05)),
          quad((-r, -r, 0.01), (r, -r, 0.01), (r, r, 0.01), (-r, r, 0.01), (255, 255, 255), 'clock_face', ((0, 1), (1, 1), (1, 0), (0, 0)))]
    a_m = minute / 60 * 2 * math.pi
    a_h = ((hour % 12) + minute / 60) / 12 * 2 * math.pi
    ms.append(box(r * 0.07, r * 0.85, r * 0.04, (20, 20, 20)).xf(M(trans(0, 0, 0.02), rotz(-a_m))))
    ms.append(box(r * 0.11, r * 0.55, r * 0.04, (20, 20, 20)).xf(M(trans(0, 0, 0.035), rotz(-a_h))))
    ms.append(cyl(r * 0.06, r * 0.06, r * 0.06, 6, (30, 30, 30)).xf(M(trans(0, 0, 0.02), rotx(math.pi / 2))))
    return merge(ms)
