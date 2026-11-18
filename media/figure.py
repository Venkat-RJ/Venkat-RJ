"""A directly reproducible figure from FrontierOR's 30 fresh-instance study.
Source: https://github.com/Venkat-RJ/openresearch/blob/main/frontieror/scheduling-study/assets/final-instance-data.csv
The CSV in this directory is a snapshot of that source. Lower weighted tardiness is better.
"""
import csv
from pathlib import Path
from xml.sax.saxutils import escape
from generate import PALETTES, text, rect, path, circle

ROOT=Path(__file__).resolve().parent
DATA=list(csv.DictReader((ROOT/'frontieror-instances.csv').open()))
ORDER=['tf3/2-uniform','tf3/2-priority','tf7/4-uniform','tf7/4-priority','tf2-uniform','tf2-priority']
LABELS=['tightness 1.5   /   uniform','tightness 1.5   /   priority','tightness 1.75  /   uniform','tightness 1.75  /   priority','tightness 2.0   /   uniform','tightness 2.0   /   priority']

def build(theme):
 p=PALETTES[theme]
 o=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="328" viewBox="0 0 900 328" role="img" aria-labelledby="title desc">',
 '<title id="title">FrontierOR, 30 fresh scheduling instances</title>',
 '<desc id="desc">Each dot is an instance, positioned by normalized mean objective difference. Twenty-nine instances favored the frozen solver and one favored the historical EGRASP comparator. The comparison is restricted to this study.</desc>']
 o.append(rect(0,0,900,328,p['sheet'],rx=2,stroke=p['rule'],**{'stroke-width':1}))
 o.append(text(27,30,'FRONTIEROR   /   FROZEN STUDY',p,11,700,'ochre','mono',**{'letter-spacing':1}))
 o.append(text(27,60,'30 fresh scheduling instances',p,27,600,'ink','serif'))
 o.append(text(873,40,'29 / 30',p,28,700,'mint','serif',**{'text-anchor':'end'}))
 o.append(text(872,57,'comparisons won',p,11,500,'quiet',**{'text-anchor':'end'}))
 x0=262; xr=844; low=-5; high=25
 xof=lambda v:x0+(v-low)/(high-low)*(xr-x0)
 for t in range(-5,26,5):
  x=xof(t)
  o.append(path(f'M {x:.1f} 81 V 280',p,stroke='rule' if t==0 else 'grid',sw=1.45 if t==0 else .75))
  o.append(text(round(x,1),302,f'{t:+d}%',p,10,700 if t==0 else 400,'quiet','mono',**{'text-anchor':'middle'}))
 for i,group in enumerate(ORDER):
  y=101+i*29
  o.append(text(25,y+3,LABELS[i],p,12,550,'quiet','mono'))
  if i>0: o.append(path(f'M 26 {y-16} H 871',p,stroke='grid',sw=.8))
  subset=[float(r['normalized_advantage'])*100 for r in DATA if r['stratum']==group]
  for j,v in enumerate(subset):
   x=xof(v)
   jitter=[-7,-3,0,4,7][j]
   o.append(circle(round(x,2),y+jitter,4.4,p['mint'] if v>0 else p['coral'],stroke=p['sheet'],**{'stroke-width':.8}))
 # legend and sober caption
 o.append(text(27,324,'Right of zero = better mean weighted tardiness for the frozen solver. Synthetic data; historical reference.',p,10,400,'dim','sans'))
 o.append('</svg>')
 return '\n'.join(o)+'\n'

if __name__=='__main__':
 assert len(DATA)==30
 assert sum(float(r['normalized_advantage'])>0 for r in DATA)==29
 assert sum(float(r['normalized_advantage'])<0 for r in DATA)==1
 for k in PALETTES:
  p=ROOT/f'frontieror-{k}.svg'
  p.write_text(build(k))
  print(p, p.stat().st_size, 'bytes')
