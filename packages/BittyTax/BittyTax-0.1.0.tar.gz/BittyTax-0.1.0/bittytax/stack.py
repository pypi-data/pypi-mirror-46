class Stack:
    def __init__(self):
        self.data = []
    def push(self,n):
        self.data.append(n)
    def pop(self):
        return self.data.pop()
    def __iter__(self):
        return self
    def next(self):
        if len(self.data)>0:
            return self.pop()
        else:
            raise StopIteration
