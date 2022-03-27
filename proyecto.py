# data
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.objects.log.util import dataframe_utils
from pm4py import format_dataframe

# process mining 
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

# viz
from pm4py.visualization.petrinet import visualizer as pn_visualizer
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualization

# misc 
from pm4py.objects.conversion.process_tree import converter as pt_converter
import json
# from collections import Counter

#Trazas

from sklearn.cluster import KMeans
from sklearn import metrics
import pandas as pd
import numpy as np
import operator
import random
import math
import time
import copy

ActividadesLI = dict()
CentroidesFinales=list()
TrazasC=list()
##Dicionarios para contar las trazas
TrazasSinRepetir = dict()

##Dicionarios para combertir de evento <-> letra y evento <-> numero
ActividadesN = dict()
ActividadesL = dict()
ActividadesNI = dict()
# global ActividadesLI
##Contador de eventos
contA=0
##Inicializar lista de trazas
listaTraza=list()

# xes 
log = xes_importer.apply('Sepsis Cases - Event LogArtificial.xes')

# csv
##df = pd.read_csv('running-example.csv')
##df = dataframe_utils.convert_timestamp_columns_in_df(df)
##df = df.sort_values('time:timestamp')



##Leer archivo xes
log = log_converter.apply(log)
dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)

########## Inicio de Lectura de trazas ###################

##Recorrer el log de eventos y registrar cada evento
for x in log:
    Traza=list()
    for y in x:
        evento = y["concept:name"]
        if evento not in ActividadesN:
            contA=contA+1
            ##Registrar el evento en los diccionarios de evento
            ActividadesN[evento]=contA
            ActividadesL[evento]=chr(contA+64)
            ActividadesNI[contA]=evento
            ActividadesLI[chr(contA+64)]=evento
        ##Generar la traza en envetos tipo A,B,C,D,D,F
        Traza.append(ActividadesL[evento])
    ##Agregar la traza a la lista de trazas
    # print(Traza)
    sourceFile = open('traza.txt', 'w')
    print(Traza, file = sourceFile, end = '')
    sourceFile.close()
    sourceFile= open("traza.txt", "r")
    s=sourceFile.readline()
    sourceFile.close()
    buscar="'"+s+"'"
    
    # print(buscar)
    if TrazasSinRepetir.get(buscar)== None:
        TrazasSinRepetir[buscar]=1
    else:
        TrazasSinRepetir[buscar]=TrazasSinRepetir.get(buscar)+1
    listaTraza.append(Traza)

## Calculo de Varianza ##
    ## Agrupar por trazas iguales ##
for key, value in TrazasSinRepetir.items():
    if value>=2:
        print(key, ' : ', value)
# print(TrazasSinRepetir)

########## Fin de Lectura de trazas ###################




########## Inicio de Inductive ###################
# create the process tree
tree = inductive_miner.apply_tree(log)

# viz
gviz = pt_visualizer.apply(tree)
pt_visualizer.view(gviz)

# convert the process tree to a petri net
net, initial_marking, final_marking = pt_converter.apply(tree)

# alternatively, use the inductive_miner to create a petri net from scratch
# net, initial_marking, final_marking = inductive_miner.apply(log)

# viz
parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
gviz = pn_visualizer.apply(net, initial_marking, final_marking, 
                           parameters=parameters, 
                           variant=pn_visualizer.Variants.FREQUENCY, 
                           log=log)
pn_visualizer.view(gviz)
########## Fin de Inductive ###################