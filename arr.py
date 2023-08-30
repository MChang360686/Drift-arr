import csv


# Make classes
class Ultimate_Parent:
    def __init__(self, children):
        self.children = children
        pass

    def mnd(self):
        pass

class Parent:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        pass

    def mnd(self):
        pass

class Child:
    def __init__(self, parent):
        self.parent = parent

    def mnd(self):
        pass

if __name__ == '__main__':
    pass