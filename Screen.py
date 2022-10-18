#Screen class

from Compound import *
import numpy as np

class Screen:
    def __init__(self, range, compounds, plate):
        self.range = range #dictionary by compound that needs a range reported
        self.compounds = compounds #a list
        self.plate = plate #has a property max_volume (see API)

    def calcConcentration(self,compound, outConc):
        outVol = []
        maxVol = self.plate.max_volume
        for conc in outConc:
            outVol.append(compound.dilute(outConc, maxVol))
        return outVol

class oneD(Screen):
    def __init__(self, index, *args, **kwargs):
        self.index = index #a list
        super().__init__(*args, **kwargs)

    def getOutConc(self, compound):
        #get np array
        return np.linspace(start=self.range[compound][0], stop=self.range[compound][1], num=len(self.plate.wells())).tolist()

    def getAllVol(self):
        dict = {}
        outConc = self.getOutConc(self.compounds[self.index[0]])
        out = self.calcConcentration(self.compounds[self.index[0]],outConc)
        dict[self.compounds[self.index[0]]] = out
        #add fixed volumes other compounds when constructing input file
        return dict

class twoD(Screen):

    def __init__(self, index, *args, **kwargs):
        self.index = index #a list
        super().__init__(*args, **kwargs)

    def getOutConc(self, compound):
        if isinstance(compound,Salt):
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1], num=len(self.plate.rows()[0])).tolist()
        if isinstance(compound, Precipitate):
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1], num=len(self.plate.columns()[0])).tolist()

    def getAllVol(self):
        dict = {}
        for ind in self.index:
            outConc = self.getOutConc(self.compounds[ind])
            out = self.calcConcentration(self.compounds[ind],outConc)
            dict[self.compounds[ind]] = out
        #add fixed volumes other compounds when constructing input file
        return dict

class threeD(Screen):

    def getOutConc(self, compound):
        if isinstance(compound,Salt):
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1], num=len(self.plate.rows()[0])).tolist()
        if isinstance(compound, Precipitate):
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1], num=len(self.plate.columns()[0])).tolist()

    def getAllVol(self):
        dict = {}
        for compound in self.compounds:
            if isinstance(compound,Salt) or isinstance(compound, Precipitate):
                outConc = self.getOutConc(compound)
                out = self.calcConcentration(self.compound,outConc)
                dict[compound] = out
        return dict