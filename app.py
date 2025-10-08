import streamlit as st
import random
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cognitive Spectrum Manager", page_icon="📶", layout="wide")
st.title("📶 Cognitive Spectrum Manager – SDR & CR Simulator")
st.caption("A real-time demonstration of Software Defined Radio and Cognitive Radio principles without datasets.")

# --- Parameters ---
TOTAL_BANDS = 12
SPECTRUM = [random.choice([0, 1]) for _ in range(TOTAL_BANDS)]  # 0-free, 1-occupied

# --- Functions ---

def spectrum_sense():
    """Simulate spectrum sensing by randomly assigning free/occupied states."""
    global SPECTRUM
    SPECTRUM = [random.choice([0, 1]) for _ in range(TOTAL_BANDS)]
    return SPECTRUM

def cognitive_decision(environment_factor):
    """Select best free band based on environment awareness."""
    free_bands = [i for i, band in enumerate(SPECTRUM) if band == 0]
    if not free_bands:
        return None
    # Environment factor: prefer lower bands in urban, higher in rural
    if environment_factor == "Urban":
        return min(free_bands)
    else:
        return max(free_bands)

def cognition_cycle(chosen_band):
    """Return the cognition cycle log."""
    return {
        "Sense": "Spectrum sensed successfully.",
        "Orient": "Knowledge structured based on band usage.",
        "Plan": "Selecting the optimal free band.",
        "Decide": f"Selected Band: {chosen_band}" if chosen_band is not None else "No free band available.",
        "Act": "Cognitive radio tuned to the new band." if chosen_band is not None else "Waiting for spectrum opportunity."
    }

# --- Sidebar ---
st.sidebar.header("Simulation Settings")
env_factor = st.sidebar.radio("📍 Environment Awareness", ["Urban", "Rural"])
auto_refresh = st.sidebar.checkbox("Auto Refresh Simulation", value=False)
refresh_interval = st.sidebar.slider("⏱ Refresh Interval (sec)", 1, 5, 2)

# --- Simulation Start ---
if st.button("🔁 Run Cognitive Simulation") or auto_refresh:
    if auto_refresh:
        st.info("Auto-refresh is ON. The simulation will update every few seconds...")

    while True:
        spectrum = spectrum_sense()
        chosen_band = cognitive_decision(env_factor)
        log = cognition_cycle(chosen_band)

        # --- Spectrum Visualization ---
        fig, ax = plt.subplots(figsize=(10, 1))
        colors = ["green" if b == 0 else "red" for b in spectrum]
        ax.bar(range(TOTAL_BANDS), [1]*TOTAL_BANDS, color=colors)
        ax.set_xticks(range(TOTAL_BANDS))
        ax.set_yticks([])
        ax.set_title("📡 Spectrum Occupancy (Green = Free, Red = Occupied)")
        st.pyplot(fig)

        # --- Cognitive Cycle ---
        st.subheader("🧠 Cognition Cycle Log")
        for phase, message in log.items():
            st.write(f"**{phase}:** {message}")

        # --- Result ---
        if chosen_band is not None:
            st.success(f"✅ Secondary user allocated to Band {chosen_band}")
        else:
            st.warning("⚠️ No free spectrum found. Waiting...")

        if not auto_refresh:
            break
        time.sleep(refresh_interval)
        st.rerun()
