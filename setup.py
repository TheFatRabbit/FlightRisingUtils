import tkinter
import pyautogui
import json
import keyboard
import time
import sys

# DEFAULT CONFIG JSON:
# {"keybind": "g", "screen_bbox": [700, 400, 1400, 1000]}

config = json.load(open("config.json"))

gui = tkinter.Tk()
gui.geometry("250x300")
gui.title("G&G Helper Setup")
gui.attributes("-topmost", True)

def set_keybind():
    hotkey_to_add = keybind_entry.get()

    try:
        keyboard.add_hotkey(hotkey_to_add, None)
        keyboard.remove_hotkey(hotkey_to_add)
    except:
        hotkey_to_add = None
    
    if hotkey_to_add is not None:
        keybind_entry.delete(0, tkinter.END)
        keybind_label.pack_forget()
        keybind_entry.pack_forget()
        keybind_submit.pack_forget()

        config["keybind"] = hotkey_to_add
        keybind_button.config(text=f"Keybind: {config['keybind']}")
        update_json()
    else:
        keybind_entry.delete(0, tkinter.END)
        keybind_entry.insert(0, "Invalid keybind")

keybind_label = tkinter.Label(gui, text="Enter the new keybind.")
keybind_entry = tkinter.Entry(gui)
keybind_submit = tkinter.Button(gui, text="Submit", command=set_keybind)

def reset_keybind():
    keybind_label.pack()
    keybind_entry.pack()
    keybind_submit.pack()

point_needed = None

def get_click_location(event):
    global point_needed
    x, y = pyautogui.position()
    print(x, y)
    if point_needed == "top_left":
        config["screen_bbox"][0] = x
        config["screen_bbox"][2] = y
        top_left_button.config(text="Set Top Left")
        gui.unbind("<Button-1>")
        update_json()
    elif point_needed == "bottom_right":
        config["screen_bbox"][1] = x
        config["screen_bbox"][3] = y
        bottom_right_button.config(text="Set Bottom Right")
        gui.unbind("<Button-1>")
        update_json()

    point_needed = None

def set_top_left():
    global point_needed
    top_left_button.config(text="Click top left corner")

    gui.bind("<Button-1>", get_click_location)
    point_needed = "top_left"

def set_bottom_right():
    global point_needed
    bottom_right_button.config(text="Click bottom right corner")

    gui.bind("<Button-1>", get_click_location)
    point_needed = "bottom_right"

keybind_button = tkinter.Button(gui, text=f"Keybind: {config['keybind']}", command=reset_keybind)
top_left_button = tkinter.Button(gui, text="Set Top Left", command=set_top_left)
bottom_right_button = tkinter.Button(gui, text="Set Bottom Right", command=set_bottom_right)

keybind_button.pack()
top_left_button.pack()
bottom_right_button.pack()

invalid_bbox_label = tkinter.Label(text="Invalid bounds.")

def update_json():
    if config["screen_bbox"][0] > config["screen_bbox"][2] or config["screen_bbox"][1] > config["screen_bbox"][3]:
        invalid_bbox_label.pack()
        return

    with open("config.json", "w") as json_file:
        json.dump(config, json_file)

def exit():
    sys.exit()

gui.mainloop()