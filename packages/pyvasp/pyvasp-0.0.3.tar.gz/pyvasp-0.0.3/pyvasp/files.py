import os
import re
import linecache
import numpy as np
from collections import OrderedDict

class Poscar(object):
    '''
    POSCAR file for vasp

    Attributes:
        scale: A float indicating the cell constant.
        lattice: A numpy array indicating the lattice vector.
        selective: A boolean indicating if the selective dynamics is done.
        coorType: A string ('Direct' or 'Cartesian') incicating the
            coordination system. 
        coorDict: A dict of elements with their coordinations.
    '''

    def __init__(self, file=None):
        if file == None:
           pass
        else:
            assert os.path.exists(file), f'Error: {file} does not exist'
            (self.scale, self.lattice, self.selective, self.coorType,
             self.coorDict, self.fixDict) = self.read(file)
    
    def read(self, file):
        if file == 'POSCAR' or file == 'CONTCAR' or file == '*.vasp':
            return self.readvasp(file)
        elif file == '*.cif':
            return self.readcif(file)
        elif file == '*.xyz':
            return self.readxyz(file)
        else:
            print('Error: filetype is wrong')
            
    def readvasp(self, file):
        lines = linecache.getlines(file)
        comment = lines[0].strip()
        scale = float(lines[1].strip())
        lattice = np.array([lines[i].strip().split() for i in range(2, 5)],
                           dtype=np.float)
        eles = lines[5].strip().split()
        nums = [int(i) for i in lines[6].strip().split()]
        natom = sum(nums)
        selective = lines[7].strip()[0] in 'sS'
        coorType = ('Direct' if lines[7+selective].strip()[0] in 'dD'
                    else 'Cartesian')
        coors = np.array([lines[i].strip().split()[:3]
                          for i in range(8+selective,
                                         8+selective+natom)],
                         dtype=np.float)
        if coorType == 'Cartesian':
            coors = self.toDirect(coors, lattice)

        fixs = np.array(
            [lines[i].strip().split()[3:6] for i in range(9, 9+natom)]
            if selective else [['F', 'F', 'F'] for i in range(natom)])
        coorDict = self.toDict(eles, nums, coors)
        fixDict = self.toDict(eles, nums, fixs)
        
        return (scale, lattice, selective, coorType, coorDict, fixDict)
    
#     def readcif(file):
        
#     def readxyz(file):

    
    def toDict(self, eles, nums, conts):
        someDict = OrderedDict()
        start = 0
        for ele, num in zip(eles, nums):
            someDict[ele] = conts[start:start+num].tolist()
            start += num
        return someDict
    
    def toArray(self, someDict):
        return np.concatenate(
            [value for key, value in someDict.items()], axis=0)

    def toCartesian(self, coors, lattice):
        return np.matmul(coors, lattice)
    
    def toDirect(self, coors, lattice):
        return np.matmul(coors, np.linalg.inv(lattice))
    
    @property
    def nums(self):
        return {key:len(value) for key, value in self.coorDict.items()}
    
    @property
    def natom(self):
        return sum(self.nums.values())
    
    @property
    def coors(self):
        return self.toArray(self.coorDict)
    
    @property
    def fixs(self):
        return self.toArray(self.fixDict)
    
    def setFix(self, ele, index, fix=['T', 'T', 'T']):
        self.selective = True
        self.fixDict[ele][index-1] = fix
    
    def setCentre(self):
        self.oldcentre = (np.max(self.coors, axis=0) +
                          np.min(self.coors, axis=0)) / 2
        self.coorDict = self.toDict(
            list(self.nums.keys()), list(self.nums.values()),
            self.coors + 0.5 - self.oldcentre)
        
    def addAtom(self, ele, coordiante, fix=['T', 'T', 'T']):
        if ele in self.coorDict.keys():
            self.coorDict[ele].append(np.array(coordiante))
            self.fixDict[ele].append(np.array(fix))
        else:
            self.coorDict[ele] = np.array(coordiante)
            self.fixDict[ele] = np.array(fix)

    def write(self, arr, coorType='Direct', fname='pos.vasp'):
        with open(fname, 'w') as f:
            f.write(f'POSCAR by pyvasp\n')
            f.write(f'{self.scale:19.14f}\n')
            for i in range(3):
                f.write(f'{self.lattice[i][0]:22.16f}'
                        f'{self.lattice[i][1]:22.16f}'
                        f'{self.lattice[i][2]:22.16f}\n')
            for atom in self.nums:
                f.write(f'{atom:>5s}')
            f.write('\n')
            for n in self.nums.values():
                f.write(f'{n:5d}')
            f.write('\n')

            if self.selective:
                f.write(f'Selective dynamics\n{self.coorType}\n')
                for j in range(self.natom):
                    f.write(f'{arr[j][0]:20.16f}'
                            f'{arr[j][1]:20.16f}'
                            f'{arr[j][2]:20.16f}'
                            f'{self.fixs[j][0]:>4s}'
                            f'{self.fixs[j][1]:>4s}'
                            f'{self.fixs[j][2]:>4s}\n')
            else:
                f.write(f'{self.coorType}\n')
                for j in range(self.natom):
                    f.write(f'{arr[j][0]:20.16f}'
                            f'{arr[j][1]:20.16f}'
                            f'{arr[j][2]:20.16f}\n')

class Potcar(object):
    '''
    POTCAR file for vasp

    Attributes:
        potDict: A dict of elements with their mass, number of electron,
            encut, and enaug.
    '''

    def __init__(self, file=None):
        assert os.path.exists(file), f'Error: {file} does not exists'
        pattern = re.compile('''
        VRHFIN[ ]=(?P<name>[A-Z][a-z]?)[ ]?:[\s\S]*?
        POMASS[ ]=[ ]*(?P<mass>[0-9]+\.[0-9]+);[ ]*
        ZVAL[ ]*=[ ]*(?P<nele>[0-9]+\.[0-9]+)[\s\S]*?
        ENMAX[ ]*=[ ]*(?P<enmax>[0-9]+\.[0-9]+);[\s\S]*?
        EAUG[ ]*=[ ]*(?P<eaug>[0-9]+\.[0-9]+)\n
        ''', re.VERBOSE)
        self.potDict = OrderedDict()
        with open(file) as f:
            for i in pattern.finditer(f.read()):
                self.potDict[i.group('name')] = list(
                    map(float, [i.group('mass'), i.group('nele'),
                                i.group('enmax'), i.group('eaug')]))
