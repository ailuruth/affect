# This Mac (measured 2026-11-25T08:49:05Z from macOS)

| Item | Value | Source |
|---|---|---|
| Model | MacBook Pro (MacBookPro18,1) | system_profiler SPHardwareDataType |
| Chip | Apple M1 Pro | sysctl -n machdep.cpu.brand_string |
| CPU cores | 10 (8 performance, 2 efficiency) | system_profiler; hw.perflevel0/1.physicalcpu |
| GPU cores | 16 | system_profiler SPDisplaysDataType |
| Unified memory | 16 GB (17,179,869,184 bytes) | sysctl -n hw.memsize |
| Disk (volume holding this repository) | 460 GiB total, 378 GiB used, **55 GiB free (12% free)** | df -h . |
| macOS | 27.2.1 (build 26B131) | sw_vers |
| PyTorch | 2.15.0, MPS available and built, Python 3.15.2 (research/foundations/sims uv environment) | torch.backends.mps |

## Budget rules (operator note Q10)

- **Disk.** Operator lowered the floor to 10% free on 2026-11-25 (Q11); the text below predates that. Keep at least 20% free, which is about **92 GiB**. Measured free space is **55 GiB**, already **37 GiB below the floor**. **No downloads beyond tiny pilots are possible** until space is freed or the rule is relaxed. This is put to the operator in research/questions.md.
- **Memory.** 16 GB unified memory, and the operator uses this Mac for other work. Plan peak use at **≤ 6 GB** per experiment, with no run approaching 16 GB.
- **Run time.** Ask the operator before any run expected to take more than about 6 hours.
- **Downloads.** Ask before any single download over 20 GB. Re-check `df -h .` before every download.
