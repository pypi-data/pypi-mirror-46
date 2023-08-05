# -*- coding: utf-8 -*-

"""Unit tests for DFT calculation parser functions."""

import os
import unittest

from htdefects.mixing.parsers import *
from htdefects.mixing.calculation import MixingCalculationSet


class TestParsers(unittest.TestCase):
    """Unit tests for :class:`htdefects.mixing.parsers`."""

    base_calc_dir = os.path.join('sample_vasp_data', 'Co_mixing_defects')

    def test_get_number_of_atoms(self):
        calc_dir = os.path.join(self.base_calc_dir, 'solvent', 'static')
        natoms = get_number_of_atoms(calc_dir)
        self.assertEqual(natoms.scalars[0].value, 1)

    def test_get_total_energy(self):
        calc_dir = os.path.join(self.base_calc_dir, 'solutes',
                                'Si', 'reference_structure', 'static')
        toten = get_total_energy(calc_dir)
        self.assertAlmostEqual(toten.scalars[0].value, -10.8498326)

    def test_get_total_energy_pa(self):
        calc_dir = os.path.join(self.base_calc_dir, 'solutes',
                                'Si', 'reference_structure', 'static')
        toten = get_total_energy(calc_dir)
        natoms = get_number_of_atoms(calc_dir)
        # all OK
        toten_pa = get_total_energy_pa(toten, natoms)
        self.assertAlmostEqual(toten_pa.scalars[0].value, -5.4249163)
        # one of total energy, natoms not available
        self.assertIsNone(get_total_energy_pa(toten, None))
        self.assertIsNone(get_total_energy_pa(None, natoms))

    def test_get_volume(self):
        calc_dir = os.path.join(self.base_calc_dir, 'solutes',
                                'Si', 'reference_structure', 'static')
        volume = get_volume(calc_dir)
        self.assertAlmostEqual(volume.scalars[0].value, 40.83)

    def test_get_volume_pa(self):
        calc_dir = os.path.join(self.base_calc_dir, 'solutes',
                                'Si', 'reference_structure', 'static')
        volume = get_volume(calc_dir)
        natoms = get_number_of_atoms(calc_dir)
        # all OK
        volume_pa = get_total_energy_pa(volume, natoms)
        self.assertAlmostEqual(volume_pa.scalars[0].value, 20.415)
        # one of total energy, natoms not available
        self.assertIsNone(get_total_energy_pa(volume, None))
        self.assertIsNone(get_total_energy_pa(None, natoms))

    def test_get_ntv_data(self):
        calc_dir = os.path.join(self.base_calc_dir, 'solutes',
                                'Si', 'reference_structure', 'static')
        props = get_ntv_data(calc_dir)
        self.assertEqual(props['number_of_atoms'].scalars[0].value, 2)
        self.assertAlmostEqual(props['total_energy_per_atom'].scalars[0].value,
                               -5.4249163)
        self.assertEqual(props['volume_per_atom'].scalars[0].value, 20.415)

    @unittest.skip('TODO: unskip after faster supercell finding algo')
    def test_parse_mixing_calculations_data(self):
        co_fcc = os.path.join('sample_vasp_data', 'Co_fcc.vasp')
        mc = MixingCalculationSet(solvent_element='Co',
                                  solvent_reference_structure_file=co_fcc,
                                  solute_elements=['Al', 'Si', 'Ti', 'W'],
                                  min_image_dist=8)
        props = parse_mixing_calculations_data(mc.mixing_calculations)
        print(props)

    def test_parse_calculations_from_tree(self):
        props = parse_calculations_from_tree(self.base_calc_dir)
        self.assertSetEqual(set(props['solutes'].keys()),
                            {'Al', 'Si', 'Ti', 'W'})
        # Ti hcp reference structure
        ti_ref = props['solutes']['Ti']['reference_structure']
        self.assertEqual(ti_ref['number_of_atoms'].scalars[0].value, 2)
        self.assertAlmostEqual(ti_ref['total_energy_per_atom'].scalars[
                                   0].value, -7.82963432)
        self.assertAlmostEqual(ti_ref['volume_per_atom'].scalars[0].value,
                               17.215)
        # Al has no solute reference structure (it is already fcc)
        self.assertIsNone(props['solutes']['Al']['reference_structure'])
        # Al dilute mixing defect structure
        al_defect = props['solutes']['Al']['defect']
        self.assertEqual(al_defect['number_of_atoms'].scalars[0].value, 98)
        self.assertAlmostEqual(al_defect['total_energy_per_atom'].scalars[
                                   0].value, -6.99482732)
        self.assertAlmostEqual(al_defect['volume_per_atom'].scalars[0].value,
                               10.8673469)


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)
