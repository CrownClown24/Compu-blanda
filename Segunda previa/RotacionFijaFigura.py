import pygame
from grafica import *
ANCHO = 600
ALTO = 400

def Plano(p, origen):
    ox=origen[0]
    oy=origen[1]
    pygame.draw.line(p,BLANCO,[ox,0],[ox,ALTO])
    pygame.draw.line(p,BLANCO,[0,oy],[ANCHO,oy])
    pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    origen=[300,200]
    #Plano(pantalla,origen)
    A = [100,75]
    B = [150,100]
    C = [200,25]
    pf = A
    trianguloPuntos(pantalla, Cart_plano(A, origen), Cart_plano(B, origen), Cart_plano(C, origen))
    ang=0
    fin = False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    ang=5
                    pantalla.fill(NEGRO)
                    B = EscalarR(pf,B)
                    C = EscalarR(pf,C)
                    B = Rotacion(B,ang)
                    C = Rotacion(C,ang)
                    B = EscalarS(pf, B)
                    C = EscalarS(pf, C)
                    trianguloPuntos(pantalla,Cart_plano(A, origen), Cart_plano(B, origen), Cart_plano(C, origen))
                if event.button == 5:
                    ang=-5
                    pantalla.fill(NEGRO)
                    B = EscalarR(pf,B)
                    C = EscalarR(pf,C)
                    B = Rotacion(B,ang)
                    C = Rotacion(C,ang)
                    B = EscalarS(pf, B)
                    C = EscalarS(pf, C)
                    trianguloPuntos(pantalla,Cart_plano(A, origen), Cart_plano(B, origen), Cart_plano(C, origen))
