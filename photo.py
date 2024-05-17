import pygame 
import pygame.camera 

from PIL import Image, ImageFilter

from gtts import gTTS
import os


newJpg = 'camPhotoInitial.jpg'
finalJpg = 'resizedCamOutput.jpg'

def photoMain():
    takePhoto()
    resized_image = resizeImage(newJpg, 600, 600)
    resized_image.save(finalJpg) 

#for reformating the categorys comes in ['x','y']
def textReformater(category_names):
    category_counts = {}
    for category in category_names:
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    # Replace duplicated categories with the count
    result = []
    for category, count in category_counts.items():
        if count > 1:
            result.append(f"{count} {category}s")
        else:
            result.append(category)

    # Join the elements in the list with a comma and space
    result_string = ' and '.join(result)
    frontText = "In this image i see a "
    return(frontText + result_string)


def textToSpeech(text):

    # Create a gTTS object
    tts = gTTS(text=text, lang="en", slow=False)

    # Save the speech as a file
    tts.save("output.mp3")

    # Play the speech
    os.system("mpg321 output.mp3")  


#designed so that the ratio is kept the same by cropping the longer side
def resizeImage(image_path, target_width, target_height):
    # Open the image
    img = Image.open(image_path)
    
    # Calculate the aspect ratio of the original image
    original_width, original_height = img.size
    original_aspect_ratio = original_width / original_height
    
    # Calculate the aspect ratio of the target dimensions
    target_aspect_ratio = target_width / target_height
    
    # Determine which side to crop
    if original_aspect_ratio > target_aspect_ratio:
        # Original image is wider, crop the sides
        new_width = int(original_height * target_aspect_ratio)
        left = (original_width - new_width) / 2
        upper = 0
        right = left + new_width
        lower = original_height
    else:
        # Original image is taller, crop the top and bottom
        new_height = int(original_width / target_aspect_ratio)
        left = 0
        upper = (original_height - new_height) / 3
        right = original_width
        lower = upper + new_height
    
    # Crop the image
    cropped_img = img.crop((left, upper, right, lower))
    
    # Resize the cropped image to the target dimensions
    resized_img = cropped_img.resize((target_width, target_height))
    
    return resized_img

def takePhoto():
    # initializing  the camera 
    pygame.camera.init() 
    
    # make the list of all available cameras 
    camlist = pygame.camera.list_cameras() 
    
    # if camera is detected or not 
    if camlist: 
        # initializing the cam variable with default camera 
        cam = pygame.camera.Camera(camlist[0], (640, 480)) 
    
        # opening the camera 
        cam.start() 
    
        # capturing the single image 
        image = cam.get_image() 
    
        # saving the image 
        pygame.image.save(image, newJpg) 
        
        cam.stop()
    # if camera is not detected the moving to else part 
    else: 
        print("No camera on current device") 

if __name__ == "__main__":
    photoMain() 
