import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import matplotlib.animation as animation

# Parámetros del sistema
m, M, l, g = 0.3, 0.5, 0.254, 9.81
ñ = m / (M + m)

# Condiciones iniciales: [d_th, d_x, th, x]
y0 = np.array([0.0, 0.0, np.pi/2, 1.0])

# Definir las ecuaciones diferenciales
def F(t, y):
    d_th, d_x, th, x = y
    dd_th = (-ñ * d_th**2 * np.sin(th) * np.cos(th) - g / l * np.sin(th)) / (1 - ñ * np.cos(th)**2)
    dd_x = ñ * l * d_th**2 * np.sin(th) - ñ * l * dd_th * np.cos(th)
    return [dd_th, dd_x, d_th, d_x]

# Tiempo de simulación
t_eval = np.linspace(0, 10, 240)  # Simular 10 segundos, 24 FPS

# Resolver el sistema de ecuaciones diferenciales
sol = solve_ivp(F, [0, 10], y0, t_eval=t_eval)

# Extraer las soluciones
d_th = sol.y[0]
d_x = sol.y[1]
th = sol.y[2]
x = sol.y[3]
t = sol.t

# Calcular las posiciones del péndulo en función del tiempo
x_pendulum = x + l * np.sin(th)
y_pendulum = -l * np.cos(th)

# Crear la figura para la animación y las gráficas
fig, (ax_anim, ax_pos) = plt.subplots(2, 1, figsize=(8, 10))

# Configuración de la animación
ax_anim.set_xlim([-0.25,0.25])
ax_anim.set_ylim([-0.25, 0.25])
ax_anim.set_aspect('equal')

# Dibujar el péndulo y el carro
cart, = ax_anim.plot([], [], 'ks', markersize=15)  # Carro
pendulum_line, = ax_anim.plot([], [], 'r-', lw=2)  # Cuerda del péndulo
pendulum_mass, = ax_anim.plot([], [], 'bo', markersize=8)  # Masa del péndulo

# Configuración de las gráficas de posición
ax_pos.set_title("Posición del péndulo en función del tiempo")
ax_pos.set_xlim(0, 10)
ax_pos.set_ylim(-2, 2)
ax_pos.set_xlabel("Tiempo (s)")
ax_pos.set_ylabel("Posición (m)")
line_x, = ax_pos.plot([], [], label="x(t)")
line_y, = ax_pos.plot([], [], label="y(t)")
ax_pos.legend()

# Función para actualizar la animación y las gráficas de posición en cada cuadro
def animate(i):
    # Posiciones del carro y el péndulo
    x_cart = x[i]
    th_pend = th[i]
    
    # Posiciones del péndulo
    x_pend = x_cart + l * np.sin(th_pend)
    y_pend = -l * np.cos(th_pend)
    
    # Actualizar las posiciones del carro
    cart.set_data([x_cart], [0])
    
    # Actualizar las posiciones del péndulo (línea y masa)
    pendulum_line.set_data([x_cart, x_pend], [0, y_pend])
    pendulum_mass.set_data([x_pend], [y_pend])
    
    # Actualizar las gráficas de posición
    line_x.set_data(t[:i], x_pendulum[:i])
    line_y.set_data(t[:i], y_pendulum[:i])
    
    return cart, pendulum_line, pendulum_mass, line_x, line_y

# Configurar la animación
ani = animation.FuncAnimation(fig, animate, frames=len(t), interval=1000/24, blit=True)

# Mostrar la animación y las gráficas de posición
plt.tight_layout()
plt.show()
