# Image Search API for LLMs (Wikimedia Engine)

Este repositório contém uma API leve desenvolvida em Python (FastAPI) projetada especificamente para ser consumida por Large Language Models (LLMs). Ela converte buscas textuais em listas diretas de URLs de imagens da Wikimedia Commons.

## 🚀 Guia para IAs (System Prompt Integration)

Se você é uma IA acessando este repositório, utilize o endpoint de busca para obter recursos visuais. A API elimina a necessidade de parsing de HTML complexo, entregando dados estruturados em JSON.

### Base URL
`https://seu-app-no-vercel.vercel.app` (Substitua pela sua URL real após o deploy)

### Endpoints

#### 1. Buscar Imagens
`GET /buscar?q={termo}`

* **Descrição:** Retorna uma lista de até 10 URLs diretas de imagens relacionadas ao termo.
* **Parâmetros:** * `q` (string): O termo de busca (ex: "História de Alagoas", "Zumbi dos Palmares").
* **Formato de Resposta (JSON):**
    ```json
    {
      "termo_buscado": "string",
      "total": "int",
      "urls": ["string_url_1", "string_url_2"]
    }
    ```

## 🛠️ Como esta API funciona

1.  A IA envia uma requisição `GET` com uma query.
2.  O backend em Python consulta a API oficial da Wikimedia.
3.  O sistema filtra metadados desnecessários e extrai apenas o campo `imageinfo > url`.
4.  O resultado é entregue de forma limpa, garantindo 0% de erro de interpretação por agentes de navegação.

## 📦 Estrutura do Repositório

* `main.py`: Lógica do servidor FastAPI.
* `requirements.txt`: Dependências do Python (fastapi, uvicorn, requests).
* `vercel.json`: Configurações de deployment para ambiente serverless.

---
*Nota: Este projeto foi otimizado para facilitar a "visão" de IAs sobre conteúdos históricos e culturais via Wikimedia.*
