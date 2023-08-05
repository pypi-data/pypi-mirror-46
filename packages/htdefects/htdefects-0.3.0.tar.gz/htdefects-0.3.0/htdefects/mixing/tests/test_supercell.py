# -*- coding: utf-8 -*-

"""Unit tests for the supercell handler functions."""

import os
import unittest

from dftinpgen import atoms

from htdefects.mixing.supercell import get_supercell_for_mixing
from htdefects.mixing.supercell import supercell_by_translation
from htdefects.mixing.supercell import get_natoms_bounds_for_ase_supercell
from htdefects.mixing.supercell import calc_min_image_dist
from htdefects.mixing.supercell import supercell_from_ase


class TestSupercell(unittest.TestCase):
    data_dir = 'sample_vasp_data'
    al_fcc = atoms.Structure(os.path.join(data_dir, 'Al_fcc.vasp'))
    co_fcc = atoms.Structure(os.path.join(data_dir, 'Co_fcc.vasp'))
    ti_hcp = atoms.Structure(os.path.join(data_dir, 'Ti_hcp.vasp'))

    def test_get_supercell_for_mixing(self):
        supercell = get_supercell_for_mixing(self.al_fcc,
                                             min_image_dist=10)
        self.assertEqual(supercell.totalnatoms, 92)
        self.assertAlmostEqual(calc_min_image_dist(supercell), 12.38, places=2)

    def test_supercell_by_translation(self):
        supercell = supercell_by_translation(self.al_fcc,
                                             min_image_dist=10)
        self.assertEqual(supercell.totalnatoms, 108)
        self.assertAlmostEqual(calc_min_image_dist(supercell), 12.38, places=2)

    def test_get_natoms_bounds_for_ase_supercell(self):
        low, high = get_natoms_bounds_for_ase_supercell(self.co_fcc,
                                                        min_image_dist=6)
        self.assertEqual(low, 16)
        self.assertEqual(high, 160)

    def test_calc_min_image_dist(self):
        image_dist = calc_min_image_dist(self.ti_hcp)
        self.assertAlmostEqual(image_dist, 2.917369, places=6)

    def test_supercell_from_ase(self):
        supercell = supercell_from_ase(self.co_fcc,
                                       min_image_dist=6)
        self.assertEqual(supercell.totalnatoms, 28)
        self.assertAlmostEqual(calc_min_image_dist(supercell), 6.18, places=2)


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)
