import numpy as np
import cv2

class Q2:
    def __init__(self):
        self.imageData = self.load_Lena_image("../1_2.bmp")

    def load_Lena_image(self, path):
        return cv2.imread(path, cv2.IMREAD_COLOR)

    def show_lena_image(self):
        cv2.imshow("Lena Image", self.imageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def dataType_and_max_min(self):
        print("Data type of the image: ", self.imageData.dtype)
        print("Maximum Data value: ", np.amax(self.imageData))
        print("Minimum Data value: ", np.amin(self.imageData))
        print("\n\n")

    def convertoDouble_andShow(self):
        self.convertedToDouble = self.imageData.astype('float')
        cv2.imshow("Lena Image", self.convertedToDouble)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def correctly_showing_double_image(self):
        # Lets normalize the values stored in convertedToDouble variable to 0-1 scale
        self.convertedToDouble_correctly = self.convertedToDouble / 255
        # Now lets show the normalized image
        cv2.imshow("Lena Image - Normalized", self.convertedToDouble_correctly)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main():
    Q2_ = Q2()

    # Part a
    Q2_.show_lena_image()

    # Part b
    Q2_.dataType_and_max_min()

    # Part c
    Q2_.convertoDouble_andShow()

    # Part d
    Q2_.correctly_showing_double_image()


if __name__ == "__main__":
    main()