"""remplace des fonctions/constantes entières dans un fichier ; les nouvelles sont insérées avant la suivante existante."""
import sys, re

STOP = re.compile(r'(?m)^(def |class |[A-Z_][A-Z_0-9]* = |# -{10}|add\(|if __name__)')


def replace_funcs(path, new_src):
    s = open(path).read()
    blocks = re.split(r'(?m)^(?=def |[A-Z_][A-Z_0-9]* = )', new_src.strip('\n') + '\n')
    pending = ''
    for b in blocks:
        if not b.strip():
            continue
        m = re.match(r'def (\w+)\(', b)
        name = m.group(1) if m else re.match(r'([A-Z_][A-Z_0-9]*) = ', b).group(1)
        pat = re.compile(r'(?m)^def ' + name + r'\(') if m else re.compile(r'(?m)^' + name + r' = ')
        body = b.rstrip('\n') + '\n\n\n'
        mm = pat.search(s)
        if mm is None:
            pending += body
            continue
        i = mm.start()
        nxt = STOP.search(s, i + 5)
        j = nxt.start() if nxt else len(s)
        s = s[:i] + pending + body + s[j:]
        pending = ''
    if pending:
        s = s.rstrip('\n') + '\n\n\n' + pending
    open(path, 'w').write(s)


if __name__ == '__main__':
    replace_funcs(sys.argv[1], open(sys.argv[2]).read())
