# Tradução Inglês para Francês com FastAPI e HuggingFace

API desenvolvida com FastAPI que recebe um texto em inglês e retorna sua tradução para o francês utilizando o modelo `Helsinki-NLP/opus-mt-en-fr` da HuggingFace, através da biblioteca `transformers`.

## Estrutura

```
.
├── main.py           # criação da aplicação e carregamento do modelo na inicialização
├── models.py         # modelos Pydantic de requisição e resposta
├── routes.py         # endpoints da API
├── services.py       # pipeline de tradução do transformers
└── requirements.txt
```

## Textos longos

O modelo aceita no máximo 512 tokens por entrada e tende a omitir partes do conteúdo quando recebe muitas frases de uma vez. Por isso o texto é dividido em parágrafos e frases, as frases são traduzidas em lotes (`batch_size=8`) e o resultado é remontado mantendo as quebras de parágrafo. Assim a API processa tanto frases curtas quanto textos mais longos.

## Requisitos

- Python 3.12 ou superior
- Cerca de 2 GB livres para as dependências e o modelo

## Como executar

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Na primeira execução o modelo é baixado automaticamente do HuggingFace Hub. A documentação interativa fica disponível em http://127.0.0.1:8000/docs.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Verifica se a API está no ar |
| POST | `/translate` | Traduz um texto do inglês para o francês |

### POST /translate

Corpo da requisição:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `text` | string | sim | Texto em inglês (1 a 10000 caracteres) |

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you today?"}'
```

Resposta:

```json
{
  "model": "Helsinki-NLP/opus-mt-en-fr",
  "source_language": "en",
  "target_language": "fr",
  "original_text": "Hello, how are you today?",
  "translated_text": "Bonjour, comment allez-vous aujourd'hui ?"
}
```

Textos vazios ou acima do limite retornam status `422`.
