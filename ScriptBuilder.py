import sys

# Python function
def runScriptBuilder(filename, protocolFilePath):
    # Reading parameter file
    with open(filename, 'r') as f:
        lines = f.read()
        lines = lines.split("\n\n")

    tips_raw = str(lines[0].split("\n"))
    tuberack_raw = str(lines[1].split("\n"))
    instr_raw = str(lines[2].split("\n"))
    plates_raw = str(lines[3].split("\n"))
    screens_raw = lines[4].split('\n')
    if screens_raw[-1] == '':
        screens_raw = str(screens_raw[:-1])
    else:
        screens_raw = str(screens_raw)
    
    # Reading compound library
    with open('compLibrary.txt', 'r') as l:
        lines = l.read()
        lines = lines.split("\n")[:-1]

    labels = str(lines[0::3])
    types = str(lines[1::3])
    stockConc = str(lines[2::3])

    # Writing the script from the template
    template = open("template.py", "r")

    with open(protocolFilePath, 'w') as main:
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
        raise Exception("Wrong number of arguments! Expected a parameter file path and a protocol file path.")
        
    runScriptBuilder(filename, protocolpath)