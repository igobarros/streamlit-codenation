
'''
@Autor: Igo Pereira Barros
@Email: igorestacioceut@gmail.com

'''


# ---------------------------------- Bibliotecas -------------------------------------

import base64
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder, LabelEncoder

import smtplib
from email.message import Message

from pymongo import MongoClient

from settings import CONFIG_MONGODB, CONFIG_GMAIL



# -------------------------------- Gera link para download do dataset ---------------------------

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    	in:  dataframe
    	out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return b64


# ---------------------------- Calcula a correlação das variáveis categóricas -------------------

def conditional_entropy(x, y):

    """

    Calculates the conditional entropy of x given y: S(x|y)



    Wikipedia: https://en.wikipedia.org/wiki/Conditional_entropy



    :param x: list / NumPy ndarray / Pandas DataFrame

        A sequence of measurements

    :param y: list / NumPy ndarray / Pandas DataFrame

        A sequence of measurements

    :return: float

    """

    # entropy of x given y

    y_counter = Counter(y)

    xy_counter = Counter(list(zip(x,y)))

    total_occurrences = sum(y_counter.values())

    entropy = 0.0

    for xy in xy_counter.keys():

        p_xy = xy_counter[xy] / total_occurrences

        p_y = y_counter[xy[1]] / total_occurrences

        entropy += p_xy * np.log(p_y/p_xy)

    return entropy


# ------------------------------ Enviar email ----------------------------------------

def send_mail(sender_mail, password, receiver_mail, subject_matter, text_email):
	'''
	    Informações:
	    -----------
		    sender_mail:
                - email do usuário emissor
                - tipo string
	        password:
	            - senha do usuário emissor
	            - tipo string
	        receiver_mail:
	            - email do usuário receptor
	            - tipo string
		    subject_matter:
		        - assunto do email enviado
		        - tipo string
		    text_email:
		        - texto que será enviado
		        - tipo string
	'''

	try:
		msg = Message()
		msg['Subject'] = subject_matter
		msg['From'] = sender_mail
		msg['To'] = receiver_mail
		msg.add_header('Content-Type','text/html')
		msg.set_payload(text_email)

		# Send the message via local SMTP server.
		s = smtplib.SMTP('smtp.gmail.com:587')
		s.starttls()
		s.login(str(sender_mail), str(password))
		s.sendmail(str(sender_mail), str(receiver_mail), msg.as_string().encode(encoding='utf-8'))
		s.quit()
	except Exception as e:
		raise e




# ----------------------------- Configurações de cache de leitura de arquivos do Streamlit -------------------------------
class FileReference:
    def __init__(self, filename):
        self.filename = filename


def hash_file_reference(file_reference):
    filename = file_reference.filename
    return (filename, os.path.getmtime(filename))



# -------------------------------- Sidebar -------------------------------------
st.sidebar.title('Carregando os dados')

select_datas = st.sidebar.selectbox('Escolha a extensão do arquivo', options=[
		'Selecione uma opção'
		, 'csv'
		, 'xlsx'
		, 'Base tutorial - Servidor(MongoAtlas) Base(House Price - Kaggle)'
	])


file = st.sidebar.file_uploader('Uploader do arquivo', type=select_datas)

# Carregando os dados de arquivo
@st.cache(hash_funcs={FileReference: hash_file_reference})
def read_file_data(file):
	if file is not None:
		if select_datas == 'csv':
			df = pd.read_csv(file)
			return df
		elif select_datas == 'xlsx':
			df = pd.read_excel(file)
			return df

# Carregando os dados do MongoAtlas
@st.cache(hash_funcs={MongoClient: id})
def datas_tutorial():
	return MongoClient(CONFIG_MONGODB['MONGO_URI'])
		


# -------------------------- Conteúdo da página principal -----------------------

def main():

	# Muda a cor de background da página
	st.markdown('''
				
				<style>
				section {
				    color: #000000;
				    background-color: rgb(240,248,255);
				    etc. 
				}
				</style>
			''', unsafe_allow_html=True)
	

	df = read_file_data(file)

	
	if not isinstance(df, pd.DataFrame):
		if select_datas == 'Base tutorial - Servidor(MongoAtlas) Base(House Price - Kaggle)':
			client = datas_tutorial()
			db = client[CONFIG_MONGODB['MONGO_DB']]
			collections = db[CONFIG_MONGODB['MONGO_COLLECTIONS']]
			df = pd.DataFrame.from_records(data=collections.find({}, projection={'_id': False}))


	if df is not None:

		st.title('Pré-processamento dos dados - Regressão')

		exploration = pd.DataFrame({
			'columns' : df.columns
			, 'types' : df.dtypes
			, 'NA #': df.isna().sum()
			, 'NA %' : (df.isna().sum() / df.shape[0]) * 100
		})


		num_features = df.select_dtypes(include=[np.number]).copy()
		cat_features = df.select_dtypes(exclude=[np.number]).copy()

		# ---------------------------- INFORMAÇÕES DA BASE ------------------------------------

		st.markdown('# Informações da base')
		if st.checkbox('Show raw data'):
			value = st.slider('Choose a number the lines', min_value=1, max_value=100, value=5)
			st.dataframe(df.head(value), width=900, height=600)
			st.markdown('** Dimenssão da base**')
			st.markdown(df.shape)
			st.markdown('**Informações estatísticas descritiva dos dados**')
			st.dataframe(df.describe(), width=900, height=600)
			st.markdown('**Algumas informações da base como (nome da coluna, tipo, números de NaNs e porcentagem de NaNs)**')
			st.dataframe(exploration, width=900, height=600)


		# ------------------------- IMPUTAÇÃO DOS DADOS --------------------------------------	



		st.markdown('# Imputação das variáveis')

		percentual = st.slider('Informe um limite de percentual de valor faltante para imputar os dados', min_value=0, max_value=100)
		num_columns_list = list(exploration[(exploration['NA %']  > percentual) & (exploration['types'] != 'object')]['columns'])
		cat_columns_list = list(exploration[(exploration['NA %']  > percentual) & (exploration['types'] == 'object')]['columns'])

		st.markdown(num_columns_list)


		# ---------------------------- Variáveis Numéricas --------------------------------------

		st.markdown('### Imputação das variáveis numéricas')

		
		#features_nan = st.multiselect('Informe as colunas para imputação', options=num_columns_list)

		imputer = st.selectbox('Escolha uma opção de imputação', options=(
			'Selecione uma opção',
			'Imputar por -1',
			'Imputar por 0',
			'Imputar pela média',
			'Imputar pela mediana',
			'Imputar pela moda',
			'Dropar'
		))


		if imputer == 'Imputar por -1':
			num_features.fillna(-1, inplace=True)
			

		elif imputer == 'Imputar por 0':
			num_features.fillna(0, inplace=True)
			

		elif imputer == 'Imputar pela média':
			num_features.fillna(num_features[num_columns_list].mean(), inplace=True)
			

		elif imputer == 'Imputar pela mediana':
			num_features.fillna(num_features[num_columns_list].median(), inplace=True)


		elif imputer == 'Imputar pela moda':
			num_features.fillna(num_features[num_columns_list].mode(), inplace=True)

		elif imputer == 'Dropar':
			num_features.dropna(axis=1, inplace=True)


		# ------------------------- Variáveis Categóricas -------------------------
		st.markdown('### Imputação dos dados categóricos')

		st.markdown(cat_columns_list)

		#cat_features_nan = st.multiselect('Informe as colunas para imputação', options=cat_columns_list)

		cat_imputer = st.selectbox('Escolha uma opção de imputação', options=(
			'Selecione uma opção',
			'Imputar com Unknown',
			'Imputar com Missing',
			'Dropar'
		))


		if cat_imputer == 'Imputar com Unknown':
			cat_features.fillna('Unknown',inplace=True)


		elif cat_imputer == 'Imputar com Missing':
			cat_features.fillna('Missing', inplace=True)


		elif cat_imputer == 'Dropar':
			cat_features.dropna(axis=1, inplace=True)


		# ------------------------------ CORRELAÇÃO DAS VARIÁVEIS -----------------------------

		st.markdown('# Correlação das variáveis')

		select_corr = st.selectbox('Informe o método de correlação que deseja aplicar', options=(
			'Selecione uma opção'
			, 'pearson'
			, 'kendall'
			, 'spearman'
		))

		if st.checkbox('Qual método usar ?'):
			st.markdown('''
				**Correlação de Person**
				* Variáveis quantitativas
				* Variáveis com distribuição normal ou amostra suficientimente grade
				* Preferível para relações do tipo linear

				**Correlação de Kerdell**
				* Variáveis em escala ordinal
				* Preferível quando se têm amostras pequenas

				**Correlação de Spearman**
				* Variáveis quantitativas ou em escala ordinal
				* Utilizar quando não se tem a normalidade das variáveis
				* Preferível quando não se tem uma relação linear

			''')

		if select_corr != 'Selecione uma opção':
			if df.shape[1] <= 30:
				plt.rcParams['figure.figsize'] = (10, 8)
				sns.heatmap(num_features.corr(method=select_corr), annot=True, linewidths=0.5, linecolor='black', cmap='Blues')
				st.pyplot(dpi=100)
			else:
				plt.rcParams['figure.figsize'] = (20, 10)
				sns.heatmap(num_features.corr(method=select_corr), annot=True, linewidths=0.5, linecolor='black', cmap='Blues')
				st.pyplot(dpi=100)

		
		num_fit_features = st.multiselect('Selecione as features mais imporantes', options=list(num_features.columns))


		# -------------------------------- TRANSFORMAÇÃO DAS VARIÁVEIS ------------------------

		st.markdown('# Transformação das variáveis dependentes')

		st.markdown('### Variáveis numéricas')

		option_scaler = st.selectbox('Escolhe o método de transformação', options=(
			'Selecione uma método'
			, 'Normalização'
			, 'Padronização'
		))


		if option_scaler == 'Normalização':
			for col in num_features[num_fit_features].columns:
				minmaxscaler = MinMaxScaler()
				num_features[col] = minmaxscaler.fit_transform(num_features[col].values.reshape(-1, 1))

			st.dataframe(num_features[num_fit_features].head())

		elif option_scaler == 'Padronização':
			for col in num_features[num_fit_features].columns:
				standardscaler = StandardScaler()
				num_features[col] = standardscaler.fit_transform(num_features[col].values.reshape(-1, 1))

			st.dataframe(num_features[num_fit_features].head())

		st.markdown('### Variáveis categóricas')

		op = list(df.columns)
		op.insert(0, 'Selecione uma opção')
		select_cat_corr = st.selectbox('Informe a variável independente/alvo/target para calcular a correlação com as features categóricas', options=op)
		
		cat_corr = {}

		if select_cat_corr != 'Selecione uma opção':
			for col in cat_features.columns:
				cat_corr[col] = conditional_entropy(cat_features[col], df[select_cat_corr])
		
		series_cat_corr = pd.Series(cat_corr, name='correlation')
		st.dataframe(series_cat_corr)

		select_cat_features = st.multiselect('Selecione as variáveis categóricas que serão transformadas', options=list(cat_features.columns))

		radio_cat_fit_features = st.radio('Selecione o método de transformação', options=(
			'Marque o método de transformação'
			, 'OneHotEncoder'
			, 'LabelEncoder'
		))

		if radio_cat_fit_features == 'OneHotEncoder':
			for col in cat_features[select_cat_features].columns:
				onehot = OneHotEncoder(sparse=False, handle_unknown='ignore')
				cat_features[col] = onehot.fit_transform(cat_features[col].values.reshape(-1, 1))

		elif radio_cat_fit_features == 'LabelEncoder':
			for col in cat_features[select_cat_features].columns:
				labelencoder = LabelEncoder()
				cat_features[col] = labelencoder.fit_transform(cat_features[col].values.reshape(-1, 1))

		st.markdown('#### Base tratada - Final')
		X = pd.concat([num_features[num_fit_features], cat_features[select_cat_features]], axis=1)
		st.dataframe(X.head(), width=900, height=600)


		# -------------------------------- TRANSFORMAÇÃO DA TARGET ------------------------

		st.markdown('# Transformação da variável independente/target')

		op2 = list(df.columns)
		op2.insert(0, 'Selecione uma opção')
		select_target = st.selectbox('Target', options=op2)

		select_method = st.selectbox('Selecione o método de transformação', options=(
			'Selecione uma opção'
			, 'Raiz quadrada'
			, 'Logarítica log'
			, 'Logarítica log1p'
		))

		if select_method == 'Raiz quadrada':
			X['target'] = np.sqrt(df[select_target].copy())

		elif select_method == 'Logarítica log':
			X['target'] = np.log(df[select_target].copy())

		elif select_method == 'Logarítica log1p':
			X['target'] = np.log1p(df[select_target].copy())

		st.dataframe(X.head(), width=900, height=600)


		# --------------------- DOWNLOAD DA BASE PRÉ-PROCESSADA | Suporte Técnico -------------------

		select_download = st.sidebar.selectbox('Download da base | Suporte a plataforma', options=(
			'Selecione uma opção'
			, 'Link para download'
			, 'Dúvida sobre a plataforma'
		))

		if select_download == 'Link para download':

			if not X.empty:
				b64 = get_table_download_link(X)

				st.sidebar.markdown(f'''

					<style>
						.button {{
						  display: block;
						  padding: 8px 16px;
						  font-size: 16px;
						  cursor: pointer;
						  text-align: center;
						  text-decoration: none;
						  outline: none;
						  color: #fff;
						  background-color:rgba(246, 51, 102, .6);
						  border: none;
						  border-radius: 15px;
						  box-shadow: 0 9px #999;
						  margin:auto;
						}}

						.button:hover {{
							background-color:rgba(246, 51, 102);
						}}

						.button:active {{
						  background-color:rgba(246, 51, 102);
						  box-shadow: 0 5px #666;
						  transform: translateY(4px);
						}}
					</style>
					
					<a style="text-decoration:none;" href="data:file/csv;base64,{b64}" download="preprocessed.csv"><button class="button">Download</button></a>
				''', unsafe_allow_html=True)
			else:
				st.sidebar.text('Complete o pré-processamento')


		elif select_download == 'Dúvida sobre a plataforma':
			subject_matter = st.sidebar.text_input(label='ASSUNTO - Pressione enter e avançe para o próximo campo')
			email = st.sidebar.text_input(label='SEU EMAIL - Pressione enter e avançe para o próximo campo')
			text_mail = st.sidebar.text_area(label='MENSAGEM - Pressione Ctrl + Enter')

			complete_text_mail = f'<b>E-mail - {email}</b><br /><br /> <h3>Descrição:</h3><p align="justify">{text_mail}</p>'

			if subject_matter and email and text_mail:

				send_mail(CONFIG_GMAIL['SENDER_MAIL']
						, CONFIG_GMAIL['PASSWORD']
						, CONFIG_GMAIL['RECEIVER_MAIL']
						, subject_matter
						, complete_text_mail)


	else:

		# -------------------------- Vídeo da página inicial ----------------------------------

		st.title('Codenation - Aceleradev Data Science')

		def video_youtube(src: str, width="100%", height=315):
			
			st.write(
				f'<iframe width="{width}" height="{height}" src="{src}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
				unsafe_allow_html=True,
			)

		video_youtube(src="https://www.youtube.com/embed/5gD2zeEqAQs")

		st.sidebar.image('logo.png', width=300)
		
		st.markdown('### Apresentação: ')
		st.image('autor.png', width=100)
		st.markdown('[**Linkedin - Igo Pereira Barros**](https://www.linkedin.com/in/igo-pereira-barros-developer/)')
		st.markdown('[**Linkedin - Codenation**](https://www.linkedin.com/company/code-nation)')
		st.markdown('[**Discord - Codenation**](https://discord.gg/AvxQRyF)')

			
if __name__ == '__main__':
	main()
