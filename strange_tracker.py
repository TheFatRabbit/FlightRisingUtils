import tkinter

def increment_widget_value(widget):
    widget_str = widget.cget("text")
    widget_num = int(widget_str[widget_str.index(": ")+2:]) + 1
    widget_str = widget_str[:widget_str.index(": ")+2]
    widget.config(text=f"{widget_str}{widget_num}")

gui = tkinter.Tk()
gui.title("Strange Chest Tracker")
gui.geometry("300x300")
gui.attributes("-topmost", True)

fam_btn = tkinter.Button(gui, text="Familiars: 0", command=lambda: increment_widget_value(fam_btn))
apparel_btn = tkinter.Button(gui, text="Apparel: 0", command=lambda: increment_widget_value(apparel_btn))
gene_btn = tkinter.Button(gui, text="Genes: 0", command=lambda: increment_widget_value(gene_btn))
scene_btn = tkinter.Button(gui, text="Scenes: 0", command=lambda: increment_widget_value(scene_btn))
vista_btn = tkinter.Button(gui, text="Vistas: 0", command=lambda: increment_widget_value(vista_btn))
egg_btn = tkinter.Button(gui, text="Eggs: 0", command=lambda: increment_widget_value(egg_btn))
scroll_btn = tkinter.Button(gui, text="Scrolls: 0", command=lambda: increment_widget_value(scroll_btn))

fam_btn.pack()
apparel_btn.pack()
gene_btn.pack()
scene_btn.pack()
vista_btn.pack()
egg_btn.pack()
scroll_btn.pack()

gui.mainloop()