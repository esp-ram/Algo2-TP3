# import csv

def crear_grafo():
    return {}


def agregar_vertice(grafo,vertice):
    grafo[vertice] = {}


def borrar_vertice(grafo,vertice):
    try:
        grafo.pop(vertice)
        for key in grafo:
            if vertice in grafo[key]:
                grafo[key].pop(vertice)
    except:
        return false


def ver_vertices(grafo):
    return list(grafo.keys())


def ver_adyacentes(grafo,vertice):
    try:
        return list(grafo[vertice].keys())
    except:
        return False

# REVIEW: probalemente no hace falta el try junto con el if
def agregar_arista(grafo,vert1,vert2,peso=0):
    if(vert1 and vert2 in grafo):
        try:
            grafo[vert1][vert2] = peso
            grafo[vert2][vert1] = peso
        except:
            return False


def agregar_arista_dir(grafo,vert1,vert2,peso=0):
    if(vert1 and vert2 in grafo):
        try:
            grafo[vert1][vert2] = peso
        except:
            return False


def remover_arista(grafo,vert1,vert2):
    try:
        grafo[vert1].pop(vert2)
        grafo[vert2].pop(vert1)
    except:
        return False


def obtener_peso(grafo,vert1,vert2):
    try:
        return grafo[vert1][vert2]
    except:
        return False

# REVIEW: probalemente no hace falta el try junto con el if
def cambiar_peso(grafo,vert1,vert2,peso):
    if(vert1 and vert2 in grafo):
        try:
            grafo[vert1][vert2] = peso
            grafo[vert2][vert1] = peso
        except:
            return False




##### TESTS ####
"""
f = crear_grafo()
agregar_vertice(f,"vertex1")
agregar_vertice(f,"vertex2")
agregar_vertice(f,"vertex3")
agregar_vertice(f,"vertex4")
agregar_vertice(f,"vertex5")
agregar_vertice(f,"vertex6")

agregar_arista(f,"vertex1","vertex2")
agregar_arista(f,"vertex3","vertex5",54)
agregar_arista(f,"vertex1","vertex4",212)
agregar_arista(f,"vertex5","vertex6",12)
agregar_arista(f,"vertex4","vertex21",34)
print(obtener_peso(f,"vertex3","vertex5"))
cambiar_peso(f,"vertex3","vertex5",7)
print(obtener_peso(f,"vertex3","vertex5"))
agregar_arista(f,"vertex1","vertex6",12)

print(ver_adyacentes(f,"vertex1"))
print(ver_vertices(f))
print(f)
borrar_vertice(f,"vertex1")
print(f)


vuelos = crear_grafo()
tiempo = crear_grafo()

with open('vuelos.csv', "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        agregar_vertice(vuelos,row[0])
        agregar_vertice(vuelos,row[1])
        agregar_vertice(tiempo,row[0])
        agregar_vertice(tiempo,row[1])

with open('vuelos.csv', "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        agregar_arista(vuelos,row[0],row[1],row[3])
        agregar_arista(tiempo,row[0],row[1],row[2])





#print(vuelos)
print((ver_adyacentes(vuelos,"JFK")))
print(obtener_peso(vuelos,"JFK","OAK"))
print((ver_adyacentes(tiempo,"JFK")))
print(obtener_peso(tiempo,"LAS","JAX"))
print(obtener_peso(vuelos,"LAS","JAX"))
"""
