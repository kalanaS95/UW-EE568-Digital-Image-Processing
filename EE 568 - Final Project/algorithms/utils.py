import cv2
import numpy as np

class utils:
    def __init__(self, imagePath):
        self.Imagepath = imagePath

    def load_image_data(self):
        return cv2.imread(self.Imagepath, cv2.IMREAD_COLOR)

    def display_Image(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def convert_to_grayScale(self, ImageData):
        return cv2.cvtColor(ImageData, cv2.COLOR_BGR2GRAY)

    def image_negative(self, ImageData):
        return 255 - ImageData


