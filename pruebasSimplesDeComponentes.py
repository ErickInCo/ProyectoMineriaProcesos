lst = ['A', 'E', 'F']
lst2 = ['A', 'E', 'F', 'C', 'B']
listaContarTrazas=list()

nlist=list()
nlist.append(lst)
nlist.append(1)
listaContarTrazas.append(nlist)
nlist=list()
nlist.append(lst2)
nlist.append(21)
listaContarTrazas.append(nlist)
# sourceFile = open('traza.txt', 'w')
# print(lst2, file = sourceFile, end = '')
# sourceFile.close()
# sourceFile= open("traza.txt", "r")
# s=sourceFile.readline()
# sourceFile.close()
# s2="'"+s+"'"
print(listaContarTrazas)
ban=1
for x in listaContarTrazas:
    print(x[0])
    if lst2 == x[0]:
        ban=0
        print("si esta")
        break
# print(list1)
# str2="'"+print(list1)+"'"
# print(str2)