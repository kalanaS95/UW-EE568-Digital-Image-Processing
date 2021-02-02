import numpy as np
import cv2
import matplotlib.pyplot as plt

class Q1:
    def __init__(self, path, ImageName):
        self.Imagename = ImageName
        self.ImageData = self.load_imgae_data(path)
        self.HSV_ImageData = self.Convert_to_HSV(self.ImageData)
        self.fixedIntensityData = None

    def load_imgae_data(self, path):
        return cv2.imread(path, cv2.IMREAD_COLOR)

    def Convert_to_HSV(self, ImageData):
        return cv2.cvtColor(ImageData, cv2.COLOR_BGR2HSV)

    def display_Image(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def perform_linear_stretch(self):
        H, S, V = cv2.split(self.HSV_ImageData)
        Intensity_counts = np.zeros(256, dtype=np.uint8)
        # finding min and max values for linear streching
        max_val, min_val = np.amax(V), np.amin(V)

        # Plot intensity distribution before
        self.intensity_histogram(Intensity_counts, V, self.Imagename + ": "+ " Intensity Levels and their counts - Before Linear Stretching", "Intensity Levels", "Counts")
        # Plot CDF before
        self.plot_cdf(Intensity_counts, self.Imagename + ": "+ " Cumulative  Distribution Function - Before Linear Stretching", "Intensity Levels", "Probability")
        for x in V:
            self.linear_stretch(x, min_val, max_val)
        Intensity_counts = np.zeros(256, dtype=np.uint8)
        # Plot intensity distribution after
        self.intensity_histogram(Intensity_counts, V, self.Imagename + ":" + " Intensity Levels and their counts - After Linear Stretching",
                                 "Intensity Levels", "Counts")
        # Plot CDF after
        self.plot_cdf(Intensity_counts, self.Imagename + ": " + " Cumulative  Distribution Function - after Linear Stretching",
                      "Intensity Levels", "Probability")

        # now lets combine H S V channels together and convert back to BRG
        final_image = cv2.merge([H, S, V])
        out = cv2.cvtColor(final_image, cv2.COLOR_HSV2BGR)
        self.display_Image(self.Imagename + ": Original Image", self.ImageData)
        self.display_Image(self.Imagename + ": Linear Stretched", out)

    def linear_stretch(self, IntensityData, min, max):
        # First calcualte the constant value in the equation
        constant = 255/(max - min)

        # Peform linear stretch for each pixel
        for pixel_index in range(len(IntensityData)):
            IntensityData[pixel_index] = constant * (IntensityData[pixel_index] - min)

    def perform_Histogram_equalization(self):
        H, S, V = cv2.split(self.HSV_ImageData)
        Intensity_counts = np.zeros(256, dtype=np.uint8)

        # calling intensity_histogram will help me to count pixels and their occurences. So i dont have to count them in the histogram eq function
        self.intensity_histogram(Intensity_counts, V, self.Imagename + ":" + " Intensity Levels and their counts - Before Histogram Equalization",
                                 "Intensity Levels", "Counts")
        # Plot CDF before
        self.plot_cdf(Intensity_counts,
                      self.Imagename + ": " + " Cumulative  Distribution Function - Before Histogram Equalization",
                      "Intensity Levels", "Probability")
        equalized_V = self.Histogram_equalization(V)
        Intensity_counts = np.zeros(256, dtype=np.uint8)
        self.intensity_histogram(Intensity_counts, equalized_V, self.Imagename + ":" + " Intensity Levels and their counts - After Histogram Equalization",
                                 "Intensity Levels", "Counts")
        # Plot CDF before
        self.plot_cdf(Intensity_counts,
                      self.Imagename + ": " + " Cumulative  Distribution Function - After Histogram Equalization",
                      "Intensity Levels", "Probability")

        # now lets combine H S V channels together and convert back to BRG
        final_image = cv2.merge([H, S, equalized_V])
        out = cv2.cvtColor(final_image, cv2.COLOR_HSV2BGR)
        self.display_Image(self.Imagename + ": Original Image", self.ImageData)
        self.display_Image(self.Imagename + ": Histogram Equalization", out)

    def Histogram_equalization(self, IntensityData):
        falttened_matrix = IntensityData.flatten()
        imageData_hist = np.zeros(256)

        # couting occurence of each pixel
        for pix in IntensityData:
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
        equalized_image = np.reshape(a=equalized_image, newshape=IntensityData.shape)
        # return equalized channel data
        return equalized_image

    def perform_histogram_specification(self, targetImage):
        targetImage_BRG = cv2.imread(targetImage, cv2.IMREAD_COLOR)
        targetImage_HSV = cv2.cvtColor(targetImage_BRG, cv2.COLOR_BGR2HSV)
        # Split Original Image HSV channels
        H, S, V = cv2.split(self.HSV_ImageData)
        # Split target Image HSV channels
        H_, S_, V_ = cv2.split(targetImage_HSV)
        Intensity_counts = np.zeros(256, dtype=np.uint8)
        # calling intensity_histogram will help me to count pixels and their occurences. So i dont have to count them
        # in the histogram eq function
        self.intensity_histogram(Intensity_counts, V,
                                 self.Imagename + ":" + " Intensity Levels and their counts - Before Histogram Specification",
                                 "Intensity Levels", "Counts")
        # Plot CDF before
        self.plot_cdf(Intensity_counts,
                      self.Imagename + ": " + " Cumulative  Distribution Function - Before Histogram Specification",
                      "Intensity Levels", "Probability")

        specified_V = self.histogram_specification(V, V_)
        Intensity_counts = np.zeros(256, dtype=np.uint8)
        # calling intensity_histogram will help me to count pixels and their occurences. So i dont have to count them
        # in the histogram eq function
        self.intensity_histogram(Intensity_counts, V_,
                                 self.Imagename + ":" + " Intensity Levels and their counts - After Histogram Specification",
                                 "Intensity Levels", "Counts")
        # Plot CDF before
        self.plot_cdf(Intensity_counts,
                      self.Imagename + ": " + " Cumulative  Distribution Function - After Histogram Specification",
                      "Intensity Levels", "Probability")

        # now lets combine H S V channels together and convert back to BRG
        final_image = cv2.merge([H, S, specified_V])
        out = cv2.cvtColor(final_image, cv2.COLOR_HSV2BGR)
        self.display_Image(self.Imagename + ": Original Image", self.ImageData)
        self.display_Image(self.Imagename + ": Histogram Specification", out)

    def histogram_specification(self, source, targetImage):
        oldshape = source.shape
        source = source.ravel()
        target = targetImage.ravel()

        s_values, bin_idx, s_counts = np.unique(source, return_inverse=True, return_counts=True)
        t_values, t_counts = np.unique(target, return_counts=True)

        s_quantiles = np.cumsum(s_counts).astype(np.float64)
        s_quantiles /= s_quantiles[-1]
        t_quantiles = np.cumsum(t_counts).astype(np.float64)
        t_quantiles /= t_quantiles[-1]

        interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

        # make sure to convert to unit_8 we dont need decimal places in the return matrix
        return (interp_t_values[bin_idx].reshape(oldshape)).astype(np.uint8)


    def intensity_histogram(self, counts, IntensityData, Title, Xlabel, Ylabel):
        Intensity_levels = [str(x) for x in range(256)]
        for curr in IntensityData:
            for x in curr:
                counts[x] += 1

        plt.bar(Intensity_levels, list(counts))
        # rotate x axis labels, so we can see them clear
        plt.xticks(rotation=90)
        plt.title(Title)
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.show()



    def plot_cdf(self, IntensityData_counted, Title, Xlabel, Ylabel):
        list_sum = np.sum(IntensityData_counted)
        # divide every entry by list_sum to get the PDF
        pdf = IntensityData_counted / list_sum
        # Calculating CDF
        CDF = np.zeros(256)

        for x in range(0, 256):
            if x == 0:
                CDF[x] = pdf[x]
            else:
                CDF[x] = np.sum(pdf[0:x+1])

        Intensity_levels = [str(x) for x in range(256)]
        # Plotting CDF
        plt.bar(Intensity_levels, list(CDF))
        # rotate x axis labels, so we can see them clear
        plt.xticks(rotation=90)
        plt.title(Title)
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.show()

def main():

    # For first Image
    image1 = Q1("../4_1.jpg", "4_1.jpg")
    image1.perform_linear_stretch()
    image1.perform_Histogram_equalization()
    image1.perform_histogram_specification("../4_1_fixed.jpg")

    # For second Image
    image2 = Q1("../4_2.jpg", "4_2.jpg")
    image2.perform_linear_stretch()
    image2.perform_Histogram_equalization()
    image2.perform_histogram_specification("../4_2_fixed.jpg")

if __name__ == "__main__":
    main()