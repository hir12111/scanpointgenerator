from collections import OrderedDict
import unittest

from scanpointgenerator import SpiralGenerator


class SpiralGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.g = SpiralGenerator(['x', 'y'], "mm", [0.0, 0.0], 1.5, alternate_direction=True)

    def test_init(self):
        self.assertEqual(self.g.position_units, dict(x="mm", y="mm"))
        self.assertEqual(self.g.index_dims, [6])
        self.assertEqual(self.g.index_names, ["x", "y"])

    def test_iterator(self):
        positions = [{'y': -0.3211855677650875, 'x': 0.23663214944574582},
                     {'y': -0.25037538922751695, 'x': -0.6440318266552169},
                     {'y': 0.6946549630820702, 'x': -0.5596688286164636},
                     {'y': 0.9919687803189761, 'x': 0.36066957248394327},
                     {'y': 0.3924587351155914, 'x': 1.130650533568409},
                     {'y': -0.5868891557832875, 'x': 1.18586065489788},
                     {'y': -1.332029488076613, 'x': 0.5428735608675326}]
        lower = [{'y': 0.0, 'x': 0.0},
                 {'y': -0.5189218293602549, 'x': -0.2214272368007088},
                 {'y': 0.23645222432582483, 'x': -0.7620433832656455},
                 {'y': 0.9671992383675001, 'x': -0.13948222773063082},
                 {'y': 0.7807653675717078, 'x': 0.8146440851904461},
                 {'y': -0.09160107657707395, 'x': 1.2582363345925418},
                 {'y': -1.0190886264001306, 'x': 0.9334439933089926}]
        upper = [{'y': -0.5189218293602549, 'x': -0.2214272368007088},
                 {'y': 0.23645222432582483, 'x': -0.7620433832656455},
                 {'y': 0.9671992383675001, 'x': -0.13948222773063082},
                 {'y': 0.7807653675717078, 'x': 0.8146440851904461},
                 {'y': -0.09160107657707395, 'x': 1.2582363345925418},
                 {'y': -1.0190886264001306, 'x': 0.9334439933089926},
                 {'y': -1.4911377166541206, 'x': 0.06839234794968006}]
        indexes = [0, 1, 2, 3, 4, 5, 6]

        for i, p in enumerate(self.g.iterator()):
            self.assertEqual(p.positions, positions[i])
            self.assertEqual(p.lower, lower[i])
            self.assertEqual(p.upper, upper[i])
            self.assertEqual(p.indexes, [indexes[i]])
        self.assertEqual(i, 6)

    def test_to_dict(self):
        expected_dict = OrderedDict()
        expected_dict['type'] = "SpiralGenerator"
        expected_dict['name'] = ['x', 'y']
        expected_dict['units'] = 'mm'
        expected_dict['centre'] = [0.0, 0.0]
        expected_dict['radius'] = 1.5
        expected_dict['scale'] = 1
        expected_dict['alternate_direction'] = True

        d = self.g.to_dict()

        self.assertEqual(expected_dict, d)

    def test_from_dict(self):
        _dict = OrderedDict()
        _dict['type'] = "SpiralGenerator"
        _dict['name'] = ['x', 'y']
        _dict['units'] = 'mm'
        _dict['centre'] = [0.0, 0.0]
        _dict['radius'] = 1.5
        _dict['scale'] = 1
        _dict['alternate_direction'] = True

        units_dict = OrderedDict()
        units_dict['x'] = 'mm'
        units_dict['y'] = 'mm'

        gen = SpiralGenerator.from_dict(_dict)

        self.assertEqual(['x', 'y'], gen.name)
        self.assertEqual(units_dict, gen.position_units)
        self.assertEqual([0.0, 0.0], gen.centre)
        self.assertEqual(1.5, gen.radius)
        self.assertEqual(1, gen.scale)
