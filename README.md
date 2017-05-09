### Note to Dr. Gourd:
To view the final code please see the <b>Working Code.py</b> file.  
  
To just view the GUI and Manual code method, download the <b>bikelock.gif</b> and <b>WorkingCode-GUIandManual_Input.py</b> files   
These should function on any computer that has python with the Tkinter module.   
  
![Alt text](GUI_Home_example.PNG)
Picture of GUI ^


#### Louisiana Tech Engineering HNRS 122- H05 Final Project
## Lock Control System 
#### Project Title: Better Bike Lock   

A simple Python script for reading codes from the Parallax RFID Reader 28140 (Serial port version) was forked from github user cspenscer.
This code was then modified and built upon to meet the needs of our project, it's much more complex now. 

##### Project Description: 
We used a Raspberry Pi 3 to serve as the main control for the program and the <b>Working Code.py</b> file is the one which contains the most up to date and functioning code. The system takes in user input either from an RFID (Radio Frequency Identificatoin) enabled card or manually from a keypad built into the GUI. This input is then stored as a key in a dictionary and used to control the opening and closing of the locks. Initially, the code is stored, a lock assigned, and then the lock is opened and closed. After the code is entered a second time, the lock is opened and then that key:value pair is cleared from the dictionary. 

##### Project Materials: 
  * Raspberry Pi 3
  * 7in LCD touchscreen display
  * Arduino Uno
  * 2 SPST relays
  * 2 transistors
  * 2 Linear Actuators 
  * A 18" x 24" sheet of Acrylic cut into a box to house the electrical components

Elements that were added to cspencer's original code include: 

* A GUI which includes, buttons, a text box message display, and a logo picture. 
* A locking method that takes in input from RFID and manual sources.
