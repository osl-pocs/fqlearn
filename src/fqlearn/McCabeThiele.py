import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.optimize import fsolve

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

    def set_data(self, compound_a: str, compound_b: str) -> None:
        """
        Description
        -----------
        This function open the the liquid vapor equilibrium data
        for the two compounds compound_a and compound_b.

        Parameters
        ----------
        compound_a : str
                    Name of the compound_a, it is the most volatile
        compound_b : str
                    Name of the compound_b, it is the less volatile

        Returns
        -------
        None

        Notes
        -----
        If there is no matches for the compounds names, prints a message
        indicating that there are no matches for the compounds names.
        """
        if (compound_a, compound_b) in self.available_pair:
            self.compound_a = compound_a
            self.compound_b = compound_b
            archivo_csv = f"src/data/{self.compound_a}-{self.compound_b}.csv"

            if os.path.exists(archivo_csv):
                df = pd.read_csv(archivo_csv)
                self.x = df["x"].tolist()
                self.y = df["y"].tolist()
            else:
                print(
                    f"No hay datos disponibles para el par de compuestos {compound_a}-{compound_b}"
                )
        else:
            print("No hay datos disponibles para ese par de compuestos")

    def set_compositions(self, xD, xW):
        """
        xD (Composition at the destilate)
        xW (Composition in the liquid)
        """
        # To Do: Validate inputs
        self.xD = xD
        self.xW = xW


    def eq_line(self, a: float, b: float) -> callable:
        """
        Description
        -----------
        This function is used to return a new line function


        Parameters
        ---------
        a : float
            This value represents the slope of the new line.
        b : float
            This value represents the intersection with the y axis
            and the new line.

        Returns
        -------
        line : callable
                A function that represents a line with
                slope `a` and `b` as intersection in the `y` axis.
        """

        def line(x):
            return a + b * x

        return line
    
    def set_feed(self, q, xF):
        """
        This function stores feed values
        q (relative heat)
        xF (Feed composition)
        """
        # To Do: Validate inputs if
        self.xF = xF
        self.q = q

        """
        if q == 1:
            raise Exception('Not implemented yet') #To do list
        return lambda x: q*x/(q-1) - xF/(q-1) 
        """

    def interpolate_data(self):
        self.x_data = np.linspace(self.x[0], self.x[-1], 100)
        self.y_data = pchint(self.x, self.y, self.x_data)

    def create_feed_line(self, q, xF):
        """
        Create feed line with q, xF
        Store the function
        Store feed method
        """
        if q == 1:
            raise Exception("Not implemented yet")  # To do list
        self.feed = lambda x: q * x / (q - 1) - xF / (q - 1)

    def reflux_min(self, x_in, y_in, x_D):
        k = (x_D - x_in) / (x_D - y_in)
        R = 1 / (k - 1)
        self.Rmin = R
        return R
    
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

    def solve(self):
        """
        Solve the system with the user inputs:
        q, xF, xD, xW
        """
        self.xe = []
        self.ye = []
        self.interpolate_data()
        self.create_feed_line(self.q, self.xF)
        # x_in y y_in punto de intersección con la curva de eq y feed
        x_int, y_int = self.find_intersection()
        self.x_int = x_int
        self.y_int = y_int
        r_min = self.reflux_min(x_int, y_int, self.xD)
        r = 1.5 * r_min
        self.line_recti = self.eq_line(self.xD / (r + 1), r / (r + 1))
        yF = self.line_recti(self.xF)
        slope = (self.xW - yF) / (self.xW - self.xF)
        origin = -slope * self.xF + yF
        self.line_strip = self.eq_line(origin, slope)

        xp = self.xD
        self.xe.append(self.xD)
        self.ye.append(self.xD)
        etapas = 0
        while xp > self.xW:
            line_xpn = self.eq_line(xp, 0)
            xpn, xp = self.inter_line(line_xpn, self.x_data, self.y_data)

            etapas += 1
            self.ye.append(xp)
            self.xe.append(xpn)

            if xpn > self.x_int:
                xp = self.line_recti(xpn)
            else:
                xp = self.line_strip(xpn)

            self.ye.append(xp)
            self.xe.append(xpn)

        self.steps = etapas

    def find_intersection(self, epsilon=1e-5):
        def difference_function(x):
            return self.y_data - self.feed(x)

        # Verifica el cambio de signo para encontrar intervalos que contienen la intersección
        sign_changes = np.where(np.diff(np.sign(difference_function(self.x_data))))[0]

        if len(sign_changes) == 0:
            return None

        intersections = []

        # Utiliza interpolación para encontrar la intersección en cada subintervalo
        for i in sign_changes:
            x_interval = self.x_data[i : i + 2]
            y_interval = self.y_data[i : i + 2]
            interpolator = interp1d(
                x_interval, y_interval, kind="linear", fill_value="extrapolate"
            )
            intersection = fsolve(
                lambda x: interpolator(x) - self.feed(x), np.mean(x_interval)
            )
            intersections.extend(intersection)

        

        return intersections[0], self.feed(np.array(intersections))[0]
    
    def describe(self):
        print('El reflujo mínimo es de: {}\n'
            'El composición líquida de salida: {}\n'.format(self.Rmin, self.xW))

        print('\nComposición de entrada y salida en cada etapa:')
        for etapa in range(self.steps + 1):
            x_in = self.xe[etapa]
            y_out = self.ye[etapa]
            print(f'Etapa {etapa + 1}: Entrada = {x_in:.4f}, Salida = {y_out:.4f}')

        print('\nNúmero total de etapas: {}'.format(self.steps))

    def plot(self):
        x_rect = np.linspace(self.x_int, self.xD, 50)
        y_rect = np.array([self.line_recti(x) for x in x_rect])
        _, ax = plt.subplots()
        x_strip = np.linspace(self.xW, self.x_int, 50)
        y_strip = np.array([self.line_strip(c) for c in x_strip])
        

        ax.plot(self.x_data, self.y_data, label="Equilibrium")
        ax.scatter(self.x_int, self.y_int, label = 'Intersección')
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
