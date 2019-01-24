from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import pandas as pd
import random as rd

def leerarchivo(nom):
    arch=open(nom,"r")
    datos = arch.readlines()
    datos.pop(0)
    arch.close()
    listaF=[]
    for i,v in enumerate(datos):
        listaF.append(v.strip().split("|"))
    return listaF


def generarDataFrame():
    return pd.read_csv("filtrado.csv",sep="|")

def crearGraficoBarrasFranja(arch):
    horas = ["00:00 a 06:00", "06:00 a 12:00", "12:00 a 18:00", "18:00 a 00:00"]
    for i,franja in enumerate(["madrugada", "mañana", "tarde", "noche"]):
        r=str(rd.randint(0,255))
        g=str(rd.randint(0,255))
        b=str(rd.randint(0,255))

        datos = sismoFranjaHorariaProvincia(arch, franja)
        df = pd.DataFrame(datos)
        data=[
            go.Bar(
                x=df['Provincias'],
                y=df['CantidadSismos'],
                marker=dict(
                    color='rgba('+r+','+g+','+b+', 0.7)',
                    line=dict(
                        color='rgba('+r+','+g+','+b+', 1.0)',
                        width=2,
                    )
                )
            )
        ]
        layout = go.Layout(
            title="Sismos Franja horaria: "+franja+" ("+horas[i]+")",
            xaxis=dict(
                title='Provincias',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Cantidad de Sismos',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
        fig = go.Figure(data=data, layout=layout)

        plot(fig, filename='sismos'+franja+'.html',auto_open=False)


def sismoFranjaHorariaProvincia(lista, franja):
    dic = {"Provincias":[],"CantidadSismos":[]}
    minLim = 0
    maxLim = 0
    if franja == "mañana":
        minLim = 6
        maxLim = 12
    elif franja == "tarde":
        minLim = 12
        maxLim = 18
    elif franja == "noche":
        minLim = 18
        maxLim = 24
    else:
        minLim = 00
        maxLim = 6

    for sismo in lista:
        if maxLim > int(sismo[1].split(':')[0]) >= minLim:
            if sismo[-1] in dic["Provincias"]:
                dic["CantidadSismos"][dic["Provincias"].index(sismo[-1])] += 1
            else:
                dic["Provincias"].append(sismo[-1])
                dic["CantidadSismos"].append(1)
    return dic

def sismosMaximoProvincia(lista):
    dic = {"Provincias":[],"MagnitudMaxima":[]}
    for sismo in lista:
        if sismo[-1] in dic["Provincias"]:
            dic["MagnitudMaxima"][dic["Provincias"].index(sismo[-1])].append(float(sismo[2]))
        else:
            dic["Provincias"].append(sismo[-1])
            dic["MagnitudMaxima"].append([float(sismo[2])])

    for i,mag in enumerate(dic["MagnitudMaxima"]):
        dic["MagnitudMaxima"][i]=max(mag)
    return dic

def crearGraficoBarrasMagnitud(lista):
    datos=sismosMaximoProvincia(lista)
    colors={'Micro': 'green','Menor': 'lightgreen','Ligero': 'darkgreen','Moderado': 'orange','Fuerte':'red'}
    bins=[0,2,4,5,6,7]
    labels=['Micro','Menor','Ligero','Moderado','Fuerte']
    datos['label']=pd.cut(datos["MagnitudMaxima"],bins=bins,labels=labels)

    df = pd.DataFrame(datos).sort_values("MagnitudMaxima",ascending=True)
    bars=[]
    for label, label_df in df.groupby('label'):
        bars.append(go.Bar(x=label_df["Provincias"],
                           y=label_df["MagnitudMaxima"],
                           name=label,
                           marker={'color': colors[label]}))

    layout = go.Layout(
        title="Magnitud de Sismo Máxima por Provincia",
        xaxis=dict(
            title='Provincias',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Magnitud Máxima',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.FigureWidget(data=bars, layout=layout)

    plot(fig, filename='sismosmaximo.html',auto_open=False)


def sismosRegion(lista):
    costa=["El Oro","Esmeraldas","Guayas","Los Rios","Manabi","Sta Elena"]
    sierra=["Azuay","Bolivar","Canar","Carchi","Chimborazo","Cotopaxi","Imbabura","Loja","Pichincha","Sto Dom Tsachilas","Tungurahua"]
    oriente=["Morona Stgo","Napo","Orellana","Pastaza","Sucumbios","Zamora Ch"]
    insular=["Galapagos"]
    dic={"Region":["Costa","Sierra","Oriente","Insular"],"NumeroSismos":[0,0,0,0]}
    for sismo in lista:
        if sismo[-1] in costa:
            dic["NumeroSismos"][0]+=1
        elif sismo[-1] in sierra:
            dic["NumeroSismos"][1]+=1
        elif sismo[-1] in oriente:
            dic["NumeroSismos"][2]+=1
        elif sismo[-1] in insular:
            dic["NumeroSismos"][3]+=1
    return dic

def crearGraficaPastel(lista):
    datos = sismosRegion(lista)
    df = pd.DataFrame(datos)
    data = [
                go.Pie(labels=df["Region"],
                       values=df["NumeroSismos"],
                       hoverinfo='label+value',
                       textinfo='percent'
                       )
    ]
    layout=go.Layout(
        title="Cantidad de Sismos por Región"
    )

    fig = go.FigureWidget(data=data, layout=layout)
    plot(fig, filename='sismosregiones.html',auto_open=False)

def sismosProfundidadRegion(lista):
    dic={"Tipo":["Superficial","Intermedio","Profundo"],"Cantidad":[0,0,0]}
    for sismo in lista:
        if 0<float(sismo[3])<=60:
            dic["Cantidad"][0]+=1
        elif 60<float(sismo[3])<=300:
            dic["Cantidad"][1]+=1
        elif float(sismo[3])>300:
            dic["Cantidad"][2]+=1
    return dic

def crearPastelProfundidad(lista):
    datos=sismosProfundidadRegion(lista)
    colors=["red","yellow","green"]
    df = pd.DataFrame(datos)
    data = [go.Pie(labels=df["Tipo"],
                   values=df["Cantidad"],
                   hoverinfo='label+value',
                   textinfo='percent',
                   marker=dict(colors=colors)
                   )
    ]

    layout = go.Layout(
        title="Tipos de sismos según su Profundad",
    )
    fig = go.FigureWidget(data=data, layout=layout)
    plot(fig, filename='sismosprofundidad.html',auto_open=False)



mapbox_access_token = "pk.eyJ1Ijoiam9hbmVzY28iLCJhIjoiY2pyYTJzNXV5MG56ejN5czdsbHlzcWlxbCJ9.ls23IZMjQ4Rndi0J4rPd9A"

data =[
    go.Scattermapbox(
        lat=['-2.176049'],
        lon=['-79.919096'],
        mode='markers',
    )
]
layout = go.Layout(
    height=600,
    autosize=True,
    hovermode='closest',
    mapbox=dict(
                sourcetype = 'geojson',
                source = 'provincias.geojson',
                type = 'fill',
                color = 'rgba(163,22,19,0.8)'
            ),
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=27.8,
            lon=-83
        ),
        pitch=0,
        zoom=5.2
    )

fig = dict(data=data, layout=layout)
plot(fig, filename='county-level-choropleths-python')

#crearGraficaPastel(sismos)
#crearGraficoBarrasFranja(sismos)
#crearGraficoBarrasMagnitud(sismos)
