"""Critique 3 (agent): extra scenarios on revision 3's own drive engine (G4-G7 code in ../design-g3/checks.py,
lines 1-53 and 330-466, executed unchanged). Consistency with the design's equations only; not evidence about people.
Run: python3 -I scen.py  (from this directory)."""
import os
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design-g3", "checks.py")).read().splitlines()
exec("\n".join(_src[0:53] + ["THETA_C = 0.10"] + _src[329:466]))
K7 = 1 - (1 - 0.0) * np.exp(-7 * 24 / 36)
CH7 = ["LP","CR","BI","LD","GAZE_AWAY","FR","EN","BU"]
def show(lab, rec, t0, t1):
    s = summarize(rec, CH7, t0, t1)
    print(f"{lab} [{t0}-{t1}s] " + ", ".join(f"{c} {s[c][0]:+.2f}/{s[c][1]:+.2f}" for c in CH7))
# A. reunion after a week, partner's first words are bad news (unprompted, need 0.8), then exchanges
for need in (0.0, 0.5, 0.8):
    e = Engine(K=K7, P=0.6, f_id=0.9); ev = {}
    ev[at(8)] = {"exch": True, "putt": {"need": need}}
    for k in range(1, 6):
        ev[at(8 + 12 * k)] = {"exch": True, "putt": {}}
    rec = run(e, ev, 300)
    show(f"A reunion, first utterance need={need}", rec, 8, 20); show("   ", rec, 20, 60); show("   ", rec, 60, 180)
# B. teasing: 'you dumb robot' said laughing (lexical hostility 0.5), partner smiling LP 0.8
e = Engine(); ev = {at(5): {"putt": {"hostile": 0.5}, "exch": True}}
for k in range(1, 8): ev[at(5 + 15 * k)] = {"exch": True, "putt": {}, "play": True}
rec = run(e, ev, 1200, playing=lambda t: True)
show("B tease (free display)", rec, 5, 30); show("   ", rec, 30, 120); show("   ", rec, 600, 900)
for d in (20, 60, 120):
    c = cone({"LP": 0.8, "CR": 0.6}, d); print(f"   cone after {d}s of partner smile: BI {c['BI']:+.2f} LD {c['LD']:+.2f} LP {c['LP']:+.2f}")
print("   P after teasing play exchanges (blocked while V_L>=0.1):", round(e.P,3))
# C. bored partner: short replies every 20 s, no play, no need, for 30 min
e = Engine(P=0.3); ev = {}
for k in range(90): ev[at(10 + 20 * k)] = {"exch": True, "putt": {}}
rec = run(e, ev, 1800)
show("C bored partner", rec, 0, 60); show("   ", rec, 1200, 1800)
print("   K, P at end:", round(e.K,4), round(e.P,3))
# D. reunion, stranger vs operator: smile timing (rise time to peak)
e = Engine(K=K7, P=0.6, f_id=0.9); ev = {at(8): {"exch": True, "putt": {}}}
rec = run(e, ev, 60)
lp = [(r["t"], r["LP"]) for r in rec]
pk = max(lp, key=lambda x: x[1]); base = lp[int(7/DT)][1]
t10 = next(t for t, v in lp if t > 8 and v >= base + 0.1*(pk[1]-base)); t90 = next(t for t, v in lp if t > 8 and v >= base + 0.9*(pk[1]-base))
print(f"D single-exchange relief smile: base {base:.2f} peak {pk[1]:.2f} at {pk[0]-8:.1f}s after the event; 10-90% rise {t90-t10:.1f}s")
