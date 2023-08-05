# -*- coding: utf-8 -*-

"""Unit tests for dilute mixing defect representation models."""

import os
import unittest

from dftinpgen import atoms

from htdefects.mixing.defect import MixingDefect, MixingDefectError
from htdefects.mixing.defect import MixingDefectSet, MixingDefectSetError


class TestMixingDefect(unittest.TestCase):
    """Unit tests for :class:`htdefects.mixing.MixingDefect`."""

    data_dir = 'sample_vasp_data'
    al_fcc = atoms.Structure(os.path.join(data_dir, 'Al_fcc.vasp'))
    co_fcc = atoms.Structure(os.path.join(data_dir, 'Co_fcc.vasp'))
    ti_hcp = atoms.Structure(os.path.join(data_dir, 'Ti_hcp.vasp'))
    al_fcc_super = atoms.Structure(os.path.join(data_dir,
                                                'Al_fcc_super_6.vasp'))
    ti_hcp_super = atoms.Structure(os.path.join(data_dir,
                                                'Ti_hcp_super_10.vasp'))

    def test_solvent_solute_elements(self):
        # solvent and solute elements
        md = MixingDefect(solvent_element='Al',
                          solvent_reference_structure=self.al_fcc,
                          solute_element='Ca',
                          min_image_dist=6.,
                          supercell_for_mixing=self.al_fcc_super)
        self.assertEqual(md.solvent_element, 'Al')
        self.assertEqual(md.solute_element, 'Ca')

        # unsupported solvent element
        with self.assertRaises(MixingDefectError):
            md = MixingDefect(solvent_element='Al1',
                              solvent_reference_structure=self.al_fcc,
                              solute_element='Ca',
                              min_image_dist=6.)
            print(md)

        # unsupported solute element
        with self.assertRaises(MixingDefectError):
            md = MixingDefect(solvent_element='Al',
                              solvent_reference_structure=self.al_fcc,
                              solute_element='Ca1',
                              min_image_dist=6.)
            print(md)

    def test_solvent_solute_reference_structures(self):
        # solvent reference structure without solvent element fail
        with self.assertRaises(MixingDefectError):
            md = MixingDefect(solvent_element='Co',
                              solvent_reference_structure=self.al_fcc,
                              solute_element='Ca',
                              min_image_dist=8.)
            print(md)

        # solvent reference structure
        md = MixingDefect(solvent_element='Al',
                          solvent_reference_structure=self.al_fcc,
                          solute_element='Ca',
                          min_image_dist=6.,
                          supercell_for_mixing=self.al_fcc_super)
        self.assertAlmostEqual(md.solvent_reference_structure.cell[0][0],
                               4.1259673)

        # solute reference structure without solute element fail
        with self.assertRaises(MixingDefectError):
            md = MixingDefect(solvent_element='Al',
                              solvent_reference_structure=self.al_fcc,
                              solute_element='Ca',
                              solute_reference_structure=self.co_fcc)
            print(md)

        # solute reference structure
        md = MixingDefect(solvent_element='Al',
                          solvent_reference_structure=self.al_fcc,
                          solute_element='Co',
                          solute_reference_structure=self.co_fcc,
                          min_image_dist=6.,
                          supercell_for_mixing=self.al_fcc_super)
        self.assertAlmostEqual(md.solute_reference_structure.cell[0][0],
                               3.5688)

    def test_min_image_dist(self):
        md = MixingDefect(solvent_element='Al',
                          solvent_reference_structure=self.al_fcc,
                          solute_element='Co',
                          solute_reference_structure=self.co_fcc,
                          min_image_dist=6.,
                          supercell_for_mixing=self.al_fcc_super)
        self.assertAlmostEqual(md.min_image_dist, 6.)

        # min image distance fallback
        md = MixingDefect(solvent_element='Al',
                          solvent_reference_structure=self.al_fcc,
                          solute_element='Co',
                          solute_reference_structure=self.co_fcc,
                          supercell_for_mixing=self.al_fcc_super)
        self.assertAlmostEqual(md.min_image_dist, 12.)

        # parsing error
        with self.assertRaises(ValueError):
            md = MixingDefect(solvent_element='Al',
                              solvent_reference_structure=self.al_fcc,
                              solute_element='Co',
                              solute_reference_structure=self.co_fcc,
                              min_image_dist='fifteen',
                              supercell_for_mixing=self.al_fcc_super)
            print(md)

    def test_supercell_for_mixing(self):
        pass

    def test_solute_in_solvent_structure(self):
        md = MixingDefect(solvent_element='Ti',
                          solvent_reference_structure=self.ti_hcp,
                          solute_element='Co',
                          solute_reference_structure=self.co_fcc,
                          min_image_dist=10.,
                          supercell_for_mixing=self.ti_hcp_super)
        # title
        self.assertEqual(md.solute_in_solvent_structure.title, 'Ti2')
        # atom types
        self.assertListEqual(md.solute_in_solvent_structure.atomtypes, ['Co'])
        # scaled lattice vectors
        for lv, lv_ref in zip(md.solute_in_solvent_structure.cell[1],
                              [-1.2547253, 2.1732221, 0.]):
            self.assertAlmostEqual(lv, lv_ref)

    def test_defect_structure(self):
        md = MixingDefect(solvent_element='Al',
                          solvent_reference_structure=self.al_fcc,
                          solute_element='Co',
                          solute_reference_structure=self.co_fcc,
                          min_image_dist=6.,
                          supercell_for_mixing=self.al_fcc_super)
        # atom types
        self.assertListEqual(md.defect_structure.atomtypes, ['Al', 'Co'])
        # natoms
        self.assertListEqual(list(md.defect_structure.natoms), [27, 1])
        # title
        self.assertEqual(md.defect_structure.title, 'Al27Co1')


class TestMixingDefectSet(unittest.TestCase):
    """Unit tests for :class:`htdefects.mixing.MixingDefectSet`."""

    data_dir = 'sample_vasp_data'
    al_fcc = atoms.Structure(os.path.join(data_dir, 'Al_fcc.vasp'))
    co_fcc = atoms.Structure(os.path.join(data_dir, 'Co_fcc.vasp'))
    ti_hcp = atoms.Structure(os.path.join(data_dir, 'Ti_hcp.vasp'))
    al_fcc_super = atoms.Structure(os.path.join(data_dir,
                                                'Al_fcc_super_6.vasp'))

    def test_solvent_elements(self):
        # solvent element
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)
        self.assertEqual(md.solvent_element, 'Al')

        # unsupported solvent element
        with self.assertRaises(MixingDefectError):
            md = MixingDefectSet(solvent_element='Al1',
                                 solvent_reference_structure=self.al_fcc,
                                 min_image_dist=6.)
            print(md)

    def test_solvent_reference_structure(self):
        # solvent reference structure without solvent element fail
        with self.assertRaises(MixingDefectSetError):
            md = MixingDefectSet(solvent_element='Ca',
                                 solvent_reference_structure=self.al_fcc,
                                 min_image_dist=5.)
            print(md)

        # solvent reference structure
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)
        self.assertAlmostEqual(md.solvent_reference_structure.cell[0][0],
                               4.1259673)

    def test_solute_elements_set(self):
        # no solute elements specified
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)
        self.assertListEqual(md.solute_elements, [])

        # solute elements as comma-separated string
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             solute_elements=' Co, Ca, Co ,Mn',
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)
        self.assertListEqual(md.solute_elements, ['Ca', 'Co', 'Mn'])

        # solute elements as a list; auto-removal of solvent element
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             solute_elements=['Co', 'Al', 'Ca', 'Al', 'Mn'],
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)
        self.assertListEqual(md.solute_elements, ['Ca', 'Co', 'Mn'])

        # solute elements set disallow setter
        with self.assertRaises(MixingDefectSetError):
            md.solute_elements = ['Ca', 'Si']

    def test_solute_reference_structures_set(self):
        # no reference structures given
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             solute_elements=['Co', 'Ti'],
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)
        self.assertDictEqual(md.solute_reference_structures,
                             {'Co': None, 'Ti': None})

        # invalid elements, structures in the reference structures dictionary
        srs = {'Co1': self.co_fcc}
        with self.assertRaises(MixingDefectError):
            md = MixingDefectSet(solvent_element='Al',
                                 solvent_reference_structure=self.al_fcc,
                                 solute_elements=['Co'],
                                 solute_reference_structures=srs)
            print(md)

        srs = {'Co': self.ti_hcp}
        with self.assertRaises(MixingDefectSetError):
            md = MixingDefectSet(solvent_element='Al',
                                 solvent_reference_structure=self.al_fcc,
                                 solute_elements=['Co'],
                                 solute_reference_structures=srs)
            print(md)

        # solute reference structures not a dictionary fail
        with self.assertRaises(MixingDefectSetError):
            md = MixingDefectSet(solvent_element='Al',
                                 solvent_reference_structure=self.al_fcc,
                                 solute_elements=['Co', 'Ti', 'Si'],
                                 solute_reference_structures=self.co_fcc)
            print(md)

        # all OK
        srs = {'Co': self.co_fcc, 'Ti': self.ti_hcp}
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             solute_elements=['Co', 'Ti', 'Si'],
                             solute_reference_structures=srs,
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)
        self.assertDictEqual(md.solute_reference_structures,
                             {'Co': self.co_fcc,
                              'Ti': self.ti_hcp,
                              'Si': None})

        # solute reference structure set disallow setter
        with self.assertRaises(MixingDefectSetError):
            md.solute_reference_structures = {'Co': self.ti_hcp}

    def test_min_image_dist(self):
        # min image dist OK
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             solute_elements=['Co', 'Si'],
                             solute_reference_structures={'Co': self.co_fcc},
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)
        self.assertAlmostEqual(md.min_image_dist, 6.)

        # min image distance fallback
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             solute_elements=['Co', 'Si'],
                             solute_reference_structures={'Co': self.co_fcc},
                             supercell_for_mixing=self.al_fcc_super)
        self.assertAlmostEqual(md.min_image_dist, 12.)

        # min image distance disallow setter
        with self.assertRaises(MixingDefectSetError):
            md.min_image_dist = 8.0

    def test_mixing_defects(self):
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             solute_elements=['Al', 'Co', 'Si'],
                             solute_reference_structures={'Co': self.co_fcc},
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)
        # list of solutes
        self.assertListEqual(sorted(md.mixing_defects.keys()), ['Co', 'Si'])
        # solvent element
        self.assertEqual(md.mixing_defects['Co'].solvent_element, 'Al')
        # solvent reference structure
        self.assertEqual(md.mixing_defects['Si'].solvent_reference_structure,
                         self.al_fcc)
        # solute element
        self.assertEqual(md.mixing_defects['Co'].solute_element, 'Co')
        # solute reference structures (None, if not specified)
        self.assertEqual(md.mixing_defects['Co'].solute_reference_structure,
                         self.co_fcc)
        self.assertEqual(md.mixing_defects['Si'].solute_reference_structure,
                         None)

    def test_add_solute_to_defects_set(self):
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             solute_elements=['Al', 'Co', 'Si'],
                             solute_reference_structures={'Co': self.co_fcc},
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)

        # solute already present
        with self.assertRaises(MixingDefectSetError):
            md.add_solute_to_defects_set('Si')

        # solute same as solvent
        with self.assertRaises(MixingDefectSetError):
            md.add_solute_to_defects_set('Al')

        # add solute without reference structure
        md.add_solute_to_defects_set('Mn')
        self.assertEqual(md.mixing_defects['Mn'].solvent_element, 'Al')
        self.assertEqual(md.mixing_defects['Mn'].solute_reference_structure,
                         None)
        self.assertEqual(md.solute_reference_structures['Mn'], None)
        self.assertListEqual(md.solute_elements, ['Co', 'Mn', 'Si'])

        # add solute with reference structure
        md.add_solute_to_defects_set('Ti',
                                     solute_reference_structure=self.ti_hcp)
        self.assertEqual(md.mixing_defects['Ti'].solute_reference_structure,
                         self.ti_hcp)
        self.assertEqual(md.solute_reference_structures['Ti'], self.ti_hcp)
        self.assertListEqual(md.solute_elements, ['Co', 'Mn', 'Si', 'Ti'])

    def test_remove_solute_from_defects_set(self):
        srs = {'Co': self.co_fcc, 'Ti': self.ti_hcp}
        md = MixingDefectSet(solvent_element='Al',
                             solvent_reference_structure=self.al_fcc,
                             solute_elements=['Al', 'Co', 'Si', 'Ti'],
                             solute_reference_structures=srs,
                             min_image_dist=6.,
                             supercell_for_mixing=self.al_fcc_super)

        # element not among solutes
        with self.assertRaises(MixingDefectSetError):
            md.remove_solute_from_defects_set('Al')

        # remove solute as expected
        md.remove_solute_from_defects_set('Co')
        self.assertListEqual(sorted(md.mixing_defects.keys()), ['Si', 'Ti'])
        self.assertDictEqual(md.solute_reference_structures,
                             {'Si': None, 'Ti': self.ti_hcp})
        self.assertListEqual(md.solute_elements, ['Si', 'Ti'])


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)
