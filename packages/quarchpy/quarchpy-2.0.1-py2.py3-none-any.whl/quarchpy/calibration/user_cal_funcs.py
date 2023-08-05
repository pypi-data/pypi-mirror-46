'''
General functions to help the user perform a calibration
'''

import quarchpy

'''
Function to print useful sections of standard calibration text to the user
'''
def displayCalInstruction (instructionName):
    if (instructionName.upper() == "OPEN_HD"):
        print ("")
        print ("Quarch Technology Calibration System")
        print ("(C) 2019, All rights reserved")
        print ("")
        print ("Full calibration process for QTL1999 HD Power Modules")
        print ("V" + quarchpy.calibration.calCodeVersion)
        print ("")
        