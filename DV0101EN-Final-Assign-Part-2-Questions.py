#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Lista de años
year_list = [i for i in range(1980, 2024, 1)]

# Diseño de la aplicación
app.layout = html.Div([
    # Título
    html.H1("Automobile Sales Statistics Dashboard", 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    
    # Menú desplegable para tipo de informe
    html.Div([
        dcc.Dropdown(id='dropdown-statistics',
                     options=[
                         {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                         {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                     ],
                     placeholder='Select a report type',
                     value='Select Statistics',
                     style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign-last': 'center'})
    ]),
    
    # Menú desplegable para el año
    html.Div([
        dcc.Dropdown(id='select-year',
                     options=[{'label': i, 'value': i} for i in year_list],
                     placeholder='Select a year',
                     value='Select-year',
                     style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign-last': 'center'})
    ]),

    # Div para mostrar gráficos
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
])

# Devolución de llamada para habilitar/deshabilitar el menú de selección de año
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(report_type):
    if report_type == 'Yearly Statistics':
        return False
    else:
        return True

# Devolución de llamada para actualizar los gráficos en función de la selección del informe y año
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(report_type, selected_year):
    if report_type == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Gráfico 1: Ventas de automóviles durante períodos de recesión (gráfico de líneas)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Automobile Sales During Recession Period"))

        # Gráfico 2: Promedio de ventas por tipo de vehículo (gráfico de barras)
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Sales by Vehicle Type"))

        # Gráfico 3: Gráfico circular del gasto en publicidad por tipo de vehículo
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                          title="Advertising Expenditure Share by Vehicle Type"))

        # Gráfico 4: Gráfico de barras sobre el efecto de la tasa de desempleo en las ventas de automóviles
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
        ]

    elif report_type == 'Yearly Statistics':
        yearly_data = data[data['Year'] == selected_year]

        # Gráfico 1: Ventas de automóviles en el año seleccionado
        yearly_sales = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yearly_sales, x='Year', y='Automobile_Sales', title=f"Automobile Sales in {selected_year}"))

        # Gráfico 2: Promedio de ventas por tipo de vehículo en el año seleccionado
        avg_sales_year = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.bar(avg_sales_year, x='Vehicle_Type', y='Automobile_Sales', title=f"Average Sales by Vehicle Type in {selected_year}"))

        # Gráfico 3: Gasto en publicidad por tipo de vehículo
        exp_year = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.pie(exp_year, values='Advertising_Expenditure', names='Vehicle_Type',
                          title=f"Advertising Expenditure Share by Vehicle Type in {selected_year}"))

        # Gráfico 4: Efecto de la tasa de desempleo en las ventas de automóviles
        unemp_year_data = yearly_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.bar(unemp_year_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title=f"Effect of Unemployment Rate on Vehicle Type and Sales in {selected_year}"))

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
        ]

if __name__ == '__main__':
    app.run_server(debug=True) 
