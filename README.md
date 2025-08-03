# FIAP - MLOps - Streamlit App - Score de Crédito

Este repositório contém a interface web do projeto de **score de crédito**, desenvolvido como parte do trabalho final da disciplina de MLOps do MBA da FIAP.

A aplicação foi construída com [Streamlit](https://streamlit.io/) e conecta-se a uma API hospedada na AWS, que realiza a predição com base no modelo de Machine Learning treinado.

---

## 💻 Visão Geral

A interface coleta informações do usuário como:

- Número de cartões de crédito
- Pagamentos atrasados
- Utilização do limite
- Histórico de crédito
- Tipos de empréstimo em aberto
- Pagamento mínimo
- Entre outros

Com esses dados, o app envia uma requisição à **API de predição**, que responde com um score classificado como:

- `Ruim`
- `Médio`
- `Bom`

---

## 🚀 Como executar o app localmente

### ✅ Requisitos

- Python 3.10+
- [Streamlit](https://docs.streamlit.io/)
- API de predição rodando (local ou na nuvem)

### 🔧 Instalação

Clone o repositório:

```bash
git clone https://github.com/luciancsilva/fiap-10dtsr-mlops-app-trabalho-final.git
cd fiap-10dtsr-mlops-app-trabalho-final
pip install -r requirements.txt

