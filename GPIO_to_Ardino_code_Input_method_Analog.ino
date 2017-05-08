// Simple code to control linear actuators based on input from Raspberry pi GPIO pins
// Note actuators hooked up in a cascading circuit similar to the one found in 
// LaTech's Living with the Lab ENGR 121 fishtank project 
    // To find a better picture of the circuit see the switching of solenoid PowerPoint
    // at http://www2.latech.edu/~dehall/LWTL/ENGR121/notes/6_switching_of_solenoid.ppt
// - Code written by Andre Aguillard & Matt Reed

void setup() {
  analogReference(EXTERNAL);//This is so we can use 3.3V as a reference
  pinMode(7,OUTPUT);
  pinMode(12,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // Uncomment if you want to see the output of the analogRead pins:
//  Serial.println("Value at pin 2:"); Serial.print(analogRead(2));
//  Serial.println(analogRead(3));
  
  //Linked to GPIO pin 21
  if (analogRead(2)<512)
  {
      digitalWrite(7,HIGH);
  }
  else if(analogRead(2)>512){
      digitalWrite(7,LOW);
  }

  //Linked to GPIO pin 20
  if (analogRead(3)>512)
  {
      digitalWrite(12,HIGH);
  }
  else if(analogRead(3)<512){
      digitalWrite(12,LOW);
  }

}
