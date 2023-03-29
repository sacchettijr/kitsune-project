# KITSUNE PROJECT

Projeto criado por um grupo de amigos apenas para fins de conhecimento e estudo. 

---

## Requisitos

Para o projeto funcionar como deve é necessário que possua no computador os seguintes programas:

- Terminal
- Docker
- WSL2 (Windows)

Caso seja necessário, recomendo [esse tutorial](https://youtu.be/05YN8F8ajBc) para instalação. 

---

## Execução

Para iniciar o sistema só é necessário estar na pasta do projeto com o terminal e ser executado o comando do Docker. Assim, o próprio Docker vai se responsabilizar em instalar os programas necessários (ex.: banco de dados) e subir a aplicação. O comando para criar e subir a aplicação: 

```
docker compose up --build
```

Se tudo ocorreu corretamente, será possivel acessar a página das aplicações pelo endereço local + porta. Exemplo: 

Serviço     |   Endereço
:----------:|:-----------------:
Django      |   127.0.0.1:8000
pgAdmin     |   127.0.0.1:5050
PostgreSQL  |   127.0.0.1:5432
---