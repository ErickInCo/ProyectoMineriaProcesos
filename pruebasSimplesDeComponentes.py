lst = ['A', 'E', 'F']
lst2 = ['A', 'E', 'F', 'C', 'B']
sourceFile = open('traza.txt', 'w')
print(lst2, file = sourceFile, end = '')
sourceFile.close()
sourceFile= open("traza.txt", "r")
s=sourceFile.readline()
sourceFile.close()
s2="'"+s+"'"
print(s2)
# print(list1)
# str2="'"+print(list1)+"'"
# print(str2)