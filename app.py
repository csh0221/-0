import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Optical Birefringence Simulator", page_icon="💎", layout="wide")

st.title("💎 광학적 이방체 & 복굴절(Birefringence) 시뮬레이터")
st.caption("결정 내부의 광축 방향 및 굴절률차에 의해 비편광이 정상광선(o-ray)과 비정상광선(e-ray)으로 분리되는 현상을 시뮬레이션합니다.")

tab1, tab2 = st.tabs(["🎮 시뮬레이터", "📚 광축(Optic Axis) 쉽게 이해하기"])

# =============================================================================
# TAB 1: 복굴절 시뮬레이터
# =============================================================================
with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("⚙️ 광학 매개변수 설정")

        def update_material_indices():
            mat = st.session_state.tab1_material
            if mat == "Calcite (복굴절/일축성 음성 - 방해석)":
                st.session_state.tab1_no = 1.658
                st.session_state.tab1_ne = 1.486
            elif mat == "Quartz (복굴절/일축성 양성 - 수정)":
                st.session_state.tab1_no = 1.544
                st.session_state.tab1_ne = 1.553
            elif mat == "Rutile (복굴절/일축성 양성 - 루틸)":
                st.session_state.tab1_no = 2.616
                st.session_state.tab1_ne = 2.903
            elif mat == "Halite/Glass (단굴절/등방성 - 암염/유리)":
                st.session_state.tab1_no = 1.544
                st.session_state.tab1_ne = 1.544
            elif mat == "Diamond (단굴절/등방성 - 다이아몬드)":
                st.session_state.tab1_no = 2.417
                st.session_state.tab1_ne = 2.417

        if 'tab1_no' not in st.session_state:
            st.session_state.tab1_no = 1.658
        if 'tab1_ne' not in st.session_state:
            st.session_state.tab1_ne = 1.486

        mat_options = [
            "Calcite (복굴절/일축성 음성 - 방해석)", 
            "Quartz (복굴절/일축성 양성 - 수정)", 
            "Rutile (복굴절/일축성 양성 - 루틸)", 
            "Halite/Glass (단굴절/등방성 - 암염/유리)", 
            "Diamond (단굴절/등방성 - 다이아몬드)", 
            "Custom"
        ]
        material_choice = st.selectbox("결정 재질 선택", mat_options, key="tab1_material", on_change=update_material_indices)
        
        n_o = st.slider("정상광선 굴절률 (n_o)", 1.000, 3.000, key="tab1_no", step=0.001)
        n_e = st.slider("비정상광선 굴절률 (n_e)", 1.000, 3.000, key="tab1_ne", step=0.001)
        optic_axis_deg = st.slider("광축 각도 (Optic Axis Angle, deg)", 0, 90, 45, step=1, key="tab1_oa")
        incident_angle_deg = st.slider("입사각 (Incident Angle, deg)", 0, 75, 30, step=1, key="tab1_inc")
        wavelength_nm = st.slider("입사광 파장 (Wavelength, nm)", 400, 700, 550, step=10, key="tab1_wave")

        def wavelength_to_rgb(wl):
            gamma = 0.8
            if wl < 440:
                r, g, b = -(wl - 440) / 60.0, 0.0, 1.0
            elif wl < 490:
                r, g, b = 0.0, (wl - 440) / 50.0, 1.0
            elif wl < 510:
                r, g, b = 0.0, 1.0, -(wl - 510) / 20.0
            elif wl < 580:
                r, g, b = (wl - 510) / 70.0, 1.0, 0.0
            elif wl < 645:
                r, g, b = 1.0, -(wl - 645) / 65.0, 0.0
            else:
                r, g, b = 1.0, 0.0, 0.0
            return (max(0.0, r)**gamma, max(0.0, g)**gamma, max(0.0, b)**gamma)

        light_color = wavelength_to_rgb(wavelength_nm)

    with col2:
        theta_i = np.radians(incident_angle_deg)
        theta_OA = np.radians(optic_axis_deg)

        sin_theta_ro = np.sin(theta_i) / n_o
        val_ro = np.clip(sin_theta_ro, -1.0, 1.0)
        theta_r_o = np.arcsin(val_ro)

        term_cos = np.cos(theta_OA) / n_o
        term_sin = np.sin(theta_OA) / n_e
        n_e_eff = 1.0 / np.sqrt(term_cos**2 + term_sin**2)

        sin_theta_re = np.sin(theta_i) / n_e_eff
        val_re = np.clip(sin_theta_re, -1.0, 1.0)
        theta_r_e = np.arcsin(val_re)

        fig1, ax1 = plt.subplots(figsize=(8, 6))
        
        ax1.fill_between([-4, 4], 0, 4, color='#e0f7fa', alpha=0.4, label="Air (n=1.0)")
        ax1.fill_between([-4, 4], -4, 0, color='#e8eaf6', alpha=0.6, label="Crystal")
        ax1.axhline(0, color='black', lw=2)
        ax1.axvline(0, color='gray', linestyle='--', alpha=0.7, label="Normal Line")

        x_inc = [-3 * np.tan(theta_i), 0]
        y_inc = [3, 0]
        ax1.plot(x_inc, y_inc, color=light_color, lw=3, label="Incident Light")

        x_o = [0, 3 * np.sin(theta_r_o)]
        y_o = [0, -3 * np.cos(theta_r_o)]
        ax1.plot(x_o, y_o, color='#1e88e5', lw=2.5, linestyle='-', label=f"o-ray (n_o={n_o:.3f})")

        x_e = [0, 3 * np.sin(theta_r_e)]
        y_e = [0, -3 * np.cos(theta_r_e)]
        ax1.plot(x_e, y_e, color='#e53935', lw=2.5, linestyle='--', label=f"e-ray (n_eff={n_e_eff:.3f})")

        oa_dx = np.cos(theta_OA)
        oa_dy = -np.sin(theta_OA)
        ax1.quiver(0, -2, oa_dx, oa_dy, scale=3, color='purple', alpha=0.8, label=f"Optic Axis ({optic_axis_deg} deg)")

        ax1.set_xlim(-3, 3)
        ax1.set_ylim(-3.5, 3)
        ax1.set_aspect('equal')
        ax1.set_title("Ray Splitting in Anisotropic Crystal", fontsize=12, fontweight='bold')
        ax1.legend(loc="lower left", fontsize='small')
        ax1.grid(True, linestyle=':', alpha=0.6)

        st.pyplot(fig1)
        plt.close(fig1)

        delta_n_val = n_e - n_o
        ro_deg_val = np.degrees(theta_r_o)
        re_deg_val = np.degrees(theta_r_e)
        diff_deg_val = abs(np.degrees(theta_r_o - theta_r_e))

        st.info(f"**Ray Trajectory Data:**\n- Birefringence (Δn = n_e - n_o): `{delta_n_val:+.4f}`\n- o-ray Angle: `{ro_deg_val:.2f}°`\n- e-ray Angle: `{re_deg_val:.2f}°`\n- Separation Angle (Δθ): `{diff_deg_val:.2f}°`")

# =============================================================================
# TAB 2: 광축(Optic Axis) 개념 가이드
# =============================================================================
with tab2:
    st.header("💡 광축(Optic Axis)이란 무엇인가요?")
    st.markdown("""
    **광축(Optic Axis)**은 결정 내부에서 **"복굴절(빛 갈라짐)이 일어나지 않는 특수한 방향"**을 의미합니다.
    빛이 광축과 정확히 평행하게 지나가면 비정상광선($e$-ray)과 정상광선($o$-ray)의 속도 차이가 사라져 **단굴절처럼 하나의 빛으로만 진행**합니다.
    """)

    st.markdown("---")

    st.subheader("🔍 광물 구조에 따른 광축 분류")
    
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("### 1. 등방성 (단굴절 광물)")
        st.write("**대표 광물:** 암염(Halite), 다이아몬드, 유리")
        st.write("- **광축 특징:** 광축이라는 개념 자체가 존재하지 않음 (모든 방향에서 속도가 동일)")
        st.write("- **현상:** 빛이 어느 방향으로 입사해도 절대 갈라지지 않음 ($n_o = n_e$)")

    with col_b:
        st.markdown("### 2. 일축성 (Uniaxial 광물)")
        st.write("**대표 광물:** 방해석(Calcite), 수정(Quartz), 루틸(Rutile)")
        st.write("- **광축 특징:** 단 **1개의 광축**을 가짐 (결정의 C축 방향)")
        st.write("- **양성 광물 ($n_e > n_o$):** 수정, 루틸 ($e$-ray가 더 느림)")
        st.write("- **음성 광물 ($n_e < n_o$):** 방해석 ($e$-ray가 더 빠름)")

    with col_c:
        st.markdown("### 3. 이축성 (Biaxial 광물)")
        st.write("**대표 광물:** 운모(Mica), 감람석(Olivine), 휘석(Pyroxene)")
        st.write("- **광축 특징:** **2개의 광축**을 가짐")
        st.write("- **현상:** 결정 구조가 비대칭적이라 서로 다른 2개의 광축 방향을 따라 빛의 속도 상쇄점이 존재함")

    st.markdown("---")
    st.success("""
    💡 **실험 팁 (시뮬레이터 활용법):**
    `1. 광축 각도` 슬라이더를 조정하여 입사각과 광축이 서로 같아지는 각도로 맞추면, 광선 분리 각도(Δθ)가 줄어드는 것을 확인할 수 있습니다!
    """)
