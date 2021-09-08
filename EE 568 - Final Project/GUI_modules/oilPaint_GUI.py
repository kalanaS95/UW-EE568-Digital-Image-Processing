from GUI_modules.main_canvas import *
from tkinter.font import BOLD, Font
from algorithms.oilpaint import *
from algorithms.oilPaint_GPU import *

class oilPaint_GUI:
    def __init__(self, root, imagePath, work_width, work_height, effectName):
        self.mainCanvas = canvas_GUI(root, imagePath, work_width, work_height, effectName)
        self.slider = None
        self.past = 3
        self.kernelLabel = None
        self.sigmaLabel = None
        self.sigmaSlider = None
        self.processButton = None
        self.GPU_OPTIMIZE = None
        self.IS_GPU_OPTIMIZED = False
        self.draw_GUI()
        # priming the code, this way numba can build code cache and during the next run things willmuch faster !
        oil_paint(np.array(self.mainCanvas.PIL_image), 3, 10)

    def draw_GUI(self):
        self.mainCanvas.draw_window()
        self.mainCanvas.root.update()

        adjust_height = self.mainCanvas.adjustment_area.winfo_height()
        adjust_width = self.mainCanvas.adjustment_area.winfo_width()

        # draw slider for kernel size
        self.slider = tk.Scale(self.mainCanvas.adjustment_area, length=adjust_width//2, width=adjust_height//8, orient=tk.HORIZONTAL, from_=3, to=19,  command=self.fix, tickinterval=2, showvalue=0)
        self.slider.place(x=adjust_width//4, y=adjust_height//8)
        self.kernelLabel = tk.Label(self.mainCanvas.adjustment_area, text="Kernel Size: 3 x 3", font=Font(self.mainCanvas.adjustment_area, size=12))
        self.kernelLabel.place(x=adjust_width // 4, y=adjust_height // 8 - 25)
        self.mainCanvas.root.update()

        # Sigma label
        self.sigmaLabel = tk.Label(self.mainCanvas.adjustment_area, text="Intensity Levels: 10", font=Font(self.mainCanvas.adjustment_area, size=12))
        self.sigmaLabel.place(x=adjust_width // 4, y=adjust_height // 8 + self.slider.winfo_height() + 5)
        self.mainCanvas.root.update()
        # Sigma label
        self.sigmaSlider = tk.Scale(self.mainCanvas.adjustment_area, length=adjust_width // 2, width=adjust_height // 8, orient=tk.HORIZONTAL, from_=10, to=255, showvalue=0, command=self.sigma_slide)
        self.sigmaSlider.place(x=adjust_width // 4, y=adjust_height // 8 + self.slider.winfo_height() + self.sigmaLabel.winfo_height() + 5)
        self.mainCanvas.root.update()

        # GPU OPTIMIZE Button
        self.GPU_OPTIMIZE = tk.Checkbutton(self.mainCanvas.adjustment_area, text="Use GPU optimization (For real time processing)", command=self.GPU_toggle)
        self.GPU_OPTIMIZE.place(x=adjust_width // 4,y=adjust_height // 8 + self.slider.winfo_height() + self.sigmaLabel.winfo_height() + self.sigmaSlider.winfo_height() + 5)
        self.GPU_OPTIMIZE.deselect()

        # Process button
        self.processButton = tk.Button(self.mainCanvas.adjustment_area, text="Process Image (CPU)", command=self.processImage)
        self.processButton.place(x=adjust_width, y=adjust_height)
        self.mainCanvas.root.update()
        self.processButton.place(x=adjust_width - self.processButton.winfo_width() - 15, y=adjust_height - self.processButton.winfo_height() - 25)


    def fix(self, n):
        n = int(n)
        if not n % 2:
            self.slider.set(n + 1 if n > self.past else n - 1)
            self.past = self.slider.get()
            self.kernelLabel['text'] = f"Kernel Size: {self.past} x {self.past}"
            self.real_time_process()


    def sigma_slide(self, n):
        self.sigmaLabel['text'] = f"Intensity Levels: {n}"
        self.real_time_process()

    def GPU_toggle(self):
        if(self.IS_GPU_OPTIMIZED):
            self.IS_GPU_OPTIMIZED = False
        else:
            self.IS_GPU_OPTIMIZED = True
        self.real_time_process()

    def processImage(self):
        if (not self.IS_GPU_OPTIMIZED):
            oilPaint_ = oilPaint(self.mainCanvas.ImagePath, np.array(self.mainCanvas.PIL_image))
            results = oilPaint_.perform_oilPaint((int)(self.slider.get()), (int)(self.sigmaSlider.get()))
            PIL_Image = Image.fromarray(results)
            photo_result = ImageTk.PhotoImage(PIL_Image)
            self.mainCanvas.render_result_image(photo_result)

    def real_time_process(self):
        if (self.IS_GPU_OPTIMIZED):
            results = oil_paint(np.array(self.mainCanvas.PIL_image), (int)(self.slider.get()), (int)(self.sigmaSlider.get()))
            PIL_Image = Image.fromarray(results)
            photo_result = ImageTk.PhotoImage(PIL_Image)
            self.mainCanvas.render_result_image(photo_result)

