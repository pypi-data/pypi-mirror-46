import unittest
from megnet.activations import softplus2
import numpy as np
import tensorflow as tf


def softplus_np(x):
    return np.log(np.exp(x) + 1) - np.log(2.)


class TestSP(unittest.TestCase):
    def test_softplus(self):
        sess = tf.InteractiveSession()
        x = 10.0
        self.assertAlmostEqual(sess.run(softplus2(x)), softplus_np(x), places=5)


if __name__ == '__main__':
    unittest.main()
