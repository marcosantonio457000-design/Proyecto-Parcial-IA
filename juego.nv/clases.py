import random

from balas import *
from SPRITES import *
from configuracion import *
from menu import *
from ia import *


# ---------------- CLASES ----------------Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013
class Jugador:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.cooldown = 0
        self.vida = 100
        self.invulnerable = 0

    def mover(self, teclas, mapa):
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
          
class Enemigo:
   
    def __init__(self, x, y, tiene_tarjeta=False, vida=1):
        self.x = x
        self.y = y
        self.vivo = True
        self.tiene_tarjeta = tiene_tarjeta
        self.cooldown = 0
        self.arbol = None
        self.vida = vida
    

    # -------- Construcción del árbol de comportamiento-------- Marcos Antonio Alfonseca Guerrero/Matricula 23-SISN-2-013 
    def construir_arbol(self, jugador, mapa):

        condicion = CondicionJugadorCerca(self, jugador)

        secuencia_perseguir = Sequence([
            condicion,
            AccionPerseguir(self, jugador, mapa)
        ])

        patrullar = AccionPatrullar(self, mapa)

        self.arbol = Selector([
            secuencia_perseguir,
            patrullar
        ])

    
    def actualizar(self, jugador, mapa):

        if not self.vivo:
            return

        if self.cooldown > 0:
            self.cooldown -= 0.01
            return

        # Construye el árbol solo una vez
        if self.arbol is None:
            self.construir_arbol(jugador, mapa)

       
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