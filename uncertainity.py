import streamlit as st
import numpy as np
import math

st.set_page_config(page_title="Uncertainty Calculator", layout="centered")

st.title("📊 Expanded Uncertainty Calculator")
st.write("Flexible calculator for **Type A + multiple Type B uncertainties**")

# -------------------------------
# USER CONTROLS
# -------------------------------
n = st.number_input("Number of readings (n)", min_value=2, max_value=50, value=5, step=1)
m = st.number_input("Number of Type B uncertainty sources", min_value=1, max_value=10, value=1, step=1)

st.divider()

# -------------------------------
# MEASUREMENT INPUTS
# -------------------------------
st.subheader("Measurements")

values = []
cols = st.columns(min(n, 5))

for i in range(n):
    with cols[i % len(cols)]:
        val = st.number_input(f"Reading {i+1}", key=f"v{i}", value=50.0)
        values.append(val)

values = np.array(values)

st.divider()

# -------------------------------
# TYPE B INPUTS
# -------------------------------
st.subheader("Type B Uncertainty Sources")

uB_values = []
for i in range(m):
    u = st.number_input(
        f"Type B uncertainty {i+1}",
        key=f"uB{i}",
        value=0.23,
        step=0.01
    )
    uB_values.append(u)

uB_values = np.array(uB_values)

# -------------------------------
# CALCULATION
# -------------------------------
if st.button("Calculate uₑ"):
    try:
        # Mean
        mu = np.mean(values)

        # Sample standard deviation (important!)
        std_dev = np.std(values, ddof=1)

        # ----- Type A uncertainty -----
        uA = std_dev / math.sqrt(n)

        # ----- Type B uncertainty -----
        uB_components = uB_values / math.sqrt(3)
        uB = math.sqrt(np.sum(uB_components**2))

        # ----- Combined uncertainty -----
        uc = math.sqrt(uA**2 + uB**2)

        # ----- Expanded uncertainty -----
        k = 1.96  # 95% confidence
        ue = (k * uc / mu) * 100

        # -------------------------------
        # OUTPUT
        # -------------------------------
        st.success("✅ Calculation Complete")

        st.write(f"**Mean (μ):** {mu:.4f}")
        st.write(f"**Sample standard deviation:** {std_dev:.4f}")

        st.write(f"**Type A uncertainty (uₐ):** {uA:.4f}")
        st.write(f"**Combined Type B uncertainty (uᵦ):** {uB:.4f}")
        st.write(f"**Combined uncertainty (u𝒸):** {uc:.4f}")

        st.markdown(f"### 🎯 **Expanded Uncertainty uₑ (%) = {ue:.3f}**")

    except Exception as e:
        st.error(f"Calculation error: {e}")
