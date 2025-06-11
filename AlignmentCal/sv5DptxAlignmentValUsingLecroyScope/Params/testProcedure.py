# SVT Test
# SVT version 25.1.rc1
# Test saved 2025-03-06_1107
# Form factor: SV5C_4L8G_MIPI_DPHY_GENERATOR
# PY3
# Checksum: 68dd9484336566f1c92cbf5a8f423fa7
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


autoscaleScope = _create('autoscaleScope', 'SvtFunction', iespName=None)
calOptions = _create('calOptions', 'SvtDataRecord', iespName=None)
initScope = _create('initScope', 'SvtFunction', iespName=None)
measureDeltaTime = _create('measureDeltaTime', 'SvtFunction', iespName=None)
performScopeCal = _create('performScopeCal', 'SvtFunction', iespName=None)
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName=None)
writeCalFileTemp = _create('writeCalFileTemp', 'SvtFunction', iespName=None)

dphyParams1 = _create('dphyParams1', 'SvtMipiDphyParameters')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiGenerator1 = _create('mipiGenerator1', 'SvtMipiDphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

autoscaleScope.args = ''
autoscaleScope.code = r'''# Set to center by going to default
osci.write(":SYSTem:PRESet DEFault")
sleepMillis(calOptions.scopeAutoScaleDelay)

# Make sure all skew are at 0. This is not reset by default
osci.write(":CALibrate:SKEW CHANnel1,0")
osci.write(":CALibrate:SKEW CHANnel2,0")
osci.write(":CALibrate:SKEW CHANnel3,0")

# Display the channels
osci.write(":CHANnel1:DISPlay 1")
osci.write(":CHANnel2:DISPlay 1")
osci.write(":CHANnel3:DISPlay 1")

# Autoscale the channels
osci.write(":AUToscale:VERTical CHANnel1")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel2")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel3")
sleepMillis(calOptions.scopeAutoScaleDelay)
# Clear display
osci.write(":CDISplay")

# Make sure we're getting mean values
osci.write(":MEASure:STATistics MEAN")


# Measure average voltage of channel 1 to set trigger level
osci.write(":MEASure:VAVerage DISPlay,CHANnel1")
sleepMillis(calOptions.scopeAutoScaleDelay)
varAverage = osci.query_ascii_values(":MEASure:VAVerage? DISPlay,CHANnel1")
currentValue = varAverage[0]

triggerValue = currentValue

# Set trigger level to be just below the mid-point of the 3-level waveform
myString = ":TRIGger:LEVel CHANNEL1, %f" % triggerValue
osci.write(myString)

# Clear display
osci.write(":CDISplay")
sleepMillis(100)

# Set timebase to proper value
osci.write(":TIMebase:SCALe 100e-012")
osci.write(":TRIGger:EDGE:SLOPe RISIng")
# Turn averaging on
osci.write(":ACQuire:AVERage:COUNt 16")
osci.write(":ACQuire:AVERage 1")

# Define delta-time measurement parameters
osci.write(":MEASure:DELTatime:DEFine RISing,1,MIDDle,RISing,1,MIDDle")
'''
autoscaleScope.wantAllVarsGlobal = False

calOptions.addField('serialNumber', descrip='''Serial number of device under test.''', attrType=str, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', defaultVal=2000.0, displayOrder=(0, 3.0))
calOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function.''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', defaultVal=2000.0, displayOrder=(0, 4.0))
calOptions.addField('numAverages', descrip='''Number of times the measurement is querried from the scope.''', attrType=int, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', defaultVal=100, displayOrder=(0, 5.0))
calOptions.addField('calLanes', descrip='''Range of channels to measure.''', attrType=list, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 6.0))
calOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', attrSubType=float, defaultVal=[3375.0, 4125.0, 5125.0, 6125.0], displayOrder=(0, 7.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.serialNumber = '1234'
calOptions.scopeIPAddress = 'TCPIP0::10.30.30.155::inst0::INSTR'
calOptions.scopeMeasurementDelay = 2000.0
calOptions.scopeAutoScaleDelay = 2000.0
calOptions.numAverages = 100
calOptions.calLanes = [1, 2, 3, 4, 5]
calOptions.calRates = [3375.0, 4125.0, 5125.0, 6000.0, 6125.0]
calOptions.callCustomInitMethod()
initScope.args = 'scopeIpAddress'
initScope.code = r'''import pyvisa
#connect to scope
rm = pyvisa.ResourceManager()
osci = rm.open_resource(scopeIpAddress)
#osci.lock_excl()
# Set to center by going to default
osci.write(":SYSTem:PRESet DEFault")
sleepMillis(calOptions.scopeAutoScaleDelay)

# Display/Enable the channels
osci.write(":CHANnel1:DISPlay 1")
osci.write(":CHANnel2:DISPlay 1")
osci.write(":CHANnel3:DISPlay 1")
osci.timeout = 10000

return osci
'''
initScope.wantAllVarsGlobal = False

measureDeltaTime.args = 'channel'
measureDeltaTime.code = r'''# Assumes all measurements are relative to channel 1
channelString = "CHANNEL%d" % channel
commandString = ":MEASure:DELTatime CHANnel1,"+channelString
osci.write(commandString)

sleepMillis(calOptions.scopeAutoScaleDelay)

currentDeltaTime = 0
commandString = ":MEASure:DELTatime? CHANnel1,"+channelString
for i in range(calOptions.numAverages) :
    varAmp = osci.query_ascii_values(commandString)
    currentDeltaTime += varAmp[0]
currentDeltaTime = currentDeltaTime / calOptions.numAverages

return currentDeltaTime
'''
measureDeltaTime.wantAllVarsGlobal = False

performScopeCal.args = 'lane,wire,position,  dataRate'
performScopeCal.code = r'''print("Performing coarse loop...")
coarseDelay = measureDeltaTime(position)
print("delay is %g..." % coarseDelay)


return coarseDelay
'''
performScopeCal.wantAllVarsGlobal = False

writeCalFile.args = 'measuredCoarseDelayDict, failCoarseDelayDict'
writeCalFile.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "valReport_"+calOptions.serialNumber
folderPath = resultFolderCreator1.run()
FilePathString = "valReport_"+calOptions.serialNumber+".txt"
filePath = os.path.join(folderPath, FilePathString)
wires = ['P', 'N']
##: Create file and while loop to fill it up
with open(filePath, "w") as outFile:
    for rate in calOptions.calRates:
        print("#Data Rate = %f" % rate, file=outFile)
        print("#Tx Skew Coarse", file=outFile)
        for lane in [5,1, 2, 3, 4]:
            for wire in [0,1]:
                print("%d  %s," %(lane,wires[wire]), end=' ', file=outFile)
        print("", file=outFile)
        for lane in [5,1, 2, 3, 4]:
            for wire in [0,1]:
                print("%g," % measuredCoarseDelayDict[lane][rate][wire], end=' ', file=outFile)
        print("", file=outFile)
        for lane in [5,1, 2, 3, 4]:
            for wire in [0,1]:
                print("%g," % failCoarseDelayDict[lane][rate][wire], end=' ', file=outFile)
        print("", file=outFile)
'''
writeCalFile.wantAllVarsGlobal = False

writeCalFileTemp.args = 'measuredCoarseDelayDict, failCoarseDelayDict'
writeCalFileTemp.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "valReportTemp_"+calOptions.serialNumber
folderPath = resultFolderCreator1.run()
FilePathString = "valReportTemp_"+calOptions.serialNumber+".txt"
filePath = os.path.join(folderPath, FilePathString)
wires = ['A', 'B', 'C']

##: Create file and while loop to fill it up
with open(filePath, "w") as outFile:
    for rate in calOptions.calRates:
        print("#Data Rate = %f" % rate, file=outFile)
        print("#Tx Skew Coarse", file=outFile)
        for lane in [5,1, 2, 3, 4]:
            for wire in [0,1]:
                print("%d  %s," %(lane,wires[wire]), end=' ', file=outFile)
        print("", file=outFile)
        for lane in [5,1, 2, 3, 4]:
            for wire in [0,1]:
                print("%g," % measuredCoarseDelayDict[lane][rate][wire], end=' ', file=outFile)
        print("", file=outFile)
        for lane in [5,1, 2, 3, 4]:
            for wire in [0,1]:
                print("%g," % failCoarseDelayDict[lane][rate][wire], end=' ', file=outFile)
        print("", file=outFile)
'''
writeCalFileTemp.wantAllVarsGlobal = False


dphyParams1.clockTrailBits = ''
dphyParams1.clockZeroBits = '0000'
dphyParams1.hsTrailBits = ''
dphyParams1.hsZeroBits = '0000'
dphyParams1.sotBits = '00011101'
dphyParams1.tAlpClk01Duration = (0.0, 20.0)
dphyParams1.tAlpClk10Duration = (0.0, 40.0)
dphyParams1.tAlpHs01Duration = (0.0, 20.0)
dphyParams1.tAlpHs10Duration = (0.0, 40.0)
dphyParams1.tAlpxDuration = 120.0
dphyParams1.tClockLpx01Duration = (0.0, 80.0)
dphyParams1.tClockPostDuration = (60.0, 60.0)
dphyParams1.tClockPreDuration = (32.0, 0.0)
dphyParams1.tClockPrepareDuration = (0.0, 80.0)
dphyParams1.tClockTrailDuration = (0.0, 80.0)
dphyParams1.tClockZeroDuration = (0.0, 300.0)
dphyParams1.tHsExitDuration = 240.0
dphyParams1.tHsIdleClkHs0Duration = (0.0, 60.0)
dphyParams1.tHsIdlePostDuration = 8
dphyParams1.tHsIdlePreDuration = 8
dphyParams1.tHsLpx01Duration = (0.0, 80.0)
dphyParams1.tHsPrepareDuration = (5.0, 60.0)
dphyParams1.tHsTrailDuration = (8.0, 60.0)
dphyParams1.tHsZeroDuration = (10.0, 145.0)
dphyParams1.tPreamble = 32
dphyParams1.tTaGetDuration = 5
dphyParams1.tTaGoDuration = 4.0
dphyParams1.tTaSureDuration = 1.0
dphyParams1.tlpxDuration = 80.0
dphyParams1.useAlp = False
dphyParams1.usePreambleSequence = False

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 5000.0
mipiClockConfig1.referenceClocks = None
mipiClockConfig1.sscEnabled = False
mipiClockConfig1.sscFrequency = 50.0
mipiClockConfig1.sscSpread = 1.0

mipiGenerator1.clockConfig = mipiClockConfig1
mipiGenerator1.clockSkew = 0.0
mipiGenerator1.commonNoise = None
mipiGenerator1.continuousClock = False
mipiGenerator1.dataLanes = [1, 2, 3, 4]
mipiGenerator1.dataSkews = [0.0]
mipiGenerator1.hsClockCommonVoltage = 200.0
mipiGenerator1.hsClockPostTap = 0
mipiGenerator1.hsClockPreTap = 0
mipiGenerator1.hsClockVoltageAmplitude = 200.0
mipiGenerator1.hsDataCommonVoltages = [200.0]
mipiGenerator1.hsDataPostTaps = [0]
mipiGenerator1.hsDataPreTaps = [0]
mipiGenerator1.hsDataVoltageAmplitudes = [200.0]
mipiGenerator1.jitterInjection = None
mipiGenerator1.lpClockHighVoltage = 1200.0
mipiGenerator1.lpClockLowVoltage = 0.0
mipiGenerator1.lpDataHighVoltages = [1200.0]
mipiGenerator1.lpDataLowVoltages = [0.0]
mipiGenerator1.params = dphyParams1
mipiGenerator1.pattern = DPHY_packetLoop1000_prbs9
mipiGenerator1.resetPatternMemory = True
mipiGenerator1.splitDataAcrossLanes = True

mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'
mipiProtocol.useEotp = False

resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'

#! TEST PROCEDURE
#svtVersion = requireSvtVersionInRange("21.1", None)
iesp = getIespInstance()
mipiClockConfig1.maxWaitMillisForSetDataRate = 120000

fail = 0
# Connect to scope
osci = initScope(calOptions.scopeIPAddress)
iesp.setMeasurementTimeout(60000)

# Define results dictionary
measureCoarseDelayDict = dict()
for lane in [1, 2, 3, 4,5] :
   measureCoarseDelayDict[lane] = dict()
   for dataRate in sorted(calOptions.calRates) :
      measureCoarseDelayDict[lane][dataRate] = dict()
      for wire in [0,1]:
          measureCoarseDelayDict[lane][dataRate][wire] = 0

#initialize generator
mipiGenerator1.dataLanes = [1,2,3,4]

failCoarseDelayDict = dict()
for lane in [1, 2, 3, 4,5] :
   failCoarseDelayDict[lane] = dict()
   for dataRate in sorted(calOptions.calRates) :
      failCoarseDelayDict[lane][dataRate] = dict()
      for wire in [0,1]:
          failCoarseDelayDict[lane][dataRate][wire] = 0

for lane in calOptions.calLanes:
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring D-PHY Lane %d..." % lane)

    if lane == 1 :
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire Pos to Ch1, Wire Neg to Ch2' % lane
    elif lane == 5:
        myString = 'Please connect clock signals to the oscilloscope. Wire Pos to Ch2, Wire Neg to Ch3. IMPORTANT: Keep Lane 1Pos connected to Ch1'
    else:
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire Pos to Ch2, Wire Neg to Ch3. IMPORTANT: Keep Lane 1Pos connected to Ch1' % lane

    waitForGuiOkDialog(myString)
    #auto scale once per lane
    autoScale = True

    for dataRate in calOptions.calRates :
        halfUi = 1000000 / dataRate / 2 * 1e-12
       # print "HalfUi: %e" % halfUi
        print("Measuring at %f Mbps..." % dataRate)
        iesp.writeSubPartRegister(0x0930, 0x00, 0x00) # diable cal mode
        iesp.writeSubPartRegister(0x0934, 0x00, 0x01) # disable halfUI offset on clock

        #do clock commit
        mipiClockConfig1.dataRate = dataRate
        #initialize generator after clock commit
        mipiGenerator1.setup()
        #enable alignment pattern
        iesp.writeSubPartRegister(0x0C80, 0x00, 0x01)
        # Prepare scope for measurement
        autoscaleScope()

        if lane==1 :

            coarseDelay1 = performScopeCal(lane,1,2,dataRate)
            measureCoarseDelayDict[lane][dataRate][1] = coarseDelay1 * 1e12

            if (abs(coarseDelay1) > halfUi/2):
                failCoarseDelayDict[lane][dataRate][1] = coarseDelay1
                print("fail on channel 1N get %g" % (lane, failCoarseDelayDict[lane][dataRate][1]))
                fail = 1

        elif lane==5 :
            print(halfUi)
            #use scope to measure values
            coarseDelay0 = performScopeCal(lane,0,2,dataRate)
            measureCoarseDelayDict[lane][dataRate][0] = (coarseDelay0)* 1e12
            if abs(coarseDelay0) > halfUi/2:
                failCoarseDelayDict[lane][dataRate][0] = coarseDelay0
                print("fail on Clock P get %g" % (failCoarseDelayDict[lane][dataRate][0]))

            coarseDelay1 = performScopeCal(lane,1,3,dataRate)
            measureCoarseDelayDict[lane][dataRate][1] = (coarseDelay1)* 1e12
            if abs(coarseDelay1) > halfUi/2:
                failCoarseDelayDict[lane][dataRate][1] = coarseDelay1
                print("fail on Clock N get %g" % (failCoarseDelayDict[lane][dataRate][1]))
                fail = 1

        else:
            #use scope to measure values
            coarseDelay0 = performScopeCal(lane,0,2,dataRate)
            measureCoarseDelayDict[lane][dataRate][0] = coarseDelay0 * 1e12

            if (abs(coarseDelay0) > halfUi/2):
                failCoarseDelayDict[lane][dataRate][0] = coarseDelay0
                print("fail on channel %d P get %f" % (lane, failCoarseDelayDict[lane][dataRate][0]))

            coarseDelay1 = performScopeCal(lane,1,3,dataRate)
            measureCoarseDelayDict[lane][dataRate][1] = coarseDelay1 * 1e12

            if (abs(coarseDelay1) > halfUi/2):
                failCoarseDelayDict[lane][dataRate][1] = coarseDelay1
                print("fail on channel %d N get %g" % (lane, failCoarseDelayDict[lane][dataRate][1]))
                fail = 1

writeCalFileTemp(measureCoarseDelayDict, failCoarseDelayDict)
writeCalFile(measureCoarseDelayDict, failCoarseDelayDict)
iesp.writeSubPartRegister(0x0C80, 0x00, 0x00)
iesp.writeSubPartRegister(0x0934, 0x00, 0x00) 

if fail == 1 :
    writeNoteForTestRun("Fail")
else :
    writeNoteForTestRun("Pass")

if fail == 0 :
    writeNoteForTestRun("PASS")
    filePath = getParamsFilePath("Pass.png")

    myFileUrl = str(filePath)

    popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
elif fail:
    writeNoteForTestRun("FAIL, please check report")
    filePath = getParamsFilePath("Fail.png")

    myFileUrl = str(filePath)

    popupDialog(title='Test Failed!', msg='Test Failed > Place Product in Fail Bin', buttonLabels=['PLACE PRODUCT IN THE FAIL BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
