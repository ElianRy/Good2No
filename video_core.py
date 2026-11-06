"""Timeline, sous-titres mot par mot, filigrane, boucle de rendu, mixage audio."""
import math, os, re, subprocess, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import engine
from engine import render, ps1_post, upscale

FPS = 30
OW, OH = 1080, 1920
FONT = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
F_SUB = ImageFont.truetype(FONT, 84)
F_WM = ImageFont.truetype(FONT, 40)
SUB_Y = 1230
WM_TEXT = '@good2no0'


# ------------------------------------------------------------------ timing
def est_timing(lines, cps=14.5, gap=0.35, lead=0.4):
    """estime le début/fin de chaque mot. Retourne liste de lignes [{'words':[(w,t0,t1)], 't0','t1'}]"""
    out = []
    t = lead
    for line in lines:
        words = line.split()
        ws = []
        lt0 = t
        for w in words:
            core = re.sub(r'[^\wÀ-ÿ\d]', '', w)
            d = max(0.16, (len(core) + 1) / cps)
            if re.search(r'\d{3,}', core):
                d *= 2.6  # les nombres sont longs à dire
            elif re.search(r'\d', core):
                d *= 1.6
            ws.append([w, t, t + d])
            t += d
            if w.endswith('…') or w.endswith('...'):
                t += 0.45
            elif w.endswith(('.', '!', '?', ':')):
                t += 0.3
            elif w.endswith((',', ';')):
                t += 0.14
        out.append({'words': ws, 't0': lt0, 't1': t})
        t += gap
    return out


def load_timing(path):
    with open(path) as f:
        return json.load(f)


def chunks(timing, maxw=3, maxc=16):
    """groupes de mots affichés ensemble"""
    res = []
    for li, L in enumerate(timing):
        cur = []
        for w in L['words']:
            txt = ' '.join(x[0] for x in cur + [w])
            if cur and (len(cur) >= maxw or len(txt) > maxc):
                res.append(cur)
                cur = []
            cur.append(w)
            if w[0].endswith(('.', ',', '…', ':', '?', '!', ';')) and len(cur) >= 1:
                res.append(cur)
                cur = []
        if cur:
            res.append(cur)
    # durée d'affichage : jusqu'au chunk suivant (max +0.6 s après le dernier mot)
    out = []
    for i, c in enumerate(res):
        t0 = c[0][1]
        t1 = c[-1][2] + 0.6
        if i + 1 < len(res):
            t1 = min(t1, res[i + 1][0][1])
        out.append((t0, t1, c))
    return out


class Subs:
    def __init__(self, timing, upper=False):
        self.ch = chunks(timing)
        self.upper = upper
        self._cache = {}

    def draw(self, img, t):
        """img PIL RGB 1080x1920"""
        cur = None
        for (t0, t1, c) in self.ch:
            if t0 <= t < t1:
                cur = c
                break
        d = ImageDraw.Draw(img)
        if cur is not None:
            words = [w[0].upper() if self.upper else w[0] for w in cur]
            active = 0
            for i, w in enumerate(cur):
                if t >= w[1]:
                    active = i
            # pop sur le mot actif
            sp = d.textlength(' ', font=F_SUB)
            widths = [d.textlength(w, font=F_SUB) for w in words]
            total = sum(widths) + sp * (len(words) - 1)
            lines = [list(range(len(words)))]
            if total > OW - 120:
                # coupe en deux lignes
                best = 1
                for k in range(1, len(words)):
                    a = sum(widths[:k]) + sp * (k - 1)
                    b = sum(widths[k:]) + sp * (len(words) - k - 1)
                    if max(a, b) < max(sum(widths[:best]) + sp * (best - 1), sum(widths[best:]) + sp * (len(words) - best - 1)):
                        best = k
                lines = [list(range(best)), list(range(best, len(words)))]
            y = SUB_Y - (len(lines) - 1) * 50
            for ln in lines:
                lw = sum(widths[i] for i in ln) + sp * (len(ln) - 1)
                x = (OW - lw) / 2
                for i in ln:
                    fill = (255, 226, 60) if i == active else (255, 255, 255)
                    d.text((x, y), words[i], font=F_SUB, fill=fill, stroke_width=9, stroke_fill=(0, 0, 0), anchor='ls')
                    x += widths[i] + sp
                y += 100
        return img


def watermark(img):
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    tw = d.textlength(WM_TEXT, font=F_WM)
    d.text(((OW - tw) / 2, SUB_Y + 150), WM_TEXT, font=F_WM, fill=(255, 255, 255, 150), stroke_width=3, stroke_fill=(0, 0, 0, 110), anchor='ls')
    img.paste(ov, (0, 0), ov)
    return img


# ------------------------------------------------------------------ shots
class Timeline:
    def __init__(self, timing):
        self.timing = timing
        self.shots = []  # (t0, fn)

    def T(self, line, word=0, end=False):
        L = self.timing[line]
        if word == 'end':
            return L['t1']
        if word < 0:
            word = len(L['words']) + word
        w = L['words'][word]
        return w[2] if end else w[1]

    def word_t(self, line, needle, end=False):
        strip = lambda x: re.sub(r'[^\wÀ-ÿ\d\']', '', x.lower())
        ws = self.timing[line]['words']
        for w in ws:
            if strip(w[0]) == strip(needle):
                return w[2] if end else w[1]
        for w in ws:
            if needle.lower() in w[0].lower():
                return w[2] if end else w[1]
        raise KeyError(needle)

    def add(self, t0, fn):
        self.shots.append((t0, fn))

    def duration(self):
        return self.timing[-1]['t1'] + 1.2

    def at(self, t):
        sh = sorted(self.shots, key=lambda s: s[0])
        for i, (t0, fn) in enumerate(sh):
            t1 = sh[i + 1][0] if i + 1 < len(sh) else self.duration()
            if t0 <= t < t1 or (i == len(sh) - 1 and t >= t0):
                return fn, t - t0, t1 - t0
        return sh[0][1], 0, 1


def frame(tl, t, subs=None, wm=True, post=None):
    fn, lt, dur = tl.at(t)
    res = fn(lt, dur, t)
    mesh, cam, env = res[:3]
    extra = res[3] if len(res) > 3 else {}
    img, zb = render(mesh, cam, env)
    if 'post_lin' in extra:
        img = extra['post_lin'](img)
    img8 = upscale(ps1_post(img))
    pim = Image.fromarray(img8)
    if 'flash' in extra and extra['flash'] > 0:
        a = min(1.0, extra['flash'])
        pim = Image.blend(pim, Image.new('RGB', pim.size, extra.get('flash_col', (255, 255, 255))), a)
    if 'fade' in extra and extra['fade'] > 0:
        pim = Image.blend(pim, Image.new('RGB', pim.size, (0, 0, 0)), min(1.0, extra['fade']))
    if 'overlay' in extra:
        extra['overlay'](pim)
    if 'post_pil' in extra:
        extra['post_pil'](pim)
    if getattr(tl, 'overlay', None) is not None:
        tl.overlay(pim, t)
    if subs is not None:
        subs.draw(pim, t)
    if wm:
        watermark(pim)
    return pim


def render_video(tl, out_mp4, audio_wav=None, subs=None, workers=2, t_range=None, fps=FPS, tmpdir=None):
    dur = tl.duration()
    n = int(math.ceil(dur * fps))
    f0, f1 = (0, n) if t_range is None else (int(t_range[0] * fps), int(t_range[1] * fps))
    tmpdir = tmpdir or os.path.splitext(out_mp4)[0] + '_parts'
    os.makedirs(tmpdir, exist_ok=True)
    script = sys.argv[0]
    # chaque worker = sous-processus qui rend une plage
    per = (f1 - f0 + workers - 1) // workers
    procs = []
    parts = []
    for k in range(workers):
        a, b = f0 + k * per, min(f1, f0 + (k + 1) * per)
        if a >= b:
            continue
        part = os.path.join(tmpdir, f'part{k}.mp4')
        parts.append(part)
        procs.append(subprocess.Popen([sys.executable, script, '--part', str(a), str(b), part, str(fps)]))
    for p in procs:
        if p.wait() != 0:
            raise RuntimeError('worker failed')
    lst = os.path.join(tmpdir, 'list.txt')
    with open(lst, 'w') as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst]
    if audio_wav:
        cmd += ['-ss', str(f0 / fps), '-t', str((f1 - f0) / fps), '-i', audio_wav, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '192k', '-shortest']
    cmd += ['-c:v', 'copy', out_mp4]
    subprocess.check_call(cmd)


def part_main(tl, subs, argv):
    a, b, out, fps = int(argv[0]), int(argv[1]), argv[2], int(argv[3])
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}',
                          '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', out],
                         stdin=subprocess.PIPE)
    for i in range(a, b):
        im = frame(tl, i / fps, subs)
        p.stdin.write(im.tobytes())
    p.stdin.close()
    p.wait()


def contact_sheet(tl, times, out, subs=None, cols=4, scale=0.25):
    ims = [frame(tl, t, subs).resize((int(OW * scale), int(OH * scale)), Image.BILINEAR) for t in times]
    rows = (len(ims) + cols - 1) // cols
    w, h = ims[0].size
    sheet = Image.new('RGB', (cols * w, rows * (h + 30)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 20)
    for i, im in enumerate(ims):
        x, y = (i % cols) * w, (i // cols) * (h + 30)
        sheet.paste(im, (x, y + 30))
        m, s = divmod(times[i], 60)
        d.text((x + 6, y + 4), f'{int(m)}:{s:05.2f}', font=f, fill=(255, 255, 0))
    sheet.save(out)


def mix_voice(voice_wav, sfx_wav, out_wav, sfx_gain=0.4):
    """voix bien devant, bruitages en dessous, niveau final normalisé"""
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', voice_wav, '-i', sfx_wav, '-filter_complex',
                           f'[0:a]aresample=44100,pan=stereo|c0=c0|c1=c0,volume=1.6[v];[1:a]volume={sfx_gain}[s];'
                           '[v][s]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95,loudnorm=I=-14:TP=-1.0:LRA=11',
                           '-ar', '44100', out_wav])
