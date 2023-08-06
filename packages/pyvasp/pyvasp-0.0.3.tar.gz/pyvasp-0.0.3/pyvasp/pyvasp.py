#DESCRIPTION: a command line tool for vasp
#LICENSE: MIT
#AUTHOR: Wenbo Fu
#MAIL: ltaiwb@outlook.com
#VERSION: 0.0.3

from job import sub_vasp

def main():
    import argparse
    
    # main args
    parser = argparse.ArgumentParser(
        prog='pv', prefix_chars='-',
        description='Multi-option python program for VASP calculation and data')

    parser.add_argument(
        '-b', dest='barr', action='store_true',
        help='get the neb barrier')
    parser.add_argument(
        '-c', dest='check', action='store_true',
        help='check the input file')
    parser.add_argument(
        '--cp', dest='cp2k', action='store_true',
        help='convert POSCAR to cp2k file')
    parser.add_argument(
        '--centre', dest='centre', action='store_true',
        help='set centre of POSCAR')
    parser.add_argument(
        '--fix', dest='fix', action='store', nargs=2,
        help='set fix of nth X element')
    parser.add_argument(
        '--ne', dest='nelect', action='store_true',
        help='print the number of electrons from POSCAR and POTCAR')
    parser.add_argument(
        '--rs', dest='resize', action='store_true',
        help='reform the lattice')
    parser.add_argument(
        '-f', dest='fp', metavar='N',
        nargs='?', const=0, default=None, type=int,
        help='plot max-force vs ion-step from Nth (default: %(const)s) step')
    parser.add_argument(
        '-g', dest='bg', action='store_true',
        help='get energy barrier')
    parser.add_argument(
        '-m', dest='mp', metavar='N',
        nargs='?', const=0, default=None, type=int,
        help='plot Ek, Ep, T, Etot of md from Nth (default: %(const)s) fs')
    parser.add_argument(
        '-p', dest='bp', action='store_true',
        help='plot barrier energy vs images from barrier file')
    parser.add_argument(
        '-r', dest='kie', action='store_true',
        help='print the reaction rate constant')

    # sub commands
    subparser = parser.add_subparsers(title='sub-commands', dest='subcmd',
                                      description='useful sub commands')

    # sub command job
    jobparser = subparser.add_parser('job',
                                     help='vasp job control')
    jobparser.add_argument(
        '-q', dest='queue',default='high',
        help='queue name')
    jobparser.add_argument(
        '-p', dest='ppn', default=28, type=int,
        help='No. of processors of each node')
    jobparser.add_argument(
        '-n', dest='node', default=1, type=int,
        help='No. of node')
    jobparser.add_argument(
        '-m', dest='mode', default='std',
        help='vasp version')
    jobparser.add_argument(
        '--name', dest='name', default='std',
        help='job name')
    jobparser.add_argument(
        '--fname', dest='fname', default='stdout',
        help='output file name')
    jobparser.set_defaults(func=sub_vasp)

    args = parser.parse_args()

    if args.barr:
        from neb import getBarr
        _, x, _ = getBarr()
        print(x)

    if args.check:
        try:
            assert Poscar('POSCAR').nums.keys() == Potcar(
                'POTCAR').potDict.keys(), 'Error: POTCAR does not match POSCAR'
            print('check success')
        except AssertionError as error:
            print(str(error))

    if args.cp2k:
        from files import Poscar
        from linecache import getlines
        
        pos = Poscar('POSCAR')
        inp = getlines('inp')
        vector_id = ('A', 'B', 'C')
        
        cell_index = inp.index('    &END CELL\n')
        for i in range(3):
            vector = pos.lattice[i, :].tolist()
            inp.insert(cell_index + i,
                       '      {}{:20.16f}{:20.16f}{:20.16f}\n'.format(vector_id[i], *vector))
        
        coord_index = inp.index('    &END COORD\n')
        for element, coors in pos.coorDict.items():
            cnt = 0
            for coor in coors:
                inp.insert(coord_index + cnt,
                           '      {:<2s}{:20.16f}{:20.16f}{:20.16f}\n'.format(element, *coor))
                cnt += 1
        
        with open('inp', 'w') as f:
            f.write(''.join(inp))

    if args.centre:
        from files import Poscar
        pos = Poscar('POSCAR')
        pos.setCentre()
        pos.write(pos.coors)

    if args.fix:
        from files import Poscar
        pos = Poscar('POSCAR')
        pos.setFix(args.fix[0], int(args.fix[1]))
        pos.write(arr=pos.coors)

    if args.nelect:
        from files import Poscar, Potcar
        pos = Poscar('POSCAR')
        pot = Potcar('POTCAR')
        nelect = 0
        for element, num in pos.nums.items():
            nelect += num * pot.potDict[element][1]
        print(int(nelect))

    if args.resize:
        from files import Poscar
        from functions import vec_resize
        pos = Poscar('POSCAR')
        pos.write(arr=vec_resize(pos.coors))

    if args.fp != None:
        import opt
        opt.force_plot(args.fp)

    if args.mp != None:
        import md
        md.md_plot(args.mp)

    if args.bp:
        import neb
        neb.barr_plot()

    if args.kie:
        import neb
        neb.kie()

    if args.subcmd == 'job':
        args.func(args)
