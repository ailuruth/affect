# Loom3 (Jonathan Sutton Fields; npm @lovelace_lol/loom3, 2025-2026)

Sources read: github.com/meekmachine/Loom3 README (full) and LICENSE; npm metadata for @lovelace_lol/loom3 1.0.47; GitHub metadata for meekmachine/embody (renderer-agnostic successor).

## Claims
- A three.js character controller that maps FACS action units to a rig's morph targets and bones, so callers "simply say `setAU(12, 0.8)`".
- Runtime: AUs, visemes, direct morphs, "continuum pairs", composite rotations, timed transitions (`transitionAU(au, value, ms)`), mixer playback; plus rig inspection and preset validation tools.

## Evidence
- Presets: `CC4_PRESET` for Character Creator 4 rigs ("87 AUs total" in `auToMorphs`, "32 bone bindings" in `auToBones`, e.g. AU51 -> head yaw, AU61 -> eye rotation) and `BETTA_FISH_PRESET`. No ARKit-52 preset in the README, but `extendPresetWithProfile` supports custom maps.
- Each AU maps to left, right and center morph lists, so asymmetric activation is first-class.
- Ships no character asset; examples load `/character.glb`.
- Peer dependency three >= 0.150.0; package unpacked about 2.5 MB. Created 2025-09-01, last push 2026-10-04, 4 stars. A newer renderer-agnostic repo, meekmachine/embody (MIT, created 2026-05-28), carries its history.

## License (paper, code, model weights)
- Code: MIT ("Copyright (c) 2025-2026 Jonathan Sutton Fields"). Character Creator 4 assets have their own vendor license (not reviewed). No paper.

## Runs on this Mac without a GPU?
- Yes in principle: plain three.js/WebGL on the integrated GPU. No performance numbers are stated.

## Verdict: watch
- Its contract (AU id + intensity + transition time in, per-side morphs and bones out) is the brief's Body interface, MIT, in the browser stack we use.
- It is young, has a single author, and is tied to CC4 rigs. Adopting it means writing an ARKit-52 preset ourselves.
- An AU-to-ARKit table of our own may be smaller than the dependency. Copy the design, decide on the code at build time.

## Role in S2
- rendering (AU-to-morph mapping layer)
