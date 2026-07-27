import tkinter as tk
from math import ceil, sin, cos, pi
from pathlib import Path
import json
import random
from PIL import Image, ImageDraw, ImageFont, ImageTk
from z_new_support import *
from Seat import Seat



def get_combo_pool(pool_format, spot_total_ev, spot_max_ev, combos_dict, combos_order, prefolded_combos):
    pool = []
    if "tot" in pool_format:
        percent = float(pool_format.split("-")[1])
        percent =  percent / 100 if (100 >= percent > 1) else percent
        goal = spot_total_ev * percent
        # print(f"{goal = }")
        accumulated = 0
        for combo in combos_order:
            if combo in prefolded_combos:

                continue
            combo_ev_max = max(v[1] for k, v in combos_dict[combo][1].items() if k != "Fold")
            if (accumulated < goal and combo_ev_max >= 0) or (accumulated == goal and combo_ev_max == 0):
                accumulated += combo_ev_max
                pool.append(combo)

        return pool
    elif "mb" in pool_format:
        percent = float(pool_format.split("-")[1])
        percent =  percent / 100 if (100 >= percent > 1) else percent
        goal = spot_max_ev * percent
        negative_goal = -goal
        # print(f"{goal = }")
        # print(f"{negative_goal = }")
        for combo in combos_order:
            if combo in prefolded_combos:

                continue
            combo_ev_max = max(v[1] for k, v in combos_dict[combo][1].items() if k != "Fold")
            if goal >= combo_ev_max >= negative_goal:
                pool.append(combo)

        return pool
    elif "bd" in pool_format:
        percent = float(pool_format.split("-")[1])
        percent =  percent / 100 if (100 >= percent > 1) else percent
        factor = float(pool_format.split("-")[2])
        factor =  factor / 100 if (100 >= factor > 1) else factor
        goal = spot_max_ev * percent
        negative_goal = -(goal * factor)
        # print(f"{goal = }")
        # print(f"{negative_goal = }")
        for combo in combos_order:
            if combo in prefolded_combos:

                continue
            combo_ev_max = max(v[1] for k, v in combos_dict[combo][1].items() if k != "Fold")
            if goal >= combo_ev_max >= negative_goal:
                pool.append(combo)

        return pool
    else:
        pool = [c for c in combos_order if c not in prefolded_combos]

        return pool


def add_solution():
    options = [
        depth_var.get(),
        hero_position_var.get(),
        spot_action_text_var.get(),
        villain_position_var.get(),
        combo_pool_type_var.get(),
        folder_var.get()
    ]

    try:
        mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict = get_data(options[0], options[1], options[2], options[3], options[5])
    except:
        print("NOT FOUND")
        return

    item = " | ".join(options)

    # Só adiciona se ainda não existir
    if item not in spots_listbox.get(0, tk.END):
        spots_listbox.insert(tk.END, item)


def delete_solution():
    selected = spots_listbox.curselection()

    if not selected:
        print("None selcted")
        return

    spots_listbox.delete(selected[0])


def draw_pool_chart(pool: set[str]):
    title_bar_height = 11

    chart_width = (cell_size * matrix_size)
    chart_height = chart_width + title_bar_height

    chart = Image.new("RGB", (chart_width + 1, chart_height + 1), "#ffffff")
    draw = ImageDraw.Draw(chart)

    title_font = ImageFont.truetype("ROBOTOCONDENSED-SEMIBOLD.ttf", size=11)
    matrix_font = ImageFont.truetype("ROBOTOCONDENSED-BLACK.ttf", size=14)
    idx_font = ImageFont.truetype("ROBOTOCONDENSED-SEMIBOLD.ttf", size=8)

    x = 0
    y = 0

    draw.rectangle((x, y, chart_width, title_bar_height), outline="#000000")
    title = f"COMBOS POOL ({len(pool)})"
    text_width, text_height = get_text_boundaries(title, title_font)
    draw.text(((chart_width - text_width) / 2, -1), text=title, font=title_font, fill="black")

    for row in range(matrix_size):
        for col in range(matrix_size):
            x_1 = (cell_size * col)
            y_1 = title_bar_height + (cell_size * row)
            x_2 = x_1 + cell_size
            y_2 = y_1 + cell_size
            combo = combos_matrix[row][col]
            combo_width, combo_height = get_text_boundaries(combo, matrix_font)
            combo_x = x_1 + ((cell_size - combo_width) // 2) + 1
            combo_y = y_1 + ((cell_size - combo_height) // 2) - 2
            if combo in pool:
                draw.rectangle((x_1, y_1, x_2, y_2), outline="#000000", fill='#8a8a2d')
            else:
                draw.rectangle((x_1, y_1, x_2, y_2), outline="#000000", fill=None)

            if "Q" in combo:
                draw.text((combo_x, combo_y + 1), combo, font=matrix_font, fill="black")
            else:
                draw.text((combo_x, combo_y), combo, font=matrix_font, fill="black")

    return chart


def get_right_action_precise_frequency(combo_info: dict):
    sorted_dict = dict(sorted(combo_info.items(), key=lambda item: item[1][0]))
    accumulated = 0
    carry = 0.0
    actions_range = {}
    last_index = len(combo_info) - 1
    for i, (action, data) in enumerate(sorted_dict.items()):
        freq = data[0]
        carry = ceil(carry)
        if carry > 0:
            carry += 1
        if i != last_index:
            actions_range[action] = [freq + accumulated, carry, int(freq)]
        else:
            actions_range[action] = [freq + accumulated, carry, 100]
        carry = freq
        accumulated += freq
    rng = random.random() * 100
    right_action = None
    for k, v in actions_range.items():
        if rng < v[0]:
            right_action = k
            break
    if not right_action:
        right_action = list(sorted_dict.keys())[-1]
    final_rng = random.randint(actions_range[right_action][1], actions_range[right_action][2])

    return right_action, final_rng


def get_answer(combo, action_choosed, right_action, rng, combo_info, spot_text):
    right_action_freq = [v[0] for k, v in combo_info.items() if k == right_action][0]
    line1 = ""
    line2 = ""
    line1 += f"🎯{action_choosed} "
    right_action_ev = [v[1] for k, v in combo_info.items() if k == right_action][0]
    action_choosed_freq = [v[0] for k, v in combo_info.items() if k == action_choosed][0]
    action_choosed_ev = [v[1] for k, v in combo_info.items() if k == action_choosed][0]
    line1 += f"✅{right_action}  "
    line2 += f"{combo} | RNG: {rng}     "
    for i, (action, data) in enumerate(combo_info.items()):
        line2 += f"{action}: {data}"
        if i < len(combo_info) - 1:
            line2 += "  |  "
    if action_choosed == right_action:
        answer_color = "green"
        answer_text_color = "white"
        line1 += f"   {spot_text}   👉 RIGHT ANSWER 👈   Acc/EVloss: (1 / 0)"
        update_last_combo_result_frame(line1, line2, answer_color, answer_text_color)
        
        return 1, 0, right_action_ev
    else:
        freq_spread = normalize_float(1 - ((right_action_freq - action_choosed_freq) / 100), 4) if right_action_freq > action_choosed_freq else normalize_float(1 - ((action_choosed_freq - right_action_freq) / 100), 4)
        ev_spread = -normalize_float(abs(action_choosed_ev) - right_action_ev) if right_action_ev > action_choosed_ev else 0
        if ev_spread == 0:
            answer_color = "yellow"
            answer_text_color = "black"
            line1 += f"   {spot_text}   👉 IMPRECISE ANSWER 👈   Acc/EVloss: ({freq_spread} / {ev_spread})"
        else:
            answer_color = "red"
            answer_text_color = "black"
            line1 += f"   {spot_text}   👉 WRONG ANSWER 👈   Acc/EVloss: ({freq_spread} / {ev_spread})"
        update_last_combo_result_frame(line1, line2, answer_color, answer_text_color)

        return freq_spread, ev_spread, right_action_ev


def play(positions_in_order, combo_pool, combos_order, mode_str, spot_string, spot_actions, mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict):
    combo = random.choice(combo_pool)
    combo_info = combos_dict[combo][1]
    right_action, rng = get_right_action_precise_frequency(combo_info)
    spot_text = mode_str + " " + spot_string
    combo_colors_info_dict, spot_actions_text_colors, combos_order, fold_combos = parse_data(mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict)
    chart = draw_proof_chart(combo_colors_info_dict, spot_actions_text_colors, combos_order, fold_combos)
    chart_tk = ImageTk.PhotoImage(chart)
    help_label.config(image=chart_tk)
    help_label.image = chart_tk
    pool_chart = draw_pool_chart(combo_pool)
    pool_chart_tk = ImageTk.PhotoImage(pool_chart)
    pool_label.config(image=pool_chart_tk)
    pool_label.image = pool_chart_tk
    # pool_frame.place(x=1038, y=368)
    draw_table(table_canvas, combo, rng, positions_in_order, pot_odds_and_stacks, positions_actions, spot_text)
    action_choosed = None
    def choose_action(i):
        nonlocal action_choosed
        action_choosed = spot_actions[i]
        action_selected.set(True)
    for widget in btns_frame.winfo_children():
        widget.destroy()
    for i, action in enumerate(spot_actions):
        btn = tk.Button(btns_frame, text=f"{i+1}: {action}", command=lambda i=i: choose_action(i), font=("Arial", 14, "bold"))
        btn.grid(row=0, column=i, padx=3)
    action_selected.set(False)
    for i in range(len(spot_actions)):
        root.bind(str(i + 1), lambda event, i=i: choose_action(i) )
    root.wait_variable(action_selected)
    freq_point, ev_point, right_action_ev = get_answer(combo, action_choosed, right_action, rng, combos_dict[combo][1], spot_text)

    return combo, freq_point, ev_point, right_action_ev


def start_trainer():
    global training, table_canvas, lr_canvas, cr_canvas
    table_canvas.delete("all")
    lr_canvas.delete("all")
    cr_canvas.delete("all")
    if spots_listbox.size() == 0:
        add_solution()
    training = True
    result_dict = {"hands_played": 0, "right_hands_count": 0, "last_right": False, "right_streak": 0, "max_streak": 0, "imprecise_hands_count": 0, "wrong_hands_count": 0}
    played_hands = {}
    right_hands = {}
    imprecise_hands = {}
    wrong_hands = {}
    total_freq_points = 0
    ev_loss = 0
    total_ev = 0
    while training:
        options = random.choice(spots_listbox.get(0, tk.END))
        opt_parts = options.split(" | ")
        options = [*opt_parts]
        mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict = get_data(options[0], options[1], options[2], options[3], options[5])
        mode_str, spot_string, spot_position, spot_actions, combos_order, prefolded_combos, spot_max_ev, spot_total_ev = parse_spot(mode_depth, positions_actions, actions_frequencies, combos_dict)
        hero_idx = positions.index(spot_position)
        positions_in_order = positions[hero_idx:] + positions[:hero_idx]
        pool = get_combo_pool(options[4], spot_total_ev, spot_max_ev, combos_dict, combos_order, prefolded_combos)
        combo, freq_point, ev_point, right_action_ev = play(positions_in_order, pool, combos_order, mode_str, spot_string, spot_actions, mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict)
        played_hands.setdefault(combo, 0)
        played_hands[combo] += 1
        total_freq_points += freq_point
        ev_loss += ev_point
        total_ev += right_action_ev
        result_dict["hands_played"] += 1
        if freq_point == 1:
            result_dict["right_hands_count"] += 1
            right_hands.setdefault(combo, 0)
            right_hands[combo] += 1
            if result_dict["last_right"]:
                result_dict["right_streak"] += 1
                result_dict["max_streak"] = result_dict["right_streak"] if result_dict["right_streak"] > result_dict["max_streak"] else result_dict["max_streak"]
            result_dict["last_right"] = True
        elif ev_point == 0:
            result_dict["imprecise_hands_count"] += 1
            imprecise_hands.setdefault(combo, 0)
            imprecise_hands[combo] += 1
            result_dict["last_right"] = False
            result_dict["right_streak"] = 0
        else:
            result_dict["wrong_hands_count"] += 1
            wrong_hands.setdefault(combo, 0)
            wrong_hands[combo] += 1
            result_dict["last_right"] = False
            result_dict["right_streak"] = 0
        accuracy = normalize_float(total_freq_points / result_dict["hands_played"])
        line = f"🟢 {normalize_float(result_dict["right_hands_count"]/result_dict["hands_played"] * 100, 2)}% ({result_dict["right_hands_count"]}) | 🟡 {normalize_float(result_dict["imprecise_hands_count"]/result_dict["hands_played"] * 100, 2)}% ({result_dict["imprecise_hands_count"]}) | 🔴 {normalize_float(result_dict["wrong_hands_count"]/result_dict["hands_played"] * 100, 2)}% ({result_dict["wrong_hands_count"]}) | 👍 {normalize_float((result_dict["right_hands_count"] + result_dict["imprecise_hands_count"])/result_dict["hands_played"] * 100, 2)}% ({result_dict["right_hands_count"] + result_dict["imprecise_hands_count"]}) | Streak: {result_dict["right_streak"]} | Best Streak: {result_dict["max_streak"]}"
        p_line1 = f"✅{normalize_float(result_dict["right_hands_count"]/result_dict["hands_played"] * 100, 2)}% ({result_dict["right_hands_count"]})  ⚠️{normalize_float(result_dict["imprecise_hands_count"]/result_dict["hands_played"] * 100, 2)}% ({result_dict["imprecise_hands_count"]})  ❎{normalize_float(result_dict["wrong_hands_count"]/result_dict["hands_played"] * 100, 2)}% ({result_dict["wrong_hands_count"]})  👍{normalize_float((result_dict["right_hands_count"] + result_dict["imprecise_hands_count"])/result_dict["hands_played"] * 100, 2)}% ({result_dict["right_hands_count"] + result_dict["imprecise_hands_count"]})  🔥{result_dict["right_streak"]}  🏆{result_dict["max_streak"]}"
        p_line2 = f"HANDS: {result_dict["hands_played"]} | ACC: {normalize_float(accuracy*100, 2)}% | EV loss: {normalize_float(ev_loss, 2)}/{normalize_float(total_ev, 2)}"
        update_current_result_frame(p_line1, p_line2)

def stop_trainer():
    global training
    training = False


def delete_all_solution():
    spots_listbox.delete(0, tk.END)


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


def draw_table(canvas: tk. Canvas, combo, rng, positions_in_order, pot_odds_and_stacks, positions_actions, spot_text):
    canvas.delete("all")
    canvas.create_oval(oval_center_x - oval_radius_x, oval_center_y - oval_radius_y, oval_center_x + oval_radius_x, oval_center_y + oval_radius_y, fill=table_color, outline="black")
    spot_text_parts = spot_text.split(" | ")
    table_line1 = " | ".join(part for part in spot_text_parts[:2])
    table_line2 = " | ".join(part for part in spot_text_parts[2:])
    pot_odds = f"Pot odds: {pot_odds_and_stacks[0]["pot_odds"]} %"
    rng = rng
    canvas.create_text(table_line1_x, table_line1_y, font=("Arial", 9, "bold"), text=table_line1)
    canvas.create_text(table_line2_x, table_line2_y, font=("Arial", 9), text=table_line2)
    canvas.create_text(pot_odds_x, pot_odds_y, font=("Arial", 11, "bold"), text=pot_odds)
    canvas.create_text(510, 530, font=("Arial", 40), text="🎲")
    canvas.create_text(562, 533, font=("Arial", 30), text=rng)
    seats: list[Seat] = []
    for i in range(8):
        seats.append(Seat(i, canvas, oval_center_x, oval_center_y, oval_radius_x, oval_radius_y, combo, positions_in_order, pot_odds_and_stacks, positions_actions))
        seats[i].draw_seat(combo)


def update_last_combo_result_frame(line_1: str, line_2: str, line1_color: str, line1_text_color:str):
    lr_canvas.delete("all")
    line1_text = lr_canvas.create_text(last_result_line1_x, last_result_line1_y + 1, font=("Arial", 9, "bold"), text=line_1, fill=line1_text_color)
    x1, y1, x2, y2 = lr_canvas.bbox(line1_text)
    line1_rect = lr_canvas.create_rectangle(x1 - 2, y1 - 2, x2 + 2, y2 + 2, fill=line1_color, outline="")
    lr_canvas.tag_raise(line1_text, line1_rect)
    lr_canvas.create_text(last_result_line2_x, last_result_line2_y, font=("Arial", 12, "bold"), text=line_2, fill="white")


help_visible = False
def toggle_help(event=None):
    global help_visible

    if help_visible:
        help_frame.place_forget()
    else:
        help_frame.place(x=0, y=2)

    help_visible = not help_visible

pool_visible = False
def toggle_pool(event=None):
    global pool_visible

    if pool_visible:
        pool_frame.place_forget()
    else:
        pool_frame.place(x=0, y=368)

    pool_visible = not pool_visible



training = False

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
pot_odds_y = oval_center_y + 45

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
depth_var = tk.StringVar(root, value="100")
hero_position_var = tk.StringVar(root, value="UTG")
spot_action_text_var = tk.StringVar(root, value="rfi")
villain_position_var = tk.StringVar(root, value="None")
combo_pool_type_var = tk.StringVar(root, value="bd-0.01-0.7")
action_selected = tk.BooleanVar(value=False)

depths = ["200", "160", "130", "100", "80", "70", "60", "55", "50", "45", "40", "25"]
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

# btn = tk.Button(btns_frame,bd=3, relief="raised", text=f"1: Raise 2.3", font=("Arial", 14, "bold"), padx=0)
# btn.grid(row=0, column=0, padx=3)

last_result_frame = tk.Frame(main_frame, width=last_result_frame_width, height=last_result_frame_height, bg="red")
last_result_frame.pack(side="bottom", fill="both")
lr_canvas = tk.Canvas(last_result_frame, width=last_result_frame_width, height=last_result_frame_height, highlightthickness=0, bd=0, bg=bgd_color)
lr_canvas.pack()

options_frame = tk.Frame(root, width=options_frame_width, height=options_frame_height, bg=bgd_color)
options_frame.pack(side="left")
options_frame.pack_propagate(False)

dropdowns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
dropdowns_frame.place(relx=0.5, rely=0.08, anchor="center")
depth_dropdown = tk.OptionMenu(dropdowns_frame, depth_var, *depths)
depth_dropdown.grid(row=0, column=0, sticky="e", padx=(0,5), pady=(0,5))
hero_position_dropdown = tk.OptionMenu(dropdowns_frame, hero_position_var, *positions, command=get_possible_villains)
hero_position_dropdown.grid(row=0, column=1, sticky="w", pady=(0,5))
spot_action_text_dropdown = tk.OptionMenu(dropdowns_frame, spot_action_text_var, *spot_actions_text, command=get_possible_villains)
spot_action_text_dropdown.grid(row=1, column=0, sticky="e", padx=(0,5))
villain_position_dropdown = tk.OptionMenu(dropdowns_frame, villain_position_var, *possible_villains)
villain_position_dropdown.grid(row=1, column=1, sticky="w")
combo_pool_type_dropdown = tk.OptionMenu(dropdowns_frame, combo_pool_type_var, *combo_pool_types)
combo_pool_type_dropdown.grid(row=2, column=0, columnspan=2, pady=(5,0))

solutions_btns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
solutions_btns_frame.place(relx=0.5, rely=0.18, anchor="center")
add_solution_buttom = tk.Button(solutions_btns_frame, text="ADD SPOT", command=add_solution)
add_solution_buttom.grid(row=3, column=0, padx=(0,5), pady=(5,0))
del_solution_buttom = tk.Button(solutions_btns_frame, text="DEL SPOT", command=delete_solution)
del_solution_buttom.grid(row=3, column=1, padx=(0,5), pady=(5,0))
del_all_buttom = tk.Button(solutions_btns_frame, text="DEL ALL", command=delete_all_solution)
del_all_buttom.grid(row=3, column=2, pady=(5,0))

spots_listbox = tk.Listbox(root, width=39, height=15)
spots_listbox.place(x=801, y=150)

start_stop_btns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
start_stop_btns_frame.place(relx=0.5, rely=0.7, anchor="center")
start_trainer_buttom = tk.Button(start_stop_btns_frame, text="START", command=start_trainer)
start_trainer_buttom.grid(row=0, column=0, padx=(0, 15))
stop_trainer_buttom = tk.Button(start_stop_btns_frame, text="STOP", command=stop_trainer)
stop_trainer_buttom.grid(row=0, column=1)

charts_frame = tk.Frame(root, width=charts_frame_width, height=charts_frame_height, bg=bgd_color)
charts_frame.pack(side="left")
help_frame = tk.Frame(charts_frame, bg="black", width=325, height=336)
help_label = tk.Label(help_frame, bd=0, bg="black")
help_label.pack()
pool_frame = tk.Frame(charts_frame, bg="black", width=325, height=336)
pool_label = tk.Label(pool_frame, bd=0)
pool_label.pack()
h_key_label = tk.Label(charts_frame, text="Type <h> to toggle help")
h_key_label.place(x=20, y=343)
p_key_label = tk.Label(charts_frame, text="Type <p> to toggle pool")
p_key_label.place(x=163, y=343)

root.bind("h", toggle_help)
root.bind("p", toggle_pool)
h_key_label.bind("<Button-1>", toggle_help)
p_key_label.bind("<Button-1>", toggle_pool)

root.mainloop()
