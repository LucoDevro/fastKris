import sys

# Python function
def runScriptBuilder(filename, protocolFilePath):
    # Reading parameter file
    with open(filename, 'r') as f:
        lines = f.read()
        lines = lines.split("\n\n")
        f.close()

    tips_raw = str(lines[0].split("\n"))
    tuberack_raw = str(lines[1].split("\n"))
    instr_raw = str(lines[2].split("\n"))
    plates_raw = str(lines[3].split("\n"))
    if 'win' not in sys.platform:
        screens_raw = str(lines[4].split('\n')[:-1])
    else:
        screens_raw = str(lines[4].split('\n'))
    
    # Reading compound library
    with open('compLibrary.txt', 'r') as l:
        lines = l.read()
        lines = lines.split("\n")[:-1]
        l.close()

    labels = str(lines[0::3])
    types = str(lines[1::3])
    stockConc = str(lines[2::3])

    # Writing the script from the template
    template = open("template.py", "r")

    with open(protocolFilePath, 'w') as main:
        main.write('from opentrons import protocol_api\n\n')
        main.write('tips_raw = ' + tips_raw + "\n")
        main.write('tuberack_raw = ' + tuberack_raw + "\n")
        main.write('instr_raw = ' + instr_raw + "\n")
        main.write('plates_raw = ' + plates_raw + "\n")
        main.write('screens_raw = ' + screens_raw + "\n\n")
        main.write('labels = ' + labels + '\n')
        main.write('types = ' + types + '\n')
        main.write('stockConc = ' + stockConc + '\n\n')
        main.write(template.read())
        template.close()
        main.close()
        
# bash command-line support
if __name__ == "__main__":
    # calling without arguments triggers default file paths
    if len(sys.argv) == 1:
        filename = "params.txt"
        protocolpath = "protocol.py"
    elif len(sys.argv) == 3:
        filename = sys.argv[1]
        protocolpath = sys.argv[2]
    else:
        raise Exception("Wrong number of arguments! Expected a file path and a protocol path.")
        
    runScriptBuilder(filename, protocolpath)
    