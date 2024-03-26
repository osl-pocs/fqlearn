import matplotlib as plt
import numpy as np
import pandas as pd
import ternary
from scipy.interpolate import CubicSpline

# Make images higher resolution and set default size
plt.rcParams["figure.dpi"] = 200
plt.rcParams["figure.figsize"] = (4, 4)


# This class plots a ternary phase diagrams using triangular axes
class ThreeComponent:
    def __init__(self):
        self.scale = 100
        self.figure, self.tax = ternary.figure(scale=self.scale)
        self.tax.boundary(linewidth=1.5)
        self.tax.gridlines(color="black", multiple=6)
        self.tax.gridlines(color="blue", multiple=2, linewidth=0.5)
        self.fontsize = 8
        # self.tax.ticks(fontsize=5)
        self.offset = 0.14
        self.tax.set_title("Three Component Phase Diagram\n", fontsize=self.fontsize)
        self.tax.left_axis_label(
            "Mass fraction of C", fontsize=self.fontsize, offset=self.offset
        )
        self.tax.right_axis_label(
            "Mass fraction of B", fontsize=self.fontsize, offset=self.offset
        )
        self.tax.bottom_axis_label(
            "Mass fraction of A", fontsize=self.fontsize, offset=self.offset
        )
        self.tax.left_corner_label("C", fontsize=self.fontsize)
        self.tax.right_corner_label("A", fontsize=self.fontsize)
        self.tax.top_corner_label("B", fontsize=self.fontsize)
        self.tax.ticks(axis="lbr", linewidth=1, multiple=10, offset=0.02)

        self.tax.set_background_color(
            color="whitesmoke", alpha=0.7
        )  # the default, essentially

        self.points = []
        self.right_eq_line = []
        self.left_eq_line = []

    # To add points to the plot
    def add_point(self, points):
        # Check if points is a list of lists or a single list
        if isinstance(
            points[0], (int, float)
        ):  # Check if the first element of points is a number
            assert points[0] + points[1] + points[2] == self.scale
            self.points.append(points)
        else:
            # If points is a list of lists
            for point in points:
                assert point[0] + point[1] + point[2] == self.scale
                self.points.append(point)
        self.tax.scatter(
            self.points, linewidth=1.0, marker="o", color="blue", label="Points"
        )
        return self.points

    # To plot equilibrium line joining the points
    def eq_line(self, points):
        self.add_point(points)
        self.tax.plot(points, linewidth=1.0, label="Equilibrium line")
        return self.points

    # To join the corresponding points of 2 solutes
    def solute_points(self, soluteA, soluteB):
        for i in range(len(soluteA)):
            pointA = soluteA[i]
            assert sum(pointA) == self.scale
            pointB = soluteB[i]
            assert sum(pointB) == self.scale
            # Extract x and y coordinates of each point
            xA, yA, zA = pointA
            xB, yB, zB = pointB
            # Plot the two points
            self.tax.scatter(
                [(xA, yA, zA), (xB, yB, zB)], marker="s", color="blue", label="Points"
            )
            # Plot a line connecting the two points
            self.tax.plot(
                [(xA, yA, zA), (xB, yB, zB)],
                linewidth=1.0,
                color="green",
                label="Plotted curve",
            )
        i + 1
        self.points.extend(soluteA)
        self.points.extend(soluteB)
        return self.points

    # Cubic spline interpolation of the points
    def interpolate(self, points):
        # Remove duplicate points
        new_points = list(set(points))

        # Multiply each point by 100
        new_points = [(x * 100, y * 100, z * 100) for x, y, z in new_points]

        xyz = [(x, y, z) for x, y, z in new_points]
        sorted_points = sorted(xyz, key=lambda m: m[0])
        x = [x for x, y, z in sorted_points]
        y = [y for x, y, z in sorted_points]
        z = [z for x, y, z in sorted_points]

        # Plot the points
        self.tax.scatter(
            sorted_points, linewidth=1.0, marker="o", color="blue", label="Points"
        )

        # Cubic spline interpolation
        f = CubicSpline(x, y, bc_type="natural")
        x_cubic = np.linspace(0, 100, 100)
        y_cubic = f(x_cubic)

        # Remove negative points
        points_to_plot = [
            [i, j]
            for i, j in np.column_stack((x_cubic, y_cubic))
            if 0 <= i <= 100 and 0 <= j <= 100
        ]

        # Plot the curve
        self.tax.plot(points_to_plot, linewidth=1.0, label="Interpolated curve")

    # To generate the plot
    def plot(self):
        self.tax.clear_matplotlib_ticks()
        self.tax.get_axes().axis("off")
        self.tax.legend()
        ternary.plt.show()
