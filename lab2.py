import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -------------------------------------------------------
# Параметры
# -------------------------------------------------------
L = 1.0     # Длина стержня
R = 0.1     # Радиус диска
rect_width = 0.1 # Ширина прямоугольника
rect_height = 0.05 # Высота прямоугольника

# -------------------------------------------------------
# Законы движения (придумал на рандом)
# -------------------------------------------------------

def phi(t):
    """
    Угол стержня, управляет горизонтальным
    перемещением диска. Чем больше phi(t), тем больше
    смещение диска по оси X.
    """
    return np.sin(1.5 * t)

def s_func(t):
    """
    Расстояние от нижнего ползуна (C) до плоскости поверхности (y = 0).
    """
    return 0.2 + 0.1 * np.sin(3.0 * t)

# -------------------------------------------------------
# Вспомогательные функции
# -------------------------------------------------------

def create_circle(x_center, y_center, radius, num_points=50):
    """
    Создаём набор точек для рисования окружности (диск).
    """
    angles = np.linspace(0, 2*np.pi, num_points)
    x_vals = x_center + radius * np.cos(angles)
    y_vals = y_center + radius * np.sin(angles)
    return x_vals, y_vals

def create_zigzag_spring(x1, y1, x2, y2, num_zigs=10, amplitude=0.05):
    """
    Создаёт набор точек для рисования пружины в виде зигзага.
    """
    # Длина пружины
    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    # Угол между пружиной и горизонталью
    angle = np.arctan2(y2 - y1, x2 - x1)

    # Создаём точки вдоль пружины
    t = np.linspace(0, length, num_zigs * 2 + 1)
    x_vals = x1 + t * np.cos(angle) + amplitude * np.sin(np.pi * num_zigs * t / length) * np.sin(angle)
    y_vals = y1 + t * np.sin(angle) - amplitude * np.sin(np.pi * num_zigs * t / length) * np.cos(angle)

    return x_vals, y_vals

def create_rectangle(x_center, y_center, width, height):
    """
    Создаёт координаты вершин прямоугольника для рисования.
    """
    x_vals = [x_center - width / 2, x_center + width / 2, x_center + width / 2, x_center - width / 2, x_center - width / 2]
    y_vals = [y_center - height / 2, y_center - height / 2, y_center + height / 2, y_center + height / 2, y_center - height / 2]
    return x_vals, y_vals

"""
 -------------------------------------------------------
 Геометрия системы
 -------------------------------------------------------
 Обозначения:
  A(t) - центр диска, лежит на оси Y=0 и двигается только по X
  B(t) - верхний ползун (xB фиксирована, см. ниже), к нему крепится пружина
  C(t) - нижний ползун (сдвигается по оси Y, yC = s(t))

  Условимся:
   - xB = 0 (координата X верхнего ползуна фиксирована)
   - Длина стержня = L#   - Угол phi(t) задаёт, насколько диск смещён вдоль X
     по формуле xA = L * sin(phi), yA = 0
   - Тогда верхний ползун B(t) = (0, yB), где yB = L * cos(phi)
   - Нижний ползун C(t) = (0, yC), где yC = s(t)

"""

def get_positions(t):
    """
    Возвращает координаты:
      A(t) = (xA, 0)
      B(t) = (0, yB)
      C(t) = (0, yC)
    """
    angle = phi(t)
    xA = L * np.cos(angle)
    yA = 0.0
    xB = 0.0
    yB = L * np.sin(angle)
    s_val = s_func(t)
    xC = 0.0
    yC = s_val
    return xA, yA, xB, yB, xC, yC

# -------------------------------------------------------
# Настройка анимации
# -------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_aspect('equal')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-0.5, 2.0)
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
    t_current = frame * 0.05  # превращаем номер кадра в "время"

    # Получаем координаты точек
    xA, yA, xB, yB, xC, yC = get_positions(t_current)

    # 1) Диск (A) - отображаем окружностью
    circle_x, circle_y = create_circle(xA, yA, R)
    disk_plot.set_data(circle_x, circle_y)

    # 2) Стержень - прямая от A до B
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

# Запускаем анимацию
ani = FuncAnimation(
    fig, 
    update,
    frames=200,
    init_func=init,
    blit=True,
    interval=50  # миллисекунды между кадрами
)

plt.legend()
plt.show()