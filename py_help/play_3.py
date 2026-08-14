import pyautogui as pg
import random

plays = 900

opt = ["2", "3"]

pg.PAUSE = 0.2
pg.click((321, 432))
pg.click((868, 513))

for i in range(plays):
    pg.press(random.choice(opt))

pg.click((987, 512))
