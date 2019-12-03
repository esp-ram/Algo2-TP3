from grafos import *
import csv
import operator


# TODO: ordenar la cola en cada paso(simular el heap)
def dijkstra(grafo,origen):
    distancia = {}
    padre = {}

    for vertice in ver_vertices(grafo):
        distancia[vertice] = float('inf')

    distancia[origen] = 0
    padre[origen] = None

    cola = []

    cola.append((distancia[origen],origen))

    while len(cola) != 0:
        dist,vertice = cola.pop(0)
        for w in ver_adyacentes(grafo,vertice):
            if distancia[vertice] + obtener_peso(grafo,vertice,w) < distancia[w]:
                distancia[w] = distancia[vertice] + obtener_peso(grafo,vertice,w)
                padre[w] = vertice
                cola.append((distancia[w],w))

    return padre,distancia


# REVIEW: verificar que origen/destino estan en el diccionario
def camino_dist_minimo(grafo,origen,destino):
    fath,dist = dijkstra(grafo,origen)
    camino = [destino]
    while camino[0] != origen:
        camino.insert(0,fath[camino[0]])
    return (camino,dist[destino])


def BFS(grafo,origen):
    visitados = set()
    padre = {}
    orden = {}
    cola = []
    visitados.add(origen)
    orden[origen] = 0
    padre[origen] = None
    cola.append(origen)
    while len(cola) != 0:
        vertice = cola.pop(0)
        for w in ver_adyacentes(grafo,vertice):
            if w not in visitados:
                visitados.add(w)
                cola.append(w)
                padre[w] = vertice
                orden[w] = orden[vertice]+1

    return padre,orden


#### TESTS ####
"""
precios = crear_grafo()

with open('vuelos.csv', "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        agregar_vertice(precios,row[0])
        agregar_vertice(precios,row[1])

with open('vuelos.csv', "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        agregar_arista(precios,row[0],row[1],int(row[3]))

print(BFS(precios,"SAN"))
"""

"""
print(camino_minimo(precios,"SAN","JFK"))
print(camino_minimo(precios,"SAN","LGA"))
print(camino_minimo(precios,"CLD","JFK"))
print(camino_minimo(precios,"CLD","LGA"))

print(distancia_minima(precios,"LAS","MIA"))
"""

"""
lista=[]

lista.append(camino_dist_minimo(precios,"SAN","JFK"))
lista.append(camino_dist_minimo(precios,"SAN","LGA"))
lista.append(camino_dist_minimo(precios,"CLD","JFK"))
lista.append(camino_dist_minimo(precios,"CLD","LGA"))

print(min(lista,key=operator.itemgetter(1)))
"""
