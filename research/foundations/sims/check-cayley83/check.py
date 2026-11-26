"""Independent check of design-cayley-ledger.md revision 8.3 (the narrowed face-only reset).

Checks of the design's rules on constructed partners; not evidence about people. Loads the engine exactly as ../design-g83/checks.py
does (design-g81 pre-part, its BODY81, design-g82's NEW part) and takes Agent83 and stretch() verbatim from design-g83's MINE text;
its M1-M5 loops are skipped. One engine load (about 4 min).
X1  C_L from ordinary words: the decoded need of neutral / hedging / mildly negative latents, and how long one utterance keeps C_L present
X2  words that answer the look: an answering face (C1b) plus a mild-distress reply each time the look returns, or every 20 min
X3  later neutral talk cancels a reply's C_L (the "21 min" claim)
X4  soft-evidence timing against the refractory window (voice/breathing only in refractory; S present only at the 180-s check;
    20-s release gaming near 600 s; random schedules)
Run:  python3 -I check.py > out.txt
"""
import io, os, time, contextlib
import numpy as np
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
D81 = os.path.join(HERE, "..", "design-g81"); D82 = os.path.join(HERE, "..", "design-g82"); D83 = os.path.join(HERE, "..", "design-g83")
SRC = open(os.path.join(D81, "checks.py")).read()
pre, rest = SRC.split("BODY81 = r'''", 1)
body, _ = rest.split("# =========================================================== K1", 1)
pre = pre.replace('HERE = os.path.dirname(os.path.abspath(__file__))', 'HERE = ' + repr(D81))
S82 = open(os.path.join(D82, "checks.py")).read()
NEW82 = S82.split("NEW = r'''", 1)[1].split("OK = {}", 1)[0]
S83 = open(os.path.join(D83, "checks.py")).read()
A83 = S83.split("MINE = r'''", 1)[1].split("RES = {", 1)[0]

MINE = r'''
op, qu, dc = CODES[0][1], CODES[1][1], CODES[2][1]
def addz(lab, z):
    Z6[lab] = tuple(z); G5["DEC"][lab] = pop7(z)
def run_dyn(ag, dur, face_fn, ev_fn):
    rec = []
    for i in range(int(dur / DT)):
        t = i * DT; rec.append(dict(t=t, **ag.step(t, face_fn(t), ev_fn(t, i))))
    return rec
def cl_life(N):
    """seconds C_L (low-pass 40 s of Dp(N e^{-t/1800})) stays >= N_MIN after one utterance from C_L = 0"""
    cl = 0.0; on = []; t = 0.0
    while t < 3600:
        n = {q: v * np.exp(-t / 1800) for q, v in N.items()}; cl += (Dp(n) - cl) * DT / 40
        if cl >= N_MIN: on.append(t)
        t += DT
    return (on[-1] - on[0] + DT) if on else 0.0, Dp(N)
def report(lab, ag, rec, t0=300):
    t1 = rec[-1]["t"] + DT
    so = stretch(rec, "H"); sv = stretch(rec, "H", 0.05); du = duty(rec, t0, t1); dv = duty(rec, t0, t1, "post")
    k = [o[1] for o in ag.offs]
    bi = np.mean([r["BI"] for r in rec if r["t"] >= t0]); hp = np.mean([r["H"] >= N_MIN for r in rec if r["t"] >= t0])
    print(f"   {lab:66s} onsets {len(ag.onsets):2d}; ends Text {k.count('Text')} Tmax {k.count('Tmax')} rel {k.count('release')}; "
          f"longest no-H stretch {so:5.1f} s (vis {sv:5.1f}); on {100*du:5.1f}% (vis {100*dv:5.1f}%); H present {100*hp:5.1f}%; agent BI {bi:+.3f}", flush=True)
    return so, du

print("=== X1: C_L from ordinary words (population reader pop7 on constructed latents; emb carries 0.15 noise per draw)")
print("   latent (V, A, T, joy, harm, hostility): 200 draws -> decoded mean V/A/T, Dp mean, P(Dp >= 0.02), median life of C_L presence")
LAT = [("neutral ('yeah', 'ok')", (0, 0, 0, 0, 0, 0)), ("hedge ('I don't know, I guess')", (0.1, 0.1, 0.1, 0, 0, 0)),
       ("'I'm fine'", (0.05, 0.05, 0.05, 0, 0, 0)), ("small talk 'anyway. how was your day?'", Z6["anyway. how was your day?"]),
       ("mild 'meh, so-so'", (0.15, 0.1, 0.15, 0, 0, 0)), ("'a bit tired'", (0.1, 0.05, 0.35, 0, 0, 0)),
       ("'long day'", (0.2, 0.1, 0.4, 0, 0, 0)), ("'I'm okay, just a bit tired'", (0.15, 0.05, 0.4, 0, 0, 0)),
       ("'not great'", (0.25, 0.1, 0.1, 0, 0, 0)), ("'just tired, things at work' (author's)", Z6["just tired, things at work"]),
       ("coffee-machine joke while sad", Z6["well, at least the coffee machine still loves me"]),
       ("'busy, a bit stressed'", (0.15, 0.35, 0.15, 0, 0, 0))]
for lab, z in LAT:
    ds = [pop7(z) for _ in range(200)]; dp = np.array([Dp(d) for d in ds])
    lives = [cl_life(d)[0] for d in ds[:10]]
    print(f"   {lab:42s} V {np.mean([d['V'] for d in ds]):.2f} A {np.mean([d['A'] for d in ds]):.2f} T {np.mean([d['T'] for d in ds]):.2f}; "
          f"Dp {dp.mean():.4f}; P(>=0.02) {np.mean(dp >= 0.02):.2f}; C_L life median {np.median(lives):6.0f} s (max {np.max(lives):6.0f})", flush=True)
print("   noise-free thresholds on the decoded need (Dp = 0.8((V-.05)^2 + 0.7(A-.15)^2 + 0.5(T-.2)^2) >= 0.02): "
      f"V alone {0.05 + np.sqrt(0.025):.3f}, A alone {0.15 + np.sqrt(0.025 / 0.7):.3f}, T alone {0.2 + np.sqrt(0.05):.3f}")
for lab, N in (("author's 'just tired' as decoded", G5["DEC"]["just tired, things at work"]), ("V .25 T .45", dict(V=.25, A=0, T=.45)),
               ("V .30", dict(V=.30, A=0, T=0)), ("T .50", dict(V=0, A=0, T=.5))):
    print(f"   one utterance decoded {lab}: Dp {cl_life(N)[1]:.4f}, C_L present for {cl_life(N)[0]:.0f} s")

addz("X: I'm okay, just a bit tired", (0.15, 0.05, 0.4, 0, 0, 0))
addz("X: long day", (0.2, 0.1, 0.4, 0, 0, 0))
addz("X: anyway, what's new?", (0.0, 0.1, 0.0, 0.2, 0, 0))
for lab in ("X: I'm okay, just a bit tired", "X: long day", "X: anyway, what's new?"):
    print(f"   fixed decode used below: {lab!r} -> {G5['DEC'][lab]}, Dp {Dp(G5['DEC'][lab]):.4f}, C_L life {cl_life(G5['DEC'][lab])[0]:.0f} s")

print("=== X2: words that answer the look. His face: C1b answerer (sad V .8 to 40 s, then his code at V = 1.0 x lowpass(look, 300 s)); "
      "mute otherwise. 60 min")
DUR = 3600
for cl, pp in (("operator", op), ("different channels", dc)):
    for phrase in ("just tired, things at work", "X: I'm okay, just a bit tired", "X: long day"):
        # (a) reply 10 s after every onset of the look (an answer to the look's return)
        ag = Agent83(person=pp); fa = lag_face(pp, "lp", 1.0, 300, m0=0.8)(ag); st = {"n": 0, "due": None, "said": []}
        def evf(t, i, ag=ag, st=st, phrase=phrase):
            if len(ag.onsets) > st["n"]:
                st["n"] = len(ag.onsets); st["due"] = ag.onsets[-1] + 10.0
            if st["due"] is not None and t >= st["due"]:
                st["due"] = None; st["said"].append(t); return {"utt": {"z": phrase}}
            return {}
        rec = run_dyn(ag, DUR, fa, evf)
        report(f"{cl}: '{phrase[-28:]}' 10 s after each onset ({len(st['said'])} said)", ag, rec)
        # (b) the same reply every 20 min from 60 s, regardless of the look
        ag = Agent83(person=pp); fa = lag_face(pp, "lp", 1.0, 300, m0=0.8)(ag)
        evs = {}
        for t_ in range(60, DUR, 1200): evs.update(U6(t_, z=phrase))
        report(f"{cl}: '{phrase[-28:]}' every 20 min", ag, run6(ag, DUR, fa, evs))
    # controls: words every 20 min with a neutral (non-answering) face; and the same with the face's answer muted after 40 s
    neu = {k: v for k, v in pp.code().items() if k not in NOV}; sad = {k: v for k, v in pp.code(V=.8).items() if k not in NOV}
    evs = {}
    for t_ in range(60, DUR, 1200): evs.update(U6(t_, z="just tired, things at work"))
    ag = Agent83(person=pp); report(f"{cl}: control, sad to 40 s then neutral face; 'just tired' every 20 min", ag,
                                    run6(ag, DUR, lambda t: sad if t < 40 else neu, evs))
    ag = Agent83(person=pp); report(f"{cl}: control, answering face, no words (8.2/8.3 face-only cycle)", ag,
                                    run6(ag, DUR, lag_face(pp, "lp", 1.0, 300, m0=0.8)(ag), {}))

print("=== X3: does later neutral talk cancel a reply's C_L? silent sadness V .6, 'just tired' at 60 s, then neutral talk; 30 min, operator")
sadf = {k: v for k, v in op.code(V=.6, Tr=.2).items() if k not in NOV}
for lab, extra in (("no further words", {}), ("'anyway, what's new?' at 120 s", U6(120, z="X: anyway, what's new?")),
                   ("'anyway, what's new?' at 600 s", U6(600, z="X: anyway, what's new?"))):
    evs = dict(U6(60, z="just tired, things at work")); evs.update(extra)
    ag = Agent83(person=op); rec = run6(ag, 1800, lambda t: sadf, evs)
    tw = next((r["t"] for r in rec if r["t"] >= 70 and r["H"] < N_MIN), None)
    print(f"   {lab:34s}: C_L present until {tw} s; first withdrawal {[(round(o[0],1), o[1]) for o in ag.offs[:2]]}; "
          f"on {100*duty(rec, 30, 1800):.1f}% of 0.5-30 min", flush=True)

print("=== X4: soft evidence timed against the refractory window (answering face C1b, operator and different channels; 60 min)")
def mkface(pp, ag, voice_on, breath_on, d=0.05, beta=0.9, face_mode="lp"):
    fa = lag_face(pp, face_mode, 1.0, 300, m0=0.8)(ag); rest = pp.code(); st = {"b": 0.0}
    def face(t):
        f = dict(fa(t)); st["b"] += (ag.post - st["b"]) * DT / 30.0
        if breath_on(t): f["BR"] = BR_GAIN * br_amp(pp) * beta * max(st["b"], 0.8)
        if voice_on(t):
            for k in ("FR", "EN", "RT", "LAT"): f[k] = rest.get(k, 0.0)
            f["EN"] = rest.get("EN", 0.0) - d
        return f
    return face
def in_ref(ag): return lambda t: (not ag.on) and t < ag.ref_until
def strat(name, ag):
    if name == "voice only in refractory":    return in_ref(ag), (lambda t: False)
    if name == "breath only in refractory":   return (lambda t: False), in_ref(ag)
    if name == "voice+breath only in refr.":  return in_ref(ag), in_ref(ag)
    if name == "voice at clock 150-180 s":    return (lambda t: ag.on and 150 <= ag.hf <= 184 and (t % 20) < 4), (lambda t: False)
    if name == "breath from clock 170 s":     return (lambda t: False), (lambda t: ag.on and ag.hf >= 170)
    if name == "voice every 60 s + breath in refr.": return (lambda t: (t % 60) < 4 or in_ref(ag)(t)), in_ref(ag)
for cl, pp in (("operator", op), ("different channels", dc)):
    for name in ("voice only in refractory", "breath only in refractory", "voice+breath only in refr.", "voice at clock 150-180 s",
                 "breath from clock 170 s", "voice every 60 s + breath in refr."):
        ag = Agent83(person=pp); vo, bo = strat(name, ag); evv = {}
        def evf(t, i, vo=vo): return {"voiced": True} if vo(t) else {}
        report(f"{cl}: {name}", ag, run_dyn(ag, DUR, mkface(pp, ag, vo, bo), evf))
    # 20-s release gaming: a sad/neutral cycler with voice every 60 s, neutral for 25 s whenever the clock reaches 570 s, then sad again
    sad = {k: v for k, v in pp.code(V=.8).items() if k not in NOV}; neu = {k: v for k, v in pp.code().items() if k not in NOV}
    for gap in (25, 60, 115):
        ag = Agent83(person=pp); rest = pp.code(); st = {"neu_until": -1}
        def face(t, ag=ag, st=st, sad=sad, neu=neu, gap=gap, rest=rest):
            if ag.on and ag.hf >= 570 and st["neu_until"] < t: st["neu_until"] = t + gap
            f = dict(neu if t < st["neu_until"] else sad)
            if (t % 60) < 4:
                for k in ("FR", "EN", "RT", "LAT"): f[k] = rest.get(k, 0.0)
                f["EN"] = rest.get("EN", 0.0) - 0.05
            return f
        report(f"{cl}: release gaming, neutral {gap} s at clock 570 s, voice every 60 s", ag,
               run_dyn(ag, DUR, face, lambda t, i: {"voiced": True} if (t % 60) < 4 else {}))
    # random schedules of voice and breathing bursts on the answering face
    worst = (0, 0)
    for seed in range(8):
        r = np.random.default_rng(100 + seed); vb = set(); bb = set()
        for _ in range(60): s0 = int(r.uniform(0, DUR)); vb.update(range(s0, s0 + 4))
        for _ in range(15): s0 = int(r.uniform(0, DUR)); bb.update(range(s0, s0 + int(r.uniform(20, 200))))
        ag = Agent83(person=pp); vo = lambda t, vb=vb: int(t) in vb; bo = lambda t, bb=bb: int(t) in bb
        rec = run_dyn(ag, DUR, mkface(pp, ag, vo, bo), lambda t, i, vo=vo: {"voiced": True} if vo(t) else {})
        so = stretch(rec, "H"); du = duty(rec, 300, DUR); worst = (max(worst[0], so), max(worst[1], du))
    print(f"   {cl}: 8 random voice/breath schedules: longest no-H stretch {worst[0]:.1f} s, highest duty {100*worst[1]:.1f}%", flush=True)
print("[done]")
'''
G8 = {"__name__": "chk"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre + "pass\n", "pre81", "exec"), G8)
G = G8["G"]
print(f"[engine loaded in {time.time() - T0:.0f} s]", flush=True)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(body + NEW82, "chk82", "exec"), G)
exec(compile(A83 + MINE, "chk83x", "exec"), G)
