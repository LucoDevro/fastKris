with open('inputdata3.txt', 'r') as f:
    lines = f.read()
    lines = lines.split("\n\n")
f.close()

main = open("pythonInput.py", "r")

tips_raw = str(lines[0].split("\n"))
instr_raw = str(lines[1].split("\n"))
plates_raw = str(lines[2].split("\n"))
screens_raw = str(lines[3].split('\n')[:-1])

with open("main2.py", 'a') as main2:
    main2.write('from opentrons import protocol_api\n\n')
    main2.write('tips_raw =' + tips_raw + "\n")
    main2.write('instr_raw =' + instr_raw + "\n")
    main2.write('plates_raw =' + plates_raw + "\n")
    main2.write('screens_raw =' + screens_raw + "\n\n")
    main2.write(main.read())
    main2.close()
