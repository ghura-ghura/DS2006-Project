from src.utils.pygame import get_back_instruction_rect, is_back_instruction_clicked
from src.utils.pygame import draw_title, handle_event
from src.menu.search.input.main import InputField
from src.utils.file import get_file_path_by_name
from src.types.main import SetBackRectFunction
from src.menu.config import config
from pygame import (
    KEYDOWN, K_BACKSPACE, K_RETURN, K_ESCAPE, K_LEFT, K_RIGHT, K_HOME, K_END, MOUSEBUTTONDOWN,
    Surface, event as pygame_event, font, time, display, mouse, draw, Rect
)

class Search:
    def __init__(self, surface: Surface, back_font: font.Font) -> None:
        self.title_config = config["title_config"]
        self.menu_config = config["menu_config"]
        self.window_config = config["window"]
        self.search_config = config["search"]
        self.input_field_config = self.search_config["input_field"]

        self.selected_result: str | None = None
        self.result_rects: list[Rect] = []
        self.back_rect: Rect | None = None
        self.results: list[str] = []
        self.isSearching = False

        self.back_font = back_font
        self.surface = surface

        self.input_field = InputField(
            placeholder_color=self.input_field_config["placeholder_color"],
            text_padding_left=self.input_field_config["text_padding_left"],
            background_color=self.input_field_config["background_color"],
            field_dimensions=self.input_field_config["dimensions"],
            border_color=self.input_field_config["border_color"],
            border_width=self.input_field_config["border_width"],
            field_position=self.input_field_config["position"],
            placeholder=self.input_field_config["placeholder"],
            text_color=self.input_field_config["text_color"],
            font_size=self.input_field_config["font_size"],
            on_text_change=lambda t: self.filter_results(t),
            max_length=self.input_field_config["max_length"],
            on_submit=self.load_selected_result,
            surface=surface,
        )

        self.input_field.set_focus(True)
        self.filter_results("")

    def draw_search_results(self) -> None:
        if not self.results:
            self.result_rects = []
            return None
            
        result_y = self.input_field.rect.bottom + (self.input_field_config["text_padding_left"] * 2)
        result_font = font.Font(None, self.search_config["result_font_size"])
        self.result_rects = []

        for i, result in enumerate(self.results[:self.search_config["max_results"]]):
            result_surface = result_font.render(result, True, self.search_config["result_color"])
            result_rect = result_surface.get_rect()
            result_rect.x = self.input_field.rect.x
            result_rect.y = result_y + (i * self.search_config["result_gap"])
            
            self.result_rects.append(result_rect)

            mouse_pos = mouse.get_pos()
            if result_rect.collidepoint(mouse_pos):
                highlight_rect = Rect(result_rect.x - 5, result_rect.y - 2, result_rect.width + self.input_field_config["text_padding_left"], result_rect.height + 4)
                draw.rect(self.surface, self.search_config["highlight_color"], highlight_rect)

            self.surface.blit(result_surface, result_rect)

    def filter_results(self, text: str) -> None:
        txt = text.strip().lower()

        show_all = True if not txt else False
        self.results = get_file_path_by_name(txt, show_all=show_all)

    def load_selected_result(self) -> None:
        print(self.results)
        print(self.selected_result)
        if self.results:
            self.selected_result = self.results[0]
            print(f"Selected dataset: {self.selected_result}")
            self.isSearching = False 

    def start(self, title: str, title_font: font.Font, clock: time.Clock, set_back_rect: SetBackRectFunction) -> None:
        self.isSearching = True
        while self.isSearching:
            handle_event(
                on_key_down=lambda event: self.on_key_down(event),
                on_mouse_down=lambda event: self.on_mouse_down(event),
            )

            self.surface.fill(self.window_config["color"])

            draw_title(
                position=self.title_config["position"],
                color=self.title_config["color"],
                surface=self.surface,
                font=title_font,
                title=title,
            )

            self.input_field.draw()
            self.draw_search_results()

            back_rect = get_back_instruction_rect(
                position=self.menu_config["back_position"],
                color=self.menu_config["back_color"],
                text=self.menu_config["back_text"],
                back_font=self.back_font,
                surface=self.surface,
            )
            self.back_rect = back_rect
            set_back_rect(back_rect)

            display.flip()
            clock.tick(60)

    def on_key_down(self, event: pygame_event.Event) -> bool:
        if event.key == K_ESCAPE:
            self.isSearching = False
            return False

        if not self.handle_event(event):
            return False

        return True

    def on_mouse_down(self, event: pygame_event.Event) -> bool:
        if self.back_rect and is_back_instruction_clicked(mouse_position=event.pos, back_rect=self.back_rect):
            self.isSearching = False
            return True

        if self.check_if_result_clicked(event):
            return True
            
        if not self.handle_event(event):
            return False

        if not self.input_field.is_colliding(event.pos):
            self.input_field.set_focus(False)
            return False

        return True

    def check_if_result_clicked(self, event: pygame_event.Event) -> bool:
        for i, result_rect in enumerate(self.result_rects):
            if result_rect.collidepoint(event.pos):
                self.selected_result = self.results[i]
                print(f"Selected dataset: {self.selected_result}")
                self.isSearching = False
                return True
        return False

    def handle_event(self, event: pygame_event.Event) -> bool:
        if event.type == MOUSEBUTTONDOWN:
            if self.input_field.is_colliding(event.pos):
                self.input_field.set_focus(True)
                self.input_field.set_cursor_where_clicked(event.pos[0])
                return True
            else:
                self.input_field.set_focus(False)
                return False

        if not self.input_field.get_active():
            return False

        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.input_field.handle_backspace()
                return True
            elif event.key == K_RETURN:
                self.handle_submit()
                return True
            elif event.key == K_ESCAPE:
                self.input_field.set_focus(False)
                return True
            elif event.key == K_LEFT:
                self.input_field.move_cursor(-1)
                return True
            elif event.key == K_RIGHT:
                self.input_field.move_cursor(1)
                return True
            elif event.key == K_HOME:
                self.input_field.set_cursor_position(0)
                return True
            elif event.key == K_END:
                self.input_field.set_cursor_position_to_end()
                return True
            elif len(event.unicode) > 0 and not self.input_field.text_length_exceeds_max_length():
                self.input_field.insert_char_at_cursor_position(event.unicode)
                return True

        return False

    def handle_submit(self) -> None:
        if self.results:
            self.load_selected_result()