from grafos import *
from util_grafos import *
import csv
import random



tiempos = crear_grafo()
copia = []

with open('vuelos.csv', "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        agregar_vertice(tiempos,row[0])
        agregar_vertice(tiempos,row[1])
        copia.append(row)

with open('vuelos.csv', "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        agregar_arista(tiempos,row[0],row[1],int(row[2]))

# p = prim(tiempos,"SAN")

# total = 0
# for key in p:
#     for k1 in p[key]:
#         total += p[key][k1]



def recorrida(grafo, lista, inicio, longMaximo, longActual,resultado):
    if longActual > longMaximo[len(longMaximo)-1]:
        return False


    completo = True
    i = 0
    for item in ver_vertices(grafo):
        if item not in lista:
            completo = False
            i += 1

    # 164 es el minimo de costo minimo de vuelos_inventados
    # si la cantidad de vuelos que faltan multiplicado por el costo minimo igualmente se
    # excede del maximo se descarta
    if ((i)*24 + longActual) >= longMaximo[len(longMaximo)-1]:
        return False


    if completo == True:
        print("cumple",lista,"long",longActual)
        pap = lista.copy()
        longMaximo.append(longActual)
        resultado.append(pap)
        return

    for vertice in ver_adyacentes(grafo,inicio):
        print("inicio: {}, adyacente: {}".format(inicio,vertice))
        lista.append(vertice)
        if recorrida(grafo,lista,vertice,longMaximo,longActual+obtener_peso(grafo,inicio,vertice),resultado) != True:
            lista.pop()
            continue
        longMaximo = longActual+obtener_peso(grafo,inicio,vertice)



def N_Lugares(grafo, final, inicio, cantidad, lista, n,resultado):
    if n == cantidad:
        # print("n == cantidad y ultimo vertice",lista[len(lista)-1])
        if lista[len(lista)-1] in ver_adyacentes(grafo,final):
            # print("CAMINO COMPLETO!!!!!!!!!!!")
            pap = lista.copy()
            resultado.append(pap)
            return lista
        return False

    for vertex in ver_adyacentes(grafo,inicio):
        if len(resultado) != 0:
            return
        # print("ady {} para vertice {}".format(vertex,inicio))
        if vertex in lista:
            # print("vertice visitado")
            continue
        lista.append(vertex)
        if N_Lugares(grafo,final,vertex,cantidad,lista,n+1,resultado) != True:
            lista.pop()
            continue



def pagerank(grafo,diccionario):
    tamano = len(ver_vertices(grafo))
    for vertice in ver_vertices(grafo):
        total = 0
        for adyacente in ver_adyacentes(grafo,vertice):
            total += (diccionario[adyacente] / (len(ver_adyacentes(grafo,adyacente))))
        diccionario[vertice] = ((1-0.85)/tamano) + (0.85)*total
    return diccionario



"""
lista = []
respuesta = []
largos = []
lista.append("SAN")
print(total)
# minimo teorico 8500
# minimo mst 22250
largos.append(8500)
# recorrida(tiempos,lista,"SAN",largos,0,respuesta)
# print("Mejor ruta: {}, Costo: {}".format(respuesta[len(respuesta)-1],largos[len(largos)-1]))
"""

"""
l1 = []
l1.append("SAN")
r1 = []
N_Lugares(tiempos,"SAN","SAN",5,l1,0,r1)
print(r1)
"""

factor = 1/len(ver_vertices(tiempos))
dicc = {}
for vertice in ver_vertices(tiempos):
    dicc[vertice] = factor

# for i in range(100):
#     pagerank(tiempos,dicc)
lista_diccs = []
lista_diccs.append(dicc)
i=0
lista_diccs.append(pagerank(tiempos,lista_diccs[i]))
i+=1
ban = True
while(ban):
    for vertice in ver_vertices(tiempos):
        if abs(lista_diccs[i][vertice] - lista_diccs[i-1][vertice]) < 0.09:
            ban = False
            break
    lista_diccs.append(pagerank(tiempos,lista_diccs[i]))
    i += 1


li = []
for key in dicc:
    li.append((key,dicc[key]))

li.sort(key = operator.itemgetter(1))

print(li)
