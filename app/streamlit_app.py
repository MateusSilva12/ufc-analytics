# app/streamlit_app.py
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="UFC Data Portfolio", layout="wide")

@st.cache_data
def load_data(csv_path="data/ufc_fights_detailed.csv"):
    return pd.read_csv(csv_path)

@st.cache_resource
def load_model(path="models/xgb_ufc.joblib"):
    return joblib.load(path)

st.title("UFC / MMA Data Portfolio")
st.markdown("Explore dados, estatísticas por lutador e um modelo básico de previsão de vencedor.")

df = load_data()
st.sidebar.header("Opções")
view = st.sidebar.selectbox("Visão", ["Resumo", "Buscar Lutador", "Análises", "Predictor"])

if view == "Resumo":
    st.header("Resumo do Dataset")
    st.write("Número de lutas:", df.shape[0])
    st.write("Colunas:", list(df.columns))
    st.dataframe(df.head())

if view == "Buscar Lutador":
    name = st.text_input("Nome do lutador (exato ou parte)")
    if name:
        sub = df[df.apply(lambda r: name.lower() in str(r).lower(), axis=1)]
        st.write(f"Resultados encontrados: {sub.shape[0]}")
        st.dataframe(sub[["fight_url", "fighter_1", "fighter_2", "method", "round", "time"]].drop_duplicates().head(100))

if view == "Análises":
    st.header("Análises rápidas")
    st.subheader("Distribuição de métodos de vitória")
    if "method" in df.columns:
        meth = df["method"].value_counts().head(20)
        st.bar_chart(meth)

    st.subheader("Top lutadores por aparição")
    top = pd.concat([df["fighter_1"], df["fighter_2"]]).value_counts().head(20)
        # mostrar como tabela
    st.table(top)

if view == "Predictor":
    st.header("Predictor - Baseline")
    st.write("Carregando modelo...")
    try:
        mdl = load_model()
        model = mdl["model"]
        le = mdl["label_encoder"]
        features = mdl["features"]
    except Exception as e:
        st.error("Modelo não encontrado. Rode o training e coloque o arquivo models/xgb_ufc.joblib")
        st.stop()

    st.write("Selecione valores (exemplo com features difference):")
    # gerar inputs default zerados
    inputs = {}
    for f in features:
        inputs[f] = st.number_input(f, value=0.0, format="%.3f")
    X = pd.DataFrame([inputs])
    pred = model.predict(X)[0]
    pred_label = le.inverse_transform([pred])[0]
    st.write("Predito:", pred_label)

st.markdown("---")
st.write("Projeto: UFC Data Portfolio — por Mateus Silva")
