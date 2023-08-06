import re
import numpy as np
from scipy.signal import savgol_filter

def md_plot(start_step):
    import subprocess as sp
    import numpy as np
    import matplotlib.pyplot as plt 

    sh_cmd = ("grep POTIM INCAR | awk '{print $3}'",
              "grep T= OSZICAR | awk '{printf(\"%f %f %f %f %f\\n\", $1, $11, $3, $7, $5)}'")

    timestep = float(sp.run(sh_cmd[0], stdout=sp.PIPE ,shell=True).stdout)
    tmp = sp.run(sh_cmd[1], stdout=sp.PIPE ,shell=True).stdout.decode()
    data = np.array([i.split() for i in tmp.splitlines()]).astype(float)
    data[:, 0] *= timestep

    plt_list = [data[start_step:, i+1] for i in range(4)]
    label_list = ['Kinetic Energy', 'Temperature', 'Potential Energy', 'Total Energy']
    unit_list = ['eV', 'T', 'eV', 'eV']
    for i in range(4):
        plt.subplot(2,2,i+1)
        plt.plot(data[start_step:, 0], plt_list[i], 'red', label=label_list[i])
        plt.xlim((np.min(data[start_step:, 0]), np.max(data[start_step:, 0])))
        plt.ylim((np.min(plt_list[i]), np.max(plt_list[i])))
        plt.xlabel('step/fs', {'fontsize':'large', 'verticalalignment':'center', 'horizontalalignment':'center'})
        plt.ylabel(label_list[i]+'/'+unit_list[i], {'fontsize':'large', 'verticalalignment':'center', 'horizontalalignment':'center'})
        plt.title(label_list[i], {'fontsize':'xx-large', 'fontweight':'medium'}, color='g')
    plt.tight_layout() 
    plt.show()


def bias_potential(cv_array, hill_bin, hill_height, hill_width):
    """
    Calculate the time-denpendent bias potntial of metadynamics
    """
    nstep = cv_array.shape[0]
    steps = np.arange(nstep) + 1
    bias = np.zeros(nstep)
    for step in steps[hill_bin-1:]:
        sum_bias_index = np.floor(step / hill_bin).astype(int)
        for bi in range(sum_bias_index):
            bias[step-1] += hill_height * np.exp(
                - np.power(cv_array[step-1] - cv_array[(bi+1)*hill_bin-1], 2)
                / 2 / np.power(hill_width, 2))
    return bias

def fep(cv_fname, ene_fname):
    """
    Plot free energy profile of metadynamics
    """
    cv = np.loadtxt(cv_fname)
    ene =np.loadtxt(ene_fname)
    index = np.argsort(cv)
    rene = np.flip(ene[index])
    cv.sort()
    y = savgol_filter(rene, 3001, 3)
    plt.plot(cv, y-y.min())
    # plt.plot(cv, rene-rene.min())
    plt.show()
