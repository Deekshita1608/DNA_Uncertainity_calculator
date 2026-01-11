import streamlit as st
import numpy as np
import math
from scipy import stats

st.set_page_config(page_title="Uncertainty Calculator", layout="centered")

st.title("📊 Expanded Uncertainty Calculator")
st.write("Enter **5 readings** and the value of **u₂** to compute **uₑ (%)**")

# ---- Inputs ----
st.subheader("Measurements (n = 5)")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    v1 = st.number_input("Reading 1", value=53.3)
with col2:
    v2 = st.number_input("Reading 2", value=56.4)
with col3:
    v3 = st.number_input("Reading 3", value=52.4)
with col4:
    v4 = st.number_input("Reading 4", value=56.9)
with col5:
    v5 = st.number_input("Reading 5", value=56.0)

u2 = st.number_input("Enter u₂", value=0.23, step=0.01)

# ---- Compute ----
if st.button("Calculate uₑ"):
    try:
        val = np.array([v1, v2, v3, v4, v5])

        mu = np.mean(val)
        n = 5
        std_dev = np.std(val)
        su = std_dev / math.sqrt(n)

        t = 2.78
        ur = t * su

        ad = round(ur, 4)
        k = 1.96
        us = ad + k * (u2 / math.sqrt(3))

        u = ad + math.sqrt(ur**2 + us**2)
        ue = u * 100 / stats.mode(val, keepdims=True)[0][0]

        # ---- Output ----
        st.success("✅ Calculation Complete")
        st.write(f"**Mean (μ):** {mu:.4f}")
        st.write(f"**Standard deviation:** {std_dev:.4f}")
        st.write(f"**uᵣ:** {ur:.4f}")
        st.write(f"**uₛ:** {us:.4f}")
        st.markdown(f"### 🎯 Final **uₑ (%) = {ue:.3f}**")

    except Exception as e:
        st.error(f"Calculation error: {e}")
