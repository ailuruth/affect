# OpenFACS (Cuculo and D'Amelio, ICIG 2019)

Sources read: github.com/phuselab/openFACS README, LICENSE, releases, repo tree, python/openFACS.py, source/Source/ActionUnitsFace/MeshActor.cpp.

## Claims
- An open-source FACS-based 3D face that renders facial expressions from action-unit intensities in real time, with an API usable "without any prior experience in computer graphics".

## Evidence
- Interface: a UDP server on localhost:5000 takes JSON with 18 AUs (AU1, 2, 4, 5, 6, 7, 9, 10, 12, 14, 15, 17, 20, 23, 25, 26, 28, 45) plus a `Speed` interpolation rate (python/openFACS.py).
- MeshActor.cpp interpolates toward the target AUs each tick and adds "livingness": random blink timing, neck sway, eye and mouth micro-motion, each toggled by hotkeys.
- `demo/` ships nine prototypical-emotion AU vectors (anger, happiness, sadness, ...).
- Releases contain only a Linux build (`openFACS_Linux.tar.gz`, `ActionUnitsFace-Linux-Shipping`). The repo has the Unreal Engine 4 C++ source and config, but no `Content/` folder, so the face mesh and morph targets are not in the repo.
- Last push 2021-12-16.

## License (paper, code, model weights)
- Code: MIT (LICENSE, "Copyright (c) 2019 PHuSe Lab"). Paper: Springer LNCS. The face asset's license is not stated, and the asset is not in the repo.

## Runs on this Mac without a GPU?
- No as shipped: Linux-only UE4 binary. Rebuilding for macOS would need UE4 plus the missing mesh assets. No frame-rate numbers are stated.

## Verdict: reject (as a runtime); keep as an interface reference
- The AU-in/face-out contract (AU vector + transition speed, autonomic livingness layered on top) matches the brief's Body and Motor components. The format is worth copying.
- It cannot run in the browser or on this Mac, and its assets are missing.
- Its emotion demo vectors are presets and must not be used (Principle 2).

## Role in S2
- none (interface reference for the rendering contract only)
