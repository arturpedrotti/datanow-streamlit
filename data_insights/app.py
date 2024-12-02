from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

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

# Function to remove outliers using IQR
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Clean data
data = remove_outliers(data, 'Renda')

# Initialize Dash app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    ],
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
    ],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
)

# Set the server for deployment
server = app.server

# Custom index string to use the modified index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    app.index_string = f.read()

# Define layout
app.layout = html.Div([
    # Dropdown for state selection
    html.Label("Selecione o Estado (UF):", style={'fontSize': '18px', 'color': '#ffffff'}),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': nome, 'value': uf} for uf, nome in uf_map.items()],
        placeholder="Todos os Estados",
        style={
            'backgroundColor': '#ffffff', 'color': '#000000',
            'border': '1px solid #004d99', 'borderRadius': '5px',
            'width': '60%', 'margin': 'auto', 'padding': '5px'
        },
        clearable=True
    ),
    html.Br(),

    # Graph 1: Income vs Education
    html.Div(id='graph1-container', children=[
        html.H2("Relação: Anos de Estudo e Renda Média", style={'textAlign': 'center'}),
        dcc.Graph(id='income-education-graph')
    ]),
    html.Hr(),

    # Graph 2: Income by Age Group
    html.Div(id='graph2-container', children=[
        html.H2("Distribuição de Renda Média por Faixa Etária", style={'textAlign': 'center'}),
        dcc.Graph(id='age-income-graph')
    ]),
    html.Hr(),

    # Graph 3: Income by Gender
    html.Div(id='graph3-container', children=[
        html.H2("Renda Média por Gênero", style={'textAlign': 'center'}),
        dcc.Graph(id='income-gender-graph')
    ]),
    html.Hr(),
])

# Callbacks for updating graphs
@app.callback(
    [Output('income-education-graph', 'figure'),
     Output('age-income-graph', 'figure'),
     Output('income-gender-graph', 'figure')],
    [Input('state-dropdown', 'value')]
)
def update_graphs(selected_state):
    filtered_data = data if not selected_state else data[data['UF'] == selected_state]

    # Graph 1: Income vs Education
    education_data = filtered_data.groupby('Anos de Estudo')['Renda'].mean().reset_index()
    fig1 = px.line(
        education_data, x='Anos de Estudo', y='Renda',
        title='Renda Média vs Anos de Estudo',
        markers=True, template='plotly_dark'
    )

    # Graph 2: Income by Age Group
    age_data = filtered_data.groupby('Idade')['Renda'].mean().reset_index()
    fig2 = px.bar(
        age_data, x='Idade', y='Renda',
        title='Renda Média por Idade', template='plotly_dark'
    )

    # Graph 3: Income by Gender
    gender_data = filtered_data.groupby('Sexo')['Renda'].mean().reset_index()
    fig3 = px.pie(
        gender_data, names='Sexo', values='Renda',
        title='Distribuição de Renda por Gênero', hole=0.4
    )

    # Adjust figure styles
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')

    return fig1, fig2, fig3

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
