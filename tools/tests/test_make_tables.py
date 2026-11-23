"""Run: python3 -I tools/tests/test_make_tables.py"""
import json, os, sys, unittest
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..'))
import make_tables as mt  # noqa: E402

STUDY = os.path.expanduser('~/pvz-research/unnamed-tables.json')
VANILLA = os.path.join(HERE, '..', 'fixtures', 'vanilla-tables.json')


class MakeTablesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(STUDY):
            raise unittest.SkipTest('needs unnamed-tables.json, the table export of your own Unnamed exe')
        cls.out = mt.build(json.load(open(STUDY)), json.load(open(VANILLA)))

    def test_video_costs(self):
        p = self.out['plants']
        self.assertEqual(p['POTATOMINE']['seedCost'], 50)
        self.assertEqual(p['FUMESHROOM']['seedCost'], 100)
        self.assertEqual(p['PLANTERN']['seedCost'], 150)
        self.assertEqual(p['GARLIC']['seedCost'], 100)
        self.assertEqual(p['MARIGOLD']['seedCost'], 150)

    def test_other_diffs(self):
        self.assertEqual(self.out['plants']['WALLNUT']['refreshTime'], 2400)
        self.assertEqual(self.out['projectiles']['STAR']['damage'], 1)
        self.assertEqual(self.out['projectiles']['COBBIG']['damage'], 400)
        self.assertEqual(self.out['zombies']['POLEVAULTER']['zombieValue'], 3)

    def test_only_changed_fields(self):
        self.assertNotIn('PEASHOOTER', self.out['plants'])          # Peashooter row identical to vanilla
        self.assertNotIn('refreshTime', self.out['plants']['POTATOMINE'])

    def test_mod_only_plants_excluded(self):
        names = set(self.out['plants'])
        self.assertTrue(all(not n.startswith('0X') and not n.isdigit() for n in names))
        self.assertLessEqual(len(names), 53)


if __name__ == '__main__':
    unittest.main()
