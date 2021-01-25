import numpy as np
import cv2

class Q1:
    def __init__(self):
        self.ImageData = self.load_imgae_data("../3_1.bmp")

    def load_imgae_data(self, path):
        return cv2.imread(path, cv2.IMREAD_COLOR)

    def Covert_to_negative(self, ImageData):
        rows, columns, _ = ImageData.shape
        # Access the Image data row by row and pass to the negative function
        for x in range(rows):
            for y in range(columns):
                # Then set the corresponding rows with the results
                ImageData[x][y] = self.perform_negative_op_on_rows(ImageData[x][y])

    def perform_negative_op_on_rows(self, row):
        return np.array([255 - row[0], 255 - row[1], 255 - row[2]])

    def display_Image(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    Q1_ = Q1()

    Q1_.Covert_to_negative(Q1_.ImageData)
    Q1_.display_Image("Negative Image", Q1_.ImageData)

if __name__ == "__main__":
    main()