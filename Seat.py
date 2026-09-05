import tkinter as tk
from math import pi, sin, cos
import random
from main_support import *



def get_combo_family(combo):
    if len(combo) > 3:

        return 0
    if combo[0] == combo[1]:

        return list(f"{combo[0]}{s_1}{combo[1]}{s_2}" for i, s_1 in enumerate(suits) for j, s_2 in enumerate(suits) if i > j)
    elif combo[2] == "o":

        return list(f"{combo[0]}{s_1}{combo[1]}{s_2}" for i, s_1 in enumerate(suits) for j, s_2 in enumerate(suits) if i != j)
    elif combo[2] == "s":

        return list(f"{combo[0]}{s}{combo[1]}{s}" for s in suits)
    


class Seat():
    def __init__(self, index, canvas: tk.Canvas, oval_center_x, oval_center_y, oval_radius_x, oval_radius_y, combo, positions_in_order, pot_odds_and_stacks, positions_actions):
        self.canvas = canvas
        self.hand = None
        self.index = index
        self.position = "UTG1" if not positions_in_order else positions_in_order[index]
        self.stack = pot_odds_and_stacks[1][self.position]
        self.action = ""
        if index == 0:
            try:
                self.action = next(l[2] for l in positions_actions[::-1] if l[0] == self.position and l[2] != "spot")
            except:
                self.action = "N/A"
        elif self.position == "BB":
            try:
                self.action = next(l[2] for l in positions_actions[::-1] if l[0] == self.position and l[2] != "spot")
            except:
                self.action = "N/A"
        else:
            self.action = next(l[2] for l in positions_actions[::-1] if l[0] == self.position and l[2] != "spot")
        if self.action.startswith("C"):
            self.bet = "1"
        if self.action in ["N/A", "Fold"]:
            self.bet = ""
        if self.position in ["SB", "BB"] and self.action in ["N/A", "Fold"]:
            self.bet = "0.5" if self.position == "SB" else "1"
        if "Raise" in self.action or "Allin" in self.action:
            self.bet = self.action.split(" ")[1]
        # if self.bet == "":
        #     self.bet = 0.5 if self.position == "SB" else 1 if self.position == "BB" else self.bet
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
        self.hand = hand_str
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


    def draw_hidden_cards(self, index):
        gap = 2
        total_width = self.cards_width
        card_width = (total_width - gap) // 2
        card_height = int(card_width * 1.36)
        x0 = self.cards_center_x - total_width / 2
        y0 = self.cards_center_y - card_height / 2
        if index == 4:
            y0 += 10
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


    def draw_seat(self, combo):
        self.canvas.create_oval(
            self.circle_center_x - self.circle_radius,
            self.circle_center_y - self.circle_radius,
            self.circle_center_x + self.circle_radius,
            self.circle_center_y + self.circle_radius,
            fill="#E9E9E9",
            outline="black"
        )
        
        if self.position == "BTN":
            self.canvas.create_oval(self.btn_center_x - self.btn_radius, self.btn_center_y - self.btn_radius, self.btn_center_x + self.btn_radius, self.btn_center_y + self.btn_radius, fil="#F39508")
            self.canvas.create_text(self.btn_center_x, self.btn_center_y, font=("Arial", 10, "bold"), text="D")
        self.canvas.create_text(self.position_center_x, self.position_center_y, font=("Arial", 18, "bold"), text=self.position)
        self.canvas.create_text(self.stack_center_x, self.stack_center_y, font=("Arial", 10, "bold"), text=self.stack)
        self.canvas.create_text(self.bet_center_x, self.bet_center_y, font=("Arial", 9, "bold"), text=self.bet)
        if self.index != 0 and self.action != "Fold":
            self.draw_hidden_cards(self.index)
        elif self.index == 0:
            self.draw_hero_cards(combo)
