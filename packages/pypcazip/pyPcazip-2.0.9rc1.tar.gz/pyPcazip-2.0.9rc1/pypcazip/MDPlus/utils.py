from __future__ import absolute_import, print_function, division
import numpy as np
from scipy.spatial.distance import pdist, squareform
from mdio.rmsd_utils import kabsch_rmsd, kabsch_fit

def pib(coords, box):
    """
    Pack coordinates into periodic box.

    Args:
        coords: (N,3) numpy array of atom coordinates.
        box: (3,3) numpy array of box parameters.

    Returns:
        coords: (N,3) numpy array of packed coordinates (overwrites input).
    """
    import numpy as np

    import numpy as np

    assert len(coords.shape) == 2
    assert coords.shape[1] == 3
    assert box.shape == (3, 3)

    boxinv = np.zeros((3))
    boxinv[0] = 1.0 / box[0,0]
    boxinv[1] = 1.0 / box[1,1]
    boxinv[2] = 1.0 / box[2,2]

    for xyz in coords:
        s = np.floor(xyz[2] * boxinv[2])
        xyz[2] -= s * box[2,2]
        xyz[1] -= s * box[2,1]
        xyz[0] -= s * box[2,0]

        s = np.floor(xyz[1] * boxinv[1])
        xyz[1] -= s * box[1,1]
        xyz[0] -= s * box[1,0]

        s = np.floor(xyz[0] * boxinv[0])
        xyz[0] -= s * box[0,0]

    return coords

def pdb2selection(pdbfile):
    '''
    Create selection strings from pdbfile data.

    A little utility function to convert 'mask' pdb files into
    MDTraj-style selection strings. Basically it reads the second column
    (atom number) and uses it to construct 'index' selections. Runs
    of consecutive numbers are expressed in 'start to stop' form.

    Args:
        pdbfile (str): Name of a PDB file

    Returns:
        selection (str): MDtraj format selection string
    '''

    sel = ''
    i = 0
    j = 0
    with open(pdbfile, 'r') as f:
        for line in f:
            if line.find('ATOM') == 0 or line.find('HETATM') == 0:
                k = int(line.split()[1])
                # the next line catches the initialization process:
                if i == 0:
                    i = k
                    j = k - 1
                # are we in a run of consecutive numbers?:
                if k == j + 1:
                    j = k
                else:
                    # time to write out another selection:
                    sel = sel + ' index {0} to {1} or'.format(i, j)
                    i = k
                    j = k
                # end-of-file reached. Make sure last selection is included:
    if i > 0 and j > 0:
        sel = sel + ' index {0} to {1} or'.format(i, j)
    if len(sel) > 3:
        # remove the trailing ' or':
        sel = sel[:-3]
    return sel

def _xfix(Xin, Dref, known):
    """
    Shake type procedure: adjust selected interatomic distances in Xin to move towards
    the values in Dref
    
    """
    D = squareform(pdist(Xin))
    DX = np.zeros_like(Xin)
    C = np.zeros_like(Xin)
    n = len(D)
    for i in range(n -1):
        for j in range(i+1, n):
            if known[i,j]:
                dij = D[i, j]
                ddij = (Dref[i, j] - dij)
                ddij = ddij * 0.5
                v = Xin[j] - Xin[i]
                DX[j] += v * ddij / dij
                DX[i] -= v * ddij / dij
                C[i] += 1
                C[j] += 1
                
    C = np.where(C == 0, 1, C)
    DX = DX / C
    Xout = Xin + DX
    return Xout

def make_ba(X, topology, angles=False):
    """
    Construct a 2D logical array of bonds and (optionally) angles.
    Entry[i,j] is True if atoms i and j are bonded or (optionally) 1,3 related.

    Args:
        X ([N, 3] numpy array): coordinates
        top (mdio.Topology): topology
        angles(logical, optional): If true, both bonds and angles are found.

    Returns:
        ba[N,N]: Boolean numpy array, entries are True where i and j are bonded
                 or 1,3 related.
    
    """
    D = squareform(pdist(X))
    n_atoms = len(X)
    
    ba = D < -1.0
    for i in range(n_atoms - 1):
        ri = topology.atom(i).element.radius
        for j in range(i + 1, n_atoms):
            rj = topology.atom(j).element.radius
            if (ri + rj) * 1.2 > D[i, j]:
                ba[i, j] = True
                ba[j, i] = True
                
    if angles:
        anglearr = D < -1.0
        for i in range(n_atoms - 1):
            for j in range(i + 1, n_atoms):
                if ba[i, j]:
                    for k in range(n_atoms):
                        if k != i:
                            anglearr[i, k] = ba[j, k]
                            anglearr[k, i] = anglearr[i, k]
        ba = ba + anglearr
    return ba

def refine(Xcrude, Xref, ba, tol=0.01):
    """
    Refine a set of coordinates.
    
    The method involves an iterative process of adjusting coordinates 
    in the input structure to match a set of interatomic distances in
    the target structure until the rmsd between the two converges.

    Args:
        Xcrude ([N, 3] numpy array): Input coordinates
        Xref ([N, 3] numpy array): Reference (target) coordinates
        ba ([N, N] logical numpy array): Flags bonds and angles
        tol (float) : target tolerance for bond length error

    Returns:
        [N, 3] numpy array: refined coordinates.
    """
    
    Xnew = Xcrude
    Dref = squareform(pdist(Xref))
    Dnew = squareform(pdist(Xnew))
    DD = Dnew - Dref
    DD = np.where(ba, DD, 0.0)
    new_err2 = (DD * DD).mean()
    old_err2 = new_err2 + 1.0
    tol2 = tol * tol
    while old_err2 - new_err2 > tol2:
        old_err2 = new_err2
        Xnew = xfix(Xnew, Dref, ba)
        Dnew = squareform(pdist(Xnew))
        DD = Dnew - Dref
        DD = np.where(ba, DD, 0.0)
        new_err2 = (DD * DD).mean()
        print(new_err2)
    
    return Xnew

