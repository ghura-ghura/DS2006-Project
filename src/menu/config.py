COLORS: dict[str, tuple[int, int, int]] = {
    "WHITE": (255, 255, 255),
    "GRAY": (128, 128, 128),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
}

DATASETS_FOLDER = "dataset"

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
WINDOW_COLOR: tuple[int, int, int] = COLORS["BLACK"]

TITLE = "Train a model"
TITLE_FONT_SIZE = 72
TITLE_COLOR: tuple[int, int, int] = COLORS["WHITE"]
TITLE_POSITION: tuple[int, int] = (400, 150)

MENU_FONT_SIZE = 48
MENU_MARGIN_TOP = 75
MENU_GAP = 50

SELECTOR_COLOR: tuple[int, int, int] = COLORS["RED"]
SELECTOR_OFFSET = 150
SELECTOR_SIZE = 20

BACK_POSITION: tuple[int, int] = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
BACK_COLOR: tuple[int, int, int] = COLORS["GRAY"]
BACK_TEXT = "Press Esc to quit"
BACK_FONT_SIZE = 24

INPUT_FIELD_POSITION: tuple[int, int] = (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 50)
INPUT_FIELD_BACKGROUND_COLOR: tuple[int, int, int] = COLORS["BLACK"]
INPUT_FIELD_PLACEHOLDER_COLOR: tuple[int, int, int] = COLORS["GRAY"]
INPUT_FIELD_BORDER_COLOR: tuple[int, int, int] = COLORS["WHITE"]
INPUT_FIELD_TEXT_COLOR: tuple[int, int, int] = COLORS["WHITE"]
INPUT_FIELD_DIMENSIONS: tuple[int, int] = (400, 40)
INPUT_FIELD_CURSOR_BLINK_SPEED = 500
INPUT_FIELD_PLACEHOLDER = "Search..."
INPUT_FIELD_TEXT_PADDING_LEFT = 10
INPUT_FIELD_BORDER_WIDTH = 2
INPUT_FIELD_MAX_LENGTH = 100
INPUT_FIELD_FONT_SIZE = 32


PRIMARY_MENU_OPTIONS: list[str] = [
    "Load dataset",
    "Train model",
    "Evaluate model",
]

input_field = {
    "cursor_blink_speed": INPUT_FIELD_CURSOR_BLINK_SPEED,
    "placeholder_color": INPUT_FIELD_PLACEHOLDER_COLOR,
    "text_padding_left": INPUT_FIELD_TEXT_PADDING_LEFT,
    "background_color": INPUT_FIELD_BACKGROUND_COLOR,
    "border_width": INPUT_FIELD_BORDER_WIDTH,
    "border_color": INPUT_FIELD_BORDER_COLOR,
    "placeholder": INPUT_FIELD_PLACEHOLDER,
    "dimensions": INPUT_FIELD_DIMENSIONS,
    "max_length": INPUT_FIELD_MAX_LENGTH,
    "text_color": INPUT_FIELD_TEXT_COLOR,
    "font_size": INPUT_FIELD_FONT_SIZE,
    "position": INPUT_FIELD_POSITION,
}

search = {
    "highlight_color": COLORS["GRAY"],
    "result_color": COLORS["WHITE"],
    "input_field": input_field,
    "result_font_size": 24,
    "max_results": 10,
    "result_gap": 30,
}

window = {
    "dimensions": (WINDOW_WIDTH, WINDOW_HEIGHT),
    "color": WINDOW_COLOR,
}

title_config: dict[str, str | int | tuple[int, int, int]] = {
    "position": TITLE_POSITION,
    "font_size": TITLE_FONT_SIZE,
    "color": TITLE_COLOR,
    "title": TITLE,
}

menu_options: dict[str, list[str]] = {
    "primary": PRIMARY_MENU_OPTIONS,
}

menu_config = {
    "back_font_size": BACK_FONT_SIZE,
    "back_position": BACK_POSITION,
    "margin_top": MENU_MARGIN_TOP,
    "font_size": MENU_FONT_SIZE,
    "back_color": BACK_COLOR,
    "options": menu_options,
    "back_text": BACK_TEXT,
    "gap": MENU_GAP,
}

selector_config = {
    "offset": SELECTOR_OFFSET,
    "color": SELECTOR_COLOR,
    "size": SELECTOR_SIZE,
}

config = {
    "selector_config": selector_config,
    "title_config": title_config,
    "menu_config": menu_config,
    "search": search,
    "window": window,
    "colors": COLORS,
}