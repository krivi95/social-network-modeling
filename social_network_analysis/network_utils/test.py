class A():
    def __init__(self):
        self.__a = 1
        self._a = 1

class B(A):
    def __init__(self):
        super().__init__()
        self.b = 2

class C(B):
    def __init__(self):
        super().__init__()
        self.c=3
        print

print(A().__a)
