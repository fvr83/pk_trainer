from PIL import Image, ImageDraw, ImageFont



suits = "shdc"

cards_width = 64
cards_height = int((cards_width / 2) * 1.36)



def get_combo_family(combo):
    if len(combo) > 3:

        return 0
    if combo[0] == combo[1]:

        return set(f"{combo[0]}{s_1}{combo[1]}{s_2}" for i, s_1 in enumerate(suits) for j, s_2 in enumerate(suits) if i > j)
    elif combo[2] == "o":

        return set(f"{combo[0]}{s_1}{combo[1]}{s_2}" for i, s_1 in enumerate(suits) for j, s_2 in enumerate(suits) if i != j)
    elif combo[2] == "s":

        return set(f"{combo[0]}{s}{combo[1]}{s}" for s in suits)


def get_text_boundaries(text: str, font: tuple) -> tuple[int]:
    text_len = len(text)
    img_size = text_len * 11
    img = Image.new("RGB", (img_size, int(img_size / 3)), "#ffffff")
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    return width, height


def draw_cards(combo):
    rank_font = ImageFont.truetype("ROBOTOCONDENSED-BLACK.ttf", 36)
    suit_font = ImageFont.truetype("arial.ttf", 20)
    hand_str = get_combo_family(combo).pop()
    card_1_str = hand_str[:2]
    rank_1 = card_1_str[0]
    rank_1_width, rank_1_height = get_text_boundaries(rank_1, rank_font)
    suit_1 = card_1_str[1]
    suit_1_width, suit_1_height = get_text_boundaries(suit_1, suit_font)
    card_1_color = "#9C1818" if suit_1 in "hd" else "black"
    card_2_str = hand_str[2:]
    rank_2 = card_2_str[0]
    rank_2_width, rank_2_height = get_text_boundaries(rank_2, rank_font)
    suit_2 = card_2_str[1]
    suit_2_width, suit_2_height = get_text_boundaries(suit_2, suit_font)
    card_2_color = "#9C1818" if suit_2 in "hd" else "black"

    suit_dict = {"s": "♠", "h": "♥", "d": "♦", "c": "♣"}

    gap = 2
    cards_img = Image.new("RGB", (cards_width, cards_height), "#515152")
    draw = ImageDraw.Draw(cards_img)
    draw.rounded_rectangle((0, 0, (cards_width / 2) - (gap / 2), cards_height - 1), 4, "#ffffff", "#4B4848")
    draw.text(((cards_width - gap - rank_1_width - 10) / 4, (cards_height - rank_1_height - 5) / 2), rank_1, card_1_color, font=rank_font)
    draw.text(((cards_width - gap - suit_1_width - 30) / 16, (cards_height - suit_1_height - 70) / 8), suit_dict[suit_1], card_1_color, font=suit_font)
    draw.rounded_rectangle(((cards_width / 2) + (gap / 2), 0, cards_width - 1, cards_height - 1), 4, "#ffffff", "#4B4848")
    draw.text(((cards_width - gap - rank_2_width + 12) * 0.75, (cards_height - rank_2_height - 5) / 2), rank_2, card_2_color, font=rank_font)
    draw.text(((cards_width - gap - suit_2_width + 17) * 0.5, (cards_height - suit_2_height - 70) / 8), suit_dict[suit_2], card_2_color, font=suit_font)

    return cards_img


cards_img = draw_cards("KQo")
cards_img.show()