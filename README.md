# Pré-processamento - Regressão com Streamlit

### Aceleradev Data Science - Codenation

## Como rodar o projeto:

**Linux e Mac**
```
$ pip install virtualvenv
$ virtualenv .venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

**Windows**
```
> pip install virtualenv
> virtualenv venv
> ..\venv\Scripts\activate
> pip install -r requirements.txt
```

## Configurando o projeto
<h3>Suporte a E-mail</h3>

No arquivo ```settings.py``` altere as credenciais do dicionário ```CONFIG_GMAIL``` para as do seu email que deseja vincular ao app.
```
CONFIG_GMAIL = {
	'SENDER_MAIL': 'usuario@bacana.com',
	'PASSWORD': 'usuario12345',
	'RECEIVER_MAIL': 'usuario@bacana.com'
}
```

**DICAS:**

<p align="justify">1- Faça uma nova conta de email apenas para realizar esse procedimento, mas não impede de você usar seu email pessoal é só uma recomendação.</p>
<p align="justify">2 - Pode ser que em algum determinado momento o envio de email gere um erro, o mesmo ocorre porque o Gmail bloqueia o acesso de terceiros ao email via conexão SMTPLIB. Para reverter essa situação acesse esse [site](https://myaccount.google.com/lesssecureapps) de configurações do gmail e ative a opção de aceitar aplicativos menos seguros.</p>

<h3>Suporte a MongoDB Local e MongoDB na nuvem(MongoAtlas)</h3>

No arquivo ```settings.py``` altere as credenciais do dicionário ```CONFIG_MONGODB``` para as do seu banco de dados.

```
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
https://streamlit-regressao.herokuapp.com/

## Apresentando a plataforma

<p align="justify">O objetivo do app é realizar pré-processamento em bases com problemas do tipo regressão</p>
<p align="justify">Procedimentos realizados oferecido pelo app:</p>

	1 - Informações da base
	2 - Imputação dos dados (Numéricas e Categóricas)
	3 - Correlação das variáveis
	4 - Transformação das variáveis dependentes (Numéricas e Categóricas)
	5 - Transformação da variável independente/target

<p align="justify">Página inicial do app</p>
<img src="mainpage.png" alt="Conteúdo da página principal" width="800" height="600">

## Apresentações e agradecimentos
<p align="justify">A codenation oferece programas de aceleração gratuitos para desenvolvedoras e desenvolvedores buscando atualização profissional e novas oportunidades de trabalho. E neste mês de abril de 2020 tive a oportunidade de participar da acaleração em data science e estou bastante animado com o programa, comunidade ativa, suporte de ótima qualidade e conteúdos incríveis.</p>


<div style="display: inline-block;">
	<img src="autor.png" alt="Autor - Igo Pereira Barros" width="100" height="100">
	<span style="display: flow-root;">
		<a href="https://www.linkedin.com/in/igo-pereira-barros-developer/" target="_black">Linkedin - Autor</a>
	</span>
</div>

<div style="display: inline-block; padding-left: 50px;">
	<img src="logo.png" align="Codenation" width="100" height="100">
	<span style="display: flow-root;">
		<a href="https://www.linkedin.com/company/code-nation" target="_black">Linkedin - Codenation</a>
	</span>
</div>


## Licensa
Esse projeto é de código aberto com licensa do MIT LICENSE.