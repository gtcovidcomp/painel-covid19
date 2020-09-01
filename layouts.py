import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
from data.data import update_df


path_dir = (os.path.dirname(os.path.abspath(__file__))+'/').replace('/','//')+'data//'

try:
    df = pd.read_csv(f'{path_dir}Dados Cidades.csv', encoding='UTF-8')
    
except FileNotFoundError:
    update_df()
    df = pd.read_csv(f'{path_dir}Dados Cidades.csv', encoding='UTF-8')

local = dcc.Location(id='url', refresh=False)


################################ START Header Itens ####################################

none = html.Div(className='none')

navbar = html.Div(
    children = [
        local,
        html.Nav(
            id = 'navbar',
            className = 'links',
            style = {'align-self':'center', 'width':'100%'}
            )
    ],
    style = {'display':'flex'}
    )

logos = html.Div(
    className = 'logos',
    children = [
        html.Img(src = '/assets/Imagens/ufrj.png', className = 'ufrj'),
        html.Img(src = '/assets/Imagens/macae.png', className = 'macae'),
        html.Img(src = '/assets/Imagens/uff.png', className = 'uff'),
        html.Img(src = '/assets/Imagens/ict.png', className = 'ict'),
        html.Img(src = '/assets/Imagens/gt.png', className = 'gt')
        ]
    )


titulo = html.Span(['Painel COVID-19'], id = 'titulo', 
                                   className = 'titulo', 
                                   style ={
                                       'text-align':'center', 
                                       'display':'flex'
                                       })


header = html.Div(
    className = 'header com_borda',
    children = [
        local,
        logos, 
        titulo,
        navbar
        ]
    )



header2 = html.Div(
    className = 'header com_borda',
    children = [
        local,
        logos, 
        html.H1(['Painel COVID-19'], className = 'titulo', style ={'text-align':'center', 'display':'flex'}),
        navbar
        ]
    )
################################# END Header Itens #####################################


        
############################## START Main Page Layout ##################################
mainPage = html.Div(
    className = 'main_page',
    children = [
        header, 
        html.Div(
            className = 'value value1 com_borda',
            children = [
                html.P(children=['Confirmados:'], className= 'value_title'),
                html.H1(
                    id = 'n_conf',
                    style={'text-align':'center'}
                )
            ]
        ),
        html.Div(
            className = 'value value2 com_borda',
            children = [
                html.P(children=['Óbitos:'], className= 'value_title'),
                html.H1(
                    id = 'n_obitos',
                    style={'text-align':'center'}
                    )
            ]
        ),
        html.Div(
            className = 'value value3 com_borda',
            children = [
                html.P(children=['Recuperados:'], className= 'value_title'),
                html.H1(
                    id = 'n_recup',
                    style={'text-align':'center'}
                )
            ]
        ),
        html.Div(
            className = 'value value4 com_borda tooltip',
            id = 'div_incidencia',
            children = [
                html.P(children=['Taxa de Incidência:'], className= 'value_title'),
                html.P(['por 100 mil habitantes'], className='value_sub'),
                html.H1(
                    id = 't_incidencia',
                    style={'text-align':'center'}
                ),
                html.Span(['Taxa de Incidência: Número de casos em relação ao tamanho da população.'], 
                          className = 'tooltiptext'
                          )
            ]
        ),
        html.Div(
            className = 'value value5 com_borda tooltip',
            id = 'div_letalidade',
            children = [
                html.P(children=['Taxa de Letalidade:'], className= 'value_title'),
                html.H1(
                    id = 't_letalidade',
                    style={'text-align':'center'}
                    ),
                html.Span(['Taxa de Letalidade: Porcentagem de Óbitos em relação ao número de casos.'], 
                          className = 'tooltiptext'
                          )
            ]
        ),
        html.Div(
            className = 'value value6 com_borda tooltip',
            id = 'div_mortalidade',
            children = [
                html.P(children=['Taxa de Mortalidade:'], className= 'value_title'),
                html.P(['por 100 mil habitantes'], className='value_sub'),
                html.H1(
                    id = 't_mortalidade',
                    style={'text-align':'center'}
                ),
                html.Span(['Taxa de Mortalidade: Número de Óbitos em relação ao tamanho da população.'], 
                          className = 'tooltiptext'
                          )
            ]
        ),
        html.Div(
            className = 'series1 com_borda',
            id = 'grupo_graficos_1',
            children = [
                dcc.Tabs(id = 'tabs_1', value = 'tab_gerais', style = dict(height = '3vh'), children = [
                    dcc.Tab(label = 'Dados Gerais', value = 'tab_gerais',
                        style = dict(padding = '0px'), selected_style = dict(padding = '0px')),
                    dcc.Tab(label = 'Comparação de cidades', value = 'tab_comparacao',
                        style = dict(padding = '0px', ), selected_style = dict(padding = '0px')),
                    dcc.Tab(label = 'Bairros', value = 'tab_bairros',
                        style = dict(padding = '0px', ), selected_style = dict(padding = '0px')),
                    dcc.Tab(label = 'Faixa etária', value = 'tab_faixa_etaria',
                        style = dict(padding = '0px', ), selected_style = dict(padding = '0px'))
                ]),
                dcc.Graph(id = 'conteudo_graficos_1', className='conteudo_graficos', config = {'locale':'pt-BR'})
            ]
        ),
        html.Div(
            className = 'series2 com_borda',
            id = 'grupo_graficos_2',
            children = [
                dcc.Tabs(id = 'tabs_2', value = 'tab_isolamento', style = dict(height = '3vh'), children = [
                    dcc.Tab(label = 'Taxa de isolamento', value = 'tab_isolamento',
                        style = dict(padding = '0px', ), selected_style = dict(padding = '0px')),
                    dcc.Tab(label = 'Acumulados por semana', value = 'tab_acumulados',
                        style = dict(padding = '0px', ), selected_style = dict(padding = '0px')),
                    dcc.Tab(label = 'Sexo', value = 'tab_sexo',
                        style = dict(padding = '0px', ), selected_style = dict(padding = '0px')),
                    dcc.Tab(label = 'Sintomas', value = 'tab_sintomas',
                        style = dict(padding = '0px', ), selected_style = dict(padding = '0px'))
                ]),
                dcc.Graph(id = 'conteudo_graficos_2', className='conteudo_graficos', config = {'locale':'pt-BR'})
            ]
        ),
        html.Div(
            className = 'drop com_borda',
            children =[
                html.H3(['Filtro:'], style= {'margin':'auto'}),
                dcc.Dropdown(
                    id = 'dropdown_cities',
                    placeholder = 'Selecione uma opção',
                    value = 'Região',
                    style = {'font-weight':'900', 'font-size':'1.2em','border-radius':'0px'}
                )
            ],
            style = {'display':'grid', 'grid-template-columns':'2fr 8fr'}
        ),
        dcc.Graph(
            className = 'map com_borda',
            id = 'mapa_casos',
            config = {'locale':'pt-BR'}
        ),
        dcc.Interval(
            id = 'interval_main',
            interval = 10*60*1000,
            n_intervals = 0
        ),
        dcc.Store(
            id = 'store_main',
            storage_type='local'
        ),
        dcc.Store(
            id = 'store_isolamento',
            storage_type='local'
        )
    ]
)
############################### END Main Page Layout ###################################


################################ START No Page Layout ##################################
sobrePage = html.Div(className= 'sobre_page',
                     children = [
                         header2,
                         dcc.Interval(
                             id = 'interval2',
                             interval = 5*60*60*1000,
                             n_intervals = 0
                             ),
                         html.Div(className='sobre_texts', id='textos')
                         ]
                     )

################################# END No Page Layout ###################################


################################ START No Page Layout ##################################
noPage = html.Div([header2,html.H1(["Page not found"])])
################################# END No Page Layout ###################################
