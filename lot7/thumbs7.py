"""Miniatures du lot 7 (1080x1920) : rendu PS1 identique aux vidéos (180x320 x6), titre entier tout en haut, numéro d'épisode.
usage : python3 thumbs7.py chaise|viande|fleming"""
import sys, os, math, runpy
NAME = sys.argv[1]
sys.argv = ['thumb']
G = runpy.run_path(f'/home/claude/g2n/lot7/{NAME}/video.py', run_name='thumb')
import engine
engine.W, engine.H, engine.UPS = 180, 320, 6   # même look PS1 que les vidéos (pixels bien visibles)
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
OUT = '/home/claude/g2n/lot7/livrables'
os.makedirs(OUT, exist_ok=True)
W_, Y_, R_ = (255, 255, 255), (255, 226, 60), (255, 80, 60)


def shot(fn, lt, dur, tg, cam=None):
    m, c, e = fn(lt, dur, tg)[:3]
    img, _ = engine.render(m, cam or c, e)
    return Image.fromarray(engine.upscale(engine.ps1_post(img)))


def darken_top(img, frac=0.5, k=0.65):
    a = np.asarray(img).astype(np.float32)
    h = a.shape[0]
    g = np.clip(1 - np.arange(h) / (h * frac), 0, 1)[:, None, None] * k
    return Image.fromarray((a * (1 - g)).clip(0, 255).astype(np.uint8))


def title(img, lines, y0=150, size=112):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, size)
    y = y0
    for line in lines:
        sp = d.textlength(' ', font=f)
        widths = [d.textlength(t, font=f) for t, _ in line]
        tot = sum(widths) + sp * (len(line) - 1)
        ff = f
        if tot > 1010:
            ff = ImageFont.truetype(FONT, int(size * 1010 / tot))
            widths = [d.textlength(t, font=ff) for t, _ in line]
            sp = d.textlength(' ', font=ff)
            tot = sum(widths) + sp * (len(line) - 1)
        x = (1080 - tot) / 2
        for (t, c), w in zip(line, widths):
            d.text((x + 7, y + 9), t, font=ff, fill=(0, 0, 0), stroke_width=13, stroke_fill=(0, 0, 0))
            d.text((x, y), t, font=ff, fill=c, stroke_width=12, stroke_fill=(0, 0, 0))
            x += w + sp
        y += int(ff.size * 1.12)
    return y


def episode(img, n, y, serie=None):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 50)
    txt = f'ÉPISODE {n}' + (f' · {serie}' if serie else '')
    w = d.textlength(txt, font=f)
    if w > 980:
        f = ImageFont.truetype(FONT, int(50 * 980 / w))
        w = d.textlength(txt, font=f)
    x0 = (1080 - w) / 2 - 28
    d.rounded_rectangle([x0, y, x0 + w + 56, y + f.size + 34], radius=22, fill=(235, 30, 60), outline=(0, 0, 0), width=5)
    d.text((540, y + (f.size + 34) / 2), txt, font=f, fill=(255, 255, 255), anchor='mm')


if NAME == 'chaise':
    img = shot(G['shot_hook'], 1.0, 2.6, 1.0, G['Cam']((2.6, 1.0, 5.2), (0.0, 2.6, -0.4), 60))
    img = darken_top(img)
    y = title(img, [[('IL', W_), ('VOLE', W_), ('SUR', W_), ('UNE', W_)], [('CHAISE', Y_), ('DE', Y_), ('JARDIN', Y_)], [('À', W_), ('5 000 M', R_)]], 120)
    episode(img, 22, y + 30)
elif NAME == 'viande':
    img = shot(G['shot_hook'], 0.7, 2.6, 0.7)
    img = darken_top(img)
    y = title(img, [[('IL', W_), ('A', W_), ('PLU', W_)], [('DE', Y_), ('LA', Y_), ('VIANDE', Y_)], [('CRUE', R_), ('!', R_)]], 120, 120)
    episode(img, 23, y + 30)
else:
    img = shot(G['shot_title'], 0.5, 1.6, 0.5, G['Cam']((0.0, 2.2, 0.75), (0, 0, 0), 40))
    img = darken_top(img)
    y = title(img, [[('SA', W_), ('VAISSELLE', W_), ('SALE', W_)], [('A', W_), ('SAUVÉ', Y_), ('DES', W_)], [('MILLIONS', R_), ('DE', W_), ('VIES', R_)]], 120, 108)
    episode(img, 24, y + 30)
img.save(f'{OUT}/miniature_ep{dict(chaise=22, viande=23, fleming=24)[NAME]}.png')
print('ok', NAME)
