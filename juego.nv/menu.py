import pygame
import sys
from configuracion import *

def menu_inicial():

    esperando = True

    titulo_fuente = pygame.font.SysFont("arial",70)
    texto_fuente = pygame.font.SysFont("arial",35)

    while esperando:

        RELOJ.tick(60)
        PANTALLA.fill((10,10,10))

        titulo = titulo_fuente.render("ESCAPA DEL LABORATORIO",True,BLANCO)
        texto = texto_fuente.render("Presiona ENTER para jugar",True,BLANCO)

        PANTALLA.blit(titulo,(ANCHO//2 - titulo.get_width()//2,200))
        PANTALLA.blit(texto,(ANCHO//2 - texto.get_width()//2,320))

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