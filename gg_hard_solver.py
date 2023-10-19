import json
import pyautogui
from PIL import Image, ImageDraw
import keyboard

config = json.load(open("config.json"))

start = (config["a"][0], config["a"][1])
pix_width = (config["b"][0] - config["a"][0]) / 4
pix_height = config["ah"][1] - config["a"][1]
x_offset = config["a"][0] - config["ad"][0]
y_offset = config["a"][1] - config["ad"][1]

board_locations = (
    (
        (start[0], start[1], start[0]+pix_width, start[1]+pix_height),
        (start[0], start[1], start[0]+pix_width*2, start[1]+pix_height),
        (start[0], start[1], start[0]+pix_width*3, start[1]+pix_height),
        (start[0], start[1], start[0]+pix_width*4, start[1]+pix_height)
    ),
    (
        (start[0]+x_offset, start[1]+y_offset)
    )
)

board = [
    [None] * 4,
    [None] * 5,
    [None] * 6,
    [None] * 7,
    [None] * 6,
    [None] * 5,
    [None] * 4
]

for i, row in enumerate(board):
    for j, space in enumerate(board[i]):
        mod_x_offset = (-abs(i-3)+3) * x_offset
        mod_y_offset = i * (y_offset) + i * pix_height
        base_x = start[0] + mod_x_offset
        base_y = start[1] + mod_y_offset
        space = [base_x + j * pix_width, base_y, base_x + pix_width * (j+1), base_y + pix_height]
        board[i][j] = space
print(board[0][0])
screen_width, screen_height = pyautogui.size()

overlay = Image.new('RGBA', (screen_width, screen_height), (0, 0, 0, 0))

draw = ImageDraw.Draw(overlay)

box_color = (255, 255, 255, 255)
box_position = board[0][0]
draw.rectangle(box_position, outline=box_color)

overlay.show()

#print(board_locations)