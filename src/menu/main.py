from src.utils.pygame import draw_title, draw_options, get_back_instruction_rect, is_back_instruction_clicked
from src.menu.selector.arrow import ArrowSelector
from src.utils.pygame import quit_program
from src.menu.search.main import Search
from src.menu.config import config
from typing import Callable
from pygame import (
    QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_UP, K_DOWN, K_RETURN, K_SPACE, K_ESCAPE,
    display, time, font, event as pygame_event, mouse,
    init as pygame_init, Rect,
)

class Menu:
    def __init__(self, load_file: Callable[[str], None]) -> None:
        pygame_init()

        self.selector_config = config["selector_config"]
        self.title_config = config["title_config"]
        self.menu_config = config["menu_config"]
        self.window_config = config["window"]

        self.non_selected_option_color = config["colors"]["WHITE"]
        self.selected_option_color = config["colors"]["RED"]
        self.selected_option_index = 0

        self.surface = display.set_mode(self.window_config["dimensions"])
        self.caption = display.set_caption(self.title_config["title"])
        self.search: Search | None = None

        self.back_font = font.Font(None, self.menu_config["back_font_size"])
        self.title_font = font.Font(None, self.title_config["font_size"])
        self.menu_font = font.Font(None, self.menu_config["font_size"])

        self.options = self.menu_config["options"]["primary"]
        self.back_rect: Rect | None = None
        self.load_file = load_file
        self.clock = time.Clock()

        self.arrow_selector = ArrowSelector(
            offset=self.selector_config["offset"],
            color=self.selector_config["color"],
            size=self.selector_config["size"],
            surface=self.surface,
        )
        
    def start(self) -> None:
        while True:
            for event in pygame_event.get():
                if event.type == QUIT:
                    quit_program()
                elif event.type == KEYDOWN:
                    self.onKeyDown(event)
                elif event.type == MOUSEBUTTONDOWN:
                    self.onMouseDown(event)

            self.surface.fill(self.window_config["color"])

            back_rect = get_back_instruction_rect(
                position=self.menu_config["back_position"],
                color=self.menu_config["back_color"],
                text=self.menu_config["back_text"],
                back_font=self.back_font,
                surface=self.surface,
            )
            self.set_back_rect(back_rect)

            draw_title(self.surface, self.title_config["title"], self.title_font, self.title_config["color"], self.title_config["position"])
                        
            draw_options(
                selector_fn=lambda i: self.arrow_selector.draw(
                    title_position=self.title_config["position"],
                    margin_top=self.menu_config["margin_top"],
                    gap=self.menu_config["gap"],
                    index=i,
                ) if i == self.selected_option_index else None,
                color_fn=lambda i: self.selected_option_color if i == self.selected_option_index else self.non_selected_option_color,
                title_position=self.title_config["position"],
                margin_top=self.menu_config["margin_top"],
                gap=self.menu_config["gap"],
                surface=self.surface,
                options=self.options,
                font=self.menu_font,
                alpha=None,
            )

            display.flip()
            self.clock.tick(60)

    def onOptionClick(self, option: str) -> None:
        match option:
            case "Load dataset":
                self.load_dataset()
            case "Train model":
                self.train_model()
            case "Evaluate model":
                self.evaluate_model()

    def load_dataset(self) -> None:
        if self.search is None:
            self.search = Search(self.surface, self.back_font, self.load_file)
        
        self.search.start(
            set_back_rect=self.set_back_rect,
            title_font=self.title_font,
            title="Load Dataset",
            clock=self.clock,
        )
    
    def train_model(self) -> None:
        pass

    def evaluate_model(self) -> None:
        pass

    def onKeyDown(self, event: pygame_event.Event) -> None:
        if event.key == K_UP:
            self.selected_option_index = (self.selected_option_index - 1) % len(self.options)
        elif event.key == K_DOWN:
            self.selected_option_index = (self.selected_option_index + 1) % len(self.options)
        elif event.key == K_RETURN or event.key == K_SPACE:
            self.onOptionClick(self.options[self.selected_option_index])
        elif event.key == K_ESCAPE:
            quit_program()

    def onMouseDown(self, event: pygame_event.Event) -> None:
        match event.button:
            case 1:
                mouse_position = mouse.get_pos()
                
                if self.back_rect and is_back_instruction_clicked(mouse_position, self.back_rect):
                    quit_program()
                    return
                
                option_data = self.get_option_by_position(
                    option_y=self.title_config["position"][1],
                    title_x=self.title_config["position"][0],
                    mouse_position=mouse_position,
                )

                if option_data is not None:
                    option, option_index = option_data
                    self.selected_option_index = option_index
                    self.onOptionClick(option)

    def get_option_by_position(self, mouse_position: tuple[int, int], option_y: int, title_x: int) -> tuple[str, int] | None:
        for i, option in enumerate(self.options):
            y_position = option_y + self.menu_config["margin_top"] + (i * self.menu_config["gap"])
            
            option_surface = self.menu_font.render(option, True, (255, 255, 255))
            option_rect = option_surface.get_rect(center=(title_x, y_position))
            
            clickable_rect = Rect(
                option_rect.x - 10,
                option_rect.y - 5,
                option_rect.width + 20,
                option_rect.height + 10
            )

            if clickable_rect.collidepoint(mouse_position):
                return (option, i)

        return None

    def set_back_rect(self, back_rect: Rect) -> None:
        self.back_rect = back_rect
