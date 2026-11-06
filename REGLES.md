# Good2No — règles de fabrication (style PS1 3D maison)

Style : moteur PS1 maison (engine.py / lib.py), personnages Human articulés construits en code. PAS Blender, PAS pixel art 2D, PAS mannequins glTF.

Ce qui marche le mieux :
- Visages : aucun ou ultra simples (2 points pour les yeux, pas de bouche).
- Personnages en plan moyen/large, jamais de gros plan visage/mains.
- Objet tenu en main : suggéré, pas en gros plan (sinon objets qui flottent).
- 1 à 3 personnages par plan (+ foule en fond si besoin).
- Bâtiments simples MAIS décors remplis d'accessoires (caisses, bancs, lampadaires…) : jamais vide.
- Gestes simples : marcher, courir, tomber, montrer, assis, immobile.
- Plans variés et coupes toutes les 1-2 s (contre-plongée, vue du ciel, inserts), première seconde choc.
- CHAPEAUX : si un personnage porte un chapeau, on ne voit QUE le chapeau sur sa tête, jamais le crâne à travers.
  (codé dans lib.py : le crâne est coupé sous le chapeau + bandeau qui ferme le dessus — vérifier quand même vue de dessus)
- Rien qui flotte, textures propres.

## Lot 7 (5 nov. 2026) : ce qui est désormais la base -> dossier lot7/
- **Look PS1 obligatoire** : `from g2n7 import *` EN PREMIER (règle engine.PS1_MODE=True, 180x320 agrandi x6 sans lissage, visages 2 points).
- **Voix automatique** : `python3 lot7/tts7.py <nom>` appelle Gemini (clé dans ~/.g2n_key, jamais dans le dépôt), une requête par vidéo, balises de ton optionnelles dans BALISES de scripts7.py, puis lance align7.py tout seul.
- **Voix** : un seul wav Gemini par vidéo. `python3 lot7/align7.py <nom> <voix.wav> [silence_max] [silence_gardé]`
  -> coupe le blanc du début (voix dès 0,0 s), raccourcit les silences trop longs, ASR sherpa-onnx (zipformer fr, à télécharger
  depuis les releases GitHub k2-fsa/sherpa-onnx dans /home/claude/asr), timing.json mot par mot (décalage ASR -0,12 s corrigé).
  Les textes (sous-titres + texte lu) sont dans lot7/scripts7.py. Vérifier dans la sortie « ASR: » que Gemini n'a pas sauté de phrase.
- **Émeu à chapeau** : `emu_mesh(pos, yaw, scale_=..., peck=..., statue=couleur)` (vivant, figurine, statue) ; `emu_image()` = portrait 3/4 comme le logo.
- **Pastilles** (g2n7) : `emu_pastille(3.3, 3.2, y=300)` début, `end_card(t0, dur)` fin (« Alors, tu as trouvé l'émeu ? »),
  `retiens(t0, dur, y=300)` pour le « retiens bien ce détail » (boucle ouverte, payée plus tard dans la vidéo).
  Badges de date/lieu à y=700 (jamais y=150 : sous les onglets TikTok). Accroche C2.hook_title y=250 de 0 à 2,6 s.
- **Fin en boucle** : le dernier plan appelle le plan d'accroche avec p = lt - dur, la dernière image = la première.
- **Pas de musique** : seulement des bruitages (audio.py / common2.py).
- Rendu : `python3 video.py` (2 workers), `--sheet` planche contact, `--at 12.5 30` images isolées. Miniatures : `python3 lot7/thumbs7.py <nom>`
  (même résolution PS1 que les vidéos, 180x320 x6 : demandé le 6 nov.).
- Retours du 6 nov. à ne plus refaire : avion de ligne = props7.airliner() (fuselage, cockpit vitré, ailes épaisses, réacteurs, empennage) ;
  camion = props7.truck(roll=...) avec vitres (on voit le chauffeur) et roues à rayons qui tournent ; routes vues de haut surélevées
  (pas de scintillement avec le sol) ; draps pincés sur la corde, loin des personnages ; un morceau tenu en main doit aller jusqu'à la bouche ;
  le contenu d'un bocal doit être plus petit que le bocal ; une personne assise sur un lit a le bassin posé sur le matelas ;
  un objet porté se tient à deux mains (ik_r / ik_l) et la personne se tourne vers la caméra ; bâtiments : pas de fenêtre sur une porte,
  façades avec encadrements, perron, colonnes ; globe = vraie carte des continents (fleming/video.py : earth_sphere).
- Attention résolution basse : une corde/ficelle doit faire au moins 3-4 cm de rayon pour rester visible.

Options moteur :
- lib.SIMPLE_FACES = True  -> visages 2 points (à mettre avant d'importer world).
- Look PS1 renforcé (en test) : engine.PS1_MODE = True ; engine.W, engine.H, engine.UPS = 180, 320, 6
  (basse déf, sommets qui tremblent, textures affines). Exemple : PS1=1 python3 violet/test_regles.py

Méthode (usine, 6 nov. 2026) : Elian écrit « vidéo » -> Claude propose 10 sujets détaillés -> Elian en choisit 3 -> scripts (lot N/scriptsN.py) + voix Gemini automatique (tts7.py) -> rendu des 3 vidéos (V1) envoyé directement, sans validation intermédiaire -> retours d'Elian au format « temps + problème » -> V2 -> une fois validé : miniature, légende, hashtags, commentaire épinglé.
Codes TikTok : accroche choc 1re seconde, « abonne-toi » au milieu (voix + pastille logo), question en commentaire à la fin, tutoiement.

## Rétention & algorithme (validé par Elian, oct. 2026)
- FIN EN BOUCLE : la dernière image rejoint la première (même plan/cadrage) pour que la vidéo reparte sans coupure visible.
- Promesse dans les 0-2 s, contexte posé en moins de 10 s.
- « Abonne-toi » au milieu : 2 s maximum (voix courte + pastille logo).
- Chapitres à l'écran (« ACCIDENT 1/3 », « JOUR 1 »…) dès qu'il y a une progression.
- Toujours un rebondissement final juste avant la question en commentaire.
- Vidéos en SÉRIES (voir SERIES.md), avec « Épisode N » sur la miniature et dans la légende.

## Référencement (SEO TikTok)
- Le mot-clé principal (nom du sujet : Titanic, Hachikō…) est DIT dans les 5 premières secondes ET écrit à l'écran.
- Légende : mot-clé dans les 150 premiers caractères + 3 à 5 hashtags de niche (jamais 20).
- Commentaire épinglé par Elian dans la 1re heure (question qui lance le débat).
- Republier aussi en YouTube Shorts.

## Livrables à chaque vidéo
V1 puis V2 : la vidéo seule. Après validation : 1. Miniature (« Épisode N »)  2. Légende + 3 à 5 hashtags  3. Commentaire à épingler
