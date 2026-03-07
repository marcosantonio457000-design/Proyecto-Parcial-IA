import math
import pygame
from configuracion import *

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
        pygame.draw.rect(PANTALLA, AMARILLO, self.rect)
