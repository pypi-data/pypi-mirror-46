# -*- coding: utf-8 -*-

"""Unit tests for dilute mixing defect calculations."""

import os
import shutil
import unittest

from dftinpgen.calculation import DftCalc

from htdefects.mixing.calculation import MixingCalculationSet as MCSet
from htdefects.mixing.calculation import MixingCalculationError as MCError


def _get_pseudo_dir():
    pseudo_dir = os.path.expanduser("~/pseudo")
    if os.path.isdir(pseudo_dir):
        pseudo_dir_found = True
    else:
        pseudo_dir_found = False
        # TODO: an organic way of handling user input pseudo dir
        # (@hegdevinayi@gmail.com)
        """
        # get the pseudo directory
        message = ('Enter the (absolute) path to the pseudos directory:\n'
                   '(If not found, some tests will be skipped)')
        pseudo_dir = input(message)
        pseudo_dir = os.path.expanduser(pseudo_dir.strip())
        # look for the specified directory
        if os.path.isdir(pseudo_dir):
            pseudo_dir_found = True
        else:
            print('Pseudopotentials directory not found. The corresponding'
                  ' tests will be skipped.')
        """
    return pseudo_dir, pseudo_dir_found


class TestMixingCalculationSet(unittest.TestCase):
    """Unit tests for `htdefects.mixing.MixingCalculationSet`."""

    pseudo_dir, pseudo_dir_found = _get_pseudo_dir()

    def setUp(self):
        """Set up sample data to help with testing."""
        self.data_dir = 'sample_vasp_data'
        self.al_fcc = os.path.join(self.data_dir, 'Al_fcc.vasp')
        self.co_fcc = os.path.join(self.data_dir, 'Co_fcc.vasp')
        self.ti_hcp = os.path.join(self.data_dir, 'Ti_hcp.vasp')
        self.si_dia = os.path.join(self.data_dir, 'Si_diamond.vasp')
        self.w_bcc = os.path.join(self.data_dir, 'W_bcc.vasp')
        self.al_fcc_super = os.path.join(self.data_dir, 'Al_fcc_super_6.vasp')
        self.co_fcc_super_98 = os.path.join(self.data_dir,
                                            'Co_fcc_super_98_atoms.vasp')

    def _get_co_fcc_mcs(self):
        self.setUp()
        co_fcc_mcs = MCSet(solvent_element='Co',
                           solvent_reference_structure_file=self.co_fcc,
                           solute_elements='Al, Si, Ti, W',
                           solute_reference_structure_files={
                               'Si': self.si_dia,
                               'Ti': self.ti_hcp,
                               'W': self.w_bcc
                           },
                           supercell_for_mixing=self.co_fcc_super_98,
                           min_image_dist=10)
        return co_fcc_mcs

    def test_solvent_structure_file(self):
        # missing structure file
        with self.assertRaises(MCError):
            mc = MCSet(solvent_element='Al',
                       solvent_reference_structure_file='Al_fcc',
                       supercell_for_mixing=self.al_fcc_super)
            print(mc)

        # all OK
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super)
        self.assertEqual(mc.solvent_reference_structure_file, self.al_fcc)

    def test_solute_structure_files(self):
        # empty dictionary
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super)
        self.assertDictEqual(mc.solute_reference_structure_files, {})

        # solute structure file not found
        with self.assertRaises(MCError):
            mc = MCSet(solvent_element='Al',
                       solvent_reference_structure_file=self.al_fcc,
                       solute_reference_structure_files={'Co': 'Co_fcc'},
                       supercell_for_mixing=self.al_fcc_super)
            print(mc)

        # all OK
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   solute_reference_structure_files={'Ti': self.ti_hcp},
                   supercell_for_mixing=self.al_fcc_super)
        self.assertDictEqual(mc.solute_reference_structure_files,
                             {'Ti': self.ti_hcp})

    def test_calc_dir(self):
        # calc dir fallback
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super)
        calc_dir = os.path.join('sample_vasp_data', 'Al_mixing_defects')
        self.assertEqual(mc.calc_dir, calc_dir)

        # calc dir specified
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super,
                   calc_dir='Nondefault_loc')
        self.assertEqual(mc.calc_dir, 'Nondefault_loc')

    def test_pseudo_dir(self):
        # pseudo dir fallback
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super)
        default_dir = os.path.expanduser('~/pseudo')
        self.assertEqual(mc.pseudo_dir, default_dir)

    def test_do_relaxation(self):
        # default
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super)
        self.assertTrue(mc.do_relaxation)

        # string
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super,
                   do_relaxation=' FALSE ')
        self.assertFalse(mc.do_relaxation)

        # boolean
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super,
                   do_relaxation=False)
        self.assertFalse(mc.do_relaxation)

    def test_dft_code(self):
        # default
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super)
        self.assertEqual(mc.dft_code, 'vasp')

        # not supported raises error
        with self.assertRaises(MCError):
            mc = MCSet(solvent_element='Al',
                       solvent_reference_structure_file=self.al_fcc,
                       supercell_for_mixing=self.al_fcc_super,
                       dft_code='ABINIT')
            print(mc)

        # pwscf
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super,
                   dft_code=' pwSCF ')
        self.assertEqual(mc.dft_code, 'pwscf')

    def test_dft_params(self):
        # VASP case
        # default
        mc = MCSet(dft_code='vasp', solvent_element='Al',
                   supercell_for_mixing=self.al_fcc_super,
                   solvent_reference_structure_file=self.al_fcc)
        self.assertEqual(mc.dft_params, 'default')

        # dictionary of tags and values
        mc = MCSet(dft_code='vasp', solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super,
                   dft_params={'ispin': 1, 'ldau': True})
        # because, by default, calculation.py adds (at least) the tag encut
        # and its value to the parameters dictionary
        compare_params = dict([(k, mc.dft_params[k]) for k
                               in ['ispin', 'ldau']])
        self.assertDictEqual(compare_params, {'ispin': 1, 'ldau': True})

        # PWSCF case
        # default
        mc = MCSet(dft_code='pwscf', solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super)
        self.assertEqual(mc.dft_params, 'default')

        # dictionary of tags and values
        mc = MCSet(dft_code='pwscf', solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super,
                   dft_params={'ispin': 1, 'ldau': True})
        # because, by default, calculation.py adds (at least) the tag encut
        # and its value to the parameters dictionary
        compare_params = dict([(k, mc.dft_params[k]) for k
                               in ['ispin', 'ldau']])
        self.assertDictEqual(compare_params, {'ispin': 1, 'ldau': True})

    def test_from_scratch(self):
        # default
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super)
        self.assertFalse(mc.from_scratch)

        # string
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super,
                   from_scratch=' FALSE ')
        self.assertFalse(mc.from_scratch)

        # boolean
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super,
                   from_scratch=True)
        self.assertTrue(mc.from_scratch)

    @unittest.skipIf(not pseudo_dir_found, '"pseudo_dir" not found')
    def test_setup_dft_calcs(self):
        # VASP case
        mc = MCSet(dft_code='vasp', solvent_element='Al',
                   pseudo_dir=self.pseudo_dir,
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super)

        # without relaxation
        dft_calcs = mc._setup_dft_calcs(mc.solvent_reference_structure,
                                        mc.calc_dir, do_relaxation=False)

        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['static'].directory))
        # and the "relax" calculation is *not* created
        self.assertIsNone(dft_calcs['relax'])
        # are all the input files written?
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['static'].directory, 'POSCAR')))
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['static'].directory, 'POTCAR')))
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['static'].directory, 'INCAR')))
        shutil.rmtree(mc.calc_dir)

        # with relaxation
        dft_calcs = mc._setup_dft_calcs(mc.solvent_reference_structure,
                                        mc.calc_dir,
                                        do_relaxation=True)
        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['relax'].directory))
        # are all the input files written?
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['relax'].directory, 'POSCAR')))
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['relax'].directory, 'POTCAR')))
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['relax'].directory, 'INCAR')))
        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['static'].directory))
        # are all the input files written?
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['static'].directory, 'POSCAR')))
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['static'].directory, 'POTCAR')))
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['static'].directory, 'INCAR')))
        shutil.rmtree(mc.calc_dir)

        # PWSCF case
        mc = MCSet(dft_code='pwscf', solvent_element='Al',
                   pseudo_dir=self.pseudo_dir,
                   solvent_reference_structure_file=self.al_fcc,
                   supercell_for_mixing=self.al_fcc_super)
        # without relaxation
        dft_calcs = mc._setup_dft_calcs(mc.solvent_reference_structure,
                                        mc.calc_dir,
                                        do_relaxation=False)

        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['static'].directory))
        # and the "relax" calculation is *not* created
        self.assertIsNone(dft_calcs['relax'])
        # are all the input files written?
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['static'].directory,
                         'Al.pbe-n-kjpaw_psl.1.0.0.UPF')))
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['static'].directory, 'pw.in')))
        shutil.rmtree(mc.calc_dir)

        # with relaxation
        dft_calcs = mc._setup_dft_calcs(mc.solvent_reference_structure,
                                        mc.calc_dir,
                                        do_relaxation=True)
        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['relax'].directory))
        # are all the input files written?
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['relax'].directory,
                         'Al.pbe-n-kjpaw_psl.1.0.0.UPF')))
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['relax'].directory, 'pw.in')))
        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['static'].directory))
        # are all the input files written?
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['static'].directory,
                         'Al.pbe-n-kjpaw_psl.1.0.0.UPF')))
        self.assertTrue(os.path.isfile(
            os.path.join(dft_calcs['static'].directory, 'pw.in')))
        shutil.rmtree(mc.calc_dir)

    @unittest.skipIf(not pseudo_dir_found, '"pseudo_dir" not found')
    def test_setup_mixing_calculations(self):
        mc = MCSet(solvent_element='Al',
                   solvent_reference_structure_file=self.al_fcc,
                   solute_elements=['Co', 'Ti'],
                   solute_reference_structure_files={'Ti': self.ti_hcp},
                   supercell_for_mixing=self.al_fcc_super,
                   pseudo_dir=self.pseudo_dir)
        mc.setup_mixing_calculations()
        # is the directory structure correct?
        base_dir = os.path.join('sample_vasp_data', 'Al_mixing_defects')
        # solvent
        self.assertTrue(os.path.isdir(os.path.join(base_dir, 'solvent')))
        # Co
        self.assertTrue(os.path.isdir(os.path.join(base_dir, 'solutes', 'Co')))
        self.assertTrue(os.path.isdir(
            os.path.join(base_dir, 'solutes', 'Co', 'solvent_structure')))
        self.assertFalse(os.path.isdir(
            os.path.join(base_dir, 'solutes', 'Co', 'reference_structure')))
        self.assertTrue(os.path.isdir(
            os.path.join(base_dir, 'solutes', 'Co', 'defect')))
        # Ti
        self.assertTrue(os.path.isdir(
            os.path.join(base_dir, 'solutes', 'Ti')))
        self.assertTrue(os.path.isdir(
            os.path.join(base_dir, 'solutes', 'Ti', 'solvent_structure')))
        self.assertTrue(os.path.isdir(
            os.path.join(base_dir, 'solutes', 'Ti', 'reference_structure')))
        self.assertTrue(os.path.isdir(
            os.path.join(base_dir, 'solutes', 'Ti', 'defect')))
        shutil.rmtree(mc.calc_dir)

        # the mixing calculations dictionary
        # accessed via the "mixing_calculations" property
        mmc = mc.mixing_calculations
        self.assertListEqual(sorted(mmc.keys()), ['solutes', 'solvent'])
        self.assertListEqual(sorted(mmc['solvent'].keys()),
                             ['relax', 'static'])
        self.assertListEqual(sorted(mmc['solutes'].keys()),
                             ['Co', 'Ti'])
        self.assertListEqual(sorted(mmc['solutes']['Co'].keys()),
                             ['defect', 'reference_structure',
                              'solvent_structure'])
        self.assertListEqual(sorted(mmc['solutes']['Ti'].keys()),
                             ['defect', 'reference_structure',
                              'solvent_structure'])
        self.assertEqual(mmc['solutes']['Co']['reference_structure'], None)
        self.assertListEqual(sorted(mmc['solutes']['Co'][
                                        'solvent_structure'].keys()),
                             ['relax', 'static'])
        self.assertListEqual(sorted(mmc['solutes']['Co']['defect'].keys()),
                             ['relax', 'static'])
        self.assertListEqual(sorted(mmc['solutes']['Ti'][
                                        'reference_structure'].keys()),
                             ['relax', 'static'])
        self.assertListEqual(sorted(mmc['solutes']['Ti'][
                                        'solvent_structure'].keys()),
                             ['relax', 'static'])
        self.assertListEqual(sorted(mmc['solutes']['Ti']['defect'].keys()),
                             ['relax', 'static'])
        self.assertTrue(isinstance(mmc['solutes']['Ti']['defect']['relax'],
                                   DftCalc))

    @unittest.skipIf(not pseudo_dir_found, '"pseudo_dir" not found')
    def test_mixing_calculations_data_property(self):
        co_fcc_mcs = self._get_co_fcc_mcs()
        co_fcc_mcs.setup_mixing_calculations()
        mcd = co_fcc_mcs.mixing_calculations_data
        self.assertEqual(mcd['solvent']['number_of_atoms'].scalars[
                                 0].value, 1)
        self.assertIsNone(mcd['solutes']['Al']['reference_structure'])
        self.assertEqual(mcd['solutes']['Si']['defect'][
                             'number_of_atoms'].scalars[0].value, 98)

    @unittest.skipIf(not pseudo_dir_found, '"pseudo_dir" not found')
    def test_calculate_mixing_energy(self):
        co_fcc_mcs = self._get_co_fcc_mcs()
        co_fcc_mcs.setup_mixing_calculations()
        # Al has no reference structure
        self.assertIsNone(co_fcc_mcs.calculate_mixing_energy(
                'Al', reference='reference_structure'))
        # Al mixing energy
        e_mix_al = co_fcc_mcs.calculate_mixing_energy('Al')
        self.assertAlmostEqual(e_mix_al.scalars[0].value, -0.88740334)
        # Si mixing energy w.r.t. to the solvent crystal structure
        e_mix_si_ss = co_fcc_mcs.calculate_mixing_energy('Si')
        self.assertAlmostEqual(e_mix_si_ss.scalars[0].value, -1.58521121)
        # Si mixing energy w.r.t. to the its ground state crystal structure
        e_mix_si_rs = co_fcc_mcs.calculate_mixing_energy(
                'Si', reference='reference_structure')
        self.assertAlmostEqual(e_mix_si_rs.scalars[0].value, -1.04898232)

    @unittest.skipIf(not pseudo_dir_found, '"pseudo_dir" not found')
    def test_calculate_mixing_volume(self):
        co_fcc_mcs = self._get_co_fcc_mcs()
        co_fcc_mcs.setup_mixing_calculations()
        # Al mixing volume
        v_mix = co_fcc_mcs.calculate_mixing_volume('Al')
        self.assertAlmostEqual(v_mix.scalars[0].value, 3.66)
        # Si mixing volume
        v_mix = co_fcc_mcs.calculate_mixing_volume('Si')
        self.assertAlmostEqual(v_mix.scalars[0].value, 1.10)
        # Ti mixing volume
        v_mix = co_fcc_mcs.calculate_mixing_volume('Ti')
        self.assertAlmostEqual(v_mix.scalars[0].value, 4.51)
        # W mixing volume
        v_mix = co_fcc_mcs.calculate_mixing_volume('W')
        self.assertAlmostEqual(v_mix.scalars[0].value, 5.37)

    @unittest.skipIf(not pseudo_dir_found, '"pseudo_dir" not found')
    def test_calculate_solute_mixing_properties(self):
        co_fcc_mcs = self._get_co_fcc_mcs()
        co_fcc_mcs.setup_mixing_calculations()
        # Al
        al_props = co_fcc_mcs.calculate_solute_mixing_properties('Al')
        self.assertAlmostEqual(al_props['mixing_energy_ss'].scalars[0].value,
                               -0.88740334)
        self.assertIsNone(al_props['mixing_energy_rs'])
        self.assertAlmostEqual(al_props['mixing_volume'].scalars[0].value,
                               3.66)
        # Si
        si_props = co_fcc_mcs.calculate_solute_mixing_properties('Si')
        self.assertAlmostEqual(si_props['mixing_energy_ss'].scalars[0].value,
                               -1.58521121)
        self.assertAlmostEqual(si_props['mixing_energy_rs'].scalars[0].value,
                               -1.04898232)
        self.assertAlmostEqual(si_props['mixing_volume'].scalars[0].value,
                               1.10)

    @unittest.skipIf(not pseudo_dir_found, '"pseudo_dir" not found')
    def test_mixing_properties_property(self):
        co_fcc_mcs = self._get_co_fcc_mcs()
        co_fcc_mcs.setup_mixing_calculations()
        mp = co_fcc_mcs.mixing_properties
        # Set of solutes
        self.assertSetEqual(set(mp.keys()), {'Al', 'Si', 'Ti', 'W'})
        # Al mixing properties
        self.assertAlmostEqual(mp['Al']['mixing_energy_ss'].scalars[0].value,
                               -0.88740334)
        self.assertIsNone(mp['Al']['mixing_energy_rs'])
        self.assertAlmostEqual(mp['Al']['mixing_volume'].scalars[0].value,
                               3.66)


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)
