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


def cambiar_peso(grafo,vert1,vert2,peso):
    if(vert1 and vert2 in grafo):
        try:
            grafo[vert1][vert2] = peso
            grafo[vert2][vert1] = peso
        except:
            return False
