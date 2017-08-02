from tkinter import*
import serial
import _thread


class Trackbars():
    def __init__(self,master):
        tkFrame = Frame(master)
        tkFrame.pack()

        self.lowerSlider = Scale(tkFrame, from_=180, to_=-180, orient=VERTICAL)
        self.lowerSlider.pack(side=LEFT)

        self.upperSlider = Scale(tkFrame, from_=180, to_=-180, orient=VERTICAL)
        self.upperSlider.pack(side=LEFT)

        self.button = Button(tkFrame, text= "Zero", command=self.setToZero)
        self.button.pack(side=LEFT)

    def setToZero(self):
        self.lowerSlider.set(0)
        self.upperSlider.set(0)
        print("Setting to Zero")
    def getLeft(self):
        return self.lowerSlider.get()
    def getRight(self):
        return self.upperSlider.get()

def sendMotorData(track):
    ser = serial.Serial('COM4', 38400, timeout=0)
    while 1:
        stringOut = str(track.getLeft()) + "," + str(track.getRight()) + ","
        print(stringOut)
        ser.write(bytes(stringOut, "ascii"))
    ser.close()

if __name__ == "__main__":

    root = Tk()
    motorControl = Trackbars(root)
    _thread.start_new_thread(sendMotorData, (motorControl,))
    root.mainloop()
    print("closing")




