import pkg_resources
import datetime
import xml.etree.ElementTree
import quarchpy

'''
Contains basic information for populating the header section of a calibration file and similar
'''
class CalibrationHeaderInformation ():
    def __init__(self):
        self.quarchEnclosureSerial = None
        self.quarchInternalSerial = None
        self.quarchFirmware = None
        self.quarchFpga = None
        self.calInstrumentId = None
        self.quarchpyVersion = None
        self.calCoreVersion = None
        self.calTime = None
        self.calTemperature = None
        self.calNotes = None
        self.calFileVersion = "1.0"
        
    '''
    Convert to standard XML text
    '''
    def toXmlText(self):
        # Header node
        headerObject = ElementTree.Element("Header")
        # Quarch module information
        quarchModuleObject = ElementTree.SubElement(headerObject, "QuarchModule")
        ElementTree.SubElement(quarchModuleObject, "EnclosureSerial").text = self.quarchEnclosureSerial
        ElementTree.SubElement(quarchModuleObject, "InternalSerial").text = self.quarchInternalSerial
        ElementTree.SubElement(quarchModuleObject, "ModuleFirmware").text = self.quarchFirmware
        ElementTree.SubElement(quarchModuleObject, "ModuleFpga").text = self.quarchFpga
        # Calibration instrument information
        calInstrumentObject = ElementTree.SubElement(headerObject, "CalInstrument")
        ElementTree.SubElement(calInstrumentObject, "Identity").text = self.calInstrumentId
        # Calibration software information
        CalSoftwareObject = ElementTree.SubElement(headerObject, "CalSoftware")
        ElementTree.SubElement(CalSoftwareObject, "QuarchPy").text = self.quarchpyVersion
        ElementTree.SubElement(CalSoftwareObject, "CalCoreVersion").text = self.calCoreVersion
        ElementTree.SubElement(CalSoftwareObject, "CalFileVersion").text = self.calFileVersion
        # General information        
        ElementTree.SubElement(headerObject, "CalTime").text = self.calTime
        ElementTree.SubElement(headerObject, "CalTemperature").text = self.calTemperature
        ElementTree.SubElement(headerObject, "calNotes").text = self.calNotes
        
        return ElementTree.tostring(headerObject)

    '''
    Convert to standard report text
    '''
    def toReportText(self):
        reportText = ""
        reportText += "CALIBRATION INFORMATION\n"
        reportText += "-----------------------\n"
        reportText += "\n"
        reportText += "Quarch Enclosure#: "
        reportText += self.quarchEnclosureSerial + "\n"
        reportText += "Quarch Serial#: "
        reportText += self.quarchInternalSerial + "\n"
        reportText += "Quarch Versions: "
        reportText += "FW:" + self.quarchFirmware + ", FPGA: " + self.quarchFpga + "\n"
        reportText += "\n"
        reportText += "Calibration Instrument#:\n"
        reportText += self.calInstrumentId + "\n"
        reportText += "\n"
        reportText += "Calibration Versions:\n"
        reportText += "QuarchPy Version: " + str(self.quarchpyVersion) + "\n"
        reportText += "Calibration Version: " + str(self.calCoreVersion) + "\n"
        reportText += "\n"
        reportText += "Calibration Details:\n"
        reportText += "Calibration Time: " + str(self.calTime) + "\n"
        reportText += "Calibration Temperature: " + str(self.calTemperature) + "\n"
        reportText += "Calibration Notes: " + str(self.calNotes) + "\n"
        
        return reportText
        
        
        

'''
Populates the header with Keithley specific information
'''       
def populateCalHeader_Keithley (calHeader, myCalInstrument):
    calHeader.calInstrumentId = myCalInstrument.sendCommandQuery ("*IDN?")
    
'''
Populates the header with PPM specific information
'''       
def populateCalHeader_HdPpm (calHeader, myDevice):
    # Serial numbers (ensure QTL at start)
    calHeader.quarchEnclosureSerial = myDevice.sendCommand("*ENCLOSURE?")
    if (calHeader.quarchEnclosureSerial.find ("QTL") == -1):
        calHeader.quarchEnclosureSerial = "QTL" + calHeader.quarchEnclosureSerial
    calHeader.quarchInternalSerial = myDevice.sendCommand ("*SERIAL?")
    if (calHeader.quarchInternalSerial.find ("QTL") == -1):
        calHeader.quarchInternalSerial = "QTL" + calHeader.quarchInternalSerial
    # Code version (FPGA)
    idStr = myDevice.sendCommand ("*IDN?").upper()
    pos = idStr.find ("FPGA 1:")
    if (pos != -1):
        versionStr = idStr[pos+7:]
        pos = versionStr.find ("\n")
        if (pos != -1):
            versionStr = versionStr[:pos].strip()
        else:
            pass
    else:
        versionStr = "NOT-FOUND"    
    calHeader.quarchFpga = versionStr.strip()
    
    # Code version (FW)    
    pos = idStr.find ("PROCESSOR:")
    if (pos != -1):
        versionStr = idStr[pos+10:]
        pos = versionStr.find ("\n")
        if (pos != -1):
            versionStr = versionStr[:pos].strip()            
        else:
            pass
    else:
        versionStr = "NOT-FOUND"    
    calHeader.quarchFirmware = versionStr.strip()
    
'''
Populates the header with system specific information
'''       
def populateCalHeader_System (calHeader):
    # Calibration core version
    calHeader.calCoreVersion = quarchpy.calibration.calCodeVersion
    # Quarchpy version
    calHeader.quarchpyVersion = pkg_resources.get_distribution("quarchpy").version
    # Calibration time
    calHeader.calTime = datetime.datetime.now()
    