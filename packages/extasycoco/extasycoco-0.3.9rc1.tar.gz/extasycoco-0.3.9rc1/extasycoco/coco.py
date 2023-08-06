import numpy as np
import scipy.ndimage as nd
#import mdtraj as mdt
import mdio as mdt
import logging as log
from MDPlus.analysis import mapping, pca
from scipy.spatial.distance import pdist, squareform
from scipy.linalg import eigh
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def new_points(map, method='coco', npoints=1):
    """
    The CoCo (Complementary Coordinates) methods. The input is an
    MDPlus Map object defining the sampling so far of the conformational space.
    Various CoCo methods will identify 'interesting' regions to
    be sampled next.
    """
    if method == 'coco':
        """
        returns new points, generated using the COCO procedure,
        in the form of an (npoints,D) numpy array, where D is the number of
        dimensions in the map.
        """
        cp = np.zeros((npoints,map.ndim))
        # make a temporary binary image, and invert
        tmpimg = np.where(map._H > 0, 0, 1)
        for i in range(npoints):
            dis = nd.morphology.distance_transform_edt(tmpimg)
            indMax = np.unravel_index(dis.argmax(),dis.shape)
            for j in range(map.ndim):
                cp[i,j]=map._edges[j][0]+indMax[j]*map.cellsize[j]
            
            tmpimg[indMax] = 0
        return cp

    elif method == 'hpoints':
        """
        hpoints returns new points that form a halo of unsampled space
        just beyond the sampled region.
        """
        # This is the halo filter:
        def f(arr):
            cval = arr[len(arr)/2]
            if cval == 0 and np.max(arr) > 0:
                return 1
            else:
                return 0

        halo = nd.filters.generic_filter(map._H,f,size=3,mode='constant')
        npoints = int(np.sum(halo))
        hp = np.zeros((npoints,map.ndim))
        for i in range(npoints):
            indMax = np.unravel_index(halo.argmax(),map.shape)
            for j in range(map.ndim):
                hp[i,j]=map.edges[j][0]+indMax[j]*map.cellsize[j]
            
            halo[indMax] = 0
        return hp

    elif method == 'fpoints':
        """
        fpoints returns new points at the frontier of sampled space
        """
        # This is the frontier filter:
        def f(arr):
            cval = arr[len(arr)/2]
            if cval > 0 and np.min(arr) == 0:
                return 1
            else:
                return 0

        front = nd.filters.generic_filter(map._H,f,size=3,mode='constant')
        npoints = int(np.sum(front))
        fp = np.zeros((npoints,map.ndim))
        for i in range(npoints):
            indMax = np.unravel_index(front.argmax(),map.shape)
            for j in range(map.ndim):
                fp[i,j]=map._edges[j][0]+indMax[j]*map.cellsize[j]
            
            front[indMax] = 0
        return fp

    elif method == 'bpoints':
        """
        bpoints() returns new points not at the frontier of sampled space
        """
        # This is the buried filter:
        def f(arr):
            cval = arr[len(arr)/2]
            if cval > 0 and np.min(arr) > 0:
                return 1
            else:
                return 0

        bur = nd.filters.generic_filter(map._H,f,size=3,mode='constant')
        npoints = int(np.sum(bur))
        bp = np.zeros((npoints,map.ndim))
        for i in range(npoints):
            indMax = np.unravel_index(bur.argmax(),map.shape)
            for j in range(map.ndim):
                bp[i,j]=map._edges[j][0]+indMax[j]*map.cellsize[j]
            
            bur[indMax] = 0
        return bp

    elif method == 'rpoints':
        """
        rpoints() returns one point per bin of sampled space, and its weight
        """

        tmpimg = map._H.copy()
        hsum = np.sum(map._H)
        npoints = tmpimg[np.where(tmpimg > 0)].size
        wt = np.zeros((npoints))
        rp = np.zeros((npoints,map.ndim))
        for i in range(npoints):
            indMax = np.unravel_index(tmpimg.argmax(),map.shape)
            for j in range(map.ndim):
                rp[i,j]=map._edges[j][0]+indMax[j]*map.cellsize[j]
            
            tmpimg[indMax] = 0
            wt[i] = map._H[indMax]/hsum
        return rp,wt

    else:
        raise ValueError('Unknown method: {}'.format(method))

def complement(trajectory, selection='all', npoints=1, gridsize=10, ndims=3, refine=False, logfile=None, nskip=0, rank=0, currentpoints=None, newpoints=None):
    '''The CoCo process as a function.

    Args:
        trajectory (MDTraj Trajectory): Input trajectory
        selection (MDTraj selection): atoms to include in the analysis
        npoints (int): Number of new points to generate
        gridsize (int): number of bins in each dimension of the histogram
        ndims (int): number of dimensions to use in the PCA
        refine (Bool): whether or not to refine approximate structures
        logfile (file): Open file handle where info may be written
        nskip (int): Number of top PCs to ignore.
        rank (int): MPI rank (to control log messages)
        currentpoints (str): The file listing the projections of input points
        newpoints (str): The file listing projections of new points

    Returns:
        MDTraj Trajectory of new structures
    '''
    if not isinstance(trajectory, mdt.Trajectory):
        raise TypeError('Error: trajectory must be an MDTraj trajectory')

    sel = trajectory.topology.select(selection)
    nsel = len(sel)
    if nsel == 0:
        raise ValueError('Error: selection matches no atoms')
    
    # Some sanity checking for situations where few input structures have
    # been given. If there is just one, just return copies of it. If there
    # are < 5, ensure ndims is reasonable, and that the total number of 
    # grid points (at which new structures might be generated) is OK too.
    # Adust both ndims and gridsize if required, giving warning messages.
    out_traj = trajectory[0]
    tmp_traj = trajectory[0]
    for rep in range(npoints - 1):
        out_traj += tmp_traj

    if len(trajectory) == 1:
        if logfile is not None:
            logfile.write("WARNING: Only one input structure given, CoCo\n")
            logfile.write("procedure not possible, new structures will be\n")
            logfile.write("copies of the input structure.\n")

        if rank == 0:
            log.info('Warning: only one input structure!')
    else:
        tmp_traj = mdt.Trajectory(trajectory.xyz[0], trajectory.topology)
        tmp_traj.topology = trajectory.topology.subset(sel)
        tmp_traj.xyz = trajectory.xyz[:,sel]
        
        if rank == 0:
            log.info('running pcazip...')
        p = pca.fromtrajectory(tmp_traj)
        if rank == 0:
            log.info('Total variance: {0:.2f}'.format(p.totvar))
            
        if len(tmp_traj) <= ndims or p.n_vecs < ndims: 
            ndims = min(len(tmp_traj) - 1, p.n_vecs)
            if rank == 0:
                log.info("Warning - resetting ndims to {}".format(ndims))
                if logfile is not None:
                    logfile.write('Warning - ndims must be smaller than the\n')
                    logfile.write("number of input structures, resetting it to {}\n\n".format(ndims))

        ntot = ndims * gridsize
        if ntot < npoints:
            gridsize = (npoints/ndims) + 1
            if rank == 0:
                log.info("Warning - resetting gridsize to {}".format(gridsize))
                if logfile is not None:
                    logfile.write('Warning - gridsize too small for number of\n')
                    logfile.write("output structures, resetting it to {}\n\n".format(gridsize))
       
        if logfile is not None:
            logfile.write("Total variance in trajectory data: {0:.2f}\n\n".format(p.totvar))
            logfile.write("Conformational sampling map will be generated in\n")
            logfile.write("{0} dimensions at a resolution of {1} points\n".format(ndims, gridsize))
            logfile.write("in each dimension.\n\n")
            logfile.write("{} complementary structures will be generated.\n\n".format(npoints))
        projsSel = p.projs[nskip:ndims + nskip].T
                    
        if currentpoints is not None and rank == 0:
            np.savetxt(currentpoints, projsSel)

        # Build a map from the projection data.
        m = mapping.Map(projsSel, resolution=gridsize, boundary=1)
        # Report on characteristics of the COCO map:
        
        if logfile is not None:
            logfile.write("Sampled volume: {0:6.0f} Ang.^{1}.\n".format(m.volume, ndims))
        # Find the COCO points.
        nreps = int(npoints)
        if rank == 0:
            log.info('generating new points...')
        cp = new_points(m, npoints=nreps)
        
        if newpoints is not None and rank == 0:
            np.savetxt(newpoints, cp)

        if logfile is not None:
            logfile.write("\nCoordinates of new structures in PC space:\n")
            for i in range(nreps):
                logfile.write( '{:4d}'.format(i))
                for j in cp[i]:
                    logfile.write(' {:6.2f}'.format(j))
                logfile.write('\n')

        for rep in range(nreps):
            # add zeros to start of cp if we are skipping over top EVs
            stmp = [0.0] * nskip + list(cp[rep])
            # Convert the point to a crude structure.
            e = p.scores(p.closest(stmp))
            e[:len(stmp)] = stmp
            crude = p.unmap(e, regularize=refine) * 0.1

            # merge the optimised subset into the full coordinates array:
            tmp_traj = out_traj[rep]
            tmp_traj.xyz[0, sel] = crude
            tmp_traj.superpose(out_traj[rep], atom_indices=sel)
            out_traj.xyz[rep, sel] = tmp_traj.xyz[0, sel]

    return out_traj
def dm2x(dm):
    """
    Convert a distance matrix to a set of coordinates.

    See:
        https://math.stackexchange.com/questions/156161/finding-the-coordinates-of-points-from-distance-matrix

    Args:
        dm (vector): distance matrix in condensed form.

    Returns:
        [natoms, 3] numpy array of coordinates.

    """
    d = squareform(dm)
    d2 = d * d
    m = np.zeros_like(d2)
    for i in range(d2.shape[0]):
        for j in range(d2.shape[1]):
            m[i,j] = (d2[0, i] + d2[0, j] - d2[i, j]) / 2
    w, v = eigh(m)
    wr = np.sqrt(np.where(w > 0, w, 0))
    reconstructed_xyz = (wr * v)[:, -3:]
    return reconstructed_xyz

def dm_complement(trajectory, selection, npoints, ndims, ntrials=1000, 
                  radius=10.0, ethresh=7.0, bump_scale=1.0, rank=0, 
                  logfile=None, currentpoints=None, newpoints=None):
    """
    The CoCo method(ish) using PCA in distance matrix space.
    
    Args:
        trajectoryj (MD Trajectory): Input trajectory
        selection (MDTraj selection): atoms to include in the analysis
        npoints (int): Number of new structures to returng
        ndims (int): number of dimensions to use in the PCA
        ntrials (int): number of trial structures to generate
        radius (float): the search radius (in multiples of the first eigenvalue)
        ethresh (float): cutoff to reject bad structures (units of mean Z-scores of values
                         in the distance matrix compared to the input data)
        bump_scale (float): scaling factor applied to rejection of trial structures
                            with close contacts (units of the fraction of the minimum
                            value found in the input data)
                            
        logfile (file): Open file handle where info may be written
        rank (int): MPI rank (to control log messages)
        currentpoints (str): The file listing the projections of input points
        newpoints (str): The file listing projections of new points

    Returns:
        MDTraj Trajectory of new structures
    """
    if not isinstance(trajectory, mdt.Trajectory):
        raise TypeError('Error: trajectory must be an mdt.Trajectory')

    sel = trajectory.topology.select(selection)
    nsel = len(sel)
    if nsel == 0:
        raise ValueError('Error: selection matches no atoms')
    
    # Some sanity checking for situations where few input structures have
    # been given. If there is just one, just return copies of it. If there
    # are < 5, ensure ndims is reasonable, and that the total number of 
    # grid points (at which new structures might be generated) is OK too.
    # Adust both ndims and gridsize if required, giving warning messages.
    
    out_traj = trajectory[0]
    tmp_traj = trajectory[0]
    for rep in range(npoints - 1):
        out_traj += tmp_traj

    if len(trajectory) == 1:
        if logfile is not None:
            logfile.write("WARNING: Only one input structure given, CoCo\n")
            logfile.write("procedure not possible, new structures will be\n")
            logfile.write("copies of the input structure.\n")
        if rank == 0:
            log.info('Warning: only one input structure!')
    else:
        tmp_traj = mdt.Trajectory(trajectory.xyz[0], trajectory.topology)
        tmp_traj.topology = trajectory.topology.subset(sel)
        tmp_traj.xyz = trajectory.xyz[:,sel]

        if len(tmp_traj) <= ndims: 
            ndims =len(tmp_traj) - 1
            if rank == 0:
                log.info("Warning - resetting ndims to {}".format(ndims))
                if logfile is not None:
                    logfile.write('Warning - ndims must be smaller than the\n')
                    logfile.write("number of input structures, resetting it to {}\n\n".format(ndims))

       
        if rank == 0:
            log.info('calculating distance matrices...')

        dm_series = np.array([pdist(x) for x in tmp_traj.xyz])
        dm_mean = dm_series.mean(axis=0)
        dm_std = dm_series.std(axis=0)
        dmin = dm_series.min() * bump_scale
    
        if rank == 0:
            log.info('Running PCA...')

        pca = PCA(n_components=ndims)
        pca.fit(dm_series)
        pval = pca.explained_variance_[0] * radius
    
        if rank == 0:
            log.info('Total variance: {0:.2f}'.format(pca.explained_variance_.sum()))
            
        if logfile is not None:
            logfile.write("Total variance in trajectory data: {0:.2f}\n\n".format(pca.explained_variance_.sum()))
            logfile.write("Conformational sampling will be performed in\n")
            logfile.write("{0} dimensions at a radius of {1} \n".format(ndims,radius))
            logfile.write("from the data centroid.\n\n")
            logfile.write("{} complementary structures will be generated.\n\n".format(npoints))
                    
        if currentpoints is not None and rank == 0:
            np.savetxt(currentpoints, pca.transform(dm_series))

        if rank == 0:
            log.info('Looking for complementary structures...')

        new_projs = []
        d_bad = 0
        e_bad = 0
        while len(new_projs) < npoints:
            for i in range(ntrials):
                test_projs = np.random.sample(ndims) - 0.5
                l = np.sqrt((test_projs * test_projs).sum())
                test_projs = test_projs * pval / l
        
                test_dm = pca.inverse_transform([test_projs])[0]
    
                if test_dm.min() > dmin:
                    d = test_dm - dm_mean
                    e = ((d * d) / (dm_std * dm_std)).mean()
                    if e < ethresh:
                        new_projs.append(test_projs)
                    else:
                        e_bad += 1
                else:
                    d_bad += 1
            if len(new_projs) < npoints:
                pval = pval * 0.7
                radius = radius * 0.7
                log.warn('Warning: search radius reduced to {}'.format(radius))
    
        new_projs = np.array(new_projs)
        labels = KMeans(n_clusters=npoints, random_state=0).fit_predict(new_projs)
        selection = []
        for i in range(npoints):
            j = np.where(labels == i)
            selection.append(j[0][0])
        select_proj = new_projs[selection]

        if newpoints is not None and rank == 0:
            np.savetxt(newpoints, select_proj)

        if logfile is not None:
            logfile.write("\nCoordinates of new structures in PC space:\n")
            for i in range(npoints):
                logfile.write( '{:4d}'.format(i))
                for j in select_proj[i]:
                    logfile.write(' {:6.2f}'.format(j))
                logfile.write('\n')

        select_dms = pca.inverse_transform(select_proj)
        select_xyz = []
        test_traj = mdt.Trajectory(tmp_traj.xyz[0], tmp_traj.topology)
        for dm in select_dms:
            # Convert distance matrix to coordinates
            x = dm2x(dm)
            # Check for inversion
            test_traj.xyz = x
            rmsd1 = mdt.rmsd(tmp_traj[0], test_traj)[0]
            x[:,0] = -x[:,0]
            test_traj.xyz = x
            rmsd2 = mdt.rmsd(tmp_traj[0], test_traj)[0]
            if rmsd2 > rmsd1:
                x[:,0] = -x[:,0]
            test_traj.superpose(tmp_traj[0])
            select_xyz.append(test_traj.xyz[0])

        for rep in range(npoints):
            # merge the optimised subset into the full coordinates array:
            out_traj.xyz[rep, sel] = select_xyz[rep]
    return out_traj
