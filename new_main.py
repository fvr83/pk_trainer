import sqlite3
import tkinter as tk



# ===================================
# ------- SQL FUNCTIONS -------
# ===================================

def load_database():
    conn = sqlite3.connect(database_file)
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
            address TEXT,
            email TEXT,
            personal_id TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trainings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            hands_trained INTEGER DEFAULT 0,
            right_hands INTEGER DEFAULT 0,
            imprecise_hands INTEGER DEFAULT 0,
            wrong_hands INTEGER DEFAULT 0,
            train_accuracy REAL,
            train_ev_loss REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            training_id INTEGER NOT NULL,
            spot TEXT,
            combo TEXT,
            user_decision TEXT,
            correct_decision TEXT,
            evaluation TEXT,
            decision_time REAL,
            accuracy REAL,
            ev_loss REAL,
            FOREIGN KEY (user_id) REFERENCES users(id),
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
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def add_user(user_name, password, name, address, email, personal_id):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()




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



# ===================================
# ------- ROOT VARIABLES -------
# ===================================

root_width, root_height = 1366, 707

main_frame_width, main_frame_height = 800, 707
options_frame_width, options_frame_height = 240, root_height
charts_frame_width, charts_frame_height = 326, root_height

table_frame_width = current_progress_frame_width = last_result_frame_width = actions_frame_width = main_frame_width
current_progress_frame_height = 36
table_frame_height = 560
actions_frame_height = 75
last_result_frame_height = 36

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

depths = ["200", "160", "130", "100", "80", "70", "60", "55", "50", "45", "40", "38", "35", "32", "30", "28", "26", "25", "22", "20", "19", "17", "16", "15", "14", "13", "12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
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
action_selected = tk.BooleanVar(value=False)
clock_var = tk.BooleanVar(value=False)
pause_each_var = tk.BooleanVar(value=True)
limit_type_var = tk.StringVar(root, value="hands")
limit_value_var = tk.StringVar(root, value="inf")

main_frame = tk.Frame(root, width=main_frame_width, height=main_frame_height, bg='#ffffff')
main_frame.pack(side="left", fill="both")

options_frame = tk.Frame(root, width=options_frame_width, height=options_frame_height, bg=bgd_color)
options_frame.pack(side="left", fill='both')
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

charts_frame = tk.Frame(root, width=charts_frame_width, height=charts_frame_height, bg='#ffffff')
charts_frame.pack(side="left", fill='both')

show_password.bind("<ButtonPress-1>", show_password_press)
show_password.bind("<ButtonRelease-1>", show_password_release)
show_password.bind("<Leave>", show_password_leave)

load_database()

root.mainloop()
