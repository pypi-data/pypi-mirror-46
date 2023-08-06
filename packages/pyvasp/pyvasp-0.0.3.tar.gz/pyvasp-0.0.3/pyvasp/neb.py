import numpy as np
import matplotlib.pyplot as plt 
from numpy import sqrt, exp, power
from functions import Slice, getInfo
from scipy.integrate import quad
from scipy.interpolate import splrep, splev, InterpolatedUnivariateSpline
from scipy.constants import physical_constants, k, h, hbar, pi

k_in_ev = physical_constants['Boltzmann constant in eV/K'][0]

def getBarr():
    '''get energies of N images
    Return:
        maxEnergyIndex: int
        maxEnergy: float
        relativeEnergy: ndarray
    '''
    nimage = int(getInfo('INCAR', 'IMAGES', 2))
    energies = np.zeros(nimage+2)
    for ii in range(nimage+2):
        energies[ii] = float(getInfo(f'0{ii:d}/OUTCAR', 'entropy=', 6))

    return (np.argmax(energies),
            np.max(energies - energies[0]),
            energies - energies[0])

def plotBarr():
    _, _, iy = getBarr()
    ix = np.arange(iy.shape[0])
    fx = np.linspace(ix.min(), ix.max(), 500)

    tck = splrep(ix, iy, s=0)
    fy = splev(fx, tck, der=0)
    # another plot method
    # fy = InterpolatedUnivariateSpline(ix, iy)(xx)

    plt.plot(fx, fy, color='red')
    plt.scatter(ix, iy)
    plt.show()

def getFreq(file):
    '''return freq in eV
    Args:
        file: string
    
    Return:
        realFreq: ndarray
        imagFreq: ndarray
    '''
    realFreq = np.array(getInfo(file, 'f  =', 9, last=False)).astype(float)
    imagFreq = np.array(getInfo(file, 'f/i=', 8, last=False)).astype(float)

    return realFreq / 1000, imagFreq / 1000

def zpe(freqArray):
    '''return zero point energy in eV
    '''
    return 1 / 2 * np.sum(freqArray)

def preFactor(freqIS, freqTS, T):
# another method
#   return (k * T / h * np.prod(exp(-TS_freq / 2 / k_in_ev / T) / 
#           (1 - exp(-TS_freq / k_in_ev / T))) /
#           np.prod(exp(-IS_freq / 2 / k_in_ev / T) /
#           (1 - exp(-IS_freq / k_in_ev / T))))

    return (k * T / h * np.prod(1 - exp(- freqIS / k_in_ev / T))
            / np.prod(1 - exp(- freqTS / k_in_ev / T)))


def rateConstant(pattern, T):
    index, Eb, _ = getBarr()
    freqIS, _ = getFreq(f'00/fvib/{pattern:}/OUTCAR')
    freqTS, _ = getFreq(f'0{index:}/fvib/{pattern:}/OUTCAR')
    Ebc = Eb + zpe(freqTS) - zpe(freqIS)
    return Ebc, preFactor(freqIS, freqTS, T) * exp(- Ebc / k_in_ev / T)

def kie(T=300):
    _, Eb, _ = getBarr()
    EbcH, rH = rateConstant('H', T)
    EbcD, rD = rateConstant('D', T)
    EbcT, rT = rateConstant('T', T)
    print(Eb, EbcH, rH, EbcD, rD, EbcT, rT, rH/rT, rH/rD, rD/rT)

def tunnelingRate(mass, barrHeight, barrWidth, deltaZPE, hbarByOmega,
                  T, coiEne):
    '''
    Args:
        mass: mass of hydrogen isotopes.
        barrHeight: barrier height in eV from one coincidence state to another.
        barrWidth: barrier height in A from one coincidence state to another.
        deltaZPE: zpe difference between coincidence state and transition state
            from one coincidence state to another.
        hbarByOmega: vibrational energy of hydrogen in eV at the coincidence
            state, which can claculate from summing the vasp vibration energy
            of hydrogen on three directions.
        T: temperature.
        coiEne: coincidence energy from self-trapped state from to coincidence
            state.
    Returns:
        tunneling rate of phonon-assistanted.
    '''
    def integrand(x, mass, barrHeight, barrWidth, deltaZPE):
        return sqrt(2 * mass * (4 * barrHeight / power(barrWidth, 2)
                                * power(x, 2) - barrHeight - deltaZPE))
    
    lower = - barrWidth / 2 * sqrt((barrHeight + deltaZPE) / barrHeight)
    upper = + barrWidth / 2 * sqrt((barrHeight + deltaZPE) / barrHeight)
    # tunneling matrix element
    jtm = 0.5 * hbarByOmega / pi * exp(- quad(integrand, lower, upper) / hbar)
    
    return (sqrt(pi / coiEne / k_in_ev / T) * power(jtm, 2) / 2 / hbar
            * exp(- coiEne / k_in_ev / T))

# TODOdo write barrier
#   if args.bg:
#       _, barr, barrSeries = neb.getBarr()
#       print(f'{barr:.8f}')
#       with open('barr.dat', 'w') as f:
#           for img in barrSeries:
#               f.write(f'{img:.8f}\n')
