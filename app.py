import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Optical Birefringence Simulator", page_icon="💎", layout="wide")

st.title("💎 광학적 이방체 & 복굴절(Birefringence) 시뮬레이터")
st.caption("결정 내부의 광축 방향 및 굴절률차에 의해 비편광이 정상광선(o-ray)과 비정상광선(e-ray)으로 분리되는 현상을 시뮬레이션합니다.")

# 세션 상태 기본값 안전 초기화
if 'tab1_no' not in st.session_state:
    st.session_state['tab1_no'] = 1.658
if 'tab1_ne' not in st.session_state:
    st.session_state['tab1_ne'] = 1.486

def update_material_indices():
    mat = st.session_state.get('tab1_material', '')
    if "Calcite" in mat:
        st.session_state['tab1_no'] = 1.658
        st.session_state['tab1_ne'] = 1.486
    elif "Quartz" in mat:
        st.session_state['tab1_no'] = 1.544
        st.session_state['tab1_ne'] = 1.553
    elif "Rutile" in mat:
        st.session_state['tab1_no'] = 2.616
        st.session_state['tab1_ne'] = 2.903
    elif "Halite" in mat:
        st.session_state['tab1_no'] = 1.544
        st.session_state['tab1_ne'] = 1.544
    elif "Diamond" in mat:
        st.session_state['tab1_no'] = 2.417
        st.session_state['tab1_ne'] = 2.417

tab1, tab2 = st.tabs(["🎮 시뮬레이터", "📚 광축(Optic Axis) 쉽게 이해하기"])

with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("⚙️ 광학 매개변수 설정")

        mat_options = [
            "Calcite (복굴절/일축성 음성 - 방해석)", 
            "Quartz (복굴절/일축성 양성 - 수정)", 
            "Rutile (복굴절/일축성 양성 - 루틸)", 
            "Halite/Glass (단굴절/등방성 - 암염/유리)", 
            "Diamond (단굴절/등방성 - 다이아몬드)", 
            "Custom"
        ]
        
        st.selectbox("결정 재질 선택", mat_options, key="tab1_material", on_change=update_material_indices)
        
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

        fig, ax = plt.subplots(figsize=(9, 6.5), facecolor='#0e1117')
        ax.set_facecolor('#0e1117')
        
        ax.fill_between([-4, 4], 0, 4, color='#1a2436', alpha=0.7, label="Air (n=1.0)")
        ax.fill_between([-4, 4], -4, 0, color='#161b26', alpha=0.9, label="Crystal Medium")
        ax.axhline(0, color='#ffffff', lw=2, linestyle='-', alpha=0.9)
        ax.axvline(0, color='#888888', linestyle=':', alpha=0.6, label="Normal Line")

        x_inc = [-3 * np.tan(theta_i), 0]
        y_inc = [3, 0]
        ax.plot(x_inc, y_inc, color=light_color, lw=6, alpha=0.3)
        ax.plot(x_inc, y_inc, color=light_color, lw=2.5, label="Incident Ray")

        x_o = [0, 3.5 * np.sin(theta_r_o)]
        y_o = [0, -3.5 * np.cos
