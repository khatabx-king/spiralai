# SpiralAI

## AI designs. Physics verifies.

A physics-verified scientific design agent exploring graphene mechanical energy storage with Meta Muse Spark Open.

29/29 automated tests passing | Minimum-strain optimization | Independent scientific verification | Iterative autonomous design | Official Meta hackathon model

SpiralAI explores an ambitious scientific question:

Can an AI agent help discover physically plausible graphene mechanical energy-storage concepts without being allowed to invent the physics?

Instead of asking a language model to predict scientific performance directly, SpiralAI separates:

AI design reasoning -> deterministic physics -> independent verification -> redesign

The AI is allowed to design, but it is not allowed to grade its own homework.

## Why SpiralAI?

Generative AI can produce scientifically plausible ideas.

But plausible reasoning is not the same as physical validity.

SpiralAI gives the AI freedom to explore while keeping numerical scientific claims under the control of deterministic physics and an independent verifier.

SpiralAI can:

- propose candidate designs
- evaluate candidates with deterministic physics tools
- learn from verified results
- revise unsuccessful candidates
- minimize strain for a requested energy target
- reject unsupported numerical claims
- request additional validation when the current model is insufficient
- stop honestly when a target cannot be supported

Muse designs. Physics calculates. The verifier decides.

## Working Agent Demonstration

SpiralAI runs an iterative design, physics, verification, and redesign loop.

In one verified run, the target was:

50 Wh/kg system-level specific energy

The agent produced:

| Iteration | Muse proposal | Verified physics result | Independent verification |
|---|---:|---:|---|
| 1 | 5.0% strain | 26.07 Wh/kg | TARGET_NOT_REACHED |
| 2 | 7.0% strain | 49.61 Wh/kg | TARGET_NOT_REACHED |
| 3 | 7.1% strain | 50.96 Wh/kg | TARGET_REACHED |

The language model did not generate the energy-density values.

The deterministic Python physics engine calculated them, and the independent verifier determined whether the evidence supported the requested target.

Agent behavior can vary between runs.

Scientific status:

THEORETICAL_SIMULATION

Experimental validation:

NO

These values are screening estimates, not experimentally demonstrated graphene-device performance.

## Minimum-Strain Optimization

Simply reaching an energy target is not enough.

SpiralAI now searches for the lowest verified strain that satisfies the requested energy target within the current analytical screening boundary.

Objective:

minimize strain

subject to:

verified system specific energy >= requested target

and:

0% <= strain <= 10%

For a theoretical target of 50 Wh/kg, the deterministic minimum-strain optimizer found:

| Metric | Verified result |
|---|---:|
| Minimum verified strain | 7.0312% |
| Verified system specific energy | 50.0331 Wh/kg |
| Optimization iterations | 10 |
| Evidence class | THEORETICAL_SIMULATION |
| Experimental validation | NO |

The optimizer uses deterministic physics and independent verification.

Muse does not calculate the minimum-strain solution.

If a requested target cannot be reached within the current screening boundary, SpiralAI returns:

TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY

rather than inventing a solution.

## Verified Build

Current verified implementation:

- 29/29 automated tests passing
- Official hackathon model: meta-models/muse-spark-open-1026
- Deterministic graphene physics engine
- AI-facing physics-tool interface
- Independent scientific verification layer
- Iterative AI -> physics -> verification -> redesign workflow
- Deterministic minimum-strain optimization
- Unsupported AI-generated numerical results rejected
- False experimental-validation claims rejected
- Missing physics evidence rejected
- Repeated candidates detected
- Maximum iteration limits enforced
- Invalid model output handled
- Higher-risk candidates can trigger MORE_VALIDATION_REQUIRED
- Unrealistic targets can be rejected honestly
- Public Git history documents hackathon development

Current automated test result:

29 passed

## How SpiralAI Works

SpiralAI deliberately separates AI reasoning from scientific calculation and verification.

1. Muse Spark Open-1026 proposes a candidate design.
2. The deterministic Python physics engine calculates performance.
3. The independent verifier checks the result and model limits.
4. Verified feedback is returned to Muse.
5. Muse proposes a revised candidate.
6. The process repeats until a justified stopping state is reached.

```Architecture:

Scientific Target
    |
    v
Muse Spark Open-1026
    |
    v
Candidate Design
    |
    v
Deterministic Physics Engine
    |
    v
Independent Scientific Verifier
    |
    +-- TARGET_REACHED
    +-- TARGET_NOT_REACHED
    +-- MORE_VALIDATION_REQUIRED
    +-- PHYSICAL_CONSTRAINT_VIOLATION
    +-- INVALID_RESULT
    |
    v
Verified Feedback
    |
    v
Redesign or Stop
```

### Independent Scientific Verification

SpiralAI does not trust a numerical result simply because an AI generated it.

The verifier checks that:

- numerical performance came from the verified physics engine
- required evidence fields are present
- design inputs remain inside the supported screening range
- the requested target was actually achieved
- theoretical results are not represented as experimental results
- unsupported numerical claims are rejected
- higher-fidelity validation is requested when the screening model is insufficient

A candidate outside the current conservative analytical screening boundary can return:

MORE_VALIDATION_REQUIRED

rather than being automatically accepted.

A numerical result that did not originate from the verified physics engine can return:

INVALID_RESULT

## Agent Reliability

The iterative controller is tested against both successful and unsuccessful behavior.

Current controller states include:

- TARGET_REACHED
- TARGET_NOT_REACHED
- NO_IMPROVEMENT
- MORE_VALIDATION_REQUIRED
- INVALID_MODEL_OUTPUT
- MAX_ITERATIONS_REACHED

Minimum-strain optimization can additionally return:

- MINIMUM_STRAIN_FOUND
- TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY

An unsuccessful design trajectory is still a valid scientific result.

SpiralAI does not force every research question to end with success.

## Evidence Classification

All current SpiralAI numerical results are classified as:

THEORETICAL_SIMULATION

Current experimental-validation status:

NO

The intended validation pathway is:

```Analytical physics
-> numerical screening
-> AI-guided optimization
-> finite-element / molecular-dynamics validation
-> fabrication
-> mechanical cycling
-> experimental validation
```
SpiralAI currently operates in the analytical, numerical-screening, and AI-guided-optimization stages.

## Scientific Limitations

Current SpiralAI results are theoretical and simulated screening results.

They are not:

- experimental measurements
- fabricated-device performance
- demonstrated cycle-life results
- demonstrated fatigue resistance
- demonstrated manufacturability
- experimentally validated system-level energy density
- proof that graphene mechanical storage can replace lithium-ion batteries

Real devices would introduce additional effects including:

- graphene defects
- fatigue
- anchor mechanics
- actuators
- mechanical coupling
- energy-conversion losses
- control electronics
- packaging mass
- environmental effects
- fabrication tolerances

These effects require progressively higher-fidelity modelling and experimental study.

## Prior Work Disclosure

SpiralAI is inspired by the author's unpublished theoretical research conducted before the hackathon into graphene mechanical energy-storage structures.

The unpublished manuscript and its specific clock-spiral derivations are not included in this public repository.

Earlier exploratory calculations performed before the hackathon are also not presented as hackathon contributions.

The public hackathon implementation includes:

- Meta Muse Spark Open integration
- deterministic public physics tools
- AI-facing physics-tool interface
- independent scientific verifier
- iterative agent workflow
- controller reliability testing
- deterministic minimum-strain optimization
- automated tests
- public software architecture

The separation between prior theoretical research and hackathon development is intentional.

## Repository Structure

```spiralai/
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
|-- tests/
|   |-- test_graphene.py
|   |-- test_tools.py
|   |-- test_verifier.py
|   |-- test_minimum_strain.py
|   |-- test_iterative_agent.py
|
|-- README.md
|-- .gitignore
```
## Run SpiralAI

Requirements:

- Python 3.9 or newer
- OpenAI-compatible Python SDK
- Baseten API key with access to the official hackathon Muse Spark Open model

Install dependencies:

python -m pip install openai pytest

Set BASETEN_API_KEY as an environment variable.

Never place an API key directly into source code or commit an API key to GitHub.

Run the iterative agent:

python -m agent.iterative_agent

Run deterministic minimum-strain optimization:

python -m optimization.minimum_strain

Run all tests:

python -m pytest -v

Current verified result:

29 passed

## Next Milestones

The next development priorities are:

1. reproducible JSONL run logging and provenance
2. deterministic multi-run agent benchmarks
3. benchmark targets of 10, 25, 50, 100, 250, and 1000 Wh/kg
4. measurement of success rate and correct stopping-state rate
5. measurement of average agent iterations and unnecessary tool calls
6. measurement of invalid-output and verifier-escalation rates
7. interactive SpiralAI Agent Console
8. visualization of PLAN -> ACT -> PHYSICS -> VERIFY -> REDESIGN
9. API-failure demo fallback
10. higher-fidelity simulation interfaces
11. final three-minute hackathon demonstration

The goal is not merely to show one successful AI run.

The goal is to measure whether the scientific-design agent is reliable across many trajectories.

## Meta Global AI Developer Hackathon 2026

Track: Indie Developer

Theme: Push the Frontier

SpiralAI combines:
```
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

Can AI generate a promising scientific design?

More importantly:

Can AI recognize when the available physics says no?

## Core Principle

AI designs. Physics verifies.

When the available evidence is insufficient:

SpiralAI says so.
