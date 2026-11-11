# Evolution Journal

## Entry 001 — Version 0.1 (Baseline)
- **Status**: Initial baseline paper generated.
- **Core Hypotheses**: RSI is distinct from iterative refinement; evaluation reliability is the primary bottleneck.
---


## Iteration 20261111_132623 — 2026-11-11
**Summary**: This revision updates the living paper to Version 0.2 by incorporating five new empirical and architectural studies published in November 2026. Key additions include the formalization of the "RSI Tax" (which reveals that verification accounts for 74.8–93.6% of improvement overhead), multi-agent harness and memory adaptation systems (SciMARS, ForgeSystem), verifier-gated weight-space control policies (NCP), and real-world latency constraints that lead embodied physical agents to explicitly eschew RSI in favor of direct execution (BEHAVIOR-1K).

# Evolution Journal: Entry #002
**Date:** November 2026  
**Subject:** Integration of New Empirical Studies (RSI Tax, SciMARS, ForgeSystem, NCP, BEHAVIOR-1K)

### 1. Ingested Research Synthesis
Five papers published in November 2026 were processed and integrated:
- **arXiv:2611.13524 (Zhang et al., 2026):** Introduces "The RSI Tax", demonstrating that verification consumes 74.8–93.6% of self-improvement token costs. Shows bounded static baselines can outperform complex RSI loops (Meta-Harness, EvoSkill, RRSI) by 65.6–71.0% in token efficiency.
- **arXiv:2611.12552 (Wu & Liu, 2026):** Proposes SciMARS, proving that multi-agent systems benefit from dynamic role procedure adaptation and shared memory graph editing in scientific discovery tasks.
- **arXiv:2611.12288 (Q. He et al., 2026):** Proposes ForgeSystem, establishing a 3-tier structure (Control Layer, Forge Loop, RSI Loop) to produce specialized software artifacts (megakernels, training engines).
- **arXiv:2611.13236 (Aksoy, 2026):** Proposes Neural Control Plane (NCP) for transactional weight-space control policy optimization, demonstrating how verifier admission gates reject candidate rules when proxy metric drops fail to yield exact-answer accuracy gains.
- **arXiv:2611.13818 (Y. He et al., 2026):** Details the 2nd place BEHAVIOR-1K solution, explicitly highlighting why real-time physical robotics (1-2 FPS constraint) deliberately bypasses RSI and agentic harness loops.

### 2. Conceptual Updates to the Living Paper
- **Taxonomy Expansion (Section 2):** Added decoupled demand-specific RSI to distinguish offline harness/kernel adaptation from online task execution.
- **Mechanics & Frameworks (Section 3 & 4):** Updated mechanics to cover harness topology modification (SciMARS), weight-space control-plane interventions (NCP), and dual-loop artifact forge systems (ForgeSystem). Added empirical real-time counter-examples (BEHAVIOR-1K).
- **Verification Bottleneck Quantified (Section 5):** Integrated the exact token cost breakdown of the RSI Tax, establishing that verification (74.8–93.6%) is the overwhelming financial and computational bottleneck. Added NCP's exact-answer failure mode as an example of proxy metric optimization.
- **Economic & Latency Constraints (Section 6 & 7):** Established the formal economic condition ($\Delta \text{Utility}_{\text{task}} > \text{RSI Tax}$) required for RSI viability, contrasting it against simple bounded-note baselines.

### 3. Hypothesis Evaluation & Status

| Hypothesis ID | Description | Pre-0.2 Status | Post-0.2 Status | Supporting Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **H-VERIFY-01** | Verification costs will dominate RSI compute budgets. | Hypothesized | **Confirmed** | Zhang et al. (2026) empirically proves verification accounts for 74.8–93.6% of the RSI Tax. |
| **H-ECON-01** | Simple bounded baselines can economically outcompete unconstrained RSI loops. | Unexamined | **Confirmed** | Zhang et al. (2026) shows bounded-note baseline matches performance with 65.6–71% token savings. |
| **H-LATENCY-01** | Real-time embodied applications will avoid online RSI due to throughput constraints. | Unexamined | **Confirmed** | Y. He et al. (2026) eschews RSI/harnesses to sustain $\ge 1$ FPS on 100 BEHAVIOR tasks. |
| **H-DECOUPLE-01** | Sustainable RSI requires decoupling execution data planes from adaptation control planes. | Emerging | **Strengthened** | ForgeSystem (Q. He et al., 2026) and NCP (Aksoy, 2026) both successfully implement decoupled dual-loop architectures. |

### 4. Open Questions for Future Iterations
1. *Sub-linear Verification:* Can verification techniques (e.g., formal methods, statistical sampling, lightweight surrogate verifiers) reduce the 74.8–93.6% verification tax without compromising admission safety?
2. *Asynchronous RSI Convergence:* How do asynchronous control-plane RSI loops (like ForgeSystem) scale over extended time horizons when task distributions drift?
---