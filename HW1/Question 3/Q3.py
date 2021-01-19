import numpy as np
import cv2

class Q3():
    def __init__(self):
        self.X = self.load_image("../1_3.tif")

    def load_image(self, path):
        return cv2.imread(path, cv2.IMREAD_COLOR)

    def convert_to_grayScale(self):
        self.Y = cv2.cvtColor(self.X, cv2.COLOR_BGR2GRAY)

    def showImage(self, ImageData, Title):
        cv2.imshow(Title, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def imageRotate(self,ImageData, degrees):
        # lets get height and width of the image this way we can find the center point of the image
        # for cv2.GetRotationMatrix2D functions first argument
        height, width = ImageData.shape

        # lets perform rotation, -120 degrees beacause we need to rotate this image 120 degrees clockwise
        # and scaling factor is 1
        matrix = cv2.getRotationMatrix2D((height/2, width/2), degrees, 1)

        return cv2.warpAffine(self.Y, matrix, (height, width))

    def rotateImage_120_clockwise(self):
        return self.imageRotate(self.Y, -120)

    def rotateImage_10_degrees_times_10_clockwise(self):
        # lets do the first 10 degree rotation here, rest will be done in the below loop
        results = self.imageRotate(self.Y, -10)
        for itr in range(0,11):
            results = self.imageRotate(results, -10)

        return results

    def generateImage(self,ImageName, ImageData):
        cv2.imwrite(ImageName, ImageData)

def main():
    Q3_ = Q3()

    # Part a
    Q3_.convert_to_grayScale()
    Q3_.showImage(Q3_.Y, "Grayscale Image")


    # Part b
    imageData = Q3_.rotateImage_120_clockwise()
    Q3_.showImage(imageData, "120 degree clockwise rotation")
    Q3_.generateImage("../Z0.tif", imageData)

    # Part c
    imageData_ = Q3_.rotateImage_10_degrees_times_10_clockwise()
    Q3_.showImage(imageData_, "120 degree clockwise rotation (10 degree x 12)")
    Q3_.generateImage("../Z1.tif", imageData_)


if __name__ == "__main__":
    main()