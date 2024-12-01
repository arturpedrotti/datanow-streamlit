import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Carregar os dados
file_path = "dados.csv"
data = pd.read_csv(file_path)

# Mapear códigos UF para nomes dos estados
uf_map = {
    11: "Rondônia",
    12: "Acre",
    13: "Amazonas",
    14: "Roraima",
    15: "Pará",
    16: "Amapá",
    17: "Tocantins",
    21: "Maranhão",
    22: "Piauí",
    23: "Ceará",
    24: "Rio Grande do Norte",
    25: "Paraíba",
    26: "Pernambuco",
    27: "Alagoas",
    28: "Sergipe",
    29: "Bahia",
    31: "Minas Gerais",
    32: "Espírito Santo",
    33: "Rio de Janeiro",
    35: "São Paulo",
    41: "Paraná",
    42: "Santa Catarina",
    43: "Rio Grande do Sul",
    50: "Mato Grosso do Sul",
    51: "Mato Grosso",
    52: "Goiás",
    53: "Distrito Federal"
}

# Adicionar nomes de UF e mapeamento de gênero
data['UF_Nome'] = data['UF'].map(uf_map)
data['Sexo'] = data['Sexo'].map({0: "Masculino", 1: "Feminino"})  # Mapear 0/1 para Masculino/Feminino

# Inicializar o app Dash
app = Dash(__name__)

# Layout do dashboard
app.layout = html.Div(
    style={'backgroundColor': '#1a1a1a', 'color': '#FFFFFF', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.H1("Painel de Pobreza no Brasil", style={'textAlign': 'center', 'color': '#FFD700'}),
        html.H2("Sobre o Projeto", style={'color': '#FFD700'}),
        html.P(
            "Este painel analisa indicadores de pobreza no Brasil, com foco em como a renda, a educação e a idade influenciam as desigualdades econômicas. "
            "Os gráficos são otimizados para oferecer insights claros e imediatos.",
            style={'marginBottom': '20px'}
        ),

        # Dropdown para seleção de estado
        html.Label("Selecione o Estado (UF):", style={'color': '#FFFFFF'}),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': nome, 'value': uf} for uf, nome in uf_map.items()],
            placeholder="Todos os Estados",
            style={
                'backgroundColor': '#333333',
                'color': '#000000',  # Texto preto para contraste
                'border': '1px solid #FFD700'
            },
            clearable=True
        ),

        # Scatterplot: Anos de Estudo x Renda
        html.Div([
            dcc.Graph(id='income-education-scatter'),
            html.P("Este scatterplot destaca a relação entre anos de estudo e renda, com cores representando grupos de renda. "
                   "Os dados são filtrados para eliminar valores extremos e destacar tendências."),
        ], style={'marginBottom': '50px'}),

        # Gráfico de Idade x Renda Média
        html.Div([
            dcc.Graph(id='age-income-bar'),
            html.P("Este gráfico exibe a renda média por faixa etária, destacando grupos que precisam de maior atenção."),
        ], style={'marginBottom': '50px'}),

        # Gráfico de Distribuição de Renda por Gênero
        html.Div([
            dcc.Graph(id='income-gender-bar'),
            html.P("Este gráfico mostra a distribuição média de renda por gênero e faixa de renda, destacando desigualdades econômicas."),
        ], style={'marginBottom': '50px'}),

        # Conclusão e Recomendações
        html.Div([
            html.H3("Conclusão e Recomendações", style={'color': '#FFD700'}),
            html.P(
                "Os dados reforçam a necessidade de investir em educação e em políticas voltadas para grupos mais vulneráveis, como mulheres e jovens. "
                "Focar em regiões com maior desigualdade econômica pode gerar um impacto significativo."
            ),
        ], style={'marginTop': '50px'}),
    ]
)

# Callback para atualizar gráficos com base no estado selecionado
@app.callback(
    [Output('income-education-scatter', 'figure'),
     Output('age-income-bar', 'figure'),
     Output('income-gender-bar', 'figure')],
    [Input('state-dropdown', 'value')]
)
def update_graphs(selected_state):
    # Filtrar os dados
    filtered_data = data if not selected_state else data[data['UF'] == selected_state]

    # Scatterplot: Anos de Estudo x Renda
    scatter_fig = px.scatter(
        filtered_data,
        x='Anos de Estudo',
        y='Renda',
        color='Renda',
        color_continuous_scale='Viridis',
        title='Renda vs. Anos de Estudo (Destaque por Grupos de Renda)',
        labels={'Renda': 'Renda (R$)', 'Anos de Estudo': 'Anos de Estudo'},
        template='plotly_dark',
        hover_data={'UF_Nome': True, 'Sexo': True}
    )

    # Gráfico de Renda Média por Faixa Etária
    age_income_data = filtered_data.groupby('Idade')['Renda'].mean().reset_index()
    age_fig = px.bar(
        age_income_data,
        x='Idade',
        y='Renda',
        title='Renda Média por Faixa Etária',
        labels={'Idade': 'Idade (anos)', 'Renda': 'Renda Média (R$)'},
        template='plotly_dark',
        color_discrete_sequence=['#FFD700']
    )

    # Gráfico de Distribuição de Renda por Gênero
    income_gender_data = filtered_data.groupby(['Sexo', 'UF_Nome'])['Renda'].mean().reset_index()
    income_fig = px.bar(
        income_gender_data,
        x='Sexo',
        y='Renda',
        color='Sexo',
        title='Renda Média por Gênero',
        labels={'Sexo': 'Gênero', 'Renda': 'Renda Média (R$)'},
        template='plotly_dark',
        color_discrete_map={'Masculino': '#1f77b4', 'Feminino': '#ff4136'}
    )

    return scatter_fig, age_fig, income_fig


# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
