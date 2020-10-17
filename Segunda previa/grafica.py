import pygame
import math

BLANCO = [255,255,255]
VERDE = [0,255,0]
ROJO = [255,0,0]
AZUL = [0,0,255]
AMARILLO = [255,255,0]
NEGRO = [0,0,0]

def Iris(): #devuelve una lista con 3 numeros random para dar un color
    return [random.randrange(255),random.randrange(255),random.randrange(255)]

def Neg(Punto): # da el negativo de un punto
	return [-Punto[0],-Punto[1]]

def Punto(p, pos, cl=BLANCO): #cl seria el color predeterminado si no mando ningun color
    pygame.draw.circle(p, cl, pos, 2)
    pygame.display.flip()

def Cart_plano(punto,origen): #Pasa una coordenada de pantalla a una de plano cartesiano
    xp = punto[0] + origen[0]
    yp = -punto[1] + origen[1]
    return [xp,yp]

def Escalar(punto, multiplicador): #Cambia la posicion del punto respecto al valor que den a multiplicar
    mp = punto[0]*multiplicador[0]
    mp2 = punto[1]*multiplicador[1]
    return [mp,mp2]

def EscalarR(pf, punto): #Lo envia al origen
    xp = punto[0]-pf[0]
    yp = punto[1]-pf[1]
    return[xp,yp]

def EscalarS(pf, punto): #Regreso al punto inicial
    xp = punto[0]+pf[0]
    yp = punto[1]+pf[1]
    return[xp,yp]

def tranformacionInversa(punto, origen): #Lo coloca al otro lado de la pantalla
    nx = punto[0] + origen[0]
    ny = -1*punto[1] + origen[1]
    nuevoPunto = [nx, ny]
    return nuevoPunto

def trianguloPuntos(pantalla, punto1, punto2, punto3): #Dado 3 puntos hace un triangulo
    pygame.draw.line(pantalla,BLANCO,punto1,punto2)
    pygame.draw.line(pantalla,BLANCO,punto2,punto3)
    pygame.draw.line(pantalla,BLANCO,punto1,punto3)
    pygame.display.flip()

def Rotacion(punto,angulo): #Rotacion horaria
    A = math.radians(angulo)
    xp = punto[0]*math.cos(A) - punto[1]*math.sin(A)
    yp = punto[0]*math.sin(A) + punto[1]*math.cos(A)
    return [xp, yp]

def Polar(radio, angulo): #
    xp = radio*math.cos(math.radians(angulo))
    yp = radio*math.sin(math.radians(angulo))
    return [int(xp), int(yp)]
