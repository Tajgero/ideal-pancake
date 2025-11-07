import tensorflow as tf
import numpy as np
import sys
import cv2
import os


def load_images(folder):
    images_path = []
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            images_path.append(os.path.join(folder, file))
    return images_path


def load_preprocessed_images(folder, img_width, img_height):
    images = load_images(folder)
    processed_images = []
    for image in images:
        processed_image = preprocess(image, img_width, img_height)
        processed_images.append(processed_image)
    return processed_images, images


def preprocess(file_path, img_width, img_height):
    """Preprocessing image"""
    
    # Modifies image
    img = cv2.imread(file_path)
    img = cv2.resize(img, (img_width, img_height))
    img = np.expand_dims(img, 0)
    
    return img


if __name__ == "__main__":
    """
    Tries to predict simple image with given model trained on
    GTSRB data set
    """
    
    classes_gtsrb = { 
        0:'Speed limit (20km/h)',
        1:'Speed limit (30km/h)', 
        2:'Speed limit (50km/h)', 
        3:'Speed limit (60km/h)', 
        4:'Speed limit (70km/h)', 
        5:'Speed limit (80km/h)', 
        6:'End of speed limit (80km/h)', 
        7:'Speed limit (100km/h)', 
        8:'Speed limit (120km/h)', 
        9:'No passing', 
        10:'No passing veh over 3.5 tons', 
        11:'Right-of-way at intersection', 
        12:'Priority road', 
        13:'Yield',
        14:'Stop', 
        15:'No vehicles', 
        16:'Veh > 3.5 tons prohibited', 
        17:'No entry', 
        18:'General caution', 
        19:'Dangerous curve left', 
        20:'Dangerous curve right', 
        21:'Double curve', 
        22:'Bumpy road', 
        23:'Slippery road', 
        24:'Road narrows on the right', 
        25:'Road work', 
        26:'Traffic signals', 
        27:'Pedestrians', 
        28:'Children crossing', 
        29:'Bicycles crossing', 
        30:'Beware of ice/snow',
        31:'Wild animals crossing', 
        32:'End speed + passing limits', 
        33:'Turn right ahead', 
        34:'Turn left ahead', 
        35:'Ahead only', 
        36:'Go straight or right', 
        37:'Go straight or left', 
        38:'Keep right', 
        39:'Keep left', 
        40:'Roundabout mandatory', 
        41:'End of no passing', 
        42:'End no passing veh > 3.5 tons'
    }

    IMG_WIDTH = 30
    IMG_HEIGHT = 30
    
    if len(sys.argv) != 2:
        sys.exit("Usage: python predict_traffic.py model")
        
    # Load model
    model = tf.keras.models.load_model(sys.argv[1])
    
    # Load preprocessed images
    images, images_path = load_preprocessed_images("images", IMG_WIDTH, IMG_HEIGHT)
        
    # Predictions
    for image, image_path in zip(images, images_path):
        prediction = model.predict(image).argmax()
        name = classes_gtsrb[prediction]
        print("=" * 10)
        print(f"Prediction of {os.path.basename(image_path)}:")
        print(name)
        print("=" * 10)
