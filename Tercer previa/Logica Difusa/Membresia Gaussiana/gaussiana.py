import numpy as np
import skfuzzy as sk
import matplotlib.pyplot as plt

x = np.arange(0,11,0.1)

vd_gaussiana = sk.gaussmf(x, np.mean(x), np.std(x))

plt.figure()
plt.plot(x,vd_gaussiana,'b',linewidth=1.5,label='Servicio')

plt.title('Calidad del servicio en un restaurante')
plt.ylabel("Membresia")
plt.xlabel("Nivel del servicio")
plt.legend(loc='center right', bbox_to_anchor=(1.25,0.5), ncol=1, fancybox=True,shadow=True)
plt.show()