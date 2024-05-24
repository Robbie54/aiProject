//https://www.robotics.org.za/ESP32-DEV-CH340-C
//https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf


#include <gpio_viewer.h>
GPIOViewer gpio_viewer;


#include <ESP32Servo.h>

#include <Wire.h>
#include <string.h>
#include <SPI.h>
#include <TFT_eSPI.h>       
#include <AnimatedGIF.h>  

#include "GifDraw.h"


#include <vector>

// Examples images
#include "images/otherGIFs/hyperspace.h"
#include "images/otherGIFs/x_wing.h"
#include "images/otherGIFs/colortest.h"


#include "images/Afraid.h"
#include "images/Angry.h"
#include "images/Disdain.h"
#include "images/Excited.h"
#include "images/LookLeft.h"
#include "images/LookRight.h"
#include "images/Sad.h"
#include "images/Static.h"

TFT_eSPI tft = TFT_eSPI();
AnimatedGIF gif;

Servo myServo;
int servoPin = 23; 
int potPin = 35; 
int ADC_Max = 4096;

#define DISPLAY_WIDTH  tft.width()
#define DISPLAY_HEIGHT tft.height()
#define BUFFER_SIZE 256            // Optimum is >= GIF width or integral division of width

#ifdef USE_DMA
  uint16_t usTemp[2][BUFFER_SIZE]; // Global to support DMA use
#else
  uint16_t usTemp[1][BUFFER_SIZE];    // Global to support DMA use
#endif
bool     dmaBuf = 0;
  

void gifPlayer(const std::vector<std::pair<const uint8_t*, size_t>> gifImages){

  // Loop through each GIF
  for (int i = 0; i < gifImages.size(); i++) {
    if (gif.open((uint8_t *)gifImages[i].first, gifImages[i].second, GIFDraw))
    {
      // Serial.printf("Successfully opened GIF; Canvas size = %d x %d\n", gif.getCanvasWidth(), gif.getCanvasHeight());
      tft.startWrite();
      while (gif.playFrame(true, NULL))
      {
        yield();
      }
      gif.close();
      tft.endWrite(); 
    }
  }
}

void setup() {
  Serial.begin(115200);
 
  // gpio_viewer.connectToWifi("Red Earth", "Uluru2020");


  tft.begin();
  tft.setRotation(2);     // Adjust Rotation of your screen (0-3)
  tft.fillScreen(TFT_BLACK);
  gif.begin(BIG_ENDIAN_PIXELS);

  pinMode(13, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
  pinMode(27, INPUT_PULLUP);
  pinMode(26, INPUT_PULLUP);
  pinMode(25, INPUT_PULLUP);
  pinMode(33, INPUT_PULLUP);

  // Allow allocation of all timers
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  myServo.setPeriodHertz(50);// Standard 50hz servo
  myServo.attach(servoPin, 500, 2400);   // attaches the servo on pin 18 to the servo object
                                         // using SG90 servo min/max of 500us and 2400us
                                         

  // gpio_viewer.begin();
}

void loop()
{

    std::vector<std::pair<const uint8_t*, size_t>> angryGif = {
        {Angry1, sizeof(Angry1)},
        {Angry2, sizeof(Angry2)},
        {Angry3, sizeof(Angry3)}
    };
    
    std::vector<std::pair<const uint8_t*, size_t>> disdainGif = {
        {Disdain1, sizeof(Disdain1)},
        {Disdain2, sizeof(Disdain2)},
        {Disdain3, sizeof(Disdain3)}
    };

    std::vector<std::pair<const uint8_t*, size_t>> excitedGif = {
        {Excited1, sizeof(Excited1)},
        // {Excited2, sizeof(Excited2)},
        {Excited3, sizeof(Excited3)}
    };

    std::vector<std::pair<const uint8_t*, size_t>> lookLeftGif = {
        {LookLeft1, sizeof(LookLeft1)},
        {LookLeft2, sizeof(LookLeft2)},
        {LookLeft3, sizeof(LookLeft3)}
    };

    std::vector<std::pair<const uint8_t*, size_t>> lookRightGif = {
        {LookRight1, sizeof(LookRight1)},
        {LookRight2, sizeof(LookRight2)},
        {LookRight3, sizeof(LookRight3)}
    };

    std::vector<std::pair<const uint8_t*, size_t>> sadGif = {
        {Sad1, sizeof(Sad1)},
        {Sad2, sizeof(Sad2)},
        {Sad3, sizeof(Sad3)}
    };

    std::vector<std::pair<const uint8_t*, size_t>> staticGif = {
        {defaultFace, sizeof(defaultFace)},
    };

    std::vector<std::pair<const uint8_t*, size_t>> singleBlinkGif = {
        {SingleBlink, sizeof(SingleBlink)},
    };

  
  // std::vector<const uint8_t*> staticGif = {defaultFace, SingleBlink, DoubleBlink};
  // const uint8_t* e = Excited2;
  int potVal = analogRead(potPin);
  potVal = map(potVal, 0, ADC_Max, 0, 180);
  myServo.write(potVal);

  int buttonState1 = digitalRead(13); //look left
  int buttonState2 = digitalRead(14);// right 
  int buttonState3 = digitalRead(27); //blink
  int buttonState4 = digitalRead(26); //angry 
  int buttonState5 = digitalRead(25); //excited 
  int buttonState6 = digitalRead(33); //sad
  char input;
  if(Serial.available()){
        input = Serial.read();
        // Serial.print("You typed: " );
        // Serial.println(input);
           if (input == '1') {
        buttonState1 = LOW;
        }
        if (input == '2') {
            buttonState2 = LOW;
        }
        if (input == '3') {
            buttonState3 = LOW;
        }
        if (input == '4') {
            buttonState4 = LOW;
        }
        if (input == '5') {
            buttonState5 = LOW;
        }
        if (input == '6') {
            buttonState6 = LOW;
        }
    }

  if(buttonState1 == LOW){
    gifPlayer(lookLeftGif);
  }
  else if(buttonState2 == LOW){
    gifPlayer(lookRightGif);
  }
  else if(buttonState3 == LOW){
    gifPlayer(singleBlinkGif);
  }
  else if(buttonState4 == LOW){
    gifPlayer(angryGif);
  }
   else if(buttonState5 == LOW){
    gifPlayer(excitedGif);
  }
   else if(buttonState6 == LOW){
    gifPlayer(sadGif);
  }
  else{
    staticGif;
  }

}