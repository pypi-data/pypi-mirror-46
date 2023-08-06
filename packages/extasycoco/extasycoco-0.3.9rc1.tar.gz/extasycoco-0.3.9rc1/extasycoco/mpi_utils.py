#import mdtraj as mdt
import mdio as mdt
import numpy as np

def mpi_load(comm, trajfiles, top=None, selection=None, atom_indices=None):
    """
    Load a set of trajectory files in parallel via MPI.
    """

    if comm is None:
        size = 1
        rank = 0
    else:
        size = comm.Get_size()
        rank = comm.Get_rank()

    if isinstance(trajfiles, str):
        trajfiles = [trajfiles,]

    if rank == 0:
        if selection is not None:
            if top is None:
                t_tmp = mdt.load_frame(trajfiles[0], 0)
            else:
                t_tmp = mdt.load_frame(trajfiles[0], 0, top=top)
            atom_indices = t_tmp.topology.select(selection)

    if comm is None:
        if top is None:
            t = mdt.load(trajfiles, atom_indices=atom_indices)
        else:
            t = mdt.load(trajfiles, top=top, atom_indices=atom_indices)
        return t

    if rank == 0:
        if top is not None:
            test_t = mdt.load(top, atom_indices=atom_indices)
        else:
            test_t = mdt.load(trajfiles[0], atom_indices=atom_indices)
    else:
        test_t = None
    test_t = comm.bcast(test_t, root=0)
    atom_indices = comm.bcast(atom_indices, root=0)

    nfiles = len(trajfiles)
    offsets = np.rint(np.linspace(0, nfiles, size, endpoint=False)).astype(np.int)
    offsets = np.append(offsets, [nfiles])
    i = offsets[rank]
    j = offsets[rank + 1]
    if j > i:
        if top is not None:
            t = mdt.load(trajfiles[i:j], top=top, atom_indices=atom_indices)
        else:
            t = mdt.load(trajfiles[i:j], atom_indices=atom_indices)
    else:
        t = test_t[0:0]

    sendcounts = np.array(comm.gather(t.n_frames, root=0))
    sendcounts = comm.bcast(sendcounts, root=0)

    n_atoms = t.n_atoms
    tcounts = sendcounts
    xcounts = sendcounts * n_atoms * 3
    bcounts = sendcounts * 3
    tot_frames = sendcounts.sum()
    has_box = t.unitcell_lengths is not None

    xyz = np.empty((tot_frames, n_atoms, 3), dtype=t.xyz.dtype)
    time = np.empty(tot_frames, dtype=t.time.dtype)
    if has_box:
        unitcell_lengths = np.empty((tot_frames, 3), dtype=t.unitcell_lengths.dtype)
        unitcell_angles = np.empty((tot_frames, 3), dtype=t.unitcell_angles.dtype)
    else:
        unitcell_lengths = None
        unitcell_angles = None

    comm.Gatherv(t.xyz, (xyz, xcounts), root=0)
    comm.Gatherv(t.time, (time, tcounts), root=0)
    comm.Bcast(xyz, root=0)
    comm.Bcast(time, root=0)
    
    if has_box:
        comm.Gatherv(t.unitcell_lengths, (unitcell_lengths, bcounts),  root=0)
        comm.Gatherv(t.unitcell_angles, (unitcell_angles, bcounts), root=0)
        comm.Bcast(unitcell_lengths, root=0)
        comm.Bcast(unitcell_angles, root=0)

    t_all = mdt.Trajectory(xyz, t.topology, time=time, 
                           unitcell_lengths=unitcell_lengths, 
                           unitcell_angles=unitcell_angles)
    return t_all
