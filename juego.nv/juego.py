import pygame
import random
import sys

from configuracion import *
from SPRITES import *
from menu import *
from balas import *
from clases import *
from ia import *
pygame.init()

pygame.mixer.music.load("assets/musica.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  #Reproducir en bucle

#----------------- CONTROL (JOYSTICK) ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
pygame.joystick.init()
joystick = None

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Control conectado:", joystick.get_name())
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
mensaje_tarjeta = False
tiempo_mensaje = 0
mensaje_robots = False
tiempo_mensaje_robots = 0
mensaje_tarjeta_falta = False
tiempo_mensaje_tarjeta_falta = 0
mostrar_menu_final = False
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

    # Vida 
    vida_actual = (jugador.vida / 100) * ancho_barra
    pygame.draw.rect(PANTALLA, (0, 200, 0), (x, y, vida_actual, alto_barra))

    # Borde
    pygame.draw.rect(PANTALLA, BLANCO, (x, y, ancho_barra, alto_barra), 2)
# ---------------- LOOP  ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
while True:

    RELOJ.tick(60)
    if FONDO:
      PANTALLA.blit(FONDO, (0, 0))
    else:
     PANTALLA.fill(NEGRO)
      
    boton_menu = pygame.Rect(ANCHO//2 - 150, ALTO//2 - 40, 300, 60)
    boton_salir = pygame.Rect(ANCHO//2 - 150, ALTO//2 + 40, 300, 60)
     
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()

                if mostrar_menu_final:

                    if boton_menu.collidepoint(mouse_pos):
                       estado = "menu"

                    if boton_salir.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

                else:
                    jugador_pix = (
                        jugador.x*TAM_CELDA + TAM_CELDA/2,
                        jugador.y*TAM_CELDA + TAM_CELDA/2
                    )

                    balas.append(Bala(jugador_pix, mouse_pos))

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e and computadora:
                if (jugador.x, jugador.y) == computadora:

                    if jugador.tiene_tarjeta:
                        for e in enemigos:
                         e.vivo = False

                        mensaje_robots = True
                        tiempo_mensaje_robots = pygame.time.get_ticks()
                        mostrar_menu_final = True

                    else:
                        mensaje_tarjeta_falta = True
                        tiempo_mensaje_tarjeta_falta = pygame.time.get_ticks()

        if evento.type == pygame.JOYBUTTONDOWN:
            if evento.button == 0:  # botón 1 del joystick

                mouse_pos = pygame.mouse.get_pos()

                jugador_pix = (
                    jugador.x*TAM_CELDA + TAM_CELDA/2,
                    jugador.y*TAM_CELDA + TAM_CELDA/2
                    )

                balas.append(Bala(jugador_pix, mouse_pos))

        if evento.type == pygame.JOYBUTTONDOWN:
            if evento.button == 1:

                if computadora:
                    if abs(jugador.x - computadora[0]) <= 1 and abs(jugador.y - computadora[1]) <= 1:

                        if jugador.tiene_tarjeta:
                            for e in enemigos:
                                e.vivo = False

                            mensaje_robots = True
                            tiempo_mensaje_robots = pygame.time.get_ticks()
                            mostrar_menu_final = True

    teclas = pygame.key.get_pressed()
    jugador.mover(teclas, mapa)

    if joystick:
        eje_x = joystick.get_axis(0)
        eje_y = joystick.get_axis(1)

        dx = 0
        dy = 0

        if eje_x > 0.5:
            dx = 1
        elif eje_x < -0.5:
            dx = -1

        if eje_y > 0.5:
            dy = 1
        elif eje_y < -0.5:
            dy = -1

        nx = jugador.x + dx
        ny = jugador.y + dy

    if 0 <= nx < COLUMNAS and 0 <= ny < FILAS:
        if mapa[ny][nx] == 0:
            jugador.x = nx
            jugador.y = ny

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
     e.actualizar(jugador, mapa)

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
        jugador.tiene_tarjeta = True
        tarjeta = None
        mensaje_tarjeta = True
        tiempo_mensaje = pygame.time.get_ticks()
    # --------------Dibujar-------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
    dibujar_mapa()

    if puerta:
        tamano_puerta = TAM_CELDA + 50

        x_pix = puerta[0] * TAM_CELDA - (tamano_puerta - TAM_CELDA) // 2
        y_pix = puerta[1] * TAM_CELDA - (tamano_puerta - TAM_CELDA) // 2

    if SPRITE_PUERTA:
        PANTALLA.blit(SPRITE_PUERTA, (x_pix, y_pix))
    else:
        pygame.draw.rect(
            PANTALLA,
            VERDE,
            (x_pix, y_pix, TAM_CELDA, TAM_CELDA)
        )

    if tarjeta:
       x_pix = tarjeta[0] * TAM_CELDA
       y_pix = tarjeta[1] * TAM_CELDA

       if SPRITE_TARJETA:
        PANTALLA.blit(SPRITE_TARJETA, (x_pix, y_pix))
       else:
        pygame.draw.rect(
            PANTALLA,
            AMARILLO,
            (x_pix, y_pix, TAM_CELDA, TAM_CELDA)
        )

    if computadora:
        x = computadora[0]*TAM_CELDA
        y = computadora[1]*TAM_CELDA

        PANTALLA.blit(SPRITE_COMPUTADORA, (x, y))

        if abs(jugador.x - computadora[0]) <= 1 and abs(jugador.y - computadora[1]) <= 1:
            texto = fuente.render("Presiona E para usar", True, BLANCO)
            PANTALLA.blit(texto, (x-40, y-20))

    jugador.dibujar()

    for e in enemigos:
        e.dibujar()

    for bala in balas:
        bala.dibujar()
    dibujar_barra_vida(jugador)

    if mensaje_tarjeta:
        texto = fuente.render("TARJETA OBTENIDA", True, AMARILLO)
        rect = texto.get_rect(center=(ANCHO//2, 50))
        PANTALLA.blit(texto, rect)

    if pygame.time.get_ticks() - tiempo_mensaje > 3000:
        mensaje_tarjeta = False

        if mensaje_robots:
            texto = fuente.render("LOS ROBOTS HAN SIDO DESACTIVADOS", True, VERDE)
            rect = texto.get_rect(center=(ANCHO//2, 80))
            PANTALLA.blit(texto, rect)

            if pygame.time.get_ticks() - tiempo_mensaje_robots > 3000:
               mensaje_robots = False

        if mensaje_tarjeta_falta:
            texto = fuente.render("NECESITAS LA TARJETA", True, ROJO)
            rect = texto.get_rect(center=(ANCHO//2, 120))
            PANTALLA.blit(texto, rect)

            if pygame.time.get_ticks() - tiempo_mensaje_tarjeta_falta > 3000:
               mensaje_tarjeta_falta = False
    

               if mostrar_menu_final:

                  boton_menu = pygame.Rect(ANCHO//2 - 150, ALTO//2 - 40, 300, 60)
                  boton_salir = pygame.Rect(ANCHO//2 - 150, ALTO//2 + 40, 300, 60)

                  pygame.draw.rect(PANTALLA, VERDE, boton_menu)
                  pygame.draw.rect(PANTALLA, ROJO, boton_salir)

                  texto_menu = fuente.render("VOLVER AL MENU", True, NEGRO)
                  texto_salir = fuente.render("SALIR", True, NEGRO)

                  PANTALLA.blit(texto_menu, texto_menu.get_rect(center=boton_menu.center))
                  PANTALLA.blit(texto_salir, texto_salir.get_rect(center=boton_salir.center))

    pygame.display.flip()