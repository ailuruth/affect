# Stivers, Enfield, Brown, Englert, Hayashi, Heinemann, Hoymann, Rossano, de Ruiter, Yoon & Levinson 2009, "Universals and cultural variation in turn-taking in conversation"

PNAS 106(26):10587-10592. doi:10.1073/pnas.0903616106. PMC2705608.

Source read: the PMC full text, read through a summarizing web fetch (the fetch tool returns a model-written account with quoted numbers, not the raw page), covering abstract, introduction, results, Table 1, discussion and methods. Direct downloads of the PDF and XML failed. The supplementary tables with per-language means, medians, modes and sample sizes (Tables S3-S4) were NOT read. Treat the numbers below as the fetch reported them; check against the article before citing exact values.

## Claims
- Question: is conversational timing culturally variable (claims of long Nordic silences, overlap-tolerant Antiguan or New York speech) or a universal system with small calibrations?
- Data: videotaped spontaneous informal conversations in 10 languages on 5 continents (including Danish, Dutch, English, Italian, Japanese, Korean, Lao, Tzeltal, Yélî-Dnye, ‡Ākhoe Hai‖om); about 350 consecutive questions per language from 5-17 interactions; 101 conversations; no interaction over 3% of the data. Polar (yes/no) questions only (67% of the questions in the sample).
- Timing coded in ELAN as the offset from the end of the question to the start of the response, where a response starts when "a vocal or gestural response was initiated" (so nods count), measured in 10 ms steps and rounded to 100 ms.
- Distribution: unimodal, slightly right-skewed. Overall mode 0 ms, every language's mode between 0 and +200 ms. Medians from 0 ms (English, Japanese, Tzeltal, Yélî-Dnye) to +300 ms (Danish, ‡Ākhoe Hai‖om, Lao); overall median +100 ms. Overall mean +208 ms; fastest Japanese +7 ms, slowest Danish +469 ms; all language means within about 250 ms of the cross-language mean.
- The same factors shift timing in every language (multilevel regression, responses in 101 interactions in 10 languages, estimates in ms): non-answer +132 (CI 59 to 204); confirmation -207 (-269 to -145); a visible component (nod, shrug, headshake, conventional blink) -87 (-137 to -37); a pure information request +129 (79 to 179); questioner gaze at the responder -69 (-123 to -15). Answers beat non-answers in all languages; confirmations were 100-500 ms faster than disconfirmations (significant in 7/10); visible responses faster in all 10 (significant in 7); gaze speeds responses in 9/10 (significant in 5).
- Perceived timeliness differs by culture: responses judged "on time" averaged about 200 ms in Danish and Lao against 36 and 83 ms in Japanese and Tzeltal (t(847) = -10.97, p < .001): a cultural "calibration" of what counts as a delay.
- Language structure (where the question is marked, family relatedness) does not explain the differences.
- Conclusion: a universal system that minimizes gaps and overlaps, with local variation "quantitative only", and high sensitivity to deviations of about 100 ms; an interactional foundation for language with likely ethological roots.

## Evidence with numbers
As above (mixed model fixed effects with 95% CIs; language-level variance 19,555 and interaction-level 14,091 ms^2).

## What it implies for an engine whose voice is driven from an internal state through an innate vocal body, with real-time timing
- The target distribution for the engine's response onsets is known and nearly universal: mode 0-200 ms after the operator's turn ends, mean around 200 ms, almost nothing beyond a second. It is measured with the same coding (first vocal or visible response), so the engine's face counts: a nod or a facial onset can open its turn faster than speech (visible responses were 87 ms faster).
- Delay is meaningful. Disconfirmations and non-answers come 130-200 ms later in every culture, so listeners read a late response as trouble. The engine's latency must therefore be driven by its state (an engine that disagrees or is uncertain should be later, an engine that agrees earlier), and system latency must be small enough that it does not swamp this signal. A pipeline whose minimum latency is 600-800 ms makes every response sound like a dispreferred one.
- Gaze speeds responses in nearly every language: the engine's gaze at the operator at the end of its question is a turn-yielding cue it can produce, and the operator's gaze at the engine is an input to its own turn-taking.
- The per-person calibration of "on time" (about 200 ms vs under 100 ms) is the kind of parameter that should be learned by living with the operator, not fixed; ten Bosch et al. (in levinson-torreira-2015-turn-taking-timing.md) show people adjust their gap length to the partner.
- An evaluation instrument: compare the engine's floor-transfer-offset distribution, and its dependence on (dis)confirmation, against these published values.

## License
PNAS, author-choice open access on PMC. No data released beyond the supplement.

## Verdict: adopt (target timing distribution and the state-dependent delay factors)
Read Tables S3-S4 for per-language numbers before using any single language as a reference.
