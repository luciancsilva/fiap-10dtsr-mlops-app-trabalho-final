# FIAP - MLOps - API de Score de Crédito

Este repositório contém a API que serve como backend do projeto de **score de crédito** desenvolvido como trabalho final da disciplina de MLOps no MBA da FIAP.

A API está empacotada em um container Docker e implantada na **AWS Lambda** via **ECR**, sendo acessada por meio do **API Gateway**.

---

## 📦 Funcionalidade

A API expõe um endpoint `/prediction` que recebe um payload JSON com os dados do cliente e retorna:

* A **classe prevista** (`"Bom"`, `"Neutro"` ou `"Ruim"`)
* O **rótulo numérico** correspondente (`"1"`, `"0"` ou `"-1"`)

Exemplo de resposta:

```json
{
  "prediction": 1,
  "classe": "Bom"
}
```
