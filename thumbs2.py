"""Miniatures verticales 1080x1920 (rendu interne x2 pour plus de détails) + titre en haut."""
import sys, os, math
sys.argv = ['x']
NAME = os.environ['THUMB']
sys.path[:0] = [f'/home/claude/g2n/{NAME}', '/home/claude/g2n']
import engine
engine.W, engine.H, engine.UPS = 540, 960, 2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

src = open(f'/home/claude/g2n/{NAME}/video.py').read().split('if __name__')[0]
exec(src)

FONT = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
OUT = '/home/claude/g2n/thumbs'
os.makedirs(OUT, exist_ok=True)


def shot(mesh, cam, env, extra=None):
    img, _ = engine.render(mesh, cam, env)
    if extra and 'post_lin' in extra:
        img = extra['post_lin'](img)
    return Image.fromarray(engine.upscale(engine.ps1_post(img)))


def title(img, lines, y0=150, size=118):
    """lines : liste de lignes, chaque ligne = liste de (texte, couleur)"""
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, size)
    y = y0
    for line in lines:
        widths = [d.textlength(t, font=f) for t, _ in line]
        sp = d.textlength(' ', font=f)
        x = (1080 - sum(widths) - sp * (len(line) - 1)) / 2
        for (t, c), w in zip(line, widths):
            # ombre portée puis contour épais
            d.text((x + 8, y + 10), t, font=f, fill=(0, 0, 0), stroke_width=14, stroke_fill=(0, 0, 0), anchor='la')
            d.text((x, y), t, font=f, fill=c, stroke_width=13, stroke_fill=(0, 0, 0), anchor='la')
            x += w + sp
        y += int(size * 1.12)
    return img


def vignette(img, k=0.45):
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    m = np.clip(1 - k * np.clip(r - 0.6, 0, 1) ** 1.5, 0, 1)
    a = np.asarray(img).astype(np.float32) * m[..., None]
    # dégradé sombre en haut pour le titre
    g = np.clip(1 - (yy / (h * 0.5)), 0, 1)[..., None] * 0.6
    a = a * (1 - g)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


W_, Y_, R_ = (255, 255, 255), (255, 226, 60), (255, 70, 50)

def from_shot(fn, lt, dur, tg, cam=None):
    m, c, e, ex = fn(lt, dur, tg)
    img = shot(m, cam or c, e, ex)
    if ex.get('post_pil'):
        ex['post_pil'](img)
    return img


if NAME == 'violet':
    m, c, e, ex = shot_hook(1.2, 2.5, 1.2)
    cam = Cam((-230, 5, 135), (-75, 24, 0), 52)
    img = vignette(shot(m, cam, e), 0.3)
    title(img, [[('3', R_), ('NAUFRAGES.', W_)], [('1', Y_), ('SEULE', W_)], [('SURVIVANTE.', Y_)]], y0=110, size=116)
elif NAME == 'gage':
    m, c, e = xray_frame(0, 0, 1.0, -0.35, fov=40, dist=1.15)
    c = Cam((c.pos[0], c.pos[1] - 0.12, c.pos[2]), (0, -0.07, 0), 40)
    img = vignette(shot(m, c, e), 0.3)
    title(img, [[('UNE', W_), ('BARRE', W_), ('DE', W_), ('FER', Y_)], [('DANS', W_), ('LE', W_), ('CRÂNE…', Y_)], [('ET', W_), ('IL', W_), ('PARLE', R_), ('!', R_)]], y0=110, size=100)
else:
    m, c, e, ex = shot_snow(1.0, 2.0, 1.0)
    fw = np.array([math.sin(DOG_YAW - 0.45), 0, math.cos(DOG_YAW - 0.45)])
    cam = Cam(tuple(SPOT + fw * 2.6 + np.array([0, 1.0, 0])), tuple(SPOT + np.array([0.0, 0.45, 0.0])), 48)
    img = vignette(shot(m, cam, e), 0.3)
    title(img, [[('IL', W_), ('A', W_), ('ATTENDU', W_)], [('SON', W_), ('MAÎTRE', Y_)], [('9', R_), ('ANS', R_), ('ET', W_), ('DEMI', R_)]], y0=110, size=108)

img.save(f'{OUT}/miniature_{NAME}.png')
print('ok', NAME)
