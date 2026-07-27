import tkinter as tk
from math import ceil, sin, cos, pi
from pathlib import Path
import json
import random
from PIL import Image, ImageDraw, ImageFont, ImageTk



def draw_hidden_cards(canvas, x0, y0, cards_width):

    x0 = int(x0)
    y0 = int(y0)

    cards_height = int((cards_width / 2) * 1.36)

    gap = 2

    card_width = (cards_width - gap) // 2


    def draw_card_back(x0, y0, x1, y1,color1="#8CB4FF", color2="#3E6CC4"):
        border = max(2, int(card_width * 0.10))
        left = x0 + border
        top = y0 + border
        right = x1 - border
        bottom = y1 - border
        canvas.create_rectangle(left, top, right, bottom, fill="white", outline="#4B4848")
        size = max(4, int(card_width * 0.06))
        width = right - left + 2
        height = bottom - top + 1
        cols = width // size
        rows = height // size
        mesh_width = cols * size
        mesh_height = rows * size
        start_x = left + (width - mesh_width) // 2
        start_y = top + (height - mesh_height) // 2
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * size
                y = start_y + row * size
                if (row + col) % 2 == 0:
                    canvas.create_polygon(x, y, x + size, y, x, y + size, fill=color1, outline="")
                    canvas.create_polygon(x + size, y, x + size, y + size, x, y + size, fill=color2, outline="")
                else:
                    canvas.create_polygon(x, y, x + size, y,x + size, y + size, fill=color1, outline="")
                    canvas.create_polygon(x, y, x + size, y + size, x, y + size, fill=color2, outline="")
                    
    card1_x0 = x0
    card1_y0 = y0
    card1_x1 = x0 + card_width
    card1_y1 = y0 + cards_height
    card2_x0 = x0 + card_width + gap
    card2_y0 = y0
    card2_x1 = card2_x0 + card_width
    card2_y1 = y0 + cards_height


    # fundo atrás das cartas
    canvas.create_rectangle(
        x0, y0,
        x0 + cards_width,
        y0 + cards_height,
        fill="#515152",
        outline=""
    )
    cards_height = (cards_width * 68) // 100    # ou int((cards_width / 2) * 1.36)

    gap = 2
    half = cards_width // 2

    card1_x0 = x0
    card1_y0 = y0
    card1_x1 = x0 + half - gap // 2
    card1_y1 = y0 + cards_height

    card2_x0 = x0 + half + gap // 2
    card2_y0 = y0
    card2_x1 = x0 + cards_width
    card2_y1 = y0 + cards_height

    canvas.create_rectangle(
        x0,
        y0,
        x0 + cards_width,
        y0 + cards_height,
        fill="#515152",
        outline=""
    )

    canvas.create_rectangle(
        card1_x0, card1_y0,
        card1_x1, card1_y1,
        fill="#FFFFFF",
        outline="#4B4848"
    )

    canvas.create_rectangle(
        card2_x0, card2_y0,
        card2_x1, card2_y1,
        fill="#FFFFFF",
        outline="#4B4848"
    )

    draw_card_back(card1_x0, card1_y0, card1_x1, card1_y1)
    draw_card_back(card2_x0, card2_y0, card2_x1, card2_y1)


def draw_table():
    global seats
    try:
        canvas.destroy()
    except:
        pass
    canvas = tk.Canvas(main_frame, width=main_frame_width, height=main_frame_height, background=bgd_color)
    canvas.pack()
    oval_center_x = (main_frame_width // 2) + 2
    oval_center_y = main_frame_height // 2
    oval_radius_x = 300
    oval_radius_y = 175

    canvas.create_oval(
        oval_center_x - oval_radius_x,
        oval_center_y - oval_radius_y,
        oval_center_x + oval_radius_x,
        oval_center_y + oval_radius_y,
        fill=table_color,
        outline="black"
    )

    for i in range(8):
        seats.append(Seat(i, canvas, oval_center_x, oval_center_y, oval_radius_x, oval_radius_y))
        seats[i].draw_seat()



class Seat():
    def __init__(self, index, canvas, oval_center_x, oval_center_y, oval_radius_x, oval_radius_y):
        self.canvas = canvas
        self.index = index
        self.position = ""
        self.stack = ""
        self.bet = ""
        self.action = ""

        self.angle = ((2 * pi) * (self.index / 8)) + (pi / 2)
        self.circle_center_x = oval_center_x + (oval_radius_x * cos(self.angle))
        self.circle_center_y = oval_center_y + (oval_radius_y * sin(self.angle))
        self.circle_radius = 35
        self.btn_radius = 7
        self.cards_width = 96 if index == 0 else 64
        self.cards_height = int((self.cards_width / 2) * 1.36)

        self.circle_center_x = oval_center_x + (oval_radius_x * cos(self.angle))
        self.circle_center_y = oval_center_y + (oval_radius_y * sin(self.angle))

        self.btn_center_x = (oval_center_x + ((oval_radius_x - self.circle_radius) * cos(self.angle)))
        self.btn_center_y = (oval_center_y + ((oval_radius_y - self.circle_radius) * sin(self.angle)))

        self.cards_center_x = (oval_center_x + ((oval_radius_x + self.circle_radius + 30) * cos(self.angle)))
        self.cards_center_y = (oval_center_y + ((oval_radius_y + self.circle_radius + 30) * sin(self.angle)))
        self.card_x_0 = self.cards_center_x - (self.cards_width / 2)
        self.card_y_0 = self.cards_center_y - (self.cards_height / 2)
        self.card_x_1 = self.cards_center_x + (self.cards_width / 2)
        self.card_y_1 = self.cards_center_y + (self.cards_height / 2)

    def draw_seat(self):
        self.canvas.create_oval(
            self.circle_center_x - self.circle_radius,
            self.circle_center_y - self.circle_radius,
            self.circle_center_x + self.circle_radius,
            self.circle_center_y + self.circle_radius,
            fill="white",
            outline="black"
        )
        # self.canvas.create_rectangle((self.card_x_0, self.card_y_0, self.card_x_1, self.card_y_1), fill="white", outline="black")
        self.cards_tmp = draw_hidden_cards(self.canvas, self.card_x_0, self.card_y_0, self.cards_width)
        # self.cards = ImageTk.PhotoImage(self.cards_tmp)
        # self.canvas.create_image(self.card_x_0, self.card_y_0, anchor="nw", image=self.cards)


root = tk.Tk()
root.title("Preflop")
root_width, root_height = 1366, 707
root.geometry(f"{root_width}x{root_height}+0+0")
root.resizable(False, False)

main_frame_width, main_frame_height = 800, 707
options_frame_width, options_frame_height = 241, 707
charts_frame_width, charts_frame_height = 325, 707

bgd_color = "#515152"
table_color = "#61cc4b"
btn_color = "#F39508"
position_color = "#E9E9E9"

folder_var = tk.StringVar(root, value="json_results")
depth_var = tk.StringVar(root, value="200")
hero_position_var = tk.StringVar(root, value="UTG")
spot_action_text_var = tk.StringVar(root, value="rfi")
villain_position_var = tk.StringVar(root, value="None")
combo_pool_type_var = tk.StringVar(root, value="bd-0.01-0.7")
action_selected = tk.BooleanVar(value=False)

depths = ["200", "160", "130", "100", "80", "70", "60", "55", "50", "45", "40"]
positions = ["UTG", "UTG1", "LJ", "HJ", "CO", "BTN", "SB", "BB"]
spot_actions_text = ["rfi", "vs_rfi", "vs_open_shove", "vs_3bet_nai_low", "vs_3bet_ai", "vs_limp", "vs_raise_ai", "vs_raise_nai_low"]
combo_pool_types = ["all", "tot-75", "tot-100", "bd-0.01-0.7", "mb-0.01", "mb-0.1", "mb-0"]
possible_villains = ["None"]
seats = []

main_frame = tk.Frame(root, width=main_frame_width, height=main_frame_height, bg=bgd_color)
main_frame.pack(side="left")

options_frame = tk.Frame(root, width=options_frame_width, height=options_frame_height, bg=btn_color)
options_frame.pack(side="left")

charts_frame = tk.Frame(root, width=charts_frame_width, height=charts_frame_height, bg=table_color)
charts_frame.pack(side="left")

draw_table()

root.mainloop()