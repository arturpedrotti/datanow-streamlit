import os
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from flask import Flask

# Initialize Flask server and set static folder
server = Flask(__name__, static_folder='../static')

# Initialize Dash app
app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    ],
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
    ],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
)

# Read index.html from templates folder
with open('templates/index.html', 'r', encoding='utf-8') as f:
    app.index_string = f.read()

# Load data
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

# Limit data to Anos de Estudo <= 16
data = data[data['Anos de Estudo'] <= 16]

# Define the app layout
app.layout = html.Div([
    # Dropdown for state selection
    html.Div([
        html.Label("Selecione o Estado (UF):", style={'fontSize': '18px', 'color': '#ffffff'}),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': nome, 'value': uf} for uf, nome in uf_map.items()],
            placeholder="Selecione um Estado",
            style={
                'backgroundColor': '#ffffff', 'color': '#000000',
                'border': '1px solid #004d99', 'borderRadius': '5px',
                'width': '60%', 'margin': 'auto', 'padding': '5px'
            },
            clearable=True
        ),
    ], style={'textAlign': 'center', 'marginTop': '20px'}),
    html.Br(),

    # Container for the graphs (initially empty)
    html.Div(id='graphs-container'),
])

# Callback to update the graphs
@app.callback(
    Output('graphs-container', 'children'),
    [Input('state-dropdown', 'value')]
)
def update_graphs(selected_state):
    if not selected_state:
        # Do not display graphs if no state is selected
        return []
    else:
        # Filter data based on the selected state
        filtered_data = data[data['UF'] == selected_state]

        # Check if the DataFrame is not empty
        if filtered_data.empty:
            return [html.Div("Nenhum dado disponível para o estado selecionado.", style={'color': 'white', 'textAlign': 'center'})]

        # Graph 1: Renda Média vs Anos de Estudo
        education_data = filtered_data.groupby('Anos de Estudo')['Renda'].mean().reset_index()
        fig1 = px.line(
            education_data, x='Anos de Estudo', y='Renda',
            title='Renda Média vs Anos de Estudo',
            markers=True, template='plotly_dark'
        )

        # Adjust x-axis to show all years
        fig1.update_xaxes(dtick=1)

        # Graph 2: Renda Média por Faixa Etária
        bins = [0, 18, 25, 35, 45, 60, 100]
        labels = ['0-18', '19-25', '26-35', '36-45', '46-60', '60+']
        filtered_data = filtered_data.copy()  # Avoid SettingWithCopyWarning
        filtered_data['Faixa Etária'] = pd.cut(filtered_data['Idade'], bins=bins, labels=labels, include_lowest=True)
        age_data = filtered_data.groupby('Faixa Etária')['Renda'].mean().reset_index()
        fig2 = px.bar(
            age_data, x='Faixa Etária', y='Renda',
            title='Renda Média por Faixa Etária', template='plotly_dark'
        )

        # Graph 3: Renda Média por Gênero
        gender_data = filtered_data.groupby('Sexo')['Renda'].mean().reset_index()
        fig3 = px.bar(
            gender_data, x='Sexo', y='Renda', color='Sexo',
            title='Renda Média por Gênero', template='plotly_dark'
        )

        # Adjust figure styles
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False)

        # Return the graphs
        return [
            html.Div([
                html.H2("Relação: Anos de Estudo e Renda Média", style={'textAlign': 'center'}),
                dcc.Graph(figure=fig1)
            ]),
            html.Hr(),
            html.Div([
                html.H2("Distribuição de Renda Média por Faixa Etária", style={'textAlign': 'center'}),
                dcc.Graph(figure=fig2)
            ]),
            html.Hr(),
            html.Div([
                html.H2("Renda Média por Gênero", style={'textAlign': 'center'}),
                dcc.Graph(figure=fig3)
            ]),
            html.Hr(),
        ]

# Run the app
if __name__ == '__main__':
    app.run(host="192.168.0.99", port=8050, debug=True)
