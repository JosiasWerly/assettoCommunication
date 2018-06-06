# roll 
# pitch
# heave
# yaw  
# sway 
# surge

#st
# <Axis1a> sway
# <Axis2a> heave
# <Axis3a> surge
# <Axis4a> pitch
# <Axis5a> rool
# <Axis6a> yaw
#57600
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
        self.spfactor.sRange(0, 20000)
        
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
