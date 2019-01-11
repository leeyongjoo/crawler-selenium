col = ['name', 'type', 'nm', 'coreclock', 'b_coreclock', 'sp',
           'pcie', 'gddr', 'memoryclock', 'volume', 'bus']

class VGA:

    def __init__(self):
        self.d = { c:"NA" for c in col }

    def setData(self, s):
        pass

v = VGA()
print(v.d)