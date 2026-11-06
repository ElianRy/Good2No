"""Ajouts lot 4 : textes d'accroche, appel à s'abonner, compteur, secousses, femme, chien, cheval, sons et musiques."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from lib import *
import audio as A

F_HOOK = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 118)
F_HOOK_S = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 96)
F_CTA = ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', 50)
F_BADGE = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 54)
OW, OH = 1080, 1920


def _logo(size=86):
    im = Image.open('/home/claude/g2n/logo.png').convert('RGBA').resize((size, size), Image.LANCZOS)
    m = Image.new('L', (size * 4, size * 4), 0)
    ImageDraw.Draw(m).ellipse([0, 0, size * 4 - 1, size * 4 - 1], fill=255)
    im.putalpha(m.resize((size, size), Image.LANCZOS))
    return im


LOGO = _logo()


# ------------------------------------------------------------------ textes à l'écran
def _pop(u):
    """facteur d'échelle d'apparition : 1.35 -> 1.0 avec petit rebond"""
    if u < 0:
        return 0
    if u < 0.12:
        return 1.35 - 0.45 * (u / 0.12)
    if u < 0.22:
        return 0.9 + 0.1 * ((u - 0.12) / 0.1)
    return 1.0


def hook_title(lines, t0, t1, y=300, accent=None):
    """gros titre d'accroche (2 lignes max). accent = index de la ligne en jaune"""
    def ov(img, t):
        if not (t0 <= t < t1):
            return
        u = t - t0
        s = _pop(u)
        alpha = 1.0 if t < t1 - 0.12 else max(0, (t1 - t) / 0.12)
        layer = Image.new('RGBA', (OW, 520), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        yy = 40
        for i, ln in enumerate(lines):
            f = F_HOOK
            w = d.textlength(ln, font=f)
            if w > 1000:
                f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', int(118 * 1000 / w))
                w = d.textlength(ln, font=f)
            col = (255, 226, 60) if accent == i else (255, 255, 255)
            d.text(((OW - w) / 2, yy), ln, font=f, fill=col + (255,), stroke_width=12, stroke_fill=(0, 0, 0, 255))
            yy += int(f.size * 1.08)
        if s != 1.0:
            nw, nh = int(OW * s), int(520 * s)
            layer = layer.resize((nw, nh), Image.BILINEAR)
        else:
            nw, nh = OW, 520
        if alpha < 1:
            a = np.asarray(layer).copy()
            a[..., 3] = (a[..., 3] * alpha).astype(np.uint8)
            layer = Image.fromarray(a)
        jx = int(math.sin(u * 47) * 4) if u < 0.35 else 0
        img.paste(layer, ((OW - nw) // 2 + jx, y - (nh - 520) // 2), layer)
    return ov


def cta(t0, dur=3.0, y=250):
    """« + Abonne-toi » : pastille rouge qui glisse, le + pulse puis devient une coche"""
    def ov(img, t):
        u = t - t0
        if not (0 <= u < dur):
            return
        slide = min(1.0, u / 0.2)
        out = max(0.0, (u - dur + 0.25) / 0.25)
        x_off = int((1 - ease(slide)) * -700 + ease(out) * 700)
        done = u > dur * 0.62
        layer = Image.new('RGBA', (OW, 200), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        txt = 'Abonné !' if done else 'Abonne-toi'
        tw = d.textlength(txt, font=F_CTA)
        bw = int(tw + 210)
        x0 = (OW - bw) // 2
        d.rounded_rectangle([x0 + 6, 46, x0 + bw + 6, 156], radius=55, fill=(0, 0, 0, 120))
        d.rounded_rectangle([x0, 40, x0 + bw, 150], radius=55, fill=(235, 30, 60, 255) if not done else (40, 40, 45, 255),
                            outline=(255, 255, 255, 255), width=5)
        # avatar : logo de la chaîne en rond, liseré blanc
        d.ellipse([x0 + 10, 48, x0 + 104, 142], fill=(255, 255, 255, 255))
        layer.paste(LOGO, (x0 + 14, 52), LOGO)
        d.text((x0 + 120, 95), txt, font=F_CTA, fill=(255, 255, 255, 255), anchor='lm')
        # bouton + / ✓
        cx, cy = x0 + 92, 130
        pr = 20 + (3 * math.sin(u * 14) if not done else 0)
        d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=(255, 255, 255, 255))
        if done:
            d.line([cx - 9, cy, cx - 2, cy + 8, cx + 10, cy - 8], fill=(235, 30, 60, 255), width=6)
        else:
            d.rectangle([cx - 10, cy - 3, cx + 10, cy + 3], fill=(235, 30, 60, 255))
            d.rectangle([cx - 3, cy - 10, cx + 3, cy + 10], fill=(235, 30, 60, 255))
        img.paste(layer, (x_off, y), layer)
    return ov


def badge(text, t0, dur=2.2, y=150, col=(255, 226, 60)):
    """petite étiquette en haut (ex. « ACCIDENT 2/3 »)"""
    def ov(img, t):
        u = t - t0
        if not (0 <= u < dur):
            return
        s = _pop(u)
        a = 1.0 if u < dur - 0.15 else (dur - u) / 0.15
        layer = Image.new('RGBA', (OW, 140), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        w = d.textlength(text, font=F_BADGE)
        x0 = (OW - w) / 2 - 30
        d.rounded_rectangle([x0, 20, x0 + w + 60, 116], radius=18, fill=(15, 15, 18, int(220 * a)))
        d.text((OW / 2, 68), text, font=F_BADGE, fill=col + (int(255 * a),), anchor='mm')
        if s != 1.0:
            layer = layer.resize((int(OW * s), int(140 * s)), Image.BILINEAR)
        img.paste(layer, ((OW - layer.size[0]) // 2, y - (layer.size[1] - 140) // 2), layer)
    return ov


def tint(col=(255, 120, 80), k=0.45, sepia=False):
    """post-traitement PIL : teinte (légende) ou sépia (daguerréotype)"""
    def f(img):
        a = np.asarray(img).astype(np.float32)
        if sepia:
            g = a.mean(axis=2, keepdims=True)
            a = g * np.array([1.07, 0.88, 0.66], np.float32)
        a = a * (1 - k) + (a.mean(axis=2, keepdims=True) * np.array(col, np.float32) / 255.0) * k * 1.4
        img.paste(Image.fromarray(a.clip(0, 255).astype(np.uint8)))
    return f


def chain(*fs):
    def f(img):
        for g in fs:
            g(img)
    return f


def comment_bubble(t0, dur=3.0, y=1450, text='Moi je pense que…', user='toi'):
    """fausse bulle de commentaire TikTok qui glisse du bas (incitation à commenter)"""
    def ov(img, t):
        u = t - t0
        if not (0 <= u < dur):
            return
        k = ease(min(1.0, u / 0.25))
        layer = Image.new('RGBA', (OW, 260), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        fn = ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', 34)
        fs = ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf', 40)
        x0, x1 = 90, OW - 90
        d.rounded_rectangle([x0, 30, x1, 220], radius=36, fill=(255, 255, 255, 240))
        d.polygon([(x0 + 70, 218), (x0 + 120, 218), (x0 + 60, 252)], fill=(255, 255, 255, 240))
        d.ellipse([x0 + 26, 56, x0 + 106, 136], fill=(200, 200, 205, 255))
        d.ellipse([x0 + 50, 66, x0 + 82, 98], fill=(250, 250, 250, 255))
        d.pieslice([x0 + 36, 96, x0 + 96, 156], 180, 360, fill=(250, 250, 250, 255))
        d.text((x0 + 128, 62), user, font=fn, fill=(120, 120, 128, 255))
        n = int(len(text) * min(1.0, max(0.0, (u - 0.3) / 1.2)))
        cursor = '|' if (u * 2) % 1 < 0.5 else ' '
        d.text((x0 + 128, 112), text[:n] + cursor, font=fs, fill=(20, 20, 25, 255))
        # coeur
        hx, hy = x1 - 70, 100
        d.ellipse([hx - 18, hy - 12, hx, hy + 6], fill=(235, 30, 60, 255))
        d.ellipse([hx - 2, hy - 12, hx + 16, hy + 6], fill=(235, 30, 60, 255))
        d.polygon([(hx - 18, hy - 1), (hx + 16, hy - 1), (hx - 1, hy + 20)], fill=(235, 30, 60, 255))
        img.paste(layer, (0, int(y + (1 - k) * 300)), layer)
    return ov


def overlays(*fns):
    """combine plusieurs overlays (fonction img, t) en un seul pour video_core.frame"""
    def f(img, t):
        for fn in fns:
            fn(img, t)
    return f


def vignette(img, k=0.6, col=(0, 0, 0)):
    """assombrit les bords (PIL, en place)"""
    a = np.asarray(img).astype(np.float32)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    r = np.hypot((xx - a.shape[1] / 2) / (a.shape[1] / 2), (yy - a.shape[0] / 2) / (a.shape[0] / 2))
    m = np.clip((r - 0.55) / 0.6, 0, 1)[..., None] * k
    a = a * (1 - m) + np.array(col, np.float32) * m
    img.paste(Image.fromarray(a.clip(0, 255).astype(np.uint8)))


# ------------------------------------------------------------------ caméra
def shake(cam, amp, t, freq=31.0):
    """secousse de caméra (amp en mètres)"""
    if amp <= 0:
        return cam
    o = np.array([math.sin(t * freq), math.sin(t * freq * 1.37 + 1.1), math.sin(t * freq * 0.83 + 2.3)]) * amp
    return Cam(tuple(np.asarray(cam.pos) + o), tuple(np.asarray(cam.at) + o * 0.6), cam.fov, cam.roll + math.sin(t * freq * 0.7) * amp * 0.05)


def decay(lt, t_hit, k=3.0):
    """1 au moment de l'impact puis décroît"""
    d = lt - t_hit
    return 0.0 if d < 0 else math.exp(-d * k)


def punch(c0, lt, dur=0.35, zoom=0.82):
    """zoom brusque à l'ouverture d'un plan (fov réduit au début qui revient)"""
    k = max(0.0, 1 - lt / dur)
    return Cam(c0.pos, c0.at, c0.fov * (1 - (1 - zoom) * ease(k)), c0.roll)


# ------------------------------------------------------------------ femme
def woman_extra(style='bun', cap=None, apron=False, veil=False, hair=(70, 45, 30), cardigan=None):
    """accessoires féminins : chignon, coiffe d'hôtesse, voile d'infirmière, tablier"""
    hair = C(hair)

    def f(P, at):
        h = at['head']
        t = at['torso']
        ms = []
        if P.get('hair', True):
            # cheveux plus longs sur les côtés et chignon
            ms.append(box(0.27, 0.09, 0.27, hair).xf(M(h, trans(0, 0.22, -0.005))))
            for s in (-1, 1):
                ms.append(box(0.035, 0.2, 0.18, hair).xf(M(h, trans(s * 0.128, 0.05, -0.04))))
            ms.append(box(0.26, 0.24, 0.05, hair).xf(M(h, trans(0, 0.04, -0.12))))
            if style == 'bun':
                ms.append(sphere(0.085, 6, 4, hair).xf(M(h, trans(0, 0.2, -0.17))))
            elif style == 'grey_bun':
                ms.append(sphere(0.08, 6, 4, hair).xf(M(h, trans(0, 0.24, -0.12))))
        if cap == 'steward':
            ms.append(box(0.2, 0.06, 0.12, (250, 250, 248)).xf(M(h, trans(0, 0.29, 0.02), rotx(-0.2))))
            ms.append(box(0.22, 0.02, 0.02, (250, 250, 248)).xf(M(h, trans(0, 0.28, 0.09))))
        if veil:
            ms.append(box(0.29, 0.06, 0.29, (250, 250, 248)).xf(M(h, trans(0, 0.25, -0.01))))
            ms.append(box(0.3, 0.38, 0.06, (250, 250, 248)).xf(M(h, trans(0, -0.1, -0.15))))
            for s in (-1, 1):
                ms.append(box(0.03, 0.3, 0.2, (250, 250, 248)).xf(M(h, trans(s * 0.145, -0.02, -0.06))))
            ms.append(box(0.27, 0.05, 0.02, (250, 250, 248)).xf(M(h, trans(0, 0.24, 0.13))))
            ms.append(box(0.05, 0.035, 0.01, (200, 25, 30)).xf(M(h, trans(0, 0.24, 0.142))))
            ms.append(box(0.015, 0.06, 0.01, (200, 25, 30)).xf(M(h, trans(0, 0.24, 0.142))))
        if apron:
            ms.append(box(0.3, 0.32, 0.02, (250, 250, 246)).xf(M(t, trans(0, 0.05, 0.13))))
            ms.append(box(0.42, 0.05, 0.25, (250, 250, 246)).xf(M(t, trans(0, 0.0, 0.0))))
        if cardigan is not None:
            ms.append(box(0.45, 0.5, 0.27, C(cardigan), faces='blrud').xf(M(t, trans(0, 0.04, 0))))
            for s in (-1, 1):
                ms.append(box(0.1, 0.5, 0.27, C(cardigan), faces='f').xf(M(t, trans(s * 0.17, 0.04, 0))))
        return merge(ms)
    return f


# ------------------------------------------------------------------ objets
def baby(face_tex=None):
    """bébé emmailloté, tête vers +z, ~45 cm"""
    W = (240, 238, 228)
    ms = [sphere(0.1, 8, 5, W, 'blanket').xf(M(trans(0, 0, -0.03), scale(0.95, 0.85, 1.9))),
          sphere(0.085, 8, 5, W, 'blanket').xf(trans(0, 0.01, 0.15))]
    ms.append(sphere(0.06, 7, 4, (238, 200, 175)).xf(M(trans(0, 0.035, 0.2), scale(1, 1, 0.9))))
    for s_ in (-1, 1):
        ms.append(box(0.016, 0.01, 0.01, (40, 30, 25)).xf(trans(s_ * 0.022, 0.06, 0.252)))
    ms.append(box(0.025, 0.008, 0.01, (190, 110, 100)).xf(trans(0, 0.03, 0.255)))
    return merge(ms)


tex_noise('blanket', (225, 222, 210), (242, 240, 232), seed=150, octaves=1) if 'blanket' not in TEXB else None


# ------------------------------------------------------------------ chien (akita)
tex_noise('fur_akita', (226, 210, 180), (240, 228, 205), seed=151, octaves=3, speck=0.05, speck_col=(205, 188, 160))


class Dog:
    """akita low-poly, regarde vers +z, ~65 cm au garrot. ear_l_drop : l'oreille gauche tombante (Hachikō âgé)"""
    F = 'fur_akita'

    def __init__(self, size=1.0, col=(255, 255, 255), ear_l_drop=0.0):
        self.size, self.col, self.ear_l_drop = size, C(col), ear_l_drop

    def mesh(self, pos=(0, 0, 0), yaw=0.0, pose=None):
        P = dict(phase=0.0, amp=0.0, sit=0.0, lie=0.0, hp=0.0, hy=0.0, tail=0.0, mouth=0.0, jump=0.0, eyes=1.0)
        if pose:
            P.update(pose)
        F, W = self.F, self.col
        s = self.size
        root = M(trans(pos), roty(yaw), scale(s))
        ms = []
        ph, amp = P['phase'], P['amp']
        sit, lie, jump = P['sit'], P['lie'], P['jump']
        # corps : bascule vers l'arrière en position assise, s'abaisse couché, se cabre en sautant
        body_y = 0.6 - 0.36 * lie - 0.17 * sit + 0.12 * jump + abs(math.sin(ph)) * 0.025 * amp
        pb = -0.55 * sit - 0.6 * jump
        body = M(root, trans(0, body_y, 0), rotx(pb))
        hipp = M(body, trans(0, 0, -0.32))
        chest = M(body, trans(0, 0.02, 0.3))
        ms.append(box(0.3, 0.3, 0.75, W, F).xf(M(body, trans(0, -0.14, 0))))
        ms.append(box(0.34, 0.34, 0.3, W, F).xf(M(chest, trans(0, -0.15, 0.02))))
        ms.append(box(0.2, 0.18, 0.02, (248, 244, 236)).xf(M(chest, trans(0, -0.16, 0.175))))   # poitrail clair
        # cou + tête (contre la bascule)
        neck = M(chest, trans(0, 0.06, 0.1), rotx(0.55 - pb - 0.9 * lie))
        ms.append(box(0.19, 0.3, 0.19, W, F).xf(M(neck, trans(0, -0.06, 0))))
        head = M(neck, trans(0, 0.22, 0.02), rotx(-0.55 + 0.9 * lie), roty(P['hy']), rotx(-P['hp']))
        ms.append(box(0.24, 0.2, 0.22, W, F).xf(M(head, trans(0, -0.08, 0))))
        ms.append(box(0.27, 0.12, 0.14, W, F).xf(M(head, trans(0, -0.08, -0.02))))   # joues
        mz = M(head, trans(0, -0.07, 0.11))
        ms.append(frustum(0.14, 0.11, 0.1, 0.08, 0.15, W, F, dy1=-0.01).xf(M(mz, trans(0, 0.0, 0))))
        ms.append(box(0.06, 0.045, 0.03, (25, 20, 18)).xf(M(mz, trans(0, 0.035, 0.16))))   # truffe
        self.mouth = (mz @ np.array([0, -0.035, 0.12, 1.0]))[:3]
        self.head = head[:3, 3].copy()
        jaw = M(mz, trans(0, -0.045, 0.0), rotx(0.5 * P['mouth']))
        ms.append(frustum(0.1, 0.035, 0.08, 0.03, 0.13, W, F).xf(M(jaw, trans(0, -0.01, 0))))
        if P['mouth'] > 0.2:
            ms.append(box(0.05, 0.012, 0.08, (210, 100, 110)).xf(M(jaw, trans(0, -0.02, 0.12), rotx(0.4))))
        for sx in (-1, 1):
            if P['eyes'] > 0.5:
                ms.append(box(0.04, 0.035, 0.01, (25, 18, 14)).xf(M(head, trans(sx * 0.06, -0.02, 0.112))))
                ms.append(box(0.012, 0.012, 0.005, (240, 240, 240), emis=0.5).xf(M(head, trans(sx * 0.06 + 0.01, -0.01, 0.118))))
            else:
                ms.append(box(0.045, 0.008, 0.01, (40, 30, 25)).xf(M(head, trans(sx * 0.06, -0.03, 0.112))))
            # oreilles dressées triangulaires (la gauche peut tomber)
            drop = self.ear_l_drop if sx < 0 else 0.0
            ear = M(head, trans(sx * 0.075, 0.1, -0.03), rotz(-sx * (0.2 + 1.5 * drop)), rotx(-0.1 - 0.7 * drop))
            ms.append(Mesh([[(-0.06, 0, 0), (0.06, 0, 0), (0, 0.13, 0)], [(-0.06, 0, -0.04), (0.06, 0, -0.04), (0, 0.13, -0.02)],
                            [(-0.06, 0, 0), (0, 0.13, 0), (0, 0.13, -0.02)], [(0.06, 0, 0), (0, 0.13, -0.02), (0, 0.13, 0)],
                            [(-0.06, 0, 0), (-0.06, 0, -0.04), (0, 0.13, -0.02)], [(0.06, 0, 0), (0.06, 0, -0.04), (0, 0.13, -0.02)]],
                           W * 0.95).xf(ear))
            ms.append(Mesh([[(-0.035, 0.01, 0.004), (0.035, 0.01, 0.004), (0, 0.09, 0.004)]], C((215, 160, 150))).xf(ear))
        # queue enroulée sur le dos (signe de l'akita)
        tb = M(hipp, trans(0, 0.02, -0.04))
        pts = [(0, 0, 0), (0, 0.13, -0.05), (0, 0.22, 0.02), (0.02, 0.2, 0.14), (0.03, 0.12, 0.17)]
        wag = P['tail']
        for i in range(len(pts) - 1):
            a_ = np.array(pts[i]) + np.array([math.sin(wag) * 0.03 * i, 0, 0])
            b_ = np.array(pts[i + 1]) + np.array([math.sin(wag) * 0.03 * (i + 1), 0, 0])
            ms.append(rod(a_, b_, 0.055 - i * 0.007, W, F, n=5).xf(tb))
        # pattes : avant fixées à la poitrine, arrière au bassin ; repliées couchées / assises
        legs = (('fl', chest, -1, 0.06, 0.0), ('fr', chest, 1, 0.06, math.pi), ('bl', hipp, -1, 0.02, math.pi), ('br', hipp, 1, 0.02, 0.0))
        for name, base, sx, zo, off in legs:
            front = name[0] == 'f'
            sw = 0.5 * math.sin(ph + off) * amp
            if front:
                a1 = sw + 0.55 * sit * 1.0 + 0.5 * jump - 1.45 * lie
                kn = max(0.0, -sw) * 0.6 * amp + 0.15 * lie
            else:
                a1 = sw - 0.7 * sit + 1.6 * lie - 0.3 * jump
                kn = -(max(0.0, sw) * 0.7 * amp + 2.3 * sit + 1.9 * lie)
            hip = M(base, trans(sx * 0.1, -0.2, zo), rotx(a1))
            ms.append(box(0.1, 0.22, 0.12, W, F).xf(M(hip, trans(0, -0.22, 0))))
            knee = M(hip, trans(0, -0.21, 0), rotx(kn if front else -kn))
            ms.append(box(0.08, 0.17, 0.09, W, F).xf(M(knee, trans(0, -0.17, 0))))
            ms.append(box(0.09, 0.05, 0.12, W * 0.96, F).xf(M(knee, trans(0, -0.19, 0.03), rotx(-(a1 + (kn if front else -kn) + pb)))))
        return merge(ms)


def dog_walk(phase, amp=1.0, **kw):
    p = dict(phase=phase, amp=amp)
    p.update(kw)
    return p


# ------------------------------------------------------------------ cheval
tex_noise('fur_horse', (110, 70, 45), (130, 85, 55), seed=152, octaves=3, speck=0.05)


def horse(phase=0.0, amp=1.0, col=(255, 255, 255), head_down=0.0):
    """cheval, regarde vers +z, ~1,6 m au garrot"""
    F = 'fur_horse'
    W = C(col)
    ms = [box(0.55, 0.6, 1.55, W, F).xf(trans(0, 1.05, 0))]
    ms.append(sphere(0.33, 7, 4, W, F).xf(M(trans(0, 1.38, 0.62), scale(0.9, 0.85, 1.0))))
    ms.append(sphere(0.32, 7, 4, W, F).xf(M(trans(0, 1.36, -0.6), scale(0.9, 0.85, 1.0))))
    neck = M(trans(0, 1.45, 0.75), rotx(-0.7 + head_down * 0.8))
    ms.append(box(0.28, 0.75, 0.32, W, F).xf(M(neck, trans(0, 0, 0.0))))
    ms.append(box(0.06, 0.7, 0.22, (40, 28, 20)).xf(M(neck, trans(0, 0.05, -0.12))))   # crinière
    head = M(neck, trans(0, 0.72, 0.08), rotx(1.6 - head_down * 0.3))
    ms.append(box(0.24, 0.62, 0.3, W, F).xf(M(head, trans(0, 0, 0))))
    ms.append(box(0.2, 0.08, 0.2, (40, 30, 25)).xf(M(head, trans(0, 0.6, 0.02))))
    for s in (-1, 1):
        ms.append(box(0.06, 0.14, 0.05, W).xf(M(head, trans(s * 0.08, -0.08, -0.12), rotx(-0.8))))
        ms.append(box(0.03, 0.04, 0.04, (20, 15, 12)).xf(M(head, trans(s * 0.125, 0.18, 0.08))))
    ms.append(cyl(0.05, 0.02, 0.8, 5, (40, 28, 20)).xf(M(trans(0, 1.3, -0.8), rotx(-2.6))))
    for (x, z, ph) in ((-0.18, 0.6, 0), (0.18, 0.6, math.pi), (-0.18, -0.62, math.pi), (0.18, -0.62, 0)):
        lg = M(trans(x, 1.0, z), rotx(0.45 * math.sin(phase + ph) * amp))
        ms.append(box(0.15, 0.5, 0.18, W, F).xf(M(lg, trans(0, -0.5, 0))))
        kn = M(lg, trans(0, -0.5, 0), rotx(-max(0, math.sin(phase + ph)) * 0.8 * amp))
        ms.append(box(0.11, 0.48, 0.12, W, F).xf(M(kn, trans(0, -0.48, 0))))
        ms.append(box(0.13, 0.08, 0.15, (30, 25, 20)).xf(M(kn, trans(0, -0.52, 0.01))))
    return merge(ms)


# ------------------------------------------------------------------ éclairages
def flash_env(env, k, pos=None, col=(0.85, 0.87, 0.95)):
    if k <= 0:
        return env
    e = env.copy(amb=min(1.0, env.amb + 0.35 * k))
    e.sky_top = env.sky_top + (np.array([0.55, 0.58, 0.72]) - env.sky_top) * k
    e.sky_hor = env.sky_hor + (np.array(col) - env.sky_hor) * k
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
        o = np.array([rr.uniform(-area, area), 0, rr.uniform(-area, area)]) + f * area * 0.6
        p = cp + o
        p[1] = cp[1] - 3 + ((rr.uniform(0, 12) - t * 18) % 12)
        ms.append(strip([p, p - np.array([slant[0], 0.7, slant[2]])], 0.025, cam, col, emis=0.6, alpha=0.6))
    return merge(ms)


def particles(center, t, cam, n=40, area=(6, 5, 6), fall=1.0, size=0.08, col=(255, 255, 255), seed=0, drift=(0.3, 0, 0.1),
              tex=0, spin=False, alpha=1.0, emis=0.6):
    """flocons / pétales / feuilles qui tombent"""
    rr = np.random.default_rng(seed)
    ms = []
    c = np.asarray(center, float)
    for i in range(n):
        ph = rr.random()
        y = (ph * area[1] - t * fall) % area[1]
        x = rr.uniform(-area[0], area[0]) + math.sin(t * 1.3 + i) * 0.3 + drift[0] * t % (2 * area[0])
        z = rr.uniform(-area[2], area[2]) + drift[2] * t
        x = (x + area[0]) % (2 * area[0]) - area[0]
        p = c + np.array([x, y - area[1] / 2, z])
        cc = np.clip(np.asarray(C(col)) * (0.9 + 0.2 * rr.random()), 0, 1)
        ms.append(billboard(p, size, size * (0.6 if spin else 1.0), cam, cc, tex, emis=emis, alpha=alpha,
                            rot=t * 3 + i if spin else 0.0))
    return merge(ms)


# ------------------------------------------------------------------ sons supplémentaires
SR = A.SR


def impact(d=1.6):
    """gros « boum » de bande-annonce : sub qui descend + claque"""
    t = A.t_(d)
    f = 70 * np.exp(-t * 2.2) + 32
    ph = np.cumsum(2 * np.pi * f / SR)
    x = np.sin(ph) * np.exp(-t / 0.6) * np.minimum(1, t / 0.004)
    x += A.lp_fast(A.noise(d), 2500) * A.env_ad(len(t), 0.001, 0.06) * 0.8
    x += A.lp_fast(A.noise(d), 200) * A.env_ad(len(t), 0.005, 0.4) * 0.6
    return A.norm(np.tanh(x * 1.8), 0.95)


def riser(d=1.0):
    """montée de tension (souffle qui monte) avant une révélation"""
    t = A.t_(d)
    n = A.noise(d)
    x = A.bp_fast(n, 600, 6000) * (t / d) ** 2.2
    f = 200 + 900 * (t / d) ** 2
    x += np.sin(np.cumsum(2 * np.pi * f / SR)) * (t / d) ** 2 * 0.25
    x *= np.minimum(1, (d - t) / 0.02)
    return A.norm(x, 0.6)


def swoosh(d=0.35):
    t = A.t_(d)
    e = np.sin(np.pi * t / d) ** 3
    x = A.bp_fast(A.noise(d), 900, 7000) * e
    return A.norm(x, 0.55)


def record_scratch(d=0.55):
    t = A.t_(d)
    f = 900 * np.abs(np.sin(2 * np.pi * 2.6 * t)) + 120
    ph = np.cumsum(2 * np.pi * f / SR)
    x = np.sign(np.sin(ph)) * 0.4 + A.hp_fast(A.noise(d), 1500) * 0.6
    x *= np.minimum(1, (d - t) / 0.05) * np.minimum(1, t / 0.005)
    return A.norm(A.bp_fast(x, 200, 6000), 0.6)


def pop(d=0.18):
    t = A.t_(d)
    x = np.sin(2 * np.pi * (500 + 900 * t / d) * t) * A.env_ad(len(t), 0.002, 0.05)
    return A.norm(x, 0.5)


def ding(d=0.8):
    t = A.t_(d)
    x = (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 2636 * t)) * np.exp(-t * 6)
    return A.norm(x * np.minimum(1, t / 0.002), 0.4)


def phone_ring(d=4.0):
    """sonnerie de téléphone à cloches (deux salves par cycle)"""
    t = A.t_(d)
    out = np.zeros(len(t))
    gate = (((t % 2.0) < 0.4) | (((t % 2.0) > 0.6) & ((t % 2.0) < 1.0))).astype(float)
    trem = (np.sign(np.sin(2 * np.pi * 20 * t)) + 1) / 2
    for f, a in ((1350, 1.0), (1720, 0.6), (2900, 0.3)):
        out += np.sin(2 * np.pi * f * t) * a
    return A.norm(out * gate * (0.5 + 0.5 * trem), 0.55)


def ship_horn(d=2.5):
    t = A.t_(d)
    x = sum(a * np.sign(np.sin(2 * np.pi * f * t)) for f, a in ((92, 1.0), (116, 0.7), (138, 0.5)))
    x = A.lp_fast(x, 700) * np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.3)
    return A.norm(x, 0.7)


def metal_groan(d=2.5):
    t = A.t_(d)
    f = 60 + 25 * np.sin(2 * np.pi * 0.7 * t) + 10 * np.sin(2 * np.pi * 3.1 * t)
    ph = np.cumsum(2 * np.pi * f / SR)
    x = np.sign(np.sin(ph)) * 0.5 + np.sin(ph * 2.01) * 0.4 + A.lp_fast(A.noise(d), 400) * 0.6
    x = A.bp_fast(x, 50, 900) * np.sin(np.pi * t / d) ** 0.7
    return A.norm(np.tanh(x * 2), 0.7)


def crash_metal(d=2.0):
    """choc de coques : craquement métallique + grondement"""
    t = A.t_(d)
    x = A.lp_fast(A.noise(d), 300) * A.env_ad(len(t), 0.003, 0.7)
    for f in (180, 410, 760, 1330, 2100):
        x += np.sin(2 * np.pi * f * t + np.random.default_rng(int(f)).random() * 6) * np.exp(-t * (4 + f / 400)) * 0.3
    x += A.hp_fast(A.noise(d), 1500) * A.env_ad(len(t), 0.001, 0.15) * 0.7
    return A.norm(np.tanh(x * 1.5), 0.95)


def water_rush(d=4.0):
    x = A.lp_fast(A.noise(d), 1500) + A.bp_fast(A.noise(d), 200, 800) * 0.6
    m = 0.75 + 0.25 * np.sin(2 * np.pi * 0.9 * A.t_(d))
    return A.norm(x * m, 0.55)


def underwater(d=4.0):
    x = A.lp_fast(A.noise(d), 260)
    bub = np.zeros(int(d * SR))
    rr = np.random.default_rng(3)
    for _ in range(int(d * 6)):
        s = rr.integers(0, len(bub) - 4000)
        tt = A.t_(0.08)
        f = rr.uniform(300, 900) * (1 + tt * 6)
        bub[s:s + len(tt)] += np.sin(np.cumsum(2 * np.pi * f / SR)) * np.exp(-tt * 40)
    return A.norm(x + bub * 0.4, 0.6)


def heartbeat(d=2.0, bpm=60):
    out = np.zeros(int(d * SR))
    per = 60 / bpm
    for k in range(int(d / per) + 1):
        for o, a in ((0.0, 1.0), (0.22, 0.7)):
            s = int((k * per + o) * SR)
            tt = A.t_(0.15)
            b = np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 25) * a
            e = min(len(out), s + len(b))
            if s < len(out):
                out[s:e] += b[:e - s]
    return A.norm(out, 0.8)


def gallop(d=4.0, rate=2.2):
    out = np.zeros(int(d * SR))
    for k in range(int(d * rate)):
        for o in (0.0, 0.07, 0.16):
            s = int((k / rate + o) * SR)
            c = A.lp_fast(A.noise(0.06), 700) * A.env_ad(int(0.06 * SR), 0.001, 0.015)
            e = min(len(out), s + len(c))
            if s < len(out):
                out[s:e] += c[:e - s]
    return A.norm(out, 0.45)


def pluck(f, d=1.6, bright=0.5):
    """corde pincée (Karplus-Strong) : koto / harpe"""
    n = int(d * SR)
    N = max(2, int(SR / f))
    buf = np.random.default_rng(int(f)).uniform(-1, 1, N)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % N]
        buf[i % N] = 0.5 * (buf[i % N] + buf[(i + 1) % N]) * (0.994 + 0.004 * bright)
    return out * np.exp(-A.t_(d) * 1.2)


_PLUCK_CACHE = {}


def pluck_c(f, d=1.6):
    k = (round(f, 1), d)
    if k not in _PLUCK_CACHE:
        _PLUCK_CACHE[k] = pluck(f, d)
    return _PLUCK_CACHE[k]


def music_bed(mx, t0, t1, mood='tense', bpm=100, gain=0.18, seed=0):
    """fond musical synthétisé.
    tense : pulsation grave + tic-tac, sad : arpèges pincés lents (gamme mineure), japan : koto pentatonique, epic : nappe + percus"""
    rr = np.random.default_rng(seed)
    beat = 60 / bpm
    n_beats = int((t1 - t0) / beat)
    if mood == 'tense':
        for k in range(n_beats):
            t = t0 + k * beat
            tt = A.t_(0.35)
            kick = np.sin(2 * np.pi * (55 * np.exp(-tt * 8) + 38) * tt) * np.exp(-tt * 9)
            mx.add(kick, t, gain * (1.0 if k % 2 == 0 else 0.55))
            mx.add(A.tick(), t + beat / 2, gain * 0.35)
        dr = t1 - t0
        tt = A.t_(dr)
        pad = (np.sin(2 * np.pi * 55 * tt) + 0.4 * np.sin(2 * np.pi * 82.4 * tt)) * 0.4
        mx.add(A.norm(pad, 0.5), t0, gain * 0.5, 1.0, 1.0)
    elif mood in ('sad', 'japan', 'hope'):
        if mood == 'japan':
            scale_ = [220.0, 246.9, 261.6, 329.6, 349.2, 440.0, 493.9, 523.3]   # mode « miyako-bushi »
        elif mood == 'hope':
            scale_ = [261.6, 293.7, 329.6, 392.0, 440.0, 523.3, 587.3, 659.3]
        else:
            scale_ = [220.0, 261.6, 293.7, 329.6, 349.2, 440.0, 523.3]
        k = 0
        t = t0
        while t < t1 - 0.5:
            f = scale_[rr.integers(0, len(scale_))] if k % 4 else scale_[0] / (1 if mood != 'sad' else 2)
            mx.add(pluck_c(f, 2.0), t, gain * (0.9 if k % 4 == 0 else 0.6))
            t += beat * (1 if mood != 'sad' else 2)
            k += 1
        dr = t1 - t0
        tt = A.t_(dr)
        base = scale_[0] / 2
        pad = sum(np.sin(2 * np.pi * base * r * tt) for r in (1, 1.5, 2.0)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.1 * tt))
        mx.add(A.norm(A.lp_fast(pad, 800), 0.4), t0, gain * 0.35, 1.5, 1.5)
    elif mood == 'epic':
        for k in range(n_beats):
            t = t0 + k * beat
            tt = A.t_(0.5)
            tom = np.sin(2 * np.pi * (90 * np.exp(-tt * 5) + 50) * tt) * np.exp(-tt * 6)
            if k % 4 in (0, 3) or k % 8 == 6:
                mx.add(tom, t, gain)
        dr = t1 - t0
        tt = A.t_(dr)
        pad = sum(np.sign(np.sin(2 * np.pi * f * tt)) * a for f, a in ((73.4, 1.0), (110, 0.6), (146.8, 0.4)))
        mx.add(A.norm(A.lp_fast(pad, 500), 0.5), t0, gain * 0.5, 0.8, 1.0)


def cut_sounds(mx, starts, gain=0.12, skip=()):
    """petit « swoosh » sur chaque changement de plan pour dynamiser"""
    for i, t in enumerate(sorted(starts)):
        if i == 0 or t in skip:
            continue
        mx.add(swoosh(0.3), t - 0.15, gain)
