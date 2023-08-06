import numpy as np
import mdio.base 
from mdio.utilities import la2v, v2la

def pdb_atom_parse(line):
    """
    Extract data from an ATOM or HETATM line.
    """
    if line[-1] == '\n':
        line = line[:-1]
    line = line.ljust(80)
    result = {}
    result['serial'] = int(line[6:11])
    result['name'] = line[12:16]
    result['altloc'] = line[16]
    result['resName'] = line[17:20]
    result['chainID'] = line[21]
    result['resSeq'] = int(line[22:26])
    result['icode'] = line[26]
    result['x'] = float(line[30:38])
    result['y'] = float(line[38:46])
    result['z'] = float(line[46:54])
    result['occupancy'] = line[54:60]
    result['tempfactor'] = line[60:66]
    result['element'] = line[76:78]
    result['charge'] = line[78:80]
    return result
    
class PDBFileReader(object):
    def __init__(self, filename, atom_indices=None, top=None, selection=None):
        #print('DEBUG: Reading header')
        self.filename = filename
        self.atom_indices = atom_indices
        self.selection = selection
        self.top = top
        self.unitcell_vectors = None
        self.index = -1
        self.buffer = ' ' * 80
        self.f = open(filename, 'r')
        while not self.buffer[:6] in ['CRYST1', 'MODEL ', 'ATOM  ','HETATM', 'EOF   ']:
            self.buffer = self.f.readline()
            if self.buffer == "":
                  self.buffer = 'EOF   '
            else:
               self.buffer = self.buffer.ljust(80)
        if self.buffer[:6] == 'CRYST1':
            a = float(self.buffer[6:15])
            b = float(self.buffer[15:24])
            c =float(self.buffer[24:33])
            alpha = float(self.buffer[33:40])
            beta = float(self.buffer[40:47])
            gamma = float(self.buffer[47:54])
            self.unitcell_vectors = la2v((a, b, c), (alpha, beta, gamma))
        while not self.buffer[:6] in ['MODEL ', 'ATOM  ','HETATM', 'EOF   ']:
            self.buffer = self.f.readline()
            if self.buffer == "":
                self.buffer = 'EOF   '
            else:
                self.buffer = self.buffer.ljust(80)
        if self.buffer =='EOF   ':
            raise IOError('Error - this does not seem to be a valid PDB file.')
        #print('DEBUG: header read.')
            
    def read_frame(self):
        #print('DEBUG: reading frame.')
        if self.buffer[:6] == 'EOF   ':
            return None
        while not self.buffer[:6] in ['ATOM  ', 'HETATM', 'EOF   ']:
            self.buffer = self.f.readline()
            if self.buffer == "":
                self.buffer = 'EOF   '
            else:
                self.buffer = self.buffer.ljust(80)
        if self.buffer == 'EOF   ':
            return None

        result = []
        index = -1
        if self.buffer[:6] in ['ATOM  ', 'HETATM']:
            while self.buffer[:6] in ['ATOM  ', 'HETATM', 'TER   ']:
                if self.buffer[:6] in ['ATOM  ', 'HETATM']:
                    index += 1
                    data = pdb_atom_parse(self.buffer)
                    data['index'] = index
                    result.append(data)
                self.buffer = self.f.readline()
                if self.buffer == "":
                    self.buffer = 'EOF   '
                else:
                    self.buffer = self.buffer.ljust(80)
        if self.top is None:
            #print('DEBUG: generating topology')
            self.top = mdio.base.Topology(result)
            if self.selection is not None:
                self.atom_indices = self.top.select(self.selection)
            if self.atom_indices is not None:
                self.top = self.top.subset(self.atom_indices)
            #print('DEBUG: topology generated.')
        self.index += 1
        crds = np.array([[data['x'], data['y'], data['z']] for data in result])
        if self.atom_indices is not None:
            crds = crds[self.atom_indices]
        frame = mdio.base.Frame(crds, 
                      box=self.unitcell_vectors, 
                      time=self.index,
                      units='angstroms')
        #print('DEBUG: frame read.')

        return frame

    def read(self):
        frames = []
        frame = self.read_frame()
        while frame is not None:
            frames.append(frame)
            frame = self.read_frame()
        return mdio.base.Trajectory(frames, top=self.top)

    def close(self):
        self.f.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
        
class PDBFileWriter(object):
    def __init__(self, filename, top=None):
        if top is None:
            raise RuntimeError('Error - cannot write PDB format without a topology.')
        if isinstance(top, mdio.base.Topology):
            self.top = top
        else:
            ttop = mdio.load(top)
            self.top = ttop.topology
        self.filename = filename
        self.index = -1
        self.f = open(filename, 'w')

    def write_frame(self, frame):
        scalefactor = 10.0
        self.index += 1
        if self.index == 0:
            if frame.unitcell_vectors is not None:
                lengths, angles = v2la(frame.unitcell_vectors * scalefactor)
                crystformat = 'CRYST1{:9.3f}{:9.3f}{:9.3f}{:7.2f}{:7.2f}{:7.2f}\n'
                self.f.write((crystformat.format(lengths[0], lengths[1], lengths[2], angles[0], angles[1], angles[2])))
        modelformat = 'MODEL     {:4d}\n'
        self.f.write(modelformat.format(self.index + 1))
        atomformat = 'ATOM  {:5d} {:4s} {:3s} {:1s}{:4d}    {:8.3f}{:8.3f}{:8.3f}\n'
        alist = self.top.atomlist
        xyz = frame.xyz * scalefactor
        for i in range(frame.n_atoms):
            name = alist[i]['name'].strip()
            if len(name) == 1:
                name = ' ' + name + '  '
            elif len(name) == 2:
                name = ' ' + name + ' '
            elif len(name) == 3:
                name = ' '  + name
            else:
                name = name[:4]
            resName = alist[i]['resName'].strip().ljust(3)[:3]
            chainID = alist[i]['chainID'].strip().ljust(1)[0]
            self.f.write(atomformat.format(alist[i]['serial'],
                                           name, 
                                           resName,
                                           chainID,
                                           alist[i]['resSeq'],
                                           xyz[i,0],
                                           xyz[i,1],
                                           xyz[i,2]))
        self.f.write('ENDMDL\n')
        
    def write(self, trajectory):
        if isinstance(trajectory, np.ndarray):
            trajectory = mdio.base.Trajectory(trajectory)
        for i in range(len(trajectory)):
            self.write_frame(trajectory.frame(i))

    def close(self):
        self.f.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()

def pdb_open(filename, mode='r', atom_indices=None, top=None, selection=None):
    """
    Open a PDB file.
    """
    if not mode in ["r", "w"]:
        raise ValueError('Error: mode must be "r" or "w".')
    if mode == 'r':
        return PDBFileReader(filename, atom_indices=atom_indices, top=None, selection=selection)
    else:
        return PDBFileWriter(filename, top=top)
