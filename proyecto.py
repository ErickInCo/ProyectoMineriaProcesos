# data
from audioop import reverse
import pandas as pd
import pm4py
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

from sympy import re

# KL Divergente
import math

# Ordenar las trazas por el segundo elemento de la lista de forma decendente
# Python code to sort the tuples using second element 
# of sublist Inplace way to sort using sort()
def Sort(sub_li):
  
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of 
    # sublist lambda has been used
    sub_li.sort(key = lambda x: x[1], reverse=1)
    return sub_li

# Funcion para calcular la seleccion por probabilidad de frecuencias
def prob(a,b,trazas):
    """
    Cuenta el numero de veces que aparece el par de eventos a seguido de b en las trazas, 
    para despues dividir entre el numero de trazas
    
    :param a: Primer evento
    :param b: Segundo evento
    :param trazas: lista de trazas en el sistema
    :return: La probabilidad de que apareza a,b en todas las trazas
    """
    cont=0
    total=len(trazas)#Total de Trazas
    for x in trazas:#Recorrer todas las trazas
        for y in range(2,len(x)):#Recorrer cada traza (trazaOrigina,a,b,c) por elemento empezando desde el elemento b
            if x[y-1]==a and x[y]==b:#Condicion para saber si se cumple evento a,b
                cont=cont+1#Contar dicho evento
                break
    return cont/total#regresar la probabilidad (numero de eventos / total de trazas)

# Funcion para ordenar los resultados de seleccion de frecuencias
def ordenar(e):
    return e[-1]#Ordena por el ultimo elemento, es decir la frecuencia en cada traza



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


#Archivos de datos 

# nombrearchivo="Sepsis Cases - Event LogArtificial.xes"
#nombrearchivo="CCC19LogCSV.csv"
# nombrearchivo="ArtificialPatientTreatment.csv"
nombrearchivo="example.xes"
# nombrearchivo="Hospital Billing - Event Log.xes"
# nombrearchivo="Sepsis Cases - Event Log.xes"



# Importar los datos para archivos xes

if nombrearchivo[-3:]=="xes":
    # Importar el log de eventos a python
    # Importing the log file into the python environment.
    log = xes_importer.apply(nombrearchivo)
    #Convertir los datos a formato log
    # The above code is applying the log_converter function to the log variable.
    log = log_converter.apply(log)
    #Generar datos en formato de tabla
    dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)

#Importar los datos para archivos csv
elif nombrearchivo[-3:]=="csv":
    #Importar el log de eventos a python especificando que el archivo es separado por "," comas
    dataframe = pd.read_csv(nombrearchivo, sep=',')
    #Transformar los datos en formato de log para compativilidad con libreria pm4py
    # The above code is converting the dataframe into a format that is compatible with the pm4py library.
    dataframe = pm4py.format_dataframe(dataframe, case_id='patient', activity_key='action', timestamp_key='DateTime')
    log = pm4py.convert_to_event_log(dataframe)

#Indicador de nombres de evento en las bitacoras
eventkey='concept:name'

# Crear log de eventos vacio para almacenar la SI en formato log
# Creating an empty event log.
log2 = pm4py.objects.log.obj.EventLog()


########## Inicio de Lectura de trazas ###################

##Recorrer el log de eventos y registrar cada evento
#Variables para datos generales como Traza mas grande y mas pequeña, promedio de tamaño
c2=0
trazaMG=0
trazaMC=10000
trazapromedio=0
sumatamanoTraza=0

#Recorrer todo el log
# Iterating through the log list and printing each item in the list.
for x in log:
    Traza=list()#Inicializar traza vacia 
    # Appending the value of Trace to the list Traza.
    Traza.append(x)#Agregar la traza en formato log a la lista
    #recorer toda la traza
    # Iterating through the list Trace and printing each element.
    for y in x:
        # Creating a new variable called evento, which is the value of the variable y at the index
        # eventkey.
        evento = y[eventkey]#Almacenar el evento utilizando el identificador eventkey
        #Comprobar si el evento se registro anteriormente 
        # Checking if the evento is not in the list ActividadesN.
        if evento not in ActividadesN:
            contA=contA+1# incrementar el contador de eventos distintos
            ##Registrar el evento en los distintos diccionarios de eventos
            ActividadesN[evento]=contA#Nombre/Numero
            ActividadesL[evento]=chr(contA+64)#Nombre/Letra
            ActividadesNI[contA]=evento#Numero/Nombre
            ActividadesLI[chr(contA+64)]=evento#Letra/Nombre
        ##Generar la traza en envetos tipo A,B,C,D,D,F
        Traza.append(ActividadesL[evento])#Agregar a la traza auxiliar la representacion del evento en Letra
    
    ##Agregar la traza a la lista de trazas sin repetir y contar incidencias
    ban=1#Indicador si la traza ya existete en la lista 0 Ya existe 1 No existe
    #Recorrer el lista de trazas sin repetir
    for x in TrazasSinRepetir:
        if x[0][1:]==Traza[1:]:#identifcar si la traza es igual con otra de la lista
            ban=0#Marcar que ya esta en la lista
            x[1]=x[1]+1#incrementar en 1 la frecuencia
            break
    if ban==1:#Si no existe la traza
        laux=list()
        laux.append(Traza.copy())#Agregar la traza a lista auxiliar
        laux.append(1)#colocar una frecuencia de 1
        TrazasSinRepetir.append(laux.copy())#Agregar la traza con su frecuencia a las trazas sin repetir
    
    sumatamanoTraza=sumatamanoTraza+len(Traza)-1#Contador de tamaño de traza para el promedio de tamaño
    if len(Traza)-1>trazaMG:#Identificar si existe una traza mas grande 
        trazaMG=len(Traza)-1#asignar el valor de la nueva traza mas grande
    if len(Traza)-1<trazaMC:#identificar si existe una traza mas chica
        trazaMC=len(Traza)-1#asignar el valor de la nueva traza mas chica

    listaTraza.append(Traza)#agregar la traza ya con formato a la lista de trazas

## Calculo de Varianza ##
    ## Agrupar por trazas iguales ##
    #Ordenar las trazas por numero de incidencias

TrazasSinRepetir=Sort(TrazasSinRepetir)#Ordenar las trazas por frecuencia

########## Imprimir datos de trazas#############
print("########################################################\n\n")
trazapromedio=sumatamanoTraza/len(listaTraza)
print("Longitud de traza mas grande : "+str(trazaMG))
print("Longitud de traza mas chica : "+str(trazaMC))
print("Longitud promedio de traza : "+str(trazapromedio))
print("\n\n")
print("########################################################\n\n")
########## Imprimir Trazas ###################
i=1
print("########################################################\n\n")
for x in listaTraza:
    print(i, end=" ")
    for y in range(1,len(x)):
        print(x[y], end=",")
    print()
    i=i+1
print("########################################################\n\n")

##Buscar frecuencias relativas
#Recorrer las trazas sin repetir
for x in TrazasSinRepetir:
    fr=x[1]/len(listaTraza)#obtener la frecuencia calculando el numero de incidencias entre el total de trazas
    x.append(fr)#agregar el resultado al final de la traza

##Calcular varianza
sumas=0#contador
#recorrer las trazas sin repetir
for x in TrazasSinRepetir:
    sumas=sumas+(x[2]**2)#realizar una sumatoria de fr^2

k=len(TrazasSinRepetir)#el valor k se obtiene del numero total de trazas sin repetir
varianza=(1-(sumas))/((k-1)/k)# la varianza se obtiene con la formula


# Dp
# l numero de eventos en todas las trasas
# n numero de trasas
# s arreglo con datos de cada n/l
# f numero de evento en todas las trazas
# v arreglo con las frecuencias de evento por traza
ldato=0
slista=list()
#Recorrer las trazas
for x in listaTraza:
    tt=len(x[1:])#Obtener el tamño de la traza
    ldato=ldato+tt#Agregar el valor al contador de tamaño
    slista.append(tt)#agregar el valor a la slista
n=len(listaTraza)#obtener el valor n con el numero de trazas

myArray = np.array(slista)#convertir los datos en array
myInt = ldato#guardar el dato por el cual va a dividir a cada valor
newArray = myArray/myInt#realizar la divicion de cada elemento entre el ldato


leventos=list(ActividadesL.values())#convertir a lista el diccionario de actividades por letra
veventos=list()
feventos=list()

#recorrer lista de eventos en letra
for x in leventos:
    # calcular f y v
    v=list()
    f=0
    #recorer las trazas
    for y in listaTraza:
        z=y[1:]#almacenar temporalmente la traza en formato de letras
        count_a = z.count(x)# Contar el numero de evento actual X en la traza actual Z
        f=f+count_a#almacenar el acumulado en contador f
        v.append(count_a)#agregar a la lista el valor de incidencias del evento X por la traza
    veventos.append(v)#alamacenar el dato v en la lista final
    feventos.append(f)#alamacenar el dato f en la lista final


# Calculo de DP
DP=0
resultadosdp=list()
#recorrer desde 0 hasta el numero total de eventos 
for x in range(0,len(leventos)):
    resultado=0
    #recorrer desde 0 hasta el numero total de trazas
    for y in range(0,n):
        resultado=resultado+abs((veventos[x][y]/feventos[x])-newArray[y])#calculo parcial de la formula de DP (|v/fi|-prob)
    dpsinnorml=0.5*resultado#multiplicar el resultado x 0.5
    resultadosdp.append( round(dpsinnorml, 2))# agregar el resultado de dp redondeado a 2 decimales

    DP=DP+dpsinnorml#Acumulado de DP



myArray2 = np.array(resultadosdp)#pasar a array para calcular el promedio
DPpromedio=np.average(myArray2)#calculo de promedio de dp
# Fin de calculo de DP


# Calculo de KL Divergencia
KLd=0
resultadosKLd=list()
#recorrer desde 0 hasta el numero total de eventos
for x in range(0,len(leventos)):
    resultado=0
    #recorrer desde 0 hasta el numero total de trazas
    for y in range(0,n):
        try:
            reslog=math.log2((veventos[x][y]/feventos[x])*(1/newArray[y]))#calculo parcial de la formula de KL (log((v/f)*(1/prob)))
        except ValueError:
            reslog=0#En caso de que el valor no compatibles con log se toma el valor 0
        formula=(veventos[x][y]/feventos[x])*reslog#calculo del resto de la formula KL (v/f *  reultadoLog)
        resultado=resultado+formula#resultado acumulado
        
    KLDnorml=resultado
    
    # print(KLDnorml)
    # print("\n")
    resultadosKLd.append( round(KLDnorml, 2))#agregar resultado redondeado a 2 decimales


    KLd=KLd+KLDnorml#acumulado de kld

# print(KLd)

myArray3 = np.array(resultadosKLd)#convertir a array para manipulacion
KLpromedio=np.average(myArray3)#obtener el promedio de KL

# Fin de calculo de KLdivergente


########## Imprimir Trazas sin repetir ###################
i=1
print("########################################################\n\n")
for x in TrazasSinRepetir:
    print(i, end=" ")
    noMostrar=0
    for y in x:
        if noMostrar==0:
            print(y[1:], end=", ")
            noMostrar=+1
        else:
            print(y, end=", ")
    print()
    i=i+1
print("########################################################\n\n")


# print("IVC= "+str(varianza))
print("Datos DP")
for x in range(0,len(resultadosdp)):
    print(str(leventos[x])+" : "+str(resultadosdp[x]))
print("DP promedio= "+str(DPpromedio))
print("\n")

print("Datos KL")
for x in range(0,len(resultadosKLd)):
    print(str(leventos[x])+" : "+str(resultadosKLd[x]))
print("KLdivergente promedio= "+str(KLpromedio))
print("\n")





########## Fin de Lectura de trazas ###################

########## Variables de seleccion ###################
Pusuario = .5
umbral = .5
TotalTrazasSelecc=len(listaTraza)*Pusuario



########## Seleccion de Instancias  ###################
SI=list()
#realizar seleccion de instancias dependiendo del umbral
if DPpromedio<umbral:
    print("Seleccion de instancias por frecuencia")
    
    print("Se seleccionaran "+str(TotalTrazasSelecc) + " Trazas")
    con=0
    # SI=list()
    #recorrer las trazas sin repetir
    for x in TrazasSinRepetir:
        for y in range(0,x[1]):
            SI.append(x[0].copy())#agregar la traza a la SI
            con=con+1#Aumentar el contador de numero de SI
            if len(SI)>=TotalTrazasSelecc:#SI el numero supera el total de numero de SI terminarl la seleccion
                break
        if len(SI)>=TotalTrazasSelecc:#SI el numero supera el total de numero de SI terminarl la seleccion
            break
    c=0 
    #recorrer la SI
    for x in SI:
        log2.append(x[0])#agregar la traza en formato de log para analisis
        print(c,end=" :")#imprimir No. de traza
        print(x[1:])#Imprimir la traza en formato de letras
        c=c+1# incrementar contador
    # ########## Inicio de BPMN de SI ###################
    # print("\n\nBPMN de la seleccion de instancias\n\n")
    # process_tree2 = pm4py.discover_tree_inductive(log2)
    # bpmn_model2 = pm4py.convert_to_bpmn(process_tree2)
    # pm4py.view_bpmn(bpmn_model2)

    # ########## Fin de BPMN de SI ###################
    ########## Inicio de BPMN completo ###################
    print("\n\nBPMN completo\n\n")
    process_tree = pm4py.discover_tree_inductive(log)#crear arbol de descubrimiento
    bpmn_model = pm4py.convert_to_bpmn(process_tree)#Convertir a bpmn
    pm4py.view_bpmn(bpmn_model)#mostrar bpmn

    ########## Fin de BPMN completo ###################
    # Alineamiento
    net, initial_marking, final_marking = inductive_miner.apply(log2)#obtener variables de log de SI
    from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments#Agregar liberiras
    aligned_traces = alignments.apply_log(log2, net, initial_marking, final_marking)# realizar aliniamiento 
    print(alignments)#imprimir alineamientos
    #recorrer los resultados de los alineamientos por traza
    for x in aligned_traces:
        print(x)#imprimir resultados por traza
    from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness#agregar librerias
    log_fitness = replay_fitness.evaluate(aligned_traces, variant=replay_fitness.Variants.ALIGNMENT_BASED)#calculo de fitnes

    print(log_fitness) #imprimir resultados

        


elif DPpromedio>=umbral:
    print("Selección de instancias por similitud")
    print("Se seleccionaran "+str(TotalTrazasSelecc) + "Trazas")
    ########## Seleccion por patrones de secuencia frecuentes ###################
    #recorrer las trazas
    for x in listaTraza:
        contval=0
        #recorrer la trazas en formato de letras
        for y in range(2,len(x)):
            #calcular el valor de la traza usando la probabilidad si es mayor (+1) o menor(-1) a la seleccionada
            if prob(str(x[y-1]),str(x[y]),listaTraza) >= Pusuario:
                contval=contval+1
            else:
                contval=contval-1
        x.append(contval)#agregar el resultado a la traza
    listaTraza.sort(reverse=True, key=ordenar)#ordenar con base en el resutado
    c=0
    #recorrer las trazas
    for x in listaTraza:
        # print(x)
        print(x[1:])#mostrar traza en formato letra
        SI.append(x.copy())#agragar a la SI
        log2.append(x[0])#agregar la traza en formato Log
        c=c+1#incrementar contador de trazas en la SI
        if c==TotalTrazasSelecc:#Terminar de seleccionar cuando se alcance el numero buscado
            break
    print(c)
    ########## Inicio de BPMN de SI ###################
    print("\n\nBPMN de la seleccion de instancias\n\n")
    process_tree2 = pm4py.discover_tree_inductive(log2)#Generar arbol de descubrimiento
    bpmn_model2 = pm4py.convert_to_bpmn(process_tree2)#convertir el arbol a bpmn
    pm4py.view_bpmn(bpmn_model2)#mostrar BPMN

    ########## Fin de BPMN de SI ###################
    # Alineamiento
    net, initial_marking, final_marking = inductive_miner.apply(log2)#obtener variables de log de SI
    from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments#Agregar liberiras
    aligned_traces = alignments.apply_log(log2, net, initial_marking, final_marking)# realizar aliniamiento 
    print(alignments)#imprimir alineamientos
    #recorrer los resultados de los alineamientos por traza
    for x in aligned_traces:
        print(x)#imprimir resultados por traza
    from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness#Agregar liberiras
    log_fitness = replay_fitness.evaluate(aligned_traces, variant=replay_fitness.Variants.ALIGNMENT_BASED)#calculo de fitnes

    print(log_fitness) #imprimir resultados

# Generacion pb
N=2
#recorrer la SI
for x in SI:
    nGramSum=1
    #recorrer la traza en formato letra a partir del segundo evento
    for i in range(N,len(x)):
        buscar=x[i-1:i]#Elemento a buscar (a)
        buscarC=x[i-1:i+1]#Elemento a buscar (a,b)
        cBuscar=0#contador de elemento (a)
        cBuscarC=0#contador de elemento (a,b)
        #recorrer la SI
        for y in SI:
            #Buscar y contar las instancias del elemento (a) en las trazas de la SI
            res = len([buscarC for idx in range(len(y)) if y[idx : idx + len(buscarC)] == buscarC])
            cBuscarC+=res#Incrementar el contador el numero de incidencias (a)
            #Buscar y contar las instancias del elemento (a,b) en las trazas de la SI
            res = len([buscar for idx in range(len(y)) if y[idx : idx + len(buscar)] == buscar])
            cBuscar+=res#Incrementar el contador el numero de incidencias (a,b)
        divi=(cBuscarC/cBuscar)#calcular el valor entre numero de  (a,b)/(a)
        nGramSum=nGramSum*divi#Multiplicar el resultado 
        # print(buscarC,end=" / ")
        # print(buscar)
        # print(str(cBuscarC)+" / "+str(cBuscar))
        # print(divi)
        # print("div = "+str(nGramSum)+"\n\n")
    x.append(nGramSum)#agregar a la traza la suma de Ngram

print("\n\nPromedios\n\n")
cc=1
#imprimir numero de traza con su promedio correspondiente
for x in SI:
    print("Traza "+str(cc)+"  "+str(x[-1]))
    cc+=1

# Margen de error
margenErrorP=0
margenErrorN=0
meX=0
#recorrer desde 0 hasta el total de SI
for x in range(0,len(SI)):
    #calculo de la formula ((fit-promFitnes)^2)/nTrazas
    res=((aligned_traces[x]["fitness"]-log_fitness["average_trace_fitness"])**2)/len(SI)
    meX+=res#acumular resultado
#calculo del margen de error con la formula 0.97x raiz2(acumulado/ntrazas)
margenErrorP=0.95* math.sqrt(meX/len(SI))
margenErrorN=-1*margenErrorP

print("Margen de Error = ±" + str(margenErrorP) )#mostrar margen de error

print()
#imprimir las trazas de la SI con su valores
for x in range(0,len(SI)):
    t=SI[x][1:-1]
    f=aligned_traces[x]["fitness"]
    b=SI[x][-1]
    print(str(t)+"  "+str(f)+"   "+str(b))

#Econf
econf=0
pacumulada=0
uconf=len(SI)/len(listaTraza)
#recorrer desde 0 hastar el numero de trasas en SI
for x in range(0,len(SI)):
    t=SI[x][1:-1]#Almacenar la traza en formato de letra
    f=aligned_traces[x]["fitness"]#buscar el fitnes correspondiete a esa traza
    b=SI[x][-1]#buscar el valor b
    #aplicar la formula de econf
    # econf+=(b*f)+((1-pacumulada)*uconf)   #Anterior
    econf+=(b*f)
    pacumulada+=b
print("Econf")
print(str(econf)+" ±"+str(margenErrorP))#mostrar econf con margen de error