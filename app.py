import streamlit as st
import requests
import json

"""
Credit‑Score API App (sem perfis de demonstração)
================================================
Interface Streamlit minimalista que envia **todas** as features obrigatórias
para um endpoint REST de *credit‑scoring*.

A estrutura segue a orientação do professor (API‑first) e substitui
a versão da colega, removendo completamente os perfis predefinidos para
que cada usuário preencha seus próprios dados.
"""

# –– Configuração da página
st.set_page_config(
    page_title="Quantum Finance - Credit Score Predictor - MLOps - FIAP 10DTSR",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="auto",
)

###########################
# Função de requisição API
###########################

def get_prediction(payload: dict):
    """POSTa o payload e devolve (prediction, proba) ou (None, None) em erro."""
    endpoint = st.secrets["API_ENDPOINT"]
    headers = {
        "Content-Type": "application/json",
        "x-api-key": st.secrets["API_KEY"],
    }
    try:
        resp = requests.post(endpoint, headers=headers, data=json.dumps(payload), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("prediction"), data.get("proba")
    except (requests.RequestException, ValueError) as err:
        st.error(f"Erro ao consultar API: {err}")
        return None, None

####################
# Sidebar – Formulário
####################
with st.sidebar:
    st.header("Preencha as features")

    Age = st.slider("Idade", min_value=18, max_value=100, value=30, step=1)
    Annual_Income = st.number_input("Renda Anual (R$)", min_value=0.0, max_value=1_000_000.0, value=0.0, step=1000.0, format="%.2f")
    Num_Bank_Accounts = st.number_input("Nº de contas bancárias", 0, 20, value=0, step=1)
    Num_Credit_Card = st.number_input("Nº de cartões de crédito", 0, 12, value=0, step=1)
    Num_of_Delayed_Payment = st.number_input("Pagamentos atrasados", 0, 50, value=0, step=1)
    Credit_Utilization_Ratio = st.slider("Utilização do limite (%)", 0.0, 100.0, value=0.0, step=0.1)

    Payment_of_Min_Amount_bool = st.radio("Pagou valor mínimo em algum cartão?", ["Não", "Sim"], horizontal=True)
    Total_EMI_per_month = st.number_input("EMI mensal (R$)", 0.0, 10_000.0, value=0.0, step=10.0, format="%.2f")
    Credit_History_Age_Formated = st.number_input("Histórico de crédito (meses)", 0, 600, value=0, step=1)

    loan_features = [
        "Auto_Loan",
        "Credit-Builder_Loan",
        "Personal_Loan",
        "Home_Equity_Loan",
        "Mortgage_Loan",
        "Student_Loan",
        "Debt_Consolidation_Loan",
        "Payday_Loan",
    ]
    loans_selected = st.multiselect("Tipos de empréstimo em aberto", loan_features, default=[])

    Missed_Payment_bool = st.radio("Perdeu algum pagamento nos últimos 12 meses?", ["Não", "Sim"], horizontal=True)

    run_button = st.button("Calcular Score")

###################
# Construção Payload
###################
action_placeholder = st.empty()

if run_button:
    Payment_of_Min_Amount = 1 if Payment_of_Min_Amount_bool == "Sim" else 0
    Missed_Payment_Day = 1 if Missed_Payment_bool == "Sim" else 0

    # Flags de empréstimo
    loan_flags = {loan: 1 if loan in loans_selected else 0 for loan in loan_features}

    feature_dict = {
        "Age": Age,
        "Annual_Income": Annual_Income,
        "Num_Bank_Accounts": Num_Bank_Accounts,
        "Num_Credit_Card": Num_Credit_Card,
        "Num_of_Delayed_Payment": Num_of_Delayed_Payment,
        "Credit_Utilization_Ratio": Credit_Utilization_Ratio,
        "Payment_of_Min_Amount": Payment_of_Min_Amount,
        "Total_EMI_per_month": Total_EMI_per_month,
        "Credit_History_Age_Formated": Credit_History_Age_Formated,
        "Missed_Payment_Day": Missed_Payment_Day,
        **loan_flags,
    }

    payload = {"data": feature_dict}

    with st.spinner("Consultando modelo..."):
        prediction, proba = get_prediction(payload)

    # –– Exibição de resultados
    if prediction is None:
        st.stop()

    if prediction == 1:
        st.success("💚 **SCORE: BOM** – risco baixo de inadimplência.")
    elif prediction == 0:
        st.warning("🟠 **SCORE: REGULAR** – risco moderado.")
    elif prediction == -1:
        st.error("❤️‍🔥 **SCORE: RUIM** – alto risco de inadimplência.")
    else:
        st.info(f"Resultado bruto do modelo: {prediction}")

    if proba is not None and isinstance(proba, (list, tuple)) and len(proba) == 3:
        labels = ["Poor", "Regular", "Good"]
        proba_percent = [round(p * 100, 1) for p in proba]
        st.subheader("Confiança do modelo (%)")
        cols = st.columns(3)
        for col, label, pct in zip(cols, labels, proba_percent):
            col.metric(label, f"{pct}%")

    with st.expander("Payload + Resposta bruta"):
        st.code(json.dumps(payload, indent=2), language="json")
        st.code({"prediction": prediction, "proba": proba})
