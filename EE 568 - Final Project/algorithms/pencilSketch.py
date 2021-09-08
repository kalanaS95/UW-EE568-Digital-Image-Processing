import numpy as np
from algorithms.utils import *


class pencilSketch:
    def __init__(self, imageData, imagepath):
        self.originalImage = imageData
        self.utils_ = utils(imagepath)
        self.grayScaleImage = self.utils_.convert_to_grayScale(self.originalImage)
        self.negativeImage = self.utils_.image_negative(self.grayScaleImage)

    def dnorm(self, x, mu, sd):
        return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)

    def gaussian_kernel(self, kernel_size, sigma=1):
        kernel_1D = np.linspace(-(kernel_size // 2), kernel_size // 2, kernel_size)
        for i in range(kernel_size):
            kernel_1D[i] = self.dnorm(kernel_1D[i], 0, sigma)
        kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)

        kernel_2D *= 1.0 / kernel_2D.max()

        return kernel_2D

    '''
    This function only accepts kernels with a mid point i.e 3x3, 5x5, 7x7, etc.
    '''
    def gaussian_blur(self, kernel_size, sigma, imageData):
        kernel = self.gaussian_kernel(kernel_size, sigma)
        # add padding to the image
        padding_pixels = kernel_size // 2
        image_padded = np.pad(imageData, ((padding_pixels, padding_pixels), (padding_pixels, padding_pixels)), 'constant')
        padded_h, padded_w = np.shape(image_padded)

        for row in range(padding_pixels, padded_h - padding_pixels):
            for col in range(padding_pixels, padded_w - padding_pixels):
                newPixel_val = np.sum(image_padded[row - padding_pixels:row + padding_pixels + 1, col - padding_pixels:col + padding_pixels + 1] * kernel)/ np.sum(kernel)
                if(newPixel_val > 255):
                    newPixel_val = 255
                image_padded[row][col] = newPixel_val

        #finally we need to remove the extra padding and return the image data
        return image_padded[padding_pixels:padded_h - padding_pixels, padding_pixels:padded_w - padding_pixels]

    def pencil_sketch(self, kernel_size, sigma):
        gaussian_negative = self.gaussian_blur(kernel_size, sigma, self.negativeImage)
        return self.dodge(self.grayScaleImage, gaussian_negative)


    def dodge(self, grayscale, negative):
        height, width = np.shape(grayscale)
        result = np.zeros((height, width), np.uint8)

        for row in range(height):
            for col in range(width):
                if negative[row, col] == 255:
                    result[row, col] = 255
                else:
                    pix = (grayscale[row, col] << 8) / (255 - negative[row, col])
                    if pix > 255:
                        pix = 255
                    result[row, col] = pix

        return result