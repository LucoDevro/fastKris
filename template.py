metadata = {
    'apiLevel': '2.9',
    'protocolName': 'Crystallization screen',
    'description': '''This protocol has been automatically generated using fastKris.
                      Manual modifications will be overwritten.''',
    'author': 'fastKris 1.0'
}

import warnings
import numpy as np

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
        
        # Calculating total liquid requirements
        total_vols = {c: round(sum(vols[c]), 3) for c in vols.keys()}
        print("This screen needs:")
        for c in total_vols.keys():
            print(str(c) + ":\t" + str(total_vols[c]) + " uL")

        # reorder the indexing of the wells so that wells are filled row by row
        well_order = np.array(range(len(screen.plate.rows()[0]) * len(screen.plate.columns()[0]))) \
            .reshape(len(screen.plate.rows()[0]), len(screen.plate.columns()[0])) \
            .transpose().flatten().tolist()
            
        for compound in vols.keys():
            print("Adding compound " + str(screen.compounds.index(compound)+1))
            
            # selecting the correct stock solution
            stock = screen.stocks[screen.compounds.index(compound)]
            stock_vol = stock.max_volume
            
            # after adding the last compound, the content will be mixed
            last = (compound == list(vols.keys())[-1])

            # fill the wells one by one
            for i in range(len(well_order)):     
                
                # volume for this compound in this well
                vol = vols[compound][i]
                
                # the well to prepare
                well = screen.plate.wells()[well_order[i]]
                
                # skip negative volumes with a warning
                if vol < 0:
                    warnings.warn('Negative diluent volume in ' + str(well) + ': Skipping for now...')
                    continue
                
                # picking the most appropiate pipette according to the volume to be pipetted
                if vol <= small_pipette.max_volume:
                    if vol >= small_pipette.min_volume:
                        instrument = small_pipette
                    else:
                        raise Exception("No suitable pipette attached for all volumes to be pipetted! Smallest pipette: " \
                                        + str(small_pipette.min_volume) + ' - ' + str(small_pipette.max_volume) + \
                                        " Biggest pipette: " + str(big_pipette.min_volume) + ' - ' + str(big_pipette.max_volume) \
                                        + " This volume: " + str(vol))
                elif vol <= big_pipette.max_volume:
                    if vol >= big_pipette.min_volume:
                        instrument = big_pipette
                    else:
                        raise Exception("No suitable pipette attached for all volumes to be pipetted! Smallest pipette: " \
                                        + str(small_pipette.min_volume) + ' - ' + str(small_pipette.max_volume) + \
                                        " Biggest pipette: " + str(big_pipette.min_volume) + ' - ' + str(big_pipette.max_volume) \
                                        + " This volume: " + str(vol))
                else:
                    raise Exception("No suitable pipette attached for all volumes to be pipetted! Smallest pipette: " \
                                    + str(small_pipette.min_volume) + ' - ' + str(small_pipette.max_volume) + \
                                    " Biggest pipette: " + str(big_pipette.min_volume) + ' - ' + str(big_pipette.max_volume) \
                                    + " This volume: " + str(vol))
                
                # Make sure a tip is attached
                if not(instrument.has_tip):
                    instrument.pick_up_tip()
                
                # Only when adding the last compound, put the tip in the liquid, mix and drop the tip
                if last:
                    instrument.transfer(vol, stock, well, new_tip = "never")
                    instrument.mix(repetitions = 3, volume = small_pipette.max_volume)
                    instrument.drop_tip()
                else:
                    # Transfer the volume and blow out, but avoid putting the tip into the liquid to reuse it for the other wells
                    # Adapt the instrument's aspiration well bottom clearance depending on the available stock volume. 
                    # ASSUMPTION: stock tubes initially are full. We'll take a large margin of 2.5 cm to anticipate it's not.
                    instrument.well_bottom_clearance.aspirate = max(stock_vol / stock.max_volume * stock.depth - 25, 1)
                    instrument.well_bottom_clearance.dispense = well.depth
                    instrument.transfer(vol, stock, well, new_tip = "never")
                    instrument.blow_out()
                    # Revert the instrument's well bottom clearances to the default values
                    instrument.well_bottom_clearance.aspirate = 1
                    instrument.well_bottom_clearance.dispense = 1
                    
                # substract the transferred volume from the stock volume
                stock_vol -= vol
                
                # log to stdout
                print("Transferred " + str(vol) + " uL of " + str(compound) + \
                      " from " + str(stock) + " into " + str(well) + " using " + str(instrument))
                
            # drop any remaining tips when ready with a compound
            if small_pipette.has_tip:
                small_pipette.drop_tip()
            if big_pipette.has_tip:
                big_pipette.drop_tip()
                
    print("DONE!\n\n\n")

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
    unknwLoc = [loc not in ['left', 'right'] for loc in instrumentLocation]
    if np.any(unknwLoc):
        raise Exception('Unknown pipet position: "' + str(instrumentLocation[unknwLoc.index(True)]) + '"')

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
    all_screen_stocks = screens_raw[2::6]
    all_screen_ranges = screens_raw[3::6]
    all_screen_plates = screens_raw[4::6]
    all_screen_workVol = screens_raw[5::6]
    numberOfScreens = len(all_screen_types)
    for s in range(numberOfScreens):

        # screen type (1D, 2D or 3D)
        screen_type = int(all_screen_types[s])
        if not(screen_type in set([1,2])):
            raise Exception('Unknown screen type!')
        
        # parse plate number and link the plate object to it
        screen_plate = int(all_screen_plates[s])
        try:
            screen_plate = protocol.loaded_labwares[screen_plate]
        except KeyError:
            raise Exception('Cannot load well plate. There is nothing assigned to slot ' + str(screen_plate) + '!')
        
        # well working volume
        screen_workVol = int(all_screen_workVol[s])
        if screen_workVol < 0:
            raise Exception('Working volumes cannot be negative!')
        if screen_workVol > screen_plate.wells()[0].max_volume:
            raise Exception('Working volume exceeds the well volume!')

        # compounds used in this particular screen
        screen_compounds_pre = all_screen_compounds[s].split(',')
        if len(screen_compounds_pre) != 4:
            raise Exception('A screen requires four compounds! Currently assigned: ' + str(len(screen_compounds_pre)))
        unknwComp = [c not in compoundLibrary.keys() for c in screen_compounds_pre]
        if np.any(unknwComp):
            raise Exception('Unknown compound: "' + str(screen_compounds_pre[unknwComp.index(True)]) + '"')
        screen_compounds = [compoundLibrary[i] for i in screen_compounds_pre]
        
        # stocks for each compound
        screen_stocks = []
        tubes_rackAndLocation = all_screen_stocks[s].split(',')
        for rl in tubes_rackAndLocation:
            rl_split = rl.split('/')
            try:
                r = protocol.loaded_labwares[int(rl_split[0])]
            except KeyError:
                raise Exception('Cannot find stock tube. There is nothing assigned to slot ' + rl_split[0] + '!')
            if "tuberack" not in r.name.lower():
                raise Exception('Stocks have to be in a tuberack! There is no tuberack assigned to slot ' + rl_split[0])
            l = rl_split[1]
            screen_stocks.append(r[l])

        # parsing compound concentration ranges and linking them to the associated compound
        screen_range_raw = all_screen_ranges[s].split(',')
        screen_range = {}
        for c in range(len(screen_range_raw)):
            raw_range = [float(i) for i in screen_range_raw[c].split('-')]
            srt_range = sorted(raw_range)
            if not(srt_range == raw_range):
                warnings.warn('Ranges are not given from low to high. Rearranging for now...')
            screen_range[screen_compounds[c]] = tuple(srt_range)

        # creating Screen objects from the parsed properties, depending on the screen type
        if screen_type == 1:
            screen = oneD(screen_range, screen_compounds, screen_plate, screen_workVol, screen_stocks)
        elif screen_type == 2:
            screen = twoD(screen_range, screen_compounds, screen_plate, screen_workVol, screen_stocks)
        else:
            raise Exception('Unknown screen type: "' + str(screen_type) + '"')
        screens.append(screen)

    return [tips, tuberacks, instruments, plates, screens]


def loadLibrary():
    compLibrary = {}
    if not(len(labels) == len(set(labels))):
        raise Exception("Duplicate compound labels detected! Please check your labels!")
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
            raise Exception("Compound type not understood: " + labels[i])

    return compLibrary


### Supporting classes ###
    
# Screen class

class Screen:

    def __init__(self, range, compounds, plate, workVol, stocks):
        self.range = range  # dictionary by compound that needs a range reported
        self.compounds = compounds  # a list
        self.workVol = workVol
        self.plate = plate
        self.stocks = stocks

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
            warnings.warn('Negative diluent volume detected! Please check your concentration ranges!')
        dict[self.compounds[diluent_index]] = diluent_vol.flatten().tolist()
        return dict

# Compound class

class Compound:

    def __init__(self, stock, label):
        self.stock = stock
        self.label = label


class Salt(Compound):

    def __str__(self):
        return self.label + ' (Salt)'

    def dilute(self, outputConc, wellVol):
        return outputConc * wellVol / self.stock


class Precipitant(Compound):

    def __str__(self):
        return self.label + ' (Precipitant)'

    def dilute(self, outputPerc, wellVol):
        return outputPerc * wellVol / self.stock


class Buffer(Compound):

    def __str__(self):
        return self.label + ' (Buffer)'

    def dilute(self, outputConc, wellVol):
        return outputConc * wellVol / self.stock

class Diluent(Compound):
    
    def __init__(self, label):
        self.stock = 0
        self.label = label
        
    def __str__(self):
        return self.label + ' (Diluent)'
    
