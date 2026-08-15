import tkinter as tk
from tkinter import ttk
from math import ceil, sin, cos, pi
from pathlib import Path
import json
import random
from PIL import Image, ImageDraw, ImageFont, ImageTk
from main_support import *
from Seat import Seat
import time



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
        status_label.config(text="NOT FOUND")
        return

    item = " | ".join(options)

    if item not in spots_listbox.get(0, tk.END):
        spots_listbox.insert(tk.END, item)
    status_label.config(text="")
    status_label.after(120, lambda: status_label.config(text="SPOT ADDED"))


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
        ev_spread = normalize_float(action_choosed_ev - right_action_ev) if right_action_ev > action_choosed_ev else 0
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


def play(complete_spot, positions_in_order, combo_pool, combos_order, mode_str, spot_string, spot_actions, mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict):
    global all_spots_result_dict
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
    action_start_time = time.time()
    root.wait_variable(action_selected)
    action_end_time = time.time()
    action_time = action_end_time - action_start_time
    freq_point, ev_point, right_action_ev = get_answer(combo, action_choosed, right_action, rng, combos_dict[combo][1], spot_text)
    all_spots_result_dict[complete_spot]["hands_played_list"].append([spot_text, combo, rng, action_choosed, right_action, freq_point, ev_point, action_time])

    return combo, freq_point, ev_point, right_action_ev


def tick_clock():
    if not paused:
        elapsed = int(time.time() - start_time - paused_time)

        d = elapsed // 86400
        h = (elapsed % 86400) // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        if clock_var.get():
            if d:
                clock_label.config(text=f"{d}d {h:02}:{m:02}:{s:02}")
            else:
                clock_label.config(text=f"{h:02}:{m:02}:{s:02}")

    if training:
        root.after(200, tick_clock)   # atualiza 5x por segundo


def start_trainer():
    global training, table_canvas, lr_canvas, cr_canvas, start_time, paused, elapsed, pause_started, paused_time, all_spots_result_dict, result_frame
    if result_frame is not None:
        result_frame.destroy()
        result_frame = None
    training = False
    paused = False
    pause_started = None
    paused_time = 0
    start_time = 0
    elapsed = 0
    start_trainer_buttom.config(text="RESTART")
    pause_trainer_buttom.config(text="PAUSE")
    table_canvas.delete("all")
    lr_canvas.delete("all")
    cr_canvas.delete("all")
    if spots_listbox.size() == 0:
        add_solution()
    status_label.after(150, lambda: status_label.config(text="TRAINING"))
    training = True
    all_spots_result_dict = {}
    result_dict = {"hands_played": 0, "total_freq_points": 0, "ev_loss": 0, "total_ev": 0, "right_hands_count": 0, "imprecise_hands_count": 0, "wrong_hands_count": 0, "accuracy": 0, 
                   "last_right": False, "right_streak": 0, "max_streak": 0, "played_hands_dict": {}, "right_hands_dict": {}, "imprecise_hands_dict": {}, "wrong_hands_dict": {}, "pool": set(), 
                   "hands_played_list": []}
    start_time = time.time()
    tick_clock()
    while training:
        try:
            chosen_options = random.choice(spots_listbox.get(0, tk.END))
        except:
            status_label.config(text="NO SPOT SELECTED")

            return
        spot_string_parts = chosen_options.split(" | ")
        complete_spot = "|".join(part for part in spot_string_parts[:-1])
        all_spots_result_dict.setdefault(complete_spot, result_dict)
        opt_parts = chosen_options.split(" | ")
        options = [*opt_parts]
        mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict = get_data(options[0], options[1], options[2], options[3], options[5])
        mode_str, spot_string, spot_position, spot_actions, combos_order, prefolded_combos, spot_max_ev, spot_total_ev = parse_spot(mode_depth, positions_actions, actions_frequencies, combos_dict)
        hero_idx = positions.index(spot_position)
        positions_in_order = positions[hero_idx:] + positions[:hero_idx]
        pool = get_combo_pool(options[4], spot_total_ev, spot_max_ev, combos_dict, combos_order, prefolded_combos)
        combo, freq_point, ev_point, right_action_ev = play(complete_spot, positions_in_order, pool, combos_order, mode_str, spot_string, spot_actions, mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict)
        for c in pool:
            all_spots_result_dict[complete_spot]["pool"].add(c)
        all_spots_result_dict[complete_spot]["played_hands_dict"].setdefault(combo, 0)
        all_spots_result_dict[complete_spot]["played_hands_dict"][combo] += 1
        all_spots_result_dict[complete_spot]["total_freq_points"] += freq_point
        all_spots_result_dict[complete_spot]["ev_loss"] += ev_point
        all_spots_result_dict[complete_spot]["total_ev"] += right_action_ev
        all_spots_result_dict[complete_spot]["hands_played"] += 1
        if freq_point == 1:
            all_spots_result_dict[complete_spot]["right_hands_count"] += 1
            all_spots_result_dict[complete_spot]["right_hands_dict"].setdefault(combo, 0)
            all_spots_result_dict[complete_spot]["right_hands_dict"][combo] += 1
            if all_spots_result_dict[complete_spot]["last_right"]:
                all_spots_result_dict[complete_spot]["right_streak"] += 1
                all_spots_result_dict[complete_spot]["max_streak"] = all_spots_result_dict[complete_spot]["right_streak"] if all_spots_result_dict[complete_spot]["right_streak"] > all_spots_result_dict[complete_spot]["max_streak"] else all_spots_result_dict[complete_spot]["max_streak"]
            all_spots_result_dict[complete_spot]["last_right"] = True
        elif ev_point == 0:
            all_spots_result_dict[complete_spot]["imprecise_hands_count"] += 1
            all_spots_result_dict[complete_spot]["imprecise_hands_dict"].setdefault(combo, 0)
            all_spots_result_dict[complete_spot]["imprecise_hands_dict"][combo] += 1
            all_spots_result_dict[complete_spot]["last_right"] = False
            all_spots_result_dict[complete_spot]["right_streak"] = 0
        else:
            all_spots_result_dict[complete_spot]["wrong_hands_count"] += 1
            all_spots_result_dict[complete_spot]["wrong_hands_dict"].setdefault(combo, 0)
            all_spots_result_dict[complete_spot]["wrong_hands_dict"][combo] += 1
            all_spots_result_dict[complete_spot]["last_right"] = False
            all_spots_result_dict[complete_spot]["right_streak"] = 0
        all_spots_result_dict[complete_spot]["accuracy"] = normalize_float(all_spots_result_dict[complete_spot]["total_freq_points"] / all_spots_result_dict[complete_spot]["hands_played"])
        p_line1 = f"✅{normalize_float(all_spots_result_dict[complete_spot]["right_hands_count"]/all_spots_result_dict[complete_spot]["hands_played"] * 100, 2)}% ({all_spots_result_dict[complete_spot]["right_hands_count"]})  ⚠️{normalize_float(all_spots_result_dict[complete_spot]["imprecise_hands_count"]/all_spots_result_dict[complete_spot]["hands_played"] * 100, 2)}% ({all_spots_result_dict[complete_spot]["imprecise_hands_count"]})  ❎{normalize_float(all_spots_result_dict[complete_spot]["wrong_hands_count"]/all_spots_result_dict[complete_spot]["hands_played"] * 100, 2)}% ({all_spots_result_dict[complete_spot]["wrong_hands_count"]})  👍{normalize_float((all_spots_result_dict[complete_spot]["right_hands_count"] + all_spots_result_dict[complete_spot]["imprecise_hands_count"])/all_spots_result_dict[complete_spot]["hands_played"] * 100, 2)}% ({all_spots_result_dict[complete_spot]["right_hands_count"] + all_spots_result_dict[complete_spot]["imprecise_hands_count"]})  🔥{all_spots_result_dict[complete_spot]["right_streak"]}  🏆{all_spots_result_dict[complete_spot]["max_streak"]}"
        if all_spots_result_dict[complete_spot]["total_ev"] > 0:
            p_line2 = f"HANDS: {all_spots_result_dict[complete_spot]["hands_played"]} | Acc: {normalize_float(all_spots_result_dict[complete_spot]["accuracy"]*100, 2)}% | EV loss: {normalize_float(all_spots_result_dict[complete_spot]["ev_loss"], 2)}/{normalize_float(all_spots_result_dict[complete_spot]["total_ev"], 2)} ({normalize_float(all_spots_result_dict[complete_spot]["ev_loss"]/all_spots_result_dict[complete_spot]["total_ev"]*100)}%)"
        else:
            p_line2 = f"HANDS: {all_spots_result_dict[complete_spot]["hands_played"]} | Acc: {normalize_float(all_spots_result_dict[complete_spot]["accuracy"]*100, 2)}% | EV loss: {normalize_float(all_spots_result_dict[complete_spot]["ev_loss"], 2)}/{normalize_float(all_spots_result_dict[complete_spot]["total_ev"], 2)}"
        update_current_result_frame(p_line1, p_line2)


# def start_trainer():
#     global training, table_canvas, lr_canvas, cr_canvas, start_time, paused, elapsed, pause_started, paused_time
#     training = False
#     paused = False
#     pause_started = None
#     paused_time = 0
#     start_time = 0
#     elapsed = 0
#     start_trainer_buttom.config(text="RESTART")
#     pause_trainer_buttom.config(text="PAUSE")
#     table_canvas.delete("all")
#     lr_canvas.delete("all")
#     cr_canvas.delete("all")
#     if spots_listbox.size() == 0:
#         add_solution()
#     status_label.after(150, lambda: status_label.config(text="TRAINING"))
#     # spots_itens = spots_listbox.get(0, tk.END)
#     # for spot_string in spots_itens:
#         # print(spot_string)
#         # spot_string_parts = spot_string.split(" | ")
#         # complete_spot = "_".join(part for part in spot_string_parts[:-1])
#         # print(complete_spot)
#     training = True
#     result_dict = {"hands_played": 0, "right_hands_count": 0, "last_right": False, "right_streak": 0, "max_streak": 0, "imprecise_hands_count": 0, "wrong_hands_count": 0}
#     played_hands = {}
#     right_hands = {}
#     imprecise_hands = {}
#     wrong_hands = {}
#     total_freq_points = 0
#     ev_loss = 0
#     total_ev = 0
#     start_time = time.time()
#     tick_clock()
#     while training:
#         try:
#             options = random.choice(spots_listbox.get(0, tk.END))
#         except:
#             status_label.config(text="NO SPOT SELECTED")

#             return
#         opt_parts = options.split(" | ")
#         options = [*opt_parts]
#         mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict = get_data(options[0], options[1], options[2], options[3], options[5])
#         mode_str, spot_string, spot_position, spot_actions, combos_order, prefolded_combos, spot_max_ev, spot_total_ev = parse_spot(mode_depth, positions_actions, actions_frequencies, combos_dict)
#         hero_idx = positions.index(spot_position)
#         positions_in_order = positions[hero_idx:] + positions[:hero_idx]
#         pool = get_combo_pool(options[4], spot_total_ev, spot_max_ev, combos_dict, combos_order, prefolded_combos)
#         combo, freq_point, ev_point, right_action_ev = play(positions_in_order, pool, combos_order, mode_str, spot_string, spot_actions, mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict)
#         played_hands.setdefault(combo, 0)
#         played_hands[combo] += 1
#         total_freq_points += freq_point
#         ev_loss += ev_point
#         total_ev += right_action_ev
#         result_dict["hands_played"] += 1
#         if freq_point == 1:
#             result_dict["right_hands_count"] += 1
#             right_hands.setdefault(combo, 0)
#             right_hands[combo] += 1
#             if result_dict["last_right"]:
#                 result_dict["right_streak"] += 1
#                 result_dict["max_streak"] = result_dict["right_streak"] if result_dict["right_streak"] > result_dict["max_streak"] else result_dict["max_streak"]
#             result_dict["last_right"] = True
#         elif ev_point == 0:
#             result_dict["imprecise_hands_count"] += 1
#             imprecise_hands.setdefault(combo, 0)
#             imprecise_hands[combo] += 1
#             result_dict["last_right"] = False
#             result_dict["right_streak"] = 0
#         else:
#             result_dict["wrong_hands_count"] += 1
#             wrong_hands.setdefault(combo, 0)
#             wrong_hands[combo] += 1
#             result_dict["last_right"] = False
#             result_dict["right_streak"] = 0
#         accuracy = normalize_float(total_freq_points / result_dict["hands_played"])
#         p_line1 = f"✅{normalize_float(result_dict["right_hands_count"]/result_dict["hands_played"] * 100, 2)}% ({result_dict["right_hands_count"]})  ⚠️{normalize_float(result_dict["imprecise_hands_count"]/result_dict["hands_played"] * 100, 2)}% ({result_dict["imprecise_hands_count"]})  ❎{normalize_float(result_dict["wrong_hands_count"]/result_dict["hands_played"] * 100, 2)}% ({result_dict["wrong_hands_count"]})  👍{normalize_float((result_dict["right_hands_count"] + result_dict["imprecise_hands_count"])/result_dict["hands_played"] * 100, 2)}% ({result_dict["right_hands_count"] + result_dict["imprecise_hands_count"]})  🔥{result_dict["right_streak"]}  🏆{result_dict["max_streak"]}"
#         p_line2 = f"HANDS: {result_dict["hands_played"]} | ACC: {normalize_float(accuracy*100, 2)}% | EV loss: {normalize_float(ev_loss, 2)}/{normalize_float(total_ev, 2)}"
#         update_current_result_frame(p_line1, p_line2)


def pause_trainer():
    global paused, pause_started, paused_time
    if not training and not paused:
        return
    if paused:
        pause_trainer_buttom.config(text="PAUSE")
        paused = False
        paused_time += time.time() - pause_started
        status_label.config(text="TRAINING")
    else:
        paused = True
        status_label.config(text="PAUSED")
        pause_started = time.time()
        pause_trainer_buttom.config(text="CONTINUE")


def format_time(seconds):
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}s"


def normalize_float(value, decimals = 2):
    value = float(value)
    if value.is_integer():

        return int(value)
    
    if decimals is None:

        return value

    return round(value, decimals)


def parse_result_dict(all_spots_result_dict: dict):
    condensed_results = {"hands_played": 0, "total_freq_points": 0, "ev_loss": 0, "total_ev": 0, "right_hands_count": 0, "imprecise_hands_count": 0, "wrong_hands_count": 0,
                   "played_hands_dict": {}, "right_hands_dict": {}, "imprecise_hands_dict": {}, "wrong_hands_dict": {}, "pool": set(), "hands_played_list": []}
    for spot, result in all_spots_result_dict.items():
        for k, v in result.items():
            if k in ["hands_played", "total_freq_points", "ev_loss", "total_ev", "right_hands_count", "imprecise_hands_count", "wrong_hands_count"]:
                condensed_results[k] += v
            elif k in ["played_hands_dict", "right_hands_dict", "imprecise_hands_dict", "wrong_hands_dict"]:
                for combo, value in v.items():
                    condensed_results[k][combo] = (
                        condensed_results[k].get(combo, 0) + value
                    )
            elif k == "pool":
                
                condensed_results[k] |= v
            elif k == "hands_played_list":
                condensed_results[k].extend(v)
    
    hand_rank_dict = {}
    for hand_list in condensed_results["hands_played_list"]:
        _, hand, _, _, _, freq_sp, ev_sp, el_time = hand_list
        hand_rank_dict.setdefault(hand, [0, 0, 0, 0])
        hand_rank_dict[hand][0] += 1
        hand_rank_dict[hand][1] += freq_sp
        hand_rank_dict[hand][2] += ev_sp
        hand_rank_dict[hand][3] += el_time
    hand_rank_result = {}
    for hd, values in hand_rank_dict.items():
        div = values[0]
        hand_rank_result.setdefault(hd, [0, 0, 0])
        hand_rank_result[hd][0] = values[1] / div
        hand_rank_result[hd][1] = values[2] / div
        hand_rank_result[hd][2] = values[3] / div
    pool = condensed_results["pool"]
    sorted_hand_rank_result = dict(sorted(hand_rank_result.items(), key=lambda item: (item[1][0], item[1][1], -item[1][2])))
    played_hands = list(sorted_hand_rank_result.keys())
    not_played = [i for i in pool if i not in played_hands]
    np_str = ", ".join(not_played)
    np_str = f"NUMBER OF COMBOS NOT PLAYED: {len(not_played)}\n{np_str}"
    str_1 = ", ".join(list(sorted_hand_rank_result.keys()))
    str_1 = f"NUMBER OF COMBOS PLAYED: {len(sorted_hand_rank_result)}\n{str_1}\n{np_str}"

    num_hands = condensed_results["hands_played"]
    acc = f"{normalize_float(condensed_results["total_freq_points"]/condensed_results["hands_played"]*100)}%"
    try:
        total_ev = normalize_float(condensed_results["total_ev"])
        ev_loss =  normalize_float(condensed_results["ev_loss"])
        ev_loss_pc = f"{normalize_float(ev_loss/total_ev*100)}%"
        str_2 = f"HANDS PLAYED: {num_hands} | ACC: {acc} | EV loss: {ev_loss}/{total_ev} ({ev_loss_pc})"
    except:
        str_2 = f"HANDS PLAYED: {num_hands} | ACC: {acc} | EV loss: {ev_loss}/{total_ev} (0%)"

    right = condensed_results["right_hands_count"]
    imprecise = condensed_results["imprecise_hands_count"]
    wrong = condensed_results["wrong_hands_count"]
    str_3 = f"RIGHT: {right}({normalize_float(right/num_hands*100)}%) | IMPRECISE: {imprecise}({normalize_float(imprecise/num_hands*100)}%) | WRONG: {wrong}({normalize_float(wrong/num_hands*100)}%)"
    right_hands = [h for h in played_hands if h in condensed_results["right_hands_dict"]]
    imprecise_hands = [h for h in played_hands if h in condensed_results["imprecise_hands_dict"]]
    wrong_hands = [h for h in played_hands if h in condensed_results["wrong_hands_dict"]]
    str_4 = f"TOTAL COMBOS IN POOL: {len(pool)} | RIGHT COMBOS: {len(right_hands)}\nIMPRECISE HANDS: {len(imprecise_hands)}\n{', '.join(h for h in imprecise_hands)}\nWRONG HANDS: {len(wrong_hands)}\n{', '.join(h for h in wrong_hands)}"

    return str_1, str_2, str_3, str_4
    

def stop_trainer():
    global training, start_time, all_spots_result_dict, result_frame
    end_time = time.time()
    date_time_1 = time.strftime("%d/%m/%Y | %H:%M:%S", time.localtime(start_time))
    date_time_2 = time.strftime(" - %H:%M:%S", time.localtime(end_time))
    elapsed_str = format_time(end_time - start_time)
    date_str = f"{date_time_1}{date_time_2} | {elapsed_str}"
    training = False
    status_label.config(text="STOPPED")
    start_trainer_buttom.config(text="START")

    if result_frame is not None:
        result_frame.destroy()

    result_frame = tk.Frame(main_frame, bg=bgd_color)
    result_frame.place(x=0, y=0, width=main_frame_width, height=main_frame_height)
    
    title = tk.Label(
        result_frame,
        text="RESULTS",
        bg=bgd_color,
        fg="white",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=0)

    condensed_result_frame = tk.Frame(result_frame, width=main_frame_width, height=100, bg="blue")
    condensed_result_frame.pack(expand=True, fill="x")
    rf_text = tk.Text(condensed_result_frame, width=100, height=15)
    rf_text.pack()

    if not next(iter(next(iter(all_spots_result_dict.values())).values())):

        return
    str_1, str_2, str_3, str_4 = parse_result_dict(all_spots_result_dict)

    rf_text.insert(1.0, f"{date_str}\n{str_2}\n{str_3}\n{str_4}\n{str_1}")

    body = tk.Frame(result_frame, bg=bgd_color)
    body.pack(fill="both", expand=True)

    # ---------------- ESQUERDA ----------------

    listbox = tk.Listbox(body, width=35, height=25)
    listbox.pack(side="left", padx=10)

    # ---------------- DIREITA ----------------

    result_canvas = tk.Canvas(
        body,
        width=500,
        bg="#202020",
        highlightthickness=0
    )
    result_canvas.pack(side="left", fill="both", expand=True)

    spots = list(all_spots_result_dict.keys())

    for spot in spots:
        listbox.insert(tk.END, spot)

    def show_result(event):
        if not listbox.curselection():
            return

        index = listbox.curselection()[0]
        spot = spots[index]
        results = all_spots_result_dict[spot]

        result_canvas.delete("all")

        y = 20
        result_canvas.create_text(
            20, y,
            anchor="nw",
            text=spot,
            fill="white",
            font=("Arial", 16, "bold")
        )

        y += 40

        for key, value in results.items():
            result_canvas.create_text(
                20, y,
                anchor="nw",
                text=f"{key}: {value}",
                fill="white",
                font=("Consolas", 12)
            )
            y += 22

    listbox.bind("<<ListboxSelect>>", show_result)
    if spots:
        listbox.selection_set(0)
        listbox.activate(0)
        listbox.see(0)
        listbox.event_generate("<<ListboxSelect>>")


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
        elif spot_action in ["vs_3bet_nai_low", "vs_3bet_ai", "vs_raise_ai", "vs_raise_nai_low", "vs_raise_nai_low-med"]:
            villains = positions_after
        else:
            villains = ["None"]
    villain_position_dropdown["values"] = villains
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


def show_clock():
    if clock_var.get():
        clock_label.pack(side="left")
    else:
        clock_label.pack_forget()


def show_password_press(event):
    password_entry.config(show="")


def show_password_release(event):
    password_entry.config(show="*")


def show_password_leave(event):
    password_entry.config(show="*")



training = False
paused = False
pause_started = None
result_frame = None
paused_time = 0
start_time = 0
elapsed = 0
all_spots_result_dict = {}

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
options_frame_width, options_frame_height = 240, root_height
charts_frame_width, charts_frame_height = 326, root_height

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
depth_var = tk.StringVar(root, value="50")
hero_position_var = tk.StringVar(root, value="UTG")
spot_action_text_var = tk.StringVar(root, value="rfi")
villain_position_var = tk.StringVar(root, value="None")
combo_pool_type_var = tk.StringVar(root, value="bd-0.01-0.7")
combo_pool_var_1 = tk.StringVar(root, value="0")
combo_pool_var_2 = tk.StringVar(root, value="0")
action_selected = tk.BooleanVar(value=False)
clock_var = tk.BooleanVar(value=False)
pause_each_var = tk.BooleanVar(value=True)
limit_type_var = tk.StringVar(root, value="hands")
limit_value_var = tk.StringVar(root, value="inf")

depths = ["200", "160", "130", "100", "80", "70", "60", "55", "50", "45", "40", "38", "35", "32", "30", "28", "26", "25", "22", "20", "19", "17", "16", "15", "14", "13", "12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
one_to_hundred = [i for i in range(101)]
positions = ["UTG", "UTG1", "LJ", "HJ", "CO", "BTN", "SB", "BB"]
spot_actions_text = ["rfi", "vs_rfi", "vs_open_shove", "vs_3bet_nai_low", "vs_3bet_ai", "vs_limp", "vs_raise_ai", "vs_raise_nai_low", "vs_raise_nai_low-med"]
combo_pool_types = ["all", "tot-75", "tot-100", "bd-0.01-0.7", "mb-1", "mb-0.01", "mb-0.1", "mb-0"]
limits_types = ["hands", "time (s)", "all pool"]
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


last_result_frame = tk.Frame(main_frame, width=last_result_frame_width, height=last_result_frame_height, bg="red")
last_result_frame.pack(side="bottom", fill="both")
lr_canvas = tk.Canvas(last_result_frame, width=last_result_frame_width, height=last_result_frame_height, highlightthickness=0, bd=0, bg=bgd_color)
lr_canvas.pack()

options_frame = tk.Frame(root, width=options_frame_width, height=options_frame_height, bg=bgd_color)
options_frame.pack(side="left")
options_frame.pack_propagate(False)

user_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
user_frame.place(relx=0.5, rely=0.075, anchor="center")
user_label = tk.Label(user_frame, fg='white', bg=bgd_color, pady=0, text="User")
user_label.grid(row=0, column=0, columnspan=4)
user_entry = tk.Entry(user_frame, width=30, justify="center")
user_entry.grid(row=1, column=0, columnspan=4)
password_label = tk.Label(user_frame, fg='white', bg=bgd_color, pady=0, text="Password")
password_label.grid(row=2, column=0, columnspan=2, sticky='e')
show_password = tk.Label(user_frame, fg='white', bg=bgd_color, pady=0, text="👁 Show", cursor="hand2")
show_password.grid(row=2, column=1, columnspan=2, sticky='e', padx=5)
password_entry = tk.Entry(user_frame, width=30, justify="center")
password_entry.config(show="*")
password_entry.grid(row=3, column=0, columnspan=4)
login_button = tk.Button(user_frame, bd=0, pady=0, padx=0, text="LOGIN")
login_button.grid(row=4, column=0, pady=(2,0), padx=(0,1))
logout_button = tk.Button(user_frame, bd=0, pady=0, padx=0, text="LOGOUT")
logout_button.grid(row=4, column=1, pady=(2,0), padx=(0,1))
add_usr_button = tk.Button(user_frame, bd=0, pady=0, padx=0, text="ADD USR")
add_usr_button.grid(row=4, column=2, pady=(2,0), padx=(0,1))
del_usr_button = tk.Button(user_frame, bd=0, pady=0, padx=0, text="DEL USR")
del_usr_button.grid(row=4, column=3, pady=(2,0))

dropdowns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
dropdowns_frame.place(relx=0.5, rely=0.212, anchor="center")
depth_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=depth_var, values=depths, width=4, state="readonly", height=20)
depth_dropdown.grid(row=0, column=0, sticky="e", padx=(0,5), pady=0)
hero_position_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=hero_position_var, values=positions, width=5, state="readonly", height=10)
hero_position_dropdown.grid(row=0, column=1, columnspan=3, sticky="w", pady=0)
spot_action_text_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=spot_action_text_var, values=spot_actions_text, width=16, state="readonly", height=10)
spot_action_text_dropdown.grid(row=1, column=0, sticky="e", pady=2, padx=(0,5))
villain_position_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=villain_position_var, values=possible_villains, width=5, state="readonly", height=10)
villain_position_dropdown.grid(row=1, column=1, columnspan=3, sticky="w", pady=2)
combo_pool_type_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=combo_pool_type_var, values=combo_pool_types, width=10, state="readonly", height=10)
combo_pool_type_dropdown.grid(row=2, column=0, sticky="e", padx=(0,5), pady=0)
spot_action_entry_1 = ttk.Combobox(dropdowns_frame, justify="center", textvariable=combo_pool_var_1, values=one_to_hundred, width=3, state="readonly", height=20)
spot_action_entry_1.grid(row=2, column=1, sticky="e", padx=(0,2), pady=0)
spot_action_entry_2 = ttk.Combobox(dropdowns_frame, justify="center", textvariable=combo_pool_var_2, values=one_to_hundred, width=3, state="readonly", height=20)
spot_action_entry_2.grid(row=2, column=2, sticky="e", padx=0, pady=0)

edit_pool_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
edit_pool_frame.place(relx=0.5, rely=0.284, anchor="center")
edit_pool_button = tk.Button(edit_pool_frame, bd=0, pady=0, padx=0, text="EDIT POOL")
edit_pool_button.pack()

solutions_btns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
solutions_btns_frame.place(relx=0.5, rely=0.32, anchor="center")
add_solution_buttom = tk.Button(solutions_btns_frame, bd=0, pady=0, padx=5, text="ADD SPOT", command=add_solution)
add_solution_buttom.grid(row=3, column=0, padx=(0,5), pady=0)
del_solution_buttom = tk.Button(solutions_btns_frame, bd=0, pady=0, padx=5, text="DEL SPOT", command=delete_solution)
del_solution_buttom.grid(row=3, column=1, padx=(0,5), pady=0)
del_all_buttom = tk.Button(solutions_btns_frame, bd=0, pady=0, padx=5, text="DEL ALL", command=delete_all_solution)
del_all_buttom.grid(row=3, column=2, pady=0)

listbox_frame = tk.Frame(options_frame, width=options_frame_width)
listbox_frame.place(relx=0.5, rely=0.485, anchor="center")
scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")
spots_listbox = tk.Listbox(listbox_frame, width=27, height=10, yscrollcommand=scrollbar.set)
spots_listbox.pack(side="left")

limits_frame = tk.Frame(options_frame, width=options_frame_width, background=bgd_color)
limits_frame.place(relx=0.5, rely=0.79, anchor="center")
limit_label = tk.Label(limits_frame, fg='white', bg=bgd_color, pady=0, text="LIMIT:", font=("Arial", 13, "bold"))
limit_label.pack(side="left")
combo_pool_type_dropdown = ttk.Combobox(limits_frame, justify="center", textvariable=limit_type_var, values=limits_types, width=7, state="readonly", height=5)
combo_pool_type_dropdown.pack(side="left")
limit_value_entry = tk.Entry(limits_frame, textvariable=limit_value_var, width=5, justify='center')
limit_value_entry.pack(side="left")

extr_opt_frame = tk.Frame(options_frame, width=options_frame_width)
extr_opt_frame.place(relx=0.5, rely=0.83, anchor="center")
pause_each_checkbox = tk.Checkbutton(extr_opt_frame, variable=pause_each_var, bd=0, foreground="white", selectcolor="black", bg=bgd_color, text="Freeze between hands")
pause_each_checkbox.pack()

start_stop_btns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
start_stop_btns_frame.place(relx=0.51, rely=0.88, anchor="center")
start_trainer_buttom = tk.Button(start_stop_btns_frame, bd=0, pady=0, padx=5, text="START", command=start_trainer)
start_trainer_buttom.grid(row=0, column=0, padx=(0, 15))
pause_trainer_buttom = tk.Button(start_stop_btns_frame, bd=0, pady=0, padx=5, text="PAUSE", command=pause_trainer)
pause_trainer_buttom.grid(row=0, column=1, padx=(0, 15))
stop_trainer_buttom = tk.Button(start_stop_btns_frame, bd=0, pady=0, padx=5, text="STOP", command=stop_trainer)
stop_trainer_buttom.grid(row=0, column=2)

status_frame = tk.Frame(options_frame, width=options_frame_width, height=30, bg=bgd_color)
status_frame.place(relx=0.5, rely=0.93, anchor="center")
status_label = tk.Label(status_frame, bg=bgd_color, text="STOPPED", foreground="white", font=("Arial", 12, "bold"))
status_label.pack()

clock_frame = tk.Frame(options_frame, width=options_frame_width, height=25, bg=bgd_color)
clock_frame.place(relx=0.5, rely=0.98, anchor="center")
clock_frame.pack_propagate(False)
clock_check_btn = tk.Checkbutton(clock_frame, command=show_clock, variable=clock_var, text="show clock", foreground="white", selectcolor="black", bg=bgd_color)
clock_check_btn.pack(side="left")
clock_label = tk.Label(clock_frame, width=16, font=("Consolas", 12), foreground="white", bg=bgd_color)
clock_label.pack(side="left")

charts_frame = tk.Frame(root, width=charts_frame_width, height=charts_frame_height, bg=bgd_color)
charts_frame.pack(side="left")
help_frame = tk.Frame(charts_frame, bg=bgd_color, width=325, height=336)
help_label = tk.Label(help_frame, bd=0, bg=bgd_color)
help_label.pack()
pool_frame = tk.Frame(charts_frame, bg=bgd_color, width=325, height=336)
pool_label = tk.Label(pool_frame, bd=0)
pool_label.pack()
h_key_label = tk.Label(charts_frame, text="Type <h> to toggle help")
h_key_label.place(x=9, y=343)
p_key_label = tk.Label(charts_frame, text="Type <p> to toggle pool")
p_key_label.place(x=164, y=343)

root.bind("h", toggle_help)
root.bind("p", toggle_pool)
spot_action_text_dropdown.bind("<<ComboboxSelected>>", lambda event: get_possible_villains())
h_key_label.bind("<Button-1>", toggle_help)
p_key_label.bind("<Button-1>", toggle_pool)
show_password.bind("<ButtonPress-1>", show_password_press)
show_password.bind("<ButtonRelease-1>", show_password_release)
show_password.bind("<Leave>", show_password_leave)

root.mainloop()
