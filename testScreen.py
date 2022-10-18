from Screen import *
import numpy as np
#class Plate defined here only for testing
class Plate():
    def __init__(self, maxVol,nrows,ncols):
        self.max_volume = maxVol
        self.wlls = [0]*(nrows*ncols)
        self.rws = np.array([0]*24).reshape(nrows,ncols).tolist()
        self.cls = np.array([0]*24).reshape(ncols,nrows).tolist()
    def columns(self):
        return self.cls
    def rows(self):
        return self.rws
    def wells(self):
        return self.wlls

def main():
    NaCl=Salt(1, 'NaCl, 1M')
    EDTA=Precipitate(10, 'EDTA, 10%')
    AceBuffer=Buffer(7, 'Acetate buffer, pH 7')
    compounds = [NaCl,AceBuffer,EDTA]
    range1 = {NaCl:(0.1,0.33)}
    range2 = {NaCl:(0.1,0.3), EDTA:(0.28,0.4)}
    plate = Plate(100,4,6)

    screen1 = oneD([0],range1,compounds,plate)
    screen2 = twoD([0,2],range2,compounds,plate)
    screen3 = threeD(range2,compounds,plate)

    #test
    assert len(screen1.plate.rows()) == 4
    assert len(screen1.plate.rows()[0]) == 6
    #test length + value
    out1 = screen1.getAllVol()
    assert len(out1.get(NaCl)) == 24
    assert out1.get(NaCl)[3] == NaCl.dilute(0.13,100)

    out2 = screen2.getAllVol()
    assert len(out2.get(NaCl)) == 6
    assert len(out2.get(EDTA)) == 4
    assert out2.get(NaCl)[1] == NaCl.dilute(0.14, 100)
    #bc 3.6000000000000005  vs  3.6
    assert round(out2.get(EDTA)[2],5) == round(EDTA.dilute(0.36,100),5)

    out3 = screen3.getAllVol()
    assert len(out3.get(NaCl)) == 6
    assert len(out3.get(EDTA)) == 4
    assert out2.get(NaCl)[1] == NaCl.dilute(0.14, 100)
    # bc 3.6000000000000005  vs  3.6
    assert round(out2.get(EDTA)[2],14) == round(EDTA.dilute(0.36, 100),14)

main()