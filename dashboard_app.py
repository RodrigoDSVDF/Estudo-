import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# --- CONFIGURAÇÕES DA PÁGINA --- #
st.set_page_config(
    page_title="EduAnalytics 2.0 - Storytelling Interativo",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONALIZADO (COM FUNDO ESCURO NA CONCLUSÃO) --- #
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Card de história */
    .story-header {
        background: linear-gradient(145deg, #0b1e33, #163a5c);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border-bottom: 6px solid #3b82f6;
        box-shadow: 0 15px 20px -10px rgba(0,0,0,0.2);
    }
    
    /* Métricas em destaque */
    .metric-card {
        background-color: #f1f5f9;
        padding: 1rem;
        border-radius: 12px;
        border-left: 5px solid #2563eb;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Conclusão dinâmica - AGORA COM FUNDO ESCURO */
    .insight-box {
        background-color: #0f172a;  /* Fundo azul-escuro quase preto */
        border: 1px solid #334155;
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 8px solid #3b82f6;
        color: #f8fafc;  /* Texto claro */
    }
    .insight-box h4, .insight-box li, .insight-box strong {
        color: #ffffff;  /* Garante que títulos e destaques fiquem brancos */
    }
    .insight-box ul {
        color: #e2e8f0;
    }
    
    /* Tooltips e labels */
    .stSlider label, .stSelectbox label {
        font-weight: 600;
        color: #0f172a;
    }
    
    /* Ajuste para abas */
    button[data-baseweb="tab"] {
        background-color: #1e293b !important;
        color: #cbd5e1 !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 10px 20px !important;
        font-weight: 600;
        margin-right: 3px;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #0f172a !important;
        color: white !important;
        border-bottom: 4px solid #3b82f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DADOS COM GERAÇÃO SINTÉTICA REALISTA --- #
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("student_exam_scores.csv")
        st.success("✅ Arquivo real carregado com sucesso!")
        return df
    except FileNotFoundError:
        st.info("ℹ️ Arquivo não encontrado. Gerando dados sintéticos para demonstração.")
        np.random.seed(42)
        n = 500
        
        hours_studied = np.random.normal(10, 4, n).clip(1, 20)
        sleep_hours = np.random.normal(7, 1.2, n).clip(4, 10)
        attendance_percent = np.random.normal(85, 10, n).clip(60, 100)
        previous_scores = np.random.normal(70, 12, n).clip(40, 100)
        
        # Nota do exame com correlações realistas
        exam_score = (
            0.45 * hours_studied +
            0.15 * sleep_hours +
            0.25 * (attendance_percent / 10) +
            0.30 * (previous_scores / 10) +
            np.random.normal(0, 5, n)
        ).clip(30, 100)
        
        df = pd.DataFrame({
            "student_id": range(1, n+1),
            "hours_studied": hours_studied.round(1),
            "sleep_hours": sleep_hours.round(1),
            "attendance_percent": attendance_percent.round(1),
            "previous_scores": previous_scores.round(1),
            "exam_score": exam_score.round(1)
        })
        return df

df = load_data()

# --- FUNÇÕES DE CACHE PARA COMPUTAÇÕES PESADAS --- #
@st.cache_data
def compute_correlation_matrix(_df, cols):
    return _df[cols].corr()

@st.cache_data
def train_regression(_df, feature, target):
    X = _df[[feature]].values.reshape(-1, 1)
    y = _df[target].values
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    return model, r2

# --- SIDEBAR: FILTROS AVANÇADOS --- #
st.sidebar.header("🔍 **Filtros Inteligentes**")
st.sidebar.markdown("Ajuste os controles para refinar a análise:")

# Filtro de horas de estudo
hours_range = st.sidebar.slider(
    "📚 Horas de estudo (semanais)",
    float(df["hours_studied"].min()),
    float(df["hours_studied"].max()),
    (float(df["hours_studied"].min()), float(df["hours_studied"].max())),
    help="Selecione o intervalo de horas dedicadas aos estudos."
)

# Filtro de horas de sono
sleep_range = st.sidebar.slider(
    "😴 Horas de sono (média)",
    float(df["sleep_hours"].min()),
    float(df["sleep_hours"].max()),
    (float(df["sleep_hours"].min()), float(df["sleep_hours"].max())),
    help="Intervalo de horas de sono por noite."
)

# Filtro de presença
attendance_range = st.sidebar.slider(
    "📋 Frequência (%)",
    float(df["attendance_percent"].min()),
    float(df["attendance_percent"].max()),
    (float(df["attendance_percent"].min()), float(df["attendance_percent"].max())),
    help="Percentual de presença em aula."
)

# Filtro de notas anteriores
previous_range = st.sidebar.slider(
    "📝 Notas anteriores",
    float(df["previous_scores"].min()),
    float(df["previous_scores"].max()),
    (float(df["previous_scores"].min()), float(df["previous_scores"].max())),
    help="Intervalo de desempenho em avaliações passadas."
)

# Aplicar todos os filtros
df_filtered = df[
    (df["hours_studied"] >= hours_range[0]) & (df["hours_studied"] <= hours_range[1]) &
    (df["sleep_hours"] >= sleep_range[0]) & (df["sleep_hours"] <= sleep_range[1]) &
    (df["attendance_percent"] >= attendance_range[0]) & (df["attendance_percent"] <= attendance_range[1]) &
    (df["previous_scores"] >= previous_range[0]) & (df["previous_scores"] <= previous_range[1])
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**👥 Alunos na seleção:** `{df_filtered.shape[0]}`")
st.sidebar.markdown(f"**📊 Correlação (Estudo x Nota):** `{df_filtered['hours_studied'].corr(df_filtered['exam_score']):.3f}`")

# --- HEADER COM NARRATIVA --- #
st.markdown("""
<div class="story-header">
    <h1 style="margin:0; font-size:2.5rem;">📘 EduAnalytics 2.0</h1>
    <p style="font-size:1.2rem; opacity:0.9; margin-top:0.5rem;">
        O sucesso acadêmico vai além das horas de estudo. Descubra como sono, frequência e histórico se combinam 
        para prever o desempenho. Use os filtros ao lado para contar <strong>sua própria história</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# --- MÉTRICAS PRINCIPAIS (ENRIQUECIDAS) --- #
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("🎯 Média da Nota", f"{df_filtered['exam_score'].mean():.1f}")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("📚 Mediana de Estudo", f"{df_filtered['hours_studied'].median():.1f}h")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("😴 Mediana de Sono", f"{df_filtered['sleep_hours'].median():.1f}h")
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("📋 Frequência Média", f"{df_filtered['attendance_percent'].mean():.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- ABAS REORGANIZADAS --- #
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Visão Geral", 
    "📚 Estudo & Desempenho", 
    "😴 Bem-estar & Frequência",
    "🤖 Simulador & Insights"
])

with tab1:
    st.subheader("📌 Distribuição e Correlações")
    
    # 1. Histograma das notas
    fig_hist = px.histogram(
        df_filtered, x="exam_score", nbins=25,
        title="Distribuição das Notas no Exame",
        labels={"exam_score": "Nota do Exame"},
        color_discrete_sequence=["#2563eb"],
        opacity=0.8
    )
    fig_hist.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # 2. Mapa de calor otimizado (apenas triângulo inferior)
    st.markdown("#### 🔥 Matriz de Correlação (Triângulo Inferior)")
    cols_corr = ["hours_studied", "sleep_hours", "attendance_percent", "previous_scores", "exam_score"]
    corr_matrix = compute_correlation_matrix(df_filtered, cols_corr)
    
    # Máscara para esconder triângulo superior
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    corr_hidden = corr_matrix.mask(mask)
    
    fig_corr = px.imshow(
        corr_hidden,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        labels=dict(x="Variável", y="Variável", color="Correlação"),
        x=corr_hidden.columns,
        y=corr_hidden.columns
    )
    fig_corr.update_layout(
        width=600, height=600,
        xaxis_title="", yaxis_title=""
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Estatísticas descritivas rápidas
    with st.expander("📋 Estatísticas detalhadas do subconjunto filtrado"):
        st.dataframe(df_filtered.describe().round(2), use_container_width=True)

with tab2:
    st.subheader("⏳ Impacto das Horas de Estudo")
    
    col_left, col_right = st.columns([0.6, 0.4])
    
    with col_left:
        # Scatter com regressão linear
        fig_hours = px.scatter(
            df_filtered, x="hours_studied", y="exam_score",
            trendline="ols", trendline_color_override="red",
            title="Horas de Estudo vs Nota do Exame",
            labels={"hours_studied": "Horas de Estudo (semana)", "exam_score": "Nota no Exame"},
            opacity=0.7, color="exam_score", color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_hours, use_container_width=True)
    
    with col_right:
        st.markdown("##### 📈 Coeficiente de Regressão")
        model_hrs, r2_hrs = train_regression(df_filtered, "hours_studied", "exam_score")
        slope = model_hrs.coef_[0]
        intercept = model_hrs.intercept_
        st.markdown(f"""
        - **Inclinação:** `{slope:.3f}`  
        - **Intercepto:** `{intercept:.1f}`  
        - **R²:** `{r2_hrs:.3f}`  
        """)
        st.info(f"Cada hora extra de estudo está associada a um aumento de **{slope:.2f} pontos** na nota, em média.")
        
        # Boxplot por faixa de estudo
        df_filtered['study_group'] = pd.cut(df_filtered['hours_studied'], bins=4, labels=['Muito baixo', 'Baixo', 'Médio', 'Alto'])
        fig_box = px.box(df_filtered, x='study_group', y='exam_score', 
                         title="Distribuição das notas por grupo de estudo",
                         color_discrete_sequence=['#3b82f6'])
        st.plotly_chart(fig_box, use_container_width=True)

with tab3:
    st.subheader("😴 Sono e Presença – Os Pilares do Equilíbrio")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_sleep = px.scatter(
            df_filtered, x="sleep_hours", y="exam_score",
            trendline="ols", trendline_color_override="green",
            title="Horas de Sono vs Nota",
            labels={"sleep_hours": "Sono (horas)", "exam_score": "Nota"},
            opacity=0.6, color_discrete_sequence=["#10b981"]
        )
        st.plotly_chart(fig_sleep, use_container_width=True)
    
    with col2:
        fig_att = px.scatter(
            df_filtered, x="attendance_percent", y="exam_score",
            trendline="ols", trendline_color_override="orange",
            title="Frequência vs Nota",
            labels={"attendance_percent": "Presença (%)", "exam_score": "Nota"},
            opacity=0.6, color_discrete_sequence=["#f59e0b"]
        )
        st.plotly_chart(fig_att, use_container_width=True)
    
    st.markdown("#### 🔍 Relação entre Presença e Horas de Estudo")
    fig_bubble = px.scatter(
        df_filtered, x="attendance_percent", y="hours_studied", 
        size="exam_score", color="exam_score",
        title="Estudo vs Frequência (tamanho = nota)",
        labels={"attendance_percent": "Presença (%)", "hours_studied": "Horas de Estudo"},
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

with tab4:
    st.subheader("🤖 Simulador de Desempenho e Insights Automáticos")
    
    # --- SIMULADOR PREDITIVO --- #
    st.markdown("##### 🎯 Quanto você precisa estudar para atingir a nota desejada?")
    col_sim1, col_sim2 = st.columns([0.6, 0.4])
    
    with col_sim1:
        target_score = st.slider("Nota alvo:", 30, 100, 75, step=5)
        # Utiliza o modelo treinado com todos os dados (ou filtrados? Melhor com todos para robustez)
        model_full, _ = train_regression(df, "hours_studied", "exam_score")
        hours_needed = (target_score - model_full.intercept_) / model_full.coef_[0]
        hours_needed = np.clip(hours_needed, df["hours_studied"].min(), df["hours_studied"].max())
        
        st.markdown(f"📘 Para atingir **{target_score}** pontos, são necessárias aproximadamente **{hours_needed:.1f}h** de estudo semanais.")
        st.caption("Baseado no modelo linear ajustado com todos os dados históricos.")
    
    with col_sim2:
        st.markdown("##### 📊 Previsão de nota")
        input_hours = st.number_input("Horas de estudo (simulação):", 
                                      min_value=1.0, max_value=20.0, value=10.0, step=0.5)
        pred_score = model_full.predict([[input_hours]])[0]
        st.metric("Nota estimada", f"{pred_score:.1f}")
    
    st.markdown("---")
    
    # --- INSIGHTS AUTOMÁTICOS BASEADOS NO FILTRO --- #
    st.markdown("##### 💡 Insights Personalizados")
    
    # Calcula algumas estatísticas relevantes
    mean_score_filtered = df_filtered['exam_score'].mean()
    mean_score_all = df['exam_score'].mean()
    diff_score = mean_score_filtered - mean_score_all
    
    top_study = df_filtered.nlargest(10, 'exam_score')[['hours_studied', 'sleep_hours', 'attendance_percent']].mean().round(1)
    
    insight_text = f"""
    <div class="insight-box">
        <h4 style="margin-top:0;">🔎 Análise do subconjunto selecionado</h4>
        <ul>
            <li><strong>Média da nota:</strong> {mean_score_filtered:.1f} ({"acima" if diff_score > 0 else "abaixo"} da média geral de {mean_score_all:.1f}).</li>
            <li><strong>Perfil dos 10 melhores alunos:</strong> estudam em média {top_study['hours_studied']}h/semana, dormem {top_study['sleep_hours']}h e têm {top_study['attendance_percent']}% de presença.</li>
    """
    
    # Correlações condicionais
    corr_hours = df_filtered['hours_studied'].corr(df_filtered['exam_score'])
    if corr_hours > 0.6:
        insight_text += f"<li>✅ Forte correlação positiva entre estudo e nota ({corr_hours:.2f}).</li>"
    elif corr_hours > 0.3:
        insight_text += f"<li>📊 Correlação moderada entre estudo e nota ({corr_hours:.2f}).</li>"
    else:
        insight_text += f"<li>⚠️ Correlação fraca entre estudo e nota ({corr_hours:.2f}). Neste grupo, outros fatores são mais determinantes.</li>"
    
    corr_sleep = df_filtered['sleep_hours'].corr(df_filtered['exam_score'])
    if corr_sleep > 0.2:
        insight_text += f"<li>😴 O sono apresenta correlação positiva com a nota ({corr_sleep:.2f}).</li>"
    else:
        insight_text += f"<li>😴 O sono não está fortemente correlacionado com a nota neste recorte ({corr_sleep:.2f}).</li>"
    
    insight_text += f"""
            <li><strong>Recomendação:</strong> {'Fortalecer hábitos de estudo e monitorar frequência' if diff_score < 0 else 'Manter estratégias atuais e incentivar mentoria'}.</li>
        </ul>
    </div>
    """
    st.markdown(insight_text, unsafe_allow_html=True)

# --- DADOS BRUTOS (EXPANDER) --- #
with st.expander("🗂️ Visualizar base de dados completa (filtrada)"):
    st.dataframe(df_filtered, use_container_width=True)
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="dados_educacionais_filtrados.csv",
        mime="text/csv"
    )

# --- RODAPÉ --- #
st.markdown("---")
st.caption("EduAnalytics 2.0 – Dashboard interativo para tomada de decisão educacional. Desenvolvido com Streamlit e Plotly.")
