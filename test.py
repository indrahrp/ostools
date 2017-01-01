import unittest
def add(x,y):
   return x + y
   
class SimpleTest(unittest.TestCase):
   def testadd1(self):
      self.assertEquals(add(4,5),9)
      
      

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
      
if __name__ == '__main__':
   unittest.main()