"""Effets sonores synthétisés + mixage."""
import numpy as np
import wave

SR = 44100
R = np.random.default_rng(11)


def t_(d):
    return np.arange(int(d * SR)) / SR


def env_ad(n, a=0.01, d=0.5):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / max(d, 1e-4))
    return e


def lowpass(x, cutoff):
    # filtre 1 pôle répété
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for _ in range(2):
        acc = 0.0
        for i in range(len(x)):
            acc = (1 - a) * x[i] + a * acc
            y[i] = acc
        x = y.copy()
    return y


def lp_fast(x, cutoff):
    """lowpass via FFT"""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def hp_fast(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (cutoff / (f + 1e-3)) ** 4)
    return np.fft.irfft(X, len(x))


def bp_fast(x, lo, hi):
    return hp_fast(lp_fast(x, hi), lo)


def norm(x, peak=0.9):
    m = np.abs(x).max() + 1e-9
    return x / m * peak


def noise(d):
    return R.standard_normal(int(d * SR))


# ------------------------------------------------------------------ sons
def thunder(d=4.0, crack=True):
    n = noise(d)
    rum = lp_fast(n, 120) * env_ad(len(n), 0.08, d * 0.35)
    rum2 = lp_fast(noise(d), 60) * env_ad(len(n), 0.3, d * 0.4)
    out = rum * 1.0 + rum2 * 0.8
    if crack:
        c = hp_fast(noise(0.4), 1500) * env_ad(int(0.4 * SR), 0.002, 0.06)
        out[:len(c)] += c * 0.6
    # roulements
    for k in range(4):
        s = int(R.uniform(0.3, d * 0.7) * SR)
        b = lp_fast(noise(1.2), 90) * env_ad(int(1.2 * SR), 0.05, 0.4)
        e = min(len(out), s + len(b))
        out[s:e] += b[:e - s] * 0.6
    return norm(out, 0.95)


def zap(d=0.6):
    t = t_(d)
    x = hp_fast(noise(d), 2500) * env_ad(len(t), 0.001, 0.12)
    x += np.sign(np.sin(2 * np.pi * 120 * t)) * env_ad(len(t), 0.001, 0.1) * 0.3
    return norm(x, 0.9)


def rain(d=10.0):
    x = bp_fast(noise(d), 800, 6000) * 0.4
    drops = np.zeros(int(d * SR))
    for _ in range(int(d * 60)):
        p = R.integers(0, len(drops) - 300)
        drops[p:p + 300] += hp_fast(noise(300 / SR), 3000) * env_ad(300, 0.0005, 0.002) * R.uniform(0.2, 1)
    return norm(x + drops * 0.5, 0.5)


def wind(d=10.0):
    x = lp_fast(noise(d), 400)
    m = 0.6 + 0.4 * np.sin(2 * np.pi * 0.17 * t_(d)) * np.sin(2 * np.pi * 0.07 * t_(d))
    return norm(x * m, 0.5)


def birds(d=8.0):
    out = np.zeros(int(d * SR))
    for _ in range(int(d * 1.5)):
        s = R.integers(0, len(out) - SR // 2)
        dd = R.uniform(0.06, 0.15)
        t = t_(dd)
        f0 = R.uniform(2500, 4500)
        ch = np.sin(2 * np.pi * (f0 * t + R.uniform(-8000, 8000) * t * t)) * env_ad(len(t), 0.005, dd / 3)
        for r in range(R.integers(1, 4)):
            ss = s + int(r * dd * 1.3 * SR)
            if ss + len(ch) < len(out):
                out[ss:ss + len(ch)] += ch * R.uniform(0.3, 1)
    return norm(out, 0.35)


def engine_hum(d=6.0, f=45):
    t = t_(d)
    x = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2 * f * t + 1) + 0.3 * np.sign(np.sin(2 * np.pi * f / 2 * t))
    x = lp_fast(x + lp_fast(noise(d), 300) * 0.8, 500)
    return norm(x, 0.45)


def fire_crackle(d=5.0):
    base = lp_fast(noise(d), 700) * 0.3
    out = base.copy()
    for _ in range(int(d * 25)):
        p = R.integers(0, len(out) - 600)
        out[p:p + 600] += hp_fast(noise(600 / SR), 1000) * env_ad(600, 0.0005, 0.004) * R.uniform(0.3, 1.2)
    return norm(out, 0.5)


def whoosh(d=0.8):
    n = noise(d)
    t = t_(d)
    e = np.sin(np.pi * t / d) ** 2
    return norm(bp_fast(n, 300, 2500) * e, 0.6)


def stream(d=8.0):
    x = bp_fast(noise(d), 400, 3000)
    m = 0.7 + 0.3 * np.sin(2 * np.pi * 3.1 * t_(d)) * np.sin(2 * np.pi * 1.7 * t_(d))
    return norm(x * m, 0.35)


def growl(d=1.2):
    t = t_(d)
    f = 70 + 20 * np.sin(2 * np.pi * 5 * t)
    ph = np.cumsum(2 * np.pi * f / SR)
    x = np.sign(np.sin(ph)) * 0.5 + lp_fast(noise(d), 500) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t))
    x = lp_fast(x, 700) * np.sin(np.pi * t / d) ** 0.5
    return norm(x, 0.7)


def thwack(d=0.3):
    t = t_(d)
    x = np.sin(2 * np.pi * 180 * t * np.exp(-t * 8)) * env_ad(len(t), 0.001, 0.05) + hp_fast(noise(d), 800) * env_ad(len(t), 0.001, 0.02)
    return norm(x, 0.8)


def splash(d=0.7):
    x = bp_fast(noise(d), 500, 5000) * env_ad(int(d * SR), 0.005, 0.18)
    return norm(x, 0.6)


def steam_whistle(d=1.4, f=520):
    t = t_(d)
    x = sum(np.sin(2 * np.pi * f * k * t) / k for k in (1, 1.25, 1.5, 2, 3))
    x = x * (0.85 + 0.15 * np.sin(2 * np.pi * 6 * t)) + bp_fast(noise(d), f, f * 4) * 0.5
    e = np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.2)
    return norm(x * e, 0.55)


def chuff(d=6.0, rate=3.0):
    out = np.zeros(int(d * SR))
    per = int(SR / rate)
    for s in range(0, len(out) - per, per):
        p = bp_fast(noise(per / SR), 200, 3000) * env_ad(per, 0.005, 0.07)
        out[s:s + per] += p
    out += lp_fast(noise(d), 100) * 0.3
    return norm(out, 0.5)


def clank(d=0.5):
    t = t_(d)
    x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * dd) for f, dd in ((410, 12), (1130, 18), (2370, 25), (3300, 30)))
    x += hp_fast(noise(d), 2000) * env_ad(len(t), 0.001, 0.01)
    return norm(x, 0.7)


def ratchet(d=0.6):
    out = np.zeros(int(d * SR))
    for k in range(6):
        s = int(k * d / 6 * SR)
        c = clank(0.08) * 0.5
        out[s:s + len(c)] += c[:len(out) - s]
    return norm(out, 0.6)


def wheel_rattle(d=4.0):
    out = np.zeros(int(d * SR))
    for s in range(0, len(out) - 2000, int(SR * 0.25)):
        c = lp_fast(noise(0.05), 600) * env_ad(int(0.05 * SR), 0.001, 0.015)
        out[s:s + len(c)] += c
    out += lp_fast(noise(d), 200) * 0.2
    return norm(out, 0.4)


def crowd(d=6.0):
    out = np.zeros(int(d * SR))
    for _ in range(40):
        f = R.uniform(110, 260)
        t = t_(d)
        ph = np.cumsum(2 * np.pi * (f + 25 * np.sin(2 * np.pi * R.uniform(2, 5) * t)) / SR)
        v = np.sin(ph) + 0.4 * np.sin(2 * ph)
        m = np.clip(np.sin(2 * np.pi * R.uniform(0.2, 0.7) * t + R.uniform(0, 6)), 0, 1)
        out += v * m
    out = bp_fast(out, 200, 2500)
    return norm(out, 0.3)


def cannon(d=2.5):
    t = t_(d)
    x = lp_fast(noise(d), 150) * env_ad(len(t), 0.003, 0.5) * 1.2
    x += np.sin(2 * np.pi * 50 * t * np.exp(-t * 2)) * env_ad(len(t), 0.002, 0.25)
    x += hp_fast(noise(d), 1000) * env_ad(len(t), 0.001, 0.03) * 0.5
    return norm(x, 0.95)


def explosion(d=3.0):
    x = lp_fast(noise(d), 300) * env_ad(int(d * SR), 0.01, 0.9)
    x += lp_fast(noise(d), 1500) * env_ad(int(d * SR), 0.005, 0.15) * 0.5
    return norm(x, 0.9)


def bell(d=2.5, f=440):
    t = t_(d)
    x = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (1.5 + k)) for k, a in ((1, 1), (2.0, .6), (2.76, .4), (5.4, .2)))
    return norm(x * np.minimum(1, t / 0.003), 0.6)


def tick(d=0.12):
    t = t_(d)
    x = hp_fast(noise(d), 3000) * env_ad(len(t), 0.0005, 0.006) + np.sin(2 * np.pi * 2200 * t) * env_ad(len(t), 0.0005, 0.01)
    return norm(x, 0.5)


def waves(d=10.0):
    t = t_(d)
    x = lp_fast(noise(d), 900) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.12 * t) ** 2)
    return norm(x, 0.45)


def gulls(d=6.0):
    out = np.zeros(int(d * SR))
    for _ in range(int(d * 0.8)):
        s = R.integers(0, len(out) - SR)
        dd = R.uniform(0.25, 0.45)
        t = t_(dd)
        f = 1400 - 600 * t / dd
        ph = np.cumsum(2 * np.pi * f / SR)
        c = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.sin(np.pi * t / dd)
        out[s:s + len(c)] += c * R.uniform(0.3, 1)
    return norm(out, 0.3)


def footsteps(d=3.0, rate=2.0, surface='dirt'):
    out = np.zeros(int(d * SR))
    for s in range(0, len(out) - 4000, int(SR / rate)):
        c = lp_fast(noise(0.08), 900 if surface == 'dirt' else 2500) * env_ad(int(0.08 * SR), 0.002, 0.02)
        out[s:s + len(c)] += c
    return norm(out, 0.35)


def sweep_broom(d=1.5):
    t = t_(d)
    x = bp_fast(noise(d), 1500, 7000) * (0.5 + 0.5 * np.sin(2 * np.pi * 2.5 * t)) ** 2
    return norm(x, 0.35)


def monkey(d=0.6):
    t = t_(d)
    out = np.zeros(len(t))
    for k in range(3):
        s = int(k * 0.17 * SR)
        tt = t_(0.12)
        f = 900 + 500 * np.sin(np.pi * tt / 0.12)
        ph = np.cumsum(2 * np.pi * f / SR)
        c = (np.sign(np.sin(ph)) * 0.3 + np.sin(ph)) * np.sin(np.pi * tt / 0.12)
        out[s:s + len(c)] += c[:len(out) - s]
    return norm(bp_fast(out, 400, 4000), 0.5)


def glass(d=1.2):
    t = t_(d)
    x = sum(np.sin(2 * np.pi * R.uniform(2000, 7000) * t) * np.exp(-t * R.uniform(6, 20)) for _ in range(12))
    x += hp_fast(noise(d), 3000) * env_ad(len(t), 0.001, 0.05)
    return norm(x, 0.6)


def splinter(d=1.5):
    x = bp_fast(noise(d), 300, 3000) * env_ad(int(d * SR), 0.003, 0.3)
    return norm(x, 0.8)


def drumroll(d=1.5):
    out = np.zeros(int(d * SR))
    for s in range(0, len(out) - 3000, int(SR / 18)):
        c = lp_fast(noise(0.06), 400) * env_ad(int(0.06 * SR), 0.001, 0.02)
        out[s:s + len(c)] += c * (0.5 + 0.5 * s / len(out))
    return norm(out, 0.5)


def sting(d=1.0):
    """petit son 'ding' rétro"""
    t = t_(d)
    x = (np.sign(np.sin(2 * np.pi * 880 * t)) * 0.3 + np.sin(2 * np.pi * 1320 * t)) * np.exp(-t * 5)
    return norm(x, 0.35)


# ------------------------------------------------------------------ mixage
class Mixer:
    def __init__(self, dur):
        self.buf = np.zeros(int((dur + 2) * SR))

    def add(self, x, t, gain=1.0, fade_in=0.0, fade_out=0.0, length=None):
        if length is not None:
            n = int(length * SR)
            if len(x) < n:
                x = np.tile(x, n // len(x) + 1)
            x = x[:n].copy()
        else:
            x = x.copy()
        if fade_in:
            k = min(len(x), int(fade_in * SR))
            x[:k] *= np.linspace(0, 1, k)
        if fade_out:
            k = min(len(x), int(fade_out * SR))
            x[-k:] *= np.linspace(1, 0, k)
        s = int(t * SR)
        if s >= len(self.buf):
            return
        e = min(len(self.buf), s + len(x))
        self.buf[s:e] += x[:e - s] * gain

    def save(self, path, peak=0.9):
        b = self.buf
        m = np.abs(b).max()
        if m > peak:
            b = b / m * peak
        st = np.stack([b, b], 1)
        with wave.open(path, 'wb') as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((st * 32767).astype(np.int16).tobytes())


# ------------------------------------------------------------------ tonnerre réaliste (v2)
def _brown(n):
    x = np.cumsum(R.standard_normal(n))
    x -= np.convolve(x, np.ones(2001) / 2001, mode='same')  # retire la dérive
    return x / (np.abs(x).max() + 1e-9)


def _reverb(x, dur=1.6, mix=0.35, cutoff=3000):
    n = int(dur * SR)
    ir = R.standard_normal(n) * np.exp(-np.arange(n) / SR * 4.0)
    ir = lp_fast(ir, cutoff)
    ir /= np.abs(ir).sum() ** 0.5 * 8
    from numpy.fft import rfft, irfft
    L = len(x) + n
    wet = irfft(rfft(x, L) * rfft(ir, L), L)[:len(x)]
    wet = wet / (np.abs(wet).max() + 1e-9) * np.abs(x).max()
    return x * (1 - mix) + wet * mix


def thunder_close(d=5.5, seed=None):
    """coup de foudre tout proche : claquement sec qui déchire + boum + roulement"""
    rr = np.random.default_rng(seed)
    n = int(d * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    # 1) claquement déchirant : rafale d'impulsions sur ~0.3 s
    k = 0.0
    while k < 0.32:
        s = int(k * SR)
        L = int(rr.uniform(0.002, 0.007) * SR)
        burst = R.standard_normal(L) * np.exp(-np.arange(L) / L * 4)
        amp = np.exp(-k / 0.12) * rr.uniform(0.5, 1.0)
        out[s:s + L] += burst * amp
        k += rr.exponential(0.006 + k * 0.05)
    out = hp_fast(out, 300) * 5.0
    # 2) le boum grave
    boom_env = np.minimum(1, t / 0.012) * np.exp(-t / 0.7)
    boom = bp_fast(R.standard_normal(n), 45, 220) * boom_env
    boom = boom / (np.abs(boom).max() + 1e-9)
    sweep = np.sin(2 * np.pi * np.cumsum(55 * np.exp(-t * 0.8) + 25) / SR) * np.exp(-t / 0.5) * np.minimum(1, t / 0.01)
    out += boom * 1.0 + sweep * 0.35
    # 3) roulement : bruit brun modulé par des grondements aléatoires
    rum = bp_fast(_brown(n) + R.standard_normal(n) * 0.02, 60, 600)
    env = np.zeros(n)
    for _ in range(9):
        c = rr.uniform(0.4, d * 0.75)
        w = rr.uniform(0.25, 0.8)
        env += rr.uniform(0.4, 1.0) * np.exp(-((t - c) / w) ** 2)
    env *= np.exp(-t / (d * 0.45)) * np.minimum(1, t / 0.25)
    out += rum / (np.abs(rum).max() + 1e-9) * env * 1.0
    gr = bp_fast(R.standard_normal(n), 200, 1400)
    out += gr / (np.abs(gr).max() + 1e-9) * env * 0.35  # grain du roulement
    out = _reverb(out, 1.8, 0.3)
    out = np.tanh(out / (np.abs(out).max() + 1e-9) * 2.2)
    fade = np.ones(n)
    fade[-int(0.4 * SR):] = np.linspace(1, 0, int(0.4 * SR))
    return norm(out * fade, 0.98)


def thunder_far(d=6.0, seed=None):
    """tonnerre lointain : pas de claquement, long roulement sourd"""
    rr = np.random.default_rng(seed)
    n = int(d * SR)
    t = np.arange(n) / SR
    rum = lp_fast(_brown(n), 160)
    env = np.zeros(n)
    for _ in range(7):
        c = rr.uniform(0.3, d * 0.7)
        w = rr.uniform(0.4, 1.0)
        env += rr.uniform(0.4, 1.0) * np.exp(-((t - c) / w) ** 2)
    env *= np.minimum(1, t / 0.4) * np.exp(-t / (d * 0.5))
    out = rum / (np.abs(rum).max() + 1e-9) * env
    out = _reverb(out, 2.0, 0.4, 1500)
    return norm(np.tanh(out * 2), 0.8)


def arc_buzz(d=1.5):
    """arc électrique qui grésille (au ralenti)"""
    t = t_(d)
    buzz = np.sign(np.sin(2 * np.pi * 60 * t)) * 0.4 + np.sin(2 * np.pi * 180 * t) * 0.3
    crack = np.zeros(len(t))
    for _ in range(int(d * 40)):
        s = R.integers(0, len(t) - 400)
        crack[s:s + 400] += hp_fast(noise(400 / SR), 2000) * env_ad(400, 0.0005, 0.003) * R.uniform(0.3, 1)
    x = buzz * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t)) + crack * 1.5
    x *= np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.1)
    return norm(bp_fast(x, 100, 8000), 0.7)


def roar(d=1.6):
    """rugissement d'ours (plus grave et plus long que growl)"""
    t = t_(d)
    f = 95 + 35 * np.sin(np.pi * t / d) + 8 * np.sin(2 * np.pi * 6 * t)
    ph = np.cumsum(2 * np.pi * f / SR)
    x = np.sign(np.sin(ph)) * 0.5 + np.sin(2 * ph) * 0.3 + lp_fast(noise(d), 900) * 0.9
    x = bp_fast(x, 70, 1600) * np.sin(np.pi * t / d) ** 0.6
    return norm(np.tanh(x * 2), 0.8)
