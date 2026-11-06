"""Voix off Good2No automatique avec Gemini (Google AI Studio), puis calage des sous-titres (align7.py).

usage : python3 lot7/tts7.py <nom> [--voix Charon] [--modele gemini-3.8-flash-tts] [--sans-calage]
        python3 lot7/tts7.py <nom> --requete req.json   -> écrit seulement la requête Gemini (à envoyer depuis le PC d'Elian)
        python3 lot7/tts7.py <nom> --depuis-wav voix.wav -> saute l'appel Gemini, convertit + cale un wav déjà généré

- <nom> : clé de ALL dans scripts7.py (ex. chaise). Le texte lu = le « texte lu » de chaque ligne
  (ou le sous-titre s'il vaut None), précédé des balises de ton de BALISES[<nom>][numéro de ligne] s'il y en a.
- Clé API : variable GEMINI_API_KEY, sinon ~/.g2n_key. Jamais dans le dépôt.
- Une seule requête par vidéo (économise le quota gratuit). Sortie : lot7/<nom>/voix_gemini.wav,
  puis align7.py produit lot7/<nom>/voix.wav + timing.json.
"""
import sys, os, json, base64, subprocess, argparse, time, wave
import urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scripts7

# Testé le 6 nov. 2026 : ce modèle LIT à voix haute toute consigne en texte (même « Lis comme un conteur : »),
# et refuse systemInstruction. Le ton se règle donc UNIQUEMENT avec les balises [shocked] [fast]… devant les lignes.


def api_key():
    k = os.environ.get('GEMINI_API_KEY')
    p = os.path.expanduser('~/.g2n_key')
    if not k and os.path.exists(p):
        k = open(p).read().strip()
    if not k:
        sys.exit("Pas de clé Gemini : mets-la dans ~/.g2n_key")
    return k


def body_for(text, voice):
    return {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {"responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}},
    }


def synth(text, voice, model, key, tries=3):
    body = body_for(text, voice)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    d = None
    for n in range(tries):
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"x-goog-api-key": key, "Content-Type": "application/json"})
        try:
            d = json.load(urllib.request.urlopen(req, timeout=300))
            part = d['candidates'][0]['content']['parts'][0]['inlineData']
            return base64.b64decode(part['data']), part.get('mimeType', '')
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors='replace')[:600]
            if e.code == 429:
                sys.exit("QUOTA : quota gratuit Gemini atteint (429). Réessayer plus tard ou demain.\n" + msg)
            if e.code in (500, 502, 503, 504) and n < tries - 1:
                time.sleep(5 * (n + 1)); continue
            sys.exit(f"Erreur Gemini {e.code} : {msg}")
        except (KeyError, IndexError):
            if n < tries - 1:
                time.sleep(3); continue
            sys.exit("Réponse Gemini sans audio : " + json.dumps(d)[:600])


def texte_lu(name):
    tags = getattr(scripts7, 'BALISES', {}).get(name, {})
    out = []
    for i, (sub, spoken) in enumerate(scripts7.ALL[name]):
        t = spoken if spoken else sub
        out.append((tags.get(i, '') + ' ' + t).strip())
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name')
    ap.add_argument('--voix', default='Charon')
    ap.add_argument('--modele', default='gemini-3.8-flash-tts')
    ap.add_argument('--sans-calage', action='store_true')
    ap.add_argument('--requete')
    ap.add_argument('--depuis-wav')
    a = ap.parse_args()

    if a.requete:
        json.dump(body_for(texte_lu(a.name), a.voix), open(a.requete, 'w'), ensure_ascii=False)
        print('requête écrite :', a.requete); return
    out = os.path.join(HERE, a.name)
    os.makedirs(out, exist_ok=True)
    raw = os.path.join(out, 'voix_brute.wav')
    if a.depuis_wav:
        subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', a.depuis_wav, raw])
    else:
        data, mime = synth(texte_lu(a.name), a.voix, a.modele, api_key())
        if data[:4] == b'RIFF':          # Gemini renvoie déjà un wav
            open(raw, 'wb').write(data)
        else:                            # PCM brut 16 bits
            rate = int(mime.split('rate=')[1].split(';')[0]) if 'rate=' in mime else 24000
            with wave.open(raw, 'wb') as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(data)
    wav = os.path.join(out, 'voix_gemini.wav')   # align7 attend du 24 kHz mono
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-ar', '24000', '-ac', '1', wav])
    os.remove(raw)
    with wave.open(wav) as w:
        print(f"voix_gemini.wav : {w.getnframes() / w.getframerate():.1f} s (voix {a.voix}, {a.modele})")
    if not a.sans_calage:
        subprocess.check_call([sys.executable, os.path.join(HERE, 'align7.py'), a.name, wav])


if __name__ == '__main__':
    main()
