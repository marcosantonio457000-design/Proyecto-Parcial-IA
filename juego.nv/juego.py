import pygame
import random
import sys
import math
import heapq

pygame.init()

# ---------------- CONFIGURACION----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
ANCHO = 1280
ALTO = 720
TAM_CELDA = 45

COLUMNAS = ANCHO // TAM_CELDA
FILAS = ALTO // TAM_CELDA

PANTALLA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
ANCHO, ALTO = PANTALLA.get_size()

COLUMNAS = ANCHO // TAM_CELDA
FILAS = ALTO // TAM_CELDA

pygame.display.set_caption("Laboratorio Completo")

RELOJ = pygame.time.Clock()

# ---------------- SPRITE JUGADOR ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
try:
    SPRITE_JUGADOR = pygame.image.load("assets/jugador.png").convert_alpha()
    SPRITE_JUGADOR = pygame.transform.scale(
        SPRITE_JUGADOR, (TAM_CELDA, TAM_CELDA)
    )
except Exception as e:
    print("ERROR cargando sprite del jugador:", e)
    SPRITE_JUGADOR = None

# ---------------- SPRITE ENEMIGO ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
try:
    SPRITE_ENEMIGO = pygame.image.load("assets/enemigo.png").convert_alpha()
    SPRITE_ENEMIGO = pygame.transform.scale(
        SPRITE_ENEMIGO, (TAM_CELDA + 30, TAM_CELDA + 30)
    )
except Exception as e:
    print("Error cargando sprite enemigo:", e)
    SPRITE_ENEMIGO = None
# ----------------Colores-------------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
NEGRO = (20, 20, 20)
AZUL = (50, 150, 255)
ROJO = (200, 50, 50)
GRIS = (100, 100, 100)
BLANCO = (230, 230, 230)
VERDE = (50, 200, 50)
AMARILLO = (255, 255, 0)
fuente = pygame.font.SysFont("arial", 40)

def dibujar_texto(texto, x, y):
    render = fuente.render(texto, True, BLANCO)
    PANTALLA.blit(render, (x, y))
# ---------------- VARIABLES ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
numero_sala = 1
jugador_tiene_tarjeta = False
mapa = []
enemigos = []
balas = []
puerta = None
computadora = None
tarjeta = None

# ---------------- MAPA ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
def generar_mapa():
    global mapa
    mapa = []
    for y in range(FILAS):
        fila = []
        for x in range(COLUMNAS):
            if random.random() < 0.07:  
                fila.append(1)
            else:
                fila.append(0)
        mapa.append(fila)

def dibujar_mapa():
    for y in range(FILAS):
        for x in range(COLUMNAS):
            if mapa[y][x] == 1:
                pygame.draw.rect(PANTALLA, GRIS,
                    (x*TAM_CELDA, y*TAM_CELDA, TAM_CELDA, TAM_CELDA))

# ---------------- A* ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
import heapq
import time
import math

class Estado:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def Costo(self, estado_final):
        return math.dist((self.x, self.y), (estado_final.x, estado_final.y))

    def GenerarSucesores(self):
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


def Astar(estado_inicial, estado_final):
    totalnodos = 1
    nodoactual = Nodo(estado_inicial, None,
                      estado_inicial.Costo(estado_final))
    nodosgenerado = []

    nodosvisitados = set()
    heapq.heapify(nodosgenerado)

    inicio = time.perf_counter()

    while nodoactual.dato != estado_final:
        sucesores = nodoactual.dato.GenerarSucesores()

        totalnodos += len(sucesores)

        for sucesor in sucesores:
            temp = Nodo(sucesor, nodoactual,
                        sucesor.Costo(estado_final))

            if temp not in nodosvisitados:
                heapq.heappush(nodosgenerado, temp)

        nodosvisitados.add(nodoactual)

        if not nodosgenerado:
            return [], totalnodos, 0

        while nodoactual in nodosvisitados:
            nodoactual = heapq.heappop(nodosgenerado)

    camino = []
    while nodoactual:
        camino.append(nodoactual.dato)
        nodoactual = nodoactual.padre

    camino.reverse()
    fin = time.perf_counter()

    return camino, totalnodos, fin - inicio

# ---------------- CLASES ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
class Jugador:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.cooldown = 0
        self.vida = 100
        self.invulnerable = 0
    def mover(self, teclas):
        if self.cooldown > 0:
            self.cooldown -= 0.7
            return

        dx, dy = 0, 0
        if teclas[pygame.K_w]: dy = -1
        if teclas[pygame.K_s]: dy = 1
        if teclas[pygame.K_a]: dx = -1
        if teclas[pygame.K_d]: dx = 1

        nx = self.x + dx
        ny = self.y + dy

        if 0 <= nx < COLUMNAS and 0 <= ny < FILAS:
            if mapa[ny][nx] == 0:
                self.x = nx
                self.y = ny
                self.cooldown = 4

    def dibujar(self):
       if SPRITE_JUGADOR:
        PANTALLA.blit(
            SPRITE_JUGADOR,
            (self.x * TAM_CELDA, self.y * TAM_CELDA)
        )
       else: 
          pygame.draw.rect(
            PANTALLA,
            AZUL,
            (self.x * TAM_CELDA, self.y * TAM_CELDA, TAM_CELDA, TAM_CELDA)
        )
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
    def __init__(self, enemigo, jugador, rango=6):
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
    def __init__(self, enemigo, jugador):
        self.enemigo = enemigo
        self.jugador = jugador

    def ejecutar(self):
        estado_inicio = Estado(self.enemigo.x, self.enemigo.y)
        estado_objetivo = Estado(self.jugador.x, self.jugador.y)

        camino, _, _ = Astar(estado_inicio, estado_objetivo)

        if len(camino) > 1:
            siguiente = camino[1]
            self.enemigo.x = siguiente.x
            self.enemigo.y = siguiente.y
            return True

        return False


class AccionPatrullar(NodoBT):
    def __init__(self, enemigo):
        self.enemigo = enemigo

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
               mapa[v[1]][v[0]] == 0
        ]

        if vecinos_validos:
            nx, ny = random.choice(vecinos_validos)
            self.enemigo.x = nx
            self.enemigo.y = ny
            return True

        return False
class Enemigo:
   
    def __init__(self, x, y, tiene_tarjeta=False, vida=1):
        self.x = x
        self.y = y
        self.vivo = True
        self.tiene_tarjeta = tiene_tarjeta
        self.cooldown = 0
        self.arbol = None
        self.vida = vida
    

    # -------- Construcción del árbol -------- Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013 
    def construir_arbol(self, jugador):

        condicion = CondicionJugadorCerca(self, jugador)

        secuencia_perseguir = Sequence([
            condicion,
            AccionPerseguir(self, jugador)
        ])

        patrullar = AccionPatrullar(self)

        self.arbol = Selector([
            secuencia_perseguir,
            patrullar
        ])

    
    def actualizar(self, jugador):

        if not self.vivo:
            return

        if self.cooldown > 0:
            self.cooldown -= 0.01
            return

        # Construye el árbol solo una vez
        if self.arbol is None:
            self.construir_arbol(jugador)

       
        self.arbol.ejecutar()

        
        self.cooldown = 0.1

    def dibujar(self):
        if not self.vivo:
            return

        tamano = TAM_CELDA + 30

        x_pix = self.x * TAM_CELDA - (tamano - TAM_CELDA) // 2
        y_pix = self.y * TAM_CELDA - (tamano - TAM_CELDA) // 2

        if SPRITE_ENEMIGO:
            PANTALLA.blit(SPRITE_ENEMIGO, (x_pix, y_pix))
        else:
            pygame.draw.rect(
                PANTALLA,
                ROJO,
                (self.x * TAM_CELDA,
                 self.y * TAM_CELDA,
                 TAM_CELDA,
                 TAM_CELDA)
            )

class Bala:
    def __init__(self, inicio, destino):
        self.x = inicio[0]
        self.y = inicio[1]
        self.vel = 10

        dx = destino[0] - self.x
        dy = destino[1] - self.y
        dist = math.hypot(dx, dy)

        self.dir_x = dx / dist
        self.dir_y = dy / dist

        self.rect = pygame.Rect(self.x, self.y, 6, 6)

    def mover(self):
        self.x += self.dir_x * self.vel
        self.y += self.dir_y * self.vel
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def dibujar(self):
        pygame.draw.rect(PANTALLA, BLANCO, self.rect)

# ---------------- GENERAR SALAS ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
def generar_puerta():
    global puerta
    pared = random.choice(["arriba", "abajo", "izquierda", "derecha"])

    if pared == "arriba":
        puerta = (random.randint(1, COLUMNAS-2), 0)
    elif pared == "abajo":
        puerta = (random.randint(1, COLUMNAS-2), FILAS-1)
    elif pared == "izquierda":
        puerta = (0, random.randint(1, FILAS-2))
    else:
        puerta = (COLUMNAS-1, random.randint(1, FILAS-2))

def generar_sala():
    global enemigos, tarjeta, computadora

    generar_mapa()
    enemigos = []
    tarjeta = None
    computadora = None

    cantidad = random.randint(2, 4)

    for _ in range(cantidad):
        while True:
            x = random.randint(1, COLUMNAS-2)
            y = random.randint(1, FILAS-2)
            if mapa[y][x] == 0:
                break
        enemigos.append(Enemigo(x, y))

    if numero_sala == 3 and enemigos:
        elegido = random.choice(enemigos)
        elegido.tiene_tarjeta = True

    generar_puerta()

def generar_sala_final():
    global enemigos, computadora, puerta
    generar_mapa()
    enemigos = []
    puerta = None
    computadora = (COLUMNAS//2, FILAS//2)
# ---------------- MENU ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
def menu_inicial():
    esperando = True

    titulo_fuente = pygame.font.SysFont("arial", 70)
    texto_fuente = pygame.font.SysFont("arial", 35) 
    while esperando:
        RELOJ.tick(60)
        PANTALLA.fill((10, 10, 10))

        titulo = titulo_fuente.render("ESCAPA DEL LABORATORIO", True, BLANCO)
        texto = texto_fuente.render("Presiona ENTER para jugar", True, BLANCO)

        PANTALLA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 200))
        PANTALLA.blit(texto, (ANCHO//2 - texto.get_width()//2, 320))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
# ---------------- INICIO ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
jugador = Jugador()
generar_sala()
menu_inicial()
#----------------- BARRA DE VIDA ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
def dibujar_barra_vida(jugador):
    ancho_barra = 300
    alto_barra = 25
    x = 20
    y = 20

    # Fondo
    pygame.draw.rect(PANTALLA, (80, 0, 0), (x, y, ancho_barra, alto_barra))

    # Vida actual
    vida_actual = (jugador.vida / 100) * ancho_barra
    pygame.draw.rect(PANTALLA, (0, 200, 0), (x, y, vida_actual, alto_barra))

    # Borde
    pygame.draw.rect(PANTALLA, BLANCO, (x, y, ancho_barra, alto_barra), 2)
# ---------------- LOOP  ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
while True:

    RELOJ.tick(60)
    PANTALLA.fill(NEGRO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            jugador_pix = (jugador.x*TAM_CELDA + TAM_CELDA//2,
                           jugador.y*TAM_CELDA + TAM_CELDA//2)
            balas.append(Bala(jugador_pix, mouse_pos))

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e and computadora:
                if (jugador.x, jugador.y) == computadora:
                    if jugador_tiene_tarjeta:
                        for e in enemigos:
                            e.vivo = False
                        print("ROBOTS DESACTIVADOS")
                    else:
                        print("NECESITAS LA TARJETA")

    teclas = pygame.key.get_pressed()
    jugador.mover(teclas)

    # ------------Cambio de sala------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
    if puerta and (jugador.x, jugador.y) == puerta:
        numero_sala += 1
        jugador.x, jugador.y = 1, 1
        if numero_sala < 7:
            generar_sala()
        else:
            generar_sala_final()

    # -------------Actualizar enemigos---------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
    for e in enemigos:
     e.actualizar(jugador)

    # Daño por contacto
    if jugador.invulnerable > 0:
        jugador.invulnerable -= 1

    for e in enemigos:
        if e.vivo and e.x == jugador.x and e.y == jugador.y:
            if jugador.invulnerable <= 0:
                jugador.vida -= 5
                jugador.invulnerable = 30
    # --------------Mover balas---------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
    for bala in balas[:]:
        bala.mover()

        if bala.x < 0 or bala.x > ANCHO or bala.y < 0 or bala.y > ALTO:
            balas.remove(bala)
            continue

        for e in enemigos:
            if e.vivo:
                rect_e = pygame.Rect(e.x*TAM_CELDA, e.y*TAM_CELDA,
                                     TAM_CELDA, TAM_CELDA)
                if bala.rect.colliderect(rect_e):
                    e.vivo = False
                    if e.tiene_tarjeta:
                        tarjeta = (e.x, e.y)
                    if bala in balas:
                        balas.remove(bala)

    # --------------Recoger tarjeta----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
    if tarjeta and (jugador.x, jugador.y) == tarjeta:
        jugador_tiene_tarjeta = True
        tarjeta = None
        print("TARJETA OBTENIDA")
    # --------------Dibujar-------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
    dibujar_mapa()

    if puerta:
        pygame.draw.rect(PANTALLA, VERDE,
            (puerta[0]*TAM_CELDA, puerta[1]*TAM_CELDA,
             TAM_CELDA, TAM_CELDA))

    if tarjeta:
        pygame.draw.rect(PANTALLA, AMARILLO,
            (tarjeta[0]*TAM_CELDA, tarjeta[1]*TAM_CELDA,
             TAM_CELDA, TAM_CELDA))

    if computadora:
        pygame.draw.rect(PANTALLA, (150,150,255),
            (computadora[0]*TAM_CELDA, computadora[1]*TAM_CELDA,
             TAM_CELDA, TAM_CELDA))

    jugador.dibujar()

    for e in enemigos:
        e.dibujar()

    for bala in balas:
        bala.dibujar()
    dibujar_barra_vida(jugador)
    pygame.display.flip()