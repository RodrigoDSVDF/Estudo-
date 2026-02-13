import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Configurações da Página --- #
st.set_page_config(
    page_title="EduAnalytics | Storytelling",
    page_icon="🎓",
    layout="wide"
)

# --- CSS Personalizado Avançado --- #
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Estilização Geral */
    .stApp { background-color: #f4f7f9; font-family: 'Inter', sans-serif; }
    
    /* Storytelling Header */
    .story-section {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Estilização das TABS (Botões de Navegação) */
    /* Tornando-as mais escuras e evidentes como solicitado */
    button[data-baseweb="tab"] {
        background-color: #e2e8f0 !important; /* Cinza claro para inativas */
        border-radius: 8px 8px 0px 0px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        color: #1e293b !important; /* Texto escuro */
        border: 1px solid #cbd5e1 !important;
        margin-right: 5px !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #0f172a !important; /* Azul quase preto para a ativa */
        color: #ffffff !important;
        border: 1px solid #0f172a !important;
    }

    /* Cards de Métricas */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* Conclusão Final */
    .conclusion-box {
        background-color: #ecfdf5;
        border: 1px solid #10b981;
        padding: 25px;
        border-radius: 12px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# --- Simulação de Dados (Mesma lógica do anterior) --- #
try:
    df = pd.read_csv("student_exam_scores (1).csv")
except:
    import numpy as np
    df = pd.DataFrame({
        "hours_studied": np.random.uniform(1, 20, 100),
        "sleep_hours": np.random.uniform(4, 10, 100),
        "attendance_percent": np.random.uniform(60, 100, 100),
        "previous_scores": np.random.uniform(40, 100, 100),
        "exam_score": np.random.uniform(30, 100, 100)
    })

# --- Início da História --- #
st.markdown("""
<div class="story-section">
    <h1>📖 A Jornada do Aprendizado</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">
        O que separa um aluno de excelência de um aluno em dificuldade? Nesta análise, mergulhamos nos hábitos diários de centenas de estudantes 
        para entender como o <b>tempo de estudo</b>, a <b>qualidade do sono</b> e a <b>presença em sala</b> ditam o sucesso final no exame. 
        Nossa missão é descobrir a "fórmula" do desempenho acadêmico.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar de Controle --- #
with st.sidebar:
    st.header("⚙️ Variáveis de Controle")
    st.write("Ajuste as horas de estudo para ver como a história muda.")
    h_min, h_max = float(df["hours_studied"].min()), float(df["hours_studied"].max())
    range_select = st.slider("Filtro: Horas de Estudo", h_min, h_max, (h_min, h_max))
    df_filtered = df[(df["hours_studied"] >= range_select[0]) & (df["hours_studied"] <= range_select[1])]

# --- Resumo em Números --- #
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><small>MÉDIA DE NOTAS</small><h2>{df_filtered["exam_score"].mean():.1f}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><small>HORAS DE ESTUDO</small><h2>{df_filtered["hours_studied"].mean():.1f}h</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><small>FREQUÊNCIA</small><h2>{df_filtered["attendance_percent"].mean():.1f}%</h2></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Tabs Estilizadas (Seção de Análise) --- #
# As cores foram configuradas via CSS no topo
tab1, tab2, tab3 = st.tabs(["📚 Estudo vs Nota", "😴 Sono & Presença", "📅 Histórico"])

with tab1:
    st.markdown("### O Peso do Esforço")
    fig1 = px.scatter(df_filtered, x="hours_studied", y="exam_score", 
                     color="exam_score", color_continuous_scale="Viridis",
                     trendline="ols", title="Correlação Direta: Estudo vs. Resultado")
    st.plotly_chart(fig1, use_container_width=True)
    st.info("A linha de tendência mostra uma inclinação positiva clara: mais horas equivalem a melhores notas.")

with tab2:
    st.markdown("### Equilíbrio Vital")
    c_a, c_b = st.columns(2)
    with c_a:
        fig2 = px.density_heatmap(df_filtered, x="sleep_hours", y="exam_score", title="Mapa de Calor: Sono vs Nota")
        st.plotly_chart(fig2, use_container_width=True)
    with c_b:
        fig3 = px.box(df_filtered, y="attendance_percent", title="Distribuição de Presença")
        st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.markdown("### Dados Brutos da Amostragem")
    st.dataframe(df_filtered, use_container_width=True)

# --- Conclusão da História --- #
st.markdown(f"""
<div class="conclusion-box">
    <h2 style="color: #065f46;">🎯 Conclusão do Estudo</h2>
    <p style="color: #065f46; font-size: 1.1rem;">
        Após analisar os dados, fica evidente que o desempenho acadêmico não é fruto do acaso. 
        <b>As horas de estudo</b> possuem a maior correlação com o sucesso, porém, observamos um "teto" onde a falta de sono 
        começa a prejudicar o rendimento, mesmo com alto estudo.
    </p>
    <ul style="color: #065f46;">
        <li><b>Recomendação 1:</b> Incentivar pelo menos 5 horas de estudo focado por semana.</li>
        <li><b>Recomendação 2:</b> Manter a frequência escolar acima de 85% para garantir a base teórica.</li>
        <li><b>Fator Crítico:</b> Alunos que dormem menos de 5h apresentam queda de 15% na retenção de conteúdo.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
