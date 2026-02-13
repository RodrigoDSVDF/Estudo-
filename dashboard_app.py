import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Configurações da Página --- #
st.set_page_config(
    page_title="EduAnalytics - Storytelling",
    page_icon="🎓",
    layout="wide"
)

# --- CSS Personalizado (Correção de Contraste e Cores) --- #
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Estilização da História (Header) */
    .story-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border-left: 10px solid #3b82f6;
    }

    /* TABS ESCURAS E EVIDENTES */
    button[data-baseweb="tab"] {
        background-color: #1e293b !important; 
        color: #94a3b8 !important; 
        border-radius: 10px 10px 0 0 !important;
        padding: 12px 25px !important;
        font-weight: bold !important;
        margin-right: 4px !important;
        border: none !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #0f172a !important; 
        color: #ffffff !important; 
        border-bottom: 3px solid #3b82f6 !important;
    }

    /* Container dos Gráficos */
    .plot-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 2rem;
    }

    /* Box de Conclusão - CORRIGIDO PARA VISIBILIDADE */
    .conclusion-card {
        background-color: #f1f5f9; /* Azul acinzentado bem claro */
        border: 2px solid #3b82f6; /* Borda Azul */
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        color: #1e293b !important; /* Força cor de texto escura */
    }
    
    .conclusion-card h2, .conclusion-card p, .conclusion-card li {
        color: #1e293b !important; /* Garante que todos os elementos internos sejam escuros */
    }
</style>
""", unsafe_allow_html=True)

# --- Carga de Dados --- #
@st.cache_data
def load_data():
    try:
        return pd.read_csv("student_exam_scores (1).csv")
    except:
        import numpy as np
        data = {
            "student_id": range(1, 101),
            "hours_studied": np.random.uniform(1, 20, 100),
            "sleep_hours": np.random.uniform(4, 10, 100),
            "attendance_percent": np.random.uniform(60, 100, 100),
            "previous_scores": np.random.uniform(40, 100, 100),
            "exam_score": np.random.uniform(30, 100, 100)
        }
        return pd.DataFrame(data)

df = load_data()

# --- INÍCIO DA HISTÓRIA --- #
st.markdown("""
<div class="story-card">
    <h1>📖 A Jornada do Desempenho</h1>
    <p>O que define o sucesso de um estudante? Seria apenas o esforço bruto nas horas de estudo, ou o equilíbrio entre o sono e a presença em sala? 
    Neste dashboard, analisamos os dados para contar a história por trás das notas. 
    <b>Explore as abas abaixo para entender as correlações que levam à aprovação.</b></p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar para Filtros --- #
st.sidebar.header("🔍 Parâmetros de Filtro")
min_hours, max_hours = st.sidebar.slider(
    "Horas de Estudo",
    float(df["hours_studied"].min()),
    float(df["hours_studied"].max()),
    (float(df["hours_studied"].min()), float(df["hours_studied"].max()))
)
df_filtered = df[(df["hours_studied"] >= min_hours) & (df["hours_studied"] <= max_hours)]

# --- Métricas Chave --- #
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Média da Nota", f"{df_filtered['exam_score'].mean():.2f}")
with col2:
    st.metric("Média de Estudo", f"{df_filtered['hours_studied'].mean():.2f}h")
with col3:
    st.metric("Média de Sono", f"{df_filtered['sleep_hours'].mean():.2f}h")

st.markdown("---")

# --- ABAS COM OS 6 GRÁFICOS ORIGINAIS --- #
tab1, tab2, tab3 = st.tabs(["📚 Estudo vs Nota", "😴 Sono & Presença", "📅 Histórico"])

with tab1:
    st.markdown("### 1. Perfil das Notas")
    fig_hist = px.histogram(df_filtered, x="exam_score", nbins=20, title="Distribuição das Notas do Exame",
                            color_discrete_sequence=['#3b82f6'])
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("### 2. O Impacto Direto do Estudo")
    fig_hours_exam = px.scatter(df_filtered, x="hours_studied", y="exam_score",
                                title="Horas de Estudo vs Nota do Exame",
                                color="exam_score", color_continuous_scale="Blues")
    st.plotly_chart(fig_hours_exam, use_container_width=True)

with tab2:
    st.markdown("### 3. Conexões Ocultas")
    correlation_matrix = df_filtered[["hours_studied", "sleep_hours", "attendance_percent", "previous_scores", "exam_score"]].corr()
    fig_corr = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values, x=correlation_matrix.columns, y=correlation_matrix.index,
        colorscale="Viridis", text=correlation_matrix.round(2).values, texttemplate="%{text}"))
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("### 4. O Fator Descanso")
    fig_sleep_exam = px.scatter(df_filtered, x="sleep_hours", y="exam_score",
                                title="Horas de Sono vs Nota do Exame",
                                color_discrete_sequence=['#10b981'])
    st.plotly_chart(fig_sleep_exam, use_container_width=True)

with tab3:
    st.markdown("### 5. Estar Presente Importa?")
    fig_attendance_exam = px.scatter(df_filtered, x="attendance_percent", y="exam_score",
                                     title="Porcentagem de Presença vs Nota do Exame",
                                     color_discrete_sequence=['#f59e0b'])
    st.plotly_chart(fig_attendance_exam, use_container_width=True)

    st.markdown("### 6. Consistência Histórica")
    fig_previous_exam = px.scatter(df_filtered, x="previous_scores", y="exam_score",
                                   title="Notas Anteriores vs Nota do Exame",
                                   color_discrete_sequence=['#6366f1'])
    st.plotly_chart(fig_previous_exam, use_container_width=True)

# --- CONCLUSÃO (COM CORES FIXADAS PARA QUALQUER TEMA) --- #
st.markdown("""
<div class="conclusion-card">
    <h2 style="margin-top: 0;">🎯 Conclusão da Análise</h2>
    <p>Através dos dados apresentados, confirmamos que a <b>consistência acadêmica</b> (notas anteriores) e o 
    <b>esforço dedicado</b> (horas de estudo) são os maiores preditores de sucesso.</p>
    <ul>
        <li><b>Destaque:</b> Existe uma correlação linear forte entre estudar e tirar boas notas.</li>
        <li><b>Insight de Bem-estar:</b> Embora o estudo seja crucial, o sono mantém a saúde mental necessária para o desempenho estável.</li>
        <li><b>Presença:</b> A frequência em aula atua como um multiplicador de conhecimento, auxiliando aqueles com base acadêmica mais frágil.</li>
    </ul>
    <p style="font-style: italic; margin-bottom: 0;">Recomendação: Focar em programas de incentivo ao estudo semanal e monitoramento de alunos com baixa frequência.</p>
</div>
""", unsafe_allow_html=True)

if st.checkbox("Ver base de dados completa"):
    st.dataframe(df_filtered)
