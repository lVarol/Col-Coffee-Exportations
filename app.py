from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
\

app = Dash(
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)


app = dash.Dash(__name__)

server = app.server

#Load data
data = pd.read_csv('Book1.csv', encoding='utf-8', delimiter=';')
data.columns = ['Fecha', 'País de destino', 'Tipo de cafe', 'Sacos de 60 Kg. Exportados']
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
#Process data

data['Pais'] = data['País de destino']
data['Sacos'] = data['Sacos de 60 Kg. Exportados']
data['Tipo'] = data['Tipo de cafe']
data['Fecha'] = pd.to_datetime(data['Fecha'], format='%Y-%m', errors='coerce')
data['Año'] = data['Fecha']
data['Año_unico'] = data['Año'].dt.year


df_groupedline = data.groupby('Año')['Sacos'].sum().reset_index()

paises = list(data['Pais'].sort_values().unique())
paises = [pais for pais in paises if pd.notna(pais)]


df_paises = data.groupby('Pais')['Sacos'].sum().reset_index()
df_top_diez = df_paises.nlargest(10,'Sacos')

df_tipo = data.groupby('Tipo')['Sacos'].count().reset_index()

df_groupedbar = data.groupby('Año_unico')['Sacos'].sum().reset_index()

# Graphs

fig1 = px.bar(df_top_diez, x="Pais", y='Sacos',
              title="Los 10 Países que más importan Café Colombiano\n2017 - 2024",
              opacity=1.0,
              color_discrete_sequence=['#1f77b4'],
              text_auto='.3s')

fig2 = px.pie(df_tipo, values="Sacos", names="Tipo",
              title="Tipos de Café",
              hover_data=['Sacos'],
              labels={'Sacos': 'Exportaciones'})


fig3 = px.line(df_groupedline, x='Año',y='Sacos',
               title="")

fig4 = px.bar(df_groupedbar, x='Año_unico',y='Sacos',text_auto='.3s',
              title="Exportaciones 2017 - 2024")


# Graphs styles

fig1.update_layout(
        title={
        'text': "10 Países que más importan Café Colombiano<br>2017 - 2024",
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(weight='bold',size=16)
    },
    plot_bgcolor='white',  # Fondo blanco
    yaxis_title='Sacos de 60 kg',
    xaxis_title='Países',
    font=dict(size=14),
    yaxis=dict(showgrid=True, gridcolor='lightgray', range=[0, 40e6]),  # Añadir cuadrícula
    bargap=0.4,
    # height=500, 
    # width=1100,
    autosize=True,
      # Enables responsive sizing
    height=400,  # Set a fixed height or adjust as needed 
    margin=dict(l=20, r=0, t=30, b=20)  

)

fig2.update_layout(
    title={
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(weight='bold')
    },
    font=dict(size=14),
    width=400,
    height=400,  # Set a fixed height or adjust as needed
    margin=dict(l=20, r=0, t=30, b=20),
    autosize=True
)

fig2.update_traces(    
    textposition='inside',
    textinfo='percent+label')

fig3.update_layout(
    plot_bgcolor='white',  # Fondo blanco
    yaxis_title='Sacos de 60 kg',
    xaxis_title='Año',
    font=dict(size=14),
    yaxis=dict(showgrid=True, gridcolor='lightgray', range=[100000,1600000]),  # Añadir cuadrícula
    bargap=0.4,
    # height=400, 
    width=1200,
    autosize=True
)

fig4.update_layout(
    title={
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(weight='bold')
    },
    
    plot_bgcolor='white',  # Fondo blanco
    yaxis_title='Sacos de 60 kg',
    xaxis_title='Año',
    font=dict(size=14),
    yaxis=dict(showgrid=True, gridcolor='lightgray', range=[1e6,15e6],
               title_font=dict(weight='bold')),
    
    xaxis=dict(title_font=dict(weight='bold')), 
      # Añadir cuadrícula
    bargap=0.4,
    # height=500, 
    # width=800,

    autosize=True,  # Enables responsive sizing
    height=400,  # Set a fixed height or adjust as needed
    margin=dict(l=20, r=20, t=30, b=20),
)

image_path = "assets/colombia.png"
# APP layout

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(children=[
                html.Img(src=image_path, className="image"),
                html.P(children="☕", className="header-emoji")], className="inner-header"),
                html.H1(
                    children="De Colombia para el mundo.", className="header-title"
                ),
                html.P(
                    children=("Visualiza las exportaciones de café Colombiano "
                       "desde 2017 hasta 2024."),
                className="header-description"
                )
            ],
            className="header"
        ),
        html.Div(
            children=[
                html.Div(
                children=[
            dcc.Graph(id='años-exp', figure=fig4,
                          config={
        'scrollZoom': False,  
        'displayModeBar': False,
        'staticPlot': True  
        }),

            dcc.Graph(id='tipo-cafe', figure=fig2)
                ],
                className="graphs-container-1"
            ),
            html.Div(
                children=[
                    html.P(
                        children=["El propósito de esta página es ilustrar estadísticas de la exportación de café colombiano. La fuente de estos datos es directamente de  ",
                        html.A("La Federación Nacional de Cafeteros de Colombia;", href="https://federaciondecafeteros.org/wp/estadisticas-cafeteras/", target="_blank"),
                        " Exportaciones de Café Colombiano. Destino y Tipo 2017 hasta julio 2024."
                        "Con estas ilustraciones se busca ofrecer una visión más detallada de los patrones de comercio al exterior."
                        ],className="link"
                    ),
                ],className="Text-1"
                
            ),
                        html.Div(
                style={
                    'width': '100%',  # Ancho completo del contenedor
                    'height': '1px',  # Altura de la línea (delgada)
                    'background-color': 'rgba(0, 0, 0, 0.5)',  # Color de la línea
                    'margin': '20px 0 50px',  # Margen arriba y abajo para espacio
                }
            ),

            html.Div(
                children=[
                    dcc.Graph(id='tiempo-exp',figure=fig3,
                                              config={
                    'scrollZoom': False,  
                    'displayModeBar': False,
                    'staticPlot': True  
                    })
                ], className="line-chart"
            ),
            html.Div(
                children=[
                    html.P(children="El café colombiano continúa destacándose en el mercado mundial por su calidad excepcional y su reputación como uno de los mejores cafés del mundo."
                                    "A pesar de la pandemia y muchas condiciones naturales, como el fenómeno del Niño, la exportación de café colombiano se mantiene en constante alza, lo que demuestra el compromiso del país.")
                ], className="Text-2"
            ),
            html.Div(
                children=[
                    dcc.Graph(id='top-paises',figure=fig1,
                config={
                    'scrollZoom': False,  
                    'displayModeBar': False,
                    'staticPlot': True  
                    })
                ],className="top-paises",
            ),
            html.Div(
                children=[
                ],className="menu-style"
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children="País", className="menu-title"),
                            dcc.Dropdown(
                                id="Pais-filter",
                                options=[{"label": pais, "value": pais} for pais in paises],
                                value=paises[0],  # Valor inicial
                                clearable=False,
                                className="dropdown",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children="Fecha", className="menu-title"
                            ),
                            dcc.DatePickerRange(
                                id="date-range",
                                min_date_allowed=data["Fecha"].min().date(),
                                max_date_allowed=data["Fecha"].max().date(),
                                start_date=data["Fecha"].min().date(),
                                end_date=data["Fecha"].max().date(),
                            ),
                        ]
                    ),
                
                ],
                className="menu"
            ),
            html.Div(
                children=[
                    dcc.Graph(id='bar-chart',
                    config={
                    'scrollZoom': False,  
                    'displayModeBar': False,
                    'staticPlot': True  
                    }),  # Set ID for the bar graph
                    dcc.Graph(id='pie-chart'),
                ],className="graphs-container-2"
            )
            ], className="body-page"
        )
    ]
)


    # Callback para actualizar los gráficos
@app.callback(
    [Output("bar-chart", "figure"), Output("pie-chart", "figure")],  # Actualizado a 'pie-chart'
    [Input("Pais-filter", "value"), Input("date-range", "start_date"), Input("date-range", "end_date")]
)
def update_charts(selected_pais, start_date, end_date):
    # Filtrar datos según país y rango de fechas
    filtered_data = data[
        (data['Pais'] == selected_pais) &
        (data['Fecha'] >= pd.to_datetime(start_date)) &
        (data['Fecha'] <= pd.to_datetime(end_date))
    ]

    # Gráfico de barras por año
    df_groupedbar = filtered_data.groupby('Año')['Sacos'].sum().reset_index()
    bar_chart = px.line(df_groupedbar, x='Año', y='Sacos',
                       title=f"Exportaciones hacia {selected_pais} ({start_date} a {end_date})")

    bar_chart.update_layout(

  # Añadir cuadrícula
        bargap=0.4,
        yaxis_title='Sacos de 60 kg'
        )

    # Gráfico de pie para mostrar el tipo de café
    df_groupedpie = filtered_data.groupby('Tipo')['Sacos'].sum().reset_index()
    pie_chart = px.pie(df_groupedpie, values='Sacos', names='Tipo',
                       title=f"Distribución por tipo de café en {selected_pais}")
    
    pie_chart.update_traces(    
    textposition='inside',
    textinfo='percent+label')


    return bar_chart, pie_chart

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050, debug=True)


