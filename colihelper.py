import os
import gspread
import oauth2client.service_account
import pyautogui
import pygetwindow
import keyboard
import tkinter
from tkinter import font, messagebox, StringVar
from PIL import ImageGrab, ImageTk
import globals as G

dirname = os.path.dirname(__file__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name("tracker_sheet_key.json", scope)
connection = gspread.authorize(credentials)
spreadsheet = connection.open("Flight Rising Utilities")
tracker_sheet = spreadsheet.worksheet(G.TRACKER_SHEET_NAME)
stats_sheet = spreadsheet.worksheet(G.STATS_SHEET_NAME)

gui = tkinter.Tk()
gui.title("FR Coli Helper")
gui.geometry(f"{G.LEFT_SCREEN_BBOX[1][0]-G.LEFT_SCREEN_BBOX[0][0]}x{G.LEFT_SCREEN_BBOX[1][1]-G.LEFT_SCREEN_BBOX[0][1]}")
gui.geometry(f"+{G.LEFT_SCREEN_BBOX[0][0]}+{G.LEFT_SCREEN_BBOX[0][1]}")
gui.attributes("-topmost", True)
gui.option_add("*font", G.FONT)

has_uploaded = None

venue = ""
def lock_in_venue():
    gui.protocol("WM_DELETE_WINDOW", close_action)

    global venue
    venue = venue_choice.get()
    venue_selector.destroy()
    venue_confirm.destroy()

    keyboard.add_hotkey("1", lambda: attack_and_abilities("a", "e", "q"))
    keyboard.add_hotkey("2", lambda: attack_and_abilities("a", "e", "w"))
    keyboard.add_hotkey("3", lambda: attack_and_abilities("a", "e", "e"))
    keyboard.add_hotkey("4", lambda: attack_and_abilities("a", "e", "r"))
    keyboard.add_hotkey("q", lambda: attack_and_abilities("a", "a", "q"))
    keyboard.add_hotkey("w", lambda: attack_and_abilities("a", "a", "w"))
    keyboard.add_hotkey("e", lambda: attack_and_abilities("a", "a", "e"))
    keyboard.add_hotkey("r", lambda: attack_and_abilities("a", "a", "r"))
    keyboard.add_hotkey("t", lambda: attack_and_abilities("a", "s", "a"))
    keyboard.add_hotkey("y", lambda: attack_and_abilities("a", "d", "a"))

    keyboard.add_hotkey("space", fight_on)

    keyboard.add_hotkey("z", lambda: check_active_window(currency_btn))

    keyboard.add_hotkey("/", lambda: check_active_window(minor_hp_btn))
    keyboard.add_hotkey("*", lambda: check_active_window(medium_hp_btn))
    keyboard.add_hotkey("-", lambda: check_active_window(major_hp_btn))

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

    manual_input_button.grid(row=5, column=2)

    recent_loot_label.grid(row=4, column=0, columnspan=3)

    total_battles_label.grid(row=10, column=0)

    currency_btn.grid(row=10, column=2)

    minor_hp_btn.grid(row=11, column=0)
    medium_hp_btn.grid(row=11, column=1)
    major_hp_btn.grid(row=11, column=2)

    rename_recent_chest_btn.grid(row=12, column=0, columnspan=3)

def close_action():
    if has_uploaded is not None and not has_uploaded:
        if messagebox.askokcancel("Exit", "Confirm exit? You have not yet uploaded data to the sheet."):
            gui.destroy()
    else:
        gui.destroy()

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
        for index, cell in enumerate(tracker_sheet.range("B3:G3")):
            if cell.value == loot_type:
                active_column = chr(ord("B") + index)
                break
        
        active_row = tracker_sheet.acell(f"{active_column}4")
        active_row = int(active_row[active_row.index(": ")+2:])+5
        final_row = str(active_row + len(loot_arr)-1)
        active_row = str(active_row)

        # instead of this, retrieve the value by parsing Cell(Col, 4)
        # active_row = ""
        # for index, cell in enumerate(tracker_sheet.range(f"{active_column}5:{active_column}")):
        #     if cell.value == "":
        #         active_row = index + 4
        #         break

        cells_to_update = tracker_sheet.range(f"{active_column}{active_row}:{active_column}{final_row}")
        for cell, loot_value in zip(cells_to_update, loot_arr):
            cell.value = loot_value

        tracker_sheet.update_cells(cells_to_update)

        # change to bulk addition
        # for loot_name in loot_arr:
        #     tracker_sheet.update_acell(active_column + str(active_row), loot_name)
        #     active_row += 1
    
    total_battles = total_battles_label.cget("text")
    total_battles = int(total_battles[total_battles.index(": ")+2:])
    total_battles += int(stats_sheet.acell("C3").value)
    stats_sheet.update_acell("C3", total_battles)

    global has_uploaded
    has_uploaded = True

def setup_manual_input():
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
    if pygetwindow.getActiveWindow().title != "Flight Rising - Brave":
        return

    if not pyautogui.locateOnScreen(os.path.join(dirname, "images", "loot.png"), region=G.LOOT_TITLE_BOUNDS, confidence=0.97):
        return

    increment_widget_value(total_battles_label)

    loot_image = ImageGrab.grab(bbox=G.LOOT_ITEM_BOUNDS)
    loot_image.save(os.path.join(dirname, "recent_loot.png"))

    coli_screen_img = ImageGrab.grab(bbox=G.COLI_SCREEN_BOUNDS)
    coli_screen_img.save(os.path.join(dirname, "recent_coli_screen.png"))

    gui_loot_image = ImageTk.PhotoImage(loot_image)
    recent_loot_label.config(image=gui_loot_image)
    recent_loot_label.image = gui_loot_image

    pyautogui.moveTo(1200, 800)
    pyautogui.click()

    search_loot(loot_image)

def search_loot(loot_image):
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
    name = name.replace("~~", ":")

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

    global has_uploaded
    if has_uploaded is None:
        has_uploaded = False

def increment_widget_value(widget):
    widget_str = widget.cget("text")
    widget_num = int(widget_str[widget_str.index(": ")+2:]) + 1
    widget_str = widget_str[:widget_str.index(": ")+2]
    widget.config(text=f"{widget_str}{widget_num}")
   
def check_active_window(button):
    if pygetwindow.getActiveWindow().title != "Flight Rising - Brave":
        return
    increment_widget_value(button)

anti_repeat = False
def attack_and_abilities(key1, key2, key3):
    global anti_repeat
    if anti_repeat:
        return
    if pygetwindow.getActiveWindow().title != "Flight Rising - Brave":
        return
    
    anti_repeat = True
    pyautogui.press(key1)
    pyautogui.press(key2)
    pyautogui.press(key3)
    anti_repeat = False

venue_choice = StringVar()
venue_choice.set(G.DEFAULT_VENUE)
venue_selector = tkinter.OptionMenu(gui, venue_choice, *G.VENUE_NAMES)
venue_selector.pack()

bold_font = font.nametofont("TkDefaultFont")
bold_font.configure(weight="bold", size=11)

most_recent_loot_entry = tkinter.Entry(gui, font=bold_font)
raw_paste_box = tkinter.Entry(gui)

loot_boxes = {
    "Apparel": tkinter.Text(gui, width=22, height=11),
    "Battle Stones": tkinter.Text(gui, width=22, height=11),
    "Boss Familiars": tkinter.Text(gui, width=22, height=11),
    "Genes": tkinter.Text(gui, width=22, height=11),
    "Miscellaneous": tkinter.Text(gui, width=22, height=11),
    "NonBoss Familiars": tkinter.Text(gui, width=22, height=11)
}

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
manual_input_radios = (
    tkinter.Radiobutton(gui, text="Apparel", variable=input_var, value="Apparel"),
    tkinter.Radiobutton(gui, text="Battle Stones", variable=input_var, value="Battle Stones"),
    tkinter.Radiobutton(gui, text="Boss Familiars", variable=input_var, value="Boss Familiars"),
    tkinter.Radiobutton(gui, text="Genes", variable=input_var, value="Genes"),
    tkinter.Radiobutton(gui, text="Miscellaneous", variable=input_var, value="Miscellaneous"),
    tkinter.Radiobutton(gui, text="NonBoss Familiars", variable=input_var, value="NonBoss Familiars")
)

total_battles_label = tkinter.Label(gui, text="Battles: 0")

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