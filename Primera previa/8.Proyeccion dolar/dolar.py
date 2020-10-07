# COMPUTACIÓN BLANDA - Sistemas y Computación

# Steven Medina Gonzalez -Aldahir Rojas Lancheros
# -----------------------------------------------------------------
# Analisis del dolar con relacion al peso colombiano
# -----------------------------------------------------------------
# Con esto buscamos poder analizar un posible rumbo que puede tomar 
# el valor del dolar con respecto a el valor que se le da en colombia
# -----------------------------------------------------------------
import os
from utils import DATA_DIR, CHART_DIR
import numpy as np

np.seterr(all='ignore')

import scipy as sp
import matplotlib.pyplot as plt

data = np.genfromtxt(os.path.join(DATA_DIR, "USD.tsv"), 
                     delimiter="\t")

data = np.array(data, dtype=np.float64)
print(data[:10])
print(data.shape)

colors = ['g', 'k', 'b', 'm', 'r']
linestyles = ['-', '-.', '--', ':', '-']
x = data[:, 0]
y = data[:, 1]

print("Número de entradas incorrectas:", np.sum(np.isnan(y)))

x = x[~np.isnan(y)]
y = y[~np.isnan(y)]

# -----------------------------------------------------------------
def plot_models(x, y, models, fname, mx=None, ymax=None, xmin=None):
    ''' dibujar datos de entrada '''
    plt.figure(num=None, figsize=(14, 8))

    plt.clf()
    plt.scatter(x, y, s=10)
    plt.title("Valor del dolar en Colombia desde 1995") #Desde Mayo del 1995
    
    # Título en la base
    plt.xlabel("Tiempo")
    
    # Título lateral
    plt.ylabel("Valor de cierre")
    plt.xticks([w * 10 * 24 for w in range(10)],['Lustro %i' % w for w in range(10)])

    if models:
        if mx is None:
            mx = np.linspace(0, x[-1], 1000)
        for model, style, color in zip(models, linestyles, colors):
            # print "Modelo:",model
            # print "Coeffs:",model.coeffs
            plt.plot(mx, model(mx), linestyle=style, linewidth=2, c=color)

        plt.legend(["d=%i" % m.order for m in models], loc="upper left") 

    plt.autoscale(tight=True) 
    plt.ylim(ymin=0) 
    if ymax: 
        plt.ylim(ymax=ymax) 
    if xmin:
        plt.xlim(xmin=xmin) 
    plt.grid(True, linestyle='-', color='0.75')
    plt.savefig(fname) 

# Primera mirada a los datos
# -----------------------------------------------------------------
plot_models(x, y, None, os.path.join(CHART_DIR, "1400_01_01.png")) #Grafica y compara coeficientes de regresión
# Crea y dibuja los modelos de datos
# -----------------------------------------------------------------
fp1, res1, rank1, sv1, rcond1 = np.polyfit(x, y, 1, full=True)
print("Parámetros del modelo fp1: %s" % fp1)
print("Error del modelo fp1:", res1)
f1 = sp.poly1d(fp1)

fp2, res2, rank2, sv2, rcond2 = np.polyfit(x, y, 2, full=True)
print("Parámetros del modelo fp2: %s" % fp2)
print("Error del modelo fp2:", res2)
f2 = sp.poly1d(fp2)

fp4, res4, rank4, sv4, rcond4 = np.polyfit(x, y, 4, full=True)
print("Parámetros del modelo fp4: %s" % fp4)
print("Error del modelo fp4:", res4)
f4 = sp.poly1d(fp4)
f6 = sp.poly1d(np.polyfit(x, y, 6))
f50 = sp.poly1d(np.polyfit(x, y, 50))
# Se grafican los modelos
# -----------------------------------------------------------------
plot_models(x, y, [f1], os.path.join(CHART_DIR, "1400_01_02.png"))
plot_models(x, y, [f1, f2], os.path.join(CHART_DIR, "1400_01_03.png"))
plot_models(
x, y, [f1, f2, f4, f6, f50], os.path.join(CHART_DIR,
"1400_01_04.png"))

# Ajusta y dibuja un modelo utilizando el conocimiento del punto
# de inflexión
# -----------------------------------------------------------------
inflexion1 = 2.6 * 10 * 24
inflexion2 = 4 * 10 * 24
xa = x[:int(inflexion1)]
ya = y[:int(inflexion1)]
xb = x[int(inflexion1):int(inflexion2)]
yb = y[int(inflexion1):int(inflexion2)]
xc = x[int(inflexion2):]
yc = y[int(inflexion2):]

# Se grafican dos líneas rectas
# -----------------------------------------------------------------
fa = sp.poly1d(np.polyfit(xa, ya, 1))
fb = sp.poly1d(np.polyfit(xb, yb, 1))
fc = sp.poly1d(np.polyfit(xc, yc, 1))

# Se presenta el modelo basado en el punto de inflexión
# -----------------------------------------------------------------
plot_models(x, y, [fa, fb, fc], os.path.join(CHART_DIR, "1400_01_05.png"))

# Función de error
# -----------------------------------------------------------------
def error(f, x, y):
    return np.sum((f(x) - y) ** 2)

# Se imprimen los errores
# -----------------------------------------------------------------
print("Errores para el conjunto completo de datos:")
for f in [f1, f2, f4, f6, f50]:
    print("Error d=%i: %f" % (f.order, error(f, x, y)))

print("Errores solamente después del punto de inflexión")
for f in [f1, f2, f4, f6, f50]:
    print("Error d=%i: %f" % (f.order, error(f, xb, yb)))

print("Error de inflexión=%f" % (error(fa, xa, ya) + error(fb, xb, yb) + error(fb, xb, yb)))

# Se extrapola de modo que se proyecten respuestas en el futuro
# -----------------------------------------------------------------
plot_models(
    x, y, [f1, f2, f4, f6, f50],
    os.path.join(CHART_DIR, "1400_01_06.png"),
    mx=np.linspace(0 * 10 * 24, 6 * 10 * 24, 100),
    ymax=10000, xmin=0 * 10 * 24)

# La parte que sigue es relativa al entrenamiento del modelo
# y la predicción

print("Entrenamiento de datos únicamente despúes del punto de inflexión")
fb1 = fb
fb2 = sp.poly1d(np.polyfit(xc, yc, 2))
fb4 = sp.poly1d(np.polyfit(xc, yc, 4))
fb6 = sp.poly1d(np.polyfit(xc, yc, 6))
fb50 = sp.poly1d(np.polyfit(xc, yc, 50))

print("Errores después del punto de inflexión")
for f in [fb1, fb2, fb4, fb6, fb50]:
    print("Error d=%i: %f" % (f.order, error(f, xb, yb)))

# Gráficas después del punto de inflexión
# -----------------------------------------------------------------
plot_models(
    x, y, [fb1, fb2, fb4, fb6, fb50],
    os.path.join(CHART_DIR, "1400_01_07.png"),
    mx=np.linspace(0 * 10 * 24, 6 * 10 * 24, 100),
    ymax=10000, xmin=0 * 10 * 24)


# Separa el entrenamiento de los datos de prueba
# -----------------------------------------------------------------
frac = 0.3
split_idx = int(frac * len(xc))
shuffled = sp.random.permutation(list(range(len(xc))))
test = sorted(shuffled[:split_idx])
train = sorted(shuffled[split_idx:])
fbt1 = sp.poly1d(np.polyfit(xc[train], yc[train], 1))
fbt2 = sp.poly1d(np.polyfit(xc[train], yc[train], 2))
print("fbt2(x)= \n%s" % fbt2)
print("fbt2(x)-5000= \n%s" % (fbt2-5000))
fbt4 = sp.poly1d(np.polyfit(xc[train], yc[train], 4))
fbt6 = sp.poly1d(np.polyfit(xc[train], yc[train], 6))
fbt50 = sp.poly1d(np.polyfit(xc[train], yc[train], 50))

print("Prueba de error para después del punto de inflexión")
for f in [fbt1, fbt2, fbt4, fbt6, fbt50]:
    print("Error d=%i: %f" % (f.order, error(f, xc[test], yc[test])))

plot_models(
    x, y, [fbt1, fbt2, fbt4, fbt6, fbt50],
    os.path.join(CHART_DIR, "1400_01_08.png"),
    mx=np.linspace(0 * 10 * 24, 6 * 10 * 24, 100),
    ymax=10000, xmin=0 * 10 * 24)

from scipy.optimize import fsolve
print(fbt2)
print(fbt2 - 5000)
alcanzado_max = fsolve(fbt2 - 5000, x0=1279) / (10 * 24)
print("\n5000 pesos esperados en el lustre %f" % 
      alcanzado_max[0])


