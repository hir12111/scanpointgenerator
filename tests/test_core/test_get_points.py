import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import unittest

from test_util import ScanPointGeneratorTest
from scanpointgenerator import CompoundGenerator, Generator
from scanpointgenerator import LineGenerator, StaticPointGenerator
from scanpointgenerator import Point
from scanpointgenerator import CircularROI, ROIExcluder
from scanpointgenerator import RandomOffsetMutator
from scanpointgenerator.compat import range_, np

class GetPointsTest(ScanPointGeneratorTest):

    def setUp(self):
        l1 = LineGenerator("x", "mm", 0, 5, 5)
        l2 = LineGenerator("y", "nm", 0, 5, 5)
        l3 = LineGenerator("z", "mm", 0, 5, 5)
        self.comp = CompoundGenerator([l1, l2, l3], [], [], 5, True, 7)
        self.comp.prepare()

    def test_simple_points(self):
        C = self.comp.get_points(7, 12)
        np.testing.assert_array_equal(np.asarray([[0, 1, 2],[0, 1, 3],[0, 1, 4],[0, 2, 0],[0, 2, 1]]), C.indexes)
        np.testing.assert_array_equal(np.asarray([0., 0., 0., 0., 0.]), C.lower['x'])
        np.testing.assert_array_equal(np.asarray([1.25, 1.25, 1.25, 2.5 , 2.5 ]), C.lower['y'])
        np.testing.assert_array_equal(np.asarray([ 1.875,  3.125,  4.375, -0.625,  0.625]), C.lower['z'])
        np.testing.assert_array_equal(np.full(5, 5), C.duration)
        np.testing.assert_array_equal(np.full(5, 7), C.delay_after)
    
    def test_bulk(self):
        C = self.comp.get_points(42, 59)
        for a in range(42, 59):
            self.assertListAlmostEqual(self.comp.get_point(a).indexes, C.indexes[a-42])
            for axis in ["x", "y", "z"]:
                np.testing.assert_array_equal(self.comp.get_point(a).lower[axis], C.lower[axis][a-42])
                np.testing.assert_array_equal(self.comp.get_point(a).upper[axis], C.upper[axis][a-42])
                np.testing.assert_array_equal(self.comp.get_point(a).positions[axis], C.positions[axis][a-42])
            
    def test_alternating(self):
        l1 = LineGenerator("x", "mm", 0, 5, 5)
        l2 = LineGenerator("y", "nm", 0, 5, 5, True)
        l3 = LineGenerator("z", "mm", 0, 5, 5)
        comp = CompoundGenerator([l1, l2, l3], [], [], 5)
        comp.prepare()
        np.testing.assert_array_equal(np.asarray([[0,0,0],[0,0,1],[0,0,2],[0,0,3],[0,0,4],[0,1,0],[0,1,1],[0,1,2],[0,1,3],[0,1,4],[0,2,0]]), comp.get_points(0, 11).indexes)
        np.testing.assert_array_equal(np.asarray([[0,3,1],[0,3,2],[0,3,3],[0,3,4],[0,4,0],[0,4,1],[0,4,2],[0,4,3],[0,4,4],[1,4,0],[1,4,1]]), comp.get_points(16, 27).indexes) 
        
    def test_roi(self):
        l1 = LineGenerator("x", "mm", 0.5, 5.5, 6)
        l2 = LineGenerator("y", "mm", 0.5, 5.5, 6)
        r1 = CircularROI([2.5, 2.5], 1.01)
        e = ROIExcluder([r1], ["x", "y"])
        self.comp = CompoundGenerator([l1, l2], [e], [], 5, True, 7)
        self.comp.prepare()
        # Comp.size = 5, only these points included
        y = [2.5, 1.5, 2.5, 3.5, 2.5]
        y_up = [3, 2, 3, 4, 3]
        y_dn = [2, 1, 2, 3, 2]
        x = [1.5, 2.5, 2.5, 2.5, 3.5]
        C = self.comp.get_points(0,5)
        np.testing.assert_array_equal([0,1,2,3,4], C.indexes)
        np.testing.assert_array_equal(x, C.positions["x"])
        np.testing.assert_array_equal(x, C.lower["x"])
        np.testing.assert_array_equal(x, C.upper["x"])
        np.testing.assert_array_equal(y, C.positions["y"])
        np.testing.assert_array_equal(y_dn, C.lower["y"])
        np.testing.assert_array_equal(y_up, C.upper["y"])
        
    def test_random_offset(self):
        l1 = LineGenerator("x", "mm", 0.5, 5.5, 6)
        l2 = LineGenerator("y", "mm", 0.5, 5.5, 6)
        m1 = RandomOffsetMutator(12, ["x", "y"], [0.1, 0.1])
        self.comp = CompoundGenerator([l1, l2], [], [m1], 5, True, 7)
        self.comp.prepare()
        # Comp.size = 5, only these points included
        C = self.comp.get_points(0, 8)
        np.testing.assert_array_almost_equal([0.458672, 1.543717, 2.582332, 3.514304, 4.558364, 5.528023, 0.574501, 1.452161], C.positions["y"])