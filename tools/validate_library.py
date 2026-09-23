#!/usr/bin/env python3
from pathlib import Path
import csv,re,sys,collections
ROOT=Path(__file__).resolve().parents[1]; manifest=ROOT/'datasets'/'flagship-sources.csv'
with manifest.open(encoding='utf-8') as fh: rows=list(csv.DictReader(fh))
errors=[]
if len(rows)!=43:errors.append(f'expected 43 flagship rows, got {len(rows)}')
readme=(ROOT/'README.md').read_text(encoding='utf-8'); files=[]; sentence_docs=collections.defaultdict(set)
for r in rows:
 p=ROOT/r['category']/(r['slug']+'.md'); files.append(p)
 if not p.exists():errors.append(f'missing {p.relative_to(ROOT)}');continue
 text=p.read_text(encoding='utf-8')
 for key in ('english_source','romanian_source'):
  if r[key] not in text:errors.append(f'{p.relative_to(ROOT)} missing {key}')
 if f"{r['category']}/{r['slug']}.md" not in readme:errors.append(f'README missing {p.relative_to(ROOT)}')
 if 'Sources reviewed' not in text:errors.append(f'{p.relative_to(ROOT)} missing Sources reviewed')
 for bad in ('About the author','Related insights','Executive profile','This keeps the article tied to its own intent'):
  if bad in text:errors.append(f'{p.relative_to(ROOT)} contains blog/template residue: {bad}')
 # suspicious table extraction: heading followed by isolated field names rather than markdown table
 if re.search(r'(?im)^Implementation matrix\s*$[\s\S]{0,160}^Layer\s*$',text):errors.append(f'{p.relative_to(ROOT)} has flattened implementation matrix')
 for s in re.split(r'(?<=[.!?])\s+',re.sub(r'\s+',' ',text)):
  z=s.strip()
  if len(z)>=80 and not z.startswith('This repository version is designed as a reusable framework/checklist'):sentence_docs[z].add(str(p.relative_to(ROOT)))
for sent,docs in sentence_docs.items():
 if len(docs)>=8:errors.append(f'repeated sentence in {len(docs)} flagship docs: {sent[:90]}...')
for p in ROOT.rglob('*.md'):
 if '.git' not in p.parts and 'niculae-info-ai-search-frameworks' in p.read_text(encoding='utf-8'):errors.append(f'stale repo branding in {p.relative_to(ROOT)}')
print(f'library_rows={len(rows)} errors={len(errors)}')
for e in errors:print('ERROR',e)
sys.exit(1 if errors else 0)
