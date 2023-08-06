# mdio

A library of simple I/O routines for MD trajectory formats.

*mdio* is designed to provide basic MD file I/O capabilities. It's not supposed to replace great packages like
[mdtraj](www.mdtraj.org) and [mdanalysis](www.mdanalysis.org), but may be useful when all you need is basic MD 
trajectory file I/O and nothing much more.

Currently mdio supports reading and writing dcd, xtc, and Amber netcdf (.nc) format files.

## Installation:

Easiest via pip. You need numpy and cython pre-installed:

```
% pip install numpy cython
% pip install mdio
```

## Usage:


```python
import mdio
```


To load a trajectory, use *mdio.load()*. This returns an *mdio.Trajectory* object. The format of the trajectory file is detected automatically, without reference to the filename extension.

```python
>>> t = mdio.load('../test/examples/test.nc')
>>> print(t)
mdio.Trajectory with 219 frames, 892 atoms and box info.
```


Alternative ways of reading files are supported:

```python
>>> f = mdio.mdopen('../test/examples/test.nc')
>>> t2 = f.read()
>>> f.close()
>>> print(t2)
mdio.Trajectory with 219 frames, 892 atoms and box info.
```


Or using a context manager, and in a frame-by-frame way:

```python
>>> with mdio.mdopen('../test/examples/test.dcd') as f:
>>>     frames = []
>>>     frame = f.read_frame()
>>>     while frame is not None:
>>>         frames.append(frame)
>>>         frame = f.read_frame()
>>> t3 = mdio.Trajectory(frames)
>>> print(t3)
mdio.Trajectory with 219 frames, 892 atoms and box info.
```


Trajectory files can also be written in a variety of ways. The required format is inferred from the filename extension.

```python
>>> # a) Using the save() method of a trajectory object:
>>> t.save('test.nc')

>>> # b) Using mdopen():
>>> with mdio.mdopen('test2.dcd', "w") as f:
>>>     f.write(t)

>>> # c) Frame-by-frame:
>>> f =  mdio.mdopen('test3.xtc', "w")
>>> for frame in t:
>>>     f.write_frame(frame)
>>> f.close()
```


Trajectory objects have three main attributes: the coordinates (a [n_frames, n_atoms, 3] numpy array), the periodic box data (a [n_frames, 3, 3] numpy array, or [None] * n_frames) and the timepoint of the frame (an n_frames-long list of floats).

The library makes no attempt to guess the units (e.g. Angstroms or nanometres, picoseconds or nanoseconds).

```python
>>> print(type(t.crds), t.crds.shape, t.crds[0,0])
<class 'numpy.ndarray'> (219, 892, 3) [ 28.37000084  43.47999954  25.27000237]
>>> print(type(t.box), t.box.shape, t.box[0])
<class 'numpy.ndarray'> (219, 3, 3) [[ 59.41400146   0.           0.        ]
     [  0.          59.41400146   0.        ]
     [  0.           0.          59.41400146]]
>>> print(type(t.time), t.time[0])
<class 'list'> 17811.001953125
```


Trajectories can be sliced. A slice of length 1 is a Frame. Trajectories can also be subsetted:

```python
>>> print(t[5:17:3])
mdio.Trajectory with 4 frames, 892 atoms and box info.
>>> print(t[33])
mdio.Frame with 892 atoms and box info.
>>> print(t.select(range(150))) # A new trajectory with just the first 150 atoms
mdio.Trajectory with 219 frames, 150 atoms and box info.
```


Trajectories can be concatenated or appended to (if they are compatible):

```python
>>> print(t[2:7] + t[23:30:2])
mdio.Trajectory with 9 frames, 892 atoms and box info.
>>> t2 = t[7:1:-1]
>>> t2 += t[:6]
>>> print(t2)
mdio.Trajectory with 12 frames, 892 atoms and box info.
```


A few common trajectory analysis/manipulation methods are avalable: RMSD calculation, least-squares fitting, and periodic imaging:

```python
>>> r = t.rmsd_from(t[0])
>>> print(r[:3])
[1.2801753287166838e-06, 0.80062371133014676, 0.78828331069708468]
>>> tfit = t.fitted_to(t[1])
>>> print(tfit) # Note that once fitted, box info is invalid, so removed.
mdio.Trajectory with 219 frames, and 892 atoms.
>>> t_imaged = t.packed_around(776) # atom 776 is close to a box edge
>>> print(t_imaged) # Imaging does not invalidate box info
mdio.Trajectory with 219 frames, 892 atoms and box info.
>>> r_packed = t_imaged.rmsd_from(t[0])
>>> print(r_packed[:3]) # Imaging has broken up the molecular structure
[3.949846957712384, 2.9259676964180694, 3.5185721951568407]
```


The least-squares fitting routine can use weights, but you will need to set these by some external method:

```python
>>> import numpy as np
>>> weights = np.zeros(t.natoms)
>>> weights[:100] = 1.0 # Only use first 100 atoms for the fitting
>>> t_weighted_fit = t.fitted_to(t[0], weights)
```

## Author:

Charlie Laughton charles.laughton@nottingham.ac.uk

## License:

BSD 3-clause
