import pygame

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

pygame.init()

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

    

    # ---------------- FONDO y SPRITE DE TARJETA -----------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
try:
    FONDO = pygame.image.load("assets/suelo.png").convert()
    FONDO = pygame.transform.scale(FONDO, (ANCHO, ALTO))
except Exception as e:
    print("Error cargando fondo:", e)
    FONDO = None

try:
      SPRITE_TARJETA = pygame.image.load("assets/tarjeta.png").convert_alpha()
      SPRITE_TARJETA = pygame.transform.scale(
        SPRITE_TARJETA, (TAM_CELDA, TAM_CELDA)
    )
except Exception as e:
    print("Error cargando sprite tarjeta:", e)
    SPRITE_TARJETA = None

    # ---------------- SPRITE PUERTA -----------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
try:
    tamano_puerta = TAM_CELDA + 50 

    SPRITE_PUERTA = pygame.image.load("assets/puerta.png").convert_alpha()
    SPRITE_PUERTA = pygame.transform.scale(
        SPRITE_PUERTA, (tamano_puerta, tamano_puerta)
    )
except Exception as e:
    print("Error cargando sprite puerta:", e)
    SPRITE_PUERTA = None

    # ---------------- SPRITE DE COMPUTADORA -----------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
try:
    SPRITE_COMPUTADORA = pygame.image.load("assets/computadora.png").convert_alpha()
    SPRITE_COMPUTADORA = pygame.transform.scale(SPRITE_COMPUTADORA, (int(TAM_CELDA*2), int(TAM_CELDA*2)))
except Exception as e:
    print("Error cargando sprite computadora:", e)
    SPRITE_COMPUTADORA = None
