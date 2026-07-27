from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

equity_vs = {
    0: {'AA': 0.0, 'KK': 0.0, 'QQ': 0.0, 'JJ': 0.0, 'TT': 0.0, '99': 0.0, '88': 0.0, '77': 0.0, '66': 0.0, '55': 0.0, '44': 0.0, '33': 0.0, '22': 0.0, 'AKs': 0.0, 'AQs': 0.0, 'AJs': 0.0, 'ATs': 0.0, 'A9s': 0.0, 'A8s': 0.0, 'A7s': 0.0, 'A6s': 0.0, 'A5s': 0.0, 'A4s': 0.0, 'A3s': 0.0, 'A2s': 0.0, 'KQs': 0.0, 'KJs': 0.0, 'KTs': 0.0, 'K9s': 0.0, 'K8s': 0.0, 'K7s': 0.0, 'K6s': 0.0, 'K5s': 0.0, 'K4s': 0.0, 'K3s': 0.0, 'K2s': 0.0, 'QJs': 0.0, 'QTs': 0.0, 'Q9s': 0.0, 'Q8s': 0.0, 'Q7s': 0.0, 'Q6s': 0.0, 'Q5s': 0.0, 'Q4s': 0.0, 'Q3s': 0.0, 'Q2s': 0.0, 'JTs': 0.0, 'J9s': 0.0, 'J8s': 0.0, 'J7s': 0.0, 'J6s': 0.0, 'J5s': 0.0, 'J4s': 0.0, 'J3s': 0.0, 'J2s': 0.0, 'T9s': 0.0, 'T8s': 0.0, 'T7s': 0.0, 'T6s': 0.0, 'T5s': 0.0, 'T4s': 0.0, 'T3s': 0.0, 'T2s': 0.0, '98s': 0.0, '97s': 0.0, '96s': 0.0, '95s': 0.0, '94s': 0.0, '93s': 0.0, '92s': 0.0, '87s': 0.0, '86s': 0.0, '85s': 0.0, '84s': 0.0, '83s': 0.0, '82s': 0.0, '76s': 0.0, '75s': 0.0, '74s': 0.0, '73s': 0.0, '72s': 0.0, '65s': 0.0, '64s': 0.0, '63s': 0.0, '62s': 0.0, '54s': 0.0, '53s': 0.0, '52s': 0.0, '43s': 0.0, '42s': 0.0, '32s': 0.0, 'AKo': 0.0, 'AQo': 0.0, 'AJo': 0.0, 'ATo': 0.0, 'A9o': 0.0, 'A8o': 0.0, 'A7o': 0.0, 'A6o': 0.0, 'A5o': 0.0, 'A4o': 0.0, 'A3o': 0.0, 'A2o': 0.0, 'KQo': 0.0, 'KJo': 0.0, 'KTo': 0.0, 'K9o': 0.0, 'K8o': 0.0, 'K7o': 0.0, 'K6o': 0.0, 'K5o': 0.0, 'K4o': 0.0, 'K3o': 0.0, 'K2o': 0.0, 'QJo': 0.0, 'QTo': 0.0, 'Q9o': 0.0, 'Q8o': 0.0, 'Q7o': 0.0, 'Q6o': 0.0, 'Q5o': 0.0, 'Q4o': 0.0, 'Q3o': 0.0, 'Q2o': 0.0, 'JTo': 0.0, 'J9o': 0.0, 'J8o': 0.0, 'J7o': 0.0, 'J6o': 0.0, 'J5o': 0.0, 'J4o': 0.0, 'J3o': 0.0, 'J2o': 0.0, 'T9o': 0.0, 'T8o': 0.0, 'T7o': 0.0, 'T6o': 0.0, 'T5o': 0.0, 'T4o': 0.0, 'T3o': 0.0, 'T2o': 0.0, '98o': 0.0, '97o': 0.0, '96o': 0.0, '95o': 0.0, '94o': 0.0, '93o': 0.0, '92o': 0.0, '87o': 0.0, '86o': 0.0, '85o': 0.0, '84o': 0.0, '83o': 0.0, '82o': 0.0, '76o': 0.0, '75o': 0.0, '74o': 0.0, '73o': 0.0, '72o': 0.0, '65o': 0.0, '64o': 0.0, '63o': 0.0, '62o': 0.0, '54o': 0.0, '53o': 0.0, '52o': 0.0, '43o': 0.0, '42o': 0.0, '32o': 0.0},
    1: {'AA': 85.27, 'KK': 82.37, 'QQ': 79.91, 'JJ': 77.48, 'TT': 74.97, '99': 71.99, '88': 69.26, '77': 66.25, '66': 63.27, '55': 60.23, '44': 57.03, '33': 53.78, '22': 50.38, 'AKs': 66.92, 'AQs': 66.17, 'AJs': 65.41, 'ATs': 64.61, 'A9s': 62.78, 'A8s': 61.93, 'A7s': 61.07, 'A6s': 59.86, 'A5s': 59.8, 'A4s': 59.03, 'A3s': 58.19, 'A2s': 57.37, 'KQs': 63.3, 'KJs': 62.56, 'KTs': 61.83, 'K9s': 60.02, 'K8s': 58.32, 'K7s': 57.5, 'K6s': 56.67, 'K5s': 55.83, 'K4s': 54.87, 'K3s': 54.02, 'K2s': 53.22, 'QJs': 60.29, 'QTs': 59.5, 'Q9s': 57.68, 'Q8s': 56.02, 'Q7s': 54.32, 'Q6s': 53.61, 'Q5s': 52.61, 'Q4s': 51.92, 'Q3s': 51.0, 'Q2s': 50.21, 'JTs': 57.52, 'J9s': 55.66, 'J8s': 54.01, 'J7s': 52.35, 'J6s': 50.66, 'J5s': 50.02, 'J4s': 49.11, 'J3s': 48.2, 'J2s': 47.39, 'T9s': 54.06, 'T8s': 52.26, 'T7s': 50.78, 'T6s': 48.95, 'T5s': 47.19, 'T4s': 46.58, 'T3s': 45.7, 'T2s': 44.81, '98s': 50.87, '97s': 49.16, '96s': 47.38, '95s': 45.75, '94s': 43.84, '93s': 43.29, '92s': 42.31, '87s': 47.94, '86s': 46.2, '85s': 44.55, '84s': 42.62, '83s': 40.85, '82s': 40.24, '76s': 45.46, '75s': 43.75, '74s': 41.93, '73s': 40.04, '72s': 38.15, '65s': 43.14, '64s': 41.33, '63s': 39.51, '62s': 37.64, '54s': 41.51, '53s': 39.74, '52s': 37.87, '43s': 38.58, '42s': 36.89, '32s': 35.96, 'AKo': 65.25, 'AQo': 64.41, 'AJo': 63.62, 'ATo': 62.65, 'A9o': 60.84, 'A8o': 59.88, 'A7o': 58.89, 'A6o': 57.68, 'A5o': 57.7, 'A4o': 56.69, 'A3o': 55.93, 'A2o': 54.94, 'KQo': 61.55, 'KJo': 60.52, 'KTo': 59.71, 'K9o': 57.81, 'K8o': 56.05, 'K7o': 55.25, 'K6o': 54.26, 'K5o': 53.35, 'K4o': 52.27, 'K3o': 51.39, 'K2o': 50.44, 'QJo': 58.15, 'QTo': 57.28, 'Q9o': 55.31, 'Q8o': 53.7, 'Q7o': 51.76, 'Q6o': 51.09, 'Q5o': 50.13, 'Q4o': 49.14, 'Q3o': 48.21, 'Q2o': 47.23, 'JTo': 55.21, 'J9o': 53.26, 'J8o': 51.41, 'J7o': 49.71, 'J6o': 47.95, 'J5o': 47.1, 'J4o': 46.15, 'J3o': 45.23, 'J2o': 44.27, 'T9o': 51.59, 'T8o': 49.73, 'T7o': 48.0, 'T6o': 46.1, 'T5o': 44.22, 'T4o': 43.55, 'T3o': 42.49, 'T2o': 41.63, '98o': 48.13, '97o': 46.27, '96o': 44.47, '95o': 42.62, '94o': 40.59, '93o': 40.05, '92o': 39.12, '87o': 45.04, '86o': 43.22, '85o': 41.37, '84o': 39.47, '83o': 37.51, '82o': 36.8, '76o': 42.32, '75o': 40.48, '74o': 38.56, '73o': 36.68, '72o': 34.63, '65o': 39.92, '64o': 37.9, '63o': 36.09, '62o': 34.08, '54o': 38.21, '53o': 36.26, '52o': 34.3, '43o': 35.09, '42o': 33.28, '32o': 32.38},
    2: {'AA': 73.42, 'KK': 68.86, 'QQ': 64.99, 'JJ': 61.13, 'TT': 57.52, '99': 53.53, '88': 50.02, '77': 46.42, '66': 43.18, '55': 40.04, '44': 36.76, '33': 33.6, '22': 30.7, 'AKs': 50.73, 'AQs': 49.43, 'AJs': 48.2, 'ATs': 47.08, 'A9s': 44.6, 'A8s': 43.58, 'A7s': 42.38, 'A6s': 41.19, 'A5s': 41.39, 'A4s': 40.61, 'A3s': 39.7, 'A2s': 38.66, 'KQs': 47.24, 'KJs': 45.85, 'KTs': 44.82, 'K9s': 42.35, 'K8s': 40.14, 'K7s': 39.26, 'K6s': 38.25, 'K5s': 37.38, 'K4s': 36.46, 'K3s': 35.68, 'K2s': 34.83, 'QJs': 44.21, 'QTs': 43.11, 'Q9s': 40.69, 'Q8s': 38.55, 'Q7s': 36.52, 'Q6s': 35.76, 'Q5s': 34.87, 'Q4s': 34.01, 'Q3s': 33.24, 'Q2s': 32.46, 'JTs': 41.98, 'J9s': 39.37, 'J8s': 37.45, 'J7s': 35.36, 'J6s': 33.33, 'J5s': 32.75, 'J4s': 31.84, 'J3s': 31.18, 'J2s': 30.33, 'T9s': 38.71, 'T8s': 36.75, 'T7s': 34.66, 'T6s': 32.69, 'T5s': 30.72, 'T4s': 30.22, 'T3s': 29.42, 'T2s': 28.58, '98s': 35.97, '97s': 34.03, '96s': 32.08, '95s': 30.14, '94s': 28.4, '93s': 27.86, '92s': 27.12, '87s': 33.86, '86s': 32.0, '85s': 30.05, '84s': 28.11, '83s': 26.35, '82s': 25.79, '76s': 31.91, '75s': 30.15, '74s': 28.25, '73s': 26.4, '72s': 24.52, '65s': 30.31, '64s': 28.51, '63s': 26.64, '62s': 24.85, '54s': 29.06, '53s': 27.19, '52s': 25.38, '43s': 26.39, '42s': 24.69, '32s': 23.9, 'AKo': 48.11, 'AQo': 46.85, 'AJo': 45.45, 'ATo': 44.25, 'A9o': 41.47, 'A8o': 40.4, 'A7o': 39.28, 'A6o': 37.93, 'A5o': 38.14, 'A4o': 37.18, 'A3o': 36.22, 'A2o': 35.26, 'KQo': 44.36, 'KJo': 43.11, 'KTo': 41.84, 'K9o': 39.28, 'K8o': 36.99, 'K7o': 35.92, 'K6o': 34.94, 'K5o': 33.9, 'K4o': 32.96, 'K3o': 32.09, 'K2o': 31.13, 'QJo': 41.3, 'QTo': 40.19, 'Q9o': 37.52, 'Q8o': 35.26, 'Q7o': 33.08, 'Q6o': 32.29, 'Q5o': 31.3, 'Q4o': 30.33, 'Q3o': 29.55, 'Q2o': 28.55, 'JTo': 39.06, 'J9o': 36.32, 'J8o': 34.09, 'J7o': 32.03, 'J6o': 29.77, 'J5o': 29.07, 'J4o': 28.15, 'J3o': 27.34, 'J2o': 26.41, 'T9o': 35.65, 'T8o': 33.4, 'T7o': 31.26, 'T6o': 29.05, 'T5o': 27.11, 'T4o': 26.41, 'T3o': 25.59, 'T2o': 24.78, '98o': 32.69, '97o': 30.71, '96o': 28.58, '95o': 26.55, '94o': 24.5, '93o': 23.91, '92o': 23.06, '87o': 30.43, '86o': 28.42, '85o': 26.45, '84o': 24.41, '83o': 22.42, '82o': 21.85, '76o': 28.36, '75o': 26.49, '74o': 24.48, '73o': 22.52, '72o': 20.45, '65o': 26.72, '64o': 24.79, '63o': 22.81, '62o': 20.72, '54o': 25.31, '53o': 23.42, '52o': 21.54, '43o': 22.61, '42o': 20.64, '32o': 19.74},
    3: {'AA': 63.85, 'KK': 58.25, 'QQ': 53.53, 'JJ': 49.17, 'TT': 45.26, '99': 41.13, '88': 37.56, '77': 34.49, '66': 31.49, '55': 28.87, '44': 26.22, '33': 23.96, '22': 22.03, 'AKs': 41.57, 'AQs': 39.86, 'AJs': 38.45, 'ATs': 37.27, 'A9s': 34.54, 'A8s': 33.53, 'A7s': 32.34, 'A6s': 31.32, 'A5s': 31.71, 'A4s': 30.9, 'A3s': 30.16, 'A2s': 29.47, 'KQs': 38.23, 'KJs': 36.83, 'KTs': 35.6, 'K9s': 32.9, 'K8s': 30.75, 'K7s': 30.02, 'K6s': 29.1, 'K5s': 28.3, 'K4s': 27.55, 'K3s': 26.9, 'K2s': 26.25, 'QJs': 35.67, 'QTs': 34.59, 'Q9s': 31.89, 'Q8s': 29.69, 'Q7s': 27.66, 'Q6s': 27.08, 'Q5s': 26.22, 'Q4s': 25.58, 'Q3s': 24.89, 'Q2s': 24.27, 'JTs': 33.78, 'J9s': 31.27, 'J8s': 29.14, 'J7s': 27.08, 'J6s': 25.18, 'J5s': 24.62, 'J4s': 23.97, 'J3s': 23.27, 'J2s': 22.73, 'T9s': 30.87, 'T8s': 28.78, 'T7s': 26.93, 'T6s': 25.01, 'T5s': 23.16, 'T4s': 22.76, 'T3s': 22.13, 'T2s': 21.47, '98s': 28.46, '97s': 26.74, '96s': 24.79, '95s': 23.0, '94s': 21.36, '93s': 20.91, '92s': 20.33, '87s': 26.7, '86s': 24.93, '85s': 23.21, '84s': 21.46, '83s': 19.81, '82s': 19.39, '76s': 25.15, '75s': 23.42, '74s': 21.74, '73s': 20.09, '72s': 18.46, '65s': 23.72, '64s': 22.2, '63s': 20.49, '62s': 18.85, '54s': 22.69, '53s': 21.13, '52s': 19.53, '43s': 20.39, '42s': 18.88, '32s': 18.17, 'AKo': 38.58, 'AQo': 36.84, 'AJo': 35.28, 'ATo': 34.01, 'A9o': 31.11, 'A8o': 29.98, 'A7o': 28.76, 'A6o': 27.56, 'A5o': 27.97, 'A4o': 27.06, 'A3o': 26.3, 'A2o': 25.34, 'KQo': 35.14, 'KJo': 33.6, 'KTo': 32.39, 'K9o': 29.45, 'K8o': 27.07, 'K7o': 26.35, 'K6o': 25.26, 'K5o': 24.45, 'K4o': 23.57, 'K3o': 22.9, 'K2o': 22.1, 'QJo': 32.51, 'QTo': 31.33, 'Q9o': 28.39, 'Q8o': 26.03, 'Q7o': 23.99, 'Q6o': 23.27, 'Q5o': 22.38, 'Q4o': 21.53, 'Q3o': 20.86, 'Q2o': 20.13, 'JTo': 30.72, 'J9o': 27.91, 'J8o': 25.62, 'J7o': 23.35, 'J6o': 21.35, 'J5o': 20.78, 'J4o': 20.01, 'J3o': 19.31, 'J2o': 18.53, 'T9o': 27.64, 'T8o': 25.37, 'T7o': 23.21, 'T6o': 21.21, 'T5o': 19.29, 'T4o': 18.69, 'T3o': 18.05, 'T2o': 17.35, '98o': 25.06, '97o': 23.08, '96o': 21.04, '95o': 19.12, '94o': 17.35, '93o': 16.86, '92o': 16.14, '87o': 23.11, '86o': 21.26, '85o': 19.26, '84o': 17.45, '83o': 15.65, '82o': 15.21, '76o': 21.4, '75o': 19.61, '74o': 17.87, '73o': 16.06, '72o': 14.28, '65o': 20.05, '64o': 18.28, '63o': 16.47, '62o': 14.72, '54o': 18.85, '53o': 17.29, '52o': 15.38, '43o': 16.39, '42o': 14.75, '32o': 13.97},
    4: {'AA': 55.73, 'KK': 49.79, 'QQ': 44.68, 'JJ': 40.17, 'TT': 36.34, '99': 32.59, '88': 29.55, '77': 26.77, '66': 24.47, '55': 22.4, '44': 20.57, '33': 19.01, '22': 17.71, 'AKs': 35.45, 'AQs': 33.54, 'AJs': 32.19, 'ATs': 31.0, 'A9s': 28.35, 'A8s': 27.29, 'A7s': 26.33, 'A6s': 25.41, 'A5s': 25.99, 'A4s': 25.32, 'A3s': 24.71, 'A2s': 24.11, 'KQs': 32.45, 'KJs': 31.01, 'KTs': 29.97, 'K9s': 27.16, 'K8s': 25.18, 'K7s': 24.43, 'K6s': 23.62, 'K5s': 23.06, 'K4s': 22.33, 'K3s': 21.84, 'K2s': 21.36, 'QJs': 30.19, 'QTs': 29.03, 'Q9s': 26.4, 'Q8s': 24.39, 'Q7s': 22.63, 'Q6s': 21.96, 'Q5s': 21.29, 'Q4s': 20.67, 'Q3s': 20.23, 'Q2s': 19.71, 'JTs': 28.64, 'J9s': 26.02, 'J8s': 24.04, 'J7s': 22.15, 'J6s': 20.42, 'J5s': 19.99, 'J4s': 19.36, 'J3s': 18.87, 'J2s': 18.39, 'T9s': 26.0, 'T8s': 24.03, 'T7s': 22.21, 'T6s': 20.41, 'T5s': 18.81, 'T4s': 18.43, 'T3s': 17.93, 'T2s': 17.49, '98s': 23.61, '97s': 22.02, '96s': 20.41, '95s': 18.78, '94s': 17.22, '93s': 16.92, '92s': 16.35, '87s': 22.12, '86s': 20.55, '85s': 19.01, '84s': 17.48, '83s': 16.06, '82s': 15.59, '76s': 20.78, '75s': 19.37, '74s': 17.92, '73s': 16.34, '72s': 15.03, '65s': 19.69, '64s': 18.36, '63s': 16.9, '62s': 15.38, '54s': 18.95, '53s': 17.54, '52s': 16.17, '43s': 16.94, '42s': 15.63, '32s': 15.0, 'AKo': 32.36, 'AQo': 30.43, 'AJo': 28.88, 'ATo': 27.38, 'A9o': 24.57, 'A8o': 23.52, 'A7o': 22.43, 'A6o': 21.42, 'A5o': 21.99, 'A4o': 21.28, 'A3o': 20.63, 'A2o': 19.85, 'KQo': 29.33, 'KJo': 27.7, 'KTo': 26.52, 'K9o': 23.47, 'K8o': 21.28, 'K7o': 20.43, 'K6o': 19.51, 'K5o': 18.82, 'K4o': 18.23, 'K3o': 17.62, 'K2o': 17.16, 'QJo': 26.9, 'QTo': 25.64, 'Q9o': 22.79, 'Q8o': 20.59, 'Q7o': 18.57, 'Q6o': 17.88, 'Q5o': 17.21, 'Q4o': 16.54, 'Q3o': 16.01, 'Q2o': 15.41, 'JTo': 25.32, 'J9o': 22.54, 'J8o': 20.34, 'J7o': 18.33, 'J6o': 16.47, 'J5o': 15.9, 'J4o': 15.29, 'J3o': 14.7, 'J2o': 14.14, 'T9o': 22.53, 'T8o': 20.34, 'T7o': 18.33, 'T6o': 16.51, 'T5o': 14.77, 'T4o': 14.35, 'T3o': 13.79, 'T2o': 13.26, '98o': 20.0, '97o': 18.33, '96o': 16.53, '95o': 14.83, '94o': 13.14, '93o': 12.72, '92o': 12.15, '87o': 18.46, '86o': 16.84, '85o': 15.06, '84o': 13.44, '83o': 11.83, '82o': 11.51, '76o': 17.09, '75o': 15.46, '74o': 13.9, '73o': 12.29, '72o': 10.8, '65o': 15.93, '64o': 14.42, '63o': 12.8, '62o': 11.23, '54o': 14.99, '53o': 13.57, '52o': 12.05, '43o': 12.92, '42o': 11.54, '32o': 10.8},
    5: {'AA': 49.15, 'KK': 42.97, 'QQ': 37.87, 'JJ': 33.62, 'TT': 29.94, '99': 26.62, '88': 24.02, '77': 21.87, '66': 20.09, '55': 18.45, '44': 17.23, '33': 16.27, '22': 15.54, 'AKs': 31.03, 'AQs': 29.37, 'AJs': 27.8, 'ATs': 26.67, 'A9s': 24.22, 'A8s': 23.29, 'A7s': 22.36, 'A6s': 21.64, 'A5s': 22.19, 'A4s': 21.64, 'A3s': 21.23, 'A2s': 20.65, 'KQs': 28.31, 'KJs': 27.01, 'KTs': 25.84, 'K9s': 23.32, 'K8s': 21.3, 'K7s': 20.66, 'K6s': 19.99, 'K5s': 19.45, 'K4s': 18.92, 'K3s': 18.64, 'K2s': 18.25, 'QJs': 26.22, 'QTs': 25.21, 'Q9s': 22.62, 'Q8s': 20.78, 'Q7s': 19.06, 'Q6s': 18.58, 'Q5s': 17.98, 'Q4s': 17.63, 'Q3s': 17.18, 'Q2s': 16.7, 'JTs': 24.89, 'J9s': 22.34, 'J8s': 20.43, 'J7s': 18.88, 'J6s': 17.28, 'J5s': 16.89, 'J4s': 16.47, 'J3s': 16.03, 'J2s': 15.64, 'T9s': 22.4, 'T8s': 20.64, 'T7s': 18.91, 'T6s': 17.33, 'T5s': 15.96, 'T4s': 15.64, 'T3s': 15.22, 'T2s': 14.84, '98s': 20.28, '97s': 18.84, '96s': 17.31, '95s': 15.93, '94s': 14.66, '93s': 14.3, '92s': 13.97, '87s': 18.94, '86s': 17.62, '85s': 16.31, '84s': 14.83, '83s': 13.63, '82s': 13.34, '76s': 17.92, '75s': 16.69, '74s': 15.33, '73s': 13.94, '72s': 12.73, '65s': 17.05, '64s': 15.87, '63s': 14.57, '62s': 13.25, '54s': 16.5, '53s': 15.34, '52s': 14.02, '43s': 14.8, '42s': 13.62, '32s': 13.05, 'AKo': 27.83, 'AQo': 25.93, 'AJo': 24.36, 'ATo': 22.99, 'A9o': 20.25, 'A8o': 19.23, 'A7o': 18.27, 'A6o': 17.43, 'A5o': 18.06, 'A4o': 17.47, 'A3o': 16.96, 'A2o': 16.29, 'KQo': 25.01, 'KJo': 23.49, 'KTo': 22.31, 'K9o': 19.36, 'K8o': 17.41, 'K7o': 16.69, 'K6o': 15.9, 'K5o': 15.32, 'K4o': 14.76, 'K3o': 14.32, 'K2o': 13.86, 'QJo': 22.88, 'QTo': 21.69, 'Q9o': 18.87, 'Q8o': 16.83, 'Q7o': 15.0, 'Q6o': 14.35, 'Q5o': 13.86, 'Q4o': 13.35, 'Q3o': 12.92, 'Q2o': 12.49, 'JTo': 21.54, 'J9o': 18.69, 'J8o': 16.79, 'J7o': 14.83, 'J6o': 13.24, 'J5o': 12.77, 'J4o': 12.31, 'J3o': 11.78, 'J2o': 11.39, 'T9o': 18.91, 'T8o': 16.83, 'T7o': 15.05, 'T6o': 13.37, 'T5o': 11.93, 'T4o': 11.5, 'T3o': 11.02, 'T2o': 10.64, '98o': 16.58, '97o': 15.09, '96o': 13.47, '95o': 11.96, '94o': 10.49, '93o': 10.09, '92o': 9.74, '87o': 15.26, '86o': 13.85, '85o': 12.34, '84o': 10.8, '83o': 9.49, '82o': 9.13, '76o': 14.15, '75o': 12.82, '74o': 11.34, '73o': 9.94, '72o': 8.59, '65o': 13.24, '64o': 11.95, '63o': 10.56, '62o': 9.16, '54o': 12.67, '53o': 11.43, '52o': 10.02, '43o': 10.77, '42o': 9.58, '32o': 8.93},
    6: {'AA': 43.45, 'KK': 37.44, 'QQ': 32.55, 'JJ': 28.5, 'TT': 25.14, '99': 22.5, '88': 20.35, '77': 18.7, '66': 17.27, '55': 16.03, '44': 15.25, '33': 14.57, '22': 14.14, 'AKs': 27.73, 'AQs': 25.93, 'AJs': 24.62, 'ATs': 23.52, 'A9s': 21.07, 'A8s': 20.17, 'A7s': 19.49, 'A6s': 18.9, 'A5s': 19.48, 'A4s': 19.02, 'A3s': 18.64, 'A2s': 18.17, 'KQs': 25.12, 'KJs': 23.85, 'KTs': 22.84, 'K9s': 20.41, 'K8s': 18.59, 'K7s': 18.0, 'K6s': 17.46, 'K5s': 17.0, 'K4s': 16.61, 'K3s': 16.32, 'K2s': 15.93, 'QJs': 23.12, 'QTs': 22.17, 'Q9s': 19.81, 'Q8s': 18.1, 'Q7s': 16.62, 'Q6s': 16.11, 'Q5s': 15.7, 'Q4s': 15.35, 'Q3s': 15.0, 'Q2s': 14.74, 'JTs': 22.02, 'J9s': 19.58, 'J8s': 17.92, 'J7s': 16.4, 'J6s': 15.06, 'J5s': 14.67, 'J4s': 14.34, 'J3s': 14.05, 'J2s': 13.71, 'T9s': 19.8, 'T8s': 18.1, 'T7s': 16.58, 'T6s': 15.16, 'T5s': 13.91, 'T4s': 13.65, 'T3s': 13.28, 'T2s': 13.1, '98s': 17.83, '97s': 16.54, '96s': 15.22, '95s': 13.96, '94s': 12.7, '93s': 12.45, '92s': 12.19, '87s': 16.69, '86s': 15.55, '85s': 14.34, '84s': 12.96, '83s': 11.92, '82s': 11.64, '76s': 15.87, '75s': 14.8, '74s': 13.56, '73s': 12.39, '72s': 11.23, '65s': 15.24, '64s': 14.2, '63s': 12.97, '62s': 11.75, '54s': 14.82, '53s': 13.69, '52s': 12.54, '43s': 13.2, '42s': 12.17, '32s': 11.74, 'AKo': 24.45, 'AQo': 22.48, 'AJo': 20.89, 'ATo': 19.68, 'A9o': 17.08, 'A8o': 16.12, 'A7o': 15.38, 'A6o': 14.62, 'A5o': 15.25, 'A4o': 14.76, 'A3o': 14.31, 'A2o': 13.83, 'KQo': 21.81, 'KJo': 20.17, 'KTo': 19.12, 'K9o': 16.44, 'K8o': 14.6, 'K7o': 13.85, 'K6o': 13.2, 'K5o': 12.71, 'K4o': 12.3, 'K3o': 11.95, 'K2o': 11.6, 'QJo': 19.76, 'QTo': 18.61, 'Q9o': 15.99, 'Q8o': 14.13, 'Q7o': 12.49, 'Q6o': 11.98, 'Q5o': 11.47, 'Q4o': 11.06, 'Q3o': 10.77, 'Q2o': 10.42, 'JTo': 18.56, 'J9o': 15.94, 'J8o': 14.13, 'J7o': 12.47, 'J6o': 10.93, 'J5o': 10.6, 'J4o': 10.22, 'J3o': 9.81, 'J2o': 9.49, 'T9o': 16.17, 'T8o': 14.39, 'T7o': 12.74, 'T6o': 11.15, 'T5o': 9.89, 'T4o': 9.5, 'T3o': 9.11, 'T2o': 8.85, '98o': 14.17, '97o': 12.76, '96o': 11.33, '95o': 9.93, '94o': 8.63, '93o': 8.29, '92o': 8.04, '87o': 13.0, '86o': 11.74, '85o': 10.43, '84o': 9.06, '83o': 7.83, '82o': 7.56, '76o': 12.13, '75o': 11.02, '74o': 9.62, '73o': 8.38, '72o': 7.15, '65o': 11.45, '64o': 10.39, '63o': 9.08, '62o': 7.74, '54o': 10.98, '53o': 9.89, '52o': 8.7, '43o': 9.33, '42o': 8.25, '32o': 7.69},
    7: {'AA': 38.64, 'KK': 32.91, 'QQ': 28.3, 'JJ': 24.62, 'TT': 21.75, '99': 19.44, '88': 17.71, '77': 16.29, '66': 15.37, '55': 14.41, '44': 13.86, '33': 13.47, '22': 13.16, 'AKs': 24.95, 'AQs': 23.34, 'AJs': 22.05, 'ATs': 21.02, 'A9s': 18.74, 'A8s': 17.94, 'A7s': 17.37, 'A6s': 16.74, 'A5s': 17.32, 'A4s': 17.09, 'A3s': 16.74, 'A2s': 16.25, 'KQs': 22.6, 'KJs': 21.34, 'KTs': 20.31, 'K9s': 18.09, 'K8s': 16.55, 'K7s': 15.98, 'K6s': 15.5, 'K5s': 15.12, 'K4s': 14.89, 'K3s': 14.61, 'K2s': 14.34, 'QJs': 20.8, 'QTs': 19.89, 'Q9s': 17.68, 'Q8s': 16.02, 'Q7s': 14.64, 'Q6s': 14.23, 'Q5s': 13.94, 'Q4s': 13.58, 'Q3s': 13.41, 'Q2s': 13.15, 'JTs': 19.77, 'J9s': 17.48, 'J8s': 16.03, 'J7s': 14.52, 'J6s': 13.38, 'J5s': 13.07, 'J4s': 12.78, 'J3s': 12.6, 'J2s': 12.31, 'T9s': 17.68, 'T8s': 16.23, 'T7s': 14.78, 'T6s': 13.45, 'T5s': 12.39, 'T4s': 12.2, 'T3s': 11.84, 'T2s': 11.65, '98s': 15.98, '97s': 14.82, '96s': 13.58, '95s': 12.42, '94s': 11.37, '93s': 11.14, '92s': 10.92, '87s': 15.1, '86s': 14.04, '85s': 12.87, '84s': 11.67, '83s': 10.7, '82s': 10.5, '76s': 14.27, '75s': 13.4, '74s': 12.3, '73s': 11.1, '72s': 10.13, '65s': 13.83, '64s': 12.87, '63s': 11.77, '62s': 10.66, '54s': 13.5, '53s': 12.54, '52s': 11.46, '43s': 12.05, '42s': 11.11, '32s': 10.7, 'AKo': 21.59, 'AQo': 19.71, 'AJo': 18.23, 'ATo': 17.14, 'A9o': 14.62, 'A8o': 13.79, 'A7o': 13.1, 'A6o': 12.49, 'A5o': 13.09, 'A4o': 12.75, 'A3o': 12.39, 'A2o': 11.87, 'KQo': 19.08, 'KJo': 17.71, 'KTo': 16.66, 'K9o': 14.1, 'K8o': 12.43, 'K7o': 11.82, 'K6o': 11.26, 'K5o': 10.83, 'K4o': 10.46, 'K3o': 10.25, 'K2o': 9.95, 'QJo': 17.26, 'QTo': 16.27, 'Q9o': 13.82, 'Q8o': 12.08, 'Q7o': 10.61, 'Q6o': 10.19, 'Q5o': 9.73, 'Q4o': 9.42, 'Q3o': 9.15, 'Q2o': 8.89, 'JTo': 16.38, 'J9o': 13.8, 'J8o': 12.15, 'J7o': 10.62, 'J6o': 9.31, 'J5o': 8.97, 'J4o': 8.63, 'J3o': 8.36, 'J2o': 8.16, 'T9o': 14.18, 'T8o': 12.49, 'T7o': 10.97, 'T6o': 9.55, 'T5o': 8.35, 'T4o': 8.03, 'T3o': 7.78, 'T2o': 7.54, '98o': 12.38, '97o': 11.13, '96o': 9.78, '95o': 8.45, '94o': 7.35, '93o': 7.11, '92o': 6.83, '87o': 11.38, '86o': 10.35, '85o': 9.07, '84o': 7.8, '83o': 6.73, '82o': 6.47, '76o': 10.74, '75o': 9.69, '74o': 8.43, '73o': 7.23, '72o': 6.19, '65o': 10.16, '64o': 9.15, '63o': 7.92, '62o': 6.73, '54o': 9.76, '53o': 8.84, '52o': 7.65, '43o': 8.29, '42o': 7.32, '32o': 6.83},
    8: {'AA': 34.66, 'KK': 29.17, 'QQ': 24.9, 'JJ': 21.64, 'TT': 19.15, '99': 17.19, '88': 15.85, '77': 14.81, '66': 14.01, '55': 13.29, '44': 12.89, '33': 12.59, '22': 12.53, 'AKs': 22.71, 'AQs': 21.12, 'AJs': 19.93, 'ATs': 19.02, 'A9s': 16.89, 'A8s': 16.21, 'A7s': 15.62, 'A6s': 15.23, 'A5s': 15.74, 'A4s': 15.49, 'A3s': 15.19, 'A2s': 14.76, 'KQs': 20.4, 'KJs': 19.32, 'KTs': 18.5, 'K9s': 16.34, 'K8s': 14.79, 'K7s': 14.38, 'K6s': 13.99, 'K5s': 13.72, 'K4s': 13.4, 'K3s': 13.15, 'K2s': 13.04, 'QJs': 18.79, 'QTs': 18.08, 'Q9s': 15.88, 'Q8s': 14.47, 'Q7s': 13.25, 'Q6s': 12.89, 'Q5s': 12.61, 'Q4s': 12.34, 'Q3s': 12.12, 'Q2s': 11.97, 'JTs': 17.99, 'J9s': 15.84, 'J8s': 14.49, 'J7s': 13.1, 'J6s': 12.02, 'J5s': 11.8, 'J4s': 11.6, 'J3s': 11.41, 'J2s': 11.16, 'T9s': 16.1, 'T8s': 14.69, 'T7s': 13.41, 'T6s': 12.18, 'T5s': 11.18, 'T4s': 10.96, 'T3s': 10.8, 'T2s': 10.6, '98s': 14.47, '97s': 13.54, '96s': 12.38, '95s': 11.27, '94s': 10.27, '93s': 10.12, '92s': 9.88, '87s': 13.76, '86s': 12.8, '85s': 11.79, '84s': 10.71, '83s': 9.7, '82s': 9.52, '76s': 13.14, '75s': 12.35, '74s': 11.23, '73s': 10.21, '72s': 9.25, '65s': 12.78, '64s': 11.83, '63s': 10.85, '62s': 9.76, '54s': 12.45, '53s': 11.67, '52s': 10.55, '43s': 11.17, '42s': 10.3, '32s': 9.82, 'AKo': 19.22, 'AQo': 17.42, 'AJo': 16.12, 'ATo': 15.04, 'A9o': 12.76, 'A8o': 11.95, 'A7o': 11.35, 'A6o': 10.87, 'A5o': 11.47, 'A4o': 11.17, 'A3o': 10.83, 'A2o': 10.43, 'KQo': 16.94, 'KJo': 15.67, 'KTo': 14.76, 'K9o': 12.31, 'K8o': 10.73, 'K7o': 10.24, 'K6o': 9.75, 'K5o': 9.39, 'K4o': 9.14, 'K3o': 8.86, 'K2o': 8.7, 'QJo': 15.29, 'QTo': 14.42, 'Q9o': 12.03, 'Q8o': 10.51, 'Q7o': 9.14, 'Q6o': 8.74, 'Q5o': 8.38, 'Q4o': 8.13, 'Q3o': 7.91, 'Q2o': 7.7, 'JTo': 14.45, 'J9o': 12.14, 'J8o': 10.64, 'J7o': 9.19, 'J6o': 8.03, 'J5o': 7.71, 'J4o': 7.44, 'J3o': 7.22, 'J2o': 7.01, 'T9o': 12.55, 'T8o': 11.03, 'T7o': 9.6, 'T6o': 8.36, 'T5o': 7.24, 'T4o': 6.97, 'T3o': 6.72, 'T2o': 6.53, '98o': 10.89, '97o': 9.82, '96o': 8.61, '95o': 7.43, '94o': 6.34, '93o': 6.14, '92o': 5.95, '87o': 10.15, '86o': 9.18, '85o': 8.01, '84o': 6.83, '83o': 5.86, '82o': 5.6, '76o': 9.59, '75o': 8.69, '74o': 7.55, '73o': 6.37, '72o': 5.36, '65o': 9.2, '64o': 8.22, '63o': 7.12, '62o': 5.98, '54o': 8.87, '53o': 8.02, '52o': 6.86, '43o': 7.51, '42o': 6.66, '32o': 6.14},
    9: {'AA': 30.98, 'KK': 26.12, 'QQ': 22.19, 'JJ': 19.32, 'TT': 17.09, '99': 15.6, '88': 14.5, '77': 13.66, '66': 13.04, '55': 12.37, '44': 12.11, '33': 12.03, '22': 11.94, 'AKs': 20.69, 'AQs': 19.27, 'AJs': 18.2, 'ATs': 17.43, 'A9s': 15.35, 'A8s': 14.76, 'A7s': 14.29, 'A6s': 13.93, 'A5s': 14.46, 'A4s': 14.24, 'A3s': 13.95, 'A2s': 13.6, 'KQs': 18.7, 'KJs': 17.63, 'KTs': 16.86, 'K9s': 14.77, 'K8s': 13.56, 'K7s': 13.11, 'K6s': 12.79, 'K5s': 12.48, 'K4s': 12.28, 'K3s': 12.15, 'K2s': 11.89, 'QJs': 17.13, 'QTs': 16.58, 'Q9s': 14.58, 'Q8s': 13.16, 'Q7s': 12.07, 'Q6s': 11.79, 'Q5s': 11.54, 'Q4s': 11.36, 'Q3s': 11.08, 'Q2s': 10.99, 'JTs': 16.54, 'J9s': 14.57, 'J8s': 13.22, 'J7s': 12.03, 'J6s': 11.0, 'J5s': 10.75, 'J4s': 10.59, 'J3s': 10.39, 'J2s': 10.28, 'T9s': 14.8, 'T8s': 13.61, 'T7s': 12.33, 'T6s': 11.16, 'T5s': 10.3, 'T4s': 10.07, 'T3s': 9.91, 'T2s': 9.8, '98s': 13.4, '97s': 12.43, '96s': 11.41, '95s': 10.39, '94s': 9.44, '93s': 9.24, '92s': 9.09, '87s': 12.73, '86s': 11.92, '85s': 10.88, '84s': 9.83, '83s': 8.94, '82s': 8.74, '76s': 12.28, '75s': 11.49, '74s': 10.4, '73s': 9.32, '72s': 8.54, '65s': 11.86, '64s': 11.07, '63s': 10.02, '62s': 9.03, '54s': 11.65, '53s': 10.83, '52s': 9.77, '43s': 10.39, '42s': 9.57, '32s': 9.18, 'AKo': 17.11, 'AQo': 15.54, 'AJo': 14.23, 'ATo': 13.37, 'A9o': 11.2, 'A8o': 10.55, 'A7o': 9.94, 'A6o': 9.52, 'A5o': 10.16, 'A4o': 9.82, 'A3o': 9.6, 'A2o': 9.22, 'KQo': 15.15, 'KJo': 13.99, 'KTo': 13.12, 'K9o': 10.86, 'K8o': 9.42, 'K7o': 8.91, 'K6o': 8.56, 'K5o': 8.26, 'K4o': 8.0, 'K3o': 7.85, 'K2o': 7.62, 'QJo': 13.61, 'QTo': 12.91, 'Q9o': 10.71, 'Q8o': 9.24, 'Q7o': 8.03, 'Q6o': 7.62, 'Q5o': 7.4, 'Q4o': 7.16, 'Q3o': 6.96, 'Q2o': 6.78, 'JTo': 13.09, 'J9o': 10.9, 'J8o': 9.44, 'J7o': 8.1, 'J6o': 7.05, 'J5o': 6.75, 'J4o': 6.53, 'J3o': 6.36, 'J2o': 6.22, 'T9o': 11.31, 'T8o': 9.88, 'T7o': 8.53, 'T6o': 7.36, 'T5o': 6.34, 'T4o': 6.14, 'T3o': 5.92, 'T2o': 5.8, '98o': 9.87, '97o': 8.84, '96o': 7.72, '95o': 6.56, '94o': 5.58, '93o': 5.33, '92o': 5.21, '87o': 9.17, '86o': 8.3, '85o': 7.24, '84o': 6.1, '83o': 5.14, '82o': 4.96, '76o': 8.71, '75o': 7.91, '74o': 6.83, '73o': 5.77, '72o': 4.79, '65o': 8.46, '64o': 7.56, '63o': 6.47, '62o': 5.4, '54o': 8.23, '53o': 7.37, '52o': 6.31, '43o': 6.89, '42o': 6.04, '32o': 5.61}
}

vs_dict = {"UTG": 7, "UTG1": 6, "LJ": 5, "HJ": 4, "CO": 3, "BTN": 2, "SB": 1}

cell_size = 25

paint_bar_size = int(cell_size / 12)

cell_inner_size = cell_size - 1

matrix_size = 13

ranks = "AKQJT98765432"
suits = "shdc"

suit_dict = {"s": "♠", "h": "♥", "d": "♦", "c": "♣"}
suit_color = {"s": "black", "h": "red", "d": "red", "c": "black"}

combos_matrix = [[f"{r_1}{r_2}" if i == j else f"{r_1}{r_2}s" if i < j else f"{r_2}{r_1}o" for j, r_2 in enumerate(ranks)] for i, r_1 in enumerate(ranks)]

position_name_change = {"UTG": "EP", "UTG1": "MP", "LJ": "LJ", "HJ": "HJ", "CO": "CO", "BTN": "BU", "SB": "SB", "BB": "BB"}

positions = list(position_name_change.keys())

rev_position_name_change = {v: k for k, v in position_name_change.items()}

action_name_change = {"Call": "C", "Check": "C", "Raise": "R", "Allin": "A", "Fold": "F"}

color_data = { # call color 20% S in HSV BB+BU+CO R -10% V in HSV
    "UTG": ['#FFFFFF', '#ffcccc', '#ff0000', '#bf0000', '#800000', '#400000', '#ffff00'],
    "UTG1": ['#FFFFFF', '#ffe7cc', '#ff8000', '#bf6000', '#804000', '#402000', '#ffff00'],
    "LJ": ['#FFFFFF', '#e7ccff', '#8000ff', '#6000bf', '#400080', '#200040', '#ffff00'],
    "HJ": ['#FFFFFF', '#ffccff', '#ff00ff', '#bf00bf', '#800080', '#400040', '#ffff00'],
    "CO": ['#FFFFFF', '#ccffe7', '#00e673', '#00a653', '#006633', '#002613', '#ffff00'],
    "BTN": ['#FFFFFF', '#edffcc', '#99e600', '#6fa600', '#446600', '#1a2600', '#ffff00'],
    "SB": ['#FFFFFF', '#cce7ff', '#0080ff', '#0060bf', '#004080', '#002040', '#ffff00'],
    "BB": ['#FFFFFF', '#ccffff', '#00e6e6', '#00a6a6', '#006666', '#002626', '#ffff00'],
}



def sort_key(combo: str, combo_results: list[str, list[dict[str, float]]], spot_non_fold_most_frequent_actions: list[str], vs: int) -> tuple[float]:
    result = []
    if not combo_results:
        result.append(-1000)
        result.append(equity_vs[vs][combo])

        return result
    actions_dict = combo_results[1]
    for spot_action in spot_non_fold_most_frequent_actions:
        result.append(actions_dict[spot_action][1])
        result.append(actions_dict[spot_action][0])
    result.append(equity_vs[vs][combo])
    
    return result


def normalize_float(num: float, decimals: int = 2) -> float | int:
    try:
        num = float(num)
    except:
        print(f'NUM_var must be a integer or float {num}')

        return 0
    if num.is_integer():

        return int(num)
    
    return round(num, decimals)


def get_data(depth, spot_position, spot, villain_position, folder):
   
    
    for path in Path(folder).iterdir():
        if not path.is_file():

            continue
        file_extension = str(path).removeprefix(f"{folder}\\")
        file_name = file_extension.removesuffix(".json")
        if f"_{depth}bb_" not in file_name:

            continue
        with open(path, "r", encoding="utf-8") as f:
            data_temp = json.load(f)
        if villain_position and villain_position != "None":
            data = data_temp[spot_position][spot][villain_position]
        else:

            data = data_temp[spot_position][spot]
        mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict = data

    return mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict


def parse_spot(mode_depth, positions_actions, actions_frequencies, combos_dict):
    spot_sequency = {}
    for index, positon_action_tuple in enumerate(positions_actions):
        position, immediate_stack, action_choosed, avaliable_actions = positon_action_tuple
        if action_choosed not in ["N/A", "Fold"]:
            spot_sequency[index + 1] = {position: action_choosed}
    spot_position = None
    spot_string = ""
    vs = None
    positions_acted = []
    mode_str = ""
    try:
        game_mode, chip_mode, depth = mode_depth
        mode_str = f"{game_mode} {chip_mode} {depth}"
    except:
        game_mode, chip_mode, depth, limp = mode_depth
        mode_str = f"{game_mode} {chip_mode} {depth} {limp}"

    for i, (k, v) in enumerate(spot_sequency.items()):
        for position_str, action in v.items():
            position = position_str.split(" ")[0]
            if i == 0 and action == "spot":
                spot_string += f"| {position} RFI |"
                spot_position = position
                vs = vs_dict[position]

                break
            if action == "spot":
                spot_position = position
                spot_string = f"| {position} vs |" + spot_string
                if spot_position in positions_acted:
                    vs = len([p for p in positions_acted if p != spot_position])
                else:
                    vs = len(positions_acted) if spot_position == "BB" else len(positions_acted) + vs_dict[spot_position]
            else:
                spot_string += f" {position} {action} |"
                positions_acted.append(position)
    spot_actions = [action_tuple[0].strip() for action_tuple in actions_frequencies]
    spot_most_frequent_actions = [action_tuple[0].strip() for action_tuple in sorted(actions_frequencies, key=lambda x: x[1], reverse=True)]
    spot_non_fold_most_frequent_actions = [action for action in spot_most_frequent_actions if action != "Fold"]
    sorted_combos_dict = dict(sorted(combos_dict.items(), key=lambda item: sort_key(item[0], item[1], spot_non_fold_most_frequent_actions, vs), reverse=True))
    combos_order = list(sorted_combos_dict.keys())
    spot_total_ev = 0
    spot_max_ev = 0
    max_ev_combo = ""
    prefolded_combos = []
    for combo, data in sorted_combos_dict.items():
        if not data:
            prefolded_combos.append(combo)
        else:
            combo_ev_max = max(normalize_float(v[1]) for k, v in data[1].items() if k != "Fold")
            if combo_ev_max >= 0:
                if combo_ev_max > spot_max_ev:
                    spot_max_ev = combo_ev_max
                    max_ev_combo = combo
                spot_total_ev += combo_ev_max
    spot_total_ev = round(spot_total_ev, 2)

    return mode_str, spot_string, spot_position, spot_actions, combos_order, prefolded_combos, spot_max_ev, spot_total_ev


def parse_data(mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict):
    try:
        game_mode, chip_mode, depth = mode_depth
    except:
        game_mode, chip_mode, depth, limp = mode_depth
    spot_sequency = {}
    original_spot_position = None
    spot_raise_actions = []
    for index, positon_action_tuple in enumerate(positions_actions):
        position, immediate_stack, action_choosed, avaliable_actions = positon_action_tuple

        if action_choosed == "spot":
            original_spot_position = position
            spot_raise_actions = [action for action in avaliable_actions if "Raise" in action]
        if action_choosed not in ["N/A", "Fold"]:
            spot_sequency[index + 1] = {position: action_choosed}

            if "Raise" in action_choosed:
                raise_actions = [action for action in avaliable_actions if "Raise"  in action]
                raise_actions = raise_actions[::-1]
                index = raise_actions.index(action_choosed)
    spot_actions_text_colors = [[f"{depth:>3}", '#000000', '#ffffff']]
    spot_position = position_name_change[original_spot_position]
    for index, data in enumerate(spot_sequency.values()):
        for position, action in data.items():
            if action == "spot":
                text_color = "#ffffff" if position in ["LJ", "SB"] else "#000000"
                bg_color = color_data[original_spot_position][2]
                if index == 0:
                    action_string = f"{spot_position} oR"
                    spot_actions_text_colors.append([action_string, text_color, bg_color])
                else:
                    action_string = f"{spot_position} vs"
                    spot_actions_text_colors.insert(1, [action_string, text_color, bg_color])
            else:
                if action.startswith("R"):
                    position_actions_tuple = [next(t for t in positions_actions if t[0] == position)][0]
                    actions_in_tuple = position_actions_tuple[3]
                    position_raise_actions = []
                    for act in actions_in_tuple:
                        if act.startswith("R"):
                            position_raise_actions.append(act)
                    action_name_part, action_size_part = action.split(" ")
                    raise_idx = position_raise_actions[::-1].index(action)
                    bg_color = color_data[position][2 + raise_idx]
                    text_color = "#ffffff" if position in ["LJ", "SB"] or raise_idx > 1 else "#000000"
                    action_string = f"{position_name_change[position]} {action_name_change[action_name_part]}{action_size_part}"
                    spot_actions_text_colors.append([action_string, text_color, bg_color])
                elif action.startswith("C"):
                    text_color = "#000000"
                    bg_color = color_data[original_spot_position][1]
                    action_string = f"{position_name_change[position]} {action_name_change[action]}"
                    spot_actions_text_colors.append([action_string, text_color, bg_color])
                elif action.startswith("A"):
                    action_name_part, action_size_part = action.split(" ")
                    text_color = "#000000"
                    bg_color = color_data[original_spot_position][6]
                    action_string = f"{position_name_change[position]} {action_name_change[action_name_part]}"
                    spot_actions_text_colors.append([action_string, text_color, bg_color])
    spot_actions_text_colors.append(["*", "#ffffff", "#000000"])
    try:
        min_action_freq_tuple = min((action for action in actions_frequencies if action[0] != "Fold" and action[1] > 1), key=lambda x: x[1])
    except:
        min_action_freq_tuple = min((action for action in actions_frequencies if action[0] != "Fold"), key=lambda x: x[1])
    min_action_freq  = min_action_freq_tuple[1]
    sorted_actions_frequencies = sorted(actions_frequencies, key= lambda x: x[1], reverse=True)
    spot_most_frequent_actions = []
    spot_most_frequent_nonfold_actions = []
    for action_tuple in sorted_actions_frequencies: 
        action, freq, num_combos, rgb = action_tuple
        if action != "Fold":
            spot_most_frequent_nonfold_actions.append(action)
        spot_most_frequent_actions.append(action)
        if freq > 0:
            if action.startswith("R"):
                action_name_part, action_size_part = action.split(" ")
                raise_idx = spot_raise_actions[::-1].index(action)
                bg_color = color_data[position][2 + raise_idx]
                text_color = "#ffffff" if position in ["LJ", "SB"] or raise_idx > 1 else "#000000"
                action_string = f"{action_name_change[action_name_part]}{action_size_part}: {freq}"
                percent = freq / min_action_freq
                spot_actions_text_colors.append([action_string, text_color, bg_color, percent])
            elif action.startswith("C"):
                text_color = "#000000"
                bg_color = color_data[original_spot_position][1]
                action_string = f"{action_name_change[action]}: {freq}"
                percent = freq / min_action_freq
                spot_actions_text_colors.append([action_string, text_color, bg_color, percent])
            elif action.startswith("A"):
                action_name_part, action_size_part = action.split(" ")
                text_color = "#000000"
                bg_color = color_data[original_spot_position][6]
                action_string = f"{action_name_change[action_name_part]}: {freq}"
                percent = freq / min_action_freq
                spot_actions_text_colors.append([action_string, text_color, bg_color, percent])
            elif action.startswith("F"):
                text_color = "#000000"
                bg_color = "#ffffff"
                action_string = f"{action_name_change[action]}: {freq}"
                percent = freq / min_action_freq
                spot_actions_text_colors.append([action_string, text_color, bg_color, percent])
    vs = len(set(v for d in spot_sequency.values() for v in d.keys() if original_spot_position not in v))
    vs = vs_dict[original_spot_position] if vs == 0 else vs
    sorted_combos = dict(sorted(combos_dict.items(), key=lambda item: sort_key(item[0], item[1], spot_most_frequent_nonfold_actions, vs), reverse=True))
    combos_order = list(dict(sorted_combos).keys())
    combo_colors_info_dict = {}
    fold_combos = []
    total_bars_to_paint = int(cell_inner_size / paint_bar_size)
    share = 100 / total_bars_to_paint
    for combo, data in combos_dict.items():
        if not data:
            continue
        ev_max_label, actions_dict = data
        combo_most_frequent_actions = sorted(actions_dict, key=lambda action: actions_dict[action][0], reverse=True)
        combo_most_frequent_non_fold_actions = sorted((action for action in actions_dict if action != "Fold"), key=lambda action: actions_dict[action][0], reverse=True)
        colors_info = []
        has_play_freq = False
        has_ev = False
        remaining_bars_to_paint = int(cell_inner_size / paint_bar_size)
        for action in combo_most_frequent_actions:
            freq = actions_dict[action][0]
            ev = actions_dict[action][1]
            if freq > 0:
                if action.startswith("R"):
                    if ev > 0: has_ev = True
                    has_play_freq = True
                    raise_idx = spot_raise_actions[::-1].index(action)
                    color = color_data[position][2 + raise_idx]
                    bars_to_paint = int((freq * total_bars_to_paint) / 100)
                    remaining_bars_to_paint -= bars_to_paint
                    spread = ((bars_to_paint + 1) * share) - freq
                    colors_info.append([color, bars_to_paint, spread])
                elif action.startswith("C"):
                    if ev > 0: has_ev = True
                    has_play_freq = True
                    color = color_data[position][1]
                    bars_to_paint = int((freq * total_bars_to_paint) / 100)
                    remaining_bars_to_paint -= bars_to_paint
                    spread = ((bars_to_paint + 1) * share) - freq
                    colors_info.append([color, bars_to_paint, spread])
                elif action.startswith("A"):
                    if ev > 0: has_ev = True
                    has_play_freq = True
                    color = color_data[position][6]
                    bars_to_paint = int((freq * total_bars_to_paint) / 100)
                    remaining_bars_to_paint -= bars_to_paint
                    spread = ((bars_to_paint + 1) * share) - freq
                    colors_info.append([color, bars_to_paint, spread])
                elif action.startswith("F"):
                    color = color_data[position][0]
                    bars_to_paint = int((freq * total_bars_to_paint) / 100)
                    remaining_bars_to_paint -= bars_to_paint
                    spread = ((bars_to_paint + 1) * share) - freq
                    colors_info.append([color, bars_to_paint, spread])
        while remaining_bars_to_paint:
            choosed = min(colors_info, key=lambda x: x[2])
            choosed[1] += 1
            choosed[2] = 100
            remaining_bars_to_paint -= 1
        
        if not has_play_freq:
            fold_combos.append(combo)

        fold_tiles = 0
        for color_paint_list in colors_info:
            if color_paint_list[0] == "#FFFFFF":
                fold_tiles = color_paint_list[1]
                break
        
        need_info = None
        if has_play_freq and fold_tiles == total_bars_to_paint:
            act = combo_most_frequent_non_fold_actions[0]
            if act.startswith("R"):
                act_name, act_size = act.split(" ")
                need_info = f"{act_name[0]}{normalize_float(act_size, 1)}"
            else:
                need_info = f"{act[0]}"

        colors_info = [ls for ls in colors_info if ls[1] > 0]

        combo_colors_info_dict[combo] = colors_info, (need_info, has_play_freq, has_ev)
    
    fold_combos_final = [c for c in combos_order if c in fold_combos]

    return combo_colors_info_dict, spot_actions_text_colors, combos_order, fold_combos_final


def draw_red_black_line(x: int, y: int, img: Image):
    draw = ImageDraw.Draw(img)
    for i in range(24):
        if i % 2 == 0:
            draw.point((x, y + i), "#ff0000")
        else:
            draw.point((x, y + i), "#000000")


def draw_yellow_black_line(x: int, y: int, img: Image):
    draw = ImageDraw.Draw(img)
    for i in range(24):
        if i % 2 == 0:
            draw.point((x, y + i), "#ffff00")
        else:
            draw.point((x, y + i), "#000000")


def get_text_boundaries(text: str, font: tuple) -> tuple[int]:
    text_len = len(text)
    img_size = text_len * 11
    img = Image.new("RGB", (img_size, int(img_size / 3)), "#ffffff")
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    return width, height


def draw_proof_chart(combo_colors_info_dict, spot_actions_text_colors, combos_order, fold_combos):
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
    
    x_i = 0
    for part in spot_actions_text_colors:
        text = part[0]
        text_color = part[1]
        bg_color =  part[2]
        percent = None
        try:
            percent = part[3]
        except:
            pass
        text_width, text_height = get_text_boundaries(text, title_font)
        draw.rectangle((x_i + 2, y - 1, (x_i + 2) + text_width, (y - 1) + title_bar_height), fill=bg_color, outline=None)
        draw.text((x_i + 2, y - 1), text, font=title_font, fill=text_color)
        if percent:
            x_i += text_width + 1
            percent = str(round(percent))
            percent_width, percent_height = get_text_boundaries(percent, title_font)
            draw.rectangle((x_i + 2, y - 1, (x_i + 2) + percent_width, (y - 1) + title_bar_height), fill="#5f6661", outline=None)
            draw.text((x_i + 2, y - 1), percent, font=title_font, fill="#ffffff")
            x_i += percent_width + 2
        else:
            x_i += text_width + 2
    draw.rectangle((x, y, chart_width, title_bar_height), outline="#000000")
    for row in range(matrix_size):
        for col in range(matrix_size):
            x_1 = (cell_size * col)
            y_1 = title_bar_height + (cell_size * row)
            x_2 = x_1 + cell_size
            y_2 = y_1 + cell_size
            combo = combos_matrix[row][col]
            x_i = x_1
            need_info, has_play_freq, has_ev = None, False, False
            try:
                colors_parts = combo_colors_info_dict[combo]
                for part in colors_parts:
                    if isinstance(part, list):
                        for i, part_rgb in enumerate(part):
                            color = part_rgb[0]
                            pixels_to_paint = part_rgb[1] * paint_bar_size
                            draw.rectangle((x_i + 1, y_1, x_i + pixels_to_paint, y_2), fill=color, outline=None)
                            colors_sequency_size = len(colors_parts[0])
                            if color == "#FFFFFF":
                                if i == 0 and colors_sequency_size > 1:
                                    draw_red_black_line(x_i + pixels_to_paint, y_1 + 1, chart)
                                if i == colors_sequency_size - 1 and colors_sequency_size > 1:
                                    draw_yellow_black_line(x_i + 1, y_1 + 1, chart)
                                if 0 < i < colors_sequency_size - 1:
                                    draw_red_black_line(x_i + pixels_to_paint, y_1 + 1, chart)
                                    draw_yellow_black_line(x_i + 1, y_1 + 1, chart)
                            x_i += pixels_to_paint

                    elif isinstance(part, tuple):
                        need_info = part[0]
                        has_play_freq = part[1]
                        has_ev = part[2]
            except:
                pass
            
            combo_text_color = "#000000" if has_ev else "#737373" if has_play_freq else "#d9d9d9"

            if need_info:
                need_info_width, need_info_height = get_text_boundaries(need_info, idx_font)
                draw.text((x_1 + 1 + (cell_size - need_info_width) // 2, y_1 - 1), font=idx_font, text=need_info, fill=combo_text_color)

            combo_rank = str(combos_order.index(combo) + 1)
            combo_rank_width, combo_rank_height = get_text_boundaries(combo_rank, idx_font)
            combo_rank_color = "#a6a6a6" if combo_text_color == "#d9d9d9" else combo_text_color
            draw.text((x_1 + (cell_size - combo_rank_width), y_1 - 2 + (cell_size - 6)), combo_rank, fill=combo_rank_color, font=idx_font)

            if combo in fold_combos:
                folded_combo_rank = str(fold_combos.index(combo) + 1)
                draw.text((x_1 + 1, y_1 - 1), folded_combo_rank, fill="#000000", font=idx_font)

            combo_width, combo_height = get_text_boundaries(combo, matrix_font)
            combo_x = x_1 + ((cell_size - combo_width) // 2) + 1
            combo_y = y_1 + ((cell_size - combo_height) // 2) - 2
            if "Q" in combo:
                draw.text((combo_x, combo_y + 1), combo, font=matrix_font, fill=combo_text_color)
            else:
                draw.text((combo_x, combo_y), combo, font=matrix_font, fill=combo_text_color)

            draw.rectangle((x_1, y_1, x_2, y_2), outline="#000000")

    return chart
