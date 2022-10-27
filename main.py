from opentrons import protocol_api

# from Screen import *

metadata = {
    'apiLevel': '2.0',
    'protocolName': 'Crystallization dilution',
    'description': '''This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.''',
    'author': 'New API User'
}


def run(protocol: protocol_api.ProtocolContext):
    global compoundLibrary
    compoundLibrary = loadLibrary()
    print('Compound library loaded...')
    [tips, instruments, plates, screens] = setup(protocol)
    print('Screens parsed...')
    screen_vols = [s.getAllVol() for s in screens]

    reservoir_salt = protocol.load_labware('nest_12_reservoir_15ml', 7)
    reservoir_buffer = protocol.load_labware('nest_12_reservoir_15ml', 8)
    reservoir_prec = protocol.load_labware('nest_12_reservoir_15ml', 9)

    for screen in screens:
        concentration = screen.getAllVol()
        salt_value = list(concentration.values())[0]
        prec_value = list(concentration.values())[1]
        buffer_value = list(concentration.values())[2]
        for item in salt_value:
            instruments[0].transfer(item, reservoir_salt['A1'], screen.plate.wells())
        for item in prec_value:
            instruments[0].transfer(item, reservoir_buffer['A1'], screen.plate.wells())
        for item in buffer_value:
            instruments[0].transfer(item, reservoir_prec['A1'], screen.plate.wells())

            #mix_after=(3, 50))

#    reservoir_MQ = protocol.load_labware('nest_12_reservoir_15ml', 6)


#    instruments[0].transfer(100, reservoir['A1'], plates[0].wells())

#    for i in range(8):
#        row = plates[0].rows()[i]
#        instruments[0].transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))
#        instruments[0].transfer(100, row[:11], row[1:], mix_after=(3, 50))

def setup(protocol):
    with open('inputdata2.txt') as f:
        lines = f.read()
        lines = lines.split("\n\n")
        f.close()

    # parsing pipet tips
    tips_raw = lines[0].split("\n")
    tipsInput = tips_raw[0::2]
    tipsLocation = tips_raw[1::2]

    # loading pipet tips
    tips = [protocol.load_labware(tipsInput[i], tipsLocation[i]) for i in range(len(tipsInput))]

    # parsing pipetting instruments
    instr_raw = lines[1].split("\n")
    instrumentInput = instr_raw[0::2]
    instrumentLocation = instr_raw[1::2]

    # loading pipetting instruments
    instruments = [protocol.load_instrument(instrumentInput[i], instrumentLocation[i], tip_racks=[tips[i]]) for i in
                   range(len(instrumentInput))]

    # parsing plates
    plates_raw = lines[2].split("\n")
    platesInput = plates_raw[0::2]
    platesLocation = plates_raw[1::2]

    # loading plates
    plates = [protocol.load_labware(platesInput[i], platesLocation[i]) for i in range(len(platesInput))]

    # parsing screens
    screens_raw = lines[3].split('\n')
    screens = []
    all_screen_types = screens_raw[0::5]
    all_screen_compounds = screens_raw[1::5]
    all_screen_ranges = screens_raw[2::5]
    all_screen_plates = screens_raw[3::5]
    all_screen_workVol = screens_raw[4::5]
    numberOfScreens = len(all_screen_types)
    for s in range(numberOfScreens):

        # screen type (1D, 2D or 3D)
        screen_type = int(all_screen_types[s])

        # parse plate number and link the plate object to it
        screen_plate = int(all_screen_plates[s])
        screen_plate = protocol.loaded_labwares[screen_plate]

        # well working volume
        screen_workVol = int(all_screen_workVol[s])

        # compounds used in this particular screen
        screen_compounds = [compoundLibrary[i] for i in all_screen_compounds[s].split(',')]

        # parsing compound concentration ranges and linking them to the associated compound
        screen_range_raw = all_screen_ranges[s].split(',')
        screen_range = {}
        for c in range(len(screen_range_raw)):
            screen_range[screen_compounds[c]] = tuple([float(i) for i in screen_range_raw[c].split('-')])

        # creating Screen objects from the parsed properties, depending on the screen type
        if screen_type == 1:
            screen = oneD(screen_range, screen_compounds, screen_plate, screen_workVol)
        elif screen_type == 2:
            screen = twoD(screen_range, screen_compounds, screen_plate, screen_workVol)
        elif screen_type == 3:
            screen = threeD(screen_range, screen_compounds, screen_plate, screen_workVol)
        else:
            raise Exception('Unknown screen type.')
        screens.append(screen)

    return [tips, instruments, plates, screens]


def loadLibrary():
    with open('compLibrary.txt') as l:
        lines = l.read()
        lines = lines.split("\n")[:-1]
        l.close()

    labels = lines[0::3]
    types = lines[1::3]
    stockConc = lines[2::3]
    compLibrary = {}
    for i in range(len(labels)):
        if types[i].lower() == "salt":
            compLibrary[labels[i]] = Salt(float(stockConc[i]), labels[i])
        elif types[i].lower() == "precipitant":
            compLibrary[labels[i]] = Precipitant(float(stockConc[i]), labels[i])
        elif types[i].lower() == "buffer":
            compLibrary[labels[i]] = Buffer(float(stockConc[i]), labels[i])
        else:
            raise Exception("Compound type not understood.")

    return compLibrary


### Supporting classes ###
# Provisionary defined here as the OpenTrons simulation protocol bundle does not find the separate class files

# Screen class

# from Compound import *
import numpy as np


class Screen:

    def __init__(self, range, compounds, plate, workVol):
        self.range = range  # dictionary by compound that needs a range reported
        self.compounds = compounds  # a list
        self.workVol = workVol
        self.plate = plate

    def calcConcentration(self, compound, outConc):
        outVol = []
        for conc in outConc:
            outVol.append(round(compound.dilute(conc, self.workVol), 3))  # rounding up to 0.001 uL
        return outVol


class oneD(Screen):

    def __str__(self):
        return '1D screen, ' + str(self.range) + str(self.compounds) + ' on plate ' + str(self.plate) + ' (' + str(
            self.workVol) + ' uL)'

    def getOutConc(self, compound):
        # get np array
        return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                           num=len(self.plate.wells())).tolist()

    def getAllVol(self):
        dict = {}
        totVol = np.zeros(len(self.plate.rows()[0]) * len(self.plate.columns()[0]))
        for compound in self.compounds:
            outConc = self.getOutConc(compound)
            out = self.calcConcentration(compound, outConc)
            dict[compound] = out
            if not (isinstance(compound, Buffer)):
                totVol += np.array(out)
        buffer_index = [i for i in range(len(self.compounds)) if isinstance(self.compounds[i], Buffer)][0]
        dict[self.compounds[buffer_index]] = np.round(self.workVol - totVol, 3).flatten().tolist()
        return dict


class twoD(Screen):

    def __str__(self):
        return '2D screen, ' + str(self.range) + str(self.compounds) + ' on plate ' + str(self.plate) + ' (' + str(
            self.workVol) + ' uL)'

    def getOutConc(self, compound):
        if isinstance(compound, Salt):
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.rows()[0])).tolist()
        if isinstance(compound, Precipitant):
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.columns()[0])).tolist()
        if isinstance(compound, Buffer):
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.wells())).tolist()

    def getAllVol(self):
        dict = {}
        totVol = np.zeros(len(self.plate.rows()[0]) * len(self.plate.columns()[0]))
        for compound in self.compounds:
            outConc = self.getOutConc(compound)
            out = self.calcConcentration(compound, outConc)
            if isinstance(compound, Salt):
                out = np.tile(np.array(out), (len(self.plate.columns()[0]), 1)).flatten().tolist()
                totVol += np.array(out)
            elif isinstance(compound, Precipitant):
                out = np.tile(np.array(out), (len(self.plate.rows()[0]), 1)).transpose().flatten().tolist()
                totVol += np.array(out)
            dict[compound] = out
        buffer_index = [i for i in range(len(self.compounds)) if isinstance(self.compounds[i], Buffer)][0]
        dict[self.compounds[buffer_index]] = np.round(self.workVol - totVol, 3).flatten().tolist()
        return dict


# Identical to 2D class at the moment
class threeD(Screen):

    def __str__(self):
        return '3D screen, ' + str(self.range) + str(self.compounds) + ' on plate ' + str(self.plate) + ' (' + str(
            self.workVol) + ' uL)'

    def getOutConc(self, compound):
        if isinstance(compound, Salt):
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.rows()[0])).tolist()
        if isinstance(compound, Precipitant):
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.columns()[0])).tolist()
        if isinstance(compound, Buffer):
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.wells())).tolist()

    def getAllVol(self):
        dict = {}
        totVol = np.zeros(len(self.plate.rows()[0]) * len(self.plate.columns()[0]))
        for compound in self.compounds:
            outConc = self.getOutConc(compound)
            out = self.calcConcentration(compound, outConc)
            if isinstance(compound, Salt):
                out = np.tile(np.array(out), (len(self.plate.columns()[0]), 1)).flatten().tolist()
            elif isinstance(compound, Precipitant):
                out = np.tile(np.array(out), (len(self.plate.rows()[0]), 1)).transpose().flatten().tolist()
            dict[compound] = out
            totVol += np.array(out)
        buffer_index = [i for i in range(len(self.compounds)) if isinstance(self.compounds[i], Buffer)][0]
        dict[self.compounds[buffer_index]] = np.round(self.workVol - totVol, 3).flatten().tolist()
        return dict


# Compound class

class Compound:

    def __init__(self, stock, label):
        self.stock = stock
        self.label = label


class Salt(Compound):

    def __str__(self):
        return self.label + ', Salt'

    def dilute(self, outputConc, wellVol):
        return outputConc * wellVol / self.stock


class Precipitant(Compound):

    def __str__(self):
        return self.label + ', Precipitant'

    def dilute(self, outputPerc, wellVol):
        return outputPerc * wellVol / self.stock


class Buffer(Compound):

    def __str__(self):
        return self.label + ', Buffer'

    def dilute(self, outputConc, wellVol):
        return wellVol