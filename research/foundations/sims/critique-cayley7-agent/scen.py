"""Critique 7 (agent) checks: runs design-g7/checks.py up to J30 unchanged (output suppressed), then new scripts.
A: a laugh at the end of the utterance that carries the bad news (misfortune; "I got fired today, haha"), gate read at his laugh onset.
B: silent panic, three codes. C: silent sadness and grief in each code's own face, no words. Run: python3 -I scen.py > out.txt (about 30 min here).
These numbers are what the design's equations give for stated inputs, not evidence about people."""
import io, os, contextlib, sys
import numpy as np
P7F = "/home/user/affect/research/foundations/sims/design-g7/checks.py"
src = open(P7F).read()
cut = src.index("# =========================================================== J30: the scenarios")
src = src[:cut]
g = {"__name__": "g7", "__file__": P7F}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "checks_g7", "exec"), g)
for k in ("Agent7","run6","U6","at_","show","GATE","PEOPLE6","Z6","G5","pop7","LAMV","echo","GK","x_at"):
    globals()[k]=g[k]
def OWN(t, lab): return {at_(t): {"own": "OWN: " + lab}}
def ev(*items):
    out={}
    for it in items:
        for k,v in it.items(): out.setdefault(k,{}).update(v)
    return out
def gate_t(rec,t): return next(r["gate"] for r in rec if r["t"]>=t)
print("A. misfortune: laugh at the end of the same utterance (utterance end 8.0 s, latch 8.6 s)")
ag=Agent7(); evs=ev(OWN(2,"how was your weekend?"), U6(8,z="my neighbour fell off his ladder and broke his leg, haha"), OWN(10.5,"Oh no, is he all right?"))
lfm=dict(LP=.6,CR=.4,BU_L=.5,RHY=.5)
rec=run6(ag,30,lambda t: lfm if (7.5<=t<11 or 14<=t<16) else dict(LP=.3),evs)
for t in (7.0,7.5,8.0,8.5,9.0,14.0):
    gv=gate_t(rec,t); print(f"  t {t}: gate {gv:.2f}; echo BU_L at onset .5 {echo(gv,'BU_L',.5):+.3f}, LP .3 {echo(gv,'LP',.3):+.3f}")
# own disclosure with troubles-resistant laugh, calm face
Z6["I got fired today, haha"]=(0.6,0.4,0.1,0.2,0.3,0.0)
G5["DEC"]["I got fired today, haha"]=pop7(Z6["I got fired today, haha"])
print("A2. calm face, 'I got fired today, haha' (first disclosure; laugh at its end)")
ag=Agent7(); evs=ev(OWN(2,"how was your weekend?"), U6(8,z="I got fired today, haha"))
rec=run6(ag,30,lambda t: dict(LP=.55,CR=.35,BU_L=.5,RHY=.5) if 7.5<=t<10 else dict(LP=.3),evs)
for t in (7.5,8.0,8.5,9.5):
    gv=gate_t(rec,t); print(f"  t {t}: gate {gv:.2f}; echo BU_L {echo(gv,'BU_L',.5):+.3f}")
print("B. silent panic, three codes: full face 0-90 s")
for kind in ("agent-like","low-expressive","different channels"):
    pp=PEOPLE6[kind][1]; f_=pp.code(V=.3,A=.9); ag=Agent7(person=pp); rec=run6(ag,90,lambda t,f_=f_: f_,{})
    show(kind,rec,5,90,["BI","BO","TILT","LP","EN","HG","post"]); print("   onsets",ag.onsets,"bid",getattr(ag,'bid_t',None))
print("C. quiet and different-channel codes: silently sad and crying (operator-after-months engine)")
for kind in ("agent-like","low-expressive","different channels"):
    pp=PEOPLE6[kind][1]
    for lab,V in (("silent sad",.6),("grief/crying",.9)):
        f_={k:v for k,v in pp.code(V=V,Tr=.2).items() if k not in ("FR","EN","RT")}
        ag=Agent7(person=pp); rec=run6(ag,120,lambda t,f_=f_: f_,{})
        show(f"{kind} {lab}",rec,0,120,["BI","TILT","LP","post"]); print("   onsets",ag.onsets,"offs",ag.offs)
