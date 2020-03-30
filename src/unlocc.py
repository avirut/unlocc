from gui import GUI
from keybrain import KeyBrain

from PIL import Image, ImageDraw
import pystray
import sys
import json
import threading


class Unlocc:

    enabled = True
    keybrain = None
    tray = pystray.Icon('Unlocc')
    filepath = 'config.ini'
    confGUI = None
    image = None
    menu = None
    masterKey = 'caps lock'
    recordMode = True
    swaps = {}

    def __init__(self):
        print('Unlocc Launched')

    def launchapp(self):
        self.create_image()
        self.create_menu()
        self.load_config()
        self.keybrain = KeyBrain(self.masterKey, self.recordMode, self.swaps)

        self.tray = pystray.Icon('Unlocc', menu=self.menu)

        self.tray.icon = self.image
        self.tray.run()

    def create_image(self):
        # Generate an image and draw a pattern
        width = 20
        height = 20
        color1 = '#000000ff'
        color2 = '#0000ff00'
        self.image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(self.image)
        dc.rectangle(
            (width // 2, 0, width, height // 2),
            fill=color2)
        dc.rectangle(
            (0, height // 2, width // 2, height),
            fill=color2)

    def load_config(self):
        try:
            file = open(self.filepath, 'r')
        except IOError:
            print('Config Read Failed')
            return
        inp = json.loads(file.read())
        self.masterKey = inp[0]
        self.recordMode = inp[1]
        self.swaps = inp[2]

    def launch_settings(self):
        self.keybrain.shutdown()
        if self.confGUI is not None:
            del self.confGUI
        self.confGUI = GUI()
        guiThread = threading.Thread(target=self.confGUI.launch)
        guiThread.setDaemon(True)
        guiThread.start()
        guiThread.join()
        print('past')
        self.load_config()
        self.keybrain = KeyBrain(self.masterKey, self.recordMode, self.swaps)

    def on_enabled(self, icon, item):
        self.enabled = not item.checked

        if not self.enabled and self.keybrain is not None:
            self.keybrain.shutdown()
            self.keybrain = None
        elif self.enabled:
            if self.keybrain is None:
                self.keybrain = KeyBrain(self.masterKey, self.recordMode, self.swaps)
            else:
                self.keybrain.shutdown()
                self.keybrain = None
                self.keybrain = KeyBrain(self.masterKey, self.recordMode, self.swaps)

    def terminate(self):
        if self.keybrain is not None:
            self.keybrain.shutdown()
        if self.tray is not None:
            self.tray.stop()
        sys.exit()

    def create_menu(self):
        self.menu = pystray.Menu(
            pystray.MenuItem('Settings', self.launch_settings),
            pystray.MenuItem(
                'Enabled',
                self.on_enabled,
                checked=lambda item: self.enabled
            ),
            pystray.MenuItem('Exit', self.terminate)
        )


if __name__ == '__main__':
    unlocc = Unlocc()
    unlocc.launchapp()
