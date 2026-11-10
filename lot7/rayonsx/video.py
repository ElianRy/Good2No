"""Ép. 27 — Les rayons X : la main d'Anna Bertha Röntgen (Les accidents qui ont changé la science) : Würzburg, 1895."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n/lot7']
from props7 import *
from video_core import *

HERE = '/home/claude/g2n/lot7/rayonsx'
timing = load_timing(os.path.join(HERE, 'timing.json'))
tl = Timeline(timing)
T, WT = tl.T, tl.word_t
END = timing[-1]['t1'] + 0.3
tl.duration = lambda: END
cut = Cut(tl)

# ------------------------------------------------------------------ personnages
make_face('roentgen', skin=(230, 195, 170), beard=True, hair_col=(70, 60, 55))
make_face('roentgen_c', skin=(230, 195, 170), beard=True, hair_col=(70, 60, 55), eyes_closed=True)
make_face('anna', skin=(236, 205, 185), hair_col=(110, 85, 60))
make_face('doc96', skin=(225, 188, 160), mustache=True, hair_col=(60, 50, 40))
make_face('patient', skin=(232, 195, 170), hair_col=(140, 100, 60))
make_face('biz', skin=(228, 190, 160), mustache=True, hair_col=(30, 25, 22))
make_face('crowd1', skin=(230, 192, 165), hair_col=(90, 60, 40))
make_face('crowd2', skin=(215, 175, 140), mustache=True, hair_col=(50, 40, 30))
make_face('tech', skin=(190, 140, 105), hair_col=(30, 25, 20))
make_face('kid', skin=(235, 200, 175), hair_col=(160, 110, 60))
RO = Human('roentgen', skin=(230, 195, 170), shirt=(240, 238, 230), pants=(45, 45, 50), hair=(70, 60, 55), jacket=(55, 52, 50), tie=(30, 30, 30))
RO_C = Human('roentgen_c', skin=(230, 195, 170), shirt=(240, 238, 230), pants=(45, 45, 50), hair=(70, 60, 55), jacket=(55, 52, 50), tie=(30, 30, 30))
ANNA = Human('anna', skin=(236, 205, 185), shirt=(255, 255, 255), shirt_tex='dress_dark', pants=(60, 40, 52), hair=(110, 85, 60), robe=(62, 40, 52),
             extra=C2.woman_extra('bun', hair=(110, 85, 60)))
DOC = Human('doc96', skin=(225, 188, 160), shirt=(240, 240, 235), pants=(50, 50, 55), hair=(60, 50, 40), jacket=(238, 236, 228))
PATIENT = Human('patient', skin=(232, 195, 170), shirt=(200, 190, 160), pants=(80, 70, 60), hair=(140, 100, 60), sleeves='short')
BIZ = Human('biz', skin=(228, 190, 160), shirt=(240, 240, 235), pants=(35, 35, 40), hair=(30, 25, 22), jacket=(35, 35, 40), hat='bowler', hat_col=(25, 25, 25), tie=(120, 30, 30))
CROWD = [Human('crowd1', skin=(230, 192, 165), shirt=(150, 60, 70), pants=(60, 50, 60), hair=(90, 60, 40), robe=(140, 55, 65), hat='bonnet', hat_col=(60, 40, 50),
               extra=C2.woman_extra('bun', hair=(90, 60, 40))),
         Human('crowd2', skin=(215, 175, 140), shirt=(220, 215, 200), pants=(70, 60, 50), hair=(50, 40, 30), jacket=(90, 75, 60), hat='flatcap', hat_col=(80, 70, 60)),
         Human('doc96', skin=(225, 188, 160), shirt=(230, 230, 225), pants=(40, 40, 45), hair=(60, 50, 40), jacket=(50, 50, 60), hat='bowler', hat_col=(30, 30, 30)),
         Human('kid', skin=(235, 200, 175), shirt=(70, 100, 150), pants=(60, 60, 70), hair=(160, 110, 60), height=0.7, build=0.85)]
TECH = Human('tech', skin=(190, 140, 105), shirt=(90, 150, 170), pants=(90, 150, 170), hair=(30, 25, 20), sleeves='short')
MODPAT = Human('patient', skin=(232, 195, 170), shirt=(200, 70, 60), pants=(60, 70, 100), pants_tex='denim', hair=(140, 100, 60))

# ------------------------------------------------------------------ ambiances
GLOW = (170, 255, 190)
TUBE = np.array([-0.5, 0.9, -1.3])            # tube de Crookes sur la paillasse
SCREEN = np.array([1.7, 0.75, -0.6])          # écran fluorescent posé plus loin, sur un tabouret
PLATE = np.array([0.25, 0.905, -0.98])         # plaque photo (main d'Anna)
ENV_LAB = Env(sky_top=(60, 50, 40), sky_hor=(60, 50, 40), fog=(45, 38, 30), fog_near=6, fog_far=26, amb=0.55, light=(0.3, 0.85, 0.4), light_col=(255, 220, 170),
              points=[((0.9, 1.9, -1.0), (255, 210, 140), 0.6, 4)])


def env_dark(glow_k=0.0, screen_k=0.0):
    pts = []
    if glow_k > 0:
        pts.append((tuple(TUBE + np.array([0, 0.3, 0.15])), GLOW, 0.7 * glow_k, 1.4))
    if screen_k > 0:
        pts.append((tuple(SCREEN + np.array([0, 0.5, 0.25])), (190, 255, 160), 0.9 * screen_k, 1.6))
    return Env(sky_top=(10, 10, 14), sky_hor=(12, 12, 16), fog=(8, 8, 12), fog_near=3, fog_far=14, amb=0.12, light=(0.3, 0.8, 0.4), light_col=(80, 90, 110), points=pts)


ENV_NIGHT = Env(sky_top=(10, 14, 35), sky_hor=(40, 45, 70), fog=(30, 34, 55), fog_near=20, fog_far=160, amb=0.35, light=(0.3, 0.8, -0.3), light_col=(150, 170, 220))
ENV_DAY = Env(sky_top=(100, 140, 200), sky_hor=(210, 210, 205), fog=(195, 195, 190), fog_near=30, fog_far=200, amb=0.55, light=(-0.4, 0.8, 0.4))
ENV_HALL = Env(sky_top=(60, 50, 45), sky_hor=(60, 50, 45), fog=(50, 42, 36), fog_near=10, fog_far=40, amb=0.6, light=(0.2, 0.9, 0.3), light_col=(255, 230, 190),
               points=[((0, 3.0, -1.0), (255, 230, 180), 0.6, 5)])
ENV_MODERN = Env(sky_top=(70, 80, 90), sky_hor=(70, 80, 90), fog=(60, 68, 78), fog_near=10, fog_far=40, amb=0.62, light=(0.2, 0.9, 0.4), light_col=(235, 245, 255))
VINT = lambda im: C2.tint((255, 215, 160), 0.18)(im)


# ------------------------------------------------------------------ le labo de Würzburg
def _blackboard(d, n):
    d.rectangle([0, 0, n, n], fill=(30, 45, 35))
    for k in range(5):
        d.line([2, 4 + k * 5, 10 + (k * 7) % 12, 4 + k * 5], fill=(200, 205, 195))
    d.line([18, 6, 28, 22], fill=(240, 240, 235), width=2)
    d.line([28, 6, 18, 22], fill=(240, 240, 235), width=2)


tex_draw('blackboard', _blackboard)


def lab(emu=False):
    rr = np.random.default_rng(2)
    ms = [box(8, 0.05, 7, (255, 255, 255), 'planks', ts=1.5), box(8, 3.4, 0.12, (255, 255, 255), 'wallpaper_red', ts=2.0).xf(trans(0, 0, -2.2)),
          box(0.12, 3.4, 7, (255, 255, 255), 'wallpaper_red', ts=2.0).xf(trans(-2.6, 0, 0)), box(0.12, 3.4, 7, (255, 255, 255), 'wallpaper_red', ts=2.0).xf(trans(2.8, 0, 0))]
    ms.append(box(8, 0.9, 0.05, (90, 60, 40), 'wood_dark').xf(trans(0, 0, -2.13)))           # lambris
    ms.append(box(1.2, 1.6, 0.06, (255, 255, 255), 'window').xf(trans(1.6, 1.3, -2.12)))
    ms.append(bench_table(2.4, 0.9, 0.9, (255, 255, 255), 'wood_dark').xf(trans(0, 0, -1.2)))
    ms.append(induction_coil().xf(trans(-1.05, 0.9, -1.35)))
    for a, b in (((-0.85, 1.1, -1.3), (-0.75, 1.2, -1.3)), ((-1.25, 1.1, -1.3), (-1.25, 0.95, -1.6))):
        ms.append(rod(a, b, 0.01, (180, 140, 60), n=3))
    ms.append(rod((-0.85, 1.12, -1.3), (-0.75, 1.2, -1.3), 0.008, (40, 40, 40), n=3))
    for k in range(5):
        ms.append(bottle(0.2, 0.045, [(110, 70, 40), (60, 90, 60), (200, 200, 190)][k % 3], alpha=0.85).xf(trans(0.65 + k * 0.1, 0.9, -1.55)))
    ms.append(box(0.4, 0.05, 0.3, (230, 225, 210)).xf(M(trans(0.95, 0.905, -1.45), roty(0.3))))     # cahier
    ms.append(gas_lamp(True).xf(trans(1.05, 0.9, -1.0)))
    # tabouret + écran fluorescent posé plus loin
    ms.append(box(0.45, 0.72, 0.45, (90, 60, 40), 'wood_dark').xf(trans(SCREEN[0], 0, SCREEN[2])))
    # étagère à gauche (bocaux, livres)
    ms.append(shelf(1.4, 2.2, 0.4, 4).xf(M(trans(-2.25, 0, -0.6), roty(math.pi / 2))))   # décollée du mur (pas de mélange de textures)
    for lv in range(4):
        for j in range(4):
            if emu and lv == 3 and j == 1:
                continue
            ms.append(box(0.25, 0.3, 0.06 + 0.04 * rr.random(), [(120, 50, 40), (50, 70, 100), (130, 110, 60)][(lv + j) % 3]).xf(trans(-2.25, lv * 0.55 + 0.03, -1.1 + j * 0.32)))
    if emu:   # statuette en bronze d'un émeu à chapeau, sur le haut de l'étagère
        ms.append(cyl(0.13, 0.15, 0.05, 10, (70, 50, 32)).xf(trans(-2.25, 2.2, -0.75)))                     # socle en bois tourné
        ms.append(cyl(0.11, 0.11, 0.02, 10, (180, 150, 90)).xf(trans(-2.25, 2.25, -0.75)))
        ms.append(emu_mesh((-2.25, 2.27, -0.75), math.pi / 2 - 0.4, scale_=0.34))                          # statuette peinte, détaillée, avec son chapeau
    # tableau noir avec un grand X
    ms.append(box(1.4, 1.0, 0.04, (255, 255, 255), 'blackboard').xf(trans(-0.9, 1.5, -2.12)))
    ms.append(box(1.5, 0.05, 0.08, (90, 60, 40)).xf(trans(-0.9, 1.48, -2.08)))
    # chaise, fauteuil, poêle
    ms.append(box(0.45, 0.45, 0.45, (90, 60, 40), 'wood_dark').xf(trans(0.2, 0, -0.35)))
    ms.append(box(0.45, 0.55, 0.05, (90, 60, 40), 'wood_dark').xf(trans(0.2, 0.45, -0.57)))
    ms.append(cyl(0.3, 0.3, 1.0, 8, (40, 40, 42)).xf(trans(2.3, 0, -1.6)))
    ms.append(cyl(0.06, 0.06, 2.4, 6, (40, 40, 42)).xf(trans(2.3, 1.0, -1.6)))
    return merge(ms)


LAB = lab()
LAB_EMU = lab(emu=True)


def tube_on(glow, covered=False):
    ms = [crookes_tube(glow).xf(trans(TUBE))]
    if covered:
        ms.append(black_box().xf(trans(TUBE)))
    if glow > 0 and not covered:
        ms.append(Mesh())
    return merge(ms)


def screen_at(lit, hand=False):
    return xray_screen(lit, hand).xf(M(trans(SCREEN[0], 0.72, SCREEN[2]), roty(-0.9)))


# ------------------------------------------------------------------ 0. accroche
def plate_hold(c, hold_h=1.32):
    hold = np.array([c[0], hold_h, c[2] + 0.38])
    plate = photo_plate(1.0).xf(M(trans(hold + np.array([0, 0.12, 0.02])), rotx(-0.15), scale(1.2)))
    pose = dict(ik_l=tuple(hold + np.array([-0.17, -0.02, 0])), ik_r=tuple(hold + np.array([0.17, -0.02, 0])), hp=0.3)
    return plate, pose


def shot_hook(lt, dur, tg, p=None):
    """Anna tient la plaque développée : on voit les os de sa main et sa bague. Poussée rapide"""
    p = lt if p is None else p
    c = np.array([0.6, 0, -0.2])
    plate, pose = plate_hold(c)
    u = min(1.0, max(0.0, p) / 1.2)
    cam = Cam((c[0] + 0.25, 1.48, c[2] + 1.7 - 0.6 * u), (c[0], 1.4, c[2] + 0.35), 48)
    ms = [LAB, ANNA.mesh(tuple(c), 0.0, pose), plate, tube_on(0.0)]
    return merge(ms), cam, ENV_LAB, dict(post_pil=VINT)


def shot_hook_plate(lt, dur, tg):
    """gros plan : la main squelette et l'alliance"""
    c = np.array([0.6, 0, -0.2])
    plate, pose = plate_hold(c)
    g = np.array([c[0], 1.47, c[2] + 0.4])
    cam = cam_lerp(Cam(tuple(g + np.array([0.05, 0.02, 0.55])), tuple(g), 45), Cam(tuple(g + np.array([0.03, 0.02, 0.4])), tuple(g), 42), lt / dur)
    return merge([LAB, ANNA.mesh(tuple(c), 0.0, pose), plate]), cam, ENV_LAB, dict(post_pil=VINT)


def scream_pose(k):
    return dict(ik_l=(-0.1, 1.55 + 0.05 * k, 0.12), ik_r=(0.1, 1.55 + 0.05 * k, 0.12), lean=-0.2 * k, hp=-0.15 * k)


def shot_scream(lt, dur, tg):
    """elle recule, les mains sur le visage : « J'ai vu ma mort ! »"""
    k = min(1.0, lt / 0.25)
    c = np.array([0.6, 0, -0.2])
    pose = dict(la=(2.3 * k + 0.2, 0.2, 2.2 * k), ra=(2.3 * k + 0.2, 0.2, 2.2 * k), lean=-0.2 * k, hp=-0.1 * k)
    plate = photo_plate(1.0).xf(M(trans(c + np.array([0.0, 0.94, -0.75])), rotx(-math.pi / 2 + 0.2)))
    cam = Cam((c[0] + 0.3, 1.5, c[2] + 1.6), (c[0], 1.4, c[2]), 45)
    ms = [LAB, ANNA.mesh(tuple(c - np.array([0, 0, 0.08 * k])), 0.0, pose)]
    return merge(ms), C2.shake(cam, 0.05 * C2.decay(lt, 0.05, 6), tg), ENV_LAB, dict(post_pil=VINT, flash=0.3 * C2.decay(lt, 0.05, 10))


# ------------------------------------------------------------------ 1-3. Würzburg, le tube, le carton noir
def shot_title(lt, dur, tg):
    """le tube de Crookes s'allume dans le noir, crépitements"""
    fl = 0.7 + 0.3 * math.sin(tg * 40)
    g = TUBE + np.array([0, 0.3, 0])
    cam = cam_lerp(Cam(tuple(g + np.array([0.6, 0.15, 0.7])), tuple(g), 42), Cam(tuple(g + np.array([0.4, 0.1, 0.5])), tuple(g), 40), lt / dur)
    return merge([LAB, tube_on(fl)]), cam, env_dark(fl), {}


def institute():
    ms = [ground(-80, -80, 80, 80, 'gravel', ts=3.0), box(36, 12, 14, (255, 255, 255), 'stone_block', ts=2.0).xf(trans(0, 0, -12))]
    for x in np.arange(-15, 16, 3.0):
        for y in (2.0, 6.5):
            if y < 5 and abs(x) < 2.6:     # pas de fenêtre sur la porte d'entrée
                continue
            lit = (x * 7 + y) % 3 < 1
            ms.append(box(1.4, 2.4, 0.1, (255, 255, 255), 'window_lit' if lit else 'window').xf(trans(x, y, -4.95)))
            ms.append(box(1.7, 0.2, 0.25, (190, 180, 160)).xf(trans(x, y - 0.15, -4.9)))
    ms.append(box(3, 3.5, 0.15, (255, 255, 255), 'door').xf(trans(0, 0, -4.9)))
    for x in (-2, 2):
        ms.append(cyl(0.3, 0.3, 5, 8, (200, 195, 180)).xf(trans(x, 0, -4.4)))
    ms.append(box(5.5, 0.5, 1.4, (190, 185, 170)).xf(trans(0, 5, -4.4)))
    ms.append(box(6, 0.3, 2.0, (180, 175, 160)).xf(trans(0, 0, -3.6)))
    for x in (-10, 10):
        ms.append(cyl(0.06, 0.06, 3.5, 5, (40, 40, 40)).xf(trans(x, 0, 0)))
        ms.append(box(0.4, 0.5, 0.4, (255, 220, 150), emis=0.9).xf(trans(x, 3.5, 0)))
    for i in range(8):
        ms.append(deciduous(7, 2.2, i).xf(trans((-24 - i * 4) if i % 2 else (24 + i * 4), 0, -2 + (i % 3) * 3)))
    return merge(ms)


INST = institute()


def shot_city(lt, dur, tg):
    """l'institut de physique de Würzburg, la nuit : une seule fenêtre reste allumée tard"""
    u = lt / max(dur, 0.1)
    cam = Cam((-6 + 4 * u, 3, 18 - 2 * u), (0, 5, -6), 50)
    snow = C2.particles((0, 5, 5), tg, cam, 40, (10, 6, 8), 0.8, 0.08, (240, 240, 250), seed=1)
    return merge([INST, snow]), cam, ENV_NIGHT, {}


def shot_roentgen(lt, dur, tg):
    """Röntgen à sa paillasse, la bobine crépite, le tube s'allume"""
    fl = 0.6 + 0.4 * math.sin(tg * 35)
    pose = dict(ik_r=(-0.85, 1.05, -1.15), la=(0.4, 0.1, 0.6), hp=0.35, lean=0.15)
    sp = billboard((-0.95, 1.14, -1.3), 0.12, 0.12, Cam((1, 1.6, 1.2), (-0.5, 1.1, -1.3)), (230, 220, 255), 'spark', emis=1.0) if (tg * 9) % 1 < 0.4 else Mesh()
    cam = cam_lerp(Cam((1.0, 1.6, 1.2), (-0.5, 1.15, -1.2), 50), Cam((0.8, 1.55, 0.9), (-0.5, 1.15, -1.2), 48), lt / dur)
    ms = [LAB, tube_on(fl), sp, RO.mesh((-0.5, 0, -0.45), math.pi, pose)]
    return merge(ms), cam, ENV_LAB.copy(amb=0.45), dict(post_pil=VINT)


def shot_cover(lt, dur, tg):
    """il couvre le tube d'un carton noir (à deux mains), puis éteint la lampe"""
    k = min(1.0, lt / 1.2)
    bb = black_box().xf(trans(TUBE + np.array([0, 0.5 * (1 - k), 0.0])))
    hold = TUBE + np.array([0, 0.45 + 0.5 * (1 - k), 0.0])
    pose = dict(ik_l=tuple(hold + np.array([-0.22, 0, 0.05])), ik_r=tuple(hold + np.array([0.22, 0, 0.05])), hp=0.4, lean=0.2)
    off = lt > dur - 0.6
    cam = Cam((0.6, 1.6, 0.9), (-0.5, 1.1, -1.3), 50)
    env = ENV_LAB.copy(amb=0.4) if not off else env_dark(0.0)
    return merge([LAB, crookes_tube(0.8).xf(trans(TUBE)), bb, RO.mesh((-0.5, 0, -0.5), math.pi, pose)]), cam, env, dict(post_pil=VINT)


# ------------------------------------------------------------------ 4-6. l'écran brille, les os des doigts, « X »
def shot_dark(lt, dur, tg):
    """dans le noir complet : le carton noir… et plus loin, l'écran se met à briller"""
    t_on = WT(4, 'briller.') - cut['dark'] - 0.4
    lit = min(1.0, max(0.0, lt - t_on) * 2.5)
    cam = Cam((-0.3, 1.5, 1.6), (1.0, 0.9, -0.9), 52)
    ms = [LAB, tube_on(0.7, covered=True), screen_at(lit), RO.mesh((0.3, 0, -0.3), 0.9, dict(hy=0.6 * lit, ra=(0.3, 0.1, 0.3)))]
    return merge(ms), cam, env_dark(0.05, lit), {}


SN = np.array([-math.sin(0.9), 0.0, math.cos(0.9)])      # normale de l'écran (vers l'avant)
SS = np.array([math.cos(0.9), 0.0, math.sin(0.9)])       # côté de l'écran


def shot_hand(lt, dur, tg):
    """il passe lentement la main devant l'écran : l'ombre de ses os apparaît sur l'écran"""
    s = np.array([SCREEN[0], 1.2, SCREEN[2]])
    k = min(1.0, max(0.0, (lt - 0.2) / 1.0))                 # la main monte et glisse devant l'écran
    hand = s + SN * 0.16 + SS * (0.35 * (1 - k)) + np.array([0, -0.25 * (1 - k), 0])
    body = s + SN * 0.62 - SS * 0.12
    yaw = math.atan2(-SN[0], -SN[2])
    pose = dict(ik_r=tuple(hand), la=(0.2, 0.1, 0.3), hp=0.15, lean=0.15)
    cp = s + SN * 1.05 + SS * 0.75 + np.array([0, 0.25, 0])
    cam = Cam(tuple(cp), tuple(s + SN * 0.1 + np.array([0, 0.0, 0])), 50)
    ms = [LAB, screen_at(1.0, hand=k > 0.85), RO.mesh((body[0], 0, body[2]), yaw, pose)]
    return merge(ms), cam, env_dark(0.05, 1.0).copy(amb=0.22), {}


def shot_screen_bones(lt, dur, tg):
    """gros plan sur l'écran : les os des doigts"""
    s = np.array([SCREEN[0], 1.2, SCREEN[2]])
    cam = Cam(tuple(s + np.array([-0.3 * math.sin(0.9), 0.02, 0.3 * math.cos(0.9)]) ), tuple(s), 45)
    return merge([LAB, screen_at(1.0, hand=True)]), cam, env_dark(0.0, 1.0), {}


def shot_puzzled(lt, dur, tg):
    """il ne sait pas ce que c'est : il note un grand X au tableau"""
    pose = dict(ra=(2.4, 0.3, 0.6), la=(0.3, 0.1, 0.4), hp=-0.2)
    cam = cam_lerp(Cam((0.6, 1.6, 0.9), (-0.9, 1.6, -2.1), 50), Cam((0.4, 1.6, 0.6), (-0.9, 1.7, -2.1), 46), lt / dur)
    return merge([LAB, RO.mesh((-0.3, 0, -1.5), math.pi - 0.4, pose), tube_on(0.0, covered=True)]), cam, ENV_LAB, dict(post_pil=VINT)


# ------------------------------------------------------------------ 7. des semaines enfermé (émeu en bronze sur l'étagère)
def shot_weeks(lt, dur, tg):
    """il mange et dort au labo : endormi sur sa chaise, assiette vide à côté"""
    pose = sit_pose(drop=0.47, lean=0.45, hp=0.7, la=(0.9, 0.1, 1.6), ra=(0.9, 0.1, 1.6))
    plate = merge([cyl(0.13, 0.11, 0.02, 10, (240, 240, 235)), cyl(0.05, 0.05, 0.03, 6, (160, 120, 70)).xf(trans(0.03, 0.02, 0))]).xf(trans(0.75, 0.905, -0.95))
    u = lt / max(dur, 0.1)
    cam = Cam((1.3 - 0.3 * u, 1.6, 1.5), (-1.0, 1.35, -0.7), 56)
    ms = [LAB_EMU, RO_C.mesh((0.2, 0, -0.35), math.pi, pose), plate, tube_on(0.0, covered=True)]
    return merge(ms), cam, ENV_LAB.copy(amb=0.42), dict(post_pil=VINT)


# ------------------------------------------------------------------ 8-11. la main d'Anna
def tube_over_plate(glow):
    stand = merge([cyl(0.012, 0.012, 0.5, 4, (60, 60, 62)).xf(trans(PLATE[0] + 0.25, 0.9, PLATE[2] - 0.15)),
                   box(0.3, 0.02, 0.02, (60, 60, 62)).xf(trans(PLATE[0] + 0.12, 1.38, PLATE[2] - 0.15))])
    t = crookes_tube(glow).xf(M(trans(PLATE[0], 1.05, PLATE[2] - 0.15)))
    return merge([stand, t])


def flat_hand(c, skin=(236, 205, 185)):
    """main d'Anna posée à plat sur la plaque, doigts vers -z ; c = centre de la paume"""
    ms = [box(0.085, 0.022, 0.1, skin)]
    for k, L in enumerate((0.07, 0.085, 0.08, 0.065)):
        ms.append(box(0.018, 0.018, L, skin).xf(trans(-0.03 + k * 0.02, 0, -0.05 - L / 2)))
    ms.append(box(0.02, 0.018, 0.06, skin).xf(M(trans(-0.04, 0, 0.0), roty(0.6), trans(0, 0, -0.03))))
    ms.append(box(0.02, 0.006, 0.015, (215, 180, 70)).xf(trans(-0.01, 0.018, -0.08)))     # alliance
    return merge(ms).xf(trans(c))


def anna_at_plate(k=1.0):
    """Anna, penchée, la main gauche posée à plat sur la plaque : la main est placée là où l'IK amène vraiment le poignet"""
    wrist = PLATE + np.array([0.02, 0.06, 0.14])
    body = ANNA.mesh((PLATE[0] - 0.005, 0, PLATE[2] + 0.5), math.pi, dict(ik_l=tuple(wrist), la=(0.3, 0.1, 0.3), hp=0.4, lean=0.3))
    h = ANNA.attach['hand_l'][:3, 3]
    return merge([body, flat_hand((h[0], PLATE[1] + 0.018, h[2] - 0.055))])


def flat_plate():
    return merge([box(0.32, 0.012, 0.38, (60, 50, 40)).xf(trans(PLATE)), box(0.28, 0.004, 0.34, (95, 105, 115)).xf(trans(PLATE + np.array([0, 0.012, 0])))])


def shot_anna(lt, dur, tg):
    """22 décembre : Anna pose sa main sur la plaque, sous le tube"""
    cam = cam_lerp(Cam((1.6, 1.6, -1.85), (0.2, 1.05, -0.8), 52), Cam((1.45, 1.55, -1.85), (0.2, 1.05, -0.8), 50), lt / dur)
    ms = [LAB, flat_plate(), tube_over_plate(0.0), anna_at_plate(), RO.mesh((-0.6, 0, -0.5), 2.2, dict(ra=(1.2, 0.3, 0.8), hy=0.2))]
    return merge(ms), cam, ENV_LAB, dict(post_pil=VINT)


def shot_wait(lt, dur, tg):
    """gros plan : la main immobile sous le tube qui luit ; l'horloge tourne"""
    fl = 0.7 + 0.3 * math.sin(tg * 30)
    g = PLATE + np.array([0, 0.05, 0])
    cam = cam_lerp(Cam(tuple(g + np.array([-0.6, 0.6, 0.45])), tuple(g), 48), Cam(tuple(g + np.array([-0.5, 0.52, 0.38])), tuple(g), 45), lt / dur)
    clock = clock_mesh(3, (lt * 400) % 60).xf(M(trans(1.0, 1.0, -1.35), scale(0.6)))
    ms = [LAB, flat_plate(), tube_over_plate(fl), anna_at_plate(), clock]
    return merge(ms), cam, ENV_LAB.copy(amb=0.42, points=[(tuple(PLATE + np.array([0, 0.3, 0])), GLOW, 0.6 * fl, 1.0)]), {}


def shot_develop(lt, dur, tg):
    """dans la cuve du révélateur, l'image apparaît : les os… et l'alliance"""
    k = min(1.0, lt / 1.8)
    tray = merge([box(0.5, 0.03, 0.6, (30, 30, 30))] + [box(0.5, 0.07, 0.02, (30, 30, 30)).xf(trans(0, 0, s_ * 0.29)) for s_ in (-1, 1)] + [box(0.02, 0.07, 0.6, (30, 30, 30)).xf(trans(s_ * 0.24, 0, 0)) for s_ in (-1, 1)]).xf(trans(0.0, 0.9, -1.2))
    pl = photo_plate(k).xf(M(trans(0.0, 0.94, -1.17), rotx(-math.pi / 2), scale(0.95)))
    cam = cam_lerp(Cam((0.1, 1.55, -0.55), (0.0, 0.93, -1.12), 45), Cam((0.08, 1.45, -0.65), (0.0, 0.93, -1.12), 42), lt / dur)
    return merge([LAB, tray, pl]), cam, ENV_LAB.copy(amb=0.55, points=[]), dict(post_pil=C2.tint((255, 90, 70), 0.4))


# ------------------------------------------------------------------ 12-17. le monde s'affole, médecins, foires, brevet, Nobel
def shot_cta(lt, dur, tg):
    fl = 0.7 + 0.3 * math.sin(tg * 30)
    u = lt / max(dur, 0.1)
    cam = Cam((1.4 - 0.4 * u, 1.8, 1.6), (-0.3, 1.0, -1.2), 52)
    return merge([LAB, tube_on(fl), screen_at(0.8)]), cam, env_dark(fl, 0.8).copy(amb=0.25), {}


def shot_news(lt, dur, tg):
    """les journaux du monde entier publient la main squelette"""
    ms = []
    for k in range(7):
        a = tg * 2 + k * 0.9
        r = 0.6 + 0.15 * k
        p = np.array([r * math.cos(a), 1.2 + 0.25 * math.sin(a * 1.3 + k), r * math.sin(a) - 1.0])
        ms.append(box(0.42, 0.56, 0.01, (255, 255, 255), 'newspaper').xf(M(trans(p), roty(-a + 1.0), rotz(0.3 * math.sin(a)))))
    ms.append(hand_image(True, True, bg=(200, 200, 200), flesh=(150, 150, 150), bone=(60, 60, 60)).xf(M(trans(0, 1.25, -1.0), scale(1.8))))
    cam = Cam((0, 1.3, 1.2 - lt * 0.3), (0, 1.2, -1.0), 55)
    env = Env(sky_top=(230, 220, 190), sky_hor=(230, 220, 190), fog=(230, 220, 190), fog_near=10, fog_far=30, amb=0.7)
    return merge(ms), cam, env, dict(post_pil=VINT)


def clinic():
    ms = [box(7, 0.05, 6, (255, 255, 255), 'planks'), box(7, 3, 0.1, (230, 225, 210), 'plaster').xf(trans(0, 0, -2.4)),
          box(0.1, 3, 6, (225, 220, 205), 'plaster').xf(trans(-2.8, 0, 0))]
    ms.append(bench_table(1.4, 0.8, 0.85, (255, 255, 255), 'wood_dark').xf(trans(0, 0, -1.2)))
    ms.append(shelf(1.2, 1.8, 0.35, 3).xf(trans(1.6, 0, -2.2)))
    for k in range(4):
        ms.append(bottle(0.2, 0.045, [(110, 70, 40), (200, 220, 230)][k % 2]).xf(trans(1.2 + k * 0.25, 0.62, -2.2)))
    ms.append(box(0.6, 0.9, 0.05, (60, 60, 60), emis=0.0).xf(trans(-1.3, 1.4, -2.34)))
    return merge(ms)


CLINIC = clinic()


def shot_doctor(lt, dur, tg):
    """un médecin regarde l'écran : un os cassé (puis une pièce avalée)"""
    coin = lt > WT(14, 'objets') - cut['doctor'] - 0.1
    scr = xray_screen(1.0).xf(M(trans(0.15, 0.85, -1.4), scale(1.6)))
    img = hand_image(True, False, bg=(150, 220, 120), flesh=(110, 160, 90), bone=(45, 70, 40), fracture=not coin, coin=coin).xf(M(trans(0.15, 0.85 + 0.49 * 1.6, -1.4 + 0.03), scale(1.36)))
    ms = [CLINIC, scr, img, DOC.mesh((-0.55, 0, -0.6), 2.6, dict(hp=0.1, ra=(1.6, 0.3, 0.4))), PATIENT.mesh((0.75, 0, -0.9), -2.4, dict(ra=(1.3, 0.2, 0.2)))]
    cam = cam_lerp(Cam((0.6, 1.7, 0.7), (0.1, 1.45, -1.4), 48), Cam((0.5, 1.65, 0.4), (0.1, 1.5, -1.4), 44), lt / dur)
    return merge(ms), cam, ENV_DAY.copy(amb=0.6), dict(post_pil=VINT)


def fair():
    ms = [ground(-50, -50, 50, 50, 'grass_dry', ts=4.0)]
    ms.append(box(4, 2.6, 2.2, (255, 255, 255), 'planks_white').xf(trans(0, 0, -2)))
    ms.append(box(4.4, 0.15, 3.0, (255, 255, 255), 'awning').xf(M(trans(0, 2.6, -1.6), rotx(0.15))))
    for x in (-2.1, 2.1):
        ms.append(cyl(0.05, 0.05, 2.7, 5, (180, 160, 120)).xf(trans(x, 0, -0.2)))
    ms.append(box(3.0, 0.6, 0.05, (200, 40, 40)).xf(trans(0, 2.0, -0.85)))      # enseigne
    ms.append(box(2.8, 0.45, 0.06, (240, 220, 120)).xf(trans(0, 2.07, -0.83)))
    ms.append(box(1.2, 0.9, 0.7, (90, 60, 40), 'wood_dark').xf(trans(0, 0, -0.7)))   # comptoir
    ms.append(box(0.5, 0.35, 0.4, (40, 40, 40)).xf(trans(0, 0.9, -0.7)))             # boîte à regarder
    ms.append(box(0.18, 0.12, 0.12, (30, 30, 30)).xf(trans(0, 1.15, -0.45)))
    rr = np.random.default_rng(5)
    for i in range(10):
        ms.append(deciduous(rr.uniform(6, 8), 2.2, i).xf(trans(rr.uniform(-30, 30), 0, rr.uniform(-30, -8))))
    for i in range(4):
        ms.append(box(2.5, 2.4, 2.0, (255, 255, 255), 'planks_white').xf(trans(-8 + i * 5.5 if i < 2 else -2 + i * 4, 0, -9)))
        ms.append(box(2.8, 0.12, 2.4, (255, 255, 255), 'awning').xf(trans(-8 + i * 5.5 if i < 2 else -2 + i * 4, 2.4, -9)))
    return merge(ms)


FAIR = fair()


def shot_fair(lt, dur, tg):
    """à la foire : on paie pour voir ses os ; la foule rigole"""
    ms = [FAIR, CROWD[1].mesh((0.0, 0, 0.05), math.pi, dict(lean=0.4, hp=0.3, ik_r=(0.05, 1.0, -0.45), la=(0.2, 0.1, 0.3))),
          CROWD[0].mesh((-1.1, 0, 0.6), 2.6, dict(la=(1.0, 0.2, 1.8), ra=(0.4, 0.1, 0.3), hy=0.2 * math.sin(tg * 5))),
          CROWD[2].mesh((1.1, 0, 0.7), -2.6, dict(ra=(1.5, 0.3, 0.2), hy=-0.2)), CROWD[3].mesh((0.5, 0, 1.0), math.pi, dict(ra=(2.6, 0.4, 0.2), la=(2.6, 0.4, 0.2)))]
    ms.append(BIZ.mesh((0.0, 0, -1.4), 0.0, dict(ra=(1.0, 0.6, 0.4), la=(0.3, 0.1, 0.3))))
    cam = cam_lerp(Cam((2.2, 1.8, 4.2), (0, 1.2, -0.5), 50), Cam((1.8, 1.7, 3.6), (0, 1.2, -0.5), 48), lt / dur)
    return merge(ms), cam, ENV_DAY, dict(post_pil=VINT)


def study():
    ms = [box(7, 0.05, 6, (255, 255, 255), 'planks'), box(7, 3.2, 0.1, (255, 255, 255), 'wallpaper_red', ts=2.0).xf(trans(0, 0, -2.4)),
          box(0.1, 3.2, 6, (255, 255, 255), 'wallpaper_red', ts=2.0).xf(trans(-2.8, 0, 0))]
    ms.append(bench_table(1.8, 0.9, 0.78, (255, 255, 255), 'wood_dark').xf(trans(0, 0, -1.3)))
    ms.append(shelf(2.0, 2.4, 0.4, 5).xf(trans(1.6, 0, -2.2)))
    ms.append(gas_lamp(True).xf(trans(-0.6, 0.78, -1.5)))
    ms.append(box(0.8, 1.0, 0.04, (255, 255, 255), 'map_old').xf(trans(-1.0, 1.6, -2.34)))
    return merge(ms)


STUDY = study()


def shot_patent(lt, dur, tg):
    """un homme d'affaires lui tend un contrat de brevet : Röntgen le repousse"""
    no = 0.35 * math.sin(tg * 8) * min(1.0, max(0.0, lt - 0.5) * 3)
    paper = box(0.21, 0.01, 0.3, (245, 240, 225), 'note').xf(trans(0.2, 0.79, -1.1 - 0.15 * min(1, max(0, lt - 0.8))))
    ms = [STUDY, RO.mesh((0, 0, -2.0), 0.0, sit_pose(drop=0.45, hy=no, ra=(1.3, 0.1, 0.1), la=(0.6, 0.1, 0.6))), box(0.5, 0.45, 0.5, (90, 60, 40)).xf(trans(0, 0, -2.1)),
          BIZ.mesh((0.4, 0, -0.3), math.pi, dict(ra=(1.0, 0.1, 0.4), lean=0.15)), paper]
    cam = cam_lerp(Cam((1.7, 1.6, 0.3), (0, 1.0, -1.5), 50), Cam((1.5, 1.55, 0.1), (0, 1.0, -1.5), 48), lt / dur)
    return merge(ms), cam, ENV_HALL, dict(post_pil=VINT)


def hall():
    ms = [box(14, 0.05, 14, (255, 255, 255), 'planks'), box(14, 6, 0.1, (255, 255, 255), 'wallpaper_red', ts=2.5).xf(trans(0, 0, -4)),
          box(6, 0.6, 3, (110, 70, 45), 'wood_dark').xf(trans(0, 0, -2.6))]
    ms.append(box(4, 2.5, 0.05, (60, 70, 120)).xf(trans(0, 2.5, -3.9)))
    for x in (-2.5, 2.5):
        ms.append(cyl(0.25, 0.25, 5, 8, (230, 225, 210)).xf(trans(x, 0, -3.6)))
    rr = np.random.default_rng(9)
    for r in range(3):
        for k in range(7):
            h = CROWD[(r + k) % 3]
            ms.append(h.mesh((-3 + k, 0, 1.5 + r * 1.1), math.pi, sit_pose(drop=0.45, hy=0.1 * rr.normal())))
            ms.append(box(0.5, 0.45, 0.5, (100, 60, 40)).xf(trans(-3 + k, 0, 1.6 + r * 1.1)))
    return merge(ms)


HALL = hall()


def shot_nobel(lt, dur, tg):
    """1901, Stockholm : Röntgen reçoit le tout premier prix Nobel de physique"""
    med = merge([cyl(0.05, 0.05, 0.01, 12, (230, 190, 70), emis=0.3)]).xf(M(trans(0.25, 1.45, -2.2), rotx(math.pi / 2)))
    ms = [HALL, RO.mesh((-0.25, 0.6, -2.6), 0.4, dict(ra=(1.3, -0.2, 0.2))), BIZ.mesh((0.55, 0.6, -2.6), -0.6, dict(ra=(1.4, 0.3, 0.2))), med]
    cam = cam_lerp(Cam((1.2, 1.7, 2.5), (0, 1.6, -2.4), 48), Cam((0.9, 1.75, 1.6), (0, 1.7, -2.4), 44), lt / dur)
    return merge(ms), cam, ENV_HALL, dict(post_pil=VINT, flash=0.3 if (tg * 2.3) % 1 < 0.05 else 0.0)


# ------------------------------------------------------------------ 18-21. le danger, aujourd'hui
def shot_danger(lt, dur, tg):
    """le tube luit, menaçant"""
    fl = 0.7 + 0.3 * math.sin(tg * 30)
    g = TUBE + np.array([0, 0.3, 0])
    cam = cam_lerp(Cam(tuple(g + np.array([-0.7, 0.1, 0.9])), tuple(g), 42), Cam(tuple(g + np.array([-0.55, 0.08, 0.7])), tuple(g), 40), lt / dur)
    return merge([LAB, tube_on(fl)]), cam, env_dark(fl), dict(post_pil=C2.chain(C2.tint((255, 60, 50), 0.3), lambda im: C2.vignette(im, 0.8)))


def shot_burn(lt, dur, tg):
    """un chercheur garde les mains sous les rayons pendant des heures… puis des bandages"""
    t_band = WT(19, 'brûlent') - cut['burn'] - 0.2
    band = lt > t_band
    hands = [TUBE + np.array([-0.08, 0.12, 0.22]), TUBE + np.array([0.08, 0.12, 0.22])]
    if not band:
        pose = dict(ik_l=tuple(hands[0]), ik_r=tuple(hands[1]), hp=0.4, lean=0.2)
        extra = []
        env = env_dark(0.9).copy(amb=0.3)
    else:
        pose = dict(la=(1.0, 0.1, 1.5), ra=(1.0, 0.1, 1.5), hp=0.5)
        extra = []
        env = ENV_LAB
    m = DOC.mesh((-0.5, 0, -0.55), math.pi, pose)
    if band:
        for k in ('hand_l', 'hand_r'):
            extra.append(box(0.11, 0.14, 0.13, (245, 245, 240)).xf(M(DOC.attach[k], trans(0, -0.12, 0))))
    cam = Cam((1.1, 1.6, -0.2), (-0.5, 1.1, -0.9), 52)
    return merge([LAB, tube_on(0.9 if not band else 0.0), m] + extra), cam, env, dict(post_pil=VINT)


def radiology():
    ms = [box(8, 0.05, 7, (255, 255, 255), 'tile_lab', ts=1.0), box(8, 3, 0.1, (220, 230, 235)).xf(trans(0, 0, -2.6)),
          box(0.1, 3, 7, (215, 225, 230)).xf(trans(-3, 0, 0)), xray_machine().xf(trans(0, 0, -1.4))]
    ms.append(box(1.0, 1.4, 0.06, (200, 210, 215)).xf(trans(2.2, 0, -2.0)))      # paravent plombé
    ms.append(box(0.4, 0.06, 0.4, (255, 220, 60)).xf(trans(2.2, 1.6, -1.95)))     # panneau rayonnement
    return merge(ms)


RADIO = radiology()
MOD_IMG = hand_image(True, True, bg=(15, 15, 20), flesh=(80, 80, 88), bone=(235, 235, 235), ring_col=(255, 255, 255))


def shot_modern(lt, dur, tg):
    """aujourd'hui : la main sur la table, bip, c'est fini en une fraction de seconde"""
    t_flash = 1.2
    pose = dict(ik_r=(0.05, 0.98, -1.35), la=(0.3, 0.1, 0.3), hp=0.3)
    ms = [RADIO, MODPAT.mesh((0.0, 0, -0.65), math.pi, pose), TECH.mesh((2.2, 0, -1.3), -1.4, dict(ra=(1.2, 0.2, 0.8)))]
    ms.append(monitor(MOD_IMG if lt > t_flash else None).xf(trans(2.2, 1.5, -1.0)))
    cam = cam_lerp(Cam((-1.3, 1.7, 0.6), (0.3, 1.0, -1.3), 52), Cam((-1.1, 1.65, 0.4), (0.3, 1.0, -1.3), 50), lt / dur)
    fl = C2.decay(lt, t_flash, 12) if lt > t_flash else 0
    return merge(ms), cam, ENV_MODERN, dict(flash=0.35 * fl, flash_col=(200, 220, 255))


def shot_monitor(lt, dur, tg):
    """l'écran : la main, nette, en un instant"""
    cam = cam_lerp(Cam((2.2, 1.75, -0.2), (2.2, 1.75, -1.0), 45), Cam((2.2, 1.75, -0.35), (2.2, 1.75, -1.0), 42), lt / dur)
    return merge([RADIO, monitor(MOD_IMG).xf(trans(2.2, 1.5, -1.0))]), cam, ENV_MODERN, {}


def shot_question(lt, dur, tg):
    fl = 0.6 + 0.3 * math.sin(tg * 30)
    u = lt / max(dur, 0.1)
    cam = Cam((1.6 - 0.2 * u, 1.55, -1.85), (0.2, 1.05, -0.8), 52)
    return merge([LAB, flat_plate(), tube_over_plate(fl), anna_at_plate()]), cam, env_dark(fl).copy(amb=0.35), dict(post_pil=VINT)


def shot_loop(lt, dur, tg):
    return shot_hook(lt, dur, tg, p=lt - dur)


# ------------------------------------------------------------------ montage
cut.add('hook', 0.0, shot_hook)
cut.add('hook_plate', WT(0, 'squelette…') - 0.4, shot_hook_plate)
cut.add('hook_scream', WT(0, 'crie') - 0.1, shot_scream)
cut.add('title', T(1), shot_title)
cut.add('city', T(2), shot_city)
cut.add('roentgen', WT(2, 'Wilhelm') - 0.1, shot_roentgen)
cut.add('cover', T(3), shot_cover)
cut.add('dark', T(4), shot_dark)
cut.add('hand', T(5), shot_hand)
cut.add('bones', WT(5, 'os') - 0.15, shot_screen_bones)
cut.add('puzzled', T(6), shot_puzzled)
cut.add('weeks', T(7), shot_weeks)
cut.add('anna', T(8), shot_anna)
cut.add('wait', T(9), shot_wait)
cut.add('develop', T(10), shot_develop)
cut.add('scream', T(11), shot_scream)
cut.add('cta', T(12), shot_cta)
cut.add('news', T(13), shot_news)
cut.add('doctor', T(14), shot_doctor)
cut.add('fair', T(15), shot_fair)
cut.add('patent', T(16), shot_patent)
cut.add('nobel', T(17), shot_nobel)
cut.add('danger', T(18), shot_danger)
cut.add('burn', T(19), shot_burn)
cut.add('modern', T(20), shot_modern)
cut.add('monitor', T(21), shot_monitor)
cut.add('question', T(22), shot_question)
cut.add('loop', T(23), shot_loop)


def minutes_clock():
    t0, t1 = cut['wait'], cut['develop']

    def ov(img, t):
        if t0 <= t < t1:
            n = min(15, 1 + int((t - t0) / (t1 - t0) * 15))
            C2.badge(f'{n} MIN', t0, t1 - t0, y=700)(img, t)
    return ov


tl.overlay = C2.overlays(
    C2.hook_title(['ELLE A VU', 'SON SQUELETTE'], 0.0, 2.6, y=250, accent=1),
    emu_pastille(3.3, 3.2, y=300),
    C2.badge('LES RAYONS X', T(1), 1.3, y=700),
    C2.badge('WÜRZBURG, 1895', T(2), 1.8, y=700),
    C2.badge('WILHELM RÖNTGEN', WT(2, 'Wilhelm') - 0.1, 2.0, y=700),
    C2.badge('X = INCONNU', WT(6, 'inconnu.') - 0.6, 1.6, y=700),
    C2.badge('22 DÉCEMBRE 1895', T(8), 1.9, y=700),
    retiens(T(9) - 0.1, max(2.2, T(10) - T(9)), y=300),
    minutes_clock(),
    C2.cta(T(12) - 0.1, max(1.6, T(13) - T(12) + 0.05)),
    C2.badge('PAS DE BREVET', WT(16, 'brevet.') - 0.2, 1.8, y=700),
    C2.badge('PRIX NOBEL 1901', T(17) + 0.3, 2.2, y=700),
    C2.badge('DANGER', T(18) + 0.3, 1.6, y=700, col=(255, 110, 90)),
    C2.badge('15 MIN → 0,1 S', WT(20, 'Aujourd\'hui,') - 0.1, 2.4, y=700),
    end_card(T(22), T(23) - T(22)),
)

subs = Subs(timing)


def build_audio(path):
    mx = A.Mixer(END)
    S = cut
    mx.add(C2.impact(), 0.0, 0.5)
    mx.add(A.whoosh(0.8), 0.2, 0.3)
    mx.add(A.sting(1.0), S['hook_plate'], 0.4)
    mx.add(C2.impact(), S['hook_scream'], 0.6)
    mx.add(A.arc_buzz(1.3), S['title'], 0.5)
    mx.add(A.wind(S['roentgen'] - S['city']), S['city'], 0.3)
    mx.add(A.arc_buzz(S['cover'] - S['roentgen']), S['roentgen'], 0.35)
    mx.add(A.clank(0.3), S['cover'] + 1.1, 0.4)
    mx.add(A.tick(), S['cover'] + (S['dark'] - S['cover']) - 0.55, 0.5)
    mx.add(A.arc_buzz(S['puzzled'] - S['dark']), S['dark'], 0.2)
    mx.add(C2.riser(1.0), WT(4, 'briller.') - 0.8, 0.35)
    mx.add(A.sting(1.0), S['bones'], 0.4)
    mx.add(A.tick(), WT(6, 'X.'), 0.4)
    for k in range(8):
        mx.add(A.tick(), S['weeks'] + 0.4 * k, 0.15)
    mx.add(A.footsteps(1.5, 2.0), S['anna'], 0.25)
    mx.add(C2.riser(1.2), T(9) - 0.4, 0.3)
    mx.add(C2.ding(), T(9) + 0.1, 0.4)
    for k in range(int((S['develop'] - S['wait']) / 0.5)):
        mx.add(A.tick(), S['wait'] + 0.5 * k, 0.4)
    mx.add(A.arc_buzz(S['develop'] - S['wait']), S['wait'], 0.2)
    mx.add(C2.water_rush(1.5), S['develop'], 0.2)
    mx.add(A.sting(1.0), WT(10, 'alliance.') - 0.1, 0.4)
    mx.add(C2.impact(), S['scream'], 0.6)
    mx.add(C2.pop(), T(12) + 0.05, 0.5)
    mx.add(C2.ding(), T(12) + max(1.6, T(13) - T(12)) * 0.62, 0.4)
    for k in range(6):
        mx.add(C2.swoosh(), S['news'] + 0.25 + k * 0.6, 0.4)
    mx.add(A.crowd(S['patent'] - S['fair']), S['fair'], 0.4)
    mx.add(A.crowd(1.5), S['fair'] + 0.6, 0.25)
    mx.add(C2.record_scratch(), S['patent'] + 0.5, 0.2)
    mx.add(A.crowd(S['danger'] - S['nobel']), S['nobel'], 0.3)
    mx.add(A.drumroll(1.5), S['nobel'], 0.3)
    mx.add(A.arc_buzz(S['burn'] - S['danger']), S['danger'], 0.45)
    mx.add(C2.heartbeat(2.0, 70), S['danger'], 0.35)
    mx.add(A.arc_buzz(1.5), S['burn'], 0.3)
    mx.add(C2.ding(0.4), S['modern'] + 1.2, 0.5)
    mx.add(A.tick(), S['modern'] + 1.2, 0.5)
    mx.add(A.arc_buzz(1.5), S['question'], 0.2)
    C2.cut_sounds(mx, list(cut.st.values()), 0.08)
    mx.save(path)


if __name__ == '__main__':
    run(tl, subs, HERE, 'Good2No_ep27_Rayons_X', build_audio, sys.argv)
