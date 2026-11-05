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
                r, g, b = 0.0,
