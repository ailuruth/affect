# James, Barnett & Crutchfield 2016, "Information Flows? A Critique of Transfer Entropies" (Phys Rev Lett 116:238701; arXiv:1512.06479; SFI Working Paper 16-01-001)

Source read: arXiv v2 (17 Jun 2016, dated June 20, 2016), 6 pages including references, in full: introduction, background, both examples, discussion (conditioning, partial information decomposition), conclusions and the footnotes. The published PRL version was not compared against it.

## Claims
Stated as strongly as the authors state them:
- Thesis: "the transfer entropy does not, in fact, measure information flow, specifically in that it attributes an information source to influences that are not localizable and so not flows." "At one and the same time they can overestimate flow or underestimate influence."
- Their definition of flow: "Information flow from process X to process Y is the existence of information that is currently in Y, the 'cause' of which can be solely attributed to X's past. If information can be solely attributed in such a manner, we refer to it as localized."
- Root cause: "probabilistic conditioning is not a 'subtractive' operation: I[X : Y | Z] is not the information shared by X and Y once the influences of Z have been removed. Rather, it is the information shared by X and Y taking into account Z." "Conditioning can increase the information shared between two processes".
- In partial information decomposition terms, "I[X1 : Y | X2] = U1 + S": "conditioning removes the redundant information, but adds the synergistic information." "The transfer entropy, however, conflates unique information and synergistic information". Only the unique part should count as flow, but "there is as yet no broadly accepted quantification of unique information".
- Scope: the critique holds "for any related measures—such as the causation entropy—that are based on conditional mutual information between observed variables". They "conjecture" that directed information, Granger causality and Ay-Polani intervention-based flow "all ... suffer for the same reasons—conflation of dyadic and polyadic relationships." Directed information "is essentially a sum of transfer entropies and so inherits the same flaws."
- What they do not object to: "While we do not object to the transfer entropy as a measure of the reduction in uncertainty about one time series given another, we do find its mechanistic interpretation as information flow or transfer to be incorrect."
- Networks: modelling a system "by way of a graph with edges determined by transfer or causation entropies is intrinsically flawed", because pairwise edges cannot show polyadic dependence. Works on "cellular automata ... information thermodynamics ... cell regulatory networks ... and consciousness" that rely on such measures "will benefit from a close reexamination."
- Generality: "similar failures arise in Gaussian systems [13] signifying that the issue at hand is widespread" ([13] = Barrett 2015, PRE 91:052802).

## Evidence
Two constructed counterexamples, computed exactly:
- Example 1 (TE overestimates flow). X_t and Y_0 are fair coins, and Y_t = X_{t−1} ⊕ Y_{t−1}. "T_{X→Y} = 1 bit". But "I[Yt : X0:t] = 0 bit" and "I[Yt : Y0:t | X0:t] = 1 bit", so from the other side it is Y's past that predicts. The co-information is "I[Yt : X0:t : Y0:t] = −1 bit". Hence "the 1 bit of reduction in uncertainty H[Yt] should not be localized to either time series. The transfer entropy, however, erroneously localizes this information to X0:t."
- Example 2 (TE underestimates influence). X_t and Y_t are fair coins, and Z_t = X_{t−1} ⊕ Y_{t−1}. "T_{X→Z} = T_{Y→Z} = 0 bit, and it therefore underestimates influence that is present"; all pairwise MIs vanish. The causation (conditional transfer) entropy gives "C_{X→Z|(Y,Z)} = C_{Y→Z|(X,Z)} = 1 bit", which again wrongly localises a jointly held bit.
- Indirect paths: for X → Z → Y, "T_{X→Y} > 0 bit even though X does not directly influence Y", while causation entropy conditioned on Z is 0.
- Reproduced on this Mac (standard-library Python, plug-in estimates, history length 1, 200,000 samples): Example 1 gave T_{X→Y} = 1.000, I[Y_t : X_past] = 0.000, I[Y_t : Y_past | X_past] = 1.000. Example 2 gave T_{X→Z} = T_{Y→Z} = 0.000 and C_{X→Z|(Y,Z)} = 1.000 bit.

## License
arXiv non-exclusive distribution license 1.0. No code with the paper.

## Runs on this Mac without a GPU?
Yes. Both counterexamples run in under a second, CPU only (above).

## Verdict: adopt (as a binding constraint on how the TE measure is interpreted and designed)
This does not kill TE as the contingency measure. The authors explicitly accept TE "as a measure of the reduction in uncertainty about one time series given another", and that is what "contingently answered" needs: the agent's next state is better predicted given the partner's past. It does kill three things we might otherwise say or build:
- Do not call it "information flow" from the partner to the agent, or treat TE as the amount the partner "sent". Call it predictive dependence.
- Synergy is the live failure in a dyad. A partner's reply is often a function of both the agent's last move and the partner's own state (Example 1 is exactly "the next state = my move XOR your move"). Then TE partner→agent can be high even though no bit is attributable to the partner alone. Conversely, a reply that depends on a combination of two of the partner's channels can show zero pairwise TE from each channel (Example 2). Measuring per-channel TE in the sign map and summing it is wrong. Measure TE from the full joint sign vector, and do not attribute it to single channels.
- "Contingent on me" needs both directions plus a perturbation. Because conditioning can create dependence, a TE asymmetry alone does not establish who answers whom. Pair the measure with interventions (replay or delay the partner stream, still-face) and with a known-structure synthetic check like the XOR examples in the test suite.
Open: there is still no accepted measure of unique information (the authors' preferred fix), so a PID-based "true flow" is not available off the shelf.
