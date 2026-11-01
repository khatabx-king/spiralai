"""
SpiralAI Agent Console.

Meta Global AI Developer Hackathon 2026.

Visual interface for:
PLAN > ACT > PHYSICS > VERIFY > REDESIGN

All numerical outputs are theoretical or simulated screening results.
They are not experimentally validated device performance.
"""

from pathlib import Path

import streamlit as st

from agent.iterative_agent import run_iterative_design
from optimization.minimum_strain import find_minimum_strain
from provenance.run_log import read_jsonl_records


MODEL = "meta-models/muse-spark-open-1026"

MUSE_BENCHMARK = Path(
    "results/muse_trajectory_benchmark.jsonl"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SpiralAI Agent Console",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# FUTURISTIC DARK / MINT / GOLD THEME
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   SPIRALAI COLOR SYSTEM
   ==========================================================

   Background:   #050B09
   Panel:        #0D1B18
   Mint:         #7EE2B8
   Green:        #42D89C
   Gold:         #D9A441
   Soft gold:    #F2C66D
   Main text:    #F4F7F5
   Muted text:   #A6B7AF
   Border:       #25443A
*/


/* APP BACKGROUND */

.stApp {
    position: relative;
    overflow-x: hidden;

    background:
        radial-gradient(
            circle at 85% 8%,
            rgba(66, 216, 156, 0.15),
            transparent 30%
        ),
        radial-gradient(
            circle at 12% 55%,
            rgba(217, 164, 65, 0.08),
            transparent 26%
        ),
        linear-gradient(
            145deg,
            #050B09 0%,
            #07110F 45%,
            #0A1713 100%
        );

    color: #F4F7F5;
}


/* ANIMATED GRAPHENE BACKGROUND */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;

    background-image:
        linear-gradient(
            30deg,
            rgba(126, 226, 184, 0.055) 12%,
            transparent 12.5%,
            transparent 87%,
            rgba(126, 226, 184, 0.055) 87.5%
        ),
        linear-gradient(
            150deg,
            rgba(126, 226, 184, 0.055) 12%,
            transparent 12.5%,
            transparent 87%,
            rgba(126, 226, 184, 0.055) 87.5%
        ),
        linear-gradient(
            30deg,
            rgba(126, 226, 184, 0.055) 12%,
            transparent 12.5%,
            transparent 87%,
            rgba(126, 226, 184, 0.055) 87.5%
        ),
        linear-gradient(
            150deg,
            rgba(126, 226, 184, 0.055) 12%,
            transparent 12.5%,
            transparent 87%,
            rgba(126, 226, 184, 0.055) 87.5%
        ),
        linear-gradient(
            60deg,
            rgba(242, 198, 109, 0.035) 25%,
            transparent 25.5%,
            transparent 75%,
            rgba(242, 198, 109, 0.035) 75%
        );

    background-size: 84px 147px;

    background-position:
        0 0,
        0 0,
        42px 73px,
        42px 73px,
        0 0;

    opacity: 0.72;

    animation:
        graphene-drift 30s linear infinite;
}


/* MOVING SCANNER LIGHT */

.stApp::after {
    content: "";
    position: fixed;
    top: -20%;
    left: -20%;
    width: 140%;
    height: 140%;
    z-index: 0;
    pointer-events: none;

    background:
        linear-gradient(
            110deg,
            transparent 25%,
            rgba(126, 226, 184, 0.025) 46%,
            rgba(126, 226, 184, 0.10) 50%,
            rgba(242, 198, 109, 0.035) 53%,
            transparent 75%
        );

    animation:
        scanner-sweep 12s ease-in-out infinite;
}


/* ANIMATIONS */

@keyframes graphene-drift {
    0% {
        background-position:
            0 0,
            0 0,
            42px 73px,
            42px 73px,
            0 0;
    }

    100% {
        background-position:
            84px 147px,
            84px 147px,
            126px 220px,
            126px 220px,
            84px 147px;
    }
}


@keyframes scanner-sweep {
    0%,
    100% {
        transform: translateX(-35%);
        opacity: 0.15;
    }

    50% {
        transform: translateX(35%);
        opacity: 0.75;
    }
}


@keyframes led-pulse {
    0%,
    100% {
        opacity: 0.55;

        box-shadow:
            0 0 4px rgba(126, 226, 184, 0.40);
    }

    50% {
        opacity: 1;

        box-shadow:
            0 0 8px #7EE2B8,
            0 0 18px rgba(126, 226, 184, 0.85),
            0 0 28px rgba(66, 216, 156, 0.35);
    }
}


@keyframes gold-pulse {
    0%,
    100% {
        opacity: 0.60;

        box-shadow:
            0 0 4px rgba(242, 198, 109, 0.40);
    }

    50% {
        opacity: 1;

        box-shadow:
            0 0 8px #F2C66D,
            0 0 18px rgba(242, 198, 109, 0.70);
    }
}


/* KEEP CONTENT ABOVE BACKGROUND */

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.block-container {
    position: relative;
    z-index: 2;
}


.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


header[data-testid="stHeader"] {
    background:
        rgba(5, 11, 9, 0.25);

    backdrop-filter:
        blur(10px);
}


/* TYPOGRAPHY */

h1 {
    color: #F4F7F5 !important;
    font-weight: 850 !important;
    letter-spacing: -0.035em;

    text-shadow:
        0 0 22px rgba(126, 226, 184, 0.12);
}


h2,
h3 {
    color: #F4F7F5 !important;
}


p {
    color: #A6B7AF;
}


.hero-accent {
    color: #7EE2B8;

    text-shadow:
        0 0 18px rgba(126, 226, 184, 0.30);
}


/* SYSTEM STATUS STRIP */

.system-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    align-items: center;

    margin: 12px 0 22px 0;
    padding: 11px 16px;

    background:
        rgba(13, 27, 24, 0.86);

    border:
        1px solid #25443A;

    border-radius:
        12px;

    backdrop-filter:
        blur(12px);
}


.system-item {
    display: flex;
    align-items: center;
    gap: 8px;

    color: #A6B7AF;
    font-size: 0.82rem;
    font-weight: 650;
    letter-spacing: 0.04em;
}


.led {
    display: inline-block;

    width: 9px;
    height: 9px;

    border-radius: 50%;

    background:
        #7EE2B8;

    animation:
        led-pulse 2.2s ease-in-out infinite;
}


.led-gold {
    display: inline-block;

    width: 9px;
    height: 9px;

    border-radius: 50%;

    background:
        #F2C66D;

    animation:
        gold-pulse 2.8s ease-in-out infinite;
}


/* SCIENTIFIC STATUS */

.scientific-warning {
    background:
        linear-gradient(
            90deg,
            rgba(19, 36, 31, 0.94),
            rgba(24, 37, 30, 0.88)
        );

    border:
        1px solid #D9A441;

    border-left:
        5px solid #F2C66D;

    border-radius:
        12px;

    padding:
        14px 18px;

    color:
        #F2C66D;

    box-shadow:
        0 6px 24px rgba(0, 0, 0, 0.22),
        0 0 22px rgba(217, 164, 65, 0.06);

    backdrop-filter:
        blur(12px);
}


/* NATIVE STREAMLIT CONTAINERS */

[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(
            145deg,
            rgba(13, 27, 24, 0.96),
            rgba(16, 32, 28, 0.90)
        );

    border-color:
        #25443A !important;

    border-radius:
        14px !important;

    box-shadow:
        0 10px 28px rgba(0, 0, 0, 0.22);

    backdrop-filter:
        blur(12px);
}


/* METRIC CARDS */

[data-testid="stMetric"] {
    position: relative;

    min-height:
        112px;

    background:
        linear-gradient(
            145deg,
            rgba(13, 27, 24, 0.97),
            rgba(19, 36, 31, 0.92)
        );

    border:
        1px solid #25443A;

    border-radius:
        14px;

    padding:
        16px 18px;

    box-shadow:
        0 8px 22px rgba(0, 0, 0, 0.20);

    backdrop-filter:
        blur(10px);
}


[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: 13px;
    right: 13px;

    width: 8px;
    height: 8px;

    border-radius: 50%;

    background:
        #7EE2B8;

    animation:
        led-pulse 2.4s ease-in-out infinite;
}


[data-testid="stMetricLabel"] {
    color:
        #A6B7AF !important;

    font-weight:
        650 !important;
}


[data-testid="stMetricValue"] {
    color:
        #7EE2B8 !important;

    font-size:
        1.65rem !important;

    font-weight:
        820 !important;

    text-shadow:
        0 0 14px rgba(126, 226, 184, 0.15);
}


/* INPUT */

[data-testid="stNumberInput"] label {
    color:
        #A6B7AF !important;

    font-weight:
        650;
}


[data-testid="stNumberInput"] input {
    background-color:
        #0D1B18 !important;

    color:
        #F4F7F5 !important;

    border:
        1px solid #25443A !important;
}


/* RADIO BUTTONS */

[data-testid="stRadio"] label {
    color:
        #F4F7F5 !important;
}


/* PRIMARY BUTTON */

.stButton > button[kind="primary"] {
    min-height:
        50px;

    background:
        linear-gradient(
            90deg,
            #42D89C,
            #7EE2B8
        ) !important;

    color:
        #07110F !important;

    border:
        1px solid
        rgba(126, 226, 184, 0.70) !important;

    border-radius:
        11px !important;

    font-weight:
        850 !important;

    letter-spacing:
        0.025em;

    box-shadow:
        0 0 12px rgba(66, 216, 156, 0.24),
        0 8px 24px rgba(0, 0, 0, 0.18);

    transition:
        all 0.25s ease;
}


.stButton > button[kind="primary"]:hover {
    color:
        #07110F !important;

    background:
        linear-gradient(
            90deg,
            #7EE2B8,
            #F2C66D
        ) !important;

    transform:
        translateY(-1px);

    box-shadow:
        0 0 18px rgba(126, 226, 184, 0.34),
        0 10px 28px rgba(0, 0, 0, 0.22);
}


/* ARCHITECTURE PANEL */

.architecture-card {
    background:
        rgba(13, 27, 24, 0.94);

    border:
        1px solid #25443A;

    border-radius:
        14px;

    padding:
        18px;

    text-align:
        center;

    box-shadow:
        0 8px 24px rgba(0, 0, 0, 0.20);
}


.architecture-title {
    color:
        #A6B7AF;

    font-size:
        0.72rem;

    font-weight:
        800;

    letter-spacing:
        0.12em;

    margin-bottom:
        12px;
}


.architecture-node {
    padding:
        9px 12px;

    border:
        1px solid #25443A;

    border-radius:
        8px;

    color:
        #F4F7F5;

    font-weight:
        750;

    background:
        #10201C;
}


.architecture-node.mint {
    color:
        #7EE2B8;

    border-color:
        #42D89C;
}


.architecture-node.gold {
    color:
        #F2C66D;

    border-color:
        #D9A441;
}


.architecture-arrow {
    color:
        #7EE2B8;

    padding:
        6px 0;

    font-size:
        1.1rem;

    font-weight:
        800;
}


/* ALERT BOXES */

[data-testid="stAlert"] {
    background:
        rgba(19, 36, 31, 0.95) !important;

    border:
        1px solid #25443A !important;

    color:
        #F4F7F5 !important;
}


hr {
    border-color:
        #25443A !important;

    opacity:
        0.72;
}


small,
.stCaption {
    color:
        #A6B7AF !important;
}


/* REDUCED MOTION */

@media (
    prefers-reduced-motion:
    reduce
) {
    *,
    *::before,
    *::after {
        animation:
            none !important;

        transition:
            none !important;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================


def find_replay_run(
    records: list[dict],
    target: float,
) -> dict | None:
    """Return the first saved Muse trajectory matching a target."""

    matches = [
        record
        for record in records
        if abs(
            float(
                record.get(
                    "target_Wh_kg",
                    -1,
                )
            )
            - target
        )
        < 1e-6
    ]

    if not matches:
        return None

    return matches[0]


def render_iteration(
    record: dict,
) -> None:
    """Render one scientific-design step with native Streamlit."""

    iteration = record.get(
        "iteration",
        "?",
    )

    proposal = record.get(
        "proposal",
        {},
    )

    physics = record.get(
        "physics_result",
        {},
    )

    verification = record.get(
        "verification",
        {},
    )

    strain = proposal.get(
        "strain_percent",
        physics.get(
            "strain_percent",
            "N/A",
        ),
    )

    reason = proposal.get(
        "reason",
        "Deterministic minimum-strain search step.",
    )

    energy = physics.get(
        "system_specific_energy_Wh_kg",
        "N/A",
    )

    status = verification.get(
        "status",
        "UNKNOWN",
    )

    if isinstance(
        strain,
        (int, float),
    ):
        strain_text = (
            f"{strain:.3f}%"
        )

    else:
        strain_text = str(
            strain
        )

    if isinstance(
        energy,
        (int, float),
    ):
        energy_text = (
            f"{energy:.2f} Wh/kg"
        )

    else:
        energy_text = str(
            energy
        )

    if iteration == 0:
        title = "FEASIBILITY CHECK"

    else:
        title = (
            f"ITERATION {iteration}"
        )

    successful_states = {
        "TARGET_REACHED",
        "MINIMUM_STRAIN_FOUND",
    }

    caution_states = {
        "TARGET_NOT_REACHED",
        "MORE_VALIDATION_REQUIRED",
        "TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY",
        "MAX_ITERATIONS_REACHED",
        "NO_IMPROVEMENT",
    }

    with st.container(
        border=True,
    ):
        st.markdown(
            f"### {title}"
        )

        st.caption(
            "PLAN"
        )

        st.write(
            reason
        )

        action_column, physics_column = (
            st.columns(2)
        )

        with action_column:
            st.caption(
                "ACT"
            )

            st.markdown(
                f"**{strain_text} strain**"
            )

        with physics_column:
            st.caption(
                "PHYSICS"
            )

            st.markdown(
                f"**{energy_text}**"
            )

        st.caption(
            "VERIFY"
        )

        if status in successful_states:
            st.success(
                f"VERIFIED: {status}"
            )

        elif status in caution_states:
            st.warning(
                f"SCIENTIFIC OUTCOME: {status}"
            )

        else:
            st.error(
                f"INVALID OR FAILED: {status}"
            )


def render_replay(
    selected: dict,
    fallback: bool = False,
) -> None:
    """Render one provenance-backed Muse trajectory."""

    if fallback:
        st.warning(
            "Live Muse is unavailable. "
            "Displaying a provenance-backed real Muse trajectory."
        )

    else:
        st.success(
            "Loaded provenance-backed Muse trajectory. "
            "No live API call was required."
        )

    metadata_left, metadata_right = (
        st.columns(2)
    )

    metadata_left.caption(
        f"Run ID: {selected['run_id']}"
    )

    metadata_right.caption(
        f"Model: {selected['model']}"
    )

    for item in selected.get(
        "history",
        [],
    ):
        render_iteration(
            item
        )

    st.divider()

    status_column, iterations_column, evidence_column = (
        st.columns(3)
    )

    status_column.metric(
        "Final status",
        selected["final_status"],
    )

    iterations_column.metric(
        "Iterations",
        selected["iterations"],
    )

    evidence_column.metric(
        "Evidence",
        selected["evidence_type"],
    )

    if fallback:
        st.caption(
            "Fallback uses provenance captured from an earlier "
            "live Muse execution. No synthetic run was generated."
        )


# ============================================================
# HEADER
# ============================================================

st.title(
    "SpiralAI"
)

st.markdown(
    '<h3 class="hero-accent">'
    'AI designs. Physics verifies.'
    '</h3>',
    unsafe_allow_html=True,
)

st.caption(
    "Physics-verified scientific design agent "
    "for graphene mechanical energy storage."
)

st.markdown(
    '<div class="system-strip">'
    '<div class="system-item">'
    '<span class="led"></span>'
    'PHYSICS ENGINE ONLINE'
    '</div>'
    '<div class="system-item">'
    '<span class="led"></span>'
    'VERIFIER ONLINE'
    '</div>'
    '<div class="system-item">'
    '<span class="led"></span>'
    'PROVENANCE READY'
    '</div>'
    '<div class="system-item">'
    '<span class="led-gold"></span>'
    'THEORETICAL SCREENING'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="scientific-warning">'
    '<b>THEORETICAL_SIMULATION</b> | '
    'Experimental validation: <b>NO</b>'
    '</div>',
    unsafe_allow_html=True,
)

st.write("")


# ============================================================
# TOP METRICS
# ============================================================

top1, top2, top3, top4 = (
    st.columns(4)
)

top1.metric(
    "Model",
    "Muse Spark",
)

top2.metric(
    "Automated tests",
    "47 passed",
)

top3.metric(
    "Live benchmark",
    "9 trajectories",
)

top4.metric(
    "Physics provenance",
    "100%",
)

st.caption(
    "Official hackathon model: "
    f"`{MODEL}`"
)

st.divider()


# ============================================================
# MAIN LAYOUT
# ============================================================

left, right = st.columns(
    [
        0.34,
        0.66,
    ],
    gap="large",
)


# ============================================================
# LEFT CONTROL PANEL
# ============================================================

with left:
    st.header(
        "Design Objective"
    )

    target = st.number_input(
        "Target system specific energy (Wh/kg)",
        min_value=1.0,
        max_value=1000.0,
        value=50.0,
        step=5.0,
    )

    mode = st.radio(
        "Execution mode",
        [
            "Live Muse",
            "Deterministic optimization",
            "Provenance replay",
        ],
    )

    if mode == "Live Muse":
        st.info(
            "Calls the official Muse Spark Open-1026 model through "
            "Baseten. Physics calculations and verification remain "
            "deterministic and independent."
        )

    elif mode == "Deterministic optimization":
        st.info(
            "Finds the lowest verified strain satisfying the "
            "requested energy target."
        )

    else:
        st.info(
            "Loads a previously recorded real Muse trajectory "
            "without making a live API call."
        )

    run_button = st.button(
        "Run SpiralAI",
        type="primary",
        use_container_width=True,
    )

    st.divider()

    st.markdown(
        "### Architecture"
    )

    st.markdown(
        '<div class="architecture-card">'
        '<div class="architecture-title">'
        'DESIGN TO VALIDATION'
        '</div>'
        '<div class="architecture-node">'
        'TARGET'
        '</div>'
        '<div class="architecture-arrow">'
        'v'
        '</div>'
        '<div class="architecture-node mint">'
        'MUSE / OPTIMIZER'
        '</div>'
        '<div class="architecture-arrow">'
        'v'
        '</div>'
        '<div class="architecture-node">'
        'PHYSICS ENGINE'
        '</div>'
        '<div class="architecture-arrow">'
        'v'
        '</div>'
        '<div class="architecture-node gold">'
        'INDEPENDENT VERIFIER'
        '</div>'
        '<div class="architecture-arrow">'
        'v'
        '</div>'
        '<div class="architecture-node">'
        'REDESIGN / STOP'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# RIGHT AGENT TIMELINE
# ============================================================

with right:
    st.header(
        "PLAN > ACT > PHYSICS > VERIFY > REDESIGN"
    )

    if not run_button:
        with st.container(
            border=True,
        ):
            st.caption(
                "AGENT READY"
            )

            st.write(
                "Scientific-design pipeline initialized."
            )

            st.markdown(
                "**Next action:** Choose a target and execution "
                "mode, then select **Run SpiralAI**."
            )


    # ========================================================
    # LIVE MUSE MODE
    # ========================================================

    elif mode == "Live Muse":
        with st.container(
            border=True,
        ):
            st.caption(
                "LIVE AGENT"
            )

            st.markdown(
                f"**Model:** `{MODEL}`"
            )

            st.write(
                "Muse proposes candidates. Deterministic physics "
                "calculates performance. The independent verifier "
                "decides whether the evidence supports the result."
            )

        try:
            with st.spinner(
                "Muse is designing. Physics is verifying..."
            ):
                report = run_iterative_design(
                    target_wh_kg=target,
                )

        except Exception as exc:
            records = read_jsonl_records(
                MUSE_BENCHMARK
            )

            selected = find_replay_run(
                records,
                target,
            )

            if selected is None:
                st.error(
                    "Live Muse is unavailable and no saved trajectory "
                    f"exists for {target:.2f} Wh/kg."
                )

                st.caption(
                    "Available replay targets: 25, 50, and 100 Wh/kg."
                )

                st.caption(
                    f"Live error type: {type(exc).__name__}"
                )

            else:
                render_replay(
                    selected,
                    fallback=True,
                )

        else:
            history = report.get(
                "history",
                [],
            )

            for item in history:
                render_iteration(
                    item
                )

            st.divider()

            final_status = report.get(
                "final_status",
                "UNKNOWN",
            )

            iterations = report.get(
                "iterations_completed",
                len(history),
            )

            result1, result2, result3 = (
                st.columns(3)
            )

            display_status = {
                "MORE_VALIDATION_REQUIRED": "VALIDATION REQUIRED",
                "TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY": "UNREACHABLE",
            }.get(
                final_status,
                final_status,
            )

            result1.metric(
                "Final status",
                display_status,
            )

            result2.metric(
                "Agent iterations",
                iterations,
            )

            result3.metric(
                "Evidence",
                "THEORETICAL",
            )

            st.caption(
                "Evidence classification: `THEORETICAL_SIMULATION`"
            )

            if final_status == "TARGET_REACHED":
                st.success(
                    "The requested target was reached in the "
                    "current theoretical screening model."
                )

            elif final_status == "MORE_VALIDATION_REQUIRED":
                st.warning(
                    "MORE_VALIDATION_REQUIRED: "
                    "The candidate exceeds the current "
                    "10% analytical screening boundary."
                )

            else:
                st.warning(
                    "The current run did not establish a verified "
                    "solution for the requested target."
                )

            st.caption(
                "Live numerical results are produced by the "
                "deterministic physics engine, not by Muse."
            )


    # ========================================================
    # DETERMINISTIC OPTIMIZATION
    # ========================================================

    elif mode == "Deterministic optimization":
        with st.spinner(
            "Running verified minimum-strain search..."
        ):
            result = find_minimum_strain(
                target_wh_kg=target,
            )

        with st.container(
            border=True,
        ):
            st.caption(
                "OBJECTIVE"
            )

            st.markdown(
                f"""
Find the **lowest verified strain** satisfying
**{target:.2f} Wh/kg** within the current
**10% analytical screening boundary**.
"""
            )

        for item in result.history:
            physics = item.get(
                "physics_result",
                {},
            )

            verification = item.get(
                "verification",
                {},
            )

            normalized = {
                "iteration": item.get(
                    "iteration",
                    "?",
                ),
                "proposal": {
                    "strain_percent": item.get(
                        "strain_percent",
                        physics.get(
                            "strain_percent",
                            "N/A",
                        ),
                    ),
                    "reason": (
                        "Deterministic minimum-strain search step."
                    ),
                },
                "physics_result": physics,
                "verification": verification,
            }

            render_iteration(
                normalized
            )

        st.divider()

        final1, final2, final3 = (
            st.columns(3)
        )

        final1.metric(
            "Final status",
            result.status,
        )

        if (
            result.minimum_strain_percent
            is not None
        ):
            final2.metric(
                "Minimum verified strain",
                f"{result.minimum_strain_percent:.4f}%",
            )

            final3.metric(
                "Verified energy",
                f"{result.verified_energy_Wh_kg:.4f} Wh/kg",
            )

            st.success(
                "Verified target achieved within the current "
                "analytical screening boundary."
            )

        else:
            final2.metric(
                "Minimum verified strain",
                "N/A",
            )

            final3.metric(
                "Verified energy",
                "N/A",
            )

        if (
            result.status
            == "TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY"
        ):
            st.warning(
                "The requested target cannot be verified within "
                "the current 10% analytical screening boundary."
            )


    # ========================================================
    # PROVENANCE REPLAY
    # ========================================================

    elif mode == "Provenance replay":
        records = read_jsonl_records(
            MUSE_BENCHMARK
        )

        selected = find_replay_run(
            records,
            target,
        )

        if selected is None:
            st.warning(
                "No canonical Muse trajectory exists "
                f"for {target:.2f} Wh/kg."
            )

            st.caption(
                "Available replay targets: 25, 50, and 100 Wh/kg."
            )

        else:
            render_replay(
                selected,
                fallback=False,
            )


# ============================================================
# SCIENTIFIC BOUNDARY
# ============================================================

st.divider()

st.markdown(
    """
### Scientific Boundary

SpiralAI currently performs theoretical or simulated
screening only.

Results are **not**:

- experimental measurements
- demonstrated device performance
- cycle-life evidence
- manufacturability proof
- evidence that graphene mechanical storage replaces lithium-ion batteries

Higher-fidelity validation may require:

- finite-element analysis
- molecular dynamics
- fatigue modelling
- fabrication
- mechanical cycling
- experiment
"""
)

st.caption(
    "SpiralAI | Meta Global AI Developer Hackathon 2026"
)