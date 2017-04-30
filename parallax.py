import RPi.GPIO as GPIO
import serial
from tkinter import *       ### This is to set up a GUI for the lock.

### GUI for the Lock:
class GUI4Lock(Frame):
  def __init__(self, master):
    Frame.__init__(self,master) ### This sets up the main window of the GUI
    self.master = master     ### in order to build widgets on to top it.
      
  def setupGUI(self):
    l1 = Label(self.master, text="{}".format(RESPONSE))
    l1.pack(side=LEFT, expand=1)
    e1 = Entry  (self.master)
    e1.pack(side=LEFT, expand=1)
    b1 = Button(self.master, width=5, height=5, text="1")
    b1.pack()
    b2 = Button(self.master, text="2", width=5, height=5,)
    b2.pack(side=RIGHT, expand=0)

window = Tk()
window.title("Better Bike Lock Home")
t = GUI4Lock(window)
t.setupGUI()
window.mainloop()

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
      
# Assigns a code to a lock
def assignLock(code):
    ## The code for the lock is the key in the dictionary and the empty lock number
    ## becomes the value paired with it.
    locks[code] = emptyLocks[0]
    # If we assign a lock, we must then open that lock for the user to use.
    #openLock(emptyLocks[0])
    del emptyLocks[0]
    
# Checks to see if there are any open locks
def checkLocks():
    # If there are no empty locks, then there's nothing else to do.
    if (emptyLocks == []):
        response = "Sorry there are no empty locks at this time, \
                    please try again later."
    # If there are emptylocks, then assign a lock
    else:
        assignLock(code)
        response = "Assigning you a lock..."
    print response

# Unlocks a lock and adds a that lock back to the list of empty locks
def openLock(code):
    pass
    
def main():
    # Initialize the Raspberry Pi by quashing any warnings and telling it
    # we're going to use the BCM pin numbering scheme.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # This pin corresponds to GPIO18, which we'll use to turn the RFID
    # reader on and off with.
    GPIO.setup(ENABLE_PIN, GPIO.OUT)
    
    # Next we'll create a list generated from the number of locks in the
    # system, and use that to link them to GPIO pins from a list of available ones. 
    pins = [21,20,16,12,26,19,13,6,5,25,24,23]
    locksWithPins = {} # A dictionary to keep track of which pins are associated with
                       # which locks
    for x in range (1,NUMBER_OF_LOCKS+1):
      locksWithPins[x] = pin[0]
      GPIO.setup(pins[0], GPIO.OUT)
      del pins[0]
      
      
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
    emptyLocks = [x in range (1, len(NUMBER_OF_LOCKS + 1))]
    
    # Wrap everything in a try block to catch any exceptions.
    try:
        # Loop forever, or until CTRL-C is pressed.
        while 1:
            # Read in 12 bytes from the serial port.
            data = ser.read(12)
            RESPONSE = "To get a bike lock, please scan your card above or type in your ID."
            print (RESPONSE)
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
                  print response
                #If its a new code, check to see if there are any open locks
                else:
                  checkLocks(code)
                  response = "Checking for open locks..."
                  print (response)
                                  
    except:
        # If we caught an exception, then disable the reader by setting
        # the pin to HIGH, then exit.
        print("Disabling RFID reader...")
        GPIO.output(ENABLE_PIN, GPIO.HIGH)

        
if __name__ == "__main__":
    main()

   
