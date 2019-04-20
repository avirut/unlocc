import keyboard
from datetime import time


class KeyBrain:

    active = False              # whether unlocc is active or not
    master = 'caps lock'        # master key identity
    lastHit = 0                 # time at which master key was last hit
    timeout = 0.3

    def __init__(self, master):
        self.master = master
        keyboard.suppress()
        keyboard.on_press_key(key=master, callback=None, suppress=True)
        keyboard.on_release_key(
            key=master, callback=self.keypress, suppress=True)

    def keypress(self, event):
        if time.time() - self.lastHit < self.timeout:
            keyboard.send(self.master)
            self.deactivate()
        else:
            self.lastHit = time.time()
            self.activate()

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True
