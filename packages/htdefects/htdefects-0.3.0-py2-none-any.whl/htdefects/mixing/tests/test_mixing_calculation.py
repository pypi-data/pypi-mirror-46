import unittest
import os
import sys
import shutil
from htdefects.mixing.calculation import MixingCalculationSet
from htdefects.mixing.calculation import MixingCalculationError
import dftinpgen


def _get_pseudo_dir():
    # get the pseudo directory
    message = ('Enter the (absolute) path to the pseudos directory:\n'
               '(If not found, some tests will be skipped)'
               ' [default: "~/pseudos"] ')
    if sys.version_info < (3, 0):
        pseudo_dir = raw_input(message)
    else:
        pseudo_dir = input(message)
    # default to directory "pseudos" in the user's home
    if not pseudo_dir.strip():
        pseudo_dir = os.path.expanduser('~/pseudos')
    else:
        pseudo_dir = os.path.expanduser(pseudo_dir)
    # look for the specified directory
    pseudo_dir_not_found = False
    if not os.path.exists(pseudo_dir):
        pseudo_dir_not_found = True
        print('Pseudopotentials directory not found. The corresponding tests will be skipped.')
    return pseudo_dir, pseudo_dir_not_found


class TestDiluteMixingCalcSet(unittest.TestCase):
    """Class of unit tests for `citrine_defects.dilute_mixing_calculation.DiluteMixingCalcSet`."""

    _pseudo_dir, _pseudo_dir_not_found = _get_pseudo_dir()


    def test_solvent_structure_file(self):
        # missing structure file
        with self.assertRaises(MixingCalculationError):
            mc = MixingCalculationSet(solvent_element='Al',
                                      solvent_reference_structure_file='Al_fcc')

        # all OK
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp')
        self.assertEqual(mc.solvent_reference_structure_file, 'Al_fcc.vasp')


    def test_solute_structure_files(self):
        # empty dictionary
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp')
        self.assertDictEqual(mc.solute_reference_structure_files, {})

        # solute structure file not found
        with self.assertRaises(MixingCalculationError):
            mc = MixingCalculationSet(solvent_element='Al',
                                      solvent_reference_structure_file='Al_fcc.vasp',
                                      solute_reference_structure_files={'Co': 'Co_fcc'})

        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  solute_reference_structure_files={'Ti': 'Ti_hcp.vasp'})
        self.assertDictEqual(mc.solute_reference_structure_files, {'Ti': 'Ti_hcp.vasp'})


    def test_calc_dir(self):
        # calc dir fallback
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp')
        self.assertEqual(mc.calc_dir, 'Al_mixing_defects')

        # calc dir specified
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  calc_dir='Nondefault_loc')
        self.assertEqual(mc.calc_dir, 'Nondefault_loc')


    def test_pseudo_dir(self):
        # pseudo dir fallback
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp')
        default_dir = os.path.join(os.path.dirname(dftinpgen.__file__), 'pseudo')
        self.assertEqual(mc.pseudo_dir, default_dir)


    def test_do_relaxation(self):
        # default
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp')
        self.assertTrue(mc.do_relaxation)

        # string
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  do_relaxation=' FALSE ')
        self.assertFalse(mc.do_relaxation)

        # boolean
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  do_relaxation=False)
        self.assertFalse(mc.do_relaxation)


    def test_dft_code(self):
        # default
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp')
        self.assertEqual(mc.dft_code, 'vasp')

        # not supported raises error
        with self.assertRaises(MixingCalculationError):
            mc = MixingCalculationSet(solvent_element='Al',
                                      solvent_reference_structure_file='Al_fcc.vasp',
                                      dft_code='ABINIT')

        # pwscf
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  dft_code=' pwSCF ')
        self.assertEqual(mc.dft_code, 'pwscf')


    def test_dft_params(self):
        # VASP case
        # default
        mc = MixingCalculationSet(dft_code='vasp', solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp')
        self.assertEqual(mc.dft_params, 'default')

        # dictionary of tags and values
        mc = MixingCalculationSet(dft_code='vasp', solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  dft_params={'ispin': 1, 'ldau': True})
        # because, by default, calculation.py adds (at least) the tag encut and its value to the
        # parameters dictionary
        compare_params = dict([(k, mc.dft_params[k]) for k in ['ispin', 'ldau']])
        self.assertDictEqual(compare_params, {'ispin': 1, 'ldau': True})

        # PWSCF case
        # default
        mc = MixingCalculationSet(dft_code='pwscf', solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp')
        self.assertEqual(mc.dft_params, 'default')

        # dictionary of tags and values
        mc = MixingCalculationSet(dft_code='pwscf', solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  dft_params={'ispin': 1, 'ldau': True})
        # because, by default, calculation.py adds (at least) the tag encut and its value to the
        # parameters dictionary
        compare_params = dict([(k, mc.dft_params[k]) for k in ['ispin', 'ldau']])
        self.assertDictEqual(compare_params, {'ispin': 1, 'ldau': True})


    def test_from_scratch(self):
        # default
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp')
        self.assertTrue(mc.from_scratch)

        # string
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  from_scratch=' FALSE ')
        self.assertFalse(mc.from_scratch)

        # boolean
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  from_scratch=False)
        self.assertFalse(mc.from_scratch)


    @unittest.skipIf(_pseudo_dir_not_found, '"pseudo_dir" not found')
    def test_setup_dft_calcs(self):
        # VASP case
        mc = MixingCalculationSet(dft_code='vasp', solvent_element='Al',
                                  pseudo_dir=self._pseudo_dir,
                                  solvent_reference_structure_file='Al_fcc.vasp')
        ## without relaxation
        dft_calcs = mc._setup_dft_calcs(mc.solvent_reference_structure, mc.calc_dir,
                                        do_relaxation=False)

        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['static'].directory))
        # are all the input files written?
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['static'].directory, 'POSCAR')))
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['static'].directory, 'POTCAR')))
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['static'].directory, 'INCAR')))
        shutil.rmtree('Al_mixing_defects')

        ## with relaxation
        dft_calcs = mc._setup_dft_calcs(mc.solvent_reference_structure, mc.calc_dir,
                                        do_relaxation=True)
        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['relax'].directory))
        # are all the input files written?
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['relax'].directory, 'POSCAR')))
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['relax'].directory, 'POTCAR')))
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['relax'].directory, 'INCAR')))
        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['static'].directory))
        # are all the input files written?
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['static'].directory, 'POSCAR')))
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['static'].directory, 'POTCAR')))
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['static'].directory, 'INCAR')))
        shutil.rmtree('Al_mixing_defects')

        # PWSCF case
        mc = MixingCalculationSet(dft_code='pwscf', solvent_element='Al',
                                  pseudo_dir=self._pseudo_dir,
                                  solvent_reference_structure_file='Al_fcc.vasp')
        ## without relaxation
        dft_calcs = mc._setup_dft_calcs(mc.solvent_reference_structure, mc.calc_dir,
                                        do_relaxation=False)

        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['static'].directory))
        # are all the input files written?
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['static'].directory, 'Al.pbe-n-kjpaw_psl.1.0.0.UPF')))
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['static'].directory, 'pw.in')))
        shutil.rmtree('Al_mixing_defects')

        ## with relaxation
        dft_calcs = mc._setup_dft_calcs(mc.solvent_reference_structure, mc.calc_dir,
                                        do_relaxation=True)
        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['relax'].directory))
        # are all the input files written?
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['relax'].directory, 'Al.pbe-n-kjpaw_psl.1.0.0.UPF')))
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['relax'].directory, 'pw.in')))
        # is the directory created?
        self.assertTrue(os.path.isdir(dft_calcs['static'].directory))
        # are all the input files written?
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['static'].directory, 'Al.pbe-n-kjpaw_psl.1.0.0.UPF')))
        self.assertTrue(os.path.isfile(os.path.join(dft_calcs['static'].directory, 'pw.in')))
        shutil.rmtree('Al_mixing_defects')


    @unittest.skipIf(_pseudo_dir_not_found, '"pseudo_dir" not found')
    def test_setup_mixing_calculations(self):
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  solute_elements=['Co', 'Ti'],
                                  solute_reference_structure_files={'Ti': 'Ti_hcp.vasp'},
                                  pseudo_dir=self._pseudo_dir)
        mc.setup_mixing_calculations()
        # is the directory structure correct?
        # solvent
        self.assertTrue(os.path.isdir(os.path.join('Al_mixing_defects', 'solvent')))
        # Co
        self.assertTrue(os.path.isdir(os.path.join('Al_mixing_defects', 'solutes', 'Co')))
        self.assertTrue(os.path.isdir(os.path.join('Al_mixing_defects', 'solutes', 'Co', 'solvent_structure')))
        self.assertFalse(os.path.isdir(os.path.join('Al_mixing_defects', 'solutes', 'Co', 'reference_structure')))
        self.assertTrue(os.path.isdir(os.path.join('Al_mixing_defects', 'solutes', 'Co', 'defect')))
        # Ti
        self.assertTrue(os.path.isdir(os.path.join('Al_mixing_defects', 'solutes', 'Ti')))
        self.assertTrue(os.path.isdir(os.path.join('Al_mixing_defects', 'solutes', 'Ti', 'solvent_structure')))
        self.assertTrue(os.path.isdir(os.path.join('Al_mixing_defects', 'solutes', 'Ti', 'reference_structure')))
        self.assertTrue(os.path.isdir(os.path.join('Al_mixing_defects', 'solutes', 'Ti', 'defect')))

        # the mixing calculations dictionary
        self.assertListEqual(sorted(mc.mixing_calculations.keys()), ['solutes', 'solvent'])
        self.assertListEqual(sorted(mc.mixing_calculations['solvent'].keys()), ['relax', 'static'])
        self.assertListEqual(sorted(mc.mixing_calculations['solutes'].keys()), ['Co', 'Ti'])
        self.assertListEqual(sorted(mc.mixing_calculations['solutes']['Co'].keys()), ['defect', 'reference_structure', 'solvent_structure'])
        self.assertListEqual(sorted(mc.mixing_calculations['solutes']['Ti'].keys()), ['defect', 'reference_structure', 'solvent_structure'])
        self.assertEqual(mc.mixing_calculations['solutes']['Co']['reference_structure'], None)
        self.assertListEqual(sorted(mc.mixing_calculations['solutes']['Co']['solvent_structure'].keys()), ['relax', 'static'])
        self.assertListEqual(sorted(mc.mixing_calculations['solutes']['Co']['defect'].keys()), ['relax', 'static'])
        self.assertListEqual(sorted(mc.mixing_calculations['solutes']['Ti']['reference_structure'].keys()), ['relax', 'static'])
        self.assertListEqual(sorted(mc.mixing_calculations['solutes']['Ti']['solvent_structure'].keys()), ['relax', 'static'])
        self.assertListEqual(sorted(mc.mixing_calculations['solutes']['Ti']['defect'].keys()), ['relax', 'static'])
        self.assertTrue(isinstance(mc.mixing_calculations['solutes']['Ti']['defect']['relax'],
                                   dftinpgen.calculation.DftCalc))
        shutil.rmtree('Al_mixing_defects')


    def test_get_number_of_atoms(self):
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  solute_elements=['Co', 'Ti'],
                                  solute_reference_structure_files={'Ti': 'Ti_hcp.vasp'},
                                  calc_dir='Al_mixing_defects')
        self.assertEqual(mc._get_number_of_atoms(os.path.join('Al_mixing_defects', 'solvent',
                                                              'static')), 4)


    def test_get_total_energy_pa(self):
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  solute_elements=['Co', 'Ti'],
                                  solute_reference_structure_files={'Ti': 'Ti_hcp.vasp'},
                                  calc_dir='Al_mixing_defects')
        self.assertAlmostEqual(mc._get_total_energy_pa(os.path.join('Al_mixing_defects',
                                                                    'solvent', 'static')), -3.7422817525)


    def test_get_volume_pa(self):
        mc = MixingCalculationSet(solvent_element='Al',
                                  solvent_reference_structure_file='Al_fcc.vasp',
                                  solute_elements=['Co', 'Ti'],
                                  solute_reference_structure_files={'Ti': 'Ti_hcp.vasp'},
                                  calc_dir='Al_mixing_defects')
        self.assertTrue(abs(mc._get_volume_pa(os.path.join('Al_mixing_defects', 'solvent',
                                                           'static')) - 16.5) < 0.01)


    def test_parse_mixing_properties(self):
        mc = MixingCalculationSet(solvent_element='Co',
                                  solvent_reference_structure_file='Co_fcc.vasp',
                                  solute_elements=['Ag', 'Al', 'Nb', 'Ni', 'Ti', 'Zr'],
                                  solute_reference_structure_files={'Ti': 'Ti_hcp.vasp'},
                                  calc_dir='Co_mixing_defects_5',
                                  min_image_dist=5.)

        mc.parse_mixing_properties()

        import json
        with open('Co_mixing_properties.json', 'w') as fw:
            json.dump(mc.mixing_properties, fw, indent=2)

        print('Solute E_mix V_mix')
        for solute in mc.solute_elements:
            print('{:4s} {:0.3f} {:0.2f}'.format(solute,
                                                 mc.mixing_properties[solute]['mixing_energy_SS'],
                                                 mc.mixing_properties[solute]['mixing_volume']))



if __name__ == '__main__':

    unittest.main(verbosity=2)
