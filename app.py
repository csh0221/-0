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
        label_o = "o-ray (n_o=" + str(round(n_o, 3)) + ")"
        ax1.plot(x_o, y_o, color='#1e88e5', lw=2.5, linestyle='-', label=label_o)

        x_e = [0, 3 * np.sin(theta_r_e)]
        y_e = [0, -3 * np.cos(theta_r_e)]
        label_e = "e-ray (n_eff=" + str(round(n_e_eff, 3)) + ")"
        ax1.plot(x_e, y_e, color='#e53935', lw=2.5, linestyle='--', label=label_e)

        oa_dx = np.cos(theta_OA)
        oa_dy = -np.sin(theta_OA)
        oa_label = "Optic Axis (" + str(optic_axis_deg) + " deg)"
        ax1.quiver(0, -2, oa_dx, oa_dy, scale=3, color='purple', alpha=0.8, label=oa_label)

        ax1.set_xlim(-3, 3)
        ax1.set_ylim(-3.5, 3)
        ax1.set_aspect('equal')
        ax1.set_title("Ray Splitting in Anisotropic Crystal")
        ax1.legend(loc="lower left", fontsize='small')
        ax1.grid(True, linestyle=':', alpha=0.6)

        st.pyplot(fig1)
        plt.close(fig1)

        delta_n_val = round(n_e - n_o, 4)
        ro_deg_val = round(np.degrees(theta_r_o), 2)
        re_deg_val = round(np.degrees(theta_r_e), 2)
        diff_deg_val = round(abs(np.degrees(theta_r_o - theta_r_e)), 2)

        st.info(f"**📊 계산 결과 (Ray Trajectory Data):**\n"
                f"* 복굴절률 차이 (Δn = n_e - n_o): `{delta_n_val:+.4f}`\n"
                f"* o-ray 굴절각: `{ro_deg_val}°`\n"
                f"* e-ray 굴절각: `{re_deg_val}°`\n"
                f"* 광선 분리 각도 (Δθ): `{diff_deg_val}°`")

# =============================================================================
# TAB 2: 광탄성 응력 해석 (Photoelasticity)
# =============================================================================
with tab2:
    st.header("🔧 광탄성 응력 무늬 및 편광기 시뮬레이션")
    st.caption("외부 응력을 받는 투명 고분자 시험편이 시클로-광탄성 효과에 의해 무지개 색상의 간섭 무늬(Isochromatics)를 생성하는 현상입니다.")

    c1, c2 = st.columns([1, 2])

    with c1:
        st.subheader("🎛️ 시험편 및 응력 조건 설정")
        model_type = st.selectbox(
            "하중 시험편 형태 선택",
            ["3점 굽힘 보 (3-Point Bending Beam)", "원형 압축 링 (Compressed Ring)", "노치 인장판 (Notched Bar)"],
            key="tab2_model"
        )

        load_force = st.slider("인가 하중 / 응력 크기 (Load, N)", 10, 200, 80, step=5, key="tab2_force")
        fringe_constant = st.slider("재료 광탄성 정수 (C, GPa⁻¹)", 0.5, 5.0, 2.0, step=0.1, key="tab2_C")
        pol_mode = st.radio("편광기 구성 (Polariscope Type)", ["평면 편광기 (Plane Polariscope)", "원 편광기 (Circular Polariscope)"], key="tab2_pol")
        show_isoclinic = (pol_mode == "평면 편광기 (Plane Polariscope)")

    with c2:
        nx, ny = 300, 150
        x = np.linspace(-2, 2, nx)
        y = np.linspace(-1, 1, ny)
        X, Y = np.meshgrid(x, y)

        if model_type == "3점 굽힘 보 (3-Point Bending Beam)":
            M = load_force * (2.0 - np.abs(X))
            sigma_x = M * Y * 3.0
            sigma_y = np.zeros_like(X)
            tau_xy = -load_force * np.sign(X) * (1 - Y**2) * 0.5
        else:
            R_outer, R_inner = 1.0, 0.4
            r = np.sqrt(X**2 + Y**2)
            r = np.maximum(r, 0.01)
            mask = (r < R_inner) | (r > R_outer)
            sigma_x = load_force * (1 - (R_inner/r)**2) * np.cos(2*np.arctan2(Y, X))
            sigma_y = -load_force * (1 + (R_inner/r)**2) * np.sin(2*np.arctan2(Y, X))
            tau_xy = load_force * (R_inner/r)**2 * np.sin(2*np.arctan2(Y, X))
            sigma_x[mask] = 0
            sigma_y[mask] = 0
            tau_xy[mask] = 0

        center_stress = (sigma_x + sigma_y) / 2.0
        radius_stress = np.sqrt(((sigma_x - sigma_y) / 2.0)**2 + tau_xy**2)
        
        sigma_1 = center_stress + radius_stress
        sigma_2 = center_stress - radius_stress

        theta_p = 0.5 * np.arctan2(2 * tau_xy, sigma_x - sigma_y)
        delta = fringe_constant * (sigma_1 - sigma_2)

        lambda_r, lambda_g, lambda_b = 650, 540, 450
        
        I_r = np.sin(delta * 1000 / lambda_r)**2
        I_g = np.sin(delta * 1000 / lambda_g)**2
        I_b = np.sin(delta * 1000 / lambda_b)**2

        if show_isoclinic:
            isoclinic_factor = np.sin(2 * theta_p)**2
            I_r *= isoclinic_factor
            I_g *= isoclinic_factor
            I_b *= isoclinic_factor

        RGB = np.stack([I_r, I_g, I_b], axis=-1)
        RGB = np.clip(RGB, 0, 1)

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.imshow(RGB, extent=[-2, 2, -1, 1])
        ax2.set_title("Photoelastic Stress Pattern (" + pol_mode + ")", fontsize=12, fontweight='bold')
        ax2.set_xlabel("X (cm)")
        ax2.set_ylabel("Y (cm)")
        
        st.pyplot(fig2)
        plt.close(fig2)

        st.success("""
        💡 **관찰 포인트:**
        * **등색선 (Isochromatic Fringes):** 무지개 색상 띠의 밀도가 높은 곳이 **응력 집중(Stress Concentration)** 지역입니다.
        * **등경사선 (Isoclinics):** 평면 편광기 모드의 검은색 띠는 **주응력 방향이 편광축과 일치하는 위치**를 의미합니다.
        """)

# =============================================================================
# TAB 3: 이론 및 수식 정리
# =============================================================================
with tab3:
    st.header("📚 광학적 이방성 & 광탄성 수학적 모델")

    st.subheader("1. 광학적 이방체 및 복굴절 (Birefringence)")
    st.write("""
    등방성 매질(공기, 유리)에서는 빛의 속도가 방향에 상관없이 일정하지만, 이방성 결정(방해석, 수정 등)에서는 결정축 방향에 따라 굴절률이 달라집니다.
    """)
    
    st.markdown("**정상광선 (Ordinary Ray, $o$-ray) 굴절률:**")
    st.latex(r"n_o = \text{Constant}")

    st.markdown("**비정상광선 (Extraordinary Ray, $e$-ray) 유효 굴절률 ($n_e(\theta)$):**")
    st.latex(r"\frac{1}{n_e^2(\theta)} = \frac{\cos^2\theta}{n_o^2} + \frac{\sin^2\theta}{n_e^2}")

    st.markdown("---")

    st.subheader("2. 광탄성 법칙 (Photoelasticity & Stress-Optic Law)")
    st.write("""
    외부 응력을 받는 투명 변형체에 편광을 통과시키면 주응력 차이에 비례하여 위상차가 발생합니다.
    """)

    st.markdown("**Brewster의 광탄성 법칙:**")
    st.latex(r"n_1 - n_2 = C (\sigma_1 - \sigma_2)")

    st.markdown("**상대 위상차 (Relative Retardation, $\delta$):**")
    st.latex(r"\delta = \frac{2\pi d}{\lambda} (n_1 - n_2) = \frac{2\pi d}{\lambda} C (\sigma_1 - \sigma_2)")

    st.markdown("""
    * $n_1, n_2$: 주응력 방향의 굴절률
    * $\sigma_1, \sigma_2$: 주응력 (Principal Stresses)
    * $C$: 재료의 광탄성 계수 (Stress-Optic Coefficient)
    * $d$: 시험편의 두께, $\lambda$: 투과하는 빛의 파장
    """)
