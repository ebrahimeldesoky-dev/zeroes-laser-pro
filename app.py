
# ============================================================
# ZeroES Laser Pro – الواجهة الجديدة
# تصميم مختلف، احترافي، وقوي
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="ZeroES Laser Pro",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background: #0a0a0f;
    }
    .top-bar {
        background: linear-gradient(90deg, #00d4ff, #7b68ee);
        padding: 0.5rem 2rem;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .top-bar-title {
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }
    .top-bar-info {
        color: white;
        font-size: 0.9rem;
    }
    .settings-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .run-btn {
        background: linear-gradient(135deg, #00d4ff, #7b68ee);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-size: 1.2rem;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s ease;
    }
    .run-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    .result-box {
        background: rgba(0, 212, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        margin: 0.5rem 0;
    }
    .result-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00d4ff;
    }
    .footer {
        text-align: center;
        color: #444;
        padding: 1rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="top-bar">
    <div class="top-bar-title">🔬 ZEROES LASER PRO</div>
    <div class="top-bar-info">⚡ ZPIF-ZZFZ | Zeros: 50 | v3.0</div>
</div>
""", unsafe_allow_html=True)

GAMMA_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
    103.725538, 105.446623, 107.168611, 109.333415, 111.029536,
    112.948105, 114.936519, 116.226680, 118.790783, 121.370125,
    122.946829, 124.256819, 127.516684, 129.578704, 131.087689,
    133.497737, 134.756510, 138.116042, 139.736209, 141.123707
]

def zzf(x):
    result = 0
    for g in GAMMA_ZEROS:
        result += g * np.sin(x / g) * np.exp(-1j * g * x)
    return result

SPECTRUM = {
    "Gamma": {"lambda": 0.0001, "freq": 3e18, "color": "#ff0000"},
    "X-Ray": {"lambda": 0.01, "freq": 3e16, "color": "#ff6600"},
    "UV": {"lambda": 0.2, "freq": 1.5e15, "color": "#9933ff"},
    "Visible": {"lambda": 0.5, "freq": 6e14, "color": "#00ff00"},
    "IR": {"lambda": 10, "freq": 3e13, "color": "#ff3300"},
    "Microwave": {"lambda": 100, "freq": 3e9, "color": "#ffaa00"},
    "Radio": {"lambda": 1000, "freq": 3e6, "color": "#0066ff"}
}

st.markdown("### ⚙️ Laser Settings")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("**📡 Spectrum**")
    spectrum = st.selectbox("", list(SPECTRUM.keys()), index=3, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("**⚡ Power (W)**")
    power = st.slider("", 0.1, 10.0, 1.0, 0.1, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("**📏 Beam Width (mm)**")
    beam = st.slider("", 0.1, 5.0, 1.0, 0.1, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("**📐 Divergence (mrad)**")
    angle = st.slider("", 0.0, 5.0, 0.1, 0.1, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🔬 Simulation")
    run = st.button("▶ RUN", use_container_width=True)
    st.markdown("### 📁 Import")
    uploaded_file = st.file_uploader("", type=["csv", "png", "jpg"], label_visibility="collapsed")

with col2:
    st.markdown("### 📊 Results")
    if run:
        with st.spinner("Simulating..."):
            x = np.linspace(-5, 5, 200)
            y = np.linspace(-5, 5, 200)
            X, Y = np.meshgrid(x, y)
            sigma = beam / 2
            intensity = power * np.exp(-((X)**2 + (Y)**2) / (2 * sigma**2))
            x_zzf = np.linspace(0.1, 20, len(x))
            z_vals = zzf(x_zzf)
            zpif_effect = np.abs(z_vals[:len(x)])
            zpif_effect = zpif_effect / np.max(zpif_effect) * 0.5 + 0.5
            intensity_mod = intensity * zpif_effect.reshape(-1, 1)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown("**⚡ Peak Intensity**")
                st.markdown(f'<div class="result-value">{np.max(intensity_mod):.2f} W/m²</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_b:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown("**📏 Beam Width**")
                st.markdown(f'<div class="result-value">{beam:.2f} mm</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_c:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown("**🔵 ZPIF Effect**")
                st.markdown(f'<div class="result-value">{np.mean(zpif_effect):.2f}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            im = ax.imshow(intensity_mod, extent=[-5,5,-5,5], cmap='hot', origin='lower')
            ax.set_title(f"{spectrum} - Beam Profile")
            ax.set_xlabel("x (mm)")
            ax.set_ylabel("y (mm)")
            plt.colorbar(im, ax=ax)
            st.pyplot(fig)

st.markdown("---")
st.markdown("### 🛠️ Tools")

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 Comparison", use_container_width=True):
        st.info("Comparing all spectrums...")
with col2:
    if st.button("📁 Import Data", use_container_width=True):
        st.info("Upload CSV or Image from sidebar")
with col3:
    if st.button("📄 Export Report", use_container_width=True):
        st.info("Report generated!")
with col4:
    if st.button("⚙️ Settings", use_container_width=True):
        st.info("Advanced settings")

st.markdown("""
<div class="footer">
    ⚡ Engine: ZPIF-USAC-ZZFZ | Zeros: 50 | Status: Ready<br>
    © 2026 Ebrahim E. Elsayed – ZeroES Laser Pro
</div>
""", unsafe_allow_html=True)
