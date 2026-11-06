"""Décors et personnages : Jack le babouin aiguilleur (Uitenhage, années 1880)."""
import sys, math
sys.path.insert(0, '/home/claude/g2n')
import numpy as np
from lib import *

build_base_textures()

tex_noise('karoo', (170, 140, 95), (200, 170, 120), seed=41, speck=0.12, speck_col=(140, 115, 75))
tex_noise('scrub', (110, 115, 60), (145, 140, 80), seed=42, speck=0.15, speck_col=(90, 90, 50))
tex_noise('navy', (58, 66, 105), (72, 80, 125), seed=43, octaves=1)
tex_noise('loco_black', (28, 28, 30), (42, 42, 45), seed=44, octaves=1)
tex_noise('maroon', (100, 35, 30), (120, 45, 38), seed=45, octaves=1)
tex_noise('cream', (225, 210, 175), (240, 228, 198), seed=46, octaves=2)
tex_noise('sacking', (170, 150, 110), (195, 175, 130), seed=47, octaves=1, speck=0.2)
tex_noise('dress', (70, 85, 110), (85, 100, 128), seed=48, octaves=1)
tex_noise('tweed', (95, 85, 70), (120, 108, 88), seed=49, octaves=1, speck=0.25, speck_col=(70, 62, 50))
tex_noise('blanket', (190, 185, 170), (215, 210, 195), seed=50, octaves=1)
tex_stripes('carriage_win', (110, 35, 30), (40, 45, 50), n=4)


def car_window():
    def f(d, n):
        d.rectangle([0, 0, n, n], fill=(110, 38, 32))
        d.rectangle([5, 6, n - 6, n - 9], fill=(60, 70, 80))
        d.rectangle([5, 6, n - 6, n - 9], outline=(200, 170, 90))
        d.rectangle([0, n - 4, n, n], fill=(90, 30, 25))
    tex_draw('car_window', f)


car_window()

# ---------------------------------------------------------------- visages
SKIN_J = (228, 186, 150)
make_face('james', skin=SKIN_J, brow_col=(90, 60, 35), mustache=True, hair_col=(90, 60, 35))
make_face('james_shout', skin=SKIN_J, brow_col=(90, 60, 35), mustache=True, hair_col=(90, 60, 35), mouth='shout')
make_face('james_smile', skin=SKIN_J, brow_col=(90, 60, 35), mustache=True, hair_col=(90, 60, 35), mouth='smile')
make_face('james_open', skin=SKIN_J, brow_col=(90, 60, 35), mustache=True, hair_col=(90, 60, 35), mouth='open')
make_face('james_closed', skin=SKIN_J, brow_col=(90, 60, 35), mustache=True, hair_col=(90, 60, 35), eyes_closed=True)
make_face('lady', skin=(238, 205, 180), brow_col=(80, 55, 40))
make_face('lady_shock', skin=(238, 205, 180), brow_col=(80, 55, 40), mouth='shout')
make_face('insp', skin=(232, 195, 165), brow_col=(130, 130, 130), mustache=True, hair_col=(150, 150, 150))
make_face('insp_smile', skin=(232, 195, 165), brow_col=(130, 130, 130), mustache=True, hair_col=(150, 150, 150), mouth='smile')
make_face('insp_open', skin=(232, 195, 165), brow_col=(130, 130, 130), mustache=True, hair_col=(150, 150, 150), mouth='open')
make_face('farmer', skin=(205, 150, 110), brow_col=(60, 45, 30), beard=True, hair_col=(80, 60, 40))
make_face('clerk', skin=(230, 192, 160), brow_col=(60, 45, 30))
make_face('vendor', skin=(120, 80, 55), brow_col=(30, 20, 15), eye_col=(30, 20, 15))
make_face('vendor2', skin=(150, 100, 70), brow_col=(30, 20, 15), eye_col=(30, 20, 15), mouth='smile')
make_face('doctor', skin=(232, 195, 165), brow_col=(80, 70, 60), beard=True, hair_col=(120, 110, 100))


def baboon_face():
    def f(d, n):
        d.rectangle([0, 0, n, n], fill=(120, 108, 85))
        # arcades sourcilières
        d.rectangle([4, 8, n - 5, 12], fill=(70, 62, 50))
        # yeux rapprochés ambrés
        d.rectangle([9, 13, 13, 16], fill=(190, 130, 50))
        d.rectangle([18, 13, 22, 16], fill=(190, 130, 50))
        d.rectangle([11, 14, 12, 15], fill=(20, 15, 10))
        d.rectangle([20, 14, 21, 15], fill=(20, 15, 10))
        d.rectangle([14, 13, 17, 31], fill=(60, 55, 52))
    tex_draw('baboon_face', f)

    def m(d, n):
        d.rectangle([0, 0, n, n], fill=(55, 50, 50))
        d.rectangle([10, 4, 21, 9], fill=(30, 28, 28))
        d.rectangle([12, 5, 13, 7], fill=(10, 10, 10))
        d.rectangle([18, 5, 19, 7], fill=(10, 10, 10))
        d.rectangle([6, n - 6, n - 7, n - 5], fill=(30, 25, 25))
    tex_draw('baboon_muzzle', m)


baboon_face()


def _bab_eyes(d, n):
    d.rectangle([0, 0, n, n], fill=(40, 36, 35))
    for x in (5, 19):
        d.rectangle([x, 10, x + 7, 20], fill=(200, 140, 50))
        d.rectangle([x + 2, 12, x + 4, 18], fill=(15, 10, 8))


tex_draw('baboon_eyes', _bab_eyes)


# ---------------------------------------------------------------- humains
def james(face='james', peg=False, cap=True):
    return Human(face, skin=SKIN_J, shirt=(40, 46, 74), pants=(36, 40, 64), shoes=(25, 20, 18), hair=(90, 60, 35),
                 hat='kepi' if cap else None, hat_col=(30, 34, 56), shirt_tex='navy', pants_tex='navy', belt=(20, 18, 16),
                 peg_legs=peg)


def lady(face='lady'):
    return Human(face, skin=(238, 205, 180), shirt=(70, 85, 110), pants=(70, 85, 110), robe=(70, 85, 110),
                 hair=(80, 55, 40), shirt_tex='dress', hat='bonnet', hat_col=(110, 60, 85), build=0.9)


def inspector(face='insp'):
    return Human(face, skin=(232, 195, 165), shirt=(230, 230, 225), pants=(55, 50, 45), hair=(150, 150, 150),
                 hat='bowler', hat_col=(30, 28, 26), jacket=(55, 50, 45), tie=(30, 30, 30), build=1.1)


def farmer(face='farmer'):
    return Human(face, skin=(205, 150, 110), shirt=(180, 165, 130), pants=(95, 80, 60), hair=(80, 60, 40),
                 hat='flatcap', hat_col=(100, 90, 70), sleeves='short', shirt_tex='sacking', pants_tex='tweed')


def vendor(face='vendor', shirt=(200, 80, 50)):
    return Human(face, skin=(120, 80, 55) if face == 'vendor' else (150, 100, 70), shirt=shirt, pants=(90, 75, 60),
                 hair=(25, 20, 15), sleeves='short', hat='flatcap' if face == 'vendor' else None, hat_col=(60, 55, 45))


def doctor():
    return Human('doctor', skin=(232, 195, 165), shirt=(235, 235, 230), pants=(40, 38, 36), hair=(120, 110, 100),
                 jacket=(40, 38, 36), tie=(120, 30, 30))


# ---------------------------------------------------------------- babouin
def _bab_hand(shoulder, unpitch, s, a):
    pa, ab, el = a
    sh = M(shoulder, trans(s * 0.17, 0.02, 0), unpitch, rotx(-pa), rotz(s * (0.05 + ab)))
    elb = M(sh, trans(0, -0.29, 0), rotx(-el))
    return M(elb, trans(0, -0.33, 0.02))[:3, 3]


class Baboon:
    """babouin chacma low-poly : museau de chien allongé, arcades marquées, crinière d'épaules, queue « cassée»"""
    F = 'fur_baboon'

    def mesh(self, pos=(0, 0, 0), yaw=0.0, pose=None):
        P = dict(pitch=0.0, hip=0.55, la=(0.0, 0.0), ra=(0.0, 0.0), ll=(0.0, 0.0), rl=(0.0, 0.0),
                 hp=0.0, hy=0.0, mouth=0.0, tail=0.0, hand_r=None, hand_l=None, cap=False, ik_l=None, ik_r=None)
        if pose:
            P.update(pose)
        F, Wc = self.F, (255, 255, 255)
        SKIN, SKIN_D = (62, 56, 54), (40, 36, 35)
        ms = []
        root = M(trans(pos), roty(yaw))
        pelvis = M(root, trans(0, P['hip'], 0))
        torso = M(pelvis, rotx(-P['pitch']))
        unpitch = rotx(P['pitch'])
        att = {}
        # bassin, taille, poitrine (le haut du corps plus massif que l'arrière)
        ms.append(box(0.3, 0.27, 0.26, Wc, F).xf(M(torso, trans(0, -0.12, -0.02))))
        ms.append(box(0.27, 0.25, 0.26, Wc, F).xf(M(torso, trans(0, -0.11, 0.2))))
        ms.append(box(0.34, 0.32, 0.3, Wc, F).xf(M(torso, trans(0, -0.13, 0.42))))
        # crinière (poils plus longs et plus sombres sur les épaules)
        ms.append(box(0.38, 0.12, 0.3, (215, 205, 185), F).xf(M(torso, trans(0, 0.13, 0.45))))
        ms.append(box(0.36, 0.2, 0.08, (215, 205, 185), F).xf(M(torso, trans(0, -0.05, 0.6))))
        # callosités fessières
        ms.append(box(0.18, 0.12, 0.03, (120, 85, 85)).xf(M(torso, trans(0, -0.1, -0.16))))
        shoulder = M(torso, trans(0, 0.0, 0.5))
        # ---- tête
        head = M(shoulder, trans(0, 0.16, 0.14), unpitch, roty(P['hy']), rotx(-P['hp']))
        att['head'] = head
        ms.append(box(0.2, 0.16, 0.2, Wc, F).xf(M(head, trans(0, -0.02, -0.03))))       # crâne
        ms.append(box(0.16, 0.05, 0.16, Wc, F).xf(M(head, trans(0, 0.14, -0.04))))       # dessus arrondi
        ms.append(box(0.24, 0.12, 0.1, Wc, F).xf(M(head, trans(0, -0.04, 0.0))))          # favoris sur les joues
        ms.append(box(0.19, 0.035, 0.07, SKIN_D).xf(M(head, trans(0, 0.085, 0.075))))     # arcade sourcilière
        ms.append(box(0.15, 0.07, 0.02, (255, 255, 255), 'baboon_eyes').xf(M(head, trans(0, 0.015, 0.1))))  # yeux
        for s_ in (-1, 1):
            ms.append(box(0.03, 0.05, 0.04, SKIN).xf(M(head, trans(s_ * 0.11, 0.06, -0.04))))  # oreilles
        # museau long en 3 tronçons, légèrement plongeant
        mz = M(head, trans(0, -0.01, 0.1), rotx(0.28))
        ms.append(frustum(0.13, 0.11, 0.085, 0.075, 0.25, SKIN, dy1=-0.01).xf(M(mz, trans(0, -0.01, -0.01))))
        ms.append(frustum(0.05, 0.03, 0.035, 0.02, 0.24, SKIN_D).xf(M(mz, trans(0, 0.045, -0.005))))  # arête du nez
        for s_ in (-1, 1):
            ms.append(box(0.022, 0.02, 0.01, (12, 10, 10)).xf(M(mz, trans(s_ * 0.022, -0.005, 0.243))))  # narines
        jaw = M(mz, trans(0, -0.055, 0.0), rotx(P['mouth'] * 0.55))
        ms.append(frustum(0.1, 0.04, 0.07, 0.03, 0.22, SKIN).xf(M(jaw, trans(0, -0.02, 0.0))))
        if P['mouth'] > 0.2:
            ms.append(box(0.08, 0.02, 0.16, (150, 50, 55)).xf(M(jaw, trans(0, 0.0, 0.1))))
            for s_ in (-1, 1):
                ms.append(box(0.014, 0.05, 0.014, (245, 240, 225)).xf(M(mz, trans(s_ * 0.035, -0.11, 0.17))))
        if P['cap']:
            ms.append(box(0.21, 0.03, 0.21, (30, 34, 56)).xf(M(head, trans(0, 0.12, -0.03))))
            ms.append(hat_mesh('kepi', (30, 34, 56)).xf(M(head, trans(0, 0.13, -0.03), scale(0.95, 0.75, 0.95))))
        # ---- bras longs (angles absolus / verticale), IK possible
        for s, key in ((-1, 'la'), (1, 'ra')):
            a = P[key]
            pa, ab, el = (a[0], 0.0, a[1]) if len(a) == 2 else a
            ik = P['ik_' + ('l' if s < 0 else 'r')]
            if ik is not None:
                pa, ab, el = solve_arm(lambda v, s=s: _bab_hand(shoulder, unpitch, s, v), ik, (pa, ab, el),
                                       ((-1.5, 3.3), (-0.3, 1.4), (0.0, 2.6)), key=(id(self), s))
            sh = M(shoulder, trans(s * 0.17, 0.02, 0), unpitch, rotx(-pa), rotz(s * (0.05 + ab)))
            ms.append(box(0.1, 0.3, 0.11, Wc, F).xf(M(sh, trans(0, -0.3, 0))))
            elb = M(sh, trans(0, -0.29, 0), rotx(-el))
            ms.append(box(0.085, 0.28, 0.095, Wc, F).xf(M(elb, trans(0, -0.28, 0))))
            hand = M(elb, trans(0, -0.28, 0))
            ms.append(box(0.08, 0.07, 0.07, SKIN_D).xf(M(hand, trans(0, -0.07, 0.01))))
            ms.append(box(0.07, 0.04, 0.05, SKIN_D).xf(M(hand, trans(0, -0.09, 0.05))))  # doigts repliés
            att['hand_' + ('l' if s < 0 else 'r')] = M(hand, trans(0, -0.05, 0.02))
        # ---- jambes
        for s, key in ((-1, 'll'), (1, 'rl')):
            pa, kn = P[key]
            hp_ = M(pelvis, trans(s * 0.13, 0, -0.06), rotx(-pa))
            ms.append(box(0.12, 0.28, 0.14, Wc, F).xf(M(hp_, trans(0, -0.28, 0))))
            kn_ = M(hp_, trans(0, -0.27, 0), rotx(kn))
            ms.append(box(0.09, 0.27, 0.1, Wc, F).xf(M(kn_, trans(0, -0.27, 0))))
            ms.append(box(0.09, 0.05, 0.18, SKIN_D).xf(M(kn_, trans(0, -0.29, 0.05), rotx(-kn + pa))))
        # queue « cassée » de chacma : monte puis retombe
        tb = M(pelvis, trans(0, 0.05, -0.18), unpitch)
        pts = [(0, 0, 0), (0, 0.15, -0.12), (0, 0.2, -0.26), (0, 0.02, -0.4), (0, -0.25, -0.46)]
        sw = P['tail']
        for i in range(len(pts) - 1):
            a_ = np.array(pts[i]) + np.array([sw * i * 0.05, 0, 0])
            b_ = np.array(pts[i + 1]) + np.array([sw * (i + 1) * 0.05, 0, 0])
            ms.append(rod(a_, b_, 0.028, Wc, F).xf(tb))
        for k in ('hand_l', 'hand_r'):
            if P[k] is not None:
                ms.append(P[k].xf(att[k]))
        self.attach = att
        return merge(ms)


def bab_quad(phase, amp=1.0, **kw):
    s, c = math.sin(phase), math.cos(phase)
    p = dict(pitch=0.12, hip=0.55, hp=0.0, la=(0.35 * s * amp, 0.05), ra=(-0.35 * s * amp, 0.05),
             ll=(-0.35 * s * amp + 0.15, 0.25 + 0.2 * max(0, c)), rl=(0.35 * s * amp + 0.15, 0.25 + 0.2 * max(0, -c)))
    p.update(kw)
    return p


def bab_sit(**kw):
    p = dict(pitch=1.25, hip=0.16, la=(0.3, 0.6), ra=(0.3, 0.6), ll=(1.4, 1.6), rl=(1.4, 1.6), hp=0.0)
    p.update(kw)
    return p


def bab_stand(**kw):
    p = dict(pitch=1.3, hip=0.5, la=(0.4, 0.4), ra=(0.4, 0.4), ll=(0.25, 0.45), rl=(0.25, 0.45), hp=0.0)
    p.update(kw)
    return p


JACK = Baboon()


# ---------------------------------------------------------------- bœuf, charrette
def ox(phase=0.0, col=(255, 255, 255)):
    F = 'fur_ox'
    ms = [box(0.7, 0.7, 1.6, col, F).xf(trans(0, 0.75, 0)), sphere(0.4, 7, 4, col, F).xf(M(trans(0, 1.35, 0.55), scale(0.9, 0.6, 0.8)))]
    head = M(trans(0, 1.15, 0.95), rotx(0.4))
    ms.append(box(0.32, 0.38, 0.5, col, F).xf(M(head, trans(0, -0.15, 0.1))))
    ms.append(box(0.24, 0.18, 0.12, (70, 50, 40)).xf(M(head, trans(0, -0.18, 0.38))))
    for s in (-1, 1):
        ms.append(box(0.5, 0.06, 0.06, (230, 220, 190)).xf(M(head, trans(s * 0.32, 0.15, 0.1), rotz(s * 0.4))))
        ms.append(box(0.06, 0.25, 0.06, (230, 220, 190)).xf(M(head, trans(s * 0.55, 0.25, 0.1), rotz(-s * 0.3))))
        ms.append(box(0.04, 0.04, 0.02, (15, 12, 10)).xf(M(head, trans(s * 0.12, 0.0, 0.36))))
    for (x, z, ph) in ((-0.25, 0.65, 0), (0.25, 0.65, math.pi), (-0.25, -0.65, math.pi), (0.25, -0.65, 0)):
        lg = M(trans(x, 0.8, z), rotx(0.35 * math.sin(phase + ph)))
        ms.append(box(0.16, 0.8, 0.18, col, F).xf(M(lg, trans(0, -0.8, 0))))
        ms.append(box(0.17, 0.08, 0.2, (30, 25, 20)).xf(M(lg, trans(0, -0.82, 0.01))))
    ms.append(cyl(0.04, 0.02, 0.6, 4, col).xf(M(trans(0, 1.1, -0.8), rotx(-2.8))))
    return merge(ms)


def wheel(r=0.7, w=0.1, spokes=8, col=(120, 85, 50)):
    ms = [cyl(r, r, w, 14, (90, 90, 95), 'metal', caps=False).xf(M(trans(0, -w / 2, 0))),
          cyl(r * 0.94, r * 0.94, w * 0.9, 14, col, caps=False).xf(trans(0, -w * 0.45, 0)),
          cyl(0.1, 0.1, w * 1.6, 8, col).xf(trans(0, -w * 0.8, 0))]
    for k in range(spokes):
        a = k / spokes * math.pi
        ms.append(box(0.05, 0.04, r * 1.9, col).xf(M(roty(a), trans(0, -0.02, 0))))
    return merge(ms)


def ox_cart(wheel_rot=0.0):
    """charrette, timon vers +z"""
    ms = [box(1.4, 0.12, 2.2, (150, 110, 70), 'planks', ts=0.6).xf(trans(0, 0.85, 0))]
    for s in (-1, 1):
        ms.append(box(0.08, 0.45, 2.2, (140, 100, 62), 'planks', ts=0.6).xf(trans(s * 0.68, 0.97, 0)))
        ms.append(wheel(0.75).xf(M(trans(s * 0.85, 0.75, -0.2), rotz(math.pi / 2), roty(wheel_rot))))
    ms.append(box(1.4, 0.45, 0.08, (140, 100, 62), 'planks', ts=0.6).xf(trans(0, 0.97, -1.08)))
    # siège du conducteur
    ms.append(box(1.2, 0.08, 0.4, (120, 85, 55)).xf(trans(0, 1.35, 0.85)))
    ms.append(box(1.2, 0.5, 0.08, (120, 85, 55)).xf(trans(0, 0.9, 0.85)))
    # timon + joug
    ms.append(box(0.12, 0.12, 2.6, (130, 95, 60)).xf(trans(0, 0.85, 2.3)))
    ms.append(box(1.6, 0.1, 0.12, (130, 95, 60)).xf(trans(0, 1.45, 3.15)))
    # sacs dans la charrette
    for i, (x, z) in enumerate(((-0.3, -0.4), (0.3, -0.2), (0.0, 0.3))):
        ms.append(sphere(0.3, 6, 4, (255, 255, 255), 'sacking', sy=0.7).xf(trans(x, 1.1, z)))
    return merge(ms)


# ---------------------------------------------------------------- rail
TRACK_G = 1.067  # écartement du Cap


def track(x0, x1, z=0.0, rot=0.0):
    """voie le long de x"""
    L = x1 - x0
    ms = [box(L, 0.12, 3.0, (150, 140, 125), 'gravel', ts=1.2).xf(trans((x0 + x1) / 2, -0.06, z)),
          box(L, 0.06, 1.9, (255, 255, 255), 'sleepers', ts=None).xf(trans((x0 + x1) / 2, 0.0, z))]
    # traverses en vrai (plus lisibles)
    ms = [box(L, 0.15, 3.0, (150, 140, 125), 'gravel', ts=1.2).xf(trans((x0 + x1) / 2, -0.12, z))]
    n = int(L / 0.7)
    tris, cols = [], []
    for i in range(n):
        x = x0 + (i + 0.5) * L / n
        ms.append(box(0.22, 0.08, 1.9, (100, 75, 50)).xf(trans(x, 0.0, z)))
    for s in (-1, 1):
        ms.append(box(L, 0.1, 0.06, (120, 115, 110), 'metal').xf(trans((x0 + x1) / 2, 0.08, z + s * TRACK_G / 2)))
        ms.append(box(L, 0.02, 0.05, (190, 190, 190)).xf(trans((x0 + x1) / 2, 0.18, z + s * TRACK_G / 2)))
    return merge(ms).xf(roty(rot))


def points_lever(pull=0.0):
    """levier d'aiguillage au sol (contrepoids)"""
    ms = [box(0.6, 0.15, 0.3, (60, 60, 65), 'metal')]
    arm = M(trans(0, 0.15, 0), rotz(-0.7 + 1.4 * pull))
    ms.append(box(0.06, 1.0, 0.06, (40, 40, 45)).xf(arm))
    ms.append(box(0.18, 0.18, 0.14, (180, 30, 30)).xf(M(arm, trans(0, 0.85, 0))))
    return merge(ms)


def semaphore(state=0.0, h=6.0):
    ms = [box(0.2, h, 0.2, (230, 230, 225), 'planks_white').xf(trans(0, 0, 0)), box(0.3, 0.2, 0.3, (40, 40, 40)).xf(trans(0, h, 0))]
    arm = M(trans(0.0, h - 0.5, 0.15), rotz(-0.7 * state))
    ms.append(box(1.4, 0.25, 0.04, (200, 30, 30)).xf(M(arm, trans(0.75, -0.12, 0))))
    ms.append(box(0.15, 0.25, 0.045, (240, 240, 240)).xf(M(arm, trans(1.25, -0.12, 0))))
    ms.append(cyl(0.12, 0.12, 0.05, 6, (60, 60, 60)).xf(M(trans(0, h - 0.5, 0.18), rotx(math.pi / 2))))
    return merge(ms)


def rail_wheel(r=0.42, spokes=8, col=(40, 40, 42), w=0.12, counterweight=False, tyre=(150, 150, 150)):
    """roue de chemin de fer à rayons, axe selon y (comme cyl) : bandage, boudin, rayons, moyeu"""
    ms = [cyl(r, r, w, 16, tyre, 'metal', caps=False).xf(trans(0, -w / 2, 0)),
          cyl(r * 1.08, r * 1.08, w * 0.25, 16, tyre, 'metal').xf(trans(0, w / 2 - w * 0.25, 0)),   # boudin côté intérieur
          cyl(r * 0.9, r * 0.9, w * 0.5, 16, col, caps=False).xf(trans(0, -w * 0.25, 0)),
          cyl(r * 0.2, r * 0.2, w * 1.3, 8, col).xf(trans(0, -w * 0.65, 0)),
          cyl(r * 0.09, r * 0.09, w * 1.5, 6, (200, 200, 200), 'metal').xf(trans(0, -w * 0.75, 0))]
    for k in range(spokes):
        a = k / spokes * math.pi
        ms.append(box(r * 0.09, w * 0.45, r * 1.8, col).xf(M(roty(a), trans(0, -w * 0.22, 0))))
    if counterweight:
        cw = []
        for k in range(5):
            a0, a1 = math.pi + (k - 2.5) * 0.25, math.pi + (k - 1.5) * 0.25
            cw.append([(0, 0, 0), (r * 0.88 * math.cos(a1), 0, r * 0.88 * math.sin(a1)), (r * 0.88 * math.cos(a0), 0, r * 0.88 * math.sin(a0))])
        cwm = Mesh(cw, C(col) * 0.8)
        ms.append(cwm.xf(trans(0, -w * 0.5, 0)))
        ms.append(cwm.xf(trans(0, w * 0.0, 0)))
    return merge(ms)


def _axle_wheels(x, r, wr, col, spokes=8, cw=False, half=0.82):
    ms = []
    for s in (-1, 1):
        ms.append(rail_wheel(r, spokes, col, counterweight=cw).xf(M(trans(x, r, s * half), rotx(-s * math.pi / 2), roty(-s * wr))))
    return merge(ms)


def axle_box(x, y, half=1.0):
    """boîte d'essieu + ressort à lames, de chaque côté"""
    ms = []
    for s in (-1, 1):
        ms.append(box(0.22, 0.25, 0.12, (45, 45, 48)).xf(trans(x, y - 0.12, s * half)))
        for k in range(4):
            ms.append(box(0.9 - k * 0.16, 0.04, 0.1, (60, 60, 62)).xf(trans(x, y + 0.13 + k * 0.045, s * half)))
        ms.append(box(0.06, 0.5, 0.06, (40, 40, 42)).xf(trans(x - 0.18, y - 0.3, s * half)))
        ms.append(box(0.06, 0.5, 0.06, (40, 40, 42)).xf(trans(x + 0.18, y - 0.3, s * half)))
    return merge(ms)


def buffers(x, y=0.9, dirx=1):
    ms = []
    for s in (-1, 1):
        ms.append(cyl(0.07, 0.07, 0.35, 6, (50, 50, 52)).xf(M(trans(x, y, s * 0.75), rotz(-dirx * math.pi / 2))))
        ms.append(cyl(0.17, 0.17, 0.04, 10, (70, 70, 72), 'metal').xf(M(trans(x + dirx * 0.33, y, s * 0.75), rotz(-dirx * math.pi / 2))))
    ms.append(box(0.25, 0.06, 0.06, (40, 40, 40)).xf(trans(x + dirx * 0.2, y - 0.05, 0)))  # crochet d'attelage
    return merge(ms)


def locomotive(wheel_rot=0.0, smoke=True):
    """4-4-0 du Cap, avance vers +x. origine au sol sous le centre."""
    B = 'loco_black'
    ms = []
    ms.append(box(7.6, 0.4, 1.9, (40, 40, 42), B).xf(trans(0, 0.85, 0)))  # châssis
    ms.append(box(0.3, 0.45, 2.1, (170, 35, 30)).xf(trans(3.9, 0.85, 0)))  # traverse rouge
    ms.append(buffers(4.05, 1.07, 1))
    # tablier et marchepieds
    for s in (-1, 1):
        ms.append(box(6.6, 0.05, 0.45, (35, 35, 37)).xf(trans(0.3, 1.25, s * 1.0)))
        ms.append(box(6.6, 0.12, 0.03, (190, 150, 60)).xf(trans(0.3, 1.22, s * 1.23)))
    # chaudière
    boil = M(trans(-1.1, 1.85, 0), rotz(-math.pi / 2))
    ms.append(cyl(0.72, 0.72, 4.4, 12, (255, 255, 255), B).xf(boil))
    for k in range(4):
        ms.append(cyl(0.735, 0.735, 0.06, 12, (190, 150, 60), caps=False).xf(M(boil, trans(0, 0.6 + k * 1.0, 0))))
    for s in (-1, 1):  # rambarde
        ms.append(box(4.0, 0.03, 0.03, (190, 190, 190), 'metal').xf(trans(0.6, 2.35, s * 0.62)))
    # boîte à fumée + porte
    ms.append(cyl(0.76, 0.76, 0.9, 12, (30, 30, 32), B).xf(M(trans(2.4, 1.85, 0), rotz(-math.pi / 2))))
    ms.append(cyl(0.6, 0.55, 0.08, 12, (50, 50, 55), 'metal').xf(M(trans(3.3, 1.85, 0), rotz(-math.pi / 2))))
    ms.append(box(0.05, 0.08, 0.3, (190, 150, 60)).xf(trans(3.4, 1.85, 0)))
    ms.append(box(0.05, 0.3, 0.05, (190, 150, 60)).xf(trans(3.4, 1.7, 0)))
    # cheminée haute évasée
    ms.append(cyl(0.22, 0.22, 0.9, 10, (30, 30, 32), B).xf(trans(2.6, 2.5, 0)))
    ms.append(cyl(0.22, 0.38, 0.4, 10, (30, 30, 32), B).xf(trans(2.6, 3.4, 0)))
    ms.append(cyl(0.39, 0.39, 0.06, 10, (190, 150, 60)).xf(trans(2.6, 3.78, 0)))
    # dômes
    ms.append(cyl(0.3, 0.26, 0.4, 10, (190, 150, 60), 'metal').xf(trans(0.6, 2.5, 0)))
    ms.append(sphere(0.26, 8, 3, (190, 150, 60)).xf(trans(0.6, 2.9, 0)))
    ms.append(cyl(0.25, 0.22, 0.3, 8, (30, 30, 32), B).xf(trans(1.6, 2.5, 0)))
    # sifflet
    ms.append(cyl(0.05, 0.05, 0.35, 6, (200, 165, 70)).xf(trans(-1.7, 2.5, 0)))
    ms.append(cyl(0.07, 0.07, 0.15, 6, (200, 165, 70)).xf(trans(-1.7, 2.85, 0)))
    # lanterne
    ms.append(box(0.35, 0.4, 0.35, (40, 40, 40)).xf(trans(3.2, 2.7, 0)))
    ms.append(box(0.04, 0.24, 0.24, (255, 240, 180), emis=0.8).xf(trans(3.38, 2.78, 0)))
    # chasse-bœufs à barreaux
    for k in range(7):
        zz = -0.9 + k * 0.3
        ms.append(rod((3.95, 0.62, zz), (4.85, 0.1, zz * 0.3), 0.03, (80, 80, 85)))
    ms.append(rod((3.95, 0.62, -0.95), (3.95, 0.62, 0.95), 0.04, (80, 80, 85)))
    # cabine
    ms.append(box(1.7, 2.0, 2.2, (255, 255, 255), B).xf(trans(-3.0, 1.05, 0)))
    ms.append(box(2.0, 0.1, 2.5, (40, 40, 40)).xf(trans(-3.0, 3.1, 0)))
    for s in (-1, 1):
        ms.append(box(0.5, 0.5, 0.02, (60, 70, 80)).xf(trans(-2.7, 2.3, s * 1.11)))
        ms.append(box(1.5, 0.08, 0.04, (190, 150, 60)).xf(trans(-3.0, 1.9, s * 1.12)))
    # bogie avant (petites roues) + 2 essieux moteurs (grandes roues avec contrepoids)
    for x in (3.0, 2.0):
        ms.append(_axle_wheels(x, 0.42, wheel_rot * (0.75 / 0.42), (150, 30, 25), 8))
    ms.append(box(1.6, 0.18, 1.5, (40, 40, 42)).xf(trans(2.5, 0.5, 0)))
    for x in (-0.4, -2.2):
        ms.append(_axle_wheels(x, 0.75, wheel_rot, (150, 30, 25), 14, cw=True))
    # cylindres, tiges de piston, bielle motrice et bielle d'accouplement
    for s in (-1, 1):
        zz = s * 1.0
        ms.append(cyl(0.24, 0.24, 1.0, 10, (40, 40, 42), B).xf(M(trans(2.0, 0.95, s * 0.82), rotz(-math.pi / 2))))
        a = wheel_rot + (0 if s > 0 else math.pi / 2)
        pin_f = np.array([-0.4 + 0.3 * math.cos(a), 0.75 + 0.3 * math.sin(a), zz])
        pin_r = np.array([-2.2 + 0.3 * math.cos(a), 0.75 + 0.3 * math.sin(a), zz])
        ms.append(box(1.8, 0.09, 0.05, (190, 190, 195), 'metal').xf(trans((pin_f + pin_r) / 2 - np.array([0, 0.045, 0]))))
        cross = np.array([1.0 + 0.3 * math.cos(a), 0.95, zz + 0.04])
        ms.append(rod(cross, pin_f + np.array([0, 0, 0.04]), 0.045, (200, 200, 205), 'metal'))
        ms.append(rod((2.0, 0.95, zz + 0.04), cross, 0.03, (210, 210, 215), 'metal'))
        ms.append(box(0.18, 0.14, 0.08, (180, 180, 185), 'metal').xf(trans(cross - np.array([0, 0.07, 0]))))
        for p_ in (pin_f, pin_r):
            ms.append(cyl(0.05, 0.05, 0.1, 6, (220, 220, 220)).xf(M(trans(p_), rotx(math.pi / 2), trans(0, -0.05, 0))))
    ms.append(axle_box(-0.4, 1.0, 0.98))
    ms.append(axle_box(-2.2, 1.0, 0.98))
    return merge(ms)


def tender(wheel_rot=0.0):
    B = 'loco_black'
    ms = [box(4.0, 1.6, 2.2, (255, 255, 255), B).xf(trans(0, 0.9, 0)),
          box(3.6, 0.3, 1.9, (20, 20, 20), 'gravel').xf(trans(0.2, 2.45, 0)),
          box(4.0, 0.06, 2.22, (190, 150, 60)).xf(trans(0, 2.2, 0))]
    for x in (-1.3, -0.5, 0.5, 1.3):
        ms.append(_axle_wheels(x, 0.42, wheel_rot * (0.75 / 0.42), (150, 30, 25), 8))
    ms.append(axle_box(-0.9, 0.85, 1.12))
    ms.append(axle_box(0.9, 0.85, 1.12))
    ms.append(buffers(-2.0, 0.95, -1))
    return merge(ms)


def carriage(wheel_rot=0.0, lit=False, length=8.0, col=(255, 255, 255), glass=False):
    ms = [box(length, 0.35, 2.2, (40, 40, 40)).xf(trans(0, 0.85, 0))]
    n = int(length / 1.1)
    win_y0, win_y1 = 1.6, 2.6
    if not glass:
        ms.append(box(length, 1.8, 2.4, col, 'maroon').xf(trans(0, 1.1, 0)))
        for i in range(n):
            x = -length / 2 + 0.55 + i * length / n
            for s in (-1, 1):
                ms.append(box(0.8, 0.8, 0.02, (255, 255, 255), 'car_window').xf(trans(x, 1.85, s * 1.21)))
    else:
        # vraies fenêtres : murs autour des ouvertures, vitres transparentes, intérieur visible
        ms.append(box(length, 0.05, 2.3, (120, 85, 55), 'planks').xf(trans(0, 1.15, 0)))
        for s in (-1, 1):
            ms.append(box(length, win_y0 - 1.1, 0.06, col, 'maroon').xf(trans(0, 1.1, s * 1.18)))
            ms.append(box(length, 2.9 - win_y1, 0.06, col, 'maroon').xf(trans(0, win_y1, s * 1.18)))
            step = length / n
            for i in range(n + 1):
                x = -length / 2 + i * step
                ms.append(box(0.28 if 0 < i < n else 0.15, win_y1 - win_y0, 0.06, col, 'maroon').xf(trans(x, win_y0, s * 1.18)))
            for i in range(n):
                x = -length / 2 + (i + 0.5) * step
                ms.append(box(step - 0.28, win_y1 - win_y0, 0.015, (180, 205, 220), alpha=0.18).xf(trans(x, win_y0, s * 1.2)))
                ms.append(box(step - 0.2, 0.04, 0.03, (200, 170, 90)).xf(trans(x, win_y0 - 0.02, s * 1.215)))
                # banquettes face à face
                ms.append(box(step * 0.8, 0.45, 0.5, (120, 40, 40), 'cloth').xf(trans(x - 0.3, 1.2, 0)))
                ms.append(box(0.12, 0.7, 2.0, (110, 35, 35), 'cloth').xf(trans(x - 0.5, 1.6, 0)))
        for e in (-1, 1):
            ms.append(box(0.06, 1.75, 2.4, col, 'maroon').xf(trans(e * length / 2, 1.15, 0)))
        ms.append(box(length, 0.05, 2.3, (210, 200, 175), 'planks_v').xf(trans(0, 2.85, 0)))
    # toit bombé
    for s in (-1, 1):
        ms.append(quad((-length / 2 - 0.1, 2.9, s * 1.3), (length / 2 + 0.1, 2.9, s * 1.3), (length / 2 + 0.1, 3.25, 0), (-length / 2 - 0.1, 3.25, 0),
                       (90, 90, 88), 'roof_tin', ((0, 0), (length / 2, 0), (length / 2, 1), (0, 1))))
    ms.append(box(length + 0.2, 0.08, 2.6, (60, 50, 40)).xf(trans(0, 2.86, 0)))
    for s in (-1, 1):
        ms.append(box(length, 0.05, 0.03, (200, 170, 90)).xf(trans(0, 1.35, s * 1.215)))
        ms.append(box(length * 0.9, 0.06, 0.25, (50, 50, 50)).xf(trans(0, 0.72, s * 1.2)))  # marchepied
    for x in (-length / 2 + 1.0, -length / 2 + 1.8, length / 2 - 1.0, length / 2 - 1.8):
        ms.append(_axle_wheels(x, 0.42, wheel_rot * (0.75 / 0.42), (40, 40, 42), 8))
    ms.append(axle_box(-length / 2 + 1.4, 0.85, 1.0))
    ms.append(axle_box(length / 2 - 1.4, 0.85, 1.0))
    ms.append(buffers(-length / 2 - 0.05, 0.95, -1))
    ms.append(buffers(length / 2 + 0.05, 0.95, 1))
    return merge(ms)


def goods_wagon(kind='open', length=5.0, col=(130, 95, 60), wheel_rot=0.0):
    ms = [box(length, 0.35, 2.2, (40, 40, 40)).xf(trans(0, 0.85, 0))]
    if kind == 'open':
        ms.append(box(length, 0.1, 2.2, col, 'planks', ts=0.8).xf(trans(0, 1.2, 0)))
        for s in (-1, 1):
            ms.append(box(length, 0.7, 0.08, col, 'planks', ts=0.8).xf(trans(0, 1.2, s * 1.06)))
        for s in (-1, 1):
            ms.append(box(0.08, 0.7, 2.2, col, 'planks', ts=0.8).xf(trans(s * (length / 2 - 0.04), 1.2, 0)))
        ms.append(sphere(1.0, 8, 4, (255, 255, 255), 'sacking', sy=0.35).xf(M(trans(0, 1.5, 0), scale(length / 2.2, 1, 0.9))))
        for s in (-1, 1):
            for x in (-length / 3, 0, length / 3):
                ms.append(box(0.08, 0.72, 0.03, (60, 60, 60)).xf(trans(x, 1.19, s * 1.11)))
    else:
        ms.append(box(length, 1.9, 2.3, col, 'planks_v', ts=0.8).xf(trans(0, 1.2, 0)))
        ms.append(box(length + 0.1, 0.12, 2.5, (80, 80, 80)).xf(trans(0, 3.1, 0)))
        for s in (-1, 1):
            ms.append(box(1.4, 1.6, 0.03, (100, 70, 45), 'planks_v').xf(trans(0, 1.3, s * 1.16)))
            ms.append(box(1.5, 0.05, 0.05, (60, 60, 60)).xf(trans(0, 2.95, s * 1.18)))
            for x in (-length / 2 + 0.1, length / 2 - 0.1):
                ms.append(box(0.08, 1.9, 0.04, (60, 60, 60)).xf(trans(x, 1.2, s * 1.17)))
        # échelle d'accès au toit (pour le garde)
        for k in range(6):
            ms.append(box(0.04, 0.04, 0.4, (60, 60, 60)).xf(trans(length / 2 + 0.03, 1.4 + k * 0.3, 0.7)))
    for x in (-length / 2 + 1.0, length / 2 - 1.0):
        ms.append(_axle_wheels(x, 0.42, wheel_rot * (0.75 / 0.42), (40, 40, 42), 8))
        ms.append(axle_box(x, 0.85, 1.0))
    ms.append(buffers(-length / 2 - 0.05, 0.95, -1))
    ms.append(buffers(length / 2 + 0.05, 0.95, 1))
    return merge(ms)


def train(parts, x=0.0, z=0.0, wheel_rot=0.0, gap=0.4, glass_car=-1):
    """parts liste de ('loco'|'tender'|'car'|'open'|'van') ; la loco en tête vers +x"""
    L = {'loco': 8.6, 'tender': 4.0, 'car': 8.0, 'open': 5.0, 'van': 5.0}
    ms = []
    cx = x
    for i, p in enumerate(parts):
        l = L[p]
        cx -= l / 2
        if p == 'loco':
            m = locomotive(wheel_rot)
        elif p == 'tender':
            m = tender(wheel_rot)
        elif p == 'car':
            m = carriage(wheel_rot, glass=(i == glass_car))
        elif p == 'open':
            m = goods_wagon('open', col=(130, 95, 60) if i % 2 else (115, 80, 50), wheel_rot=wheel_rot)
        else:
            m = goods_wagon('van', col=(140, 70, 50), wheel_rot=wheel_rot)
        ms.append(m.xf(trans(cx, 0, z)))
        cx -= l / 2 + gap
    return merge(ms)


# ---------------------------------------------------------------- gare
def station_building():
    ms = [box(14, 3.4, 6, (255, 255, 255), 'stone_block', ts=1.2)]
    # toit
    rt = [[(-7.4, 3.4, 3.4), (7.4, 3.4, 3.4), (7.4, 5.0, 0)], [(-7.4, 3.4, 3.4), (7.4, 5.0, 0), (-7.4, 5.0, 0)],
          [(7.4, 3.4, -3.4), (-7.4, 3.4, -3.4), (-7.4, 5.0, 0)], [(7.4, 3.4, -3.4), (-7.4, 5.0, 0), (7.4, 5.0, 0)]]
    ms.append(Mesh(rt, C((150, 150, 145)), [[(0, 1), (6, 1), (6, 0)], [(0, 1), (6, 0), (0, 0)]] * 2, TEXB['roof_tin']))
    for s in (-1, 1):
        ms.append(Mesh([[(s * 7, 3.4, 3.0), (s * 7, 3.4, -3.0), (s * 7, 5.0, 0)]], C((255, 255, 255)), [[(0, 1), (2, 1), (1, 0)]], TEXB['stone_block']))
    # portes/fenêtres côté quai (+z)
    for x in (-5, -2.5, 2.5, 5):
        ms.append(box(1.1, 1.5, 0.06, (255, 255, 255), 'window').xf(trans(x, 1.1, 3.01)))
        ms.append(box(1.3, 0.12, 0.12, (220, 210, 190)).xf(trans(x, 2.62, 3.04)))
    ms.append(box(1.4, 2.4, 0.06, (255, 255, 255), 'door').xf(trans(0, 0, 3.01)))
    # auvent sur colonnes de fonte
    ms.append(box(15, 0.08, 4.0, (130, 130, 125), 'roof_tin', ts=1.0).xf(M(trans(0, 3.6, 5.0), rotx(0.12))))
    for x in np.linspace(-6.8, 6.8, 7):
        ms.append(cyl(0.08, 0.08, 3.5, 6, (40, 70, 55)).xf(trans(x, 0, 6.7)))
        ms.append(box(0.5, 0.06, 0.06, (40, 70, 55)).xf(M(trans(x, 3.2, 6.5), rotx(0.6))))
    # frise festonnée
    for x in np.linspace(-7.3, 7.3, 30):
        ms.append(box(0.4, 0.25, 0.03, (235, 230, 215)).xf(trans(x, 3.15, 6.98)))
    # panneau de gare (blanc avec traits)
    ms.append(box(3.4, 0.7, 0.08, (240, 238, 230)).xf(trans(0, 2.6, 6.75)))
    for i in range(9):
        ms.append(box(0.22, 0.38, 0.02, (25, 25, 25)).xf(trans(-1.3 + i * 0.32, 2.76, 6.8)))
    for x in (-1.6, 1.6):
        ms.append(box(0.08, 2.7, 0.08, (40, 70, 55)).xf(trans(x, 0, 6.75)))
    # lampes
    for x in (-4.5, 4.5):
        ms.append(cyl(0.05, 0.05, 2.8, 5, (40, 40, 40)).xf(trans(x, 0, 7.3)))
        ms.append(box(0.3, 0.4, 0.3, (40, 40, 40)).xf(trans(x, 2.8, 7.3)))
        ms.append(box(0.24, 0.3, 0.24, (240, 220, 150), emis=0.5).xf(trans(x, 2.85, 7.3)))
    # bancs, malles
    for x in (-3.5, 3.5):
        ms.append(box(1.6, 0.08, 0.45, (120, 85, 55)).xf(trans(x, 0.45, 3.5)))
        ms.append(box(1.6, 0.5, 0.06, (120, 85, 55)).xf(trans(x, 0.5, 3.3)))
        for xx in (-0.7, 0.7):
            ms.append(box(0.06, 0.45, 0.4, (50, 50, 50)).xf(trans(x + xx, 0, 3.5)))
    ms.append(box(0.8, 0.5, 0.5, (110, 70, 40), 'planks').xf(trans(6.0, 0, 5.8)))
    ms.append(box(0.6, 0.4, 0.45, (90, 60, 40), 'planks').xf(trans(6.1, 0.5, 5.8)))
    return merge(ms)


def platform(x0, x1, z0, z1, h=0.9):
    return merge([box(x1 - x0, h, z1 - z0, (255, 255, 255), 'stone_block', ts=1.0).xf(trans((x0 + x1) / 2, 0, (z0 + z1) / 2)),
                  box(x1 - x0, 0.06, 0.4, (220, 215, 200)).xf(trans((x0 + x1) / 2, h, z1 - 0.2))])


LEVER_COLS = [(190, 30, 30), (190, 30, 30), (30, 30, 30), (220, 190, 40), (190, 30, 30), (30, 30, 30)]


def lever_frame(pulls=None):
    pulls = pulls or [0] * 6
    ms = [box(3.0, 0.3, 0.5, (70, 70, 75), 'metal').xf(trans(0, 0, 0))]
    for i, c in enumerate(LEVER_COLS):
        x = -1.25 + i * 0.5
        arm = M(trans(x, 0.3, 0), rotx(0.35 - 0.8 * pulls[i]))
        ms.append(box(0.07, 1.45, 0.07, c).xf(arm))
        ms.append(box(0.08, 0.25, 0.08, (210, 210, 210), 'metal').xf(M(arm, trans(0, 1.25, 0))))
        ms.append(box(0.2, 0.16, 0.02, (240, 240, 230)).xf(trans(x, 0.12, 0.26)))
    return merge(ms)


def signal_box_ext():
    W = (255, 255, 255)
    ms = [box(4.2, 2.5, 3.2, W, 'brick', ts=1.0),
          box(4.4, 2.0, 0.1, W, 'planks_white', ts=1.0).xf(trans(0, 2.5, -1.65)),   # mur arrière
          box(4.4, 0.6, 0.1, W, 'planks_white', ts=1.0).xf(trans(0, 2.5, 1.65)),    # allège avant
          box(4.4, 0.2, 0.1, W, 'planks_white').xf(trans(0, 4.3, 1.65))]
    for s in (-1, 1):
        ms.append(box(0.1, 0.6, 3.4, W, 'planks_white', ts=1.0).xf(trans(s * 2.15, 2.5, 0)))
        ms.append(box(0.1, 0.2, 3.4, W, 'planks_white').xf(trans(s * 2.15, 4.3, 0)))
        ms.append(box(0.05, 1.2, 3.2, (150, 180, 200), alpha=0.22).xf(trans(s * 2.15, 3.1, 0)))
    # grandes vitres de la cabine (côté voie +z)
    ms.append(box(4.2, 1.2, 0.04, (150, 180, 200), alpha=0.22).xf(trans(0, 3.1, 1.66)))
    for x in np.linspace(-2.1, 2.1, 6):
        ms.append(box(0.08, 1.2, 0.08, (235, 232, 222)).xf(trans(x, 3.1, 1.68)))
    ms.append(box(4.4, 0.06, 0.12, (235, 232, 222)).xf(trans(0, 3.65, 1.68)))
    rt = [[(-2.6, 4.5, 2.0), (2.6, 4.5, 2.0), (2.6, 5.5, 0)], [(-2.6, 4.5, 2.0), (2.6, 5.5, 0), (-2.6, 5.5, 0)],
          [(2.6, 4.5, -2.0), (-2.6, 4.5, -2.0), (-2.6, 5.5, 0)], [(2.6, 4.5, -2.0), (-2.6, 5.5, 0), (2.6, 5.5, 0)]]
    ms.append(Mesh(rt, C((110, 50, 40)), [[(0, 1), (3, 1), (3, 0)], [(0, 1), (3, 0), (0, 0)]] * 2, TEXB['roof_red']))
    for s in (-1, 1):
        ms.append(Mesh([[(s * 2.2, 4.5, 1.7), (s * 2.2, 4.5, -1.7), (s * 2.2, 5.5, 0)]], C((255, 255, 255)), [[(0, 1), (1, 1), (.5, 0)]], TEXB['planks_white']))
    # escalier extérieur
    for k in range(9):
        ms.append(box(0.9, 0.06, 0.3, (130, 100, 70), 'planks').xf(trans(-2.65, k * 0.28, -1.2 + k * 0.28)))
    ms.append(box(0.06, 1.0, 3.0, (100, 70, 45)).xf(M(trans(-3.1, 1.6, 0.0), rotx(-0.78))))
    ms.append(box(1.0, 1.0, 0.1, (255, 255, 255), 'planks_white').xf(trans(-2.65, 2.5, 1.2)))
    # plaque nom
    ms.append(box(1.8, 0.35, 0.05, (240, 238, 230)).xf(trans(0, 2.15, 1.65)))
    return merge(ms)


def lever_grip(base, i, pull):
    """position (monde) de la poignée du levier i ; base = position du bâti"""
    x = -1.25 + i * 0.5
    a = 0.35 - 0.8 * pull
    return np.asarray(base, float) + np.array([x, 0.3 + 1.32 * math.cos(a), 1.32 * math.sin(a)])


def signal_box_int():
    """intérieur de la cabine, plancher à y=2.5"""
    ms = [box(4.2, 0.05, 3.2, (140, 105, 70), 'planks', ts=0.8).xf(trans(0, 2.45, 0)),
          box(4.2, 2.0, 0.1, (220, 212, 190), 'planks_white', ts=1.0, faces='f').xf(trans(0, 2.5, -1.6)),
          box(4.2, 0.05, 3.2, (200, 190, 165), 'planks_v').xf(trans(0, 4.5, 0))]
    ms.append(lever_frame().xf(trans(0, 2.5, 0.9)))

    def diag(d, n):
        d.rectangle([0, 0, n, n], fill=(30, 30, 30))
        d.line([0, 18, n, 18], fill=(230, 230, 230), width=2)
        d.line([8, 18, 22, 10, n, 10], fill=(230, 230, 230), width=2)
        for x in (6, 14, 22):
            d.rectangle([x, 22, x + 2, 25], fill=(200, 40, 40))
    tex_draw('diagram', diag)
    ms.append(box(2.0, 0.7, 0.04, (255, 255, 255), 'diagram').xf(trans(0, 3.7, -1.53)))
    # poêle, horloge (aiguilles bien visibles), cloches, table + registre
    ms.append(cyl(0.25, 0.25, 0.8, 8, (40, 40, 40), 'metal').xf(trans(1.6, 2.5, -1.1)))
    ms.append(cyl(0.06, 0.06, 1.2, 5, (40, 40, 40)).xf(trans(1.6, 3.3, -1.1)))
    ms.append(clock_mesh(10, 10, 0.24).xf(trans(-1.4, 3.95, -1.48)))
    for x in (-0.6, -0.2, 0.2):
        ms.append(sphere(0.08, 6, 3, (200, 165, 70)).xf(trans(x, 3.3, -1.5)))
    ms.append(box(0.9, 0.05, 0.6, (120, 85, 55), 'planks').xf(trans(-1.4, 3.3, -1.2)))
    for (x, z) in ((-1.8, -1.45), (-1.0, -1.45), (-1.8, -0.95), (-1.0, -0.95)):
        ms.append(box(0.05, 0.8, 0.05, (100, 70, 45)).xf(trans(x, 2.5, z)))
    ms.append(box(0.3, 0.008, 0.4, (240, 235, 215)).xf(trans(-1.15, 3.351, -1.3)))
    ms.append(box(0.02, 0.01, 0.38, (60, 50, 40)).xf(trans(-1.15, 3.36, -1.3)))
    return merge(ms)


def market_stall(col=(200, 60, 50), seed=0):
    rr = np.random.default_rng(seed)
    ms = [box(2.6, 0.9, 1.2, (140, 100, 62), 'planks', ts=0.8)]
    for (x, z) in ((-1.25, -0.55), (1.25, -0.55), (-1.25, 0.55), (1.25, 0.55)):
        ms.append(box(0.08, 2.4, 0.08, (110, 80, 50)).xf(trans(x, 0, z)))
    ms.append(quad((-1.4, 2.4, -0.7), (1.4, 2.4, -0.7), (1.4, 2.1, 1.0), (-1.4, 2.1, 1.0), col, 'awning', ((0, 0), (3, 0), (3, 1), (0, 1))))
    # marchandises
    goods = [(220, 120, 40), (90, 150, 50), (200, 40, 40), (230, 200, 80), (120, 70, 40)]
    for i in range(6):
        c = goods[rr.integers(0, len(goods))]
        ms.append(sphere(0.18, 6, 3, c, sy=0.7).xf(trans(-1.0 + i * 0.4, 0.98, rr.uniform(-0.3, 0.3))))
    ms.append(box(0.5, 0.35, 0.4, (160, 120, 80), 'planks').xf(trans(1.6, 0, 0.9)))
    ms.append(cyl(0.25, 0.2, 0.5, 8, (180, 110, 70)).xf(trans(-1.7, 0, 0.8)))
    return merge(ms)


def cape_house(col=(235, 225, 200)):
    ms = [box(6, 2.8, 5, col, 'plaster', ts=1.5)]
    rt = [[(-3.3, 2.8, 2.8), (3.3, 2.8, 2.8), (3.3, 4.2, 0)], [(-3.3, 2.8, 2.8), (3.3, 4.2, 0), (-3.3, 4.2, 0)],
          [(3.3, 2.8, -2.8), (-3.3, 2.8, -2.8), (-3.3, 4.2, 0)], [(3.3, 2.8, -2.8), (-3.3, 4.2, 0), (3.3, 4.2, 0)]]
    ms.append(Mesh(rt, C((150, 150, 145)), [[(0, 1), (3, 1), (3, 0)], [(0, 1), (3, 0), (0, 0)]] * 2, TEXB['roof_tin']))
    for s in (-1, 1):
        ms.append(Mesh([[(s * 3, 2.8, 2.5), (s * 3, 2.8, -2.5), (s * 3, 4.2, 0)]], C(col), [[(0, 1), (1, 1), (.5, 0)]], TEXB['plaster']))
    ms.append(box(1.0, 2.1, 0.06, (255, 255, 255), 'door').xf(trans(0, 0, 2.51)))
    for x in (-1.8, 1.8):
        ms.append(box(1.0, 1.2, 0.06, (255, 255, 255), 'window').xf(trans(x, 1.0, 2.51)))
    ms.append(box(6.4, 0.08, 1.8, (140, 140, 135), 'roof_tin').xf(M(trans(0, 2.6, 3.4), rotx(0.15))))
    for x in (-3, -1, 1, 3):
        ms.append(box(0.1, 2.6, 0.1, (110, 80, 50)).xf(trans(x, 0, 4.2)))
    ms.append(box(6.0, 0.15, 2.0, (150, 130, 110), 'planks').xf(trans(0, 0, 3.4)))
    return merge(ms)


def house_interior():
    ms = [box(6, 0.05, 5, (150, 110, 70), 'planks', ts=0.8).xf(trans(0, -0.05, 0)),
          box(6, 2.8, 0.1, (230, 220, 195), 'plaster', ts=1.5, faces='f').xf(trans(0, 0, -2.5)),
          box(0.1, 2.8, 5, (230, 220, 195), 'plaster', ts=1.5, faces='r').xf(trans(-3, 0, 0)),
          box(0.1, 2.8, 5, (230, 220, 195), 'plaster', ts=1.5, faces='l').xf(trans(3, 0, 0))]
    ms.append(box(1.0, 1.2, 0.06, (255, 255, 255), 'window').xf(trans(-1.2, 1.0, -2.44)))
    ms.append(box(1.4, 0.06, 0.8, (120, 85, 55), 'planks').xf(trans(1.2, 0.75, -1.5)))
    for (x, z) in ((0.6, -1.15), (1.8, -1.15), (0.6, -1.85), (1.8, -1.85)):
        ms.append(box(0.06, 0.75, 0.06, (100, 70, 45)).xf(trans(x, 0, z)))
    ms.append(box(0.4, 0.04, 0.3, (240, 235, 220)).xf(trans(1.0, 0.81, -1.5)))
    ms.append(cyl(0.05, 0.05, 0.1, 6, (230, 230, 230)).xf(trans(1.5, 0.81, -1.4)))
    ms.append(box(1.6, 1.8, 0.45, (120, 85, 55), 'planks').xf(trans(-2.0, 0, -2.2)))
    for k in range(3):
        ms.append(box(1.4, 0.04, 0.4, (100, 70, 45)).xf(trans(-2.0, 0.5 + k * 0.5, -1.97)))
        for j in range(4):
            ms.append(box(0.2, 0.25, 0.2, [(200, 60, 50), (240, 230, 210), (80, 100, 150), (190, 160, 60)][j]).xf(trans(-2.5 + j * 0.35, 0.54 + k * 0.5, -2.0)))
    ms.append(box(1.2, 0.02, 0.8, (150, 60, 50), 'cloth').xf(trans(0, 0.0, 0.5)))
    # poussière en tas
    return merge(ms)


def broom():
    return merge([cyl(0.02, 0.02, 1.2, 4, (150, 110, 60)), cyl(0.06, 0.12, 0.3, 6, (200, 170, 90)).xf(trans(0, -0.3, 0))])


def dustbin(lid=True):
    ms = [cyl(0.25, 0.22, 0.6, 8, (130, 130, 130), 'metal')]
    if lid:
        ms.append(cyl(0.27, 0.27, 0.05, 8, (120, 120, 120), 'metal').xf(trans(0, 0.6, 0)))
        ms.append(box(0.12, 0.04, 0.04, (80, 80, 80)).xf(trans(0, 0.67, 0)))
    for s in (-1, 1):
        ms.append(box(0.04, 0.06, 0.1, (80, 80, 80)).xf(trans(s * 0.25, 0.5, 0)))
    return merge(ms)


TROLLEY_GRIP = (0.82, -1.25)


def trolley(wheel_rot=0.0):
    """petit chariot de James (avance vers +z) : plateau bas à rebords, siège, dossier, deux brancards droits à l'arrière"""
    W = (150, 110, 70)
    ms = [box(0.8, 0.05, 1.0, W, 'planks', ts=0.5).xf(trans(0, 0.28, 0))]               # plateau
    for s in (-1, 1):
        ms.append(box(0.04, 0.14, 1.0, W, 'planks', ts=0.5).xf(trans(s * 0.38, 0.33, 0)))  # rebords bas
    ms.append(box(0.8, 0.14, 0.04, W, 'planks', ts=0.5).xf(trans(0, 0.33, 0.48)))
    ms.append(box(0.62, 0.16, 0.42, (120, 85, 55), 'planks').xf(trans(0, 0.33, -0.15)))   # siège
    ms.append(box(0.62, 0.45, 0.05, (120, 85, 55), 'planks').xf(trans(0, 0.49, -0.38)))   # dossier
    ms.append(box(0.62, 0.06, 0.03, (90, 60, 40)).xf(trans(0, 0.12, 0.47)))              # repose-pieds
    for (x, z) in ((-0.45, 0.32), (0.45, 0.32), (-0.45, -0.32), (0.45, -0.32)):
        ms.append(wheel(0.2, 0.06, 6).xf(M(trans(x, 0.2, z), rotz(math.pi / 2), roty(wheel_rot))))
    for s in (-1, 1):
        ms.append(box(0.04, 0.04, 0.9, (90, 60, 40)).xf(trans(s * 0.43, 0.2, 0)))           # essieux/longerons
    # brancards : partent des coins arrière du plateau et montent en ligne droite jusqu'aux poignées
    gy, gz = TROLLEY_GRIP
    for s in (-1, 1):
        ms.append(rod((s * 0.32, 0.33, -0.48), (s * 0.32, gy, gz), 0.025, (120, 85, 55)))
        ms.append(rod((s * 0.32, gy, gz), (s * 0.32, gy, gz - 0.12), 0.03, (60, 45, 30)))  # poignée
    ms.append(rod((-0.32, gy - 0.12, gz + 0.25), (0.32, gy - 0.12, gz + 0.25), 0.02, (120, 85, 55)))  # traverse
    return merge(ms)


def aloe(seed=0, h=1.4):
    rr = np.random.default_rng(seed)
    ms = [cyl(0.08, 0.07, h, 5, (100, 80, 60), 'bark')]
    for k in range(9):
        a = k / 9 * 6.28
        tip = (math.cos(a) * 0.55, h + 0.2 + rr.random() * 0.3, math.sin(a) * 0.55)
        side = np.array([-math.sin(a), 0, math.cos(a)]) * 0.07
        base = np.array([0, h, 0])
        ms.append(Mesh([[base + side, np.array(tip), base - side]], C((90, 120, 80)) * (0.9 + 0.2 * rr.random())))
    ms.append(cyl(0.03, 0.02, 0.6, 4, (210, 90, 40)).xf(trans(0, h + 0.2, 0)))
    ms.append(cyl(0.06, 0.02, 0.25, 5, (230, 110, 40), emis=0.2).xf(trans(0, h + 0.8, 0)))
    return merge(ms)


def bush(r=0.7, seed=0):
    return sphere(r, 6, 4, (255, 255, 255), 'scrub', sy=0.7).xf(trans(0, r * 0.4, 0))


def hills(cz=-200, seed=0, w=800):
    rr = np.random.default_rng(seed)
    ms = []
    for k in range(2):
        z = cz - k * 80
        n = 20
        xs = np.linspace(-w / 2, w / 2, n + 1)
        hs = np.convolve(15 + 25 * k + rr.random(n + 1) * 25, np.ones(3) / 3, mode='same')
        tris, uvs = [], []
        for i in range(n):
            tris += [[(xs[i], -5, z), (xs[i + 1], -5, z), (xs[i + 1], hs[i + 1], z - 10)], [(xs[i], -5, z), (xs[i + 1], hs[i + 1], z - 10), (xs[i], hs[i], z - 10)]]
            uvs += [[(0, 1), (1, 1), (1, 0)], [(0, 1), (1, 0), (0, 0)]]
        ms.append(Mesh(tris, C((190, 160, 120)) * (1 - 0.1 * k), uvs, TEXB['scrub']))
    return merge(ms)


def coins(n=4):
    rr = np.random.default_rng(n)
    return merge([cyl(0.025, 0.025, 0.006, 8, (200, 200, 205), 'metal').xf(trans(rr.uniform(-0.06, 0.06), i * 0.007, rr.uniform(-0.03, 0.03))) for i in range(n)])


def beer_bottle(level=0.5):
    ms = [cyl(0.04, 0.04, 0.2, 8, (70, 45, 20), alpha=0.85), cyl(0.04, 0.015, 0.06, 8, (70, 45, 20)).xf(trans(0, 0.2, 0)),
          cyl(0.015, 0.015, 0.06, 6, (70, 45, 20)).xf(trans(0, 0.26, 0)), cyl(0.036, 0.036, 0.2 * level, 8, (200, 140, 40)).xf(trans(0, 0.005, 0))]
    ms.append(box(0.06, 0.07, 0.002, (230, 220, 190)).xf(trans(0, 0.06, 0.041)))
    return merge(ms)


def bed():
    ms = [box(1.0, 0.5, 2.1, (240, 238, 230), 'cloth'), box(1.05, 0.05, 2.15, (90, 90, 95), 'metal').xf(trans(0, 0.25, 0))]
    ms.append(box(1.05, 1.0, 0.06, (80, 80, 85), 'metal').xf(trans(0, 0, -1.05)))
    ms.append(box(0.6, 0.12, 0.35, (250, 250, 248)).xf(trans(0, 0.5, -0.8)))
    return merge(ms)


ENV_DAY = Env(sky_top=(85, 135, 200), sky_hor=(215, 210, 190), fog=(205, 195, 170), fog_near=40, fog_far=300,
              light=(-0.5, 0.75, 0.4), amb=0.55, light_col=(255, 240, 210))
ENV_GOLD = Env(sky_top=(90, 110, 170), sky_hor=(240, 180, 120), fog=(220, 170, 125), fog_near=40, fog_far=280,
               light=(-0.8, 0.35, 0.3), amb=0.5, light_col=(255, 200, 140))
ENV_IN = Env(sky_top=(40, 35, 30), sky_hor=(40, 35, 30), fog=(30, 26, 22), fog_near=8, fog_far=40,
             light=(0.4, 0.7, 0.6), amb=0.6, light_col=(255, 235, 200))


# ---------------------------------------------------------------- marché détaillé
def crate(w=0.6, h=0.45, d=0.45, col=(160, 120, 80), fill=None):
    ms = [box(w, h, d, col, 'planks', ts=0.4)]
    if fill is not None:
        for i in range(6):
            ms.append(sphere(min(w, d) * 0.16, 5, 3, fill).xf(trans(-w * 0.3 + (i % 3) * w * 0.3, h + 0.02, -d * 0.2 + (i // 3) * d * 0.4)))
    return merge(ms)


def basket(r=0.3, h=0.3, fill=None, seed=0):
    ms = [cyl(r * 0.8, r, h, 8, (190, 155, 95), 'sacking', ts=0.3)]
    if fill is not None:
        ms.append(sphere(r * 0.92, 7, 3, fill, sy=0.35).xf(trans(0, h, 0)))
    return merge(ms)


def pot(r=0.25, col=(170, 90, 55)):
    return merge([sphere(r, 7, 4, col, sy=1.1).xf(trans(0, r, 0)), cyl(r * 0.45, r * 0.55, r * 0.5, 7, col).xf(trans(0, r * 1.9, 0))])


def sack_pile(n=4, seed=0):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        ms.append(sphere(0.32, 6, 3, (255, 255, 255), 'sacking', sy=0.6).xf(M(trans((i % 3) * 0.5 - 0.5, 0.18 + (i // 3) * 0.35, rr.uniform(-0.1, 0.1)), roty(rr.random()))))
    return merge(ms)


def chicken(col=(230, 225, 210), phase=0.0):
    ms = [sphere(0.13, 6, 3, col, sy=0.8).xf(trans(0, 0.2, 0)), sphere(0.06, 5, 3, col).xf(trans(0, 0.33, 0.1 + 0.02 * math.sin(phase * 8))),
          box(0.04, 0.03, 0.05, (230, 170, 40)).xf(trans(0, 0.32, 0.17 + 0.02 * math.sin(phase * 8))),
          box(0.03, 0.05, 0.03, (200, 40, 40)).xf(trans(0, 0.39, 0.1)),
          box(0.12, 0.12, 0.04, (200, 190, 170)).xf(M(trans(0, 0.25, -0.13), rotx(0.6)))]
    for s in (-1, 1):
        ms.append(box(0.02, 0.12, 0.02, (220, 160, 40)).xf(trans(s * 0.04, 0, 0)))
    return merge(ms)


def donkey(phase=0.0):
    F = 'fur_baboon'
    ms = [box(0.45, 0.45, 1.0, (130, 125, 120), F).xf(trans(0, 0.75, 0))]
    head = M(trans(0, 1.15, 0.55), rotx(0.6))
    ms.append(box(0.22, 0.25, 0.5, (130, 125, 120), F).xf(M(head, trans(0, -0.05, 0.15))))
    ms.append(box(0.18, 0.15, 0.12, (90, 85, 80)).xf(M(head, trans(0, -0.08, 0.42))))
    for s in (-1, 1):
        ms.append(box(0.06, 0.28, 0.04, (110, 105, 100)).xf(M(head, trans(s * 0.08, 0.15, 0.0), rotz(s * 0.3))))
    for (x, z, ph) in ((-0.15, 0.4, 0), (0.15, 0.4, math.pi), (-0.15, -0.4, math.pi), (0.15, -0.4, 0)):
        lg = M(trans(x, 0.78, z), rotx(0.3 * math.sin(phase + ph)))
        ms.append(box(0.1, 0.78, 0.11, (130, 125, 120), F).xf(M(lg, trans(0, -0.78, 0))))
    for s in (-1, 1):
        ms.append(basket(0.2, 0.35, (220, 150, 50), 0).xf(trans(s * 0.35, 0.8, 0)))
    return merge(ms)


def well():
    return merge([cyl(0.8, 0.8, 0.8, 10, (255, 255, 255), 'stone_block', ts=0.8), cyl(0.65, 0.65, 0.05, 10, (30, 40, 50)).xf(trans(0, 0.7, 0)),
                  box(0.1, 1.6, 0.1, (110, 80, 50)).xf(trans(-0.75, 0.8, 0)), box(0.1, 1.6, 0.1, (110, 80, 50)).xf(trans(0.75, 0.8, 0)),
                  cyl(0.07, 0.07, 1.6, 6, (110, 80, 50)).xf(M(trans(-0.8, 2.2, 0), rotz(-math.pi / 2))),
                  box(1.8, 0.08, 0.9, (150, 150, 145), 'roof_tin').xf(trans(0, 2.4, 0)),
                  cyl(0.12, 0.1, 0.2, 6, (120, 90, 60)).xf(trans(0.1, 1.2, 0))])


def bunting(a, b, n=12, cols=((200, 50, 50), (240, 220, 80), (60, 110, 170), (240, 240, 240))):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ms = [rod(a, b, 0.01, (60, 50, 40), n=3)]
    for i in range(n):
        t = (i + 0.5) / n
        p = a + (b - a) * t - np.array([0, 0.3 * 4 * t * (1 - t), 0])
        d = (b - a) / np.linalg.norm(b - a) * 0.12
        ms.append(Mesh([[p - d, p + d, p - np.array([0, 0.25, 0])]], C(cols[i % len(cols)])))
    return merge(ms)
