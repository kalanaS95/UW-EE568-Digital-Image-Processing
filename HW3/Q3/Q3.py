import numpy as np
import cv2
import copy

class Q3:
    def __init__(self):
        self.ImageData = self.load_imgae_data("../3_2.bmp")

    def load_imgae_data(self, path):
        return cv2.imread(path, cv2.IMREAD_COLOR)

    def display_Image(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def enhance_color(self,  Green_increase_factor, magenta_reduce_factor, ImageData):

        # lets make a deep copy of the image, this way we don't manipulate original image data
        Image_data_to_return = copy.deepcopy(ImageData)

        rows, columns, _ = Image_data_to_return.shape

        for x in range(rows):
            for y in range(columns):
                Image_data_to_return[x][y] = self.change_colors(Green_increase_factor, magenta_reduce_factor, Image_data_to_return[x][y])

        return Image_data_to_return

    def change_colors(self, Green_increase_factor, magenta_reduce_factor, row_data):

        new_green_value = row_data[1]
        new_red_value = row_data[2]
        new_blue_value = row_data[0]

        # Also, we don't need to change anything in white boarder (i.e if BRG values are same skip those pixels)
        if(not (new_green_value == new_blue_value == new_red_value)):
            new_green_value = int(new_green_value + (Green_increase_factor * new_green_value))
            new_red_value = int(new_red_value - (magenta_reduce_factor * new_red_value))
            new_blue_value = int(new_blue_value - (magenta_reduce_factor * new_blue_value))

        # make sure if the value does not overflow max of 255
        if(new_green_value >= 255):
            new_green_value = 255

        row_data[0] = new_blue_value
        row_data[1] = new_green_value
        row_data[2] = new_red_value

        return row_data

    def histogram_equalization(self, image_data):
        falttened_matrix = image_data.flatten()
        imageData_hist = np.zeros(256)

        # couting occurence of each pixel
        for pix in image_data:
            imageData_hist[pix] += 1

        # getting cumilative sum
        csum = np.cumsum(imageData_hist)
        normalize = (csum - csum.min()) * 255

        # normalizing each pixel in the channel
        n = csum.max() - csum.min()
        uniform_normalization = normalize / n
        uniform_norm = uniform_normalization.astype(np.uint8) # converting to Uint 8

        # flattening histogram
        equalized_image = uniform_norm[falttened_matrix]

        # reshaping the flattened matrix to its original shape
        equalized_image = np.reshape(a=equalized_image, newshape=image_data.shape)

        # return equalized channel data
        return equalized_image

    def equalize_image(self, image_src):

        # splitting BRG channels such that we can perform histogram equalization on each channel
        r_channel = image_src[:, :, 0]
        g_channel = image_src[:, :, 1]
        b_channel = image_src[:, :, 2]

        r_equalized = self.histogram_equalization(r_channel)
        g_equalized = self.histogram_equalization(g_channel)
        b_equalized = self.histogram_equalization(b_channel)

        return np.dstack(tup=(r_equalized, g_equalized, b_equalized))


def main():
    Q3_ = Q3()

    Q3_.display_Image("Enhanced", Q3_.enhance_color(0.6, 0.01, Q3_.ImageData))

    # Using histogram equalization
    Q3_.display_Image("Hist equalized", Q3_.equalize_image(Q3_.ImageData))

if __name__ == "__main__":
    main()