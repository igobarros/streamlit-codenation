# Pré-processamento - Regressão com Streamlit

## Rodando o projeto com docker

```
$ git clone https://github.com/igobarros/streamlit-codenation
$ cd streamlit-codenation/streamlit-docker
$ docker image build -t streamlit:app .
$ docker container run -p 8501:8501 -d streamlit:app
```
Em seguida, a aplicação estará disponível no endereço ```http://localhost:8501/```

Para encontrar o container referente a aplicação:

**Container específico a sua aplicação:**
```
$ docker ps | grep 'streamlit:app'
```

**Todos os containers:**
```
$ docker ps -a
```

**Comando para parar a execução do container:**
```
$ docker stop <id_container>
```

**Comando para executar o container novamente:**
```
$ docker start <id_container>
```