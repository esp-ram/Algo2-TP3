from grafos import *
import csv
import operator
import random


# TODO: ordenar la cola en cada paso(simular el heap)
def dijkstra(grafo,origen):
    distancia = {}
    padre = {}

    for vertice in ver_vertices(grafo):
        distancia[vertice] = float('inf')

    distancia[origen] = 0
    padre[origen] = None

    cola = []

    cola.append([distancia[origen],origen])
    while len(cola) != 0:
        cola.sort(key=operator.itemgetter(0), reverse = False)
        dist,vertice = cola.pop(0)
        for w in ver_adyacentes(grafo,vertice):
            if distancia[vertice] + obtener_peso(grafo,vertice,w) < distancia[w]:
                distancia[w] = distancia[vertice] + obtener_peso(grafo,vertice,w)
                padre[w] = vertice
                cola.append([distancia[w],w])

    return padre,distancia


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


def _DFS(grafo,origen,visitados,padre,orden):
    visitados.add(origen)
    for w in ver_adyacentes(grafo,origen):
        if w not in visitados:
            padre[w] = origen
            orden[w] = orden[origen]+1
            _DFS(grafo,w,visitados,padre,orden)


def DFS(grafo,origen):
    visitados = set()
    padres = {}
    orden = {}
    orden[origen] = 0
    padres[origen] = None
    _DFS(grafo,origen,visitados,padres,orden)
    for v in ver_vertices(grafo):
        if v not in visitados:
            orden[v] = 0
            padre[v] = None
            _DFS(grafo,v,visitados,padres,orden)
    return padres,orden


def ordenar_vertices(graf,dicc_distancia):
    lista = []
    for key in dicc_distancia:
        if dicc_distancia[key] == float('inf'):
            continue
        lista.append((key,dicc_distancia[key]))

    lista.sort(key=operator.itemgetter(1),reverse=True)
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


def orden_topologico(grafo):
    grados = {}
    for v in ver_vertices(grafo):
        grados[v] = 0

    for v in ver_vertices(grafo):
        for w in ver_adyacentes(grafo,v):
            grados[w] += 1

    cola = []

    for v in ver_vertices(grafo):
        if grados[v] == 0:
            cola.append(v)

    resultado = []

    while len(cola) != 0:
        v = cola.pop(0)
        resultado.append(v)
        for w in ver_adyacentes(grafo,v):
            grados[w] -= 1
            if grados[w] == 0:
                cola.append(w)

    if len(resultado) == len(grafo):
        return resultado
    else:
        return None


def arista_minima(grafo):
    aristas = []
    for vertice in ver_vertices(grafo):
        for ady in ver_adyacentes(grafo,vertice):
            aristas.append(grafo[vertice][ady])
    return min(aristas)
