# Open-problems matrix

_20 problems across 6 areas, window 2025-01 to 2026-09, compiled 2026-09-16._

**15 open · 5 partial · 0 solved.** Status is the field's, not this repo's.

## Learning-based control and VLAs

| Problem | Status | Evidence | Source |
|---|---|---|---|
| Semantic-vs-embodied gap: VLA systems often understand the instruction but fail to execute the task, because they inherit LLM/VLM priors with no physical-interaction experience. | 🔴 open | reported | VLA semantic-vs-embodied gap paper (2026) |
| Capability/robustness trade-off: an information-theoretic bound argues you cannot get both for free. | 🔴 open | reported | Capability/robustness trade-off (information-theoretic bound) (2026) |
| Discrete action tokenization itself limits VLA scaling. | 🔴 open | reported | Discrete action tokenization limits VLA scaling (2026) |
| Skill portability: commercial robot-skill marketplaces ship one-tap skills only as static playback. Open sub-problems are adaptation, cross-embodiment portability, provenance, safety verification, composition, and standardisation. | 🔴 open | consensus | Robot-skill marketplace survey (2026) |
| Merging whole-body control with VLA policies (the HOVER / ASAP / OmniH2O line). One survey calls this the most important open problem in the field. | 🔴 open | consensus | Whole-body + VLA survey (2026) |

## Evaluation and benchmarks

| Problem | Status | Evidence | Source |
|---|---|---|---|
| There is no SWE-bench for robotics: every paper uses a slightly different task suite, camera setup, and embodiment. The stated need is a small sharp benchmark plus a large contamination-controlled real-world one. | 🔴 open | consensus | Robotics evaluation consensus (surveys/position papers) (2026) |
| Deformable-object manipulation lacks a universal high-DoF dexterous hand with tactile sensors and comprehensive evaluation at scale. | 🔴 open | consensus | Deformable-object manipulation survey (2026) |

## World models and simulation

| Problem | Status | Evidence | Source |
|---|---|---|---|
| Learned simulators are now used as RL environments and even co-evolve with policies, but fidelity, long-horizon consistency, and trustworthy use as sim-to-real bridges remain open. | 🟡 partial | consensus | World-model survey (2026) |
| Physics-sim limits: humanoid control tasks particularly highlight the simulation-to-reality gap, suggesting improved physics modeling is needed. | 🟡 partial | reported | MuJoCo Playground writeup (2026) |

## Safety

| Problem | Status | Evidence | Source |
|---|---|---|---|
| Adversarial and backdoor attacks and environmental jailbreaks (malicious text/objects in the scene that steer the robot) have no robust defenses or evaluation standards yet. | 🔴 open | consensus | VLA-safety survey (2026) |

## Software infrastructure (ROS 2 and friends)

| Problem | Status | Evidence | Source |
|---|---|---|---|
| Added abstractions increase complexity and steepen the learning curve, especially migrating from ROS 1; adoption is hindered by tooling immaturity, documentation gaps, and limited debugging support. | 🟡 partial | consensus | "ROS 2 in a Nutshell" (2026) |
| Open-problem table covers performance, real-time guarantees, scalability, security, and ecosystem maturity; few studies provide verified end-to-end guarantees under adversarial and multi-robot conditions. | 🔴 open | consensus | "ROS 2 in a Nutshell" (2026) |
| Middleware fixes (hierarchical discovery, partition-based segmentation, RMW designs such as Zenoh) mitigate problems but increase ecosystem heterogeneity and interoperability complexity. | 🟡 partial | consensus | "ROS 2 in a Nutshell" (2026) |
| Misconfigurations, physical-unit mismatches, dependency bugs, and inter-component interaction bugs remain empirically common with only partial tooling; formal methods are hard to apply because building models and extracting parameters is manual. | 🟡 partial | consensus | SE research on ROS bugs (ICSE/ISSTA/FSE track) + Frontiers 2025 editorial (2025) |
| Runtime verification and field-based testing of ROS systems is active but immature: no standard CI / hardware-in-the-loop practice. | 🔴 open | consensus | Runtime verification / field-based testing of ROS (2025) |

## Cross-cutting

| Problem | Status | Evidence | Source |
|---|---|---|---|
| Data acquisition at scale is unresolved and recurs across the 2026 surveys. | 🔴 open | consensus | Robotics evaluation consensus (surveys/position papers) (2026) |
| Reward design remains unresolved and recurs across the 2026 surveys. | 🔴 open | consensus | "10 Open Challenges" position paper (2026) |
| Energy and compute budgets on-board recur as an unresolved constraint. | 🔴 open | consensus | "10 Open Challenges" position paper (2026) |
| Human-intent prediction recurs as unresolved across the 2026 surveys. | 🔴 open | consensus | Whole-body + VLA survey (2026) |
