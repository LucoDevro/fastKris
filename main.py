from opentrons import protocol_api
from Screen import *

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
    [tips, instruments, plates, screens]=setup(protocol)
    
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 8)
    instruments[0].transfer(100, reservoir['A1'], plates[0].wells())

    for i in range(8):
        row = plates[0].rows()[i]
        instruments[0].transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))
        instruments[0].transfer(100, row[:11], row[1:], mix_after=(3, 50))
        
def setup(protocol):
    with open('inputdata2.txt') as f:
        lines = f.read()
        lines = lines.split("\n\n")
    
    # parsing pipet tips
    tips_raw=lines[0].split("\n")
    tipsInput=tips_raw[0::2]
    tipsLocation=tips_raw[1::2]
    
    # loading pipet tips
    tips=[protocol.load_labware(tipsInput[i], tipsLocation[i]) for i in range(len(tipsInput))]
        
    # parsing pipetting instruments
    instr_raw=lines[1].split("\n")
    instrumentInput=instr_raw[0::2]
    instrumentLocation=instr_raw[1::2]
    
    # loading pipetting instruments
    instruments=[protocol.load_instrument(instrumentInput[i], instrumentLocation[i], tip_racks=[tips[i]]) for i in range(len(instrumentInput))]
    
    # parsing plates
    plates_raw=lines[2].split("\n")
    platesInput=plates_raw[0::2]
    platesLocation=plates_raw[1::2]
    
    # loading plates
    plates=[protocol.load_labware(platesInput[i], platesLocation[i]) for i in range(len(platesInput))]
        
    # parsing screens
    screens_raw=lines[3].split('\n')[:-1]
    screens=[]
    all_screen_types=screens_raw[0::4]
    all_screen_compounds=screens_raw[1::4]
    all_screen_ranges=screens_raw[2::4]
    all_screen_plates=screens_raw[3::4]
    for s in range(len(all_screen_types)):
        screen_type=int(all_screen_types[s])
        screen_plate=all_screen_plates[s]
        screen_compounds=all_screen_compounds[s].split(',')
        screen_range_raw=all_screen_ranges[s].split(',')
        screen_range={}
        for c in range(len(screen_compounds)):
            screen_range[screen_compounds[c]]=tuple([float(i) for i in screen_range_raw[c].split('-')])
        if screen_type==1:
            screen=OneD(screen_range, screen_compounds, screen_plate)
        elif screen_type==2:
            screen=TwoD(screen_range, screen_compounds, screen_plate)
        elif screen_type==3:
            screen=ThreeD(screen_range, screen_compounds, screen_plate)
        else:
            raise Exception('Unknown screen type.')
        screens.append(screen)
    
    return [tips, instruments, plates, screens]