# Meyda (audio feature extraction for JavaScript; WAC 2015 paper)

Sources read: github.com/meyda/meyda README; meyda.js.org/audio-features; npm package meyda 5.6.3 (dist sources). I did not read the WAC 2015 paper.

## Claims
- Offline and real-time audio feature extraction through the Web Audio API.
- 21 features: rms, zcr, energy, amplitude and power spectrum, spectral centroid, flatness, flux, slope, rolloff, spread, skewness, kurtosis, crest, chroma, loudness (Bark bands and total), perceptual spread and sharpness, mfcc, complexSpectrum, buffer.

## Evidence
- No f0 or pitch feature: `chroma` is pitch-class content, not f0. Pitch needs another library (see pitchy.md).
- The real-time analyzer is built on `createScriptProcessor` (8 occurrences in dist, no AudioWorklet), i.e. the deprecated main-thread ScriptProcessorNode.
- `Meyda.extract(features, buffer)` also works on raw buffers, so it can run inside our own AudioWorklet or Worker.
- Bug found here: in 5.6.3 `spectralFlux` assigns an undeclared `x` and throws `ReferenceError` under ESM strict mode (Node 24).
- Measured here (Node 24, M1 Pro, 2048 samples): `extract(['rms','energy','zcr','spectralCentroid','loudness'])` takes 0.30 ms per call.
- Last npm modification 2024-04-21; last push 2024-07-15.

## License (paper, code, model weights)
- Code: MIT. No weights.

## Runs on this Mac without a GPU?
- Yes. About 0.3 ms per frame for five features (measured).

## Verdict: watch
- Fits Principles 1 and 7 (pure DSP, local), but S2 needs only energy, voicing, f0 and rate. Energy is a one-line RMS, and the rest come from pitchy plus our own onset counting.
- Adopt `extract()` only if a later stage needs spectral or MFCC features, and never its ScriptProcessor analyzer.

## Role in S2
- none now (optional perception helper later)
