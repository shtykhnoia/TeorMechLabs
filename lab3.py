import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

# -------------------------------------------------------
# Константы
# -------------------------------------------------------
L = 1.0  # Длина стержня
R = 0.1  # Радиус диска
rect_width = 0.1  # Ширина прямоугольника
rect_height = 0.05  # Высота прямоугольника

m1 = 2.0
m2 = m3 = 0.2
c = 5.0
g = 9.81
M = 3.0

# -------------------------------------------------------
# Решение системы дифференциальных уравнений
# -------------------------------------------------------
def system_derivatives(y, t):
    phi, s, phi_dot, s_dot = y
    
    # Коэффициенты для первого уравнения
    A = 2 * (3 * m1 * np.sin(phi)**2 + 2 * m2 * np.cos(phi)**2) * L**2
    B = (3 * m1 - 2 * m2) * L**2 * phi_dot**2 * np.sin(2 * phi)
    C = 4 * (c * (L * np.sin(phi) - s) + m2 * g) * L * np.cos(phi)
    
    # Решение для phi_ddot
    phi_ddot = (4 * M - B - C) / A
    
    # Решение для s_ddot
    s_ddot = (-m3 * g + c * (L * np.sin(phi) - s)) / m3
    
    return [phi_dot, s_dot, phi_ddot, s_ddot]

# Начальные условия: phi(0) = 0, s(0) = 0, phi_dot(0) = pi/3, s_dot(0) = 0
initial_conditions = [0, 0, np.pi / 3, 0]

# Массив времени
t = np.linspace(0, 30, 1000)

# Решение системы дифференциальных уравнений
solution = odeint(system_derivatives, initial_conditions, t)

# Извлечение результатов
phi_vals = solution[:, 0]
s_vals = solution[:, 1]
phi_dot = solution[:, 2]
s_dot = solution[:, 3]

# Вычисление вторых производных
phi_ddot = np.gradient(phi_dot, t)
s_ddot = np.gradient(s_dot, t)

# Вычисление Nx и Ny
Nx = -m1 * L * (phi_ddot * np.sin(phi_vals) + phi_dot**2 * np.cos(phi_vals)) / 2
Ny = m2 * L * (phi_ddot * np.cos(phi_vals) - phi_dot**2 * np.sin(phi_vals)) + m3 * s_ddot + (m1 + m2 + m3) * g

# -------------------------------------------------------
# Построение графиков phi(t), s(t), Nx(t), Ny(t)
# -------------------------------------------------------
plt.figure(figsize=(10, 6))

# График phi(t)
plt.subplot(2, 2, 1)
plt.plot(t, phi_vals, label='phi(t)', color='blue')
plt.xlabel('Время (с)')
plt.ylabel('phi(t)')
plt.legend()
plt.grid(True)

# График s(t)
plt.subplot(2, 2, 2)
plt.plot(t, s_vals, label='s(t)', color='red')
plt.xlabel('Время (с)')
plt.ylabel('s(t)')
plt.legend()
plt.grid(True)

# График Nx(t)
plt.subplot(2, 2, 3)
plt.plot(t, Nx, label='Nx(t)', color='green')
plt.xlabel('Время (с)')
plt.ylabel('Nx(t)')
plt.legend()
plt.grid(True)

# График Ny(t)
plt.subplot(2, 2, 4)
plt.plot(t, Ny, label='Ny(t)', color='orange')
plt.xlabel('Время (с)')
plt.ylabel('Ny(t)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# -------------------------------------------------------
# Вспомогательные функции для анимации
# -------------------------------------------------------
def create_circle(x_center, y_center, radius, num_points=50):
    """Создает набор точек для рисования окружности (диск)."""
    angles = np.linspace(0, 2 * np.pi, num_points)
    x_vals = x_center + radius * np.cos(angles)
    y_vals = y_center + radius * np.sin(angles)
    return x_vals, y_vals

def create_zigzag_spring(x1, y1, x2, y2, num_zigs=10, amplitude=0.05):
    """Создает набор точек для рисования зигзагообразной пружины."""
    # Длина пружины
    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    # Угол между пружиной и горизонталью
    angle = np.arctan2(y2 - y1, x2 - x1)

    # Создаем точки вдоль пружины
    t = np.linspace(0, length, num_zigs * 2 + 1)
    x_vals = x1 + t * np.cos(angle) + amplitude * np.sin(np.pi * num_zigs * t / length) * np.sin(angle)
    y_vals = y1 + t * np.sin(angle) - amplitude * np.sin(np.pi * num_zigs * t / length) * np.cos(angle)

    return x_vals, y_vals

def create_rectangle(x_center, y_center, width, height):
    """Создает координаты вершин прямоугольника для рисования."""
    x_vals = [x_center - width / 2, x_center + width / 2, x_center + width / 2, x_center - width / 2, x_center - width / 2]
    y_vals = [y_center - height / 2, y_center - height / 2, y_center + height / 2, y_center + height / 2, y_center - height / 2]
    return x_vals, y_vals

def get_positions(t_current):
    """Возвращает координаты точек A, B и C."""
    angle = phi_vals[int(t_current / 0.03)]
    xA = L * np.cos(angle)
    yA = 0.0
    xB = 0.0
    yB = L * np.sin(angle)
    s_val = s_vals[int(t_current / 0.03)]
    xC = 0.0
    yC = s_val
    return xA, yA, xB, yB, xC, yC

# -------------------------------------------------------
# Настройка анимации
# -------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 8))  # Увеличена высота окна
ax.set_aspect('equal')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-3.0, 2.0)  # Изменены пределы оси Y
ax.grid(True)
plt.title("Диск (A) движется по оси X, стержень (phi), xB фиксирована, пружина (s)")

# Вертикальные направляющие
ax.axvline(x=0, color='gray', linestyle='--')

# Графические объекты (линии/точки)
disk_plot, = ax.plot([], [], 'b-', lw=2, label='Диск')
rod_line, = ax.plot([], [], 'k-', lw=2, label='Стержень')
spring_line, = ax.plot([], [], 'g-', lw=2, label='Пружина')
top_slider_rect, = ax.plot([], [], 'r-', lw=2, label='Верхний ползун (B, x=const)')
bottom_slider_rect, = ax.plot([], [], 'm-', lw=2, label='Нижний ползун (C)')
center_disk, = ax.plot([], [], 'yo', label='Центр диска (A)')

def init():
    disk_plot.set_data([], [])
    rod_line.set_data([], [])
    spring_line.set_data([], [])
    top_slider_rect.set_data([], [])
    bottom_slider_rect.set_data([], [])
    center_disk.set_data([], [])
    return disk_plot, rod_line, spring_line, top_slider_rect, bottom_slider_rect, center_disk

def update(frame):
    t_current = frame * 0.03  # Преобразуем номер кадра во "время"

    # Получаем координаты точек
    xA, yA, xB, yB, xC, yC = get_positions(t_current)

    # 1) Диск (A) - отображаем как окружность
    circle_x, circle_y = create_circle(xA, yA, R)
    disk_plot.set_data(circle_x, circle_y)

    # 2) Стержень - линия от A до B
    rod_line.set_data([xA, xB], [yA, yB])

    # 3) Пружина - зигзаг от B до C
    spring_x, spring_y = create_zigzag_spring(xB, yB, xC, yC)
    spring_line.set_data(spring_x, spring_y)

    # 4) Верхний ползун (точка B) - прямоугольник
    top_rect_x, top_rect_y = create_rectangle(xB, yB, rect_width, rect_height)
    top_slider_rect.set_data(top_rect_x, top_rect_y)

    # 5) Нижний ползун (точка C) - прямоугольник
    bottom_rect_x, bottom_rect_y = create_rectangle(xC, yC, rect_width, rect_height)
    bottom_slider_rect.set_data(bottom_rect_x, bottom_rect_y)

    # 6) Центр диска (точка A)
    center_disk.set_data([xA], [yA])

    return disk_plot, rod_line, spring_line, top_slider_rect, bottom_slider_rect, center_disk

# Запуск анимации
ani = FuncAnimation(
    fig, 
    update,
    frames=1000,
    init_func=init,
    blit=True,
    interval=30  # миллисекунды между кадрами
)

plt.legend()
plt.show()