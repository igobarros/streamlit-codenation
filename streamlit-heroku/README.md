# Pré-processamento - Regressão com Streamlit

## Como rodar o projeto:

**Linux e Mac**
```bash
$ pip install virtualvenv
$ virtualenv .venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

**Windows**
```bash
> pip install virtualenv
> virtualenv venv
> ..\venv\Scripts\activate
> pip install -r requirements.txt
```

## Configurando o projeto
<h3>Suporte a E-mail</h3>

No arquivo ```settings.py``` altere as credenciais do dicionário ```CONFIG_GMAIL``` para as do seu email que deseja vincular ao app.
```py
CONFIG_GMAIL = {
	'SENDER_MAIL': 'usuario@bacana.com',
	'PASSWORD': 'usuario12345',
	'RECEIVER_MAIL': 'usuario@bacana.com'
}
```

**DICAS:**

- 1 - Faça uma nova conta de email apenas para realizar esse procedimento, mas não impede de você usar seu email pessoal é só uma recomendação
- 2 - Pode ser que em algum determinado momento o envio de email gere um erro, o mesmo ocorre porque o Gmail bloqueia o acesso de terceiros ao email via conexão SMTPLIB. Para reverter essa situação acesse esse [site](https://myaccount.google.com/lesssecureapps) de configurações do gmail e ative a opção de aceitar aplicativos menos seguros

<h3>Suporte a MongoDB Local e MongoDB na nuvem(MongoAtlas)</h3>

No arquivo ```settings.py``` altere as credenciais do dicionário ```CONFIG_MONGODB``` para as do seu banco de dados.

```py
CONFIG_MONGODB = {
	'MONGO_URI': 'mongodb://user:password@localhost:27017/admin',
	'MONGO_DB': 'NAME_DB',
	'MONGO_COLLECTIONS': 'NAME_COLLECTION'
}
```


**Execute o comando após a realização de todas as configurações acima**:
```
$ streamlit run app.py
```

## Link do projeto no heroku
https://app-regressao.herokuapp.com/

