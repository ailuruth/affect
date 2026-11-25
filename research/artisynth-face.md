# ArtiSynth and its FEM face model (artisynth_core, artisynth_models)

Sources read: github.com/artisynth/artisynth_core README, LICENSE, lib/LIBRARIES, mainModels.txt, doc/installation/gitEclipseInstall.tex; github.com/artisynth/artisynth_models LICENSE and src/artisynth/models/face/ (BadinFaceDemo.java, file listing).

## Claims
- A Java system for combined multibody and finite-element biomechanical simulation with point-to-point and FEM muscles, contact and constraints, plus an interactive GUI.

## Evidence
- `mainModels.txt` lists face models: `BadinFaceDemo`, `BadinFemMuscleFaceDemo`, `RefFaceDemo`, plus jaw, tongue and larynx models.
- BadinFaceDemo builds a `FemMuscleModel` face with Mooney-Rivlin tissue, 5 ms max step, and muscles named DAO, BUC, DLI, MENT, MAS (unused), OOM, OOP, LLSAN, LAO, RIS, ZYG, LLS. These are all lower-face and perioral muscles; there is no frontalis, corrugator or orbicularis oculi, so no brow or eye AUs.
- The data folders are speech-oriented (`closure`, `fricative`, `approximant`, `lip_opening`).
- Install guide: "ArtiSynth runs on Macs based on either Apple silicon (the Apple M chips) or Intel processors"; Java 21 or later recommended. LIBRARIES lists `MacOSArm64` native solvers (AccelerateJNI, MumpsJNI).
- artisynth_core was pushed 2026-11-18; artisynth_models 2025-07-07.

## License (paper, code, model weights)
- artisynth_core: 2-clause BSD (bundles TetGen under its own license).
- artisynth_models: BSD-style with a third clause requiring citation in academic publications.

## Runs on this Mac without a GPU?
- Yes, as a desktop Java app on Apple silicon (per the install guide). No real-time or per-frame cost for the face FEM is stated, and nothing suggests it runs at 30 Hz.

## Verdict: watch
- The brief already names it as the later muscle-model source ("train on ArtiSynth simulations, without changing the interface"). License and platform fit.
- Gap to record now: the shipped face covers only the mouth region, so a full-face muscle set would have to be added before it can stand behind every AU in the S2 interface.
- Not needed for S2, where the face stays AU-driven.

## Role in S2
- none (S2 should only keep the AU interface stable so this can replace the rig later)
