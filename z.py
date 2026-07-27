import tkinter as tk
from math import ceil, sin, cos, pi
from pathlib import Path
import json
import random
from PIL import Image, ImageDraw, ImageFont, ImageTk

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

main_frame = tk.Frame(root, width=main_frame_width, height=main_frame_height, bg=bgd_color)
main_frame.pack(side="left")

canvas = tk.Canvas(main_frame, width=main_frame_width, height=main_frame_height, background=bgd_color)
canvas.pack()

cards_width = 96 # 64
cards_height = int((cards_width / 2) * 1.36)

root.mainloop()