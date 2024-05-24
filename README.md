The read me is a mess at thsi point just ignore 



### Currently using this dataset 
[Office-Home Dataset](https://datasets.activeloop.ai/docs/ml/datasets/office-home-dataset/)
 
[Deeplake Documentation](https://docs.activeloop.ai/examples/dl)

Pretrained model reference 
https://au.mathworks.com/help/deeplearning/ug/pretrained-convolutional-neural-networks.html 
(we have resnet 18 atm)


The rogue text generator attempt see w10 tut for more info

https://pytorch.org/tutorials/intermediate/char_rnn_generation_tutorial.html



## Installing

These are for the dataset
Install deeplake 3.9.1 bc deeplake 3.9.2 needs libdeeplake 0.0.123 which aint available 
```
pip install libdeeplake
pip install deeplake==3.9.1
```
You might not have below
```
pip install torch
pip install torchvision

```


# Todo


For picoVoice Rhino need to create the speechToIntent commands currently just running taking photo if any intent is fulfilled 


Minor thing but running juptyer notebook from the python file would be nice probaly just convert to python file after training model 



## Notes 




Dataset(path='hub://activeloop/fashion-mnist-train', read_only=True, tensors=['images', 'labels'])

 tensor      htype          shape        dtype  compression
 -------    -------        -------      -------  ------- 
 images      image     (60000, 28, 28)   uint8     png   
 labels   class_label    (60000, 1)     uint32    None  

  
Dataset(path='hub://activeloop/office-home-domain-adaptation', read_only=True, tensors=['images', 'domain_categories', 'domain_objects'])

      tensor           htype                shape              dtype  compression
      -------         -------              -------            -------  ------- 
      images           image     (15588, 4:6500, 18:6000, 3)   uint8    jpeg   
 domain_categories  class_label          (15588, 1)           uint32    None   
  domain_objects    class_label          (15588, 1)           uint32    None  


#### Visualisation 
I thought this was a cool way to visualise the data 
[Deep lake visualisation](https://docs.activeloop.ai/technical-details/visualization)

# PicoVoice 
https://picovoice.ai/

This was a pain to get working because ubuntu 20 uses an older version of glibc. 
So had to use an older version of picoVoice. 
Essentially i have combined the wake word (porcupine) and speech to intent (rhino) from pico voice

#### Installing
there is requirements.txt install those versions 
#### Running 

```
python3 rhino_and_porcupine.py --rhino_context_path 'YOURPATH' --porcupine_keyword_paths 'YOURPATH grasshopper_linux.ppn'
```
Make sure to run from python demo folder

