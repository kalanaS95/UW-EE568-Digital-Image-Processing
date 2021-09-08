from algorithms.utils import *
import copy
from numba import jit, cuda


'''
This function only accepts kernels with a mid point i.e 3x3, 5x5, 7x7, etc.
'''
def oil_paint(ImageData, kernelSize, intensityLevels):
    # add padding to the image
    padding_pixels = kernelSize // 2
    padded_Image =  np.pad(ImageData, ((padding_pixels,padding_pixels), (padding_pixels,padding_pixels), (0, 0)), 'constant')
    return perform_oilPaint(padded_Image, padding_pixels, intensityLevels)


@jit(nopython=True)
def perform_oilPaint(originalImage, padding_pixels, intensityLevels):
    original_height, original_width, _ = np.shape(originalImage)
    # create an empty array to hold resulting data
    result = np.zeros((original_height, original_width,3), dtype=np.uint8)

    for row in range(padding_pixels, original_height - padding_pixels):
        for col in range(padding_pixels, original_width - padding_pixels):
            result[row][col] = calculate_new_pixel_value(originalImage[row - padding_pixels:row + padding_pixels + 1, col - padding_pixels:col + padding_pixels + 1], intensityLevels)

    # finally we remove the padding pixels and return
    return result[padding_pixels:original_height - padding_pixels, padding_pixels:original_width - padding_pixels, :]

@jit(nopython=True)
def calculate_new_pixel_value(imagePatch, intensityLevels):
    patch_height, patch_width, _ = np.shape(imagePatch)
    intensityLevels_bin, averageB, averageG, averageR = np.zeros(256), np.zeros(256), np.zeros(256), np.zeros(256)

    for row in range(patch_height):
        for col in range(patch_width):
            curIntensity = (int)((((imagePatch[row][col][0] + imagePatch[row][col][1] + imagePatch[row][col][
                2]) / 3) * intensityLevels) / 255)
            #print(curIntensity)
            intensityLevels_bin[curIntensity] += 1
            averageB[curIntensity] += imagePatch[row][col][0]
            averageG[curIntensity] += imagePatch[row][col][1]
            averageR[curIntensity] += imagePatch[row][col][2]

    # find the max intensity and its index
    maxIntensity = max(intensityLevels_bin)
    maxIndex = intensityLevels_bin.argmax()

    # return new value of the pixel
    final_pixel = np.array(
        [averageB[maxIndex] / maxIntensity, averageG[maxIndex] / maxIntensity, averageR[maxIndex] / maxIntensity])
    # clipping values
    final_pixel[final_pixel > 255] = 255

    return final_pixel

