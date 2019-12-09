from grafos import *
from util_grafos import *
import csv



tiempos = crear_grafo()

with open('vuelos_inventados.csv', "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        agregar_vertice(tiempos,row[0])
        agregar_vertice(tiempos,row[1])

with open('vuelos_inventados.csv', "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        agregar_arista(tiempos,row[0],row[1],int(row[2]))

p = prim(tiempos,"BAT")

total = 0
for key in p:
    for k1 in p[key]:
        total += p[key][k1]




def recorrida(grafo, lista, inicio, longMaximo, longActual,resultado):
    if longActual > longMaximo[len(longMaximo)-1]:
        return False


    completo = True
    for item in ver_vertices(grafo):
        if item not in lista:
            completo = False


    if completo == True:
        print("cumple",lista,"long",longActual)
        pap = lista.copy()
        longMaximo.append(longActual)
        resultado.append(pap)
        return

    for vertice in ver_adyacentes(grafo,inicio):
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
        # print("ady {} para vertice {}".format(vertex,inicio))
        if vertex in lista:
            # print("vertice evisitado")
            continue
        lista.append(vertex)
        if N_Lugares(grafo,final,vertex,cantidad,lista,n+1,resultado) != True:
            lista.pop()
            continue


"""
lista = []
respuesta = []
largos = []
lista.append("BAT")
largos.append(total*2)
recorrida(tiempos,lista,"BAT",largos,0,respuesta)
print("Mejor ruta: {}, Costo: {}".format(respuesta[len(respuesta)-1],largos[len(largos)-1]))
"""


l1 = []
l1.append("BAT")
r1 = []
print(N_Lugares(tiempos,"BAT","BAT",5,l1,0,r1))
print(r1)
