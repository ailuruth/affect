# This Mac (generic description)

| Item | Value |
|---|---|
| Machine | Apple-silicon MacBook Pro (M1 Pro class) |
| Unified memory | 16 GB |
| Disk | limited free space; check `df -h .` before any download |
| Software | recent macOS; PyTorch with MPS in the research/foundations/sims uv environment |

## Budget rules (operator note Q10)

- **Disk.** Operator lowered the floor to 10% free on 2026-11-25 (Q11); the text below predates that. Keep the free-space floor the operator sets. **No downloads beyond tiny pilots are possible** until space is freed or the rule is relaxed. This is put to the operator in research/questions.md.
- **Memory.** 16 GB unified memory, and the operator uses this Mac for other work. Plan peak use at **≤ 6 GB** per experiment, with no run approaching 16 GB.
- **Run time.** Ask the operator before any run expected to take more than about 6 hours.
- **Downloads.** Ask before any single download over 20 GB. Re-check `df -h .` before every download.
