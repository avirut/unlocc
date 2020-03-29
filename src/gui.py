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
    tkkeys = []
    tkvals = []

    def __init__(self):
        print('GUI Launched')

    def launch(self):
        self.window = Tk('Unlocc Configuration')
        self.window.geometry('400x400')

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

        addbtn = Button(self.window, text='Add Swap', command=self.addSwap)
        addbtn.grid(row=4, column=0, columnspan=2)

        self.readConfig()
        self.drawSwaps()
        self.window.mainloop()

    def setMasterHook(self):
        keyboard.hook(callback=self.setMaster, suppress=True)

    def setMaster(self, event):
        self.masterKey.set(event.name)
        keyboard.unhook_all()

    def drawSwaps(self):
        for i in range(len(self.tkkeys)):
            ind = Label(self.swapframe.viewPort, text="%s" % i, width=3, borderwidth="1", relief="solid")
            ind.grid(row=row, column=0)
            keyentry = Entry(self.swapframe.viewPort, textvariable=self.tkkeys[i])
            valentry = Entry(self.swapframe.viewPort, textvariable=self.tkvals[i])
            keyentry.grid(row=i, column=1)
            valentry.grid(row=i, column=2)

    def addSwap(self):
        key = StringVar(self.swapframe.viewPort)
        val = StringVar(self.swapframe.viewPort)
        self.tkkeys.append(key)
        self.tkvals.append(val)
        keyentry = Entry(self.swapframe.viewPort, textvariable=key)
        valentry = Entry(self.swapframe.viewPort, textvariable=val)
        ind = len(self.tkkeys)
        indlbl = Label(self.swapframe.viewPort, text="%s" % ind, width=3, borderwidth="1", relief="solid")
        indlbl.grid(row=ind, column=0)
        keyentry.grid(row=ind, column=1)
        valentry.grid(row=ind, column=2)

    def writeConfig(self):
        self.swaps = {self.tkkeys[i].get(): self.tkvals[i].get() for i in range(len(self.tkkeys))}
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
        self.tkkeys = [StringVar(self.swapframe, key) for key in list(self.swaps)]
        self.tkvals = [StringVar(self.swapframe, val) for val in list(self.swaps.values())]
