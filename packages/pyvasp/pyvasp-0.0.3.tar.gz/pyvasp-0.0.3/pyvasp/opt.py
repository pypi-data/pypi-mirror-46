
def force_plot(start_step):
    import subprocess as sp
    import numpy as np
    import matplotlib.pyplot as plt 

    sh_cmd = ("grep 'ions per type' OUTCAR | awk '{print $5+$6+$7+$8+$9+$10}'",
              "grep -A {} TOTAL-FORCE OUTCAR",
              "grep EDIFFG INCAR| awk '{print $3}'")
    
    atomNum = int(sp.run(sh_cmd[0], stdout=sp.PIPE ,shell=True).stdout)
    forceCriterion = -1*float(sp.run(sh_cmd[2], stdout=sp.PIPE ,shell=True).stdout)
    tmp1 = sp.run(sh_cmd[1].format(atomNum+1, atomNum), stdout=sp.PIPE ,shell=True).stdout.decode().splitlines()
    ionStep = int((len(tmp1)+1)/(atomNum+3))
    
    tmp2 = []
    for i in range(1, ionStep+1):
        tmp2[((i-1)*atomNum):(i*atomNum-1)] = tmp1[((i-1)*atomNum+i*3-1):(i*atomNum+i*3-1)]
    
    data = np.array([i.split() for i in tmp2]).astype(float)
    
    max_force = np.zeros((ionStep, 3))
    for j in range(ionStep):
        max_force[j, :] = np.max(np.abs(data[(j*atomNum):((j+1)*atomNum-1), 3:]), axis=0)
    
    step = [k+1 for k in range(ionStep)]
    list = ['x', 'y', 'z']
    for l in range(3):
        plt.plot(step[start_step:], max_force[start_step:, l], label=list[l])
    plt.xlim((np.min(step[start_step:]), np.max(step[start_step:])))
    plt.hlines(forceCriterion, np.min(step[start_step:]), np.max(step[start_step:]))
    plt.xlabel('step')
    plt.ylabel('max_force/eV*A-1')
    plt.legend()
    plt.show()
