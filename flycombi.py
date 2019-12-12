from grafos import *
from util_grafos import *
import csv
import sys
import os

def listar_operaciones():
    print("camino_mas")
    print("camino_escalas")
    print("pagerank")


def obtener_aeropuertos(ciudad,archivo):
    aeros = []
    for city in archivo.keys():
        if city == ciudad:
            return(list(archivo[city].keys()))

    return False


def camino_mas_ops(origen,destino,grafo,archivoAero):
    aeroOrigen = obtener_aeropuertos(origen,archivoAero)
    aeroDestino = obtener_aeropuertos(destino,archivoAero)
    resultados = []
    # que pasa si no hay caminos?
    for salida in aeroOrigen:
        for llegada in aeroDestino:
            resultados.append(camino_dist_minimo(grafo,salida,llegada))

    return min(resultados,key=operator.itemgetter(1))


def camino_mas(modo,origen,destino,grafoPrecios,grafoTiempos,vuelos):
    if (modo != "barato") and (modo != "rapido"):# or origen not in lista_ciudades or destino not in lista_ciudades:
        return False
    if modo == "barato":
        recorrido = camino_mas_ops(origen,destino,grafoPrecios,vuelos)
    elif modo == "rapido":
        recorrido = camino_mas_ops(origen,destino,grafoTiempos,vuelos)

    for i in range(len(recorrido[0])):
        print(recorrido[0][i],end = " ")
        if i != len(recorrido[0])-1 :
            print("->",end = " ")
    print()



def camino_escalas(origen,destino,grafo,aeros):
    aeroOrigen = obtener_aeropuertos(origen,aeros)
    aeroDestino = obtener_aeropuertos(destino,aeros)

    if aeroOrigen == False or aeroDestino == False:
        return False

    resultados = []

    for salida in aeroOrigen:
        padres, orden = BFS(grafo,salida)

        for llegada in aeroDestino:
            resultados.append((salida,llegada,orden[llegada]))

    elegido = min(resultados,key = operator.itemgetter(2))

    recorrido = []
    recorrido.append(elegido[1])
    while recorrido[0] != elegido[0]:
        recorrido.insert(0,padres[recorrido[0]])

    for i in range(len(recorrido)):
        print(recorrido[i],end = " ")
        if i != len(recorrido)-1 :
            print("->",end = " ")
    print()



def pagerank_aux(grafo,dict):
    diccionario = dict.copy()
    tamano = len(ver_vertices(grafo))
    for vertice in ver_vertices(grafo):
        total = 0
        for adyacente in ver_adyacentes(grafo,vertice):
            total += (diccionario[adyacente] / (len(ver_adyacentes(grafo,adyacente))))
        diccionario[vertice] = ((1-0.85)/tamano) + (0.85)*total
    return diccionario


def pagerank(grafo,k):
    factor = 1/len(ver_vertices(grafo))
    parcial = {}
    for vertice in ver_vertices(grafo):
        parcial[vertice] = factor

    listaParciales = []
    listaParciales.append(parcial)
    i = 0

    completado = False
    while(completado == False):
        listaParciales.append(pagerank_aux(grafo,listaParciales[i]))
        i += 1
        for vertice in ver_vertices(grafo):
            if abs(listaParciales[i][vertice] - listaParciales[i-1][vertice]) < 0.00000000000000004:
                completado = True
            else:
                completado = False

    resultado = []
    dicc = listaParciales[len(listaParciales)-1]
    for key in dicc:
        resultado.append((key,dicc[key]))

    resultado.sort(key = operator.itemgetter(1),reverse = True)

    for j in range(k):
        print(resultado[j][0], end = " ")
    print()


# la copia de aeropuertos puede ser un diccionario key:ciudad, values:aeropuertos y coordenadas
def menu(archivoAero,archivoVuelos):
    grafoTiempos = crear_grafo()
    grafoPrecios = crear_grafo()
    copiaAero = {}
    copiaVuelos = []

    with open(archivoAero,"r") as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ',')
        for row in spamreader:
            if row[0] in copiaAero:
                copiaAero[row[0]][row[1]] = (row[2],row[3])
            else:
                copiaAero[row[0]] = {}
                copiaAero[row[0]][row[1]] = (row[2],row[3])

    with open(archivoVuelos, "r") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            agregar_vertice(grafoTiempos,row[0])
            agregar_vertice(grafoTiempos,row[1])
            agregar_vertice(grafoPrecios,row[0])
            agregar_vertice(grafoPrecios,row[1])
            copiaVuelos.append(row)

    with open(archivoVuelos, "r") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            agregar_arista(grafoTiempos,row[0],row[1],int(row[2]))
            agregar_arista(grafoPrecios,row[0],row[1],int(row[3]))

    comando = input("iniico")
    while(len(comando) > 0):
        comando = input("en while")


def Main():
    if len(sys.argv) != 3:
        return False
    # print(sys.argv[2])
    t0 = os.path.isfile(sys.argv[1])
    t1 = os.path.isfile(sys.argv[2])

    if (t0,t1) == (True,True):
        menu(sys.argv[1],sys.argv[2])


Main()
