import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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
        
        material_choice = st.selectbox(
            "대표적인 이방성 결정 선택",
            ["방해석 (Calcite)", "수정 (Quartz)", "금강석/루틸 (Rutile)", "사용자 정의"]
        )

        if material_choice == "방해석 (Calcite)":
            default_no, default_ne = 1.658, 1.486
        elif material_choice == "수정 (Quartz)":
            default_no, default_ne = 1.544, 1.553
        elif material_choice == "금강석/루틸 (Rutile)":
            default_no, default_ne = 2.616, 2.903
        else:
            default_no, default_ne = 1.600, 1.450

        n_o = st.slider("정상광선 굴절률 (n_o)", 1.000, 3.000, default_no, step=0.001)
        n_e = st.slider("비정상광선 굴절률 (n_e)", 1.000, 3.000, default_ne, step=0.001)
        
        optic_axis_deg = st.slider("광축 각도 (Optic Axis Angle, θ_OA)", 0, 90, 45, step=1)
        incident_angle_deg = st.slider("입사각 (Incident Angle, θ_i)", 0, 75, 30, step=1)
        wavelength_nm = st.slider("입사광 파장 (Wavelength, nm)", 400, 700, 550, step=10)

        # 색상 계산 (파장에 따른 대략적인 RGB)
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
        # 스넬의 법칙 및 굴절각 계산
        theta_i = np.radians(incident_angle_deg)
        theta_OA = np.radians(optic_axis_deg)

        # o-ray 굴절각 (스넬 법칙: n_air * sin(θ_i) = n_o * sin(θ_r_o))
        sin_theta_ro = np.sin(theta_i) / n_o
        theta_r_o = np.arcsin(np.clip(sin_theta_ro, -1.0, 1.0))

        # e-ray 유효 굴절률 근사 (타원체 모델)
        # n_e(θ) = 1 / sqrt( (cos(θ)/n_o)^2 + (sin(θ)/n_e)^2 )
        # 단순화된 광선 궤적 시각화 모델
        n_e_eff = 1.0 / np.sqrt((np.cos(theta_OA) / n_o)**2 + (np.sin(theta_OA) / n_e)**2)
        sin_theta_re = np.sin(theta_i) / n_e_eff
        theta_r_e = np.arcsin(np.clip(sin_theta_re, -1.0, 1.0))

        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # 공기 및 결정 경계
        ax.fill_between([-4, 4], 0, 4, color='#e0f7fa', alpha=0.3, label="공기 (Air, n=1.0)")
        ax.fill_between([-4, 4], -4, 0, color='#e8eaf6', alpha=0.5, label=f"결정 ({material_choice})")
        ax.axhline(0, color='black', lw=2)
        ax.axvline(0, color='gray', linestyle='--', alpha=0.7, label="법선 (Normal)")

        # 입사광 경로
        x_inc = [-3 * np.tan(theta_i), 0]
        y_inc = [3, 0]
        ax.plot(x_inc, y_inc, color=light_color, lw=3, label="입사 비편광 (Unpolarized Ray)")

        # o-ray 경로 (정상 광선 - s-편광 계열)
        x_o = [0, 3 * np.sin(theta_r_o)]
        y_o = [0, -3 * np.cos(theta_r_o)]
        ax.plot(x_o, y_o, color='#1e88e5', lw=2.5, linestyle='-', label=f"o-ray (정상광선, n_o={n_o:.3f})")

        # e-ray 경로 (비정상 광선 - p-편광 계열)
        x_e = [0, 3 * np.sin(theta_r_e)]
        y_e = [0, -3 * np.cos(theta_r_e)]
        ax.plot(x_e, y_e, color='#e53935', lw=2.5, linestyle='--', label=f"e-ray (비정상광선, n_eff={n_e_eff:.3f})")

        # 광축 방향 시각화
        oa_dx = np.cos(theta_OA)
        oa_dy = -np.sin(theta_OA)
        ax.quiver(0, -2, oa_dx, oa_dy, scale=3, color='purple', alpha=0.8, label=f"광축 방향 ({optic_axis_deg}°)")

        ax.set_xlim(-3, 3)
        ax.set_ylim(-3.5, 3)
        ax.set_aspect('equal')
        ax.set_title("결정 내부에서의 광선 분리 (Ray Splitting Analysis)")
        ax.legend(loc="lower left", fontsize='small')
        ax.grid(True, linestyle=':', alpha=0.6)

        st.pyplot(fig)

        st.info(f"""
        **📊 분석 결과:**
        * **복굴절률 차이 ($\Delta n = n_e - n_o$):** `{n_e - n_o:+.4f}`
        * **o-ray 굴절각:** `{np.degrees(theta_r_o):.2f}°`
        * **e-ray 굴절각:** `{np.degrees(theta_r_e):.2f}°`
        * **분리 각도 ($\Delta \theta$):** `{abs(np.degrees(theta_r_o - theta_r_e)):.2f}°`
        """)

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
            ["3점 굽힘 보 (3-Point Bending Beam)", "원형 압축 링 (Compressed Ring)", "노치 인장판 (Notched Bar)"]
        )

        load_force = st.slider("인간 하중 / 응력 크기 (Load, N)", 10, 200, 80, step=5)
        fringe_constant = st.slider("재료 광탄성 정수 (C, GPa⁻¹)", 0.5, 5.0, 2.0, step=0.1)
        pol_mode = st.radio("편광기 구성 (Polariscope Type)", ["평면 편광기 (Plane Polariscope)", "원 편광기 (Circular Polariscope)"])
        show_isoclinic = (pol_mode == "평면 편광기 (Plane Polariscope)")

    with c2:
        # 격자 생성 (2D FEM/응력장 대체용 캔버스)
        nx, ny = 300, 150
        x = np.linspace(-2, 2, nx)
        y = np.linspace(-1, 1, ny)
        X, Y = np.meshgrid(x, y)

        if model_type == "3점 굽힘 보 (3-Point Bending Beam)":
            # σx = M * y / I -> 3점 굽힘 보 시뮬레이션
            M = load_force * (2.0 - np.abs(X))
            sigma_x = M * Y * 3.0
            sigma_y = np.zeros_like(X)
            tau_xy = -load_force * np.sign(X) * (1 - Y**2) * 0.5
        elif model_type == "원형 압축 링 (Compressed Ring)":
            R_outer, R_inner = 1.0, 0.4
            r = np.sqrt(X**2 + Y**2)
            mask = (r < R_inner) | (r > R_outer)
            sigma_x = load_force * (1 - (R_inner/r)**2) * np.cos(2*np.arctan2(Y, X))
            sigma_y = -load_force * (1 + (R_inner/r)**2) * np.sin(2*np.arctan2(Y, X))
            tau_xy = load_force * (R_inner/r)**2 * np.sin(2*np.arctan2(Y, X))
            sigma_x[mask] = 0
            sigma_y[mask] = 0
            tau_xy[mask] = 0
        else: # 노치 인장판
            r_notch = np.sqrt(X**2 + Y**2)
            notch_mask = (np.abs(X) < 0.3) & (np.abs(Y) > 0.6)
            kt = 1.0 + 2.5 / (r_notch + 0.2)
            sigma_x = np.zeros_like(X)
            sigma_y = load_force * kt * 0.3
            tau_xy = load_force * 0.05 * X * Y
            sigma_x[notch_mask] = 0
            sigma_y[notch_mask] = 0
            tau_xy[notch_mask] = 0

        # 주응력(Principal Stresses) 계산
        # σ1, σ2 = (σx + σy)/2 ± sqrt(((σx - σy)/2)^2 + τxy^2)
        center_stress = (sigma_x + sigma_y) / 2.0
        radius_stress = np.sqrt(((sigma_x - sigma_y) / 2.0)**2 + tau_xy**2)
        
        sigma_1 = center_stress + radius_stress
        sigma_2 = center_stress - radius_stress
        max_shear = radius_stress  # 최대 전단응력 = (σ1 - σ2)/2

        # 주응력 방향각 (θ_p)
        theta_p = 0.5 * np.arctan2(2 * tau_xy, sigma_x - sigma_y)

        # 위상차 (Retardation δ)
        delta = fringe_constant * (sigma_1 - sigma_2)

        # 간섭 광도 계산 (RGB 무지개 간섭 무늬)
        # I = sin^2(δ / 2) (단색광 기준)
        # 다색광(White light)을 모사하기 위해 R, G, B 채널별로 파장을 다르게 적용
        lambda_r, lambda_g, lambda_b = 650, 540, 450
        
        I_r = np.sin(delta * 1000 / lambda_r)**2
        I_g = np.sin(delta * 1000 / lambda_g)**2
        I_b = np.sin(delta * 1000 / lambda_b)**2

        # 평면 편광기일 경우 경사선(Isoclinics) 효과 추가
        if show_isoclinic:
            isoclinic_factor = np.sin(2 * theta_p)**2
            I_r *= isoclinic_factor
            I_g *= isoclinic_factor
            I_b *= isoclinic_factor

        # RGB 이미지 합성
        RGB = np.stack([I_r, I_g, I_b], axis=-1)
        RGB = np.clip(RGB, 0, 1)

        fig_stress, ax_s = plt.subplots(figsize=(10, 5))
        ax_s.imshow(RGB, extent=[-2, 2, -1, 1])
        ax_s.set_title(f"광탄성 응력 무늬 시뮬레이션 ({pol_mode})", fontsize=14, fontweight='bold')
        ax_s.set_xlabel("X (cm)")
        ax_s.set_ylabel("Y (cm)")
        
        st.pyplot(fig_stress)

        st.success("""
        💡 **관찰 포인트:**
        * **주응력차(Isochromatic Fringes):** 무지개 색상 띠의 밀도가 높을수록 **응력 집중(Stress Concentration)**이 심한 지역입니다.
        * **등경사선(Isoclinics):** 평면 편광기 모드에서 나타나는 검은색 띠는 **주응력 방향이 편광축과 일치하는 위치**를 나타냅니다. (원 편광기를 사용하면 등경사선이 제거되어 pure 응력 크기만 관찰 가능합니다.)
        """)

# =============================================================================
# TAB 3: 이론 및 수식 정리
# =============================================================================
with tab3:
    st.header("📚 수학적 모델 및 원리")

    st.markdown("""
    ### 1. Optical Anisotropy & Birefringence (광학적 이방성 및 복굴절)
    등방성 매질(공기, 유리)에서는 빛의 속도가 방향에 상관없이 일정하지만, 이방성 결정(방해석, 수정 등)에서는 결정축에 따라 굴절률이 달라집니다.
    
    * **정상광선 (Ordinary Ray, $o$-ray):** 모든 방향으로 동일한 굴절률 $n_o$를 가짐 (스넬의 법칙 준수).
    * **비정상광선 (Extraordinary Ray, $e$-ray):** 진행 방향과 광축(Optic Axis)이 이루는 각도 $\\theta$에 따라 유효 굴절률이 변화함:
    
    $$ \\frac{1}{n_e^2(\\theta)} = \\frac{\\cos^2\\theta}{n_o^2} + \\frac{\\sin^2\\theta}{n_e^2} $$

    ---

    ### 2. Photoelasticity (광탄성 법칙)
    평소에는 등방성인 투명 고분자(아크릴, 에폭시 등)에 외부 응력이 가해지면, 응력의 크기에 비례하여 광학적 이방성이 유도됩니다 (**응력 복굴절**).

    * **Brewster의 광탄성 법칙 (Stress-Optic Law):**
    
    $$ n_1 - n_2 = C (\\sigma_1 - \\sigma_2) $$
    
    * $n_1, n_2$: 주응력 방향의 굴절률
    * $\sigma_1, \sigma_2$: 주응력 (Principal Stresses)
    * $C$: 재료 광탄성 계수 (Stress-Optic Coefficient)

    * **투과광의 위상차 (Relative Retardation $\delta$):**
    
    $$ \\delta = \\frac{2\\pi d}{\\lambda} (n_1 - n_2) = \\frac{2\\pi d}{\\lambda} C (\\sigma_1 - \\sigma_2) $$
    
    * $d$: 시험편의 두께, $\lambda$: 빛의 파장
    """)
