import os
import gspread
import oauth2client.service_account
import pyautogui
import pygetwindow
import keyboard
import tkinter
from tkinter import StringVar, font, messagebox
from PIL import Image, ImageGrab, ImageTk

dirname = os.path.dirname(__file__)

VENUE_NAMES = (
    "Training Fields",
    "Woodland Path",
    "Scorched Forest",
    "Sandswept Delta",
    "Silk-Strewn Wreckage",
    "Blooming Grove",
    "Forgotten Cave",
    "Bamboo Falls",
    "Thunderhead Savanna",
    "Redrock Cove",
    "Waterway",
    "Arena",
    "Volcanic Vents",
    "Rainsong Jungle",
    "Boreal Wood",
    "Crystal Pools",
    "Harpy's Roost",
    "Ghostlight Ruins",
    "Mire",
    "Kelp Beds",
    "Golem Workshop",
    "Forbidden Portal"
)

DEFAULT_VENUE = "Redrock Cove"

LOOT_TITLE_BOUNDS = (1250, 450, 1367, 507)

LOOT_ITEM_BOUNDS = (1105, 511, 1340, 745)

COLI_SCREEN_BOUNDS = (700, 400, 1400, 930)

LEFT_SCREEN_BBOX = ((0, 100), (466, 1079))

GENERIC_CHESTS = (
    "Brightshine Jubilee Chest",
    "Crystalline Gala Chest", 
    "Greenskeeper Gathering Chest",
    "Flameforger's Festival Chest",
    "Mistral Jamboree Chest",
    "Riot of Rot Chest",
    "Rockbreaker's Ceremony Chest",
    "Starfall Celebration Chest",
    "Thundercrack Carnivale Chest",
    "Trickmurk Circus Chest",
    "Wavecrest Saturnalia Chest",
    "Arena Crate",
    "Bamboo Falls Crate",
    "Blooming Grove Crate",
    "Boreal Wood Crate",
    "Crystal Pools Crate",
    "Forbidden Portal Crate",
    "Forgotten Cave Crate",
    "Ghostlight Ruins Crate",
    "Golem Workshop Crate",
    "Harpy's Roost Crate",
    "Kelp Beds Crate",
    "Mire Crate",
    "Rainsong Jungle Crate",
    "Redrock Cove Crate",
    "Sandswept Delta Crate",
    "Scorched Forest Crate",
    "Silk-Strewn Wreckage Crate",
    "Thunderhead Savanna Crate",
    "Training Fields Crate",
    "Volcanic Vents Crate",
    "Waterway Crate",
    "Woodland Path Crate"
)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name("tracker_sheet_key.json", scope)
gc = gspread.authorize(credentials)
sheet = gc.open("Flight Rising Utilities")
sheet = sheet.sheet1

gui = tkinter.Tk()
gui.title("FR Coli Helper")
gui.geometry(f"{LEFT_SCREEN_BBOX[1][0]-LEFT_SCREEN_BBOX[0][0]}x{LEFT_SCREEN_BBOX[1][1]-LEFT_SCREEN_BBOX[0][1]}")
gui.geometry(f"+{LEFT_SCREEN_BBOX[0][0]}+{LEFT_SCREEN_BBOX[0][1]}")
gui.attributes("-topmost", True)

has_uploaded = None

def on_close():
    if has_uploaded is not None and not has_uploaded:
        if messagebox.askokcancel("Exit", "Confirm exit? You have not yet uploaded data to the sheet."):
            gui.destroy()
    else:
        gui.destroy()

venue_choice = StringVar()
venue_choice.set(DEFAULT_VENUE)

venue_selector = tkinter.OptionMenu(gui, venue_choice, *VENUE_NAMES)
venue_selector.pack()

default_font = font.Font(family="Helvetica", size=10)
bold_font = font.Font(family="Helvetica", size=10, weight="bold")

most_recent_loot_entry = tkinter.Entry(gui, font=bold_font)
raw_paste_box = tkinter.Entry(gui, font=default_font)

loot_boxes = {
    "Apparel": tkinter.Text(gui, width=22, height=11, font=default_font),
    "Battle Stones": tkinter.Text(gui, width=22, height=11, font=default_font),
    "Boss Familiars": tkinter.Text(gui, width=22, height=11, font=default_font),
    "Genes": tkinter.Text(gui, width=22, height=11, font=default_font),
    "Miscellaneous": tkinter.Text(gui, width=22, height=11, font=default_font),
    "NonBoss Familiars": tkinter.Text(gui, width=22, height=11, font=default_font)
}

def add_one_common_chest():
    chest_str = common_chest_btn.cget("text")
    chest_num = chest_str[chest_str.index(": ")+2:]
    chest_num = int(chest_num) + 1
    common_chest_btn.config(text=f"Common chests: {chest_num}")

common_chest_btn = tkinter.Button(gui, text="Common chests: 0", command=add_one_common_chest, font=default_font)

def send_to_sheet():
    loot = {
        "Apparel": loot_boxes["Apparel"].get("2.0", "end").split("\n"),
        "Battle Stones": loot_boxes["Battle Stones"].get("2.0", "end").split("\n"),
        "Boss Familiars": loot_boxes["Boss Familiars"].get("2.0", "end").split("\n"),
        "Genes": loot_boxes["Genes"].get("2.0", "end").split("\n"),
        "Miscellaneous": loot_boxes["Miscellaneous"].get("2.0", "end").split("\n"),
        "NonBoss Familiars": loot_boxes["NonBoss Familiars"].get("2.0", "end").split("\n")
    }

    for loot_type, loot_arr in loot.items():
        active_column = ""
        for index, cell in enumerate(sheet.range("B3:G3")):
            if cell.value == loot_type:
                active_column = chr(ord("B") + index)
                break
        
        active_row = ""
        for index, cell in enumerate(sheet.range(f"{active_column}4:{active_column}")):
            if cell.value == "":
                active_row = index + 4
                break

        for loot_name in loot_arr:
            sheet.update_acell(active_column + str(active_row), loot_name)
            active_row += 1
        
        global has_uploaded
        has_uploaded = True

to_sheet_button = tkinter.Button(gui, text="Send data to sheet", command=send_to_sheet, font=default_font)

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

    manual_input_radios[0].grid_forget()
    manual_input_radios[1].grid_forget()
    manual_input_radios[2].grid_forget()
    manual_input_radios[3].grid_forget()
    manual_input_radios[4].grid_forget()
    manual_input_radios[5].grid_forget()

manual_input_name_label = tkinter.Label(gui, text="Name", font=default_font)
manual_input_name_entry = tkinter.Entry(gui, font=default_font)
manual_input_num_label = tkinter.Label(gui, text="Amount", font=default_font)
manual_input_num_entry = tkinter.Entry(gui, font=default_font)
manual_input_num_entry.insert(0, "1")
manual_input_submit = tkinter.Button(gui, text="Submit", font=default_font, command=submit_manual_input)

input_var = StringVar()
input_var.set("Apparel")
manual_input_radios = (
    tkinter.Radiobutton(gui, text="Apparel", font=default_font, variable=input_var, value="Apparel"),
    tkinter.Radiobutton(gui, text="Battle Stones", font=default_font, variable=input_var, value="Battle Stones"),
    tkinter.Radiobutton(gui, text="Boss Familiars", font=default_font, variable=input_var, value="Boss Familiars"),
    tkinter.Radiobutton(gui, text="Genes", font=default_font, variable=input_var, value="Genes"),
    tkinter.Radiobutton(gui, text="Miscellaneous", font=default_font, variable=input_var, value="Miscellaneous"),
    tkinter.Radiobutton(gui, text="NonBoss Familiars", font=default_font, variable=input_var, value="NonBoss Familiars")
)

def manual_data():
    manual_input_name_label.grid(row=6, column=0)
    manual_input_name_entry.grid(row=7, column=0)
    manual_input_num_label.grid(row=6, column=1)
    manual_input_num_entry.grid(row=7, column=1)
    manual_input_submit.grid(row=6, column=2, rowspan=2)

    manual_input_radios[0].grid(row=8, column=0)
    manual_input_radios[1].grid(row=8, column=1)
    manual_input_radios[2].grid(row=8, column=2)
    manual_input_radios[3].grid(row=9, column=0)
    manual_input_radios[4].grid(row=9, column=1)
    manual_input_radios[5].grid(row=9, column=2)

manual_add_button = tkinter.Button(gui, text="Manually input data", command=manual_data, font=default_font)

total_battles_label = tkinter.Label(gui, text="Battles: 0", font=default_font)

def add_fest_currency():
    currency_str = currency_btn.cget("text")
    currency_num = currency_str[currency_str.index(": ")+2:]
    currency_num = int(currency_num) + 1
    currency_btn.config(text=f"Fest Currency: {currency_num}")

currency_btn = tkinter.Button(gui, text="Fest Currency: 0", command=add_fest_currency, font=default_font)

def add_minor():
    minor_str = minor_hp_btn.cget("text")
    minor_num = minor_str[minor_str.index(": ")+2:]
    minor_num = int(minor_num) + 1
    minor_hp_btn.config(text=f"Minor HP Potions: {minor_num}")

def add_medium():
    medium_str = medium_hp_btn.cget("text")
    medium_num = medium_str[medium_str.index(": ")+2:]
    medium_num = int(medium_num) + 1
    medium_hp_btn.config(text=f"Medium HP Potions: {medium_num}")

def add_major():
    major_str = major_hp_btn.cget("text")
    major_num = major_str[major_str.index(": ")+2:]
    major_num = int(major_num) + 1
    major_hp_btn.config(text=f"Major HP Potions: {major_num}")

minor_hp_btn = tkinter.Button(gui, text="Minor HP Potions: 0", command=add_minor, font=default_font)
medium_hp_btn = tkinter.Button(gui, text="Medium HP Potions: 0", command=add_medium, font=default_font)
major_hp_btn = tkinter.Button(gui, text="Major HP Potions: 0", command=add_major, font=default_font)

def rename_most_recent_chest():
    if most_recent_chest == "N/A":
        return
    
    rename_recent_chest_btn.grid_forget()
    rename_recent_chest_btn.grid(row=12, column=0)
    rename_recent_chest_entry.grid(row=12, column=1)
    rename_recent_chest_submit.grid(row=12, column=2)

def rename_most_recent_chest_submit():
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

most_recent_chest = "N/A"
rename_recent_chest_btn = tkinter.Button(gui, text=f"Rename last chest", command=rename_most_recent_chest, font=default_font)
rename_recent_chest_entry = tkinter.Entry(gui, font=default_font)
rename_recent_chest_submit = tkinter.Button(gui, text="Submit", command=rename_most_recent_chest_submit, font=default_font)

gui_loot_image = None
recent_loot_label = tkinter.Label(gui, image=gui_loot_image)

venue = ""
def lock_venue():
    gui.protocol("WM_DELETE_WINDOW", on_close)

    global venue
    venue = venue_choice.get()
    venue_selector.destroy()
    venue_confirm.destroy()
    reconfigure_bounds.destroy()

    keyboard.add_hotkey("1", scratch_1)
    keyboard.add_hotkey("2", scratch_2)
    keyboard.add_hotkey("3", scratch_3)
    keyboard.add_hotkey("4", scratch_4)
    keyboard.add_hotkey("q", elim_1)
    keyboard.add_hotkey("w", elim_2)
    keyboard.add_hotkey("e", elim_3)
    keyboard.add_hotkey("r", elim_4)
    keyboard.add_hotkey("t", rally_1)
    keyboard.add_hotkey("y", haste_1)

    keyboard.add_hotkey("space", space_key)

    keyboard.add_hotkey("z", fest_currency_key)

    keyboard.add_hotkey("/", minor_hp_key)
    keyboard.add_hotkey("*", medium_hp_key)
    keyboard.add_hotkey("-", major_hp_key)

    most_recent_loot_entry.grid(row=0, column=0, columnspan=3, sticky="nsew")

    raw_paste_box.grid(row=1, column=0, columnspan=3, sticky="nsew")
    raw_paste_box.insert(0, "Raw: ")

    loot_boxes["Apparel"].grid(row=2, column=0)
    loot_boxes["Battle Stones"].grid(row=2, column=1)
    loot_boxes["Boss Familiars"].grid(row=2, column=2)
    loot_boxes["Genes"].grid(row=3, column=0)
    loot_boxes["Miscellaneous"].grid(row=3, column=1)
    loot_boxes["NonBoss Familiars"].grid(row=3, column=2)

    loot_boxes["Apparel"].insert("1.0", "Apparel: 0")
    loot_boxes["Battle Stones"].insert("1.0", "Battle Stones: 0")
    loot_boxes["Boss Familiars"].insert("1.0", "Boss Familiars: 0")
    loot_boxes["Genes"].insert("1.0", "Genes: 0")
    loot_boxes["Miscellaneous"].insert("1.0", "Miscellaneous: 0")
    loot_boxes["NonBoss Familiars"].insert("1.0", "NonBoss Familiars: 0")

    common_chest_btn.grid(row=5, column=0)

    to_sheet_button.grid(row=5, column=1)

    manual_add_button.grid(row=5, column=2)

    recent_loot_label.grid(row=4, column=0, columnspan=3)

    total_battles_label.grid(row=10, column=0)

    currency_btn.grid(row=10, column=2)

    minor_hp_btn.grid(row=11, column=0)
    medium_hp_btn.grid(row=11, column=1)
    major_hp_btn.grid(row=11, column=2)

    rename_recent_chest_btn.grid(row=12, column=0, columnspan=3)

venue_confirm = tkinter.Button(gui, text="Confirm Selection", command=lock_venue)
venue_confirm.pack()

anti_repeat = False
def scratch_1():
    global anti_repeat

    if anti_repeat:
        return

    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    anti_repeat = True
    pyautogui.press("a")
    pyautogui.press("e")
    pyautogui.press("q")
    anti_repeat = False
def scratch_2():
    global anti_repeat

    if anti_repeat:
        return

    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    anti_repeat = True
    pyautogui.press("a")
    pyautogui.press("e")
    pyautogui.press("w")
    anti_repeat = False
def scratch_3():
    global anti_repeat

    if anti_repeat:
        return

    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    anti_repeat = True
    pyautogui.press("a")
    pyautogui.press("e")
    pyautogui.press("e")
    anti_repeat = False
def scratch_4():
    global anti_repeat

    if anti_repeat:
        return

    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    anti_repeat = True
    pyautogui.press("a")
    pyautogui.press("e")
    pyautogui.press("r")
    anti_repeat = False

def elim_1():
    global anti_repeat

    if anti_repeat:
        return

    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    anti_repeat = True
    pyautogui.press("a")
    pyautogui.press("a")
    pyautogui.press("q")
    anti_repeat = False
def elim_2():
    global anti_repeat

    if anti_repeat:
        return

    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    anti_repeat = True
    pyautogui.press("a")
    pyautogui.press("a")
    pyautogui.press("w")
    anti_repeat = False
def elim_3():
    global anti_repeat

    if anti_repeat:
        return

    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    anti_repeat = True
    pyautogui.press("a")
    pyautogui.press("a")
    pyautogui.press("e")
    anti_repeat = False
def elim_4():
    global anti_repeat

    if anti_repeat:
        return

    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    anti_repeat = True
    pyautogui.press("a")
    pyautogui.press("a")
    pyautogui.press("r")
    anti_repeat = False

def rally_1():
    global anti_repeat

    if anti_repeat:
        return

    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    anti_repeat = True
    pyautogui.press("a")
    pyautogui.press("s")
    pyautogui.press("a")
    anti_repeat = False

def haste_1():
    global anti_repeat

    if anti_repeat:
        return

    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    anti_repeat = True
    pyautogui.press("a")
    pyautogui.press("d")
    pyautogui.press("a")
    anti_repeat = False

def space_key():
    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return

    if not pyautogui.locateOnScreen(os.path.join(dirname, "images", "loot.png"), region=LOOT_TITLE_BOUNDS, confidence=0.97):
        return

    battles_str = total_battles_label.cget("text")
    battles_num = int(battles_str[battles_str.index(": ")+2:]) + 1
    total_battles_label.config(text=f"Battles: {battles_num}")

    loot_image = ImageGrab.grab(bbox=LOOT_ITEM_BOUNDS)
    loot_image.save(os.path.join(dirname, "recent_loot.png"))

    coli_screen_img = ImageGrab.grab(bbox=COLI_SCREEN_BOUNDS)
    coli_screen_img.save(os.path.join(dirname, "recent_coli_screen.png"))

    gui_loot_image = ImageTk.PhotoImage(loot_image)
    recent_loot_label.config(image=gui_loot_image)
    recent_loot_label.image = gui_loot_image

    pyautogui.moveTo(1200, 800)
    pyautogui.click()

    search_rewards(loot_image)

def fest_currency_key():
    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    add_fest_currency()
def minor_hp_key():
    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    add_minor()
def medium_hp_key():
    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    add_medium()
def major_hp_key():
    if (pygetwindow.getActiveWindow().title != "Flight Rising - Brave"):
        return
    
    add_major()

def search_rewards(loot_image):
    match_list = []
    for folder_path in os.listdir(os.path.join(dirname, "images", venue)):
        for image_filename in os.listdir(os.path.join(dirname, "images", venue, folder_path)):
            if ".ini" in image_filename:
                continue
            location = pyautogui.locate(os.path.join(dirname, "images", venue, folder_path, image_filename), loot_image, confidence=0.922)
            if location:
                match_list.append((image_filename.replace(".png", ""), folder_path))
    if len(match_list) == 1:
        add_loot(match_list[0][0], match_list[0][1])
    elif len(match_list) > 1:
        choose_drops(match_list)

def choose_drops(matches):
    tempgui = tkinter.Tk()
    tempgui.title("Drop Selector")
    tempgui.attributes("-topmost", True)

    description_lbl = tkinter.Label(tempgui, text="Multiple drops detected.\nChoose the correct drop(s)", font=default_font)

    drop_btns = []
    for drop in matches:
        drop_btns.append(tkinter.Button(tempgui, text=drop[0], command=lambda name=drop[0], loc=drop[1]: add_loot(name, loc), font=default_font))
    
    description_lbl.pack()
    for btn in drop_btns:
        btn.pack()
    
    close_btn = tkinter.Button(tempgui, text="Close", command=lambda: close_tempgui(tempgui), font=default_font)
    close_btn.pack()

    tempgui.geometry(f"250x{len(drop_btns) * 35 + 85}")
    tempgui.geometry("+470+100")
    tempgui.mainloop()

def close_tempgui(tempgui):
    tempgui.destroy()

def add_loot(name, type):
    name = name.replace("~~", ":")

    if type == "Common Chests":
        add_one_common_chest()
        return

    most_recent_loot_entry.insert(0, f"{name}, ")
    raw_paste_box.insert(tkinter.END, f"[item={name}] ")
    loot_boxes[type].insert("end", f"\n{name}")
    
    line_index = loot_boxes[type].search("\n", "1.0", stopindex="end")
    first_line = loot_boxes[type].get("1.0", line_index)
    num_loot = int(first_line[first_line.index(": ")+2:])
    num_loot += 1
    first_line = first_line[:first_line.index(": ")+2] + str(num_loot)
    loot_boxes[type].delete("1.0", f"1.{len(first_line)}")
    loot_boxes[type].insert("1.0", first_line)

    global has_uploaded
    if has_uploaded is None:
        has_uploaded = False
    
    if name in GENERIC_CHESTS:
        global most_recent_chest
        most_recent_chest = name
        rename_recent_chest_btn.config(text=f"Rename last chest")

def change_bboxes():
    config_gui = tkinter.Tk()
    config_gui.title("Configure Bounds")
    config_gui.attributes("-topmost", True)
    config_gui.geometry("250x250")
    config_gui.geometry("+470+100")

    # change bboxes here

    config_gui.mainloop()

reconfigure_bounds = tkinter.Button(gui, text="Configure Bounds", command=change_bboxes)
reconfigure_bounds.pack()

gui.mainloop()