import numpy as np
import cv2
from tkinter import *

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()


        self.button = Button(
            frame, text='Quit', fg='red', command=frame.quit
            )
        self.button.pack(side=LEFT)

        self.scale = Scale(
            frame, from_=0,to_=255,orient=VERTICAL,
        )
        self.scale.set(15)
        self.scale.pack()

        self.printInt = Button(
            frame, text='Scale', fg='green',command=self.printScale
        )
        self.printInt.pack(side=LEFT)

        self.hi_there = Button(frame, text='Hello', fg='blue', command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print("Hello Everyone!")

    def printScale(self):
        print("meme")
        print(self.scale.get())


if __name__ == "__main__":
    root = Tk()

    app = App(root)

    root.mainloop()
    root.destroy()

