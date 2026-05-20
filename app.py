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

st.caption("Consola analítica avanzada para el procesamiento de modos armónicos y cinemática de fluidos.")

st.markdown("---")



# Interfaz segmentada por canales operacionales

tab_workspace = st.tabs(["[MÓDULO-A] DINÁMICA DE PARTICULACIÓN", "[MÓDULO-B] ARREGLO DOPPLER", "[MÓDULO-C] MAPA DE RESONANCIA DE CAVIDADES"])



# ===================================================================================================

# MÓDULO A: DINÁMICA DE PARTICULACIÓN (MORADO SUAVE)

# ===================================================================================================

with tab_workspace[0]:

    col_g1, col_c1 = st.columns([5, 3])

   

    with col_c1:

        st.markdown('<div class="control-panel">', unsafe_allow_html=True)

        st.subheader("⚙️ Propiedades del Fluido")

        medio_index = st.selectbox("Coeficiente del Medio:", ["Fase Gaseosa (Aire Estándar)", "Fase Líquida (Medio Acuático)", "Fase Sólida (Matriz Cúbica)"])

        v_fase = 343.0 if "Gaseosa" in medio_index else 1533.0 if "Líquida" in medio_index else 3560.0

       

        st.markdown("---")

        st.subheader("⚡ Parámetros del Estimulador")

        amplitud_móvil = st.slider("Cresta de Presión (P0)", 0.5, 3.0, 1.5, step=0.1)

        frec_hz = st.number_input("Entrada de Frecuencia (F) [Hz]", min_value=50.0, max_value=500.0, value=220.0, step=20.0)

        tiempo_instante = st.number_input("Punto de Tiempo (t) [s]", min_value=0.00, value=0.00, step=0.01, format="%.2f", key="p_time")

        st.markdown('</div>', unsafe_allow_html=True)

       

        st.markdown("**Formulación de Desplazamiento Molecular:**")

        omega_rad = 2 * np.pi * frec_hz

        k_num = omega_rad / v_fase

        st.latex(rf"\xi(x,t) = \xi_{{max}} \cdot \sin(k x - \omega t)")



    with col_g1:

        np.random.seed(42)

        total_particulas = 1500

        x_estatico = np.random.uniform(0, 10, total_particulas)

        y_estatico = np.random.uniform(-3, 3, total_particulas)

       

        desplazamiento_longitudinal = (amplitud_móvil * 0.35) * np.sin(k_num * x_estatico - omega_rad * tiempo_instante)

        x_dinamico = x_estatico + desplazamiento_longitudinal

       

        fig_particulas = go.Figure(data=go.Scatter(

            x=x_dinamico, y=y_estatico, mode='markers',

            marker=dict(color='#b39ddb', size=3, opacity=0.5)

        ))

        fig_particulas.update_layout(

            template="plotly_dark",

            title="Distribución Longitudinal de Partículas (Densidad de Presión)",

            xaxis=dict(title="Longitud de la Cámara (m)", range=[0, 10], showgrid=False),

            yaxis=dict(title="Corte Transversal (m)", range=[-3.5, 3.5], showgrid=False),

            plot_bgcolor='#0e0e12', paper_bgcolor='#0f0f14'

        )

        st.plotly_chart(fig_particulas, use_container_width=True)



# ===================================================================================================

# MÓDULO B: ARREGLO DOPPLER (MORADO SUAVE)

# ===================================================================================================

with tab_workspace[1]:

    col_g2, col_c2 = st.columns([5, 3])

   

    with col_c2:

        st.markdown('<div class="control-panel">', unsafe_allow_html=True)

        st.subheader("🚨 Dinámica Vectorial")

        f_emision_dop = st.number_input("Frecuencia Base (f0) [Hz]", value=160.0, step=10.0)

        v_vector_dop = st.slider("Velocidad de la Fuente (vs) [m/s]", 0.0, 300.0, 120.0, step=20.0)

        st.markdown('</div>', unsafe_allow_html=True)

       

        st.markdown("**Ecuación Cinematico-Angular:**")

        st.latex(r"f_{ang} = f_0 \left[ \frac{c_{medio}}{c_{medio} - v_s \cos(\theta)} \right]")

       

    with col_g2:

        angulos_radar = np.array([0, 30, 60, 90, 120, 150, 180])

        c_aire = 343.0

        frecuencias_percibidas = f_emision_dop * (c_aire / (c_aire - v_vector_dop * np.cos(np.radians(angulos_radar))))

       

        fig_barras_dop = go.Figure(data=go.Bar(

            x=[f"Sensor {a}°" for a in angulos_radar], y=frecuencias_percibidas,

            marker_color='#9575cd', text=[f"{f:.1f} Hz" for f in frecuencias_percibidas], textposition='auto'

        ))

        fig_barras_dop.update_layout(

            template="plotly_dark", title="Espectro Captado por Nodos de Monitoreo Angular",

            xaxis_title="Orientación del Captador (θ)", yaxis_title="Frecuencia Registrada (Hz)",

            plot_bgcolor='#0e0e12', paper_bgcolor='#0f0f14'

        )

        st.plotly_chart(fig_barras_dop, use_container_width=True)



# ===================================================================================================

# MÓDULO C: MAPA DE RESONANCIA (2D MAP CON FORMULACIÓN MUTADA)

# ===================================================================================================

with tab_workspace[2]:

    col_g3, col_c3 = st.columns([5, 3])

   

    with col_c3:

        st.markdown('<div class="control-panel">', unsafe_allow_html=True)

        st.subheader("📐 Geometría de la Guía")

       

        # Cambiamos las etiquetas por definiciones físicas formales

        frontera_tipo = st.radio(

            "Condiciones de Contorno de la Cavidad:",

            ["Simétrica (Simetría de Presión Libre-Libre)", "Asimétrica (Restricción Nodo-Antinodo)"]

        )

        indice_modo_m = st.slider("Índice de Modo Activo (m)", 1, 5, 2, step=1)

        longitud_caligrafica = st.number_input("Extensión de la Guía (ℒ) [m]", min_value=0.5, max_value=5.0, value=3.0, step=0.5)

        st.markdown('</div>', unsafe_allow_html=True)

       



    with col_g3:

        # Recuperamos el mapa de calor continuo 2D pero con la estética lavanda suave

        c_sonido_base = 343.0

       

        if "Simétrica" in frontera_tipo:

            nu_eigen = (indice_modo_m * c_sonido_base) / (2 * longitud_caligrafica)

        else:

            nu_eigen = ((2 * indice_modo_m - 1) * c_sonido_base) / (4 * longitud_caligrafica)

           

        st.info(f"🎯 Eigenfrecuencia Fundamental Computada ($\nu_m$): {nu_eigen:.2f} Hz")

       

        # Configuración del mapa de calor continuo

        k_eigen = (2 * np.pi * nu_eigen) / c_sonido_base

        x_plano = np.linspace(0, longitud_caligrafica, 180)

        y_plano = np.linspace(-0.5, 0.5, 90)

        X_mat, Y_mat = np.meshgrid(x_plano, y_plano)

       

        # Simulación de la distribución de ondas estacionarias espaciales

        Z_presion_interna = np.sin(k_eigen * X_mat) * np.cos(Y_mat * np.pi)

       

        # Gráfica de contorno continuo con escala de grises a lavanda suave

        fig_mapa_2d = go.Figure(data=go.Contour(

            z=Z_presion_interna, x=x_plano, y=y_plano,

            colorscale=[[0, '#0f0f14'], [0.5, '#512da8'], [1, '#b39ddb']],

            contours_coloring='heatmap',

            line_width=0,

            showscale=True

        ))

        fig_mapa_2d.update_layout(

            template="plotly_dark",

            title="Distribución de Antinodos de Presión Estacionaria (Perfil de Contorno)",

            xaxis_title="Eje de Extensión Longitudinal (m)",

            yaxis_title="Eje Transversal",

            plot_bgcolor='#0e0e12', paper_bgcolor='#0f0f14'

        )

        st.plotly_chart(fig_mapa_2d, use_container_width=True)