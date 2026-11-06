"""Décors et personnages : Violet Jessop (Olympic 1911, Titanic 1912, Britannic 1916)."""
import sys, math
sys.path[:0] = ['/home/claude/g2n']
import numpy as np
from lib import *
from common2 import *

build_base_textures()

# ---------------------------------------------------------------- textures
tex_noise('hull_black', (24, 24, 27), (36, 36, 40), seed=201, octaves=1)
tex_noise('hull_grey', (110, 116, 122), (128, 134, 140), seed=202, octaves=1)
tex_noise('hull_whiteb', (232, 232, 226), (246, 246, 240), seed=203, octaves=1)
tex_noise('ice', (200, 225, 238), (240, 250, 255), seed=204, octaves=3, speck=0.05, speck_col=(170, 205, 225))
tex_noise('sea_night', (8, 18, 34), (16, 30, 50), seed=205, speck=0.02, speck_col=(60, 80, 110))
tex_noise('sea_day', (30, 100, 135), (50, 130, 160), seed=206, speck=0.03, speck_col=(200, 230, 240))
tex_noise('sea_aegean', (20, 95, 150), (40, 125, 175), seed=207, speck=0.03, speck_col=(210, 235, 245))
tex_noise('wallpaper', (150, 120, 95), (170, 140, 110), seed=208, octaves=1, speck=0.1, speck_col=(120, 70, 70))
tex_noise('grass_night', (28, 40, 30), (40, 55, 38), seed=209, speck=0.08, speck_col=(20, 30, 22))
tex_noise('dress_black', (30, 30, 38), (42, 42, 52), seed=210, octaves=1)
tex_noise('uniform_navy', (28, 30, 48), (38, 40, 62), seed=211, octaves=1)
tex_noise('coat', (70, 60, 50), (90, 78, 64), seed=212, octaves=1)
tex_noise('coat2', (55, 58, 70), (70, 74, 88), seed=213, octaves=1)
tex_noise('underwater', (10, 60, 80), (20, 85, 105), seed=214)


def _ports(name, base, dot, lit=False):
    def f(d, n):
        d.rectangle([0, 0, n, n], fill=base)
        for y in (9, 22):
            for x in (3, 11, 19, 27):
                d.rectangle([x, y, x + 2, y + 2], fill=dot)
    tex_draw(name, f)


_ports('ports', (26, 26, 30), (150, 150, 140))
_ports('ports_lit', (12, 12, 14), (255, 225, 140))
_ports('ports_white', (236, 236, 230), (60, 70, 80))


def _superwin(name, base, win, frame):
    def f(d, n):
        d.rectangle([0, 0, n, n], fill=base)
        for x in (2, 12, 22):
            d.rectangle([x, 8, x + 7, 20], fill=frame)
            d.rectangle([x + 1, 9, x + 6, 19], fill=win)
        d.rectangle([0, 28, n, 29], fill=tuple(int(c * 0.85) for c in base))
    tex_draw(name, f)


_superwin('superwin', (236, 234, 226), (60, 75, 90), (200, 195, 185))
_superwin('superwin_lit', (40, 40, 44), (255, 220, 140), (70, 65, 60))
_superwin('superwin_dusk', (190, 188, 182), (255, 210, 130), (150, 145, 140))


def _redcross(d, n):
    d.rectangle([0, 0, n, n], fill=(240, 240, 235))
    d.rectangle([12, 3, 19, 28], fill=(200, 25, 30))
    d.rectangle([3, 12, 28, 19], fill=(200, 25, 30))


tex_draw('redcross', _redcross)


def _ship_painting(d, n):
    d.rectangle([0, 0, n, n], fill=(110, 80, 40))
    d.rectangle([2, 2, n - 3, n - 3], fill=(150, 180, 200))
    d.rectangle([2, 20, n - 3, n - 3], fill=(60, 100, 130))
    d.polygon([(5, 20), (27, 20), (25, 24), (7, 24)], fill=(20, 20, 20))
    d.rectangle([7, 16, 25, 19], fill=(240, 240, 235))
    for x in (9, 13, 17, 21):
        d.rectangle([x, 9, x + 2, 15], fill=(200, 150, 60))
        d.rectangle([x, 9, x + 2, 10], fill=(20, 20, 20))


tex_draw('ship_painting', _ship_painting)


def _photo_frame(d, n):
    d.rectangle([0, 0, n, n], fill=(60, 45, 30))
    d.rectangle([3, 3, n - 4, n - 4], fill=(200, 190, 165))
    d.ellipse([11, 7, 20, 16], fill=(120, 100, 85))
    d.rectangle([9, 16, 22, n - 4], fill=(70, 60, 55))


tex_draw('photo_frame', _photo_frame)

# ---------------------------------------------------------------- visages / personnages
SKIN_V = (240, 205, 182)
HAIR_V = (62, 40, 28)
make_face('violet', skin=SKIN_V, brow_col=(70, 45, 30), eye_col=(60, 80, 100))
make_face('violet_smile', skin=SKIN_V, brow_col=(70, 45, 30), eye_col=(60, 80, 100), mouth='smile')
make_face('violet_shock', skin=SKIN_V, brow_col=(70, 45, 30), eye_col=(60, 80, 100), mouth='open')
make_face('violet_shout', skin=SKIN_V, brow_col=(70, 45, 30), eye_col=(60, 80, 100), mouth='shout')
make_face('violet_closed', skin=SKIN_V, brow_col=(70, 45, 30), eyes_closed=True)
make_face('violet_old', skin=(232, 196, 175), brow_col=(170, 165, 160), eye_col=(60, 80, 100), soot=0.0)
make_face('violet_old_shock', skin=(232, 196, 175), brow_col=(170, 165, 160), eye_col=(60, 80, 100), mouth='open')
make_face('officer', skin=(232, 192, 165), brow_col=(80, 60, 40))
make_face('pass_m', skin=(228, 190, 160), brow_col=(60, 45, 30), mustache=True, hair_col=(60, 45, 30))
make_face('pass_m2', skin=(220, 180, 150), brow_col=(120, 90, 60), beard=True, hair_col=(120, 90, 60))
make_face('pass_w', skin=(236, 200, 178), brow_col=(110, 80, 50))
make_face('pass_w_fear', skin=(236, 200, 178), brow_col=(110, 80, 50), mouth='open')
make_face('soldier', skin=(225, 185, 155), brow_col=(70, 50, 35))
make_face('soldier_hurt', skin=(225, 185, 155), brow_col=(70, 50, 35), eyes_closed=True)


def violet(face='violet', outfit='steward'):
    """outfit : steward (robe noire, tablier, coiffe), nurse (blanc, voile croix rouge), old (gilet, cheveux gris), coat (manteau, nuit)"""
    if outfit == 'nurse':
        return Human(face, skin=SKIN_V, shirt=(244, 244, 238), pants=(244, 244, 238), robe=(244, 244, 238), shoes=(40, 30, 25),
                     hair=HAIR_V, hair_style='bald', build=0.88, extra=woman_extra('none', veil=True, apron=False))
    if outfit == 'old':
        return Human(face, skin=(232, 196, 175), shirt=(225, 220, 205), pants=(80, 70, 75), robe=(80, 70, 75), shoes=(40, 30, 25),
                     hair=(200, 198, 195), hair_style='bald', build=0.9, extra=woman_extra('grey_bun', hair=(205, 203, 200), cardigan=(130, 60, 70)))
    if outfit == 'coat':
        return Human(face, skin=SKIN_V, shirt=(45, 45, 55), pants=(30, 30, 38), robe=(45, 45, 55), shoes=(30, 25, 22),
                     hair=HAIR_V, hair_style='bald', build=0.92, extra=woman_extra('bun', hair=HAIR_V))
    return Human(face, skin=SKIN_V, shirt=(32, 32, 40), pants=(32, 32, 40), robe=(32, 32, 40), shoes=(25, 22, 20),
                 hair=HAIR_V, hair_style='bald', shirt_tex='dress_black', build=0.88,
                 extra=woman_extra('bun', cap='steward', apron=True, hair=HAIR_V))


def officer(face='officer'):
    return Human(face, skin=(232, 192, 165), shirt=(30, 32, 50), pants=(30, 32, 50), hair=(80, 60, 40), hat='kepi',
                 hat_col=(28, 30, 45), jacket=(30, 32, 50), shirt_tex='uniform_navy', tie=(20, 20, 25))


def lifebelt_extra(base=None):
    def f(P, at):
        t = at['torso']
        ms = [box(0.46, 0.3, 0.3, (240, 238, 228), 'cloth').xf(M(t, trans(0, 0.14, 0))),
              box(0.47, 0.04, 0.31, (90, 80, 70)).xf(M(t, trans(0, 0.27, 0)))]
        if base:
            ms.append(base(P, at))
        return merge(ms)
    return f


def passenger(kind=0, belt=True):
    kinds = [
        dict(face='pass_m', skin=(228, 190, 160), shirt=(70, 60, 50), pants=(50, 45, 40), hair=(60, 45, 30), hat='bowler', hat_col=(30, 28, 26), shirt_tex='coat'),
        dict(face='pass_w', skin=(236, 200, 178), shirt=(90, 50, 60), pants=(90, 50, 60), robe=(90, 50, 60), hair=(110, 80, 50), hat='bonnet',
             hat_col=(70, 50, 60), build=0.88),
        dict(face='pass_m2', skin=(220, 180, 150), shirt=(55, 58, 70), pants=(40, 40, 45), hair=(120, 90, 60), hat='flatcap', hat_col=(70, 70, 70), shirt_tex='coat2'),
        dict(face='pass_w_fear', skin=(236, 200, 178), shirt=(50, 70, 90), pants=(50, 70, 90), robe=(50, 70, 90), hair=(70, 50, 35), hat='bonnet',
             hat_col=(40, 50, 70), build=0.88),
    ]
    k = dict(kinds[kind % 4])
    face = k.pop('face')
    if belt:
        k['extra'] = lifebelt_extra()
    return Human(face, **k)


def soldier(face='soldier'):
    def band(P, at):
        return box(0.27, 0.07, 0.27, (250, 250, 248)).xf(M(at['head'], trans(0, 0.14, 0)))
    return Human(face, skin=(225, 185, 155), shirt=(120, 110, 80), pants=(110, 100, 72), hair=(70, 50, 35),
                 extra=band if face == 'soldier_hurt' else None)


# ---------------------------------------------------------------- paquebots
def _hull_bands(stations, bands, tex_for_band, col_for_band=None, ts=4.0, emis=0.0, deck_tex='planks', deck_col=(255, 255, 255), transom=(30, 30, 34)):
    """coque à partir de stations (x, demi-largeur haut, demi-largeur bas) et bandes (y0, y1) ; faces des deux bords"""
    ms = []
    yk, yd = bands[0][0], bands[-1][1]
    for bi, (y0, y1) in enumerate(bands):
        tex = tex_for_band(bi)
        col = (255, 255, 255) if col_for_band is None else col_for_band(bi)
        tris, uvs = [], []
        for i in range(len(stations) - 1):
            xa, wa_t, wa_b = stations[i]
            xb, wb_t, wb_b = stations[i + 1]
            ka0, ka1 = (y0 - yk) / (yd - yk), (y1 - yk) / (yd - yk)
            wa0, wa1 = wa_b + (wa_t - wa_b) * ka0, wa_b + (wa_t - wa_b) * ka1
            wb0, wb1 = wb_b + (wb_t - wb_b) * ka0, wb_b + (wb_t - wb_b) * ka1
            for s in (-1, 1):
                p = [(xa, y0, s * wa0), (xb, y0, s * wb0), (xb, y1, s * wb1), (xa, y1, s * wa1)]
                u = [(xa / ts, (y1 - y0) / (ts * 1.4)), (xb / ts, (y1 - y0) / (ts * 1.4)), (xb / ts, 0), (xa / ts, 0)]
                tris += [[p[0], p[1], p[2]], [p[0], p[2], p[3]]]
                uvs += [[u[0], u[1], u[2]], [u[0], u[2], u[3]]]
        ms.append(Mesh(tris, C(col), uvs, TEXB[tex] if isinstance(tex, str) else tex, emis=emis if bi == len(bands) - 1 else 0.0))
    # fond plat
    bt = []
    for i in range(len(stations) - 1):
        xa, _, wa = stations[i]
        xb, _, wb = stations[i + 1]
        bt += [[(xa, yk, -wa), (xb, yk, -wb), (xb, yk, wb)], [(xa, yk, -wa), (xb, yk, wb), (xa, yk, wa)]]
    ms.append(Mesh(bt, C((70, 66, 66))))
    # tableau arrière + pont
    xa, wa_t, wa_b = stations[0]
    ms.append(quad((xa, yk, -wa_b), (xa, yk, wa_b), (xa, yd, wa_t), (xa, yd, -wa_t), transom))
    dt, du = [], []
    for i in range(len(stations) - 1):
        xa, wa, _ = stations[i]
        xb, wb, _ = stations[i + 1]
        p = [(xa, yd, -wa), (xb, yd, -wb), (xb, yd, wb), (xa, yd, wa)]
        dt += [[p[0], p[1], p[2]], [p[0], p[2], p[3]]]
        du += [[(xa / 3, -wa / 3), (xb / 3, -wb / 3), (xb / 3, wb / 3)], [(xa / 3, -wa / 3), (xb / 3, wb / 3), (xa / 3, wa / 3)]]
    ms.append(Mesh(dt, C(deck_col), du, TEXB[deck_tex]))
    return merge(ms)


LINER_ST = [(-131, 9.0, 4.0), (-127, 12.0, 8.0), (-118, 14.0, 12.0), (80, 14.0, 13.0), (105, 11.5, 8.5), (122, 6.0, 2.5), (132, 0.6, 0.3)]
LINER_DECK = 19.0
LINER_KEEL = -10.5
FUNNEL_X = (62.0, 36.0, 10.0, -16.0)


def propeller(rot, r=3.4, blades=3, col=(150, 120, 70)):
    ms = [cyl(0.5, 0.5, 1.2, 8, col, 'metal').xf(M(rotz(math.pi / 2), trans(0, -0.6, 0)))]
    for k in range(blades):
        a = rot + k * 2 * math.pi / blades
        ms.append(box(0.25, r, 1.3, col, 'metal').xf(M(rotx(a), trans(0, 0.2, 0), rotx(0.0), roty(0.5))))
    return merge(ms)


def liner(kind='titanic', lights=0.0, prop_rot=0.0, smoke_t=None, cam=None, gash=False, hole=False):
    """paquebot classe Olympic, proue vers +x, ligne de flottaison y=0 (1 unité = 1 m). kind : olympic, titanic, britannic"""
    white = kind == 'britannic'
    lit = lights > 0.5
    if white:
        tex_band = lambda b: 'hull_whiteb' if b == 0 else 'ports_white'
    else:
        tex_band = lambda b: 'hull_black' if b == 0 else ('ports_lit' if lit else 'ports')
    ms = [_hull_bands(LINER_ST, [(LINER_KEEL, 3.0), (3.0, LINER_DECK)], tex_band, ts=4.0, emis=0.85 if lit else 0.0, transom=(225, 225, 220) if white else (30, 30, 34))]
    if white:
        # bande verte et croix rouges de navire-hôpital
        for s in (-1, 1):
            ms.append(box(196, 1.4, 0.1, (40, 140, 60)).xf(trans(-18, 8.5, s * 14.06)))
            for x in (-70, 30):
                ms.append(box(9, 9, 0.12, (255, 255, 255), 'redcross').xf(trans(x, 9.6, s * 14.08)))
    else:
        for s in (-1, 1):  # liseré doré + bande blanche du pont-promenade
            ms.append(box(196, 0.35, 0.08, (210, 175, 70)).xf(trans(-18, 15.5, s * 14.05)))
    sw = 'superwin_lit' if lit else 'superwin'
    # superstructure (ponts A/B) et roof du pont des embarcations
    ms.append(box(152, 5.5, 22.6, (255, 255, 255), sw, ts=3.0, top_tex='planks', top_col=(230, 210, 170)).xf(trans(4, LINER_DECK, 0)))
    ms.append(box(130, 3.0, 17.0, (255, 255, 255), sw, ts=3.0, top_col=(238, 236, 228)).xf(trans(0, LINER_DECK + 5.5, 0)))
    ms.append(box(10, 3.2, 21.0, (255, 255, 255), sw, ts=3.0, top_col=(238, 236, 228)).xf(trans(72, LINER_DECK + 5.5, 0)))   # passerelle
    ms.append(box(4, 1.0, 26.0, (238, 236, 228)).xf(trans(74, LINER_DECK + 7.7, 0)))                                          # ailerons de passerelle
    top = LINER_DECK + 8.5
    for i, fx in enumerate(FUNNEL_X):
        fm = merge([cyl(3.3, 3.3, 17.5, 12, (205, 145, 60)), cyl(3.35, 3.35, 4.0, 12, (25, 25, 25)).xf(trans(0, 17.5, 0)),
                    cyl(3.0, 3.0, 0.3, 12, (15, 15, 15)).xf(trans(0, 21.4, 0))])
        ms.append(fm.xf(M(trans(fx, top, 0), rotz(0.1), scale(1.0, 1.0, 0.8))))
    # mâts + étai
    for mx, mh in ((100, 52), (-98, 48)):
        ms.append(cyl(0.45, 0.25, mh, 6, (190, 160, 110)).xf(trans(mx, LINER_DECK, 0)))
    ms.append(rod((100, LINER_DECK + 50, 0), (-98, LINER_DECK + 46, 0), 0.08, (40, 40, 40), n=3))
    ms.append(rod((100, LINER_DECK + 50, 0), (131, LINER_DECK, 0), 0.08, (40, 40, 40), n=3))
    ms.append(rod((-98, LINER_DECK + 46, 0), (-130, LINER_DECK, 0), 0.08, (40, 40, 40), n=3))
    # canots sur le pont des embarcations (entre le roof et le bord)
    for s in (-1, 1):
        for x in list(np.arange(62, 18, -8.5)) + list(np.arange(-14, -66, -8.5)):
            ms.append(lifeboat_mesh(8.0, 2.2, 1.0, empty=True).xf(trans(x, LINER_DECK + 5.8, s * 10.0)))
            for dx in (-3.6, 3.6):
                ms.append(rod((x + dx, LINER_DECK + 5.5, s * 9.2), (x + dx, LINER_DECK + 8.6, s * 10.2), 0.12, (230, 230, 225), n=4))
    # hélices + gouvernail
    for z, r in ((-7.5, 3.6), (0.0, 2.9), (7.5, 3.6)):
        ms.append(propeller(prop_rot * (1 if z >= 0 else -1), r, 3 if z else 4).xf(trans(-134 - (2 if z == 0 else 0), -6.5, z)))
        ms.append(cyl(0.45, 0.45, 16, 6, (60, 60, 60)).xf(M(trans(-120, -6.5, z), rotz(math.pi / 2))))
    ms.append(box(4, 11, 0.6, (40, 40, 40)).xf(trans(-139, -10.5, 0)))
    if gash:  # flanc tribord arrière enfoncé (collision Hawke) : trou + tôles tordues
        ms.append(box(7, 6, 0.4, (10, 8, 8)).xf(trans(-92, -1.5, 13.9)))
        ms.append(box(5, 3, 0.4, (10, 8, 8)).xf(trans(-92, -5.0, 13.6)))
        rr = np.random.default_rng(12)
        for i in range(9):
            a = i / 9 * 2 * math.pi
            px, py = -92 + math.cos(a) * 3.6, 1.5 + math.sin(a) * 3.0
            ms.append(box(1.6, 1.2, 0.12, (45, 45, 50), 'metal').xf(M(trans(px, py, 14.1), rotz(a), rotx(rr.uniform(-0.7, -0.2)))))
    if lights > 0:
        for x in np.arange(-110, 120, 12):
            ms.append(box(0.4, 0.4, 0.4, (255, 230, 160), emis=1.0).xf(trans(x, LINER_DECK + 1.2, 13.0)))
            ms.append(box(0.4, 0.4, 0.4, (255, 230, 160), emis=1.0).xf(trans(x, LINER_DECK + 1.2, -13.0)))
    return merge(ms)


def funnel_smoke(m_world, t, cam, n=4, col=(70, 66, 62), alpha=0.7):
    """fumée des 3 cheminées actives, m_world = matrice du navire"""
    ms = []
    for i, fx in enumerate(FUNNEL_X[:3]):
        tip = (m_world @ np.array([fx - 2.2, LINER_DECK + 8.5 + 21.5, 0, 1]))[:3]
        ms.append(smoke_sprites(tip, t + i, cam, n=n, size=6, rise=18, seed=40 + i, col=col, drift=(-1.4, 0, 0.2), alpha=alpha))
    return merge(ms)


def lifeboat_mesh(L=8.5, B=2.4, H=1.1, empty=False, col=(245, 245, 240)):
    """canot en bois, proue vers +x, plat-bord à y=H/2"""
    st = [(-L / 2, B * 0.32, B * 0.18), (-L / 2 + 0.6, B / 2, B * 0.32), (L / 2 - 1.4, B / 2, B * 0.32), (L / 2, 0.08, 0.05)]
    tris, uvs = [], []
    y0, y1 = -H / 2, H / 2
    for i in range(len(st) - 1):
        xa, wa, ba = st[i]
        xb, wb, bb = st[i + 1]
        for s in (-1, 1):
            p = [(xa, y0, s * ba), (xb, y0, s * bb), (xb, y1, s * wb), (xa, y1, s * wa)]
            tris += [[p[0], p[1], p[2]], [p[0], p[2], p[3]]]
            uvs += [[(0, 1), (1, 1), (1, 0)], [(0, 1), (1, 0), (0, 0)]]
    ms = [Mesh(tris, C(col), uvs, TEXB['planks_white'])]
    ms.append(quad((-L / 2, y0, -st[0][2]), (-L / 2, y0, st[0][2]), (-L / 2, y1, st[0][1]), (-L / 2, y1, -st[0][1]), col))
    # fond intérieur et bancs
    ms.append(box(L - 1.6, 0.05, B * 0.62, (150, 115, 75), 'planks').xf(trans(-0.4, y0 + 0.25, 0)))
    if not empty:
        for x in np.linspace(-L / 2 + 1.2, L / 2 - 2.0, 4):
            ms.append(box(0.3, 0.06, B * 0.9, (150, 115, 75)).xf(trans(x, y0 + 0.65, 0)))
    ms.append(box(L - 0.4, 0.08, 0.1, (110, 80, 50)).xf(trans(-0.2, y1, B / 2 - 0.04)))
    ms.append(box(L - 0.4, 0.08, 0.1, (110, 80, 50)).xf(trans(-0.2, y1, -B / 2 + 0.04)))
    if empty:
        ms.append(box(L - 1.2, 0.05, B * 0.95, (235, 235, 228)).xf(trans(-0.4, y1, 0)))   # bâche
    return merge(ms)


def oar(L=3.2):
    return merge([cyl(0.035, 0.035, L, 5, (170, 130, 80)), box(0.14, 0.7, 0.03, (170, 130, 80)).xf(trans(0, -0.05, 0))])


def hawke(t=0.0):
    """HMS Hawke : croiseur gris à éperon, proue vers +x"""
    st = [(-50, 5.5, 3.5), (-45, 8.5, 6.5), (35, 8.5, 6.5), (46, 4.0, 2.5), (52, 0.6, 1.5), (55, 0.3, 0.8)]
    ms = [_hull_bands(st, [(-7.0, 1.0), (1.0, 5.5)], lambda b: 'hull_grey', ts=3.0, deck_tex='planks_grey', deck_col=(170, 170, 170))]
    ms.append(box(30, 3.0, 9, (140, 146, 150), 'hull_grey', ts=2.0).xf(trans(5, 5.5, 0)))
    ms.append(box(8, 3.0, 7, (150, 156, 160), 'hull_grey').xf(trans(24, 8.5, 0)))
    for fx in (8, -2):
        ms.append(cyl(1.8, 1.8, 11, 10, (125, 130, 135)).xf(trans(fx, 8.5, 0)))
        ms.append(cyl(1.85, 1.85, 1.2, 10, (30, 30, 30)).xf(trans(fx, 18.3, 0)))
    for mx, mh in ((30, 26), (-30, 22)):
        ms.append(cyl(0.3, 0.15, mh, 6, (110, 100, 80)).xf(trans(mx, 5.5, 0)))
    for gx in (40, -40):
        ms.append(cyl(1.5, 1.5, 1.2, 10, (130, 135, 140)).xf(trans(gx, 5.5, 0)))
        ms.append(cyl(0.18, 0.18, 5, 6, (60, 60, 60)).xf(M(trans(gx, 6.3, 0), rotz(-math.pi / 2 * (1 if gx > 0 else -1)))))
    # éperon (sous la flottaison)
    ms.append(frustum(4.0, 3.0, 0.4, 0.4, 7.0, (100, 104, 110), 'hull_grey').xf(M(trans(48, -3.5, 0), roty(math.pi / 2))))
    return merge(ms)


def sea(t=0.0, tex='sea_night', size=3000, y=0.0, ts=12.0, cx=0.0, cz=0.0):
    m = grid(cx - size, cz - size, cx + size, cz + size, 8, 8, lambda x, z: y, (255, 255, 255), tex, ts)
    m.uv = m.uv + np.array([t * 0.03, t * 0.015])
    return m


def stars(n=260, r=1500, seed=3):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        a, e = rr.uniform(0, 2 * math.pi), rr.uniform(0.05, 1.2)
        p = np.array([math.cos(a) * math.cos(e), math.sin(e), math.sin(a) * math.cos(e)]) * r
        s = rr.uniform(2.0, 4.5)
        ms.append(box(s, s, s, (255, 250, 235) if i % 5 else (200, 220, 255), emis=1.0).xf(trans(p)))
    return merge(ms)


STARS = stars()


def iceberg(seed=1):
    ms = [rock(1.0, seed, (255, 255, 255), 'ice').xf(scale(26, 22, 20))]
    ms.append(rock(1.0, seed + 1, (255, 255, 255), 'ice').xf(M(trans(8, 10, -4), scale(14, 20, 12))))
    ms.append(rock(1.0, seed + 2, (255, 255, 255), 'ice').xf(M(trans(-10, 4, 6), scale(12, 10, 10))))
    return merge(ms)


def ice_floes(n=30, seed=4, area=200):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        x, z = rr.uniform(-area, area), rr.uniform(-area, area)
        s = rr.uniform(1.0, 4.0)
        ms.append(rock(1.0, i, (255, 255, 255), 'ice').xf(M(trans(x, -0.2, z), scale(s, s * 0.4, s * 1.2))))
    return merge(ms)


def flare(pos, age, cam):
    """fusée de détresse blanche qui éclate en étoiles"""
    if age < 0:
        return Mesh()
    p = np.asarray(pos, float)
    ms = []
    if age < 0.7:
        h = age / 0.7 * 60
        ms.append(strip([p, p + np.array([0, h, 0])], 0.6, cam, (255, 240, 200), emis=1.0, alpha=0.6))
        ms.append(billboard(p + np.array([0, h, 0]), 3, 3, cam, (255, 255, 255), 'spark', emis=1.0))
    else:
        k = age - 0.7
        c = p + np.array([0, 60 - k * 3, 0])
        rr = np.random.default_rng(9)
        for i in range(14):
            d = rr.normal(size=3)
            d /= np.linalg.norm(d)
            q = c + d * k * 14 + np.array([0, -4.9 * k * k, 0])
            ms.append(billboard(q, 2.2, 2.2, cam, (255, 255, 240), 'spark', emis=1.0, alpha=max(0, 1 - k * 0.4)))
    return merge(ms)


def mine(t=0.0):
    ms = [sphere(0.55, 8, 6, (40, 40, 38), 'metal')]
    for k in range(8):
        a = k / 8 * 2 * math.pi
        e = 0.6 if k % 2 else -0.3
        d = np.array([math.cos(a) * math.cos(e), math.sin(e), math.sin(a) * math.cos(e)])
        ms.append(rod(d * 0.5, d * 0.75, 0.05, (60, 60, 55), n=4))
    for i in range(8):
        ms.append(box(0.05, 0.12, 0.08, (70, 70, 65)).xf(trans(0, -0.6 - i * 0.12, 0)))
    return merge(ms)


def splash_fx(pos, age, cam, size=3.0, seed=0, col=(235, 245, 250)):
    if age < 0 or age > 1.6:
        return Mesh()
    rr = np.random.default_rng(seed)
    ms = []
    p = np.asarray(pos, float)
    for i in range(10):
        v = rr.normal(size=3) * np.array([1, 0.3, 1]) * size * 0.6 + np.array([0, size * 2.2, 0])
        q = p + v * age + np.array([0, -9.8 * age * age, 0])
        if q[1] < p[1] - 0.2:
            continue
        s = size * 0.5 * (1 - age / 1.6) + 0.2
        ms.append(billboard(q, s, s, cam, col, 'puff', emis=0.4, alpha=0.85 * (1 - age / 1.6)))
    return merge(ms)


def water_column(pos, age, cam, h=60.0, seed=0):
    """gerbe d'eau géante (mine)"""
    if age < 0 or age > 4:
        return Mesh()
    rr = np.random.default_rng(seed)
    ms = []
    p = np.asarray(pos, float)
    k = min(1.0, age / 0.8)
    for i in range(18):
        o = rr.normal(size=3) * np.array([6, 0, 6])
        yy = h * k * rr.uniform(0.3, 1.0) - max(0, age - 1.5) * 12
        if yy < 0:
            continue
        s = 10 * (0.6 + rr.random() * 0.6) * (0.6 + 0.4 * k)
        ms.append(billboard(p + o + np.array([0, yy, 0]), s, s, cam, (230, 238, 240), 'puff', emis=0.4, alpha=0.9 * max(0, 1 - age / 4)))
    return merge(ms)


def bubbles(base, t, cam, n=14, seed=0, area=1.0, rise=2.5):
    rr = np.random.default_rng(seed)
    ms = []
    for i in range(n):
        ph = (t * 0.8 + rr.random()) % 1.0
        p = np.asarray(base, float) + np.array([rr.uniform(-area, area) + math.sin(t * 5 + i) * 0.05, ph * rise, rr.uniform(-area, area)])
        s = rr.uniform(0.04, 0.12)
        ms.append(billboard(p, s, s, cam, (200, 235, 245), 'puff', emis=0.6, alpha=0.7))
    return merge(ms)


# ---------------------------------------------------------------- décors rapprochés
def deck_set(kind='olympic', night=False, x0=-25, x1=25, sea_y=-22.0, crowd=None):
    """pont-promenade du pont des embarcations : planches, roof à gauche (z<0), bastingage à droite (z=+4)"""
    ms = [box(x1 - x0, 0.2, 9, (255, 255, 255), 'planks', ts=0.8).xf(trans((x0 + x1) / 2, -0.2, 0))]
    sw = 'superwin_lit' if night else 'superwin'
    ms.append(box(x1 - x0, 3.0, 0.3, (255, 255, 255), sw, ts=3.0).xf(trans((x0 + x1) / 2, 0, -4.4)))
    ms.append(box(x1 - x0, 0.3, 1.2, (240, 238, 230)).xf(trans((x0 + x1) / 2, 3.0, -3.9)))
    # bastingage
    ms.append(box(x1 - x0, 0.12, 0.18, (150, 110, 70), 'wood_dark' if 'wood_dark' in TEXB else 0).xf(trans((x0 + x1) / 2, 1.05, 4.2)))
    for x in np.arange(x0, x1, 1.2):
        ms.append(box(0.06, 1.05, 0.06, (240, 240, 235)).xf(trans(x, 0, 4.2)))
    for y in (0.35, 0.7):
        ms.append(box(x1 - x0, 0.04, 0.04, (240, 240, 235)).xf(trans((x0 + x1) / 2, y, 4.2)))
    # canots suspendus aux bossoirs au-dessus du bord
    for x in np.arange(x0 + 4, x1 - 2, 9.5):
        ms.append(lifeboat_mesh(8.0, 2.2, 1.0, empty=True).xf(trans(x, 2.3, 2.6)))
        for dx in (-3.4, 3.4):
            ms.append(rod((x + dx, 0, 3.6), (x + dx, 3.6, 3.4), 0.08, (235, 235, 230), n=4))
            ms.append(rod((x + dx, 3.6, 3.4), (x + dx * 0.98, 3.9, 2.6), 0.08, (235, 235, 230), n=4))
            ms.append(rod((x + dx * 0.98, 3.9, 2.6), (x + dx * 0.98, 2.9, 2.6), 0.02, (60, 50, 40), n=3))
    # base d'une cheminée derrière le roof
    ms.append(cyl(3.3, 3.3, 14, 12, (205, 145, 60)).xf(trans(4, 3.2, -9)))
    # coque qui plonge vers la mer
    ms.append(box(x1 - x0, 22, 0.3, (255, 255, 255), 'ports_lit' if night else ('ports_white' if kind == 'britannic' else 'ports'), ts=4.0).xf(trans((x0 + x1) / 2, sea_y, 4.6)))
    if night:
        for x in np.arange(x0 + 2, x1, 8):
            ms.append(box(0.3, 0.4, 0.3, (255, 230, 160), emis=1.0).xf(trans(x, 2.4, -4.2)))
    return merge(ms)


def corridor():
    """coursive intérieure (lambris blanc, portes, lampes) pour la collision"""
    ms = [box(14, 0.05, 2.4, (120, 30, 35), 'red_cloth' if 'red_cloth' in TEXB else 0).xf(trans(0, -0.05, 0))]
    for s in (-1, 1):
        ms.append(box(14, 2.6, 0.1, (240, 236, 222), 'planks_white', ts=0.8, faces='f' if s < 0 else 'b').xf(trans(0, 0, s * 1.25)))
    ms.append(box(14, 0.1, 2.6, (245, 242, 232)).xf(trans(0, 2.6, 0)))
    for x in (-4.5, -0.5, 3.5):
        ms.append(box(0.9, 2.0, 0.05, (255, 255, 255), 'door').xf(trans(x, 0, -1.19)))
        ms.append(box(0.3, 0.2, 0.15, (255, 230, 160), emis=0.9).xf(trans(x + 1.6, 2.35, 1.15)))
    return merge(ms)


tex_noise('red_cloth', (150, 30, 35), (175, 40, 42), seed=215, octaves=1) if 'red_cloth' not in TEXB else None


def tray(cups=3):
    ms = [box(0.42, 0.02, 0.3, (200, 200, 205), 'metal')]
    for i in range(cups):
        ms.append(cyl(0.035, 0.03, 0.06, 6, (250, 250, 250)).xf(trans(-0.12 + i * 0.12, 0.02, 0)))
    return merge(ms)


def suitcase():
    return merge([box(0.5, 0.35, 0.16, (110, 70, 40)), box(0.12, 0.04, 0.03, (40, 30, 20)).xf(trans(0, 0.36, 0))])


def quay_set():
    """quai de Southampton : pavés, grue, bollards, entrepôt, passerelle vers le paquebot (z>0)"""
    ms = [box(400, 1.5, 40, (255, 255, 255), 'stone_block', ts=1.4).xf(trans(0, -1.5, -20))]
    ms.append(box(80, 12, 18, (150, 90, 70), 'brick', ts=2.0).xf(trans(-30, 0, -32)))
    ms.append(box(84, 1.0, 22, (120, 120, 118), 'roof_tin', ts=2).xf(trans(-30, 12, -32)))
    for x in np.arange(-120, 120, 14):
        ms.append(cyl(0.3, 0.25, 0.7, 6, (40, 40, 40)).xf(trans(x, 0, -1.0)))
    # grue
    ms.append(box(1.2, 18, 1.2, (100, 60, 40), 'rust').xf(trans(30, 0, -8)))
    ms.append(box(16, 1.0, 1.0, (100, 60, 40), 'rust').xf(M(trans(30, 18, -8), roty(0.6), trans(5, 0, 0))))
    # caisses
    rr = np.random.default_rng(2)
    for i in range(10):
        ms.append(box(1.2, 1.0, 1.0, (150, 115, 75), 'planks').xf(M(trans(rr.uniform(-60, 60), 0, rr.uniform(-12, -4)), roty(rr.random()))))
    return merge(ms)


def gangway(L=14, h=6.0):
    """passerelle inclinée de (0,0,0) quai à (0,h,L) coque"""
    a = math.atan2(h, L)
    lg = math.hypot(L, h)
    m = M(rotx(-a))
    ms = [box(1.6, 0.12, lg, (150, 115, 75), 'planks', ts=0.6).xf(M(m, trans(0, 0, lg / 2)))]
    for s in (-1, 1):
        ms.append(box(0.05, 1.0, lg, (230, 230, 225), alpha=0.6).xf(M(m, trans(s * 0.8, 0.1, lg / 2))))
    return merge(ms)


def tug(t=0.0):
    st = [(-12, 3.5, 2.0), (6, 3.5, 2.2), (12, 0.4, 0.3)]
    ms = [_hull_bands(st, [(-3, 2.0)], lambda b: 'hull_black', ts=2.0)]
    ms.append(box(7, 2.5, 4.5, (235, 230, 220), 'superwin', ts=2.0).xf(trans(0, 2.0, 0)))
    ms.append(cyl(0.8, 0.8, 4, 8, (200, 60, 40)).xf(trans(-2, 4.5, 0)))
    return merge(ms)


def cottage(storm_k=0.0):
    """salon de Violet à la retraite (Suffolk) : papier peint, fenêtre sous l'orage, fauteuil, guéridon"""
    ms = [box(6, 0.05, 5, (110, 75, 50), 'planks', ts=0.7).xf(trans(0, -0.05, 0))]
    ms.append(box(2.6, 0.02, 1.8, (130, 40, 45), 'rug' if 'rug' in TEXB else 0).xf(trans(0.3, 0.0, 0.4)))
    # murs avec ouverture de fenêtre (mur du fond z=-2.5)
    ms.append(box(6, 2.8, 0.12, (255, 255, 255), 'wallpaper', ts=1.0, faces='f').xf(trans(0, 0, -2.5)) if False else Mesh())
    wx0, wx1, wy0, wy1 = 0.6, 2.2, 1.0, 2.3
    for (xa, xb, ya, yb) in ((-3, wx0, 0, 2.8), (wx1, 3, 0, 2.8), (wx0, wx1, 0, wy0), (wx0, wx1, wy1, 2.8)):
        ms.append(box(xb - xa, yb - ya, 0.12, (255, 255, 255), 'wallpaper', ts=1.0).xf(trans((xa + xb) / 2, ya, -2.5)))
    ms.append(box(0.12, 2.8, 5, (255, 255, 255), 'wallpaper', ts=1.0).xf(trans(-3, 0, 0)))
    ms.append(box(6, 0.1, 5, (235, 230, 215)).xf(trans(0, 2.8, 0)))
    # cadre et croisillons de la fenêtre, vitre
    cx, cy = (wx0 + wx1) / 2, (wy0 + wy1) / 2
    for (w, h, x, y) in ((wx1 - wx0 + 0.16, 0.08, cx, wy0 - 0.08), (wx1 - wx0 + 0.16, 0.08, cx, wy1), (0.08, wy1 - wy0, wx0 - 0.04, wy0),
                         (0.08, wy1 - wy0, wx1 + 0.04, wy0), (0.05, wy1 - wy0, cx, wy0), (wx1 - wx0, 0.05, cx, cy)):
        ms.append(box(w, h, 0.1, (235, 232, 222)).xf(trans(x, y, -2.44)))
    ms.append(box(wx1 - wx0 + 0.3, 0.06, 0.25, (235, 232, 222)).xf(trans(cx, wy0 - 0.1, -2.35)))
    ms.append(box(wx1 - wx0, wy1 - wy0, 0.01, (120, 140, 170), alpha=0.25).xf(trans(cx, wy0, -2.46)))
    # dehors : nuit (plan sombre + silhouette d'arbre)
    ms.append(box(12, 8, 0.1, (25, 30, 45)).xf(trans(1.5, -2, -8)))
    ms.append(cyl(0.25, 0.15, 5, 5, (15, 15, 20)).xf(trans(2.5, -1, -6)))
    ms.append(sphere(1.6, 6, 4, (15, 18, 22)).xf(trans(2.5, 4.0, -6)))
    # rideaux
    for x in (wx0 - 0.25, wx1 + 0.25):
        ms.append(box(0.35, 1.8, 0.08, (140, 50, 55), 'red_cloth').xf(trans(x, 0.7, -2.36)))
    # fauteuil (face à +z, à gauche)
    ac = (120, 70, 50)
    ms.append(box(0.9, 0.42, 0.8, ac, 'cloth').xf(trans(-1.2, 0, -0.3)))
    ms.append(box(0.9, 0.7, 0.18, ac, 'cloth').xf(trans(-1.2, 0.42, -0.65)))
    for s in (-1, 1):
        ms.append(box(0.16, 0.25, 0.8, ac, 'cloth').xf(trans(-1.2 + s * 0.45, 0.42, -0.3)))
    # guéridon avec lampe
    ms.append(cyl(0.3, 0.3, 0.04, 10, (90, 60, 35)).xf(trans(-0.2, 0.68, -0.6)))
    ms.append(cyl(0.04, 0.04, 0.68, 6, (90, 60, 35)).xf(trans(-0.2, 0, -0.6)))
    ms.append(cyl(0.18, 0.12, 0.08, 8, (90, 60, 35)).xf(trans(-0.2, 0, -0.6)))
    ms.append(cyl(0.05, 0.05, 0.3, 6, (180, 160, 110)).xf(trans(-0.35, 0.72, -0.75)))
    ms.append(cyl(0.18, 0.1, 0.18, 8, (240, 220, 170), emis=0.8).xf(trans(-0.35, 1.02, -0.75)))
    # tableau d'un paquebot + photo encadrée
    ms.append(box(0.7, 0.5, 0.04, (255, 255, 255), 'ship_painting').xf(trans(-1.4, 1.5, -2.42)))
    ms.append(box(0.04, 0.3, 0.24, (255, 255, 255), 'photo_frame').xf(trans(-2.92, 1.6, 0.5)))
    # buffet
    ms.append(box(1.4, 0.9, 0.5, (100, 65, 40), 'planks_v').xf(trans(-2.0, 0, 1.5)))
    return merge(ms)


PHONE_POS = np.array([-0.05, 0.70, -0.5])


def phone(lift=0.0, ring=0.0, t=0.0, handset=True):
    """téléphone noir des années 50 ; lift 0..1 = combiné décroché (géré à part si handset=False)"""
    sh = math.sin(t * 60) * 0.01 * ring
    ms = [frustum(0.24, 0.12, 0.2, 0.1, 0.22, (25, 25, 25)).xf(M(trans(sh, 0.06, -0.11))),
          box(0.22, 0.03, 0.24, (25, 25, 25)).xf(trans(sh, 0.0, 0.0))]
    ms.append(cyl(0.07, 0.07, 0.015, 10, (200, 200, 190)).xf(M(trans(sh, 0.1, 0.1), rotx(0.6))))
    ms.append(cyl(0.05, 0.05, 0.02, 10, (25, 25, 25)).xf(M(trans(sh, 0.1, 0.1), rotx(0.6), trans(0, 0.01, 0))))
    for s in (-1, 1):
        ms.append(box(0.03, 0.05, 0.03, (25, 25, 25)).xf(trans(sh + s * 0.09, 0.12, -0.02)))
    if handset and lift <= 0:
        ms.append(handset_mesh().xf(M(trans(sh, 0.16 + ring * 0.01 * math.sin(t * 50), -0.02), roty(math.pi / 2))))
    return merge(ms)


def handset_mesh():
    """combiné le long de x (écouteur -x, micro +x)"""
    return merge([box(0.24, 0.035, 0.05, (25, 25, 25)),
                  box(0.07, 0.05, 0.07, (25, 25, 25)).xf(trans(-0.12, -0.02, 0)),
                  box(0.07, 0.05, 0.07, (25, 25, 25)).xf(trans(0.12, -0.02, 0))])


def cemetery():
    ms = [grid(-30, -30, 30, 30, 6, 6, None, (255, 255, 255), 'grass_night', 3.0)]
    rr = np.random.default_rng(5)
    for i in range(16):
        x, z = rr.uniform(-12, 12), rr.uniform(-14, -2)
        if abs(x) < 1.5 and z > -6:
            continue
        h = rr.uniform(0.6, 1.2)
        st = merge([box(0.6, h, 0.15, (150, 150, 145), 'rock'), cyl(0.3, 0.3, 0.15, 8, (150, 150, 145), 'rock').xf(M(trans(0, h, -0.075), rotx(math.pi / 2)))])
        ms.append(st.xf(M(trans(x, 0, z), roty(rr.uniform(-0.2, 0.2)), rotz(rr.uniform(-0.08, 0.08)))))
    # petite tombe au centre (croix)
    ms.append(box(0.08, 0.7, 0.08, (170, 170, 165), 'rock').xf(trans(0, 0, -3)))
    ms.append(box(0.4, 0.08, 0.08, (170, 170, 165), 'rock').xf(trans(0, 0.5, -3)))
    ms.append(box(0.5, 0.12, 0.8, (120, 120, 115), 'rock').xf(trans(0, 0, -2.6)))
    # arbre mort et grille
    ms.append(cyl(0.25, 0.1, 5, 5, (40, 35, 32), 'bark').xf(trans(-5, 0, -8)))
    for a, l in ((0.6, 2.5), (-0.7, 2.0), (0.2, 1.6)):
        ms.append(cyl(0.08, 0.03, l, 4, (40, 35, 32)).xf(M(trans(-5, 3.5, -8), rotz(a))))
    for x in np.arange(-15, 15, 0.4):
        ms.append(box(0.04, 1.4, 0.04, (25, 25, 28)).xf(trans(x, 0, -15)))
    return merge(ms)


ENV_NIGHT_SEA = Env(sky_top=(4, 6, 16), sky_hor=(18, 24, 44), fog=(14, 18, 34), fog_near=200, fog_far=2600,
                    light=(0.3, 0.6, 0.5), amb=0.42, light_col=(140, 160, 210))
ENV_DAY_SEA = Env(sky_top=(80, 130, 200), sky_hor=(205, 215, 220), fog=(190, 205, 215), fog_near=250, fog_far=2600,
                  light=(-0.4, 0.75, 0.5), amb=0.55, light_col=(255, 245, 228))
ENV_GREY_SEA = Env(sky_top=(120, 130, 145), sky_hor=(185, 190, 195), fog=(170, 175, 182), fog_near=200, fog_far=2000,
                   light=(-0.4, 0.75, 0.5), amb=0.6, light_col=(240, 240, 240))
ENV_AEGEAN = Env(sky_top=(60, 120, 205), sky_hor=(215, 225, 230), fog=(200, 215, 225), fog_near=300, fog_far=3000,
                 light=(0.5, 0.75, 0.4), amb=0.55, light_col=(255, 248, 230))
ENV_DAWN = Env(sky_top=(50, 60, 100), sky_hor=(235, 160, 120), fog=(190, 150, 140), fog_near=150, fog_far=2200,
               light=(-0.8, 0.25, 0.4), amb=0.5, light_col=(255, 190, 150))
ENV_UNDER = Env(sky_top=(60, 150, 170), sky_hor=(12, 55, 75), fog=(8, 45, 62), fog_near=1, fog_far=28,
                light=(0.2, 1.0, 0.2), amb=0.6, light_col=(150, 220, 230))
ENV_ROOM = Env(sky_top=(30, 25, 22), sky_hor=(30, 25, 22), fog=(20, 16, 14), fog_near=6, fog_far=30,
               light=(0.4, 0.7, 0.6), amb=0.5, light_col=(255, 220, 170))
ENV_STORM = Env(sky_top=(14, 16, 26), sky_hor=(40, 44, 58), fog=(30, 34, 46), fog_near=8, fog_far=60,
                light=(-0.3, 0.8, 0.4), amb=0.45, light_col=(150, 160, 190))
ENV_CORR = Env(sky_top=(40, 30, 25), sky_hor=(40, 30, 25), fog=(30, 22, 18), fog_near=6, fog_far=26,
               light=(0.3, 0.9, 0.3), amb=0.55, light_col=(255, 225, 170))
