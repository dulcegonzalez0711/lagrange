import numpy as np 
from numpy.linalg import inv
from matplotlib import pyplot as plt
from math import cos, sin, tan, pi

def G(y,t): 
    x_d, θ_d, x, θ = y[0], y[1], y[2], y[3]

    x_dd = (l0+x) * θ_d**2 - k/m*x + g*cos(θ)
    θ_dd = -2.0/(l0+x) * x_d * θ_d - g/(l0+x) * sin(θ)    

    return np.array([x_dd, θ_dd, x_d, θ_d])

def RK4_step(y, t, dt):
    k1 = G(y,t)
    k2 = G(y+0.5*k1*dt, t+0.5*dt)
    k3 = G(y+0.5*k2*dt, t+0.5*dt)
    k4 = G(y+k3*dt, t+dt)

    return dt * (k1 + 2*k2 + 2*k3 + k4) / 6

# Variables
m = 0.060    # Masa
l0 = 0.1      # Longitud inicial
g = 9      # Aceleración gravitacional
k = 9.8       # Constante del resorte

delta_t = 0.01
time = np.arange(0.0, 6, delta_t)

# Estado inicial
y = np.array([0, np.deg2rad(51.3), 0.0 , 0])   # [velocidad, desplazamiento]

Y1 = []  # Para desplazamiento
Y2 = []  # Para ángulo

# Solución por pasos de tiempo
for t in time:
    y = y + RK4_step(y, t, delta_t) 
    Y1.append(y[2])  # Desplazamiento
    Y2.append(y[3])  # Ángulo

# Gráfica para desplazamiento x
plt.figure(figsize=(10, 5))
plt.plot(time, Y1, color='blue', linewidth=2)
plt.title('Desplazamiento del Péndulo Elástico (x) vs. Tiempo', fontsize=14)
plt.xlabel('Tiempo (s)', fontsize=12)
plt.ylabel('Desplazamiento (m)', fontsize=12)
plt.grid(True)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.savefig('desplazamiento.png', dpi=300)  # Guarda la figura
plt.show()

# Gráfica para ángulo θ
plt.figure(figsize=(10, 5))
plt.plot(time, np.rad2deg(Y2), color='red', linewidth=2)  # Convertir a grados
plt.title('Ángulo del Péndulo Elástico (θ) vs. Tiempo', fontsize=14)
plt.xlabel('Tiempo (s)', fontsize=12)
plt.ylabel('Ángulo (°)', fontsize=12)
plt.grid(True)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.savefig('angulo.png', dpi=300)  # Guarda la figura
plt.show()
