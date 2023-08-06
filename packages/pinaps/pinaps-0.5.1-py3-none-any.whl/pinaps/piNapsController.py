import sys
import serial
import time
import RPi.GPIO as GPIO
from enum import IntEnum

from SC16IS750 import SC16IS750 #Will be moving this to only be imported when needed. After testing pip instal SC16IS750
import blinoExceptions

class PiNapsController:
    ##Direct control from PI or through I2C chip##
    class Control(IntEnum):
        NONE = 0
        GPIO = 1
        I2C = 2

    ##Pi to EEG sensor interface##
    class Interface(IntEnum):
        NONE = 0
        UART = 1
        I2C = 2

    ##Pi pins##
    class PI_PINS(IntEnum):
        POWER = 23
        TX = 14
        RX = 15
        IN_1 = 4
        IN_2 = 17

    ##I2C pins##
    class I2C_PINS(IntEnum):
        POWER = 4
        IN_1 = 7
        IN_2 = 6
        LED_RED = 1
        LED_GREEN = 2
        LED_BLUE = 3

    ##Possible PiNaps I2C addresses##
    class I2C_ADDRESSES(IntEnum):
        A0x90 = 0x90
        A0x92 = 0x92
        A0x98 = 0x98
        A0x9A = 0x9A

    ##Baudrate values##
    class Baudrate(IntEnum):
        BAUD_1_2K = 1200
        BAUD_9_6K = 9600
        BAUD_57_6K = 57600

    ##EEG sensor operating modes##
    class OutputMode(IntEnum):
        MODE_REDUCED = 0
        MODE_BASIC = 1
        MODE_EEG_RAW = 3
        MODE_FFT = 4

    ##Init interfaces and GPIO pins##
    def __init__(self, I2C_Address = 0x9A):
        self._control = self.Control.GPIO
        self._interface = self.Interface.NONE
        self._UART = None
        self._I2C = None
        self._I2C_Address = I2C_Address
        GPIO.setmode(GPIO.BCM)

    def defaultInitialise(self):
        self.setControlInterfaceI2C()
        self.setEEGSensorInterfaceUART()
        self.setBasicMode()

    ##Set control from PI directly or through I2C##
    def setControlInterface(self, selectedControl):
        if(selectedControl == self.Control.GPIO):
            GPIO.setup(self.PI_PINS.POWER, GPIO.OUT)
            GPIO.setup(self.PI_PINS.IN_1, GPIO.OUT)
            GPIO.setup(self.PI_PINS.IN_2, GPIO.OUT)
        if(selectedControl == self.Control.I2C):
            self._I2C = SC16IS750.SC16IS750(14745600, self._I2C_Address)
            self._I2C.writeRegister(self._I2C.registers.IODIR, 0xFF)
        self._control = selectedControl

    def setControlInterfaceI2C(self):
        self.setControlInterface(self.Control.I2C)
        
    def setControlInterfaceGPIO(self):
        self.setControlInterface(self.Control.GPIO)

    ##Activate a chosen LED##
    def activateLED(self, selectedLED):
        if(self._control == self.Control.I2C):
            self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, selectedLED)
        else:
            raise ConfigError("LED could not be activated. Make sure I2C configured properly.")

    def activateRedLED(self):
        self.activateLED(self.I2C_PINS.LED_RED)

    def activateGreenLED(self):
        self.activateLED(self.I2C_PINS.LED_GREEN)

    def activateBlueLED(self):
        self.activateLED(self.I2C_PINS.LED_BLUE)

    ##Deactivate a chosen LED##
    def deactivateLED(self, selectedLED):
        if(self._control == self.Control.I2C):
            self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, selectedLED)
        else:
            raise ConfigError("LED could not be activated. Make sure I2C configured properly.")

    def deactivateRedLED(self):
        self.deactivateLED(self.I2C_PINS.LED_RED)

    def deactivateGreenLED(self):
        self.deactivateLED(self.I2C_PINS.LED_GREEN)

    def deactivateBlueLED(self):
        self.deactivateLED(self.I2C_PINS.LED_BLUE)

    ##Deactivate all LEDs##
    def deactivateAllLEDs(self):
        if(self._control == self.Control.I2C):
            self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.LED_RED)
            self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.LED_GREEN)
            self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.LED_BLUE)
        else:
            raise ConfigError("LED could not be activated. Make sure I2C configured properly.")

    ##Button Functions##
    def checkButton(self):
        self._I2C.unsetRegisterBit(self._I2C.registers.IODIR, 0)
        return self._I2C.readRegister(self._I2C.registers.IOSTATE)

    def setEEGSensorInterface(self, selectedInterface):
        ##Activate EEG sensor & set switch to I2C UART##
        if(selectedInterface == self.Interface.I2C):
            self._interface = self.Interface.I2C

            ##Activate direct from PI##
            if(self._control == self.Control.GPIO):
                GPIO.output(self.PI_PINS.POWER, GPIO.HIGH)
                GPIO.output(self.PI_PINS.IN_1, GPIO.HIGH)
                GPIO.output(self.PI_PINS.IN_2, GPIO.HIGH)
                
            ##Activate through I2C##
            if(self._control == self.Control.I2C):
                self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.POWER)
                self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, 5)
                self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.IN_1)
                self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.IN_2)
                
            if(self._control == self.Control.NONE):
                raise ConfigError("Can not activate EEG Sensor. Make sure Pinaps control configure first.")

        ##Activate EEG sensor & set switch to PI UART##
        if(selectedInterface == self.Interface.UART):
            self._interface = self.Interface.UART
            self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_57_6K)
            
            ##Activate direct from PI##
            if(self._control == self.Control.GPIO):
                GPIO.output(self.PI_PINS.POWER, GPIO.HIGH)
                GPIO.output(self.PI_PINS.IN_1, GPIO.LOW)
                GPIO.output(self.PI_PINS.IN_2, GPIO.HIGH)
                
            ##Activate through I2C##
            if(self._control == self.Control.I2C):
                self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.POWER)
                self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, 5)
                self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.IN_1)
                self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.IN_2)
                
            if(self._control == self.Control.NONE):
                raise ConfigError("Can not activate EEG Sensor. Make sure Pinaps control configure first.")

        ##Deactivate EEG sensor & set switch off##
        if(selectedInterface == self.Interface.NONE):
            self._interface = self.Interface.NONE
            #Close Pi UART interface if open#
            if(self._UART != None):
                self._UART.close()
                
            ##Deactivate direct from PI##
            if(self._control == self.Control.GPIO):
                GPIO.output(self.PI_PINS.POWER, GPIO.LOW)
                
            ##Deactivate through I2C##
            if(self._control == self.Control.I2C):
                self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.POWER)
                self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, 5)
                self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.IN_1)
                self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, self.I2C_PINS.IN_2)
                
            if(self._control == self.Control.NONE):
                raise ConfigError("Can not deactivate EEG Sensor. Make sure Pinaps control configure first.")

    def setEEGSensorInterfaceI2C(self):
        self.setEEGSensorInterface(self.Interface.I2C)

    def setEEGSensorInterfaceUART(self):
        self.setEEGSensorInterface(self.Interface.UART)

    ##Check if data waiting from TGAT##
    def isWaiting(self):
        if(self._interface == self.Interface.UART):
            if(self._UART.inWaiting()):
                return True
        if(self._interface == self.Interface.I2C):
            if(self._I2C.dataWaiting()):
                return True
        if(self._interface == self.Interface.NONE):
            raise ConfigError("No interface setup. Make sure a chosen interface has been setup.")
        return False

    ##Check how much data is waiting from TGAT##
    def dataWaiting(self):
        if(self._interface == self.Interface.UART):
            return self._UART.inWaiting()
        if(self._interface == self.Interface.I2C):
            return self._I2C.dataWaiting()
        if(self._interface == self.Interface.NONE):
            raise ConfigError("No interface setup. Make sure a chosen interface has been setup.")

    ##Read byte of data waiting from EEG sensor##
    def readEEGSensor(self):
        if(self._interface == self.Interface.UART):
            return self._decodeByte(self._UART.read())
        if(self._interface == self.Interface.I2C):
            return self._I2C.readRegister(self._I2C.registers.RHR)
        if(self._interface == self.Interface.NONE):
            raise ConfigError("No interface setup. Make sure a chosen interface has been setup.")

    ##Set the EEG sensor operating mode##
    def setMode(self, output_mode):
        #Set EEG sensor mode using UART interface#
        if(self._interface == self.Interface.UART):
            if(output_mode == self.OutputMode.MODE_REDUCED):
                self._UART.write([0x01])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_1_2K)
                self._UART.write([0x01])
            if(output_mode == self.OutputMode.MODE_BASIC):
                self._UART.write([0x00])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_9_6K)
                self._UART.write([0x00])
            if(output_mode == self.OutputMode.MODE_EEG_RAW):
                self._UART.write([0x02])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_57_6K)
                self._UART.write([0x02])
            if(output_mode == self.OutputMode.MODE_FFT):
                self._UART.write([0x03])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_57_6K)
                self._UART.write([0x03])
#	    ##If mode fails, retry##
#	    if(self.isWaiting() == False):
#		time.sleep(.300)
#		self.setMode(output_mode)

        #Set EEG sensor mode using I2C interface#
        if(self._interface == self.Interface.I2C):
            self._I2C.writeRegister(self._I2C.registers.LCR, 0x03) #UART Attributes - no parity, 8 databits, 1 stop bit
            self._I2C.writeRegister(self._I2C.registers.FCR, 0x07) #Fifo control - Enable + Reset RX + TX
            #sc.writeRegister(sc.registers.THR, 0x02) #
            if(output_mode == self.OutputMode.MODE_REDUCED):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x01)
                self._I2C.setBaudrate(self.Baudrate.BAUD_1_2K)
            if(output_mode == self.OutputMode.MODE_BASIC):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x00)
                self._I2C.setBaudrate(self.Baudrate.BAUD_9_6K)
            if(output_mode == self.OutputMode.MODE_EEG_RAW):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x2)
                self._I2C.setBaudrate(self.Baudrate.BAUD_57_6K)
            if(output_mode == self.OutputMode.MODE_FFT):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x3)
                self._I2C.setBaudrate(self.Baudrate.BAUD_57_6K)

#	    if(self.isWaiting() == False):
#		time.sleep(.300)
#		self.setMode(output_mode)

        if(self._interface == self.Interface.NONE):
            raise ConfigError("No interface setup. Make sure a chosen interface has been setup.")

    def setBasicMode(self):
        self.setMode(self.OutputMode.MODE_BASIC)

    def setRawEEGMode(self):
        self.setMode(self.OutputMode.MODE_EEG_RAW)

    def setFFTMode(self):
        self.setMode(self.OutputMode.MODE_FFT)
            
    ##Decode data recieved over UART##
    def _decodeByte(self, byte):
        #return byte.decode('utf-8')
        return int((str(byte)).encode('hex'), 16)
