import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load the data
file_path = "dados.csv"
data = pd.read_csv(file_path)

# Map UF codes to state names
uf_map = {
    11: "Rondônia", 12: "Acre", 13: "Amazonas", 14: "Roraima", 15: "Pará",
    16: "Amapá", 17: "Tocantins", 21: "Maranhão", 22: "Piauí", 23: "Ceará",
    24: "Rio Grande do Norte", 25: "Paraíba", 26: "Pernambuco", 27: "Alagoas",
    28: "Sergipe", 29: "Bahia", 31: "Minas Gerais", 32: "Espírito Santo",
    33: "Rio de Janeiro", 35: "São Paulo", 41: "Paraná", 42: "Santa Catarina",
    43: "Rio Grande do Sul", 50: "Mato Grosso do Sul", 51: "Mato Grosso",
    52: "Goiás", 53: "Distrito Federal"
}
data['UF_Nome'] = data['UF'].map(uf_map)
data['Sexo'] = data['Sexo'].map({0: "Masculino", 1: "Feminino"})

# Initialize the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'},
    children=[
        html.H1("Painel de Alocação de Recursos Públicos", style={'textAlign': 'center', 'color': '#004d99'}),
        html.Hr(),

        # Dropdown for state selection
        html.Label("Selecione o Estado (UF):", style={'color': '#004d99'}),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': nome, 'value': uf} for uf, nome in uf_map.items()],
            placeholder="Todos os Estados",
            style={
                'backgroundColor': '#f2f2f2', 'border': '1px solid #004d99',
                'borderRadius': '5px', 'width': '50%', 'margin': 'auto'
            },
            clearable=True
        ),
        html.Br(),

        # Graph 1: Income vs Education
        html.Div(id='graph1-container', children=[
            html.H2("Relação: Anos de Estudo e Renda Média", style={'color': '#004d99'}),
            dcc.Graph(id='income-education-graph')
        ]),
        html.Div(id='insight1', children=[
            html.P(
                "INSIGHT: Investir em educação impacta diretamente na renda média. "
                "Priorizar programas educacionais em estados de baixa escolaridade é recomendável."
            )
        ], style={'padding': '10px', 'backgroundColor': '#e6f7ff', 'borderRadius': '5px'}),
        html.Hr(),

        # Graph 2: Income by Age Group
        html.Div(id='graph2-container', children=[
            html.H2("Distribuição de Renda Média por Faixa Etária", style={'color': '#004d99'}),
            dcc.Graph(id='age-income-graph')
        ]),
        html.Div(id='insight2', children=[
            html.P(
                "INSIGHT: Jovens entre 20-30 anos possuem menores rendas, indicando a necessidade de "
                "programas voltados para inserção no mercado de trabalho e formação técnica."
            )
        ], style={'padding': '10px', 'backgroundColor': '#e6f7ff', 'borderRadius': '5px'}),
        html.Hr(),

        # Graph 3: Income by Gender
        html.Div(id='graph3-container', children=[
            html.H2("Renda Média por Gênero", style={'color': '#004d99'}),
            dcc.Graph(id='income-gender-graph')
        ]),
        html.Div(id='insight3', children=[
            html.P(
                "INSIGHT: Mulheres ainda recebem 30% menos que os homens. "
                "Reduzir essa desigualdade é uma prioridade."
            )
        ], style={'padding': '10px', 'backgroundColor': '#e6f7ff', 'borderRadius': '5px'}),
        html.Hr(),
    ]
)

# Callbacks to update graphs based on selected state
@app.callback(
    [Output('income-education-graph', 'figure'),
     Output('age-income-graph', 'figure'),
     Output('income-gender-graph', 'figure')],
    [Input('state-dropdown', 'value')]
)
def update_graphs(selected_state):
    # Filter data
    filtered_data = data if not selected_state else data[data['UF'] == selected_state]

    # Graph 1: Income vs Education
    education_data = filtered_data.groupby('Anos de Estudo')['Renda'].mean().reset_index()
    fig1 = px.line(
        education_data, x='Anos de Estudo', y='Renda',
        title='Renda Média vs Anos de Estudo',
        markers=True, template='plotly_white',
        color_discrete_sequence=['#004d99']
    )

    # Graph 2: Income by Age Group
    age_data = filtered_data.groupby('Idade')['Renda'].mean().reset_index()
    fig2 = px.bar(
        age_data, x='Idade', y='Renda',
        title='Renda Média por Idade', template='plotly_white',
        color_discrete_sequence=['#ff6600']
    )

    # Graph 3: Income by Gender
    gender_data = filtered_data.groupby('Sexo')['Renda'].mean().reset_index()
    fig3 = px.pie(
        gender_data, names='Sexo', values='Renda',
        title='Distribuição de Renda por Gênero', hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    return fig1, fig2, fig3


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

