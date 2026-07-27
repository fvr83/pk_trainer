import tkinter as tk
from math import ceil, sin, cos, pi
from pathlib import Path
import json
import random
from PIL import Image, ImageDraw, ImageFont, ImageTk
from z_new_support import *



def get_possible_villains(selected=None):
    if hero_position_var.get() == "":
        villains = ["None"]
    else:
        hero_idx = positions.index(hero_position_var.get())
        positions_before = positions[:hero_idx]
        positions_after = positions[hero_idx + 1:]
        spot_action = spot_action_text_var.get()
        if spot_action == "rfi":
            villains = ["None"]
        elif spot_action in ["vs_rfi", "vs_open_shove", "vs_limp"]:
            villains = positions_before
        elif spot_action in ["vs_3bet_nai_low", "vs_3bet_ai", "vs_raise_ai", "vs_raise_nai_low"]:
            villains = positions_after
        else:
            villains = ["None"]
    menu = villain_position_dropdown["menu"]
    menu.delete(0, "end")
    for villain in villains:
        menu.add_command(label=villain, command=tk._setit(villain_position_var, villain))
    # villain_position_var.set(villains[0])


def get_combo_family(combo):
    if len(combo) > 3:

        return 0
    if combo[0] == combo[1]:

        return list(f"{combo[0]}{s_1}{combo[1]}{s_2}" for i, s_1 in enumerate(suits) for j, s_2 in enumerate(suits) if i > j)
    elif combo[2] == "o":

        return list(f"{combo[0]}{s_1}{combo[1]}{s_2}" for i, s_1 in enumerate(suits) for j, s_2 in enumerate(suits) if i != j)
    elif combo[2] == "s":

        return list(f"{combo[0]}{s}{combo[1]}{s}" for s in suits)


def update_current_result_frame(line_1: str, line_2: str):
    cr_canvas.delete("all")
    cr_canvas.create_text(current_progress_line1_x, current_progress_line1_y + 1, font=("Arial", 12, "bold"), text=line_1, fill="white")
    cr_canvas.create_text(current_progress_line2_x, current_progress_line2_y, font=("Arial", 12, "bold"), text=line_2, fill="white")


def draw_table(canvas: tk. Canvas):
    canvas.delete("all")
    canvas.create_oval(oval_center_x - oval_radius_x, oval_center_y - oval_radius_y, oval_center_x + oval_radius_x, oval_center_y + oval_radius_y, fill=table_color, outline="black")
    table_line1 = "MTT ChipEV | 200 bb | UTG1 vs"
    table_line2 = "UTG R2.3 | UTG1 R8.23 | BTN R20.84 | SB C | BB C | UTG R60.88"
    pot_odds = "Pot odds: 43.5%"
    rng = "100"
    canvas.create_text(table_line1_x, table_line1_y, font=("Arial", 9, "bold"), text=table_line1)
    canvas.create_text(table_line2_x, table_line2_y, font=("Arial", 9), text=table_line2)
    canvas.create_text(pot_odds_x, pot_odds_y, font=("Arial", 11, "bold"), text=pot_odds)
    canvas.create_text(510, 530, font=("Arial", 40), text="🎲")
    canvas.create_text(562, 533, font=("Arial", 30), text=rng)
    seats: list[Seat] = []
    for i in range(8):
        seats.append(Seat(i, canvas))
        seats[i].draw_seat()


def update_last_combo_result_frame(line_1: str, line_2: str, line1_color: str):
    lr_canvas.delete("all")
    line1_text = lr_canvas.create_text(last_result_line1_x, last_result_line1_y + 1, font=("Arial", 9, "bold"), text=line_1, fill="white")
    x1, y1, x2, y2 = lr_canvas.bbox(line1_text)
    line1_rect = lr_canvas.create_rectangle(x1 - 2, y1 - 2, x2 + 2, y2 + 2, fill=line1_color, outline="")
    lr_canvas.tag_raise(line1_text, line1_rect)
    lr_canvas.create_text(last_result_line2_x, last_result_line2_y, font=("Arial", 12, "bold"), text=line_2, fill="white")



class Seat():
    def __init__(self, index, canvas: tk.Canvas):
        self.canvas = canvas
        self.index = index
        self.position = "UTG1"
        self.stack = "99999"
        self.bet = "12345678"
        self.action = ""

        if self.bet == "":
            self.bet = 0.5 if self.position == "SB" else 1 if self.position == "BB" else self.bet

        self.cards_width = 152 if index == 0 else 64
        self.cards_height = int((self.cards_width / 2) * 1.36)
        self.circle_radius = 35
        self.btn_radius = 8

        self.angle = ((2 * pi) * (self.index / 8)) + (pi / 2)
        
        self.btn_center_x = (oval_center_x + ((oval_radius_x - self.circle_radius) * cos(self.angle)))
        self.btn_center_y = (oval_center_y + ((oval_radius_y - self.circle_radius) * sin(self.angle)))

        self.bet_center_x = (oval_center_x + ((oval_radius_x - self.circle_radius - 34) * cos(self.angle)))
        self.bet_center_y = (oval_center_y + ((oval_radius_y - self.circle_radius - 30) * sin(self.angle)))
        
        self.circle_center_x = oval_center_x + (oval_radius_x * cos(self.angle))
        self.circle_center_y = oval_center_y + (oval_radius_y * sin(self.angle))

        self.cards_center_x = (oval_center_x + ((oval_radius_x + self.circle_radius + 30) * cos(self.angle)))
        self.cards_center_y = (oval_center_y + ((oval_radius_y + self.circle_radius + 30) * sin(self.angle)))
        self.card_x_0 = self.cards_center_x - (self.cards_width // 2)
        self.card_y_0 = self.cards_center_y - (self.cards_height // 2)
        self.card_x_1 = self.cards_center_x + (self.cards_width // 2)
        self.card_y_1 = self.cards_center_y + (self.cards_height // 2)

        self.position_center_x = self.circle_center_x
        self.position_center_y = self.circle_center_y - int(self.circle_radius / 4)

        self.stack_center_x = self.circle_center_x
        self.stack_center_y = self.circle_center_y + int(self.circle_radius / 4)



    def draw_hero_cards(self, combo):
        gap = 2
        total_width = self.cards_width
        card_width = (total_width - gap) // 2
        card_height = int(card_width * 1.36)
        hands_avaliable = get_combo_family(combo)
        hand_str = random.choice(hands_avaliable)
        x0 = self.cards_center_x - total_width / 2
        y0 = (self.cards_center_y - card_height / 2) + 2
        cards = [hand_str[:2], hand_str[2:]]
        for i, (rank, suit) in enumerate(cards):
            left = x0 + i * (card_width + gap)
            top = y0
            right = left + card_width
            bottom = top + card_height
            self.canvas.create_rectangle(left, top, right, bottom, fill="white", outline="black", width=1)
            color = suit_color[suit]
            self.canvas.create_text(left + 2, top - 10, anchor="nw", text=suit_dict[suit], font=("Arial", 30, "bold"), fill=color)
            value_x_offset = 8
            value_y_offset = 6 if rank != "Q" else 3
            self.canvas.create_text(((left + right) / 2) + value_x_offset, ((top + bottom) / 2) + value_y_offset, text=rank, font=("Impact", 70), fill=color)


    def draw_hidden_cards(self):
        gap = 2
        total_width = self.cards_width
        card_width = (total_width - gap) // 2
        card_height = int(card_width * 1.36)
        x0 = self.cards_center_x - total_width / 2
        y0 = self.cards_center_y - card_height / 2
        for i in range(2):
            left = x0 + i * (card_width + gap)
            top = y0
            right = left + card_width
            bottom = top + card_height
            self.canvas.create_rectangle(left, top, right, bottom, fill="white", outline="black", width=1) # White border
            margin = max(2, card_width // 12) # card blue area
            self.canvas.create_rectangle(left + margin + 1, top + margin + 1, right - margin + 1, bottom - margin + 1, fill="#3568D4", outline="")
            step = max(4, card_width // 8) # simple draw on back
            x = left + margin # vertical lines
            while x <= right - margin:
                self.canvas.create_line(x, top + margin, x, bottom - margin, fill="#7FAEFF" )
                x += step
            y = top + margin # horizontal lines
            while y <= bottom - margin:
                self.canvas.create_line(left + margin, y, right - margin, y, fill="#7FAEFF")
                y += step


    def draw_seat(self):
        self.canvas.create_oval(
            self.circle_center_x - self.circle_radius,
            self.circle_center_y - self.circle_radius,
            self.circle_center_x + self.circle_radius,
            self.circle_center_y + self.circle_radius,
            fill=position_color,
            outline="black"
        )
        
        if self.position == "UTG1":
            self.canvas.create_oval(self.btn_center_x - self.btn_radius, self.btn_center_y - self.btn_radius, self.btn_center_x + self.btn_radius, self.btn_center_y + self.btn_radius, fil=btn_color)
            self.canvas.create_text(self.btn_center_x, self.btn_center_y, font=("Arial", 10, "bold"), text="D")
        self.canvas.create_text(self.position_center_x, self.position_center_y, font=("Arial", 18, "bold"), text=self.position)
        self.canvas.create_text(self.stack_center_x, self.stack_center_y, font=("Arial", 10, "bold"), text=self.stack)
        self.canvas.create_text(self.bet_center_x, self.bet_center_y, font=("Arial", 9, "bold"), text=self.bet)
        if self.index != 0:
            self.draw_hidden_cards()
        else:
            self.draw_hero_cards("KQo")
        update_current_result_frame("✅12923(100%)  ⚠️12355(100%)  ❎12456(100%)  👍18326(100%)  🔥2 | 🏆5", "HANDS: 999 | Acc: 99% | EV loss: 12354.5/987545261")
        update_last_combo_result_frame("🎯Allin 200 ✅Raise 2.3  | Acc/EVloss: 0.4424 / -14.35 | 👉 WRONG ANSWER 👈 | MTT ChipEV 200 | UTG1 vs_rfi UTG", "KQs | RNG: 59    Allin: [0, -0.2] | Raise 2.3: [100, 2.1] | Fold: [0, 0]", "red")



root = tk.Tk()
root.title("Preflop")
root_width, root_height = 1366, 707
root.geometry(f"{root_width}x{root_height}+0+0")
root.resizable(False, False)

main_frame_width, main_frame_height = 800, 707
table_frame_width = current_progress_frame_width = last_result_frame_width = actions_frame_width = main_frame_width
current_progress_frame_height = 36
table_frame_height = 560
actions_frame_height = 75
last_result_frame_height = 36
options_frame_width, options_frame_height = 241, root_height
charts_frame_width, charts_frame_height = 325, root_height

oval_center_x = (table_frame_width // 2) - 1
oval_center_y = table_frame_height // 2 - 14
oval_radius_x = 300
oval_radius_y = 175

table_line1_x = oval_center_x
table_line1_y = oval_center_y - 11
table_line2_x = oval_center_x
table_line2_y = oval_center_y + 11
pot_odds_x = oval_center_x
pot_odds_y = oval_center_y + 30

current_progress_line1_x = current_progress_frame_width // 2
current_progress_line1_y = (current_progress_frame_height // 5) + 1
current_progress_line2_x = current_progress_frame_width // 2
current_progress_line2_y = current_progress_frame_height - 7

last_result_line1_x = last_result_frame_width // 2
last_result_line1_y = (last_result_frame_height // 5) + 1
last_result_line2_x = last_result_frame_width // 2
last_result_line2_y = last_result_frame_height - 8

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

main_frame = tk.Frame(root, width=main_frame_width, height=main_frame_height, bg=bgd_color)
main_frame.pack(side="left", fill="both")

current_progress_frame = tk.Frame(main_frame, width=current_progress_frame_width, height=current_progress_frame_height, bg="red")
current_progress_frame.pack(anchor="n", fill="both")
cr_canvas = tk.Canvas(current_progress_frame, width=current_progress_frame_width, height=current_progress_frame_height, highlightthickness=0, bd=0, bg=bgd_color)
cr_canvas.pack()

table_frame = tk.Frame(main_frame, width=table_frame_width, height=table_frame_height, bg=bgd_color)
table_frame.pack(anchor="n", fill="both")
table_canvas = tk.Canvas(table_frame, width=table_frame_width, height=table_frame_height, highlightthickness=0, bd=0, background=bgd_color)
table_canvas.pack()

actions_frame = tk.Frame(main_frame, width=actions_frame_width, height=actions_frame_height, bg=bgd_color)
actions_frame.pack(anchor="n", fill="both", expand=True)
btns_frame = tk.Frame(actions_frame, width=10, height=10, bg=bgd_color)
btns_frame.place(relx=0.5, rely=0.5, anchor="center")

btn = tk.Button(btns_frame,bd=3, relief="raised", text=f"1: Raise 2.3", font=("Arial", 14, "bold"), padx=0)
btn.grid(row=0, column=0, padx=3)

last_result_frame = tk.Frame(main_frame, width=last_result_frame_width, height=last_result_frame_height, bg="red")
last_result_frame.pack(side="bottom", fill="both")
lr_canvas = tk.Canvas(last_result_frame, width=last_result_frame_width, height=last_result_frame_height, highlightthickness=0, bd=0, bg=bgd_color)
lr_canvas.pack()

options_frame = tk.Frame(root, width=options_frame_width, height=options_frame_height, bg=btn_color)
options_frame.pack(side="left")
options_frame.pack_propagate(False)

dropdowns_frame = tk.Frame(options_frame, width=options_frame_width, bg=btn_color)
dropdowns_frame.pack(fill="both", expand=True)
depth_dropdown = tk.OptionMenu(dropdowns_frame, depth_var, *depths)
depth_dropdown.grid(row=0, column=0)
hero_position_dropdown = tk.OptionMenu(root, hero_position_var, *positions, command=get_possible_villains)
hero_position_dropdown.place(x=900, y=32)

charts_frame = tk.Frame(root, width=charts_frame_width, height=charts_frame_height, bg=table_color)
charts_frame.pack(side="left")

draw_table(table_canvas)

root.mainloop()
