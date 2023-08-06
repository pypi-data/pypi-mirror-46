"""
This module contains various support/utility functions.
"""

import numpy as np
from ase.geometry import find_mic
from ase.geometry import get_distances
from .io.logging import logger

from hiphive.force_constant_model import ForceConstantModel


logger = logger.getChild('utilities')


def get_displacements(atoms, atoms_ideal):
    """ Computes the smallest possible displacements from displaced
    atoms relative to ideal atoms.

    Notes
    -----
    * uses :func:`ase.geometry.find_mic`
    * assumes `pbc=[True, True, True]`.

    Parameters
    ----------
    atoms : ase.Atoms
        configuration with displaced atoms
    atoms_ideal : ase.Atoms
        ideal configuration relative to which displacements are computed

    Returns
    -------
    numpy.ndarray
        displacements
    """
    if not np.array_equal(atoms.numbers, atoms_ideal.numbers):
        raise ValueError('Atomic numbers do not match.')

    displacements = []
    for pos, ideal_pos in zip(atoms.positions, atoms_ideal.positions):
        v_ij = np.array([pos - ideal_pos])
        displacements.append(find_mic(v_ij, atoms_ideal.cell, pbc=True)[0][0])
    return np.array(displacements)


def prepare_structures(structures, atoms_ideal, calc):
    """
    Prepares a set of structures in the format suitable for a
    :class:`StructureContainer <hiphive.StructureContainer>`.

    **Note:** Changes the structures in place.
    """
    for atoms in structures:
        atoms.set_calculator(calc)
        forces = atoms.get_forces()
        displacements = get_displacements(atoms, atoms_ideal)
        atoms.positions = atoms_ideal.get_positions()
        atoms.new_array('forces', forces)
        atoms.new_array('displacements', displacements)


def find_permutation(atoms, atoms_ref):
    """ Finds the best permutation for mapping atoms to atoms_ref.

    E.g.
    p = find_permuation(atoms1, atoms2)
    atoms1[p] == atoms2

    """
    assert np.linalg.norm(atoms.cell - atoms_ref.cell) < 1e-10
    dist_matrix = get_distances(
        atoms.positions, atoms_ref.positions, cell=atoms_ref.cell, pbc=True)[1]
    permutation = []
    for i in range(len(atoms_ref)):
        dist_row = dist_matrix[:, i]
        permutation.append(np.argmin(dist_row))

    if len(set(permutation)) != len(permutation):
        raise Exception('Duplicates in permutation')
    for i, p in enumerate(permutation):
        if atoms[p].symbol != atoms_ref[i].symbol:
            raise Exception('Matching lattice sites have different occupation')
    return permutation


def get_neighbor_shells(atoms, cutoff, dist_tol=1e-5):
    """ Gets list of neighbor shells.

    Distances are grouped into shells via the following algorithm:

    1. Find smallest atomic distance `d_min`

    2. Find all pair distances in the range `d_min + 1 * dist_tol`

    3. Construct a shell from these and pop them from distance list

    4. Go to 1.

    Parameters
    ----------
    atoms : ase.Atoms
        Atoms used for finding shells
    cutoff : float
        exclude neighbor shells which have a distance larger than cutoff
    dist_tol : float
        distance tolerance

    Returns
    -------
    list(Shell)
        neighbor shells
    """

    # TODO: Remove this once this feature have been in ASE long enough
    try:
        from ase.neighborlist import neighbor_list
    except ImportError:
        raise ImportError('get_neighbor_shells uses new functionality from ASE'
                          ', please update ASE in order to use this function.')

    # get distances
    ijd = neighbor_list('ijd', atoms, cutoff)
    ijd = list(zip(*ijd))
    ijd.sort(key=lambda x: x[2])

    # sort into shells
    symbols = atoms.get_chemical_symbols()
    shells = []
    for i, j, d in ijd:
        types = tuple(sorted([symbols[i], symbols[j]]))
        for shell in shells:
            if abs(d - shell.distance) < dist_tol and types == shell.types:
                shell.count += 1
                break
        else:
            shell = Shell(types, d, 1)
            shells.append(shell)
    shells.sort(key=lambda x: (x.distance, x.types, x.count))

    # warning if two shells are within 2 * tol
    for i, s1 in enumerate(shells):
        for j, s2 in enumerate(shells[i+1:]):
            if s1.types != s2.types:
                continue
            if not s1.distance < s2.distance - 2 * dist_tol:
                logger.warning('Found two shells within 2 * dist_tol')

    return shells


class Shell:
    """
    Neighbor Shell class

    Parameters
    ----------
    types : list or tuple
        atomic types for neighbor shell
    distance : float
        interatomic distance for neighbor shell
    count : int
        number of pairs in the neighbor shell
    """

    def __init__(self, types, distance, count=0):
        self.types = types
        self.distance = distance
        self.count = count

    def __str__(self):
        s = '{}-{}   distance: {:10.6f}    count: {}'.format(
            *self.types, self.distance, self.count)
        return s

    __repr__ = __str__


def extract_parameters(fcs, cs):
    """ Extracts parameters from force constants

    This function can be used to extract parameters to create a
    ForceConstantPotential from a known set of force constants.

    Parameters
    ----------
    fcs : ForceConstants
    cs : ClusterSpace
    """
    fcm = ForceConstantModel(fcs.supercell, cs)
    return np.linalg.lstsq(*fcm.get_fcs_sensing(fcs), rcond=None)[0]
