# Report 

This is just a quick brief on the project. There are a few sections to the project 
- The object detection and its attempts
- The wake word and speech to intent engine (picovoice - rhino and porcupine)
- the esp32 and serial sending
- The voice and photo taking 

Firstly i would like to say this project differes considerably from the teaser video mainly because i realised that I wouldn't have the processing power to reasonably train 
a model from scratch and transfer learning would yeild subpar or on par in more specific circumstances making it not an exciting project. 

In the training folder there is some old attempts at image classification and object detection I was able to subdivide the datasets and prepeare them for training. 
Training however was not feasible with my cpu even on just a small set of catagories to overfit for a few specific objects. 
Was still very interesting learning how deeplake prepeares datasets for training and how the models are trained especially using pretrained models.   

I also became interested in lstm for rnn and thought it could be interested to train a character generator for the determiners of the list of nouns that was produced from the object detection. (determining a, an , and or blank for plurals) 
It became clear however that i was still better off just using a simple function since there wernt many cases and the main difference was having multiple of the same objects or single as most objects determiner was 'a'. 



## Picovoice 
https://picovoice.ai/

Initially i wanted to use pico voice as it has the potential to be setup on a microcrontroller but this 
was a huge mistake. I was unable to install the latest version due to my version of linux so i had to downgrade 
picovoice which after a lot of trail and error turns out they don't allow you to train speech to intent or wake words on older versions. 
Overal it was just a pain and i should have used one of the audio feature detection or inferercne tutorials on pytorch. 

This is also why i say "make me an espresso" instead of take a photo or something. I was limited to the default template speech to intents. :(


## Esp32
This was entirely a side quest has a lot of potential for future projects. Will hopefully use pytorches audio tutorials to set up a speech to intent engine for it in the future

## The voice and photo taking
Nothing to remarkable here, its just basic python stuff and image resize for the model to understand 


