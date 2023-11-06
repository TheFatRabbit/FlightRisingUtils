import json
import pyautogui
import pygetwindow
import tkinter
from PIL import Image, ImageDraw, ImageGrab
import keyboard
import os

dirname = os.path.dirname(__file__)

config = json.load(open("config.json"))

# delete this once confirm this works
# whole screen = (700, 400), (1400, 1000) = 700x600
# a location = (930, 540) LOCAL (230, 140)
# a diagonal location = (960, 522) LOCAL (260, 122)
# a vertical location = (930, 574) LOCAL (230, 174)
# b location = (1170, 540) LOCAL (470, 140)

screen_width = config["screen_bbox"][2] - config["screen_bbox"][0]
screen_height = config["screen_bbox"][3] - config["screen_bbox"][1]

top_left_point = (23/70 * screen_width + config["screen_bbox"][0], 7/30 * screen_height + config["screen_bbox"][1])
top_left_point_diagonal = (13/35 * screen_width + config["screen_bbox"][0], 61/300 * screen_height + config["screen_bbox"][1])
top_left_point_vertical = (23/70 * screen_width + config["screen_bbox"][0], 29/100 * screen_height + config["screen_bbox"][1])
top_right_point = (47/70 * screen_width + config["screen_bbox"][0], 7/30 * screen_height + config["screen_bbox"][1])

# print(f"{top_left_point}\n{top_left_point_diagonal}\n{top_left_point_vertical}\n{top_right}")

pixel_width = (top_right_point[0] - top_left_point[0]) / 4
pixel_height = (top_left_point_vertical[1] - top_left_point[1]) + 2 * (top_left_point[1] - top_left_point_diagonal[1])
x_offset = top_left_point[0] - top_left_point_diagonal[0]
y_offset = top_left_point[1] - top_left_point_diagonal[1]

top_left_pixel = (top_left_point[0] + pixel_width/2, top_left_point_diagonal[1] + pixel_height/2)

board_bounds = [
    [None] * 4,
    [None] * 5,
    [None] * 6,
    [None] * 7,
    [None] * 6,
    [None] * 5,
    [None] * 4
]

for i, row in enumerate(board_bounds):
    for j, pixel in enumerate(board_bounds[i]):
        modified_x_offset = (-abs(i-3)+3) * x_offset + j * pixel_width
        modified_y_offset = i*y_offset + i*(pixel_height/2)
        center_x = top_left_pixel[0] + modified_x_offset
        center_y = top_left_pixel[1] + modified_y_offset
        board_bounds[i][j] = (int(center_x - (pixel_width/2)), int(center_y - (pixel_height/2)), int(center_x + (pixel_width/2)), int(center_y + (pixel_height/2)))

# board_strings = [
#     [None] * 4,
#     [None] * 5,
#     [None] * 6,
#     [None] * 7,
#     [None] * 6,
#     [None] * 5,
#     [None] * 4
# ]

board_strings = [
    ["X"] * 4,
    ["X"] * 5,
    ["X"] * 6,
    ["X"] * 7,
    ["X"] * 6,
    ["X"] * 5,
    ["X"] * 4
]

# img = ImageGrab.grab(board_bounds[1][0])
# img.show()
# print(Image.open(os.path.join(dirname, "images", "glimmer.png")).size)

for i, row in enumerate(board_bounds):
    for j, pixel in enumerate(board_bounds[i]):
        if pyautogui.locate(os.path.join(dirname, "glimmer.png"), ImageGrab.grab(board_bounds[i][j]), confidence=0.9):
            board_strings[i][j] = "X"
        elif pyautogui.locate(os.path.join(dirname, "gloom.png"), ImageGrab.grab(board_bounds[i][j]), confidence=0.9):
            board_strings[i][j] = "O"
        else:
            print(f"Failed to find pixel ({i}, {i})")

def print_formatted_board():
    for i, row in enumerate(board_strings):
        print(" " * abs(i-3), end="")
        for cell in row:
            print(f"{cell} ", end="")
        print()

click_list = [
    [False] * 4,
    [False] * 5,
    [False] * 6,
    [False] * 7,
    [False] * 6,
    [False] * 5,
    [False] * 4
]

print_formatted_board()

def toggle_string(i, j):
    if i < 0 or j < 0:
        raise IndexError("list index out of range")

    global board_strings
    board_strings[i][j] = "X" if board_strings[i][j] == "O" else "O"

def simulate_click(i, j):
    print(f"Click: ({i}, {j})")

    global click_list
    click_list[i][j] = not click_list[i][j]
    
    toggle_string(i, j)

    try:
        toggle_string(i, j+1)
    except IndexError:
        pass
    try:
        toggle_string(i+1, j+1)
    except IndexError:
        pass
    try:
        toggle_string(i+1, j)
    except IndexError:
        pass
    try:
        toggle_string(i, j-1)
    except IndexError:
        pass
    try:
        toggle_string(i-1, j-1)
    except IndexError:
        pass
    try:
        toggle_string(i-1, j)
    except IndexError:
        pass

def propagate_4():
    pass

def propagate_5():
    pass

def propagate_6():
    pass

for i, row in enumerate(board_strings):
    if i < 3:
        for j, pixel in enumerate(row):
            if pixel == "X":
                simulate_click(i+1, j+1)
                print_formatted_board()
    # check 4
    # click through r4
    # check 5
    # click through r5
    # check 6
    # click through r6

print("--------------")
print_formatted_board()

# def solve_board():
#     gui = tkinter.Tk()
#     gui.geometry # set geo based on notebook calcs
#     gui.attributes("-topmost", True)
#     gui.title("G&G Hard Solver by TheFatRabbit")

#     board_image = ImageGrab.grab(bbox=config["screen_bbox"])
#     board_image.show()

# keyboard.add_hotkey(config["keybind"], solve_board)

# keyboard.wait()



# OVERLAY
#screen_width, screen_height = pyautogui.size()

#window = pygetwindow.getWindowsWithTitle("Fairgrounds | Glimmer & Gloom Flight Rising - Brave")

#if not window:
#    window = pygetwindow.getActiveWindow()
#else:
#    window = window[0]

#window.resizeTo(screen_width, screen_height)

#window.moveTo(0, 0)

#color = "white"
#pyautogui.moveTo(board[0][0][0], board[0][0][1])
#pyautogui.dragTo(board[0][0][2], board[0][0][3], duration=.5, button="left")

#overlay = Image.new('RGBA', (screen_width, screen_height), (0, 0, 0, 0))

#draw = ImageDraw.Draw(overlay)

#box_color = (255, 255, 255, 255)
#box_position = board[0][0]
#draw.rectangle(box_position, outline=box_color)

#overlay.show()

#print(board_locations)