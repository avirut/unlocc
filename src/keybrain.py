import keyboard
import time


class KeyBrain:

    active = False                  # whether unlocc is active or not
    master = 'caps lock'            # master key identity
    lastType = keyboard.KEY_UP
    lastHit = 0                     # time at which master key was last hit
    timeout = 0.3                   # second timeout between presses for double
    recordMode = True
    recordedEvents = []
    hook = None
    swaps = {}

    def __init__(self, master, recordmode, swaps):
        self.master = master
        self.recordMode = recordmode
        self.swaps = swaps
        self.init_master()

    def init_master(self):
        keyboard.hook_key(
            key=self.master, callback=self.masterpress, suppress=True)

    def masterpress(self, event):
        down = event.event_type == keyboard.KEY_DOWN
        double = down and ((time.time() - self.lastHit) < self.timeout)

        if down and self.lastType == keyboard.KEY_DOWN:
            return

        self.lastType = event.event_type

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

            if self.recordMode:
                typed = ''
                for event in self.recordedEvents:
                    typed += event.name
                if typed in self.swaps:
                    keyboard.write(self.swaps[typed])

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
            if event.event_type == keyboard.KEY_UP:
                self.lastType = event.event_type
                self.deactivate()
            else:
                return
        elif event.event_type == keyboard.KEY_DOWN:
            self.recordedEvents.append(event)

    def receive(self, event):
        if event.name == self.master:
            if event.event_type == keyboard.KEY_UP:
                self.lastType = event.event_type
                self.deactivate()
            else:
                return
        elif event.name in self.swaps:
            keyboard.write(self.swaps[event.name])
        else:
            keyboard.write(event.name)

    def shutdown(self):
        keyboard.unhook_all()


if __name__ == '__main__':
    keybrain = KeyBrain('caps lock')
