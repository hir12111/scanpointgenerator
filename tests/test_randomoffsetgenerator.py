from collections import OrderedDict
import unittest

from test_util import ScanPointGeneratorTest
from scanpointgenerator import RandomOffsetGenerator
from scanpointgenerator import LineGenerator

from pkg_resources import require
require("mock")
from mock import patch, MagicMock


class RandomOffsetGeneratorTest(ScanPointGeneratorTest):

    def setUp(self):
        line_gen = LineGenerator("x", "mm", 1.0, 5.0, 5)
        self.g = RandomOffsetGenerator(line_gen, 1, dict(x=0.25))

    def test_init(self):
        self.assertEqual(self.g.position_units, dict(x="mm"))
        self.assertEqual(self.g.index_dims, [5])
        self.assertEqual(self.g.index_names, ["x"])

    def test_iterator(self):
        positions = [1.0165839522345654, 1.808864087257092,
                     3.007833629207929, 4.049827994120938, 5.033343651164651]
        lower = [0.620443884723302, 1.4127240197458288,
                 2.4083488582325105, 3.5288308116644336, 4.541585822642794]
        upper = [1.4127240197458288, 2.4083488582325105,
                 3.5288308116644336, 4.541585822642794, 5.5251014796865086]
        indexes = [0, 1, 2, 3, 4]

        for i, p in enumerate(self.g.iterator()):
            self.assertEqual(p.positions, dict(x=positions[i]))
            self.assertEqual(p.lower, dict(x=lower[i]))
            self.assertEqual(p.upper, dict(x=upper[i]))
            self.assertEqual(p.indexes, [indexes[i]])
        self.assertEqual(i, 4)


class TestSerialisation(unittest.TestCase):

    def setUp(self):
        self.l = MagicMock()
        self.l_dict = MagicMock()
        self.max_offset = dict(x=0.25)

        self.g = RandomOffsetGenerator(self.l, 1, self.max_offset)

    def test_to_dict(self):
        self.l.to_dict.return_value = self.l_dict

        expected_dict = OrderedDict()
        expected_dict['type'] = "RandomOffsetGenerator"
        expected_dict['generator'] = self.l_dict
        expected_dict['seed'] = 1
        expected_dict['max_offset'] = self.max_offset

        d = self.g.to_dict()

        self.assertEqual(expected_dict, d)

    @patch('scanpointgenerator.randomoffsetgenerator.Generator')
    def test_from_dict(self, SPG_mock):
        SPG_mock.from_dict.return_value = self.l

        _dict = OrderedDict()
        _dict['generator'] = self.l_dict
        _dict['seed'] = 1
        _dict['max_offset'] = self.max_offset

        units_dict = OrderedDict()
        units_dict['x'] = 'mm'

        gen = RandomOffsetGenerator.from_dict(_dict)

        self.assertEqual(gen.gen, self.l)
        self.assertEqual(1, gen.seed)
        self.assertEqual(self.max_offset, gen.max_offset)


if __name__ == "__main__":
    unittest.main()