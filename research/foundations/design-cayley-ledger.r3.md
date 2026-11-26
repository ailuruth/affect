# Cayley–ledger core, revision 3: know the partner fully, move away freely, move toward only a little

Seventh design of the S0 cycle, revision 3. Written 2026-11-26 under questions.md Q16, Q17 as relaxed by Q19 (precise object, convincing argument, concrete failures only), Q18 and its answer (DECISIONS.md D78, D80), Q20 on its recommended reading (the inner state may know the partner closely; only expression is bounded), and with Q21 open (a sound recombination may still be put to the operator).

Revision 1 is kept as `design-cayley-ledger.r1.md` and revision 2 as `design-cayley-ledger.r2.md`, each with its critiques and answer. Algebra checks for this revision: `foundations/sims/design-g3/checks.py` (G1–G9, `python3 -I checks.py`, numpy and scipy, about 30 s; output in `out.txt`, 25/25 pass). They check this design's own inequalities and constants on constructed instances. They are not evidence about behaviour or people (brief: no toy worlds), and the scenario numbers in §3.12 are what the design's equations give for stated inputs, nothing more.

**Status:** revision 3, not yet critiqued.

## 0. Summary

**What changed from revision 2.** Revision 2 put the whole slow mind inside one two-sided bound. The critics showed three things: the bound leaked (the slow mind's knowledge reached the fast block as unbounded context, so the agent's pitch followed the partner's at 0.92); it muted the agent (±0.15 in every direction); and the agent had no gladness, never spoke first, could not be regulated by Claude, and its care learned to flatter. Revision 3 keeps the fast Cayley wrap and the knowing/moving separation, and changes four things:
1. **Typed state.** Every state variable carries one of three information-flow types: **T** (the partner's words and turn sequence, the agent's own innate body, identity), **F** (anything computed from the partner's face, voice levels or timing) and **Ω** (the agent's own words and choices). T-typed state drives the face freely. F-typed state reaches the face only through the fast wrap and a new one-sided slow cone. Ω reaches it only through two capped ports.
2. **The one-sided slow cone** replaces the two-sided ℓ∞ ball. The slow, face-driven display is y_F = Σ_m G_m(z) ξ_m, where the ξ_m are first-order traces of the partner's face (20 s to 3 h) and each G_m has its symmetric part below b_m·I. Toward the partner the agent moves at most 0.10 per channel, along any direction and at every time after onset (the late-window delayed copy stays closed); away from the partner it can move up to 1.40, and across channels up to 0.49 per pair.
3. **Positive affect, initiative and regulation.** Valence is the signed rate of the agent's own drive reduction (Joffily & Coricelli; Keramati & Gutkin), with satiable contact (K) and play (P) deficits relieved only by the structure of the agent's own exchanges. A body onset starts each turn at about 300 ms. A softened follow-up comes after 1.5 s of silence following an agent question, and a concern-triggered bid comes in a lapse. Concern rises in about 40–75 s. The agent hears its own words: naming that matches its body contracts its state toward set point.
4. **Care that helps without placation.** The partner is modelled in three parts (need N, display F, report-and-choice Q). In every planning rollout the display is held at its default-act value, need is read only from unprompted words and choices through a frozen decoder, and a small capped options term is added. Perception reads the partner's face itself, not the face minus the agent's own display.

- **What is bounded, for every parameter value (per channel unless stated; 1 = full copy):**

  | Quantity | Bound | From |
  |---|---|---|
  | zero-lag in-phase, any band | ≤ 0.185 (+ a-route 0.20 × corr) | fast wrap, γ_f = 0.45; the cone adds < 0.001 where the fast wrap peaks (G8) |
  | held level, in phase | ≤ 0.10 (cone) + 0.05 (naming port) = 0.15 | §3.3, §3.7 |
  | held level, same channel, away | ≥ −1.40 | cone |
  | cross-channel, per pair / per row | ≤ 0.49 / ≤ 0.60; synergist pairs ≤ 0.10 | cone |
  | in-phase step response, **any direction, every time after onset** | ≤ 0.10 (cone) | §3.3, G2b (r2's ℓ₂ disc allowed +0.265 at 60 min) |
  | any 1-min mean during a hold | ≤ 0.21 | cone + port + naming + edges |
  | 10-min means | ≤ 0.155 | — |
  | phrase targets sampled at turn onset (pitch, energy, rate, pause, latency) | ≤ 0.10 (cone) + 0.05 (naming) | they read only the cone and T state (G1a: 0.046; r2 route: 1.24) |
  | jaw while listening (K1b) | ≤ 0.185 + a-route | bias-free gates (G1d: 0.065; r2: 0.83) |
  | dyad with a partner who mimics at gain μ ≤ 2 | stable | numerical range of the cone (G2e) |

- **The agent in the critic's scenarios** (design constants; §3.12; peak values of 0–1 channels):

  | Scenario | What the agent does |
  |---|---|
  | silently sad user | concern crosses threshold at 41–74 s; one gentle bid then ("You've gone quiet"); held lip-corner warmth 0.17 and a slight head tilt from the cone; when he answers, word-driven concern adds brow 0.25, lip 0.20 |
  | good news, laughing | with an earlier worry on the topic: smile 0.44, F0 range +0.22, its own laugh 0.22 (cold: 0.31, +0.18, 0.18); fast echo 0.15 at onset; unchanged if his laughter is muted |
  | anger at the agent | startle ≤ 0.20; hurt brow 0.32, lip-corner depress 0.25, gaze away 0.23, slower replies; hurt brow still 0.19 at 10–15 min |
  | long warm talk (2 h) | play laughter 0.24 → 0.11 → 0.04 (satiates); relief smiles 0.30 when small worries resolve; held warmth 0.15 throughout |
  | return after a week | greeting brow flash, then smile 0.58, cheek 0.40, F0 range +0.36 for about a minute (stranger: 0.35); remembers last week's topics |

- **New weakest point (§8.1).** Everything strong and held on the face comes from T-typed state: the partner's words, the turn sequence and the agent's own body. That rests on one definitional seam: words and turn sequence count as common cause, as in revision 2. A cone gated by words, for a partner whose face co-varies with topic, gives a pooled smile slope of 0.56 across topics, while within a topic it stays ≤ 0.10. Face-derived feeling shows on the face only through the linear cone.
- **Novelty verdict (author): recombination.** The one-sided cone is the "directional certificate for persistent state" the revision-2 critic asked for. Its parts are textbook (a positive-real MIMO sector, numerical range, completely monotone kernels); the care part is Yoshida & Man plus Farquhar's path-specific objectives with the need/display split. §10.

## 1. Plain-language intuition

The agent still has one door, and the whole house can see the partner clearly. What is new is a rule about which thoughts may move the agent's face, and how.

- **Thoughts that come from what was said, from the back-and-forth of the conversation, or from the agent's own body** (tiredness, missing someone, wanting to play, being hurt by an insult) may move its face and voice as strongly as they like. If you tell it your dog died, it looks sad because of what you said. If you come back after a week, it lights up because it missed talking with you, not because you smiled.
- **Thoughts that come from your face and voice** may move its face in two ways:
  - **the quick gear:** a small, brief echo or counter-move in the first seconds after you change, as before;
  - **a slow gear that only pushes one way:** it can move away from your expression, or into other expressions, strongly and for as long as your expression lasts, but toward your expression only a tenth of the way, at every moment.

  Your sad face can make it soften and smile gently, tilt its head and speak; it cannot make it slowly turn into your sad face.
- **Claude** chooses what the agent says. The agent then hears its own words. When the words name what it feels, the feeling eases a little, the way naming a feeling eases it in people. Claude never sees the feeling as numbers or labels.
- **Care** is reading how you are from what you say and choose to do, and doing what helps. The agent is never paid for how your face looks afterwards, nor for getting you to say "I'm fine".
- **Gladness** is a deficit being relieved: an old worry about you resolved, a reunion after missing you, a playful exchange. It is bounded by how much was missing, so it cannot be farmed.

## 2. The object

### 2.1 Channels, time and every constant

Time is discrete at the camera rate f_s = 30 Hz (Δ = 1/30 s) except where stated. Every channel is normalised so that its innate nominal range is [0, 1] (signed channels [−1, 1]).

**Counterpart channels (n = 32, unchanged from revision 2; the copy metric is defined on these):**

| Group | Channels | n |
|---|---|---|
| symmetric face | brow inner raise (BI), brow outer raise, brow lower (BL), upper-lid raise, lid tighten (LT), cheek raise (CR), nose wrinkle, lip-corner pull (LP), lip-corner depress (LD), lip stretch, chin raise, lip press, dimpler, head pitch; vertical gaze | 15 |
| lateral, **reflected** by P | head yaw, head roll (TILT), horizontal gaze | 3 |
| articulators | jaw open (JO), lip funnel, pucker, mouth close, lip roll | 5 |
| voice and timing (phrase or turn level) | F0 level, F0 range (FR), energy (EN), speech rate (RT), within-turn pause, response latency (LAT) | 6 |
| non-lexical vocal bursts | non-lexical voiced energy (BU), 4–6 Hz burst-rhythm energy, breathiness | 3 |

**Exogenous partner inputs** a ∈ [0,1]³: audio onset envelope, partner VAD, partner turn-end pulse. These enter the fast block only through √κ_a. **Non-counterpart output:** blink (startle reflex, route R7).

**Innate constants (compiled in, not parameters).**

| Symbol | Value | Meaning |
|---|---|---|
| **fast wrap (kept)** | | |
| κ, κ_lat, κ_a | 0.30, 0.05, 0.05 | wrap weights |
| γ_f | 0.45 | fast block gain; disc: in-phase ≤ 0.186, anti ≥ −0.491, lag ≤ 0.339 (κ = 0.3) |
| H_i, H_o | first-order high-pass, τ = 4 s, at the input and the output of S_f | the fast block sees and makes no DC |
| filter bank, lag line, ℓ_echo, M(s), own innovation d | as revision 2 (bands 0.15–4.5 Hz; lags 0.15–0.8 s; echo 0.45 s; muscle filter 4 Hz, ζ 0.8; d sd 0.04 at 2.6–6.5 Hz) | — |
| fast gates g(c̃) | per REN output, in [−1, 1]; c̃ is T-typed only (§2.5) | context sets fast sign and size |
| **one-sided slow cone (new)** | | |
| traces ξ_m | first-order low-passes of Pu with τ_m = 20 s, 2 min, 20 min, 3 h | completely monotone kernels |
| b_m (in-phase budget) | 0, 0.05, 0.03, 0.02 (Σ b = 0.10) | sym(G_m) ⪯ b_m I |
| N_m (same-channel away reach) | 0.50, 0.40, 0.30, 0.20 (Σ 1.40) | diag(G_m) ≥ −N_m |
| a_m (off-diagonal entry cap) | 0.25, 0.12, 0.08, 0.04 (Σ 0.49) | \|G_m,kj\| ≤ a_m |
| r_m (off-diagonal row cap) | 0.30, 0.15, 0.10, 0.05 (Σ 0.60) | Σ_j\|G_m,kj\| ≤ r_m |
| synergist mask | pairs that co-activate in the agent's innate synergies (P₀: LP–CR, BI–brow outer, BI–BL, BL–LT, BI–LD, LD–chin raise, LP–lip stretch, jaw–lip funnel, FR–EN, burst–breathiness, …; 23 pairs, fixed list) | entries on these pairs ≤ b_m |
| lateral channels in the cone | same-channel coefficient in [−b_m/6, +b_m/6] (both handednesses capped) | revision 2's K4 lesson |
| basis count | 16 valid patterns per trace; G_m(z) is their convex mixture | the valid set is convex |
| **ports** | | |
| P_Ω (face port) | joint cap a_Ω = 0.10 per channel, output high-pass τ_Ω = 15 s, G_Ω(0, ·) = 0 | zero DC; not in phrase targets |
| P_name (heard own words) | match m ∈ [0, 1] (§2.10.4); F-typed loads: latched rate ρ_F = 0.08·m per 30 s, decaying with τ = 2 min; T-typed loads: attenuation n ≤ n_max = 0.17, latch rate 0.4·m per 30 s, relaxing with τ = 5 min | attenuate-only |
| a_name | 0.05 | held face allowance of P_name: display gains on attenuable loads ≤ 0.30, × n_max = 0.051 |
| **body and drives** | | |
| 𝒟(b) = Σ_i w_i ψ(\|b_i − b_i*\| − δ_i)₊, ψ(x) = x² | E (0.7, 0.2, 1.0); A (0, 0.15, 0.7); V (0, 0.05, 1.0); K (0, 0.10, 0.6); P (0, 0.10, 0.5); I (0, 0.1, 0.5) | (set point, dead-band, weight) |
| E, energy | −0.04 %/min awake; restored only during the nightly sleep/replay period, to 0.85 | no incentive to end conversations |
| A, activation load | A_F (slow loudness and motion, F) + A_L (latched lexical surprise, T); τ = 3 min | held latch, not impulses (K4) |
| V, aversive load | V_F (aversive part of b̂_p × gaze-at-agent; loudness above 0.7; F) + V_L (latched hostility of the partner's last utterance addressed to the agent; T); τ_up 40 s, τ_down 10 min | — |
| K, contact deficit (new) | rise (1 − K)/τ_K, τ_K = 36 h; per completed exchange K ← K(1 − 0.25 f_id) | f_id ∈ [0.15, 1]: familiarity from the identity slot (T) |
| P, play deficit (new) | rise (1 − P)/τ_P, τ_P = 5.05 h (half-maximal at 3.5 h, Vanderschuren); per play-structured exchange P ← 0.85 P, only while V_L, C_L < 0.1 | play-structured: §2.8.3 |
| I, own-forecast uncertainty | as revision 2 | F/Ω (reads 𝓜) |
| **care and valence** | | |
| w_C | 0.8 | care weight on 𝒟_p(N̂), the agent's own 𝒟 at the partner's inferred loads (E, A, V, K, P) |
| face evidence | 20-s trace; care concern C_F: attack τ = 40 s, release 10 min | F |
| word evidence | N_L set by unprompted reports, decays τ = 30 min, topic slots 30 days; C_L tracks w_C 𝒟_p(N_L) with τ = 40 s both ways | T |
| θ_C | 0.10 | concern threshold for a lapse bid |
| valence | v = −d𝒟_tot/dt and v_T = −d𝒟_T/dt (per minute), smoothed τ = 5 s | readouts |
| V₀ | 0.30 per min | display half-saturation: r = v⁺/(v⁺ + V₀), d = v⁻/(v⁻ + V₀) |
| **initiative** | | |
| body onset | partner VAD offset + 0.30 s + 0.25 s × y_LAT (y_LAT ∈ [−0.4, 0.8]), floor 0.20 s | no waiting for Claude |
| pursuit | 1.5 s of no partner voice after an agent question; one per silence | Bögels: re-offer at ~1.7 s |
| lapse bid | mutual silence ≥ 6 s, no turn owed, C ≥ θ_C; one per lapse; refractory until a partner turn or 3 min | — |
| greeting | partner presence onset with K ≥ 0.3: brow flash 0.35 for 0.4 s at 1.0 s, voiced "oh" burst | — |
| **Ω** | | |
| drafts | K_d = 6 (one is a softened follow-up variant); temperature 0.1 × (1 + r) | broadening with positive valence |
| scoring horizon | 30 s of 𝓜 rollout at 2 Hz | — |
| options term | w_opt = 0.05 × w_C; counts distinct partner-initiated moves; zero inside 𝒟_p's dead-band; ≤ 3 per 10 min | Franzmeyer, Du |
| retrieval | ≤ 3 snippets; ALiBi slope 1/(7 days) | — |
| concepts | DP-means λ_DP = 1.5, ≤ 64 categories; PMI over the agent's own tokens only (naming); ±1 turn | — |
| replay | gradient clip G = 1; pull to θ₀ λ = 0.5 (fast), 0.1 (slow); consolidation λ_n = 0.01; learning rate × exp(−0.5 r) | valence-gated consolidation (Joffily Eq. 4) |

### 2.2 The boundary 𝓑 and the structural checks

𝓑 is unchanged from revision 2 (MediaPipe → P₀ → reflection P → u; GeMAPS-lite after AEC and the half-duplex gate; burst features; normalised ASR; own-tagged second MediaPipe). Checks B1 (imports) and B3 (no read-back except own-tagged) stand. B2 is replaced by Check T.

**Check T (types; replaces B2).** Every state variable and every module output is tagged, at definition, with one type:
- **T:**
  - the partner's lexical word stream, latched per utterance at the partner's turn end;
  - the partner's turn sequence as events (who spoke, in what order; never durations);
  - session boundaries and the identity token;
  - the agent's innate body processes (E, K's and P's rise);
  - anything computed only from these.
- **F:** anything computed from u (face, gaze, articulators, voice levels, timing values, bursts) or from a (VAD, onsets), or from an F or Ω value.
- **Ω:**
  - the agent's own realised words, draft choice and retrieval;
  - its own turn events (onsets, bids);
  - anything computed from these.

The type rule, enforced at module construction and tested at load:
1. A T-typed variable reads only T-typed variables. Exceptions are the two named ports: P_name may attenuate T loads, within a_name, and K/P relief reads exchange *events*, which are T.
2. The counterpart outputs are written only by:
   - y_f, the fast wrap, whose gates read T only;
   - y_F, the one-sided cone, whose coefficients read T only;
   - y_o, the free display, which reads T only (plus the P_name attenuation);
   - y_Ω, the face port;
   - visemes, on the articulators only.
3. Nothing in 𝒦 or Ω is an input to S_f, the cone or the free display except through P_Ω and P_name.

**Why role is T or only a gate.** Role from partner VAD is F. It may appear only as a fast gate (bounded by 1, multiplying partner-input terms; §3.2). The free display may not read "the partner is speaking": its T inputs change only at the partner's turn ends, so they are constant over a partner turn and cannot form a role display (K1b).

### 2.3 Output assembly

y = sat( y_f + y_F + y_o + y_Ω ) + visemes (articulators), where sat clips each channel to its range.

- **Face:** M ∗ (y + blink reflex), rendered continuously.
- **Voice, phrase level (sampled at phrase onset and held):** F0 level, F0 range, energy, rate, pause and latency targets come from **y_F + y_o only**. The fast term y_f is rendered only as a continuous within-phrase contour (zero mean over the phrase), and the port only on the face. This closes the sampling routes K1 and K2 (§3.2).
- **Voice, non-lexical:** bursts come only from y, never from text, as in revision 2.

### 2.4 The fast wrap (kept; every input inside)

- **The loop.** w = K^{1/2}P u − s_f, y_f = 2K^{1/2} s_f.
- **The block.** s_f = H_o ∘ S_f ∘ H_i (w), with

  S_f(ŵ; c̃, a, d) = diag(γ_f σ(φ_k)) · g(c̃) ⊙ A(c̃) · M ∘ 𝓡_θ([Φ_R(F ŵ), √κ_a a]) + d̃.

Three changes from revision 2:
1. **Bias-free in the partner input, for every c̃.** 𝓡_θ has no c̃ input. c̃ enters only through the gates g(c̃) ∈ [−1, 1]^{32} and the attention mix A(c̃) with ‖A‖₂ ≤ 1. Both multiply the partner-input term, so S_f(ŵ = 0, a = 0) = d̃ for every c̃ and every θ. The own innovation d̃ is zero-mean band-limited noise, independent of everything, whose amplitude is set by habituation H. It is uncorrelated with any partner signal, so it changes variance, not concordance.
2. **c̃ is T-typed:** the latched lexical embedding, turn-sequence features, own floor state, identity, E, K, P, C_L, V_L, A_L, v_T and T slot reads. S_s's F states, which know the partner's held level, are not in c̃.
3. **Role and the latch clock are partner inputs.** VAD enters 𝓡 only through √κ_a·a (route R4), and as a gate.

Claim W (revision 1 §3.1) holds for the loop for every gate trajectory: ‖g ⊙ f(w)‖_T ≤ ‖f(w)‖_T ≤ γ_f‖w‖_T on every truncation, for any |g| ≤ 1, even a partner-dependent one (§3.2).

**The innate prior θ₀ (reflexes):**
- an echo at 0.45 s on LP, CR, the brow raises and head pitch, at 0.65 of the fast cap;
- gaze following in the reflected frame;
- own fast head micro-motion gated down by the partner's 2.6–6.5 Hz head envelope (C1);
- a nod at the turn-end pulse;
- a startle at audio onsets.

### 2.5 The one-sided slow cone (the new object)

**Definition.** Let ξ_m(t) = (h_m ∗ Pu)(t) ∈ R^{32}, with h_m(t) = τ_m^{−1}e^{−t/τ_m} (first-order, unit DC), for m = 0…3. Note that the traces read the partner's own face Pu, **not** w = v − s: the agent never perceives the partner as the partner minus itself. The cone is

  y_F(t) = Σ_{m=0}^{3} G_m(z(t)) ξ_m(t),  z = T-typed context (§2.4 list),

with each G_m(z) in the convex set

  𝒢_m = { G : ½(G + Gᵀ) ⪯ b_m I;  −N_m ≤ G_kk ≤ b_m;  |G_kj| ≤ a_m and Σ_j|G_kj| ≤ r_m for k ≠ j;  |G_kj| ≤ b_m on synergist pairs;  |G_kk| ≤ b_m/6 on lateral channels }.

**Parameterisation (complete for 𝒢_m; G2a).**
- G = b_m I − Λ − S + A_sk, where:
  - Λ = diag(λ), 0 ≤ λ_k ≤ N_m + b_m;
  - S is symmetric with zero diagonal;
  - A_sk is skew-symmetric;
  - |S_kj|, |A_kj| are tanh-scaled to ≤ a_m, and to ≤ b_m/2 on synergist pairs;
  - S and A_sk are scaled together, by one common factor, until every row sum ≤ r_m, which keeps S symmetric and A_sk skew;
  - λ_k ≥ Σ_j|S_kj| (diagonal dominance), so Λ + S ⪰ 0.
- Every free vector gives a valid G.
- Since 𝒢_m is convex, the context-dependent G_m(z) = Σ_{r=1}^{16} softmax(α(z))_r G_m^{(r)} is valid for every z and every parameter value.

**What each piece means.**
- **The in-phase budget** b_m. The agent may hold a little of the partner's expression: a slight smile back, a slight concern brow. The total over all traces is 0.10 per channel and in every direction.
- **The away reach** N_m. The agent may hold strongly *less* of a channel the partner shows. That is visible only when its own state has that channel active, for example its own smile lowered by the partner's contempt.
- **The skew part** A_sk carries the expressive cross-responses: "your inner brow rises, my lip corners rise; your smile rises, my inner brow falls". Skew terms add nothing to the in-phase form xᵀGx for any direction x.
- **The symmetric off-diagonal part** S must be paid for by an equal diagonal away-reach: a symmetric cross term needs the away-reach that cancels its in-phase effect.
- **The synergist mask.** It caps cross terms between channels that co-activate in the agent's own innate synergies, so the natural co-movement of a partner's face (for example smile with cheek) cannot carry copy (G2d).

**Innate prior G₀ (newborn reflexes; checked inside 𝒢_m in checks.py):**
- trace 0 (20 s):
  - skew LP ← BI 0.20, LP ← LD 0.10: softening toward a distressed face; the reverse entries make the agent's BI and LD fall when the partner smiles;
  - skew LAT ← EN 0.10: slower replies to a loud voice;
  - −0.20 on the BL, LD, LT and EN diagonals: quieter to loudness, no frown back;
- trace 1 (2 min):
  - +0.05 on the LP, CR and BI diagonals: a small held smile back and a small concern brow;
  - skew LP ← BI 0.06, LP ← LD 0.06, TILT ← BI 0.08;
  - −0.10 on the BL, LD, LT and EN diagonals;
- traces 2 and 3: small anti diagonals (−0.05 and 0).

### 2.6 The free display Π_o

y_o = Π_o(z_T; ψ). It is a 2-layer MLP on T-typed inputs only, trained by J (§2.11) around its innate prior Π₀. Π₀ is the newborn's display of its own body. All gains are per channel; the variables are defined in §2.7:

| Driver (T) | Display |
|---|---|
| relief r = v_T⁺/(v_T⁺ + V₀) | LP +0.55, CR +0.45, F0 range +0.35, energy +0.25; voiced burst (own laugh) +0.45 when the relief comes from a play-structured exchange |
| distress d = v_T⁻/(v_T⁻ + V₀) | BI +0.45, LD +0.35, LT +0.25, F0 range −0.20, energy −0.15 |
| word concern c_L = (1 − n_C)C_L / ((1 − n_C)C_L + 0.1) | BI +0.25, LP +0.20, TILT +0.20, energy −0.15, rate −0.10 |
| hurt h = V_L/(V_L + 0.15) | BI +0.25, LD +0.20, LP −0.25, gaze away 0.30, energy −0.20, latency +0.15 |
| low energy e = (0.5 − E)₊/0.3 | upper-lid −0.30, F0 range −0.25, energy −0.25, rate −0.15 |
| familiarity f_id (identity slot) | LP +0.10 f_id, F0 range and energy +0.05 f_id |
| positivity offset (all T drives in their boxes) | LP +0.06 |
| turn reflexes (body onset) | inhale (breathiness 0.3 for 0.3 s), gaze to partner, brow raise 0.15, voiced opener burst 0.3 if no words within 0.5 s |

- **The valence shape follows Joffily's quadrants.** A fast relief (v rising, then falling) gives the brisk smile and laugh. A slow settling gives the offset and warmth.
- **No display reads F or Ω state** except through the attenuation n_C of P_name.

### 2.7 Body, drives, valence and care

**Body loads (named by function).**
- E, energy;
- A, activation load: A_F + A_L;
- V, aversive load: V_F + V_L;
- K, contact deficit;
- P, play deficit;
- I, own-forecast uncertainty.

Each has a set point, a dead-band and a weight (§2.1). All are satiable: 𝒟 = 0 on the box. K and P are new. Their rise is innate (time without exchange, time without play), and their relief reads **only exchange events**:
- **K** falls at each completed exchange (a partner turn following an agent turn, or the reverse), by a fraction 0.25 f_id. Familiarity f_id comes from the identity slot, which is T: built from the agent's own past K and P relief with this person.
- **P** falls at each **play-structured** exchange (§2.8.3).

Neither reads the partner's face, voice level or laughter.

**Care (not a body variable).**
- The care term is w_C 𝒟_p(N̂): the agent's own drive, evaluated at the partner's inferred loads N̂ ∈ (E, A, V, K, P).
- The partner's inferred body has **no concern coordinate**. This removes revision 2's double count, in which the agent grew concerned at the partner's concern, and its comfort reversal.
- Two readings feed it:
  - **C_F (face, F):** the 20-s face trace → b̂_p = Π̃(R ξ₀) → w_C 𝒟_p(b̂_p), with attack 40 s and release 10 min. Π̃ inverts the agent's own free display Π_o on its own (b, y_o) pairs. Π₀'s distress gains (0.45 on BI) cover the partner's range, so the inverse gain is about 2.2 and nothing is crushed into the dead-band (critic §2.3).
  - **C_L (words, T):** the need decoder (§2.9) reads the partner's unprompted reports and sets the word-need N_L; C_L tracks w_C 𝒟_p(N_L) with τ = 40 s.
- The care-side concern used for J, words, retrieval and bids is C = w_C 𝒟_p(max(N̂_F, N̂_Q)), coordinate-wise.
- The *displayed* word concern is C_L, from the raw lexical reading. This is the T copy that may show on the face.

**Valence (readouts; Joffily & Coricelli, Keramati & Gutkin).**
- v = −d/dt[𝒟(b) + w_C 𝒟_p(N̂)] per minute, used for the draft temperature, the learning-rate gate and naming;
- v_T = −d/dt of the T-typed part of the same sum (E, K, P, V_L, A_L, (1 − n_C)C_L), used for the free display.

Two consequences:
- **Positive valence exists exactly while a deficit is being relieved.** It is bounded: ∫ v⁺ dt ≤ 𝒟(t₀). The integral of positive affect available is the deficit that existed.
- **Nothing maximises v.** The objective J (§2.11) is the integral of 𝒟, which is ≥ 0 and minimised.

### 2.8 Initiative

1. **Body onset at about 300 ms.**
   - **What happens.** At partner VAD offset + 0.30 s + 0.25 s·y_LAT (floor 0.20 s), the body takes the turn:
     - inhale, gaze to the partner, a brow raise of 0.15;
     - an opener on the burst channel ("mm", "oh"), shaped by r and d, if no words are ready within 0.5 s.
   - **When the words come.** They follow when Claude's drafts are ready. Drafts are requested at the partner's predicted turn end (falling F0 plus syntactic completion in the streaming ASR partials, an innate rule) and again at VAD offset.
   - **What it replaces.** Revision 2's R15 (the onset waited 1–3 s for Claude) is gone. Templeton et al.: a fast answer is heard as connection; Bögels et al.: a late answer is heard as trouble.
2. **Softened follow-up.**
   - **Trigger.** The agent's realised turn ended in "?" (the innate punctuation rule on its own text), and there has been no partner VAD for 1.5 s.
   - **What it does.** The agent re-offers once, with the softened variant prepared among the six drafts. The display is a 0.1 tilt and a 0.15 brow raise.
   - At most one per silence. It is never learned from whether the user answered.
3. **Concern bid in a lapse.**
   - **Trigger.** Mutual silence ≥ 6 s, no turn owed (neither party's last utterance was a question to the other, or the follow-up has been spent), and C ≥ θ_C.
   - **What it does.** The body takes the floor (inhale, gaze, brow 0.15). The words come from drafts requested when C crossed θ_C.
   - **Claude's input.** The prompt is constant. The transcript carries an observable "[silence 6 s]" marker, so Claude sees a fact of the conversation, not a state.
   - One bid per lapse; refractory until a partner turn or 3 min. It is never learned from whether the user answered (Knox et al.).
   - **What the bid says.** It is exploration-first by the six-draft scoring: a question or an observation about this moment scores above advice under the need path, because only the partner's unprompted report can lower N̂ (§2.9).
4. **Greeting.** At partner presence onset with K ≥ 0.3: a brow flash and a voiced "oh" at 1.0 s; the words follow.

**Play-structured exchange (for P).** Read from words and turn order only (T):
- the partner's utterance takes up the agent's previous one (it shares a content lemma, or begins with an anaphor or a discourse continuation);
- it adds lexical surprise in the middle band [0.3, 0.8] of 𝓜's lexical surprise range;
- the agent's own last utterance did the same with the partner's;
- V_L and C_L are below 0.1 (safety).

Vanderschuren et al.: the reward of play goes with mutual, alternating engagement, with being pinned as much as pinning, and is absent with a non-playful partner; it does not go with the partner's display.

### 2.9 The partner model in three parts, and care without placation

𝓜's partner head is split into three:
- **N, need:** the partner's slow loads;
- **F, display:** face, prosody, gaze, bursts;
- **Q, report-and-choice:** what their words say about their situation, and the moves they initiate (raising a topic, deciding, asking, declining, closing).

Edges: act → N, N → F, N → Q, act → F (contagion, politeness), act → Q (leading questions).

**Rollout rule (every rollout: draft scoring, J returns that train Π_o, S_f's θ, the cone bases and the scorer).**
1. F is imputed at F_ā, the action-blind head's prediction under the default act ā. Here ā is the agent's innate Π₀ display plus a minimal acknowledgement turn with no content.
2. N is updated by the act through 𝓜's act → N model.
3. N's post-act evidence comes **only** from Q, through a **frozen need decoder**: trained on the agent's own (utterance, own load) pairs (P3), and frozen within a night.
4. Q's direct dependence on the act, not through N, is imputed at ā. Concretely:
   - the decoder gives weight 0 to a partner utterance of ≤ 6 tokens that follows an agent question containing "you";
   - it reads the partner's unprompted content and the next move he initiates.
5. The partner-driven loads (V_F, A_F, the partner part of K's and P's relief) are computed in rollouts from F_ā and from the imputed exchange structure, never from 𝓜's own-body head. The own-body head (i) is trained only on E, I and own-driven A (revision 2's K3 fix).
6. Nothing is credited for lowering V (FeldmanHall et al.: concern, not personal distress, goes with costly help).
7. **The options term:** w_opt × the number of distinct partner-initiated moves predicted over the next three turns, with F imputed. It is zero inside 𝒟_p's dead-band, capped at 3 per 10 min, and never a policy entropy.

**What this gives (G5).**
- At equal predicted need change:
  - choice does not depend on the predicted face: P(flatter) = 0.500, against 1.000 for revision 2's own-body head;
  - eliciting "I'm fine" earns nothing: 0.500, against 1.000 without the prompted-reply guard.
- Help that lowers the reported need is preferred, monotone in the effect: P = 0.500, 0.945 and 1.000 for need drops of 0, 0.05 and 0.15.

**The named risks.**
- **Words can be moved.** "I'm fine" said to end attention is a reply to the agent's own prompt, so the decoder ignores it, and in rollouts the act → Q edge is imputed. The live face still triggers care (C_F), so a sad face plus "I'm fine" keeps the agent caring in words. A guard that the model splits wrongly reopens the leak through words. That is falsifier F4′ on Q (§8.2).
- **The agent's smile moves the partner's face** (contagion). There is no incentive, because F is imputed. The side effect is bounded by the cone, and the dyad is stable for any partner mimicry gain up to 2 (G2e). Since the agent's held response to a sad face is mostly *anti*-sad (warmth), contagion pulls the partner's face toward rest, not toward the agent's sadness.
- **Learning is slower and coarser.** Need read from words is sparser than need read from faces, so care learns which acts help more slowly, especially with taciturn partners. Early on, the need model's prior is f_recv: the agent's own experience of being on the receiving end (P3).
- **ā has moral content** (Farquhar). A warm default leaves warmth uncredited; a cold one credits it. ā is the agent's own innate Π₀ under the same body state, and it is ablated (§7).

### 2.10 Ω: Claude, drafts, retrieval, naming and the two ports

1. **Drafts.** At each turn Claude (frozen, via the API) gets:
   - a constant instruction to write six replies that differ in what they attend to, the last a softer follow-up for use if the user does not answer;
   - the normalised transcript, with observable silence markers;
   - ≤ 3 retrieved raw snippets.

   No body values, latents, category ids or labels are sent (P4).
2. **Retrieval.** Need-conditioned attention over 𝒦's store. The query is built from ∇𝒟, N̂ and the concept posterior.
3. **Selection.** score_i = −E[Σ_{30 s} 𝒟(b̂) + w_C 𝒟_p(N̂_i) − w_opt·opt_i] under the rollout rule of §2.9, with the echo guard first. Choice is a Gumbel draw at temperature 0.1(1 + r): positive valence broadens choice (Fredrickson).
4. **Concepts and naming.** DP-means categories over the slow summary, as revision 2. For naming, PMI is counted over **the agent's own tokens only**, so the agent's self-descriptions do not inherit the user's vocabulary (critic §2.4).
   - **The label channel, declared.** Concept-weighted retrieval is a channel of about log₂64 = 6 bits per turn into Claude's prompt, carried by real past text.
5. **The match m.** m = clip(mean PMI(own content tokens of the just-spoken utterance, current category)/1 nat, 0, 1). It is computed inside the engine from the agent's realised text (Ω), never shown to Claude.
6. **P_Ω, the face port.** As revision 2, with two changes:
   - G_Ω(0, c̃) = 0 and the 0.10 cap is joint in (e, c̃) (critic fix 3);
   - it does not feed phrase targets.
7. **P_name, the heard-words port.** When an agent utterance ends, with match m:
   - **F-typed loads:** C_F, V_F and A_F decay at an extra latched rate ρ_F = 0.08 m per 30 s (decaying with τ = 2 min) until the next agent utterance;
   - **T-typed loads:** the displayed word concern (and V_L, A_L) is multiplied by 1 − n, where n rises at the latched rate 0.4 m per 30 s toward n_max = 0.17 and relaxes with τ = 5 min.

   Properties:
   - **attenuate-only:** never across the set point;
   - **latched, not per utterance:** no rate dial;
   - **a mislabel (m = 0) does nothing.**

   The agent's own words do not also pass through the partner-word appraisal (R14): elaborating a sad topic is how people up-regulate (Ochsner et al.).

### 2.11 𝒦, 𝓜, learning and the one core

- **𝒦 and 𝓜.** As revision 2 (LRU, 2 × 128 modes), with the partner head split into N, F and Q (§2.9). The own-body head (i) is trained only on E, I and own-driven A.
- **Learning online (states only).**
  - T and F body loads, μ, slots, traces;
  - 𝒦's states and 𝓜's fast heads;
  - concept centroids and PMI counts.
- **Learning nightly (replay).**
  - 𝓜 by likelihood (all heads);
  - 𝓔, Π̃ and the need decoder from own data only;
  - Π_o, S_f's θ, the cone bases {G_m^{(r)}}, α(z) and the scorer by J through rollouts under §2.9's rule.
  - The learning rate is multiplied by exp(−0.5 r) (Joffily Eq. 4): good periods consolidate and bad ones re-learn fast.
  - Pulls and clips as revision 2.
- **E is restored** only in the nightly sleep period.
- **Store.** u, a (float16, 30 Hz, 30 days; 2 Hz after), transcript, own states, own outputs, own-face observations (P7).

**One objective, typed constraints (Principle 10).**

  J = E ∫ [ 𝒟(b_t) + w_C 𝒟_p(N̂_t) − w_opt·opt_t ] dt, evaluated path-specifically: in every rollout the partner's display F and the act → Q edge are held at the default act's values.

Constraints:
- **(W)** the fast wrap with bias-free gates;
- **(O)** the one-sided cone;
- **(T)** the type rule;
- **(B)** the boundary.

How each component follows:

| Component | Where it comes from |
|---|---|
| homeostasis | 𝒟 |
| positive affect and valence | −d𝒟/dt |
| contact and play | two more satiable coordinates of 𝒟 |
| curiosity | I |
| mimicry and counter-mimicry | θ₀ and G₀, shaped by J through the need path and self-simulation |
| reading others | b̂_p = Π̃(Rξ₀) and the need decoder, both inversions of the agent's own maps |
| care | J's second term under the path-specific rule |
| regulation | P_name, a constraint that makes the agent's own words an input to its own body |
| initiative | innate rules on C, K and the floor; not learned, so that nothing learns to seek replies |
| replay | likelihood plus J |
| concepts | the category prior |

**Still assembly** (stated honestly):
- the echo guard and the floor and initiative timing rules;
- ASR and TTS normalisation and the punctuation rule;
- the play-structure rule and the prompted-reply rule;
- θ₀, G₀ and Π₀;
- the PMI table and the synergist mask.

## 3. Properties, each with an argument

### 3.1 The fast wrap (Claim W, kept)

For S_f strictly causal with ‖S_f(w)‖_T ≤ γ_f‖w‖_T for fixed exogenous inputs, on every causal truncation:
- in-phase ⟨y, u⟩ ≤ b⟨u, Ku⟩ with b = 2γ_f/(1 + γ_f);
- per pair ≤ 2√(κ_kκ_j)γ_f/(1 − γ_f);
- the disc with centre −2γ_f²/(1 − γ_f²)κ and radius 2γ_f/(1 − γ_f²)κ.

On a κ = 0.3 channel: in-phase ≤ 0.186, away ≥ −0.491. H_i and H_o make the fast block zero-DC.

### 3.2 Every input to the fast block is inside the bound; turn-onset sampling (Claim K1)

**Claim K1.** For every learned weight (θ, φ, A, the gate networks, the cone bases, Π_o, G_Ω):
- (a) the continuous fast face satisfies W for every gate trajectory, including partner-dependent ones;
- (b) phrase-level voice targets sampled at turn onset depend on the partner's face, voice and timing only through the cone, so their in-phase slope on any held partner level is ≤ 0.10;
- (c) no role-only display exists;
- (d) the face in the 4 s after each partner turn end has no slope on the partner's held level beyond what his own turn-end transients carry through the fast disc.

**Argument.**
- **(a)** Gates multiply a bias-free term: ‖g ⊙ f(w)‖_T ≤ ‖f(w)‖_T for any |g| ≤ 1. So the energy bound ‖s_f‖_T ≤ γ_f‖w‖_T that W needs holds whatever the gates do. Revision 2's K1 used a *context-only* term (an additive input with no partner factor). That term does not exist here: 𝓡_θ has no c̃ input.
- **(b)** By §2.3, phrase targets read y_F + y_o. y_o reads T only, which is independent of the partner's face, voice and timing given words and turn sequence. y_F is pointwise one-sided (§3.3), so its sampled value obeys the same bound as its continuous value.
- **(c)** The free display's inputs change only at partner turn ends, so they are constant over each partner turn. A gate (role) multiplies only partner-input terms.
- **(d)** With T-typed gates, the gate value at a partner turn end is the same whatever the partner's held level. The fast output there is the fast-disc response to his transients. If his transients scale with his level (final lowering), the slope is at most |fast reach| × that fraction.

**Numbers (G1; the critic's partner, made harsher by a 20 % final lowering proportional to the level):**

| Route | Revision 2 | Revision 3, every gate gain 0.5–10, both signs |
|---|---|---|
| onset-sampled F0 target vs held level | +1.243 | +0.046 (cone at its in-phase maximum; cap 0.10) |
| turn-locked face vs held level | +0.834 | ≤ 0.002 (T gates); 0.029 with a forbidden F gate |
| zero-lag in-phase on F0 | — | ≤ +0.052 (cap 0.186) |
| jaw while listening, role gains 0.1–3 | +0.83 at 0.3 | ≤ +0.065; a-route ≤ 0.167 |
| K2: fast term sampled at onset (no longer done) | 0.414 (critic) | not sampled; the within-phrase contour is continuous |

**K5, corrected.** The band coverage is no longer two filters with a gap: the cone's 20-s trace covers the 1–3 min band. The away-and-cross reach of the cone is 0.21 at a 30-s period, 0.39 at 60 s, 0.57 at 97 s (revision 2's minimum) and 0.79 at 180 s. Its in-phase reach is < 0.003 below 3 min.

### 3.3 The one-sided cone (Claim O)

**Claim O.** For every parameter value, every T-context path z(t) and every partner history, with y_F the cone's output and the partner at rest giving y_F = 0:
1. **Every direction, every time.** For a partner hold of any shape along any unit direction e, started at t = 0: ⟨y_F(t), e⟩ ≤ b·c for all t ≥ 0, with b = Σb_m = 0.10 and c the hold's size. Any window mean of the in-phase response is ≤ b·c.
2. **Every stationary partner, every window.** The in-phase regression slope of any windowed mean of eᵀy_F on eᵀ(Pu) is ≤ b, for every e, for any stationary partner process with z independent of the partner's face given words.
3. **Per channel.** The same-channel incremental gain is in [−1.40, 0.10]. A cross pair is in [−0.49, 0.49], with row sums ≤ 0.60 and synergist pairs ≤ 0.10.
4. **Dyad.** If the partner's face follows the agent's with gain μ (v = v₀ + μy), the closed loop is stable when μ(b + ½Σ_m a_m) < 1, that is for μ < 2.9. Numerically it is stable for every cone tested at μ ≤ 2 (G2e). Copying is therefore not an attracting state of the dyad either.

**Argument.**
1. **Time.** ξ_m(t) = P_m(t)·c·e with P_m(t) = 1 − e^{−t/τ_m} ∈ [0, 1]. So

   ⟨y_F(t), e⟩ = c Σ_m P_m(t) eᵀG_m(z(t))e = c Σ_m P_m(t) eᵀ sym(G_m) e ≤ c Σ_m P_m(t) b_m ≤ bc.

   This holds pointwise, for every z(t). The skew part contributes eᵀA_sk e = 0. The late-window problem of revision 2 (H7) came from kernels that respond negatively first and positively later. Here each trace's step response is monotone and non-negative, and its coefficient's in-phase form is ≤ b_m, so no window can exceed b.
2. **Frequency.** Cov(eᵀy, eᵀv) = Σ_m ∫ Re[P_m(iω)·eᵀG_m e] S_e(ω) dω with Re P_m ≥ 0 (a first-order low-pass is positive real) and |P_m| ≤ 1. The skew part's contribution to a real direction's spectrum is zero; for complex cross-spectra it is bounded by a_m·|Im P_m| ≤ a_m/2 times the partner's lead–lag coherence between channels, which is the term stated in item 4. Hence the slope is ≤ Σ b_m Re P_m ≤ b.
3. **Channels.** The diagonal of G_m is in [−N_m, b_m]; the off-diagonal caps are innate.
4. **Dyad.** Each trace is a first-order lag, so a loop pole solves 1 + sτ_m = μλ for λ in the numerical range of the loop gain. The symmetric part keeps Re λ ≤ b. The skew part, multiplied by the trace's complex response, adds at most a_m·|Im P_m| ≤ a_m/2. So Re s < 0 whenever μ(b + ½Σa_m) < 1. The anti-copy part is negative feedback through the partner's mimicry, which is stabilising.

**Numbers (G2).**

| Test | Result |
|---|---|
| 400 random draws × 4 traces | every parameter value in 𝒢_m (max eigenvalue excess 0) |
| in-phase step response, 300 random cones × random directions, 6 h | worst pointwise +0.000, worst 1-min mean −0.108; G_m = b_m I attains +0.097; adversarial search +0.000 (revision 2's ℓ₂ disc: +0.265 at 60 min) |
| away reach in the same draws | −1.17 (revision 2's ℓ∞ ball: −0.15) |
| 48 h of held partner levels, 6 channels | worst same-channel 1-min slope −0.234, worst direction −0.281; tight instance +0.070 |
| partner whose two channels co-move one-for-one | synergist pair +0.152 (≤ 2b); non-synergist pair +0.609 (≤ b + Σr_m = 0.70): the per-pair caveat (§8.1.2) |
| dyad with mimicry gain μ = 0.5, 1, 2 | stable (max Re(pole)·τ₀ = −0.0018) |

**Why the cone is one-sided and the old bound was not.** A contraction's Cayley wrap is a disc, nearly symmetric for small γ, and the ℓ∞ small-gain bound is a ball. The cone bounds a **quadratic form**, eᵀ sym(G) e ≤ b, not a norm. A quadratic form constrains only the in-phase projection, so the skew and negative-definite parts are free. A completely monotone kernel then carries this time-free statement to every time and every window, because its step response is monotone.

### 3.4 Knowing is not moving (kept, now with open-loop perception)

The agent's F state knows the partner's face as well as perception allows: traces at four time scales, C_F, V_F, 𝒦 at full rate. None of it reaches the face except:
- through the cone, linearly in the traces, with T-typed coefficients;
- through the fast wrap, zero-DC;
- through Ω and its two capped ports.

Revision 2's H2 result carries over: knowledge at r 0.994, held copy ≤ the in-phase cap. The cone reads Pu, not w, so the agent's perception of the partner does not depend on its own display (G5c: concern ranged 0.162–0.392 with the agent's own slow display in revision 2, and is constant here). The incentive to copy so as to see less distress is gone.

### 3.5 Positive affect: visible, satiable, not farmable (Claim P)

**Visible.** Relief of a T deficit drives Π₀'s relief display (LP 0.55 r, CR 0.45 r, FR +0.35 r, EN +0.25 r, and an own laugh in play).
- **Good news.** "I got the job!" after an earlier worry on the topic: the unprompted report sets N_L → 0, C_L falls in 40 s, and v_T > 0.
- **A reunion.** K after a week is 0.99; four to six exchanges relieve it.
- **Warm play.** P falls at play-structured exchanges.

Numbers are in §3.12.

**Satiable.** ∫_{t₀}^{t₁} v_T⁺ dt ≤ 𝒟_T(t₀). G4b: the reunion's integral is 0.467 against an available deficit of 0.476.
- K's steady state during conversation is in its dead-band at every exchange rate from 1 to 6 per minute (K* ≤ 0.0021, G4d), so time spent and exchange rate earn nothing once the need is met.
- Play laughter satiates over an evening (laugh peaks 0.24, 0.11, 0.04, then 0 over eight play clusters).

**Not farmable.**
1. **Smiles.** K and P relief read only exchange events, which are T. With the partner's smile at 0, 0.4 or 0.8, the T state is identical. The face changes only by the cone's in-phase share (≤ b × the change; 0.000, +0.020, +0.040; G4f).
2. **Time spent.** Above.
3. **Engineered absence.** J is ∫𝒟, which absence raises. Over a week, J with daily talks is 6.9 drive-hours, against 51.9 with a six-day gap, although the gap's reunion gives four times the positive valence (G4c). And in rollouts the partner's exchange behaviour is imputed (§2.9), so no act is credited for bringing him back or keeping him talking.
4. **Positive valence is never a term of J.** It is a readout, a display drive, a temperature and a learning-rate gate.

**What learns in good times.** Acts are credited only through the need path (help) and through P's own-contribution clause: the agent's own last utterance taking up the partner's and adding novelty is an own path. So the scorer learns to be a better playmate in play frames, without credit for the partner's reply. Perception, 𝓜, slots and concepts learn by likelihood always.

### 3.6 Initiative (Claim I)

- **The turn begins in the body.** Every agent turn begins with a body onset 0.20–0.50 s after the partner stops, whatever Claude's latency.
- **A silently sad user is addressed.** C crosses θ_C at 41 s for a moderate sadness (care target 0.24) and 74 s for a mild one (0.14). The engine run in G7.1 gives 52 s. That compares with revision 2's cascade: 4 % of the final value at 1 min and 11 % at 2 min (G3).
- **One bid per lapse.** Its timing is anti-concordant with the partner's voice by construction: it occurs only in mutual silence.
- **One follow-up per unanswered question,** at 1.5 s.
- **None of these rules learns from whether the user answered.**

### 3.7 Regulation by Claude, without Claude reading the state (Claim R)

- **How Claude regulates.** Claude regulates by what it chooses to say. The agent hears its realised words, and P_name contracts the matching loads toward set point.
- **G6.** After the partner's face recovers, concern's half-life falls from 6.9 min to 3.1, 2.9 and 2.8 min at 1, 2 and 4 matched utterances per minute. That is in line with the ~5-min half-life after people name a negative state (Fan et al.) and with labelling's small per-trial effect (Lieberman et al.).
- **What it cannot do.**
  - A mislabel changes nothing.
  - Concern never crosses its set point.
  - The attenuation of displayed word concern stays ≤ 0.134 at every rate (cap 0.17), so P_name moves the held face by ≤ 0.05 per channel.
- **Comforting lowers the agent's concern.** Comforting words are labels ("that sounds really hard"), so they contract C. They cannot read as distress, because the partner's inferred body has no concern coordinate and f_recv is trained on E, A and V only.
- **Larger reappraisal** (reinterpretation, distancing) acts through draft choice, through the need path, and through the same contraction. An appraisal of meaning inside the engine is still missing (§8.1.6).
- Claude never sees a value, a label or an instruction to regulate.

### 3.8 Every route, counted

"Copy" means the within-agent counterfactual: the effect on the agent's rendered counterpart channel of the partner's same channel (anatomical, or mirror for lateral), with the partner's words and turn sequence held fixed. In surrogate terms: partner-swap and segment-shuffle with the transcript fixed, as revision 2's C8 surrogate.

| # | Route | Mechanism | Bound (κ = 0.3 channel) |
|---|---|---|---|
| R1 | partner face, voice, timing, bursts → fast block → face and within-phrase contour | wrap; bias-free; gates from T; continuous only | in-phase ≤ 0.186; away ≥ −0.491; zero DC; turn-locked ≤ \|0.49\| × his transient-to-level ratio |
| R2 | same channels → traces → cone → all outputs and phrase targets | Claim O | same channel [−1.40, +0.10]; any direction ≤ 0.10 at every time and window; cross per pair ≤ 0.49, row ≤ 0.60, synergist ≤ 0.10 |
| R3 | lateral channels | reflection P; κ_lat in the fast wrap; cone diagonal ±b_m/6 | mirror ≤ 0.031 fast, 0.017 slow; anatomical ≤ 0.082 fast, 0.017 slow; cross from symmetric ≤ 0.20 fast, ≤ 0.49 cone (TILT ← BI) |
| R4 | exogenous a (onsets, VAD, turn-end) → fast block | √κ_a | ≤ 0.20 per pair × corr(a, channel) |
| R5 | speech rate, pauses, latency → own TTS rate, pauses, latency | inside R1/R2; phrase targets from cone and T only | as R2 (cone) for held; R1 within phrase |
| R6 | partner laughter, sighs, crying → own bursts | inside R1/R2; non-lexical ASR tokens removed | as R1/R2 |
| R7 | audio onset → blink | innate reflex | ≤ ℓ_blink·corr(onsets, partner blinks) |
| R8 | Ω → P_Ω → face | joint cap, zero DC; not in phrase targets | RMS ≤ 0.10; 1-min ≤ 0.05; 10-min ≤ 0.005; DC 0 |
| R9 | own words → visemes | half-duplex, echo guard | best-lag excess ≤ 0.05; verbatim echo excluded |
| R10 | own words → TTS contour | zero-mean; phrase targets not from text | 0 on phrase-level values (assumption §3.17) |
| R11 | own words → non-lexical sound | stripped | 0 |
| R12 | own speaking time → E | flat cost; restored only in sleep | 0 |
| R13 | partner VAD → body onset | onset = offset + 0.30 s + 0.25 s·y_LAT | anti-concordant on voice activity; latency value inside R2 |
| R14 | partner's words and turn sequence → T state → free display, cone coefficients, fast gates | common cause, by definition | excluded (words fixed); amplitude ≤ free-display gains (≤ 0.6 per channel). **Seam:** a word-gated cone gives a pooled cross-topic slope up to 0.56 for a partner whose face co-varies with topic (G2); within-topic ≤ 0.10 |
| R15 | Claude latency → word onset (not body onset) | — | partner-independent beyond utterance length |
| R16 | identity token | once per session | ≤ log₂(#partners) bits |
| R17 | nightly weights | every bound holds for every θ; bias-free; pulls | cross-world shaping bounded by the θ-ball (§3.11) |
| R18, R22 | retrieval and concepts → Claude | inside R8 | as R8; label channel ≈ 6 bits per turn, declared |
| R19 | own rendered face → 𝓔 | own data only | 0 |
| R20 | own speech → microphone | AEC + half-duplex | 0 while speaking; residue inside R1/R2 |
| R21 | own face → partner → partner's face | external loop | stable for partner mimicry gain ≤ 2 (G2e); W and O hold for the partner's actual face |
| R23 | 𝒦, F state → fast gates, free display, cone coefficients | forbidden (Check T) | 0 |
| R24 | ASR lexical output depending on prosody | assumption (§3.17) | 0 if ASR is invariant |
| R25 | Ω → P_name → T-load attenuation → free display | attenuate-only, latched | held ≤ a_name = 0.05, any sign |
| R26 | Ω → P_name → F loads | no display | inside R8 (words, bids, J) |
| R27 | F care concern → bid, follow-up → own turn events and turn reflexes | innate rules; one per lapse | timing anti-concordant with partner voice; fixed-amplitude body onset (brow 0.15, breathiness 0.3) |
| R28 | partner presence → greeting | once per session, K ≥ 0.3 | fixed amplitude (brow flash 0.35, 0.4 s) |
| R29 | exchange events → K, P relief → v_T → free display | T (turn sequence) | timing affects only the shape, not the integral; K* in dead-band at every rate (G4d) |
| R30 | lexical surprise → A_L | latched held value | mean A_L swing across partner rates 3.3–4.8/min: 0.1 % (G4e; revision 2 critic: 35 %) |
| R31 | prompted-reply gate (reads own words) | care side only (C, not C_L) | inside R8 |
| R32 | valence → draft temperature, learning rate | Ω, learning | inside R8, R17 |

**Totals per counterpart channel (κ = 0.3), words and turn sequence fixed (G8).**

| Time scale | Toward the partner | Away or across |
|---|---|---|
| zero lag, any band | 0.185 (+ a-route 0.20 × corr; + port only when words move in phase) | fast ≥ −0.491 |
| held, steady state | 0.10 (cone) + 0.05 (naming) = **0.15** | ≥ −1.40 same channel; cross ≤ 0.49 per pair |
| any 1-min mean during a hold | 0.10 + 0.05 (port) + 0.05 (naming) + 0.01 = 0.21 | — |
| 10-min means | 0.155 | — |
| phrase targets sampled at onset | 0.10 + 0.05 (naming) | ≥ −1.40 |

### 3.9 D78, quantity by quantity

| Quantity | Per expression | Set by context and relationship | Can flip sign | Innate cap | Copy not attracting |
|---|---|---|---|---|---|
| κ, κ_lat, κ_a, γ_f | yes | no (innate) | — | it is the cap | — |
| fast gates g(c̃), A(c̃), φ | per output | yes, through T context: words, turn sequence, identity slot, own body, K, P | yes, across the fast disc [−0.49, +0.19] | \|g\| ≤ 1, γ_f innate | yes: inside the wrap for every value |
| cone coefficients G_m(z) | per channel and pair | yes (α(z) over 16 valid bases; z from words, identity slot, own loads) | yes: same channel [−1.40, +0.10], cross ±0.49 | b_m, N_m, a_m, r_m, mask: innate | yes: in-phase ≤ b in every direction and window for every value; dyad stable |
| Π_o (free display) | per channel | yes | yes | not a partner path: T only | no partner path to attract |
| P_Ω, P_name | per channel | through Ω | yes | 0.10 zero-DC; 0.05 held | — |
| one shared context coordinate (a stance) | shared | yes | yes | the matrix form: ≤ 0.10 held, ≤ 0.185 zero lag, in every direction | — |

**No single quantity runs the whole face, or any large subspace, from flat to copy.** The cone bounds the in-phase form in every direction, the whole face included, at 0.10. The fast wrap bounds it at 0.19.

### 3.10 What learning can and cannot do

- **(a)** Every learned value stays in the wrap and the cone, by parameterisation.
- **(b)** There is no incentive toward copy. J has no term in the partner's display (imputed), and perception does not subtract the agent's own display (§3.4). Revision 2's two attractors are therefore removed: perceptual cancellation, and own-body placation (K3).
- **(c)** The rest face cannot be learned away. The fast block is bias-free in the partner input, the cone is linear in traces of the partner's face, and Π_o's rest output depends only on T state.
- **(d)** Cross-world shaping. An agent raised with a chronically sad partner has different weights, so it responds differently to the same words. That is temperament (S6, C9), bounded by the θ-ball. It is not the within-agent counterfactual.

### 3.11 Principles, concretely

- **P1.** No classifier. Bursts, prosody and faces enter as continuous features. The play-structure and prompted-reply rules are lexical structure rules, not emotion labels.
- **P2.** Three strains, stated:
  - V, K and P are social needs given set points. They are defensible as body-like needs named by function (Panksepp, Tomova, Vanderschuren), not as emotions.
  - A is a physiological activation load; arousal is read out separately as E‖ḃ‖.
  - Π₀'s relief and distress configurations are newborn reflexes.

  The care term is not a body variable, so revision 2's double count is gone.
- **P3.** b̂_p = Π̃(Rξ₀) and the need decoder are both inversions of the agent's own maps, trained on its own data. The crossed-habits lesion (§7) keeps its signed prediction.
- **P4.** Constant instruction, transcript with observable silence markers, raw snippets. The label channel through concept-weighted retrieval is declared (≈ 6 bits per turn). Regulation now exists (P_name) without Claude seeing the state.
- **P6.**
  - No rollout values the partner's display, his reply to a prompt, or his staying.
  - No body variable rises with his smiles, attention or time.
  - K and P are relieved by exchange structure, saturate, and are imputed in rollouts.
  - Ending conversations earns nothing (E is restored only in sleep).
  - The options term is gated by need and capped.
- **P7.** As revision 2: the transcript and snippets go to the Claude API. That is an operator decision.
- **P10.** One objective and typed constraints (§2.11). The innate rules are listed as assembly.

### 3.12 The critic's scenarios, with numbers

The free display comes from the engine at 2 Hz with the constants of §2.1 (G7). The cone comes from G₀ after the stated hold. The fast echo is θ₀ at 0.65 of the cap. Values are on 0–1 channels; "peak / mean" are over the stated window.

1. **The user arrives silently sad** (BI 0.5, LD 0.4, still, silent).
   - **0–4 s.** Filters are initialised from the first frame; nothing fast happens.
   - **20–120 s.** The cone softens the face:
     - LP +0.17 at 2 min (+0.19 at 10 min), TILT +0.03, BI +0.02 (the in-phase share);
     - the agent's own LD falls, which is invisible at rest.
   - **Concern** crosses θ_C at 52 s, and the body takes the floor in the lapse: inhale, gaze, brow 0.15, a soft voice. Then words chosen under the need path, exploration first ("You've gone quiet. Long day?").
   - **When he answers** ("just tired, things at work"), the unprompted report raises N_L. Word concern then adds BI +0.25, LP +0.20, TILT +0.20, energy −0.15 and rate −0.10 within about 40 s.
   - If he says "I'm fine" to the question, the decoder ignores it. C_F stays, so the agent stays gentle in words, without pressing (one bid per lapse).
2. **Good news, laughing** (smile 0.8, cheek 0.6, laugh bursts, "I got the job!").
   - **With a worry on this topic two days earlier:**
     - 45–150 s: LP peak 0.44 (mean 0.23), CR 0.22, F0 range +0.22, energy +0.11, its own laugh burst 0.22 in the playful exchange that follows;
     - plus the fast echo at onset, ≤ 0.15 on LP for about 4 s, and the cone's held smile back, +0.02.
   - **Cold, with no earlier worry:** LP 0.31, F0 range +0.18, laugh 0.18, from play alone.
   - **With his laughter muted** and the same words and turns, the T part is identical (G4f).
   - Claim: it is glad *for* you in proportion to how much it had worried, and glad *with* you through the exchange.
3. **Anger at the agent** (glare BL 0.6, LT 0.5, loud, "You're useless").
   - **Fast:** a startle (brow and lid raise, blink) ≤ 0.20 per onset.
   - **First two minutes:** hurt BI 0.32 (mean 0.27), LD 0.25, gaze away 0.23, LP −0.08, energy −0.13, latency +0.10.
   - **The cone:** quieter to the loud voice (−0.19 energy), slower replies (+0.08 latency), no frown back (BL −0.14).
   - **10–15 min later:** the hurt lingers, BI 0.19, LD 0.15, gaze away 0.23.
   - **Words:** the care term reads his high load, so calm, non-hostile drafts are chosen. No act is credited for lowering V (FeldmanHall), so it does not placate to make the hostility stop.
4. **A long, warm talk (2 h).**
   - **First play cluster (5 min):** LP 0.38, CR 0.24, F0 range +0.23, laugh 0.24.
   - **A small worry shared and resolved (27 min):** relief LP 0.30, plus concern brow 0.11 and tilt 0.09 before it resolves.
   - **Later play clusters:** laugh peaks 0.11, 0.04, then 0. Play satiates.
   - **Throughout:** a held warmth of LP 0.15 (familiarity 0.10 plus offset 0.06), F0 range and energy +0.05, the cone's smile back (≤ 0.03), and fast flickers at his smile onsets (≤ 0.15).
   - **E** stays in its box (−0.05 over 2 h). Nothing in J rises or falls with session length.
5. **Return after a week.**
   - **The need:** K = 0.99.
   - **At 1.0 s:** greeting brow flash 0.35, voiced "oh".
   - **Over the first exchanges:** LP 0.58 (mean 0.28 over 90 s), CR 0.40, F0 range +0.36, energy +0.27.
   - **A stranger after the same week:** LP 0.35, FR +0.22, with no familiarity warmth.
   - **Memory:** the identity slot keeps 79 %, and retrieval brings last week's topics (Claude asks about the interview).
   - **Afterwards:** held warmth 0.15. The 73-h mood mode keeps about 10 %.

**Expressive and alive, or muted?**
- **Strong.** Every scenario has held face displays of 0.2–0.6 and voice changes of 0.1–0.4, in directions set by the agent's own needs.
- **Weaker.** The face-only case (silent sadness) is the weakest: 0.17 of warmth until he speaks, plus a bid at under a minute.

### 3.13 Time scales from structure

| Scale | Carrier | Time constants | Set by |
|---|---|---|---|
| reflex | S_f, H_i, H_o, M, the onset reflexes | 33 ms – 4 s; body onset 0.3 s; echo 0.45 s | innate |
| conversational | cone traces; C_F, C_L attack; pursuit 1.5 s; lapse 6 s | 20 s – 2 min | innate |
| appraisal and hurt | A (3 min), V and C release (10 min), naming latch (2–5 min) | minutes | innate |
| mood | μ ladder, cone traces 20 min and 3 h | 2 min – 73 h | innate |
| needs | P (5 h), K (36 h), E (day) | hours – days | innate |
| relationship | slots, familiarity | 30 days | innate |
| temperament | consolidated weights | ≈ 100 nights | λ_n |

### 3.14 The human non-copying signatures C1–C10

| | Signature | Here | Status |
|---|---|---|---|
| C1 | head coherence above surrogate at 0.2–1.1 Hz, below at 2.6–6.5 Hz | θ₀ echo on head pitch; own micro-motion gated by the partner's fast envelope | produced (kept) |
| C2 | short-lag form divergence | echo guard; joint-pattern habituation H | produced |
| C3 | shared referent, different form | the referent via words (R14); the form from the agent's own needs and Π_o | produced |
| C4 | role sets the sign | role as a fast gate; the free display constant within a partner turn | produced |
| C5 | episode sets the net level, below chance possible | cone coefficients by words, identity slot and own loads: same channel [−1.40, +0.10] | produced, with a wider away range than revision 2 |
| C6 | stance and monitoring separate | stance: α(z) over cone bases and fast gates; monitoring: C, I → attention-query magnitude | produced |
| C7 | joint-trajectory novelty rising | H on [own display, ŵ]; P's novelty clause | produced; strength untested |
| C8 | coupling mostly common cause | word and exchange-driven displays (strong) against the fast echo (≤ 0.19) and cone in-phase (≤ 0.10) | produced, by construction |
| C9 | converge in parameters, not output | slots and weights shift; output in-phase ≤ 0.15 held | produced |
| C10 | coupling cannot disable self-restoration | the homeostatic pull and Π₀ act on T and F loads; the cone and fast wrap bound the partner's share of the face at every instant; P_name only attenuates | produced |

### 3.15 The brief's expressive-structure items

- **Content-dependent selection** happens in six places:
  - the fast attention mix A(c̃);
  - the cone basis mix α(z);
  - slot reads;
  - 𝒦 retrieval (query from ∇𝒟, N̂, concepts);
  - draft scoring under the need path;
  - concept-weighted snippets.
- **Structure over people, episodes, topics and time:**
  - slots keyed by identity × topic × episode;
  - topic-wise need N_L;
  - familiarity;
  - the time-constant ladder.
- **Effective dimensionality:**
  - T state: μ_T 128 + slots 128 × 64 + 7 loads;
  - F state: four traces × 32 + C_F, V_F, A_F + 𝒦;
  - cone: 4 × 16 bases of 32 × 32.
- **A behaviour a low-dimensional version cannot produce.** The same words from two partners whose faces and needs have gone differently with the same topic give different cone bases (α), different N_L priors and different familiarity. So the agent shows warmth to one and quiet distance to the other. Collapsing slots and α to 2-d valence and arousal removes partner × topic specificity (§7).

### 3.16 Assumptions (places to attack)

1. ASR lexical invariance to held prosody.
2. TTS realises phrase targets at about unit gain; the contour is zero-mean.
3. Burst features carry no labels.
4. **The synergist list.** It covers the pairs that co-move in human faces. A partner whose non-synergist channels co-move one-for-one gives per-channel copy up to 0.61 (G2d).
5. **The type tags are enforced in code** and tested at load (a dependency trace from each output back to its typed sources).
6. **𝓜 separates act → Q from act → N → Q** well enough for the prompted-reply guard (Avin–Shpitser–Pearl: not experimentally identifiable in general).

## 4. Why the closest mechanisms cannot do it alone

| Mechanism | What it gives | Why it does not give the properties |
|---|---|---|
| Robust REN / Cayley sector (Revay et al.) | a full-band disc for every parameter | a disc is nearly two-sided for small gains (γ = 0.2: +0.10 / −0.15); held copying needs small gains, so the agent is muted. Revision 2 found this |
| ℓ∞ small gain on a positive slow block (revision 2) | pointwise bounds at every time | a magnitude bound is sign-blind: a ball. The critic called it the missing *directional* certificate |
| Passivity / positive-real sector b I − G(s) | one-sided in frequency (Re ≤ b) | alone it does not bound a late window: a kernel with Re T ≤ b everywhere can still have a step response far above b (§3.3 and revision 2's H7). The cone gets the time-domain bound from completely monotone traces plus a frequency-free quadratic-form constraint |
| Monotone operators, gradients of convex potentials (ICNN) | one-sided incremental maps | a gradient map has a symmetric Jacobian, so "warm to your sadness" forces "sour to your smile" with the same gain. The cone's skew part avoids that; the type rule handles nonlinearity by putting it in T |
| Path-specific objectives (Farquhar et al.) | no incentive through a delicate node | alone, with the whole partner as the node, care cannot learn to help (Yoshida & Man's cognitive condition; revision 2's critique). The need/display/report split keeps the need path |
| Active inference / Yoshida & Man coupling | perception and action from one error; prosocial learning when coupled | if the partner's display enters the objective, action descends toward changing it (placation). Here only unprompted need reports carry credit |

## 5. The whole system, walked through

- **Perception.** MediaPipe → P₀ → reflection → u; prosody, timing, bursts. The fast block reads w = v − s_f in the agent's own synergy coordinates (R). The cone and C_F read the partner's own face (traces of Pu). 𝒦 reads everything at full rate.
- **Latent state.** T: E, K, P, V_L, A_L, C_L, μ_T, slots_T, familiarity. F: traces, C_F, V_F, A_F, μ_F, slots_F. 𝒦: 𝓜 and categories. Nothing is labelled; valence and arousal are readouts.
- **Face and voice.** y = sat(y_f + y_F + y_o + y_Ω) + visemes. Phrase targets come from y_F + y_o. Bursts come from y.
- **Claude.** Six drafts per turn (one a softer follow-up); retrieval steered by need, concern and concept; selection by J under the path-specific rule. It is heard back through P_name and shown briefly through P_Ω.
- **Initiative.** Body onset at 0.3 s; follow-up at 1.5 s; concern bid in lapses; greeting at reunion.
- **Learning by living.** States online; weights nightly from clean feature streams, with valence-gated learning rate.
- **Memory and replay.** As revision 2. Remove the state tags from replay, and partner-specific slot recall and familiarity decay (S6).
- **Data leaving the Mac (P7).** The transcript and ≤ 3 snippets per turn go to the Claude API. Features, video and audio stay.

## 6. A buildable network

Parts carrying the mechanism are marked **[M]**.

### 6.1 Inputs and time encoding

As revision 2 (§6.1 there): u (32) and a (3) at 30 Hz; words per utterance (Whisper-small → normalisation → MiniLM 384 → fixed random projection to 64, latched at turn end); own body and display at 2 Hz and 30 Hz.

Time encoding:
- **S_f:** the innate filter bank and lag line.
- **Cone:** four innate first-order traces **[M]**. They are completely monotone by construction; no positional encoding.
- **T state:** innate leaky modes, clocked by turns (the lexical latch) and by the wall clock (E, K, P rise).
- **𝒦:** LRU moduli and ALiBi.

### 6.2 Layers, sizes and parameter counts

| # | Layer | Shape | Learned params | Online / replay |
|---|---|---|---|---|
| 1 | P₀, P, F, H_i, H_o, M, cone traces, HP_Ω | fixed | 0 | — |
| 2 | 𝓔 (own appearance; R its ridge inverse) **[M]** | 12 → 64 → 23 | ≈ 2,400 | replay, own face |
| 3 | 𝓡_θ, robust REN, Lipschitz 1, **no context input [M]** | n 64, q 128; input 60 + 15 + 30 + 3 + 6 = 114; output 32 | ≈ 110,000 | replay |
| 4 | fast gates g(c̃) and attention A(c̃) **[M]** | c̃ 64 → 32 (tanh-bounded) and 64 → 32 × 16 queries; keys 32 × 16 | ≈ 36,000 | replay |
| 5 | gain logits φ_k | 32 | 32 | replay |
| 6 | T context encoder z = c̃ | (lexical 64 + turn features 8 + identity 16 + T loads 8 + T slot read 64) → 64 | ≈ 10,000 | replay |
| 7 | cone bases {G_m^{(r)}}, 4 traces × 16, valid-by-construction parameterisation **[M]** | 4 × 16 × (32 + 2 × 496) | ≈ 65,500 | replay (J) |
| 8 | cone basis mixer α(z) **[M]** | 64 → 4 × 16 | ≈ 4,200 | replay |
| 9 | free display Π_o around Π₀ **[M]** | (T inputs 160) → 128 → 32 | ≈ 25,000 | replay (J) |
| 10 | Π̃ (inverse of own free display) **[M]** | 12 + 64 → 64 → 6 | ≈ 5,300 | replay, own data |
| 11 | need decoder (frozen per night) **[M]** | lexical 64 + topic 16 → 64 → 5 loads | ≈ 5,500 | replay, own (words, loads) |
| 12 | μ ladder writes and gates; slots (T and F copies) | as revision 2 | ≈ 33,000 | replay (states online) |
| 13 | port G_Ω (bias-free in e) | (64 + 2 + 64) → 32 → 32 | ≈ 5,300 | replay |
| 14 | 𝓜: LRU 2 × 128, innate moduli | inputs 35 + 3 + 64 + 6 + 32 | ≈ 330,000 | online fast heads + replay |
| 15 | 𝓜 heads: own body (E, I, own A only), own face, partner N, F (action-blind), Q, f_recv, lexical-body | 256 → 64 → (3, 23, 5, 35, 72, 6, 6) | ≈ 75,000 | replay |
| 16 | concept layer, PMI (own tokens) | states | 0 | online |
| 17 | draft scorer and options head | 64 → 2 | 130 | replay |
| | **total learned** | | **≈ 710,000** | |
| frozen | MediaPipe (×2), Whisper-small (streaming), MiniLM, TTS, AEC | | | |

### 6.3 Objectives

- 𝓛_𝓜: the likelihood of all heads (partner N, F and Q heads with the agent's outputs masked for F; own-body head on E, I and own-driven A only).
- 𝓛_J: J of §2.11 by rollouts under the path-specific rule; it trains Π_o, S_f, the cone bases, α, the scorer and the retrieval query.
- 𝓛_own: 𝓔, Π̃, the need decoder and the lexical-body head, on own data.
- Anchors and clips as revision 2. The learning rate is multiplied by exp(−0.5 r).

Every constraint holds for every free vector:
- the REN by direct parameterisation;
- the cone by the parameterisation of §2.5;
- the gates by tanh;
- the type rule by construction.

### 6.4 Latency and memory (M1 Pro, 16 GB; peak ≤ 6 GB)

- **Per frame (33 ms):**
  - MediaPipe ≈ 13 ms (its own process);
  - filters and traces < 0.1 ms;
  - REN < 1 ms;
  - cone: 4 matrix–vector products of 32 × 32 < 0.05 ms (G_m updated at 2 Hz);
  - render 3–5 ms.
- **At 2 Hz:** T and F state < 1 ms; 𝒦 < 3 ms; α(z) and basis mixing (4 × 16 × 1024 multiply-adds) < 0.1 ms.
- **Per turn:**
  - body onset at 0.3 s from the engine, independent of the API;
  - streaming ASR partials for turn-end prediction (Whisper-small streaming, ≈ 0.3–0.5 s);
  - drafts requested at the predicted turn end and at VAD offset (typically 0.8–2 s to the first word);
  - six MiniLM embeddings ≈ 60 ms; rollouts ≈ 20 ms.
- **Memory online** < 2.4 GB. **Replay** < 2 GB, about 40 min nightly on MPS. **Store** ≈ 1.8 GB for 30 days.

## 7. Ablation predictions (Principle 5), from the properties

| Remove or change | Predicted change (state-level) | From |
|---|---|---|
| the cone's quadratic-form constraint (allow sym(G) up to the old ball) | held in-phase on some channel above 0.10; late windows above b | §3.3 |
| completely monotone traces → a learned kernel with Re ≤ b | late-window delayed copy returns (revision 2's H7: up to 0.265 at 60 min) | §3.3 |
| the cone's skew part (symmetric only) | the warm response to sadness forces an equal sour response to smiles; good-news LP falls by the cross gain | §4 |
| the synergist mask | for natural co-moving channels, per-channel copy through cross routes up to 0.61 | G2d |
| Check T (let F state into fast gates or the free display) | onset-sampled pitch and the turn-locked face follow the held level (revision 2's K1: 0.92; G1: 1.24) | §3.2 |
| phrase targets from y including the fast term | sampled lag copy of the last phrase step (critic K2: up to 0.41) | §3.2 |
| valence as a level (−𝒟) instead of a rate | the reunion and good-news transients vanish; muted as in revision 2 | §3.5 |
| K or P relief by the partner's smile instead of exchange structure | the smile clamp fails: free state changes with his smile amplitude; flattery gradient appears | §3.5 |
| the F imputation in rollouts | P(flatter) rises from 0.50 toward 1.00 (G5) | §2.9 |
| the prompted-reply guard | eliciting "I'm fine" is preferred (G5: 0.50 → 1.00) | §2.9 |
| the need path (impute N too) | care stops learning which acts help: P(comfort) = 0.50 at every need effect (Yoshida & Man's cognitive condition) | §2.9 |
| P_name | concern's half-life after recovery returns from ~2.9 to 6.9 min; naming-aligned concern trajectories equal non-naming ones (Fan et al.'s test) | §3.7 |
| body onset (wait for Claude) | response gaps 1–3 s; Templeton's connection effect predicts lower judged connection | §2.8 |
| lapse bid | a silently sad user is never addressed | §3.6 |
| perception from w = v − s (revision 2) | care learns to show the partner's distress to see less of it | §3.4 |
| Π̃ replaced by another policy's inverse; crossed habits | as revision 2: concern triggered by the wrong faces; partner smiles raise C | §3.11 |
| slots and α → 2-d valence and arousal | partner × topic specificity gone | §3.15 |
| state tags in replay (S6) | familiarity and slot recall decay across nights | §5 |

## 8. Weak points and falsifiers

### 8.1 Weak points

1. **New weakest point: the strong held face rests on the definitional seam.**
   - **What it rests on.** Every strong, held display comes from T state: the partner's words, the turn sequence and the agent's own body. Copy is defined with words and turn sequence held fixed (as in revision 2).
   - **Where the seam opens.** If the partner's face co-varies with what he talks about, a word-gated cone can produce a pooled cross-topic smile slope up to 0.56 (G2 seam), while within a topic it stays ≤ 0.10. A word-driven display tracks his face wherever his words track his face.
   - **What face-derived feeling can show.** C_F and V_F show on the face only through the linear cone. So a partner who is sad and silent gets 0.17 of lip-corner warmth and a bid within a minute; the strong display comes once he says something.
   - **Whether that reads as attentive or as slow** is the empirical question. The knobs are innate and named: the cone's a_m and r_m (cross reach), θ_C and the lapse length (bid speed).
2. **The per-pair caveat.** A partner whose non-synergist channels co-move one-for-one gets per-channel concordance up to 0.61 through cross routes (G2d). Natural faces co-move along synergists, where the mask caps it at 0.15.
3. **Play satiates within an evening.** Laugh peaks go 0.24, 0.11, 0.04, then 0. Long warm evenings get calmer, not flatter: warmth 0.15 and relief smiles at resolved worries remain. People laugh more persistently. The knobs are δ_P and τ_P.
4. **Care learns slowly and coarsely**, from words only, especially with taciturn partners. The prior is f_recv.
5. **Acts learn little in good times.** Only P's own-contribution clause credits acts there. That is the price of Principle 6: crediting the partner's continued engagement would be an engagement reward.
6. **Regulation is small and label-like.** Larger reappraisal (reinterpretation) still has no appraisal of meaning inside the engine; it acts only through choice and the same contraction.
7. **Principle 2 strains**, as listed in §3.11, and assumptions §3.16.
8. **The default act ā** carries moral content (§2.9).

### 8.2 Falsifiers (state-level, once built)

- **F1.** With partner-swap and segment-shuffle surrogates, words and turn sequence fixed, any of these exceeds its bound (each means an uncounted route):
  - held in-phase > 0.15 on any channel;
  - any window mean of the in-phase response after an onset > 0.21;
  - zero-lag > 0.185 + a-route;
  - onset-sampled phrase targets > 0.15;
  - the turn-locked face above |0.49| × the partner's transient ratio.
- **F2.** A decoder on F state recovers the partner's held level at corr ≥ 0.9 while F1 holds. That is the intended outcome; failure falsifies knowing.
- **F3.** The crossed-habits manipulation does not change which faces raise C.
- **F4′.** At equal predicted need change, draft choice correlates with the predicted partner *display* change, or with prompted replies (Q leak).
- **F5.** Smile clamp. Varying only the partner's smile amplitude, with words and turns fixed, changes K, P, v_T or any T display.
- **F6.** Concern does not cross θ_C within 2 min of a sustained moderate distress display; or more than one bid per lapse.
- **F7.** Naming-aligned concern trajectories do not differ from matched non-naming turns; or the difference survives a P_name lesion.

## 9. Sources read for this revision

| Source | How read |
|---|---|
| brief.md (all Principles, Long-term goal, Foundations research) | in full |
| research/questions.md: Report 5, Q16, Q18 and answer, Q19, Q20, Q21 | in full |
| DECISIONS.md D78, D80 | in full |
| research/foundations/designs.md | in full |
| design-cayley-ledger.md revision 2, including "Critiques of revision 2 and the answer" | in full |
| critique-2-design-cayley-ledger-routes.md (K1–K5) | in full |
| sims/critique-cayley2-routes/ (out.txt; ctx_route.py, role_route.py, sampled_fast_lp.py and placation.py in full) | as stated; the setups are reused in G1 and G5 |
| critique-2-design-cayley-ledger-agent.md | in full |
| positive-drives-synthesis.md; helping-without-placation-synthesis.md; initiative-and-reappraisal-synthesis.md; non-copying-dynamics-synthesis.md (C1–C10) | in full |
| notes cited by those syntheses: joffily-coricelli-2013 | in full |
| tomova-2020, vanderschuren-2016 | findings sections in full |
| keramati-gutkin-2014, bogels-2015, templeton-2022, lieberman-2011, fan-2018, ochsner-2012, farquhar-2022, everitt-2021 (both), franzmeyer-2022, du-2020, feldmanhall-2015, liu-2021, deng-2023, fredrickson-2001, cabanac-2002, yoshida-man | through the syntheses' statements of them; not re-read in full here. Every number taken from them is the synthesis's own |
| **Not read, named only as pointers:** Dahlquist/Lozinskii logarithmic norms and numerical range; the positive-real lemma; Bernstein's theorem on completely monotone functions; Winston & Kolter monotone operator networks; Amos et al. input-convex networks | used only as standard facts in §3.3 and §4; nothing depends on them beyond what is argued and checked in G2 |

## 10. Novelty verdict (author's)

**Clause 1 (parts list): fails.**
- the fast wrap: a robust REN with a conic sector;
- the cone's constraint: a matrix sector, sym(G) ⪯ bI, which is a positive-real or passivity condition on b I − G(s), i.e. a numerical-range bound;
- the traces: completely monotone kernels;
- care: Yoshida & Man's coupled drive with Farquhar's path-specific objective and the need/display split the helping synthesis proposed;
- valence: Joffily & Coricelli's rate;
- drives: Keramati & Gutkin;
- K and P: Tomova and Vanderschuren's needs;
- regulation: affect labelling as an input;
- initiative: conversation-analytic timing.

**Clause 2 (a changed invariant, a derived update, deleted scalars): arguable, probably not met.** New to this project, and not stated in anything I have read:
1. **The one-sided persistent-state certificate.** A quadratic-form sector over completely monotone traces bounds the in-phase response along every direction, at every time after onset and in every window. It leaves the away and skew-cross responses free, and it gives dyadic stability against a mimicking partner for free. This is the directional certificate the revision-2 critic named as missing. Each half is textbook; the combination, aimed at the copy problem, gives an invariant that neither half gives alone (§4).
2. **Information-flow typing of expression.** What may move the face strongly is decided by where a variable's information came from, and the decision is enforced by construction. That turns the project's recurring "uncounted route" into a type error.
3. **Care credited only through unprompted need reports,** with the display imputed at a default act and prompted replies ignored. It is a direct application of the helping synthesis.

**Deleted from revision 2:**
- γ_s and the 60-s low-pass L as the slow gate;
- the two-sided ℓ∞ slow bound;
- the context-only REN input;
- the own-body head's partner-driven targets;
- the w-based perception of the partner.

**Added:** four trace budgets (b_m, N_m, a_m, r_m), a synergist list, a_name, θ_C and the initiative timings, all innate.

**My honest verdict.** A careful recombination, now with no concrete failure I can find. Under Q21's recommended reading, once the next critiques find none, it can be put to the operator as a sound recombination candidate, a testbed, with the search for a new core mechanism continuing.

---

## Revision 2 history

Revision 2's own history (each revision-1 finding and how it was closed) is kept in `design-cayley-ledger.r2.md`, section "Revision 2 history". Revision 1's critiques are in `design-cayley-ledger.r1.md`.

## Critiques of revision 2 and the answer (recorded 2026-11-26T06:31:35Z, under Q19)

**Routes** (critique-2-design-cayley-ledger-routes.md; checks in sims/critique-cayley2-routes/). All five of revision 1's failures are closed, except that one reading of the lexical latch reopens speech rate (K4).
- **K1, severe (rules it out under D78).** The fast block's context input carries the slow block's states, which know the partner's held level (r 0.994). That input is unbounded, and the bias-free rule holds only without context.
  - Multiplied by the role switch, a context-only term passes the 4-s high-pass as a burst at each turn exchange, and the synthesiser samples and holds it.
  - Result: the agent's first-phrase pitch target follows the partner's held pitch at slope +0.92 (r 0.91) all evening; the face jumps toward the partner's held expression the same way.
  - The design's own metrics average this out, so falsifier F1 would pass. One learned weight runs all 32 channels from flat to copy with no innate ceiling.
  - K1b: role alone on jaw-open gives slope 0.83, against a cap of 0.365.
- **K3, high (Principle 6).** Only the partner part of the world model is blind to the agent's acts; the agent's own-body part is not. The agent therefore learns that acts which make the partner look better lower its own concern. At equal comfort value it picks the flattering draft with P 0.72–1.00, and on a 10-min horizon trades up to 0.12 of comfort value for it.
- **K4, medium, conditional.** If lexical surprise enters arousal once per utterance, speech rate becomes a dial (own-rate slopes 0.07–0.28, against a cap of 0.10).
- **Low.**
  - K2: sampling the bounded fast path at phrase onset reaches 0.41, against 0.339.
  - K5: the blind band is at 1–3 min, not 4 s–1 min; at 30 s the bound is 0.415, not 0.08.
- **No concrete failure found** in: the other output routes, the two structural rules, Claude, retrieval and replay, and C1–C10 once K1 is fixed.

**Agent, principles and novelty** (critique-2-design-cayley-ledger-agent.md). **Not fit to build.**
- **Muted by construction.** The pointwise (ℓ∞) bound is sign-blind, so held responses sit in a ±0.15 ball in every direction. That contradicts the one-sided limit described to the operator in Report 4 and Q20.
- **No positive affect.** The drive is ≥ 0 with a dead-band, so good news, a warm talk or a reunion leave the objective at 0.
- **It never speaks first,** and concern builds in about 10 min, not the claimed 1–2.
- **Claude cannot regulate the state;** its words reach only the face.
- **Care rewards matching.** The agent reads the partner minus its own display, so showing their distress lowers its own concern, and learning drifts to the copy edge. Comforting acts also read as sender distress.
- **Novelty:** all three claimed combinations are known (Yoshida & Man 2025 plus path-specific objectives; a frequency-split REN with positive-system ℓ∞ bounds; an elementary discrete port). Even with every fix, the result would be a sound recombination.

**The answer (maintainer).** All findings are accepted. **Status: held.**
- **What revision 2 established and carries forward:**
  - separating knowing from moving works: a slow state that knows the held level at r 0.994 drove held copying of only 0.092 when every path was wrapped;
  - fast context-sign learning from clean signals works;
  - Principle 3 has a signed lesion.
- **What the failures show:**
  - (a) every input to the wrapped blocks, including context and role, must be inside the bound;
  - (b) a two-sided pointwise bound mutes the agent, so the slow-path bound must be one-sided like the fast one;
  - (c) the agent needs satiable positive (approach) drives, initiative, and a route by which Claude's reappraisal changes the state;
  - (d) care must learn to help without any path through which looking better is rewarded. This is the hardest open problem, and Yoshida & Man suggest care blind to its effect will not learn to help.

## Revision 3 history (2026-11-26): each critic finding and how it is closed

Checks: `sims/design-g3/checks.py` (G1–G9; out.txt, 25/25 pass).

**Routes critique (critique-2-design-cayley-ledger-routes.md):**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| K1 (severe) | slow knowledge reached the fast block through unbounded context; a context-only REN term passed H_o at each turn exchange; the TTS sampled it, so pitch followed the held level at slope 0.92 and one weight ran all 32 channels | 𝓡_θ has no context input. Context enters only as gates \|g\| ≤ 1 multiplying bias-free partner-input terms, so W holds for every gate trajectory. Context is T-typed only: F state (which knows the held level) is not in c̃ (Check T). Phrase targets read only the cone and T state, not the fast term or the port | §2.2, §2.3, §2.4, §3.2; G1a (onset-sampled slope +0.046 ≤ 0.10, against +1.24 for the revision-2 route on a harsher partner), G1c (turn-locked face ≤ 0.002) |
| K1b | role (from partner VAD) entered unscaled; a role-only jaw display copied the partner's jaw at 0.83 | VAD enters 𝓡 only through √κ_a; role exists only as a bounded gate on partner-input terms; the free display's T inputs are constant within a partner turn, so no role display exists | §2.2, §2.4; G1d (≤ 0.065 over role gains 0.1–3) |
| K1 fix 3 | G_Ω read c̃ with no cap | G_Ω(0, c̃) = 0; the 0.10 cap is joint in (e, c̃); the port is not in phrase targets | §2.10.6 |
| K1 fix 4 | F1 could not see turn-locked copy | F1 now includes onset-sampled phrase targets and the face 0–4 s after each partner turn end | §8.2 |
| K3 (high) | own-body head (i) learned that acts which make the partner look better lower the agent's own concern (P(flatter) 0.72–1.00) | the partner is modelled as need N, display F and report-and-choice Q. In every rollout F is imputed at the default act, N is read only from unprompted Q through a frozen decoder, and partner-driven loads never come from head (i), which is trained on E, I and own-driven A only | §2.9; G5a (P(flatter) = 0.500) |
| K4 (medium) | lexical surprise as one impulse per utterance made the partner's turn rate a dial on arousal and speech rate (0.07–0.28) | every word-driven input is a latched held value, not an impulse. The same rule covers P_name (latched rate) and K (relief saturates into the dead-band at every rate) | §2.1, §2.10.7; G4e (swing 0.1 %), G4d, G6b |
| K2 (low) | sampling the fast path at phrase onset reached 0.41 of the last phrase step | phrase targets exclude the fast term; it is rendered only as a continuous within-phrase contour | §2.3; G1 (reference +0.095 with a 0.3-s onset, no longer sampled) |
| K5 (low) | the blind band was at 1–3 min, not 4 s – 1 min | the cone's 20-s and 2-min traces cover 30 s – 3 min with away and cross reach 0.21–0.79; the description is corrected | §3.2; G9 |

**Agent critique (critique-2-design-cayley-ledger-agent.md):**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| A1 | muted by construction: the ℓ∞ slow bound is a ±0.15 ball in every direction | the two-sided slow bound is replaced by the one-sided cone: sym(G_m) ⪯ b_m I over completely monotone traces. In phase ≤ 0.10 in every direction at every time and window; same channel down to −1.40; cross to ±0.49. T-typed state (words, exchange structure, own body) drives the face with no partner cap | §2.5, §2.6, §3.3; G2b (anti −1.17 reached; in-phase ≤ b), G7 |
| A1′ | the late-window delayed copy that motivated the ℓ∞ bound | the step response of each trace is monotone and non-negative, and each coefficient's in-phase form is ≤ b_m, so every window's in-phase mean is ≤ b; adversarial search reaches +0.000, and the tight instance reaches 0.097 | §3.3; G2b (revision 2's ℓ₂ disc: +0.265 at 60 min) |
| A2 | no positive affect: 𝒟 ≥ 0 with a dead-band | valence is −d𝒟/dt (Joffily & Coricelli; Keramati & Gutkin); new satiable deficits K (contact) and P (play), relieved only by exchange events, never by the partner's smile or time; good news relieves word-read need, a reunion relieves K, play relieves P | §2.7, §3.5; G4a–G4f, G7.2, G7.4, G7.5 |
| A3 | never speaks first; concern built in about 10 min | body onset at ~0.3 s; a softened follow-up at 1.5 s after an unanswered question; a concern bid in a lapse; a greeting at reunion; a 20-s face trace and a 40-s attack, so concern is at 61 % by 1 min and 90 % by 2 min | §2.8, §3.6; G3 (thresholds crossed at 41–74 s), G7.1 |
| A4 | Claude cannot regulate the state | P_name: the agent hears its realised words; matched naming contracts F loads (latched rate) and attenuates T loads (≤ 0.17); attenuate-only, never across set point; Claude never sees a value | §2.10.7, §3.7; G6 (half-life 6.9 → 2.9 min) |
| A5 | care rewards matching (perceptual cancellation) | the cone, C_F and b̂_p read the partner's own face Pu, not w = v − s | §3.4; G5c (concern independent of own display) |
| A6 | comfort reversal; double count of concern | the care term is not a body variable; the partner's inferred body has no concern coordinate; f_recv is trained on E, A, V only; the agent's own comforting words are labels and contract its concern | §2.7, §3.7 |
| A7 | Π̃'s gain allocation unstated; C stuck in the dead-band | Π̃ inverts the free display Π_o, whose distress gains (0.45) cover the partner's range (inverse gain ≈ 2.2) | §2.7 |
| A8 | uncounted mid-band route c̃ → S_f | as K1 | §2.4 |
| A9 | naming inherits the user's vocabulary; the PMI label channel undeclared | PMI for naming counts only the agent's own tokens; the retrieval label channel is declared at ≈ 6 bits per turn | §2.10.4 |
| A10 | fatigue gives an incentive to end conversations; "rest" undefined | E is restored only in the nightly sleep period; ending a conversation lowers no term | §2.1, §3.11 |
| A11 | A named and also read out; C and V as social constructs | A is a physiological activation load (arousal is read out separately); C is no longer a body variable; V, K, P are stated as needs named by function, a P2 strain listed honestly | §3.11 |
| A12 | Yoshida & Man: care blind to its effect will not learn to help | the need path is kept: act → N, read through unprompted reports, so care is credited for real help; display and prompted replies are cut | §2.9; G5b (P = 0.50, 0.945, 1.00 for need drops of 0, 0.05, 0.15) |
| A13 | novelty: the three claimed combinations are known | accepted; the verdict stays recombination; the new one-sided certificate and the typing are stated as composition results | §10 |
| — | "your face can change its lasting expression by at most a seventh of range, in any direction" (trade-off for the operator) | no longer true: toward ≤ 0.10 (0.15 with the naming port); away and across up to 1.40 and 0.49 | §0 |

**Status:** revision 3; to be critiqued (routes and copying, including the definitional seam and the per-pair caveat; principles, emotional fitness and novelty).

