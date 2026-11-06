"""Ép. 24 — La pénicilline (Les accidents qui ont changé la science, ép. 3) : Fleming 1928, Oxford 1941, Peoria 1943."""
import sys, os, math
sys.path[:0] = ['/home/claude/g2n/lot7']
from props7 import *
from video_core import *

HERE = '/home/claude/g2n/lot7/fleming'
timing = load_timing(os.path.join(HERE, 'timing.json'))
tl = Timeline(timing)
T, WT = tl.T, tl.word_t
END = timing[-1]['t1'] + 0.3
tl.duration = lambda: END
cut = Cut(tl)

# ------------------------------------------------------------------ personnages
make_face('fleming', skin=(232, 196, 170), hair_col=(150, 140, 130))
make_face('florey', skin=(228, 190, 160))
make_face('chain', skin=(222, 186, 150), mustache=True, hair_col=(40, 30, 25))
make_face('alexander', skin=(225, 185, 160))
make_face('alexander_c', skin=(215, 175, 150), eyes_closed=True)
make_face('mary', skin=(235, 200, 175))
make_face('vendor', skin=(210, 165, 130), mustache=True, hair_col=(50, 40, 30))
make_face('lonp', skin=(225, 185, 150))
COAT = (238, 238, 232)
FLEMING = Human('fleming', skin=(232, 196, 170), shirt=(240, 240, 235), pants=(70, 70, 75), hair=(150, 140, 130), jacket=COAT, tie=(120, 30, 40))
FLEMING_OUT = Human('fleming', skin=(232, 196, 170), shirt=(240, 240, 235), pants=(70, 70, 75), hair=(150, 140, 130), jacket=(80, 75, 70), tie=(120, 30, 40),
                    hat='bowler', hat_col=(60, 55, 50))
FLOREY = Human('florey', skin=(228, 190, 160), shirt=(240, 240, 235), pants=(60, 60, 65), hair=(80, 60, 40), jacket=COAT, tie=(40, 50, 90))
CHAIN = Human('chain', skin=(222, 186, 150), shirt=(240, 240, 235), pants=(60, 60, 65), hair=(40, 30, 25), jacket=COAT, tie=(30, 30, 30))
ALEX = Human('alexander', skin=(225, 185, 160), shirt=(200, 210, 225), pants=(200, 210, 225), hair=(70, 55, 40))
ALEX_C = Human('alexander_c', skin=(215, 175, 150), shirt=(200, 210, 225), pants=(200, 210, 225), hair=(70, 55, 40))
MARY = Human('mary', skin=(235, 200, 175), shirt=(80, 120, 150), pants=(80, 120, 150), hair=(110, 70, 40), robe=(70, 110, 140),
             extra=C2.woman_extra('bun', hair=(110, 70, 40)))
VENDOR = Human('vendor', skin=(210, 165, 130), shirt=(220, 215, 200), pants=(70, 65, 60), hair=(50, 40, 30), hat='flatcap', hat_col=(90, 80, 70),
               extra=C2.woman_extra(None, apron=True) if False else None)
LONDONERS = [Human('lonp', skin=(225, 185, 150), shirt=(220, 220, 215), pants=(50, 50, 55), hair=(60, 45, 30), jacket=(60, 60, 70), hat='bowler', hat_col=(30, 30, 30)),
             Human('chain', skin=(222, 186, 150), shirt=(220, 220, 215), pants=(80, 70, 60), hair=(40, 30, 25), jacket=(110, 90, 70), hat='flatcap', hat_col=(80, 70, 60)),
             Human('mary', skin=(235, 200, 175), shirt=(140, 60, 70), pants=(140, 60, 70), hair=(70, 50, 30), robe=(130, 55, 65), hat='bonnet', hat_col=(60, 40, 50),
                   extra=C2.woman_extra('bun', hair=(70, 50, 30)))]

ENV_LAB = Env(sky_top=(70, 65, 58), sky_hor=(70, 65, 58), fog=(55, 50, 45), fog_near=8, fog_far=35, amb=0.6, light=(0.5, 0.8, 0.4),
              points=[((-1.5, 2.2, -1.0), (255, 235, 200), 0.6, 6)])
ENV_DAY = Env(sky_top=(110, 140, 185), sky_hor=(200, 205, 210), fog=(185, 190, 195), fog_near=40, fog_far=300, amb=0.55, light=(-0.4, 0.8, 0.4))
ENV_HOSP = Env(sky_top=(60, 64, 70), sky_hor=(60, 64, 70), fog=(50, 54, 60), fog_near=8, fog_far=35, amb=0.6, light=(0.3, 0.9, 0.3),
               points=[((0, 2.6, 0.5), (255, 245, 225), 0.6, 6)])
ENV_PEORIA = Env(sky_top=(70, 135, 210), sky_hor=(215, 220, 225), fog=(205, 210, 215), fog_near=40, fog_far=300, amb=0.55, light=(-0.3, 0.85, 0.5))
SEPIA = lambda im: C2.tint((255, 220, 170), 0.35, sepia=False)(im)


# ------------------------------------------------------------------ labo de St Mary's (1928)
def lab():
    ms = [box(9, 0.05, 8, (255, 255, 255), 'planks', ts=1.5), box(9, 3.4, 0.15, (255, 255, 255), 'brick_lon', ts=2.0).xf(trans(0, 0, -3)),
          box(0.15, 3.4, 8, (255, 255, 255), 'plaster_old', ts=2.5).xf(trans(-3.2, 0, 0)), box(0.15, 3.4, 8, (255, 255, 255), 'plaster_old', ts=2.5).xf(trans(3.2, 0, 0))]
    # fenêtre (avec vue) + paillasse dessous
    ms.append(box(1.6, 1.6, 0.06, (255, 255, 255), 'window').xf(trans(-0.6, 1.2, -2.92)))
    ms.append(bench_table(3.0, 0.9, 0.9, (255, 255, 255), 'wood_dark').xf(trans(-0.5, 0, -2.4)))
    ms.append(microscope().xf(trans(-1.4, 0.9, -2.4)))
    ms.append(cyl(0.05, 0.06, 0.15, 6, (60, 60, 65)).xf(trans(0.6, 0.9, -2.5)))          # bec Bunsen
    rr = np.random.default_rng(1)
    for k in range(9):   # piles de boîtes de Petri en désordre
        ms.append(petri_stack(int(rr.integers(3, 8)), 0.05, k).xf(trans(-0.9 + k * 0.17 + rr.uniform(-0.03, 0.03), 0.9, -2.2 + rr.uniform(-0.15, 0.15))))
    for k in range(6):
        ms.append(bottle(0.22, 0.045, [(110, 70, 40), (60, 90, 60), (200, 200, 190)][k % 3]).xf(trans(0.3 + k * 0.12, 0.9, -2.7)))
    for k in range(5):
        ms.append(box(0.3, 0.005, 0.22, (240, 235, 215)).xf(M(trans(0.2 + rr.uniform(-0.3, 0.6), 0.905 + k * 0.004, -2.2 + rr.uniform(-0.1, 0.15)), roty(rr.uniform(-0.6, 0.6)))))
    # étagère de droite (l'émeu figurine est caché parmi les flacons)
    ms.append(shelf(1.6, 2.2, 0.4, 4).xf(M(trans(2.95, 0, -1.2), roty(-math.pi / 2))))
    for k in range(4):
        for j in range(4):
            if k == 2 and j == 2:
                continue
            ms.append(bottle(0.24, 0.05, [(110, 70, 40), (60, 90, 60), (200, 200, 190), (70, 70, 120)][(k + j) % 4]).xf(trans(2.95, k * 0.545 + 0.03, -1.75 + j * 0.36)))
    ms.append(emu_mesh((2.92, 2 * 0.545 + 0.03, -1.75 + 2 * 0.36), -math.pi / 2, scale_=0.22))
    # deuxième table, pleine elle aussi
    ms.append(bench_table(1.6, 0.8, 0.9, (255, 255, 255), 'wood_dark').xf(trans(1.6, 0, 0.6)))
    for k in range(5):
        ms.append(petri_stack(int(rr.integers(2, 6)), 0.05, 20 + k).xf(trans(1.1 + k * 0.22, 0.9, 0.6 + rr.uniform(-0.2, 0.2))))
    ms.append(cyl(0.12, 0.08, 0.25, 8, (200, 225, 230), alpha=0.5).xf(trans(2.1, 0.9, 0.8)))
    # désordre : papiers par terre, livres empilés, caisse
    for k in range(10):
        ms.append(box(0.3, 0.004, 0.22, (240, 235, 215)).xf(M(trans(rr.uniform(-1.5, 2.2), 0.03, rr.uniform(-1.6, 1.5)), roty(rr.uniform(0, 3)))))
    for k in range(5):
        ms.append(box(0.32, 0.06, 0.24, [(120, 40, 40), (40, 60, 100), (60, 90, 50)][k % 3]).xf(M(trans(1.4, 0.9 + k * 0.06, 0.35), roty(rr.uniform(-0.3, 0.3)))))
    ms.append(box(0.6, 0.4, 0.5, (255, 255, 255), 'planks').xf(trans(2.4, 0, 1.6)))
    ms.append(box(0.6, 0.4, 0.5, (255, 255, 255), 'planks').xf(M(trans(2.4, 0.4, 1.6), roty(0.3))))
    # porte, porte-manteau, lampe
    ms.append(box(1.0, 2.2, 0.08, (255, 255, 255), 'door').xf(M(trans(-3.12, 0, 1.6), roty(math.pi / 2))))
    ms.append(cyl(0.03, 0.03, 1.8, 5, (60, 45, 30)).xf(trans(-2.7, 0, 0.4)))
    ms.append(box(0.3, 0.3, 0.3, (255, 235, 180), emis=0.7).xf(trans(-0.5, 3.0, -1.2)))
    ms.append(rod((-0.5, 3.4, -1.2), (-0.5, 3.3, -1.2), 0.01, (30, 30, 30), n=3))
    ms.append(box(1.4, 0.8, 0.03, (255, 255, 255), 'chart_lab').xf(trans(1.4, 1.8, -2.92)))
    return merge(ms)


def _chart(d, n):
    d.rectangle([0, 0, n, n], fill=(235, 228, 205))
    for k in range(4):
        d.ellipse([3 + k * 7, 6, 7 + k * 7, 10], outline=(60, 60, 60))
    for y in range(14, n - 2, 3):
        d.line([3, y, n - 4, y], fill=(120, 110, 95))


tex_draw('chart_lab', _chart, bg=(235, 228, 205))
LAB = lab()
DOOR = np.array([-2.9, 0, 1.6])
BENCH = np.array([-0.5, 0.9, -2.2])


def suitcase():
    return merge([box(0.5, 0.35, 0.15, (110, 70, 40)), box(0.12, 0.04, 0.03, (40, 30, 20)).xf(trans(0, 0.36, 0))])


def shot_hook(lt, dur, tg, p=None):
    """0 : les piles de boîtes sales au premier plan ; Fleming, chapeau et valise, s'en va en vacances"""
    p = lt if p is None else p
    u = min(1.0, max(0.0, (p + 2.0) / 5.0))
    st = np.array([-0.6, 0, -1.0])
    fp = st + (DOOR + np.array([0.6, 0, 0]) - st) * u
    yaw = math.atan2(DOOR[0] + 0.6 - st[0], DOOR[2] - st[2])
    ms = [LAB, FLEMING_OUT.mesh(tuple(fp), yaw, walk_pose(tg * 6, 0.8, ra=(0.1, 0.1, 0.1), hand_r=suitcase().xf(trans(0, -0.2, 0))))]
    cam = Cam((-0.35 + 0.03 * p, 1.32, -2.75 + 0.03 * p), (-2.2, 0.95, 1.2), 56)
    return merge(ms), cam, ENV_LAB, {}


def hospital_ward(n=8):
    ms = [box(14, 0.05, 8, (255, 255, 255), 'tile_lab', ts=1.0), box(14, 3.5, 0.1, (220, 225, 215)).xf(trans(0, 0, -3.5)),
          box(0.1, 3.5, 8, (215, 220, 210)).xf(trans(-7, 0, 0))]
    for i in range(n):
        x = -6 + i * 1.6
        ms.append(merge([box(0.9, 0.5, 1.9, (240, 240, 238)).xf(trans(0, 0.15, 0)), box(0.9, 0.9, 0.06, (150, 150, 155)).xf(trans(0, 0, -0.95)),
                         box(0.7, 0.12, 0.35, (250, 250, 248)).xf(trans(0, 0.65, -0.7)), box(0.92, 0.3, 1.35, (150, 180, 200)).xf(trans(0, 0.63, 0.6))]).xf(trans(x, 0, -2.3)))
        ms.append(box(1.0, 1.2, 0.05, (255, 255, 255), 'window').xf(trans(x, 1.6, -3.42)))
    return merge(ms)


WARD = hospital_ward()


def shot_lives(lt, dur, tg):
    """des millions de vies : une salle d'hôpital, les patients se relèvent"""
    ms = [WARD]
    for i in range(8):
        x = -6 + i * 1.6
        up = min(1.0, max(0.0, (lt - i * 0.12) / 0.4))
        # bassin posé sur le matelas (dessus à 0,65 m), jambes tendues ; il passe d'allongé à assis
        ms.append(ALEX.mesh((x, 0.27, -2.2), 0.0, dict(ll=(1.57, 0), rl=(1.57, 0), drop=0.45, lean=-1.42 * (1 - up), la=(0.3, 0.2, 0.3), ra=(0.3, 0.2, 0.3))))
    cam = cam_lerp(Cam((4.5, 2.3, 3.5), (-1.0, 0.8, -2.3), 55), Cam((4.0, 2.2, 3.0), (-1.0, 0.8, -2.3), 52), lt / dur)
    return merge(ms), cam, ENV_HOSP, {}


# ------------------------------------------------------------------ la boîte de Petri (gros plan)
def dish_close(mold=1.0, clear=1.0, seed=2, scale_=10.0):
    """boîte de Petri agrandie x10 : colonies jaunes, moisissure, zone claire autour"""
    rr = np.random.default_rng(seed)
    R = 0.05 * scale_
    ms = [cyl(R, R, 0.012 * scale_, 16, (215, 228, 232)), cyl(R * 0.95, R * 0.95, 0.006 * scale_, 16, (200, 180, 130)).xf(trans(0, 0.004 * scale_, 0)),
          cyl(R * 1.01, R * 1.01, 0.02 * scale_, 16, (225, 235, 240), caps=False, alpha=0.5)]
    mc = np.array([R * 0.35, 0, -R * 0.25])
    top = 0.0112 * scale_
    for i in range(70):
        a, r = rr.uniform(0, 6.28), R * 0.9 * math.sqrt(rr.random())
        p = np.array([math.cos(a) * r, top, math.sin(a) * r])
        d = np.linalg.norm((p - mc)[[0, 2]])
        s = 1.0
        if d < R * 0.55:
            s = max(0.0, 1.0 - clear * (1.0 - d / (R * 0.55)) * 1.6)
        if s > 0.05:
            ms.append(cyl(0.0045 * scale_ * s * rr.uniform(0.7, 1.2), 0.004 * scale_ * s, 0.004 * scale_, 6, (255, 220, 50)).xf(trans(p)))
    if mold > 0:
        ms.append(sphere(R * 0.2 * mold, 8, 4, (255, 255, 255), 'mold', sy=0.4).xf(trans(mc + np.array([0, top, 0]))))
        for k in range(5):
            a = k * 1.3
            ms.append(sphere(R * 0.08 * mold, 6, 3, (255, 255, 255), 'mold', sy=0.5).xf(trans(mc + np.array([math.cos(a) * R * 0.15 * mold, top, math.sin(a) * R * 0.15 * mold]))))
    return merge(ms)


TABLE_TOP = merge([box(4, 0.05, 4, (255, 255, 255), 'wood_dark', ts=1.0)])


def shot_title(lt, dur, tg):
    cam = cam_lerp(Cam((0.0, 2.8, 0.9), (0, 0, 0), 40), Cam((0.0, 2.4, 0.8), (0, 0, 0), 40), lt / dur)
    return merge([TABLE_TOP.xf(trans(0, -0.05, 0)), dish_close(1.0, 1.0)]), cam, ENV_LAB, {}


def shot_dish(lt, dur, tg):
    """la moisissure a poussé… et autour d'elle, plus de bactéries"""
    t_b = WT(8, 'bactéries') - cut['dish']
    mold = min(1.0, 0.3 + lt / 1.5)
    clear = min(1.0, max(0.0, (lt - t_b + 0.3) / 1.0))
    cam = cam_lerp(Cam((0.4, 2.6, 1.0), (0, 0, 0), 40), Cam((0.3, 1.8, 0.7), (0.1, 0, -0.08), 40), lt / dur)
    return merge([TABLE_TOP.xf(trans(0, -0.05, 0)), dish_close(mold, clear)]), cam, ENV_LAB, {}


# ------------------------------------------------------------------ Londres 1928
def bus(col=(190, 35, 35)):
    ms = [box(2.3, 1.9, 8, col).xf(trans(0, 0.5, 0)), box(2.3, 1.8, 8, col).xf(trans(0, 2.45, 0)), box(2.35, 0.1, 8.05, (230, 225, 210)).xf(trans(0, 2.4, 0))]
    for y in (1.3, 3.2):
        ms.append(box(2.36, 0.6, 7.0, (60, 70, 80)).xf(trans(0, y, -0.3)))
    for z in (-2.8, 2.8):
        for s in (-1, 1):
            ms.append(cyl(0.5, 0.5, 0.3, 10, (25, 25, 28)).xf(M(trans(s * 1.05, 0.5, z), rotz(math.pi / 2), trans(0, -0.15, 0))))
    return merge(ms)


def london():
    ms = [ground(-120, -120, 120, 120, 'cobble' if 'cobble' in TEXB else 'gravel', ts=3.0), box(240, 0.05, 10, (255, 255, 255), 'asphalt', ts=6).xf(trans(0, 0.02, 0)),
          box(240, 0.15, 3, (190, 185, 175), 'concrete').xf(trans(0, 0, -6.5))]
    for i, x in enumerate(np.arange(-60, 61, 10)):
        h = 12 + (i % 3) * 2
        ms.append(box(9.8, h, 8, (255, 255, 255), 'brick_lon', ts=2.5).xf(trans(x, 0, -12)))
        for y in np.arange(2.0, h - 1, 3.0):
            for dx in (-3, 0, 3):
                ms.append(box(1.4, 1.8, 0.06, (255, 255, 255), 'window').xf(trans(x + dx, y, -7.97)))
        ms.append(box(9.8, 0.4, 0.4, (200, 195, 180)).xf(trans(x, h, -8.0)))
    ms.append(box(4, 0.8, 0.1, (40, 50, 80)).xf(trans(0, 3.0, -7.9)))
    ms.append(box(1.6, 2.4, 0.06, (255, 255, 255), 'door').xf(trans(0, 0, -7.96)))
    for x in (-15, 15):
        ms.append(cyl(0.1, 0.08, 4, 6, (30, 30, 30)).xf(trans(x, 0, -5.4)))
        ms.append(box(0.35, 0.5, 0.35, (255, 230, 170), emis=0.6).xf(trans(x, 4, -5.4)))
    # tour de l'horloge au loin
    ms.append(box(10, 80, 10, (200, 185, 140), 'stone_block', ts=4).xf(trans(80, 0, -250)))
    ms.append(Mesh([[(75, 80, -245), (85, 80, -245), (80, 100, -250)], [(85, 80, -255), (75, 80, -255), (80, 100, -250)],
                    [(75, 80, -255), (75, 80, -245), (80, 100, -250)], [(85, 80, -245), (85, 80, -255), (80, 100, -250)]], C((70, 80, 70))))
    return merge(ms)


LONDON = london()


def _sign_smh(d, n):
    from PIL import ImageFont
    d.rectangle([0, 0, n, n], fill=(40, 50, 80))
    f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 7)
    d.text((n / 2, n / 2), "ST MARY'S", font=f, fill=(235, 225, 190), anchor='mm')


tex_draw('sign_smh', _sign_smh, bg=(40, 50, 80))


def shot_london(lt, dur, tg):
    x = -40 + lt * 12
    ms = [LONDON, box(4, 0.8, 0.1, (255, 255, 255), 'sign_smh').xf(trans(0, 3.0, -7.85)), bus().xf(M(trans(x, 0, 2.0), roty(math.pi / 2)))]
    for i in range(3):
        px = -6 + i * 4 + lt * (1.2 if i % 2 else -1.2)
        ms.append(LONDONERS[i].mesh((px, 0.15, -6.2), math.pi / 2 if i % 2 else -math.pi / 2, walk_pose(tg * 5 + i, 0.8)))
    cam = cam_lerp(Cam((6, 2.0, 12), (0, 4, -8), 55), Cam((5, 1.8, 10), (0, 4, -8), 52), lt / dur)
    return merge(ms), cam, ENV_DAY, {}


def fleming_bench(tg, lean=0.4, look=0.0):
    return FLEMING.mesh((-1.4, 0, -1.55), math.pi, dict(lean=lean, hp=0.5, hy=look, ra=(1.1, 0.2, 0.9), la=(1.1, 0.2, 0.9)))


def shot_study(lt, dur, tg):
    """il étudie des bactéries au microscope"""
    ms = [LAB, fleming_bench(tg)]
    cam = cam_lerp(Cam((0.1, 1.5, -0.6), (-1.4, 1.2, -2.2), 50), Cam((-0.1, 1.45, -0.9), (-1.4, 1.2, -2.2), 47), lt / dur)
    return merge(ms), cam, ENV_LAB, {}


def shot_stacks(lt, dur, tg):
    """insert : les petites boîtes en verre, empilées"""
    cam = cam_lerp(Cam((-0.2, 1.25, -1.5), (-0.4, 0.92, -2.2), 48), Cam((-0.3, 1.2, -1.7), (-0.4, 0.92, -2.2), 45), lt / dur)
    return merge([LAB]), cam, ENV_LAB, {}


def shot_mess(lt, dur, tg):
    """le labo en désordre, vue large (l'émeu figurine est sur l'étagère de droite)"""
    u = lt / max(dur, 0.1)
    cam = Cam((-2.2 + 0.4 * u, 2.0, 2.5), (1.9, 1.1, -1.3), 55)
    ms = [LAB, fleming_bench(tg)]
    return merge(ms), cam, ENV_LAB, {}


def shot_leave(lt, dur, tg):
    """chapeau, valise : il part en vacances en laissant tout sur la paillasse"""
    fp = np.array([-1.4, 0, -1.4]) + np.array([-0.9, 0, 2.6]) * min(1.0, lt / max(dur, 0.1))
    yaw = math.atan2(-0.9, 2.6)
    ms = [LAB, FLEMING_OUT.mesh(tuple(fp), yaw, walk_pose(tg * 6, 0.8, ra=(0.1, 0.1, 0.1), hand_r=suitcase().xf(trans(0, -0.2, 0))))]
    cam = Cam((1.6, 1.7, 2.4), tuple(fp + np.array([0, 1.0, 0])), 55)
    return merge(ms), cam, ENV_LAB, {}


# ------------------------------------------------------------------ marché de Peoria (1943)
def market():
    ms = [ground(-100, -100, 100, 100, 'gravel', ts=3.0), box(200, 0.05, 10, (255, 255, 255), 'asphalt', ts=6).xf(trans(0, 0.02, 4)),
          box(200, 0.15, 4, (195, 192, 185), 'concrete', ts=2).xf(trans(0, 0, -1))]
    for i, x in enumerate(np.arange(-40, 41, 10)):
        h = 7 + (i % 2) * 3
        ms.append(box(9.8, h, 8, (255, 255, 255), ['brick_red', 'stucco', 'brick'][i % 3], ts=2.5).xf(trans(x, 0, -7)))
        ms.append(box(2.8, 1.8, 0.06, (255, 255, 255), 'window').xf(trans(x + 2.5, 1.0, -2.97)))
        ms.append(box(9.8, 0.1, 1.6, (255, 255, 255), 'awning').xf(M(trans(x, 3.0, -2.3), rotx(0.3))))
    # étal de fruits
    ms.append(bench_table(3.0, 1.0, 0.85, (255, 255, 255), 'planks').xf(trans(0, 0.15, -1.6)))
    rr = np.random.default_rng(4)
    for k in range(5):
        crate_ = box(0.55, 0.22, 0.4, (255, 255, 255), 'planks').xf(trans(-1.2 + k * 0.6, 1.0, -1.6))
        ms.append(crate_)
        fc = [(230, 140, 40), (200, 40, 40), (240, 210, 60), (90, 160, 60), (230, 140, 40)][k]
        for j in range(6):
            ms.append(sphere(0.06, 6, 3, fc).xf(trans(-1.2 + k * 0.6 + rr.uniform(-0.18, 0.18), 1.24, -1.6 + rr.uniform(-0.12, 0.12))))
    for k in range(3):
        ms.append(melon(0.12, 0.0, k).xf(trans(1.05 + rr.uniform(-0.1, 0.1), 1.0, -1.7 + k * 0.25)))
    ms.append(box(1.0, 0.5, 0.05, (230, 225, 200)).xf(trans(0, 2.2, -2.9)))
    for x in (-8, 8):
        ms.append(merge([box(1.8, 0.7, 4.6, (40, 45, 60)).xf(trans(0, 0.4, 0)), box(1.6, 0.6, 2.4, (40, 45, 60)).xf(trans(0, 1.1, -0.3))]).xf(M(trans(x, 0, 5), roty(math.pi / 2))))
    return merge(ms)


MARKET = market()
MOLDY = melon(0.13, 1.0, 7)
MOLDY_POS = np.array([0.95, 1.0, -1.35])


def shot_melon_tease(lt, dur, tg):
    """retiens bien : un melon pourri (lent travelling avant)"""
    ms = [MARKET, MOLDY.xf(trans(MOLDY_POS))]
    tgt = MOLDY_POS + np.array([0, 0.12, 0])
    cam = cam_lerp(Cam(tuple(tgt + np.array([0.7, 0.5, 1.3])), tuple(tgt), 45), Cam(tuple(tgt + np.array([0.35, 0.25, 0.65])), tuple(tgt), 40), lt / dur)
    return merge(ms), cam, ENV_PEORIA, dict(post_pil=lambda im: C2.vignette(im, 0.75))


def shot_return(lt, dur, tg):
    """début septembre, Fleming rentre : la porte, la valise"""
    fp = DOOR + np.array([0.3 + lt * 0.8, 0, -0.3 - lt * 0.6])
    ms = [LAB, FLEMING_OUT.mesh(tuple(fp), math.atan2(1.2, -1.0), walk_pose(tg * 6, 0.8, ra=(0.1, 0.1, 0.1), hand_r=suitcase().xf(trans(0, -0.2, 0))))]
    cam = Cam((1.0, 1.6, -1.0), tuple(DOOR + np.array([0.6, 1.2, 0])), 55)
    return merge(ms), cam, ENV_LAB, {}


def shot_look(lt, dur, tg):
    """Fleming penché sur la boîte"""
    ms = [LAB, FLEMING.mesh((-0.5, 0, -1.45), math.pi, dict(lean=0.55, hp=0.6, la=(1.0, 0.3, 1.0), ra=(1.0, 0.3, 1.0))),
          petri(0.05).xf(trans(-0.5, 0.905, -2.05)), dish_close(1.0, 1.0, scale_=1.0).xf(trans(-0.5, 0.905, -2.05))]
    cam = cam_lerp(Cam((-2.5, 1.8, 0.3), (-0.5, 1.05, -1.9), 48), Cam((-2.3, 1.75, 0.0), (-0.5, 1.0, -1.9), 45), lt / dur)
    return merge(ms), cam, ENV_LAB, {}


def flask(fill=0.5, col=(240, 220, 120)):
    return merge([cyl(0.1, 0.03, 0.18, 8, (210, 230, 235), alpha=0.4), cyl(0.03, 0.03, 0.08, 6, (210, 230, 235), alpha=0.4).xf(trans(0, 0.18, 0)),
                  cyl(0.09, 0.09 - 0.06 * fill, 0.15 * fill, 8, col).xf(trans(0, 0.005, 0))])


def shot_produce(lt, dur, tg):
    """problème : presque rien au fond du flacon"""
    ms = [LAB, FLEMING.mesh((-0.5, 0, -1.45), math.pi, dict(hy=0.45 * math.sin(tg * 7) * min(1.0, lt), la=(1.2, 0.1, 0.8), ra=(1.2, 0.1, 0.8), hp=0.3))]
    for k in range(4):
        ms.append(flask(0.6).xf(trans(-0.9 + k * 0.25, 0.9, -2.0)))
    ms.append(cyl(0.015, 0.015, 0.06, 6, (210, 230, 235), alpha=0.5).xf(trans(0.2, 0.9, -1.9)))
    ms.append(cyl(0.012, 0.012, 0.006, 6, (240, 220, 120)).xf(trans(0.2, 0.905, -1.9)))
    cam = Cam((0.5, 1.5, -0.6), (-0.4, 1.15, -1.8), 50)
    return merge(ms), cam, ENV_LAB, {}


def shot_forgot(lt, dur, tg):
    """dix ans d'oubli : le flacon prend la poussière sur l'étagère"""
    ms = [LAB, cyl(0.04, 0.04, 0.12, 6, (210, 230, 235), alpha=0.5).xf(trans(2.95, 1.65, -0.9)), box(0.1, 0.03, 0.002, (230, 225, 200)).xf(trans(2.95, 1.7, -0.86))]
    cam = cam_lerp(Cam((1.8, 1.8, -0.4), (2.95, 1.7, -0.9), 45), Cam((2.2, 1.75, -0.6), (2.95, 1.7, -0.9), 40), lt / dur)
    ms.append(C2.particles((2.5, 1.7, -0.8), tg, cam, 30, (0.8, 0.8, 0.8), 0.1, 0.012, (230, 225, 210), 3, alpha=0.6))
    return merge(ms), cam, ENV_LAB.copy(amb=0.45), dict(post_pil=C2.chain(C2.tint((210, 190, 150), 0.5, sepia=True), lambda im: C2.vignette(im, 0.7)))


def shot_cta(lt, dur, tg):
    u = lt / max(dur, 0.1)
    cam = Cam((-2.0 + u, 2.3, 2.8), (0.5, 1.0, -1.5), 55)
    return LAB, cam, ENV_LAB, {}


# ------------------------------------------------------------------ Oxford 1941
def _sign_rad(d, n):
    from PIL import ImageFont
    d.rectangle([0, 0, n, n], fill=(225, 215, 190))
    f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 5)
    d.text((n / 2, n / 2 - 4), 'RADCLIFFE', font=f, fill=(60, 50, 40), anchor='mm')
    d.text((n / 2, n / 2 + 4), 'INFIRMARY', font=f, fill=(60, 50, 40), anchor='mm')


tex_draw('sign_rad', _sign_rad, bg=(225, 215, 190))
STONE = (228, 214, 180)


def georgian_window(w=1.3, h=2.0):
    """fenêtre à petits carreaux avec encadrement de pierre et appui"""
    return merge([box(w + 0.3, h + 0.3, 0.08, (238, 228, 200)).xf(trans(0, -0.15, 0)),
                  box(w, h, 0.1, (255, 255, 255), 'window').xf(trans(0, 0, 0.02)),
                  box(w + 0.4, 0.12, 0.25, (238, 228, 200)).xf(trans(0, -0.2, 0.1))])


def infirmary():
    """Radcliffe Infirmary (Oxford) : façade géorgienne en pierre, corps central à fronton, perron, porte à double battant"""
    ms = [ground(-100, -100, 100, 100, 'grass', ts=3.0), box(14, 0.06, 30, (255, 255, 255), 'gravel', ts=3).xf(trans(0, 0.02, 12))]
    # ailes (2 étages + attique), corniche, toit
    ms.append(box(44, 11, 12, (255, 255, 255), 'stone_block', ts=2.5).xf(trans(0, 0, -10)))
    ms.append(box(44.6, 0.5, 12.6, STONE).xf(trans(0, 11, -10)))
    ms.append(box(44, 1.6, 10, (90, 95, 100), 'roof_tin').xf(trans(0, 11.5, -10)))
    ms.append(box(44.2, 0.35, 12.2, STONE).xf(trans(0, 3.6, -10)))          # bandeau entre étages
    for x in np.arange(-20, 21, 3.2):
        if abs(x) < 7.5:
            continue
        for y in (1.4, 5.2, 8.6):
            ms.append(georgian_window(1.3, 2.0 if y < 8 else 1.5).xf(trans(x, y, -3.96)))
    # corps central en avancée
    ms.append(box(15, 13, 3, (255, 255, 255), 'stone_block', ts=2.5).xf(trans(0, 0, -4.0)))
    ms.append(box(15.6, 0.5, 3.6, STONE).xf(trans(0, 13, -4.0)))
    ms.append(Mesh([[(-7.8, 13.5, -2.2), (7.8, 13.5, -2.2), (0, 16.5, -2.2)]], C(STONE)))          # fronton
    ms.append(Mesh([[(-6.6, 13.9, -2.15), (6.6, 13.9, -2.15), (0, 15.9, -2.15)]], C((210, 198, 168))))
    ms.append(cyl(0.6, 0.6, 0.15, 12, (40, 40, 40)).xf(M(trans(0, 14.6, -2.1), rotx(math.pi / 2))))   # horloge du fronton
    ms.append(cyl(0.52, 0.52, 0.16, 12, (240, 235, 220)).xf(M(trans(0, 14.6, -2.08), rotx(math.pi / 2))))
    for x in (-5.0, -2.5, 2.5, 5.0):
        for y in (5.2, 8.6):
            ms.append(georgian_window(1.3, 2.0).xf(trans(x, y, -2.46)))
    ms.append(box(5.5, 0.9, 0.12, (255, 255, 255), 'sign_rad').xf(trans(0, 4.2, -1.0)))
    # portique : perron, colonnes, entablement
    for k in range(4):
        ms.append(box(9.0 - k * 0.5, 0.18, 3.6 - k * 0.35, (205, 200, 190), 'concrete').xf(trans(0, k * 0.18, -0.7 - k * 0.17)))
    for x in (-3.3, -1.3, 1.3, 3.3):
        ms.append(box(0.75, 0.3, 0.75, STONE).xf(trans(x, 0.72, -0.4)))
        ms.append(cyl(0.3, 0.26, 3.2, 10, (238, 230, 205)).xf(trans(x, 1.02, -0.4)))
        ms.append(box(0.7, 0.25, 0.7, STONE).xf(trans(x, 4.2, -0.4)))
    ms.append(box(8.0, 0.8, 1.6, STONE).xf(trans(0, 4.45, -0.9)))
    # porte : encadrement, double battant en bois, imposte vitrée
    ms.append(box(2.6, 3.4, 0.1, (238, 228, 200)).xf(trans(0, 0.72, -2.45)))
    ms.append(box(2.0, 2.6, 0.12, (70, 40, 30)).xf(trans(0, 0.72, -2.38)))
    ms.append(box(0.04, 2.5, 0.14, (40, 25, 20)).xf(trans(0, 0.75, -2.37)))
    for x in (-0.5, 0.5):
        for y in (1.1, 2.2):
            ms.append(box(0.7, 0.7, 0.14, (85, 50, 38)).xf(trans(x, y, -2.36)))
        ms.append(box(0.06, 0.06, 0.18, (200, 170, 70)).xf(trans(x * 0.25, 1.9, -2.32)))
    ms.append(box(2.0, 0.55, 0.12, (255, 255, 255), 'window').xf(trans(0, 3.35, -2.38)))
    # lanternes, grilles, massifs, arbres, voiture d'époque
    for x in (-4.6, 4.6):
        ms.append(cyl(0.07, 0.07, 3.0, 6, (30, 30, 30)).xf(trans(x, 0, 1.5)))
        ms.append(box(0.4, 0.55, 0.4, (255, 225, 160), emis=0.6).xf(trans(x, 3.0, 1.5)))
        ms.append(box(0.5, 0.1, 0.5, (30, 30, 30)).xf(trans(x, 3.55, 1.5)))
    for x in np.arange(-22, -7, 0.4).tolist() + np.arange(7.2, 22, 0.4).tolist():
        ms.append(box(0.04, 1.1, 0.04, (25, 25, 25)).xf(trans(x, 0, 5)))
    ms.append(box(14.6, 0.06, 0.06, (25, 25, 25)).xf(trans(-14.6, 1.05, 5)))
    ms.append(box(14.6, 0.06, 0.06, (25, 25, 25)).xf(trans(14.6, 1.05, 5)))
    for x in (-12, -9, 9, 12):
        ms.append(sphere(0.8, 7, 4, (60, 110, 55), sy=0.7).xf(trans(x, 0.3, -2.6)))
    ms += [deciduous(9, 3.5, i).xf(trans(x, 0, 9)) for i, x in enumerate((-16, 16))]
    ms.append(merge([box(1.8, 0.8, 4.2, (30, 30, 35)).xf(trans(0, 0.45, 0)), box(1.6, 0.7, 2.0, (30, 30, 35)).xf(trans(0, 1.15, -0.3)),
                     box(1.5, 0.5, 0.05, (110, 140, 160)).xf(trans(0, 1.25, 0.72))]).xf(M(trans(-4.5, 0, 7.5), roty(1.4))))
    return merge(ms)


INFIRMARY = infirmary()


def shot_oxford(lt, dur, tg):
    cam = cam_lerp(Cam((7, 1.7, 21), (0, 6.5, -4), 55), Cam((4.5, 1.7, 14), (0, 4.5, -3), 52), lt / dur)
    return INFIRMARY, cam, ENV_DAY, {}


def helmet():
    """casque de policier anglais (custodian)"""
    return merge([cyl(0.13, 0.12, 0.2, 8, (25, 28, 40)), sphere(0.12, 8, 4, (25, 28, 40), sy=1.1).xf(trans(0, 0.2, 0)), cyl(0.16, 0.16, 0.02, 8, (25, 28, 40)),
                  box(0.06, 0.07, 0.02, (210, 200, 160)).xf(trans(0, 0.15, 0.13))])


def hospital_room():
    ms = [box(8, 0.05, 8, (255, 255, 255), 'tile_lab', ts=1.0), box(8, 3.4, 0.1, (220, 225, 215)).xf(trans(0, 0, -2.5)),
          box(0.1, 3.4, 8, (215, 220, 210)).xf(trans(-2.5, 0, 0)), box(1.2, 1.4, 0.06, (255, 255, 255), 'window').xf(trans(1.0, 1.4, -2.42))]
    ms.append(merge([box(1.0, 0.5, 2.0, (240, 240, 238)).xf(trans(0, 0.15, 0)), box(1.0, 1.0, 0.06, (150, 150, 155)).xf(trans(0, 0, -1.0)),
                     box(0.8, 0.12, 0.4, (250, 250, 248)).xf(trans(0, 0.65, -0.72))]).xf(trans(0, 0, -1.2)))
    ms.append(box(0.45, 0.45, 0.45, (110, 85, 60)).xf(trans(-1.2, 0, -0.6)))   # chaise
    ms.append(helmet().xf(trans(-1.2, 0.45, -0.6)))
    ms.append(box(0.5, 0.7, 0.4, (200, 200, 195)).xf(trans(0.9, 0, -2.0)))
    ms.append(cyl(0.015, 0.015, 1.7, 4, (180, 180, 180)).xf(trans(0.7, 0, -1.6)))
    ms.append(box(0.12, 0.2, 0.06, (230, 230, 220), alpha=0.6).xf(trans(0.7, 1.55, -1.6)))
    return merge(ms)


ROOM = hospital_room()


def patient(up=0.0, face=None, blanket=True):
    who = ALEX_C if face == 'closed' else ALEX
    # bassin posé sur le matelas (dessus à 0,65 m) : allongé (up=0) -> assis (up=1), sans flotter au-dessus du lit
    m = who.mesh((0, 0.27, -1.35), 0.0, dict(ll=(1.57, 0), rl=(1.57, 0), drop=0.45, lean=-1.42 * (1 - up), la=(0.2, 0.2, 0.3), ra=(0.2, 0.2, 0.3)))
    ms = [m]
    if blanket:
        ms.append(box(1.02, 0.3, 1.35, (150, 180, 200)).xf(trans(0, 0.65, -0.75)))   # couverture sur les jambes
    return merge(ms)


def shot_test(lt, dur, tg):
    """Florey et Chain au chevet d'Albert Alexander ; son casque de policier sur la chaise"""
    ms = [ROOM, patient(0.0), FLOREY.mesh((0.9, 0, -0.6), -math.pi / 2 - 0.3, dict(hp=0.3, ra=(1.1, 0.2, 0.8))), CHAIN.mesh((1.0, 0, 0.5), -math.pi / 2 - 0.9, dict(hp=0.2))]
    cam = cam_lerp(Cam((-1.6, 1.7, 2.2), (0.2, 0.9, -1.0), 52), Cam((-1.3, 1.65, 1.8), (0.2, 0.9, -1.0), 50), lt / dur)
    return merge(ms), cam, ENV_HOSP, {}


def shot_dying(lt, dur, tg):
    ms = [ROOM, patient(0.0)]
    cam = cam_lerp(Cam((0.9, 1.5, -0.6), (0, 0.95, -1.8), 45), Cam((0.7, 1.4, -0.9), (0, 0.95, -1.8), 42), lt / dur)
    return merge(ms), cam, ENV_HOSP.copy(amb=0.45), dict(post_pil=C2.chain(C2.tint((255, 110, 100), 0.3), lambda im: C2.vignette(im, 0.7, (60, 0, 0))))


def shot_better(lt, dur, tg):
    up = min(1.0, lt / 0.8)
    ms = [ROOM, patient(up), FLOREY.mesh((1.1, 0, -1.0), -math.pi / 2 - 0.3, dict(hp=0.2))]
    cam = cam_lerp(Cam((1.2, 1.5, 1.6), (0, 1.1, -1.4), 50), Cam((1.0, 1.5, 1.3), (0, 1.15, -1.4), 48), lt / dur)
    return merge(ms), cam, ENV_HOSP.copy(points=[((1.0, 2.0, -2.0), (255, 220, 160), 1.0, 5)]), dict(post_pil=C2.tint((255, 220, 160), 0.2))


def shot_empty_vials(lt, dur, tg):
    ms = [ROOM, patient(0.0)]
    for k in range(4):
        ms.append(cyl(0.03, 0.03, 0.1, 6, (210, 230, 235), alpha=0.5).xf(trans(0.75 + k * 0.08, 0.7, -2.0)))
    cam = cam_lerp(Cam((1.3, 1.1, -1.4), (0.85, 0.75, -2.0), 45), Cam((1.15, 1.0, -1.55), (0.85, 0.75, -2.0), 42), lt / dur)
    return merge(ms), cam, ENV_HOSP.copy(amb=0.42), dict(post_pil=C2.tint((150, 160, 200), 0.3))


def shot_empty_bed(lt, dur, tg):
    ms = [ROOM, box(1.02, 0.08, 1.9, (240, 240, 238)).xf(trans(0, 0.65, -1.2))]
    cam = cam_lerp(Cam((-1.8, 1.4, 1.6), (0, 0.8, -1.2), 50), Cam((-1.6, 1.4, 1.3), (0, 0.8, -1.2), 48), lt / dur)
    fade = max(0.0, (lt - dur + 0.6) / 0.6) * 0.6
    return merge(ms), cam, ENV_HOSP.copy(amb=0.4), dict(post_pil=C2.tint((150, 160, 200), 0.35), fade=fade)


# ------------------------------------------------------------------ recherche mondiale
tex_noise('ocean', (40, 80, 150), (60, 100, 170), seed=701, octaves=2)


CONTINENTS = {
    'na': [(-168, 66), (-140, 70), (-95, 72), (-80, 63), (-62, 58), (-55, 49), (-67, 45), (-76, 35), (-80, 31), (-80, 25), (-82, 30), (-90, 29), (-97, 27),
           (-97, 19), (-91, 15), (-84, 10), (-78, 8), (-86, 13), (-95, 16), (-106, 22), (-112, 30), (-118, 34), (-124, 40), (-125, 48), (-133, 56), (-150, 60), (-165, 60)],
    'gl': [(-52, 60), (-42, 60), (-20, 70), (-18, 80), (-40, 83), (-65, 80), (-58, 70)],
    'sa': [(-80, 9), (-72, 12), (-60, 10), (-50, 0), (-35, -6), (-40, -22), (-48, -28), (-58, -38), (-65, -42), (-68, -55), (-74, -50), (-72, -35), (-70, -18), (-76, -14), (-81, -5)],
    'eu': [(-9, 37), (-9, 43), (-1, 44), (-4, 48), (2, 51), (8, 54), (11, 58), (5, 62), (14, 67), (22, 70), (30, 70), (40, 67), (45, 60), (48, 46), (40, 41),
           (28, 41), (26, 38), (22, 37), (19, 42), (13, 45), (16, 40), (12, 38), (8, 44), (3, 43), (0, 38)],
    'uk': [(-5, 50), (1, 51), (-1, 54), (-3, 58.5), (-6, 57), (-5, 54)],
    'af': [(-17, 15), (-16, 22), (-13, 28), (-6, 35), (10, 37), (11, 33), (20, 31), (32, 31), (34, 28), (43, 12), (51, 12), (48, 5), (40, -5), (40, -15),
           (35, -24), (32, -29), (20, -35), (17, -29), (12, -18), (13, -6), (9, 1), (9, 4), (-3, 5), (-8, 5), (-13, 8), (-17, 12)],
    'as': [(40, 45), (45, 60), (60, 68), (70, 72), (80, 74), (100, 77), (115, 74), (140, 72), (160, 70), (180, 66), (180, 64), (165, 60), (160, 55), (142, 52),
           (140, 46), (132, 43), (129, 35), (122, 31), (121, 25), (113, 22), (108, 18), (109, 12), (104, 9), (100, 13), (98, 8), (101, 3), (98, 17), (94, 18),
           (90, 22), (86, 21), (80, 15), (78, 8), (73, 17), (72, 22), (67, 25), (58, 25), (56, 27), (52, 25), (55, 22), (59, 22), (55, 17), (45, 13), (43, 15),
           (35, 28), (35, 33), (36, 36)],
    'jp': [(130, 31), (136, 34), (141, 38), (142, 44), (140, 42), (136, 36), (131, 34)],
    'id': [(95, 5), (105, -6), (115, -8), (125, -9), (140, -4), (150, -10), (140, -8), (130, -3), (118, 0), (110, 2), (104, 1)],
    'au': [(114, -22), (122, -18), (130, -12), (136, -12), (142, -11), (146, -19), (153, -26), (151, -34), (146, -39), (140, -37), (135, -34), (130, -32), (118, -35), (115, -33)],
    'nz': [(172, -35), (178, -38), (174, -41), (168, -46), (171, -44)],
    'md': [(44, -16), (50, -15), (49, -25), (44, -24)],
}
DESERTS = [[(-15, 28), (32, 30), (35, 15), (-15, 15)], [(36, 30), (58, 24), (55, 15), (44, 14)], [(118, -20), (140, -20), (140, -30), (120, -30)],
           [(-117, 37), (-105, 37), (-105, 28), (-114, 28)], [(75, 45), (110, 45), (110, 38), (75, 38)]]


def _earth_map():
    from PIL import Image, ImageDraw
    W_, H_ = 720, 360
    im = Image.new('RGB', (W_, H_), (35, 75, 150))
    d = ImageDraw.Draw(im)
    P = lambda pts: [((lo + 180) / 360 * W_, (90 - la) / 180 * H_) for lo, la in pts]
    for k, pts in CONTINENTS.items():
        d.polygon(P(pts), fill=(70, 140, 60))
    for pts in DESERTS:
        d.polygon(P(pts), fill=(200, 175, 110))
    d.rectangle([0, 0, W_, 0.04 * H_], fill=(240, 245, 250))
    d.rectangle([0, 0.9 * H_, W_, H_], fill=(240, 245, 250))
    return np.asarray(im)


EARTH = _earth_map()


def earth_sphere(r, nu=64, nv=32):
    """globe terrestre : une couleur par facette, échantillonnée sur une carte des continents (est = sens trigo vu du nord)"""
    tris, cols = [], []
    H_, W_ = EARTH.shape[:2]

    def P(lo, la):
        lo, la = math.radians(lo), math.radians(la)
        return (r * math.cos(la) * math.cos(lo), r * math.sin(la), -r * math.cos(la) * math.sin(lo))
    for j in range(nv):
        la0, la1 = -90 + 180 * j / nv, -90 + 180 * (j + 1) / nv
        for i in range(nu):
            lo0, lo1 = -180 + 360 * i / nu, -180 + 360 * (i + 1) / nu
            px = int(((lo0 + lo1) / 2 + 180) / 360 * W_) % W_
            py = min(H_ - 1, int((90 - (la0 + la1) / 2) / 180 * H_))
            c = EARTH[py, px] / 255.0
            p0, p1, p2, p3 = P(lo0, la0), P(lo1, la0), P(lo1, la1), P(lo0, la1)
            tris += [[p0, p1, p2], [p0, p2, p3]]
            cols += [c, c]
    return Mesh(tris, np.array(cols))


EARTH_MESH = earth_sphere(0.3)


def globe(rot=0.0):
    """globe de bureau : la Terre sur un pied en bois, axe incliné, méridien en laiton"""
    tilt = M(rotz(0.41))
    ms = [EARTH_MESH.xf(M(tilt, roty(rot)))]
    # méridien (demi-cercle en laiton) + axe
    pts = [np.array([0.33 * math.sin(a), 0.33 * math.cos(a), 0]) for a in np.linspace(-math.pi * 0.95, 0.05, 12)]
    for p0, p1 in zip(pts[:-1], pts[1:]):
        ms.append(rod(p0, p1, 0.008, (180, 140, 60), n=3).xf(tilt))
    ms.append(rod((0, -0.36, 0), (0, 0.36, 0), 0.008, (180, 140, 60), n=3).xf(tilt))
    ms.append(rod((0, -0.5, 0), (0.0, -0.33, 0), 0.02, (90, 65, 40), n=4))
    ms.append(cyl(0.13, 0.16, 0.06, 10, (90, 65, 40)).xf(trans(0, -0.56, 0)))
    return merge(ms)


def shot_globe(lt, dur, tg):
    ms = [LAB, globe(tg * 0.6 + 1.2).xf(trans(2.15, 1.46, 0.45))]
    cam = cam_lerp(Cam((2.9, 1.8, 2.5), (2.1, 1.35, 0.45), 45), Cam((2.75, 1.75, 2.2), (2.1, 1.35, 0.45), 42), lt / dur)
    return merge(ms), cam, ENV_LAB, {}


def shot_peoria(lt, dur, tg):
    """Peoria, 1943 : la laborantine passe devant l'étal…"""
    x = -5 + lt * 1.3
    ms = [MARKET, MOLDY.xf(trans(MOLDY_POS)), MARY.mesh((x, 0.15, 0.0), math.pi / 2, walk_pose(tg * 5, 0.8)),
          VENDOR.mesh((0.0, 0.15, -2.5), 0.0, dict(la=(0.4, 0.1, 1.4), ra=(0.4, 0.1, 1.4)))]
    cam = cam_lerp(Cam((-2, 2.2, 7.0), (0, 1.3, -1.5), 52), Cam((-1, 2.0, 6.0), (0, 1.3, -1.5), 50), lt / dur)
    return merge(ms), cam, ENV_PEORIA, {}


MARY_POS = np.array([1.3, 0.15, -0.8])


def mary_melon(yaw, center=None, hp=0.15):
    """Mary tient le melon pourri à deux mains devant elle ; center = centre du melon (sinon contre la poitrine)"""
    fw = np.array([math.sin(yaw), 0, math.cos(yaw)])
    rt = np.array([math.cos(yaw), 0, -math.sin(yaw)])
    if center is None:
        center = MARY_POS + np.array([0, 1.2, 0]) + fw * 0.27
    hands = dict(ik_r=center - rt * 0.15 + np.array([0, -0.02, 0]), ik_l=center + rt * 0.15 + np.array([0, -0.02, 0]), hp=hp)
    return merge([MOLDY.xf(trans(center - np.array([0, 0.12, 0]))), MARY.mesh(tuple(MARY_POS), yaw, hands)])


def shot_pick(lt, dur, tg):
    """… elle prend le melon pourri sur l'étal, se retourne et le rapporte (tenu à deux mains)"""
    y0, y1 = math.pi - 0.3, 0.5
    lift = min(1.0, max(0.0, (lt - 0.25) / 0.5))
    turn = min(1.0, max(0.0, (lt - 0.8) / 0.7))
    turn = turn * turn * (3 - 2 * turn)
    yaw = y0 + (y1 - y0) * turn
    c_stall = MOLDY_POS + np.array([0, 0.12, 0])
    fw = np.array([math.sin(yaw), 0, math.cos(yaw)])
    c_chest = MARY_POS + np.array([0, 1.2, 0]) + fw * 0.27
    c = c_stall + (c_chest - c_stall) * lift
    ms = [MARKET, mary_melon(yaw, c, hp=0.35 * (1 - turn))]
    cam = cam_lerp(Cam((2.8, 1.7, 1.6), (1.0, 1.15, -1.2), 48), Cam((2.5, 1.65, 1.3), (1.0, 1.15, -1.2), 45), lt / dur)
    return merge(ms), cam, ENV_PEORIA, {}


def tanks():
    ms = [box(30, 0.05, 20, (255, 255, 255), 'concrete', ts=3), box(30, 8, 0.2, (190, 190, 185)).xf(trans(0, 0, -6))]
    for i in range(5):
        x = -8 + i * 4
        ms.append(cyl(1.3, 1.3, 4.5, 12, (190, 195, 200), 'metal').xf(trans(x, 0.6, -2.5)))
        ms.append(sphere(1.3, 12, 4, (190, 195, 200), 'metal', sy=0.4).xf(trans(x, 5.1, -2.5)))
        for s in (-1, 1):
            ms.append(cyl(0.08, 0.08, 0.6, 5, (90, 90, 95)).xf(trans(x + s * 0.9, 0, -2.5 + s * 0.6)))
        ms.append(rod((x, 5.6, -2.5), (x, 7.5, -2.5), 0.1, (120, 120, 125), n=5))
    ms.append(rod((-10, 7.5, -2.5), (10, 7.5, -2.5), 0.12, (120, 120, 125), n=5))
    return merge(ms)


TANKS = tanks()


def shot_tanks(lt, dur, tg):
    u = lt / max(dur, 0.1)
    cam = Cam((-9 + 4 * u, 1.6, 7), (0, 3.0, -2.5), 55)
    return TANKS, cam, ENV_LAB.copy(sky_top=(80, 85, 90), sky_hor=(80, 85, 90), fog=(70, 72, 76)), {}


def shot_factory(lt, dur, tg):
    """chaîne de production : des milliers de flacons"""
    ms = [box(30, 0.05, 20, (255, 255, 255), 'concrete', ts=3), box(30, 0.9, 1.0, (70, 75, 80)).xf(trans(0, 0, 0))]
    for k in range(40):
        x = -15 + ((k * 0.75 + lt * 1.2) % 30)
        ms.append(cyl(0.05, 0.05, 0.16, 6, (230, 225, 200)).xf(trans(x, 0.9, 0)))
        ms.append(cyl(0.052, 0.052, 0.03, 6, (200, 80, 60)).xf(trans(x, 1.06, 0)))
    ms.append(MOLDY.xf(M(trans(1.5, 0.9, -2.2), scale(2.5))))
    ms.append(box(0.8, 0.9, 0.8, (230, 228, 220)).xf(trans(1.5, 0, -2.2)))
    cam = cam_lerp(Cam((-3, 1.6, 2.6), (1.0, 1.0, -0.8), 50), Cam((-2.5, 1.5, 2.2), (1.2, 1.0, -0.8), 48), lt / dur)
    return merge(ms), cam, ENV_LAB.copy(sky_top=(80, 85, 90), sky_hor=(80, 85, 90), fog=(70, 72, 76)), {}


def shot_who(lt, dur, tg):
    """qui l'a trouvé ? silhouette dans l'ombre"""
    ms = [MARKET, mary_melon(0.4)]
    cam = cam_lerp(Cam((2.8, 1.4, 2.0), (1.2, 1.4, -0.8), 48), Cam((2.6, 1.4, 1.7), (1.2, 1.4, -0.8), 46), lt / dur)
    env = ENV_PEORIA.copy(amb=0.15, light_col=(60, 60, 70), sky_top=(40, 45, 60), sky_hor=(90, 95, 110), fog=(60, 62, 70))
    return merge(ms), cam, env, dict(post_pil=lambda im: C2.vignette(im, 0.85))


def shot_mary(lt, dur, tg):
    ms = [MARKET, mary_melon(0.45)]
    cam = cam_lerp(Cam((2.4, 1.55, 1.4), (1.2, 1.35, -0.8), 45), Cam((2.2, 1.55, 1.1), (1.2, 1.35, -0.8), 42), lt / dur)
    return merge(ms), cam, ENV_PEORIA, {}


def shot_question(lt, dur, tg):
    """le vrai héros : Fleming… ou le melon ?"""
    ms = [LAB, FLEMING.mesh((-0.2, 0, -1.4), math.pi + 0.5, dict(hp=0.4, hy=-0.3, la=(0.5, 0.2, 1.4), ra=(0.5, 0.2, 1.4))), MOLDY.xf(trans(0.4, 0.9, -2.1))]
    cam = cam_lerp(Cam((1.2, 1.5, -0.2), (0.0, 1.1, -1.9), 50), Cam((1.0, 1.45, -0.4), (0.0, 1.1, -1.9), 48), lt / dur)
    return merge(ms), cam, ENV_LAB, {}


def shot_loop(lt, dur, tg):
    return shot_hook(lt, dur, tg, p=lt - dur)


# ------------------------------------------------------------------ montage
cut.add('hook', 0.0, shot_hook)
cut.add('lives', WT(0, 'sauver') - 0.1, shot_lives)
cut.add('title', T(1), shot_title)
cut.add('london', T(2), shot_london)
cut.add('study', T(3), shot_study)
cut.add('stacks', WT(3, 'petites') - 0.1, shot_stacks)
cut.add('mess', T(4), shot_mess)
cut.add('leave', T(5), shot_leave)
cut.add('tease', T(6), shot_melon_tease)
cut.add('return', T(7), shot_return)
cut.add('dish', T(8), shot_dish)
cut.add('look', T(9), shot_look)
cut.add('produce', T(10), shot_produce)
cut.add('forgot', T(11), shot_forgot)
cut.add('cta', T(12), shot_cta)
cut.add('oxford', T(13), shot_oxford)
cut.add('test', T(14), shot_test)
cut.add('dying', T(15), shot_dying)
cut.add('better', T(16), shot_better)
cut.add('vials', T(17), shot_empty_vials)
cut.add('empty_bed', T(18), shot_empty_bed)
cut.add('globe', T(19), shot_globe)
cut.add('peoria', T(20), shot_peoria)
cut.add('pick', WT(20, 'rapporte') - 0.1, shot_pick)
cut.add('tanks', T(21), shot_tanks)
cut.add('factory', T(22), shot_factory)
cut.add('who', T(23), shot_who)
cut.add('mary', T(24), shot_mary)
cut.add('question', T(25), shot_question)
cut.add('loop', T(26), shot_loop)


def years_counter():
    t0, t1 = cut['forgot'], cut['cta']

    def ov(img, t):
        if t0 <= t < t1:
            u = (t - t0) / (t1 - t0)
            C2.badge(str(1929 + int(10 * u)), t0, t1 - t0 + 0.01, y=700)(img, t)
    return ov


tl.overlay = C2.overlays(
    C2.hook_title(['SA VAISSELLE SALE', 'A SAUVÉ DES MILLIONS'], 0.0, 2.6, y=250, accent=1),
    emu_pastille(3.3, 3.2, y=300),
    C2.badge('PÉNICILLINE', T(1) + 0.3, 1.3, y=700),
    C2.badge('LONDRES, 1928', T(2), 1.8, y=700),
    retiens(T(6) - 0.1, max(2.4, T(7) - T(6)), y=300),
    C2.badge('SEPTEMBRE 1928', T(7), 1.8, y=700),
    years_counter(),
    C2.cta(T(12) - 0.1, max(1.8, T(13) - T(12) + 0.05)),
    C2.badge('OXFORD, 1941', T(13), 1.8, y=700),
    C2.badge('JOUR 5', T(17) + 0.2, 1.6, y=700, col=(255, 140, 90)),
    C2.badge('PEORIA, 1943', T(20) + 0.3, 2.0, y=700),
    C2.badge('x 200', WT(21, '200') - 0.1, 1.8, y=700),
    C2.badge('QUI ?', T(23) + 0.3, 2.4, y=700, col=(255, 140, 90)),
    C2.badge('« MARY LA MOISIE »', WT(24, '«') if False else T(24) + 0.6, 1.9, y=700),
    end_card(T(25), T(26) - T(25)),
)

subs = Subs(timing)


def build_audio(path):
    mx = A.Mixer(END)
    S = cut
    mx.add(C2.impact(), 0.0, 0.45)
    mx.add(A.footsteps(3, 2.0, 'wood') if True else None, 0.0, 0.4, length=S['lives'])
    mx.add(A.clank(0.4), 0.15, 0.25)
    mx.add(C2.riser(1.0), S['lives'] - 0.8, 0.3)
    mx.add(A.crowd(4), S['lives'], 0.25, length=S['title'] - S['lives'])
    mx.add(C2.ding(), S['title'] + 0.3, 0.35)
    mx.add(A.crowd(4), S['london'], 0.3, length=S['study'] - S['london'])
    mx.add(A.engine_hum(2.2, 55), S['london'], 0.3)
    mx.add(A.bell(1.5, 440), S['london'] + 0.4, 0.15)
    mx.add(A.tick(), S['study'] + 0.3, 0.25)
    mx.add(A.glass(0.6), S['stacks'] + 0.1, 0.2)
    mx.add(A.footsteps(2, 2.0), S['leave'], 0.35, length=S['tease'] - S['leave'])
    mx.add(C2.riser(1.2), T(6) - 0.5, 0.3)
    mx.add(C2.ding(), T(6) + 0.1, 0.4)
    mx.add(A.crowd(4), S['tease'], 0.15, length=S['return'] - S['tease'])
    mx.add(A.footsteps(2, 2.0), S['return'], 0.35, length=S['dish'] - S['return'])
    mx.add(C2.riser(1.2), WT(8, 'bactéries') - 1.0, 0.3)
    mx.add(C2.sting() if hasattr(C2, 'sting') else A.sting(), WT(8, 'bactéries') + 0.1, 0.35)
    mx.add(C2.ding(), WT(9, 'pénicilline.'), 0.35)
    mx.add(A.glass(0.6), S['produce'] + 0.3, 0.2)
    for i in range(int((S['cta'] - S['forgot']) / 0.2)):
        mx.add(A.tick(), S['forgot'] + i * 0.2, 0.15)
    mx.add(C2.pop(), T(12) + 0.05, 0.5)
    mx.add(C2.ding(), T(12) + max(1.8, T(13) - T(12)) * 0.62, 0.4)
    mx.add(A.birds(4), S['oxford'], 0.3, length=S['test'] - S['oxford'])
    mx.add(C2.heartbeat(S['better'] - S['test'], 70), S['test'], 0.4)
    mx.add(C2.ding(), S['better'] + 0.3, 0.35)
    mx.add(C2.heartbeat(S['globe'] - S['vials'], 50), S['vials'], 0.45)
    mx.add(C2.impact(), S['empty_bed'] + 0.1, 0.3)
    mx.add(A.whoosh(0.8), S['globe'], 0.3)
    mx.add(A.crowd(5), S['peoria'], 0.3, length=S['tanks'] - S['peoria'])
    mx.add(A.engine_hum(4, 60), S['tanks'], 0.3, length=S['who'] - S['tanks'])
    mx.add(C2.impact(), WT(21, '200'), 0.35)
    mx.add(A.clank(0.4), S['factory'] + 0.2, 0.2)
    mx.add(A.clank(0.4), S['factory'] + 0.9, 0.2)
    mx.add(C2.record_scratch(), S['who'] + 0.1, 0.3)
    mx.add(C2.ding(), S['mary'] + 0.6, 0.35)
    mx.add(A.tick(), S['question'] + 0.2, 0.25)
    mx.add(A.footsteps(2, 2.0), S['loop'], 0.35, length=END - S['loop'])
    C2.cut_sounds(mx, list(cut.st.values()), 0.08)
    mx.save(path)


if __name__ == '__main__':
    run(tl, subs, HERE, 'Good2No_ep24_Penicilline', build_audio, sys.argv)
