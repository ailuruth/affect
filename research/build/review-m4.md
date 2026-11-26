# Review of the M4 offline core: the new innate constants, the G₀ budget conflict, the README approximations

Independent reviewer, 2026-11-26T23:30:55Z. I did not write the code. Read: `engine/config/innate.py`, `INNATE.lock`,
`innate_names.txt`, `git diff 8519146 812a80c` on those three files (and the M4 commits that touch them, f33e62d to
812a80c); `engine/routes/cone.py`; `engine/invariants/asserts.py` (A6); `engine/state/body.py` (A_F, N_L);
`engine/README.md`; research/build/spec.md §1.3, §1.5, §3.3, §4.3, §6; design-cayley-ledger.md (revision 9.2: the
audit table S1–S50 and M1–M8, §2.5 "Held cone", §2.7, the assembly list); design-cayley-ledger.r5.md §2.1, §2.5–§2.7
(where the values come from) and r6 §2.1, §2.5; questions.md Q29 and DECISIONS.md D88. I ran
`tests/test_innate_names.py` and `tests/test_cone.py` (16 passed) and one short numeric check of A6 under three dyad
priors (below). Nothing was committed, downloaded or left running.

## Verdict: CHANGES NEEDED (one real defect, the rest is text)

None of the 23 new constants is a situation-specific rule, and none comes from the threat silencing or the squint
drop that revision 9 removed (audit S5): there is no constant, branch or comment for either anywhere in `engine/`.
All 23 values match their sources (r5 §2.5–§2.7, spec §1.5) digit for digit, and no M0 value was changed (the diff
of `innate.py` only adds lines). The one real problem is the G₀ entry LP ← f_glare: it is a legitimate part of the
kept threat reflex (S41), but it has been **too large for its budget since revision 6**, and the code's A6 does not
count it at all unless the dyad prior happens to sign the pair one way. Fix it before the M3 sign prior is loaded.

### Ranked list

1. **(high) LP ← f_glare is over budget, and A6 under-counts it.** See Part 2. Fix: resize the two entries to fit
   F_m s_X c_LP (−0.012 on the 2-min trace, −0.0035 on the 20-min trace), and charge every non-reflected G₀ cross
   entry at weight 1 whatever the dyad prior says. Spec-owner change; no operator decision.
2. **(medium) README's statement of the budget use is wrong.** It says the entry "uses 86 % of LP's budget as an
   unsigned pair (weight 0.3)". The code classifies an unsigned face pair as `forbidden`, so the entry is charged 0
   and learned entries may fill the whole LP budget on top of it. Correct it with item 1.
3. **(medium) N_L's "low-information" rule is implemented stricter than the design.** The design defines it (audit
   S39): an utterance lowers the need estimate *in proportion to the population reader's confidence* in its
   decoding. The code lets no utterance lower N_L. Needs a spec-owner definition of that confidence (Part 3).
4. **(low) A_F has had no formula since revision 3.** Holding it at 0 is safe and matches A14's declared update terms
   (which list none for A_F). The spec should say A = A_L, or define A_F. Spec owner.
5. **(low) g_o is written twice in the spec** (in a_laugh and at assembly). The README's reading (once, at assembly)
   matches the design's numbers. Spec text fix.
6. **(low) Three category labels are loose** (no behaviour change; A15 passes): `own_synergies` is tagged `ceiling`
   but is the agent's own muscle synergies (design's assembly list: newborn structure; better `newborn`);
   `face_channels` is the D70 data scope (better `generic`, fit definition); `embedding_dims` is a model size
   (better `generic`, engineering). `echo_gate_unread` is a type rule (rule 11′); `ceiling` is acceptable.
7. **(info) Two README definitions need the spec owner's confirmation:** "addressed" utterances (h_word) = all of his,
   and "partner-initiated" (I, and the S40 credit rule) = not directly after an agent turn. Both are reasonable and
   name no situation, but the spec does not define them.

## Part 1. The 23 new constants

The binding rule (Q29, D88; spec §3.3, A15): innate only for body, reflexes, newborn muscle patterns, per-expression
copy ceilings and general learning biases, plus `generic` parameters that name no situation, scene, user type or
event. Every row below was checked against the audit row that keeps its mechanism.

| Constant | Tagged | Kept by | Allowed? | Note |
|---|---|---|---|---|
| `cone_away_caps` | ceiling | r5 §2.5 table (a_m, r_m) | yes | structural caps on every away entry, every situation |
| `cone_lateral_rows` | ceiling | r5 reflection rule | yes | which rows are lateral; TILT excluded, as r5 |
| `own_synergies` | ceiling | design assembly list; M8 | yes | the six r5 synergies, renamed by channel codes; members and signs match r5. Label: `newborn` fits better |
| `derived_feature_sign_as` | ceiling | r5 §2.5 | yes | sign convention (f_glare as BL etc.); not the squint drop |
| `face_channels` | ceiling | spec §3.1, D70 | yes | data scope; label `generic` (fit definition) fits better |
| `echo_gate_unread` | ceiling | rule 11′ | yes | a type rule; removes inputs, never adds a route |
| `p_name_max` | ceiling | S49, P4 | yes | attenuate-only bound |
| `g0_glare_to_HG` | reflex | S41 | yes | gaze away from a glare, by reflection; 0.25 ≤ a_0 = 0.25, 0.05 ≤ a_1 |
| `g0_glare_traces` | reflex | S41 | yes | trace placement of the S41 entries (r5 finding 6 moved them off the 20-s trace) |
| `appraisal_return_channels` | reflex | S44 (glad-with) | yes | the social smile and laugh back |
| `appraisal_orient_basis` | reflex | S44 (startle-orient) | yes | 0.10 ≤ the 0.15 away cross cap |
| `pi0_rise_voice` | newborn | S45 | yes | the own-rise row's lower voice |
| `pi0_drop_row` | newborn | S45 | yes | own relief row; values = r5 |
| `pi0_word_latch_row` | newborn | S45 | yes | r5's hurt row, driven by the agent's own latch h_word, not by a scene |
| `pi0_activation_row` | newborn | S45, M6 | yes | |
| `pi0_low_energy_row` | newborn | S45 | yes | |
| `pi0_progress_drop_row` | newborn | S45 | yes | r5's curiosity-relief row |
| `pi0_driver_shape` | newborn | S45 | yes | saturations of the row drivers |
| `appraisal_net_shape` | bias | spec §1.5.2 | yes | network size |
| `display_delta_shape` | bias | spec §1.5.3 | yes | network size and its 0.3 bound |
| `embedding_dims` | bias | spec §1.2.6 | yes | label `generic` (engineering) fits better |
| `listener_display_form` | generic, fit def. | spec §1.5.5, §3.2 | yes | names two turn events; see below |
| `qhat_form` | generic, fit def. | spec §1.5.5 | yes | input list of the logistic model |

What is correctly *absent*: the removed r5 rows c_L (S27), familiarity (S28), greeting (S25), the sigh's gaze drift
before a bid (S35) and the turn-onset brow (S36) are not in Π₀; the G₀ sympathy, accommodation and away-diagonal
entries (S29–S31) are not in G₀; rule J is gone from `synergy_sign_table` (M8).

**`listener_display_form` names two events** (`his_utterance_end`, `session_start`). A15 forbids a generic value that
names an event. These are the spec's own T feature anchors (time since the event, 2-s bins), present in every
session and every turn, and whose weights are fitted from dyads, starting at 0. `session_start` is the design's
learned replacement for the removed greeting flash (S25): it is the source that makes a rule unnecessary, not a rule.
I accept it; its `why` should say "feature anchor; weights fitted from recorded listeners".

**Threat-reflex entries and revision 9's audit.** S5 removed the *threat silencing* (the posture's face load blanked
while he glares) and the 8.1 *squint drop* (his BL and LPR taken out of what the posture read). Both belonged to the
posture, which is gone. S41 separately *keeps* the threat reflex V_F and its G₀ entries, naming them: "gaze away from
a glare; LP ← glare −0.035, BI ← glare +0.006". So `g0_glare_to_HG`, `g0_glare_traces` (and the M0 entries
`g0_glare_to_LP`, `g0_glare_to_BI`) are the kept reflex, not remnants of S5.

## Part 2. The budget conflict on LP ← f_glare

**What the code does.** f_glare enters the cone as BL (`derived_feature_sign_as`); LP and BL are both face channels,
so LP ← f_glare is a face pair, signed only by the M3 dyad prior. Checked with `check_a6` on G₀ alone:

| dyad prior on (LP, BL) | class of −0.035 | charged | A6 |
|---|---|---|---|
| 0 (none, today) | forbidden (G₀ exempt) | 0 | silent |
| +1 | forbidden (G₀ exempt) | 0 | silent |
| −1 (his frown goes with a listener's smile falling) | charged, weight 1 | 0.035 vs 0.01225 (m 1); 0.010 vs 0.0035 (m 2) | **fires on traces 1 and 2** |

Budgets: F_1 s_X c_LP = 0.7 × 0.05 × 0.35 = 0.01225; F_2 s_X c_LP = 0.2 × 0.05 × 0.35 = 0.0035. A prior of −1 is the
likely outcome (a listener's lip pull and a speaker's brow lowering rarely rise together), so A6 would fire, and its
fail-safe would drop the cone to G₀ and the diagonal, which still contains the offending entry.

Two defects follow:
- **Under prior 0 or +1 the entry is not charged at all.** `usage` adds nothing for a `forbidden` entry, so
  `project_learned` leaves LP's full charged budget to learned entries on non-face pairs (e.g. LP ← EN, signed +1 by
  the joy synergy). LP's cross total can then reach 0.035 + 0.012 on the 2-min trace. A6's docstring ("innate G₀
  entries are exempt from the prior, not from the budgets") is not what it does.
- **Under prior −1 the entry breaks the budget**, and with it the pooled-share argument of A0 / Lemma S for LP
  (pooled total 0.974 c_LP; the extra 0.023 / 0.35 = 0.065 c would take it to about 1.04 c).

**Where it came from.** r5 §2.5 sized the entries to r5's shares: s_X(LP) = 0.15, so F_1 s_X c = 0.0368 ≥ 0.035 and
F_2 s_X c = 0.0105 ≥ 0.010, charged at weight 1 because rule J signed joy against sadness. Revision 6 cut s_X(LP) to
0.05 (to make room for the onset lobe r_k = 0.608) and stated "G₀'s entries are unchanged and inside the new budget
sets (the charged entries on LP, BI and TILT are below F_m s_X c_k for the new s_X)" (r6 §2.5). For LP that was false
(0.035 > 0.012), and it carried through revisions 7–9.2 and the spec unchecked. BI ← glare (0.006 ≤ 0.010) is fine.

**Should the entry exist after revision 9?** Yes, at a size that fits. It is not part of the removed threat silencing
(S5): it is listed by name under S41, which revision 9 kept as a reflex, and in the held-cone text (§2.5) and spec
§1.5.1. It acts on every glare aimed at the agent, whoever he is and whatever the scene, so it is a reflex, not a
situation rule. What is wrong is only its size, a bookkeeping error from revision 6.

**The correct, non-situational resolution.**
1. Resize: LP ← f_glare = −0.012 (trace 1) and −0.0035 (trace 2), i.e. at most F_m s_X c_LP, the same rule r5 applied
   to the 20-s-trace entries (its finding 6). Its visible effect shrinks from −0.035 f_glare to −0.012 f_glare on lip
   pull, an attenuation only.
2. Make the budget independent of the prior: charge every non-reflected G₀ cross entry at weight 1, whatever M3 finds
   (the worst case over priors), and subtract it from the learned budget. Then G₀ fits its sets before and after M3,
   and A6 can never fire on G₀.
3. Add a test: G₀ inside its budgets under priors −1, 0 and +1 on every G₀ pair.
4. Update `g0_glare_to_LP` in `innate.py` and INNATE.lock (a reviewed change), spec §1.5.1, and the design's §2.5 and
   S41 text, with a line in the history: "r6's share change left LP ← glare over budget; resized".

Not acceptable: raising s_X(LP) (LP's pooled total would exceed 0.996 c), exempting G₀ from the budget, or making the
entry depend on the prior's outcome (that would make an innate constant's legality depend on data). Deleting the LP
entry outright is also safe and non-situational (it only removes an output); it is the spec owner's choice, but
revision 9 kept it on purpose, so resizing is the smaller change.

## Part 3. The README's approximations

| README item | Design | Needs |
|---|---|---|
| g_o applied once (free display carries 0.40 q̂; g_o multiplies the smile–laugh part at assembly) | S18 and design §2.1: "a_laugh = 0.40 q̂ · g_o"; spec §1.5.4: "g_o only the agent's own smile–laugh displays (drop, contact drop, own laugh)". The design means one g_o; the spec wrote it in both places | **spec text fix only** (owner): write a_laugh = 0.40 q̂ and say g_o is applied at assembly. State that g_o then acts on the whole envelope at render time rather than being latched at his turn; the bound 0.40 still holds since g_o ≤ 1 |
| A_F held at 0 | A_F ("slow loudness and motion", F) has never had a formula (r3–r5 name it only); spec A14's declared update terms for A are only A_L's | **design decision (spec owner)**, low stakes: delete A_F (A = A_L) or define it. A new formula would be a new innate route from his loudness and motion into the body and would need its own audit row. Holding 0 is attenuate-only and safe meanwhile |
| "low-information" undefined; every utterance only raises N_L | S39 does define it: lowering "only in proportion to the population reader's confidence in its decoding (low-information evidence counts only upward)" | **design decision (spec owner)**: name the confidence measure (e.g. the reader's predicted-variance or a calibrated probability, fitted with it at M3; a `generic` fit definition) and implement N_L ← N_L − c · (N_L − r)₊ alongside the max. With today's untrained reader set its confidence to 0, which gives the current behaviour, so no M4 result changes. As built, a confident "it's fine now" can never lower his need estimate, a behaviour the design did not choose |

None of the three needs the operator: they are spec-owner decisions. The operator questions open for M1 are Q34
items 4, 5 and 10 (and, for the Claude checks, item 1); see research/build/handoff.md.
