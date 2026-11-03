# SpiralAI

## AI designs. Physics verifies.

A physics-verified scientific design agent exploring graphene mechanical energy storage with Meta Muse Spark Open.

**47/47 automated tests passing | Live Muse agent | Independent physics verification | Minimum-strain optimization | Provenance-tracked benchmarks | Resilient Agent Console**

SpiralAI explores a fundamental question for scientific AI:

> **Can an AI agent generate useful scientific designs without being allowed to invent the physics that validates them?**

SpiralAI separates creative AI reasoning from deterministic numerical calculation and independent scientific verification.

```text
AI DESIGN
    |
    v
DETERMINISTIC PHYSICS
    |
    v
INDEPENDENT VERIFICATION
    |
    v
VERIFIED FEEDBACK
    |
    v
REDESIGN OR STOP
```

> **Muse designs. Physics calculates. The verifier decides.**

## Why SpiralAI?

Generative AI can produce scientifically plausible ideas, but plausible reasoning is not the same as physical validity.

SpiralAI gives an AI agent freedom to explore while keeping numerical scientific claims under the control of deterministic physics and an independent verifier.

The system can:

- propose candidate designs with Meta Muse Spark Open;
- evaluate candidates using deterministic physics;
- independently verify numerical provenance;
- learn from verified results;
- redesign unsuccessful candidates;
- optimize for minimum required strain;
- detect repeated or invalid proposals;
- reject unsupported numerical claims;
- refuse false experimental-validation claims;
- escalate candidates beyond the supported screening boundary;
- preserve complete run provenance;
- replay real recorded trajectories if the live API is unavailable;
- stop honestly when the available physics cannot justify a target.

## Agent Console

SpiralAI includes an interactive scientific-design console built with Streamlit.

The interface visualizes:

```text
PLAN -> ACT -> PHYSICS -> VERIFY -> REDESIGN
```

The console supports three execution modes.

### Live Muse

Runs the official hackathon model:

```text
meta-models/muse-spark-open-1026
```

Muse proposes candidate designs while all numerical physics is calculated independently.

### Deterministic Optimization

Searches for the lowest verified strain satisfying a requested system-level energy target.

### Provenance Replay

Loads a previously recorded real Muse trajectory from JSONL provenance records.

This mode requires no live API call and provides a resilient demonstration fallback. If the live model endpoint becomes unavailable, SpiralAI can fall back to a provenance-backed run rather than generating synthetic replacement evidence.

## Working Muse Agent Demonstration

For a theoretical system-level target of:

```text
50 Wh/kg
```

one recorded Muse trajectory produced:

| Iteration | Muse proposal | Verified physics | Independent verification |
|---:|---:|---:|---|
| 1 | 5.0% strain | 26.07 Wh/kg | `TARGET_NOT_REACHED` |
| 2 | 7.0% strain | 49.61 Wh/kg | `TARGET_NOT_REACHED` |
| 3 | 7.1% strain | 50.96 Wh/kg | `TARGET_REACHED` |

Muse did **not** calculate these energy values. The deterministic Python physics engine calculated them, and the independent verifier evaluated whether the results supported the target.

Scientific classification:

```text
THEORETICAL_SIMULATION
```

Experimental validation:

```text
NO
```

## Minimum-Strain Optimization

Reaching a target is not sufficient if a much lower-strain solution exists.

SpiralAI therefore includes a deterministic minimum-strain optimizer.

Objective:

```text
minimize strain
```

subject to:

```text
verified system specific energy >= requested target
```

within:

```text
0% <= strain <= 10%
```

For a theoretical target of `50 Wh/kg`, the optimizer converged to:

| Metric | Result |
|---|---:|
| Minimum verified strain | **7.0312%** |
| Verified system specific energy | **50.0331 Wh/kg** |
| Optimization iterations | **10** |
| Evidence classification | `THEORETICAL_SIMULATION` |
| Experimental validation | **NO** |

The optimization is deterministic. Muse does not calculate the optimized numerical result.

If a target cannot be reached within the current analytical screening boundary, SpiralAI returns:

```text
TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY
```

instead of fabricating a solution.

## When Physics Says No

For a theoretical target of `100 Wh/kg`, a real Muse run demonstrated the scientific boundary:

```text
10.00% strain
      |
      v
96.71 Wh/kg
      |
      v
TARGET_NOT_REACHED
```

Muse then proposed a candidate slightly beyond the current conservative screening boundary. Although the theoretical calculation exceeded the target, the verifier did not certify it and returned:

```text
MORE_VALIDATION_REQUIRED
```

Additional evidence may include:

- finite-element analysis;
- molecular dynamics;
- fatigue modelling;
- fabrication;
- mechanical cycling;
- experimental measurement.

> **SpiralAI does not change the physics until the answer becomes yes.**

## Deterministic Benchmark

SpiralAI was evaluated across six fixed theoretical energy targets.

| Target | Minimum verified strain | Verified result |
|---:|---:|---:|
| 10 Wh/kg | **3.0566%** | 10.0173 Wh/kg |
| 25 Wh/kg | **4.9023%** | 25.0962 Wh/kg |
| 50 Wh/kg | **7.0312%** | 50.0331 Wh/kg |
| 100 Wh/kg | N/A | `TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY` |
| 250 Wh/kg | N/A | `TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY` |
| 1000 Wh/kg | N/A | `TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY` |

Summary:

```text
Targets evaluated:       6
Reachable:               3
Unreachable:             3
Provenance records:      6/6
Experimental claims:     0
```

Targets are not forced to succeed. An unreachable target is treated as a valid scientific result.

## Live Muse Reliability Benchmark

SpiralAI was evaluated using **9 live Muse Spark Open-1026 trajectories**.

```text
25 Wh/kg  x 3 runs
50 Wh/kg  x 3 runs
100 Wh/kg x 3 runs

Total: 9 live Muse trajectories
```

Observed baseline:

| Metric | Result |
|---|---:|
| Valid model outputs | **9/9, 100%** |
| Correct stopping states | **9/9, 100%** |
| Physics provenance coverage | **9/9, 100%** |
| Invalid model outputs | **0/9** |
| Repeated proposals | **0/9** |
| Unsupported experimental claims | **0/9** |
| Verifier escalations | **2/9** |
| Average agent iterations | **2.11** |

This is a small hackathon benchmark, not a claim of general statistical reliability. Its purpose is to establish a reproducible baseline rather than rely on a single hand-picked successful demonstration.

## Provenance

Scientific-design runs can be stored as append-only JSONL records.

Each record can preserve:

```text
schema version
run ID
UTC timestamp
model
objective
target
iteration history
physics outputs
verification states
final status
minimum verified strain
verified energy
evidence classification
experimental-validation status
metadata
scientific disclaimer
```

Provenance enables auditability, benchmark analysis, trajectory inspection, reproducibility, API-failure replay, and separation of AI reasoning from verified numerical evidence.

## Architecture

```text
SCIENTIFIC TARGET
        |
        v
META MUSE SPARK OPEN-1026
        |
        | proposes
        v
CANDIDATE DESIGN
        |
        v
DETERMINISTIC PHYSICS ENGINE
        |
        | calculates
        v
INDEPENDENT SCIENTIFIC VERIFIER
        |
        +--> TARGET_REACHED
        +--> TARGET_NOT_REACHED
        +--> MORE_VALIDATION_REQUIRED
        +--> PHYSICAL_CONSTRAINT_VIOLATION
        +--> INVALID_RESULT
        |
        v
VERIFIED FEEDBACK + PROVENANCE
        |
        v
REDESIGN OR STOP
```

The AI cannot modify the physics equations or verification rules merely to make a candidate pass.

## Meta AI Integration

SpiralAI uses the official Meta Global AI Developer Hackathon model:

```text
meta-models/muse-spark-open-1026
```

served through Baseten.

Muse performs scientific-design reasoning, candidate generation, interpretation of verified history, adaptation after failed candidates, and design-strategy decisions.

Muse does **not** provide the authoritative numerical physics result. That responsibility belongs to deterministic Python tools.

## Independent Scientific Verification

SpiralAI does not trust a numerical result simply because an AI produced it.

The verifier checks that:

- numerical performance originated from the physics engine;
- required scientific evidence fields exist;
- candidate parameters remain inside supported model limits;
- requested targets were actually achieved;
- theoretical results are not represented as experimental results;
- unsupported numerical claims are rejected;
- higher-fidelity validation is requested when necessary.

Explicit states include:

```text
TARGET_REACHED
TARGET_NOT_REACHED
MORE_VALIDATION_REQUIRED
INVALID_RESULT
INVALID_MODEL_OUTPUT
NO_IMPROVEMENT
MAX_ITERATIONS_REACHED
MINIMUM_STRAIN_FOUND
TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY
```

## Automated Tests

Current verified test status:

```text
47 passed
```

The automated suite covers graphene physics, AI-facing physics tools, verifier behavior, minimum-strain optimization, controller stopping states, invalid model output, repeated candidates, JSONL provenance, benchmark configuration, benchmark scoring, and scientific-claim safeguards.

Run:

```bash
python -m pytest -q
```

## Repository Structure

```text
spiralai/
|
|-- agent/
|   |-- muse_agent.py
|   |-- iterative_agent.py
|   |-- tools.py
|
|-- physics/
|   |-- graphene.py
|
|-- optimization/
|   |-- minimum_strain.py
|
|-- verification/
|   |-- verifier.py
|
|-- provenance/
|   |-- run_log.py
|
|-- benchmarks/
|   |-- run_minimum_strain_benchmark.py
|   |-- run_muse_trajectory_benchmark.py
|
|-- results/
|   |-- minimum_strain_benchmark.jsonl
|   |-- muse_trajectory_benchmark.jsonl
|
|-- ui/
|   |-- app.py
|
|-- tests/
|   |-- test_graphene.py
|   |-- test_tools.py
|   |-- test_verifier.py
|   |-- test_minimum_strain.py
|   |-- test_iterative_agent.py
|   |-- test_provenance.py
|   |-- test_benchmark.py
|   |-- test_muse_benchmark.py
|
|-- README.md
|-- .gitignore
```

## Run SpiralAI

### Requirements

- Python 3.10+
- OpenAI-compatible Python SDK
- Streamlit
- pytest
- Baseten API key for Live Muse mode

Install:

```bash
python -m pip install -r requirements.txt
```

Configure `BASETEN_API_KEY` as an environment variable. Never commit API keys to GitHub.

### Launch the Agent Console

```bash
python -m streamlit run ui/app.py
```

Available modes:

```text
Live Muse
Deterministic optimization
Provenance replay
```

### Run the iterative agent

```bash
python -m agent.iterative_agent
```

### Run minimum-strain optimization

```bash
python -m optimization.minimum_strain
```

### Run the deterministic benchmark

```bash
python -m benchmarks.run_minimum_strain_benchmark
```

### Run the Muse trajectory benchmark

This calls the live model and may consume inference credits.

```bash
python -m benchmarks.run_muse_trajectory_benchmark
```

Benchmark output uses append-only JSONL provenance. Re-running the canonical benchmark appends additional records.

## Scientific Status

Every current SpiralAI result is classified as:

```text
THEORETICAL_SIMULATION
```

Experimental validation:

```text
NO
```

The current validation pathway is:

```text
Analytical Physics
        |
        v
Numerical Screening
        |
        v
AI-Guided Design
        |
        v
Deterministic Optimization
        |
        v
FEA / Molecular Dynamics
        |
        v
Fatigue Modelling
        |
        v
Fabrication
        |
        v
Mechanical Cycling
        |
        v
Experimental Validation
```

SpiralAI currently operates in the analytical, numerical-screening, and AI-guided-design/optimization stages.

## Scientific Limitations

Current results are not:

- experimental measurements;
- fabricated-device performance;
- demonstrated cycle-life performance;
- demonstrated fatigue resistance;
- demonstrated manufacturability;
- experimentally validated system-level energy density;
- evidence that graphene mechanical energy storage replaces lithium-ion batteries.

Real devices introduce additional effects including defects, fatigue, anchors, actuators, mechanical coupling, conversion losses, electronics, packaging, environmental effects, and fabrication tolerances.

These require progressively higher-fidelity modelling and experimental validation.

## Prior Work Disclosure

SpiralAI is inspired by the author's **unpublished theoretical research conducted before the hackathon** into graphene mechanical energy-storage structures.

The unpublished manuscript and its specific clock-spiral derivations are **not included in this public repository**.

Earlier exploratory calculations conducted before the hackathon are not presented as hackathon contributions.

The public hackathon implementation includes:

- Meta Muse Spark Open integration;
- deterministic public physics tools;
- independent scientific verification;
- iterative AI design workflow;
- minimum-strain optimization;
- controller reliability logic;
- provenance infrastructure;
- deterministic benchmarking;
- live Muse benchmarking;
- API-resilient provenance replay;
- interactive Agent Console;
- automated tests;
- public software architecture.

The separation between prior theoretical research and hackathon development is intentional.

## Meta Global AI Developer Hackathon 2026

**Track:** Indie Developer
**Theme:** Push the Frontier

SpiralAI combines:

```text
AI agents
+
materials science
+
graphene
+
mechanical energy storage
+
verifiable scientific computing
```

The project asks:

> **Can AI generate a promising scientific design?**

But more importantly:

> **Can AI recognize when the available physics says no?**

## Next Scientific Stages

Future scientific development may include richer geometry-aware design tools, finite-element modelling, molecular-dynamics integration, fatigue and cyclic-loading models, multi-objective optimization, larger agent benchmarks, fabrication planning, mechanical cycling, and experimental validation.

These are future stages, not demonstrated capabilities of the current public build.

## Core Principle

> ## AI designs. Physics verifies.

And when the available evidence is not sufficient:

> ## SpiralAI says so.
