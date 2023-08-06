import numpy as np
from  mdio import rmsd_utils
from os.path import splitext
import mdio.dcdio 
import mdio.ncio 
import mdio.xtcio 
import mdio.pdbio 
import mdio.groio
import mdio.rstio
import mdio.mdcrdio
from mdio.utilities import la2v, v2la

class Frame(object):
    """
    A frame of trajectory data.
    
    """
    def __init__(self, xyz, box=None, time=0.0, precision=1000, timestep = 1.0, units='nanometers'):
        if units == 'nanometers':
            self.units = 1.0
        elif units == 'angstroms':
            self.units = 0.1

        xyz = np.array(xyz, dtype=np.float32) * self.units
        if len(xyz.shape) != 2:
            raise TypeError('Error - crds must be a [N,3] array.')
        if xyz.shape[1] != 3:
            raise TypeError('Error - crds must be a [N,3] array.')
        self.n_atoms = xyz.shape[0]
        self.xyz = xyz
        if box is not None:
            box = np.array(box, dtype=np.float32) * self.units
            if box.min() == 0.0 and box.max() == 0.0:
                box = None
            elif len(box.shape) == 1 and len(box) == 6:
                tbox = np.zeros((3,3), dtype=np.float32)
                tbox[0, 0] = box[0]
                tbox[1, 0] = box[1]
                tbox[1, 1] = box[2]
                tbox[2, 0] = box[3]
                tbox[2, 1] = box[4]
                tbox[2, 2] = box[5]
                box = tbox
            elif box.shape != (3,3):
                raise ValueError('Error - unrecognised box data {}'.format(box))
        self.unitcell_vectors = box
        if self.unitcell_vectors is not None:
            self.unitcell_lengths, self.unitcell_angles = v2la(self.unitcell_vectors)
        else:
            self.unitcell_lengths = None
            self.unitcell_angles = None
        self.time = float(time)
        self.precision = int(precision)
        self.timestep = timestep

    def __str__(self):
        if self.unitcell_vectors is not None:
            return "mdio.Frame with {} atoms and box info.".format(self.natoms)
        else:
            return "mdio.Frame with {} atoms.".format(self.natoms)

    def select(self, atom_indices):
        """
        Create a new Frame from selected atoms.
        """
        return Frame(self.xyz[atom_indices], self.unitcell_vectors, self.time)

    def rmsd_from(self, frame, weights=None):
        """
        The RMSD of this Frame from a reference Frame.
        """
        if isinstance(frame, Trajectory):
            frame = frame[0]
        elif not isinstance(frame, Frame):
            raise TypeError('Error - argument must be a Frame or Trajectory')

        if frame.xyz.shape != self.xyz.shape:
            raise ValueError("Error - reference structure has {} atoms but frame has {} atoms.".format(frame.xyz.shape[0], self.xyz.shape[0]))
        return rmsd_utils.kabsch_rmsd(self.xyz, frame.xyz, weights)

    def fitted_to(self, frame, weights=None):
        """
        Returns a copy of the frame least-squares fitted to the reference.
        """
        if isinstance(frame, Trajectory):
            frame = frame[0]
        elif not isinstance(frame, Frame):
            raise TypeError('Error - argument must be a Frame or Trajectory')

        if frame.xyz.shape != self.xyz.shape:
            raise ValueError("Error - reference structure has {} atoms but frame has {} atoms.".format(frame.xyz.shape[0], self.xyz.shape[0]))

        xyz = rmsd_utils.kabsch_fit(self.xyz, frame.xyz, weights)
        return Frame(xyz, None, self.time)

    def packed_around(self, centre_atom_index):
        """
        Pack the coordinates in a frame into the periodic box.
        """
        if self.unitcell_vectors is None:
            return self
        A = self.unitcell_vectors.T
        B = np.linalg.inv(A)
        box_centre = np.matmul(A, [0.5, 0.5, 0.5])
        dv = box_centre - self.xyz[centre_atom_index]
        r = self.xyz + dv
        f = np.matmul(B, r.T)
        g = f - np.floor(f)
        t = np.matmul(A, g)
        xyz = t.T - dv
        return Frame(xyz, self.unitcell_vectors, self.time)

    """
    def save(self, filename):
        ext = splitext(filename)[1]
        if ext in [".nc", ".ncdf"]:
            opener = mdio.ncio.nc_open
        elif ext in [".dcd"]:
            opener = mdio.dcdio.dcd_open
        elif ext in [".xtc"]:
            opener = mdio.xtcio.xtc_open
        elif ext in [".pdb"]:
            opener = mdio.pdbio.pdb_open
        elif ext in [".gro"]:
            opener = mdio.groio.gro_open
        elif ext in [".rst", ".rst7"]:
            opener = mdio.rstio.rst_open
        elif ext in [".mdcrd"]:
            opener = mdio.mdcrdio.mdcrd_open
        else:
            raise TypeError('Error - unrecognised file extension ({})'.format(ext))
        with opener(filename, "w") as f:
            f.write_frame(self)
    """


# Trajectory-level objects for mdio

class Trajectory(object):
    """
    A series of Frames.
    """
    def __init__(self, data, top=None):
        if isinstance(data, Frame):
            frames = [data]
        elif isinstance(data, list):
            if not isinstance(data[0], Frame):
                raise TypeError('Error - argument must be a frame or list of frames.')
            frames = data
        elif isinstance(data, np.ndarray):
            s = data.shape
            if len(s) < 2 or len(s) > 3:
                raise TypeError('Error - argument must be a [natoms, 3] or [nframes, natoms, 3] array')
            if s[-1] != 3:
                raise TypeError('Error - argument must be a [natoms, 3] or [nframes, natoms, 3] array')
            if len(s) == 2:
                data = [data]
            frames = [Frame(x) for x in data] 
        else:
            raise TypeError('Error - unsupported data type for initialisation.')

        self.xyz = np.array([frames[0].xyz])
        self.unitcell_vectors = np.array([frames[0].unitcell_vectors])
        self.time = np.array([frames[0].time])
        if len(frames) > 1:
            self.append(frames[1:])
        if top is not None:
            if isinstance(top, Topology):
                self.topology = top
            else:
                self.topology = Topology(top)
        else:
            self.topology = None
        self.top = self.topology
        self.comm = None

    def __str__(self):
        if self.unitcell_vectors[0] is None:
            return "mdio.Trajectory with {} frames, and {} atoms.".format(len(self.xyz), self.n_atoms)
        else:
            return "mdio.Trajectory with {} frames, {} atoms and box info.".format(len(self.xyz), self.n_atoms)

    def __len__(self):
        """
        Length of the trajectory.
        """
        return len(self.xyz)

    def __getitem__(self, key):
        """
        Returns a sub-Trajectory.
        """
        xyz = self.xyz[key]
        unitcell_vectors = self.unitcell_vectors[key]
        time = self.time[key]
        if isinstance(key, int):
            return Trajectory(Frame(xyz, unitcell_vectors, time), top=self.topology)
        else:
            return Trajectory([Frame(xyz[i], unitcell_vectors[i], time[i]) for i in range(len(xyz))], top=self.topology)

    def __add__(self, other):
        if not isinstance(other, Trajectory):
            raise NotImplementedError('Error - can only add a Trajectory to a Trajectory.')
        result = Trajectory(self.frames())
        result.append(other.frames())
        return result

    def __iadd__(self, other):
        if not isinstance(other, Trajectory):
            raise NotImplementedError('Error - can only add a Trajectory to a Trajectory.')
        self.append(other.frames())
        return self

    @property
    def n_frames(self):
        return self.xyz.shape[0]

    @property
    def n_atoms(self):
        return self.xyz.shape[1]

    def append(self, data):
        """
        Append exra data to a Trajectory

        Data may be a single Frame or a list of Frames.
.
        """
        if isinstance(data, Frame):
            frames = [data]
        elif isinstance(data, list):
            if all([isinstance(d, Frame) for d in data]):
                frames = data
            else:
                raise TypeError('Error - argument must be a frame or list of frames')
        else:
            raise TypeError('Error - argument must be a frame or list of frames.')
        xyz = []
        unitcell_vectors = []
        time = []
        for frame in frames:
            if frame.xyz.shape != self.xyz[0].shape:
                raise ValueError('Error - all frames must contain the same number of atoms.')
            if (frame.unitcell_vectors is None and self.unitcell_vectors[0] is not None) or (frame.unitcell_vectors is not None and self.unitcell_vectors[0] is None):
                raise ValueError('Error - mixing frames with and without box info.')
            xyz.append(frame.xyz)
            unitcell_vectors.append(frame.unitcell_vectors)
            time.append(frame.time)

        self.xyz = np.vstack((self.xyz, xyz))
        self.time = np.concatenate((self.time, time))
        if self.unitcell_vectors[0] is None:
            self.unitcell_vectors = np.concatenate((self.unitcell_vectors, unitcell_vectors))
        else:
            self.unitcell_vectors = np.vstack((self.unitcell_vectors, unitcell_vectors))

    def frame(self, index):
        return Frame(self.xyz[index], self.unitcell_vectors[index], self.time[index])
 
    def frames(self):
        return [self.frame(i) for i in range(len(self))]

    def select(self, atom_indices):
        """
        Create a new Trajectory from selected atoms.
        """
        frames = []
        for i in range(len(self.xyz)):
            frames.append(Frame(self.xyz[i][atom_indices], self.unitcell_vectors[i], self.time[i]))
        if self.topology is not None:
            top = self.topology.subset(atom_indices)
        else:
            top = None
        return Trajectory(frames, top=top)

    def rmsd_from(self, frame, weights=None):
        """
        The RMSD of each Frame from a reference Frame.
        """
        if isinstance(frame, Trajectory):
            frame = frame.frame(0)
        elif not isinstance(frame, Frame):
            raise TypeError('Error - argument must be a Frame or Trajectory')

        if frame.xyz.shape != self.xyz[0].shape:
            raise ValueError("Error - reference structure has {} atoms but trajectory has {} atoms.".format(frame.xyz.shape[0], self.xyz.shape[0]))
        return [rmsd_utils.kabsch_rmsd(xyz, frame.xyz, weights) for xyz in self.xyz]

    def fitted_to(self, frame, weights=None):
        """
        Returns a copy of the trajectory least-squares fitted to the reference.
        """
        if isinstance(frame, Trajectory):
            frame = frame.frame(0)
        elif not isinstance(frame, Frame):
            raise TypeError('Error - argument must be a Frame or Trajectory')

        if frame.xyz.shape != self.xyz[0].shape:
            raise ValueError("Error - reference structure has {} atoms but trajectory has {} atoms.".format(frame.xyz.shape[0], self.xyz.shape[0]))

        xyz = [rmsd_utils.kabsch_fit(x, frame.xyz, weights) for x in self.xyz]
        frames = []
        for i in range(len(xyz)):
            frames.append(Frame(xyz[i], None, self.time[i]))
        return Trajectory(frames, top=self.topology)

    def superpose(self, reference):
        new = self.fitted_to(reference)
        self.xyz = new.xyz
        return self

    def packed_around(self, atom_indices=None, selection=None):
        """
        Pack the coordinates in a trajectory into the periodic box.
        """
        if self.unitcell_vectors[0] is None:
            return self
        if selection is not None and self.topology is None:
            raise RuntimeError('Error - selection needs a topology')
        if selection is not None:
            atom_indices = self.topology.select(selection)
            
        frames = []
        for i in range(len(self.xyz)):
            A = self.unitcell_vectors[i].T
            B = np.linalg.inv(A)
            if atom_indices is not None:
                box_centre = np.matmul(A, [0.5, 0.5, 0.5])
                dv = box_centre - self.xyz[i][atom_indices].mean(axis=0)
            else:
                dv = 0.0
            r = self.xyz[i] + dv
            f = np.matmul(B, r.T)
            g = f - np.floor(f)
            t = np.matmul(A, g)
            xyz = t.T - dv
            frames.append(Frame(xyz, self.unitcell_vectors[i], self.time[i]))
        return Trajectory(frames, top=self.topology)

    def mean_structure(self):
        """
        Returns a Frame with the mean structure.
        """
        xyz = self.xyz.mean(axis=0)
        time = np.array(self.time).mean()
        if self.unitcell_vectors[0] is not None:
            unitcell_vectors = self.unitcell_vectors.mean(axis=0)
        else:
            unitcell_vectors = None
       
        return Frame(xyz, unitcell_vectors, time)


    def save(self, filename):
        ext = splitext(filename)[1]
        if ext in [".nc", ".ncdf"]:
            opener = mdio.ncio.nc_open
        elif ext in [".dcd"]:
            opener = mdio.dcdio.dcd_open
        elif ext in [".xtc"]:
            opener = mdio.xtcio.xtc_open
        elif ext in [".pdb"]:
            opener = mdio.pdbio.pdb_open
        elif ext in [".rst", "rst7"]:
            opener = mdio.rstio.rst_open
        elif ext in [".mdcrd"]:
            opener = mdio.mdcrdio.mdcrd_open
        elif ext in [".gro"]:
            opener = mdio.groio.gro_open
        else:
            raise TypeError('Error - unrecognised file extension ({})'.format(ext))
        with opener(filename, "w", top=self.topology) as f:
            f.write(self)

class Topology(object):

    """
    A basic PDB based topology object from which selections can be turned into lists of atom indices.
    
    """
    def __init__(self, source):
        if isinstance(source, mdio.base.Topology):
            self.atomlist = source.atomlist
        elif isinstance(source, str):
            ttop = mdio.load(source)
            self.atomlist = ttop.topology.atomlist
            if self.atomlist is None:
                raise IOError('Error getting topology from {}.'.format(source))
        elif isinstance(source, list) and isinstance(source[0], dict):
            self.atomlist = source
        else:
            raise ValueError('Error initialising topology with given data type {}.'.format(type(source)))
             
        self.n_atoms = len(self.atomlist)
        self.n_residues = 0
        self.n_chains = 0
        self.bonds = []
        self.residuelist = []
        self.chainlist = []
        rcname = None
        cname = None
        
        for a in self.atomlist:
            reschain = str(a['resSeq']) + '_' + a['chainID']
            chainid = a['chainID']
            if cname != chainid:
                self.n_chains += 1
                cname = chainid
                c = {}
                c['chainID'] = chainid
                c['index'] = self.n_chains - 1
                self.chainlist.append(c)

            if reschain != rcname:
                self.n_residues += 1
                rcname = reschain
                r = {}
                r['index'] = self.n_residues - 1
                r['chainIndx'] = self.n_chains - 1
                r['resSeq'] = a['resSeq']
                r['chainID'] = a['chainID']
                r['resName'] = a['resName']
                self.residuelist.append(r)

            a['resIndx'] = self.n_residues - 1
            a['chainIndx'] = self.n_chains - 1

        for i, a in enumerate(self.atomlist):
            a['mass'] = self.atom(i).element.mass
            a['element'] = self.atom(i).element.symbol
        
    def atom(self, index):
        return Atom(index, self)

    @property
    def atoms(self):
        indx = 0
        while indx < self.n_atoms:
            yield Atom(indx, self)
            indx += 1

    def residue(self, index):
        return Residue(index, self)

    @property
    def residues(self):
        resindx = 0
        while resindx < self.n_residues:
            yield Residue(resindx, self)
            resindx += 1

    def chain(self, index):
        return Chain(index, self)

    @property
    def chains(self):
        chainindx = 0
        while chainindx < self.n_chains:
            yield Chain(chainindx, self)
            chainindx += 1

    def _parser_1(self, expression):
        words = expression.split()
        sub_expressions = []
        i = 0
        sub_expression = []
        for w in words:
            if w in ['and', 'or']:
                sub_expressions.append(" ".join(sub_expression))
                sub_expression = []
                sub_expressions.append(w)
            else:
                sub_expression.append(w)
        sub_expressions.append(" ".join(sub_expression))
        return sub_expressions
    
    def _parser_2(self, expression):
        words = expression.split()
        if words[0] == 'not':
            words = words[1:]
            invert = True
        else:
            invert = False
        w0 = words[0]
        if not w0 in ['index', 'name', 'residue', 'resname', 'chainID', 'resSeq', 'resName', 'chainID', 'element', 'mass', 'all']:
            raise ValueError('Error - cannot parse {}'.format(expression))
        if w0 in ['name', 'resName', 'resname', 'chainID', 'chainid', 'element']:
            if len(words) > 2:
                raise ValueError('Error - cannot parse {}'.format(expression))
            if w0 == 'resname':
                w0 = 'resName'
            if w0 == 'chainid':
                w0 = 'chainID'
            ll = len(self.atomlist[0][w0])
            w1 = words[1].lstrip().ljust(ll)
            
            subset = set([a['index'] for a in self.atomlist if a[w0].lstrip().ljust(ll)  == w1])
        elif w0 in ['index', 'residue', 'resSeq']:
            if w0 == 'residue':
                w0 = 'resSeq'
            try:
                indices = self._parser_3(words[1:])
            except:
                raise ValueError('Error - cannot parse {}'.format(expression))
            if not invert:
                subset = set([a['index'] for a in self.atomlist if a[w0] in indices])
            else:
                subset = set([a['index'] for a in self.atomlist if not a[w0] in indices])
        elif w0 in ['mass']:
            if len(words) != 3:
                raise ValueError('Error - cannot parse {}'.format(expression))
            if not words[1] in ['<', '<=', '==', '>', '>=']:
                raise ValueError('Error - cannot parse {}'.format(expression))
            test = '{mass} ' + words[1] + ' ' + words[2]
            if not invert:
                subset = set([a['index'] for a in self.atomlist if eval(test.format(**a))])
            else:
                subset = set([a['index'] for a in self.atomlist if not eval(test.format(**a))])
        elif w0 == 'all':
            if len(words) != 1:
                raise ValueError('Error - cannot parse {}'.format(expression))
            if not invert:
                subset = set([a['index'] for a in self.atomlist])
            else:
                subset = set([])
        else:
            raise ValueError('Error - cannot parse {}'.format(expression))
        return subset

    def _parser_3(self, words):
        if len(words) == 1:
            return [int(words[0])]
        else:
            if not words[1] == 'to':
                raise ValueError
            i = int(words[0])
            j = int(words[2])
            return range(i, j+1)
    
    def select(self, expression):
        p = self._parser_1(expression)
        s = self._parser_2(p[0])
        for x in p[1:]:
            if x in ['or', 'and']:
                 op = x
            else:
                s2 = self._parser_2(x)
                if op == 'or':
                    s = s.union(s2)
                else:
                    s = s.intersection(s2)
        return sorted(s)

    def subset(self, atom_indices):
        alist = [a for a in self.atomlist if a['index'] in atom_indices]
        return Topology(alist)

    @classmethod
    def from_dataframe(cls, atoms, bonds=None):
        if len(atoms) == 0:
            raise ValueError('Error - no atoms.')
        atomlist = atoms.to_dict(orient='records')
        return mdio.base.Topology(atomlist)
    
class Element(object):
    def __init__(self, symbol='X', mass=1.0, radius=1.0):
        self.symbol = symbol
        self.mass = mass
        self.radius = radius

    @classmethod
    def from_symbol(self, symbol):
        element_symbols = ['H', 'C', 'N', 'O', 'P', 'S']
        element_masses = [1, 12, 14, 16, 31, 32]
        element_radii = [0.032, 0.076, 0.071, 0.066, 0.107, 0.105] # in nanometers
        try:
            i = element_symbols.index(symbol)
        except ValueError:
            i = element_symbols.index('C')
        return Element(element_symbols[i], element_masses[i], element_radii[i])
            
class Atom(object):
    def __init__(self, index, topology):
        self.index = index
        self.topology = topology
        self.serial = self.topology.atomlist[index]['serial']
        self.name = self.topology.atomlist[index]['name']
        resindx = self.topology.atomlist[index]['resIndx']
        self.residue = self.topology.residue(resindx)
        chainindx = self.topology.atomlist[index]['chainIndx']
        self.chain = self.topology.chain(chainindx)
        element_symbol = self.name.lstrip(' 0123456789')[0]
        self.element = Element.from_symbol(element_symbol)
            
class Residue(object):
    def __init__(self, resindx, topology):
        self.resindx = resindx
        self.topology = topology
        self.resSeq = self.topology.residuelist[resindx]['resSeq']
        self.name = self.topology.residuelist[resindx]['resName']
        chainindx = self.topology.residuelist[resindx]['chainIndx']
        self.chain = self.topology.chain(chainindx)

    @property
    def atoms(self):
        indx = 0
        while indx < self.topology.n_atoms:
            if self.topology.atomlist[indx]['resIndx'] == self.resindx:
                yield Atom(indx, self.topology)
                indx += 1
            else:
                indx += 1

class Chain(object):
    def __init__(self, chainindx, topology):
        self.index = chainindx
        self.topology = topology
        self.chainid = self.topology.chainlist[chainindx]['chainID']

    @property
    def residues(self):
        resindx = 0
        while resindx < self.topology.n_residues:
            if self.topology.residuelist[resindx]['chainID'] == self.chainid:
                yield Residue(resindx, self.topology)
                resindx += 1
            else:
                resindx += 1

def mpi_load(filenames, top=None, atom_indices=None, selection=None, comm=None):
    """
    MPI-powered file loader
    """
    if comm is None or isinstance(filenames, str):
        traj = load(filenames, top=top, atom_indices=atom_indices, selection=selection)
        traj.comm = comm
        return traj
    else:
        size = comm.Get_size()
        rank = comm.Get_rank()
    if size == 1:
        return load(filenames, top=top, atom_indices=atom_indices, selection=selection)
    nfiles = len(filenames)
    offsets = np.rint(np.linspace(0, nfiles, size, endpoint=False)).astype(np.int)
    offsets = np.append(offsets, [nfiles])

    i = offsets[rank]
    j = offsets[rank + 1]
    if j > i:
        t = mdio.load(filenames[i:j], top, atom_indices=atom_indices, selection=selection)
    else:
        t = mdio.load_frame(filenames[0], 0, top=top, atom_indices=atom_indices, selection=selection)
        t.xyz = t.xyz[0:0]
        t.time = t.time[0:0]
        if t.unitcell_vectors is not None:
            t.unitcell_vectors = t.unitcell_vectors[0:0]

    sendcounts = np.array(comm.gather(t.n_frames, root=0))
    sendcounts = comm.bcast(sendcounts, root=0)

    n_atoms = t.n_atoms
    tcounts = sendcounts
    xcounts = sendcounts * n_atoms * 3
    bcounts = sendcounts * 9
    tot_frames = sendcounts.sum()
    has_box = t.unitcell_vectors is not None

    xyz = np.empty((tot_frames, n_atoms, 3), dtype=t.xyz.dtype)
    time = np.empty(tot_frames, dtype=t.time.dtype)
    if has_box:
        unitcell_vectors = np.empty((tot_frames, 3, 3), dtype=t.unitcell_vectors.dtype)
    else:
        unitcell_vectors = None

    comm.Gatherv(t.xyz, (xyz, xcounts), root=0)
    comm.Gatherv(t.time, (time, tcounts), root=0)
    comm.Bcast(xyz, root=0)
    comm.Bcast(time, root=0)
    
    if has_box:
        comm.Gatherv(t.unitcell_vectors, (unitcell_vectors, bcounts),  root=0)
        comm.Bcast(unitcell_vectors, root=0)

    t_all = mdio.Trajectory(xyz, t.topology) 
    t_all.time = time
    t_all.unitcell_vectors = unitcell_vectors
    t_all.comm = comm
    return t_all

def slice_parse(filename):
    """
    Split a filename into real name and possible [start:stop:step] components
    """
    def int_or_none(c):
        try:
            result = int(c)
        except:
            result = None
        return result

    if '[' in filename:
        if not ']' in filename:
            raise ValueError('Error in filename {}.'.format(filename))
        i = filename.find('[')
        j = filename.find(']')
        indices = filename[i+1:j]
        filename = filename[:i]
        key = slice(*[int_or_none(c) for c in indices.split(':')])
    else:
        key = None
    return filename, key

def get_opener(filename, top=None):
    """
    Returns an opener for filename.
    """
    openers = [mdio.ncio.nc_open, 
               mdio.dcdio.dcd_open, 
               mdio.xtcio.xtc_open, 
               mdio.groio.gro_open, 
               mdio.rstio.rst_open, 
               mdio.pdbio.pdb_open, 
               mdio.mdcrdio.mdcrd_open]
    for opener in openers:
        if opener == mdio.mdcrdio.mdcrd_open:
            tmptop = top
        else:
            tmptop = None
        try:
            with opener(filename, top=tmptop) as f:
                frame = f.read_frame()
            good_opener = opener
            success = True
        except:
            success = False
        if success:
            break
    if not success:
        return None
    else:
        return good_opener

def load(filenames, top=None, atom_indices=None, selection=None):
    """
    Format-detecting file loader
    """

    tlist = []
    if isinstance(filenames, str):
        filenames = [filenames,]
    for i, filename in enumerate(filenames):
        filename, key = slice_parse(filename)
        opener = get_opener(filename, top=top)
        if opener is None:
            raise TypeError('Error - {} does not have a recognised file format'.format(filename))
        with opener(filename, top=top, atom_indices=atom_indices, selection=selection) as f:
            if key is None:
                tlist.append(f.read())
            else:
                tlist.append(f.read()[key])
    result = tlist[0]
    for t in tlist[1:]:
        result += t
    return result

def load_frame(filename, index, top=None, atom_indices=None, selection=None):
    """
    Format-detecting file loader for a single frame.
    """
    opener = get_opener(filename, top=top)
    if opener is None:
        raise TypeError('Error - {} does not have a recognised file format'.format(filename))
    i = 0
    with opener(filename, top=top, atom_indices=atom_indices, selection=selection) as f:
        while i <= index:
            frame = f.read_frame()
            i += 1
    return Trajectory(frame, top=top)

def mdopen(filename, mode="r", atom_indices=None, top=None, selection=None):
    """
    Format-agnostic open routines.
    """
    if not mode in ["r", "w"]:
        raise ValueError('Error - mode must be "r" or "w"')

    if mode == "r":
        f = open(filename, 'rb')
        f.close()
        if top is not None:
            f = open(top, 'rb')
            f.close()
        opener = get_opener(filename, top=top)
        if opener is None:
            raise TypeError('Error - {} does not have a recognised file format'.format(filename))
        return opener(filename, atom_indices=atom_indices, top=top, selection=selection)

    else:
        ext = splitext(filename)[1]
        if ext in [".nc", ".ncdf"]:
            opener = mdio.ncio.nc_open
        elif ext in [".dcd"]:
            opener = mdio.dcdio.dcd_open
        elif ext in [".xtc"]:
            opener = mdio.xtcio.xtc_open
        elif ext in [".pdb"]:
            opener = mdio.pdbio.pdb_open
        elif ext in [".gro"]:
            opener = mdio.groio.gro_open
        elif ext in [".rst", ".rst7"]:
            opener = mdio.rstio.rst_open
        elif ext in [".mdcrd"]:
            opener = mdio.mdcrdio.mdcrd_open
        else:
            raise TypeError('Error - unrecognised file extension ({})'.format(ext))
        return opener(filename, "w", top=top)

def get_indices(pdbfile, selection):
    top = Topology(pdbfile)
    return top.select(selection)

def rmsd(traj1, traj2):
    return traj1.rmsd_from(traj2)

