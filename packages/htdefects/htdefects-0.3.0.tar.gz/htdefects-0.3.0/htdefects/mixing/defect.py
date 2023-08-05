# -*- coding: utf-8 -*-

"""Module to represent (sets of) dilute mixing defects."""

import copy
import six
import numpy as np

from dftinpgen import atoms

from htdefects.data import ELEM_VOLUMES
from htdefects.mixing import supercell


class MixingDefectError(Exception):
    """Base class for errors associated with a dilute mixing defect."""
    pass


def _validate_input_element(element):
    """Is the input a valid element?"""
    if element not in atoms.ATOMIC_MASSES:
        msg = 'Invalid input element: {}'.format(element)
        raise MixingDefectError(msg)


def _structure_has_element(structure, element):
    """Does structure have the specified element?"""
    if element in structure.atomtypes:
        return True
    else:
        return False


def read_structure_from_file(structure_file):
    """Read the crystal structure in `structure_file` and
    return a :class:`dftinpgen.atoms.Structure` object."""
    structure = atoms.Structure(structure_file)
    return structure


class MixingDefect(object):
    """Class to represent a dilute mixing defect."""

    def __init__(self, solvent_element=None,
                 solvent_reference_structure=None, solute_element=None,
                 solute_reference_structure=None, min_image_dist=None,
                 supercell_for_mixing=None, **kwargs):
        """Constructor.

        Parameters
        ----------

        solvent_element: str
            Symbol of the solvent element.

        solvent_reference_structure: :class:`dftinpgen.atoms.Structure` or str
            Reference crystal structure of the solvent. If input is a
            string, the full path to the structure file must be provided.

        solute_element: str
            Symbol of the solute/impurity element.

        solute_reference_structure: :class:`dftinpgen.atoms.Structure` or str
            Reference crystal structure of the solute. If input is a string,
            the full path to the structure file must be provided.

        min_image_dist: float
            Minimum distance between periodic images of the defect in a
            supercell, in Angstrom.

            Defaults to 12 Angstrom.

        supercell_for_mixing: :class:`dftinpgen.atoms.Structure` or str
            Supercell structure used for creating a dilute mixing defect.
            If input is a string, the full path to the structure file must
            be provided.

        kwargs: dict
            Arbitrary keyword arguments.

        Raises
        ------

        MixingDefectError
            * If the solvent/solute element is not recognized.
            * If the solvent reference structure is not in the correct format.
            * If the solute reference structure is not in the correct format.
            * If the solvent (solute) element is not in the input solvent
              (solute) reference structure.
            * If the mixing supercell does not contain the solvent element.

        """

        self._solvent_element = None
        self.solvent_element = solvent_element

        self._solvent_reference_structure = None
        self.solvent_reference_structure = solvent_reference_structure

        self._solute_element = None
        self.solute_element = solute_element

        self._solute_reference_structure = None
        self.solute_reference_structure = solute_reference_structure

        self._min_image_dist = None
        self.min_image_dist = min_image_dist

        self._supercell_for_mixing = None
        self.supercell_for_mixing = supercell_for_mixing

    @property
    def solvent_element(self):
        """Atomic symbol of the solvent element."""
        return self._solvent_element

    @solvent_element.setter
    def solvent_element(self, solvent_element):
        _validate_input_element(solvent_element)
        self._solvent_element = solvent_element

    @property
    def solvent_reference_structure(self):
        """Reference crystal structure of the solvent."""
        return self._solvent_reference_structure

    @solvent_reference_structure.setter
    def solvent_reference_structure(self, solvent_reference_structure):
        if solvent_reference_structure is None:
            msg = 'Solvent reference structure is not specified'
            raise MixingDefectError(msg)

        if isinstance(solvent_reference_structure, str):
            solvent_reference_structure = read_structure_from_file(
                    solvent_reference_structure)
        if not _structure_has_element(solvent_reference_structure,
                                      self.solvent_element):
            msg = 'Solvent structure must contain solvent element'
            raise MixingDefectError(msg)
        self._solvent_reference_structure = solvent_reference_structure

    @property
    def solute_element(self):
        """Atomic symbol of the solute element."""
        return self._solute_element

    @solute_element.setter
    def solute_element(self, solute_element):
        _validate_input_element(solute_element)
        self._solute_element = solute_element

    @property
    def solute_reference_structure(self):
        """Reference crystal structure of the solute."""
        return self._solute_reference_structure

    @solute_reference_structure.setter
    def solute_reference_structure(self, solute_reference_structure):
        if solute_reference_structure is None:
            return
        if isinstance(solute_reference_structure, str):
            solute_reference_structure = read_structure_from_file(
                    solute_reference_structure)
        if not _structure_has_element(solute_reference_structure,
                                      self.solute_element):
            msg = 'Solute reference structure must contain solute element'
            raise MixingDefectError(msg)
        self._solute_reference_structure = solute_reference_structure

    @property
    def min_image_dist(self):
        """Minimum distance between periodic defect images in Angstrom."""
        return self._min_image_dist

    @min_image_dist.setter
    def min_image_dist(self, min_image_dist):
        self._min_image_dist = 12.0
        if min_image_dist is None:
            return
        self._min_image_dist = float(min_image_dist)

    @property
    def supercell_for_mixing(self):
        """Solvent supercell to use for creating a dilute mixing defect."""
        return self._supercell_for_mixing

    @supercell_for_mixing.setter
    def supercell_for_mixing(self, supercell_for_mixing):
        if supercell_for_mixing is None:
            self._supercell_for_mixing = supercell.get_supercell_for_mixing(
                    structure=self.solvent_reference_structure,
                    min_image_dist=self.min_image_dist,
            )
            return
        elif isinstance(supercell_for_mixing, str):
            supercell_for_mixing = read_structure_from_file(
                    supercell_for_mixing)
        if not _structure_has_element(supercell_for_mixing,
                                      self.solvent_element):
            msg = 'Defect supercell does not contain solvent element'
            raise MixingDefectError(msg)
        self._supercell_for_mixing = supercell_for_mixing

    @property
    def solute_in_solvent_structure(self):
        """Bulk solute in the crystal structure of the solvent.

        The structure is generated by replacing all solvent atoms in
        :attr:`self.solvent_reference_structure` with solute atoms, and
        scaling the lattice vectors according to the elemental volumes of the
        solute and the solvent in their respective ground states (using data
        in :data:`htdefects.ELEM_VOLUMES` dictionary).

        *Note*: Currently implemented only for elemental solvents.

        """
        if len(self.solvent_reference_structure.atomtypes) > 1:
            raise NotImplementedError

        structure = copy.deepcopy(self.solvent_reference_structure)
        structure.title = '{}{}'.format(structure.atomtypes[0],
                                        structure.natoms[0])

        # replace all solvent atoms with solute atoms
        structure.atomtypes = [self.solute_element]
        structure.gen_atominfo()

        # scale the cell isotropically
        volume_ratio = (ELEM_VOLUMES[self.solute_element]/
                        ELEM_VOLUMES[self.solvent_element])
        scaling_factor = volume_ratio**(1./3.)
        structure.cell = np.array([[a_n*scaling_factor for a_n in a]
                                   for a in structure.cell])

        # recalculate ionic positions in cartesian coordinates
        structure.ionsc = np.dot(structure.ions, structure.cell)
        structure.cellinfo()
        return structure

    def replace_solvent_atom_with_solute(self, structure):
        """Substitute a solvent atom in the structure with a solute atom.

        Parameters
        ----------

        structure: :class:`dftinpgen.atoms.Structure`
            Crystal structure (typically supercell) of the solvent.

        Returns
        -------

        :class:`dftinpgen.atoms.Structure`
            Solvent supercell with one substitutional solute atom.

        """
        # Replace a solvent atom in the supercell with the solute
        structure.atomtypes.append(self.solute_element)
        structure.natoms = np.array([structure.natoms.tolist()[0]-1, 1])
        structure.gen_atominfo()

        # Set title as the composition
        title = ''.join(['{}{}'.format(e, n) for e, n in zip(
                structure.atomtypes, structure.natoms)])
        structure.title = title

    @property
    def defect_structure(self):
        """Solvent supercell with a single solute atom."""
        defect = copy.deepcopy(self.supercell_for_mixing)
        self.replace_solvent_atom_with_solute(defect)
        return defect


class MixingDefectSetError(Exception):
    """Base class for errors associated with a set of dilute mixing defects."""
    pass


class MixingDefectSet(object):
    """Class to represent a set of dilute mixing defects."""

    def __init__(self, solvent_element=None, solvent_reference_structure=None,
                 solute_elements=None, solute_reference_structures=None,
                 min_image_dist=None, supercell_for_mixing=None, **kwargs):
        """

        Parameters
        ----------

        solvent_element: str
            Atomic symbol of the solvent element.

        solvent_reference_structure: :class:`dftinpgen.atoms.Structure` or str
            Reference crystal structure of the solvent. If input is a
            string, the full path to the structure file must be provided.

        solute_elements: list(str) or str
            List of atomic symbols of the solutes. A comma-delimited string
            of atomic symbols is also acceptable.

            E.g.: ["Al", "Ca", "Sr", "O"] and "Al,Ca,Sr,O" are equivalent.

        solute_reference_structure: dict(str, str) or dict(str,
            :class:`dftinpgen.atoms.Structure`)
            Dictionary with solute elements as keys and the corresponding
            structures as values. If values are string, the full path to the
            structure file must be provided.

        min_image_dist: float
            Minimum distance between periodic images of a defect in a
            supercell, in Angstrom.

            Defaults to 12 Angstrom.

        supercell_for_mixing: :class:`dftinpgen.atoms.Structure` or str
            Supercell structure used for creating a dilute mixing defect.
            If input is a string, the full path to the structure file must
            be provided.

        kwargs: dict
            Arbitrary keyword arguments.

        Raises
        ------

        MixingDefectSetError
            * If the solvent/solute elements are not recognized.
            * If the solvent reference structure is not in the correct format.
            * If the solute reference structures are not in the correct format.
            * If the solvent (solute) element is not in the input solvent
              (solute) reference structures.
            * If the minimum image distance is reset after initial setup.
            * If the mixing supercell does not contain the solvent element.
            * If a solute already present in the defects set is added.
            * If a solute not present in the defects set is removed.

        """
        self._solvent_element = None
        self.solvent_element = solvent_element

        self._solvent_reference_structure = None
        self.solvent_reference_structure = solvent_reference_structure

        self._solute_elements = None
        self.solute_elements = solute_elements

        self._solute_reference_structures = None
        self.solute_reference_structures = solute_reference_structures

        self._min_image_dist = None
        self.min_image_dist = min_image_dist

        self._supercell_for_mixing = None
        self.supercell_for_mixing = supercell_for_mixing

        self._mixing_defects = None
        self._set_mixing_defects()

    @property
    def solvent_element(self):
        """Atomic symbol of the solvent element."""
        return self._solvent_element

    @solvent_element.setter
    def solvent_element(self, solvent_element):
        _validate_input_element(solvent_element)
        self._solvent_element = solvent_element

    @property
    def solvent_reference_structure(self):
        """Reference crystal structure of the solvent."""
        return self._solvent_reference_structure

    @solvent_reference_structure.setter
    def solvent_reference_structure(self, solvent_reference_structure):
        if solvent_reference_structure is None:
            msg = 'Solvent reference structure is not specified'
            raise MixingDefectError(msg)
        if isinstance(solvent_reference_structure, str):
            solvent_reference_structure = read_structure_from_file(
                    solvent_reference_structure)
        if not _structure_has_element(solvent_reference_structure,
                                      self.solvent_element):
            msg = 'Solvent structure must contain solvent element'
            raise MixingDefectSetError(msg)
        self._solvent_reference_structure = solvent_reference_structure

    @property
    def solute_elements(self):
        """List of atomic symbols of solute elements."""
        return self._solute_elements

    @solute_elements.setter
    def solute_elements(self, solute_elements):
        if self.solute_elements is not None:
            msg = ('Use the "add_solute_to_defects_set()" and/or '
                   '"remove_solute_from_defects_set()" functions to modify '
                   'the list of solute elements')
            raise MixingDefectSetError(msg)

        if solute_elements is None:
            self._solute_elements = []
            return

        if isinstance(solute_elements, six.string_types):
            elements_set = set([e.strip() for e in solute_elements.split(',')])
        else:
            elements_set = set(solute_elements)

        if self.solvent_element in elements_set:
            elements_set.remove(self.solvent_element)

        for element in elements_set:
            _validate_input_element(element)

        self._solute_elements = sorted(list(elements_set))

    @property
    def solute_reference_structures(self):
        """Dictionary of solutes and corresponding reference structures."""
        return self._solute_reference_structures

    @solute_reference_structures.setter
    def solute_reference_structures(self, solute_reference_structures):
        if self.solute_reference_structures is not None:
            msg = ('Use the "add_solute_to_defects_set()" and/or '
                   '"remove_solute_from_defects_set()" functions to modify '
                   'the set of solute reference structures')
            raise MixingDefectSetError(msg)

        self._solute_reference_structures = dict([(e, None) for e in
                                                  self.solute_elements])

        if solute_reference_structures is None:
            return

        try:
            for element, structure in solute_reference_structures.items():
                _validate_input_element(element)
                if isinstance(structure, str):
                    structure = read_structure_from_file(structure)
                if not _structure_has_element(structure, element):
                    msg = ('Solute reference structure does not contain '
                           'solute element')
                    raise MixingDefectSetError(msg)
                self._solute_reference_structures.update({element: structure})
        except AttributeError:
            msg = 'Input "solute_reference_structures" should be a dictionary'
            raise MixingDefectSetError(msg)

    @property
    def min_image_dist(self):
        """Minimum distance between periodic defect images in Angstrom."""
        return self._min_image_dist

    @min_image_dist.setter
    def min_image_dist(self, min_image_dist):
        if self.min_image_dist is not None:
            msg = 'Cannot set minimum image distance after initial setup'
            raise MixingDefectSetError(msg)

        self._min_image_dist = 12.0
        if min_image_dist is None:
            return
        try:
            self._min_image_dist = float(min_image_dist)
        except ValueError:
            print('Invalid minimum image_distance: {}.'.format(min_image_dist))
            print('Using default value of 12 Angstrom.')

    @property
    def supercell_for_mixing(self):
        """Solvent supercell to use for creating a dilute mixing defect."""
        return self._supercell_for_mixing

    @supercell_for_mixing.setter
    def supercell_for_mixing(self, supercell_for_mixing):
        if supercell_for_mixing is None:
            self._supercell_for_mixing = supercell.get_supercell_for_mixing(
                    structure=self.solvent_reference_structure,
                    min_image_dist=self.min_image_dist,
            )
            return
        elif isinstance(supercell_for_mixing, str):
            supercell_for_mixing = read_structure_from_file(
                    supercell_for_mixing)
        if not _structure_has_element(supercell_for_mixing,
                                      self.solvent_element):
            msg = 'Defect supercell does not contain solvent element'
            raise MixingDefectError(msg)
        self._supercell_for_mixing = supercell_for_mixing

    @property
    def mixing_defects(self):
        """Dictionary of solute elements and the corresponding
        :class:`htdefects.MixingDefect` objects."""
        return self._mixing_defects

    def _set_mixing_defects(self):
        self._mixing_defects = {}
        for element in self.solute_elements:
            solute_str = self.solute_reference_structures.get(element, None)
            self._mixing_defects[element] = MixingDefect(
                solvent_element=self.solvent_element,
                solvent_reference_structure=self.solvent_reference_structure,
                solute_element=element,
                solute_reference_structure=solute_str,
                min_image_dist=self.min_image_dist,
                supercell_for_mixing=self.supercell_for_mixing,
            )

    def add_solute_to_defects_set(self, solute_element,
                                  solute_reference_structure=None):
        """Adds a solute to the list of defects if not in it already.

        Parameters
        ----------

        solute_element: str
            Atomic symbol of the solute element to be added.

        solute_reference_structure: :class:`dftinpgen.atoms.Structure`
            Reference crystal structure of the solute.

        Raises
        ------

        MixingDefectSetError
            If solute element already present in the list of solutes.

        """
        if solute_element in self.mixing_defects:
            msg = ('Solute "{}" already present in the defects set. Remove it'
                   ' using the "remove_solute_from_defects_set()" function'
                   ' first'.format(solute_element))
            raise MixingDefectSetError(msg)

        if solute_element == self.solvent_element:
            msg = 'Solute specified is same as solvent'
            raise MixingDefectSetError(msg)

        self._mixing_defects[solute_element] = MixingDefect(
            solvent_element=self.solvent_element,
            solvent_reference_structure=self.solvent_reference_structure,
            solute_element=solute_element,
            solute_reference_structure=solute_reference_structure,
            min_image_dist=self.min_image_dist,
            supercell_for_mixing=self.supercell_for_mixing
        )

        self._solute_reference_structures.update({
            solute_element: solute_reference_structure
        })
        self._solute_elements = sorted(self._mixing_defects.keys())

    def remove_solute_from_defects_set(self, solute_element):
        """Removes a solute from the set of mixing defects, if present.

        Parameters
        ----------

        solute_element: str
            Atomic symbol of the solute to be removed.

        Raises
        ------

        MixingDefectSetError
            If solute to be removed is not in the list of solutes.

        """
        if solute_element not in self._mixing_defects:
            msg = 'Solute "{}" is not in the defects set to be removed'.format(
                solute_element)
            raise MixingDefectSetError(msg)

        self._mixing_defects.pop(solute_element)
        self._solute_reference_structures.pop(solute_element)
        self._solute_elements = sorted(self._mixing_defects.keys())
