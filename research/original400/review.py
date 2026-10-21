from pathlib import Path
import json,copy,hashlib
BASE=Path(__file__).parent
old=json.loads((BASE/'before/questions.json').read_text());by={q['id']:q for q in old}
reviews={};patches={}
def batch(module,text):
 for line in text.strip().splitlines():
  parts=line.split('|');n,note=parts[:2];ident=f'FDE-{module}-{int(n):03}';assert ident in by and ident not in reviews,ident
  reviews[ident]={'id':ident,'finding':note,'decision':'revise' if len(parts)>2 else 'retain'}
  if len(parts)>2:patches[ident]={'stem':parts[2],'teachingNote':note}
def edit(ident,**kwargs):
 ident='FDE-'+ident;patches.setdefault(ident,{}).update(kwargs);reviews[ident]['decision']='revise'
