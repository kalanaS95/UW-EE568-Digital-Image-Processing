import numpy as np
import cv2
import copy


class Q1:
    def __init__(self, path):
        self.ImageData = self.load_imgae_data(path)
        self.filter = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        self.boosted = None

    def load_imgae_data(self, path):
        return cv2.imread(path, cv2.IMREAD_COLOR)

    def display_Image(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def perform_high_boost(self):
        ImageData_cpy = copy.deepcopy(self.ImageData)
        B, G, R = cv2.split(ImageData_cpy)

        B_ = self.high_boost(B)
        G_ = self.high_boost(G)
        R_ = self.high_boost(R)

        self.boosted = cv2.merge([B_, G_, R_])
        self.display_Image("Filter applied", self.boosted)

    def high_boost(self, ImageData):
        height, width = np.shape(ImageData)

        # figuring out the pixels we can get 3x3 patches
        start_row, end_row = 1, height - 1
        start_col, end_col = 1, width - 1

        # this variable will keep all the patches we extract from the bellow loop
        patches = []

        # now lets extract 3x3 patches
        for curr_row in range(start_row, end_row):
            for curr_col in range(start_col, end_col):
                patches.append(np.array([ImageData[curr_row - 1][curr_col - 1], ImageData[curr_row - 1][curr_col], ImageData[curr_row - 1][curr_col + 1],
                                ImageData[curr_row][curr_col - 1], ImageData[curr_row][curr_col], ImageData[curr_row][curr_col + 1],
                                ImageData[curr_row + 1][curr_col - 1], ImageData[curr_row + 1][curr_col], ImageData[curr_row + 1][curr_col + 1]]))

        # convert to np array and lets reshape it --> gives #pathes x 9 matrix
        patches = np.array(patches).reshape((height - 2) * (width - 2), 9)
        # now lets convert 3x3 filter into 9x1 matrix
        filter = self.filter.reshape(9,1)
        # then lets multiply these filter and patches matrix together
        result = np.matmul(patches, filter)
        # lets reshape the resulting matrix
        result = result.reshape(height - 2, width - 2)
        # Normalize intensities between 0-1
        result = result / 255
        # Clip any negative values to 0, and values > 1 to 1
        result[result < 0] = 0
        result[result > 1] = 1

        return result

    def sharpenImage(self):
        height, width, _ = np.shape(self.ImageData)

        # break image data into 3 channels
        B, G, R = cv2.split(self.ImageData)

        B = B[1:height - 1, 1:width - 1]/255
        G = G[1:height - 1, 1:width - 1]/255
        R = R[1:height - 1, 1:width - 1]/255

        #break filter data into 3 channels
        B_f, G_f, R_f = cv2.split(self.boosted)

        # lets sharpen each channel
        B_sharp = np.add(B,B_f)
        R_sharp = np.add(R, R_f)
        G_sharp = np.add(G, G_f)

        # Clip any negative values to 0, Clip values larger than 255 to 255
        B_sharp[B_sharp < 0] = 0
        B_sharp[B_sharp > 1] = 1
        R_sharp[R_sharp < 0] = 0
        R_sharp[R_sharp > 1] = 1
        G_sharp[G_sharp < 0] = 0
        G_sharp[G_sharp > 1] = 1

        final = cv2.merge([B_sharp, G_sharp, R_sharp])
        self.display_Image("Sharpened Image", final)


def main():
    Q1_ = Q1("../5_1.bmp")
    Q1_.perform_high_boost()
    Q1_.sharpenImage()

if __name__ == "__main__":
    main()