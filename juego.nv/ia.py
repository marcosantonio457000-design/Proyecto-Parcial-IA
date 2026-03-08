import math
import heapq
import time
import random
from configuracion import *



class NodoBT:
    def ejecutar(self):
        pass


class Selector(NodoBT):
    def __init__(self, hijos):
        self.hijos = hijos

    def ejecutar(self):
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False


class Sequence(NodoBT):
    def __init__(self, hijos):
        self.hijos = hijos

    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True


class CondicionJugadorCerca(NodoBT):
    def __init__(self, enemigo, jugador, rango=10):
        self.enemigo = enemigo
        self.jugador = jugador
        self.rango = rango

    def ejecutar(self):
        distancia = math.dist(
            (self.enemigo.x, self.enemigo.y),
            (self.jugador.x, self.jugador.y)
        )
        return distancia < self.rango


class AccionPerseguir(NodoBT):
    def __init__(self, enemigo, jugador, mapa):
        self.enemigo = enemigo
        self.jugador = jugador
        self.mapa = mapa 

    def ejecutar(self):
        estado_inicial = Estado(self.enemigo.x, self.enemigo.y)
        estado_objetivo = Estado(self.jugador.x, self.jugador.y)

        camino, _, _ = Astar(estado_inicial, estado_objetivo, self.mapa)

        if len(camino) > 1:
            siguiente = camino[1]
            self.enemigo.x = siguiente.x
            self.enemigo.y = siguiente.y
            return True

        return False


class AccionPatrullar(NodoBT):
    def __init__(self, enemigo, mapa):
        self.enemigo = enemigo
        self.mapa = mapa

    def ejecutar(self):
        vecinos = [
            (self.enemigo.x+1, self.enemigo.y),
            (self.enemigo.x-1, self.enemigo.y),
            (self.enemigo.x, self.enemigo.y+1),
            (self.enemigo.x, self.enemigo.y-1)
        ]

        vecinos_validos = [
            v for v in vecinos
            if 0 <= v[0] < COLUMNAS and
               0 <= v[1] < FILAS and
               self.mapa[v[1]][v[0]] == 0

        ]

        if vecinos_validos:
            nx, ny = random.choice(vecinos_validos)
            self.enemigo.x = nx
            self.enemigo.y = ny
            return True

        return False
    
    # ---------------- A* ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
class Estado:
     def __init__(self, x, y):
        self.x = x
        self.y = y
        
     def Costo(self, estado_final):
        return math.dist((self.x, self.y), (estado_final.x, estado_final.y))

     def GenerarSucesores(self, mapa):
        sucesores = []
        movimientos = [(1,0),(-1,0),(0,1),(0,-1)]

        for dx, dy in movimientos:
            nx = self.x + dx
            ny = self.y + dy

            if 0 <= nx < COLUMNAS and 0 <= ny < FILAS:
                if mapa[ny][nx] == 0:
                   sucesores.append(Estado(nx, ny))

        return sucesores


     def __eq__(self, other):
        return isinstance(other, Estado) and self.x == other.x and self.y == other.y

     def __hash__(self):
        return hash((self.x, self.y))
class Nodo:
    def __init__(self, dato, padre, costo):
        self.dato = dato
        self.padre = padre
        self.costo = costo

    def __lt__(self, other):
        return self.costo < other.costo

    def __eq__(self, other):
        return isinstance(other, Nodo) and self.dato == other.dato

    def __hash__(self):
        return hash(self.dato)


def Astar(estado_inicial, estado_final, mapa):
    totalnodos = 1
    nodoactual = Nodo(estado_inicial, None,
                      estado_inicial.Costo(estado_final))
    nodosgenerado = []

    nodosvisitados = set()
    heapq.heapify(nodosgenerado)

    inicio = time.perf_counter()

    while nodoactual.dato != estado_final:
        sucesores = nodoactual.dato.GenerarSucesores(mapa)

        totalnodos += len(sucesores)

        for sucesor in sucesores:
            temp = Nodo(sucesor, nodoactual,
                        sucesor.Costo(estado_final))

            if temp not in nodosvisitados:
                heapq.heappush(nodosgenerado, temp)

        nodosvisitados.add(nodoactual)

        if not nodosgenerado:
            return [], totalnodos, 0

        while nodosgenerado and nodoactual in nodosvisitados:
                nodoactual = heapq.heappop(nodosgenerado)

        if not nodosgenerado and nodoactual in nodosvisitados:
            return [], totalnodos, 0

    camino = []
    while nodoactual:
        camino.append(nodoactual.dato)
        nodoactual = nodoactual.padre

    camino.reverse()
    fin = time.perf_counter()

    return camino, totalnodos, fin - inicio
