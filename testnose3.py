import code  
import operator
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises



class Math:
	def sum(self, a, b):  
		return a + b
	def subs(self, a, b):
		return a - b
	def mul(self, a, b):
		return a * b
m = Math()

def test_sum():  
    """Check is sum method is equivalent to operator"""
    #eq_(m.sum(1, 1), operator.add(1, 1))
    assert_equal(m.sum(1,1), 2)


def test_sub():
	"""Check is sub method is equivalent to operator"""
	#eq_(m.sub(2, 1), operator.sub(2, 1))


def test_mul():  
    """Check is mul method is equivalent to operator"""
    #eq_(m.mul(1, 1), operator.mul(1, 1))