import tkinter as tk
from PIL import ImageTk, Image
from tkinter.font import BOLD, Font

class canvas_GUI:
    def __init__(self, root, imagePath, work_width, work_height, effectName):
        self.ImagePath = imagePath
        self.PIL_image = Image.open(self.ImagePath)
        self.ImageInfo = ImageTk.PhotoImage(self.PIL_image)
        self.work_width = work_width
        self.work_height = work_height
        self.canvasWindow = None
        self.Original_Image_canvas = None
        self.Result_Image_canvas = None
        self.adjustment_area = None
        self.effectName = effectName
        self.root = root

    def draw_window(self):
        self.canvasWindow = tk.Toplevel(self.root)
        # turn off main window resize
        self.canvasWindow.resizable(False, False)
        # set window name
        self.canvasWindow.title(f"Pixel Perfect Effects - {self.effectName} Effect")
        # figuring out canvas window height and width
        canvas_window_height = (int)(self.work_height - (self.root.winfo_height() + 100))
        canvas_window_width = (int)(self.work_width/2)
        self.canvasWindow.geometry(
            f"{canvas_window_width}x{canvas_window_height}+{(int)(self.work_width / 4)}+{(int)(self.work_height - (canvas_window_height + self.root.winfo_height() + 100))}")

        # Now lets create the width and height we need to fit both images with in the window
        total_width_required = self.ImageInfo.width()*2 + 150 + 20 # 50 for padding between both images, 20 for padding between both window edges and images
        total_height_required = self.ImageInfo.height() + 20 # 20 for padding between both vertical padding between window edges

        print("Window Info: ", canvas_window_width, canvas_window_height)
        print("Canvas Info: ", total_width_required, total_height_required)

        if total_width_required < canvas_window_width and total_height_required < canvas_window_height - (int)(canvas_window_height/4): # if both are smaller than window no scaling down requried
            self.Original_Image_canvas = tk.Canvas(self.canvasWindow, height=self.ImageInfo.height(), width=self.ImageInfo.width())
            self.Original_Image_canvas.place(x=(int)((canvas_window_width - total_width_required)/2), y=(int)((canvas_window_height - (canvas_window_height / 4) - total_height_required)/2))
            self.Result_Image_canvas = tk.Canvas(self.canvasWindow, height=self.ImageInfo.height(), width=self.ImageInfo.width())
            self.Result_Image_canvas.place(x=(int)((canvas_window_width - total_width_required)/2) + self.ImageInfo.width() + 150 , y=(int)((canvas_window_height - (canvas_window_height / 4) - total_height_required) / 2))
            # add image to the first canvas
            self.Original_Image_canvas.create_image(0, 0, anchor=tk.NW, image=self.ImageInfo)
            self.Original_Image_canvas.image = self.ImageInfo
            self.Result_Image_canvas.create_image(0, 0, anchor=tk.NW, image=self.ImageInfo)
            self.Result_Image_canvas.image = self.ImageInfo

        else: # meaning we cannot fit the image in our canvas so we gotta scale this baby to fit in the screen

            # find width and height once image is scaled
            if self.ImageInfo.width() > self.ImageInfo.height(): # if its a wider image
                scaled_width = (int)((canvas_window_width - (20 + 150))/2)
                scaled_height = (int)(canvas_window_height - 20 - (canvas_window_height / 4))
            else: # if its a longer image
                scaled_height = (int)(canvas_window_height - 20 - (canvas_window_height / 4))
                scaled_width = (int)((canvas_window_width - (20 + 150))/2)

            # reconstructing the image
            self.PIL_image.thumbnail((scaled_width, scaled_height), Image.ANTIALIAS)
            self.ImageInfo = ImageTk.PhotoImage(self.PIL_image)

            total_width_required = self.ImageInfo.width() * 2 + 150 + 20  # 50 for padding between both images, 20 for padding between both window edges and images
            total_height_required = self.ImageInfo.height() + 20  # 20 for padding between both vertical padding between window edges

            self.Original_Image_canvas = tk.Canvas(self.canvasWindow, height=self.ImageInfo.height(), width=self.ImageInfo.width())
            self.Original_Image_canvas.place(x=(int)((canvas_window_width - total_width_required) / 2) + 10, y=(int)((canvas_window_height - (canvas_window_height / 4) - total_height_required)/2))
            self.Result_Image_canvas = tk.Canvas(self.canvasWindow, height=self.ImageInfo.height(), width=self.ImageInfo.width())
            self.Result_Image_canvas.place(x=(int)((canvas_window_width - total_width_required)/2) + self.ImageInfo.width() + 150 , y=(int)((canvas_window_height - (canvas_window_height / 4) - total_height_required)/2))
            self.Original_Image_canvas.create_image(0, 0, anchor=tk.NW, image=self.ImageInfo)
            self.Original_Image_canvas.image = self.ImageInfo
            self.Result_Image_canvas.create_image(0, 0, anchor=tk.NW, image=self.ImageInfo)
            self.Result_Image_canvas.image = self.ImageInfo

        # draws the place holder for slider/parameter area
        self.adjustment_area = tk.LabelFrame(self.canvasWindow, cursor="hand2", width=canvas_window_width, height=(int)(canvas_window_height/4), text="Parameter Adjustments", font=Font(self.canvasWindow, size=12, weight=BOLD) )
        self.adjustment_area.place(x=0, y=canvas_window_height - (int)(canvas_window_height/4))


    def render_result_image(self, Image):
        self.Result_Image_canvas.create_image(0, 0, anchor=tk.NW, image=Image)
        self.Result_Image_canvas.image = Image






