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
    # print(key)
    for k1 in p[key]:
        # print(k1)
        # print(p[key][k1])
        total += p[key][k1]
###




def recorrida(grafo, lista, inicio, longMaximo, longActual,resultado):
    if longActual > longMaximo[len(longMaximo)-1]:
        return False


    completo = True
    for item in ver_vertices(grafo):
        if item not in lista:
            completo = False


    if completo == True:
        print("cumple",lista,"long",longActual)
        # print("respuesta")
        pap = lista.copy()
        # print("pap:",pap)
        longMaximo.append(longActual)
        resultado.append(pap)
        return

    for vertice in ver_adyacentes(grafo,inicio):
        lista.append(vertice)
        # print("agrego vertice",vertice,"adyacente de",inicio)
        if recorrida(grafo,lista,vertice,longMaximo,longActual+obtener_peso(grafo,inicio,vertice),resultado) != True:
            lista.pop()
            continue
        longMaximo = longActual+obtener_peso(grafo,inicio,vertice)
        # lista.append(vertice)

    return
# r=0



lista = []
respuesta = []
largos = []
lista.append("BAT")
largos.append(total*2)
recorrida(tiempos,lista,"BAT",largos,0,respuesta)
# print(respuesta)
# print(largos)

print("Mejor ruta: {}, Costo: {}".format(respuesta[len(respuesta)-1],largos[len(largos)-1]))

"""
for i in range(len(respuesta)):
    print("ruta: {} , costo: {}".format(respuesta[i],largos[i+1]))
"""

"""
BAT -> LAN -> ASH -> BH6 -> NAR -> ATL -> JFK -> ATL -> SHE -> RIV -> WAC
Costo: 2644
"""
