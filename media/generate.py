#!/usr/bin/env python3
"""Source for Venkat-RJ's animated GitHub research notebook.
Original illustrations, SVG SMIL animation, no JS or external assets.
Run: python generate.py
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent
DURATION = 32.0

PALETTES = {
    "dark": {
        "paper": "#111518", "sheet": "#181E20", "sheet2": "#222A2B", "ink": "#F0EAE0",
        "quiet": "#ADB3AC", "dim": "#7D8B86", "rule": "#3C4544", "grid": "#303A3A",
        "ochre": "#E2C56B", "coral": "#F18B7A", "mint": "#96CFAF", "white": "#F2E6D5",
        "shadow": "#06090A", "stamp": "#DF8174",
    },
    "light": {
        "paper": "#F5F2EA", "sheet": "#FCFAF4", "sheet2": "#EDE9DE", "ink": "#232A2B",
        "quiet": "#556462", "dim": "#73847E", "rule": "#BCC6BE", "grid": "#E1E5DD",
        "ochre": "#9C741C", "coral": "#BE564B", "mint": "#347F65", "white": "#FCF9F0",
        "shadow": "#A8B0A7", "stamp": "#CF6659",
    },
}

def attrs(d: dict) -> str:
    return " ".join(f'{k}="{escape(str(v), {chr(34): "&quot;"})}"' for k, v in d.items())

def el(tag: str, content: str = "", **kw) -> str:
    return f"<{tag} {attrs(kw)}>{content}</{tag}>" if content else f"<{tag} {attrs(kw)}/>"

def text(x, y, s, p, font=15, weight=400, fill="ink", family="sans", **extra):
    families={"sans":"'Helvetica Neue', Arial, sans-serif", "mono":"'SFMono-Regular', Consolas, 'Liberation Mono', monospace", "serif":"Georgia, 'Times New Roman', serif"}
    props={"x":x,"y":y,"fill":p.get(fill,fill),"font-size":font,"font-weight":weight,"font-family":families[family]}
    props.update(extra)
    return el("text",escape(s),**props)

def anim(attr, frames, **more):
    assert frames[0][0] == 0 and frames[-1][0] == DURATION, frames
    assert all(frames[i][0]<frames[i+1][0] for i in range(len(frames)-1)), frames
    props={"attributeName":attr,"values":";".join(str(v) for _,v in frames),
           "keyTimes":";".join(f"{t/DURATION:.6f}" for t,_ in frames),
           "dur":f"{DURATION:g}s","repeatCount":"indefinite","calcMode":"linear"}
    props.update(more)
    return el("animate","",**props)

def trans(kind, frames):
    return el("animateTransform","",attributeName="transform",attributeType="XML",type=kind,
              values=";".join(str(v) for _,v in frames),
              keyTimes=";".join(f"{t/DURATION:.6f}" for t,_ in frames),
              dur=f"{DURATION:g}s",repeatCount="indefinite",calcMode="linear",additive="replace")

def oval(cx,cy,rx,ry,color,**kw): return el("ellipse","",cx=cx,cy=cy,rx=rx,ry=ry,fill=color,**kw)
def rect(x,y,w,h,color,**kw): return el("rect","",x=x,y=y,width=w,height=h,fill=color,**kw)
def circle(cx,cy,r,color,**kw): return el("circle","",cx=cx,cy=cy,r=r,fill=color,**kw)
def path(d,p,color="none",stroke="ink",sw=2,**kw): return el("path","",d=d,fill=p.get(color,color),stroke=p.get(stroke,stroke),**{"stroke-width":sw,"stroke-linecap":"round","stroke-linejoin":"round",**kw})

def fade(*points):
    """Opacity animation; frame sequences (timestamp, numeric opacity)."""
    frames=list(points)
    assert frames[0][0]==0 and frames[-1][0]==DURATION
    return anim("opacity",frames)

def label_group(p, label, x,y,start,end,color="quiet",font=11):
    # short held duration, 0.07 second in and out
    fade_frames=([(0,1),(end,1),(min(31.98,end+0.07),0),(30.37,0),(30.48,1),(32,1)] if start==0 else [(0,0),(max(0,start-0.06),0),(start,1),(end,1),(min(31.98,end+0.07),0),(32,0)])
    assert all(fade_frames[i][0]<fade_frames[i+1][0] for i in range(len(fade_frames)-1))
    return el("g",fade(*fade_frames)+text(x,y,label,p,font,600,color,"mono"),opacity=0)

def bot(p):
    ink=p['ink']; yellow=p['ochre']; paper=p['paper']; white=p['white']; quiet=p['quiet']
    # Agent is a pencil-sized, one-eyed lab doodle, not an AI humanoid avatar.
    pieces=[]
    pieces.append(oval(0,24,24,5,p['shadow'],opacity="0.42"))
    # backpack
    pieces.append(rect(-23,-3,12,25,yellow,rx=4,stroke=ink,**{"stroke-width":1.7}))
    # legs alternate so it has a distinctive walk cycle
    legleft=path("M -9 15 L -12 24 L -21 24",p,stroke="ink",sw=3.4)
    legright=path("M 10 15 L 13 24 L 22 24",p,stroke="ink",sw=3.4)
    pieces.append(el("g",trans("rotate",[(0,"0 -8 17"),(2,"0 -8 17"),(2.4,"-17 -8 17"),(2.8,"10 -8 17"),(3.4,"0 -8 17"),(4,"-12 -8 17"),(5,"0 -8 17"),(7,"0 -8 17"),(8.4,"30 -8 17"),(10,"0 -8 17"),(12,"0 -8 17"),(13.2,"-12 -8 17"),(15,"0 -8 17"),(22,"0 -8 17"),(27.5,"0 -8 17"),(32,"0 -8 17")])+legleft))
    pieces.append(el("g",trans("rotate",[(0,"0 8 17"),(2,"0 8 17"),(2.5,"15 8 17"),(3,"-10 8 17"),(3.5,"0 8 17"),(4,"10 8 17"),(5,"0 8 17"),(7,"0 8 17"),(8.4,"-30 8 17"),(10,"0 8 17"),(12,"0 8 17"),(13.2,"10 8 17"),(15,"0 8 17"),(22,"0 8 17"),(27.5,"0 8 17"),(32,"0 8 17")])+legright))
    # body / white tiled face
    pieces.append(rect(-19,-23,38,42,white,rx=13,stroke=ink,**{"stroke-width":2.3}))
    pieces.append(path("M -12 -19 L -6 -26 L 8 -26 L 14 -18",p,stroke="ink",sw=1.6))
    pieces.append(rect(-16,3,32,5,yellow,rx=2))
    # one eye with tiny pupil moving to investigation later
    pieces.append(circle(3,-10,9,paper,stroke=ink,**{"stroke-width":2}))
    pupil=circle(6,-10,3.4,ink)
    pieces.append(el("g",trans("translate",[(0,"0 0"),(6,"0 0"),(7,"-3 0"),(8.1,"0 -2"),(11,"-4 0"),(13,"3 0"),(18,"0 0"),(21,"3 0"),(26,"0 0"),(32,"0 0")])+pupil))
    # blinking eyelid
    lid=path("M -5 -10 Q 3 -15 11 -10",p,stroke="ink",sw=2.8)
    pieces.append(el("g",fade((0,0),(1.48,0),(1.52,1),(1.72,0),(5.9,0),(6,1),(6.13,0),(17.9,0),(18,1),(18.16,0),(32,0))+lid,opacity=0))
    # mouth smiles, then shocked, then smile again
    smile=path("M -3 5 Q 2 10 8 4",p,stroke="ink",sw=1.9)
    pieces.append(el("g",fade((0,1),(7.8,1),(8.05,0),(13,0),(13.2,1),(32,1))+smile,opacity=1))
    surprise=oval(3,6,2.6,4,paper,stroke=ink,**{"stroke-width":1.3})
    pieces.append(el("g",fade((0,0),(8,0),(8.05,1),(12.6,1),(12.8,0),(32,0))+surprise,opacity=0))
    # antenna w/ little amber dot
    pieces.append(path("M 0 -23 L 3 -33 L 13 -37",p,stroke="ink",sw=2))
    pieces.append(circle(13,-37,4,yellow,stroke=ink,**{"stroke-width":1}))
    # arms, left carries pencil, right later offers high five
    armleft=path("M -18 -1 Q -30 0 -30 12",p,stroke="ink",sw=3)
    pieces.append(el("g",trans("rotate",[(0,"0 -18 -1"),(3,"0 -18 -1"),(4,"-18 -18 -1"),(5,"-10 -18 -1"),(6,"0 -18 -1"),(8.3,"65 -18 -1"),(10,"0 -18 -1"),(14,"-18 -18 -1"),(20,"0 -18 -1"),(32,"0 -18 -1")])+armleft))
    armright=path("M 19 -1 Q 32 0 32 -13",p,stroke="ink",sw=3)
    pieces.append(el("g",trans("rotate",[(0,"0 18 -1"),(3,"0 18 -1"),(4,"-35 18 -1"),(5,"-15 18 -1"),(8,"0 18 -1"),(9,"60 18 -1"),(12,"10 18 -1"),(14,"0 18 -1"),(21,"-25 18 -1"),(24,"-65 18 -1"),(25,"0 18 -1"),(32,"0 18 -1")])+armright))
    # character travel and tumble, slight squash before jump
    body=el("g","".join(pieces),id="little-investigator")
    tilt=el("g",trans("rotate",[(0,"0"),(7.8,"0"),(8.45,"83"),(9.6,"88"),(10.6,"15"),(11.5,"0"),(22,"0"),(23.6,"-12"),(24.2,"0"),(32,"0")])+body,id="agent-tilt")
    squish=el("g",trans("scale",[(0,"1 1"),(2,"1 1"),(2.2,"1.12 0.82"),(2.5,"0.93 1.08"),(2.8,"1 1"),(7.7,"1 1"),(8.3,"1.28 0.72"),(9.2,"1 1"),(22.1,"1 1"),(22.3,"1.14 0.86"),(23,"1 1"),(32,"1 1")])+tilt,id="agent-squash")
    track=[(0,"480 345"),(1.7,"480 345"),(2.12,"470 260"),(2.65,"495 249"),(3.25,"505 250"),(4.2,"530 246"),(5.2,"557 241"),(5.7,"568 244"),(6.5,"583 240"),(7.4,"606 248"),(8.0,"632 251"),(8.43,"641 274"),(9.3,"651 274"),(10.6,"650 263"),(11.7,"625 249"),(12.9,"572 248"),(13.8,"579 245"),(16,"589 245"),(18,"596 246"),(21,"616 246"),(23,"665 248"),(24.2,"710 245"),(25.4,"744 248"),(26.3,"763 252"),(27,"777 265"),(28,"790 340"),(32,"480 345")]
    travel=el("g",trans("translate",track)+squish,transform="translate(480 345)",id="agent-travel")
    return travel

def validator(p):
    ink=p['ink']; red=p['stamp']; white=p['white']
    parts=[]
    # A tiny personified rubber stamp with grumpy eyebrows, changing its mind after verification.
    parts.append(rect(-28,-24,56,36,red,rx=6,stroke=ink,**{"stroke-width":2.2}))
    parts.append(rect(-22,-38,44,16,p['sheet2'],rx=5,stroke=ink,**{"stroke-width":2}))
    parts.append(rect(-15,-49,30,13,p['sheet2'],rx=6,stroke=ink,**{"stroke-width":2}))
    parts.append(rect(-34,11,68,9,red,rx=3,stroke=ink,**{"stroke-width":2}))
    parts.append(circle(-10,-10,3.8,ink));parts.append(circle(10,-10,3.8,ink))
    parts.append(path("M -17 -17 L -5 -13 M 5 -13 L 17 -17",p,stroke="ink",sw=2.3))
    parts.append(path("M -7 3 Q 0 0 7 3",p,stroke="ink",sw=1.7))
    parts.append(path("M -33 -5 L -45 -9 M 33 -5 L 45 -9",p,stroke="ink",sw=2.2))
    parts.append(path("M -16 20 L -20 27 L -26 27 M 16 20 L 19 27 L 26 27",p,stroke="ink",sw=2.2))
    core=el("g","".join(parts))
    lean=el("g",trans("rotate",[(0,"-15"),(7.0,"-15"),(7.8,"8"),(8.2,"-8"),(8.4,"0"),(10,"0"),(11.2,"-12"),(12.8,"0"),(22,"0"),(23.2,"-15"),(24,"0"),(28,"0"),(32,"-15")])+core)
    travel=[(0,"750 -100"),(6.75,"750 -100"),(7.45,"748 160"),(7.75,"748 142"),(8.1,"748 161"),(8.4,"748 155"),(9.7,"741 155"),(10.1,"731 175"),(11,"725 187"),(12.4,"763 202"),(13.2,"798 209"),(19.5,"798 209"),(20.7,"785 197"),(22,"773 155"),(23.1,"742 155"),(23.5,"734 150"),(24,"745 155"),(25.5,"785 188"),(26.8,"815 245"),(27.9,"885 330"),(31.9,"885 330"),(32,"750 -100")]
    return el("g",trans("translate",travel)+lean,transform="translate(750 -100)",id="validator")

def status(p, s, color,start,end):
    return label_group(p,s,849,84,start,end,color,10).replace('font-family="\'SFMono-Regular\', Consolas, \'Liberation Mono\', monospace"', 'font-family="\'SFMono-Regular\', Consolas, \'Liberation Mono\', monospace" text-anchor="end"')

def build(theme):
    p=PALETTES[theme]
    parts=[]
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="340" viewBox="0 0 900 340" role="img" aria-labelledby="title description">')
    parts.append('<title id="title">Venkat Reddy, research notebook</title>')
    parts.append('<desc id="description">An original looping animation: a little researcher tests a hypothesis, celebrates too early, fails replication, examines a missing control, reruns experiments, and documents a bounded result. Research is a process, not a victory graphic.</desc>')
    parts.append('<defs><clipPath id="experiment-window"><rect x="421" y="65" width="451" height="240" rx="1"/></clipPath></defs>')
    parts.append(rect(0,0,900,340,p['paper']))
    parts.append(rect(15,15,870,310,"none",rx=2,stroke=p['rule'],**{"stroke-width":1}))
    # outer furniture: folio marks and rule
    parts.append(text(36,43,"VR  /  FIELD NOTES",p,11,700,"ochre","mono",**{"letter-spacing":1.5}))
    parts.append(text(863,43,"RESEARCH LOG     001 / ∞",p,10,500,"dim","mono",**{"text-anchor":"end"}))
    parts.append(path("M 34 58 H 866",p,stroke="rule",sw=1))
    parts.append(text(36,101,"VENKAT",p,49,600,"ink","serif",**{"letter-spacing":-1.2}))
    parts.append(text(36,148,"REDDY",p,49,600,"ink","serif",**{"letter-spacing":-1.2}))
    parts.append(rect(37,167,42,3,p['ochre']))
    parts.append(text(36,199,"Researching systems that",p,17,400,"quiet"))
    parts.append(text(36,222,"can test their own ideas.",p,17,400,"quiet"))
    parts.append(text(36,271,"AUTONOMOUS RESEARCH",p,10,650,"dim","mono",**{"letter-spacing":0.6}))
    parts.append(text(36,289,"OPTIMIZATION  /  RELIABLE AI",p,10,650,"dim","mono",**{"letter-spacing":0.25}))
    # Main notebook stage panel
    parts.append(rect(420,65,451,240,p['sheet'],rx=2,stroke=p['rule'],**{"stroke-width":1.3}))
    parts.append(rect(420,65,451,29,p['sheet2']))
    parts.append(text(435,84,"EXPERIMENT  /  001",p,10,800,"quiet","mono"))
    parts.append(circle(733,79,3.5,p['ochre']))
    parts.append(status(p,"UNTESTED", "quiet", 0,4.83))
    parts.append(status(p,"LOOKS GOOD!", "mint",4.85,7.38))
    parts.append(status(p,"NOT REPLICATED", "coral",7.4,12.95))
    parts.append(status(p,"CONTROLLED RE-RUN", "ochre",13,21.92))
    parts.append(status(p,"CHECKED  /  SCOPED", "mint",21.95,27.33))
    parts.append(status(p,"READY FOR NEXT IDEA", "quiet",27.35,30.22))
    # very subtle graph paper; no grids outside the stage
    stage=[]
    for x in range(443,859,31):
        stage.append(path(f"M {x} 98 V 288",p,stroke="grid",sw=.65))
    for y in range(112,294,25):
        stage.append(path(f"M 436 {y} H 860",p,stroke="grid",sw=.65))
    stage.append(path("M 452 221 H 853",p,stroke="rule",sw=1.4))
    stage.append(path("M 465 119 V 269",p,stroke="rule",sw=1.2))
    stage.append(text(480,116,"NOTES / WORKSPACE",p,10,500,"dim","mono"))
    # pad at left of stage, physical sticky note agent pushes
    stage.append(rect(478,136,137,73,p['sheet2'],rx=3,stroke=p['rule'],**{"stroke-width":1.1}))
    stage.append(text(491,158,"HYPOTHESIS",p,10,800,"ochre","mono"))
    stage.append(text(491,180,"This might work.",p,12,500,"ink"))
    stage.append(path("M 491 190 L 579 190",p,stroke="rule",sw=1))
    # label note scribble moves upward as agent drags it
    idea=text(0,0,"!",p,24,800,"ochre","serif")
    stage.append(el("g",trans("translate",[(0,"509 151"),(3,"509 151"),(4,"518 147"),(5,"554 133"),(5.9,"591 121"),(6.5,"601 110"),(7.7,"601 110"),(7.9,"615 131"),(8.2,"629 190"),(10,"629 190"),(10.3,"580 272"),(12,"580 272"),(13,"509 151"),(32,"509 151")])+fade((0,0),(2.9,0),(3.1,1),(8,1),(9,0),(32,0))+idea,id="optimistic-idea"))
    # plotting area line, simple non-quantified fictional illustration
    stage.append(text(649,127,"OBSERVED RESULT",p,9,750,"dim","mono"))
    stage.append(path("M 642 214 H 841",p,stroke="quiet",sw=1,**{"stroke-dasharray":"4 5"}))
    stage.append(text(843,209,"baseline",p,9,500,"dim","mono",**{"text-anchor":"end"}))
    # early apparent success, line is drawn and then erased by replication
    early=path("M 644 210 C 672 201 682 214 697 175 S 733 146 747 159 S 780 120 814 135",p,stroke="mint",sw=3.2,**{"stroke-dasharray":"280 280","stroke-dashoffset":"280"})
    early=early[:-2]+">"+anim("stroke-dashoffset",[(0,280),(4.95,280),(6.45,0),(8.0,0),(8.13,280),(32,280)])+"</path>"
    stage.append(el("g",fade((0,0),(4.91,0),(5,1),(8.06,1),(8.20,0),(32,0))+early,id="premature-win",opacity=0))
    # fast cartoon star shapes bursting for a moment, restrained palette
    for i,(x,y,r) in enumerate([(693,132,5),(745,106,6),(797,127,4),(822,162,5),(674,159,3)]):
        star=path(f"M {x-r} {y} L {x+r} {y} M {x} {y-r} L {x} {y+r}",p,stroke="ochre",sw=2.4)
        stage.append(el("g",fade((0,0),(6+i*.10,0),(6.1+i*.10,1),(7.05+i*.06,1),(7.8,0),(32,0))+star,opacity=0))
    # red rejection line, strike through the questionable result
    wrong=path("M 675 145 L 810 188",p,stroke="coral",sw=3.1)+path("M 809 145 L 675 188",p,stroke="coral",sw=3.1)
    stage.append(el("g",fade((0,0),(7.65,0),(8.1,1),(11.6,1),(12.1,0),(32,0))+wrong,opacity=0))
    # overlooked assumption appears as a magnified line entry and gets circled
    assumption=rect(475,138,178,59,p['sheet2'],rx=3,stroke=p['coral'],**{"stroke-width":1.5})
    assumption+=text(485,158,"FOUND THE PROBLEM",p,10,800,"coral","mono")
    assumption+=text(485,178,"Missing control.",p,14,700,"ink")
    assumption+=circle(621,173,13,"none",stroke=p['coral'],**{"stroke-width":2})
    stage.append(el("g",fade((0,0),(10.9,0),(11.4,1),(13.2,1),(13.5,0),(32,0))+assumption,opacity=0))
    # magnifying glass sweeps in bot's hand
    mag=circle(0,0,18,"none",stroke=p['ochre'],**{"stroke-width":3.5})+path("M 12 13 L 28 31",p,stroke="ochre",sw=4.5)
    stage.append(el("g",trans("translate",[(0,"550 320"),(10.3,"550 320"),(10.8,"535 194"),(11.6,"585 172"),(12.3,"620 169"),(13.1,"535 312"),(32,"550 320")])+fade((0,0),(10.2,0),(10.5,1),(12.6,1),(13.1,0),(32,0))+mag,opacity=0))
    # re-run panel with clear, honest controls
    rerun=rect(479,132,145,83,p['sheet2'],rx=3,stroke=p['rule'],**{"stroke-width":1.2})
    rerun+=text(490,153,"CHANGE ONE THING",p,10,800,"ochre","mono")
    rerun+=rect(489,165,10,10,"none",stroke=p['mint'],**{"stroke-width":1.4})+path("M 491 170 L 495 174 L 503 163",p,stroke="mint",sw=2)
    rerun+=text(505,174,"same baseline",p,11,500,"ink")
    rerun+=rect(489,184,10,10,"none",stroke=p['mint'],**{"stroke-width":1.4})+path("M 491 189 L 495 193 L 503 182",p,stroke="mint",sw=2)
    rerun+=text(505,193,"same budget",p,11,500,"ink")
    stage.append(el("g",fade((0,0),(13.1,0),(13.6,1),(22,1),(22.3,0),(32,0))+rerun,opacity=0))
    # three replay traces shown sequentially with discrete colors and distinct trajectories
    traces=[("M 648 209 Q 698 183 725 185 T 818 164",15.1,16.2),
            ("M 648 209 Q 689 201 729 188 T 818 175",16.8,17.9),
            ("M 648 209 Q 699 198 726 190 T 818 181",18.5,19.6)]
    for i,(d,start,finish) in enumerate(traces):
        trace=path(d,p,stroke=["mint","ochre","quiet"][i],sw=2.4,opacity="0.92",**{"stroke-dasharray":"270 270","stroke-dashoffset":"270"})
        trace=trace[:-2]+">"+anim("stroke-dashoffset",[(0,270),(start,270),(finish,0),(22,0),(22.4,270),(32,270)])+"</path>"
        stage.append(el("g",fade((0,0),(start-.12,0),(start,1),(22.2,1),(22.5,0),(32,0))+trace,opacity=0))
        stage.append(label_group(p,f"RUN {i+1}",653+i*65,250,start,22.2,["mint","ochre","quiet"][i],9))
    # final stamped note rather than victory metric
    conclusion=rect(492,133,345,107,p['sheet2'],rx=4,stroke=p['rule'],**{"stroke-width":1.2})
    conclusion+=text(508,157,"RESEARCH NOTE  /  001",p,11,800,"ochre","mono")
    conclusion+=text(508,179,"Claim: improvement observed",p,13,650,"ink")
    conclusion+=text(508,199,"Scope: tested configurations",p,12,500,"quiet")
    conclusion+=text(508,218,"Evidence: saved and checked",p,12,500,"quiet")
    stage.append(el("g",fade((0,0),(21.2,0),(21.7,1),(27.1,1),(27.4,0),(32,0))+conclusion,opacity=0))
    # validation stamp from the tiny adversary
    stamp=el("g",trans("rotate",[(0,"-17 0 0"),(22,"-17 0 0"),(22.8,"0 0 0"),(23.3,"-8 0 0"),(24,"0 0 0"),(32,"-17 0 0")])+rect(-55,-16,110,31,"none",rx=4,stroke=p['mint'],**{"stroke-width":2.4})+text(0,6,"CHECKED ✓",p,15,800,"mint","mono",**{"text-anchor":"middle"}),id="checked-stamp")
    stage.append(el("g",trans("translate",[(0,"757 109"),(21.95,"757 109"),(22.4,"753 155"),(23,"733 167"),(24,"732 168"),(27,"732 168"),(27.5,"732 168"),(32,"757 109")])+fade((0,0),(22,0),(22.36,1),(26.6,1),(27,0),(32,0))+stamp,opacity=0))
    # round impact lines, quick anticipation and impact
    impact=path("M 687 131 L 668 121 M 691 115 L 683 98 M 786 131 L 804 121",p,stroke="coral",sw=2.8)
    stage.append(el("g",fade((0,0),(7.58,0),(7.65,1),(8.2,0),(32,0))+impact,opacity=0))
    stage.append(validator(p))
    stage.append(bot(p))
    # narrator strip along bottom of workspace, different humorous subheadings over the sequence
    strip=rect(433,278,422,22,p['sheet2'],rx=1)
    stage.append(strip)
    for lbl,start,end in [
      ("01 / A promising idea",0,4.78),
      ("02 / Victory declared too soon",4.82,7.35),
      ("03 / The result fights back",7.38,10.95),
      ("04 / Check your assumptions",11,13.28),
      ("05 / Replicate under controls",13.32,21.0),
      ("06 / Record what the evidence supports",21.05,27.2),
      ("07 / On to the next question",27.25,30.22),
    ]:
        stage.append(label_group(p,lbl,444,293,start,end,"quiet",10))
    # stage is clipped to the notebook: bot cannot protrude into profile text
    parts.append(el("g","".join(stage),**{"clip-path":"url(#experiment-window)"}))
    # bottom footer line / author index
    parts.append(path("M 34 309 H 866",p,stroke="rule",sw=1))
    parts.append(text(36,320,"NOT A DEMO OF A REAL EXPERIMENT. THE WORK BELOW IS.",p,8.8,500,"dim","mono"))
    parts.append(text(863,320,"VENKAT-RJ / GITHUB",p,9,550,"dim","mono",**{"text-anchor":"end"}))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"

def static_from(animated: str)->str:
    import re
    s=re.sub(r"<animate(?:Transform)?\s[^>]+/>","",animated)
    s=s.replace("looping animation:","still illustration representing a looping animation:")
    # This is a static cover, default positions are the pre-animation states.
    return s

if __name__=="__main__":
    for theme in PALETTES:
        s=build(theme)
        (OUT/f"experiment-{theme}.svg").write_text(s,encoding="utf-8")
        (OUT/f"experiment-{theme}-static.svg").write_text(static_from(s),encoding="utf-8")
        print(f"{theme}: {len(s):,} bytes, {s.count('<animate'):,} SMIL tracks")
