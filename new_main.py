import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
import re
import bcrypt
from tkinter import ttk



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
                combos_pool TEXT,
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
            CREATE TABLE IF NOT EXISTS hands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                training_id INTEGER NOT NULL,
                spot TEXT,
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
# ------- SQL VARIABLES -------
# ===================================
database_file = "db_trainer.db"



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



# ===================================
# ------- ROOT VARIABLES -------
# ===================================
logged_in = False
logged_user_id = None
logged_username = None

root_width, root_height = 1366, 707

main_frame_width, main_frame_height = 800, 707
options_frame_width, options_frame_height = 240, root_height
charts_frame_width, charts_frame_height = 326, root_height

table_frame_width = current_progress_frame_width = last_result_frame_width = actions_frame_width = main_frame_width
current_progress_frame_height = 36
table_frame_height = 560
actions_frame_height = 41
last_result_frame_height = 70

oval_center_x = (table_frame_width // 2) - 1
oval_center_y = table_frame_height // 2 - 14
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

current_progress_line1_x = current_progress_frame_width // 2
current_progress_line1_y = (current_progress_frame_height // 5) + 1
current_progress_line2_x = current_progress_frame_width // 2
current_progress_line2_y = current_progress_frame_height - 7

last_result_line1_x = last_result_frame_width // 2
last_result_line1_y = (last_result_frame_height // 8) - 1
last_result_line2_x = last_result_frame_width // 2
last_result_line2_y = last_result_frame_height - 45

bgd_color = "#515152"
table_color = "#61cc4b"
btn_color = "#F39508"
position_color = "#E9E9E9" 

depths = ["200", "160", "130", "100", "80", "70", "60", "55", "50", "45", "40", "38", "35", "32", "30", "28", "26", "25", "22", "20", "19", "17", "16", "15", "14", "13", "12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
one_to_hundred = [i for i in range(101)]
positions = ["UTG", "UTG1", "LJ", "HJ", "CO", "BTN", "SB", "BB"]
spot_actions_text = ["rfi", "vs_rfi", "vs_open_shove", "vs_3bet_nai_low", "vs_3bet_ai", "vs_limp", "vs_raise_ai", "vs_raise_nai_low", "vs_raise_nai_low-med"]
combo_pool_types = ["all", "tot-75", "tot-100", "bd-0.01-0.7", "mb-1", "mb-0.01", "mb-0.1", "mb-0"]
limits_types = ["hands", "time (s)", "all pool"]
possible_villains = ["None"]



# ===================================
# ------- MAIN ROOT -------
# ===================================
root = tk.Tk()
root.title("Preflop Trainer")
root.geometry(f"{root_width}x{root_height}+0+0")
root.resizable(False, False)

folder_var = tk.StringVar(root, value="json_results")
depth_var = tk.StringVar(root, value="50")
hero_position_var = tk.StringVar(root, value="UTG")
spot_action_text_var = tk.StringVar(root, value="rfi")
villain_position_var = tk.StringVar(root, value="None")
combo_pool_type_var = tk.StringVar(root, value="bd-0.01-0.7")
combo_pool_var_1 = tk.StringVar(root, value="0")
combo_pool_var_2 = tk.StringVar(root, value="0")
action_selected = tk.BooleanVar(value=False)
clock_var = tk.BooleanVar(value=True)
pause_each_var = tk.StringVar(value="never")
limit_type_var = tk.StringVar(root, value="hands")
limit_value_var = tk.StringVar(root, value="inf")
show_part_results = tk.BooleanVar(value=True)
show_curr_results = tk.BooleanVar(value=True)

# MAIN FRAME
main_frame = tk.Frame(root, width=main_frame_width, height=main_frame_height, bg='#ffffff')
main_frame.pack(side="left", fill="both")

# OPTIONS FRAME
options_frame = tk.Frame(root, width=options_frame_width, height=options_frame_height, bg=bgd_color)
options_frame.pack(side="left", fill='both')

user_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
user_frame.place(relx=0.5, rely=0.06, anchor="center")
user_label = tk.Label(user_frame, fg='white', bg=bgd_color, pady=0, text="User")
user_label.grid(row=0, column=0, columnspan=4)
user_entry = tk.Entry(user_frame, width=30, justify="center")
user_entry.grid(row=1, column=0, columnspan=4)
password_label = tk.Label(user_frame, fg='white', bg=bgd_color, pady=0, text="Password")
password_label.grid(row=2, column=0, columnspan=4)
password_entry = tk.Entry(user_frame, width=26, justify='center')
password_entry.config(show="*")
password_entry.grid(row=3, column=0, columnspan=4, sticky='w')
show_password = tk.Label(user_frame, fg='white', bg=bgd_color, pady=0, text="👁", cursor="hand2")
show_password.grid(row=3, column=1, columnspan=4, sticky='e', padx=(0,10))

login_btns_frame = tk.Frame(options_frame, bg=bgd_color)
login_btns_frame.place(relx=0.5, rely=0.15, anchor="center")
login_button = tk.Button(login_btns_frame, bd=0, pady=0, padx=0, text="LOGIN", font=("Arial1", 9), command=lambda:login(root, user_entry.get(), password_entry.get()))
login_button.grid(row=0, column=0)
logout_button = tk.Button(login_btns_frame, bd=0, pady=0, padx=0, text="LOGOUT", font=("Arial1", 9), command=logout)
logout_button.grid(row=0, column=1, padx=(5, 5))
add_usr_button = tk.Button(login_btns_frame, bd=0, pady=0, padx=0, text="SIGN UP", font=("Arial1", 9), command=add_user_toplevel)
add_usr_button.grid(row=0, column=2, padx=(0,5))
del_usr_button = tk.Button(login_btns_frame, bd=0, pady=0, padx=0, text="DEL USR", font=("Arial1", 9), command=lambda:delete_user(root, user_entry.get()))
del_usr_button.grid(row=0, column=3)

login_status_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
login_status_frame.place(relx=0.5, rely=0.185, anchor="center")
login_status_label = tk.Label(login_status_frame, fg='white', bg=bgd_color, pady=0, text="Login before start.", justify="center")
login_status_label.pack()

dropdowns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
dropdowns_frame.place(relx=0.5, rely=0.25, anchor="center")
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
edit_pool_frame.place(relx=0.5, rely=0.33, anchor="center")
edit_pool_button = tk.Button(edit_pool_frame, bd=0, pady=0, padx=0, text="EDIT POOL")
edit_pool_button.pack()

solutions_btns_frame = tk.Frame(options_frame, width=options_frame_width, bg=bgd_color)
solutions_btns_frame.place(relx=0.5, rely=0.37, anchor="center")
add_solution_buttom = tk.Button(solutions_btns_frame, bd=0, pady=0, padx=5, text="ADD SPOT") #, command=add_solution)
add_solution_buttom.grid(row=3, column=0, padx=(0,5), pady=0)
del_solution_buttom = tk.Button(solutions_btns_frame, bd=0, pady=0, padx=5, text="DEL SPOT") #, command=delete_solution)
del_solution_buttom.grid(row=3, column=1, padx=(0,5), pady=0)
del_all_buttom = tk.Button(solutions_btns_frame, bd=0, pady=0, padx=5, text="DEL ALL") #, command=delete_all_solution)
del_all_buttom.grid(row=3, column=2, pady=0)

choosen_spots_frame = tk.Frame(options_frame, width=options_frame_width)
choosen_spots_frame.place(relx=0.5, rely=0.515, anchor="center")
scrollbar = tk.Scrollbar(choosen_spots_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")
choosen_spots_list = ttk.Treeview(choosen_spots_frame, height=7, columns=("col1", "col2", "col3", "col4"))
choosen_spots_list.heading("#0", text="")
choosen_spots_list.heading("#1", text="bb")
choosen_spots_list.heading("#2", text="HERO")
choosen_spots_list.heading("#3", text="VIL.")
choosen_spots_list.heading("#4", text="SPOT")
choosen_spots_list.column("#0", width=1, stretch=tk.NO)
choosen_spots_list.column("#1", width=31)
choosen_spots_list.column("#2", width=40)
choosen_spots_list.column("#3", width=40)
choosen_spots_list.column("#4", width=106)
choosen_spots_list.pack(side="left")

# CHARTS FRAME
charts_frame = tk.Frame(root, width=charts_frame_width, height=charts_frame_height, bg=bgd_color)
charts_frame.pack(side="left", fill='both')

help_frame = tk.Frame(charts_frame, bg=bgd_color, width=325, height=336)
help_label = tk.Label(help_frame, bd=0, pady=0)
help_label.pack()
pool_frame = tk.Frame(charts_frame, bg=bgd_color, width=325, height=336)
pool_label = tk.Label(pool_frame, bd=0, pady=0)
pool_label.pack()

#BINDS
show_password.bind("<ButtonPress-1>", show_password_press)
show_password.bind("<ButtonRelease-1>", show_password_release)
show_password.bind("<Leave>", show_password_leave)

load_database()

root.mainloop()
