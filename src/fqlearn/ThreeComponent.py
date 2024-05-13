import matplotlib as plt
import numpy as np
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
        self.fontsize = 7
        self.offset = 0.14
        self.tax.set_title("Ternary Phase Diagram\n", fontsize=10)
        self.tax.left_axis_label(
            "Mass fraction of C", fontsize=self.fontsize, offset=self.offset
        )
        self.tax.right_axis_label(
            "Mass fraction of B", fontsize=self.fontsize, offset=self.offset
        )
        self.tax.bottom_axis_label(
            "Mass fraction of A", fontsize=self.fontsize, offset=0.05
        )
        self.tax.left_corner_label("C", fontsize=9)
        self.tax.right_corner_label("A", fontsize=9)
        self.tax.top_corner_label("B", fontsize=9, offset=self.offset)
        self.tax.ticks(axis="lbr", linewidth=1, multiple=10, offset=0.02)

        self.tax.set_background_color(
            color="whitesmoke", alpha=0.7
        )  # the default, essentially

        # Initialize required variables
        self.right_eq_line = []
        self.left_eq_line = []
        self.points = self.right_eq_line + self.left_eq_line

    # Add points to the plot
    def add_point(self, points):
        # Check if points is an empty list
        if not points:
            raise ValueError(
                "The 'points' list cannot be empty. Please provide valid points."
            )

        # Remove duplicate points
        points_to_plot = list(set(points))

        # Multiply each point by 100
        points_to_plot = [(x * 100, y * 100, z * 100) for x, y, z in points_to_plot]

        # Plot the points
        self.tax.scatter(points_to_plot, linewidth=1.0, marker="o", color="red")
        return points_to_plot

    # Sort the added points
    def sort_points(self, points):
        points_to_plot = self.add_point(points)
        # Sort the points in ascending order
        xyz = [(x, y, z) for x, y, z in points_to_plot]
        sorted_points = sorted(xyz, key=lambda m: m[0])

        # New list to store sorted points
        new_sorted_points = []

        # Check if the points are in a list of lists or a single list
        if isinstance(
            sorted_points[0], (int, float)
        ):  # Check if the first element of points is a number
            assert sorted_points[0] + sorted_points[1] + sorted_points[2] == self.scale
            new_sorted_points.append(sorted_points)
        else:
            # If the points are in a list of lists
            for sorted_point in sorted_points:
                assert sorted_point[0] + sorted_point[1] + sorted_point[2] == self.scale
                new_sorted_points.append(sorted_point)

        # Plot the points
        self.tax.scatter(new_sorted_points, linewidth=1.0, marker="o", color="red")
        return new_sorted_points

    # Plot an equilibrium line joining the points on the right and left
    def add_eq_line(self, right_eq_line, left_eq_line):
        # Add the points
        self.right_eq_line = self.sort_points(right_eq_line)
        self.left_eq_line = self.sort_points(left_eq_line)
        eq_line = self.right_eq_line + self.left_eq_line

        # Remove duplicate points
        eq_line_plot = list(set(eq_line))

        # Sort the points in ascending order
        xyz = [(x, y, z) for x, y, z in eq_line_plot]
        sorted_eq = sorted(xyz, key=lambda m: m[0])

        self.tax.plot(sorted_eq, linewidth=1.0, color="blue", label="Equilibrium line")

    # Join the corresponding points of 2 solutes
    def solute_points(self, soluteA, soluteB):
        # Multiply each point by 100
        new_soluteA = [(x * 100, y * 100, z * 100) for x, y, z in soluteA]
        new_soluteB = [(x * 100, y * 100, z * 100) for x, y, z in soluteB]

        # Sort the points in ascending order
        xyz = [(x, y, z) for x, y, z in new_soluteA]
        sorted_soluteA = sorted(xyz, key=lambda m: m[0])
        xyz = [(x, y, z) for x, y, z in new_soluteB]
        sorted_soluteB = sorted(xyz, key=lambda m: m[0], reverse=True)

        for i in range(len(soluteA)):
            pointA = sorted_soluteA[i]
            assert sum(pointA) == self.scale
            pointB = sorted_soluteB[i]
            assert sum(pointB) == self.scale

            # Extract x and y coordinates of each point
            xA, yA, zA = pointA
            xB, yB, zB = pointB

            # Plot the two points
            self.tax.scatter([(xA, yA, zA), (xB, yB, zB)], marker="s", color="red")
            # Plot a line connecting the two points
            self.tax.plot(
                [(xA, yA, zA), (xB, yB, zB)],
                linewidth=1.0,
                color="blue",
            )
        i + 1

    # Calculate the slope between the points on the left and right
    def eq_slope(self, right_eq_line, left_eq_line):
        # Multiply each point by 100
        right_eq_line = [(x * 100, y * 100, z * 100) for x, y, z in right_eq_line]
        left_eq_line = [(x * 100, y * 100, z * 100) for x, y, z in left_eq_line]

        # Sort the points in ascending order
        xyz = [(x, y, z) for x, y, z in right_eq_line]
        right_eq = sorted(xyz, key=lambda m: m[0])
        xyz = [(x, y, z) for x, y, z in left_eq_line]
        left_eq = sorted(xyz, key=lambda m: m[0], reverse=True)

        slopes = []

        for i in range(len(right_eq_line)):
            pointA = right_eq[i]
            assert sum(pointA) == self.scale
            pointB = left_eq[i]
            assert sum(pointB) == self.scale

            # Extract x and y coordinates of each point
            xA, yA, _ = pointA
            xB, yB, _ = pointB

            # Calculate the slope of the line joining the points
            if xA - xB != 0:  # Check for vertical line
                slope = (yA - yB) / (xA - xB)
                slopes.append(slope)
            else:
                # For vertical lines, return None for slope
                slopes.append(0)
        i + 1
        print("Slope = ", slopes)

        # Calculate average of the slopes
        avg_slope = sum(slopes) / len(slopes)
        print("Average slope = ", avg_slope)
        return avg_slope

    # Interpolate the points
    def interpolate_points(self, points):
        sorted_points = self.sort_points(points)

        # Cubic spline interpolation
        x = [x for x, y, z in sorted_points]
        y = [y for x, y, z in sorted_points]

        f = CubicSpline(x, y, bc_type="natural")
        x_cubic = np.linspace(0, 100, 100)
        y_cubic = f(x_cubic)

        # Remove negative points
        interpolated_points = [
            [i, j]
            for i, j in np.column_stack((x_cubic, y_cubic))
            if 0 <= i <= 100 and 0 <= j <= 100
        ]

        return interpolated_points

    # Calculate the derivative of the interpolated points
    def derivative(self, points):
        points_to_derive = self.interpolate_points(points)

        # Extract x and y values
        x = [x for x, _ in points_to_derive]
        y = [y for _, y in points_to_derive]

        # Calculate derivative
        dydx = np.diff([y]) / np.diff([x])

        return dydx

    # Calculate the index of the point halving the equilibrium line
    def min_diff(self, right_eq_line, left_eq_line):
        self.points = right_eq_line + left_eq_line
        dydx = self.derivative(self.points)
        avg_slope = self.eq_slope(right_eq_line, left_eq_line)

        min_index = 0
        # Initialize min_diff_value with the first element difference
        min_diff_value = abs(dydx[0][0] - avg_slope)

        # Iterate over indices of dydx to find the index with the derivative value closest to the average slope
        for index in range(0, dydx.size):
            diff = abs(dydx[0][index] - avg_slope)
            if diff < min_diff_value:
                min_diff_value = diff
                min_index = index

        return min_index

    # Divide the equilibrium line in half
    def div_half(self, right_eq_line, left_eq_line):
        # Add the points
        self.points = right_eq_line + left_eq_line
        interpolated_points = self.interpolate_points(self.points)

        # Use index to separate right and left side
        index = self.min_diff(right_eq_line, left_eq_line)
        self.interpolated_right_side = interpolated_points[index:]
        self.interpolated_left_side = interpolated_points[: index + 1]

        # Plot the curve
        self.tax.plot(
            self.interpolated_right_side,
            linewidth=1.0,
            color="blue",
            label="Right interpolated curve",
        )
        self.tax.plot(
            self.interpolated_left_side,
            linewidth=1.0,
            color="orange",
            label="Left interpolated curve",
        )

    # To generate the plot
    def plot(self):
        self.tax.clear_matplotlib_ticks()
        self.tax.get_axes().axis("off")
        self.tax.legend()
        ternary.plt.show()
