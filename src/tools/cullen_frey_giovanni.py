########################################################################################################################
# Print Cullen-Frey chart
#
# Written by Rian Koja and Giovani Guarnieri to publish in a GitHub repository with specified licence.
########################################################################################################################


# Standard imports:
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.stats import skew, kurtosis


def cullenfrey(skews, kurt, legend, title):
    xd = [s*s for s in skews]
    yd = kurt
    poly_x1 = max([4, max(xd) * 1.1])
    poly_y1 = poly_x1 + 1
    poly_y2 = 1.5 * poly_x1 + 3
    y_lim = max([poly_y2,  10, max(yd) * 1.1])

    x = [0, poly_x1, poly_x1, 0]
    y = [1, poly_y1, poly_y2, 3]

    # Prepare poligonal region:
    scale = 1
    step = max([0.1, poly_x1/1000])
    poly = Polygon(np.c_[x, y]*scale, facecolor='#1B9AAA', edgecolor='#1B9AAA', alpha=0.5)

    fig, ax = plt.subplots()
    ax.add_patch(poly)
    # colors = ['b', 'g', 'r', 'c', 'm', 'y']
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
              'tab:olive', 'tab:cyan']
    for xx, yy, label, color, in zip(xd, yd, legend, colors):
        ax.plot(xx, yy, marker="o", label=label, linestyle='', c=color)
    ax.plot(0, 4.187999875999753, label="logistic", marker='+', c='black', linestyle='None')
    ax.plot(0, 1.7962675925351856, label="uniform", marker='^', c='black', linestyle='None')
    ax.plot(4, 9, label="exponential", marker='s', c='black', linestyle='None')
    ax.plot(0, 3, label="normal", marker='*', c='black', linestyle='None')
    ax.plot(np.arange(0, poly_x1, step), 3/2. * np.arange(0, poly_x1, step) + 3, label="gamma", linestyle='-',
            c='black')
    ax.plot(np.arange(0, poly_x1, step), 2 * np.arange(0, poly_x1, step) + 3, label="lognormal", linestyle='-.',
            c='black')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
    ax.set_ylim(y_lim, 0)
    ax.set_xlim(-0.2, poly_x1)
    ax.grid('both')
    plt.xlabel("Skewness²")
    plt.title(title + ": Cullen and Frey map")
    plt.ylabel("Kurtosis")
    plt.tight_layout()
    plt.draw()


# Example usage:
if __name__ == "__main__":
    cullenfrey([0.5, 2], [0.5, 2], ["Example legend 1", "Example legend 2"], "Example title")
    plt.show()
