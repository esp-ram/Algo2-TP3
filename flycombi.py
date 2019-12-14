#!/usr/bin/python3
from grafos import *
from util_grafos import *
import csv
import sys
import os
COMANDOS_DISPONIBLES = ["camino_mas","camino_escalas","pagerank","centralidad","nueva_aerolinea","vacaciones","itinerario","exportar_kml"]
AMORTIGUACION = 0.85
PRECISION = 0.00000000000000005


def formato_flechas(texto):
    for i in range(len(texto)):
        print(texto[i],end = " ")
        if i != len(texto)-1 :
            print("->",end = " ")
    print()


def listar_operaciones():
    for op in COMANDOS_DISPONIBLES:
        print(op)


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
    for salida in aeroOrigen:
        for llegada in aeroDestino:
            resultados.append(camino_dist_minimo(grafo,salida,llegada))

    return min(resultados,key=operator.itemgetter(1))


# REVIEW: verificar si las ciudades existen
def camino_mas(modo,origen,destino,grafoPrecios,grafoTiempos,vuelos):
    if (modo != "barato") and (modo != "rapido"):# or origen not in lista_ciudades or destino not in lista_ciudades:
        return False
    if modo == "barato":
        recorrido = camino_mas_ops(origen,destino,grafoPrecios,vuelos)
    elif modo == "rapido":
        recorrido = camino_mas_ops(origen,destino,grafoTiempos,vuelos)

    formato_flechas(recorrido[0])
    """
    for i in range(len(recorrido[0])):
        print(recorrido[0][i],end = " ")
        if i != len(recorrido[0])-1 :
            print("->",end = " ")
    print()
    """
    return recorrido[0]


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

    formato_flechas(recorrido)
    """
    for i in range(len(recorrido)):
        print(recorrido[i],end = " ")
        if i != len(recorrido)-1 :
            print("->",end = " ")
    print()
    """
    return recorrido


def pagerank_aux(grafo,dict):
    diccionario = dict.copy()
    tamano = len(ver_vertices(grafo))
    for vertice in ver_vertices(grafo):
        total = 0
        for adyacente in ver_adyacentes(grafo,vertice):
            total += (diccionario[adyacente] / (len(ver_adyacentes(grafo,adyacente))))
        diccionario[vertice] = ((1-AMORTIGUACION)/tamano) + (AMORTIGUACION)*total
    return diccionario


def pagerank(grafo,k):
    if (k.isdigit() == False) and int(k) <= 0:
        return False
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
            if abs(listaParciales[i][vertice] - listaParciales[i-1][vertice]) < PRECISION:
                completado = True
            else:
                completado = False

    resultado = []
    dicc = listaParciales[len(listaParciales)-1]
    for key in dicc:
        resultado.append((key,dicc[key]))

    resultado.sort(key = operator.itemgetter(1),reverse = True)

    # TODO:  formato de print
    limite = min(int(k),len(resultado))


    for i in range(limite):
        print(resultado[i][0],end = "")
        if i != limite-1 :
            print(",",end = " ")
    print()



def N_Lugares(grafo, final, inicio, cantidad, lista, n,resultado):
    if n == cantidad:
        if lista[len(lista)-1] in ver_adyacentes(grafo,final):
            pap = lista.copy()
            resultado.append(pap)
            return lista
        return False

    for vertex in ver_adyacentes(grafo,inicio):
        if len(resultado) != 0:
            return
        if vertex in lista:
            continue
        lista.append(vertex)
        if N_Lugares(grafo,final,vertex,cantidad,lista,n+1,resultado) != True:
            lista.pop()
            continue


def vacaciones(origen,k,grafo,aeros):
    if (k.isdigit() == False) and int(k) <= 0:
        return False
    aeroOrigen = obtener_aeropuertos(origen.title(),aeros)
    resParciales = []
    resultad = []
    for item in aeroOrigen:
        print(item)
        resParciales.append(item)
        N_Lugares(grafo,item,item,int(k),resParciales,0,resultad)
        if len(resultad) != 0:
            resultad[0].append(item)
            break
        resParciales.pop(0)

    formato_flechas(resultad[0])
    return resultad[0]


def nueva_aerolinea(archivo,grafo,copiaVuelos):
    inicio = "JFK" # TODO: elegir un vertice random
    resultado = prim(grafo,inicio)
    vuelos = []
    for punto in ver_vertices(resultado):
        for vertice in ver_adyacentes(resultado,punto):
            for linea in copiaVuelos:
                if ((linea[0] == punto and linea[1] == vertice) or (linea[1] == punto and linea[0] == vertice)):
                    if linea not in vuelos:
                        vuelos.append(linea)

    with open(archivo,"w") as arch:
        for item in vuelos:
            arch.write("{},{},{},{},{}\n".format(item[0],item[1],item[2],item[3],item[4]))


def itinerario_aux(ciudades,dependencias,grafo,archivoAero):
    orden = crear_grafo()
    for ciudad in ciudades:
        agregar_vertice(orden,ciudad)

    for depende in dependencias:
        agregar_arista_dir(orden,depende[0],depende[1])

    ordenRecorrido = orden_topologico(orden)

    vuelos = []

    for i in range(len(ordenRecorrido)-1):
        lista = []
        airSalida = obtener_aeropuertos(ordenRecorrido[i],archivoAero)
        airLlegada = obtener_aeropuertos(ordenRecorrido[i+1],archivoAero)
        for aeroS in airSalida:
            for aeroL in airLlegada:
                c,d = camino_dist_minimo(grafo,aeroS,aeroL)
                lista.append((c,d))
        vuelos.append(min(lista,key=operator.itemgetter(1)))

    for rec in vuelos:
        formato_flechas(rec[0])


def itinerario(archivo,grafo,archivoAero):
    if (os.path.isfile(archivo) == False):
        return False

    copia = []
    with open(archivo,"r") as datos:
        lector = csv.reader(datos,delimiter = ',')
        for row in lector:
            copia.append(row)

    listaDependencias = []
    for i in range(1,len(copia)):
        listaDependencias.append(copia[i])


    for ciudad in copia[0]:
        print("{},".format(ciudad),end = ' ')
    print()
    itinerario_aux(copia[0],listaDependencias,grafo,archivoAero)


def escritura_ubicacion(aeropuerto,coord,arch):
    arch.write('\t\t<Placemark>\n\t\t\t<name>{}</name>\n\t\t\t<Point>\n\t\t\t\t<coordinates>{}, {}</coordinates>\n\t\t\t</Point>\n\t\t</Placemark>\n\n'.format(aeropuerto,coord[0],coord[1]))

def escritura_traza(coord0,coord1,arch):
    arch.write('\t\t<Placemark>\n\t\t\t<LineString>\n\t\t\t\t<coordinates>{}, {} {}, {}</coordinates>\n\t\t\t</LineString>\n\t\t</Placemark>\n\n'.format(coord0[0],coord0[1],coord1[0],coord1[1]))

def escritura_cierre(arch):
    arch.write('\t</Document>\n</kml>')

def escritura_encabezado(arch):
    arch.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    arch.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n\t<Document>\n')
    arch.write('\t\t<name>KML de ejemplo</name>\n\t\t<description>Un ejemplo introductorio.</description>\n\n')


def escritura_kml(ubicaciones,recorrido,ruta):
    archivo = open(ruta,"w")
    escritura_encabezado(archivo)
    for key in ubicaciones.keys():
        escritura_ubicacion(key,ubicaciones[key],archivo)

    for i in range(len(recorrido)-1):
        escritura_traza(ubicaciones[recorrido[i]],ubicaciones[recorrido[i+1]],archivo)

    escritura_cierre(archivo)

    archivo.close()

def exportar_kml(archivo,last,aeropuertos):
    coordenadas = {}
    for item in last:
        for ciudad in aeropuertos.keys():
            if item in aeropuertos[ciudad].keys():
                coordenadas[item] = aeropuertos[ciudad][item]

    escritura_kml(coordenadas,last,archivo)


# TODO: formato print
def centralidad_B(n,grafo):
    centro = centralidad(grafo)
    lista = []
    for key in centro:
        lista.append((key,centro[key]))

    lista.sort(key=operator.itemgetter(1),reverse=True)
    limite = min(len(lista),n)
    for i in range(limite):
        print(lista[i])



def menu(archivoAero,archivoVuelos):
    grafoTiempos = crear_grafo()
    grafoPrecios = crear_grafo()
    grafoFrecuencias = crear_grafo()
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
            agregar_vertice(grafoFrecuencias,row[0])
            agregar_vertice(grafoFrecuencias,row[1])
            copiaVuelos.append(row)

    with open(archivoVuelos, "r") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            agregar_arista(grafoTiempos,row[0],row[1],int(row[2]))
            agregar_arista(grafoPrecios,row[0],row[1],int(row[3]))
            agregar_arista(grafoFrecuencias,row[0],row[1],1/int(row[4]))


    # itinerario("itinerario_ejemplo.csv",grafoTiempos,copiaAero)
    # print(copiaAero)
    # centralidad_B(5,grafoFrecuencias)
    # exportar_kml("kmtest.txt",["SAN","ABQ","HOU","AUS","LAX","BNA","SAN"],copiaAero)
    entrada = input()
    # entrada = ""
    ultimaRespuesta = []
    while(len(entrada) > 0):
        try:
            comando,opciones = entrada.split(" ",1)
        except Exception as e:
            print("ERROR")
        else:
            # print(comando)
            opciones = opciones.split(",")

            if len(opciones) == 3 and comando == "camino_mas":
                print("entra a camino_mas")
                resp = camino_mas(opciones[0],opciones[1],opciones[2],grafoPrecios,grafoTiempos,copiaAero)
                if len(ultimaRespuesta) != 0:
                    ultimaRespuesta.pop()
                ultimaRespuesta.append(resp)
            elif len(opciones) == 2 and comando == "camino_escalas":
                print("entra a camino_escalas")
                resp = camino_escalas(opciones[0],opciones[1],grafoPrecios,copiaAero)
                if len(ultimaRespuesta) != 0:
                    ultimaRespuesta.pop()
                ultimaRespuesta.append(resp)
            elif len(opciones) == 1 and comando == "pagerank":
                print("entra a pagerank")
                pagerank(grafoPrecios,opciones[0])
            elif len(opciones) == 2 and comando == "vacaciones":
                print("entra a vacaciones")
                resp = vacaciones(opciones[0],opciones[1],grafoPrecios,copiaAero)
                if len(ultimaRespuesta) != 0:
                    ultimaRespuesta.pop()
                ultimaRespuesta.append(resp)
            elif len(opciones) == 1 and comando == "nueva_aerolinea":
                print("entra a nueva_aerolinea")
                nueva_aerolinea(opciones[0],grafoPrecios,copiaVuelos)
            elif len(opciones) == 1 and comando == "itinerario":
                print("entra a itinerario")
                itinerario(opciones[0],grafoPrecios,copiaAero)
            elif len(opciones) == 1 and comando == "exportar_kml":
                print("entra a kml")
                if len(ultimaRespuesta != 0):
                    exportar_kml(opciones[0],ultimaRespuesta)
            elif len(opciones) == 1 and comando == "centralidad":
                print("entra a centralidad")
                centralidad_B(int(opciones[0]),grafoFrecuencias)
            else:
                print("opcion mala")
        # print(capitalize(opciones[1]))
        # print(opciones)
        entrada = input()



def Main():
    if len(sys.argv) != 3:
        return False
    # print(sys.argv[2])
    t0 = os.path.isfile(sys.argv[1])
    t1 = os.path.isfile(sys.argv[2])

    if (t0,t1) == (True,True):
        menu(sys.argv[1],sys.argv[2])


Main()
