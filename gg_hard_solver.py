import json
import pyautogui
import pygetwindow
import tkinter
from PIL import Image, ImageDraw, ImageGrab
import keyboard

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
top_right = (47/70 * screen_width + config["screen_bbox"][0], 7/30 * screen_height + config["screen_bbox"][1])

top_left_pixel = (top_left_point[0], top_left_point_diagonal[1])

# print(f"{top_left_point}\n{top_left_point_diagonal}\n{top_left_point_vertical}\n{top_right}")

pix_width = (top_right[0] - top_left_point[0]) / 4
pix_height = top_left_point_vertical[1] - top_left_point[1]
x_offset = top_left_point[0] - top_left_point_diagonal[0]
y_offset = top_left_point[1] - top_left_point_diagonal[1]

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
        modified_x_offset = (-abs(i-3)+3) * x_offset
        modified_y_offset = i*y_offset + i*pix_height


# for i, row in enumerate(board_bounds):
#     for j, space in enumerate(board_bounds[i]):
#         mod_x_offset = (-abs(i-3)+3) * x_offset
#         mod_y_offset = i * (y_offset) + i * pix_height
#         base_x = top_left_point[0] + mod_x_offset
#         base_y = top_left_point[1] + mod_y_offset
#         space = [base_x + j * pix_width, base_y, base_x + pix_width * (j+1), base_y + pix_height]
#         board_bounds[i][j] = space

# board_strings = [
#     [None] * 4,
#     [None] * 5,
#     [None] * 6,
#     [None] * 7,
#     [None] * 6,
#     [None] * 5,
#     [None] * 4
# ]

def solve_board():
    gui = tkinter.Tk()
    gui.geometry # set geo based on notebook calcs
    gui.attributes("-topmost", True)
    gui.title("G&G Hard Solver by TheFatRabbit")

    board_image = ImageGrab.grab(bbox=config["screen_bbox"])
    board_image.show()

keyboard.add_hotkey(config["keybind"], solve_board)

keyboard.wait()



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