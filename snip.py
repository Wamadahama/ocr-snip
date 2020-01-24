from PIL import *
from PIL import Image

import pytesseract 


import cv2
import platform

import io
from io import BytesIO


import tkinter
from tkinter import Frame, Canvas,BOTH

pf = platform.system()
fname = 'temp'
filetype = 'png'
file_name = fname + "." + filetype 


class Selection:
    def __init__(self, root):
        #                    x1 y1 x2 y2
        self.bounding_box = [0,0, 0,0]
        self.is_selecting = False
        self.root = root
        self.root.wait_visibility(root)
        self.root.wm_attributes("-alpha", 0.5)
        self.root.wm_attributes('-fullscreen', True)
        self.root.bind("<Button-1>", self.start_capture)
        self.root.bind("<B1-Motion>", self.draw_box)
        self.root.bind("<ButtonRelease-1>", self.stop_capture)
        self.root.title("ocr-snip")
        self.current_rect = None
        self.canvas = Canvas(self.root)
        self.root.mainloop()

    def start_capture(self, event):
        print("{} {}".format(event.x, event.y))
        self.is_selecting = True 
        self.bounding_box[0] = event.x
        self.bounding_box[1] = event.y

    def stop_capture(self, event):
        print("{} {}".format(event.x , event.y))
        self.bounding_box[2] = event.x
        self.bounding_box[3] = event.y

        # swap the pairs if its started from the right 
        bounding_box = self.bounding_box
        mag = (bounding_box[2] - bounding_box[0], bounding_box[3] - bounding_box[1])
        if mag[0] < 0:
            bounding_box[0], bounding_box[2] = bounding_box[2], bounding_box[0]
        if mag[1] < 0:
            bounding_box[1], bounding_box[3] = bounding_box[3], bounding_box[1]

        print(bounding_box)

        self.root.destroy() #self.root.withdraw()
    def draw_box(self, event):
        x1,y1 = self.bounding_box[0], self.bounding_box[1]
        x2,y2 = event.x, event.y
        if self.is_selecting == True:
            self.canvas.delete(self.current_rect)
            self.current_rect = self.canvas.create_rectangle(x1, y1, x2,y2, outline="#111", fill="#f66", width=1)
            self.canvas.pack(fill=BOTH, expand=1)

            

def capture(bounding_box):
    if pf == 'Windows' or pf == 'Darwin':
        from PIL import ImageGrab
        return ImageGrab.grab(bounding_box)
    elif pf == 'Linux': 
        import qtpy 
        from qtpy import QtGui
        from qtpy import QtCore
        from qtpy import QtWidgets 
        QApplication = QtWidgets.QApplication
        QBuffer = qtpy.QtCore.QBuffer
        QIODevice = qtpy.QtCore.QIODevice
        QScreen = qtpy.QtGui.QScreen

        app = QApplication([])

        imgbuffer = QBuffer()
        imgbuffer.open(QIODevice.ReadWrite)
        QScreen.grabWindow(QApplication.primaryScreen(),
                        QApplication.desktop().winId()).save(imgbuffer, filetype)

        bufferedIO = BytesIO()
        bufferedIO.write(imgbuffer.data())
        imgbuffer.close()

        bufferedIO.seek(0)

        image = Image.open(bufferedIO)
        image = image.crop(bounding_box)
        return image 

def ocr():
    cv_img = cv2.imread(file_name)
    # Pre processing 
    grayscale = cv2.resize(cv_img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    grayscale = cv2.cvtColor(grayscale, cv2.COLOR_BGR2GRAY)
    grayscale = cv2.threshold(grayscale, 0, 2555, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #grayscale = cv2.medianBlur(grayscale, 2)
    cv2.imwrite(file_name, grayscale)
    text = pytesseract.image_to_string(Image.open(file_name))
    print(text)
    

def main():
    root = tkinter.Tk()
    screen_capture = Selection(root) 
    root.mainloop()
    image = capture(screen_capture.bounding_box)
    image.save(file_name)
    ocr()

main()
    
