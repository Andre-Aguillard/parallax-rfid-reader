#! /usr/bin/env python3

import RPi.GPIO as GPIO
import serial
from tkinter import *       ### This is to set up a GUI for the lock.

### GUI for the Lock:
class GUI4Lock(Frame):
  def __init__(self, master):
    Frame.__init__(self,master) ### This sets up the main window of the GUI
       self.master = master     ### in order to build widgets on to pof it.
      
  def setupGUI(self):
    l1 = Label(self.master, text="Please scan your card above or enter your ID below.")
    l1.grid(row=0, column=0, sticky=E+W)
    img = PhotoImage(file="logo.jpg")
    l2 = Label(self.master image=image)
    l2.image= img
    l2.grid
    e1 = Entry  (self.master)
    e1.grid(row=1, column=1, sticky=W)

window = Tk()
window.title("Better Bike Lock Home")


#Define variables

ENABLE_PIN  = 18              # The BCM pin number corresponding to GPIO1
SERIAL_PORT = '/dev/ttyAMA0'  # The location of our serial port.  This may
                              # vary depending on OS version.
  
NUMBER_OF_LOCKS = 2           #set the number of locks

def validate_rfid(code):
    # A valid code will be 12 characters long with the first char being
    # a line feed and the last char being a carriage return.
    s = code.decode("ascii")

    if (len(s) == 12) and (s[0] == "\n") and (s[11] == "\r"):
        # We matched a valid code.  Strip off the "\n" and "\r" and just
        # return the RFID code.
        return s[1:-1]
    else:
        # We didn't match a valid code, so return False.
        return False

    
def main():
    # Initialize the Raspberry Pi by quashing any warnings and telling it
    # we're going to use the BCM pin numbering scheme.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # This pin corresponds to GPIO18, which we'll use to turn the RFID
    # reader on and off with.
    GPIO.setup(ENABLE_PIN, GPIO.OUT)

    # Setting the pin to LOW will turn the reader on.  You should notice
    # the green LED light on the reader turn red if successfully enabled.

    print("Enabling RFID reader...\n")
    GPIO.output(ENABLE_PIN, GPIO.LOW)

    # Set up the serial port as per the Parallax reader's datasheet.
    ser = serial.Serial(baudrate = 2400,
                        bytesize = serial.EIGHTBITS,
                        parity   = serial.PARITY_NONE,
                        port     = SERIAL_PORT,
                        stopbits = serial.STOPBITS_ONE,
                        timeout  = 1)
    
    # Create a dictionary that associates the bike lock number with a code -Aguillard
    locks{}
    # Create a list of empty locks based initially off the number of locks -Aguillard
    # in the system
    emptyLocks = [x in range len(1,NUMBER_OF_LOCKS+1)]
    
# Assigns a code to a lock
def assignLock(code):
    locks[code] = emptyLocks[0]
    # If we assign a lock, we must then open that lock for the user to use.
    #openLock(emptyLocks[0])
    del emptyLocks[0]
    
    
# Checks to see if there are any open locks
def checkLocks():
    # If there are no empty locks, then there's nothing else to do.
    if (emptyLocks = []):
        response = "Sorry there are no empty locks at this time, \
                    please try again later."
    # If there are emptylocks, then assign a lock
    else:
        assignLock(code)
        response = "Assigning you a lock..."
        
        
    
  
# Unlocks a lock and adds a that lock back to the list of empty locks
def unlockLock(code):
    pass

    # Wrap everything in a try block to catch any exceptions.
    try:
        # Loop forever, or until CTRL-C is pressed.
        while 1:
            # Read in 12 bytes from the serial port.
            data = ser.read(12)

            # Attempt to validate the data we just read.
            code = validate_rfid(data)
            
            # If validate_rfid() returned a code, display it.
            if code:
                print("Read RFID code: " + code);
                #check to see if the 
                if (code in locks) :
                  unlockLock(code)
                  # Set the response. 
                  ## The response will be display on the GUI once that is finished
                  response = "Thank you for using a better bike lock, \
                          We appreciate your business. Have a great day!"
                #If its a new code, check to see if there are any open locks
                else:
                  checkLocks(code)
                  response = "Checking for open locks..."
                
    except:
        # If we caught an exception, then disable the reader by setting
        # the pin to HIGH, then exit.
        print("Disabling RFID reader...")
        GPIO.output(ENABLE_PIN, GPIO.HIGH)

        
if __name__ == "__main__":
    main()

   
