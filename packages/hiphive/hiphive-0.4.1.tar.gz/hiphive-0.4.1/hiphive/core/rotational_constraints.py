"""
Functionality for enforcing rotational sum rules
"""
from sklearn.linear_model import Ridge
import numpy as np
from scipy.sparse import coo_matrix
from .utilities import SparseMatrix


def enforce_rotational_sum_rules(cs, parameters, sum_rules, **kwargs):
    """ Enforces rotational sum rules by projecting parameters.

    Note
    ----
    The interface to this function might change in future releases.

    Parameters
    ----------
    cs : ClusterSpace
        the underlying cluster space
    parameters : numpy.ndarray
        parameters to be constrained
    sum_rules : list(str)
        type of sum rules to enforce; possible values: 'Huang', 'Born-Huang'
    ridge_alpha : float
        hyperparameter to the ridge regression algorithm; keyword argument
        passed to the optimizer; larger values specify stronger regularization,
        i.e. less correction but higher stability [default: 1e-6]
    iterations : int
        number of iterations to run the projection since each step projects
        the solution down to each nullspace in serial; keyword argument
        passed to the optimizer [default: 10]

    Returns
    -------
    numpy.ndarray
        constrained parameters

    Examples
    --------
    The rotational sum rules can be enforced to the parameters before
    constructing a force constant potential as illustrated by the following
    snippet::

        cs = ClusterSpace(reference_structure, cutoffs)
        sc = StructureContainer(cs)
        # add structures to structure container
        opt = Optimizer(sc.get_fit_data())
        opt.train()
        new_params = enforce_rotational_sum_rules(cs, opt.parameters,
            sum_rules=['Huang', 'Born-Huang'])
        fcp = ForceConstantPotential(cs, new_params)
    """
    parameters = parameters.copy()
    # handle optional kwargs input
    iterations = kwargs.pop('iterations', 10)
    ridge_alpha = kwargs.pop('ridge_alpha', 1e-6)
    if len(kwargs) != 0:
        raise ValueError('Unrecognised kwargs: {}'.format(kwargs))

    # make orbit-parameter index map
    params = []
    n = 0
    for orbit_index, orbit in enumerate(cs.orbits):
        number_params_in_orbit = len(orbit.eigentensors)
        params.append(list(range(n, n + number_params_in_orbit)))
        n += number_params_in_orbit

    # create lookuptable for force constants
    lookup = {}
    for orbit_index, orbit in enumerate(cs.orbits):
        for of in orbit.orientation_families:
            for cluster_index, perm_index in zip(of.cluster_indices,
                                                 of.permutation_indices):
                cluster = cs._cluster_list[cluster_index]
                perm = cs._permutations[perm_index]
                lookup[tuple(cluster)] = [et.transpose(perm) for et in
                                          of.eigentensors], orbit_index

    # append the sum rule matrices
    Ms = []
    args = (lookup, params, cs.atom_list, cs._prim)
    for sum_rule in sum_rules:
        if sum_rule == 'Huang':
            Ms.append(_create_Huang_constraint(*args))
        elif sum_rule == 'Born-Huang':
            Ms.append(_create_Born_Huang_constraint(*args))
        else:
            raise ValueError('At least one unknown sum rule: {}'
                             .format(sum_rule))

    cvs_trans = cs._cvs

    for i, M in enumerate(Ms):
        row, col, data = [], [], []
        for r, c, v in M.row_list():
            row.append(r)
            col.append(c)
            data.append(np.float64(v))
        M = coo_matrix((data, (row, col)), shape=M.shape)
        Ms[i] = M.dot(cvs_trans)

    for _ in range(iterations):
        for M in Ms:
            clf = Ridge(alpha=ridge_alpha)
            d = M.dot(parameters)
            clf.fit(M, d)
            parameters -= clf.coef_  # subtract the correction

    return parameters


def _create_Huang_constraint(lookup, parameter_map, atom_list, prim):

    m = SparseMatrix(3**4, parameter_map[-1][-1] + 1, 0)

    def R(i, j):
        pi = atom_list[i].pos(prim.basis, prim.cell)
        pj = atom_list[j].pos(prim.basis, prim.cell)
        return pi - pj

    for i in range(len(prim)):
        for j in range(len(atom_list)):
            ets, orbit_index = lookup.get(tuple(sorted((i, j))), (None, None))
            if ets is None:
                continue
            inv_perm = np.argsort(np.argsort((i, j)))
            et_indices = parameter_map[orbit_index]
            for et, et_index in zip(ets, et_indices):
                et = et.transpose(inv_perm)
                Rij = R(i, j)
                Cij = np.einsum(et, [0, 1], Rij, [2], Rij, [3])
                Cij -= Cij.transpose([2, 3, 0, 1])
                for k in range(3**4):
                    m[k, et_index] += Cij.flat[k]
    return m


def _create_Born_Huang_constraint(lookup, parameter_map, atom_list, prim):

    constraints = []

    for i in range(len(prim)):
        m = SparseMatrix(3**3, parameter_map[-1][-1] + 1, 0)
        for j in range(len(atom_list)):
            ets, orbit_index = lookup.get(tuple(sorted((i, j))), (None, None))
            if ets is None:
                continue
            inv_perm = np.argsort(np.argsort((i, j)))
            et_indices = parameter_map[orbit_index]
            R = atom_list[j].pos(prim.basis, prim.cell)
            for et, et_index in zip(ets, et_indices):
                et = et.transpose(inv_perm)
                tmp = np.einsum(et, [0, 1], R, [2])
                tmp -= tmp.transpose([0, 2, 1])
                for k in range(3**3):
                    m[k, et_index] += tmp.flat[k]
        constraints.append(m)

    M = SparseMatrix.vstack(*constraints)
    return M
