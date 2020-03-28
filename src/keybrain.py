import keyboard
import time


class KeyBrain:

    active = False                  # whether unlocc is active or not
    master = 'caps lock'            # master key identity
    lastHit = 0                     # time at which master key was last hit
    timeout = 0.3                   # second timeout between presses for double
    recordMode = False
    recordedEvents = []
    hook = None

    def __init__(self, master):
        self.master = master
        self.init_master()

    def init_master(self):
        keyboard.on_press_key(
            key=self.master, callback=self.keypress, suppress=True)
        keyboard.on_release_key(
            key=self.master, callback=self.keypress, suppress=True)

    def keypress(self, event):
        down = event.event_type == keyboard.KEY_DOWN
        double = down and ((time.time() - self.lastHit) < self.timeout)

        if event.event_type == keyboard.KEY_DOWN:
            print(time.time() - self.lastHit)

        if double:
            print('sending a turnon')
            self.deactivate()
            keyboard.send(self.master)
        elif event.event_type == keyboard.KEY_DOWN:
            self.lastHit = time.time()
            self.activate()
        elif event.event_type == keyboard.KEY_UP:
            self.deactivate()

    def deactivate(self):
        if self.active:
            self.active = False
            keyboard.unhook_all()
            self.init_master()
            self.recordedEvents = []

    def activate(self):
        if not self.active:
            self.recordedEvents = []
            self.active = True

            callback = self.record if self.recordMode else self.receive
            self.hook = keyboard.hook(callback=callback, suppress=True)

    def record(self, event):
        if event.name == self.master:
            self.deactivate()
        elif event.event_type == keyboard.KEY_DOWN:
            self.recordedEvents.append(event)

    def receive(self, event):
        if event.name == self.master:
            self.deactivate()
        else:
            keyboard.send(event.name)
