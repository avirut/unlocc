import keyboard
import time
import sys


class KeyBrain:

    active = False              # whether unlocc is active or not
    master = 'caps lock'        # master key identity
    lastHit = 0                 # time at which master key was last hit
    timeout = 0.3               # second timeout between presses for double
    lastType = keyboard.KEY_UP  # type of last keypress

    def __init__(self, master):
        self.master = master
        keyboard.on_press_key(
            key=master, callback=self.keypress, suppress=True)
        keyboard.on_release_key(
            key=master, callback=self.keypress, suppress=True)

    def keypress(self, event):
        double = (time.time() - self.lastHit) < self.timeout
        if event.event_type == self.lastType:
            return None
        else:
            self.lastType = event.event_type

        if double and event.event_type == keyboard.KEY_DOWN:
            self.deactivate()
            keyboard.send(self.master)
        elif event.event_type == keyboard.KEY_DOWN:
            self.lastHit = time.time()
            self.activate()
        elif event.event_type == keyboard.KEY_UP:
            self.deactivate()

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True
