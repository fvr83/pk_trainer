import random
import math
import time


def get_time_string(seconds: float, round_decimals: int = 2, t_print: bool = False) -> str:
    string = ''
    years = int(seconds // 31104000)
    if years: string += f'{years}y '
    seconds %= 31104000
    months = int(seconds // 2592000)
    if months: string += f'{months}m '
    seconds %= 2592000
    days = int(seconds // 86400)
    if days: string += f'{days}d '
    seconds %= 86400
    hours = int(seconds // 3600)
    if hours: string += f'{hours}h '
    seconds %= 3600
    minutes = int(seconds // 60)
    if minutes: string += f'{minutes}m '
    seconds = round(seconds % 60, round_decimals)
    string += f'{seconds}s'
    if t_print: print(f'TIME STRING: {string}')

    return string


def get_right_action_by_frequency(combo_info: dict[str, list[int | float]]):
    # print(f'{combo_info = }')
    sorted_dict = dict(sorted(((k, v) for k, v in combo_info.items() if v[0] > 0), key=lambda item: (item[1][0], -item[1][1])))
    # print(f'{sorted_dict = }')
    freq_ranges = []
    accumulated = 0
    last_freq = 0
    for v in sorted_dict.values():
        freq = v[0]
        freq_ranges.append([accumulated + freq, last_freq - freq if last_freq == freq else last_freq, freq])
        accumulated += freq
        last_freq = freq
    # print(f'{freq_ranges = }')
    rng = round(random.random() * accumulated, 2)
    # print(f'{rng = }')
    freq_ranges[-1][-1] = 100.0
    right_action = None
    right_action_freq = None
    right_action_ev = None
    low_rng = None
    high_rng = None
    for i, ls in enumerate(freq_ranges):
        if ls[0] >= rng:
            act_tuple = list(sorted_dict.items())[i]
            right_action = act_tuple[0]
            right_action_freq = act_tuple[1][0]
            right_action_ev = act_tuple[1][1]
            low_rng = ls[1]
            high_rng = ls[2]

            break
    if high_rng - low_rng >= 2:
        final_rng = random.randint(math.ceil(low_rng), math.floor(high_rng))
    else:
        final_rng = math.floor(high_rng)
    # print(f'{right_action = }')
    # print(f'{final_rng = }')

    return right_action, right_action_freq, right_action_ev, final_rng


def get_right_action_evenly(combo_info: dict[str, list[int | float]]):
    all_in = []
    raises = []
    call_check = []
    fold = []
    for action, (freq, ev) in combo_info.items():
        if freq > 0:
            match action[0]:
                case 'A':
                    all_in.append(action)
                case 'R':
                    raises.append(action)
                case 'C':
                    call_check.append(action)
                case 'F':
                    fold.append(action)
    raises.sort(key=lambda x: x.split(' ')[1], reverse=True)
    actions = all_in + raises + call_check + fold
    # print(f'{actions = }')
    rng = random.randint(1, 100)
    # print(f'{rng = }')
    idx = (rng - 1) // int(100 // len(actions))
    # print(f'{idx = }')
    right_action = actions[idx]
    # print(f'{right_action = }')

    return right_action, rng

def get_playable_any_ev_action(combo_info: dict[str, list[int | float]]):
    rng = 100
    right_actions = tuple()
    for action, (freq, ev) in combo_info.items():
        if freq > 0:
            right_actions += (action, )
    print(right_actions)
    return right_actions, rng





def main() -> None:
    combo_info = {'Allin 50': [10, -2.03], 'Raise 2': [30.5, 0.1], 'Call': [49.5, 0.1], 'Fold': [10, 0]}
    # combo_info = {'Allin 50': [10, 0], 'Raise 2': [30.5, 0.1], 'Call': [49.5, 0.1], 'Fold': [10, 0]}
    # combo_info = {'Allin 50': [11, -2.03], 'Raise 2': [30.5, 0.1], 'Call': [49.5, 0.1], 'Fold': [9, 0]}
    # combo_info = {'Allin 50': [5, -2.03], 'Raise 2': [40.5, 0.1], 'Raise 3': [5, 0.05], 'Call': [49.5, 0.1], 'Fold': [0, 0]}

    # results_dict = {k: 0 for k in combo_info.keys()}
    # iterations = 10_000_000
    # t_start = time.time()
    # for _ in range(iterations):
    #     right_action, right_action_freq, right_action_ev, final_rng = get_right_action_by_frequency(combo_info)
    #     for k, v in combo_info.items():
    #         if k == right_action:
    #             results_dict[k] += 1
    # results_dict = {k: round(v / iterations * 100, 2) for k, v in results_dict.items()}
    # t_elapsed = time.time() - t_start
    # print()
    # print('ITERATIONS:', f'{iterations:_}')
    # print(f'{"EXPECTED":>12} {"ACHIEVED":>12}')
    # for k, v in results_dict.items():
    #     print(f'{combo_info[k][0]:>12} {v:>12}')
    # print()
    # print("TIME ELAPSED:", get_time_string(t_elapsed))

    # results_dict = {k: 0 for k in combo_info.keys()}
    # iterations = 10_000_000
    # t_start = time.time()
    # for _ in range(iterations):
    #     right_action = get_right_action_evenly(combo_info)
    #     for k, v in combo_info.items():
    #         if k == right_action:
    #             results_dict[k] += 1
    # results_dict = {k: round(v / iterations * 100, 2) for k, v in results_dict.items()}
    # t_elapsed = time.time() - t_start
    # print()
    # print('ITERATIONS:', f'{iterations:_}')
    # print(f'{"ACHIEVED":>12}')
    # for k, v in results_dict.items():
    #     print(f'{v:>12}')
    # print()
    # print("TIME ELAPSED:", get_time_string(t_elapsed))
    get_playable_any_ev_action(combo_info)



if __name__ == "__main__":
    main()
