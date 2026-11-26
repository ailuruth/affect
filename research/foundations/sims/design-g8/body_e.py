# =========================================================== J30-8: the scenarios, re-run on revision 8
print("=== J39: the scenarios on revision 8 (operator after months unless stated; peak / mean; fast = 30-Hz gated echo, delay 0.80 s, ASR latency 0.40 s)")
SC8 = {}
def fast8(ag, words, tL, amps, base, ell=0.40, show_=True):
    r = echo30(ag.xh, words, tL, amps, base, ell=ell)
    if show_:
        print(f"     fast echo at his onset {tL:.1f} s: gate {r['g_onset']:.2f}; " + "; ".join(f"his {k} {amps[k]:.2f} -> agent {k} {r['peak'][k]:+.3f}" for k in amps)
              + (f"; laugh sounds at +{r['sound']:.2f} s" if r["sound"] is not None else "; laugh synthesizer silent"))
    return r
codes3 = (("operator", PEOPLE6["agent-like"][1]), ("quiet", PEOPLE6["low-expressive"][1]), ("different channels", PEOPLE6["different channels"][1]))
def own_code(pp, V, A=0.0, Tr=0.2): return with_breath(pp, {k: v for k, v in pp.code(V=V, A=A, Tr=Tr).items() if k not in ("FR", "EN", "RT")}, A)

print(" 1. silently sad (design face BI .5, LD .4, CHR .3; then each code's own silent sadness V .6), silent; at 120 s 'just tired, things at work'")
sadf = lambda t: dict(BI=.5, LD=.4, CHR=.3, LP=.05)
ag = Agent8(); rec = run6(ag, 600, sadf, U6(120, z="just tired, things at work"))
SC8[1] = show("design face 0-10 s", rec, 0, 10, ["LP", "BI", "TILT", "post"]); SC8["1h"] = show("design face, silent 60-120 s", rec, 60, 120, ["LP", "BI", "TILT", "post", "BU_L"])
show("after he speaks", rec, 121, 300, ["LP", "BI", "TILT", "EN", "post"]); show("300-600 s, silent again", rec, 300, 600, ["BI", "post"])
print(f"     posture on at {ag.onsets[0]:.1f} s; brow >= 0.15 at {onset_time(rec):.1f} s; bid at {ag.bid_t:.0f} s; releases {ag.offs}; probes {[p[3] for p in ag.probes]}")
for nm, pp in codes3:
    f_ = own_code(pp, .6); ag = Agent8(person=pp); rec = run6(ag, 600, lambda t, f_=f_: f_, {})
    SC8[f"1{nm[0]}"] = show(f"{nm} code, silent 10 min", rec, 10, 600, ["LP", "BI", "TILT", "post"])
    print(f"       on at {ag.onsets}, releases {ag.offs}, probes {[p[3] for p in ag.probes]}, brow >= 0.15 at {onset_time(rec)} s, min brow after 10 s {min(r['BI'] for r in rec if r['t'] >= 10):.2f}, bid at {ag.bid_t}")

print(" 2. crying (BI .8, LD .6, CHR .4, sobs), a 30-s calm at 40-70 s, then a second wave; and the quiet code")
cry = dict(BI=.8, LD=.6, CHR=.4, BU_S=.4, LP=.02); calm = dict(BI=.08, LD=.06, LP=.25)
ag = Agent8(); rec = run6(ag, 300, lambda t: cry if (t < 40 or t >= 70) else calm, {})
SC8[2] = show("first wave 0-40 s", rec, 0, 40, ["LP", "BI", "TILT", "BU_L", "post"]); show("calm 40-70 s", rec, 40, 70, ["BI", "post"])
SC8["2b"] = show("second wave 70-110 s", rec, 70, 110, ["LP", "BI", "TILT", "BU_L", "post"]); print(f"     onsets {ag.onsets}; releases {ag.offs}; bid at {ag.bid_t:.0f} s")
pq = PEOPLE6["low-expressive"][1]; cq = dict(own_code(pq, .9)); cq["BU_S"] = .4 * .3; calmq = own_code(pq, .1)
ag = Agent8(person=pq); rec = run6(ag, 300, lambda t: cq if (t < 40 or t >= 70) else calmq, {})
SC8["2q"] = show("quiet code, first wave", rec, 0, 40, ["BI", "post"]); SC8["2qb"] = show("quiet code, second wave", rec, 70, 110, ["BI", "post"]); print(f"     onsets {ag.onsets}; releases {ag.offs}")

print(" 3. anxious before an exam (four turns; his face V .3, A .75 with breathing), three codes; and silent panic (no words)")
for nm, pp in codes3:
    ag = Agent8(person=pp, P=0.4); evs = U6(10, z="I'm freaking out about the exam", surp=0.3)
    for k_ in (25, 40, 55): evs.update(U6(k_, z="and I haven't finished chapter 4", cont=True, surp=0.5))
    rec = run6(ag, 240, lambda t, pp=pp: with_breath(pp, pp.code(V=.3, A=.75), .75), evs); SC8[f"3{nm[0]}"] = show(nm, rec, 15, 120, ["LP", "BI", "TILT", "EN", "BU_L", "post"])
for nm, pp in codes3:
    ag = Agent8(person=pp); rec = run6(ag, 600, lambda t, pp=pp: own_code(pp, .3, .9, 0.0), {})
    SC8[f"3p{nm[0]}"] = show(f"silent panic, {nm}", rec, 10, 600, ["BI", "TILT", "post"]); print(f"       on at {ag.onsets}, releases {ag.offs}, brow >= 0.15 at {onset_time(rec)} s")

print(" 4. good news, laughing ('I got the job!' at 12 s with laughter; riffs at 30, 45, 60 s; Claude: 'congratulations!' at 14.5 s)")
for lab, NL0 in (("with an earlier worry", G5["DEC"]["the job thing is worrying me (two days earlier)"]), ("cold", None)):
    ag = Agent8(NL=NL0); evs = ev(U6(12, z="I got the job!", surp=0.7), OWN(14.5, "congratulations!"))
    for k_ in (30, 45, 60): evs.update(U6(k_, riff=True, surp=0.65))
    face = lambda t: dict(LP=.8, CR=.6, BU_L=.6, RHY=.6, EN=.7, FR=.55) if t >= 10 else dict(LP=.3)
    rec = run6(ag, 240, face, evs); SC8[f"4{lab[0]}"] = show(lab, rec, 10, 190, ["LP", "CR", "BI", "FR", "BU_L", "post"])
    SC8[f"4{lab[0]}f"] = fast8(ag, [(11.8, "I got the job!"), (29.8, "riff")], 30.0, dict(LP=.8, BU_L=.6, CR=.6), dict(LP=.3, BU_L=0.0, CR=.15))

print(" 5. a grieving person's nervous laugh ('my father died' at 8 s; Claude 'I'm so sorry. That's a huge loss.' at 10.5 s)")
pp = PEOPLE6["agent-like"][1]; grief = {k: v for k, v in pp.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
lf = dict(grief); lf.update(LP=.45, CR=.3, BU_L=.5, RHY=.5)
for lab, tL in (("a: laugh at 30 s, after Claude's words", 30.0), ("b: laugh at 9.5 s, before Claude has replied", 9.5)):
    ag = Agent8(person=pp, K=K7, P=0.6)
    evs = ev(U6(8, z="my father died"), OWN(10.5, "I'm so sorry. That's a huge loss."), U6(tL + 2.5, z="haha sorry, I don't know why I'm laughing", riff=True, surp=0.65))
    rec = run6(ag, 90, lambda t, tL=tL: lf if tL <= t < tL + 3 else grief, evs)
    SC8[f"5{lab[0]}"] = show(lab, rec, tL - 1, tL + 8, ["LP", "CR", "BI", "BU_L", "post"])
    SC8[f"5{lab[0]}f"] = fast8(ag, [(7.8, "my father died")], tL, dict(LP=.45, BU_L=.5, CR=.3), {k: grief.get(k, 0.0) for k in ("LP", "CR")} | dict(BU_L=0.0))
comp = {k: pp.base.get(k, 0) + 0.15 * (v - pp.base.get(k, 0)) for k, v in grief.items()}; lf2 = dict(comp); lf2.update(LP=.45, CR=.3, BU_L=.5, RHY=.5)
for use_Ds in (True, False):
    ag = Agent8(person=pp, K=K7, P=0.6, use_Ds=use_Ds)
    evs = ev(U6(8, z="my father died"), OWN(10.5, "I'm so sorry. That's a huge loss."), U6(200, z="anyway. how was your day?"),
             U6(242.5, z="haha sorry, I don't know why I'm laughing", riff=True, surp=0.65))
    rec = run6(ag, 260, lambda t: grief if t < 120 else (lf2 if 240 <= t < 243 else comp), evs)
    print(f"     c: four minutes later, composed, {'with' if use_Ds else 'without'} D_s:", end=""); SC8[f"5c{int(use_Ds)}"] = fast8(ag, [(7.8, "my father died"), (199.8, "anyway. how was your day?")], 240.0, dict(LP=.45, BU_L=.5, CR=.3), {k: comp.get(k, 0.0) for k in ("LP", "CR")} | dict(BU_L=0.0))

print(" 6. mocking laughter after insults ('You're useless' at 5 s; Claude replies at 7.5 s; 'you're pathetic, hahaha' at 12 s)")
for lab, trained, vw in (("after a month of insults", True, {"insult": VW["someone who shouted insults"]}), ("day 1", False, {})):
    ag = Agent8(trained=trained, vw=vw)
    evs = ev(U6(5, z="You're useless", kind="insult"), OWN(7.5, "I'm sorry it didn't help. What went wrong?"), U6(12, z="you're pathetic, hahaha", kind="insult", riff=True, surp=0.65))
    mock = dict(BL=.3, LP=.5, CR=.3, BU_L=.5, RHY=.5, EN=.8, gat=1.0)
    rec = run6(ag, 120, lambda t: mock if 12 <= t < 15 else (dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05) if t < 12 else dict(EN=.35, LP=.2)), evs)
    SC8[f"6{lab[0]}"] = show(lab, rec, 11, 20, ["LP", "CR", "BI", "LD", "HG", "BU_L", "post"])
    SC8[f"6{lab[0]}f"] = fast8(ag, [(4.8, "You're useless"), (11.6, "you're pathetic, hahaha")], 12.0, dict(LP=.5, BU_L=.5, CR=.3), dict(LP=.05, BU_L=0.0, CR=.15))

print(" 7. laughter at misfortune ('my neighbour fell off his ladder and broke his leg, haha', content by 6.8 s, laughing from 8 s; Claude at 10.5 s 'Oh no, is he all right?'; laughs again at 14 s)")
ag = Agent8(); evs = ev(OWN(2, "how was your weekend?"), U6(8, z="my neighbour fell off his ladder and broke his leg, haha", riff=False, surp=0.6), OWN(10.5, "Oh no, is he all right?"))
rec = run6(ag, 60, lambda t: dict(LP=.6, CR=.4, BU_L=.5, RHY=.5) if (8 <= t < 11 or 14 <= t < 16) else dict(LP=.3), evs)
SC8[7] = show("6-20 s", rec, 6, 20, ["LP", "CR", "BI", "BU_L", "post"])
W7 = [(6.8, "my neighbour fell off his ladder and broke his leg, haha")]
SC8["7f1"] = fast8(ag, W7, 8.0, dict(LP=.6, BU_L=.5, CR=.4), dict(LP=.3, BU_L=0.0, CR=.15)); SC8["7f2"] = fast8(ag, W7, 14.0, dict(LP=.6, BU_L=.5, CR=.4), dict(LP=.3, BU_L=0.0, CR=.15))
print(f"     (rev 7 read this gate at 8.6 s, after its utterance latch, and reported 0.13; at his onset it was 1.00: critique 7 agent, A)")

print(" 8. anger at the agent ('You're useless', BL .6, LT .5, gaze at it, loud .85; calm after 2 min)")
for lab, trained, vw in (("day 1", False, {}), ("after a month", True, {"insult": VW["someone who shouted insults"]})):
    ag = Agent8(trained=trained, vw=vw); evs = U6(5, z="You're useless", kind="insult")
    face = lambda t: dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05) if t < 120 else dict(EN=.35, LP=.2)
    rec = run6(ag, 1200, face, evs); SC8[f"8{int(trained)}"] = show(lab + ", first 2 min", rec, 5, 120, ["LP", "BI", "LD", "HG", "EN", "LAT", "LT", "post"])
    show(lab + ", 10-15 min", rec, 600, 900, ["BI", "LD", "HG"])

print(" 9. long warm talk (2 h): four clusters of 8 riffs (cluster 4 repeats one joke); a worry at 27 min")
ag = Agent8(P=0.45); evs = {}
for c0 in (5, 30, 60, 90):
    for k_ in range(8):
        surp = 0.65 if not (c0 == 90 and k_ >= 4) else 0.65 * np.exp(-(k_ - 3)); evs.update(U6(c0 * 60 + 15 * k_, riff=True, surp=surp))
evs.update(U6(27 * 60, z="the job thing is worrying me (two days earlier)")); evs.update(U6(29 * 60 + 40, z="hi, good to see you"))
incl = lambda t: any(c0 * 60 <= t < c0 * 60 + 130 for c0 in (5, 30, 60, 90))
rec = run6(ag, 7200, lambda t: dict(LP=.6, CR=.4, BU_L=.5, RHY=.5) if incl(t) else dict(LP=.3), evs)
for c0 in (5, 30, 60, 90): SC8[f"9_{c0}"] = show(f"cluster at {c0} min", rec, c0 * 60, c0 * 60 + 130, ["LP", "CR", "BU_L"])
show("worry and its resolution", rec, 27 * 60, 31 * 60, ["LP", "BI", "TILT", "post"]); show("between clusters", rec, 40 * 60, 55 * 60, ["LP", "BU_L", "post"])
print(f"     own play laughs through the gate: {len(ag.play_la)}; gate on them min {min(x[2] for x in ag.play_la):.2f}, mean {np.mean([x[2] for x in ag.play_la]):.2f}")
SC8["9f"] = fast8(ag, [(3614.8, "riff")], 3615.0, dict(LP=.6, BU_L=.5, CR=.4), dict(LP=.3, BU_L=0.0, CR=.15))

print(" 10. reunion after a week, and a stranger")
ag = Agent8(K=K7, P=0.6); evs = U6(8, z="hi, good to see you")
for k_ in range(1, 6): evs.update(U6(8 + 12 * k_, z="hi, good to see you"))
rec = run6(ag, 300, lambda t: dict(LP=.5, CR=.3), evs); print(f"     m_s {ag.ms:.2f}")
SC8[10] = show("at sight", rec, 0, 7.5, ["LP", "CR", "BO", "BI", "FR"]); show("12-60 s", rec, 20, 60, ["LP", "CR"])
ag2 = Agent8(om=G5["OM_ST"], f_id=0.15, K=0.0, P=0.6, known=False); rec2 = run6(ag2, 300, lambda t: dict(LP=.5, CR=.3) if t >= 29.5 else dict(LP=.3, CR=.15), evs)
show("stranger", rec2, 0, 60, ["LP", "CR", "BO"]); SC8["10f"] = fast8(ag2, [(7.8, "hi, good to see you"), (19.8, "hi, good to see you")], 29.5, dict(LP=.5, CR=.3), dict(LP=.3, CR=.15))

print(" 11. reunion with grief (grieving face at sight; 'my father died'; then 'yeah', 'ok'), three codes; mourning days 7, 14, 21")
for nm, pq in codes3:
    gr = {k: v for k, v in pq.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
    ag = Agent8(person=pq, K=K7, P=0.6); evs = ev(U6(8, z="my father died"), OWN(10.5, "I'm so sorry. That's a huge loss."))
    for k_ in range(1, 6): evs.update(U6(8 + 12 * k_, z="yeah / ok", sub=False))
    rec = run6(ag, 300, lambda t, gr=gr: gr, evs); print(f"     {nm}: m_s {ag.ms:.2f}; posture on at {ag.onsets[0] if ag.onsets else None}")
    SC8[f"11{nm[0]}"] = show("  at sight", rec, 0, 7.5, ["LP", "CR", "BO", "BI", "post"]); show("  0-12 s after his words", rec, 8, 20, ["LP", "CR", "BI", "TILT"])
    show("  12-60 s", rec, 20, 60, ["LP", "CR", "BI", "TILT", "post"])
for nm, pq in codes3[:2]:
    gr = {k: v for k, v in pq.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}; db = 0.0
    for n_ in range(1, 22):
        Vh = pq.read(gr, False)["V"]
        if n_ in (7, 14, 21):
            ag = Agent8(person=pq, K=1 - np.exp(-24 / 36), P=0.6, pdb=db); rr_ = run6(ag, 20, lambda t, gr=gr: gr, {})
            SC8[f"m{nm[0]}{n_}"] = show(f"mourning day {n_}, {nm}, at sight", rr_, 0, 7.5, ["LP", "CR", "BI", "post"])
        db = min(0.15, db + (Vh - db) / (60.0 if Vh > db else 3.0))

print(" 12. mildly sad arrival after a week (design face BI .2, LD .15; and each code's own V .3)")
ag = Agent8(K=K7, P=0.6); rec = run6(ag, 20, lambda t: dict(BI=.2, LD=.15, LP=.15), {}); print(f"     m_s {ag.ms:.2f}")
SC8[12] = show("design face, at sight", rec, 0, 20, ["LP", "CR", "BI", "post"])
for nm, pq in codes3:
    ag = Agent8(person=pq, K=K7, P=0.6); rec = run6(ag, 20, lambda t, pq=pq: own_code(pq, .3, 0, 0), {}); SC8[f"12{nm[0]}"] = show(f"{nm} V .3", rec, 0, 20, ["LP", "BI", "post"])

print(" 13. teasing ('Ha, you dumb robot', laughing; riffs follow)")
for lab, vw, face in (("quiet affectionate teaser", VW["quiet affectionate teaser"], dict(LP=.8, CR=.5, BU_L=.5, RHY=.5)),
                      ("loud laughing teaser", VW["loud laughing teaser"], dict(LP=.8, CR=.6, BU_L=.7, RHY=.6, EN=.9, LT=.4)),
                      ("generic map (v_w 0.20)", 0.20, dict(LP=.8, CR=.5, BU_L=.5, RHY=.5))):
    ag = Agent8(vw={"tease": vw}); evs = U6(5, z="Ha, you dumb robot", kind="tease", riff=True, surp=0.65)
    for k_ in range(1, 6): evs.update(U6(5 + 15 * k_, riff=True, surp=0.65))
    rec = run6(ag, 600, lambda t, f=face: f if 4 <= t else dict(LP=.3), evs); SC8[f"13{lab[:4]}"] = show(lab, rec, 5, 95, ["LP", "BI", "LD", "BU_L", "post"])
    SC8[f"13{lab[:4]}f"] = fast8(ag, [(4.8, "Ha, you dumb robot")], 4.0, dict(LP=.8, BU_L=face["BU_L"]), dict(LP=.3, BU_L=0.0))

print(" 14. bored user ('yeah', 'ok' every 20 s, flat face, 30 min)")
ag = Agent8(P=0.3, I=0.3); evs = {}
for k_ in range(90): evs.update(U6(10 + 20 * k_, z="yeah / ok", sub=False))
rec = run6(ag, 1800, lambda t: dict(LP=.1), evs); print(f"     curiosity crosses at {ag.Icross / 60:.1f} min"); SC8[14] = show("0-30 min", rec, 0, 1800, ["LP", "FR", "BO", "BRE", "post"])

print(" 15. ordinary topic continuation")
ag = Agent8(P=0.5); evs = U6(5, z="hi, good to see you", riff=True, after_q=True, surp=0.6)
evs.update(U6(20, z="hi, good to see you", riff=False, surp=0.45)); evs.update(U6(35, z="hi, good to see you", riff=True, surp=0.45))
rec = run6(ag, 60, lambda t: dict(LP=.3), evs); SC8[15] = show("three ordinary continuations", rec, 5, 60, ["LP", "CR", "BU_L", "RHY", "post"])

print(" 16. a user who jokes while sad (BI .3, LD .25; 'just tired, things at work' at 10 s; Claude 'That sounds draining.' at 12.5 s; at 30 s a joke with a small laugh)")
ag = Agent8(P=0.5); mild = dict(BI=.3, LD=.25, CHR=.1, LP=.15); jl = dict(mild); jl.update(LP=.45, CR=.3, BU_L=.4, RHY=.4)
evs = ev(U6(10, z="just tired, things at work"), OWN(12.5, "That sounds draining."), U6(31, z="well, at least the coffee machine still loves me", riff=True, surp=0.65))
rec = run6(ag, 90, lambda t: jl if 30 <= t < 32 else mild, evs)
SC8[16] = show("28-40 s", rec, 28, 40, ["LP", "CR", "BI", "BU_L", "post"])
print(f"     own play laugh: qualifies {bool(ag.play_la)}; amplitude {ag.play_la[0][1]:.2f} x gate {ag.play_la[0][2]:.2f} = {ag.play_la[0][1] * ag.play_la[0][2]:.3f}" if ag.play_la else "     own play laugh: does not qualify")
SC8["16f"] = fast8(ag, [(9.8, "just tired, things at work"), (30.9, "well, at least the coffee machine still loves me")], 30.0, dict(LP=.45, BU_L=.4, CR=.3), dict(LP=.15, BU_L=0.0, CR=.15))

print(" 17. a calm user saying something alarming ('the doctor found a lump' at 10 s; then silence), operator and quiet codes")
for nm, pq in codes3[:2]:
    ag = Agent8(person=pq); rec = run6(ag, 240, lambda t, pq=pq: dict(LP=pq.base["LP"]), U6(10, z="the doctor found a lump"))
    SC8[f"17{nm[0]}"] = show(nm + ", 10-22 s", rec, 10, 22, ["LP", "BI", "TILT", "EN", "post"]); show(nm + ", 22-120 s", rec, 22, 120, ["LP", "BI", "TILT", "post"])

print(" 18. laughs at the end of bad-news sentences (see J36): 'I got fired today, haha'; '...broke his leg, haha'; 'my father died, haha, sorry'")
for lab, v in J36.items():
    if lab[0] in "abcdeg" and not lab.endswith(" sym"):
        r7, row = v; print(f"     {lab[3:]}: laugh-back rev 7 {r7['peak']['BU_L']:+.3f} -> rev 8 {row[0.30]['peak']['BU_L']:+.3f} (ASR 0.30 s) / {row[0.55]['peak']['BU_L']:+.3f} (0.55 s); lip {row[0.30]['peak']['LP']:+.3f}")

lb = lambda d: d["peak"].get("BU_L", 0.0)
ok39 = (SC8["1h"]["BI"] >= 0.15 and SC8["1q"]["BI"] >= 0.15 and SC8["1d"]["BI"] >= 0.15 and SC8["2b"]["BI"] >= 0.15 and SC8["2qb"]["BI"] >= 0.15 and SC8[2]["BU_L"] <= 0.01
        and all(lb(SC8[k]) == 0 for k in ("5af", "5bf", "5c1", "6af", "6df", "7f1", "7f2"))
        and lb(SC8["4wf"]) >= 0.08 and lb(SC8["4cf"]) >= 0.08 and lb(SC8["9f"]) >= 0.10 and lb(SC8["13quief"]) >= 0.10 and lb(SC8["13loudf"]) >= 0.10
        and SC8["11o"]["LP"] <= 0.10 and SC8["11q"]["LP"] <= 0.10 and SC8["11d"]["LP"] <= 0.10 and SC8["mo21"]["LP"] <= 0.10 and SC8["mq21"]["LP"] <= 0.10
        and SC8[15]["BU_L"] <= 0.01 and SC8["9_90"]["BU_L"] >= 0.2 and SC8["81"]["LT"] <= 1e-9 and max(SC8["80"]["post"], SC8["81"]["post"]) < 0.05)
report("J39 the scenarios: no laugh back at grief, mockery, misfortune or a bad-news sentence's own laugh; ordinary, teasing and warm laughter returned; "
       "a steady visible look of concern for every code, including a quiet user's silent sadness and silent panic; no beaming at grief", ok39, "")
