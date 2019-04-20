import keyboard
from threading import Timer


masterTimer = None


def resetTimer():
    global masterTimer
    masterTimer.cancel()
    masterTimer = None
    print('reset the timer')


def handleMaster(key):
    global masterTimer
    if masterTimer is not None:
        print(masterTimer)
        keyboard.send(key.name)
    masterTimer = Timer(0.3, resetTimer)
    masterTimer.start()


keyboard.on_press_key(key='caps lock', callback=handleMaster, suppress=True)

# keyboard.on_press(callback=lambda key: print('pressed ' + key.name))

input('hello')
