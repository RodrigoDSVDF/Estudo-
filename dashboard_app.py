
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar o dataset
df = pd.read_csv("student_exam_scores.csv")

# --- Configurações da Página --- #
st.set_page_config(page_title="Análise de Desempenho de Estudantes",
                   page_icon=":books:",
                   layout="wide")

# --- CSS Personalizado --- #
st.markdown("""
<style>
.main-header {
    font-size: 3em;
    font-weight: bold;
    color: #2E86C1;
    text-align: center;
    margin-bottom: 30px;
}
.subheader {
    font-size: 1.8em;
    font-weight: bold;
    color: #34495E;
    margin-top: 20px;
    margin-bottom: 15px;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 5rem;
    padding-right: 5rem;
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
st.markdown("<p class=\'main-header\'>Dashboard de Análise de Desempenho de Estudantes</p>", unsafe_allow_html=True)

# --- Sidebar para Filtros (Exemplo) --- #
st.sidebar.header("Filtros")

# Exemplo de filtro: faixa de horas de estudo
min_hours, max_hours = st.sidebar.slider(
    "Horas de Estudo",
    float(df["hours_studied"].min()),
    float(df["hours_studied"].max()),
    (float(df["hours_studied"].min()), float(df["hours_studied"].max()))
)
df_filtered = df[(df["hours_studied"] >= min_hours) & (df["hours_studied"] <= max_hours)]

# --- Seção de Métricas Chave --- #
st.markdown("<p class=\'subheader\'>Métricas Chave</p>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Média da Nota do Exame", value=f"{df_filtered["exam_score"].mean():.2f}")
with col2:
    st.metric(label="Média de Horas de Estudo", value=f"{df_filtered["hours_studied"].mean():.2f}")
with col3:
    st.metric(label="Média de Horas de Sono", value=f"{df_filtered["sleep_hours"].mean():.2f}")

# --- Visualizações Interativas com Plotly --- #
st.markdown("<p class=\'subheader\'>Visualizações Interativas</p>", unsafe_allow_html=True)

# 1. Distribuição das Notas do Exame (Histograma)
fig_hist = px.histogram(df_filtered, x="exam_score", nbins=20, title="Distribuição das Notas do Exame",
                        labels={"exam_score": "Nota do Exame"})
st.plotly_chart(fig_hist, use_container_width=True)
st.markdown("**Conclusão:** O histograma da nota do exame mostra uma distribuição aproximadamente normal, com a maioria dos estudantes concentrada em torno da média, e caudas mais finas em notas muito baixas ou muito altas.")

# 2. Horas de Estudo vs Nota do Exame (Scatter Plot)
fig_hours_exam = px.scatter(df_filtered, x="hours_studied", y="exam_score",
                            title="Horas de Estudo vs Nota do Exame",
                            labels={"hours_studied": "Horas de Estudo", "exam_score": "Nota do Exame"},
                            hover_data=["student_id", "sleep_hours", "attendance_percent", "previous_scores"])
st.plotly_chart(fig_hours_exam, use_container_width=True)
st.markdown("**Conclusão:** Este scatter plot revela uma **forte correlação positiva** entre as horas de estudo e a nota do exame. Estudantes que dedicam mais tempo aos estudos tendem a obter notas mais altas.")

# 3. Matriz de Correlação (Heatmap)
st.markdown("<p class=\'subheader\'>Matriz de Correlação</p>", unsafe_allow_html=True)
correlation_matrix = df_filtered[["hours_studied", "sleep_hours", "attendance_percent", "previous_scores", "exam_score"]].corr()
fig_corr = px.imshow(correlation_matrix, text_auto=True, aspect="auto",
                     title="Matriz de Correlação entre Variáveis",
                     color_continuous_scale="Viridis")
st.plotly_chart(fig_corr, use_container_width=True)
st.markdown("**Conclusão:** A matriz de correlação quantifica a força e a direção das relações lineares entre as variáveis. `hours_studied` tem a correlação mais forte com `exam_score` (0.777), seguido por `previous_scores` (0.431). `attendance_percent` e `sleep_hours` têm correlações positivas mais fracas.")

# 4. Horas de Sono vs Nota do Exame (Scatter Plot)
fig_sleep_exam = px.scatter(df_filtered, x="sleep_hours", y="exam_score",
                            title="Horas de Sono vs Nota do Exame",
                            labels={"sleep_hours": "Horas de Sono", "exam_score": "Nota do Exame"},
                            hover_data=["student_id", "hours_studied", "attendance_percent", "previous_scores"])
st.plotly_chart(fig_sleep_exam, use_container_width=True)
st.markdown("**Conclusão:** Observa-se uma correlação positiva, embora mais fraca, entre as horas de sono e a nota do exame. Mais horas de sono parecem estar associadas a notas ligeiramente melhores, mas a relação não é tão linear ou pronunciada quanto a das horas de estudo.")

# 5. Porcentagem de Presença vs Nota do Exame (Scatter Plot)
fig_attendance_exam = px.scatter(df_filtered, x="attendance_percent", y="exam_score",
                                 title="Porcentagem de Presença vs Nota do Exame",
                                 labels={"attendance_percent": "Porcentagem de Presença", "exam_score": "Nota do Exame"},
                                 hover_data=["student_id", "hours_studied", "sleep_hours", "previous_scores"])
st.plotly_chart(fig_attendance_exam, use_container_width=True)
st.markdown("**Conclusão:** Existe uma correlação positiva entre o percentual de presença e a nota do exame. Estudantes com maior frequência nas aulas tendem a ter notas mais elevadas, sugerindo a importância da participação em sala de aula.")

# 6. Notas Anteriores vs Nota do Exame (Scatter Plot)
fig_previous_exam = px.scatter(df_filtered, x="previous_scores", y="exam_score",
                               title="Notas Anteriores vs Nota do Exame",
                               labels={"previous_scores": "Notas Anteriores", "exam_score": "Nota do Exame"},
                               hover_data=["student_id", "hours_studied", "sleep_hours", "attendance_percent"])
st.plotly_chart(fig_previous_exam, use_container_width=True)
st.markdown("**Conclusão:** As notas anteriores dos estudantes mostram uma correlação positiva com a nota do exame atual. Isso indica que o desempenho passado é um bom preditor do desempenho futuro, refletindo a consistência acadêmica.")

# --- Informações Adicionais (Opcional) --- #
st.markdown("<p class=\'subheader\'>Informações Adicionais</p>", unsafe_allow_html=True)
st.write("Este dashboard permite explorar a relação entre diversas variáveis e o desempenho dos estudantes em exames. Utilize os filtros na barra lateral para interagir com os dados.")

# Exibir os dados filtrados (opcional)
if st.checkbox("Mostrar Dados Brutos Filtrados"):
    st.dataframe(df_filtered)

