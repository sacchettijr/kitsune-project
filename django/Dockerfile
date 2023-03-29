#   APLICATIVO:VERSÃO
FROM python:latest
ENV PYTHONUNBUFFERED=1
#   APONTA O DIRETÓRIO OU CRIA CASO NÃO EXISTA
WORKDIR /app
#   COPIA OS REQUERIMENTOS PARA O PROJETO E INSTALA
COPY . /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#   CRIA USUÁRIO SEM PRIVILÉGIO
RUN adduser --disabled-password --gecos '' myuser