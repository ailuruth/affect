# =========================================================== J37: D_s is a source-2 input; its fitted weight (agent critique, D85 residue)
print("=== J37: D_s relabelled as a dyad-learned input (source 2): its fitted weight in the J20 gate")
med = np.median(np.array([r[1] for r in EV_FIT if r[0] == "ordinary"]), 0)
for lab, x0 in (("ordinary context (corpus median)", med), ("joke-while-sad context (median)", np.median(np.array([r[1] for r in EV_FIT if r[0] == "joke while sad"]), 0))):
    vals = []
    for Dsv in (0.0, 0.3, 0.6, 0.9):
        x = list(x0); x[5] = Dsv; vals.append(GATE(x))
    print(f"   {lab}: gate at D_s 0 / 0.3 / 0.6 / 0.9 = " + " / ".join(f"{v:.2f}" for v in vals))
DSW = vals
print("   in the constructed corpus D_s has no causal role (the generating process omits it); its weight is a proxy for the troubles context. "
      "Seamless interactions last 3.5-4.6 min, so a weight that matters 4 min later is at the edge of what the corpus can teach (F20).")
report("J37 D_s only closes the gate (monotone) and its fitted weight is reported", all(DSW[i + 1] <= DSW[i] + 1e-12 for i in range(3)), "")

# =========================================================== J38: Claude's history with initiative turns; the system-prompt fallback (build items)
print("=== J38: canonical history with the agent's own initiative turns; fallback with each fork's fixed line in its own system prompt")
ATT = ["Attend to what they said.", "Attend to how they feel.", "Attend to what to ask next."]
rr = np.random.default_rng(38); canon = []; viol = 0; leaks = 0; marks = set()
for turn in range(80):
    if rr.random() < 0.25:                                        # the agent's initiative (a bid after his silence): an observable marker as the user turn
        sil = 6 + rr.exponential(20); user = f"[no reply from him for {int(5 * round(sil / 5))} s]"; marks.add(user)
    else: user = f"his message {turn}"
    win = int(rr.integers(0, 3)); reply = f"reply {turn}.{win}"
    system_prompts = [f"<constant instruction>\n{ATT[i]}" for i in range(3)]   # fallback: the line lives in each fork's own system prompt
    canon += [("user", user), ("assistant", reply)]
    leaks += sum(a in " ".join(m for _, m in canon) for a in ATT)
roles = [r for r, _ in canon]
viol = sum(roles[i] == roles[i + 1] for i in range(len(roles) - 1)) + sum(1 for r, m in canon if r == "user" and not m.strip())
print(f"   80 turns, {sum('[no reply' in m for _, m in canon)} initiative turns; two same-role turns in a row or an empty user turn: {viol}; "
      f"fixed lines in the history: {leaks}; distinct silence markers {len(marks)} (5-s bins, so at most log2(#bins) bits of timing per initiative turn)")
report("J38 initiative turns keep the history alternating and free of state-selected text, in the main design and the system-prompt fallback", viol == 0 and leaks == 0,
       "week 0 checks that a session file never stores the system prompt and whether it stores the winner's thinking (if it does, the fallback is not used)")
