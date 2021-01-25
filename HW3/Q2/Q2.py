import numpy as np
import cv2
import copy


class Q2:
    def __init__(self):
        self.ImageData = self.load_imgae_data("../3_2.bmp")
        self.HSV_ImageData = self.Convert_to_HSV(self.ImageData)

    def load_imgae_data(self, path):
        return cv2.imread(path, cv2.IMREAD_COLOR)

    def Convert_to_HSV(self, ImageData):
        return cv2.cvtColor(ImageData, cv2.COLOR_BGR2HSV)

    def display_Image(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def display_R_G_B(self, Color_type):

        # lets make a deep copy of the data so that we don't change the original
        Image_to_return = copy.deepcopy(self.ImageData)

        rows, columns, _ = Image_to_return.shape

        for x in range(rows):
            for y in range(columns):
                Image_to_return[x][y] = self.Convert_row_to_R_G_B(Image_to_return[x][y], Color_type)


        return Image_to_return

    def Convert_row_to_R_G_B(self, row, Color_type):
        if (Color_type == 'B'):
            row[1], row[2] = row[0], row[0]
            return row
        elif (Color_type == 'R'):
            row[0], row[1] = row[2], row[2]
            return row
        elif (Color_type == 'G'):
            row[0], row[2] = row[1], row[1]
            return row

    def display_H_S_V(self, Color_type):
        # lets make a deep copy of the data so that we don't change the original
        Image_to_return = copy.deepcopy(self.HSV_ImageData)

        rows, columns, _ = Image_to_return.shape

        for x in range(rows):
            for y in range(columns):
                Image_to_return[x][y] = self.Convert_row_to_H_S_V(Image_to_return[x][y], Color_type)

        return Image_to_return




    def Convert_row_to_H_S_V(self, row, Color_type):
        if (Color_type == 'H'):
            row[1], row[2] = row[0], row[0]
            return row
        elif (Color_type == 'S'):
            row[0], row[2] = row[1], row[1]
            return row
        elif (Color_type == 'V'):
            row[0], row[1] = row[2], row[2]
            return row


def main():
    Q2_ = Q2()

    # Part a
    Q2_.display_Image("R only image", Q2_.display_R_G_B('R'))
    Q2_.display_Image("G only image", Q2_.display_R_G_B('G'))
    Q2_.display_Image("B only image", Q2_.display_R_G_B('B'))

    # part b
    Q2_.display_Image("H only image", Q2_.display_H_S_V('H'))
    Q2_.display_Image("S only image", Q2_.display_H_S_V('S'))
    Q2_.display_Image("V only image", Q2_.display_H_S_V('V'))


if __name__ == "__main__":
    main()
