import math
import sympy as s
import matplotlib.pyplot as plot
import numpy as np
from matplotlib.animation import FuncAnimation

t = s.Symbol('t')

x = (1 - s.sin(t)) * s.cos(2 * t)
y = (1 - s.sin(t)) * s.sin(2 * t)

Vx = s.diff(x, t)
Vy = s.diff(y, t)

ax = s.diff(Vx, t)
ay = s.diff(Vy, t)

rx = -Vy / s.sqrt(Vx * Vx + Vy * Vy)
ry = Vx / s.sqrt(Vx * Vx + Vy * Vy)

step = 1000
T = np.linspace(0, 2 * math.pi, step)
X = np.zeros_like(T)
Y = np.zeros_like(T)
VX = np.zeros_like(T)
VY = np.zeros_like(T)
AX = np.zeros_like(T)
AY = np.zeros_like(T)
RX = np.zeros_like(T)
RY = np.zeros_like(T)


for i in range(len(T)):
    X[i] = x.subs(t, T[i])
    Y[i] = y.subs(t, T[i])
    VX[i] = 0.5 * Vx.subs(t, T[i])
    VY[i] = 0.5 * Vy.subs(t, T[i])
    AX[i] = 0.2 * ax.subs(t, T[i])
    AY[i] = 0.2 * ay.subs(t, T[i])
    RX[i] = rx.subs(t, T[i])
    RY[i] = ry.subs(t, T[i])

fgr = plot.figure()
grf = fgr.add_subplot(1, 1, 1)
grf.axis('equal')
grf.set(xlim=[-6, 6], ylim=[-6, 6])
grf.plot(X, Y)

Pnt = grf.plot(X[0], Y[0], marker='o')[0]
Vpl = grf.plot([X[0], X[0] + VX[0]], [Y[0], Y[0] + VY[0]], 'r')[0]
Apl = grf.plot([X[0], X[0] + AX[0]], [Y[0], Y[0] + AY[0]], 'g')[0]
Rpl = grf.plot([X[0], X[0] + RX[0]], [Y[0], Y[0] + RY[0]], 'b')[0]


def vect_arrow(vec_x, vec_y, _x, _y):
    a = 0.15
    b = 0.1
    arr_x = np.array([-a, 0, -a])
    arr_y = np.array([b, 0, -b])

    phi = math.atan2(vec_y, vec_x)

    rot_x = arr_x * np.cos(phi) - arr_y * np.sin(phi)
    rot_y = arr_x * np.sin(phi) + arr_y * np.cos(phi)

    arr_x = rot_x + _x + vec_x
    arr_y = rot_y + _y + vec_y

    return arr_x, arr_y


ArVX, ArVY = vect_arrow(VX[0], VY[0], X[0], Y[0])
V_arr = grf.plot(ArVX, ArVY, 'r')[0]

ArAX, ArAY = vect_arrow(AX[0], AY[0], X[0], Y[0])
A_arr = grf.plot(ArAX, ArAY, 'g')[0]

ArRX, ArRY = vect_arrow(RX[0], RY[0], X[0], Y[0])
R_arr = grf.plot(ArRX, ArRY, 'b')[0]


def anim(j):
    global ArVX, ArVY, ArAX, ArAY, ArRX, ArRY
    Pnt.set_data([X[j]], [Y[j]])

    Vpl.set_data([X[j], X[j] + VX[j]], [Y[j], Y[j] + VY[j]])
    ArVX, ArVY = vect_arrow(VX[j], VY[j], X[j], Y[j])
    V_arr.set_data(ArVX, ArVY)

    Apl.set_data([X[j], X[j] + AX[j]], [Y[j], Y[j] + AY[j]])
    ArAX, ArAY = vect_arrow(AX[j], AY[j], X[j], Y[j])
    A_arr.set_data(ArAX, ArAY)

    Rpl.set_data([X[j], X[j] + RX[j]], [Y[j], Y[j] + RY[j]])
    ArRX, ArRY = vect_arrow(RX[j], RY[j], X[j], Y[j])
    R_arr.set_data(ArRX, ArRY)

    return [Pnt, Vpl, V_arr, Apl, A_arr, Rpl, R_arr]


an = FuncAnimation(fgr, anim, frames=step, interval=1)

plot.show()