from algorithms.utils import *
import copy
from sklearn.feature_extraction.image import extract_patches_2d

class oilPaint:
    def __init__(self, imagePath, imageData):
        self.utils_ = utils(imagePath)
        self.originalImage = imageData

    '''
    This function only accepts kernels with a mid point i.e 3x3, 5x5, 7x7, etc.
    '''
    def perform_oilPaint(self, kernelSize, intensityLevels):
        original_height, original_width, _ = np.shape(self.originalImage)
        # create an empty array to hold resulting data
        result = copy.deepcopy(self.originalImage)

        padding = kernelSize // 2

        #extract patches from the image
        patches = extract_patches_2d(self.originalImage, (kernelSize, kernelSize))

        intensity_values = []

        for currPatch in patches:
            intensity_values.append(self.calculate_new_pixel_value(np.array_split(currPatch.flatten(), (kernelSize * kernelSize)), intensityLevels))


        new_pixel_intensities = np.array(intensity_values).flatten().reshape(original_height - (padding * 2), original_width - (padding * 2), 3)

        result[padding: original_height - padding, padding: original_width - padding] = new_pixel_intensities
        return result

    def calculate_new_pixel_value(self, imagePatch, intensityLevels):
        intensityLevels_bin, averageB, averageG, averageR = np.zeros(256), np.zeros(256), np.zeros(256), np.zeros(256)

        for pxl in range(len(imagePatch)):
            curIntensity = (int)((((imagePatch[pxl][0] + imagePatch[pxl][1] + imagePatch[pxl][2]) / 3) * intensityLevels) / 255)
            intensityLevels_bin[curIntensity] += 1
            averageB[curIntensity] += imagePatch[pxl][0]
            averageG[curIntensity] += imagePatch[pxl][1]
            averageR[curIntensity] += imagePatch[pxl][2]

        # find the max intensity and its index
        maxIntensity = max(intensityLevels_bin)
        maxIndex = intensityLevels_bin.argmax()


        # return new value of the pixel
        final_pixel = np.array([averageB[maxIndex]/maxIntensity, averageG[maxIndex]/maxIntensity, averageR[maxIndex]/maxIntensity], dtype=np.uint8)
        # clipping values
        final_pixel[final_pixel > 255] = 255

        return final_pixel