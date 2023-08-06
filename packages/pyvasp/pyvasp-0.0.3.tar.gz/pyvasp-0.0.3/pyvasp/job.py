import os
from dataclasses import dataclass
@dataclass
class Sub_args(object):
    queue: str
    ppn: int
    node: int
    mode: str
    name: str
    fname: str

def sub_vasp(args):
    import os
    import logging
    import subprocess as sp

    file_doc = f"""#PBS -N {args.name}
#PBS -l nodes={args.node}:ppn={args.ppn}
#PBS -q {args.queue}
#PBS -j oe
#PBS -r n
#PBS -o {args.fname}

NP=`cat $PBS_NODEFILE |wc -l`
cd $PBS_O_WORKDIR

date
mpirun -np $NP -machinefile $PBS_NODEFILE /public/ltaiwb/app/vasp/{args.queue}/vasp_{args.mode} 2>&1
date
"""

    logging.basicConfig(filename=os.path.join(os.getenv('HOME'), 'zrecords'),
                        format='%(asctime)s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        level=logging.INFO)

    with open('vasp.pbs', 'w') as f:
        f.write(file_doc)
    msg = sp.run('qsub vasp.pbs', stdout=sp.PIPE ,shell=True).stdout.decode()
    jobid = int(msg.split('.')[0])
    logging.info(f'No. {jobid}{args.queue:>7s} {os.getcwd()}')
