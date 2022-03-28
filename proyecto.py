# data
from audioop import reverse
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



#Trazas

import pandas as pd
import numpy as np
import copy


# Python code to sort the tuples using second element 
# of sublist Inplace way to sort using sort()
def Sort(sub_li):
  
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of 
    # sublist lambda has been used
    sub_li.sort(key = lambda x: x[1], reverse=1)
    return sub_li




##Dicionarios para contar las trazas
TrazasSinRepetir = list()

##Dicionarios para combertir de evento <-> letra y evento <-> numero
ActividadesN = dict()
ActividadesL = dict()
ActividadesNI = dict()
ActividadesLI = dict()

##Contador de eventos
contA=0
##Inicializar lista de trazas
listaTraza=list()

# xes 
log = xes_importer.apply('Sepsis Cases - Event LogArtificial.xes')


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
    ##Agregar la traza a la lista de trazas sin repetir y contar incidencias
    
    ban=1
    for x in TrazasSinRepetir:
        if x[0]==Traza:
            ban=0
            x[1]=x[1]+1
            break
    if ban==1:
        laux=list()
        laux.append(Traza.copy())
        laux.append(1)
        TrazasSinRepetir.append(laux.copy())
        
    listaTraza.append(Traza)

## Calculo de Varianza ##
    ## Agrupar por trazas iguales ##
    #Ordenar las trazas por numero de incidencias

TrazasSinRepetir=Sort(TrazasSinRepetir)

##Buscar frecuencias relativas
for x in TrazasSinRepetir:
    fr=x[1]/len(listaTraza)
    x.append(fr)

##Calcular varianza
sumas=0
for x in TrazasSinRepetir:
    sumas=sumas+(x[2]**2)

k=len(TrazasSinRepetir)
varianza=(1-(sumas))/((k-1)/k)

for x in TrazasSinRepetir:
    if x[1]>=1:
        print(x[0], ' : ', x[1], ' : ', x[2])


print("IVC= "+str(varianza))



# print(TrazasSinRepetir)

########## Fin de Lectura de trazas ###################




