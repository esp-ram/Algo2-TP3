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
def padre_dist_minimo(grafo,origen,destino):
    fath,dist = dijkstra(grafo,origen)
    return (fath[destino],dist[destino])



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


def ordenar_vertices(graf,dicc_distancia):
    lista = []
    for key in dicc_distancia:
        if dicc_distancia[key] == float('inf'):
            continue
        lista.append((key,dicc_distancia[key]))

    lista.sort(key=operator.itemgetter(1),reverse=True)
    # print(lista)
    listaref = []
    for item in lista:
        listaref.append(item[0])
    return listaref


def centralidad(grafo):
    centr = {}
    for v in ver_vertices(grafo):
        centr[v] = 0

    for v in ver_vertices(grafo):
        padre,distancia = dijkstra(grafo,v)
        centr_aux = {}
        for w in ver_vertices(grafo):
            centr_aux[w] = 0

        vertices_ordenados = ordenar_vertices(grafo,distancia)
        for w in (vertices_ordenados):
            if padre[w] == None:
                continue
            centr_aux[padre[w]] += (1 + centr_aux[w])

        for w in ver_vertices(grafo):
            if w == v:
                continue
            centr[w] += centr_aux[w]

    return centr


def prim(grafo,vertice):
    visitados = set()
    visitados.add(vertice)
    cola = []
    for w in ver_adyacentes(grafo,vertice):
        cola.append((vertice,w,obtener_peso(grafo,vertice,w)))

    cola.sort(key=operator.itemgetter(2))

    gr = crear_grafo()
    for vertex in ver_vertices(grafo):
        agregar_vertice(gr,vertex)

    while len(cola)!= 0:
        cola.sort(key=operator.itemgetter(2))
        v,w,peso = cola.pop(0)
        if w in visitados:
            continue

        agregar_arista(gr,v,w,peso)
        visitados.add(w)
        for x in ver_adyacentes(grafo,w):
            if x not in visitados:
                cola.append((w,x,obtener_peso(grafo,w,x)))

    return gr

#### TESTS ####
"""
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
        """

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
tiempos = crear_grafo()


cont_atl=0
cont_ord=0
cont_lax=0
cont_dfw=0
cont_den=0

with open('vuelos.csv',"r") as csvfile:
    spamreader = csv.reader(csvfile,delimiter=',')
    for row in spamreader:
        agregar_vertice(tiempos,row[0])
        agregar_vertice(tiempos,row[1])
        # if (row[0] or row[1]) == "ATL":
        #     cont_atl += 1
        # elif (row[0] or row[1]) == "ORD":
        #     cont_ord += 1
        # elif (row[0] or row[1]) == "LAX":
        #     cont_lax += 1
        # elif (row[0] or row[1]) == "DFW":
        #     cont_dfw += 1
        # elif (row[0] or row[1]) == "DEN":
        #     cont_den += 1
        # totalvuelos += int(row[4])

# print(cont_atl)
# print(cont_ord)
# print(cont_lax)
# print(cont_dfw)
# print(totalvuelos)


with open('vuelos.csv', "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        agregar_arista(tiempos,row[0],row[1],1/int(row[4]))

p,di = dijkstra(tiempos,"JFK")
o = ordenar_vertices(tiempos,di)
print(o)

c = centralidad(tiempos)
# print(c)
def ord(dixi):
    lista = []
    for key in dixi:
        lista.append((key,dixi[key]))

    lista.sort(key=operator.itemgetter(1),reverse=True)
    return lista

print(ord(c))
"""

"""
print(camino_dist_minimo(tiempos,"SAN","JFK"))
print(camino_dist_minimo(tiempos,"SAN","LGA"))
print(camino_dist_minimo(tiempos,"CLD","JFK"))
print(camino_dist_minimo(tiempos,"CLD","LGA"))
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
