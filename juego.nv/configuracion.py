import pygame

pygame.init()

ANCHO = 1280
ALTO = 720
TAM_CELDA = 45

PANTALLA = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
ANCHO, ALTO = PANTALLA.get_size()

COLUMNAS = ANCHO // TAM_CELDA
FILAS = ALTO // TAM_CELDA

RELOJ = pygame.time.Clock()

pygame.display.set_caption("Laboratorio Completo")

NEGRO = (20,20,20)
AZUL = (50,150,255)
ROJO = (200,50,50)
GRIS = (100,100,100)
BLANCO = (230,230,230)
VERDE = (50,200,50)
AMARILLO = (255,255,0)