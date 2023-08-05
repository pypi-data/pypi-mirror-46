# -*- coding: utf-8 -*-

"""Classes to manage DFT calculations of mixing defects."""

import os
import shutil
import six

import dftinpgen
from dftinpgen import calculation
from pypif.pif import Property, Scalar

from htdefects.mixing.defect import MixingDefectSet
from htdefects.mixing.parsers import parse_mixing_calculations_data


def _get_prop_val(ddict, key):
    if ddict is None or ddict.get(key, None) is None:
        return None
    return ddict.get(key).scalars[0].value


class MixingCalculationError(Exception):
    """Base class for errors associated with dilute mixing calculations."""
    pass


class MixingCalculationSet(MixingDefectSet):
    """Class to set up calculations for a set of dilute mixing defects."""

    def __init__(self, solvent_element=None,
                 solvent_reference_structure_file=None,
                 solute_elements=None, solute_reference_structure_files=None,
                 min_image_dist=None, supercell_for_mixing=None,
                 calc_dir=None, pseudo_dir=None, do_relaxation=None,
                 dft_code=None, dft_params=None, from_scratch=None,
                 **kwargs):
        """Constructor.

        Parameters
        ----------

        solvent_element: str
            Atomic symbol of the solvent element.

        solvent_reference_structure_file: str
            Location of the structure of the solvent in the VASP5 format.

        solute_elements: list(str)
            List of atomic symbols of solutes.

        solute_reference_structure_files: dict(str, str)
            Dictionary of solute elements and the path to the respective
            solute reference structure files in the VASP5 format.

        min_image_dist: float, optional
            Minimum distance between periodic images of a defect in a
            supercell, in Angstrom.

            Defaults to 12 Angstrom.

        supercell_for_mixing: :class:`dftinpgen.atoms.Structure` or str
            Supercell structure used for creating a dilute mixing defect.
            If input is a string, the full path to the structure file must
            be provided.

        calc_dir: str, optional
            Directory to perform all the defect calculations in.

            Defaults to a folder named "[solvent_element]_defects_set" at the
            location of the :attr:`self.solvent_reference_structure_file`.

        pseudo_dir: str, optional
            Location (path) of the pseudopotential files.

            Defaults to a folder "pseudo" in the current user's home directory.

        do_relaxation: bool, optional
            Should the structures be relaxed before a final total energy
            calculation? If True, separate folders are created for the
            relaxation and static runs for each defect.

            Defaults to True.

        dft_code: str, optional
            Name of the DFT package to use. Currently available options are
            VASP and PWscf.

            Defaults to VASP.

        dft_params: str or dict(str, int or float or str or bool), optional
            Dictionary of parameters for the DFT calculations and their
            corresponding values. If a string "default" is input instead,
            defaults as defined in the :mod:`dftinpgen` module are used.

            Defaults to "default".

        from_scratch: bool, optional
            Should the calculations be started from scratch? If true,
            the entire directory structure and input files will be deleted
            if present, and fresh calculations will be set up.

            Defaults to False.

        kwargs: dict
            Arbitrary keyword arguments.

        """

        self._solvent_reference_structure_file = None
        self.solvent_reference_structure_file = \
            solvent_reference_structure_file

        self._solute_reference_structure_files = None
        self.solute_reference_structure_files = \
            solute_reference_structure_files

        super(MixingCalculationSet, self).__init__(
            solvent_element=solvent_element,
            solvent_reference_structure=solvent_reference_structure_file,
            solute_elements=solute_elements,
            solute_reference_structures=solute_reference_structure_files,
            min_image_dist=min_image_dist,
            supercell_for_mixing=supercell_for_mixing,
            **kwargs)

        self._calc_dir = None
        self.calc_dir = calc_dir

        self._pseudo_dir = None
        self.pseudo_dir = pseudo_dir

        self._do_relaxation = None
        self.do_relaxation = do_relaxation

        self._dft_code = None
        self.dft_code = dft_code

        self._dft_params = None
        self.dft_params = dft_params

        self._from_scratch = None
        self.from_scratch = from_scratch

        self._mixing_calculations = {}
        self._mixing_calculations_data = {}
        self._mixing_properties = {}

    @property
    def solvent_reference_structure_file(self):
        """Location of the structure of the solvent, in the VASP5 format."""
        return self._solvent_reference_structure_file

    @solvent_reference_structure_file.setter
    def solvent_reference_structure_file(self,
                                         solvent_reference_structure_file):
        if not os.path.isfile(solvent_reference_structure_file):
            msg = 'Solvent structure {} not found'.format(
                    solvent_reference_structure_file)
            raise MixingCalculationError(msg)
        self._solvent_reference_structure_file = \
            solvent_reference_structure_file

    @property
    def solute_reference_structure_files(self):
        """Dictionary of the solute elements and the path to the
        corresponding structure files in the VASP5 format."""
        return self._solute_reference_structure_files

    @solute_reference_structure_files.setter
    def solute_reference_structure_files(self,
                                         solute_reference_structure_files):
        self._solute_reference_structure_files = {}
        if solute_reference_structure_files is None:
            return
        for elem, struct_file in solute_reference_structure_files.items():
            if not os.path.isfile(struct_file):
                msg = 'Solute structure file {} not found'.format(struct_file)
                raise MixingCalculationError(msg)
            self._solute_reference_structure_files.update({elem: struct_file})

    @property
    def calc_dir(self):
        """Location where the calculations need to be set up/performed."""
        return self._calc_dir

    @calc_dir.setter
    def calc_dir(self, calc_dir):
        if calc_dir is None:
            solvent_structure_file_dir = os.path.dirname(
                    self.solvent_reference_structure_file)
            calc_dir_name = '{}_mixing_defects'.format(self.solvent_element)
            self._calc_dir = os.path.join(solvent_structure_file_dir,
                                          calc_dir_name)
        else:
            self._calc_dir = calc_dir

    @property
    def pseudo_dir(self):
        """Location (system path) of the pseudopotential files."""
        return self._pseudo_dir

    @pseudo_dir.setter
    def pseudo_dir(self, pseudo_dir):
        if pseudo_dir is None:
            self._pseudo_dir = os.path.expanduser('~/pseudo')
        else:
            self._pseudo_dir = pseudo_dir

    @property
    def do_relaxation(self):
        """Should all structures be relaxed or not?"""
        return self._do_relaxation

    @do_relaxation.setter
    def do_relaxation(self, do_relaxation):
        self._do_relaxation = True
        if isinstance(do_relaxation, six.string_types):
            self._do_relaxation = do_relaxation.strip().lower()[0] == 't'
        elif isinstance(do_relaxation, bool):
            self._do_relaxation = do_relaxation

    @property
    def dft_code(self):
        """Name of the DFT package to use. Current options: VASP/PWscf."""
        return self._dft_code

    @dft_code.setter
    def dft_code(self, dft_code):
        if dft_code is None:
            self._dft_code = 'vasp'
            return
        if dft_code.strip().lower() not in calculation.supported_codes:
            msg = 'DFT code {} not supported. Choose one of {}'.format(
                    dft_code, '/'.join(calculation.supported_codes))
            raise MixingCalculationError(msg)
        self._dft_code = dft_code.strip().lower()

    @property
    def dft_params(self):
        """Dictionary with parameters and corresponding values to
        be used in the DFT calculations. Alternatively, string "default"
        refers to using default parameters from the :mod:`dftinpgen`
        module."""
        return self._dft_params

    @dft_params.setter
    def dft_params(self, dft_params):
        self._dft_params = 'default'
        if dft_params is not None:
            self._dft_params = dft_params

    @property
    def from_scratch(self):
        """Should previous set of calculations be deleted and new
        calculations be set up?"""
        return self._from_scratch

    @from_scratch.setter
    def from_scratch(self, from_scratch):
        self._from_scratch = False
        if isinstance(from_scratch, six.string_types):
            self._from_scratch = from_scratch.strip().lower()[0] == 't'
        elif isinstance(from_scratch, bool):
            self._from_scratch = from_scratch

    def setup_mixing_calculations(self):
        """Sets up all the relevant mixing calculations, and populates a
        dictionary with the directory structure and the respective
        :class:`dftinpgen.calculation.DftCalc` objects.

        Uses the following directory structure for all the calculations
        (creating directories when necessary/as specified) under the top
        directory called "[solvent]_mixing_defects":
        -> solvent -> relax, static
        -> solutes -> [element 1] -> reference_structure -> relax, static
                                     solvent_structure   -> relax, static
                                     defect              -> relax, static
                   -> [element 2] -> reference_structure -> relax, static
                                     solvent_structure   -> relax, static
                                     defect              -> relax, static
                   -> [element 3] -> ...
            ...
        The corresponding :class:`dftinpgen.calculation.DftCalc` objects
        are stored in a dictionary :attr:`self.mixing_calculations` with a
        nested structure that mimics the directory structure above.

        """
        # make defect set directory
        if self.from_scratch:
            if os.path.isdir(self.calc_dir):
                shutil.rmtree(self.calc_dir)

        if not os.path.isdir(self.calc_dir):
            os.mkdir(self.calc_dir)

        # solvent
        calc_dir = os.path.join(self.calc_dir, 'solvent')
        if not os.path.isdir(calc_dir):
            os.mkdir(calc_dir)
        dft_calcs = self._setup_dft_calcs(self.solvent_reference_structure,
                                          calc_dir,
                                          do_relaxation=self.do_relaxation)
        self._mixing_calculations['solvent'] = dft_calcs

        # all solutes
        self._mixing_calculations['solutes'] = {}
        ref_to_struct = {
            'defect': 'defect_structure',
            'solvent_structure': 'solute_in_solvent_structure',
            'reference_structure': 'solute_reference_structure'
        }
        for solute, defect in self.mixing_defects.items():
            self._mixing_calculations['solutes'][solute] = {}
            if not os.path.isdir(os.path.join(self.calc_dir, 'solutes',
                                              solute)):
                os.makedirs(os.path.join(self.calc_dir, 'solutes', solute))

            for ref, struct in ref_to_struct.items():
                calc_dir = os.path.join(self.calc_dir, 'solutes', solute, ref)
                self._mixing_calculations['solutes'][solute][ref] = \
                    self._setup_dft_calcs(getattr(defect, struct),
                                          calc_dir,
                                          do_relaxation=self.do_relaxation)

    def _setup_dft_calcs(self, structure, calc_dir, do_relaxation=True):
        """Sets up the DFT calculation(s) for the specified structure in
        the specified directory.

        Parameters
        ----------

        structure: :class:`dftinpgen.atoms.Structure`
            Input structure.

        calc_dir: str
            Path to the directory where calculations have to be set up.

        do_relaxation: bool, optional
            Should a relaxation calculation be performed.

            Defaults to True.

        Returns
        -------

        dict(str, :class:`dftinpgen.calculation.DftCalc`) or None
        Dictionary of job type ("relax"/"static") and the corresponding DFT
        calculations, or None if no structure is specified.

        """
        if structure is None:
            return None

        if not os.path.isdir(calc_dir):
            os.mkdir(calc_dir)

        job_types = ['relax', 'static']
        dft_calcs = dict([(jt, None) for jt in job_types])
        if not do_relaxation:
            job_types.remove('relax')

        for job_type in job_types:
            dft_calcs[job_type] = self._setup_dft_calc(structure,
                                                       calc_dir,
                                                       job_type=job_type)
        return dft_calcs

    def _setup_dft_calc(self, structure, calc_base_dir, job_type='static'):
        """Sets up a DFT calculation in the specified directory, for the
        specified structure and DFT calculation type.

        Parameters
        ----------

        structure: :class:`dftinpgen.atoms.Structure`
            Input structure.

        calc_base_dir: str
            Path to the directory where calculations have to be set up. A
            subdirectory named after the [job_type] will be created.

        job_type: str, optional
            The type of DFT calculation. Only "relax" and "static"
            currently implemented. "Static" is simply a total energy
            calculation without any structural relaxation.

            Defaults to "static".

        Returns
        -------

        :class:`dftinpgen.calculation.DftCalc`
            Object with info about the DFT calculation that was set up.

        """
        job_dir = os.path.join(calc_base_dir, job_type)

        if not os.path.isdir(job_dir):
            os.mkdir(job_dir)

        structure_file = os.path.join(job_dir, 'POSCAR')
        structure.pposcar(structure_file)

        dft_calc = calculation.DftCalc(job_dir,
                                       structure_file,
                                       self.pseudo_dir,
                                       params=self.dft_params,
                                       code=self.dft_code,
                                       jobtype=job_type)
        dft_calc.gen_input_files()

        return dft_calc

    @property
    def mixing_calculations(self):
        """Dictionary with the solvent/solute and all the corresponding DFT
        calculation objects or None.

        The structure of the dictionary mimics the directory structure:
        {
            "solvent": {
                "relax": :class:`dftinpgen.calculation.DftCalc`,
                "static": :class:`dftinpgen.calculation.DftCalc`
            },
            "solutes": {
                "[solute 1]": {
                    "reference_structure": {
                        "relax": :class:`dftinpgen.calculation.DftCalc`,
                        "static: :class:`dftinpgen.calculation.DftCalc`
                    },
                    "solvent_structure": {
                        ...
                    },
                    "defect": {
                        ...
                    }
                },
                "[solute 2]": {
                    ...
                    ...
                },
                ...
                ...
            }
        }

        """
        return self._mixing_calculations

    @mixing_calculations.setter
    def mixing_calculations(self, mc=None):
        self._mixing_calculations = mc

    def _parse_mixing_calculations_data(self):
        self._mixing_calculations_data = parse_mixing_calculations_data(
                self.mixing_calculations)

    @property
    def mixing_calculations_data(self):
        """Dictionary of properties relevant to mixing parsed directly from
        output files of DFT calculations.

        The nested structure of the dictionary mimics the default directory
        structure of the calculations (see :attr:`self.mixing_calculations`).
        """
        if not self._mixing_calculations_data:
            self._parse_mixing_calculations_data()
        return self._mixing_calculations_data

    @mixing_calculations_data.setter
    def mixing_calculations_data(self, mcd=None):
        self._mixing_calculations_data = mcd

    def calculate_mixing_energy(self, solute, reference='solvent_structure'):
        """Calculates energy of dilute mixing:

        E_mix(solute) = E_defect(N) - (N-1)*E_solvent - 1*E_solute

        Parameters
        ----------

        solute: str
            Atomic symbol of the solute element.

        reference: str, optional
            Which solute structure should be used as reference? Options are
            "solvent_structure" (true mixing energy, i.e., the solute and
            solvent are both in the crystal structure of the solvent),
            and "reference_structure" (the solute is in the specified
            crystal structure, which may not be the same as that of the
            solvent).

            Defaults to "solvent_structure".

        Returns
        -------

        :class:`pypif.pif.Property` or None
            Energy of dilute mixing if all required quantities are
            available, else None.

        """
        mcd = self.mixing_calculations_data
        n_atoms = _get_prop_val(mcd['solutes'][solute]['defect'],
                                'number_of_atoms')
        e_solvent = _get_prop_val(mcd['solvent'],
                                  'total_energy_per_atom')
        e_defect = _get_prop_val(mcd['solutes'][solute]['defect'],
                                 'total_energy_per_atom')
        e_solute = _get_prop_val(mcd['solutes'][solute][reference],
                                 'total_energy_per_atom')
        if any([p is None for p in [n_atoms, e_defect, e_solvent, e_solute]]):
            return None
        e_mix = n_atoms*e_defect - (n_atoms-1)*e_solvent - 1*e_solute
        return Property(name='Mixing energy ({})'.format(reference),
                        data_type='COMPUTATIONAL',
                        scalars=[Scalar(value=e_mix)],
                        units='eV/defect')

    def calculate_mixing_volume(self, solute):
        """Calculate the volume of dilute mixing:
        
        V_mix(solute) = V_defect(N) - V_solvent(N)
        
        Parameters
        ----------
        
        solute: str
            Atomic symbol of the solute element.

        Returns
        -------

        :class:`pypif.pif.Property` or None.
            Dilute mixing volume of the specified solute if all the required
            quantities are available, else None.

        """
        mcd = self.mixing_calculations_data
        n_atoms = _get_prop_val(mcd['solutes'][solute]['defect'],
                                'number_of_atoms')
        v_defect = _get_prop_val(mcd['solutes'][solute]['defect'],
                                 'volume_per_atom')
        v_solvent = _get_prop_val(mcd['solvent'],
                                  'volume_per_atom')
        if any([p is None for p in [n_atoms, v_defect, v_solvent]]):
            return None
        v_mix = n_atoms*v_defect - n_atoms*v_solvent
        return Property(name='Mixing volume',
                        data_type='COMPUTATIONAL',
                        scalars=[Scalar(value=v_mix)],
                        units='Angstrom^3/defect')

    def calculate_solute_mixing_properties(self, solute):
        """Calculates the dilute mixing energy and dilute mixing volume for
        the specified solute.

        Parameters
        ----------

        solute: str
            Atomic symbol of the solute element.

        Returns
        -------

        dict(str, :class:`pypif.pif.Property` or None)
            Dictionary of energy and volume of dilute mixing for the solute.

        """
        props = {
            'mixing_energy_ss': self.calculate_mixing_energy(
                    solute, reference='solvent_structure'),
            'mixing_energy_rs': self.calculate_mixing_energy(
                    solute, reference='reference_structure'),
            'mixing_volume': self.calculate_mixing_volume(solute)
        }
        return props

    def calculate_mixing_properties(self):
        """Calculate dilute mixing energy and volume for all solutes."""
        self._parse_mixing_calculations_data()
        for solute in self.solute_elements:
            self._mixing_properties[solute] = \
                self.calculate_solute_mixing_properties(solute)

    @property
    def mixing_properties(self):
        """Dictionary of dilute mixing energy and volumes of all solutes."""
        if not self._mixing_properties:
            self.calculate_mixing_properties()
        return self._mixing_properties
