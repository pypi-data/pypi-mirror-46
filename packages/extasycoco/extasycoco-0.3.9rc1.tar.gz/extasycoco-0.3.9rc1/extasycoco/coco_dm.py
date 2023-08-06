#import mdtraj as mdt
import mdio as mdt
import logging as log
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.linalg import eigh
from sklearn.decomposition import PCA
    
def dm_score(dm, dm_mean, dm_k):
    """
    Returns the elastic energy of a distance matrix.
    """
    d = dm - dm_mean
    return ((d * d) * dm_k).mean()

def dm2x(dm, tref):
    """
    Converts a distance matrix into a set of Cartesian points.

    tref is a reference structure (as an MDTraj tarjectory) that is used
    to check for inversion.
    """
    d2 = squareform(dm)
    m = np.zeros_like(d2)
    for i in range(d2.shape[0]):
        for j in range(d2.shape[1]):
            m[i,j] = (d2[0, i] + d2[0, j] - d2[i, j]) / 2
    w, v = eigh(m)
    wr = np.sqrt(np.where(w > 0, w, 0))
    reconstructed_xyz = (wr * v)[:, -3:]
    ttmp = mdt.Trajectory(reconstructed_xyz, tref.topology)
    rmsd1 = mdt.rmsd(tref, ttmp)[0]
    ttmp.xyz[0,:,0] = -ttmp.xyz[0,:,0]
    rmsd2 = mdt.rmsd(tref, ttmp)[0]
    if rmsd2 > rmsd1:
        ttmp.xyz[0,:,0] = -ttmp.xyz[0,:,0]
    ttmp.superpose(tref)
    return ttmp.xyz[0]
    
def dm_parameterize(dm_series, var_cut):
    rmin = dm_series.min(axis=1).mean()
    kmin = 1.0 / dm_series.min(axis=1).var()
    rmax = dm_series.max(axis=1).mean()
    kmax = 1.0 / dm_series.max(axis=1).var()
    rvar = dm_series.var(axis=1).mean()
    kvar = 1.0 / dm_series.var(axis=1).var()

    kvar2 = 1.0 / dm_series.var(axis=0)
    kvar2c = kvar2.copy()
    kvar2c.sort()
    kvar2c = kvar2c[::-1]

    kv_cut = kvar2c[int(len(kvar2) * var_cut)]
    dm_mean = dm_series.mean(axis=0)
    dm_k_cut = np.where(kvar2 >= kv_cut, kvar2, 0.0)
    dms = np.array([dm_score(dm, dm_mean, dm_k_cut) for dm in dm_series])
    rcut = dms.mean()
    kcut = 1.0 / dms.var()

    parameters = {}
    parameters['rmin'] = rmin
    parameters['kmin'] = kmin
    parameters['rmax'] = rmax
    parameters['kmax'] = kmax
    parameters['rvar'] = rvar
    parameters['kvar'] = kvar
    parameters['dm_mean'] = dm_mean
    parameters['dm_k'] = dm_k_cut
    parameters['rcut'] = rcut
    parameters['kcut'] = kcut
    return parameters

def e(dm, parameters):
    dmind = dm.min() - parameters['rmin']
    emin = (dmind * dmind) * parameters['kmin']
    dmaxd = dm.max() - parameters['rmax']
    emax = (dmaxd * dmaxd) * parameters['kmax']
    dvard = dm.var() - parameters['rvar']
    evar = (dvard * dvard) * parameters['kvar']
    dcutd = dm_score(dm, parameters['dm_mean'], parameters['dm_k']) - parameters['rcut']
    ecut = (dcutd * dcutd) * parameters['kcut']
    return emin + emax + evar + ecut * 2.0
    
def dm_mc(dm_start, search_vectors, step_size, n_samples, 
          save_interval, e, parameters, escale):

    dm_samples = []
    n_steps = n_samples * save_interval
    dm = dm_start
    e_dm = e(dm, parameters)
    n_vecs = len(search_vectors)
    for i in range(n_steps):
        dr = np.random.random(n_vecs) * 2.0 - 1.0
        dd = np.dot(search_vectors.T, dr.T)
        dd = (step_size * dd) / np.sqrt(((dd * dd).sum()))
        accepted=True
        while accepted:
            dm_new = dm + dd
            e_dm_new = e(dm_new, parameters)
            de = (e_dm_new - e_dm) * escale
            if de <= 0.0:
                dm = dm_new
                e_dm = e_dm_new
            else:
                if np.exp(-de) > np.random.random():
                    dm = dm_new
                    e_dm = e_dm_new
                else:
                    accepted = False
        if i % save_interval == 0:
            dm_samples.append(dm)
        #if i % (n_steps // 10) == 0:
            #print(int(100 * i / n_steps))
    return np.array(dm_samples)

def coco(include_data, exclude_data, n_points, grid_dims, grid_bins):
    pca = PCA(n_components=grid_dims)
    pca.fit(include_data)
    projs = pca.transform(include_data)
    exc_projs = pca.transform(exclude_data)

    enough_new_points = False
    while not enough_new_points:
        h, edges = np.histogramdd(projs[:,:grid_dims], bins=grid_bins)
        h_exc, edges = np.histogramdd(exc_projs[:,:grid_dims], bins=edges)
        h = np.where(h_exc == 0, h, 0)
        n_samples = (h > 0).sum()
        if n_samples < n_points:
            grid_bins += 1
            print('Warning: increasing grid_bins to {}'.format(grid_bins))
        else:
            enough_new_points = True

    unsafe = h == 0
    occupied = h_exc > 0
    available = h > 0
    crds = np.where(h > -1)
    crds = np.array(crds).T
    dists = squareform(pdist(crds))
    coco_list = []
    for i in range(n_points):
        deo = dists[available.flatten()][:, occupied.flatten()]
        mineo = deo.min(axis=1)
        minboth = np.zeros(len(crds))
        minboth[available.flatten()] = mineo
        minboth = minboth.reshape(h.shape)
        minboth[unsafe] == 0
        maxloc = np.argmax(minboth)
        coco_list.append(np.unravel_index(maxloc, h.shape))
        available.flat[maxloc] = False
        occupied.flat[maxloc] = True
    edges = np.array(edges)
    c0 = (edges[:, 1] + edges[:, 0]) / 2
    dx = edges[:, 1] - edges[:, 0]
    p_new = np.array([c0 + dx * c for c in coco_list])
    dm_new = pca.inverse_transform(p_new)
        
    return dm_new

def dm_complement(traj, logfile=None, 
                  n_points=1, n_samples=10000, pca_dims=30, step_scale=0.1,
                  grid_dims=3, grid_bins=5, var_cut=0.1, comm=None):
    """
    The distance-matrix based CoCo method.

    Args:
        traj (MDTraj trajectory): the input coordinates.
        logfile (file): Open file handle to a log file.
        n_points (int): number of new structures to generate.
        n_samples (int): number of candidate structures to generate.
        pca_dims (int): Number of PCs to use for the search.
        step_scale (float): Scale factor for the search step size.
        grid_dims (int): Number of PCs to use for the partitioning step.
        grid_bins (int): Numbero of bins n each dimension for the partitioning.
        var_cut (float): variance cutoff fraction for elastic network 
                         generation.
        comm (MPI communicator): Optional MPI communicator

    Returns:
        MDTraj trajectory

    The method is as follows:

        1. The input structures are converted to distance matrices.
        2. PCA is performed on the distance matrices.
        3. New structures are generated through a 'ballistic walk' through
           the pca_dim dimensional PC space as follows:

           a. A starting point in PC space is selected.
           b. A random unit vector of length pca_dim is created.
           c. The sample point is moved in increments along the vector. 
              At each step the "energy" of the structure is evaluated against
              a penalty function that restrains:
                  i. The deviation of the smallest distance in the distance
                     matrix from the average value seen in the input data.
                  ii. Similarly for the maximum distance.
                  iii. Similarly for the variance in the distance matrix.
                  iv. An elastic energy term, calculated for just the
                      user-chosen fraction of distances with the lowest  
                      variance in the input data, and using a force constant
                      inversely proportional to their variance. 
           d. The energy change associated with this step is accepted or not
              according to the usual Metropolis MC method. If it is
              accepted, the search continues along the same search vector,
              oterwise a new random search direction is chosen. 
           e. At every 20th step, the structure (distance matrix) is added
              to the list of candidates.
           f. If the desiired number of samples has not been collected yet,
              The process then repeats from step b.
              
        4. A diverse selection of n_points structures from the list of
           candidates is made. This is done usng a second PCA-based procedure:

           a. PCA is performed on the candidates, in grid_dim dimensions.
           b. The structures are assigned to grid_bins bins in the grid_dim 
              dimensonal PC space.
           c. Bins that are occupied by points from the input trajectory are
              rejected, so new points will be complementary.
           d. A set of N diverse bns is selected using the standard CoCo
              approach: the distance of an unoccupied bin most distant from
              any occupied bin is selected, this is then added to the list
              of occupied bins, and the process iterated.
           e. For each of the chosen bins, a structure corresponding to the
              centre of the bin is generated.

        5. The selected structures are converted to an MDTraj trajectory and
           returned.
    
    """

    if comm is None:
        rank = 0
        size = 1
    else:
        rank = comm.Get_rank()
        size = comm.Get_size()

    while n_points > grid_dims * grid_bins:
        grid_bins += 1
        
    pca_dims = min(pca_dims, len(traj) - 3)

    if rank == 0:
        log.info('Calculating distance matrices')
        if logfile is not None:
            logfile.write('Calculating distance matrices')
    dm_series = np.array([pdist(x) for x in traj.xyz])
    dm_series = dm_series * dm_series
    ddm = dm_series[1:] - dm_series[:-1]
    step_size = np.sqrt((ddm * ddm).mean())
    print('input stepsize={}'.format(step_size))

    parameters = dm_parameterize(dm_series, var_cut)
    n_k = (parameters['dm_k'] > 0.0).sum()
    if rank == 0:
        log.info('{} out of {} distances will be restrained'.format(n_k, len(dm_series[0])))
        if logfile is not None:
            logfile.write('{} out of {} distances will be restrained'.format(n_k, len(dm_series[0])))
    
    e_series = np.array([e(dm, parameters) for dm in dm_series])
    de_series = e_series[1:] - e_series[:-1]
    escale = 2.0 / de_series.std()
    
    if rank == 0:
        log.info('Running PCA on input structures')
        if logfile is not None:
            logfile.write('Running PCA on input structures')
    pca = PCA(n_components=pca_dims)
    pca.fit(dm_series)
    search_vectors = pca.components_
    
    if rank == 0:
        log.info('Generating new candidate structures')
        if logfile is not None:
            logfile.write('Generating new candidate structures')

    save_interval = 20
    step_size = step_size * step_scale
    n_samples = n_samples // size
    dm_samples = dm_mc(dm_series[0], search_vectors, step_size, n_samples,
                       save_interval, e, parameters, escale)
    if comm is not None:
        total_dm_samples_shape = list(dm_samples.shape)
        total_dm_samples_shape[0] = total_dm_samples_shape[0] * size
        total_dm_samples = np.empty(total_dm_samples_shape, 
                                    dtype=dm_samples.dtype)
        comm.Gather(dm_samples, total_dm_samples, root=0)
        dm_samples = total_dm_samples

    if rank > 0:
        return None

    if rank == 0:
        log.info('Selecting complementary structures from {} candidates'.format(len(dm_samples)))
        if logfile is not None:
            logfile.write('Selecting complementary structures from candidates')

    dm_new = coco(dm_samples, dm_series, n_points, grid_dims, grid_bins)

    if rank == 0:
        log.info('CoCo points identified, generating new structures.')
        if logfile is not None:
            logfile.write('CoCo points identified, generating new structures.')

    x_new = np.array([dm2x(dm, traj[0]) for dm in dm_new])
    traj_new = mdt.Trajectory(x_new, traj.topology)
    return traj_new
