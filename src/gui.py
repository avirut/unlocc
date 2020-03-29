from tkinter import *
import json
import keyboard


class GUI:

    window = None
    filepath = 'config.ini'
    masterKey = None
    recordMode = True
    swaps = {}

    def __init__(self):
        print('GUI')

    def launch(self):
        self.window = Tk('Unlocc Configuration')
        self.window.geometry('400x600')

        self.readConfig()

        savebtn = Button(master=self.window, text='Save', command=self.writeConfig)
        savebtn.grid(row=0, column=0, columnspan=2)

        masterlbl = Label(self.window, text='Master Key')
        masterlbl.grid(row=1, column=0)

        masterbox = Button(
            self.window, textvariable=self.masterKey, command=self.setMasterHook)
        masterbox.grid(row=1, column=1)

        modebox = Checkbutton(
            self.window, text='Record Mode', variable=self.recordMode,
            onvalue=True, offvalue=False)
        modebox.grid(row=2, column=0, columnspan=2)

        self.window.mainloop()

    def setMasterHook(self):
        keyboard.hook(callback=self.setMaster, suppress=True)

    def setMaster(self, event):
        self.masterKey.set(event.name)
        print(self.masterKey.get())
        keyboard.unhook_all()

    def writeConfig(self):
        config = [self.masterKey.get(), self.recordMode, self.swaps]
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
        self.masterKey.set(inp[0])
        self.recordMode = inp[1]
        self.swaps = inp[2]
