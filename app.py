import streamlit as st
from streamlit.errors import StreamlitAPIException
import requests
import json

"""
Quantum Finance - Credit Score Analysis
=======================================
Sistema de análise de score de crédito utilizando modelo de Machine Learning via API.

Projeto Final - Quantum Finance
FIAP - MBA em DATA SCIENCE & ARTIFICIAL INTELLIGENCE
Disciplina: MLOps | Turma: 10DTSR

Equipe:
- RM358585 - Matheus Vitor da Silva Souza
- RM359082 - Lucian Cláudio da Silva  
- RM359495 - Maurício Mourão Jorge
"""

# –– Configuração da página (robusta contra múltiplas chamadas)
try:
    st.set_page_config(
        page_title="Quantum Finance - Credit Score",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
except StreamlitAPIException:
    pass  # Já definida

###########################
# Helper para ler segredos
###########################

def _get_secret(*keys, default=None):
    """Tenta retornar a primeira chave existente em st.secrets dentre `keys`."""
    for key in keys:
        if key in st.secrets:
            return st.secrets[key]
    if default is not None:
        return default
    raise KeyError(f"Nenhuma das chaves {keys} encontrada em st.secrets")

###########################
# Função de requisição API
###########################

def get_prediction(payload: dict):
    """POSTa o payload e devolve (prediction, proba) ou (None, None) em erro."""
    endpoint = _get_secret("API_ENDPOINT", "API-ENDPOINT")
    api_key = _get_secret("API_KEY", "API-KEY")
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
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
# Sidebar - Changelog
####################
with st.sidebar:
    st.markdown("# 📋 Changelog")
    st.markdown("---")
    
    st.markdown("### **v3.0** - Versão Final FIAP")
    st.markdown("*Agosto 2025*")
    st.markdown("""
    - ✅ Interface redesenhada para tela principal
    - ✅ Features de empréstimo traduzidas
    - ✅ Visual profissional para apresentação
    - ✅ Sidebar com histórico de versões
    - ✅ Melhor organização dos inputs
    """)
    
    st.markdown("### **v2.0** - Estabilização")
    st.markdown("*Julho 2025*")
    st.markdown("""
    - ✅ Chaves em `st.secrets` flexíveis
    - ✅ `set_page_config` garantido
    - ✅ Tratamento robusto de erros
    - ✅ Timeout configurável na API
    """)
    
    st.markdown("### **v1.0** - MVP")
    st.markdown("*Junho 2025*")
    st.markdown("""
    - ✅ Integração com API de ML
    - ✅ Interface básica funcional
    - ✅ Validação de inputs
    """)
    
    st.markdown("---")
    st.markdown("**🎓 Projeto Final**")
    st.markdown("**FIAP - MBA em DATA SCIENCE**")
    st.markdown("**& ARTIFICIAL INTELLIGENCE**")
    st.markdown("**Disciplina:** MLOps")
    st.markdown("**Turma:** 10DTSR")
    st.markdown("")
    st.markdown("**👥 Equipe Quantum Finance:**")
    st.markdown("• **RM358585** - Matheus Vitor da Silva Souza")
    st.markdown("• **RM359082** - Lucian Cláudio da Silva")
    st.markdown("• **RM359495** - Maurício Mourão Jorge")

####################
# Cabeçalho Principal
####################
st.markdown("# 🏦 Quantum Finance - Análise de Score de Crédito")
st.markdown("### Sistema inteligente de avaliação de risco creditício")
st.markdown("---")

st.markdown("""
<div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem;">
    <h4>🎯 Como funciona</h4>
    <p>Preencha as informações financeiras abaixo e nosso modelo de Machine Learning 
    analisará o perfil de risco creditício, fornecendo uma classificação precisa 
    baseada em algoritmos avançados.</p>
</div>
""", unsafe_allow_html=True)

####################
# Formulário Principal
####################

st.markdown("## 📊 Dados Pessoais e Financeiros")

# Primeira linha - Dados básicos
col1, col2, col3 = st.columns(3)

with col1:
    Age = st.slider("👤 Idade", min_value=18, max_value=100, value=30, step=1)
    
with col2:
    Annual_Income = st.number_input(
        "💰 Renda Anual (R$)", 
        min_value=0.0, 
        max_value=1_000_000.0, 
        value=50000.0, 
        step=1000.0, 
        format="%.2f"
    )
    
with col3:
    Credit_History_Age_Formated = st.number_input(
        "📅 Histórico de Crédito (meses)", 
        0, 600, 
        value=24, 
        step=1
    )

st.markdown("---")

# Segunda linha - Contas e cartões
st.markdown("## 🏛️ Relacionamento Bancário")

col1, col2, col3, col4 = st.columns(4)

with col1:
    Num_Bank_Accounts = st.number_input(
        "🏦 Nº de Contas Bancárias", 
        0, 20, 
        value=2, 
        step=1
    )
    
with col2:
    Num_Credit_Card = st.number_input(
        "💳 Nº de Cartões de Crédito", 
        0, 12, 
        value=2, 
        step=1
    )
    
with col3:
    Credit_Utilization_Ratio = st.slider(
        "📈 Utilização do Limite (%)", 
        0.0, 100.0, 
        value=30.0, 
        step=0.1
    )
    
with col4:
    Total_EMI_per_month = st.number_input(
        "📊 Parcelas Mensais (R$)", 
        0.0, 10_000.0, 
        value=500.0, 
        step=50.0, 
        format="%.2f"
    )

st.markdown("---")

# Terceira linha - Histórico de pagamentos
st.markdown("## 📋 Histórico de Pagamentos")

col1, col2, col3 = st.columns(3)

with col1:
    Num_of_Delayed_Payment = st.number_input(
        "⏰ Pagamentos Atrasados", 
        0, 50, 
        value=0, 
        step=1
    )
    
with col2:
    Payment_of_Min_Amount_bool = st.radio(
        "💳 Pagou Valor Mínimo do Cartão?",
        ["Não", "Sim"], 
        horizontal=True,
        index=1
    )
    
with col3:
    Missed_Payment_bool = st.radio(
        "❌ Perdeu Pagamento nos Últimos 12 Meses?",
        ["Não", "Sim"], 
        horizontal=True,
        index=0
    )

st.markdown("---")

# Quarta linha - Tipos de empréstimo
st.markdown("## 🏠 Empréstimos Ativos")

# Mapeamento das features traduzidas
loan_features_map = {
    "Auto_Loan": "🚗 Financiamento de Veículo",
    "Credit-Builder_Loan": "🔨 Empréstimo para Construção de Crédito",
    "Personal_Loan": "👤 Empréstimo Pessoal",
    "Home_Equity_Loan": "🏠 Empréstimo com Garantia Imobiliária",
    "Mortgage_Loan": "🏘️ Financiamento Imobiliário",
    "Student_Loan": "🎓 Financiamento Estudantil",
    "Debt_Consolidation_Loan": "💼 Empréstimo para Consolidação de Dívidas",
    "Payday_Loan": "⚡ Empréstimo Emergencial (Payday)"
}

loan_features = list(loan_features_map.keys())
loan_labels = list(loan_features_map.values())

st.markdown("**Selecione os tipos de empréstimo que você possui atualmente:**")
loans_selected_labels = st.multiselect(
    "Tipos de empréstimo em aberto",
    loan_labels,
    default=[],
    label_visibility="collapsed"
)

# Converter labels de volta para as chaves originais
loans_selected = [
    key for key, label in loan_features_map.items() 
    if label in loans_selected_labels
]

st.markdown("---")

# Botão de análise
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_button = st.button(
        "🔍 **ANALISAR SCORE DE CRÉDITO**", 
        type="primary",
        use_container_width=True
    )

###################
# Processamento e Resultados
###################

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

    with st.spinner("🤖 Analisando dados com modelo de Machine Learning..."):
        prediction, proba = get_prediction(payload)

    # –– Exibição de resultados
    if prediction is None:
        st.stop()

    st.markdown("---")
    st.markdown("## 🎯 Resultado da Análise")
    
    # Resultado principal
    result_col1, result_col2 = st.columns([2, 1])
    
    with result_col1:
        if prediction == 1:
            st.markdown("""
            <div style="background-color: #d4edda; border-left: 5px solid #28a745; padding: 1rem; border-radius: 0.5rem;">
                <h2 style="color: #155724; margin: 0;">💚 SCORE: BOM</h2>
                <p style="color: #155724; margin: 0.5rem 0 0 0;">Baixo risco de crédito. Perfil creditício favorável para aprovação.</p>
            </div>
            """, unsafe_allow_html=True)
        elif prediction == 0:
            st.markdown("""
            <div style="background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 1rem; border-radius: 0.5rem;">
                <h2 style="color: #856404; margin: 0;">🟡 SCORE: NEUTRO</h2>
                <p style="color: #856404; margin: 0.5rem 0 0 0;">Requer atenção. Análise criteriosa recomendada antes da aprovação.</p>
            </div>
            """, unsafe_allow_html=True)
        elif prediction == -1:
            st.markdown("""
            <div style="background-color: #f8d7da; border-left: 5px solid #dc3545; padding: 1rem; border-radius: 0.5rem;">
                <h2 style="color: #721c24; margin: 0;">🔴 SCORE: RUIM</h2>
                <p style="color: #721c24; margin: 0.5rem 0 0 0;">Alto risco de crédito. Recomenda-se recusa ou condições especiais.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"Resultado do modelo: {prediction}")
    
    # Métricas de confiança
    if proba is not None and isinstance(proba, (list, tuple)) and len(proba) == 3:
        st.markdown("### 📊 Confiança do Modelo")
        labels = ["🔴 Ruim", "🟡 Neutro", "💚 Bom"]
        proba_percent = [round(p * 100, 1) for p in proba]
        
        cols = st.columns(3)
        for col, label, pct in zip(cols, labels, proba_percent):
            col.metric(label, f"{pct}%")

    # Detalhes técnicos (expansível)
    with st.expander("🔧 Detalhes Técnicos (Payload e Resposta)"):
        st.markdown("**Dados enviados para o modelo:**")
        st.code(json.dumps(payload, indent=2), language="json")
        st.markdown("**Resposta do modelo:**")
        st.code(json.dumps({"prediction": prediction, "proba": proba}, indent=2), language="json")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
        <p>🤖 Análise realizada por modelo de Machine Learning treinado com dados históricos</p>
        <p><strong>Quantum Finance</strong> | FIAP - MBA em Data Science & AI | Turma 10DTSR</p>
        <p>Matheus Souza • Lucian Silva • Maurício Jorge</p>
    </div>
    """, unsafe_allow_html=True)