import cv2
import numpy as np
import os

def colorize_image(input_image):
    dir = r"C:\Users\rakam\OneDrive\Desktop\Major Project"
    prototxt = os.path.join(dir, r"requriements\colorization_deploy_v2.prototxt")
    points = os.path.join(dir, r"requirements/pts_in_hull.npy")
    model = os.path.join(dir, r"requirements/colorization_release_v2.caffemodel")

    # Load the model
    net = cv2.dnn.readNetFromCaffe(prototxt, model)
    pts = np.load(points)

    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    # Process the input image directly
    scaled = input_image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2LAB)

    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # Colorize the image
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (input_image.shape[1], input_image.shape[0]))
    L = cv2.split(lab)[0]
    ab[:, :, 0] += 1
    ab[:, :, 1] -= 10 
    
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2RGB)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")

    return colorized
