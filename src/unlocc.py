from PIL import Image, ImageDraw
from keybrain import KeyBrain
from gui import GUI
import pystray
import sys
import threading

enabled = True
keybrain = KeyBrain('caps lock')
tray = pystray.Icon('Unlocc')
confGUI = None


def create_image():
    # Generate an image and draw a pattern
    width = 20
    height = 20
    color1 = '#000000ff'
    color2 = '#0000ff00'
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image


def launch_settings():
    global confGUI, keybrain
    keybrain.shutdown()
    confGUI = GUI()
    guiThread = threading.Thread(target=confGUI.launch)
    guiThread.start()
    guiThread.join()
    keybrain = KeyBrain('caps lock')


def on_enabled(icon, item):
    global enabled, keybrain
    enabled = not item.checked

    if not enabled and keybrain is not None:
        keybrain.shutdown()
        keybrain = None
    elif enabled:
        if keybrain is None:
            keybrain = KeyBrain('caps lock')
        else:
            keybrain.shutdown()
            keybrain = None
            keybrain = KeyBrain('caps lock')


def terminate():
    global keybrain, tray
    if keybrain is not None:
        keybrain.shutdown()
    if tray is not None:
        tray.stop()
    sys.exit()


def create_menu():
    global enabled
    menu = pystray.Menu(
        pystray.MenuItem('Settings', launch_settings),
        pystray.MenuItem(
            'Enabled',
            on_enabled,
            checked=lambda item: enabled
        ),
        pystray.MenuItem('Exit', terminate)
    )
    return menu


tray = pystray.Icon('Unlocc', menu=create_menu())

tray.icon = create_image()
tray.run()
