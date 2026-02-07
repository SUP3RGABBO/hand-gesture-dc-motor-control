int speedPin = 5; 
int dir1 = 4;
int dir2 = 3;

int ledRed = 9;
int ledOrange = 10;
int ledGreen = 11;

int speed = 0;

void setup() {
  pinMode(speedPin, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);

  pinMode(ledRed, OUTPUT);
  pinMode(ledOrange, OUTPUT);
  pinMode(ledGreen, OUTPUT);

  // Direzione avanti
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, LOW);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    bool isNumber = true;
    for (int i = 0; i < command.length(); i++) {
      if (!isDigit(command[i])) {
        isNumber = false;
        break;
      }
    }

    if (isNumber) {
      speed = command.toInt();
      if (speed < 0) speed = 0;
      if (speed > 255) speed = 255;

      analogWrite(speedPin, speed);

     
      if (speed <= 85) {
        digitalWrite(ledRed, HIGH);
        digitalWrite(ledOrange, LOW);
        digitalWrite(ledGreen, LOW);
      } else if (speed <= 170) {
        digitalWrite(ledRed, LOW);
        digitalWrite(ledOrange, HIGH);
        digitalWrite(ledGreen, LOW);
      } else {
        digitalWrite(ledRed, LOW);
        digitalWrite(ledOrange, LOW);
        digitalWrite(ledGreen, HIGH);
      }
    }
  }
}
