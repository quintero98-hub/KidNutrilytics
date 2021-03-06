import pandas as pd
import plotly.express as px
from itertools import cycle
import requests

def nombres(x):
    if x == 'Desnutricion Aguda Moderada' or x == 'Desnutricion aguda severa':
        x = 'Desnutricion'
    else:
        x
    return x

def ploting_distribution(base_pivot):
    base_pivot['EstadoPesoTalla_New'] = base_pivot['EstadoPesoTalla'].apply(nombres)
    base_pivot['FechaValoracionNutricional'] = pd.to_datetime(base_pivot['FechaValoracionNutricional'])
    base_pivot['FechaValoracionNutricional_MesAño'] = base_pivot['FechaValoracionNutricional'].dt.to_period('M')
    frecuencias_mes = base_pivot[['FechaValoracionNutricional_MesAño','EstadoPesoTalla_New']].groupby(['FechaValoracionNutricional_MesAño','EstadoPesoTalla_New']).size()
    porcentajes_mes = frecuencias_mes.groupby(level=0).apply(lambda x : 100 * x / float(x.sum()))
    porcentajes_mes = porcentajes_mes.reset_index()
    porcentajes_mes.columns = ['FechaValoracionNutricional_MesAño', 'EstadoPesoTalla_New', 'Porcentajes']
    x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    y = porcentajes_mes[porcentajes_mes['EstadoPesoTalla_New'] == 'Desnutricion']['Porcentajes']
    y1 = y[:12]
    y2 = y[12:24]
    y3 = y[24:]
    fig = px.line(porcentajes_mes, x=x, y=[y1,y2,y3], color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
    names = cycle(['Malnutrition 2017', 'Malnutrition 2018', 'Malnutrition 2019'])
    fig.for_each_trace(lambda x : x.update(name = next(names)))
    fig.update_layout(xaxis_title="Month", yaxis_title="Percentage (%)")
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_layout(legend=dict(x=0.1,y=1))
    return fig
