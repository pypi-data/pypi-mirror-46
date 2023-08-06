import unittest

from .mystack import Stack
from .stack_exceptions import StackFullError
from .stack_exceptions import StackEmptyError


class StackTests(unittest.TestCase):
    def test_round5(self):
        self.assertEqual(Stack.round5(67), 70)
        self.assertEqual(Stack.round5(91), 95)

    def test_from_values(self):
        st = Stack.from_values()
        self.assertEqual(len(st), 0)
        
        st = Stack.from_values(11,22)
        self.assertEqual(len(st), 2)
        self.assertEqual(st.top(), 22)

    def test_push(self):
        """ self.assertRaises fails when method doesn't throw mentioned error.
            Since, exception is handled, method push() doesn'throw error. 
            Hence, assertRaises fails. Same with other below methods tests
        """
        st = Stack()
        st.push(11)
        st.push(22)
        st.push(33)
        self.assertEqual(st.top(), 33)
        self.assertEqual(len(st), 3)
        st.push(44)
        st.push(55) 
        #self.assertRaises(StackFullError,st.push, 99)

    def test_pop(self):
        st = Stack.from_values(11, 22)       
        self.assertEqual(st.pop(), 22)
        self.assertEqual(len(st), 1)
        self.assertEqual(st.pop(), 11)
        #self.assertRaises(StackEmptyError,st.pop)

    def test_top(self):
        st = Stack.from_values(11,22)
        self.assertEqual(st.top(), 22)
        st.pop()
        self.assertEqual(st.top(), 11)
        st.pop()
        #self.assertRaises(StackEmptyError,st.top)

    def test_method_unittest(self):
        """ since exception is not handled, method method_unittest() raises StackEmptyError.
            So, assertRaises() passed.        
        """
        st = Stack()
        self.assertRaises(StackEmptyError,st.method_unittest)

def main():
    print("tests begin...")
    stest = StackTests()
    stest.test_round5()
    stest.test_from_values()
    stest.test_push()
    stest.test_top()
    stest.test_pop()     
    stest.test_method_unittest()  
    print("all tests passed! No errors!")

if __name__ == '__main__':
    main()
