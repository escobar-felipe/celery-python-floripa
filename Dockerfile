FROM python:3.10-slim-buster

WORKDIR /opt/app/

RUN pip install --upgrade pip

COPY app/requirements.txt /opt/app/requirements.txt

RUN pip --no-cache-dir install -r requirements.txt

# Copie o diretório 'app' para dentro de '/opt/app/'
COPY app /opt/app/app

# Configure o PYTHONPATH para incluir '/opt/app/'
ENV PYTHONPATH="/opt/app:${PYTHONPATH}"

# Configurações adicionais
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

EXPOSE 8000
