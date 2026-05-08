from pathlib import Path
import re

root = Path('db')

pat = re.compile(r'\w+\.\w+\.tsv')
files = [p for p in root.glob('*.tsv') if pat.match(p.name)]

for src in files:
    print(src)
    dst = Path(root / f'{src.stem}.fixed.tsv')
    with src.open('r', encoding='utf-8') as fin, dst.open('w', encoding='utf-8') as fout:
        for i, line in enumerate(fin):
            if '\\t' in line:
                line = line.replace('\\t', '\t')
                print(i, end=' ')
            fout.write(line)
        print()
