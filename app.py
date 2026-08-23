# ============================================================
# ZeroES Laser Pro – نسخة مستقرة
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="ZeroES Laser Pro", page_icon="🔬", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0a0a0f; }
    .main-title { font-size: 3rem; color: #00d4ff; text-align: center; font-weight: 700; }
    .result-box { background: rgba(0,212,255,0.05); padding: 1rem; border-radius: 10px; border: 1px solid #00d4ff; }
    .result-value { font-size: 1.5rem; font-weight: 700; color: #00d4ff; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔬 ZeroES Laser Pro</div>', unsafe_allow_html=True)
st.markdown("---")

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

col1, col2, col3 = st.columns(3)

with col1:
    power = st.slider("⚡ Power (W)", 0.1, 10.0, 1.0, 0.1)
with col2:
    beam = st.slider("📏 Beam Width (mm)", 0.1, 5.0, 1.0, 0.1)
with col3:
    spectrum = st.selectbox("📡 Spectrum", ["Visible", "IR", "UV", "Microwave", "Radio"])

if st.button("▶ RUN SIMULATION", use_container_width=True):
    with st.spinner("Simulating with ZPIF..."):
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
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("**⚡ Peak Intensity**")
            st.markdown(f'<div class="result-value">{np.max(intensity_mod):.2f} W/m²</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("**📏 Beam Width**")
            st.markdown(f'<div class="result-value">{beam:.2f} mm</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
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
        
        st.success("✅ Simulation complete!")

st.markdown("---")
st.caption("⚡ Engine: ZPIF-USAC-ZZFZ | Zeros: 50 | © 2026 Ebrahim E. Elsayed")
