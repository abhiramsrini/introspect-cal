# SVT Test
# SVT version 23.1.0
# Test saved 2023-03-13_1425
# Form factor: SV5C_4L8G_MIPI_CPHY_GENERATOR
# PY3
# Checksum: 856057c761e42abf1bd16122439de7ec
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


initScope = _create('initScope', 'SvtFunction', iespName='None')
performScopeMeasurement = _create('performScopeMeasurement', 'SvtFunction', iespName='None')
performValidationOnCollectedData = _create('performValidationOnCollectedData', 'SvtFunction', iespName='None')
validationOptions = _create('validationOptions', 'SvtDataRecord', iespName='None')
writeRawData = _create('writeRawData', 'SvtFunction', iespName='None')

cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiCphyGenerator1 = _create('mipiCphyGenerator1', 'SvtMipiCphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

initScope.args = 'scopeIpAddress'
initScope.code = r'''import win32com.client

# Connect to Lecroy scope using ActiveDSO
osci = win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
osci.MakeConnection(scopeIpAddress)
sleepMillis(validationOptions.scopeConnectionTimeout)

# Reset all scope settings to default
osci.WriteString("*RST", True)
sleepMillis(validationOptions.scopeAutoScaleDelay)

# Set deskew to 0 for all channels
osci.WriteString("C1:DESKEW 0", True)
osci.WriteString("C2:DESKEW 0", True)
osci.WriteString("C3:DESKEW 0", True)
osci.WriteString("C4:DESKEW 0", True)

# Enable channels
osci.WriteString("C1:TRA ON", True)
osci.WriteString("C2:TRA ON", True)
osci.WriteString("C3:TRA ON", True)

return osci
'''
initScope.wantAllVarsGlobal = False

performScopeMeasurement.args = ''
performScopeMeasurement.code = r'''# Set timebase to proper value
osci.WriteString("TDIV 50NS", True)

# Autoscale the channels
osci.WriteString("C1:ASET FIND", True)
osci.WriteString("C2:ASET FIND", True)
osci.WriteString("C3:ASET FIND", True)

# Clear display
osci.WriteString("CLEAR_SWEEPS", True)

# Setup measurement parameters for average and amplitude
osci.WriteString("C1:PARAMETER_CUSTOM 'P1', 'VoltAvg'", True)
osci.WriteString("C1:PARAMETER_CUSTOM 'P2', 'PkPk'", True)

sleepMillis(validationOptions.scopeAutoScaleDelay)
currentValue = float(osci.WriteString("C1:PARAMETER_VALUE? P1", True))

sleepMillis(validationOptions.scopeMeasurementDelay)
currentAmp = float(osci.WriteString("C1:PARAMETER_VALUE? P2", True))

triggerValue = currentValue - 0.25*currentAmp

# Set trigger level to be just below the mid-point of the 3-level waveform
osci.WriteString(f"C1:TRLV {triggerValue}", True)

# Clear display and wait
osci.WriteString("CLEAR_SWEEPS", True)
sleepMillis(100)

## Now perform measurements on all channels
commonModeReturnList = list()
amplitudeReturnList = list()
for channel in [1,2,3] :
    # Setup measurements for each channel
    osci.WriteString(f"C{channel}:PARAMETER_CUSTOM 'P1', 'VoltAvg'", True)
    osci.WriteString(f"C{channel}:PARAMETER_CUSTOM 'P2', 'PkPk'", True)
    sleepMillis(validationOptions.scopeMeasurementDelay)
    
    # Get average voltage
    varAverage = float(osci.WriteString(f"C{channel}:PARAMETER_VALUE? P1", True))
    if validationOptions.connectedToTerminationBoard :
        commonModeReturnList.append(varAverage*1000) #convert to mV
    else:
        commonModeReturnList.append((varAverage*1000*(50+impedance))/(50)) #convert to mV and apply scope attenuation factor

    # Get amplitude
    varAmp = float(osci.WriteString(f"C{channel}:PARAMETER_VALUE? P2", True))
    amplitudeReturnList.append(varAmp*1000) #convert to mV

return(commonModeReturnList, amplitudeReturnList)
'''
performScopeMeasurement.wantAllVarsGlobal = False

performValidationOnCollectedData.args = 'commonData, ampData'
performValidationOnCollectedData.code = r'''fail = 0
print("Checking measured data...")
for lane in validationOptions.calLanes :
        for cm in validationOptions.commonModeValues :
            for amp in validationOptions.amplitudeValues :
                for wire in range(3) :
                    commonErrorValue = abs( commonData[lane][cm][amp][wire] - cm )
                    commonErrorPercent = commonErrorValue / cm * 100
                    ampErrorValue = abs( ampData[lane][cm][amp][wire] - amp )
                    ampErrorPercent = ampErrorValue / amp * 100
                    if not ( commonErrorValue < validationOptions.absoluteErrorThreshold or commonErrorPercent < validationOptions.percentErrorThreshold ):
                        print("Found a failing condition on Lane %d wire %d..." % (lane,wire))
                        print("Target common mode is %f mV" % cm)
                        print("Measured common mode is %f mV" % commonData[lane][cm][amp][wire])
                        print("Absolute Error is %f mV" % commonErrorValue)
                        print("Percent Error is %f percent" % commonErrorPercent)
                        fail = 1
                        #return False
                    if not ( ampErrorValue < validationOptions.absoluteErrorThreshold or ampErrorPercent < validationOptions.percentErrorThreshold ) :
                        print("Found a failing condition on Lane %d wire %d..." % (lane,wire))
                        print("Target amplitude is %f mV" % amp)
                        print("Measured amplitude is %f mV" % ampData[lane][cm][amp][wire])
                        print("Absolute Error is %f mV" % ampErrorValue)
                        print("Percent Error is %f percent" % ampErrorPercent)
                        #return False
                        fail = 1
if fail == 1:
    return False
else:
    return True
'''
performValidationOnCollectedData.wantAllVarsGlobal = False

validationOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal='1234', displayOrder=(0, 1.0))
validationOptions.addField('scopeIPAddress', descrip='''IP address or hostname of the Teledyne Lecroy oscilloscope''', attrType=str, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal='10.20.20.200', displayOrder=(0, 2.0))
validationOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal=3000.0, displayOrder=(0, 3.0))
validationOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal=2000.0, displayOrder=(0, 4.0))
validationOptions.addField('calDataRate', descrip='''Base data rate for performing voltage measurements''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal=500.0, displayOrder=(0, 5.0))
validationOptions.addField('calLanes', descrip='''Range of lanes to measure''', attrType=list, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 6.0))
validationOptions.addField('commonModeValues', descrip='''Range of common-mode voltages to be verified''', attrType=list, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', attrSubType=float, defaultVal=[130.0, 390.0], displayOrder=(0, 7.0))
validationOptions.addField('amplitudeValues', descrip='''Range of differential voltages to be verified''', attrType=list, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', attrSubType=float, defaultVal=[40.0, 270.0, 290.0], displayOrder=(0, 8.0))
validationOptions.addField('connectedToTerminationBoard', descrip='''Set to true if the measurement is performed using a termination board with high-impedance probes. If the measurement is done directly on the oscilloscope 50 Ohm inputs, set to False. If set to False, a compensation value for common mode measurements is applied''', attrType=bool, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal=False, displayOrder=(0, 9.0))
validationOptions.addField('absoluteErrorThreshold', descrip='''Pass/fail threshold for the absolute value of voltage error''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal=25.0, displayOrder=(0, 10.0))
validationOptions.addField('percentErrorThreshold', descrip='''Pass/fail threshold for the percentage of voltage error''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal=10.0, displayOrder=(0, 11.0))
validationOptions.addField('scopeConnectionTimeout', descrip='''Scope connection timeout.''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal=30000.0, displayOrder=(0, 12.0))
validationOptions.addField('minVersion', descrip='''Minimum Introspect ESP software version that is supported by this script.''', attrType=str, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal='20.4', displayOrder=(0, 13.0))
validationOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
validationOptions.serialNumber = '1234'
validationOptions.scopeIPAddress = '10.20.20.200'
validationOptions.scopeMeasurementDelay = 3000.0
validationOptions.scopeAutoScaleDelay = 2000.0
validationOptions.calDataRate = 500.0
validationOptions.calLanes = [1, 2, 3, 4]
validationOptions.commonModeValues = [130.0, 390.0]
validationOptions.amplitudeValues = [40.0, 270.0, 290.0]
validationOptions.connectedToTerminationBoard = False
validationOptions.absoluteErrorThreshold = 10.0
validationOptions.percentErrorThreshold = 5.0
validationOptions.scopeConnectionTimeout = 30000.0
validationOptions.minVersion = '23.1'
validationOptions.callCustomInitMethod()
writeRawData.args = 'commonData, ampData'
writeRawData.code = r'''import time
import os
## dd/mm/yyyy format
dateToday = time.strftime("%d/%m/%Y")
timeNow = time.strftime("%H:%M:%S")

resultFolderCreator1.folderName = validationOptions.serialNumber
folderPath = resultFolderCreator1.run()

stringAppendix = ".csv"
filePathString = validationOptions.serialNumber + "_CptxVoltageCalData" + stringAppendix
filePath = os.path.join(folderPath, filePathString)
with open(filePath, "w") as outFile:
    print("CPTX Voltage Validation Data", file=outFile)
    print("Serial Number, %s" % validationOptions.serialNumber, file=outFile)
    print("Date, %s" % dateToday, file=outFile)
    print("Time, %s" % timeNow, file=outFile)
    print(" ,", file=outFile)
    print("Lane, WireA Programmed CM, WireA Programmed Amp, WireA Measured CM, WireA Measured Amp, WireB Programmed CM, WireB Programmed Amp, WireB Measured CM, WireB Measured Amp, WireC Programmed CM, WireC Programmed Amp, WireC Measured CM, WireC Measured Amp,", file=outFile)
    for lane in validationOptions.calLanes :
        for cm in validationOptions.commonModeValues :
            for amp in validationOptions.amplitudeValues :
                print("%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f," % (lane, cm, amp, commonData[lane][cm][amp][0], ampData[lane][cm][amp][0], cm, amp, commonData[lane][cm][amp][1], ampData[lane][cm][amp][1], cm, amp, commonData[lane][cm][amp][2], ampData[lane][cm][amp][2]), file=outFile)
'''
writeRawData.wantAllVarsGlobal = False


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
cphyParams1.tTaSureDuration = 1.5
cphyParams1.tWaitOptical = 150000.0
cphyParams1.tlpxDuration = 50.0
cphyParams1.useAlp = False

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 500.0
mipiClockConfig1.referenceClocks = None

mipiCphyGenerator1.clockConfig = mipiClockConfig1
mipiCphyGenerator1.commonNoise = None
mipiCphyGenerator1.hsCommonVoltagesABC = [(200.0, 200.0, 200.0)]
mipiCphyGenerator1.hsPostTaps = [0]
mipiCphyGenerator1.hsPreTaps = [0]
mipiCphyGenerator1.hsVoltageAmplitudesABC = [(200.0, 200.0, 200.0)]
mipiCphyGenerator1.jitterInjection = None
mipiCphyGenerator1.lanes = [1, 2, 3, 4]
mipiCphyGenerator1.lpHighVoltages = [1200.0]
mipiCphyGenerator1.lpLowVoltages = [0.0]
mipiCphyGenerator1.params = cphyParams1
mipiCphyGenerator1.pattern = CPHY_hsOnly333
mipiCphyGenerator1.resetPatternMemory = True
mipiCphyGenerator1.splitDataAcrossLanes = True
mipiCphyGenerator1.wireSkewsABC = [(0.0, 0.0, 0.0)]

mipiProtocol.csiScramble = False
mipiProtocol.csiScrambleNumSeeds = 'one'
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'


initScope._showInList = False
performScopeMeasurement._showInList = False
performValidationOnCollectedData._showInList = False
writeRawData._showInList = False

cphyParams1._showInList = False
mipiCphyGenerator1._showInList = False
resultFolderCreator1._showInList = False
#! TEST PROCEDURE
# Check Version
iesp = getIespInstance()

svtVersion = getSvtVersion()
if svtVersion < validationOptions.minVersion:
    errorMsg("Your version of Introspect ESP is too old (v %s). Must use installation version %s or later." % (svtVersion, validationOptions.minVersion))

# Connect to scope
osci = initScope(validationOptions.scopeIPAddress)

firmware = iesp.getFirmwareIdsFromConnection()

res = firmware[0].split("FWSV5CCPTX01")
if res[1][0] == "A":
    impedance = 27
elif res[1][0] == "B" or res[1][0] == "C":
    impedance = 45
else:
    print("ERROR: firmware is not A or B please check impedance for this firmware")
    exit()

print(impedance)

# Initialize generator
mipiCphyGenerator1.lanes = validationOptions.calLanes
mipiClockConfig1.dataRate = validationOptions.calDataRate
mipiCphyGenerator1.setup()

#disable cal mode
iesp = getIespInstance()
iesp.writeSubPartRegister(0x0C80, 0x00, 0x00)
iesp.writeSubPartRegister(0x0930, 0x00, 0x00)   # clear calibration mode

# Define results dictionary
measuredCommonModeDict = dict()
measuredAmplitudeDict = dict()

for lane in mipiCphyGenerator1.lanes :
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring C-PHY Lane %d..." % lane)
    myString = 'Please connect Lane %d signals to the oscilloscope. Wire A to Ch1, Wire B, to Ch2, and Wire C to Ch3' % lane
    waitForGuiOkDialog(myString)
    measuredCommonModeDict[lane] = dict()
    measuredAmplitudeDict[lane] = dict()

    for programmedCommonMode in validationOptions.commonModeValues :
        print("Measuring at %f mV common-mode..." % programmedCommonMode)
        measuredCommonModeDict[lane][programmedCommonMode] = dict()
        measuredAmplitudeDict[lane][programmedCommonMode] = dict()

        for programmedAmplitude in validationOptions.amplitudeValues :
            print("Measuring at %f mV amplitude..." % programmedAmplitude)
            measuredCommonModeDict[lane][programmedCommonMode][programmedAmplitude] = list()
            measuredAmplitudeDict[lane][programmedCommonMode][programmedAmplitude] = list()

            # Update the generator
            mipiCphyGenerator1.hsCommonVoltagesABC = [(programmedCommonMode, programmedCommonMode, programmedCommonMode)]
            mipiCphyGenerator1.hsVoltageAmplitudesABC = [(programmedAmplitude, programmedAmplitude, programmedAmplitude)]
            mipiCphyGenerator1.update()

            # Use scope to measure values. Each return variable is a list of 3 values corresponding to the three wires on the lane
            (measuredCommonMode, measuredAmplitude) = performScopeMeasurement()


            # Accumulate the list into the dictionaries
            for wire in range(0,3,1) :
                # Add correstion fator of 10% because of scope terminaison
                measuredCommonModeDict[lane][programmedCommonMode][programmedAmplitude].append( measuredCommonMode[wire] )
                measuredAmplitudeDict[lane][programmedCommonMode][programmedAmplitude].append( measuredAmplitude[wire] )

            # Display information messages
            wires = ['A', 'B', 'C']
            for wire in range(0,3,1) :
                print("Wire %s: Programmed % f mV common-mode, and measured %f mV..." % (wires[wire],programmedCommonMode, measuredCommonMode[wire]))
                print("Wire %s: Programmed %f mV amplitude, and measured %f mV..." % (wires[wire], programmedAmplitude, measuredAmplitude[wire]))

# Dump the raw measurement values into a csv file
writeRawData(measuredCommonModeDict, measuredAmplitudeDict)

if performValidationOnCollectedData(measuredCommonModeDict, measuredAmplitudeDict) :
    failFlag = 0 
else :
    writeNoteForTestRun("Fail")
    failFlag = 1
    
if failFlag == 0 :
    writeNoteForTestRun("PASS")
    filePath = getParamsFilePath("Pass.png")

    myFileUrl = str(filePath)

    popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
elif failFlag:
    writeNoteForTestRun("FAIL, please check report")
    filePath = getParamsFilePath("Fail.png")

    myFileUrl = str(filePath)

    popupDialog(title='Test Failed!', msg='Test Failed > Place Product in Fail Bin', buttonLabels=['PLACE PRODUCT IN THE FAIL BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
