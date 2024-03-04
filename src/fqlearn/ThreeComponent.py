import ternary
import matplotlib

# Make images higher resolution and set default size
matplotlib.rcParams['figure.dpi'] = 200
matplotlib.rcParams['figure.figsize'] = (4, 4)

# This class plots a ternary phase diagrams using triangular axes
class ThreeComponent:
    def __init__(self):
        self.scale = 100
        self.figure, self.tax = ternary.figure(scale=self.scale)
        self.tax.boundary(linewidth=1.5)
        self.tax.gridlines(color="black", multiple=6)
        self.tax.gridlines(color="blue", multiple=2, linewidth=0.5)
        self.fontsize = 8
        self.offset = 0.14
        self.tax.set_title("Three Component Phase Diagram\n", fontsize=self.fontsize)
        self.tax.left_axis_label("Mass fraction of C", fontsize=self.fontsize, offset=self.offset)
        self.tax.right_axis_label("Mass fraction of B", fontsize=self.fontsize, offset=self.offset)
        self.tax.bottom_axis_label("Mass fraction of A", fontsize=self.fontsize, offset=self.offset)

        self.tax.ticks(axis='lbr', linewidth=1, multiple=10, offset=0.02)

        self.tax.set_background_color(color="whitesmoke", alpha=0.7) # the detault, essentially
            
    def plot(self):
        self.tax.clear_matplotlib_ticks()
        self.tax.get_axes().axis('off')

        ternary.plt.show()

model = ThreeComponent()
model.plot()
