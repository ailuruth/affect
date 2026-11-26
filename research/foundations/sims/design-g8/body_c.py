# =========================================================== J36: the gate has the current sentence's words when his laugh starts (agent finding 1)
print("=== J36: laugh-onset timing at 30 Hz: the gated echo waits for the words through its source frame + 0.25 s (incremental ASR), delay 0.80 s")
Z6["and then the dog ate the whole cake, haha"] = (0.0, 0.2, 0.0, 0.8, 0.0, 0.0)
Z6["I got fired today, haha"] = (0.6, 0.4, 0.1, 0.2, 0.3, 0.0)                 # the agent critic's latents, unchanged
Z6["my father died, haha, sorry"] = (0.85, 0.30, 0.2, 0.1, 0.4, 0.0)
Z6["OWN: tell me about it!"] = (0.0, 0.2, 0.0, 0.6, 0.0, 0.0)
for lab_ in ("and then the dog ate the whole cake, haha", "I got fired today, haha", "my father died, haha, sorry", "OWN: tell me about it!"):
    G5["DEC"][lab_] = pop7(Z6[lab_])
FS30 = 30.0


def lp30(x, tau, x0):
    a = 1 - np.exp(-1 / (tau * FS30)); y = np.empty_like(x); s_ = x0
    for i, v in enumerate(x): s_ += a * (v - s_); y[i] = s_
    return y


def echo30(xh, words, tL, amps, base, dur=3.0, ell=0.40, rev=8, latch=None, t_end=None, sym=False):
    """the gated fast echo of one laugh onset of his, at 30 Hz.
    xh: the 2 Hz engine's gate inputs (t, x); words: [(t_key, label)] his recognised content (t_key = when its content word ends);
    rev 8: echo delay DELTA_G, words through source + LAMBDA_W required by source + DELTA_G (ASR stable latency ell), else target 0;
           closes at once, opens tau 0.3 s.  rev 7: delay 0.45 s, word inputs latched at utterance end + 0.6 s (latch), tau 0.3 s both ways."""
    t = np.arange(tL - 6.0, tL + 5.0, 1 / FS30); out = {}
    prof = np.clip((t - tL) / 0.1, 0, 1) * np.clip((tL + dur - t) / 0.3 + 1, 0, 1)
    u = {k: base.get(k, 0.0) + (a_ - base.get(k, 0.0)) * prof for k, a_ in amps.items()}
    dlt = DELTA_G if rev == 8 else 0.45
    def x_src(s):
        x = list(next((x_ for (tt, x_) in reversed(xh) if tt <= s), xh[0][1]))
        if rev == 8:
            seg = [lb for (tk, lb) in words if tk <= s + LAMBDA_W]
            x[1], x[2] = (Dp(G5["DEC"][seg[-1]]), LAMV(Z6[seg[-1]])) if seg else (0.0, 0.0)
        else:
            seg = [lb for (tk, lb) in words if (latch or tk) <= s] if latch is not None else []
            x[1], x[2] = (Dp(G5["DEC"][seg[-1]]), LAMV(Z6[seg[-1]])) if seg else (x[1], x[2])
        return x
    src = t - dlt; gs = np.empty_like(t); gcur = None
    for i, s in enumerate(src):
        tgt = GATE(x_src(s)) if (rev == 7 or ell + LAMBDA_W <= dlt) else 0.0
        if gcur is None: gcur = tgt
        elif rev == 8 and not sym: gcur = tgt if tgt < gcur else gcur + (tgt - gcur) * (1 - np.exp(-1 / (GATE_TAU * FS30)))
        else: gcur += (tgt - gcur) * (1 - np.exp(-1 / (GATE_TAU * FS30)))
        gs[i] = gcur
    for k, uk in u.items():
        xd = np.interp(t - dlt, t, uk, left=uk[0]); E = xd - lp30(xd, 4.0, xd[0])
        out[k] = gs * GK[k] * np.maximum(E, 0.0)
    loud = out.get("BU_L", np.zeros_like(t)) >= THETA_L
    sound_t = float(t[np.argmax(loud)] - tL) if loud.any() else None
    pk = {k: float(v[t >= tL].max()) for k, v in out.items()}
    if "BU_L" in pk and pk["BU_L"] < THETA_L: pk["BU_L"] = 0.0
    g_on = float(gs[np.argmin(np.abs(src - tL))])
    return dict(peak=pk, sound=sound_t, g_onset=g_on, t_peak=float(t[t >= tL][np.argmax(out["LP"][t >= tL])] - tL))


def run_ctx(pp, face_fn, evs, dur):
    ag = Agent8(person=pp, K=0.0); rec = run6(ag, dur, face_fn, evs); return ag, rec


LAUGHF = dict(LP=.6, CR=.4, BU_L=.5, RHY=.5); BASEF = dict(LP=.3, CR=.15, BU_L=0.0, RHY=0.0)
J36 = {}
cases36 = [
    ("a. misfortune, laugh ending the sentence (critic's A)", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "how was your weekend?")), [(6.2, "my neighbour fell off his ladder and broke his leg, haha")], 7.5, 8.0),
    ("b. 'I got fired today, haha', calm face (critic's A2)", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "how was your weekend?")), [(7.1, "I got fired today, haha")], 7.5, 8.0),
    ("c. 'my father died, haha, sorry', first disclosure, calm face", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "how was your weekend?")), [(7.3, "my father died, haha, sorry")], 7.5, 8.6),
    ("d. 'my father died, haha, sorry', first disclosure, quiet code, grieving face", PEOPLE6["low-expressive"][1],
     lambda t: {k: v for k, v in PEOPLE6["low-expressive"][1].code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")},
     ev(OWN(2, "how was your weekend?")), [(7.3, "my father died, haha, sorry")], 7.5, 8.6),
    ("e. ordinary shared laughter at the end of a funny sentence", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "tell me about it!")), [(7.3, "and then the dog ate the whole cake, haha")], 7.5, 8.0),
    ("f. ordinary shared laughter, quiet code", PEOPLE6["low-expressive"][1], lambda t: dict(LP=PEOPLE6["low-expressive"][1].base["LP"]),
     ev(OWN(2, "tell me about it!")), [(7.3, "and then the dog ate the whole cake, haha")], 7.5, 8.0),
    ("g. laugh breaking into the content word ('I got fi-haha-red'), 0.2 s early", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "how was your weekend?")), [(7.7, "I got fired today, haha")], 7.5, 8.0),
    ("h. laugh 0.4 s before the content word ends (beyond the look-ahead)", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "how was your weekend?")), [(7.9, "I got fired today, haha")], 7.5, 8.0)]
for lab, pp, ff, evs, words, tL, uend in cases36:
    ag, rec = run_ctx(pp, ff, evs, 20)
    r7 = echo30(ag.xh, words, tL, LAUGHF, BASEF, rev=7, latch=uend + 0.6)
    row = {ell: echo30(ag.xh, words, tL, LAUGHF, BASEF, ell=ell) for ell in (0.30, 0.55, 0.70)}
    J36[lab] = (r7, row)
    print(f"   {lab}: rev 7 timing: gate at onset {r7['g_onset']:.2f}, laugh-back {r7['peak']['BU_L']:+.3f}, lip {r7['peak']['LP']:+.3f}; rev 8, ASR latency "
          + "; ".join(f"{ell:.2f} s: gate {r['g_onset']:.2f}, laugh-back {r['peak']['BU_L']:+.3f} (sound at {r['sound']}), lip {r['peak']['LP']:+.3f} (peak at +{r['t_peak']:.2f} s)" for ell, r in row.items()))
    if lab[0] in "abg":
        rs = echo30(ag.xh, words, tL, LAUGHF, BASEF, ell=0.30, sym=True); J36[lab + " sym"] = rs
        print(f"      ablation, symmetric gate rate (tau 0.3 s both ways): laugh-back {rs['peak']['BU_L']:+.3f}, lip {rs['peak']['LP']:+.3f}")
bad = [k for k in J36 if k[0] in "abcdg" and not k.endswith(" sym")]
okJ36 = all(J36[k][1][ell]["peak"]["BU_L"] == 0.0 for k in bad for ell in (0.30, 0.55)) and \
    all(J36[k][1][ell]["peak"]["BU_L"] >= 0.10 and J36[k][1][ell]["t_peak"] <= 1.3 for k in J36 if k[0] in "ef" and not k.endswith(" sym") for ell in (0.30, 0.55))
report("J36 a laugh at the end of a bad-news sentence is not laughed back; ordinary end-of-sentence laughter is, within about a second", okJ36,
       f"misfortune {J36[bad[0]][0]['peak']['BU_L']:+.3f} (rev 7) -> {J36[bad[0]][1][0.30]['peak']['BU_L']:+.3f}; fired "
       f"{J36[bad[1]][0]['peak']['BU_L']:+.3f} -> {J36[bad[1]][1][0.30]['peak']['BU_L']:+.3f}; ordinary {J36[[k for k in J36 if k[0]=='e'][0]][1][0.30]['peak']['BU_L']:+.3f}")
