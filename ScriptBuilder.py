# Reading parameter file
with open('inputdata3.txt', 'r') as f:
    lines = f.read()
    lines = lines.split("\n\n")
    f.close()

tips_raw = str(lines[0].split("\n"))
tuberack_raw = str(lines[1].split("\n"))
instr_raw = str(lines[2].split("\n"))
plates_raw = str(lines[3].split("\n"))
screens_raw = str(lines[4].split('\n')[:-1])

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
with open("main.py", 'w') as main:
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
    