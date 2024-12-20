import tkinter

categories = ("Familiars", "Apparel", "Genes", "Scenes", "Vistas", "Eggs", "Scrolls")

gui = tkinter.Tk()
gui.title("Strange Chest Tracker")
gui.geometry("300x300")
gui.attributes("-topmost", True)

def increment_widget_value(widget):
    widget_str = widget.cget("text")
    widget_num = int(widget_str[widget_str.index(": ")+2:]) + 1
    widget_str = widget_str[:widget_str.index(": ")+2]
    widget.config(text=f"{widget_str}{widget_num}")

def print_info():
    s = ""
    loots = [b.cget("text") for b in increment_btns]
    for loot in loots:
        s += f"{loot[loot.index(': ')+2:]}\n"
    print(s)

increment_btns = [tkinter.Button(gui, text=f"{n}: 0", command=lambda i=i: increment_widget_value(increment_btns[i])) for i, n in enumerate(categories)]
for b in increment_btns: b.pack()

print_btn = tkinter.Button(gui, text="Print Info", command=print_info)
print_btn.pack()

gui.mainloop()