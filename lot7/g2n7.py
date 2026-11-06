"""Commun au lot 7 (5 nov. 2026) : look PS1 renforcé, émeu à chapeau, pastilles obligatoires.
À importer EN PREMIER dans chaque video.py (règle le moteur avant tout rendu)."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n']
import engine as _E
_E.PS1_MODE = True                      # sommets qui tremblent + textures affines
_E.W, _E.H, _E.UPS = 180, 320, 6        # basse déf agrandie x6 sans lissage -> pixels bien visibles
import lib
lib.SIMPLE_FACES = True                 # visages 2 points
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from lib import *
import common2 as C2
import audio as A

OW, OH = 1080, 1920
INTER = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
POPPINS = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'

# ------------------------------------------------------------------ émeu à chapeau (comme le logo)
EMU_BODY = (122, 92, 62)
EMU_NECK = (105, 110, 132)
EMU_HAT = (112, 82, 50)
tex_noise('emu_feath', (95, 70, 45), (140, 108, 74), seed=401, octaves=3, speck=0.12, speck_col=(70, 52, 34))
tex_noise('emu_skin', (92, 98, 122), (118, 124, 148), seed=402, octaves=2)


def emu_mesh(pos=(0, 0, 0), yaw=0.0, phase=0.0, walk=0.0, peck=0.0, look=0.0, scale_=1.0, statue=None):
    """émeu low-poly ~1,7 m, regarde +z. statue=(r,g,b) -> tout d'une couleur (figurine, bronze, bois)"""
    def col(c):
        return np.asarray(statue if statue is not None else c, float)
    tf = None if statue is not None else 'emu_feath'
    ts = None if statue is not None else 'emu_skin'
    root = M(trans(pos), roty(yaw), scale(scale_))
    ms = []
    bob = abs(math.sin(phase)) * 0.03 * walk
    body = M(root, trans(0, 1.02 + bob, 0))
    # corps : gros œuf de plumes, un peu penché vers l'avant
    ms.append(sphere(0.42, 8, 5, col((255, 255, 255)) if tf else col(EMU_BODY), tf or 0, sy=0.72).xf(M(body, rotx(0.15), scale(0.8, 1.0, 1.35))))
    ms.append(sphere(0.3, 7, 4, col((235, 235, 235)) if tf else col(EMU_BODY), tf or 0, sy=0.8).xf(M(body, trans(0, -0.08, -0.38))))   # croupion
    # cou
    nb = M(body, trans(0, 0.18, 0.36))
    neck_top = M(nb, rotx(-0.15 + peck * 1.2), trans(0, 0.55, 0))
    ms.append(rod(nb[:3, 3], neck_top[:3, 3], 0.075, col((255, 255, 255)) if ts else col(EMU_NECK), ts or 0, 6))
    ms.append(sphere(0.13, 6, 4, col((235, 235, 235)) if tf else col(EMU_BODY), tf or 0).xf(M(nb, trans(0, 0.02, 0))))
    # tête
    head = M(neck_top, roty(look), rotx(-peck * 0.6))
    hc = col((255, 255, 255)) if ts else col(EMU_NECK)
    ms.append(box(0.27, 0.22, 0.27, hc, ts or 0).xf(M(head, trans(0, -0.06, 0.02))))
    # bec sombre (pyramide aplatie)
    bk = col((48, 42, 40))
    ms.append(frustum(0.15, 0.09, 0.03, 0.02, 0.15, bk).xf(M(head, trans(0, -0.01, 0.15))))
    # gros yeux blancs + pupilles noires sur les côtés (comme le logo)
    for s in (-1, 1):
        if statue is None:
            ms.append(box(0.03, 0.12, 0.13, (240, 240, 234), emis=0.35).xf(M(head, trans(s * 0.14, -0.01, 0.05))))
            ms.append(box(0.02, 0.07, 0.07, (12, 12, 12)).xf(M(head, trans(s * 0.157, 0.01, 0.075))))
        else:
            ms.append(box(0.03, 0.1, 0.11, col((0, 0, 0)) * 0.6).xf(M(head, trans(s * 0.14, -0.01, 0.05))))
    # chapeau mou marron (bord + calotte cabossée) : posé, pas de crâne qui dépasse
    hat = M(head, trans(0, 0.15, 0), rotx(-0.1))
    hcol = col(EMU_HAT)
    ms.append(cyl(0.29, 0.29, 0.025, 10, hcol).xf(hat))
    ms.append(cyl(0.2, 0.17, 0.17, 8, hcol).xf(M(hat, trans(0, 0.015, 0))))
    ms.append(cyl(0.202, 0.198, 0.04, 8, col((60, 42, 25)), caps=False).xf(M(hat, trans(0, 0.02, 0))))
    ms.append(box(0.05, 0.035, 0.26, col(np.asarray(EMU_HAT) * 0.8)).xf(M(hat, trans(0, 0.175, 0))))
    # pattes grises
    for s, ph in ((-1, 0.0), (1, math.pi)):
        sw = math.sin(phase + ph) * 0.5 * walk
        hip = M(body, trans(s * 0.15, -0.15, 0.0), rotx(sw))
        knee = M(hip, trans(0, -0.42, 0))
        ms.append(rod(hip[:3, 3], knee[:3, 3], 0.04, col((120, 118, 112)), 0, 5))
        foot = M(knee, rotx(-max(0, -sw) * 0.8), trans(0, -0.45, 0.04))
        ms.append(rod(knee[:3, 3], foot[:3, 3], 0.03, col((120, 118, 112)), 0, 5))
        fb = M(trans(foot[:3, 3]), roty(yaw))
        for a in (-0.4, 0, 0.4):
            ms.append(box(0.025, 0.02, 0.13, col((110, 108, 100))).xf(M(fb, roty(a), trans(0, 0, 0.05))))
    return merge(ms)


def emu_image(size=300, statue=None):
    """image de l'émeu à chapeau seul (fond transparent), rendue avec le moteur PS1"""
    W0, H0 = _E.W, _E.H
    _E.W, _E.H = 110, 140
    env = Env(sky_top=(0, 255, 0), sky_hor=(0, 255, 0), fog=(0, 255, 0), fog_near=100, fog_far=200, amb=0.55, light=(-0.5, 0.8, 0.6))
    cam = Cam((0.75, 1.95, 1.75), (0, 1.62, 0.25), 40)   # portrait 3/4 comme le logo : tête, chapeau, cou, haut du corps
    img, zb = render(emu_mesh((0, 0, 0), 0.75, statue=statue), cam, env)
    _E.W, _E.H = W0, H0
    rgb = np.asarray(Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)))
    a = (zb < 1e8).astype(np.uint8) * 255
    im = Image.fromarray(np.dstack([rgb, a]), 'RGBA')
    bb = im.getbbox()
    im = im.crop(bb)
    k = size / max(im.size)
    return im.resize((max(1, int(im.size[0] * k)), max(1, int(im.size[1] * k))), Image.NEAREST)


EMU_IMG = None


def _emu_img():
    global EMU_IMG
    if EMU_IMG is None:
        EMU_IMG = emu_image(260)
    return EMU_IMG


def _outline(im, w=6, col=(255, 255, 255, 255)):
    """liseré autour d'une image RGBA (pour qu'elle ressorte sur le décor)"""
    a = np.asarray(im)[..., 3] > 0
    big = Image.new('RGBA', (im.size[0] + 2 * w, im.size[1] + 2 * w), (0, 0, 0, 0))
    m = Image.fromarray((a * 255).astype(np.uint8)).resize(im.size)
    from PIL import ImageFilter
    mm = Image.new('L', big.size, 0)
    mm.paste(m, (w, w))
    mm = mm.filter(ImageFilter.MaxFilter(2 * w + 1))
    big.paste(Image.new('RGBA', big.size, col), (0, 0), mm)
    big.paste(im, (w, w), im)
    return big


def _alpha(layer, a):
    if a >= 1:
        return layer
    arr = np.asarray(layer).copy()
    arr[..., 3] = (arr[..., 3] * max(0.0, a)).astype(np.uint8)
    return Image.fromarray(arr)


def emu_pastille(t0=3.3, dur=3.2, y=300):
    """« TROUVE L'ÉMEU CACHÉ DANS CETTE VIDÉO » + l'émeu à chapeau. Tiers haut (zone sûre 250-700 px), centré."""
    f = ImageFont.truetype(INTER, 58)
    emu = _outline(_emu_img().resize((180, int(180 * _emu_img().size[1] / _emu_img().size[0])), Image.NEAREST), 5)

    def ov(img, t):
        u = t - t0
        if not (0 <= u < dur):
            return
        s = C2._pop(u)
        a = 1.0 if u < dur - 0.2 else (dur - u) / 0.2
        Wd, Hd = 1000, 330
        layer = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.rounded_rectangle([8, 18, Wd - 8, Hd - 12], radius=34, fill=(15, 15, 20, 230), outline=(255, 226, 60, 255), width=6)
        ex = 30
        ey = (Hd - emu.size[1]) // 2 + 3
        bobble = int(math.sin(u * 7) * 4)
        layer.paste(emu, (ex, ey + bobble), emu)
        tx = ex + emu.size[0] + 26
        lines = ["TROUVE L'ÉMEU", 'CACHÉ DANS', 'CETTE VIDÉO 👀'.replace(' 👀', '')]
        yy = 52
        for i, ln in enumerate(lines):
            d.text((tx, yy), ln, font=f, fill=(255, 226, 60, 255) if i == 0 else (255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
            yy += 74
        if s != 1.0:
            layer = layer.resize((int(Wd * s), int(Hd * s)), Image.BILINEAR)
        layer = _alpha(layer, a)
        img.paste(layer, ((OW - layer.size[0]) // 2, y + (Hd - layer.size[1]) // 2), layer)
    return ov


def retiens(t0, dur=2.4, y=300, text='👀 RETIENS ÇA'):
    """pastille « RETIENS ÇA » (boucle ouverte), en haut dans la zone sûre"""
    f = ImageFont.truetype(INTER, 66)

    def ov(img, t):
        u = t - t0
        if not (0 <= u < dur):
            return
        s = C2._pop(u)
        a = 1.0 if u < dur - 0.2 else (dur - u) / 0.2
        layer = Image.new('RGBA', (OW, 200), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        txt = 'RETIENS ÇA'
        w = d.textlength(txt, font=f)
        eye = 70
        bw = w + eye + 90
        x0 = (OW - bw) / 2
        d.rounded_rectangle([x0, 30, x0 + bw, 170], radius=30, fill=(255, 226, 60, 255), outline=(0, 0, 0, 255), width=6)
        # petits yeux dessinés (pas d'emoji dans la police)
        cx, cy = x0 + 50, 100
        for dx in (-17, 17):
            d.ellipse([cx + dx - 15, cy - 20, cx + dx + 15, cy + 20], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=4)
            px = int(math.sin(u * 3) * 5)
            d.ellipse([cx + dx - 6 + px, cy - 6, cx + dx + 6 + px, cy + 8], fill=(0, 0, 0, 255))
        d.text((x0 + eye + 45, 100), txt, font=f, fill=(15, 15, 15, 255), anchor='lm')
        jx = int(math.sin(u * 40) * 5) if u < 0.4 else 0
        if s != 1.0:
            layer = layer.resize((int(OW * s), int(200 * s)), Image.BILINEAR)
        layer = _alpha(layer, a)
        img.paste(layer, ((OW - layer.size[0]) // 2 + jx, y - (layer.size[1] - 200) // 2), layer)
    return ov


def end_card(t0, dur, y=430):
    """« ALORS, TU AS TROUVÉ L'ÉMEU ? » + l'émeu à chapeau (centré, tiers haut-milieu)"""
    f = ImageFont.truetype(INTER, 68)
    emu = _outline(_emu_img().resize((300, int(300 * _emu_img().size[1] / _emu_img().size[0])), Image.NEAREST), 7)

    def ov(img, t):
        u = t - t0
        if not (0 <= u < dur):
            return
        s = C2._pop(u)
        a = 1.0 if u < dur - 0.2 else (dur - u) / 0.2
        Wd, Hd = 900, 640
        layer = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.rounded_rectangle([10, 10, Wd - 10, Hd - 10], radius=44, fill=(15, 15, 20, 225), outline=(255, 226, 60, 255), width=7)
        for i, ln in enumerate(['ALORS, TU AS', "TROUVÉ L'ÉMEU ?"]):
            d.text((Wd / 2, 80 + i * 82), ln, font=f, fill=(255, 226, 60, 255) if i else (255, 255, 255, 255), anchor='mm',
                   stroke_width=3, stroke_fill=(0, 0, 0, 255))
        bob = int(math.sin(u * 5) * 6)
        layer.paste(emu, ((Wd - emu.size[0]) // 2, 190 + bob), emu)
        if s != 1.0:
            layer = layer.resize((int(Wd * s), int(Hd * s)), Image.BILINEAR)
        layer = _alpha(layer, a)
        img.paste(layer, ((OW - layer.size[0]) // 2, y + (Hd - layer.size[1]) // 2), layer)
    return ov


def year_badge(text, t0, dur=1.6, y=720):
    return C2.badge(text, t0, dur, y=y)


# ------------------------------------------------------------------ montage commun
class Cut:
    """petit utilitaire : enregistre les plans avec un nom, pour l'audio et la planche contact"""
    def __init__(self, tl):
        self.tl, self.st = tl, {}

    def add(self, name, t0, fn):
        self.st[name] = t0
        self.tl.add(t0, fn)

    def __getitem__(self, k):
        return self.st[k]


def run(tl, subs, here, name, build_audio, argv):
    """mêmes commandes que les vidéos précédentes : --part / --sheet / --at / (rien = rendu final)"""
    from video_core import part_main, contact_sheet, frame, render_video, mix_voice
    if len(argv) > 1 and argv[1] == '--part':
        part_main(tl, subs, argv[2:])
    elif len(argv) > 1 and argv[1] == '--sheet':
        ts = sorted(t for t, _ in tl.shots)
        times = []
        for i, t0 in enumerate(ts):
            t1 = ts[i + 1] if i + 1 < len(ts) else tl.duration()
            times.append((t0 + t1) / 2)
        for k in range(0, len(times), 40):
            contact_sheet(tl, times[k:k + 40], os.path.join(here, f'sheet{k // 40 + 1}.png'), subs, cols=8, scale=0.16)
    elif len(argv) > 1 and argv[1] == '--at':
        for s in argv[2:]:
            frame(tl, float(s), subs).resize((540, 960), Image.NEAREST).save(os.path.join(here, f'at_{s}.png'))
    else:
        build_audio(os.path.join(here, 'sfx.wav'))
        mix_voice(os.path.join(here, 'voix.wav'), os.path.join(here, 'sfx.wav'), os.path.join(here, 'mix.wav'))
        render_video(tl, os.path.join(here, f'{name}.mp4'), os.path.join(here, 'mix.wav'), subs)
