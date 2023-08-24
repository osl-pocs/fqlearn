import csv

import matplotlib.pyplot as plt
import numpy as np
from hermite import pchint


def open_data(location):
    x, y = [], []

    with open(location, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x.append(float(row["x"]))
            y.append(float(row["y"]))
    return x, y


def eq_line(a, b):
    return lambda x: a + b * x


# Obteniendo la curva interpolada


def inter_vline(x, data_x, data_y):
    n = len(data_x)
    i, j = 0, n - 1
    while (j - i) >= 2:
        m = (j + i) // 2
        if data_x[m] > x:
            j = m
        else:
            i = m
    slope = (data_y[j] - data_y[i]) / (data_x[j] - data_x[i])
    origin = -slope * data_x[i] + data_y[i]
    line2 = eq_line(origin, slope)
    return x, line2(x)


def inter_line(line, data_x, data_y):
    n = len(data_x)
    i, j = 0, n - 1

    while (j - i) >= 2:
        m = (j + i) // 2
        if (data_y[m] - line(data_x[m])) * (data_y[j] - line(data_x[j])) < 0:
            i = m
        else:
            j = m

    slope = (data_y[j] - data_y[i]) / (data_x[j] - data_x[i])
    origin = -slope * data_x[i] + data_y[i]
    line2 = eq_line(origin, slope)
    f1 = line2(0) - line(0)
    f2 = line2(1) - line(1)
    x_in = f1 / (f1 - f2)
    y_in = line(x_in)

    return x_in, y_in


def reflux_min(x_in, y_in, x_D):
    k = (x_D - x_in) / (x_D - y_in)
    R = 1 / (k - 1)
    return R


def solve_mccabe_thiele():
    data_x, data_y = open_data("agua-metanol.csv")
    # obtención de datos interpolados
    x0 = np.linspace(data_x[0], data_x[-1], 100)
    y0 = pchint(data_x, data_y, x0)

    xF = 0.5
    xD = 0.94
    xW = 0.05

    x_int, y_int = inter_vline(xF, x0, y0)
    r_min = reflux_min(x_int, y_int, xD)
    r = 1.5 * r_min

    line_recti = eq_line(xD / (r + 1), r / (r + 1))
    yF = line_recti(xF)
    slope = (xW - yF) / (xW - xF)
    origin = -slope * xF + yF
    line_strip = eq_line(origin, slope)

    xe = []
    ye = []
    xp = xD
    xe.append(xD)
    ye.append(xD)
    etapas = 0
    while xp > xW:
        line_xpn = eq_line(xp, 0)
        xpn, xp = inter_line(line_xpn, x0, y0)

        etapas += 1
        ye.append(xp)
        xe.append(xpn)

        if xpn > xF:
            xp = line_recti(xpn)
        else:
            xp = line_strip(xpn)

        ye.append(xp)
        xe.append(xpn)

    print("etapas", etapas)
    x_rect = np.linspace(xF, xD, 50)
    y_rect = np.array([line_recti(x) for x in x_rect])
    fig, ax = plt.subplots()
    x_strip = np.linspace(xW, xF, 50)
    y_strip = np.array([line_strip(c) for c in x_strip])

    ax.plot(x0, y0, label="Curva de equilibrio")
    ax.plot([0, 1], [0, 1])
    ax.plot(x_rect, y_rect, label="Línea de rectificación")
    ax.plot(x_strip, y_strip, label="Línea de agotamiento")
    ax.plot(xe, ye, label="Etapas")
    ax.set_title("Número de etapas por McCabe Thiele\n metanol-agua")
    ax.set_ylabel("y")
    ax.set_xlabel("x")
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.grid()
    plt.legend(loc="lower right")
    plt.show()


solve_mccabe_thiele()
