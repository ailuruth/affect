# Phace: Physics-based Face Modeling and Animation (Ichim, Kadlecek, Kavan, Pauly, SIGGRAPH 2017)

Sources read: full paper PDF from users.cs.utah.edu/~ladislav/ichim17phace/ichim17phace.pdf; project page (same site). EPFL Infoscience returned an HTML page instead of the PDF.

## Claims
- Expressions are computed by minimizing nonlinear energies of passive flesh, active muscles and rigid bone, with collision and contact handling, avoiding inconsistent poses of blendshape rigs.
- A new muscle activation model (a 6-DoF symmetric activation matrix per active tet) and an inverse procedure that fits per-person models from a few expression scans.

## Evidence
- Control interface: a template with "48 blendshapes inspired by FACS" sculpted by an artist; blendshape weights from performance capture are mapped to per-frame muscle activations, and the jaw is kinematic (5 DoF).
- Statistics: forward solve averages 8 interior-point iterations per frame, "approx. 22 seconds including the collision detection update on a consumer laptop with a 3.1 GHz Intel Core i7 processor and 16GB"; inverse fitting about 3 minutes per target shape.
- Limitations: "our method is currently not suitable for realtime animation"; suggests offline generation of corrective shapes for a blendshape basis.
- The project page links only the paper and BibTeX; no code or model release.

## License (paper, code, model weights)
- Paper: ACM TOG copyright (accepted version on EPFL Infoscience). Code and models: not released.

## Runs on this Mac without a GPU?
- No in real time: about 22 s per frame on a CPU laptop as reported. No code to run anyway.

## Verdict: watch
- Theory basis for the later "muscle model behind an AU interface" step: FACS-like controls in, muscle activations and physics out, which matches the brief's plan to swap the body without changing the interface.
- Its suggestion to bake physics into corrective blendshapes offline is the realistic route for a 30 Hz loop.
- Nothing to adopt for S2.

## Role in S2
- none
