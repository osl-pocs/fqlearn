import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.optimize import fsolve

from utils.hermite import pchint


class McCabeThiele:
    def __init__(self):
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
        self.compound_a = None
        self.compound_b = None

    def volarel(self, alfa, compuesto1, compuesto2):
        """
        Redefine this function if there and volatility value
        there is no need the create a table
        """
        x = np.arange(0, 1.1, 0.1)
        y = []

        for i in range(len(x)):
            o = (alfa * x[i]) / (1 + x[i] * (alfa - 1))
            y.append(o)

        data = {'x': x, 'y': y}
        df = pd.DataFrame(data)

        nombre_archivo = f"src/data/{compuesto1}-{compuesto2}.csv"

        df.to_csv(nombre_archivo, index=False)

        print(f"Datos guardados en {nombre_archivo}")
        return nombre_archivo

    def set_data(self, compound_a: str, compound_b: str) -> None:
        """
        Open the liquid-vapor equilibrium data for the two compounds compound_a and compound_b.

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
        If there is no matches for the compounds names, prints a message indicating that there are no matches for the compounds names.
        """

        #TODO: Use volatity as an input variable for the function
        # instead of asking in the command terminal
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
                    f"No hay datos disponibles para el par de compuestos {self.compound_a}-{self.compound_b}"
                )
                alfa = int(input('Alfa = '))
                self.alfa = alfa
                nuevo_archivo = self.volarel(alfa, self.compound_a, self.compound_b)
                df = pd.read_csv(nuevo_archivo)
                self.x = df["x"].tolist()
                self.y = df["y"].tolist()
        else:
            print("No hay datos disponibles para ese par de compuestos\n"
                  "¿Deseas usar el índice de volatilidad relativa?")
            answ = int(input('1. YES\n2. NO\n'))
            if answ == 1:
                alfa = int(input('Alfa = '))
                self.alfa = alfa

                nuevo_archivo = self.volarel(alfa, compound_a, compound_b)
                df = pd.read_csv(nuevo_archivo)
                self.x = df["x"].tolist()
                self.y = df["y"].tolist()
                self.compound_a = compound_a
                self.compound_b = compound_b

    def set_compositions(self, xD, xW):
        """
        xD (Composition at the distilate)
        xW (Composition in the liquid)
        """

        # TODO: Change language messages to english
        if 0 <= xD <= 1 and 0 <= xW <= 1:
            self.xD = xD
            self.xW = xW
        else:
            print('Por favor, introduce solo valores válidos\n'
                  'Revisa los valores introducidos\n'
                  'xD = {}\n'
                  'xW = {}'.format(xD, xW))


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
        if 0 <= q <= 1 and 0 <= xF <= 1:
            self.xF = xF
            self.q = q
        else:
            print('Por favor, introduce solo valores válidos\n'
                  'Revisa los valores introducidos\n'
                  'q = {}\n'
                  'xF = {}'.format(q, xF))

        # TODO: Change language messages to english
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
            #TODO: implement when q == 1
            raise Exception("Not implemented yet")  # To do list
        self.feed = lambda x: q * x / (q - 1) - xF / (q - 1)

    def reflux_min(self, x_in, y_in, x_D):
        """
        This function calculate reflux
        """
        k = (x_D - x_in) / (x_D - y_in)
        R = 1 / (k - 1)
        self.Rmin = R
        return R
    
    def inter_line(self, line, data_x, data_y):
        #TODO: Refactor this code make it better
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

    def create_rect_line(self):
        r =self.r
        xD = self.xD
        def _create_rect_line(x):
            return (r*x+xD)/(r+1)
        self.rect_line = _create_rect_line
    
    def line_intersection(self, line1, line2):
        x = (line1(0)-line2(0))/(line1(0)-line2(0)-line1(1)+line2(1))
        return x, line2(x)

    def create_strip_line(self):
        # Rename x,y, these are intersection points rect line and feed line
        x, y = self.line_intersection(self.feed, self.rect_line)
        slope = (self.xW - y) / (self.xW - x)
        origin = -slope * x + y
        self.rx_int = x
        self.ry_int = y
        self.strip_line = self.eq_line(origin, slope)

    def solve(self):
        """
        Solve the system with the user inputs:
        q, xF, xD, xW
        """
        # xe, ye stores the values of the ladder
        self.xe = []
        self.ye = []
        
        self.interpolate_data()
        self.create_feed_line(self.q, self.xF)
        # x_in y y_in punto de intersección con la curva de eq y feed
        x_int, y_int = self.find_intersection()
        self.x_int = x_int
        self.y_int = y_int

        self.r_min = self.reflux_min(x_int, y_int, self.xD)
        self.r = 1.5 * self.r_min

        self.create_rect_line()

        self.yF = self.rect_line(self.xF)
        
        self.create_strip_line()

        xp = self.xD
        self.xe.append(self.xD)
        self.ye.append(self.xD)
        steps = 0

        while xp > self.xW:
            line_xpn = self.eq_line(xp, 0)
            xpn, xp = self.inter_line(line_xpn, self.x_data, self.y_data)

            steps += 1
            self.ye.append(xp)
            self.xe.append(xpn)

            if xpn > self.rx_int:
                xp = self.rect_line(xpn)
            else:
                xp = self.strip_line(xpn)

            self.ye.append(xp)
            self.xe.append(xpn)

        self.steps = steps

    def find_intersection(self):
        a = 0
        b = len(self.x_data)

        def _find_intersection(a, b):
            if a + 1 == b:
                return a, b
            m = (a+b)//2
            signal_change = (self.y_data[m]-self.feed(self.x_data[m]))*(self.y_data[a]-self.feed(self.x_data[a]))
            
            if signal_change < 0:
                b = m
            else:
                a = m

            return _find_intersection(a, b)
        
        def intersection(line, x1,y1,x2,y2):
            x = x1 + (y1 - line(x1))*(x2 - x1)/(line(x2) - line(x1) - y2 + y1)
            return x, line(x)
        
        print(_find_intersection(a, b))
        ida, idb = _find_intersection(a, b)
        x1, y1 =  self.x_data[ida], self.y_data[ida]
        x2, y2 = self.x_data[idb], self.y_data[idb]

        x_int, y_int = intersection(self.feed, x1,y1,x2,y2)

        return x_int, y_int
    
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
        x_rect = np.linspace(self.rx_int, self.xD, 50)
        y_rect = np.array([self.rect_line(x) for x in x_rect])
        _, ax = plt.subplots()
        x_strip = np.linspace(self.xW, self.rx_int, 50)
        y_strip = np.array([self.strip_line(c) for c in x_strip])
        
        ax.plot(self.x_data, self.y_data, label="Equilibrium")
        ax.scatter(self.x_int, self.y_int, marker = '*', c = 'red',label = 'Intersección')
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
