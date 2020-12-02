# CONTROL DIFUSO API

# Steven Medina Gonzalez - 1088354520
# Elimina Las advertencias
import warnings
warnings. filterwarnings ('ignore')

#Importa las Librerías
import numpy as np 
import skfuzzy as fuzz 
from skfuzzy import control as ctrl 

# Se crean los objetos antecedentes y consecuente a partir de las
# variables del universo y las funciones de membresía 
jugabilidad = ctrl. Antecedent(np.arange(0, 11, 1), 'Jugabilidad')
duracion = ctrl. Antecedent(np.arange(0, 11, 1), 'Duracion') 
recomendar = ctrl.Consequent(np.arange (0, 101, 1), 'Recomendar')

# La población de la función de membresía automática es posible con .automf (3, 5 o 7) 
jugabilidad.automf(3) 
duracion.automf(3)

# Las funciones de membresía personalizadas se pueden construir interactivamente con l
# API Pythonic 
recomendar['bajo'] = fuzz.trimf(recomendar.universe, [0, 0, 13])
recomendar['medio'] = fuzz. trimf (recomendar.universe, [0, 13, 25])
recomendar['alto'] = fuzz.trimf (recomendar.universe, [13, 25, 25])

# Visualización con .view)
jugabilidad['average'].view()
duracion.view
recomendar.view

# Creación de las reglas 
regla1 = ctrl.Rule(jugabilidad['poor'] | duracion['poor'], recomendar['bajo']) 
regla2 = ctrl.Rule(duracion['average'], recomendar['medio']) 
regla3 = ctrl.Rule(duracion['good'] | jugabilidad['good' ], recomendar['alto'])

# Visualización de la regla 1 
regla1.view() 

# Generación del simulador 
control_recomendar = ctrl.ControlSystem([regla1, regla2, regla3])
asignacion_recomendar = ctrl.ControlSystemSimulation(control_recomendar)

# Pasar entradas al Control System usando etiquetas 'Antecedent' con Pythonic API 
# Nota: si quiere pasar muchas entradas a la vez, usar . inputs (dict_of_data) 
asignacion_recomendar.input['Jugabilidad'] = 6.5 
asignacion_recomendar.input['Duracion'] = 9.8

# Se obtiene el valor 
asignacion_recomendar.compute() 

# Se muestra la información 
print("VProbabilidad de recomendar: ")
print (asignacion_recomendar.output['Recomendar'])

# Se muestra la curva de asignación de propina
recomendar.view(sim=asignacion_recomendar)
