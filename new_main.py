import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
import re
import bcrypt
from tkinter import ttk
from PIL import ImageTk
import random
from math import ceil
from Seat import *
from new_main_support import *



# ===================================
# ------- SQL VARIABLES -------
# ===================================
database_file = "db_trainer.db"



# ===================================
# ------- SQL FUNCTIONS -------
# ===================================
def load_database():
    conn = sqlite3.connect(database_file)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                name TEXT,
                str_name TEXT,
                str_num TEXT,
                adr_ln2 TEXT,
                neighborhood TEXT,
                p_code TEXT,
                city TEXT,
                country TEXT,
                email TEXT,
                personal_id TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trainings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                hands_trained INTEGER DEFAULT 0,
                right_hands INTEGER DEFAULT 0,
                imprecise_hands INTEGER DEFAULT 0,
                wrong_hands INTEGER DEFAULT 0,
                train_accuracy REAL,
                train_ev_loss REAL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trainings_spots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                training_id INTEGER NOT NULL,
                spot TEXT,
                combos_pool TEXT,
                spot_hands_trained INTEGER DEFAULT 0,
                spot_right_hands INTEGER DEFAULT 0,
                spot_imprecise_hands INTEGER DEFAULT 0,
                spot_wrong_hands INTEGER DEFAULT 0,
                spot_train_accuracy REAL,
                spot_train_ev_loss REAL,
                FOREIGN KEY (training_id) REFERENCES trainings(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                training_id INTEGER NOT NULL,
                chip_mode TEXT,
                combo TEXT,
                hand TEXT,
                user_decision TEXT,
                correct_decision TEXT,
                evaluation TEXT,
                decision_time REAL,
                accuracy REAL,
                ev_loss REAL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
                FOREIGN KEY (training_id) REFERENCES trainings(id)
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hands_user_id
            ON hands(user_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hands_training_id
            ON hands(training_id)
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                action TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def add_user(top_level, user_name: str, password, password_conf, name, str_name, str_num, adr_ln2, neighborhood, p_code, city, country, email, personal_id):
    user_name = user_name.strip().lower()
    if not user_name or not password or not password_conf:
        messagebox.showwarning("Required fields", "Username, password and password confirmation are required.", parent=top_level)
        return
    if not 3 <= len(user_name) <= 30:
        messagebox.showwarning("Invalid username", "Username must contain between 3 and 30 characters.", parent=top_level)
        return
    if not re.fullmatch(r"[A-Za-z0-9_]+", user_name):
        messagebox.showwarning("Invalid username", "Username may contain only letters, numbers and underscores.", parent=top_level)
        return
    if len(password) < 8:
        messagebox.showwarning("Invalid password", "Password must contain at least 8 characters.", parent=top_level)
        return
    if password != password_conf:
        messagebox.showwarning("Password mismatch", "Password and password confirmation do not match.", parent=top_level)
        return
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")
    conn = sqlite3.connect(database_file)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (user_name, password_hash)
        )
        user_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO users_data (
                user_id,
                name,
                str_name,
                str_num,
                adr_ln2,
                neighborhood,
                p_code,
                city,
                country,
                email,
                personal_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                name or None,
                str_name or None,
                str_num or None,
                adr_ln2 or None,
                neighborhood or None,
                p_code or None,
                city or None,
                country or None,
                email or None,
                personal_id or None
            )
        )
        conn.commit()
        messagebox.showinfo("Success", "User created successfully.", parent=top_level)
        top_level.destroy()
    except sqlite3.IntegrityError:
        conn.rollback()
        messagebox.showwarning("Username already exists", "This username is already registered.", parent=top_level)
    except sqlite3.Error:
        conn.rollback()
        messagebox.showerror("Database error", "An error occurred while creating the user.", parent=top_level)
    finally:
        conn.close()


def delete_user(root, username):
    username = username.strip().lower()
    if not username:
        messagebox.showwarning("Required fields", "Username required.", parent=root)
        return
    password = simpledialog.askstring("Confirm deletion", "Enter your password to confirm account deletion:", show="*", parent=root)
    if password is None:
        return
    conn = sqlite3.connect(database_file)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, password
            FROM users
            WHERE username = ?
            """,
            (username,)
        )
        user = cursor.fetchone()
        if user is None:
            messagebox.showerror("Error", "User not found.", parent=root)
            return
        user_id, password_hash = user
        if not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
            messagebox.showwarning("Invalid password", "The password is incorrect.", parent=root)
            return
        cursor.execute(
            """
            DELETE FROM users
            WHERE id = ?
            """,
            (user_id,)
        )
        conn.commit()
        messagebox.showinfo("Account deleted", "Your account has been deleted.", parent=root)
    except sqlite3.Error as error:
        conn.rollback()
        messagebox.showerror("Database error", f"Could not delete the account.\n\n{error}", parent=root)
    finally:
        conn.close()


def login(root, username, password):
    global logged_in, logged_user_id
    conn = sqlite3.connect(database_file)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, password FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        if user is None:
            messagebox.showwarning("Login failed", "Invalid username or password. Don´t have an account? SIGN UP!!!", parent=root)
            return
        user_id, password_hash = user
        if not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
            messagebox.showwarning("Login failed", "Invalid username or password. Don´t have an account? SIGN UP!!!", parent=root)
            return
        logged_in = True
        logged_user_id = user_id
        logged_username = username
        login_status_label.config(text=(f"Logged in as {logged_username}"))
        password_entry.delete(0, tk.END)
        password_entry.config(state="disabled")
        user_entry.config(state="disabled")
        add_usr_button.config(state="disabled")
        del_usr_button.config(state="disabled")
    except sqlite3.Error as error:
        messagebox.showerror("Database error", f"Could not access the database.\n\n{error}", parent=root)
    finally:
        conn.close()


def logout():
    global logged_in, logged_user_id, logged_username
    logged_in = False
    logged_user_id = None
    logged_username = None
    user_entry.config(state="normal")
    user_entry.delete(0, tk.END)
    password_entry.config(state="normal")
    login_status_label.config(text="Login before start.")
    add_usr_button.config(state="normal")
    del_usr_button.config(state="normal")



# ===================================
# ------- TRAINING VARIABLES -------
# ===================================
training = False



# ===================================
# ------- TRAINING FUNCTIONS -------
# ===================================
def continue_training(event):
    training_continue.set(True)


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


def play(pool, combos_dict):
    combo = random.choice(pool)
    combo_info = combos_dict[combo][1]
    right_action, rng = get_right_action_precise_frequency(combo_info)


def start_training():
    global training
    training = True
    while training:
        treeview_items = choosen_spots_list.get_children()
        if not treeview_items:
            add_solution()
            treeview_items = choosen_spots_list.get_children()
        if not treeview_items:
            status_label.config(text="NO SPOT SELECTED")

            return
        spot_id = random.choice(treeview_items)
        choosen_spots_list.selection_set(spot_id)
        choosen_spots_list.see(spot_id)
        pool = pools[spot_id]
        spot_values = choosen_spots_list.item(spot_id, "values")
        depth, hero, spot, villain, chip_mode = spot_values
        mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict = get_data(depth, hero, spot, villain, chip_mode)
        mode_str, spot_string, spot_position, spot_actions, combos_order, prefolded_combos, spot_max_ev, spot_total_ev = parse_spot(mode_depth, positions_actions, actions_frequencies, combos_dict)
        hero_idx = positions.index(spot_position)
        positions_in_order = positions[hero_idx:] + positions[:hero_idx]
        combo, freq_point, ev_point, right_action_ev = play(positions_in_order, pool, combos_order, mode_str, spot_string, spot_actions, mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict)

        print(depth, hero, spot, villain, chip_mode)
        print(pool)
        status_label.config(text="PRESS ENTER TO CONTINUE")
        root.bind("<Return>", continue_training)
        training_continue.set(False)
        root.wait_variable(training_continue)



# ===================================
# ------- ROOT VARIABLES -------
# ===================================
logged_in = False
logged_user_id = None
logged_username = None
help_visible = True
pool_visible = True
edit_canvas = None

current_pool = []
pools = dict()

root_width, root_height = 1356, 667

main_frame_width, main_frame_height = 800, root_height
options_frame_width, options_frame_height = 232, root_height
charts_frame_width, charts_frame_height = 326, root_height

table_frame_width = current_progress_frame_width = last_result_frame_width = actions_frame_width = main_frame_width
current_progress_frame_height = 36
table_frame_height = 552
actions_frame_height = 41
last_result_frame_height = 70

oval_center_x = (table_frame_width // 2) - 1
oval_center_y = table_frame_height // 2 - 24
oval_radius_x = 300
oval_radius_y = 175

table_line1_x = oval_center_x
table_line1_y = oval_center_y - 11
table_line2_x = oval_center_x
table_line2_y = oval_center_y + 11
pot_x = oval_center_x
pot_y = oval_center_y + 45
pot_odds_x = oval_center_x
pot_odds_y = oval_center_y + 60
rng_symbol_x = oval_center_x + 115
rng_symbol_y = oval_center_y + 260
rng_value_x = oval_center_x + 180
rng_value_y = oval_center_y + 260

current_progress_line1_x = current_progress_frame_width // 2
current_progress_line1_y = (current_progress_frame_height // 5) + 1
current_progress_line2_x = current_progress_frame_width // 2
current_progress_line2_y = current_progress_frame_height - 7

last_result_line1_x = last_result_frame_width // 2
last_result_line1_y = (last_result_frame_height // 8) + 4
last_result_line2_x = last_result_frame_width // 2
last_result_line2_y = last_result_frame_height - 40

bgd_color = "#515152"
table_color = "#61cc4b"
btn_color = "#F39508"
position_color = "#E9E9E9"
stopped_color = "#f76969"
training_color = "#36ff04"
paused_color = "#eafc4b"

depths = ["200", "160", "130", "100", "80", "70", "60", "55", "50", "45", "40", "38", "35", "32", "30", "28", "26", "25", "22", "20", "19", "17", "16", "15", "14", "13", "12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
one_to_hundred = [i for i in range(101)]
positions = ["UTG", "UTG1", "LJ", "HJ", "CO", "BTN", "SB", "BB"]
spot_actions_text = ["rfi", "vs_rfi", "vs_open_shove", "vs_3bet_nai_low", "vs_3bet_ai", "vs_limp", "vs_raise_ai", "vs_raise_nai_low", "vs_raise_nai_low-med"]
combo_pool_types = ["tot", "max", "freq more than", "bd"]
limits_types = ["hands", "time (s)", "all pool"]
possible_villains = ["None"]
folder_options = ["Chip EV"]
possible_villains = ["None"]
precisions = ["precise", "simple", "any right"]
dealing_options = ['per combo', 'per hand']
freeze_options = ["never", "wrong", "imprecise/wrong", "always", "imprecise", "right/wrong", "right/imprecise", "right"]
show_results_option = ["both", "current", "last", "none"]
roles_options = ["custom", "focus"]



# ===================================
# ------- ROOT FUNCTIONS -------
# ===================================
def show_password_press(event):
    password_entry.config(show="")


def show_password_release(event):
    password_entry.config(show="*")


def show_password_leave(event):
    password_entry.config(show="*")


def add_user_toplevel():
    def su_show_password_press(event):
        su_password_entry.config(show="")
    def su_show_password_release(event):
        su_password_entry.config(show="*")
    def su_show_password_leave(event):
        su_password_entry.config(show="*")
    def su_show_password_press_2(event):
        su_password_entry_conf.config(show="")
    def su_show_password_release_2(event):
        su_password_entry_conf.config(show="*")
    def su_show_password_leave_2(event):
        su_password_entry_conf.config(show="*")
    top_level = tk.Toplevel(root)
    top_level.title("Sign up")
    top_level_width = 400
    top_level_height = 440
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    x = int(root_x + (root_width * 0.52))
    y = root_y + 20
    top_level.geometry(f"{top_level_width}x{top_level_height}+{x}+{y}")
    su_instructions_label = tk.Label(top_level, font=("Arial", 10, "bold"), text="Fields marked with * are required.")
    su_instructions_label.pack()
    su_user_name_label = tk.Label(top_level, text=("Nickname *"))
    su_user_name_label.pack()
    su_user_name_entry = tk.Entry(top_level, justify="center", width=32)
    su_user_name_entry.pack()
    su_password_label = tk.Label(top_level, text=("Password *"))
    su_password_label.pack()
    su_pass_hide_frame = tk.Frame(top_level)
    su_pass_hide_frame.pack()
    su_password_entry = tk.Entry(su_pass_hide_frame, justify="center", width=25)
    su_password_entry.config(show="*")
    su_password_entry.pack(side="left")
    su_show_password_label = tk.Label(su_pass_hide_frame, text="Show", cursor="hand2")
    su_show_password_label.pack(side="left")
    su_password_label_conf = tk.Label(top_level, text=("Confirm Password *"))
    su_password_label_conf.pack()
    su_pass_hide_frame_conf = tk.Frame(top_level)
    su_pass_hide_frame_conf.pack()
    su_password_entry_conf = tk.Entry(su_pass_hide_frame_conf, justify="center", width=25)
    su_password_entry_conf.config(show="*")
    su_password_entry_conf.pack(side="left")
    su_show_password_label_conf = tk.Label(su_pass_hide_frame_conf, text="Show", cursor="hand2")
    su_show_password_label_conf.pack(side="left")
    su_name_label = tk.Label(top_level, text=("Real name"))
    su_name_label.pack()
    su_name_entry = tk.Entry(top_level, justify="center", width=50)
    su_name_entry.pack()
    su_address_frame = tk.Frame(top_level, width=top_level_width, height=130)
    su_address_frame.pack()
    su_street_name_label = tk.Label(su_address_frame, text="Steet name")
    su_street_name_label.place(relx=0.38, rely=0)
    su_street_name_entry = tk.Entry(su_address_frame, justify="center", width=56)
    su_street_name_entry.place(x=5, y=22)
    su_street_number_label = tk.Label(su_address_frame, text="St. num.")
    su_street_number_label.place(relx=0.88, rely=0)
    su_street_number_entry = tk.Entry(su_address_frame, justify="center", width=7)
    su_street_number_entry.place(relx=0.88, y=22)
    su_adr_line2_label = tk.Label(su_address_frame, text="Address line 2")
    su_adr_line2_label.place(relx=0.1, y=44)
    su_adr_line2_entry = tk.Entry(su_address_frame, justify="center", width=24)
    su_adr_line2_entry.place(relx=0.01, y=66)
    su_neighborhood_label = tk.Label(su_address_frame, text="Neighborhood")
    su_neighborhood_label.place(relx=0.49, y=44)
    su_neighborhood_entry = tk.Entry(su_address_frame, justify="center", width=25)
    su_neighborhood_entry.place(relx=0.4, y=66)
    su_post_code_label = tk.Label(su_address_frame, text="Postal Code")
    su_post_code_label.place(relx=0.81, y=44)
    su_post_code_entry = tk.Entry(su_address_frame, justify="center", width=12)
    su_post_code_entry.place(relx=0.8, y=66)
    su_city_label = tk.Label(su_address_frame, text="City")
    su_city_label.place(relx=0.25, y=88)
    su_city_entry = tk.Entry(su_address_frame, justify="center", width=35)
    su_city_entry.place(relx=0.03, y=111)
    su_country_label = tk.Label(su_address_frame, text="Country")
    su_country_label.place(relx=0.75, y=88)
    su_country_entry = tk.Entry(su_address_frame, justify="center", width=26)
    su_country_entry.place(relx=0.58, y=111)
    su_email_label = tk.Label(top_level, text="E-mail")
    su_email_label.pack()
    su_email_entry = tk.Entry(top_level, justify="center", width=50)
    su_email_entry.pack()
    su_personal_id_label = tk.Label(top_level, text="Personal ID")
    su_personal_id_label.pack()
    su_personal_id_entry = tk.Entry(top_level, justify="center", width=16)
    su_personal_id_entry.pack()
    su_btns_frame = tk.Frame(top_level, width=top_level_width, height=25)
    su_btns_frame.pack()
    su_signup_btn = tk.Button(su_btns_frame, text="SIGN UP", command=lambda:add_user(top_level, su_user_name_entry.get(), su_password_entry.get(), su_password_entry_conf.get(), su_name_entry.get(), su_street_name_entry.get(), su_street_number_entry.get(), su_adr_line2_entry.get(), su_neighborhood_entry.get(), su_post_code_entry.get(), su_city_entry.get(), su_country_entry.get(), su_email_entry.get(), su_personal_id_entry.get()))
    su_signup_btn.pack(side="left", pady = (10, 0), padx=10)
    su_cancel_btn = tk.Button(su_btns_frame, text="CANCEL", command= top_level.destroy)
    su_cancel_btn.pack(side="left", pady = (10, 0), padx=10)
    su_show_password_label.bind("<ButtonPress-1>", su_show_password_press)
    su_show_password_label.bind("<ButtonRelease-1>", su_show_password_release)
    su_show_password_label.bind("<Leave>", su_show_password_leave)
    su_show_password_label_conf.bind("<ButtonPress-1>", su_show_password_press_2)
    su_show_password_label_conf.bind("<ButtonRelease-1>", su_show_password_release_2)
    su_show_password_label_conf.bind("<Leave>", su_show_password_leave_2)


def pool_type_from_spot(event=None):
    if spot_action_text_var.get() == "rfi":
        combo_pool_type_var.set("bd")
        combo_pool_var_1.set("1")
        combo_pool_var_2.set("70")
    else:
        combo_pool_type_var.set("freq more than")
        combo_pool_var_1.set("0")
        combo_pool_var_2.set("0")


def pool_vars_from_pool_type(event=None):
    if combo_pool_type_var.get() == "bd":
        combo_pool_var_1.set("1")
        combo_pool_var_2.set("70")
    elif combo_pool_type_var.get() == "tot":
        combo_pool_var_1.set("100")
        combo_pool_var_2.set("0")
    elif combo_pool_type_var.get() == "max":
        combo_pool_var_1.set("1")
        combo_pool_var_2.set("0")
    elif combo_pool_type_var.get() == "freq more than":
        combo_pool_var_1.set("0")
        combo_pool_var_2.set("0")


def preview_pool(depth, hero, spot, villain, folder, pool_type, pool_var_1, pool_var_2):
    global current_pool
    try:
        mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict = get_data(depth, hero, spot, villain, folder)
    except:
        status_label.config(text="SPOT NOT FOUND", fg="white")

        return
    mode_str, spot_string, spot_position, spot_actions, combos_order, prefolded_combos, spot_max_ev, spot_total_ev = parse_spot(mode_depth, positions_actions, actions_frequencies, combos_dict)
    pool = get_combo_pool(pool_type, pool_var_1, pool_var_2, spot_total_ev, spot_max_ev, combos_dict, combos_order, prefolded_combos)
    pool_chart = draw_pool_chart(pool)
    pool_chart_tk = ImageTk.PhotoImage(pool_chart)
    pool_label.config(image=pool_chart_tk)
    pool_label.image = pool_chart_tk
    combo_colors_info_dict, spot_actions_text_colors, combos_order, fold_combos_final = parse_data(mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict)
    chart = draw_proof_chart(combo_colors_info_dict, spot_actions_text_colors, combos_order, fold_combos_final)
    chart_tk = ImageTk.PhotoImage(chart)
    help_label.config(image=chart_tk)
    help_label.image = chart_tk
    current_pool = pool
    status_label.config(text="SPOT FOUND", fg="white")


def toggle_help(event=None):
    global help_visible
    if help_visible:
        help_frame.place_forget()
    else:
        help_frame.place(x=0, y=-2)
        help_frame.lift()
    help_visible = not help_visible


def toggle_pool(event=None):
    global pool_visible
    if pool_visible:
        pool_frame.place_forget()
    else:
        pool_frame.place(x=0, y=333)
    pool_visible = not pool_visible


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


def toggle_edit_pool():
    if edit_pool_button["text"] == "EDIT POOL":
        edit_pool()
    elif edit_pool_button["text"] == "END EDIT":
        end_edit()


def edit_pool():
    global current_pool, edit_canvas
    all_dropdowns = [
        folder_dropdown,
        depth_dropdown,
        hero_position_dropdown,
        spot_action_text_dropdown,
        villain_position_dropdown,
        combo_pool_type_dropdown,
        spot_action_entry_1,
        spot_action_entry_2
    ]
    for dropdown in all_dropdowns:
        dropdown.config(state="disabled")
    solutions_buttons = [
        add_solution_buttom,
        del_solution_buttom,
        del_all_buttom
    ]
    for button in solutions_buttons:
        button.config(state="disabled")
    edit_pool_button.config(text="END EDIT")
    selected_combos = set()
    for combo in current_pool:
        selected_combos.add(combo)
    current_selection = set()
    diagonal_combos = set()
    click_mode = None
    first_clicked_combo_row = None
    first_clicked_combo_col = None
    ranks = "AKQJT98765432"
    all_combos = [f"{r_1 + r_2}" if i == j else f"{r_1 + r_2 + 's'}" if i < j else f"{r_2 + r_1 + 'o'}" for j, r_2 in enumerate(ranks) for i, r_1 in enumerate(ranks)]
    combos_matrix = [[f"{r_1 + r_2}" if i == j else f"{r_1 + r_2 + 's'}" if i < j else f"{r_2 + r_1 + 'o'}" for j, r_2 in enumerate(ranks)] for i, r_1 in enumerate(ranks)]
    matrix_length = 13
    cell_size = 25
    matrix_size = (matrix_length * cell_size) + 1
    fill_color = '#8a8a2d'
    border_color = "#000000"
    canvas = tk.Canvas(charts_frame, bd=0, highlightthickness=0, width=matrix_size, height=matrix_size + 11)
    canvas.place(x=-2, y=333)
    edit_canvas = canvas
    def get_click_row_col(event: tk.Event):
        if not (0 <= event.x < matrix_size or not 0 <= event.y < matrix_size):

            return
        adjusted_y = event.y - 10
        if adjusted_y < 0:

            return
        row = adjusted_y // cell_size
        col = event.x // cell_size

        return row, col
    def check_combo_selection_triggers(event: tk.Event, col: int, row: int, clicked_combo: str, abs_row_col: int, combos: list):
        nonlocal diagonal_combos
        if event.state in [9, 265]:
            if (row == col) and row > 0:
                for i in range(row):
                    combo_to_append = f"{ranks[row - i - 1]}{ranks[row - i - 1]}"
                    if (clicked_combo not in selected_combos) and (combo_to_append not in selected_combos):
                        combos.append(combo_to_append)
                    elif (clicked_combo in selected_combos) and (combo_to_append in selected_combos):
                        combos.append(combo_to_append)
            elif (row < col) and abs_row_col > 0:
                for i in range(abs_row_col - 1):
                    combo_to_append = f"{ranks[row]}{ranks[col - i - 1]}s"
                    if (clicked_combo not in selected_combos) and (combo_to_append not in selected_combos):
                        combos.append(combo_to_append)
                    elif (clicked_combo in selected_combos) and (combo_to_append in selected_combos):
                        combos.append(combo_to_append)
            elif (row > col) and abs_row_col > 0:
                for i in range(abs_row_col - 1):
                    combo_to_append = f"{ranks[col]}{ranks[row - i - 1]}o"
                    if (clicked_combo not in selected_combos) and (combo_to_append not in selected_combos):
                        combos.append(combo_to_append)
                    elif (clicked_combo in selected_combos) and (combo_to_append in selected_combos):
                        combos.append(combo_to_append)
        elif (event.state in [12, 268]) and (row == col):
            higher_lines = abs(col - 0)
            lower_lines = abs(col - 12)
            for i in range(higher_lines):
                combo_to_append_s = f"{ranks[i]}{ranks[row]}s"
                if (clicked_combo not in selected_combos) and (combo_to_append_s not in selected_combos):
                    combos.append(combo_to_append_s)
                elif (clicked_combo in selected_combos) and (combo_to_append_s in selected_combos):
                    combos.append(combo_to_append_s)
                combo_to_append_o = f"{ranks[i]}{ranks[row]}o"
                if (clicked_combo not in selected_combos) and (combo_to_append_o not in selected_combos):
                    combos.append(combo_to_append_o)
                elif (clicked_combo in selected_combos) and (combo_to_append_o in selected_combos):
                    combos.append(combo_to_append_o)
            for i in range(lower_lines):
                combo_to_append_s = f"{ranks[row]}{ranks[12 - i]}s"
                if (clicked_combo not in selected_combos) and (combo_to_append_s not in selected_combos):
                    combos.append(combo_to_append_s)
                elif (clicked_combo in selected_combos) and (combo_to_append_s in selected_combos):
                    combos.append(combo_to_append_s)
                combo_to_append_o = f"{ranks[row]}{ranks[12 - i]}o"
                if (clicked_combo not in selected_combos) and (combo_to_append_o not in selected_combos):
                    combos.append(combo_to_append_o)
                elif (clicked_combo in selected_combos) and (combo_to_append_o in selected_combos):
                    combos.append(combo_to_append_o)
        elif event.state == 131336: # Alt
            if not diagonal_combos:
                first_combo = combos_matrix[row][col]
                diagonal_combos.add(first_combo)
                directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                for dr, dc in directions:
                    i = 1
                    while True:
                        r = row + dr * i
                        c = col + dc * i
                        if not (0 <= r < 13 and 0 <= c < 13):

                            break
                        diagonal_combos.add(combos_matrix[r][c])
                        i += 1

        return combos
    def mouse_click(event: tk.Event):
        global current_pool
        nonlocal  click_mode
        row, col = get_click_row_col(event)
        abs_row_col = abs(row - col)
        clicked_combo = combos_matrix[row][col]
        combos = [clicked_combo]
        combos = check_combo_selection_triggers(event, col, row, clicked_combo, abs_row_col, combos)
        for combo in combos:
            if combo not in current_selection:
                current_selection.add(combo)
                if combo not in selected_combos:
                    click_mode = "select"
                    canvas.itemconfig(f"{combo}_cell", fill=fill_color)
                    selected_combos.add(combo)
                    current_pool.append(combo)
                else:
                    click_mode = "unselect"
                    canvas.itemconfig(f"{combo}_cell", fill="")
                    selected_combos.remove(combo)
                    current_pool.remove(combo)
    def mouse_drag(event: tk.Event):
        row, col = get_click_row_col(event)
        abs_row_col = abs(row - col)
        clicked_combo = combos_matrix[row][col]
        combos = [clicked_combo]
        combos = check_combo_selection_triggers(event, col, row, clicked_combo, abs_row_col, combos)
        for combo in combos:
            if diagonal_combos:
                if combo not in diagonal_combos:

                    continue
            if combo not in current_selection:
                current_selection.add(combo)
                if combo not in selected_combos and click_mode == "select":
                    canvas.itemconfig(f"{combo}_cell", fill=fill_color)
                    selected_combos.add(combo)
                    current_pool.append(combo)
                elif combo in selected_combos and click_mode == "unselect":
                    canvas.itemconfig(f"{combo}_cell", fill="")
                    selected_combos.remove(combo)
                    current_pool.remove(combo)
    def mouse_release(_):
        nonlocal current_selection, diagonal_combos, click_mode
        current_selection = set()
        diagonal_combos = set()
        click_mode = None
        edit_pool_label_local.config(text=f"COMBOS POOL ({len(selected_combos)})")
    canvas.create_rectangle(2, 0, matrix_size, 12, fill=None, outline=border_color)
    edit_pool_frame_local = tk.Frame(canvas, bd=0, highlightthickness=0)
    edit_pool_frame_local.place(relx=0.36, y=1)
    edit_pool_label_local = tk.Label(edit_pool_frame_local, pady=0, bd=0, highlightthickness=0, text=f"COMBOS POOL ({len(selected_combos)})", font=("Arial", 7,  "bold"), bg="white", fg='black')
    edit_pool_label_local.pack(pady=0)
    for row in range(matrix_length):
        for column in range(matrix_length):
            combo = combos_matrix[row][column]
            combo_bg_color = fill_color if combo in selected_combos else None
            combo_x0 = (column * cell_size) + 2
            combo_x1 = combo_x0 + cell_size
            combo_y0 = (row * cell_size) + 2 + 10
            combo_y1 = combo_y0 + cell_size
            canvas.create_rectangle(combo_x0, combo_y0, combo_x1, combo_y1, fill=combo_bg_color, outline=border_color, tags=f'{combo}_cell')
            canvas.create_text(combo_x0 + (cell_size // 2), combo_y0 + (cell_size // 2), text=combo)
    canvas.bind("<Button-1>", mouse_click)
    canvas.bind("<B1-Motion>", mouse_drag)
    canvas.bind("<ButtonRelease-1>", mouse_release)


def end_edit():
    all_dropdowns = [
        folder_dropdown,
        depth_dropdown,
        hero_position_dropdown,
        spot_action_text_dropdown,
        villain_position_dropdown,
        combo_pool_type_dropdown,
        spot_action_entry_1,
        spot_action_entry_2
    ]
    for dropdown in all_dropdowns:
        dropdown.config(state="readonly")
    solutions_buttons = [
        add_solution_buttom,
        del_solution_buttom,
        del_all_buttom
    ]
    for button in solutions_buttons:
        button.config(state="normal")
    global current_pool, edit_canvas
    edit_pool_button.config(text="EDIT POOL")
    edit_canvas.destroy()
    pool_chart = draw_pool_chart(current_pool)
    pool_chart_tk = ImageTk.PhotoImage(pool_chart)
    pool_label.config(image=pool_chart_tk)
    pool_label.image = pool_chart_tk


def add_solution():
    global pools
    options = [
        depth_var.get(),
        hero_position_var.get(),
        spot_action_text_var.get(),
        villain_position_var.get(),
        combo_pool_type_var.get(),
        folder_var.get().replace(" ", "").lower()
    ]
    try:
        mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict = get_data(options[0], options[1], options[2], options[3], options[5])
    except:
        status_label.config(text="NOT FOUND")
        return
    values = (options[0], options[1], options[2], options[3], options[5])
    for item in choosen_spots_list.get_children():
        if choosen_spots_list.item(item, "values") == values:
            return
    spot_id = choosen_spots_list.insert("", "end", values=values)
    pools[spot_id] = current_pool


def delete_solution():
    global pools
    selected_items = choosen_spots_list.selection()
    if not selected_items:

        return
    for spot_id in selected_items:
        pools.pop(spot_id, None)
        choosen_spots_list.delete(spot_id)


def delete_all_solutions():
    global pools
    for spot_id in choosen_spots_list.get_children():
        choosen_spots_list.delete(spot_id)
    pools.clear()


def show_selected_spot_treeview(event=None):
    global current_pool
    selected = choosen_spots_list.selection()
    if not selected:

        return
    spot_id = selected[0]
    item = choosen_spots_list.item(spot_id)
    values = item["values"]
    depth = values[0]
    hero = values[1]
    villain = values[3]
    spot = values[2]
    folder = values[4]
    pool = pools[spot_id]
    try:
        mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict = get_data(depth, hero, spot, villain, folder)
    except:
        status_label.config(text="SPOT NOT FOUND", fg="white")

        return
    mode_str, spot_string, spot_position, spot_actions, combos_order, prefolded_combos, spot_max_ev, spot_total_ev = parse_spot(mode_depth, positions_actions, actions_frequencies, combos_dict)
    pool_chart = draw_pool_chart(pool)
    pool_chart_tk = ImageTk.PhotoImage(pool_chart)
    pool_label.config(image=pool_chart_tk)
    pool_label.image = pool_chart_tk
    combo_colors_info_dict, spot_actions_text_colors, combos_order, fold_combos_final = parse_data(mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict)
    chart = draw_proof_chart(combo_colors_info_dict, spot_actions_text_colors, combos_order, fold_combos_final)
    chart_tk = ImageTk.PhotoImage(chart)
    help_label.config(image=chart_tk)
    help_label.image = chart_tk
    current_pool = pool
    status_label.config(text="SPOT FOUND", fg="white")


def show_clock():
    if clock_var.get():
        clock_label.pack(side="left")
    else:
        clock_label.pack_forget()


def update_last_combo_result_frame(line_1: str, line_2: str, line1_color: str, line1_text_color:str):
    lr_canvas.delete("all")
    line1_text = lr_canvas.create_text(last_result_line1_x, last_result_line1_y + 1, font=("Arial", 9, "bold"), text=line_1, fill=line1_text_color)
    x1, y1, x2, y2 = lr_canvas.bbox(line1_text)
    line1_rect = lr_canvas.create_rectangle(x1 - 2, y1 - 2, x2 + 2, y2 + 2, fill=line1_color, outline="")
    lr_canvas.tag_raise(line1_text, line1_rect)
    lr_canvas.create_text(last_result_line2_x, last_result_line2_y, font=("Arial", 12, "bold"), text=line_2, fill="white")



# ===================================
# ------- MAIN ROOT -------
# ===================================
root = tk.Tk()
root.title("Preflop Trainer")
root.geometry(f"{root_width}x{root_height}+0+0")
root.resizable(False, False)

#TK_VARS
folder_var = tk.StringVar(root, value="Chip EV")
depth_var = tk.StringVar(root, value="50")
hero_position_var = tk.StringVar(root, value="UTG")
spot_action_text_var = tk.StringVar(root, value="rfi")
villain_position_var = tk.StringVar(root, value="None")
combo_pool_type_var = tk.StringVar(root, value="bd")
combo_pool_var_1 = tk.StringVar(root, value="1")
combo_pool_var_2 = tk.StringVar(root, value="70")
action_selected = tk.BooleanVar(value=False)
clock_var = tk.BooleanVar(value=True)
pause_each_var = tk.StringVar(value="never")
limit_type_var = tk.StringVar(root, value="hands")
limit_value_var = tk.StringVar(root, value="inf")
show_part_results = tk.BooleanVar(value=True)
show_curr_results = tk.BooleanVar(value=True)
roles_var = tk.StringVar(value="custom")
dealing_options_var = tk.StringVar(value="per combo")
precision_var = tk.StringVar(value="precise")
freeze_var = tk.StringVar(value="never")
show_results_var = tk.StringVar(value="both")
training_continue = tk.BooleanVar(value=False)

# MAIN FRAME
main_frame = tk.Frame(root, width=main_frame_width, height=main_frame_height, bg='#ffffff')
main_frame.pack(side="left", fill="both")

last_result_frame = tk.Frame(main_frame, width=last_result_frame_width, height=last_result_frame_height, bg=bgd_color)
last_result_frame.pack(side="bottom", fill="both")
lr_canvas = tk.Canvas(last_result_frame, width=last_result_frame_width, height=last_result_frame_height, highlightthickness=0, bd=0, bg=bgd_color)
lr_canvas.pack()

# OPTIONS FRAME
options_frame = tk.Frame(root, width=options_frame_width, height=options_frame_height, bg=bgd_color)
options_frame.pack(side="left", fill='both')

user_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
user_frame.place(relx=0.5, rely=0.06, anchor="center")
user_label = tk.Label(user_frame, fg='white', bg=bgd_color, pady=0, text="User")
user_label.grid(row=0, column=0, columnspan=2)
user_entry = tk.Entry(user_frame, width=30, justify="center")
user_entry.grid(row=1, column=0, columnspan=2)
password_label = tk.Label(user_frame, fg='white', bg=bgd_color, pady=0, text="Password")
password_label.grid(row=2, column=0, columnspan=2)
password_entry = tk.Entry(user_frame, width=26, justify='center')
password_entry.config(show="*")
password_entry.grid(row=3, column=0, sticky='w')
show_password = tk.Label(user_frame, fg='white', bg=bgd_color, pady=0, text="👁", cursor="hand2")
show_password.grid(row=3, column=1, sticky='e', padx=(0,10))

login_btns_frame = tk.Frame(options_frame, bg=bgd_color)
login_btns_frame.place(relx=0.5, rely=0.15, anchor="center")
login_button = tk.Button(login_btns_frame, bd=0, pady=0, padx=0, text="LOGIN", font=("Arial", 9), command=lambda:login(root, user_entry.get(), password_entry.get()))
login_button.grid(row=0, column=0)
logout_button = tk.Button(login_btns_frame, bd=0, pady=0, padx=0, text="LOGOUT", font=("Arial", 9), command=logout)
logout_button.grid(row=0, column=1, padx=(5, 5))
add_usr_button = tk.Button(login_btns_frame, bd=0, pady=0, padx=0, text="SIGN UP", font=("Arial", 9), command=add_user_toplevel)
add_usr_button.grid(row=0, column=2, padx=(0,5))
del_usr_button = tk.Button(login_btns_frame, bd=0, pady=0, padx=0, text="DEL USR", font=("Arial", 9), command=lambda:delete_user(root, user_entry.get()))
del_usr_button.grid(row=0, column=3)

login_status_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
login_status_frame.place(relx=0.5, rely=0.185, anchor="center")
login_status_label = tk.Label(login_status_frame, fg='white', bg=bgd_color, pady=0, text="Login before start.", justify="center")
login_status_label.pack()

dropdowns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
dropdowns_frame.place(relx=0.5, rely=0.25, anchor="center")
folder_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=folder_var, values=folder_options, width=8, state="readonly", height=20)
folder_dropdown.grid(row=0, column=0, sticky="w", padx=(15,5), pady=0)
depth_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=depth_var, values=depths, width=4, state="readonly", height=20)
depth_dropdown.grid(row=0, column=1, sticky="w", padx=(0,5), pady=0)
hero_position_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=hero_position_var, values=positions, width=5, state="readonly", height=10)
hero_position_dropdown.grid(row=0, column=2, sticky="w", pady=0)
spot_action_text_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=spot_action_text_var, values=spot_actions_text, width=16, state="readonly", height=10)
spot_action_text_dropdown.grid(row=1, column=0, columnspan=2, sticky="w", pady=2, padx=(0,5))
villain_position_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=villain_position_var, values=possible_villains, width=5, state="readonly", height=10)
villain_position_dropdown.grid(row=1, column=2, sticky="w", pady=2)
combo_pool_type_dropdown = ttk.Combobox(dropdowns_frame, justify="center", textvariable=combo_pool_type_var, values=combo_pool_types, width=10, state="readonly", height=10)
combo_pool_type_dropdown.grid(row=2, column=0, sticky="e", padx=(0,5), pady=0)
spot_action_entry_1 = ttk.Combobox(dropdowns_frame, justify="center", textvariable=combo_pool_var_1, values=one_to_hundred, width=3, state="readonly", height=20)
spot_action_entry_1.grid(row=2, column=1, sticky="e", padx=(0,2), pady=0)
spot_action_entry_2 = ttk.Combobox(dropdowns_frame, justify="center", textvariable=combo_pool_var_2, values=one_to_hundred, width=3, state="readonly", height=20)
spot_action_entry_2.grid(row=2, column=2, sticky="e", padx=0, pady=0)

edit_pool_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
edit_pool_frame.place(relx=0.5, rely=0.33, anchor="center")
edit_pool_button = tk.Button(edit_pool_frame, bd=0, pady=0, padx=0, text="EDIT POOL", command=toggle_edit_pool)
edit_pool_button.pack()

solutions_btns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
solutions_btns_frame.place(relx=0.5, rely=0.37, anchor="center")
add_solution_buttom = tk.Button(solutions_btns_frame, bd=0, pady=0, padx=5, text="ADD SPOT", command=add_solution)
add_solution_buttom.grid(row=3, column=0, padx=(0,5), pady=0)
del_solution_buttom = tk.Button(solutions_btns_frame, bd=0, pady=0, padx=5, text="DEL SPOT", command=delete_solution)
del_solution_buttom.grid(row=3, column=1, padx=(0,5), pady=0)
del_all_buttom = tk.Button(solutions_btns_frame, bd=0, pady=0, padx=5, text="DEL ALL", command=delete_all_solutions)
del_all_buttom.grid(row=3, column=2, pady=0)

choosen_spots_frame = tk.Frame(options_frame, width=options_frame_width)
choosen_spots_frame.place(x=111, rely=0.515, anchor="center")
scrollbar = tk.Scrollbar(choosen_spots_frame, orient="vertical", width=5)
scrollbar.pack(side="right", fill="y")
choosen_spots_list = ttk.Treeview(choosen_spots_frame, height=7, columns=("col1", "col2", "col3", "col4", "col5"))
choosen_spots_list.heading("#0", text="")
choosen_spots_list.heading("#1", text="bb")
choosen_spots_list.heading("#2", text="HERO")
choosen_spots_list.heading("#3", text="SPOT")
choosen_spots_list.heading("#4", text="VIL.")
choosen_spots_list.heading("#5", text="CM")
choosen_spots_list.column("#0", width=1, stretch=tk.NO)
choosen_spots_list.column("#1", width=31)
choosen_spots_list.column("#2", width=38)
choosen_spots_list.column("#3", width=102)
choosen_spots_list.column("#4", width=54)
choosen_spots_list.column("#5", width=1)
choosen_spots_list.pack(side="left")

roles_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
roles_frame.place(relx=0.5, rely=0.665, anchor="center")
roles_label = tk.Label(roles_frame, fg="white", bg=bgd_color, text="ROLE:", font=("Arial", 12, "bold"))
roles_label.pack(side="left")
roles_dropdown = ttk.Combobox(roles_frame, background=bgd_color, justify="center", textvariable=roles_var, values=roles_options, width=10, state="readonly", height=5)
roles_dropdown.pack(side="left")

dealing_opt_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
dealing_opt_frame.place(relx=0.5, rely=0.705, anchor="center")
dealing_opt_label = tk.Label(dealing_opt_frame, fg="white", bg=bgd_color, text="DEALING:", font=("Arial", 12, "bold"))
dealing_opt_label.pack(side="left")
dealing_opt_dropdown = ttk.Combobox(dealing_opt_frame, background=bgd_color, justify="center", textvariable=dealing_options_var, values=dealing_options, width=10, state="readonly", height=5)
dealing_opt_dropdown.pack(side="left")

precision_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
precision_frame.place(relx=0.5, rely=0.744, anchor="center")
precision_label = tk.Label(precision_frame, fg="white", bg=bgd_color, text="PRECISION:", font=("Arial", 12, "bold"))
precision_label.pack(side="left")
precision_dropdown = ttk.Combobox(precision_frame, background=bgd_color, justify="center", textvariable=precision_var, values=precisions, width=8, state="readonly", height=5)
precision_dropdown.pack(side="left")

limits_frame = tk.Frame(options_frame, width=options_frame_width, background=bgd_color)
limits_frame.place(relx=0.5, rely=0.784, anchor="center")
limit_label = tk.Label(limits_frame, fg='white', bg=bgd_color, pady=0, text="LIMIT:", font=("Arial", 12, "bold"))
limit_label.pack(side="left")
combo_pool_type_dropdown = ttk.Combobox(limits_frame, justify="center", textvariable=limit_type_var, values=limits_types, width=7, state="readonly", height=5)
combo_pool_type_dropdown.pack(side="left")
limit_value_entry = tk.Entry(limits_frame, textvariable=limit_value_var, width=5, justify='center')
limit_value_entry.pack(side="left")

freeze_opt_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
freeze_opt_frame.place(relx=0.5, rely=0.824, anchor="center")
freeze_label = tk.Label(freeze_opt_frame, fg="white", bg=bgd_color, text="FREEZE:", font=("Arial", 12, "bold"))
freeze_label.pack(side="left")
freeze_dropdown = ttk.Combobox(freeze_opt_frame, background=bgd_color, justify="center", textvariable=freeze_var, values=freeze_options, width=15, state="readonly", height=5)
freeze_dropdown.pack(side="left")

show_rtresults_frame = tk.Frame(options_frame, width=options_frame_width, height=25, bg=bgd_color)
show_rtresults_frame.place(relx=0.5, rely=0.864, anchor="center")
show_rtresults_label = tk.Label(show_rtresults_frame, fg="white", bg=bgd_color, text="RTR SHOW:", font=("Arial", 12, "bold"))
show_rtresults_label.pack(side="left")
show_rtresults_dropdown = ttk.Combobox(show_rtresults_frame, background=bgd_color, justify="center", textvariable=show_results_var, values=show_results_option, width=8, state="readonly", height=5)
show_rtresults_dropdown.pack(side="left")

help_pool_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
help_pool_frame.place(relx=0.51, rely=0.8973, anchor="center")
h_key_label = tk.Label(help_pool_frame, pady=0, text="<h> - HELP", font=("Arial", 9))
h_key_label.pack(side='left', pady=0, padx=(0,5))
p_key_label = tk.Label(help_pool_frame, pady=0, text="<p> - POOL", font=("Arial", 9))
p_key_label.pack(side='right', pady=0, padx=(5,0))

start_stop_btns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
start_stop_btns_frame.place(relx=0.51, rely=0.93, anchor="center")
start_trainer_buttom = tk.Button(start_stop_btns_frame, bd=0, pady=0, padx=5, text="START", command=start_training)
start_trainer_buttom.grid(row=0, column=0, padx=(0, 15))
pause_trainer_buttom = tk.Button(start_stop_btns_frame, bd=0, pady=0, padx=5, text="PAUSE")#, command=pause_trainer)
pause_trainer_buttom.grid(row=0, column=1, padx=(0, 15))
stop_trainer_buttom = tk.Button(start_stop_btns_frame, bd=0, pady=0, padx=5, text="STOP")#, command=stop_trainer)
stop_trainer_buttom.grid(row=0, column=2)

status_frame = tk.Frame(options_frame, width=options_frame_width, height=30, bg=bgd_color)
status_frame.place(relx=0.5, rely=0.9632, anchor="center")
status_label = tk.Label(status_frame, bd=0, bg=bgd_color, text="STOPPED", foreground=stopped_color, font=("Arial", 12, "bold"))
status_label.pack()

clock_frame = tk.Frame(options_frame, width=options_frame_width, height=25, bg=bgd_color, bd=0, pady=0, highlightthickness=0)
clock_frame.place(relx=0.5, rely=0.99, anchor="center")
clock_frame.pack_propagate(False)
clock_check_btn = tk.Checkbutton(clock_frame, bd=0, highlightthickness=0, command=show_clock, variable=clock_var, text="show clock", foreground="white", selectcolor="black", bg=bgd_color)
clock_check_btn.pack(side="left")
clock_label = tk.Label(clock_frame, width=16, bd=0, font=("Consolas", 12), foreground="white", bg=bgd_color)
clock_label.pack(side="left")

# CHARTS FRAME
charts_frame = tk.Frame(root, width=charts_frame_width, height=charts_frame_height, bg=bgd_color)
charts_frame.pack(side="left", fill='both')

help_frame = tk.Frame(charts_frame, bg=bgd_color, width=325, height=336)
help_frame.place(x=0, y=-2)
help_label = tk.Label(help_frame, bd=0, pady=0)
help_label.pack()
pool_frame = tk.Frame(charts_frame, bg=bgd_color, width=325, height=336)
pool_frame.place(x=0, y=333)
pool_label = tk.Label(pool_frame, bd=0, pady=0)
pool_label.pack()

#BINDS
root.bind("h", toggle_help)
root.bind("p", toggle_pool)

show_password.bind("<ButtonPress-1>", show_password_press)
show_password.bind("<ButtonRelease-1>", show_password_release)
show_password.bind("<Leave>", show_password_leave)
spot_action_text_dropdown.bind("<<ComboboxSelected>>", lambda event: get_possible_villains())
hero_position_dropdown.bind("<<ComboboxSelected>>", lambda event: get_possible_villains())
root.bind("h", toggle_help)
root.bind("p", toggle_pool)
h_key_label.bind("<Button-1>", toggle_help)
p_key_label.bind("<Button-1>", toggle_pool)
choosen_spots_list.bind("<<TreeviewSelect>>", lambda event: show_selected_spot_treeview())

depth_var.trace_add("write", lambda *args: preview_pool(depth_var.get(), hero_position_var.get(), spot_action_text_var.get(), villain_position_var.get(), folder_var.get(), combo_pool_type_var.get(), combo_pool_var_1.get(), combo_pool_var_2.get()))
folder_var.trace_add("write", lambda *args: preview_pool(depth_var.get(), hero_position_var.get(), spot_action_text_var.get(), villain_position_var.get(), folder_var.get(), combo_pool_type_var.get(), combo_pool_var_1.get(), combo_pool_var_2.get()))
hero_position_var.trace_add("write", lambda *args: (preview_pool(depth_var.get(), hero_position_var.get(), spot_action_text_var.get(), villain_position_var.get(), folder_var.get(), combo_pool_type_var.get(), combo_pool_var_1.get(), combo_pool_var_2.get())))
spot_action_text_var.trace_add("write", lambda *args: (preview_pool(depth_var.get(), hero_position_var.get(), spot_action_text_var.get(), villain_position_var.get(), folder_var.get(), combo_pool_type_var.get(), combo_pool_var_1.get(), combo_pool_var_2.get()), pool_type_from_spot()))
villain_position_var.trace_add("write", lambda *args: preview_pool(depth_var.get(), hero_position_var.get(), spot_action_text_var.get(), villain_position_var.get(), folder_var.get(), combo_pool_type_var.get(), combo_pool_var_1.get(), combo_pool_var_2.get()))
combo_pool_type_var.trace_add("write", lambda *args: (preview_pool(depth_var.get(), hero_position_var.get(), spot_action_text_var.get(), villain_position_var.get(), folder_var.get(), combo_pool_type_var.get(), combo_pool_var_1.get(), combo_pool_var_2.get()), pool_vars_from_pool_type()))
combo_pool_var_1.trace_add("write", lambda *args: preview_pool(depth_var.get(), hero_position_var.get(), spot_action_text_var.get(), villain_position_var.get(), folder_var.get(), combo_pool_type_var.get(), combo_pool_var_1.get(), combo_pool_var_2.get()))
combo_pool_var_2.trace_add("write", lambda *args: preview_pool(depth_var.get(), hero_position_var.get(), spot_action_text_var.get(), villain_position_var.get(), folder_var.get(), combo_pool_type_var.get(), combo_pool_var_1.get(), combo_pool_var_2.get()))

# MAIN_LOOP
load_database()

preview_pool(depth_var.get(), hero_position_var.get(), spot_action_text_var.get(), villain_position_var.get(), folder_var.get(), combo_pool_type_var.get(), combo_pool_var_1.get(), combo_pool_var_2.get())

root.mainloop()
