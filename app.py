import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# 페이지 기본 설정
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="광학적 이방체 및 광탄성 시뮬레이터",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 광학적 이방체(복굴절) 및 광탄성(Photoelasticity) 시뮬레이터")
st.markdown("""
이 앱은 **결정체의 광학적 이방성(Birefringence)**과 **재료의 광탄성 응력 해석(Photoelastic Stress Analysis)** 개념을 수치 시뮬레이션 및 시각화로 제공합니다.
""")

tab1, tab2, tab3 = st.tabs([
    "💎 1. 광학적 이방체 & 복굴절 (Birefringence)", 
    "🔧 2. 광탄성 응력 해석 (Photoelasticity)",
    "📚 3. 이론 및 수식 정리"
])

# =============================================================================
# TAB 1: 광학적 이방체 & 복굴절 (Birefringence)
# =============================================================================
with tab1:
    st.header("💎 광학적 이방성 및 빛의 광선 분리 (Birefringence)")
    st.caption("결정 내부의 광축(Optic Axis) 방향 및 굴절률차에 의해 비편광이 정상광선(o-ray)과 비정상광선(e-ray)으로 분리되는 현상을 관찰합니다.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("⚙️ 결정을 이루는 광학적 매개변수")

        def update_material_indices():
            mat = st.session_state.tab1_material
            if mat == "방해석 (Calcite)":
                st.session_state.tab1_no = 1.658
                st.session_state.tab1_ne = 1.486
            elif mat == "수정 (Quartz)":
                st.session_state.tab1_no = 1.544
                st.session_state.tab1_ne = 1.553
            elif mat == "금강석/루틸 (Rutile)":
                st.session_state.tab1_no = 2.616
                st.session_state.tab1_ne = 2.903

        if 'tab1_no' not in st.session_state:
            st.session_state.tab1_no = 1.658
        if 'tab1_ne' not in st.session_state:
            st.session_state.tab1_ne = 1.486

        material_choice = st.selectbox(
            "대표적인 이방성 결정 선택",
            ["방해석 (Calcite)", "수정 (Quartz)", "금강석/루틸 (Rutile)", "사용자 정의"],
            key="tab1_material",
            on_change=update_material_indices
        )

        n_o = st.slider("정상광선 굴절률 (n_o)", 1.000, 3.000, key="tab1_no", step=0.001)
        n_e = st.slider("비정상광선 굴절률 (n_e)", 1.000, 3.000, key="tab1_ne", step=0.001)
        
        optic_axis_deg = st.slider("광축 각도 (Optic Axis Angle, θ_OA)", 0, 90, 45, step=1, key="tab1_oa")
        incident_angle_deg = st.slider("입사각 (Incident Angle, θ_i)", 0, 75, 30, step=1, key="tab1_inc")
        wavelength_nm = st.slider("입사광 파장 (Wavelength, nm)", 400, 700, 550, step=10, key="tab1_wave")

        def wavelength_to_rgb(wavelength):
            gamma = 0.8
            if 380 <= wavelength <= 440:
                r, g, b = -(wavelength - 440) / (440 - 380), 0.0, 1.0
            elif 440 <= wavelength <= 490:
                r, g, b = 0.0, (wavelength - 440) / (490 - 440), 1.0
            elif 490 <= wavelength <= 510:
                r, g, b = 0.0, 1.0, -(wavelength - 510) / (510 - 490)
            elif 510 <= wavelength <= 580:
                r, g, b = (wavelength - 510) / (580 - 510), 1.0, 0.0
            elif 580 <= wavelength <= 645:
                r, g, b = 1.0, -(wavelength - 645) / (645 - 580), 0.0
            elif 645 <= wavelength <= 780:
                r, g, b = 1.0, 0.0, 0.0
            else:
                r, g, b = 0.0, 0.0, 0.0
            return (r ** gamma, g ** gamma, b ** gamma)

        light_color = wavelength_to_rgb(wavelength_nm)

    with col2:
        theta_i = np.radians(incident_angle_deg)
        theta_OA = np.radians(optic_axis_deg)

        # o-ray 굴절각 계산
        sin_theta_ro = np.sin(theta_i) / n_o
        theta_r_o = np.arcsin(np.clip(sin_theta_ro, -1.0, 1.0))

        # e-ray 유효 굴절률 및 굴절각 계산
        n_e_eff = 1.0 / np.sqrt((np.cos(theta_OA) / n_o)**2 + (np.sin(theta_OA) / n_e)**2)
        sin_theta_re = np.sin(theta_i) / n_e_eff
        theta_r_e = np.arcsin(np.clip(sin_theta_re, -1.0, 1.0))

        fig1, ax1 = plt.subplots(figsize=(8, 6))
        
        # 영역 표시
        ax1.fill_between([-4, 4], 0, 4, color='#e0f7fa', alpha=0.4, label="Air (n=1.0)")
        ax1.fill_between([-4, 4], -4, 0, color='#e8eaf6', alpha=0.6, label=f"Crystal ({material_choice})")
        ax1.axhline(0, color='black', lw=2)
        ax1.axvline(0, color='gray', linestyle='--', alpha=0.7, label="Normal Line")

        # 입사광선
        x_inc = [-3 * np.tan(theta_i), 0]
        y_inc = [3, 0]
        ax1.plot(x_inc, y_inc, color=light_color, lw=3, label="Incident Light")

        # o-ray (정상 광선)
        x_o = [0, 3 * np.sin(theta_r_o)]
        y_o = [0, -3 * np.cos(theta_r_o)]
        ax1.plot(x_o, y_o, color='#1e88e5', lw=2.5, linestyle='-', label=f"o-ray (n_o={n_o:.3f})")

        # e-ray (비정상 광선)
        x_e = [0, 3 * np.sin(theta_r_e)]
        y_e = [0, -3 * np.cos(theta_r_e)]
        ax1.plot(x_e, y_e, color='#e53935', lw=2.5, linestyle='--', label=f"e-ray (n_eff={n_e_eff:.3f})")

        # 광축 표시
        oa_dx = np.cos(theta_OA)
        oa_dy = -np.sin(theta_OA)
        ax1.quiver(0, -2, oa_dx, oa_dy, scale=3, color='purple', alpha=0.8, label=f"Optic Axis ({
