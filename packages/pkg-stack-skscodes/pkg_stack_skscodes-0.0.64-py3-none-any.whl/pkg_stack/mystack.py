from .stack_exceptions import StackError
from .stack_exceptions import StackFullError
from .stack_exceptions import StackEmptyError
import time

class Stack:
	"""Create and perform general stack operations."""
	count = 0

	def __init__ (self, cap = 5):
		self._capacity = cap
		self._capacity=Stack.round5(cap)
		self._stack = []
		Stack.count += 1
	def __str__(self):
		return str(self._stack)
	def __len__(self):
		return len(self._stack)
	def __contains__(self, val):
		return val in self._stack

	@classmethod
	def from_values(cls,*args):
		"""Construct a Stack from given values.
		
		Params:
		*args: Integer values to be pushed onto the stack being created.
		
		Returns: The newly created Stack object
		"""
		stk = cls(len(args))
		for val in args:
			stk.push(val)
		return stk

	@staticmethod
	def round5(value):
		"""Round the value to the next multiple of 5."""			
		if value % 5 == 0:
			return value
		else:
			return value + (5 - value % 5)	

	""" Using temp() to hide member '_capacity', exposing 'temp'. 
		Added decorator '@property', so method can be used as property. 
		From outside it will look property, not method
	"""
	@property
	def temp(self):
		return self._capacity

	"""  to set val: s.temp = <value>	"""
	@temp.setter
	def temp(self,value):
		self._capacity = value

	def push(self, value):
		"""Push a value onto the stack.

		Params:
            value: An integer value to be pushed onto the stack.

        Raises:
            StackFullError: When no more values can be pushed
                onto stack due to lack of space.
        """

		try:
			if self.is_full():
				#raise Exception("Stack full")
				raise StackFullError
			else:
				return self._stack.append(value)
		except StackFullError as e:
			print(e)

	def pop(self):
		"""Pop a value from the stack.

		Returns: The integer value popped from the stack.

		Raises:
		StackEmptyError: When trying to pop from empty stack.
		"""
		try:
			if self.is_empty():
				#raise Exception("Stack empty")
				raise StackEmptyError
			else:
				pop_value = self._stack[-1]
				del self._stack[-1]		
				return pop_value
		except StackEmptyError as e:
			print(e)

	def method_unittest(self):
		raise StackEmptyError

	def top(self):
		"""Return the most recent value pushed onto stack.
        However the value is not popped from the stack it's just
        returned.

        Returns: Most recent value pushed onto stack.

        Raises:
            StackEmptyError: When trying to read from empty stack.
        """

		try:
			if self.is_empty():
				#raise Exception("Stack empty")
				raise StackEmptyError				
			return self._stack[-1]
		except Exception as e:
			print(e)

	def is_full(self):
		"""Return True when stack full otherwise False."""		
		return len(self._stack) == self._capacity

	def is_empty(self):
		"""Returns true if stack is empty, else false"""		
		return len(self._stack) == 0


def main():
	print("demo begins...")
	print()
	time.sleep(1)
	print("accessing doc string of class Stack...")	
	time.sleep(2)
	print(Stack.__doc__)
	print()
	time.sleep(3)

	print("displaying attributes of class Stack...")
	time.sleep(2)
	print(dir(Stack))
	print()	
	time.sleep(4)

	print("displaying doc string of class method 'from_values' ...")	
	time.sleep(3)
	print(Stack.from_values.__doc__)
	print()	
	time.sleep(3)

	print("testing...")
	print()
	time.sleep(1)

	print("creating empty stack...")
	time.sleep(2)
	s = Stack()	
	print(s)
	print("stack created.. ")
	print()
	time.sleep(2)

	print("checking if stack is empty...")
	time.sleep(2)
	print("stack empty? %s" % (s.is_empty()))
	print()
	time.sleep(2)	

	print("Exception use-case: doing pop on empty stack...")
	time.sleep(3)
	s.pop()
	print()
	time.sleep(2)

	print("Exception use-case: fetching top value of empty stack...")
	time.sleep(3)
	s.top()
	print()
	time.sleep(2)

	print("creating stack of size 5...")
	time.sleep(2)
	s = Stack.from_values(1,2,3,4,5)	
	print(s)
	print("stack created.. ")
	print()
	time.sleep(2)

	print("operation: pop from stack")
	time.sleep(2)
	print("popped value = %s" % (s.pop()))
	time.sleep(1)
	print("result stack: %s" % (str(s)))
	print()
	time.sleep(2)

	print("operation: push 5 onto stack")
	time.sleep(2)
	s.push(5)
	print("result stack: %s" % (str(s)))
	print()
	time.sleep(2)

	print("operation: fetch top value from stack")
	time.sleep(2)
	top = s.top()	
	print("top value = %s" % (top))	
	print("result stack: %s" % (str(s)))
	print()
	time.sleep(2)

	print("checking if stack is full...")
	time.sleep(3)
	print("is stack full? %s" % (s.is_full()))
	print()
	time.sleep(2)

	print("Exception use-case: pushing value 6 on full stack...")
	time.sleep(3)
	s.push(6)
	print()
	time.sleep(2)


	print("demo ends!")	



if __name__ == '__main__':
	main()