
#ifndef GIFDRAW_H
#define GIFDRAW_H



#include <TFT_eSPI.h>     // Include the library for the TFT display
#include <AnimatedGIF.h>

#include <vector>


#define BUFFER_SIZE 256   // Define buffer size as needed for your display/GIF processing
#define DISPLAY_WIDTH  tft.width()
#define DISPLAY_HEIGHT tft.height() 

extern TFT_eSPI tft;      // Declare 'tft' as an external variable to be defined elsewhere

extern uint16_t usTemp[][BUFFER_SIZE];  //supporting dma use 
extern bool dmaBuf;       

// Assuming GIFDraw uses specific parameters, declare them here
void GIFDraw(GIFDRAW *pDraw);  // Adjust parameters as needed



#endif