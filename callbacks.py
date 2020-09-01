from app import app
from dash.dependencies import Input, Output
import dash_html_components as html
from data.data import update_df, update_df_isolamento, dados_cidade, lat_lon_bairros
import pandas as pd
import os, json
from components import series_general, bubble_map, series_comparacao, series_isolamento, series_bairros, series_sintomas
from components import series_sexo, series_faixa_etaria, series_acumulados, bubble_map_bairros
import plotly.graph_objs as go


########################### START Main Page Callbacks ###########################


@app.callback(
    Output('navbar','children'),
    [Input('url','pathname')])
def navbar_update (pathname):
    links = {
        'Página Inicial':'/',
        'Sobre':'/sobre'
        }
    children = []
    for i in links:
        if pathname == links[i]:
            continue
        else:
            children.append(
                html.A(i,href=links[i])
                )
    return children


@app.callback(
    Output('store_main','data'),
    [Input('interval_main','n_intervals')])
def update_main_page_data(n_intervals):
    path_dir = (os.path.dirname(os.path.abspath(__file__))+'/').replace('/','//')+'data//'
    nome_tabela = 'Tabela Informes Região Norte final.xlsx'
    path_tabela = f'{path_dir}{nome_tabela}'

    time_modified = os.path.getsize(path_tabela)
    try:
        with open(f'{path_dir}file_sizes.json','r',encoding='UTF-8') as json_file:
            time_modified_check = json.load(json_file)
    except FileNotFoundError:
        time_modified_check={'Tabela Informes Região Norte final.xlsx':0,'Social Distancing Index by Cities.csv':0}
    
    if time_modified_check[nome_tabela] != time_modified:
        update_df('_new')
        time_modified = os.path.getsize(path_tabela)
        time_modified_check[nome_tabela] = time_modified
        with open(f'{path_dir}file_sizes.json','w',encoding='UTF-8') as json_file:
            json.dump(time_modified_check,json_file)
    else:
        update_df()
    with open(f'{path_dir}Dados Cidades.csv',encoding='UTF-8') as file:
        df = pd.read_csv(file)
        return df.to_json()


@app.callback(
    Output('store_isolamento','data'),
    [Input('interval_main','n_intervals')])
def update_isolation_data(n_intervals):
    path_dir = (os.path.dirname(os.path.abspath(__file__))+'/').replace('/','//')+'data//'
    nome_tabela = 'Social Distancing Index by Cities.csv'
    path_tabela = f'{path_dir}{nome_tabela}'

    time_modified = os.path.getsize(path_tabela)

    try:
        with open(f'{path_dir}file_sizes.json','r',encoding='UTF-8') as json_file:
            time_modified_check = json.load(json_file)
    except FileNotFoundError:
        time_modified_check = {'Tabela Informes Região Norte final.xlsx':0,'Social Distancing Index by Cities.csv':0}
    
    if time_modified_check[nome_tabela] != time_modified:
        update_df_isolamento('_new')
        time_modified_check[nome_tabela] = time_modified
        with open(f'{path_dir}file_sizes.json','w',encoding='UTF-8') as json_file:
            json.dump(time_modified_check,json_file)
    else:
        update_df_isolamento()
    with open(f'{path_dir}Dados Isolamento.csv',encoding='UTF-8') as file:
        df = pd.read_csv(file)
        return df.to_json()


@app.callback(
    Output('titulo','children'),
    [Input('dropdown_cities','value')
    ,Input('store_main','data')])
def update_last_updated_date(value,data):
    df = pd.read_json(data)
    selected_city = value
    if selected_city == 'Região' or selected_city == None:
        df_filtered = df
    else:
        df_filtered = df[df['Cidade'] == selected_city]
    max_date = df_filtered["Data"].map(lambda x: pd.Timestamp(x)).max().strftime('%d/%m/%Y')
    return [html.H1(['Painel COVID-19'], style = {'margin':'0px 20px','align-self':'center'}),
            html.H3([f'Relatório de: {max_date}'], style = {'margin':'0px 10px','align-self':'center'})]


@app.callback(
    Output('n_conf','children'),
    [Input('dropdown_cities','value')
    ,Input('store_main','data')])
def update_n_confirmados(value,data):
    if value != 'Região':
        df = dados_cidade(value)
        if not df.empty:
            u = len(df[df["RESULTADO DO TESTE"]=="Positivo"])
            return [str(u)]

    df = pd.read_json(data)
    df['Data'] = df['Data']
    selected_city = value
    if selected_city == None:
        return ['-']
    elif selected_city == 'Região':
        df_filtered = df
    else:
        df_filtered = df[df['Cidade'] == selected_city]
    u = int(df_filtered.groupby("Cidade")["Casos Confirmados"].max().sum())
    if u == 0:
        return ['-']
    else:
        return [str(u)]


@app.callback(
    Output('n_obitos','children'),
    [Input('dropdown_cities','value')
    ,Input('store_main','data')])
def update_n_obitos(value,data):
    if value != 'Região':
        df = dados_cidade(value)
        if not df.empty:
            u = len(df[df["EVOLUCAO DO CASO"]=="ÓBITO"])
            return [str(u)]

    df = pd.read_json(data)
    selected_city = value
    if selected_city == None:
        return ['-']
    elif selected_city == 'Região':
        df_filtered = df
    else:
        df_filtered = df[df['Cidade'] == selected_city]
    u = int(df_filtered.groupby("Cidade")["Óbitos Confirmados"].max().sum())
    if u == 0:
        return ['-']
    else:
        return [str(u)]

@app.callback(
    Output('n_recup','children'),
    [Input('dropdown_cities','value')
    ,Input('store_main','data')])
def update_n_recuperados(value,data):
    if value != 'Região':
        df = dados_cidade(value)
        if not df.empty:
            u = len(df[df["EVOLUCAO DO CASO"]=="CURA"])
            return [str(u)]

    df = pd.read_json(data)
    selected_city = value
    if selected_city == None:
        return ['-']
    elif selected_city == 'Região':
        df_filtered = df
    else:
        df_filtered = df[df['Cidade'] == selected_city]
    u = int(df_filtered.groupby("Cidade")["Casos Recuperados"].max().sum())
    if u == 0:
        return ['-']
    else:
        return [str(u)]


@app.callback(
    Output('t_incidencia','children'),
    [Input('dropdown_cities','value')
    ,Input('store_main','data')])
def update_t_incidencia(selected_city,data):
    if selected_city == 'Região' or selected_city == None:
        return ['-']

    df = pd.read_json(data)
    df_filtered = df[df['Cidade'] == selected_city]
    pop = df_filtered["pop"].iloc[0]

    df_city = dados_cidade(selected_city)
    if not df_city.empty:
        casos = len(df_city[df_city["RESULTADO DO TESTE"]=="Positivo"])
    else:
        casos = df_filtered.groupby("Cidade")["Casos Confirmados"].max().sum()

    return [f'{casos/pop*1e5:.1f}']


@app.callback(
    Output('t_letalidade','children'),
    [Input('dropdown_cities','value')
    ,Input('store_main','data')])
def update_t_letalidade(selected_city,data):
    if selected_city == 'Região' or selected_city == None:
        return ['-']

    df = dados_cidade(selected_city)
    if not df.empty:
        obitos = len(df[df["EVOLUCAO DO CASO"]=="ÓBITO"])
        casos = len(df[df["RESULTADO DO TESTE"]=="Positivo"])
    else:
        df = pd.read_json(data)
        df_filtered = df[df['Cidade'] == selected_city]
        obitos = df_filtered.groupby("Cidade")["Óbitos Confirmados"].max().sum()
        casos = df_filtered.groupby("Cidade")["Casos Confirmados"].max().sum()

    return [f'{obitos/casos*100:.2f}%']


@app.callback(
    Output('t_mortalidade','children'),
    [Input('dropdown_cities','value')
    ,Input('store_main','data')])
def update_t_mortalidade(selected_city,data):
    if selected_city == 'Região' or selected_city == None:
        return ['-']

    df = pd.read_json(data)
    df_filtered = df[df['Cidade'] == selected_city]
    pop = df_filtered["pop"].iloc[0]

    df_city = dados_cidade(selected_city)
    if not df_city.empty:
        obitos = len(df_city[df_city["EVOLUCAO DO CASO"]=="ÓBITO"])
    else:
        obitos = df_filtered.groupby("Cidade")["Óbitos Confirmados"].max().sum()
    return [f'{(obitos/pop*1e5):.1f}']

@app.callback(
    [Output('div_mortalidade','style')
    ,Output('div_letalidade','style')
    ,Output('div_incidencia','style')],
    [Input('dropdown_cities','value')])
def hide_values(value):
    if value == 'Região' or value == None:
        return [{'display':'none'} for i in [1,2,3]]
    else:
        return [{'display':'inline'} for i in [1,2,3]]


@app.callback(
    Output('dropdown_cities','options'),
    [Input('store_main','data')])
def update_dropdown_options(data):
    df = pd.read_json(data)
    options = [{'label':i,'value':i} for i in df.Cidade.unique()]
    options = [{'label':'Região','value':'Região'}]+options
    return options

def dados_indisponiveis():
        fig = go.Figure()
        fig.update_layout(title="Dados indisponíveis")
        return fig


@app.callback(
    Output('conteudo_graficos_1','figure'),
    [Input('dropdown_cities','value')
    ,Input('store_main','data')
    ,Input('tabs_1','value')])
def update_time_series(selected_city,data,tab_selected):
    if tab_selected == 'tab_gerais':
        df = pd.read_json(data)
        if selected_city != 'Região':
            df = df[df['Cidade'] == selected_city]
        return series_general(df)
    
    if tab_selected == 'tab_comparacao':
        df = pd.read_json(data)
        return series_comparacao(df)

    df = dados_cidade(selected_city)
    if df.empty:
        return dados_indisponiveis()

    if tab_selected == 'tab_bairros':
        return series_bairros(df)

    if tab_selected == 'tab_faixa_etaria':
        return series_faixa_etaria(df)

@app.callback(
    Output('conteudo_graficos_2','figure'),
    [Input('dropdown_cities','value')
    ,Input('store_main','data')
    ,Input('store_isolamento','data')
    ,Input('tabs_2','value')])
def update_time_series(selected_city,data,data_isolamento,tab_selected):
    if tab_selected == 'tab_isolamento':
        df = pd.read_json(data_isolamento)
        if selected_city != 'Região':
            df = df[df['city_name'] == selected_city]
        return series_isolamento(df)
    
    df = dados_cidade(selected_city)
    if df.empty:
        return dados_indisponiveis()
    
    if tab_selected == 'tab_acumulados':
        return series_acumulados(df)

    if tab_selected == 'tab_sexo':
        return series_sexo(df)

    if tab_selected == 'tab_sintomas':
        return series_sintomas(df)

@app.callback(
    Output('mapa_casos','figure'),
    [Input('store_main','data'),
    Input('dropdown_cities','value')])
def update_map(data, selected_city):
    df = dados_cidade(selected_city)

    if not df.empty:
        df['Casos'] = df.groupby('BAIRRO')['BAIRRO'].transform('count')
        df = lat_lon_bairros(selected_city, df)
        map = bubble_map_bairros(df)
    else:
        df = pd.read_json(data)
        map = bubble_map(df)

    return map


@app.callback(
    Output('series_casob','figure'),
    [Input('store_main','data')])
def update_series_casos_obitos(data):
    df = pd.read_json(data)
    df['Data'] = df['Data'].map(lambda x: pd.Timestamp(x))
    series_casos_obitos = series_comparacao(df)
    return series_casos_obitos

@app.callback(
    Output('series_comparacao','figure'),
    [Input('store_main','data')])
def update_comparison(data):
    df = pd.read_json(data)
    return series_comparacao(df)

############################# END Main Page Callbacks #############################

############################ START Sobre Page Callbacks ###########################
    
@app.callback(
    Output('textos','children'),
    [Input('interval2','n_intervals')]
    )
def update_about_content (n_intervals):
    path_dir = (os.path.dirname(os.path.abspath(__file__))+'/').replace('/','//')+'assets//Textos//'
    topics = ['Sobre','Dados', 'Equipe Responsável Pelo Projeto','Discentes Atuantes no Projeto', 'Contato']
    children = []
    for i in topics:
        Chil = [html.H2(i, 
                        style = {
                            'margin':'2%',
                            'color':'#27354d',
                            'font-family':'verdana',
                            'text-align':'center', 
                            'display':'flex'}
                        )]
        
        with open(f'{path_dir}{i}.txt', encoding='UTF-8') as file:
            for linha in file.readlines():
                Chil.append(html.P(linha, 
                                   style = {
                                       'font-family':'Century Gothic',
                                       'color':'#99999',
                                       'text-indent':'4%',
                                       'text-align':'justify'                                       
                                       }
                                   ))
                
        paragraph = html.Div(
            children = Chil,
            className = 'com_borda text_box',
            )
        children.append(paragraph)
    return children



############################# END Sobre Page Callbacks ############################
