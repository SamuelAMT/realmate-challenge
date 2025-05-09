# Realmate Challenge - API de Webhook e Conversações

Este projeto implementa uma API para gerenciar conversas e mensagens através de webhooks, usando Django e Django Rest Framework.

## Funcionalidades Implementadas

- Processamento de webhooks para eventos de conversas e mensagens
- Endpoint para consulta de detalhes de conversas
- Sistema de validação para regras de negócio (ex: não permitir mensagens em conversas fechadas)
- Documentação interativa com Swagger UI

## Tecnologias Utilizadas

- Django 5.2
- Django Rest Framework
- drf-yasg (Swagger para DRF)
- SQLite

## Instalação

### Com Poetry

```bash
# Instalar o Poetry (caso não tenha)
pip install poetry

# Instalar dependências
poetry install

# Aplicar migrações
poetry run python manage.py migrate

# Executar o servidor
poetry run python manage.py runserver
```

### Com Pip

```bash
# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Executar o servidor
python manage.py runserver
```

## Acessando a Documentação

Após iniciar o servidor, acesse a documentação Swagger em:
- http://localhost:8000/swagger/ 
- http://localhost:8000/redoc/

## Endpoints Disponíveis

### Webhook
- `POST /webhook/` - Recebe eventos de webhook

### Conversas
- `GET /conversations/{conversation_id}/` - Retorna detalhes de uma conversa específica

## Exemplos de Payloads para Webhooks

### Novo evento de conversa iniciada
```json
{
    "type": "NEW_CONVERSATION",
    "timestamp": "2025-02-21T10:20:41.349308",
    "data": {
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### Novo evento de mensagem recebida
```json
{
    "type": "NEW_MESSAGE",
    "timestamp": "2025-02-21T10:20:42.349308",
    "data": {
        "message_id": "49108c71-4dca-4af3-9f32-61bc745926e2",
        "direction": "RECEIVED",
        "content": "Olá, tudo bem?",
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### Novo evento de mensagem enviada
```json
{
    "type": "NEW_MESSAGE",
    "timestamp": "2025-02-21T10:20:44.349308",
    "data": {
        "message_id": "16b63b04-60de-4257-b1a1-20a5154abc6d",
        "direction": "SENT",
        "content": "Tudo ótimo e você?",
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

### Novo evento de conversa encerrada
```json
{
    "type": "CLOSE_CONVERSATION",
    "timestamp": "2025-02-21T10:20:45.349308",
    "data": {
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}
```

## Administração

Para acessar o painel de administração do Django:

1. Crie um superusuário:
```bash
python manage.py createsuperuser
```

2. Acesse o painel em:
```
http://localhost:8000/admin/
```

3. Faça login com as credenciais criadas.