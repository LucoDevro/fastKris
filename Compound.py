class Compound:
    
    def __init__(self, stock, label):
        self.stock=stock
        self.label=label
    
    def getStock(self):
        return self.stock
    
    def getLabel(self):
        return self.label
    
class Salt(Compound):
    
    def __init__(self, stock, label):
        super().__init__(stock, label)
        
    def dilute(self, outputConc, wellVol):
        return outputConc*wellVol/self.stock
    
class Precipitate(Compound):
    
    def __init__(self, stock, label):
        super().__init__(stock, label)
        
    def dilute(self, outputPerc, wellVol):
        return outputPerc*wellVol/self.stock
    
class Buffer(Compound):
    
    def __init__(self, stock, label):
        super().__init__(stock, label)