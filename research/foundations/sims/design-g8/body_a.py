# =========================================================== J31: constants revision 8 adds or changes
print("=== J31: constants added or changed in revision 8 (innate unless marked)")
print(f"   posture never reads {WR8}; it reads {FCP8} (+ voice when voiced), sobs, breathing, words")
print(f"   load L = Vc(V_p) + {W_AR} (A_b - {A_FLOOR})+^2 clip((V_p - {V_GATE0})/{V_GATE1}, 0, 1); grade a* = 0.35 + 0.65 clip((M - 0.05)/{A_SPAN8}, 0, 1)")
print(f"   threat-reflex silencing at glare >= {GLARE_SAT}; release {REL8} s below 0.02; contingency probe after {PROBE0:.0f} s face-only "
      f"(doubling to {PROBE_MAX:.0f} s): amplitude x {PROBE_DEPTH} for {PROBE_LEN:.0f} s, release if his load falls below {PROBE_FOLLOW} of before")
print(f"   gated group's echo delay {DELTA_G} s, word look-ahead {LAMBDA_W} s (words through source + {LAMBDA_W} s must be in by source + {DELTA_G} s, else the gate target is 0)")
report("J31 the posture's read set and write set are disjoint", not (set(FCP8) & set(WR8)) and all(k in WR8 for k in P7 if P7[k] != 0),
       f"writes {[k for k in P7 if P7[k] != 0]} (+ gaze x (1 - 0.5a), blink rate); reads none of them")

# =========================================================== J32: the posture's copy slope on every channel it writes
print("=== J32: copy slope of every posture channel on his same channel (routes finding 1): brow-only, outer-brow-only and lip-only partners;"
      " held levels; full-face sadness with an independent brow")
CODES8 = (("agent-like", PEOPLE6["agent-like"][1]), ("quiet code 0.3", PEOPLE6["low-expressive"][1]), ("sigma_id at floor 0.25", low_sd(0.25)),
          ("different channels", PEOPLE6["different channels"][1]))
for _, pp in CODES8:
    if not hasattr(pp, "br_amp"): pass
J32 = {}
def one_ch(pp, ch, dl): f = {"LP": pp.base["LP"]}; f[ch] = pp.base[ch] + dl; return f
for ch, dls in (("BI", (0.02, 0.06, 0.10, 0.15, 0.20, 0.30, 0.50)), ("BO", (0.05, 0.15, 0.30, 0.50)), ("LP", (-0.25, -0.15, -0.05, 0.0, 0.10))):
    for lab, pp in CODES8:
        rows = []
        for dl in dls:
            ag = Agent8(person=pp); rec = run6(ag, 90, lambda t, pp=pp, dl=dl, ch=ch: one_ch(pp, ch, dl), {})
            rows.append((dl, np.mean([r[ch] for r in rec if r["t"] > 30]), np.mean([r["post"] for r in rec if r["t"] > 30])))
        loc = max(abs((rows[i + 1][1] - rows[i][1]) / (rows[i + 1][0] - rows[i][0])) for i in range(len(rows) - 1))
        J32[("static", ch, lab)] = loc
        print(f"   static {ch}-only, {lab:22s}: " + "; ".join(f"{d:+.2f} -> {a:+.3f} (post {p:.2f})" for d, a, p in rows) + f"; steepest |local slope| {loc:.3f}")
r8 = np.random.default_rng(8)
for ch in ("BI", "BO"):
    for lab, pp in CODES8:
        lv = r8.uniform(0.0, 0.30, 30)
        face = lambda t, pp=pp, lv=lv, ch=ch: one_ch(pp, ch, lv[min(int(t // 120), 29)])
        ag = Agent8(person=pp); rec = run6(ag, 3600, face, {})
        his = np.array([face(r["t"])[ch] for r in rec]); agc = np.array([r[ch] for r in rec]); out = []
        for W in (60, 600):
            n = int(W / DT); m = len(his) // n; hm, am = his[: m * n].reshape(m, n).mean(1), agc[: m * n].reshape(m, n).mean(1)
            out.append((W, slope(hm, am), np.std(hm)))
        J32[("held", ch, lab)] = max(abs(o[1]) for o in out)
        print(f"   held {ch}-only (level re-drawn every 2 min, 60 min), {lab:22s}: " + "; ".join(f"{W // 60} min: slope {s_:+.3f} (his SD {sd:.3f})" for W, s_, sd in out)
              + f"; posture on {np.mean([r['post'] > .05 for r in rec]):.0%}")
# full-face sadness held for minutes, with an independent offset on one written channel; paired runs (offset on / off, same sadness, same seed):
# the paired difference is the causal (partial) slope on his same channel; the pooled slope over his sadness is the appraisal (declared R40')
FF = {}
for lab, pp in CODES8:
    Vl = r8.uniform(0.0, 0.8, 60); off = r8.uniform(-0.05, 0.25, 60)
    for ch in ("BI", "BO", "LP"):
        def face(t, pp=pp, Vl=Vl, off=off, ch=ch, on=True):
            i = min(int(t // 120), 59); f = {k: v for k, v in pp.code(V=Vl[i], Tr=.1).items() if k not in ("FR", "EN", "RT")}
            if on: f[ch] = f.get(ch, pp.base[ch]) + (off[i] if ch != "LP" else -off[i]); return f
            return f
        rA = run6(Agent8(person=pp), 7200, lambda t: face(t, on=True), {}); rB = run6(Agent8(person=pp), 7200, lambda t: face(t, on=False), {})
        hA = np.array([face(r["t"], on=True).get(ch, pp.base[ch]) for r in rA]); hB = np.array([face(r["t"], on=False).get(ch, pp.base[ch]) for r in rB])
        aA = np.array([r[ch] for r in rA]); aB = np.array([r[ch] for r in rB]); pA = np.array([r["post"] for r in rA]); pB = np.array([r["post"] for r in rB])
        for W in (60, 600):
            n = int(W / DT); m = len(hA) // n; bm = lambda z: z[: m * n].reshape(m, n).mean(1)
            FF[(lab, ch, W)] = (slope(bm(hA - hB), bm(aA - aB)), float(np.max(np.abs(pA - pB))), slope(bm(hB), bm(aB)), float(np.std(bm(hB))))
    print(f"   full-face sadness held (V re-drawn every 2 min, 2 h), {lab:22s}: " + "; ".join(
        f"{ch} {W // 60} min: causal slope on his {ch} {FF[(lab, ch, W)][0]:+.3f} (posture part changed by {FF[(lab, ch, W)][1]:.3f}); pooled over his sadness "
        + (f"{FF[(lab, ch, W)][2]:+.2f}" if FF[(lab, ch, W)][3] >= COND_FLOOR else f"(his SD {FF[(lab, ch, W)][3]:.3f} < floor)") for ch in ("BI", "BO", "LP") for W in (60, 600)))
CK = dict(BI=.20, BO=.10, LP=.35)
okJ32 = all(v <= CK[ch] for (kind, ch, lab), v in J32.items()) and all(abs(v[0]) <= CK[ch] and v[1] == 0.0 for (lab, ch, W), v in FF.items())
report("J32 the posture never reads what it writes: its part of every written channel is identical whatever his same channel does; every code's "
       "copy slope on BI, BO, LP stays under the channel's ceiling at 1 and 10 min; the pooled slope over his sadness is the agent's appraisal (declared, R40')", okJ32,
       f"brow-only partner, quiet code: steepest {J32[('static', 'BI', 'quiet code 0.3')]:.3f} (rev 7: 0.86), held {J32[('held', 'BI', 'quiet code 0.3')]:.3f} (rev 7: 0.56-0.60); "
       f"floor spread held {J32[('held', 'BI', 'sigma_id at floor 0.25')]:.3f} (rev 7: 0.41-0.45); all from the non-posture routes (posture 0 %)")
