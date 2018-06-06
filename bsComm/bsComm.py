import ac, acsys, math, time, datetime, sys, os, platform, time, copy
if platform.architecture()[0] == "64bit":
  sysdir = "stdlib64"
else:
  sysdir = "stdlib"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "appLibs", sysdir))
os.environ['PATH'] = os.environ['PATH'] + ";."
from sim_info import info
from serialComm import aSerial

defValue=32767
class piece():
    def __init__(self, appWin, x=0, y=0):
        self.appWin=appWin
        self.lb=ac.addLabel(appWindow,"default")
        self.p=[0, 0]
        self.v=[70, 70]
        self.setPos(x, y)       
    def setPos(self, x, y):
        self.p[0] = x
        self.p[1] = y
        ac.setPosition(self.lb, self.p[0], self.p[1])
    def setText(self, txt):
        ac.setText(self.lb, txt)
    def move(self, x, y):
        self.p[0] += x
        self.p[1] += y
        ac.setPosition(self.lb, self.p[0], self.p[1])
    def tick(self, deltaT):
        self.move(self.v[0] * deltaT, self.v[1] * deltaT)
        if self.p[0] > 400 or self.p[0] < 0:
            self.v[0] *=-1
            self.move(self.v[0] * deltaT, self.v[1] * deltaT)

        if self.p[1] > 400 or self.p[1] < 0:
            self.v[1] *=-1
            self.move(self.v[0] * deltaT, self.v[1] * deltaT)
class iPLaceable:
    def __init__(self, appWin):
        self.appWin=appWin
        self.dt=None
        return
    def sPos(self, x, y):
        ac.setPosition(self.dt, x, y)
        return
    def sText(self, txt):
        ac.setText(self.dt, txt)
        return
class jLabel(iPLaceable):
    def __init__(self, appWin):
        iPLaceable.__init__(self, appWin)
        self.dt=ac.addLabel(appWindow,"label")
        pass
class jSpinner(iPLaceable):
    def __init__(self, appWin, name="spinn"):
        iPLaceable.__init__(self, appWin)
        self.dt=ac.addSpinner(appWindow, name)
        pass
    def sRange(self, rng1=0, rng2=100):
        ac.setRange(self.dt, rng1, rng2)
    def gValue(self):
        return ac.getValue(self.dt)
    def sValue(self, value):
        return ac.setValue(self.dt, value)
    def sStep(self, value):
        ac.setStep(self.dt, value)
class wrData():
    def __init__(self, appWin,name="", x=0, y=0, factor=8000, threshold=32767):
        self.p=[x, y]
        self.lbData=jLabel(appWin)
        self.spFilter=jSpinner(appWin, "filter")
        self.spfactor=jSpinner(appWin, "factor")
        
        self.lbData.sPos(self.p[0], self.p[1])
        self.spFilter.sPos(self.p[0], self.p[1]+50)
        self.spfactor.sPos(self.p[0] + 200, self.p[1]+50)


        self.name=name
        self.factor=factor
        self.rngFilter=threshold



        self.spFilter.sRange(0, 65534)
        self.spfactor.sRange(0, 65534)
        
        self.spFilter.sStep(500)
        self.spfactor.sStep(500)

        self.spFilter.sValue(self.rngFilter)
        self.spfactor.sValue(self.factor)        
        return
    def sThresholds(self):
        self.rngFilter=self.spFilter.gValue()
        self.factor=self.spfactor.gValue()
        return ""
    def calcProcedure(self, inData):
        inData = inData * self.factor
        inData = inData + self.rngFilter
        _str=self.name + ">>" + str(int(inData))
        self.lbData.sText(_str)
        return inData


####Global Vars####
appWindow=None
ser=aSerial()
names=["Sway", "Surge", "Pitch", "Roll"]

#values={"Sway":3500, "Surge":3500.0, "Pitch":27339.0, "Roll":27339.0}
#values={"Sway":9830.0, "Surge":13107.0, "Pitch":27339.0, "Roll":27339.0}
values={"Sway":9830.0, "Surge":13107.0, "Pitch":27339.0, "Roll":16383.0}
pieces=[]
compData=[]
##################

def acMain(ac_version):
    global appWindow, ser, compData
    appWindow=ac.newApp("joeStuff")
    ac.setSize(appWindow,400,400)
    ac.console("addonLoad----OK")    
    ac.console("serialConn---"+str(ser.connect()))
    
    for x in range(0, 4):
        ac.console(names[x]+ " "+ str(values[names[x]]))
        nData = wrData(appWindow,names[x], 0, (x *100) + 40, values[names[x]])
        compData.append(nData)
    ser.sendData([32767, 32767, 32767, 32767, 32767, 32767])
    return "bsComm"


it=0
integ=[defValue, defValue, defValue, defValue]
def acUpdate(deltaT):
    global appWindow, ser, values, pieces, compData, it, integ

    values["Sway"] =(info.physics.accG[0] / 3)
    values["Surge"] =(info.physics.accG[2]/ -3)
    values["Pitch"] =((info.physics.pitch * -(180/math.pi))/10)
    values["Roll"] =(info.physics.roll* -(180/math.pi)/10)
    
    for x in range(0, 4):
        compData[x].sThresholds()
        values[names[x]] = compData[x].calcProcedure(values[names[x]])
        integ[x]=(integ[x]+values[names[x]])/2

    ac.console(str(info.physics.accG[2]*-1000))
    ser.sendData([integ[0], 32767, integ[1], integ[2], integ[3], 32767])
    #if it >= 5:
    #    ser.sendData([integ[0], 32767, integ[1], integ[2], integ[3], 32767])
    #    it = 0
    #else:
    #    it = it + 1
    for x in pieces:
        x.tick(deltaT)