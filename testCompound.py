from Compound import *

def main():
    NaCl=Salt(1, 'NaCl, 1M')
    EDTA=Precipitate(10, 'EDTA, 10%')
    AceBuffer=Buffer(7, 'Acetate buffer, pH 7')
    
    # Testing getters
    print(NaCl.getStock())
    print(NaCl.getLabel())
    print(EDTA.getStock())
    print(EDTA.getLabel())
    print(AceBuffer.getStock())
    print(AceBuffer.getLabel())
    
    # Testing diluters
    print(NaCl.dilute(0.1,100)) #10
    print(EDTA.dilute(1,100)) #10
    
main()