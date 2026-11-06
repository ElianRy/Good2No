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

if NAME == 'roy':
    th = WT(0, 'frapper') + 0.1
    lt = th + 0.02
    cam = Cam((1.4, 1.2, 4.8), (-0.3, 2.4, 0), 60)
    pose = hit_pose(lt, th, dict(la=(0, 0.1, 0.1), ra=(0, 0.1, 0.1)))
    pose['face'] = 'roy_shock'
    m1, k = strike(cam, lt, th, (0, 1.95, 0), top=(-1.5, 45, -10), seed=1, width=0.3)
    m2, _ = strike(cam, lt, th, (-6, 0, -14), top=(-10, 45, -40), seed=7, width=0.4)
    ms = merge([SUMMIT, m1, m2, ROY_N.mesh((0, 0, 0), 0.25, pose), rain_mesh(cam, 3.0, 160, 10),
                smoke_sprites((0, 2.0, 0), 1.0, cam, n=4, size=0.3, rise=1.2, seed=5, alpha=0.5)])
    env = storm_env(0.6, (0, 2, 0))
    img = vignette(shot(ms, cam, env), 0.35)
    title(img, [[('FRAPPÉ', W_), ('7', Y_), ('FOIS', W_)], [('PAR', W_), ('LA', W_), ('FOUDRE', Y_)], [('…ET', W_), ('VIVANT', R_)]], y0=120, size=112)

elif NAME == 'jack':
    base = BOX_BASE
    pull = 0.75
    g = lever_grip(base, 2, pull)
    cam = Cam((26.05, 3.25, -5.62), (25.95, 3.85, -3.0), 82)
    ms = [STATION, lever_frame([0, 0, pull, 0, 0, 0]).xf(trans(base)),
          box(4.2, 0.04, 3.2, (140, 105, 70), 'planks').xf(trans(26, 2.5, -4.2)),
          box(4.2, 2.0, 0.1, (220, 212, 190), 'planks_white', faces='f').xf(trans(26, 2.5, -5.7)),
          clock_mesh(10, 10, 0.24).xf(trans(24.6, 3.95, -5.62))]
    # Jack tourné vers la caméra, une main sur le levier, casquette, gueule ouverte
    body = np.array([25.95, 2.5, -4.25])
    ms.append(JACK.mesh(tuple(body), 0.0, bab_stand(cap=True, mouth=0.7, hp=0.1, hy=0.0, ra=(2.7, 0.5), la=(0.5, 0.4))).xf(M(trans(body), roty(math.pi), trans(-body))))
    ms.append(train(['loco', 'tender', 'car'], x=36.0, wheel_rot=0.0).xf(trans(0, 0, 0)))
    env = ENV_DAY.copy(points=[((26.0, 4.2, -3.2), (255, 235, 200), 0.8, 4), ((26.0, 3.8, -5.2), (255, 240, 215), 1.6, 3.5)])
    img = vignette(shot(merge(ms), cam, env), 0.3)
    title(img, [[('UN', W_), ('BABOUIN', Y_)], [('AIGUILLEUR', W_)], [('DE', W_), ('TRAINS', Y_)], [('PENDANT', W_), ('9', R_), ('ANS', W_)]], y0=90, size=102)

else:
    kind, p = SHIPS[0]
    lt = 0.5
    cam = Cam((p[0] + 10, 10.0, p[2] + 42), (PAL_POS[0] + 2, 5.0, -8), 50)
    ms = [TOWN, how(9, 15), pal(0.7), sea(t=2.0), warship(kind, 2.0, gun_yaws=aim_yaws(kind, p, 1.0)).xf(ship_matrix(p)),
          flagpole('red_cloth', 7, 2.0, 3.2, 2.0).xf(trans(FLAG_WORLD))]
    for tip in barrel_tips(kind, p, 1.0):
        ms.append(muzzle(tip, 0.6, cam, 3))
        ms.append(smoke_sprites(tip, 1.0, cam, n=3, size=3, rise=4, seed=3, col=(220, 220, 215), drift=(0.3, 0, -0.8), alpha=0.6))
    for k, (te, pos) in enumerate(((0.35, (6, 10, -11)), (0.15, (18, 6, -11)), (0.5, (0, 12, -12)))):
        ms.append(explosion(np.array(pos, float), te, cam, 6, k))
    ms.append(big_smoke(PAL_POS + np.array([0, 13, 0]), 2.0, cam, 12, 8, 28, 3))
    for k, dx in enumerate((-9, -3, 3, 9)):
        ms.append(fire_sprites(PAL_POS + np.array([dx, 9 + (k % 2) * 3, 7.6]), 1.0 + k, cam, 6, 2.6, 2.5, 30 + k))
    env = ENV_SMOKE.copy(points=[(tuple(PAL_POS + np.array([0, 8, 10])), (255, 140, 60), 1.3, 40)])
    img = vignette(shot(merge(ms), cam, env), 0.3)
    title(img, [[('LA', W_), ('GUERRE', W_)], [('LA', W_), ('PLUS', W_), ('COURTE', Y_)], [('DE', W_), ("L'HISTOIRE", W_)], [('38', R_), ('MINUTES', R_)]], y0=90, size=102)

img.save(f'{OUT}/miniature_{NAME}.png')
print('ok', NAME)
