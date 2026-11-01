"""
SpiralAI Agent Console.

Meta Global AI Developer Hackathon 2026.

Visual interface for:
PLAN -> ACT -> PHYSICS -> VERIFY -> REDESIGN

All current numerical outputs are theoretical/simulated screening
results and are not experimentally validated device performance.
"""

from html import escape
from pathlib import Path

import streamlit as st

from agent.iterative_agent import run_iterative_design
from optimization.minimum_strain import find_minimum_strain
from provenance.run_log import read_jsonl_records


MODEL = "meta-models/muse-spark-open-1026"

MUSE_BENCHMARK = Path(
    "results/muse_trajectory_benchmark.jsonl"
)


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

    /* --------------------------------
       CORE COLORS

       Background:   #050B09
       Panel:        #0D1B18
       Mint:         #7EE2B8
       Green:        #42D89C
       Gold:         #D9A441
       Soft gold:    #F2C66D
       Main text:    #F4F7F5
       Muted text:   #A6B7AF
       -------------------------------- */


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


    /* ANIMATED GRAPHENE HEXAGON BACKGROUND */

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

        background-size:
            84px 147px;

        background-position:
            0 0,
            0 0,
            42px 73px,
            42px 73px,
            0 0;

        opacity: 0.7;

        animation:
            graphene-drift 30s linear infinite;
    }


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


    @keyframes border-glow {
        0%,
        100% {
            border-color:
                rgba(37, 68, 58, 0.80);
        }

        50% {
            border-color:
                rgba(126, 226, 184, 0.55);
        }
    }


    /* KEEP STREAMLIT CONTENT ABOVE BACKGROUND */

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


    /* HERO TITLE ACCENT */

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

        margin:
            12px 0 22px 0;

        padding:
            11px 16px;

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


    /* SCIENTIFIC WARNING */

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


    /* CARDS */

    .spiral-card {
        position: relative;

        background:
            linear-gradient(
                145deg,
                rgba(13, 27, 24, 0.96),
                rgba(16, 32, 28, 0.90)
            );

        border:
            1px solid #25443A;

        border-radius:
            14px;

        padding:
            20px;

        margin-bottom:
            14px;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.24);

        backdrop-filter:
            blur(12px);

        animation:
            border-glow 6s ease-in-out infinite;
    }


    .spiral-card::after {
        content: "";
        position: absolute;
        top: 10px;
        right: 12px;

        width: 7px;
        height: 7px;

        border-radius: 50%;

        background:
            #7EE2B8;

        animation:
            led-pulse 2.5s ease-in-out infinite;
    }


    .success-card {
        border-left:
            6px solid #42D89C;
    }


    .warning-card {
        border-left:
            6px solid #F2C66D;
    }


    .warning-card::after {
        background:
            #F2C66D;

        animation:
            gold-pulse 2.8s ease-in-out infinite;
    }


    .fail-card {
        border-left:
            6px solid #D9A441;
    }


    /* STAGES */

    .stage {
        color:
            #7EE2B8;

        font-size:
            0.80rem;

        font-weight:
            800;

        letter-spacing:
            0.14em;
    }


    .stage-label {
        display: inline-block;

        min-width:
            86px;

        margin-bottom:
            3px;

        color:
            #F2C66D;

        font-size:
            0.76rem;

        font-weight:
            800;

        letter-spacing:
            0.09em;
    }


    /* FINAL STATUS */

    .final-status {
        display: inline-block;

        margin-top:
            5px;

        padding:
            6px 10px;

        border-radius:
            7px;

        font-size:
            1.06rem;

        font-weight:
            850;

        letter-spacing:
            0.035em;
    }


    .success-card .final-status {
        color:
            #07110F;

        background:
            linear-gradient(
                90deg,
                #42D89C,
                #7EE2B8
            );
    }


    .warning-card .final-status {
        color:
            #171005;

        background:
            linear-gradient(
                90deg,
                #D9A441,
                #F2C66D
            );
    }


    .fail-card .final-status {
        color:
            #F2C66D;

        border:
            1px solid #D9A441;

        background:
            rgba(217, 164, 65, 0.10);
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


    /* NUMBER INPUT */

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


    /* BUTTON */

    .stButton
    > button[kind="primary"] {
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


    .stButton
    > button[kind="primary"]:hover {
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


    /* ARCHITECTURE CARD */

    .architecture-card {
        position: relative;
        isolation: isolate;
        overflow: hidden;
        max-width: 460px;
        margin: 0 auto;
        padding: 18px;
        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(66, 216, 156, 0.10),
                transparent 48%
            ),
            linear-gradient(
                160deg,
                rgba(16, 32, 28, 0.98),
                rgba(8, 18, 15, 0.98)
            );
        border: 1px solid #25443A;
        border-radius: 14px;
        text-align: center;
        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.28),
            inset 0 1px 0 rgba(244, 247, 245, 0.04);
    }

    .architecture-kicker {
        margin-bottom: 14px;
        color: #A6B7AF;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.16em;
    }

    .architecture-node {
        width: 100%;
        max-width: 320px;
        margin: 0 auto;
        padding: 10px 12px;
        border: 1px solid #25443A;
        border-radius: 9px;
        color: #F4F7F5;
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.04em;
        line-height: 1.35;
        background:
            linear-gradient(
                135deg,
                rgba(16, 32, 28, 0.98),
                rgba(13, 27, 24, 0.98)
            );
        box-shadow:
            inset 0 1px 0 rgba(244, 247, 245, 0.035),
            0 4px 12px rgba(0, 0, 0, 0.14);
    }

    .architecture-node.mint {
        border-color: #42D89C;
        color: #7EE2B8;
        box-shadow:
            inset 0 0 18px rgba(66, 216, 156, 0.05),
            0 0 16px rgba(126, 226, 184, 0.10);
    }

    .architecture-node.gold {
        border-color: #D9A441;
        color: #F2C66D;
        box-shadow:
            inset 0 0 18px rgba(217, 164, 65, 0.05),
            0 0 16px rgba(242, 198, 109, 0.10);
    }

    .architecture-arrow {
        color: #7EE2B8;
        line-height: 1;
        padding: 6px 0;
        font-family: monospace;
        font-size: 0.8rem;
        font-weight: 700;
        opacity: 0.82;
    }


    /* ALERTS */

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


    /* REDUCED MOTION ACCESSIBILITY */

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


def status_class(
    status: str,
) -> str:
    """Map scientific outcomes to visual status classes."""

    if status in {
        "TARGET_REACHED",
        "MINIMUM_STRAIN_FOUND",
    }:
        return "success-card"

    if status in {
        "TARGET_NOT_REACHED",
        "MORE_VALIDATION_REQUIRED",
        "TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY",
        "MAX_ITERATIONS_REACHED",
        "NO_IMPROVEMENT",
    }:
        return "warning-card"

    return "fail-card"


def format_iteration_name(
    iteration,
) -> str:
    """Format numerical and feasibility-check iteration names."""

    if iteration == 0:
        return "FEASIBILITY CHECK"

    return f"ITERATION {iteration}"


def render_iteration(
    record: dict,
) -> None:
    """Render one verified agent or optimization step."""

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

    css = status_class(
        status
    )

    if isinstance(
        energy,
        (int, float),
    ):
        energy_text = (
            f"{energy:.2f} Wh/kg"
        )

    else:
        energy_text = escape(
            str(energy)
        )

    if isinstance(
        strain,
        (int, float),
    ):
        strain_text = (
            f"{strain:.3f}%"
        )

    else:
        strain_text = escape(
            str(strain)
        )

    safe_reason = escape(
        str(reason)
    )

    safe_status = escape(
        str(status)
    )

    iteration_name = (
        format_iteration_name(
            iteration
        )
    )

    st.markdown(
        f"""
        <div class="spiral-card {css}">

            <div class="stage">
                {iteration_name}
            </div>


            <span class="stage-label">
                PLAN
            </span>
            {safe_reason}

            <br><br>

            <span class="stage-label">
                ACT
            </span>
            Proposed strain:
            <b>{strain_text}</b>

            <br><br>

            <span class="stage-label">
                PHYSICS
            </span>
            Verified system estimate:
            <b>{energy_text}</b>

            <br><br>

            <span class="stage-label">
                VERIFY
            </span>

            <span class="final-status">
                {safe_status}
            </span>

        </div>
        """,
        unsafe_allow_html=True,
    )


def find_replay_run(
    records: list[dict],
    target: float,
) -> dict | None:
    """Return the first benchmark trajectory matching a target."""

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


# ============================================================
# HEADER
# ============================================================


st.title(
    "SpiralAI"
)


st.markdown(
    """
    <h3 class="hero-accent">
        AI designs. Physics verifies.
    </h3>
    """,
    unsafe_allow_html=True,
)


st.caption(
    "Physics-verified scientific design agent "
    "for graphene mechanical energy storage."
)


st.markdown(
    '<div class="system-strip">'
    '<div class="system-item"><span class="led"></span>PHYSICS ENGINE ONLINE</div>'
    '<div class="system-item"><span class="led"></span>VERIFIER ONLINE</div>'
    '<div class="system-item"><span class="led"></span>PROVENANCE READY</div>'
    '<div class="system-item"><span class="led-gold"></span>THEORETICAL SCREENING</div>'
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


top1, top2, top3, top4 = st.columns(
    4
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
    "`meta-models/muse-spark-open-1026`"
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
            "Live Muse calls the official hackathon model "
            "`meta-models/muse-spark-open-1026` through Baseten. "
            "All numerical results are still calculated by the "
            "deterministic physics engine and checked by the verifier."
        )

    elif mode == "Deterministic optimization":
        st.info(
            "Deterministic optimization finds the lowest verified "
            "strain satisfying the requested target."
        )

    else:
        st.info(
            "Provenance replay loads a previously recorded real Muse "
            "trajectory without making a live API call."
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
        """
        <div class="architecture-card">
            <div class="architecture-kicker">DESIGN TO VALIDATION</div>
            <div class="architecture-node">TARGET</div>
            <div class="architecture-arrow" aria-hidden="true">|<br>v</div>
            <div class="architecture-node mint">MUSE / OPTIMIZER</div>
            <div class="architecture-arrow" aria-hidden="true">|<br>v</div>
            <div class="architecture-node">PHYSICS ENGINE</div>
            <div class="architecture-arrow" aria-hidden="true">|<br>v</div>
            <div class="architecture-node gold">INDEPENDENT VERIFIER</div>
            <div class="architecture-arrow" aria-hidden="true">|<br>v</div>
            <div class="architecture-node">REDESIGN / STOP</div>
        </div>
        """,
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

        st.markdown(
            """
            <div class="spiral-card">
                <div class="stage">
                    AGENT READY
                </div>
                Scientific-design pipeline initialized.
                <br><br>
                <span class="stage-label">NEXT ACTION</span>
                Choose a target and execution mode,
                then select <b>Run SpiralAI</b>.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # LIVE MUSE MODE
    # ========================================================

    elif mode == "Live Muse":

        st.markdown(
            '<div class="spiral-card">'
            '<div class="stage">LIVE AGENT</div>'
            '<br>'
            'Model: <b>meta-models/muse-spark-open-1026</b>'
            '<br><br>'
            'Muse proposes candidates. '
            'Deterministic physics calculates performance. '
            'The independent verifier decides whether the '
            'evidence supports the result.'
            '</div>',
            unsafe_allow_html=True,
        )

        try:
            with st.spinner(
                "Muse is designing. Physics is verifying..."
            ):
                report = run_iterative_design(
                    target_wh_kg=target,
                )
        except Exception as exc:
            st.warning(
                "Live Muse is currently unavailable. "
                "Switching to provenance-backed replay."
            )

            records = read_jsonl_records(
                MUSE_BENCHMARK
            )

            selected = find_replay_run(
                records,
                target,
            )

            if selected is None:
                st.error(
                    "No saved Muse trajectory is available for "
                    f"{target:.2f} Wh/kg. "
                    "Replay targets currently available: "
                    "25, 50, and 100 Wh/kg."
                )

                st.caption(
                    f"Live error: {type(exc).__name__}"
                )

            else:
                st.markdown(
                    '<div class="spiral-card warning-card">'
                    '<div class="stage">PROVENANCE FALLBACK</div>'
                    '<br>'
                    'Displaying a previously recorded real Muse '
                    'trajectory because the live API is unavailable.'
                    '</div>',
                    unsafe_allow_html=True,
                )

                st.caption(
                    f"Run ID: {selected['run_id']}"
                )

                st.caption(
                    f"Model: {selected['model']}"
                )

                for item in selected.get(
                    "history",
                    [],
                ):
                    render_iteration(item)

                st.divider()

                f1, f2, f3 = st.columns(3)

                f1.metric(
                    "Final status",
                    selected["final_status"],
                )

                f2.metric(
                    "Iterations",
                    selected["iterations"],
                )

                f3.metric(
                    "Evidence",
                    selected["evidence_type"],
                )

                st.caption(
                    "Replay mode uses provenance captured from an "
                    "earlier live Muse execution. No synthetic "
                    "trajectory was generated."
                )

        else:
            history = report.get(
                "history",
                [],
            )

            for item in history:
                render_iteration(item)

            st.divider()

            status = report.get(
                "final_status",
                "UNKNOWN",
            )

            iterations = report.get(
                "iterations_completed",
                len(history),
            )

            m1, m2, m3 = st.columns(3)

            m1.metric(
                "Final status",
                status,
            )

            m2.metric(
                "Agent iterations",
                iterations,
            )

            m3.metric(
                "Evidence",
                "THEORETICAL_SIMULATION",
            )

            if status == "TARGET_REACHED":
                st.success(
                    "The requested target was reached in "
                    "the current theoretical screening model."
                )

            elif status == "MORE_VALIDATION_REQUIRED":
                st.warning(
                    "Muse proposed a candidate requiring evidence "
                    "beyond the current analytical screening boundary."
                )

            elif status in {
                "MAX_ITERATIONS_REACHED",
                "NO_IMPROVEMENT",
                "TARGET_NOT_REACHED",
                "INVALID_MODEL_OUTPUT",
                "INVALID_RESULT",
            }:
                st.warning(
                    "The agent did not establish a verified solution "
                    "within the current run."
                )

            st.caption(
                "Live numerical results are produced by the "
                "deterministic physics engine, not by Muse."
            )


    # ========================================================
    # DETERMINISTIC MODE
    # ========================================================

    elif mode == "Deterministic optimization":

        with st.spinner(
            "Running verified minimum-strain search..."
        ):

            result = find_minimum_strain(
                target_wh_kg=target,
            )

        objective_html = (
            '<div class="spiral-card">'
            '<div class="stage">OBJECTIVE</div>'
            '<br>'
            'Find the <b>lowest verified strain</b> satisfying '
            f'<b>{target:.2f} Wh/kg</b> '
            'within the current 10% analytical screening boundary.'
            '</div>'
        )

        st.markdown(
            objective_html,
            unsafe_allow_html=True,
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
                "iteration":
                    item.get(
                        "iteration",
                        "?",
                    ),

                "proposal": {
                    "strain_percent":
                        item.get(
                            "strain_percent",
                            physics.get(
                                "strain_percent",
                                "N/A",
                            ),
                        ),

                    "reason":
                        (
                            "Deterministic minimum-strain "
                            "search step."
                        ),
                },

                "physics_result":
                    physics,

                "verification":
                    verification,
            }

            render_iteration(
                normalized
            )

        st.divider()

        a, b, c = st.columns(
            3
        )

        a.metric(
            "Final status",
            result.status,
        )

        if (
            result.minimum_strain_percent
            is not None
        ):

            b.metric(
                "Minimum verified strain",
                f"{result.minimum_strain_percent:.4f}%",
            )

            c.metric(
                "Verified energy",
                f"{result.verified_energy_Wh_kg:.4f} Wh/kg",
            )

            st.success(
                "Verified target achieved within the "
                "current analytical screening boundary."
            )

        else:

            b.metric(
                "Minimum verified strain",
                "N/A",
            )

            c.metric(
                "Verified energy",
                "N/A",
            )

        if (
            result.status
            ==
            "TARGET_UNREACHABLE_WITHIN_SCREENING_BOUNDARY"
        ):

            st.warning(
                "The requested target cannot be verified "
                "within the current 10% analytical "
                "screening boundary."
            )


    # ========================================================
    # PROVENANCE REPLAY MODE
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
                "Available replay targets: "
                "25, 50, and 100 Wh/kg."
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

            x, y, z = st.columns(
                3
            )

            x.metric(
                "Final status",
                selected[
                    "final_status"
                ],
            )

            y.metric(
                "Iterations",
                selected[
                    "iterations"
                ],
            )

            z.metric(
                "Evidence",
                selected[
                    "evidence_type"
                ],
            )


# ============================================================
# SCIENTIFIC BOUNDARY
# ============================================================


st.divider()


st.markdown(
    """
    ### Scientific Boundary

    SpiralAI currently performs
    theoretical/simulated screening only.

    Results are **not**:

    - experimental measurements
    - demonstrated device performance
    - cycle-life evidence
    - manufacturability proof
    - evidence that graphene mechanical storage
      replaces lithium-ion batteries

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
    "SpiralAI | "
    "Meta Global AI Developer Hackathon 2026"
)
