metadata = {
    'apiLevel': '2.9',
    'protocolName': 'Crystallization screen',
    'description': '''This protocol has been automatically generated using fastKris.
                      Manual modifications will be overwritten when fastKris would run again.''',
    'author': 'LBMD'
}

import warnings

def run(protocol: protocol_api.ProtocolContext):
    global compoundLibrary
    compoundLibrary = loadLibrary()
    print('Compound library loaded...')
    [tips, tuberacks, instruments, plates, screens] = setup(protocol)
    pipette_capacities = [inst.max_volume for inst in instruments]
    small_pipette = instruments[pipette_capacities.index(min(pipette_capacities))]
    big_pipette = instruments[pipette_capacities.index(max(pipette_capacities))]
    print('Screens parsed...')

    for screen in screens:
        print("Executing Screen " + str(screens.index(screen)+1))
        vols = screen.getAllVol()

        # reorder the indexing of the wells so that wells are filled row by row
        well_order = np.array(range(len(screen.plate.rows()[0]) * len(screen.plate.columns()[0]))) \
            .reshape(len(screen.plate.rows()[0]), len(screen.plate.columns()[0])) \
            .transpose().flatten().tolist()
        for compound in vols.keys():

            print("Adding compound " + str(screen.compounds.index(compound)+1))
            
            # selecting the correct stock solution
            stock = screen.reservoirs[screen.compounds.index(compound)]
                
            # first compound can be done with the same tip so check for it
            first = (compound == list(vols.keys())[0])
            
            # after adding the last compound, the content will be mixed
            last = (compound == list(vols.keys())[-1])

            # fill the wells one by one
            for i in range(len(well_order)):               
                vol = vols[compound][i]
                
                # skip negative volumes with giving a warning
                if vol < 0:
                    warnings.warn('Negative diluent volume detected! Please check your concentration ranges! Skipping for now...')
                    continue
                
                # picking the most appropiate pipette according to the volume to be pipetted
                if vol <= small_pipette.max_volume:
                    if vol >= small_pipette.min_volume:
                        instrument = small_pipette
                    else:
                        raise Exception('No suitable pipette attached!')
                elif vol <= big_pipette.max_volume:
                    if vol >= big_pipette.min_volume:
                        instrument = big_pipette
                    else:
                        raise Exception('No suitable pipette attached!')
                else:
                    raise Exception('No suitable pipette attached!')
                    
                # Make sure the pipette is attached to a tip
                if not(instrument.has_tip):
                    instrument.pick_up_tip()
                
                # transfer the volume
                instrument.transfer(vol, stock, screen.plate.wells()[well_order[i]], new_tip = "never", trash = True)
                
                if last:
                    instrument.mix(repetitions = 3, volume = 300)
                
                # only keep the tip attached if the first compound is transferred to avoid contamination
                if (not(first) or i == len(well_order)-1):
                    instrument.blow_out()
                    instrument.drop_tip()
                    
                # log to stdout
                print("Transferring " + str(vol) + " uL of " + str(compound) + \
                      " from " + str(stock) + " into " + str(screen.plate.wells()[well_order[i]]) + \
                      " using " + str(instrument))
                
    print("Done!\n\n\n")
    print("Output of the OpenTrons API:")


def setup(protocol):
    # parsing pipet tips
    tipsInput = tips_raw[0::3]
    tipsLocation = tips_raw[1::3]
    tipsPipette = tips_raw[2::3]

    # loading pipet tips
    tips = [protocol.load_labware(tipsInput[i], tipsLocation[i]) for i in range(len(tipsInput))]

    # parsing tube racks
    tuberacksInput = tuberack_raw[0::2]
    tuberacksLocation = tuberack_raw[1::2]
    
    # loading tube racks
    tuberacks = [protocol.load_labware(tuberacksInput[i], tuberacksLocation[i]) for i in range(len(tuberacksInput))]

    # parsing pipetting instruments
    instrumentInput = instr_raw[0::2]
    instrumentLocation = instr_raw[1::2]

    # loading pipetting instruments and their associated tip racks
    tips_by_instr = {}
    tips_by_instr["left"] = [tips[i] for i in range(len(tips)) if tipsPipette[i].lower() == "left"]
    tips_by_instr["right"] = [tips[i] for i in range(len(tips)) if tipsPipette[i].lower() == "right"]
    instruments = [protocol.load_instrument(instrumentInput[i], instrumentLocation[i],
                    tip_racks=tips_by_instr[instrumentLocation[i].lower()]) for i in range(len(instrumentInput))]

    # parsing plates
    platesInput = plates_raw[0::2]
    platesLocation = plates_raw[1::2]

    # loading plates
    plates = [protocol.load_labware(platesInput[i], platesLocation[i]) for i in range(len(platesInput))]

    # parsing screens
    screens = []
    all_screen_types = screens_raw[0::6]
    all_screen_compounds = screens_raw[1::6]
    all_screen_reservoirs = screens_raw[2::6]
    all_screen_ranges = screens_raw[3::6]
    all_screen_plates = screens_raw[4::6]
    all_screen_workVol = screens_raw[5::6]
    numberOfScreens = len(all_screen_types)
    for s in range(numberOfScreens):

        # screen type (1D, 2D or 3D)
        screen_type = int(all_screen_types[s])
        if not(screen_type in set([1,2,3])):
            raise Exception('Unknown screen type!')
        
        # parse plate number and link the plate object to it
        screen_plate = int(all_screen_plates[s])
        screen_plate = protocol.loaded_labwares[screen_plate]
        
        # well working volume
        screen_workVol = int(all_screen_workVol[s])
        if screen_workVol < 0:
            raise Exception('Working volumes cannot be negative!')
        if screen_workVol > screen_plate.wells()[0].max_volume:
            raise Exception('Working volume exceeds the well volume!')

        # compounds used in this particular screen
        screen_compounds = [compoundLibrary[i] for i in all_screen_compounds[s].split(',')]
        
        # reservoirs for each compound
        screen_reservoirs = []
        tubes_rackAndLocation = all_screen_reservoirs[s].split(',')
        for rl in tubes_rackAndLocation:
            rl_split = rl.split('/')
            r = protocol.loaded_labwares[int(rl_split[0])]
            l = rl_split[1]
            screen_reservoirs.append(r[l])

        # parsing compound concentration ranges and linking them to the associated compound
        screen_range_raw = all_screen_ranges[s].split(',')
        screen_range = {}
        for c in range(len(screen_range_raw)):
            raw_range = [float(i) for i in screen_range_raw[c].split('-')]
            srt_range = sorted(raw_range)
            if not(srt_range == raw_range):
                warnings.warn('Ranges were not given from low to high. Rearranging the values for now...')
            screen_range[screen_compounds[c]] = tuple(srt_range)

        # creating Screen objects from the parsed properties, depending on the screen type
        if screen_type == 1:
            screen = oneD(screen_range, screen_compounds, screen_plate, screen_workVol, screen_reservoirs)
        elif screen_type == 2:
            screen = twoD(screen_range, screen_compounds, screen_plate, screen_workVol, screen_reservoirs)
        elif screen_type == 3:
            screen = threeD(screen_range, screen_compounds, screen_plate, screen_workVol, screen_reservoirs)
        else:
            raise Exception('Unknown screen type.')
        screens.append(screen)

    return [tips, tuberacks, instruments, plates, screens]


def loadLibrary():
    compLibrary = {}
    if not(len(labels) == len(set(labels))):
        raise Exception("Duplicate labels detected! Please check your labelling!")
    for i in range(len(labels)):
        if types[i].lower() == "salt":
            compLibrary[labels[i]] = Salt(float(stockConc[i]), labels[i])
        elif types[i].lower() == "precipitant":
            compLibrary[labels[i]] = Precipitant(float(stockConc[i]), labels[i])
        elif types[i].lower() == "buffer":
            compLibrary[labels[i]] = Buffer(float(stockConc[i]), labels[i])
        elif types[i].lower() == "diluent":
            compLibrary[labels[i]] = Diluent(labels[i])
        else:
            raise Exception("Compound type not understood!")

    return compLibrary


### Supporting classes ###
# Provisionary defined here as the OpenTrons simulation protocol bundle does not find the separate class files

# Screen class

# from Compound import *
import numpy as np


class Screen:

    def __init__(self, range, compounds, plate, workVol, reservoirs):
        self.range = range  # dictionary by compound that needs a range reported
        self.compounds = compounds  # a list
        self.workVol = workVol
        self.plate = plate
        self.reservoirs = reservoirs

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
            if isinstance(compound, Diluent):
                diluent_index = self.compounds.index(compound)
                continue
            outConc = self.getOutConc(compound)
            out = self.calcConcentration(compound, outConc)
            dict[compound] = out
            totVol += np.array(out)
        diluent_vol = np.round(self.workVol - totVol, 3)
        if np.any(diluent_vol < 0):
            warnings.warn('Negative diluent volume detected! Please check your concentration ranges!')
        dict[self.compounds[diluent_index]] = diluent_vol.flatten().tolist()
        return dict


class twoD(Screen):

    def __str__(self):
        return '2D screen, ' + str(self.range) + str(self.compounds) + ' on plate ' + str(self.plate) + ' (' + str(
            self.workVol) + ' uL)'

    def getOutConc(self, compound, dimension):
        if dimension == 'h':
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.rows()[0])).tolist()
        elif dimension == 'v':
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.columns()[0])).tolist()
        elif dimension == 'a':
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.wells())).tolist()

    def getAllVol(self):
        dict = {}
        totVol = np.zeros(len(self.plate.rows()[0]) * len(self.plate.columns()[0]))
        dimensions = ['h', 'v', 'a']
        for compound in self.compounds:
            if isinstance(compound, Diluent):
                diluent_index = self.compounds.index(compound)
                continue
            dimension = dimensions[self.compounds.index(compound)]
            outConc = self.getOutConc(compound, dimension)
            out = self.calcConcentration(compound, outConc)
            if dimension == 'h':
                out = np.tile(np.array(out), (len(self.plate.columns()[0]), 1)).flatten().tolist()
            elif dimension == 'v':
                out = np.tile(np.array(out), (len(self.plate.rows()[0]), 1)).transpose().flatten().tolist()
            dict[compound] = out
            totVol += np.array(out)
        diluent_vol = np.round(self.workVol - totVol, 3)
        if np.any(diluent_vol < 0):
            raise Exception('Negative diluent volume detected! Please check your concentration ranges!')
        dict[self.compounds[diluent_index]] = diluent_vol.flatten().tolist()
        return dict
    
# identical to twoD at the moment
class threeD(Screen):

    def __str__(self):
        return '3D screen, ' + str(self.range) + str(self.compounds) + ' on plate ' + str(self.plate) + ' (' + str(
            self.workVol) + ' uL)'

    def getOutConc(self, compound, dimension):
        if dimension == 'h':
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.rows()[0])).tolist()
        elif dimension == 'v':
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.columns()[0])).tolist()
        elif dimension == 'a':
            return np.linspace(start=self.range[compound][0], stop=self.range[compound][1],
                               num=len(self.plate.wells())).tolist()

    def getAllVol(self):
        dict = {}
        totVol = np.zeros(len(self.plate.rows()[0]) * len(self.plate.columns()[0]))
        dimensions = ['h', 'v', 'a']
        for compound in self.compounds:
            if isinstance(compound, Diluent):
                diluent_index = self.compounds.index(compound)
                continue
            dimension = dimensions[self.compounds.index(compound)]
            outConc = self.getOutConc(compound, dimension)
            out = self.calcConcentration(compound, outConc)
            if dimension == 'h':
                out = np.tile(np.array(out), (len(self.plate.columns()[0]), 1)).flatten().tolist()
            elif dimension == 'v':
                out = np.tile(np.array(out), (len(self.plate.rows()[0]), 1)).transpose().flatten().tolist()
            dict[compound] = out
            totVol += np.array(out)
        diluent_vol = np.round(self.workVol - totVol, 3)
        if np.any(diluent_vol < 0):
            raise Exception('Negative diluent volume detected! Please check your concentration ranges!')
        dict[self.compounds[diluent_index]] = diluent_vol.flatten().tolist()
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
        return outputConc * wellVol / self.stock

class Diluent(Compound):
    
    def __init__(self, label):
        self.stock = 0
        self.label = label
        
    def __str__(self):
        return self.label + ', Diluent'
    
