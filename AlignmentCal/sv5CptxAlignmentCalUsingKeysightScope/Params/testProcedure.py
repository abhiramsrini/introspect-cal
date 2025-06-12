# SVT Test
# SVT version 24.3.b7
# Test saved 2024-05-03_1528
# Form factor: SV5C_4L8G_MIPI_CPHY_GENERATOR
# PY3
# Checksum: d8c521c973e0cff4aeb971fb524c86ac
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


autoscaleScope = _create('autoscaleScope', 'SvtFunction', iespName='None')
calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
dataFile1 = _create('dataFile1', 'SvtDataFile', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
measureDeltaTime = _create('measureDeltaTime', 'SvtFunction', iespName='None')
performScopeCal = _create('performScopeCal', 'SvtFunction', iespName='None')
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName='None')
writeCalFileTemp = _create('writeCalFileTemp', 'SvtFunction', iespName='None')

cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiGenerator1 = _create('mipiGenerator1', 'SvtMipiCphyGenerator')
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
osci.write(":CALibrate:SKEW CHANnel4,0")

# Display the channels
osci.write(":CHANnel1:DISPlay 1")
osci.write(":CHANnel2:DISPlay 1")
osci.write(":CHANnel3:DISPlay 1")
osci.write(":CHANnel4:DISPlay 1")

# Autoscale the channels
osci.write(":AUToscale:VERTical CHANnel1")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel2")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel3")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel4")
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
osci.write(":TIMebase:SCALe 5e-09")
osci.write(":TRIGger:EDGE:SLOPe RISIng")
# Turn averaging on
osci.write(":ACQuire:AVERage:COUNt 16")
osci.write(":ACQuire:AVERage 1")

# Define delta-time measurement parameters
osci.write(":MEASure:DELTatime:DEFine RISing,1,MIDDle,RISing,1,MIDDle")
'''
autoscaleScope.wantAllVarsGlobal = False

calOptions.addField('serialNumber', descrip='''Serial number of device under test.''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='any', defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 3.0))
calOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function.''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 4.0))
calOptions.addField('numAverages', descrip='''Number of times the measurement is querried from the scope.''', attrType=int, iespInstanceName='any', defaultVal=100, displayOrder=(0, 5.0))
calOptions.addField('calLanes', descrip='''Range of channels to measure.''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 6.0))
calOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[4001.0, 4250.0, 4500.0, 4750.0, 5000.0, 5250.0, 5500.0, 5750.0, 6000.0, 6250.0, 6500.0, 6750.0, 7000.0, 7250.0, 7500.0, 7750.0, 8000.0], displayOrder=(0, 7.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.serialNumber = '1234'
calOptions.scopeIPAddress = 'TCPIP0::10.20.20.200::inst0::INSTR'
calOptions.scopeMeasurementDelay = 2000.0
calOptions.scopeAutoScaleDelay = 2000.0
calOptions.numAverages = 100
calOptions.calLanes = [1, 2, 3, 4]
calOptions.calRates = [4001.0, 4250.0, 4500.0, 4750.0, 5000.0, 5250.0, 5500.0, 5750.0, 6000.0, 6250.0, 6500.0, 6750.0, 7000.0, 7250.0, 7500.0, 7750.0, 8000.0]
calOptions.callCustomInitMethod()
dataFile1.delimiter = ','
dataFile1.fileName = ''
dataFile1.numFields = 1
dataFile1.otherFolderPath = r'None'
dataFile1.parentFolder = 'Results'

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
osci.write(":CHANnel4:DISPlay 1")
osci.timeout = 10000

return osci
'''
initScope.wantAllVarsGlobal = False

measureDeltaTime.args = 'channel'
measureDeltaTime.code = r'''# Assumes all measurements are relative to channel 1
channelString = "CHANNEL%d" % channel
commandString = ":MEASure:DELTatime CHANnel1,"+channelString # Calculate the delata time between channel 1 and the specified channel
osci.write(commandString)

sleepMillis(calOptions.scopeAutoScaleDelay)

currentDeltaTime = 0
commandString = ":MEASure:DELTatime? CHANnel1,"+channelString # Query the delata time between channel 1 and the specified channel
for i in range(calOptions.numAverages) :
    varAmp = osci.query_ascii_values(commandString) # Get the delta time value
    currentDeltaTime += varAmp[0] # Add to the total
currentDeltaTime = currentDeltaTime / calOptions.numAverages # Calculate the average

return currentDeltaTime
'''
measureDeltaTime.wantAllVarsGlobal = False

performScopeCal.args = 'lane,wire,position,  dataRate'
performScopeCal.code = r'''if lane == 4 and wire == 2:
    print("Performing coarse loop...")
    coarse = 0
    coarseDelay = coarse
    print("delay is %d..." % coarseDelay)
    print(" ")

else: # channels 2-16
    print("Performing coarse loop...")
    coarseDelay = measureDeltaTime(position)
    print("delay is %g..." % coarseDelay)


return coarseDelay
'''
performScopeCal.wantAllVarsGlobal = False

writeCalFile.args = 'polyCoefficients'
writeCalFile.code = r'''import datetime
import os

dataFile1.fileName = "calCoefficients_"+calOptions.serialNumber+".txt"
filePath = dataFile1.getFilePath()

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

with open(filePath, "w") as calFile:
    # Fill header section
    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : header\n")
    calFile.write("serial number : "+calOptions.serialNumber+"\n")
    calFile.write("hardware revision : Rev0\n")
    calFile.write("date of manufacture(YYYYMMDD) : "+date+"\n")
    calFile.write("date of calibration(YYYYMMDD) : "+date+"\n")
    calFile.write("END SECTION\n\n")

    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : tx_alignment_calibration_data_cphy\n")

    for c in range(4):
        for lane in [1, 2, 3, 4]:
            for wire in [0,1,2]:
                calFile.write("%0.15f," % polyCoefficients[lane][wire][c])
        calFile.write("\n")

    calFile.write("END SECTION\n")

    calFile.close()

dataFile1.saveAsResult("calCoefficients_"+calOptions.serialNumber)
dataFile1.deleteFile()
'''
writeCalFile.wantAllVarsGlobal = False

writeCalFileTemp.args = 'polyCoefficients'
writeCalFileTemp.code = r'''import datetime
import os

dataFile1.fileName = "calCoefficientsTemp_"+calOptions.serialNumber+".txt"
filePath = dataFile1.getFilePath()

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

with open(filePath, "w") as calFile:
    # Fill header section
    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : header\n")
    calFile.write("serial number : "+calOptions.serialNumber+"\n")
    calFile.write("hardware revision : Rev0\n")
    calFile.write("date of manufacture(YYYYMMDD) : "+date+"\n")
    calFile.write("date of calibration(YYYYMMDD) : "+date+"\n")
    calFile.write("END SECTION\n\n")

    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : tx_alignment_calibration_data_cphy\n")

    for c in range(4):
        for lane in [1, 2, 3, 4]:
            for wire in [0,1,2]:
                calFile.write("%0.15f," % polyCoefficients[lane][wire][c])
        calFile.write("\n")

    calFile.write("END SECTION\n")

    calFile.close()

dataFile1.saveAsResult("calCoefficientsTemp_"+calOptions.serialNumber)
dataFile1.deleteFile()
'''
writeCalFileTemp.wantAllVarsGlobal = False


cphyParams1.calAlternateSeqNumPrbs = 8
cphyParams1.calPreambleNumUI = 21
cphyParams1.calUserSequence = [0x5555, 0xAAAA]
cphyParams1.calibrationPreambleFormat = 'format_1'
cphyParams1.lp000Duration = 65.0
cphyParams1.lp001Duration = 100.0
cphyParams1.opticalLink = 'disabled'
cphyParams1.post2NumUI = 112
cphyParams1.postNumUI = 112
cphyParams1.postSymbols = '4444444'
cphyParams1.preBeginNumUI = 196
cphyParams1.preBeginSymbols = '3333333'
cphyParams1.preEndSymbols = '3333333'
cphyParams1.progSeqSymbols = '33333333333333'
cphyParams1.syncWord = '3444443'
cphyParams1.t3AlpPauseMin = 50
cphyParams1.t3AlpPauseWake = 50
cphyParams1.tHsExitDuration = 300.0
cphyParams1.tTaGetDuration = 5
cphyParams1.tTaGoDuration = 4.0
cphyParams1.tTaSureDuration = 1.0
cphyParams1.tWaitOptical = 150000.0
cphyParams1.tlpxDuration = 100.0
cphyParams1.useAlp = False

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 8000.0
mipiClockConfig1.referenceClocks = None

mipiGenerator1.clockConfig = mipiClockConfig1
mipiGenerator1.commonNoise = None
mipiGenerator1.hsCommonVoltagesABC = [(200.0, 200.0, 200.0)]
mipiGenerator1.hsPostTaps = [0]
mipiGenerator1.hsPreTaps = [0]
mipiGenerator1.hsVoltageAmplitudesABC = [(200.0, 200.0, 200.0)]
mipiGenerator1.jitterInjection = None
mipiGenerator1.lanes = [1, 2, 3, 4]
mipiGenerator1.lpHighVoltages = [1200.0]
mipiGenerator1.lpLowVoltages = [0.0]
mipiGenerator1.params = cphyParams1
mipiGenerator1.pattern = CPHY_packetLoop1000_prbs9
mipiGenerator1.resetPatternMemory = True
mipiGenerator1.splitDataAcrossLanes = True
mipiGenerator1.wireSkewsABC = [(0.0, 0.0, 0.0)]

mipiProtocol.csiScramble = False
mipiProtocol.csiScrambleNumSeeds = 'one'
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'

#! TEST PROCEDURE
svtVersion = requireSvtVersionInRange("23.1", None)
import numpy as np

iesp = getIespInstance()
# Connect to scope
osci = initScope(calOptions.scopeIPAddress)
iesp.setMeasurementTimeout(60000)

### All Rates are in OS=2 range ###
osRatio = 1

# Define results dictionary
measureCoarseDelayDict = dict()
for lane in [1, 2, 3, 4] :
    measureCoarseDelayDict[lane] = dict()
    for dataRate in sorted(calOptions.calRates) :
        xcvrRate = dataRate * osRatio
        measureCoarseDelayDict[lane][xcvrRate] = dict()
        for wire in [0,1,2]:
            measureCoarseDelayDict[lane][xcvrRate][wire] = 0

polyCoefficients = dict()
for lane in [1, 2, 3, 4] :
    polyCoefficients[lane] = dict()
    for wire in [0,1,2]:
        polyCoefficients[lane][wire] = dict()
        for c in range(4):
            polyCoefficients[lane][wire][c] = 0

dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure a default cal file has been loaded on the module."
waitForGuiOkDialog(myString)

#initialize generator
mipiGenerator1.lanes = calOptions.calLanes
mipiGenerator1.setup()

for lane in [4,3,2,1]:
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring C-PHY Lane %d..." % lane)

    if lane==4 :
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire C to Ch1, Wire B, to Ch2, and Wire A to Ch3' % lane
    else:
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire C to Ch2, Wire B to Ch3, and Wire A to Ch4. IMPORTANT: Keep Lane 4C connected to Ch1' % lane
    waitForGuiOkDialog(myString)

    #auto scale once per lane
    autoScale = True

    for dataRate in calOptions.calRates :
        print("Measuring at %f Mbps..." % dataRate)

        #do clock commit
        mipiClockConfig1.dataRate = dataRate
        #initialize generator after clock commit
        mipiGenerator1.setup()
        #enable alignment pattern
        iesp.writeSubPartRegister(0x0C80, 0x00, 0x01)

        #calculate xcvr rate
        xcvrRate = dataRate * osRatio

        # Prepare scope for measurement
        #if(autoScale):
        autoscaleScope()
        #    autoScale = False
        if lane==4 :
            #use scope to measure values
            coarseDelay0 = performScopeCal(lane,2,1,xcvrRate)
            measureCoarseDelayDict[lane][xcvrRate][2] = coarseDelay0 * 1e12
            coarseDelay1 = performScopeCal(lane,1,2,xcvrRate)
            measureCoarseDelayDict[lane][xcvrRate][1] = coarseDelay1 * 1e12
            coarseDelay2 = performScopeCal(lane,0,3,xcvrRate)
            measureCoarseDelayDict[lane][xcvrRate][0] = coarseDelay2 * 1e12
        else:
            #use scope to measure values
            coarseDelay0 = performScopeCal(lane,2,2,xcvrRate)
            measureCoarseDelayDict[lane][xcvrRate][2] = coarseDelay0 * 1e12
            coarseDelay1 = performScopeCal(lane,1,3,xcvrRate)
            measureCoarseDelayDict[lane][xcvrRate][1] = coarseDelay1 * 1e12
            coarseDelay2 = performScopeCal(lane,0,4,xcvrRate)
            measureCoarseDelayDict[lane][xcvrRate][0] = coarseDelay2 * 1e12

    for wire in [0,1,2] :
        xVals = list()
        yVals = list()
        for dataRate in sorted(calOptions.calRates) :
            #calculate xcvr rate
            xcvrRate = dataRate * osRatio
            xVals.append(xcvrRate)
            yVals.append(measureCoarseDelayDict[lane][xcvrRate][wire])
        polyCoefficients[lane][wire] = np.polyfit(xVals,yVals,3)
        print(polyCoefficients[lane][wire])
    writeCalFileTemp(polyCoefficients)

writeCalFile(polyCoefficients)
iesp.writeSubPartRegister(0x0C80, 0x00, 0x00)
