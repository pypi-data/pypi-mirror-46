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
