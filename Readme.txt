What do you need
1- High speed keysight scope
2- software 25.2.0
3- latest visa driver
https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html?srsltid=AfmBOoqLVIPdCyW5sEHvjyqBe2R0E0LdUxs1NO5PqRzCocjdPuCMoaBh#565016
4-keysight multimeter 34461A
5-A little board to connect the multimeter (see document LP calibration section)


procedure:

1- Program the default SV5_CPTX_default_flash_data.jam Cal file, using the firmware updater in the GUI. Use ALT-F to disable the compatibility check
2- Program CPHY firmware
3- open cptxAlignmentCalUsingKeysightScope. In calOption, change scope adress. 
4- Run cptxAlignmentCalUsingKeysightScope, follow the instruction to know how to connect to the scope. 
5- repeat with cptxCalUsingKeysightScope. 
6- repat with cptxLpCalUsingMultiMeter, but this time connect the unit to the multimeter. 
7- Change to DPHY firmware
8- run dptxAlignmentCalUsingKeysightScope
3- When it's finished, please send us the results, we will generate the new calibration file. 
4- We will send you back a new cal file, program it using the firmware updater in the GUI. 
5- You can run the validation procedures to make sure eveything is fine. 
