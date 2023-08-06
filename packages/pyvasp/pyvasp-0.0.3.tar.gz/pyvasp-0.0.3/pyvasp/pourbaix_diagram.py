import numpy as np
import matplotlib.pyplot as plt

def getStable(pH, potential, energy):
    chemPotential = energy[:, 1] - (3.38 + 0.059*pH + potential) * energy[:, 0]
    return int(energy[np.argmax(chemPotential), 0])


def gridPlot(grid, species):
    pH = np.linspace(-2, 16, grid)
    potential = np.linspace(-2, 2, grid)
    X, Y = np.meshgrid(pH, potential)
    
    energy = np.loadtxt(species + '.dat')
    energy[:, 1] = energy[0, 1] - energy[:, 1]

    def test_line(pH):
        return energy[-1, 1] / energy[-1, 0] - 3.73 - 0.059 * pH
    
    Z = np.zeros([grid, grid])
    for i in range(grid):
        for j in range(grid):
            Z[i, j] = getStable(X[i, j], Y[i, j], energy)

    plt.cla()
    plt.pcolor(X, Y, Z, cmap='Blues')
    plt.plot(pH, test_line(pH), 'orange')
    plt.colorbar()
    plt.xlabel('pH at 298.15K')
    plt.ylabel('Potential / V')
    plt.title(species + 'Pourbaix diagram')
#   plt.annotate(species, xy=(2, -1.5))
#   plt.annotate(species + 'H', xy=(10, 1.5))
    plt.savefig(species + '.png', dpi=500)
    plt.show()
