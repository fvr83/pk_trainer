import tkinter as tk


### VARIABLES ###
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


### ROOT ###
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

root.mainloop()
