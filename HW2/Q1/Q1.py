import numpy as np
import math
import cv2


class Q1:
    def __init__(self):
        self.ImageData = self.normalize_to_0to1(self.loadImage_data())

    def loadImage_data(self):
        return np.loadtxt("../2_1.asc")

    def normalize_to_0to1(self, imageData):
        return imageData / 255

    def showImage(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def Part_a_i(self, ImageData):
        rows, columns = np.shape(ImageData)
        return ImageData[0:rows:4, 0:columns:4]

    def Part_a_ii(self, ImageData):
        # finding rows and columns of the given image data
        rows, columns = np.shape(ImageData)

        # now lets calculate the average of 4x4 area and add it to our matrix
        rows_select = [x * 4 for x in range(0, int(rows / 4) + 1)]
        columns_select = [x * 4 for x in range(0, int(columns / 4) + 1)]

        average_array = []

        for x in range(len(rows_select) - 1):
            for y in range(len(columns_select) - 1):
                average_array.append(
                    np.mean(ImageData[rows_select[x]:rows_select[x + 1], columns_select[y]:columns_select[y + 1]]))

        # convert list to np array
        new_array = np.array(average_array)

        # reshape it to 4 times smaller matrix
        return new_array.reshape(int(rows / 4), int(columns / 4))

    def Part_b_i(self, ImageData, Enlarge):
        # finding rows and columns of the given image data
        rows, columns = np.shape(ImageData)

        # lets create a list
        Elements_to_repeat = []

        # horizontally adding more pixels
        for x in range(rows):
            temp = []
            for y in range(columns):
                for z in range(Enlarge):
                    temp.append(ImageData[x][y])
            Elements_to_repeat.append(temp)

        Enlarged_image_data = []

        # Vertically adding more pixels
        for x in Elements_to_repeat:
            for y in range(Enlarge):
                Enlarged_image_data.append(x)

        return np.array(Enlarged_image_data)

    def Part_b_ii(self, image, Enlarge):
        # Getting Original image height and width
        img_height, img_width = image.shape

        # Calculating height and width of the enlarged image using the passed in Enlarge factor
        new_height, new_width = img_height * Enlarge, img_width * Enlarge

        # lets create an empty NxM matrix for the dimensions of the enlarged image
        enlarged_imge_data = np.empty([new_height, new_width])

        # Calculating x and y ratios
        Xratio = float(img_width - 1) / (new_width - 1) if new_width > 1 else 0
        Yratio = float(img_height - 1) / (new_height - 1) if new_height > 1 else 0

        # Performing Bilinear interpolation
        for x in range(new_height):
            for y in range(new_width):
                x_l, y_l = math.floor(Xratio * y), math.floor(Yratio * x)
                x_h, y_h = math.ceil(Xratio * y), math.ceil(Yratio * x)

                Xweight, Yweight = (Xratio * y) - x_l, (Yratio * x) - y_l

                a, b, c, d = image[y_l, x_l], image[y_l, x_h], image[y_h, x_l], image[y_h, x_h]

                pixel = a * (1 - Xweight) * (1 - Yweight) + b * Xweight * (1 - Yweight) + c * Yweight * (1 - Xweight) + d * Xweight * Yweight

                enlarged_imge_data[x][y] = pixel

        return enlarged_imge_data


def main():
    Q1_ = Q1()

    # Part a i
    Y1 = Q1_.Part_a_i(Q1_.ImageData)
    Q1_.showImage("Y1", Y1)

    # Part a_ii
    Y2 = Q1_.Part_a_ii(Q1_.ImageData)
    Q1_.showImage("Y2", Y2)

    # Part b_i
    Q1_.showImage("Blocky Enlarged Image", Q1_.Part_b_i(Y1, 4))

    # Part b_ii
    Q1_.showImage("Enlarged Image using Bilinear Interpolation ", Q1_.Part_b_ii(Y1, 4))


if __name__ == "__main__":
    main()
