import unittest,configsysmod
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





class simpleTest2(unittest.TestCase):
   def setUp(self):
      self.a = 10
      self.b = 20
      name = self.shortDescription()
      if name == "Add":
         self.a = 10
         self.b = 20
         print (name, self.a, self.b)
      if name == "sub":
         self.a = 50
         self.b = 60
         print (name, self.a, self.b)
   def tearDown(self):
      print ('\nend of test',self.shortDescription())

   def testadd(self):
      """Adding"""
      result = self.a+self.b
      self.assertTrue(result == 30)
   def testsub(self):
      """sub"""
      result = self.a-self.b
      self.assertTrue(result == -10)

   def testconfigh(self):
       var=configsysmod.usage()
       
       
       
if __name__ == '__main__':
   unittest.main()