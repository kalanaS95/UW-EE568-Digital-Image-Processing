import numpy as np
import matplotlib.pyplot as plt
import cv2

class Q2:
    def __init__(self):
        self.ImageData = self.load_Lena_image("../2_2.bmp")
        self.grayLevels = np.zeros(256)

    def load_Lena_image(self, path):
        return cv2.imread(path, cv2.IMREAD_COLOR)

    def showImage(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_one_channel(self, ImageData):
        return ImageData[:, :, 0]

    def count_gray_levels(self, singleChannelData):
        for x in singleChannelData:
            for y in x:
                self.grayLevels[y] += 1

    # this function has to be run first to call the probability_function()
    # Since this function counts the gray levels
    def plot_histogram(self):
        self.count_gray_levels(self.get_one_channel(self.ImageData))
        gray_levels = [str(x) for x in range(256)]
        plt.bar(gray_levels, list(self.grayLevels))
        # rotate x axis labels, so we can see them clear
        plt.xticks(rotation=90)
        plt.title("Gray Levels and their counts")
        plt.xlabel("Gray Levels")
        plt.ylabel("Counts")
        plt.show()

    def probability_function(self):
        list_sum = np.sum(self.grayLevels)
        # divide every entry by list_sum to get the PDF
        pdf = self.grayLevels/list_sum
        # Calculating CDF
        CDF = np.zeros(256)

        for x in range(0,256):
            if x == 0:
                CDF[x] = pdf[x]
            else:
                CDF[x] = np.sum(pdf[0:x])


        gray_levels = [str(x) for x in range(256)]
        # Plotting CDF
        plt.bar(gray_levels, list(CDF))
        # rotate x axis labels, so we can see them clear
        plt.xticks(rotation=90)
        plt.title("Cumulative  Distribution Function")
        plt.xlabel("Gray Levels")
        plt.ylabel("Probability")
        plt.show()

        # Plotting PDF
        plt.bar(gray_levels, list(pdf))
        # rotate x axis labels, so we can see them clear
        plt.xticks(rotation=90)
        plt.title("Probability Density  Function")
        plt.xlabel("Gray Levels")
        plt.ylabel("Probability")
        plt.show()

def main():
    Q2_ = Q2()

    # Counts gray levels and plot histogram
    Q2_.plot_histogram()

    # Calculates PDF and CDF and plot them
    Q2_.probability_function()




if __name__ == "__main__":
    main()