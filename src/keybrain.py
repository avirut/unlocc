import keyboard
import time


class KeyBrain:

    active = False                  # whether unlocc is active or not
    master = 'caps lock'            # master key identity
    lastHit = 0                     # time at which master key was last hit
    timeout = 0.3                   # second timeout between presses for double
    lastType = keyboard.KEY_UP      # type of last keypress
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
        double = (time.time() - self.lastHit) < self.timeout

        if event.event_type == self.lastType:
            return None
        else:
            self.lastType = event.event_type

        if event.event_type == keyboard.KEY_DOWN:
            print(time.time() - self.lastHit)

        if double and event.event_type == keyboard.KEY_DOWN:
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
            for event in self.recordedEvents:
                print(event)
                # self.active = self.active
            self.recordedEvents = []
            print('deactivated')

    def activate(self):
        if not self.active:
            self.recordedEvents = []
            self.active = True
            self.hook = keyboard.hook(callback=self.record, suppress=True)
            print('activated')

    def record(self, event):
        if event.name == self.master:
            self.deactivate()
        elif event.event_type == keyboard.KEY_DOWN:
            self.recordedEvents.append(event)
