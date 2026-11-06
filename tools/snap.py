"""rend des images de test : snap(list of (mesh, cam, env)) -> planche"""
import sys
sys.path.insert(0, '/home/claude/g2n')
from engine import render, ps1_post
from PIL import Image
import numpy as np

def snap(items, out, cols=3, sc=0.5):
    ims = []
    for mesh, cam, env in items:
        img, _ = render(mesh, cam, env)
        im = Image.fromarray(ps1_post(img)).resize((int(270 * 4 * sc), int(480 * 4 * sc)), Image.NEAREST)
        ims.append(im)
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    S = Image.new('RGB', (cols * w, rows * h))
    for i, im in enumerate(ims):
        S.paste(im, ((i % cols) * w, (i // cols) * h))
    S.save(out)
