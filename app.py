import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Optical Birefringence & Photoelasticity Simulator", page_icon="🔬", layout="wide")

st.title("🔬 광학적 이방체(복굴절) 및 광탄성(Photoelasticity) 시뮬레이터")
st.markdown("이 앱은 결정체의 광학적 이방성과 재료의 광탄성 응력 해석 개념을 수치 시뮬레이션 및 시각화로 제공합니다.")

tab1, tab2, tab3 = st.tabs(["💎 1. 광학적 이방체 & 복굴절", "🔧 2. 광탄성 응력 해석", "📚 3. 이론 및 수식 정리"])

# =============================================================================
# TAB 1: 광학적 이방체 & 복굴절 (Birefringence)
# =============================================================================
with tab1:
    st.header("💎 광학적 이방성 및 빛의 광선 분리 (Birefringence)")
    st.caption("결정 내부의 광축 방향 및 굴절률차에 의해 비편광이 정상광선(o-ray)과 비정상광선(e-ray)으로 분리되는 현상입니다.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("⚙️ 광학 매개변수 설정")

        def update_material_indices():
            mat = st.session_state.tab1_material
            if mat == "Calcite":
                st.session_state.tab1_no = 1.658
                st.session_state.tab1_ne = 1.486
            elif mat == "Quartz":
                st.session_state.tab1_no = 1.544
                st.session_state.tab1_ne = 1.553
            elif mat == "Rutile":
                st.session_state.tab1_no = 2.616
                st.session_state.tab1_ne = 2.903

        if 'tab1_no' not in st.session_state:
            st.session_state.tab1_no = 1.658
        if 'tab1_ne' not in st.session_state:
            st.session_state.tab1_ne = 1.486

        mat_options = ["Calcite", "Quartz", "Rutile", "Custom"]
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
        ax1.set_title("Ray Splitting in Anisotropic Crystal")
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
# TAB 2: 광탄성 응력 해석 (Photoelasticity - 일자다리 3점 굽힘 전용)
# =============================================================================
with tab2:
    st.header("🔧 광탄성 응력 무늬 시뮬레이션 (3-Point Bending Beam)")
    st.caption("외부 하중을 받는 일자다리 구조물이 광탄성 효과에 의해 응력 간섭 무늬를 형성하는 시뮬레이션입니다.")

    c1, c2 = st.columns([1, 2])

    with c1:
        st.subheader("🎛️ 하중 및 편광 조건 설정")
        load_force = st.slider("인가 하중 크기 (Load Force, N)", 10, 200, 100, step=5, key="tab2_force")
        fringe_constant = st.slider("재료 광탄성 계수 (C, GPa⁻¹)", 0.5, 5.0, 2.5, step=0.1, key="tab2_C")
        
        pol_options = ["Circular Polariscope", "Plane Polariscope"]
        pol_choice = st.radio("편광기 구성 (Polariscope)", pol_options, key="tab2_pol")
        
        show_isoclinic = (pol_choice == "Plane Polariscope")

    with c2:
        nx, ny = 400, 150
        x = np.linspace(-2.0, 2.0, nx)
        y = np.linspace(-0.8, 0.8, ny)
        X, Y = np.meshgrid(x, y)

        L = 4.0
        P = load_force * 0.15
        M = P * (L / 2.0 - np.abs(X))
        
        sigma_x = M * Y
        sigma_y = np.zeros_like(X)
        tau_xy = -P * np.sign(X) * (0.8**2 - Y**2) * 0.5

        center_stress = (sigma_x + sigma_y) / 2.0
        radius_stress = np.sqrt(((sigma_x - sigma_y) / 2.0)**2 + tau_xy**2)
        
        sigma_1 = center_stress + radius_stress
        sigma_2 = center_stress - radius_stress
        theta_p = 0.5 * np.arctan2(2.0 * tau_xy, sigma_x - sigma_y)

        delta = fringe_constant * (sigma_1 - sigma_2)

        lambda_r = 650.0
        lambda_g = 540.0
        lambda_b = 450.0

        I_r = np.sin(delta * 12.0 / lambda_r * 100.0) ** 2
        I_g = np.sin(delta * 12.0 / lambda_g * 100.0) ** 2
        I_b = np.sin(delta * 12.0 / lambda_b * 100.0) ** 2

        if show_isoclinic:
            isoclinic_factor = np.sin(
