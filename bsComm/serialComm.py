import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dll"))
import serial
class aSerial():
    def __init__(self):
        self.srComm=None
        self.cfgs=None
    def connect(self, port="COM1", bdRate=57600):
        if self.srComm != None:
            self.srComm.close()        
        self.srComm = serial.Serial(port, bdRate, timeout=0);
        return self.srComm.isOpen()
    def loadConfig(self):
        # with open('data.json', 'r') as fp:
        #     self.cfgs = json.load(fp)
        #     print("loaded->", self.cfgs)
        pass
    def int2Byte(self, value):
        p1 = int(value/256)
        p2 = int(value - (p1 * 256))
        return bytes((p1, p2))
    def sendData(self, arrAxis):     
        stgB = bytes((115, 116))
        for x in arrAxis:
            stgB += self.int2Byte(x)
        self.srComm.write(stgB)
        return stgB


if __name__ == "__main__":
    aSer = aSerial()
    
    aSer.loadConfig()
    print(aSer.connect())
    while True:
        aSer.sendData([int(input()), 32767, 32767, 32767, 32767, 32767])
    # values = {
    #         "dof": {
    #             "pitch":100,
    #             "roll":100,
    #             "yaw":100,
    #             "surge":100,
    #             "heave":100,
    #             "sway":100
    #         }
    #     }
    # with open('data.json', 'w') as fp:
    #     json.dump(values, fp, indent=4)
    # with open('data.json', 'r') as fp:
    #     data = json.load(fp)
    #     input(data)