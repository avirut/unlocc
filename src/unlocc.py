import keyboard

recorded = keyboard.record(until='escape')

for keyPress in recorded:
    if keyPress.event_type == keyboard.KEY_DOWN:
        print(keyPress.name)
