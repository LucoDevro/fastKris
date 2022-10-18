from opentrons import protocol_api

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

with open('inputdata.txt') as f:
    lines = f.read()
    lines = lines.split("\n")

tipsinput = str(lines[0])
reservoirinput = str(lines[2])
plateinput = str(lines[4])
instrumentinput = str(lines[6])

tipslocation = int(lines[1])
reservoirlocation = int(lines[3])
platelocation = int(lines[5])

def run(protocol: protocol_api.ProtocolContext):

    tips = protocol.load_labware(tipsinput, tipslocation)
    reservoir = protocol.load_labware(reservoirinput, reservoirlocation)
    plate = protocol.load_labware(plateinput, platelocation)
    p300 = protocol.load_instrument(instrumentinput, 'left', tip_racks=[tips])
    p300.transfer(100, reservoir['A1'], plate.wells())

    for i in range(8):
        row = plate.rows()[i]
        p300.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))
        p300.transfer(100, row[:11], row[1:], mix_after=(3, 50))
