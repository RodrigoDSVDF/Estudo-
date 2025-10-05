import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar o dataset
df = pd.read_csv("student_exam_scores (1).csv") 

# --- Configurações da Página --- #
st.set_page_config(page_title="Análise de Desempenho de Estudantes",
                   page_icon=":books:",
                   layout="wide")

# --- CSS Personalizado --- #
st.markdown("""
<style>
.main-header {
    font-size: 2.5em; /* Reduzido um pouco para melhor encaixe em mobile */
    font-weight: bold;
    color: #2E86C1;
    text-align: center;
    margin-bottom: 30px;
}
.subheader {
    font-size: 1.6em; /* Reduzido um pouco para melhor encaixe em mobile */
    font-weight: bold;
    color: #34495E;
    margin-top: 20px;
    margin-bottom: 15px;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem; /* Reduzido padding para telas menores */
    padding-right: 2rem; /* Reduzido padding para telas menores */
}
.stButton>button {
    background-color: #2E86C1;
    color: white;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 1.1em;
}
.stButton>button:hover {
    background-color: #3498DB;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Título do Dashboard --- #
st.markdown("<p class='main-header'>Dashboard de Análise de Desempenho de Estudantes</p>", unsafe_allow_html=True)

# --- Sidebar para Filtros --- #
st.sidebar.header("Filtros")

min_hours, max_hours = st.sidebar.slider(
    "Horas de Estudo",
    float(df["hours_studied"].min()),
    float(df["hours_studied"].max()),
    (float(df["hours_studied"].min()), float(df["hours_studied"].max()))
)
df_filtered = df[(df["hours_studied"] >= min_hours) & (df["hours_studied"] <= max_hours)]

# --- Seção de Métricas Chave --- #
st.markdown("<p class='subheader'>Métricas Chave</p>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Média da Nota do Exame", value=f"{df_filtered['exam_score'].mean():.2f}")
with col2:
    st.metric(label="Média de Horas de Estudo", value=f"{df_filtered['hours_studied'].mean():.2f}")
with col3:
    st.metric(label="Média de Horas de Sono", value=f"{df_filtered['sleep_hours'].mean():.2f}")

# --- Visualizações Interativas com Plotly --- #
st.markdown("<p class='subheader'>Visualizações Interativas</p>", unsafe_allow_html=True)

plot_margin = dict(l=20, r=20, t=40, b=20)

# 1. Distribuição das Notas do Exame (Histograma)
fig_hist = px.histogram(df_filtered, x="exam_score", nbins=20, title="Distribuição das Notas do Exame",
                        labels={"exam_score": "Nota do Exame"})
fig_hist.update_layout(margin=plot_margin)
st.plotly_chart(fig_hist, use_container_width=True)


# 2. Horas de Estudo vs Nota do Exame (Scatter Plot)
fig_hours_exam = px.scatter(df_filtered, x="hours_studied", y="exam_score",
                            title="Horas de Estudo vs Nota do Exame",
                            labels={"hours_studied": "Horas de Estudo", "exam_score": "Nota do Exame"},
                            hover_data=["student_id", "sleep_hours", "attendance_percent", "previous_scores"])
fig_hours_exam.update_layout(margin=plot_margin)
st.plotly_chart(fig_hours_exam, use_container_width=True)


# 3. Matriz de Correlação (Heatmap)
st.markdown("<p class='subheader'>Matriz de Correlação</p>", unsafe_allow_html=True)
correlation_matrix = df_filtered[["hours_studied", "sleep_hours", "attendance_percent", "previous_scores", "exam_score"]].corr()

fig_corr = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    colorscale="Viridis",
    text=correlation_matrix.round(2).values,
    texttemplate="%{text}",
    hoverongaps=False))

fig_corr.update_layout(
    title="Matriz de Correlação entre Variáveis",
    margin=plot_margin,
    xaxis_tickangle=-45
)
fig_corr.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig_corr.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

st.plotly_chart(fig_corr, use_container_width=True)

# 4. Horas de Sono vs Nota do Exame (Scatter Plot)
fig_sleep_exam = px.scatter(df_filtered, x="sleep_hours", y="exam_score",
                            title="Horas de Sono vs Nota do Exame",
                            labels={"sleep_hours": "Horas de Sono", "exam_score": "Nota do Exame"},
                            hover_data=["student_id", "hours_studied", "attendance_percent", "previous_scores"])
fig_sleep_exam.update_layout(margin=plot_margin)
st.plotly_chart(fig_sleep_exam, use_container_width=True)


# 5. Porcentagem de Presença vs Nota do Exame (Scatter Plot)
fig_attendance_exam = px.scatter(df_filtered, x="attendance_percent", y="exam_score",
                                 title="Porcentagem de Presença vs Nota do Exame",
                                 labels={"attendance_percent": "Porcentagem de Presença", "exam_score": "Nota do Exame"},
                                 hover_data=["student_id", "hours_studied", "sleep_hours", "previous_scores"])
fig_attendance_exam.update_layout(margin=plot_margin)
st.plotly_chart(fig_attendance_exam, use_container_width=True)


# 6. Notas Anteriores vs Nota do Exame (Scatter Plot)
fig_previous_exam = px.scatter(df_filtered, x="previous_scores", y="exam_score",
                               title="Notas Anteriores vs Nota do Exame",
                               labels={"previous_scores": "Notas Anteriores", "exam_score": "Nota do Exame"},
                               hover_data=["student_id", "hours_studied", "sleep_hours", "attendance_percent"])
fig_previous_exam.update_layout(margin=plot_margin)
st.plotly_chart(fig_previous_exam, use_container_width=True)


# --- NOVA SEÇÃO: CONCLUSÕES DO ESTUDO ---
st.markdown("<p class='subheader'>Conclusões e Recomendações do Estudo</p>", unsafe_allow_html=True)

st.info(
    """
    **Principal Conclusão:** O estudo estatístico confirma que as **horas de estudo** são, de longe, o fator mais impactante na nota do exame, com uma correlação de **0.777**.
    O modelo de regressão linear demonstrou que as variáveis analisadas (horas de estudo, sono, presença e notas anteriores) explicam **84.1%** da variação nas notas dos exames, indicando um alto poder preditivo.
    """,
    icon="💡"
)

st.markdown("#### Recomendações Principais:")
    
col1, col2 = st.columns(2)
    
with col1:
    st.markdown(
        """
        - **📈 Incentivar o Estudo Consistente:** Para cada hora adicional de estudo, a nota do exame tende a aumentar em 1.56 pontos. Promover hábitos de estudo regulares é a intervenção mais eficaz.
        - **🧑‍🏫 Promover a Frequência:** A presença em aula é um fator importante. Cada ponto percentual a mais na presença está associado a um aumento de 0.11 pontos na nota.
        """
    )

with col2:
    st.markdown(
        """
        - **😴 Conscientizar sobre a Importância do Sono:** O sono adequado é um preditor significativo. Cada hora adicional de sono se relaciona com um aumento de 0.95 pontos na nota final.
        - **📚 Acompanhar o Desempenho Anterior:** As notas passadas são um excelente indicador de resultados futuros e podem ser usadas para identificar estudantes que necessitam de suporte adicional.
        """
    )
# --- FIM DA NOVA SEÇÃO ---


# --- Informações Adicionais (Opcional) --- #
st.markdown("<p class='subheader'>Informações Adicionais</p>", unsafe_allow_html=True)
st.write("Este dashboard permite explorar visualmente a relação entre diversas variáveis e o desempenho dos estudantes. Utilize os filtros na barra lateral para interagir com os dados.")

if st.checkbox("Mostrar Dados Brutos Filtrados"):
    st.dataframe(df_filtered)
