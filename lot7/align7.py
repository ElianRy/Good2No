"""Aligne une voix Gemini complète (un seul wav) sur le texte -> timing.json + voix.wav
usage : python3 align7.py chaise /chemin/voix.wav [max_silence]
- coupe le blanc du début (voix dès 0,0 s)
- raccourcit les silences trop longs (> max_silence) pour garder du rythme
- ASR sherpa-onnx (zipformer fr) + alignement difflib sur le texte lu
"""
import sys, os, re, json, wave, difflib, unicodedata
import numpy as np
import sherpa_onnx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts7 import ALL

MODEL = '/home/claude/asr/sherpa-onnx-streaming-zipformer-fr-2023-04-14'
SR = 24000


def norm(w):
    w = unicodedata.normalize('NFD', w.lower())
    w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return re.sub(r"[^a-z0-9]", '', w)


def read_wav(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        if w.getnchannels() > 1:
            x = x.reshape(-1, w.getnchannels()).mean(1)
        return x, w.getframerate()


def squeeze_silences(x, sr, max_sil=0.5, keep=0.32, thr=0.01, lead=0.0):
    env = np.convolve(np.abs(x), np.ones(int(0.02 * sr)) / (0.02 * sr), mode='same')
    loud = env > thr
    idx = np.where(loud)[0]
    a = max(0, idx[0] - int(0.02 * sr))
    b = min(len(x), idx[-1] + int(0.15 * sr))
    x, loud = x[a:b], loud[a:b]
    out = [np.zeros(int(lead * sr), np.float32)]
    i, n = 0, len(x)
    removed = 0
    while i < n:
        if loud[i]:
            j = i
            while j < n and loud[j]:
                j += 1
            out.append(x[i:j]); i = j
        else:
            j = i
            while j < n and not loud[j]:
                j += 1
            L = j - i
            if L > max_sil * sr:
                k = int(keep * sr)
                seg = np.concatenate([x[i:i + k // 2], x[j - k // 2:j]])
                out.append(seg); removed += L - k
            else:
                out.append(x[i:j])
            i = j
    print(f'silences raccourcis : -{removed / sr:.2f} s')
    return np.concatenate(out)


def recognizer():
    m = MODEL
    return sherpa_onnx.OnlineRecognizer.from_transducer(
        tokens=f'{m}/tokens.txt', encoder=f'{m}/encoder-epoch-29-avg-9-with-averaged-model.onnx',
        decoder=f'{m}/decoder-epoch-29-avg-9-with-averaged-model.onnx', joiner=f'{m}/joiner-epoch-29-avg-9-with-averaged-model.onnx',
        num_threads=2, sample_rate=16000, feature_dim=80, decoding_method='greedy_search')


def asr_words(rec, x, sr):
    PAD = 0.5
    x = np.concatenate([np.zeros(int(PAD * sr), np.float32), x])
    s = rec.create_stream()
    step = int(0.1 * sr)
    for i in range(0, len(x), step):
        s.accept_waveform(sr, x[i:i + step])
        while rec.is_ready(s):
            rec.decode_stream(s)
    s.accept_waveform(sr, np.zeros(int(1.0 * sr), np.float32))
    s.input_finished()
    while rec.is_ready(s):
        rec.decode_stream(s)
    r = rec.get_result_all(s)
    words = []
    for t, tm in zip(r.tokens, r.timestamps):
        tm = max(0.0, tm - PAD - 0.08)
        if t.startswith('▁') or t.startswith(' ') or not words:
            words.append([t.replace('▁', '').strip(), tm, tm + 0.12])
        else:
            words[-1][0] += t
            words[-1][2] = tm + 0.12
    for i in range(len(words) - 1):
        words[i][2] = min(words[i][2] + 0.1, words[i + 1][1])
    return [w for w in words if norm(w[0])]


def map_spans(src, dst):
    a = [norm(w) for w in src]
    b = [norm(w) for w in dst]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    res = [None] * len(a)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                res[i1 + k] = (j1 + k, j1 + k + 1)
        elif i2 > i1:
            n, m = i2 - i1, j2 - j1
            for k in range(n):
                s = j1 + (m * k) // n
                e = j1 + (m * (k + 1)) // n
                res[i1 + k] = (s, max(e, s))
    return res, sm.ratio()


def split_spoken(t):
    return [p for p in re.split(r"[\s\-]+", t.replace('…', ' ').replace('«', ' ').replace('»', ' ')) if norm(p)]


def main(name, wav, max_sil=0.5, keep=0.32):
    lines = ALL[name]
    x, sr = read_wav(wav)
    assert sr == SR, sr
    x = squeeze_silences(x, sr, max_sil, keep)
    dur = len(x) / sr
    rec = recognizer()
    aw = asr_words(rec, x, sr)
    # mots lus (tout le texte) avec propriétaire (ligne, mot de sous-titre)
    vwords, owner = [], []
    for li, (sub, spoken) in enumerate(lines):
        sw = sub.split()
        if spoken is None:
            for si, w in enumerate(sw):
                for p in split_spoken(w):
                    vwords.append(p); owner.append((li, si))
        else:
            # mots lus -> mots du sous-titre par alignement local
            sp = split_spoken(spoken)
            flat, own = [], []
            for si, w in enumerate(sw):
                for p in split_spoken(w):
                    flat.append(p); own.append(si)
            spans, _ = map_spans(sp, flat)
            for k, p in enumerate(sp):
                s, e = spans[k]
                si = own[min(s, len(own) - 1)] if (e > s or s < len(own)) else own[-1]
                vwords.append(p); owner.append((li, si))
    spans, ratio = map_spans(vwords, [w[0] for w in aw])
    print(f'ASR {len(aw)} mots, texte {len(vwords)} mots, ressemblance {ratio:.2f}')
    vt = [None] * len(vwords)
    for i, (s, e) in enumerate(spans):
        if e > s:
            vt[i] = (aw[s][1], aw[e - 1][2])
    known = [i for i, t in enumerate(vt) if t]
    for i in range(len(vt)):
        if vt[i] is None:
            prev = max([k for k in known if k < i], default=None)
            nxt = min([k for k in known if k > i], default=None)
            t0 = vt[prev][1] if prev is not None else 0.0
            t1 = vt[nxt][0] if nxt is not None else dur
            lo = prev + 1 if prev is not None else 0
            hi = nxt if nxt is not None else len(vt)
            L = [len(vwords[k]) + 1 for k in range(lo, hi)]
            c = sum(L[:i - lo])
            vt[i] = (t0 + (t1 - t0) * c / sum(L), t0 + (t1 - t0) * (c + L[i - lo]) / sum(L))
    timing = []
    for li, (sub, _) in enumerate(lines):
        sw = sub.split()
        ws = [[w, None, None] for w in sw]
        for k, (l2, si) in enumerate(owner):
            if l2 != li:
                continue
            a, b = vt[k]
            ws[si][1] = a if ws[si][1] is None else min(ws[si][1], a)
            ws[si][2] = b if ws[si][2] is None else max(ws[si][2], b)
        for i in range(len(ws)):
            if ws[i][1] is None:   # ponctuation seule
                p = ws[i - 1][2] if i > 0 else (timing[-1]['t1'] if timing else 0.0)
                ws[i][1], ws[i][2] = p, p + 0.1
        for i in range(1, len(ws)):
            ws[i][1] = max(ws[i][1], ws[i - 1][1] + 0.05)
            ws[i - 1][2] = max(ws[i - 1][2], ws[i - 1][1] + 0.08)
        timing.append({'words': ws, 't0': ws[0][1], 't1': ws[-1][2]})
    for L in timing:   # l'ASR répond ~0,13 s après le début réel des mots
        for w in L['words']:
            w[1], w[2] = max(0.0, w[1] - 0.12), max(0.05, w[2] - 0.12)
        L['t0'], L['t1'] = L['words'][0][1], L['words'][-1][2]
    timing[0]['words'][0][1] = 0.0
    timing[0]['t0'] = 0.0
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    os.makedirs(out, exist_ok=True)
    json.dump(timing, open(f'{out}/timing.json', 'w'), ensure_ascii=False, indent=0)
    json.dump([[w[0], round(w[1], 3), round(w[2], 3)] for w in aw], open(f'{out}/asr.json', 'w'), ensure_ascii=False)
    y = x / (np.abs(x).max() + 1e-9) * 0.95
    with wave.open(f'{out}/voix.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((y * 32767).astype(np.int16).tobytes())
    for li, L in enumerate(timing):
        print(f"{li:02d} {L['t0']:6.2f}-{L['t1']:6.2f} | {' '.join(w[0] for w in L['words'][:7])}")
    print('durée voix', round(dur, 2))
    print('ASR:', ' '.join(w[0] for w in aw))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.5, float(sys.argv[4]) if len(sys.argv) > 4 else 0.32)
