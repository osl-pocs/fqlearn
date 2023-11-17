import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve


class Point:
    def __init__(self, df):
        self.df = df

    def create_feed_line(self, q, xf):
        if q == 1:
            raise Exception("Not implemented yet")  # To do list
        return lambda x: q * x / (q - 1) - xf / (q - 1)

    def find_intersection(self, q, xf, epsilon=1e-5):
        feed = self.create_feed_line(q, xf)
        x_values = self.df["x"].values
        y_values = self.df["y"].values

        def difference_function(x):
            return y_values - feed(x)

        # Verifica el cambio de signo para encontrar intervalos que contienen la intersección
        sign_changes = np.where(np.diff(np.sign(difference_function(x_values))))[0]

        if len(sign_changes) == 0:
            return None

        intersections = []

        # Utiliza interpolación para encontrar la intersección en cada subintervalo
        for i in sign_changes:
            x_interval = x_values[i : i + 2]
            y_interval = y_values[i : i + 2]
            interpolator = interp1d(
                x_interval, y_interval, kind="linear", fill_value="extrapolate"
            )
            intersection = fsolve(
                lambda x: interpolator(x) - feed(x), np.mean(x_interval)
            )
            intersections.extend(intersection)

        return intersections

    def plot_intersection(self, q_guess, xf_guess):
        intersections = self.find_intersection(q_guess, xf_guess)

        x_values = self.df["x"].values
        y_values = self.df["y"].values

        feed = self.create_feed_line(q_guess, xf_guess)
        y_feed = feed(x_values)

        print(intersections, feed(np.array(intersections)))

        plt.plot(x_values, y_values, label="Línea de equilibrio")
        plt.plot(x_values, y_feed, label="Feed line")
        plt.scatter(
            intersections,
            feed(np.array(intersections)),
            color="red",
            label="Intersección",
        )
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.show()

        return (intersections, feed(np.array(intersections)))

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
