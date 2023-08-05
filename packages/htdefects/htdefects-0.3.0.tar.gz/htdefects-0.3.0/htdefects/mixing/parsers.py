# -*- coding: utf-8 -*-

"""Helper functions to parse mixing calculations."""

import os

from dftinpgen import atoms
from dfttopif.drivers import directory_to_pif
from pypif.pif import Property, Scalar


class ParserError(Exception):
    """Base class for errors related to parsing info from DFT calculations."""
    pass


def get_number_of_atoms(calc_dir):
    """Gets the number of atoms in the structure in the specified directory.

    Uses parsers in the :mod:`dfttopif.parsers` module (i.e., this function
    is only a light wrapper; no explicit functionality is implemented here).

    Parameters
    ----------

    calc_dir: str
        Path to the directory with the DFT calculation files.

    Returns
    -------

    :class:`pypif.pif.Property` or None
        Number of atoms in the crystal structure in the specified directory.

    """
    if calc_dir is None:
        return None
    chem = directory_to_pif(calc_dir, quality_report=False)
    natoms = list(filter(lambda x: 'number of atoms' in x.name.lower(),
                         chem.properties))
    if not natoms:
        return None
    return natoms[0]


def get_total_energy(calc_dir):
    """Gets the total energy from the DFT calculation files in the
    specified directory.

    Uses parsers in the :mod:`dfttopif.parsers` module (i.e., this function
    is only a light wrapper; no explicit functionality is implemented here).

    Parameters
    ----------

    calc_dir: str
        Path to the directory with the DFT calculation files.

    Returns
    -------

    :class:`pypif.pif.Property` or None
        Final total energy from the DFT calculation files found in
        the specified calculations directory.

    """
    if calc_dir is None:
        return None
    chem = directory_to_pif(calc_dir, quality_report=False)
    toten = list(filter(lambda x: 'total energy' in x.name.lower(),
                        chem.properties))
    if not toten:
        return None
    return toten[0]


def get_total_energy_pa(toten, natoms):
    """Calculates the total energy per atom.

    Parameters
    ----------

    toten: :class:`pypif.pif.Property`
        Total energy.

    natoms: :class:`pypif.pif.Property`
        Number of atoms in the structure (to normalize with).

    Returns
    -------

    :class:`pypif.pif.Property` or None
        Total energy per atom if both quantities are provided, else None.

    """
    if not toten or not natoms:
        return None
    toten_pa = toten.scalars[0].value/float(natoms.scalars[0].value)
    return Property(name='Total energy per atom',
                    methods=toten.methods,
                    conditions=toten.conditions,
                    data_type='COMPUTATIONAL',
                    scalars=[Scalar(value=toten_pa)],
                    units='eV/atom')


def get_volume(calc_dir):
    """Gets the volume of the structure from the DFT calculation files in the
    specified directory.

    Uses parsers in the :mod:`dfttopif.parsers` module (i.e., this function
    is only a light wrapper; no explicit functionality is implemented here).

    Parameters
    ----------

    calc_dir: str
        Path to the directory with the DFT calculation files.

    Returns
    -------

    :class:`pypif.pif.Property` or None
        Final structural volume from the DFT calculation files found in
        the specified calculations directory.

    """
    if calc_dir is None:
        return None
    chem = directory_to_pif(calc_dir, quality_report=False)
    volume = list(filter(lambda x: 'final volume' in x.name.lower(),
                         chem.properties))
    if not volume:
        return None
    return volume[0]


def get_volume_pa(vol, natoms):
    """Calculates volume per atom.

    Parameters
    ----------

    vol: :class:`pypif.pif.Property`
        Total volume.

    natoms: :class:`pypif.pif.Property`
        Number of atoms in the structure (to normalize with).

    Returns
    -------

    :class:`pypif.pif.Property` or None
        Volume per atom if both quantities are provided, else None.

    """
    if not vol or not natoms:
        return None
    vol_pa = vol.scalars[0].value/float(natoms.scalars[0].value)
    return Property(name='Volume per atom',
                    methods=vol.methods,
                    conditions=vol.conditions,
                    data_type='COMPUTATIONAL',
                    scalars=[Scalar(value=vol_pa)],
                    units='Angstrom^3/atom')


def get_ntv_data(calc_dir):
    """Gets the number of atoms, total energy per atom, and volume per atom
    from the DFT calculation files found in specified directory.

    Parameters
    ----------

    calc_dir: str
        Path to the directory with the DFT calculation files.

    Returns
    -------

    dict(str, :class:`pypif.pif.Property` or None)
        Dictionary of number of atoms, total energy and volume data.

    """
    natoms = get_number_of_atoms(calc_dir)
    props = {
        'number_of_atoms': natoms,
        'total_energy_per_atom': get_total_energy_pa(
                get_total_energy(calc_dir), natoms),
        'volume_per_atom': get_volume_pa(get_volume(calc_dir), natoms)
    }
    return props


def parse_mixing_calculations_data(mixing_calculations=None):
    """Parse all properties from mixing calculations.

    Parameters
    ----------

    mixing_calculations: dict
        Dictionary of DFT calculations for the solvent and solute reference
        structures, and the dilute mixing defect structure.

        For the nested structure of the dictionary, refer to documentation
        for :attr:`htdefects.mixing.calculation.mixing_calculations`.

    Returns
    -------

    dict
        Dictionary of data (number of atoms, total energy per atom, volume
        per atom) for the solvent and all the solutes in the mixing defects
        set. The nested structure of the dictionary is similar to that of
        :attr:`htdefects.mixing.calculation.mixing_calculations`.

        Properties for solvent/solutes not found are None.

    """
    if not mixing_calculations:
        return {}

    calcs_data = dict()

    # solvent calculation data
    calcs_data['solvent'] = get_ntv_data(mixing_calculations['solvent'][
                                             'static'].directory)

    # all solutes calculation data
    calcs_data['solutes'] = {}
    for solute in mixing_calculations['solutes']:
        calcs_data['solutes'][solute] = {}
        for ref in ['defect', 'solvent_structure', 'reference_structure']:
            calcs_data['solutes'][solute][ref] = None
            try:
                calcs_data['solutes'][solute][ref] = get_ntv_data(
                        mixing_calculations['solutes'][solute][ref][
                            'static'].directory)
            except TypeError:  # missing structures = None (not DftCalc)
                pass
    return calcs_data


def parse_calculations_from_tree(base_dir=None):
    """Parse DFT mixing calculations from the specified directory.

    The directory tree starting from the specified root directory is
    traversed, and the relevant folders are parsed to get the relevant data
    (number of atoms, total energy per atom, volume per atom).

    Parameters
    ----------

    base_dir: str
        Path to the root calculation directory.

    Returns
    -------
    dict
        Dictionary of data (number of atoms, total energy per atom, volume
        per atom) for the solvent and all the solutes in the mixing defects
        set, if the corresponding DFT calculation folders are found while
        traversing the tree. The nested structure of the dictionary is similar
        to that of :attr:`htdefects.mixing.calculation.mixing_calculations`.

        Properties for solvent/solutes not found are None.

    Raises
    ------

    ParserError if the specified root directory is not found.

    """
    if not base_dir:
        err_msg = 'Base directory for calculations not specified'
        raise ParserError(err_msg)

    if not os.path.isdir(base_dir):
        err_msg = 'Specified directory {} not found'.format(base_dir)
        raise ParserError(err_msg)

    calcs_data = dict()

    # solvent calculation data
    calc_dir = os.path.join(base_dir, 'solvent', 'static')
    if os.path.exists(calc_dir):
        calcs_data['solvent'] = get_ntv_data(calc_dir)

    # all solutes calculation data
    calcs_data['solutes'] = {}
    solutes_dir = os.path.join(base_dir, 'solutes')
    if os.path.exists(solutes_dir):
        for root, dirnames, filenames in os.walk(solutes_dir):
            try:
                solute, ref, calc = root.split('/')[-3:]
            except ValueError:
                continue
            if not calc == 'static':
                continue
            if solute not in atoms.ATOMIC_MASSES:
                continue
            if ref not in ['defect',
                           'solvent_structure',
                           'reference_structure']:
                continue
            if solute not in calcs_data['solutes']:
                calcs_data['solutes'][solute] = {
                    'solvent_structure': None,
                    'reference_structure': None,
                    'defect': None
                }
            calcs_data['solutes'][solute].update({ref: get_ntv_data(root)})

    return calcs_data
