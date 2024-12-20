import os
import json
import gspread
import oauth2client.service_account
import math
import re
import pyautogui
import pygetwindow
import keyboard
import tkinter
from tkinter import font, messagebox, StringVar
from PIL import Image, ImageGrab, ImageTk
from datetime import datetime
import globals as G

dirname = os.path.dirname(__file__)

if not os.path.isfile(os.path.join(dirname, "states.json")):
    with open(os.path.join(dirname, "states.json"), "w") as states_file:
        json.dump(G.DEFAULT_STATES, states_file, indent=2)
states = json.load(open("states.json"))
if len(states) != len(G.DEFAULT_STATES):
    for key, value in G.DEFAULT_STATES.items():
        if key not in states.keys():
            states[key] = G.DEFAULT_STATES[key].copy()
    with open(os.path.join(dirname, "states.json"), "w") as states_file:
        json.dump(G.DEFAULT_STATES, states_file, indent=2)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name("tracker_sheet_key.json", scope)
connection = gspread.authorize(credentials)
spreadsheet = connection.open("Flight Rising Utilities")
data_sheet = spreadsheet.worksheet("Session Data")
stats_sheet = spreadsheet.worksheet("Stats and Pics")
references_sheet = spreadsheet.worksheet("References")

RARE_ITEM_REGEX = re.compile("|".join(val[0] for val in references_sheet.get_values("F2:F")))

pyautogui.FAILSAFE = False

gui = tkinter.Tk()
gui.title("FR Coli Helper")
gui.geometry(f"{G.GUI_BOUNDS[2]-G.GUI_BOUNDS[0]}x{G.GUI_BOUNDS[3]-G.GUI_BOUNDS[1]}")
gui.geometry(f"+{G.GUI_BOUNDS[0]}+{G.GUI_BOUNDS[1]}")
gui.attributes("-topmost", True)
gui.option_add("*font", G.FONT)

has_uploaded = None
loot_last_battle = 0

venue = ""
def lock_in_venue():
    gui.protocol("WM_DELETE_WINDOW", close_action)

    global venue
    venue = venue_choice.get()
    if states["last_venue"] != venue:
        reset_states()
        states["last_venue"] = venue
    venue_selector.destroy()
    venue_confirm.destroy()
    
    gui.title(f"{gui.title()} - {venue}")

    total_battles_label.config(text=f"Battles: {states["battles"]}")

    found_venue = False
    for keybind_venue, keybinds in G.KEYBINDS.items():
        if keybind_venue == venue:
            for trigger, result in keybinds.items():
                keyboard.add_hotkey(trigger, lambda result=result: attack_and_abilities(result))
            found_venue = True
    if not found_venue:
        for trigger, result in G.KEYBINDS["Default"].items():
            keyboard.add_hotkey(trigger, lambda result=result: attack_and_abilities(result))

    keyboard.add_hotkey("space", fight_on)

    keyboard.add_hotkey("z", lambda: widget_value_window_check(currency_btn))

    keyboard.add_hotkey("/", lambda: widget_value_window_check(minor_hp_btn))
    keyboard.add_hotkey("*", lambda: widget_value_window_check(medium_hp_btn))
    keyboard.add_hotkey("-", lambda: widget_value_window_check(major_hp_btn))

    keyboard.add_hotkey("`", save_captcha)

    most_recent_loot_entry.grid(row=0, column=0, columnspan=3, sticky="nsew")

    raw_paste_box.grid(row=1, column=0, columnspan=3, sticky="nsew")

    for i, type in enumerate(G.LOOT_TYPES):
        loot_boxes[type].grid(row=2+math.trunc(i/3), column=i%3)

        loot_boxes[type].insert("1.0", f"{type}: {len(states[type])}")
        if len(states[type]) == 0: continue
        for loot in states[type]:
            loot_boxes[type].insert("end", f"\n{loot}")

    for loot in states["all_items"]:
        most_recent_loot_entry.insert(0, f"{loot}, ")
        raw_paste_box.insert(tkinter.END, f"[item={loot}] ")

    common_chest_btn.grid(row=5, column=0)

    to_sheet_button.grid(row=5, column=1)

    manual_input_button.grid(row=5, column=2)

    recent_loot_label.grid(row=4, column=0, columnspan=3)

    total_battles_label.grid(row=10, column=0)

    reset_states_btn.grid(row=10, column=1)

    currency_btn.grid(row=10, column=2)

    minor_hp_btn.grid(row=11, column=0)
    medium_hp_btn.grid(row=11, column=1)
    major_hp_btn.grid(row=11, column=2)

    rename_recent_chest_btn.grid(row=12, column=0, columnspan=3)

def close_action():
    if has_uploaded is not None and not has_uploaded:
        if messagebox.askokcancel("Exit", "Confirm exit? You have not yet uploaded data to the sheet."):
            with open("states.json", "w") as json_file:
                json.dump(states, json_file, indent=2)
            gui.destroy()
    else:
        with open("states.json", "w") as json_file:
            json.dump(states, json_file, indent=2)
        gui.destroy()

def send_to_sheet():
    loot = {}
    for type in G.LOOT_TYPES:
        loot[type] = loot_boxes[type].get("2.0", "end").replace("\n", ", ")

    active_row = int(stats_sheet.acell("D6").value)+2
    range_to_edit = data_sheet.range(active_row, 1, active_row, 9)
    range_to_edit[0].value = datetime.today().strftime("%m/%d/%Y")
    range_to_edit[1].value = venue
    num_battles = total_battles_label.cget("text")
    range_to_edit[2].value = num_battles[9:]
    
    for i, loot_arr in enumerate(loot.values()):
        if len(loot_arr) == 0:
            continue
        loot_arr = loot_arr[:-2]
        range_to_edit[i+3].value = loot_arr

    data_sheet.update_cells(range_to_edit, value_input_option="USER_ENTERED")

    reset_states()

    to_sheet_button.config(text="Successfully sent data")

    global has_uploaded
    has_uploaded = True

def reset_states():
    global states
    G.DEFAULT_STATES["last_venue"] = states["last_venue"]
    states = G.DEFAULT_STATES.copy()
    with open(os.path.join(dirname, "states.json"), "w") as states_file:
        json.dump(states, states_file, indent=2)

def setup_manual_input():
    manual_input_name_label.grid(row=6, column=0)
    manual_input_name_entry.grid(row=7, column=0)
    manual_input_num_label.grid(row=6, column=1)
    manual_input_num_entry.grid(row=7, column=1)
    manual_input_submit.grid(row=6, column=2, rowspan=2)

    for i in range(len(manual_input_radios)):
        manual_input_radios[i].grid(row=8+math.trunc(i/3), column=i%3)

def submit_manual_input():
    if manual_input_num_entry.get() not in ("1", "2", "3", "4"):
        return
    
    for _ in range(int(manual_input_num_entry.get())):
        add_loot(manual_input_name_entry.get(), input_var.get())

    manual_input_name_entry.delete(0, tkinter.END)
    manual_input_num_entry.delete(0, tkinter.END)
    manual_input_num_entry.insert(0, "1")
    input_var.set("Apparel")

    manual_input_name_label.grid_forget()
    manual_input_name_entry.grid_forget()
    manual_input_num_label.grid_forget()
    manual_input_num_entry.grid_forget()
    manual_input_submit.grid_forget()

    for i in range(6):
        manual_input_radios[i].grid_forget()

def setup_rename_most_recent_chest():
    if most_recent_chest == "N/A":
        return
    
    rename_recent_chest_btn.grid_forget()
    rename_recent_chest_btn.grid(row=12, column=0)
    rename_recent_chest_entry.grid(row=12, column=1)
    rename_recent_chest_submit.grid(row=12, column=2)

def submit_rename_most_recent_chest():
    global most_recent_chest

    rename_recent_chest_btn.grid_forget()
    rename_recent_chest_entry.grid_forget()
    rename_recent_chest_submit.grid_forget()
    rename_recent_chest_btn.grid(row=12, column=1)

    new_chest_name = rename_recent_chest_entry.get()

    most_recent_loot = most_recent_loot_entry.get()
    most_recent_loot = f"{new_chest_name}{most_recent_loot[most_recent_loot.index(','):]}"
    most_recent_loot_entry.delete(0, tkinter.END)
    most_recent_loot_entry.insert(0, most_recent_loot)

    raw_paste = raw_paste_box.get()
    raw_paste = f"{raw_paste[:raw_paste.rindex(most_recent_chest)]}{new_chest_name}] "
    raw_paste_box.delete(0, tkinter.END)
    raw_paste_box.insert(0, raw_paste)

    loot_box = loot_boxes["Miscellaneous"].get("1.0", tkinter.END)
    loot_box = f"{loot_box[:loot_box.rindex(most_recent_chest)]}{new_chest_name}{loot_box[loot_box.rindex(most_recent_chest)+len(most_recent_chest):]}"
    loot_box = loot_box[:-1]
    loot_boxes["Miscellaneous"].delete("1.0", tkinter.END)
    loot_boxes["Miscellaneous"].insert("1.0", loot_box)

    most_recent_chest = "N/A"

def fight_on():
    if pygetwindow.getActiveWindow().title != "Flight Rising — Mozilla Firefox":
        return

    try:
        pyautogui.locateOnScreen(os.path.join(dirname, "images", "loot.png"), region=G.LOOT_TITLE_BOUNDS, confidence=0.97)
    except pyautogui.ImageNotFoundException:
        return

    increment_widget_value(total_battles_label)
    states["battles"] += 1

    loot_image = ImageGrab.grab(bbox=G.LOOT_ITEM_BOUNDS)
    loot_image.save(os.path.join(dirname, "recent_loot.png"))

    coli_screen_img = ImageGrab.grab(bbox=G.COLI_SCREEN_BOUNDS)
    coli_screen_img.save(os.path.join(dirname, "recent_coli_screen.png"))

    gui_loot_image = ImageTk.PhotoImage(loot_image)
    recent_loot_label.config(image=gui_loot_image)
    recent_loot_label.image = gui_loot_image

    pyautogui.moveTo(1250, 850)
    pyautogui.click()

    search_loot(loot_image)

def search_loot(loot_image):
    match_list = []
    for folder_path in os.listdir(os.path.join(dirname, "images", venue)):
        for image_filename in os.listdir(os.path.join(dirname, "images", venue, folder_path)):
            if ".ini" in image_filename:
                continue
            try:
                pyautogui.locate(os.path.join(dirname, "images", venue, folder_path, image_filename), loot_image, confidence=0.922)
            except pyautogui.ImageNotFoundException:
                pass
            else:
                match_list.append((image_filename.replace(".png", "").replace("~~", ":"), folder_path))
    for folder_path in os.listdir(os.path.join(dirname, "images", "Universal")):
        for image_filename in os.listdir(os.path.join(dirname, "images", "Universal", folder_path)):
            if ".ini" in image_filename:
                continue
            try:
                pyautogui.locate(os.path.join(dirname, "images", "Universal", folder_path, image_filename), loot_image, confidence=0.922)
            except pyautogui.ImageNotFoundException:
                pass
            else:
                match_list.append((image_filename.replace(".png", "").replace("~~", ":"), folder_path))
    
    global loot_last_battle
    loot_last_battle = 0

    if len(match_list) == 1:
        add_loot(match_list[0][0], match_list[0][1])
    elif len(match_list) > 1:
        choose_loot(match_list)

def choose_loot(matches):
    tempgui = tkinter.Tk()
    tempgui.title("Drop Selector")
    tempgui.attributes("-topmost", True)

    tempgui_font = font.Font(family="Segoe UI", size=9)

    description_lbl = tkinter.Label(tempgui, text="Multiple drops detected.\nChoose the correct drop(s)", font=tempgui_font)

    drop_btns = []
    for drop in matches:
        drop_btns.append(tkinter.Button(tempgui, text=drop[0], command=lambda drop=drop: add_loot(drop[0], drop[1]), font=tempgui_font))
    
    description_lbl.pack()
    for btn in drop_btns:
        btn.pack()
    
    close_btn = tkinter.Button(tempgui, text="Close", command=lambda: tempgui.destroy(), font=tempgui_font)
    close_btn.pack()

    tempgui.geometry(f"250x{len(drop_btns) * 35 + 85}")
    tempgui.geometry("+470+100")
    tempgui.mainloop()

def add_loot(name, type):
    if type == "Common Chests":
        increment_widget_value(common_chest_btn)
        return

    most_recent_loot_entry.insert(0, f"{name}, ")
    raw_paste_box.insert(tkinter.END, f"[item={name}] ")
    loot_boxes[type].insert("end", f"\n{name}")
    
    line_index = loot_boxes[type].search("\n", "1.0", stopindex="end")
    first_line = loot_boxes[type].get("1.0", line_index)
    num_loot = int(first_line[first_line.index(": ")+2:]) + 1
    first_line = first_line[:first_line.index(": ")+2] + str(num_loot)
    loot_boxes[type].delete("1.0", f"1.{len(first_line)}")
    loot_boxes[type].insert("1.0", first_line)

    if name in G.GENERIC_CHESTS:
        global most_recent_chest
        most_recent_chest = name
        rename_recent_chest_btn.config(text=f"Rename last chest")
    else:
        states["all_items"].append(name)
        states[type].append(name)
        with open(os.path.join(dirname, "states.json"), "w") as states_file:
            json.dump(states, states_file, indent=2)

    if not os.path.isdir(os.path.join(dirname, "saved_images")):
        os.makedirs(os.path.join(dirname, "saved_images"))
    
    global loot_last_battle
    loot_last_battle += 1
    if type == "Boss Familiars" or type == "Genes" or loot_last_battle > 1 or RARE_ITEM_REGEX.match(name):
        Image.open(os.path.join(dirname, "recent_loot.png")).save(os.path.join(dirname, "saved_images", f"loot {datetime.now().strftime("%m-%d-%y %H.%M.%S")}.png"))

    global has_uploaded
    if has_uploaded is None:
        has_uploaded = False

def increment_widget_value(widget):
    widget_str = widget.cget("text")
    widget_num = int(widget_str[widget_str.index(": ")+2:]) + 1
    widget_str = widget_str[:widget_str.index(": ")+2]
    widget.config(text=f"{widget_str}{widget_num}")
   
def widget_value_window_check(button):
    if pygetwindow.getActiveWindow().title != "Flight Rising — Mozilla Firefox":
        return
    increment_widget_value(button)

is_attacking = False
def attack_and_abilities(keys):
    global is_attacking
    if is_attacking:
        return
    if pygetwindow.getActiveWindow().title != "Flight Rising — Mozilla Firefox":
        return
    
    is_attacking = True
    pyautogui.press(keys[0])
    pyautogui.press(keys[1])
    pyautogui.press(keys[2])
    is_attacking = False

def save_captcha():
    if pygetwindow.getActiveWindow().title != "Flight Rising — Mozilla Firefox":
        return
    
    try:
        pyautogui.locateOnScreen(os.path.join(dirname, "images", "camping.png"), region=G.CAMPING_TITLE_BOUNDS, confidence=0.97)
    except pyautogui.ImageNotFoundException:
        return
    
    captcha_image = ImageGrab.grab(bbox=G.CAPTCHA_BOUNDS)
    if not os.path.isdir(os.path.join(dirname, "captchas")):
        os.makedirs(os.path.join(dirname, "captchas"))
    captcha_image.save(os.path.join(dirname, "captchas", f"captcha{len(os.listdir(os.path.join(dirname, 'captchas')))}.png"))

venue_choice = StringVar()
venue_choice.set(states["last_venue"])
venue_selector = tkinter.OptionMenu(gui, venue_choice, *G.VENUE_NAMES)
venue_selector.pack()

bold_font = font.nametofont("TkDefaultFont")
bold_font.configure(weight="bold", size=11)

most_recent_loot_entry = tkinter.Entry(gui, font=bold_font)
raw_paste_box = tkinter.Entry(gui)

loot_boxes = {}
for type in G.LOOT_TYPES:
    loot_boxes[type] = tkinter.Text(gui, width=22, height=11)

common_chest_btn = tkinter.Button(gui, text="Common chests: 0", command=lambda: increment_widget_value(common_chest_btn))

to_sheet_button = tkinter.Button(gui, text="Send data to sheet", command=send_to_sheet)

manual_input_button = tkinter.Button(gui, text="Manually input data", command=setup_manual_input)
manual_input_name_label = tkinter.Label(gui, text="Name")
manual_input_name_entry = tkinter.Entry(gui)
manual_input_num_label = tkinter.Label(gui, text="Amount")
manual_input_num_entry = tkinter.Entry(gui)
manual_input_num_entry.insert(0, "1")
manual_input_submit = tkinter.Button(gui, text="Submit", command=submit_manual_input)
input_var = StringVar()
input_var.set("Apparel")

manual_input_radios = []
for type in G.LOOT_TYPES:
    manual_input_radios.append(tkinter.Radiobutton(gui, text=type, variable=input_var, value=type))

total_battles_label = tkinter.Label(gui, text="Battles: 0")

reset_states_btn = tkinter.Button(gui, text="Reset states", command=reset_states)

currency_btn = tkinter.Button(gui, text="Fest Currency: 0", command=lambda: increment_widget_value(currency_btn))

minor_hp_btn = tkinter.Button(gui, text="Minor HP Potions: 0", command=lambda: increment_widget_value(minor_hp_btn))
medium_hp_btn = tkinter.Button(gui, text="Medium HP Potions: 0", command=lambda: increment_widget_value(medium_hp_btn))
major_hp_btn = tkinter.Button(gui, text="Major HP Potions: 0", command=lambda: increment_widget_value(major_hp_btn))

most_recent_chest = "N/A"
rename_recent_chest_btn = tkinter.Button(gui, text=f"Rename last chest", command=setup_rename_most_recent_chest)
rename_recent_chest_entry = tkinter.Entry(gui)
rename_recent_chest_submit = tkinter.Button(gui, text="Submit", command=submit_rename_most_recent_chest)

gui_loot_image = None
recent_loot_label = tkinter.Label(gui, image=gui_loot_image)

venue_confirm = tkinter.Button(gui, text="Confirm Selection", command=lock_in_venue)
venue_confirm.pack()

gui.mainloop()