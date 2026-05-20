# ===================================================================================================
# MÓDULO A: PROPAGACIÓN Y MECÁNICA DE PARTÍCULAS
# ===================================================================================================
with tab_workspace[0]:
    col_g1, col_c1 = st.columns([5, 3])
    
    with col_c1:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        st.subheader("⚙️ Propiedades Termofísicas del Medio")
        medio_index = st.selectbox(
            "Medio de Propagación (Velocidad de Fase):", 
            ["Aire Estándar (Gaseoso ~343 m/s)", "Agua Destilada (Líquido ~1533 m/s)", "Acero Estructural (Sólido ~3560 m/s)"]
        )
        v_fase = 343.0 if "Aire" in medio_index else 1533.0 if "Agua" in medio_index else 3560.0
        
        st.markdown("---")
        st.subheader("⚡ Parámetros de la Fuente de Excitación")
        amplitud_móvil = st.slider("Amplitud de Presión Máxima (P₀) [Pa]", 0.5, 3.0, 1.5, step=0.1)
        frec_hz = st.number_input("Frecuencia de la Fuente (f) [Hz]", min_value=50.0, max_value=500.0, value=220.0, step=20.0)
        tiempo_instante = st.number_input("Tiempo de Observación (t) [s]", min_value=0.00, value=0.00, step=0.002, format="%.3f", key="p_time")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**Ecuación de Desplazamiento Molecular:**")
        omega_rad = 2 * np.pi * frec_hz
        k_num = omega_rad / v_fase
        st.latex(rf"\xi(x,t) = \xi_{{max}} \cdot \sin(k x - \omega t)")
        st.caption(f"Número de onda (k): {k_num:.3f} rad/m | Frecuencia angular (ω): {omega_rad:.1f} rad/s")

    with col_g1:
        # ---- 1. GRÁFICA DE PARTÍCULAS (DENSIDAD) ----
        np.random.seed(42)
        total_particulas = 1500
        x_estatico = np.random.uniform(0.2, 9.8, total_particulas)
        y_estatico = np.random.uniform(-3, 3, total_particulas)
        
        desplazamiento_longitudinal = (amplitud_móvil * 0.15) * np.sin(k_num * x_estatico - omega_rad * tiempo_instante)
        x_dinamico = x_estatico + desplazamiento_longitudinal
        
        fig_particulas = go.Figure(data=go.Scatter(
            x=x_dinamico, y=y_estatico, mode='markers',
            marker=dict(color='#b39ddb', size=3, opacity=0.6)
        ))
        fig_particulas.update_layout(
            template="plotly_dark",
            title="Perturbación Longitudinal y Zonas de Compresión/Rarefacción",
            xaxis=dict(title="Posición Axial en la Cámara (m)", range=[0, 10], showgrid=True, gridcolor='#222'),
            yaxis=dict(title="Espacio Transversal (m)", range=[-3.5, 3.5], showgrid=False),
            margin=dict(l=40, r=40, t=40, b=20),
            height=280,
            plot_bgcolor='#0e0e12', paper_bgcolor='#0f0f14'
        )
        st.plotly_chart(fig_particulas, use_container_width=True)

        # ---- 2. NUEVA GRÁFICA: ONDA CONTINUA (ESTILO TU SEGUNDA IMAGEN) ----
        # Generamos un barrido continuo de posiciones X para dibujar la función matemática pura
        x_continuo = np.linspace(0, 10, 500)
        # Calculamos la elongación matemática en cada punto
        y_continuo = amplitud_móvil * np.sin(k_num * x_continuo - omega_rad * tiempo_instante)

        fig_onda = go.Figure()
        # Línea de la onda (Color cian brillante como tu imagen de referencia)
        fig_onda.add_trace(go.Scatter(
            x=x_continuo, y=y_continuo,
            mode='lines',
            line=dict(color='#00e5ff', width=2.5)
        ))
        # Relleno sutil debajo de la curva para mejorar la estética visual
        fig_onda.add_trace(go.Scatter(
            x=x_continuo, y=y_continuo,
            mode='lines',
            fill='tozeroy',
            fillcolor='rgba(0, 229, 255, 0.05)',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig_onda.update_layout(
            template="plotly_dark",
            title="Perfil Continuo de la Onda de Presión Acústica $\Psi(x,t)$",
            xaxis=dict(title="Posición x (m)", range=[0, 10], showgrid=True, gridcolor='#222'),
            yaxis=dict(title="Desplazamiento y (m)", range=[-amplitud_móvil - 0.5, amplitud_móvil + 0.5], showgrid=True, gridcolor='#222'),
            margin=dict(l=40, r=40, t=40, b=40),
            height=280,
            plot_bgcolor='#0e0e12', paper_bgcolor='#0f0f14',
            showlegend=False
        )
        st.plotly_chart(fig_onda, use_container_width=True)
