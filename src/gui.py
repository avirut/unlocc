from tkinter import *
import json
import keyboard
from widgets import ScrollFrame


class GUI:

    window = None
    filepath = 'config.ini'
    masterKey = None
    recordMode = None
    swapframe = None
    swaps = {}

    def __init__(self):
        print('GUI Launched')

    def launch(self):
        self.window = Tk('Unlocc Configuration')
        self.window.geometry('400x400')

        self.readConfig()

        savebtn = Button(master=self.window, text='Save', command=self.writeConfig)
        savebtn.grid(row=0, column=0, columnspan=2)

        masterlbl = Label(self.window, text='Master Key')
        masterlbl.grid(row=1, column=0)

        masterbox = Button(
            self.window, textvariable=self.masterKey, command=self.setMasterHook)
        masterbox.grid(row=1, column=1)

        modebox = Checkbutton(
            self.window, text='Record Mode', variable=self.recordMode, onvalue=True, offvalue=False)
        modebox.grid(row=2, column=0, columnspan=2)

        self.swapframe = ScrollFrame(self.window)
        self.swapframe.grid(row=3, column=0, columnspan=2)

        for row in range(100):
            a = row
            j = Label(self.swapframe.viewPort, text="%s" % row, width=3, borderwidth="1", relief="solid")
            j.grid(row=row, column=0)
            t = "this is the second column for row %s" % row
            k = Button(self.swapframe.viewPort, text=t, command=lambda x=a: self.printMsg("Hello " + str(x)))
            k.grid(row=row, column=1)

        self.window.mainloop()

    def setMasterHook(self):
        keyboard.hook(callback=self.setMaster, suppress=True)

    def setMaster(self, event):
        self.masterKey.set(event.name)
        keyboard.unhook_all()

    def writeConfig(self):
        config = [self.masterKey.get(), self.recordMode.get(), self.swaps]
        output = json.dumps(config)
        file = open(self.filepath, 'w+')
        file.write(output)
        file.close()

    def readConfig(self):
        try:
            file = open(self.filepath, 'r')
        except IOError:
            print('Config Read Failed')
            return
        inp = json.loads(file.read())
        self.masterKey = StringVar(self.window, 'Unset')
        self.recordMode = BooleanVar(self.window, False)
        self.masterKey.set(inp[0])
        self.recordMode.set(inp[1])
        self.swaps = inp[2]
