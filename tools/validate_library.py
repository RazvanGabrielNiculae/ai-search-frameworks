#!/usr/bin/env python3
from pathlib import Path
import csv, re, sys
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'datasets'/'flagship-sources.csv'
rows=list(csv.DictReader(manifest.open(encoding='utf-8')))
errors=[]
if len(rows)!=43: errors.append(f'expected 43 flagship rows, got {len(rows)}')
readme=(ROOT/'README.md').read_text(encoding='utf-8')
for r in rows:
    p=ROOT/r['category']/(r['slug']+'.md')
    if not p.exists(): errors.append(f'missing {p.relative_to(ROOT)}'); continue
    text=p.read_text(encoding='utf-8')
    for key in ('english_source','romanian_source'):
        if r[key] not in text: errors.append(f'{p.relative_to(ROOT)} missing {key}')
    if f"{r['category']}/{r['slug']}.md" not in readme: errors.append(f'README missing {p.relative_to(ROOT)}')
for p in ROOT.rglob('*.md'):
    if '.git' in p.parts: continue
    text=p.read_text(encoding='utf-8')
    if 'niculae-info-ai-search-frameworks' in text: errors.append(f'stale repo branding in {p.relative_to(ROOT)}')
print(f'library_rows={len(rows)} errors={len(errors)}')
for e in errors: print('ERROR',e)
sys.exit(1 if errors else 0)
