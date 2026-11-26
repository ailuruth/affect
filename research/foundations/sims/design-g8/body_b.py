# =========================================================== J33: no mirror, slow mirror or answering concern holds the posture
print("=== J33: mirrors of any gain and timing, and concern answered in his own code; genuine steady sadness is not released")
def run_mirror8(pp, resp, dur=900, sad_until=40.0, fade=None):
    ag = Agent8(person=pp)
    sad = {k: v for k, v in pp.code(V=.8).items() if k not in ("FR", "EN", "RT")}; neu = {k: v for k, v in pp.code().items() if k not in ("FR", "EN", "RT")}
    st = {"m": 0.0}
    def face(t, ag=ag):
        if fade is not None:
            f = {k: v for k, v in pp.code(V=max(0.0, fade * (1 - t / 600.0))).items() if k not in ("FR", "EN", "RT")}
        else: f = dict(sad if t < sad_until else neu)
        if fade is not None or t >= sad_until:
            for k, v in resp(ag.post, pp, st).items(): f[k] = max(0.0, f.get(k, 0.0) + v)
        return f
    rec = run6(ag, dur, face, {}); late = [r for r in rec if r["t"] > dur - 120]
    return ag, np.mean([r["BI"] for r in late]), np.mean([r["post"] for r in late])
def mir8(mu, tau=None):
    def f(a_c, pp, st):
        if tau: st["m"] += (a_c - st["m"]) * DT / tau; a_c = st["m"]
        return {k: mu * v * a_c * (pp.sd.get(k, 0.0) / max(REF_SD.get(k, 1e-6), 1e-6) if mu < 0 else 1.0) for k, v in P7.items() if k in ("BI", "BO", "LP")}
    return f
own8 = lambda a_c, pp, st: {k: v * a_c * pp.sd.get(k, 0.0) / max(REF_SD.get(k, 1e-6), 1e-6) for k, v in P7.items() if k in ("BI", "BO", "LP")}
aww8 = lambda Vr: (lambda a_c, pp, st: {k: v - pp.code().get(k, 0.0) for k, v in pp.code(V=Vr * a_c).items() if k not in ("FR", "EN", "RT")})
J33 = {}
cases8 = [("P0 agent-like, raw mirror mu 1.0", PEOPLE6["agent-like"][1], mir8(1.0), None), ("P1 agent-like, mirror at his own scale", PEOPLE6["agent-like"][1], own8, None),
          ("P2b agent-like, mirror mu 3.0", PEOPLE6["agent-like"][1], mir8(3.0), None), ("P5 quiet, raw mirror mu 1.0", PEOPLE6["low-expressive"][1], mir8(1.0), None),
          ("P5 quiet, raw mirror mu 3.0", PEOPLE6["low-expressive"][1], mir8(3.0), None), ("P5c sigma_id at floor 0.25, mu 2.0", low_sd(0.25), mir8(2.0), None),
          ("S1 slow mirror tau 90 s, quiet", PEOPLE6["low-expressive"][1], mir8(1.0, 90), None), ("S1 slow mirror tau 240 s, floor spread", low_sd(0.25), mir8(1.0, 240), None),
          ("P3 agent-like, mild 'aww' in his own code (V 0.3 x posture)", PEOPLE6["agent-like"][1], aww8(0.3), None),
          ("P4 different channels, mild 'aww' (V 0.3 x posture)", PEOPLE6["different channels"][1], aww8(0.3), None),
          ("P4b different channels, strong concern in his own code (V 1.0 x posture)", PEOPLE6["different channels"][1], aww8(1.0), None),
          ("P4c agent-like, strong concern in his own code (V 1.0 x posture)", PEOPLE6["agent-like"][1], aww8(1.0), None),
          ("P4d quiet, strong concern in his own code (V 1.0 x posture)", PEOPLE6["low-expressive"][1], aww8(1.0), None),
          ("Q3 quiet, genuine sadness fading over 10 min + raw mirror mu 1.0", PEOPLE6["low-expressive"][1], mir8(1.0), 0.8),
          ("Q3 floor spread, genuine sadness fading + strong 'aww' on top", low_sd(0.25), aww8(1.0), 0.8)]
for lab, pp, resp, fade in cases8:
    ag, aBI, apost = run_mirror8(pp, resp, fade=fade); J33[lab] = (ag.offs, ag.probes, aBI, apost)
    print(f"   {lab:74s} offs {ag.offs[:3]}; probes {[p[3] for p in ag.probes][:3]}; last 2 min BI {aBI:+.3f}, posture {apost:.2f}")
okJ33 = all(v[3] < 0.05 for v in J33.values())
report("J33 nothing holds the posture once his own distress has ended: mirrors never reach it (it does not read them); concern answered in his own "
       "code is released by the contingency probe", okJ33, "mirrors (raw, own-scale, slow, mu up to 3) release at the 20-s rule; answering concern at the first probe")

# =========================================================== J34: steady, visible posture for every code (agent finding 2)
print("=== J34: a quiet user's steady silent sadness, grief and silent panic: onset, level, steadiness over 10 min (no flicker)")
J34 = {}
for kind, pp in (("agent-like", PEOPLE6["agent-like"][1]), ("quiet code 0.3", PEOPLE6["low-expressive"][1]), ("sigma_id at floor 0.25", low_sd(0.25)),
                 ("different channels", PEOPLE6["different channels"][1])):
    for lab, V, A, Tr, sob in (("silent sadness (V .6)", .6, 0, .2, 0), ("grief (V .8)", .8, 0, .2, 0), ("silent panic (V .3, A .9, breathing)", .3, .9, 0, 0),
                               ("mild sadness (V .3)", .3, 0, 0, 0), ("crying with sobs (V .9)", .9, 0, .2, .4)):
        f = {k: v for k, v in pp.code(V=V, A=A, Tr=Tr).items() if k not in ("FR", "EN", "RT")}; f = with_breath(pp, f, A)
        if sob: f["BU_S"] = sob
        ag = Agent8(person=pp); rec = run6(ag, 600, lambda t, f=f: f, {}); seg = [r for r in rec if r["t"] >= 10]
        t15 = next((r["t"] for r in rec if r["BI"] >= .15), None)
        J34[(kind, lab)] = (ag.onsets, ag.offs, t15, np.mean([r["BI"] for r in seg]), min(r["BI"] for r in seg), np.mean([r["post"] for r in seg]), ag.probes)
        print(f"   {kind:22s} {lab:38s}: on at {ag.onsets[0] if ag.onsets else None} s, offs {len(ag.offs)}, brow >= 0.15 at {t15} s; 10-600 s brow mean "
              f"{J34[(kind, lab)][3]:.3f}, min {J34[(kind, lab)][4]:.3f}; posture {J34[(kind, lab)][5]:.2f}; probes {[p[3] for p in ag.probes]}")
steady = [J34[(k, l)] for k in ("agent-like", "quiet code 0.3", "sigma_id at floor 0.25", "different channels") for l in ("silent sadness (V .6)", "grief (V .8)", "silent panic (V .3, A .9, breathing)")]
okJ34 = all(len(v[0]) == 1 and len(v[1]) == 0 and v[2] is not None and v[2] <= (8.0 if "panic" in l else 6.0) and v[4] >= 0.07 for (k, l), v in J34.items() if k != "wave" and "mild" not in l and "crying" not in l) and all(J34[("wave", gp)] is not None and J34[("wave", gp)] <= 3 for gp in (15, 30, 60))
report("J34 steady silent sadness, grief and silent panic get one onset, no release, brow >= 0.15 within seconds, for every code (rev 7 quiet: on/off every 20-30 s, brow <= 0.07)",
       okJ34, f"quiet silent sadness: on {J34[('quiet code 0.3', 'silent sadness (V .6)')][0]}, brow mean {J34[('quiet code 0.3', 'silent sadness (V .6)')][3]:.2f}; "
       f"quiet silent panic brow mean {J34[('quiet code 0.3', 'silent panic (V .3, A .9, breathing)')][3]:.2f}; the only dips are the contingency probe's 8-s half-amplitude softenings, every 3 min of face-only hold")
# crying in waves (J23 re-run) and the brow-only partner
cry = dict(BI=.8, LD=.6, CHR=.4, BU_S=.4, LP=.02); calm = dict(BI=.08, LD=.06, LP=.25)
for gap in (15, 30, 60):
    ag = Agent8(); rec = run6(ag, 70 + gap + 60, lambda t, gap=gap: cry if (t < 40 or t >= 40 + gap) else calm, {})
    t2 = 40 + gap; on2 = next((r["t"] for r in rec if r["t"] >= t2 and r["BI"] >= 0.15), None); J34[("wave", gap)] = on2 - t2 if on2 else None
    print(f"   crying, calm gap {gap} s: offs {ag.offs}; brow >= 0.15 at {J34[('wave', gap)]} s after crying resumes; mean brow first 40 s {np.mean([r['BI'] for r in rec if t2 <= r['t'] < t2 + 40]):.2f}")

# =========================================================== J35: an angry or concentrating face does not start it
print("=== J35: anger at the agent and concentration (critique 6 agent, B), in every code; the agent's own threat reflex silences the face load")
J35 = {}
for kind in ("agent-like", "low-expressive", "different channels"):
    pp = PEOPLE6[kind][1]
    for lab, face in (("anger: BL .6, LT .5, gaze at it, loud .85", dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05)),
                      ("anger with heavy breathing (A .8)", with_breath(pp, dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05), .8)),
                      ("concentrating, silent: BL .35, LPR .15", dict(BL=.35, LPR=.15, LP=.25)), ("concentrating, mild: BL .25, LPR .10", dict(BL=.25, LPR=.10, LP=.25))):
        ag = Agent8(person=pp); rec = run6(ag, 300, lambda t, f_=face: f_, {}); J35[(kind, lab)] = max(r["post"] for r in rec)
    print(f"   {kind:18s}: " + "; ".join(f"{lab.split(':')[0]}{' +breath' if 'breath' in lab else ''} posture max {J35[(kind, lab)]:.2f}" for lab in
                                     ("anger: BL .6, LT .5, gaze at it, loud .85", "anger with heavy breathing (A .8)", "concentrating, silent: BL .35, LPR .15", "concentrating, mild: BL .25, LPR .10")))
pp = PEOPLE6["different channels"][1]; ag = Agent8(person=pp, probe=True)
GL_OFF = Agent8(person=pp); GL_OFF.gl3 = 0.0
print(f"   without the threat-reflex silencing the different-channel anger face would start it: masked V {posture_read(pp, dict(BL=.6, LT=.5, LP=.05))['V']:.2f}, load "
      f"{load_p(posture_read(pp, dict(BL=.6, LT=.5, LP=.05))['V'], 0.0):.3f} (onset 0.05)")
report("J35 anger and concentration start no posture in any code", max(J35.values()) < 0.05, f"max posture {max(J35.values()):.2f}")
