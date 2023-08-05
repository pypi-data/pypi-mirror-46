import telnetlib
import time
'''
Class for control of Keithley source measure units for calibration purposes
'''
class keithley2460:
    '''
    Init the class
    '''
    def __init__(self, connectionString):
        self.conString = connectionString
        self.connection = None
        self.idnString = "MODEL 2460"
        
    '''
    Open the connection to the instrument
    '''
    def openConnection (self, connectionString = None):
        # Connect Telnet
        if (connectionString is not None):
            self.conString = connectionString
        self.connection = telnetlib.Telnet(self.conString)
        # Flush any initial return
        time.sleep(0.5)
        self.connection.read_very_eager()
        time.sleep(0.5)
        # Send the IDN? command
        response = self.sendCommandQuery ("*idn?")
        # Verify this looks like the expected instrument
        if (response.find (self.idnString) == -1):
            raise ValueError ("Connected device does not appear to be a keithley2460")
        
    '''
    Close the connection to the instrument
    '''
    def closeConnection (self):
        self.connection.close()
        
    '''
    Send a command to the instrument and return the response from the query
    This should only be used for commands which expect a response
    '''
    def sendCommandQuery (self, commandString):        
        # Send the command
        self.connection.write((commandString + "\r\n").encode('latin-1'))
        # Read back the response data
        resultStr = self.connection.read_until(b"\r\n",3).decode("utf-8")
        resultStr = resultStr.strip ('\r\n\t')
        # If no response came back
        if (resultStr is None):
            if (self.getStatusEavFlag () == True):
                errorStr = self.getNextError ()
                self.clearErrors ()
                raise ValueError ("Keithley query command did not run correctly: " + errorStr)
            else:
                raise ValueError ("The Keithley did not retun a response")
                            
        return resultStr
    
    '''
    Sends a command to the instrument where a response is not expected.
    Status byte check is used to verify that the command does not flag an error
    If an error is found, it will be flushed and the first error text returned
    'OK' is returned on success
    '''    
    def sendCommand (self, commandString):
        # Send the command
        self.connection.write((commandString + "\r\n").encode('latin-1'))
        # Check for errors
        if (self.getStatusEavFlag () == True):
            errorStr = self.getNextError ()
            self.clearErrors ()
            return errorStr
        else:
            return "OK"
    
        
    '''
    Enable/disable the outputs
    '''
    def setOutputEnable (self, enableState):
        if (enableState == True):
            result = self.sendCommand("OUTP ON")
        else:
            result = self.sendCommand("OUTP OFF")
            
        return result
        
    '''
    Return the output enable state as a boolean
    '''
    def getOutputEnable (self):
        result = self.sendCommandQuery ("OUTP?")
        if (int(result) == 1):
            return True
        else:
            return False
        
    '''
    Set the output voltage limit, in volts
    '''
    def setLoadVoltageLimit (self, voltValue):
        return self.sendCommand("SOUR:CURR:VLIM " + str(voltValue))
        
    '''
    Return the load voltage limit as a float
    '''
    def getLoadVoltageLimit (self):
        result = self.sendCommandQuery ("SOUR:CURR:VLIM?")
        return float(result)
        
    '''
    Switch the outputs to high impedance mode
    '''
    def setOutputMode (self, modeString):        
        modeString = modeString.upper()
        if (modeString == "HIMP"):
            result = self.sendCommand("OUTP:CURR:SMOD HIMP")
        elif (modeString == "NORMAL"):
            result = self.sendCommand("OUTP:CURR:SMOD NORMAL")
        elif (modeString == "ZERO"):
            result = self.sendCommand("OUTP:CURR:SMOD ZERO")
        else:
            raise ValueError ("Invalid mode type specified: " + modeString)
            
        return result
        
    '''
    Returns the high impedance mode as a string
    '''
    def getOutputMode (self):
        return self.sendCommandQuery("OUTP:CURR:SMOD?");
        
    '''
    Changes the instrument into the specified measurement mode
    '''
    def setMeasurementMode (self, measModeString):
        measModeString = measModeString.upper()
        if (measModeString == "VOLT"):
            result = self.sendCommand("SENS:FUNC \"VOLT\"")
        elif (measModeString == "CURR"):
            result = self.sendCommand("SENS:FUNC \"CURR\"")
        else:
            raise ValueError ("Invalid mode type specified: " + measModeString)
            
        return result
            
    '''
    Return the current measurement mode as a string
    '''
    def getMeasurementMode (self):
        return self.sendCommandQuery("SENS:FUNC?").strip('\"')
        
    '''
    Changes the instrument into the specified source/output mode
    '''
    def setSourceMode (self, sourceModeString):
        sourceModeString = sourceModeString.upper()
        if (sourceModeString == "VOLT"):
            result = self.sendCommand("SOUR:FUNC VOLT")
        elif (sourceModeString == "CURR"):
            result = self.sendCommand("SOUR:FUNC CURR")
        else:
            raise ValueError ("Invalid mode type specified: " + sourceModeString)
            
        return result

    '''
    Return the dource mode, as a string
    '''
    def getSourceMode (self):
        return self.sendCommandQuery("SOUR:FUNC?")
        
    '''
    Sets the number of measurements to be taken in a sequence
    '''
    def setMeasurementCount (self, measCount=1, measDelay="0"):
        return self.sendCommand("TRIGger:LOAD \"SimpleLoop\"," + str(measCount) + "," + str(measDelay))
        
    '''
    Set the load/drain current to supply
    '''
    def setLoadCurrent (self, ampValue):        
        #load current should always be negative
        if (ampValue <= 0): 
            ampValue = -ampValue

        # set source current
        return self.sendCommand("SOUR:CURR -" + str(ampValue));           
        
    '''
    Sets the limit for the load current in Amps
    '''
    def setLoadCurrentLimit (self, ampValue):
        return self.sendCommand("SOUR:VOLT:ILIM " + str(ampValue));

    '''
    Gets the limit for the load current in Amps (float)
    '''
    def getLoadCurrentLimit (self):
        return self.sendCommandQuery("SOUR:VOLT:ILIM?");


    '''
    Gets the current load current, as set
    '''
    def getLoadCurrent (self):                  
        result = float((self.sendCommandQuery("SOUR:CURR?")))
        return -result
        
    '''
    Measures and returns a current value
    '''
    def measureLoadCurrent (self):                  
        result = float((self.sendCommandQuery("MEAS:CURR?")))
        return -result
        
    '''
    Sets the load output voltage in Volts
    '''
    def setLoadVoltage (self, voltValue):
        return self.sendCommand("SOUR:VOLT " + str(voltValue))
        
    '''
    Gets the current load voltage value
    '''
    def getLoadVoltage (self):        
        result = float((self.sendCommandQuery("SOUR:VOLT?")))
        return result
        
    '''
    Measures the current load voltage value
    '''
    def measureLoadVoltage (self):        
        result = float((self.sendCommandQuery("MEAS:VOLT?")))
        return result
        
    '''
    Returns the status byte from the instrument (the result of the *STB? command)
    This is used to tell if the module is ready or has errored
    '''
    def getStatusByte (self):            
        resultStr = self.sendCommandQuery ("*STB?")
        # Return the result as an integer
        return int(resultStr)
        
    def printInstrumentStatus (self):
        stat = self.getStatusByte ()
        if (stat&1 != 0):
            print ("Measurement Summary Flag Set")
        if (stat&2 != 0):
            print ("Reserved Flag 1 Set")
        if (stat&4 != 0):
            print ("Error Available Flag Set")
        if (stat&8 != 0):
            print ("Questionable Event Flag Set")
        if (stat&16 != 0):
            print ("Message Available Flag Set")
        if (stat&32 != 0):
            print ("Enabled Standard Event Flag Set")
        if (stat&64 != 0):
            print ("Enabled Summary Bit Flag Set")
        if (stat&128 != 0):
            print ("Enabled Operation event Flag Set")
        if (stat == 0):
            print ("Status flags are clear")
        
    '''
    Returns the Measurement Summary Bit of the status information
    '''
    def getStatusMsbFlag (self):
        stat = self.getStatusByte ()
        # Meas bit is LSb
        if (stat&1 != 0):
            return True
        else:
            return False;
            
    '''
    Returns the Question Summary Bit of the status information
    '''
    def getStatusQsbFlag (self):
        stat = self.getStatusByte ()
        # Meas bit is LSb
        if (stat&8 != 0):
            return True
        else:
            return False;
            
    '''
    Returns the Error Available Bit of the status information
    '''
    def getStatusEavFlag (self):
        stat = self.getStatusByte ()
        # Meas bit is LSb
        if (stat&4 != 0):
            return True
        else:
            return False;
    
    '''
    Gets the next error from the instrument in a nice text form
    '''
    def getNextError (self):   
        errorStr = self.sendCommandQuery ("SYSTem:ERRor:NEXT?")
        return errorStr
    
    '''
    Clears all errors from the queue, so the status EAV flag is cleared
    '''
    def clearErrors (self):
        self.sendCommand (":SYSTem:CLEar")
        #loop = 0
        # Loop through and flush our all current errors
        #while (self.getStatusEavFlag () == True and loop < 10):
        #    print (self.getNextError ())
        #    loop += 1
    
        
        
        
        
        