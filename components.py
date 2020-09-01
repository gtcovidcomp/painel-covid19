import plotly.graph_objs as go
import plotly.express as px
import matplotlib.pyplot as plt
import dash_html_components as html
from plotly.subplots import make_subplots
from data.data import loc_dic
from plotly.tools import mpl_to_plotly
import pandas as pd
import numpy as np
import datetime

def series_general(df):
    figure=dict(
        data = [
            dict(
                x=df.groupby('Data').sum().index,
                y=df.groupby('Data').sum()['Casos Confirmados'],
                type = 'bar',
                name = 'Casos Confirmados',
                marker = {'color':'#4266ad'}
            ),
            dict(
                x=df.groupby('Data').sum().index,
                y=df.groupby('Data').sum()['Óbitos Confirmados'],
                name = 'Óbitos',
                marker = {'color':'#de0000'}
            ),
            dict(
                x=df.groupby('Data').sum().index,
                y=df.groupby('Data').sum()['Casos Recuperados'],
                name = 'Recuperados',
                marker = {'color':'#6cd100'}
            )
        ],
        layout=dict(
            height= 340, 
            title='Casos Confirmados x Óbitos',
            font={'size':14},
            margin=dict(
                l=40,
                r=40,
                b=20,
                t=60,
                pad=4
            ),
            legend=dict(x=0, y=1),
            xaxis=go.layout.XAxis(
                rangeselector=dict(
                    buttons=list([
                        dict(count=15,
                            label="15d",
                            step="day",
                            stepmode="todate"),
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="todate"),
                        dict(step="all")
                    ])
                ),
                rangeslider = dict(visible = True)
            )
        )
    )
    return figure


def bubble_map(df):
    if len(df) % 2 ==1:
        df = df[df['Data'].isin(df['Data'].unique()[::2])]
    else:
        df= df[df['Data'].isin(df['Data'].unique()[1::2])]
    map = px.scatter_mapbox(
        df,
        lon = 'lon',
        lat = 'lat',
        hover_name = 'Cidade',
        hover_data = {'Data_str':True,'Casos Recuperados':True, 'Óbitos Confirmados':True,
            'Casos Confirmados':True,'lat':False,'lon':False},
        size = 'Casos Confirmados',
        labels = {'Data_str':'Data'},
        color_discrete_sequence = ['#4266ad'],
        animation_frame = 'Data_str'
    )
    map.update_layout(
        height = 450,
    	margin=dict(l=0,r=0,b=0,t=0,pad=0),
        hovermode='closest',
        mapbox = dict(
            accesstoken= 'pk.eyJ1Ijoic2RzZGdodCIsImEiOiJjazlvdmozbm0wNHhsM2dxc28zc3RhbTFuIn0.jIjBLxeeNBXO4RD2q8g_bg',
            style = 'mapbox://styles/sdsdght/ck9oyqv8p2mul1ipbhjqly64k/draft',
            center = dict(lat=-22,lon= -42.5),
            zoom = 6
        ),
    )
    map.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 100
   # map.layout.sliders[0]['active'] = len(map.frames) - 1  # last date/frame
   # map.update_traces(marker=map.frames[-1].data[0].marker)
    return map

def bubble_map_bairros(df):
    df['Casos'] = df.groupby('BAIRRO')['BAIRRO'].transform('count')

    map = px.scatter_mapbox(
        df,
        lon = 'lon',
        lat = 'lat',
        hover_name = 'BAIRRO',
        hover_data = {
            'lat':False,'lon':False
        },
        size = 'Casos',
        labels = {'Data_str':'Data'},
        color_discrete_sequence = ['#4266ad'],
    )

    mean_lat = df['lat'].mean()
    mean_lon = df['lon'].mean()

    map.update_layout(
        height = 450,
    	margin=dict(l=0,r=0,b=0,t=0,pad=0),
        hovermode='closest',
        mapbox = dict(
            accesstoken= 'pk.eyJ1Ijoic2RzZGdodCIsImEiOiJjazlvdmozbm0wNHhsM2dxc28zc3RhbTFuIn0.jIjBLxeeNBXO4RD2q8g_bg',
            style = 'mapbox://styles/sdsdght/ck9oyqv8p2mul1ipbhjqly64k/draft',
            center = dict(lat=mean_lat,lon=mean_lon),
            zoom = 9
        ),
    )
    return map

def series_comparacao(df):
    series_casos_obitos = make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=0.05,
        x_title='Data')

    colors = px.colors.qualitative.Plotly

    for index, cidade in enumerate(df['Cidade'].unique()):
        series_casos_obitos.add_trace(go.Scatter(
            y = df[df['Cidade'] == cidade]['Casos Confirmados'],
            x = df[df['Cidade'] == cidade]['Data'],
            name = cidade,
            legendgroup = cidade,
            marker = dict(color = colors[index])),
            row = 1,
            col = 1
        )
        series_casos_obitos.add_trace(go.Scatter(
            y = df[df['Cidade'] == cidade]['Óbitos Confirmados'],
            x = df[df['Cidade'] == cidade]['Data'],
            name = '',
            legendgroup = cidade,
            showlegend = False,
            marker = dict(color = colors[index])),
            row = 2,
            col = 1
        )

    series_casos_obitos.update_yaxes(title_text = "Casos", row=1, col=1)
    series_casos_obitos.update_yaxes(title_text = "Óbitos", row=2, col=1)
    series_casos_obitos.update_layout(height= 360, margin=dict(l=20,r=10,b=60,t=10,pad=0), template = 'plotly_white')
    return series_casos_obitos

def series_barreira(df2):
    series_barr_san = dict(
        data = [
            dict(
                x=df2.groupby('Data').size().index,
                y=df2.groupby('Data').size(),
                name = 'Barreira Sanitária - Macaé',
                marker = {'color':'#191970'}
                )
            ],
        layout=dict(
            title='Nº de Pessoas Cruzando a Barreira Sanitária x Dia - Macaé',
            height = 300,
            font={'size':14},
            margin=dict(
                l=40,
                r=40,
                b=60,
                t=60,
                pad=4
            ),
            legend=dict(x=0, y=1)
        )
    )
    return series_barr_san

def series_projection(df_previsao):
    simulacao = dict(
        data = [
            dict(
                x=df_previsao['Data'],
                y=df_previsao['Infectados'],
                type = 'bar',
                name = 'Infectados',
                marker = {'color':'#4266ad'}
            ),
            dict(
                x=df_previsao['Data'],
                y=df_previsao['Previsao'],
                name = 'Projeção',
                marker = {'color':'#ff9900'}
            ),
            dict(
                x=df_previsao['Data'],
                y=df_previsao['Max'],
                name = 'Max',
                marker = {'color':'#de0000'},
                line = dict(dash='dash')
            ),
            dict(
                x=df_previsao['Data'],
                y=df_previsao['Min'],
                name = 'Min',
                marker = {'color':'#ded700'},
                line = dict(dash='dash')
            )
        ],
        layout=dict(
            title='Projeção de Casos Futuros',
            font={'size':14},
            margin=dict(
                l=40,
                r=40,
                b=60,
                t=60,
                pad=4
            ),
            legend=dict(x=0, y=1)
        )
    )
    return simulacao

def series_isolamento(df_isolamento):
    isolamento = go.Figure()

    colors = px.colors.qualitative.Plotly

    for index, cidade in enumerate(df_isolamento['city_name'].unique()):
        isolamento.add_trace(go.Scatter(
            y = df_isolamento[df_isolamento['city_name'] == cidade]['isolated'],
            x = df_isolamento[df_isolamento['city_name'] == cidade]['dt'],
            name = cidade,
            marker = dict(color = colors[index])),
        )

    isolamento.update_yaxes(title_text = "Taxa de Isolamento")
    isolamento.update_xaxes(title_text = "Data")
    isolamento.update_layout(height=300, margin=dict(l=30,r=30,b=10,t=10), template = 'plotly_white', font={'size':14})
    return isolamento

def series_bairros(df):
    df['BAIRRO']= df['BAIRRO'].str.upper()
    x = df['BAIRRO'].value_counts()
    pkmn_type_colors = ['#78C850',  # Grass
                    '#F08030',  # Fire
                    '#6890F0',  # Water
                    '#A8B820',  # Bug
                    '#A8A878',  # Normal
                    '#A040A0',  # Poison
                    '#F8D030',  # Electric
                    '#E0C068',  # Ground
                    '#EE99AC',  # Fairy
                    '#C03028',  # Fighting
                    '#F85888',  # Psychic
                    '#B8A038',  # Rock
                    '#705898',  # Ghost
                    '#98D8D8',  # Ice
                    '#7038F8',  # Dragon
                   ]

    data = go.Bar(x=x.values, y=x.index, orientation='h')
    bairro = go.Figure(data=[data])
    bairro.update_layout(height=360, margin=dict(l=20,r=10,b=0,t=10,pad=0))
    return bairro

    
def series_sintomas(df):
    febre = len(df[(df['FEBRE']=='Sim')])
    tosse = len(df[(df['TOSSE']=='Sim')])
    dispneia = len(df[(df['DISPNEIA']=='Sim')])
    garganta = len(df[(df['DOR DE GARGANTA']=='Sim')])
    outros = len(df[(df['OUTROS']=='Sim')])
    total = len(df)

    x = ['Dispneia', 'Febre', 'Tosse','Dor de garganta', 'Outros']
    y = [dispneia, febre, tosse, garganta, outros]
    per = [dispneia/total,febre/total,tosse/total,garganta/total,outros/total]
    perText = []
    for i in per:
      j = i*100
      perText.append("%.0f%s" % (j,"%"))
    
    # Use textposition='auto' for direct text
    fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=perText,
            textposition='auto',
            hovertext=y
        )])
    fig.update_layout(
    	height=300, margin=dict(l=10,r=10,b=0,t=10,pad=0),
        yaxis=dict(
            title='Número de casos positivos',
            titlefont_size=16,
            tickfont_size=14,
        )
    )

    return fig

def series_sexo(df):
    sex  = (((df['SEXO'].value_counts()/len(df)).round(3)*100))
    labels = sex.index
    dataSex= pd.DataFrame(sex,index=labels)

    colormap = {'Masculino': '#66b3ff', 'Feminino': '#ff9999'}
    fig = px.pie(dataSex, values='SEXO', names=dataSex.index, color=dataSex.index, color_discrete_map=colormap)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=300, margin=dict(l=10,r=10,b=0,t=10,pad=0), template = 'plotly_white')

    return fig

def series_faixa_etaria(df):
    #Dataframe apenas com colunas que interessam para essa visualização
    dfBairro = pd.DataFrame(df, columns = ['RESULTADO DO TESTE','BAIRRO', 'DATA DE NASCIMENTO', 'DATA INICIO DOS SINTOMAS'])
    #Garante que só ficará com os casos positivos
    dfBairro = dfBairro[dfBairro['RESULTADO DO TESTE'] == 'Positivo']
    #Rotina para calcular a idade dos pacientes
    dfBairro['DATA INICIO DOS SINTOMAS'] = pd.to_datetime(df['DATA INICIO DOS SINTOMAS'], format='%d/%m/%Y')
    dfBairro['DATA DE NASCIMENTO'] = pd.to_datetime(dfBairro['DATA DE NASCIMENTO'], format='%d/%m/%Y')
    tempoNascido = dfBairro['DATA INICIO DOS SINTOMAS'] - dfBairro['DATA DE NASCIMENTO']
    idade = [(i/365.25).days for i in tempoNascido]

    #Rotina para classificar os pacientes em faixas etárias
    faixaEtaria = []
    for i in idade:
      if i <= 9:
        faixaEtaria.append('0-9')
      elif i <= 19:
         faixaEtaria.append('10-19')
      elif i <= 29:
         faixaEtaria.append('20-29')
      elif i <= 39:
         faixaEtaria.append('30-39')
      elif i <= 49:
         faixaEtaria.append('40-49')
      elif i <= 59:
         faixaEtaria.append('50-59')
      elif i <= 69:
         faixaEtaria.append('60-69')
      else:
        faixaEtaria.append('>=70')

    #Acrescenta coluna Faixa Etária no DataFrame
    dfBairro['Faixa Etária'] = faixaEtaria

    #Remover colunas que não interessam mais
    dfBairro.drop('RESULTADO DO TESTE', axis=1, inplace=True)
    dfBairro.drop('DATA DE NASCIMENTO', axis=1, inplace=True)
    dfBairro.drop('DATA INICIO DOS SINTOMAS', axis=1, inplace=True)

    #Coloca nome dos bairros em maiúsculo
    dfBairro['BAIRRO'] = dfBairro['BAIRRO'].str.upper() 
    dfBairro['BAIRRO'] = dfBairro['BAIRRO'].str.strip() 

    dicDados = dict()
    for bairro in list(set(dfBairro['BAIRRO'])):
      dicDados[bairro] = {'0-9': 0, '10-19': 0, '20-29': 0, '30-39': 0, '40-49': 0, '50-59': 0, '60-69': 0, '>=70': 0} #cria um chave nova no dicionario com o nome desse bairro
      for ocorrencia in dfBairro.itertuples():
        if ocorrencia.BAIRRO == bairro:
          dicDados[bairro][ocorrencia[2]] = dicDados[bairro][ocorrencia[2]] + 1  

    #Gera Dataframe, dfDados, com os dados organizados para alimentar a tabela no Dash
    dfDados = pd.DataFrame.from_dict(dicDados, orient='index')
    #Coloca os bairros em ordem alfabética
    dfDados.sort_index(inplace=True)
    #Acrescenta coluna com total acumulado por bairro
    dfDados['Total'] = dfDados.sum(axis=1)
    #Acrescenta linha com total acumulado por faixa etária
    dfDados.loc['Total'] = dfDados.sum(axis=0)
    #Acrescenta coluna % com percentual por bairro
    dfDados['%'] = round((dfDados['Total']/dfDados['Total']['Total'])*100, 1)
    #Acrescenta linha % com percentual por faixa etária
    dfDados.loc['%'] = round((dfDados.loc['Total']/dfDados['Total']['Total'])*100, 1)
    #Limpa célula 
    dfDados['%']['%'] = ''
    #Reset index do Dataframe para que a primeira coluna seja nomeada com Bairro para ir para tabela no Dash
    dfDados.reset_index(inplace=True)
    dfDados.rename(columns={'index':'Bairro'}, inplace=True)

    fig = go.Figure(data=[go.Table(
        columnorder = [i for i in range(11)],
        columnwidth = [155] + [50] * 10,
        header=dict(values=list(dfDados.columns), align='left'),
        cells=dict(values=[dfDados['Bairro'], dfDados['0-9'], dfDados['10-19'], dfDados['20-29'], dfDados['30-39'], dfDados['40-49'], dfDados['50-59'], dfDados['60-69'], dfDados['>=70'], dfDados['Total'], dfDados['%']], align='left'))
    ])

    fig.update_layout(
        title = 'Casos confirmados de COVID-19 segundo Bairro de Residência e Faixa Etária ',
    	height=360, margin=dict(l=10,r=10,b=0,t=30,pad=0)
    )

    return fig

def series_acumulados(df):
    df['DATA INICIO DOS SINTOMAS'] = pd.to_datetime(df['DATA INICIO DOS SINTOMAS'], format='%d/%m/%Y')
    dataInicioSintomas = df['DATA INICIO DOS SINTOMAS']
    #Data inicial criada de acordo com arquivo fornecido pela prefeitura de Quissama
    #Na planilha o grafico de casos por semana comecou com 15-03-2020
    dataInicial = min(dataInicioSintomas)
    ultimaDataPlanilha = max(dataInicioSintomas)
    datas = [dataInicial + datetime.timedelta(days=x) for x in range(0, (ultimaDataPlanilha-dataInicial).days+7,7)]

    xdatas,yqnt,yqntAcu = [],[],[]
    for i in range(len(datas)-1):
      xdatas.append(datas[i])
      df2=df[df['DATA INICIO DOS SINTOMAS']>=datas[i]]
      quantidade = len(df2[df2['DATA INICIO DOS SINTOMAS']<datas[i+1]])
      yqnt.append(quantidade)
      yqntAcu.append(sum(yqnt)) 

    fig = go.Figure([go.Scatter(x=xdatas, y=yqntAcu)])
    fig.update_layout(
        title = 'Casos acumulados por semana de notificação',
    	height=300, margin=dict(l=10,r=10,b=0,t=30,pad=0)
    )
    return fig
