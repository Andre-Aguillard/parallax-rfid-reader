import RPi.GPIO as GPIO
import serial
from Tkinter import *       ### This is to set up a GUI for the lock.
from time import sleep 

### GUI for the Lock:
class GUI4Lock(Frame):
  def __init__(self, master):
    Frame.__init__(self,master) ### This sets up the main window of the GUI
    self.master = master     ### in order to build widgets on to top it.
      
  def setupGUI(self): # - Santiago
        #organize the GUI
        # this function works fine, as long as you have the images as actual GIFs
        self.pack(fill=BOTH, expand=1)
        #setup the player input at the bottom of the GUI
        #widget is a Tkinter Entry
        #background is white; bind return key to function process in class
        GUI4Lock.player_input = Entry(self, bg="white")
        GUI4Lock.player_input.bind("<Return>", self.process)
        GUI4Lock.player_input.pack(side=BOTTOM, fill=X)
        GUI4Lock.player_input.focus()
        
        # setup image to the left of GUI
        # widget is a Tkinter label
        # don't let image control width's size
        img = None
        GUI4Lock.image = Label(self, width=WIDTH / 2, height=HEIGHT, image = img)
        GUI4Lock.image.image = img
        GUI4Lock.image.pack(side=LEFT, fill=Y)
        GUI4Lock.image.pack_propagate(False)
        
        # setup text to right of GUI
        # first, place frame where the text will be displayed
        text_frame = Frame(self, width=WIDTH / 2, height=HEIGHT)
        # widget - same deal as above
        # disable by default
        # don't let it control frame's size # is there any way to put the text in the middle? Having it to the left
        GUI4Lock.text = Text(text_frame, bg="lightgrey", state=DISABLED)
        GUI4Lock.text.pack(fill=Y, expand=1)
        text_frame.pack(side=RIGHT, fill=Y)
        text_frame.pack_propagate(False)

window = Tk()
window.title("Better Bike Lock Home")
t = GUI4Lock(window)
RESPONSE = "Andre"
t.setupGUI()
window.mainloop()

#Define variables

ENABLE_PIN  = 18              # The BCM pin number corresponding to GPIO1
SERIAL_PORT = '/dev/ttyAMA0'  # The location of our serial port.  This may
                              # vary depending on OS version.
  
NUMBER_OF_LOCKS = 2           #set the number of locks
OPEN_TIME = 10                ### Time that lock is open for

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
    openLock(code)
    #And since that lock is full, remove it from the list of open locks
    del emptyLocks[0]
    
# Checks to see if there are any open locks
def checkLocks(code):
    # If there are no empty locks, then there's nothing else to do.
    if (emptyLocks == []):
        response = "Sorry there are no empty locks at this time, \
                    please try again later."
    # If there are emptylocks, then assign a lock
    else:
        response = "Assigning you a lock..."
        print (response)
        assignLock(code)

# Unlocks a lock and adds a that lock back to the list of empty locks
def openLock(code):
    # Opens the locks
    print ("You have {} seconds to access your lock").format(OPEN_TIME)
    x = locks[code]
    print ("Opening lock")
    GPIO.output(locksWithPins[x], GPIO.HIGH)
    sleep(OPEN_TIME)
    print ("Cosing lock...") 
    GPIO.output(locksWithPins[x], GPIO.LOW)
    
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
    global locksWithPins
    locksWithPins = {} # A dictionary to keep track of which pins are associated with
                       # which locks
    for x in range (1,NUMBER_OF_LOCKS+1):
      locksWithPins[x] = pins[0]
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
    global locks
    locks = {}
    # Create a list of empty locks based initially off the number of locks -Aguillard
    # in the system
    global emptyLocks
    emptyLocks = [x in range (1,(NUMBER_OF_LOCKS + 1))]
    
    # Wrap everything in a try block to catch any exceptions.
##    try:
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
                #If code is in locks, then the person is unlocking their lock so open the lock
                openLock(code)
                #Since this is the second time the code is scanned, that lock is now free, and empty
                emptyLocks.append (locks[code])
                # And it also is no longer associated with a code. 
                del locks[code]
                # Set the response. 
                ## The response will be display on the GUI once that is finished
                response = "Thank you for using a better bike lock, \n \
                        We appreciate your business. Have a great day!"
                print response
              #If its a new code, check to see if there are any open locks
              else:
                response = "Checking for open locks..."
                print (response)
                checkLocks(code)
                print "Thank you."
                                  
##    except:
##        # If we caught an exception, then disable the reader by setting
##        # the pin to HIGH, then exit.
##        print("Disabling RFID reader...")
##        GPIO.output(ENABLE_PIN, GPIO.HIGH)

        
if __name__ == "__main__":
    main()
