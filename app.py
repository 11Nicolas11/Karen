import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PANTALLA COMPLETA Y TEMA MORADO SUAVE (LAVANDA TECH)
st.set_page_config(
    page_title="Acoustic Waveguide Engine",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo de Laboratorio Limpio con tonos Lavanda y Violeta Atenuado
st.markdown("""
<style>
    /* Ocultar elementos heredados del sidebar */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
     
    /* Paleta Lavanda Muted */
    .stApp { background-color: #0f0f14; color: #d1c4e9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3 { color: #b39ddb !important; text-shadow: 0 0 5px rgba(179, 157, 219, 0.3); font-weight: 600; }
     
    /* Paneles de calibración interna */
    .control-panel {
        border: 1px solid #7e57c2;
        padding: 22px;
        border-radius: 10px;
        background-color: #161622;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
     
    /* Modificadores de texto en componentes */
    div[data-testid="stMarkdownContainer"] p { color: #e1bee7; }
    input, select { background-color: #1f1f2e !important; color: #b39ddb !important; border: 1px solid #512da8 !important; }
     
    /* Pestañas suavizadas */
    .stTabs [data-baseweb="tab"] { color: #9575cd !important; font-size: 14px; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #b39ddb !important; border-bottom-color: #b39ddb !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🔮 MOTOR DE ANÁLISIS ACÚSTICO Y GUÍAS DE ONDA (v5.2)")
st.caption("Consola computacional para la simulación de campos de presión, modos resonantes y cinemática de fluidos comprensibles.")
st.markdown("---")

# Interfaz segmentada por canales operacionales con nombres académicos rigurosos
tab_workspace = st.tabs([
    "[MÓDULO-A] PROPAGACIÓN Y MECÁNICA DE PARTICULAS", 
    "[MÓDULO-B] EFECTO DOPPLER CINEMÁTICO", 
    "[MÓDULO-C] MODOS PROPIOS EN CAVIDADES RESONANTES"
])

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
        # ---- GRAFICA 1: DISPERSIÓN DE PARTÍCULAS ----
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
            yaxis=dict(title="Desplazamiento Transversal (m)", range=[-3.5, 3.5], showgrid=False),
            height=280,
            margin=dict(l=40, r=40, t=40, b=20),
            plot_bgcolor='#0e0e12', paper_bgcolor='#0f0f14'
        )
        st.plotly_chart(fig_particulas, use_container_width=True)

        # ---- GRAFICA 2: ONDA CONTINUA (TIPO ONDA SENOIDAL CIAN) ----
        x_continuo = np.linspace(0, 10, 500)
        y_continuo = amplitud_móvil * np.sin(k_num * x_continuo - omega_rad * tiempo_instante)

        fig_onda = go.Figure()
        # Trazo de la línea principal (Cian brillante)
        fig_onda.add_trace(go.Scatter(
            x=x_continuo, y=y_continuo,
            mode='lines',
            line=dict(color='#00e5ff', width=2.5)
        ))
        # Efecto de sombreado / área bajo la curva sutil
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
            height=280,
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor='#0e0e12', paper_bgcolor='#0f0f14',
            showlegend=False
        )
        st.plotly_chart(fig_onda, use_container_width=True)

# ===================================================================================================
# MÓDULO B: EFECTO DOPPLER CINEMÁTICO
# ===================================================================================================
with tab_workspace[1]:
    col_g2, col_c2 = st.columns([5, 3])
     
    with col_c2:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        st.subheader("🚨 Cinemática de la Fuente")
        f_emision_dop = st.number_input("Frecuencia de Emisión en Reposo (f₀) [Hz]", value=160.0, step=10.0)
        v_vector_dop = st.slider("Velocidad de la Fuente (v_s) [m/s]", 0.0, 300.0, 120.0, step=10.0)
        st.markdown('</div>', unsafe_allow_html=True)
         
        st.markdown("---")
        st.markdown("**Ecuación General de Efecto Doppler (Aproximación Angular):**")
        st.latex(r"f' = f_0 \left[ \frac{c}{c - v_s \cos(\theta)} \right]")
        st.caption("Donde θ es el ángulo entre el vector velocidad de la fuente y la línea de vista del receptor.")
         
    with col_g2:
        angulos_radar = np.array([0, 30, 60, 90, 120, 150, 180])
        c_aire = 343.0
         
        # Corrección física: Si v_s >= c en subsónico, evitamos indeterminaciones matemáticas
        v_ajustada = min(v_vector_dop, c_aire - 1)
        frecuencias_percibidas = f_emision_dop * (c_aire / (c_aire - v_ajustada * np.cos(np.radians(angulos_radar))))
         
        fig_barras_dop = go.Figure(data=go.Bar(
            x=[f"Receptor {a}°" for a in angulos_radar], y=frecuencias_percibidas,
            marker_color='#9575cd', text=[f"{f:.1f} Hz" for f in frecuencias_percibidas], textposition='auto'
        ))
        fig_barras_dop.update_layout(
            template="plotly_dark", title="Frecuencia Aparente en Función del Ángulo de Observación (θ)",
            xaxis_title="Ubicación Angular del Receptor (θ)", yaxis_title="Frecuencia Percibida f' (Hz)",
            plot_bgcolor='#0e0e12', paper_bgcolor='#0f0f14'
        )
        st.plotly_chart(fig_barras_dop, use_container_width=True)

# ===================================================================================================
# MÓDULO C: MODOS PROPIOS EN CAVIDADES RESONANTES
# ===================================================================================================
with tab_workspace[2]:
    col_g3, col_c3 = st.columns([5, 3])
     
    with col_c3:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        st.subheader("📐 Geometría y Condiciones de Frontera")
         
        frontera_tipo = st.radio(
            "Condiciones de Contorno de la Guía:",
            ["Abierta-Abierta (Extremos en Antinodos de Presión)", "Abierta-Cerrada (Nodo en x=0, Antinodo en x=L)"]
        )
        indice_modo_m = st.slider("Número de Modo Armónico (n)", 1, 5, 2, step=1)
        longitud_caligrafica = st.number_input("Longitud del Tubo/Cavidad (L) [m]", min_value=0.5, max_value=5.0, value=3.0, step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g3:
        c_sonido_base = 343.0
         
        # Cálculo riguroso de Frecuencias Propias (Eigenfrecuencias) según condiciones de contorno
        if "Abierta-Abierta" in frontera_tipo:
            nu_eigen = (indice_modo_m * c_sonido_base) / (2 * longitud_caligrafica)
            f_espacial = lambda X: np.cos((indice_modo_m * np.pi * X) / longitud_caligrafica)
        else:
            nu_eigen = ((2 * indice_modo_m - 1) * c_sonido_base) / (4 * longitud_caligrafica)
            f_espacial = lambda X: np.sin(((2 * indice_modo_m - 1) * np.pi * X) / (2 * longitud_caligrafica))
             
        st.info(f"🎯 Frecuencia Propia Computada (fₙ): {nu_eigen:.2f} Hz")
         
        # Malla continua para el mapa de calor bidimensional
        x_plano = np.linspace(0, longitud_caligrafica, 200)
        y_plano = np.linspace(-0.5, 0.5, 100)
        X_mat, Y_mat = np.meshgrid(x_plano, y_plano)
         
        # Distribución del campo de presión acústica estacionaria P(x, y)
        Z_presion_interna = f_espacial(X_mat) * np.ones_like(Y_mat)
         
        fig_mapa_2d = go.Figure(data=go.Contour(
            z=Z_presion_interna, x=x_plano, y=y_plano,
            colorscale=[[0, '#0f0f14'], [0.5, '#512da8'], [1, '#b39ddb']],
            contours_coloring='heatmap',
            line_width=0,
            showscale=True,
            colorbar=dict(title="Presión Relativa")
        ))
        fig_mapa_2d.update_layout(
            template="plotly_dark",
            title="Distribución Espacial del Campo de Presión Acústica Estacionaria",
            xaxis_title="Dimensión Axial de la Guía de Onda (m)",
            yaxis_title="Dimensión Transversal (m)",
            plot_bgcolor='#0e0e12', paper_bgcolor='#0f0f14'
        )
        st.plotly_chart(fig_mapa_2d, use_container_width=True)
