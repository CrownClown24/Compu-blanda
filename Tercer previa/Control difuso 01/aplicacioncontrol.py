# CONTROL DIFUSO

# Steven Medina Gonzalez - 1088354520
# Encontrar la probabilidad de recomendar un juego a mis amigos  
# teniendo en cuenta la jugabilidad y duracion del juego
# Importar librerías
import numpy as np 
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Generar variables del universo
# * Jugabilidad y duracion en rangos subjetivos [0, 10] 
# * La recomendacion tiene un rango de [0, 100] en unidades de puntos porcentuales

x_jugabilidad = np.arange(0, 11, 1) 
x_duracion = np.arange(0, 11, 1) 
x_recomendar = np.arange(0, 101, 1)

# Generar funciones de pertenencia difusas 
jugabilidad_baja = fuzz.trimf(x_jugabilidad, [0, 0, 5]) 
jugabilidad_media = fuzz.trimf(x_jugabilidad, [0, 5, 10])  
jugabilidad_alta = fuzz.trimf(x_jugabilidad, [5, 10, 10]) 
duracion_bajo = fuzz.trimf(x_duracion, [0, 0, 5]) 
duracion_medio = fuzz.trimf(x_duracion, [0, 5, 10]) 
duracion_alto = fuzz.trimf(x_duracion, [5, 10, 10]) 
recomendar_baja = fuzz.trimf(x_recomendar, [0, 0, 50]) 
recomendar_media = fuzz.trimf(x_recomendar, [0, 50, 100]) 
recomendar_alta = fuzz.trimf(x_recomendar, [50, 100, 100])

# Visualizar estos universos y funciones de pertenencia.
fig, (axo, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9)) 
axo.plot(x_jugabilidad, jugabilidad_baja, 'b', linewidth=1.5, label='Mala') 
axo.plot(x_jugabilidad, jugabilidad_media, 'g', linewidth=1.5, label='Aceptable')
axo.plot(x_jugabilidad, jugabilidad_alta, 'r', linewidth=1.5, label='Buena') 
axo.set_title('Jugabilidad del juego')
axo.legend() 
ax1.plot(x_duracion, duracion_bajo, 'b', linewidth=1.5, label='Poca')
ax1.plot(x_duracion, duracion_medio, 'g', linewidth=1.5, label='Aceptable')
ax1.plot(x_duracion, duracion_alto, 'r', linewidth=1.5, label='Mucha')
ax1.set_title('Duracion del juego')
ax1.legend()

ax2.plot(x_recomendar, recomendar_baja, 'b', linewidth=1.5, label='Baja')
ax2.plot(x_recomendar, recomendar_media, 'g', linewidth=1.5, label='Media') 
ax2.plot(x_recomendar, recomendar_alta, 'r', linewidth=1.5, label='Alta')
ax2.set_title('Probabilidad de recomendar el juego')
ax2.legend()

# Ocultar los ejes superior / derecho
for ax in (axo, ax1, ax2):
    ax.spines['top'].set_visible(False) 
    ax.spines['right'].set_visible(False) 
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt. tight_layout()

# Necesitamos la activación de nuestras funciones de pertenencia difusa en estos valores. 
# Los valores exactos 6.5 y 9.8 no existen en nuestros universos ...
# ¡Para esto existe fuzz. interp_membership! 
nivel_jugabilidad_bajo = fuzz.interp_membership(x_jugabilidad, jugabilidad_baja, 6.5) 
nivel_jugabilidad_medio = fuzz.interp_membership(x_jugabilidad, jugabilidad_media, 6.5)
nivel_jugabilidad_alto = fuzz.interp_membership(x_jugabilidad, jugabilidad_alta, 6.5)
nivel_duracion_bajo = fuzz.interp_membership(x_duracion, duracion_bajo, 9.8)
nivel_duracion_medio = fuzz.interp_membership(x_duracion, duracion_medio, 9.8)
nivel_duracion_alto = fuzz.interp_membership(x_duracion, duracion_alto, 9.8)

# Ahora tomamos nuestras reglas y las aplicamos. La regla 1 se refiere a la poca duracion o mala jugabilidad
# El operador OR significa que tomamos el máximo de estos dos.
activar_regla1 = np.fmax(nivel_jugabilidad_bajo, nivel_duracion_bajo) 

# Ahora aplicamos esto recortando la parte superior de la salida correspondiente 
# función de membresía con 'np. fmin' 
activacion_recomendar_baja = np.fmin(activar_regla1, recomendar_baja) 

# eliminado por completo a 0
# Para la regla 2, conectamos un servicio aceptable con una recomendacion media.
activacion_recomendar_media = np.fmin(nivel_duracion_medio, recomendar_media)

# Para la regla 3, conectamos servicio bueno o comida buena con  recomendacion alta.
activar_regla3 = np. fmax(nivel_jugabilidad_alto, nivel_duracion_alto) 
activacion_recomendar_alta = np.fmin(activar_regla3, recomendar_alta) 
recomendar0 = np.zeros_like (x_recomendar)

# Visualizar lo anterior
fig, axo = plt.subplots(figsize=(8, 3))
axo.fill_between(x_recomendar, recomendar0, activacion_recomendar_baja, facecolor='b', alpha=0.7)
axo.plot(x_recomendar, recomendar_baja, 'b', linewidth=0.5, linestyle='--', ) 
axo.fill_between(x_recomendar, recomendar0, activacion_recomendar_media, facecolor='g', alpha=0.7)
axo.plot(x_recomendar, recomendar_media, 'g', linewidth=0.5, linestyle='--') 
axo.fill_between(x_recomendar, recomendar0, activacion_recomendar_alta, facecolor='r', alpha=0.7)
axo.plot(x_recomendar, recomendar_alta, 'r', linewidth=0.5, linestyle='--')
axo.set_title('Actividad de membresía de salida')

# Cancelar los ejes superior / derecho 
for ax in (axo,):
    ax.spines['top'].set_visible(False) 
    ax.spines['right'].set_visible(False) 
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left() 
plt.tight_layout()

# Agregar las tres funciones de pertenencia de salida juntas
agregado = np. fmax(activacion_recomendar_baja,
np.fmax(activacion_recomendar_media, activacion_recomendar_alta))

# Calcular el resultado difuso
recomendar = fuzz.defuzz(x_recomendar, agregado, 'centroid')
activacion_recomendar = fuzz. interp_membership(x_recomendar, agregado, recomendar) # Para dibujar

# Visualizar lo anterior
fig, axo = plt.subplots(figsize=(8, 3))
axo.plot(x_recomendar, recomendar_baja, 'b', linewidth=0.5, linestyle='--', )
axo.plot(x_recomendar, recomendar_media, 'g', linewidth=0.5, linestyle='--')
axo.plot(x_recomendar, recomendar_alta, 'r', linewidth=0.5, linestyle='--') 
axo.fill_between(x_recomendar, recomendar0, agregado, facecolor='Orange', alpha=0.7)
axo.plot([recomendar, recomendar], [0, activacion_recomendar], 'k', linewidth=1.5, alpha=0.9)
axo.set_title('Membresía agregada y resultado (línea)')

# Cancela los ejes superior / derecho
for ax in (axo,): 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False) 
    ax.get_xaxis().tick_bottom 
    ax.get_yaxis().tick_left()
plt.tight_layout()

plt.show()





