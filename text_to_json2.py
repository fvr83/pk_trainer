from pathlib import Path
import ast
import json


folder = "text_results"
num_files = sum(1 for item in Path(folder).iterdir() if item.is_file())
print(f"{num_files = }\n")

for path in Path(folder).iterdir():
    if not path.is_file():
        
        continue
    result = dict()
    with open(path, "r", encoding="utf-8") as f:
        file_extension = str(path).removeprefix(f"{folder}\\")
        file_name = file_extension.removesuffix(".txt")
        # print(file_name)
        content = f.read()
        # print(content)
    if "_16bb" not in file_name:
        
        continue
    limp = None
    try:
        gap_ac, tier_ac, eff_stack, game_type, game_mode, limp = file_name.split("_")
    except:
        gap_ac, tier_ac, eff_stack, game_type, game_mode, = file_name.split("_")
    # print(f"{gap_ac = }")
    # print(f"{tier_ac = }")
    # print(f"{eff_stack = }")
    # print(f"{game_type = }")
    # print(f"{game_mode = }")
    # print(f"{limp = }")
    # print("-" * 20)

    blocks = content.split("**************************************************")
    for i, block in enumerate(blocks):
        if not block.strip():

            continue
        mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict = None, None, None, None, None
        for line in block.strip().splitlines():
            if "=" in line:
                name, value = line.split("=", 1)
                name = name.strip()
                value = ast.literal_eval(value.strip())
                globals()[name] = value
        # print(f"{mode_depth = }")
        # print(f"{positions_actions = }")
        # print(f"{pot_odds_and_stacks = }")
        # print(f"{actions_frequencies = }")
        # print(f"{combos_dict = }")
        # print("-" * 20)
        
        spot_position = None
        spot_sequency = {}
        for index, positon_action_tuple in enumerate(positions_actions):
            position, immediate_stack, action_choosed, avaliable_actions = positon_action_tuple
            if action_choosed == "spot":
                spot_position = position
            if action_choosed not in ["N/A", "Fold"]:
                spot_sequency[index + 1] = {position: action_choosed}
        # print(f"{spot_position = }")
        
        result.setdefault(spot_position, dict())

        villain_position = None
        spot = ""
        raise_size = None
        raise_sizes = ["low", "low-med", "med", "med-high", "high", "super", "ultra"]
        for i, (k, position_dict) in enumerate(spot_sequency.items()):
            for position, action in position_dict.items():
                if i == 0:
                    if action == "spot":
                        spot = "rfi"
                        result[spot_position][spot] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
                    elif position == spot_position:
                        if action.startswith("C"):
                            spot = "vs_limp"
                    elif position != spot_position:
                        villain_position = position
                        if action.startswith("Allin"):
                            spot = "vs_open_shove"
                            result[spot_position].setdefault(spot, dict())
                            result[spot_position][spot][villain_position] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
                        elif action.startswith("C"):
                            # print(spot_sequency)
                            # print("VS_LIMP SET")
                            spot = "vs_limp"
                            result[spot_position].setdefault(spot, dict())
                            result[spot_position][spot][villain_position] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
                        else:
                            spot = "vs_rfi"
                            result[spot_position].setdefault(spot, dict())
                            result[spot_position][spot][villain_position] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
                            action_tuple = tuple(t[3] for t in positions_actions if t[0] == position)[0]
                            raise_actions = sorted((a for a in action_tuple if a.startswith("Raise")),key=lambda x: float(x.split()[1]))
                            raise_size = raise_sizes[raise_actions.index(action)]
                elif i == 1:
                    if action != "spot":
                        villain_position = position
                        if action.startswith("Allin"):
                            if spot == "vs_limp":
                                spot = "vs_raise_ai"
                            else:
                                spot  = "vs_3bet_ai"
                            result[spot_position].setdefault(spot, dict())
                            result[spot_position][spot][villain_position] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
                        else:
                            action_tuple = tuple(t[3] for t in positions_actions if t[0] == position)[0]
                            raise_actions = sorted((a for a in action_tuple if a.startswith("Raise")),key=lambda x: float(x.split()[1]))
                            raise_size = raise_sizes[raise_actions.index(action)]
                            if spot == "vs_limp":
                                spot = f"vs_raise_nai_{raise_size}"
                            else:
                                spot  = f"vs_3bet_nai_{raise_size}"
                            result[spot_position].setdefault(spot, dict())
                            result[spot_position][spot][villain_position] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]

        # villain_position = None
        # spot = ""
        # raise_size = None
        # raise_sizes = ["low", "low-med", "med", "med-high", "high", "super", "ultra"]
        # for i, (k, position_dict) in enumerate(spot_sequency.items()):
        #     for position, action in position_dict.items():
        #         if i == 0:
        #             if action == "spot":
        #                 spot = "rfi"
        #                 result[spot_position][spot] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
        #             elif position != spot_position:
        #                 villain_position = position
        #                 if action.startswith("Allin"):
        #                     spot = "vs_open_shove"
        #                     result[spot_position].setdefault(spot, dict())
        #                     result[spot_position][spot][villain_position] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
        #                 elif action.startswith("C"):
        #                     spot = "vs_limp"
        #                     result[spot_position].setdefault(spot, dict())
        #                     result[spot_position][spot][villain_position] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
        #                 else:
        #                     spot = "vs_rfi"
        #                     result[spot_position].setdefault(spot, dict())
        #                     result[spot_position][spot][villain_position] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
        #                     action_tuple = tuple(t[3] for t in positions_actions if t[0] == position)[0]
        #                     raise_actions = sorted((a for a in action_tuple if a.startswith("Raise")),key=lambda x: float(x.split()[1]))
        #                     raise_size = raise_sizes[raise_actions.index(action)]
        #         elif i == 1:
        #             if action != "spot":
        #                 villain_position = position
        #                 if action.startswith("Allin"):
        #                     spot  = "vs_3bet_ai"
        #                     result[spot_position].setdefault(spot, dict())
        #                     result[spot_position][spot][villain_position] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
        #                 else:
        #                     action_tuple = tuple(t[3] for t in positions_actions if t[0] == position)[0]
        #                     raise_actions = sorted((a for a in action_tuple if a.startswith("Raise")),key=lambda x: float(x.split()[1]))
        #                     raise_size = raise_sizes[raise_actions.index(action)]
        #                     spot  = f"vs_3bet_nai_{raise_size}"
        #                     result[spot_position].setdefault(spot, dict())
        #                     result[spot_position][spot][villain_position] = [mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict]
        
        # print(f"{villain_position = }")
        # print("-" * 20)
    
    destination_folder = "json_results"
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    with open(f"{destination_folder}\\{file_name}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

