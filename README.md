
# Celery Python Floripa

Este é um projeto que demonstra como integrar uma aplicação Python com **Celery**, **RabbitMQ** e **Redis** utilizando contêineres Docker. O objetivo é apresentar a configuração e execução de tarefas assíncronas em um ambiente containerizado.

## Tecnologias Utilizadas

- **Python 3.10**
- **Celery**
- **RabbitMQ**
- **Redis**
- **Docker** e **Docker Compose**

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração e Execução](#configuração-e-execução)
  - [1. Clonar o repositório](#1-clonar-o-repositório)
  - [2. Configurar variáveis de ambiente (opcional)](#2-configurar-variáveis-de-ambiente-opcional)
  - [3. Construir e executar os contêineres](#3-construir-e-executar-os-contêineres)
  - [4. Acessar a aplicação](#4-acessar-a-aplicação)
  - [5. Testar a aplicação](#5-testar-a-aplicação)
- [Como Funciona](#como-funciona)
  - [Fluxo](#fluxo)

## Pré-requisitos

- **Docker** instalado em sua máquina. [Instale o Docker aqui](https://www.docker.com/get-started).
- **Docker Compose** instalado. Geralmente, já vem com o Docker Desktop.

## Estrutura do Projeto

```plaintext
.
├── Dockerfile
├── docker-compose.yaml
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── celery_app.py
│   ├── tasks.py
│   └── requirements.txt
```

## Configuração e Execução

### 1. Clonar o repositório

Clone o repositório para a sua máquina local:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git](https://github.com/escobar-felipe/celery-python-floripa
cd celery-python-floripa
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto e defina as variáveis:
```bash
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/
```

### 3. Construir e executar os contêineres

Execute o comando abaixo para construir as imagens Docker e iniciar todos os serviços:

```bash
docker-compose up --build
```

Isso irá:

- Construir a imagem da aplicação Python.
- Baixar as imagens do RabbitMQ e Redis se ainda não estiverem presentes.
- Iniciar os contêineres `api`, `worker`, `rabbitmq` e `redis`.

### 4. Acessar a aplicação

- Acesse a API em: [http://localhost:8000](http://localhost:8000)
- A documentação interativa da API (Swagger UI) estará disponível em: [http://localhost:8000/docs](http://localhost:8000/docs)
- Acesse a interface de gerenciamento do RabbitMQ em: [http://localhost:15672](http://localhost:15672) (usuário: `guest`, senha: `guest`)

### 5. Testar a aplicação

Você pode testar a funcionalidade enviando uma requisição HTTP para a API. Por exemplo, usando `curl`:

```bash
curl -X POST http://localhost:8000/add      -H "Content-Type: application/json"      -d '{"x": 10, "y": 20}'
```

Resposta esperada:

```json
{
  "task_id": "c1d6f6f0-2b9e-4a6e-bd92-2f1e8c1b9e74"
}
```

Isso enviará uma tarefa para o Celery somar 10 + 20 de forma assíncrona.

Para verificar o resultado da tarefa, você precisará implementar um endpoint ou método para consultar o estado da tarefa usando o `task_id` retornado.

Exemplo:

```bash
curl http://localhost:8000/result/{task_id}
```

**Nota**: A implementação deste endpoint não está inclusa por padrão. Você pode adicioná-la conforme necessário.

## Como Funciona

- **FastAPI (`app/main.py`)**: Fornece uma API REST para receber requisições do usuário. Quando uma requisição é recebida, uma tarefa é enviada para o Celery processar.
- **Celery Worker (`app/celery_app.py` e `app/tasks.py`)**: Recebe tarefas da fila (gerenciada pelo RabbitMQ) e as executa de forma assíncrona.
- **RabbitMQ**: Atua como broker de mensagens, gerenciando a fila de tarefas.
- **Redis**: Armazena os resultados das tarefas executadas pelo Celery.

### Fluxo

1. O cliente envia uma requisição para a API.
2. A API enfileira uma tarefa no RabbitMQ.
3. O Celery Worker consome a tarefa da fila e a executa.
4. O resultado é armazenado no Redis.
5. O cliente pode consultar o resultado da tarefa usando o `task_id`.
