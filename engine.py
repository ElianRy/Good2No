"""Good2No - moteur 3D logiciel style PS1.
Rendu interne 270x480, z-buffer, textures basse résolution, éclairage plat,
brouillard, transparence en trame, quantification 15 bits + tramage Bayer,
agrandissement x4 au plus proche -> 1080x1920.
"""
import math
import numpy as np
from numba import njit

W, H = 270, 480
UPS = 4
TEX = 32  # taille des textures

BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) + 0.5) / 16.0


# ---------------------------------------------------------------- maths
def rotx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]], np.float64)


def roty(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]], np.float64)


def rotz(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float64)


def trans(x, y=0.0, z=0.0):
    if hasattr(x, '__len__'):
        x, y, z = x
    m = np.eye(4)
    m[:3, 3] = (x, y, z)
    return m


def scale(x, y=None, z=None):
    if y is None:
        y = z = x
    return np.diag([x, y, z, 1.0])


def M(*ms):
    r = np.eye(4)
    for m in ms:
        r = r @ m
    return r


# ---------------------------------------------------------------- textures
class TexBank:
    def __init__(self):
        self.list = [np.full((TEX, TEX, 3), 255, np.uint8)]  # 0 = blanc uni
        self.names = {'flat': 0}

    def add(self, name, img):
        img = np.asarray(img, np.uint8)
        if img.shape[:2] != (TEX, TEX):
            from PIL import Image
            img = np.asarray(Image.fromarray(img).resize((TEX, TEX), Image.NEAREST))
        if name in self.names:
            self.list[self.names[name]] = img
        else:
            self.names[name] = len(self.list)
            self.list.append(img)
        self._arr = None
        return self.names[name]

    def __getitem__(self, name):
        return self.names[name]

    def __contains__(self, name):
        return name in self.names

    def array(self):
        if getattr(self, '_arr', None) is None:
            self._arr = np.ascontiguousarray(np.stack(self.list))
        return self._arr


TEXB = TexBank()


# ---------------------------------------------------------------- maillages
class Mesh:
    """tris (N,3,3) float, col (N,3) 0..1, uv (N,3,2), tex (N,), alpha (N,), emis (N,)"""
    __slots__ = ('tris', 'col', 'uv', 'tex', 'alpha', 'emis')

    def __init__(self, tris=None, col=None, uv=None, tex=None, alpha=None, emis=None):
        if tris is None:
            tris = np.zeros((0, 3, 3))
        tris = np.asarray(tris, np.float64).reshape(-1, 3, 3)
        n = len(tris)
        self.tris = tris
        self.col = np.zeros((n, 3)) + (np.ones(3) if col is None else np.asarray(col, np.float64))
        self.uv = np.zeros((n, 3, 2)) if uv is None else np.asarray(uv, np.float64).reshape(n, 3, 2)
        self.tex = np.zeros(n, np.int32) + (0 if tex is None else np.asarray(tex))
        self.alpha = np.ones(n) * (1.0 if alpha is None else np.asarray(alpha, np.float64))
        self.emis = np.zeros(n) + (0.0 if emis is None else np.asarray(emis, np.float64))

    def __len__(self):
        return len(self.tris)

    def copy(self):
        return Mesh(self.tris.copy(), self.col.copy(), self.uv.copy(), self.tex.copy(), self.alpha.copy(), self.emis.copy())

    def xf(self, m):
        m = np.asarray(m)
        t = self.tris @ m[:3, :3].T + m[:3, 3]
        return Mesh(t, self.col, self.uv, self.tex, self.alpha, self.emis)

    def tint(self, c):
        o = self.copy()
        o.col = o.col * np.asarray(c, np.float64)
        return o

    def set(self, col=None, tex=None, alpha=None, emis=None):
        o = self.copy()
        if col is not None:
            o.col[:] = col
        if tex is not None:
            o.tex[:] = tex
        if alpha is not None:
            o.alpha[:] = alpha
        if emis is not None:
            o.emis[:] = emis
        return o


def merge(meshes):
    ms = [m for m in meshes if m is not None and len(m)]
    if not ms:
        return Mesh()
    return Mesh(np.concatenate([m.tris for m in ms]), np.concatenate([m.col for m in ms]),
                np.concatenate([m.uv for m in ms]), np.concatenate([m.tex for m in ms]),
                np.concatenate([m.alpha for m in ms]), np.concatenate([m.emis for m in ms]))


def C(c):
    """couleur 0-255 -> 0-1"""
    c = np.asarray(c, np.float64)
    return c / 255.0 if c.max() > 1.0 else c


def _quad(p0, p1, p2, p3, uvs=((0, 0), (1, 0), (1, 1), (0, 1))):
    return [[p0, p1, p2], [p0, p2, p3]], [[uvs[0], uvs[1], uvs[2]], [uvs[0], uvs[2], uvs[3]]]


def quad(p0, p1, p2, p3, col=(1, 1, 1), tex=0, uvs=((0, 0), (1, 0), (1, 1), (0, 1)), **kw):
    t, u = _quad(p0, p1, p2, p3, uvs)
    return Mesh(t, C(col), u, TEXB[tex] if isinstance(tex, str) else tex, **kw)


def box(sx, sy, sz, col=(1, 1, 1), tex=0, ts=None, top_tex=None, top_col=None, faces='all', **kw):
    """boîte centrée sur l'origine en x,z, base en y=0. ts = taille d'une répétition de texture (m)"""
    x0, x1, y0, y1, z0, z1 = -sx / 2, sx / 2, 0, sy, -sz / 2, sz / 2
    tid = TEXB[tex] if isinstance(tex, str) else tex
    ttid = tid if top_tex is None else (TEXB[top_tex] if isinstance(top_tex, str) else top_tex)

    def uvr(a, b):
        if ts is None:
            return ((0, 1), (1, 1), (1, 0), (0, 0))
        return ((0, b / ts), (a / ts, b / ts), (a / ts, 0), (0, 0))

    F = {
        'f': ((x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1), uvr(sx, sy)),   # +z avant
        'b': ((x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0), uvr(sx, sy)),   # -z
        'r': ((x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, y1, z1), uvr(sz, sy)),   # +x
        'l': ((x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0), uvr(sz, sy)),   # -x
        'u': ((x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0), uvr(sx, sz)),   # haut
        'd': ((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1), uvr(sx, sz)),   # bas
    }
    ms = []
    for k, (a, b, c, d, u) in F.items():
        if faces != 'all' and k not in faces:
            continue
        if k == 'u':
            ms.append(quad(a, b, c, d, C(top_col if top_col is not None else col), ttid, u, **kw))
        else:
            ms.append(quad(a, b, c, d, C(col), tid, u, **kw))
    return merge(ms)


def cyl(r0, r1, h, n=8, col=(1, 1, 1), tex=0, caps=True, ts=None, cap_col=None, **kw):
    """cylindre / cône tronqué vertical, base y=0"""
    tid = TEXB[tex] if isinstance(tex, str) else tex
    tris, uvs = [], []
    circ = 2 * math.pi * max(r0, r1)
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        p0 = (r0 * math.cos(a0), 0, r0 * math.sin(a0))
        p1 = (r0 * math.cos(a1), 0, r0 * math.sin(a1))
        p2 = (r1 * math.cos(a1), h, r1 * math.sin(a1))
        p3 = (r1 * math.cos(a0), h, r1 * math.sin(a0))
        if ts:
            u0, u1, v = i / n * circ / ts, (i + 1) / n * circ / ts, h / ts
        else:
            u0, u1, v = i / n, (i + 1) / n, 1
        t, u = _quad(p0, p1, p2, p3, ((u0, v), (u1, v), (u1, 0), (u0, 0)))
        tris += t
        uvs += u
    m = Mesh(tris, C(col), uvs, tid, **kw)
    if caps:
        ct, cu = [], []
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            if r1 > 0:
                ct.append([(0, h, 0), (r1 * math.cos(a1), h, r1 * math.sin(a1)), (r1 * math.cos(a0), h, r1 * math.sin(a0))])
                cu.append([(.5, .5), (.5 + .5 * math.cos(a1), .5 + .5 * math.sin(a1)), (.5 + .5 * math.cos(a0), .5 + .5 * math.sin(a0))])
            if r0 > 0:
                ct.append([(0, 0, 0), (r0 * math.cos(a0), 0, r0 * math.sin(a0)), (r0 * math.cos(a1), 0, r0 * math.sin(a1))])
                cu.append([(.5, .5), (.5 + .5 * math.cos(a0), .5 + .5 * math.sin(a0)), (.5 + .5 * math.cos(a1), .5 + .5 * math.sin(a1))])
        if ct:
            m = merge([m, Mesh(ct, C(cap_col if cap_col is not None else col), cu, tid, **kw)])
    return m


def sphere(r, nu=8, nv=5, col=(1, 1, 1), tex=0, sy=1.0, **kw):
    tid = TEXB[tex] if isinstance(tex, str) else tex
    tris, uvs = [], []
    for j in range(nv):
        v0, v1 = math.pi * j / nv - math.pi / 2, math.pi * (j + 1) / nv - math.pi / 2
        for i in range(nu):
            a0, a1 = 2 * math.pi * i / nu, 2 * math.pi * (i + 1) / nu

            def P(a, v):
                return (r * math.cos(v) * math.cos(a), r * sy * math.sin(v), r * math.cos(v) * math.sin(a))
            p0, p1, p2, p3 = P(a0, v0), P(a1, v0), P(a1, v1), P(a0, v1)
            uv = ((i / nu, 1 - j / nv), ((i + 1) / nu, 1 - j / nv), ((i + 1) / nu, 1 - (j + 1) / nv), (i / nu, 1 - (j + 1) / nv))
            if j == 0:
                tris.append([p0, p2, p3]); uvs.append([uv[0], uv[2], uv[3]])
            elif j == nv - 1:
                tris.append([p0, p1, p2]); uvs.append([uv[0], uv[1], uv[2]])
            else:
                t, u = _quad(p0, p1, p2, p3, uv)
                tris += t; uvs += u
    return Mesh(tris, C(col), uvs, tid, **kw)


def grid(x0, z0, x1, z1, nx, nz, hfun=None, col=(1, 1, 1), tex=0, ts=4.0, colfun=None, **kw):
    """terrain en grille, hfun(x,z)->y, colfun(x,z)->couleur"""
    tid = TEXB[tex] if isinstance(tex, str) else tex
    xs = np.linspace(x0, x1, nx + 1)
    zs = np.linspace(z0, z1, nz + 1)
    X, Z = np.meshgrid(xs, zs)
    Y = np.zeros_like(X) if hfun is None else np.vectorize(hfun)(X, Z)
    tris, uvs, cols = [], [], []
    for j in range(nz):
        for i in range(nx):
            p = [(X[j, i], Y[j, i], Z[j, i]), (X[j, i + 1], Y[j, i + 1], Z[j, i + 1]),
                 (X[j + 1, i + 1], Y[j + 1, i + 1], Z[j + 1, i + 1]), (X[j + 1, i], Y[j + 1, i], Z[j + 1, i])]
            u = [(X[j, i] / ts, Z[j, i] / ts), (X[j, i + 1] / ts, Z[j, i + 1] / ts),
                 (X[j + 1, i + 1] / ts, Z[j + 1, i + 1] / ts), (X[j + 1, i] / ts, Z[j + 1, i] / ts)]
            tris += [[p[0], p[1], p[2]], [p[0], p[2], p[3]]]
            uvs += [[u[0], u[1], u[2]], [u[0], u[2], u[3]]]
            c = C(colfun((X[j, i] + X[j, i + 1]) / 2, (Z[j, i] + Z[j + 1, i]) / 2)) if colfun else C(col)
            cols += [c, c]
    return Mesh(tris, np.array(cols), uvs, tid, **kw)


def billboard(pos, w, h, cam, col=(1, 1, 1), tex=0, emis=1.0, alpha=1.0, rot=0.0, anchor='center'):
    """quad face caméra"""
    f = np.asarray(cam.at, float) - np.asarray(cam.pos, float)
    f /= np.linalg.norm(f) + 1e-9
    r = np.cross(f, (0, 1, 0))
    r /= np.linalg.norm(r) + 1e-9
    u = np.cross(r, f)
    c, s = math.cos(rot), math.sin(rot)
    r, u = r * c + u * s, -r * s + u * c
    p = np.asarray(pos, float)
    if anchor == 'bottom':
        p = p + u * h / 2
    hw, hh = w / 2, h / 2
    return quad(p - r * hw - u * hh, p + r * hw - u * hh, p + r * hw + u * hh, p - r * hw + u * hh,
                col, tex, ((0, 1), (1, 1), (1, 0), (0, 0)), emis=emis, alpha=alpha)


def strip(points, width, cam, col=(1, 1, 1), emis=1.0, alpha=1.0):
    """ruban face caméra le long d'une polyligne (éclairs, fumée...)"""
    pts = np.asarray(points, float)
    cp = np.asarray(cam.pos, float)
    ms = []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        d = b - a
        v = np.cross(d, cp - (a + b) / 2)
        v /= np.linalg.norm(v) + 1e-9
        wa = width[i] if hasattr(width, '__len__') else width
        wb = width[i + 1] if hasattr(width, '__len__') else width
        ms.append(quad(a - v * wa / 2, b - v * wb / 2, b + v * wb / 2, a + v * wa / 2, col, 0, emis=emis, alpha=alpha))
    return merge(ms)


# ---------------------------------------------------------------- caméra
class Cam:
    def __init__(self, pos, at, fov=60.0, roll=0.0):
        self.pos, self.at, self.fov, self.roll = tuple(map(float, pos)), tuple(map(float, at)), fov, roll

    def view(self):
        p = np.asarray(self.pos)
        f = np.asarray(self.at) - p
        f /= np.linalg.norm(f) + 1e-12
        up = np.array([0, 1.0, 0])
        if abs(f[1]) > 0.999:
            up = np.array([0, 0, 1.0])
        r = np.cross(f, up)
        r /= np.linalg.norm(r)
        u = np.cross(r, f)
        if self.roll:
            c, s = math.cos(self.roll), math.sin(self.roll)
            r, u = r * c + u * s, -r * s + u * c
        R = np.stack([r, u, f])
        return R, p


def lerp(a, b, t):
    return a + (b - a) * t


def lerpv(a, b, t):
    return tuple(np.asarray(a, float) + (np.asarray(b, float) - np.asarray(a, float)) * t)


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def cam_lerp(c0, c1, t):
    t = ease(t)
    return Cam(lerpv(c0.pos, c1.pos, t), lerpv(c0.at, c1.at, t), lerp(c0.fov, c1.fov, t), lerp(c0.roll, c1.roll, t))


# ---------------------------------------------------------------- raster numba
@njit(cache=True, fastmath=True)
def _raster(sx, sy, sz, uv, col, tex, alpha, texs, zb, cb, fogc, fog_n, fog_f, bayer, W, H, blend, affine=False):
    n = sx.shape[0]
    TS = texs.shape[1]
    for t in range(n):
        x0, y0, x1, y1, x2, y2 = sx[t, 0], sy[t, 0], sx[t, 1], sy[t, 1], sx[t, 2], sy[t, 2]
        area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if abs(area) < 1e-9:
            continue
        minx = int(max(0.0, math.floor(min(x0, min(x1, x2)))))
        maxx = int(min(W - 1.0, math.ceil(max(x0, max(x1, x2)))))
        miny = int(max(0.0, math.floor(min(y0, min(y1, y2)))))
        maxy = int(min(H - 1.0, math.ceil(max(y0, max(y1, y2)))))
        if minx > maxx or miny > maxy:
            continue
        iz0, iz1, iz2 = 1.0 / sz[t, 0], 1.0 / sz[t, 1], 1.0 / sz[t, 2]
        if affine:   # PS1 : textures non corrigées en perspective (elles « gondolent »)
            u0, v0, u1, v1, u2, v2 = uv[t, 0, 0], uv[t, 0, 1], uv[t, 1, 0], uv[t, 1, 1], uv[t, 2, 0], uv[t, 2, 1]
        else:
            u0, v0 = uv[t, 0, 0] * iz0, uv[t, 0, 1] * iz0
            u1, v1 = uv[t, 1, 0] * iz1, uv[t, 1, 1] * iz1
            u2, v2 = uv[t, 2, 0] * iz2, uv[t, 2, 1] * iz2
        ti = tex[t]
        cr, cg, cbb = col[t, 0], col[t, 1], col[t, 2]
        al = alpha[t]
        inv = 1.0 / area
        for py in range(miny, maxy + 1):
            fy = py + 0.5
            for px in range(minx, maxx + 1):
                fx = px + 0.5
                w0 = ((x1 - fx) * (y2 - fy) - (x2 - fx) * (y1 - fy)) * inv
                w1 = ((x2 - fx) * (y0 - fy) - (x0 - fx) * (y2 - fy)) * inv
                w2 = 1.0 - w0 - w1
                if w0 < -1e-6 or w1 < -1e-6 or w2 < -1e-6:
                    continue
                iz = w0 * iz0 + w1 * iz1 + w2 * iz2
                z = 1.0 / iz
                if z >= zb[py, px]:
                    continue
                if al < 0.999 and not blend:
                    if bayer[py & 3, px & 3] > al:
                        continue
                if ti > 0:
                    zz = 1.0 if affine else z
                    uu = (w0 * u0 + w1 * u1 + w2 * u2) * zz
                    vv = (w0 * v0 + w1 * v1 + w2 * v2) * zz
                    tx = int(math.floor(uu * TS)) % TS
                    ty = int(math.floor(vv * TS)) % TS
                    r = texs[ti, ty, tx, 0] * (1.0 / 255.0) * cr
                    g = texs[ti, ty, tx, 1] * (1.0 / 255.0) * cg
                    b = texs[ti, ty, tx, 2] * (1.0 / 255.0) * cbb
                    if texs[ti, ty, tx, 0] == 255 and texs[ti, ty, tx, 1] == 0 and texs[ti, ty, tx, 2] == 255:
                        continue  # magenta = transparent
                else:
                    r, g, b = cr, cg, cbb
                f = (z - fog_n) / (fog_f - fog_n)
                if f > 0.0:
                    if f > 1.0:
                        f = 1.0
                    r = r + (fogc[0] - r) * f
                    g = g + (fogc[1] - g) * f
                    b = b + (fogc[2] - b) * f
                if blend:
                    cb[py, px, 0] = cb[py, px, 0] * (1.0 - al) + r * al
                    cb[py, px, 1] = cb[py, px, 1] * (1.0 - al) + g * al
                    cb[py, px, 2] = cb[py, px, 2] * (1.0 - al) + b * al
                else:
                    zb[py, px] = z
                    cb[py, px, 0] = r
                    cb[py, px, 1] = g
                    cb[py, px, 2] = b


@njit(cache=True)
def _clip_project(vt, uv, near, focal, cx, cy, W, H):
    """vt (N,3,3) espace caméra. Retourne tris projetés + index d'origine."""
    n = vt.shape[0]
    osx = np.empty((n * 2, 3))
    osy = np.empty((n * 2, 3))
    osz = np.empty((n * 2, 3))
    ouv = np.empty((n * 2, 3, 2))
    oid = np.empty(n * 2, np.int64)
    k = 0
    pv = np.empty((4, 3))
    pu = np.empty((4, 2))
    for t in range(n):
        za, zb_, zc = vt[t, 0, 2], vt[t, 1, 2], vt[t, 2, 2]
        if za < near and zb_ < near and zc < near:
            continue
        m = 0
        for i in range(3):
            j = (i + 1) % 3
            zi, zj = vt[t, i, 2], vt[t, j, 2]
            if zi >= near:
                pv[m, :] = vt[t, i, :]
                pu[m, :] = uv[t, i, :]
                m += 1
            if (zi >= near) != (zj >= near):
                s = (near - zi) / (zj - zi)
                pv[m, :] = vt[t, i, :] + (vt[t, j, :] - vt[t, i, :]) * s
                pu[m, :] = uv[t, i, :] + (uv[t, j, :] - uv[t, i, :]) * s
                m += 1
        for q in range(m - 2):
            ids = (0, q + 1, q + 2)
            out = True
            for a in range(3):
                v = pv[ids[a]]
                X = cx + v[0] / v[2] * focal
                Y = cy - v[1] / v[2] * focal
                # accrochage des sommets au demi-pixel (tremblement PS1)
                osx[k, a] = math.floor(X * 2.0 + 0.5) * 0.5
                osy[k, a] = math.floor(Y * 2.0 + 0.5) * 0.5
                osz[k, a] = v[2]
                ouv[k, a, 0] = pu[ids[a], 0]
                ouv[k, a, 1] = pu[ids[a], 1]
            mnx = min(osx[k, 0], min(osx[k, 1], osx[k, 2]))
            mxx = max(osx[k, 0], max(osx[k, 1], osx[k, 2]))
            mny = min(osy[k, 0], min(osy[k, 1], osy[k, 2]))
            mxy = max(osy[k, 0], max(osy[k, 1], osy[k, 2]))
            if mxx < 0 or mny > H or mxy < 0 or mnx > W:
                continue
            oid[k] = t
            k += 1
    return osx[:k], osy[:k], osz[:k], ouv[:k], oid[:k]


class Env:
    """réglages d'ambiance"""
    def __init__(self, sky_top=(90, 120, 180), sky_hor=(190, 200, 210), fog=None, fog_near=30, fog_far=220,
                 light=(-0.4, 0.8, -0.35), amb=0.45, light_col=(255, 244, 225), sky_img=None, points=()):
        self.sky_top, self.sky_hor = C(sky_top), C(sky_hor)
        self.fog = C(fog) if fog is not None else C(sky_hor)
        self.fog_near, self.fog_far = fog_near, fog_far
        l = np.asarray(light, float)
        self.light = l / np.linalg.norm(l)
        self.amb, self.light_col = amb, C(light_col)
        self.sky_img = sky_img
        self.points = list(points)  # [(pos, col(0-1), intensité, rayon)]

    def copy(self, **kw):
        import copy
        e = copy.copy(self)
        e.points = list(self.points)
        for k, v in kw.items():
            if k in ('sky_top', 'sky_hor', 'fog', 'light_col'):
                v = C(v)
            if k == 'light':
                v = np.asarray(v, float) / np.linalg.norm(v)
            setattr(e, k, v)
        return e


def sky_gradient(env, horizon_y, h=None):
    h = H if h is None else h
    y = np.arange(h, dtype=np.float32)[:, None]
    t = np.clip(1.0 - (horizon_y - y) / max(horizon_y, 1), 0, 1) ** 1.6
    t = np.where(y > horizon_y, 1.0, t)
    img = env.sky_top[None, :] * (1 - t[..., None]) + env.sky_hor[None, :] * t[..., None]
    return np.broadcast_to(img, (h, W, 3)).astype(np.float32).copy()


PS1_MODE = False   # True : sommets accrochés au pixel (tremblote) + textures affines, comme sur la vraie PS1
PS1_MAX_EDGE = 1.5  # en mode PS1, les grands triangles texturés sont découpés (comme dans les vrais jeux)


def _subdivide(mesh, max_edge):
    tr, uv = mesh.tris, mesh.uv
    keep = mesh.tex > 0
    for _ in range(4):
        e = np.max(np.stack([np.linalg.norm(tr[:, 1] - tr[:, 0], axis=1), np.linalg.norm(tr[:, 2] - tr[:, 1], axis=1),
                             np.linalg.norm(tr[:, 0] - tr[:, 2], axis=1)]), axis=0)
        big = (e > max_edge) & keep
        if not big.any() or len(tr) > 400000:
            break
        a, b, c = tr[big, 0], tr[big, 1], tr[big, 2]
        ab, bc, ca = (a + b) / 2, (b + c) / 2, (c + a) / 2
        ua, ub, uc = uv[big, 0], uv[big, 1], uv[big, 2]
        uab, ubc, uca = (ua + ub) / 2, (ub + uc) / 2, (uc + ua) / 2
        nt = np.concatenate([np.stack([a, ab, ca], 1), np.stack([ab, b, bc], 1), np.stack([ca, bc, c], 1), np.stack([ab, bc, ca], 1)])
        nu = np.concatenate([np.stack([ua, uab, uca], 1), np.stack([uab, ub, ubc], 1), np.stack([uca, ubc, uc], 1), np.stack([uab, ubc, uca], 1)])
        rep = lambda x: np.concatenate([x[big]] * 4)
        sm = ~big
        tr = np.concatenate([tr[sm], nt])
        uv = np.concatenate([uv[sm], nu])
        col, tex, al, em = (np.concatenate([x[sm], rep(x)]) for x in (mesh.col, mesh.tex, mesh.alpha, mesh.emis))
        mesh = Mesh(tr, col, uv, tex, al, em)
        keep = mesh.tex > 0
    return mesh


def render(mesh, cam, env, bg=None):
    """renvoie image float (H,W,3) 0..1 en résolution interne"""
    R, p = cam.view()
    focal = (H / 2) / math.tan(math.radians(cam.fov) / 2)
    # horizon pour le ciel
    f = R[2]
    pitch = math.asin(max(-1, min(1, f[1])))
    hor = H / 2 + math.tan(pitch) * focal
    if bg is None:
        bg = env.sky_img(cam, hor) if callable(env.sky_img) else sky_gradient(env, hor)
    cb = np.ascontiguousarray(bg.astype(np.float64))
    zb = np.full((H, W), 1e9)
    if len(mesh) and PS1_MODE:
        mesh = _subdivide(mesh, PS1_MAX_EDGE)
    if len(mesh):
        tr = mesh.tris
        # éclairage plat par face (normale orientée vers la caméra)
        e1 = tr[:, 1] - tr[:, 0]
        e2 = tr[:, 2] - tr[:, 0]
        nrm = np.cross(e1, e2)
        nl = np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
        nrm /= nl
        cen = tr.mean(axis=1)
        tocam = p - cen
        flip = np.sign(np.einsum('ij,ij->i', nrm, tocam))
        flip[flip == 0] = 1
        nrm *= flip[:, None]
        d = np.clip(nrm @ env.light, 0, 1)
        lit = env.amb + (1 - env.amb) * d[:, None] * env.light_col[None, :]
        for (pp, pc, inten, rad) in env.points:
            v = np.asarray(pp, float) - cen
            dist = np.linalg.norm(v, axis=1) + 1e-6
            ndl = np.clip(np.einsum('ij,ij->i', nrm, v) / dist, 0, 1) * 0.7 + 0.3
            att = inten * np.clip(1 - dist / rad, 0, 1) ** 2
            lit = lit + (ndl * att)[:, None] * C(pc)[None, :]
        lit = lit * (1 - mesh.emis[:, None]) + mesh.emis[:, None]
        col = np.clip(mesh.col * lit, 0, 1.6)
        vt = (tr - p) @ R.T
        sx, sy, sz, uv, oid = _clip_project(np.ascontiguousarray(vt), np.ascontiguousarray(mesh.uv), 0.05, focal, W / 2, H / 2, W, H)
        if len(oid) and PS1_MODE:
            sx = np.floor(sx + 0.5)
            sy = np.floor(sy + 0.5)
        if len(oid):
            al = mesh.alpha[oid]
            opq = al >= 0.999
            # vraie transparence : opaques d'abord, puis transparents du plus loin au plus proche
            for blend, sel in ((False, np.where(opq)[0]), (True, np.where(~opq)[0])):
                if not len(sel):
                    continue
                if blend:
                    sel = sel[np.argsort(-sz[sel].mean(axis=1))]
                o = oid[sel]
                _raster(np.ascontiguousarray(sx[sel]), np.ascontiguousarray(sy[sel]), np.ascontiguousarray(sz[sel]),
                        np.ascontiguousarray(uv[sel]), np.ascontiguousarray(col[o]), np.ascontiguousarray(mesh.tex[o].astype(np.int64)),
                        np.ascontiguousarray(al[sel]), TEXB.array(), zb, cb,
                        np.asarray(env.fog, np.float64), float(env.fog_near), float(env.fog_far), BAYER4, W, H, blend, PS1_MODE)
    return np.clip(cb, 0, 1), zb


def ps1_post(img):
    """quantification 15 bits + tramage, retourne uint8 en résolution interne"""
    b = np.tile(BAYER4, (H // 4 + 1, W // 4 + 1))[:img.shape[0], :img.shape[1]]
    v = img * 31.0 + (b[..., None] - 0.5) * 0.9
    v = np.clip(np.floor(v + 0.5), 0, 31) / 31.0
    return (v * 255).astype(np.uint8)


def upscale(img8):
    return np.repeat(np.repeat(img8, UPS, axis=0), UPS, axis=1)
