import csv
import os

import matplotlib.pyplot as plt
import numpy as np

from utils.hermite import pchint


class McCabeThiele:
    def __init__(self):
        """
        Inicialize MCabeThiele class
        """

        self.available_pair = [
            ("methanol", "water"),
            ("ethanol", "water"),
            ("acetone", "chloroform"),
            ("nitrogen", "oxygen"),
            ("toluene", "xylene"),
            ("hexane", "heptane"),
            ("hexane", "xylene"),
            ("ethylene", "ethylene_glycol"),
            ("ammonia", "sulfur_dioxide"),
            ("butanol", "ethyl_acetate"),
            ("acetone", "methyl_isobutyl_ketone"),
        ]

    def set_data(self, compound_a, compound_b):
        if (compound_a, compound_b) in self.available_pair:
            self.compound_a = compound_a
            self.compound_b = compound_b
            self.x = []
            self.y = []
            print(os.getcwd())
            with open("src/data/" f"{self.compound_a}-{self.compound_b}.csv") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.x.append(float(row["x"]))
                    self.y.append(float(row["y"]))
        else:
            print("There no available data for that pair compounds")

    def eq_line(self, a, b):
        return lambda x: a + b * x

    def inter_vline(self, x, data_x, data_y):
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
        line2 = self.eq_line(origin, slope)
        return x, line2(x)

    def inter_line(self, line, data_x, data_y):
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
        line2 = self.eq_line(origin, slope)
        f1 = line2(0) - line(0)
        f2 = line2(1) - line(1)
        x_in = f1 / (f1 - f2)
        y_in = line(x_in)

        return x_in, y_in

    def reflux_min(self, x_in, y_in, x_D):
        k = (x_D - x_in) / (x_D - y_in)
        R = 1 / (k - 1)
        self.Rmin = R
        return R

    def interpolate_data(self):
        self.x_data = np.linspace(self.x[0], self.x[-1], 100)
        self.y_data = pchint(self.x, self.y, self.x_data)

    def fit(self, xF, xD, xW):
        self.xF = xF
        self.xD = xD
        self.xW = xW
        self.xe = []
        self.ye = []
        self.interpolate_data()
        x_int, y_int = self.inter_vline(xF, self.x_data, self.y_data)
        r_min = self.reflux_min(x_int, y_int, xD)
        r = 1.5 * r_min

        self.line_recti = self.eq_line(xD / (r + 1), r / (r + 1))
        yF = self.line_recti(xF)
        slope = (xW - yF) / (xW - xF)
        origin = -slope * xF + yF
        self.line_strip = self.eq_line(origin, slope)

        xp = xD
        self.xe.append(xD)
        self.ye.append(xD)
        etapas = 0
        while xp > xW:
            line_xpn = self.eq_line(xp, 0)
            xpn, xp = self.inter_line(line_xpn, self.x_data, self.y_data)

            etapas += 1
            self.ye.append(xp)
            self.xe.append(xpn)

            if xpn > xF:
                xp = self.line_recti(xpn)
            else:
                xp = self.line_strip(xpn)

            self.ye.append(xp)
            self.xe.append(xpn)

        self.steps = etapas

    def plot(self):
        x_rect = np.linspace(self.xF, self.xD, 50)
        y_rect = np.array([self.line_recti(x) for x in x_rect])
        _, ax = plt.subplots()
        x_strip = np.linspace(self.xW, self.xF, 50)
        y_strip = np.array([self.line_strip(c) for c in x_strip])

        ax.plot(self.x_data, self.y_data, label="Equilibrium")
        ax.plot([0, 1], [0, 1])
        ax.plot(x_rect, y_rect, label="ROP")
        ax.plot(x_strip, y_strip, label="SOP")
        ax.plot(self.xe, self.ye, label="Steps")
        ax.set_title(f"Steps McCabe Thiele\n {self.compound_a}-{self.compound_b}")
        ax.set_ylabel("molar composition y")
        ax.set_xlabel("molar composition x")
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.grid()
        plt.legend(loc="lower right")
        plt.show()
