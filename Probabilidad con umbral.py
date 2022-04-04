def prob(a,b,trazas):
    cont=0
    total=len(trazas)
    for x in trazas:
        for y in range(1,len(x)):
            if x[y-1]==a and x[y]==b:
                cont=cont+1
                break
    return cont/total

def ordenar(e):
    return e[-1]

#Leer archivo, tiene que estar en la misma carpeta
ar = open ('sepsis_datos_artificales.txt', 'r')
umbral=0.3
trazas=list()

for x in ar:
    aux=x.replace("\n","")
    objetos = aux.split(",")
    trazas.append(objetos)
for x in trazas:
    contval=0
    for y in range(1,len(x)):
        if prob(x[y-1],x[y],trazas) >= umbral:
            contval=contval+1
        else:
            contval=contval-1
    x.append(contval)
trazas.sort(reverse=True, key=ordenar)
for x in trazas:
    # print(x)
    if x[-1] >0:
        print(x)

