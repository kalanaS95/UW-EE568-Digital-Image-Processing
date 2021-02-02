import numpy as np
import cv2
import random
import copy

class Q2():
    def __init__(self):
        self.ImageData = self.load_imgae_data("../4_3.bmp")
        self.noisy_Image = self.addNoise(self.ImageData)

    def load_imgae_data(self, path):
        return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    def display_Image(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def addNoise(self, Image):
        height, width = np.shape(Image)
        fifteenPercent_pixels = int(((height * width) * 15)/100)
        fiftyPercent_black = int((fifteenPercent_pixels * 50)/100)
        fiftyPercent_white = int((fifteenPercent_pixels - fiftyPercent_black))

        # counters
        black_counter = 0
        white_counter = 0

        # selected rows
        combinations = []

        # adding 50% black pixels to the selected 15% of pixels
        while(fiftyPercent_black >= black_counter):
            # randomly pick a row and randomly pick a column
            row = random.randint(0, height - 1)
            col = random.randint(0, width - 1)
            if([row, col] not in combinations):
                Image[row][col] = 0
                combinations.append([row, col])
                black_counter += 1

        # adding 50% white pixels to the selected 15% of pixels
        while(fiftyPercent_white >= white_counter):
            # randomly pick a row and randomly pick a column
            row = random.randint(0, height - 1)
            col = random.randint(0, width - 1)
            if([row, col] not in combinations):
                Image[row][col] = 255
                combinations.append([row, col])
                white_counter += 1

        print("Salt and Peper Successfully added\n")
        return Image

    def medianFilter(self, noisyImage):

        #make a deep copy of the noisy image
        noisyImage_cpy = copy.deepcopy(noisyImage)

        height, width = np.shape(noisyImage_cpy)
        median_image = np.zeros([height, width])

        for i in range(1, height - 1):
            for j in range(1, width - 1):
                data = [noisyImage_cpy[i - 1, j - 1], noisyImage_cpy[i - 1, j], noisyImage_cpy[i - 1, j + 1],noisyImage_cpy[i, j - 1], noisyImage_cpy[i, j], noisyImage_cpy[i, j + 1], noisyImage_cpy[i + 1, j - 1], noisyImage_cpy[i + 1, j], noisyImage_cpy[i + 1, j + 1]]
                data = sorted(data)
                median_image[i, j] = data[4]

        return median_image.astype(np.uint8)

    def averagingFilter(self, noisyImage):
        # make a deep copy of the noisy image
        noisyImage_cpy = copy.deepcopy(noisyImage)

        height, width = np.shape(noisyImage_cpy)
        average_image = np.zeros([height, width])

        # making a 3x3 averaging filter mask
        m = (np.ones([3, 3], dtype = np.uint8))/9

        # applying the 3x3 averaging filter mask over the noisy image
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                data = noisyImage_cpy[i - 1, j - 1] * m[0, 0] + noisyImage_cpy[i - 1, j] * m[0, 1] + noisyImage_cpy[i - 1, j + 1] * m[0, 2] + \
                       noisyImage_cpy[i, j - 1] * m[1, 0] + noisyImage_cpy[i, j] * m[1, 1] + noisyImage_cpy[i, j + 1] * m[1, 2] + noisyImage_cpy[
                           i + 1, j - 1] * m[2, 0] + noisyImage_cpy[i + 1, j] * m[2, 1] + noisyImage_cpy[i + 1, j + 1] * m[2, 2]

                average_image[i, j] = data

        return average_image.astype(np.uint8)

def main():

    Q2_ = Q2()
    #Q2_.display_Image("Test", Q2_.ImageData)
    Q2_.display_Image("Noised", Q2_.noisy_Image)
    Q2_.display_Image("Median Filter", Q2_.medianFilter(Q2_.noisy_Image))
    Q2_.display_Image("Averaging Filter", Q2_.averagingFilter(Q2_.noisy_Image))

if __name__ == "__main__":
    main()