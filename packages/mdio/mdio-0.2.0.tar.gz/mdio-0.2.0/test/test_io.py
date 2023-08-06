import mdio
import numpy as np

ncfile = 'examples/test.nc'
dcdfile = 'examples/test.dcd'
xtcfile = 'examples/test.xtc'
pdbfile = 'examples/test.pdb'
grofile = 'examples/test.gro'
testcrds = np.array([2.837, 4.348, 2.527])
testbox = np.array([[5.9414,  0.,     0.   ],
     [ 0.,    5.9414,  0.,   ],
     [ 0.,     0.,    5.9414]], dtype=np.float32)
testi = 10

def test_loader():
    t = mdio.load(ncfile)
    assert np.allclose(t.xyz[0,0], testcrds) is True
    assert np.allclose(t[0].unitcell_vectors, testbox) is True
    assert len(t) == testi

def test_opener():
    fin = mdio.open(ncfile)
    fout = mdio.open('tmp.dcd', 'w')
    frame = fin.read_frame()
    while frame is not None:
        fout.write_frame(frame)
        frame = fin.read_frame()
    fin.close()
    fout.close()

def test_consistency():
    finA = mdio.open(ncfile, 'r')
    finB = mdio.open('tmp.dcd', 'r')
    frameA = finA.read_frame()
    frameB = finB.read_frame()
    while frameA is not None:
        assert np.allclose(frameA.xyz, frameB.xyz) is True
        frameA = finA.read_frame()
        frameB = finB.read_frame()
    finA.close()
    finB.close()

def test_multiopen():
    t = mdio.load([ncfile, dcdfile])
    assert len(t) == 20

def test_with_top():
    t = mdio.load(ncfile, top=pdbfile)
    assert t.topology is not None

def test_with_top_and_indices():
    t = mdio.load(ncfile, top=pdbfile, atom_indices=range(10))
    assert t.n_atoms == 10
    sel = t.topology.select('name CA')
    assert len(sel) == 1

def test_with_selection_1():
    t = mdio.load(ncfile, top=pdbfile, selection='name CA')
    assert t.n_atoms == 58

def test_with_selection_2():
    t = mdio.load(ncfile, top=pdbfile, selection='not residue 1 to 3')
    assert t.n_atoms == 840

def test_with_selection_3():
    t = mdio.load(xtcfile, top=grofile, selection='name CA')
    assert t.n_atoms == 58

def test_with_selection_4():
    t = mdio.load(dcdfile, top=grofile, selection='not residue 1 to 3')
    assert t.n_atoms == 840

def test_with_selection_5():
    t = mdio.load(dcdfile, top=grofile, selection='element N')
    assert t.n_atoms == 84

def test_with_selection_6():
    t = mdio.load(dcdfile, top=grofile, selection='mass > 2.0')
    assert t.n_atoms == 454

def test_with_slice_2():
    t = mdio.load(dcdfile + '[3:10:3]', top=grofile, selection='mass > 2.0')
    assert t.n_frames == 3

def test_with_slice_1():
    t = mdio.load(dcdfile + '[:5]', top=grofile, selection='mass > 2.0')
    assert t.n_frames == 5
