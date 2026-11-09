# 1. 수치 계산 영역 (광선 궤적 및 유효 굴절률 계산)
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

        # 2. 다크 테마 기반 스타일 렌더링
        fig1, ax1 = plt.subplots(figsize=(9, 6.5), facecolor='#0e1117')
        ax1.set_facecolor('#0e1117')
        
        # 배경 영역 (공기 vs 결정)
        ax1.fill_between([-4, 4], 0, 4, color='#1a2436', alpha=0.7, label="Air (n=1.0)")
        ax1.fill_between([-4, 4], -4, 0, color='#161b26', alpha=0.9, label="Crystal Medium")
        ax1.axhline(0, color='#ffffff', lw=2, linestyle='-', alpha=0.9)
        ax1.axvline(0, color='#888888', linestyle=':', alpha=0.6, label="Normal Line")

        # 입사광선 (Glow 레이어링으로 광원 느낌 표현)
        x_inc = [-3 * np.tan(theta_i), 0]
        y_inc = [3, 0]
        ax1.plot(x_inc, y_inc, color=light_color, lw=6, alpha=0.3)
        ax1.plot(x_inc, y_inc, color=light_color, lw=2.5, label="Incident Ray")

        # 정상광선 (o-ray: 파란색 Glow 적용)
        x_o = [0, 3.5 * np.sin(theta_r_o)]
        y_o = [0, -3.5 * np.cos(theta_r_o)]
        ax1.plot(x_o, y_o, color='#29b6f6', lw=5, alpha=0.25)
        ax1.plot(x_o, y_o, color='#29b6f6', lw=2.5, linestyle='-', label=f"o-ray (n_o={n_o:.3f})")

        # 비정상광선 (e-ray: 빨간색/주황색 점선 Glow 적용)
        x_e = [0, 3.5 * np.sin(theta_r_e)]
        y_e = [0, -3.5 * np.cos(theta_r_e)]
        ax1.plot(x_e, y_e, color='#ff5252', lw=5, alpha=0.25)
        ax1.plot(x_e, y_e, color='#ff5252', lw=2.5, linestyle='--', label=f"e-ray (n_eff={n_e_eff:.3f})")

        # 광축 가이드 라인 및 화살표 (Optic Axis Visualizer)
        oa_dx = np.cos(theta_OA)
        oa_dy = -np.sin(theta_OA)
        ax1.plot([-2 * oa_dx, 2 * oa_dx], [-2 - 2 * oa_dy, -2 + 2 * oa_dy], color='#ab47bc', linestyle='-.', alpha=0.4, lw=1.2)
        ax1.quiver(0, -2, oa_dx, oa_dy, scale=3, color='#ab47bc', alpha=0.9, width=0.008, label=f"Optic Axis ({optic_axis_deg}°)")

        # 경계 입사점 피크 강조
        ax1.scatter([0], [0], color='#ffffff', s=40, zorder=5)

        # 그래픽 범위 및 격자 라인 세팅
        ax1.set_xlim(-3, 3)
        ax1.set_ylim(-3.5, 3)
        ax1.set_aspect('equal')
        
        # 축 및 타이틀 색상 변경
        ax1.set_title("Ray Splitting in Anisotropic Crystal", fontsize=13, fontweight='bold', color='#ffffff', pad=12)
        ax1
