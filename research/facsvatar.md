# FACSvatar (van der Struijk et al., IVA 2018)

Sources read: github.com/NumesSanguis/FACSvatar README, LICENSE_note.txt, docs/misc/license.rst, openface/OpenFace-license.txt, modules/process_facstoblend/au2blendshapes_mb.py, repo tree.

## Claims
- A modular framework that uses FACS AUs as the intermediate representation between any face tracker and any avatar, with modules connected over ZeroMQ, "Real-time" and "on any OS".

## Evidence
- Input: OpenFace 2.1 (webcam real-time path is "Windows-only for now"). Output: Unity3D (tested 2018.2) or a Blender add-on; avatars from Manuel Bastioni Lab.
- `process_facstoblend` maps AUs to blendshapes through per-AU JSON files (AU01.json ... ) of MB-Lab shape-key weights, splitting each value into `_min`/`_max` around 0.5.
- Python modules are Dockerized; no browser renderer.
- README notes v0.4.0 was merged unfinished in 2023 and v0.5.0 has "no release date yet"; last push 2023-06-29.

## License (paper, code, model weights)
- FACSvatar's own code: LGPL-3.0.
- OpenFace (the tracker it depends on): "ACADEMIC OR NON-PROFIT ORGANIZATION NONCOMMERCIAL RESEARCH USE ONLY", and derivatives become owned by CMU.
- Manuel Bastioni models: CC-BY 4.0 or AGPLv3; MB-Lab Python code GPLv3.

## Runs on this Mac without a GPU?
- README says it "should work on MacOS", but the real-time webcam path is Windows-only and the renderer is Unity or Blender. No frame-rate numbers are stated.

## Verdict: reject
- The architecture (tracker -> AU bus -> avatar) is right for Principle 1, but every piece is outside our stack: OpenFace's license, Unity/Blender rendering, dormant code.
- The idea worth keeping is the per-AU blendshape mapping table, which we would write ourselves for our rig.
- Its default use is puppetry (tracked face -> avatar), which, used directly, would make the user's face the source of when the agent's face moves.

## Role in S2
- none
