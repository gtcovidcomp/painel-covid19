import pandas as pd
import os
from data.send_email import send_email
from data.download_files_GDrive import download_files_GDrive

cidades = ['Macaé','Campos dos Goytacazes','Quissamã','Carapebus','São Francisco de Itabapoana','São Fidélis',
    'São João da Barra','Conceição de Macabu','Rio das Ostras']
loc_dic = {'Campos dos Goytacazes':(-21.7545,-41.3244),
	'Macaé':(-22.3717,-41.7857),
	'Quissamã':(-22.1086,-41.4711),
	'Carapebus':(-22.2033,-41.6625),
	'São Francisco de Itabapoana':(-21.4737,-41.1202),
	'São Fidélis':(-21.6431,-41.7578),
	'São João da Barra':(-21.6488,-41.0526),
	'Conceição de Macabu':(-22.085000, -41.867778),
	'Rio das Ostras':(-22.5273,-41.9456)
	}

def dados_cidade(city):
    city_data = {'Quissamã':'quissama.xlsx'}
    if city not in city_data:
        return pd.DataFrame()

    path_dir = (os.path.dirname(os.path.abspath(__file__))+'/').replace('/','//')
    df = pd.read_excel(f'{path_dir}{city_data[city]}')

    df['EVOLUCAO DO CASO'] = df['EVOLUCAO DO CASO'].str.upper()
        
    return df

def update_df(sufix = ''):

    path_dir = (os.path.dirname(os.path.abspath(__file__))+'/').replace('/','//')
    nome_tabela = f'Tabela Informes Região Norte final{sufix}.xlsx'
    path_tabela_norte = f'{path_dir}{nome_tabela}'    
    try:
        colunas_consideradas = ['Data', 'Casos confirmados até o dia',
                                'Número de óbitos Confirmados', 'Casos recuperados']
    
        df_macae = pd.read_excel(path_tabela_norte, sheet_name='Macaé', usecols=colunas_consideradas)
        df_campos = pd.read_excel(path_tabela_norte, sheet_name='Campos dos Goytacazes', usecols=colunas_consideradas)
        df_quiss = pd.read_excel(path_tabela_norte, sheet_name='Quissamã', usecols=colunas_consideradas)
        df_carap = pd.read_excel(path_tabela_norte, sheet_name='Carapebus', usecols=colunas_consideradas)
        df_s_fran = pd.read_excel(path_tabela_norte, sheet_name='São Francisco', usecols=colunas_consideradas)
        df_s_joao = pd.read_excel(path_tabela_norte, sheet_name='São João da Barra', usecols=colunas_consideradas)
        df_s_fid = pd.read_excel(path_tabela_norte, sheet_name='São Fidelis', usecols=colunas_consideradas)
        df_macabu = pd.read_excel(path_tabela_norte, sheet_name='Conceição de Macabu', usecols=colunas_consideradas)
        df_r_ost = pd.read_excel(path_tabela_norte, sheet_name='Rio das Ostras', usecols=colunas_consideradas)
    
    
        for cidade, df in [('Macaé',df_macae),('Campos dos Goytacazes',df_campos),('Quissamã',df_quiss),
                            ('Carapebus',df_carap),('São Francisco de Itabapoana',df_s_fran),('São Fidélis',df_s_fid),
                            ('São João da Barra',df_s_joao),('Conceição de Macabu',df_macabu),('Rio das Ostras',df_r_ost)]:
            df['Cidade'] = cidade
            df.fillna(method = 'ffill', inplace = True)
            df.fillna(value = 0, inplace = True)
    
            
        df = pd.concat([df_macae,df_campos,df_quiss,df_carap,df_s_fran,df_s_fid,df_s_joao,df_macabu,df_r_ost])
        df.reset_index(inplace=True)
        df.drop(['index'], axis = 1, inplace = True)
    
        pop_dic = {'Campos dos Goytacazes': 507548,
                'Macaé': 256672,
                'Quissamã': 24700,
                'Carapebus': 16301,
                'São Francisco de Itabapoana': 42205,
                'São Fidélis': 38669,
                'São João da Barra':36102,
                'Conceição de Macabu':23228,
                'Rio das Ostras': 150674
                }
    
        
        def lat_lon_cidades(loc_dic, df):
            for cidade,lat_lon in loc_dic.items():
                df.loc[df['Cidade']== cidade,'lat'] = lat_lon[0]
                df.loc[df['Cidade']== cidade,'lon'] = lat_lon[1]
                df.loc[df['Cidade']== cidade,'pop'] = pop_dic[cidade]
            return df
    
        def remove_strings(num):
            try:
                int(num)
                return int(num)
            except:
                return 0
    
        df['Casos recuperados'] = df['Casos recuperados'].map(remove_strings)
        
        df = lat_lon_cidades(loc_dic, df)
    
        df['Data_str'] = df['Data'].map(lambda x: x.strftime('%d/%m/%y'))
    
        df.rename(columns={
            'Casos confirmados até o dia':'Casos Confirmados',
            'Número de óbitos Confirmados':'Óbitos Confirmados',
            'Casos recuperados':'Casos Recuperados'
            },
            inplace=True)
        df.sort_values(by=['Data','Cidade'],inplace=True)
        df.to_csv(f'{path_dir}Dados Cidades.csv',encoding='UTF-8')
        
        if sufix == '_new':
            old_name = path_tabela_norte
            new_name = path_tabela_norte.replace('_new','')
            os.remove(new_name)
            os.rename(old_name,new_name)
    except FileNotFoundError:
        update_df()
    except Exception as e:
        assunto = f'Alerta! - Erro no Tratamento de Dados do Arquivo {nome_tabela} - GT - Covid19'
        mensagem = f'Ao tentar fazer tratamento de dados do arquivo {nome_tabela} o seguinte erro ocorreu: \n{e}'
        print(f'{assunto}\n{50*"="}\n\n{mensagem}')
        send_email(assunto,mensagem)
        if sufix == '_new':
            os.remove(path_tabela_norte)
            update_df()

#Barreira Sanitária
def update_df2():
    path_dir = (os.path.dirname(os.path.abspath(__file__))+'/').replace('/','//')
    nome_tabela = 'Banco Barreira Sanitária   - gráficos idade, temperatura, tosse, viagem ao exterior oucontato.xlsx'
    path_barreira_sanitaria = f'{path_dir}{nome_tabela}'

    col_cons = ['Carimbo de data/hora','Idade','De onde está vindo?',
                'Tem tosse, coriza ou dificuldade para respirar?',
                'Viajou para o exterior nos últimos 14 dias ou teve contato com paciente suspeito ou confirmado para o coronavírus?']

    df_barreira_sanitaria = pd.read_excel(path_barreira_sanitaria, sheet_name='Planilha temperatura corrig', usecols=col_cons)

    df_barreira_sanitaria.rename(columns={'Carimbo de data/hora':'Data',
                                        'Tem tosse, coriza ou dificuldade para respirar?':'Apresenta Sintomas',
                                        'Viajou para o exterior nos últimos 14 dias ou teve contato com paciente suspeito ou confirmado para o coronavírus?':'Risco de exposição ao vírus nos últimos 14 dias'
                                        },
                                        inplace=True)

    df2 = df_barreira_sanitaria.copy()
    df2['Data'] = df_barreira_sanitaria['Data'].map(lambda x: x.replace(hour=0,minute=0,second=0,microsecond=0,nanosecond=0))
    df2.to_csv(f'{path_dir}Dados Barreira.csv',encoding='UTF-8')

#Simulações
def update_df_previsao():
    path_dir = (os.path.dirname(os.path.abspath(__file__))+'/').replace('/','//')
    nome_tabela = 'Simulação Macaé.xlsx'
    path_previsao = f'{path_dir}{nome_tabela}'

    df_previsao = pd.read_excel(path_previsao, sheet_name='Resultados')

    df_previsao.rename(columns={'dia/mes/ano':'Data',
                                'infectado (acumulado)':'Infectados',
                                'provável (SIR)': 'Previsao',
                                'min SIR': 'Min',
                                'max SIR': 'Max'
                                },
                            inplace = True)
    df_previsao.to_csv(f'{path_dir}Dados Previsão.csv',encoding='UTF-8')

#Isolamento
def update_df_isolamento(sufix = ''):
    path_dir = (os.path.dirname(os.path.abspath(__file__))+'/').replace('/','//')
    nome_tabela = f'Social Distancing Index by Cities{sufix}.csv'
    path_isolamento = f'{path_dir}{nome_tabela}'
    try:
        df_isolamento = pd.read_csv(path_isolamento)
        df_isolamento = (df_isolamento.loc[
                (df_isolamento['dt']>'2020-03-20') & (df_isolamento['city_name'].isin(cidades))
                ]
            .reset_index().
            drop('index', axis = 1)
        )
        df_isolamento['dt'] = df_isolamento['dt'].map(lambda x: pd.to_datetime(x))
        df_isolamento.to_csv(f'{path_dir}Dados Isolamento.csv',encoding='UTF-8')
        if sufix == '_new':
            old_name = path_isolamento
            new_name = path_isolamento.replace('_new','')
            os.remove(new_name)
            os.rename(old_name,new_name)
    except FileNotFoundError:
        update_df_isolamento()
    except Exception as e:
        assunto = f'Alerta! - Erro no Tratamento de Dados do Arquivo {nome_tabela} - GT - Covid19'
        mensagem = f'Ao tentar fazer tratamento de dados do arquivo {nome_tabela} o seguinte erro ocorreu: \n{e}'
        print(f'{assunto}\n{50*"="}\n\n{mensagem}')
        if sufix == '_new':
            os.remove(path_isolamento)
            update_df_isolamento()

loc_dict_bairros = {
    'Quissamã':{
        'ALTO ALEGRE': {'LAT': -22.110808, 'LON': -41.472971}, 
        'BARRA DO FURADO': {'LAT': -22.096724, 'LON': -41.142647}, 
        'CANTO DA SAUDADE': {'LAT': -22.101349, 'LON': -41.469348}, 
        'CARMO': {'LAT': -22.11883, 'LON': -41.489809}, 
        'CAXIAS': {'LAT': -22.114061, 'LON': -41.468117}, 
        'CENTRO': {'LAT': -22.106822, 'LON': -41.471757000000004}, 
        'MACHADINHA': {'LAT': -22.032691, 'LON': -41.453122}, 
        'MATIAS': {'LAT': -22.10463, 'LON': -41.464644}, 
        'MORRINHOS': {'LAT': -22.129054999999997, 'LON': -41.58422}, 
        'MORRO ALTO': {'LAT': -22.107437, 'LON': -41.58894}, 
        'PENHA': {'LAT': -22.143889, 'LON': -41.517185999999995}, 
        'PINDOBAS': {'LAT': -22.113943, 'LON': -41.610628999999996}, 
        'PITEIRAS': {'LAT': -22.11354, 'LON': -41.480154999999996}, 
        'PRAIA DE JOÃO FRANCISCO': {'LAT': -22.208327, 'LON': -41.473637}, 
        'SANTA CATARINA': {'LAT': -22.072317, 'LON': -41.495179}, 
        'SITIO QUISSAMÃ': {'LAT': -22.105171, 'LON': -41.458549}, 
        'VISTA ALEGRE': {'LAT': -22.114483, 'LON': -41.470521999999995}, 
        'VIVENDAS DO CANAL': {'LAT': -22.106324, 'LON': -41.476812}, 
        'FLEXEIRAS': {'LAT': -22.118848, 'LON': -41.24134}, 
        'CAPIVARI': {'LAT': -22.092449, 'LON': -41.296377}, 
        'ALTO GRANDE': {'LAT': -22.131156, 'LON': -41.527498}, 
        'CANTO DE SANTO ANTÔNIO': {'LAT': -22.149607999999997, 'LON': -41.544412}, 
        'MANDIQUERA': {'LAT': -22.119507000000002, 'LON': -41.514963}, 
        'SANTA FRANCISCA': {'LAT': -22.116564, 'LON': -41.548693}, 
        'RIBEIRA': {'LAT': -22.118356, 'LON': -41.4662}, 
        'FLORESTA': {'LAT': -22.067104, 'LON': -41.516581}, 
        'GOIABAL': {'LAT': -22.125006, 'LON': -41.500838}, 
        'CONDE': {'LAT': -22.07183, 'LON': -41.605117}, 
        'BOA VISTA': {'LAT': -22.060682, 'LON': -41.471224}
    }
}
    
def lat_lon_bairros(cidade, df):
    if cidade not in loc_dict_bairros:
        return

    loc_dict = loc_dict_bairros[cidade]

    for bairro, lat_lon in loc_dict.items():
        df.loc[df['BAIRRO'] == bairro, 'lat'] = lat_lon['LAT']
        df.loc[df['BAIRRO'] == bairro, 'lon'] = lat_lon['LON']

    return df
