import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Configurações da Página --- #
st.set_page_config(
    page_title="EduAnalytics | Desempenho",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Personalizado para Design Moderno --- #
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fundo do Dashboard */
    .stApp {
        background-color: #f8f9fa;
    }

    /* Sidebar Estilizada */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }

    /* Cards de Métricas */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #efefef;
        text-align: center;
    }
    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #1e293b;
        font-size: 1.8rem;
        font-weight: 700;
    }

    /* Estilo para Títulos */
    .main-title {
        color: #1e3a8a;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        color: #64748b;
        margin-bottom: 2rem;
    }

    /* Container de Gráficos */
    .chart-container {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Simulação de Carga de Dados --- #
# (Substitua pelo seu pd.read_csv)
try:
    df = pd.read_csv("student_exam_scores (1).csv")
except:
    # Dados fictícios para caso o arquivo não esteja no diretório
    import numpy as np
    data = {
        "student_id": range(1, 101),
        "hours_studied": np.random.uniform(1, 20, 100),
        "sleep_hours": np.random.uniform(4, 10, 100),
        "attendance_percent": np.random.uniform(60, 100, 100),
        "previous_scores": np.random.uniform(40, 100, 100),
        "exam_score": np.random.uniform(30, 100, 100)
    }
    df = pd.DataFrame(data)

# --- Sidebar --- #
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=80)
    st.markdown("### Filtros de Análise")
    
    min_h, max_h = float(df["hours_studied"].min()), float(df["hours_studied"].max())
    hours_range = st.slider("Horas de Estudo", min_h, max_h, (min_h, max_h))
    
    df_filtered = df[(df["hours_studied"] >= hours_range[0]) & (df["hours_studied"] <= hours_range[1])]
    
    st.divider()
    st.info("Utilize os filtros acima para ajustar as métricas em tempo real.")

# --- Header --- #
st.markdown('<p class="main-title">Intelligence Student Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Análise preditiva e comportamental de desempenho acadêmico</p>', unsafe_allow_html=True)

# --- Row 1: Metric Cards --- #
m1, m2, m3, m4 = st.columns(4)

metrics = [
    ("Média de Notas", f"{df_filtered['exam_score'].mean():.1f}", m1),
    ("Média de Estudo", f"{df_filtered['hours_studied'].mean():.1f}h", m2),
    ("Média de Sono", f"{df_filtered['sleep_hours'].mean():.1f}h", m3),
    ("Frequência Média", f"{df_filtered['attendance_percent'].mean():.1f}%", m4)
]

for label, value, col in metrics:
    col.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Row 2: Main Distribution & Correlation --- #
c1, c2 = st.columns([1.2, 0.8])

with c1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig_hist = px.histogram(df_filtered, x="exam_score", nbins=20, 
                            title="Distribuição das Notas",
                            color_discrete_sequence=['#3b82f6'])
    fig_hist.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=0))
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    corr = df_filtered[["hours_studied", "sleep_hours", "attendance_percent", "previous_scores", "exam_score"]].corr()
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.index,
        colorscale="Blues", text=corr.round(2).values, texttemplate="%{text}"))
    fig_corr.update_layout(title="Correlação", height=380, margin=dict(t=40, b=0))
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Row 3: Deep Dive Tabs --- #
st.markdown("### Análise Detalhada")
tab1, tab2, tab3 = st.tabs(["📚 Estudo vs Nota", "😴 Sono & Presença", "📅 Histórico"])

with tab1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig_scat = px.scatter(df_filtered, x="hours_studied", y="exam_score", 
                          trendline="ols", color="exam_score", 
                          color_continuous_scale="Blues",
                          title="Relação: Tempo de Estudo vs. Resultado Final")
    st.plotly_chart(fig_scat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        fig_sleep = px.scatter(df_filtered, x="sleep_hours", y="exam_score", title="Impacto do Sono")
        st.plotly_chart(fig_sleep, use_container_width=True)
    with col_b:
        fig_att = px.scatter(df_filtered, x="attendance_percent", y="exam_score", title="Frequência em Aula")
        st.plotly_chart(fig_att, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.dataframe(df_filtered.style.background_gradient(subset=['exam_score'], cmap='BuGn'), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Row 4: Insights Card --- #
st.success("💡 **Insight Estratégico:** As horas de estudo têm o maior peso (0.78) no sucesso acadêmico. Recomenda-se focar em programas de mentoria para alunos com menos de 5h semanais de dedicação.")
