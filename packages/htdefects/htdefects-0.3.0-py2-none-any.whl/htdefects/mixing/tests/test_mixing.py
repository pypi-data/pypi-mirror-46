import unittest
from htdefects.mixing import defect
from dftinpgen import atoms


class TestMixingDefect(unittest.TestCase):
    """Class of unit tests for `mixing.MixingDefect`."""


    def test_solvent_solute_elements(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')

        # solvent and solute elements
        md = defect.MixingDefect(solvent_element='Al', solvent_reference_structure=al_fcc,
                                 solute_element='Ca', min_image_dist=5.)
        self.assertEqual(md.solvent_element, 'Al')
        self.assertEqual(md.solute_element, 'Ca')

        # unsupported solvent element
        with self.assertRaises(defect.MixingDefectError):
            md = defect.MixingDefect(solvent_element='Al1', solvent_reference_structure=al_fcc,
                                     solute_element='Ca', min_image_dist=5.)

        # unsupported solute element
        with self.assertRaises(defect.MixingDefectError):
            md = defect.MixingDefect(solvent_element='Al', solvent_reference_structure=al_fcc,
                                     solute_element='Ca1', min_image_dist=5.)


    def test_solvent_solute_reference_structures(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')
        co_fcc = atoms.Structure('Co_fcc.vasp')

        # solvent reference structure error if structure does not have element
        with self.assertRaises(defect.MixingDefectError):
            md = defect.MixingDefect(solvent_element='Co', solvent_reference_structure=al_fcc,
                                     solute_element='Ca', min_image_dist=5.)

        # solvent reference structure
        md = defect.MixingDefect(solvent_element='Al', solvent_reference_structure=al_fcc,
                                 solute_element='Ca', min_image_dist=5.)
        self.assertAlmostEqual(md.solvent_reference_structure.cell[0][0], 4.1259673)

        # solute reference structure error if structure does not have element
        with self.assertRaises(defect.MixingDefectError):
            md = defect.MixingDefect(solvent_element='Al', solvent_reference_structure=al_fcc,
                                     solute_element='Ca', solute_reference_structure=co_fcc,
                                     min_image_dist=5.)

        # solute reference structure
        md = defect.MixingDefect(solvent_element='Al', solvent_reference_structure=al_fcc,
                                 solute_element='Co', solute_reference_structure=co_fcc,
                                 min_image_dist=5.)
        self.assertAlmostEqual(md.solute_reference_structure.cell[0][0], 3.5688)


    def test_min_image_dist(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')
        co_fcc = atoms.Structure('Co_fcc.vasp')

        md = defect.MixingDefect(solvent_element='Al', solvent_reference_structure=al_fcc,
                                 solute_element='Co', solute_reference_structure=co_fcc,
                                 min_image_dist=5.)
        self.assertAlmostEqual(md.min_image_dist, 5.)

        # min image distance fallback
        md = defect.MixingDefect(solvent_element='Al', solvent_reference_structure=al_fcc,
                                 solute_element='Co', solute_reference_structure=co_fcc)
        self.assertAlmostEqual(md.min_image_dist, 15.)

        md = defect.MixingDefect(solvent_element='Al', solvent_reference_structure=al_fcc,
                                 solute_element='Co', solute_reference_structure=co_fcc,
                                 min_image_dist='fifteen')
        self.assertAlmostEqual(md.min_image_dist, 15.)


    def test_solute_in_solvent_structure(self):
        ti_hcp = atoms.Structure('Ti_hcp.vasp')
        co_fcc = atoms.Structure('Co_fcc.vasp')

        md = defect.MixingDefect(solvent_element='Ti', solvent_reference_structure=ti_hcp,
                                 solute_element='Co', solute_reference_structure=co_fcc,
                                 min_image_dist=5.)
        # title
        self.assertEqual(md.solute_in_solvent_structure.title, 'Ti2')
        # atom types
        self.assertListEqual(md.solute_in_solvent_structure.atomtypes, ['Co'])
        # scaled lattice vectors
        for lv, lv_ref in zip(md.solute_in_solvent_structure.cell[1], [-1.2547253, 2.1732221, 0.]):
            self.assertAlmostEqual(lv, lv_ref)


    def test_defect_structure(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')
        co_fcc = atoms.Structure('Co_fcc.vasp')

        md = defect.MixingDefect(solvent_element='Al', solvent_reference_structure=al_fcc,
                                 solute_element='Co', solute_reference_structure=co_fcc,
                                 min_image_dist=8.)
        # atom types
        self.assertListEqual(md.defect_structure.atomtypes, ['Al', 'Co'])
        # natoms
        self.assertListEqual(list(md.defect_structure.natoms), [31, 1])
        # title
        self.assertEqual(md.defect_structure.title, 'Al31Co1')



class TestMixingDefectSet(unittest.TestCase):
    """Class of unit tests for `mixing.MixingDefectSet`."""

    def test_solvent_elements(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')

        # solvent element
        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    min_image_dist=5.)
        self.assertEqual(md.solvent_element, 'Al')

        # unsupported solvent element
        with self.assertRaises(defect.MixingDefectError):
            md = defect.MixingDefectSet(solvent_element='Al1', solvent_reference_structure=al_fcc,
                                        min_image_dist=5.)


    def test_solvent_reference_structure(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')

        # solvent reference structure error if structure does not have element
        with self.assertRaises(defect.MixingDefectSetError):
            md = defect.MixingDefectSet(solvent_element='Ca', solvent_reference_structure=al_fcc,
                                        min_image_dist=5.)

        # solvent reference structure
        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    min_image_dist=5.)
        self.assertAlmostEqual(md.solvent_reference_structure.cell[0][0], 4.1259673)


    def test_solute_elements_set(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')

        # no solute elements specified
        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    min_image_dist=5.)
        self.assertListEqual(md.solute_elements, [])

        # solute elements as comma-separated string
        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    solute_elements=' Co, Ca, Co ,Mn', min_image_dist=5.)
        self.assertListEqual(md.solute_elements, ['Ca', 'Co', 'Mn'])

        # solute elements as a list; auto-removal of solvent element
        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    solute_elements=['Co', 'Al', 'Ca', 'Al', 'Mn'],
                                    min_image_dist=5.)
        self.assertListEqual(md.solute_elements, ['Ca', 'Co', 'Mn'])

        # solute elements set disallow setter
        with self.assertRaises(defect.MixingDefectSetError):
            md.solute_elements = ['Ca', 'Si']


    def test_solute_reference_structures_set(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')
        co_fcc = atoms.Structure('Co_fcc.vasp')
        ti_hcp = atoms.Structure('Ti_hcp.vasp')

        # no reference structures given
        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    solute_elements=['Co', 'Ti'], min_image_dist=5.)
        self.assertDictEqual(md.solute_reference_structures, {'Co': None, 'Ti': None})

        # invalid elements, structures in the reference structures Dictionary
        with self.assertRaises(defect.MixingDefectError):
            md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                        solute_elements=['Co'],
                                        solute_reference_structures={'Co1': co_fcc},
                                        min_image_dist=5.)

        with self.assertRaises(defect.MixingDefectError):
            md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                        solute_elements=['Co'],
                                        solute_reference_structures={'Co': ti_hcp},
                                        min_image_dist=5.)

        # check Dictionary format
        with self.assertRaises(defect.MixingDefectSetError):
            md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                        solute_elements=['Co', 'Ti', 'Si'],
                                        solute_reference_structures=co_fcc,
                                        min_image_dist=5.)
        # all OK
        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    solute_elements=['Co', 'Ti', 'Si'],
                                    solute_reference_structures={'Co': co_fcc, 'Ti': ti_hcp},
                                    min_image_dist=5.)
        self.assertDictEqual(md.solute_reference_structures, {'Co': co_fcc, 'Ti': ti_hcp, 'Si':
                                                                  None})
        # solute reference structure set disallow setter
        with self.assertRaises(defect.MixingDefectSetError):
            md.solute_reference_structures = {'Co': ti_hcp}


    def test_min_image_dist(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')
        co_fcc = atoms.Structure('Co_fcc.vasp')

        # min image dist OK
        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    solute_elements=['Co', 'Si'],
                                    solute_reference_structures={'Co': co_fcc},
                                    min_image_dist=6.)
        self.assertAlmostEqual(md.min_image_dist, 6.)

        # min image distance fallback
        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    solute_elements=['Co', 'Si'],
                                    solute_reference_structures={'Co': co_fcc})
        self.assertAlmostEqual(md.min_image_dist, 15.)

        # min image distance disallow setter
        with self.assertRaises(defect.MixingDefectSetError):
            md.min_image_dist = 8.0

    def test_mixing_defects_set(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')
        co_fcc = atoms.Structure('Co_fcc.vasp')

        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    solute_elements=['Al', 'Co', 'Si'],
                                    solute_reference_structures={'Co': co_fcc},
                                    min_image_dist=5.)
        # list of solutes
        self.assertListEqual(sorted(md.mixing_defects.keys()), ['Co', 'Si'])
        # solvent element
        self.assertEqual(md.mixing_defects['Co'].solvent_element, 'Al')
        # solvent reference structure
        self.assertEqual(md.mixing_defects['Si'].solvent_reference_structure, al_fcc)
        # solute element
        self.assertEqual(md.mixing_defects['Co'].solute_element, 'Co')
        # solute reference structures (None, if not specified)
        self.assertEqual(md.mixing_defects['Co'].solute_reference_structure, co_fcc)
        self.assertEqual(md.mixing_defects['Si'].solute_reference_structure, None)


    def test_add_solute_to_defects_set(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')
        co_fcc = atoms.Structure('Co_fcc.vasp')
        ti_hcp = atoms.Structure('Ti_hcp.vasp')

        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    solute_elements=['Al', 'Co', 'Si'],
                                    solute_reference_structures={'Co': co_fcc},
                                    min_image_dist=5.)

        # solute already present
        with self.assertRaises(defect.MixingDefectSetError):
            md.add_solute_to_defects_set('Si')

        # solute same as solvent
        with self.assertRaises(defect.MixingDefectSetError):
            md.add_solute_to_defects_set('Al')

        # add solute without reference structure
        md.add_solute_to_defects_set('Mn')
        self.assertEqual(md.mixing_defects['Mn'].solvent_element, 'Al')
        self.assertEqual(md.mixing_defects['Mn'].solute_reference_structure, None)
        self.assertEqual(md.solute_reference_structures['Mn'], None)
        self.assertListEqual(md.solute_elements, ['Co', 'Mn', 'Si'])

        # add solute with reference structure
        md.add_solute_to_defects_set('Ti', solute_reference_structure=ti_hcp)
        self.assertEqual(md.mixing_defects['Ti'].solute_reference_structure, ti_hcp)
        self.assertEqual(md.solute_reference_structures['Ti'], ti_hcp)
        self.assertListEqual(md.solute_elements, ['Co', 'Mn', 'Si', 'Ti'])


    def test_remove_solute_from_defects_set(self):
        al_fcc = atoms.Structure('Al_fcc.vasp')
        co_fcc = atoms.Structure('Co_fcc.vasp')
        ti_hcp = atoms.Structure('Ti_hcp.vasp')

        md = defect.MixingDefectSet(solvent_element='Al', solvent_reference_structure=al_fcc,
                                    solute_elements=['Al', 'Co', 'Si', 'Ti'],
                                    solute_reference_structures={'Co': co_fcc, 'Ti': ti_hcp},
                                    min_image_dist=5.)

        # element not among solutes
        with self.assertRaises(defect.MixingDefectSetError):
            md.remove_solute_from_defects_set('Al')

        # remove solute as expected
        md.remove_solute_from_defects_set('Co')
        self.assertListEqual(sorted(md.mixing_defects.keys()), ['Si', 'Ti'])
        self.assertDictEqual(md.solute_reference_structures, {'Si': None, 'Ti': ti_hcp})
        self.assertListEqual(md.solute_elements, ['Si', 'Ti'])



if __name__ == '__main__':
    unittest.main()
