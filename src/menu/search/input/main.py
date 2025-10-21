from pygame import draw as pygame_draw, Rect, font, Surface
from typing import Callable

class InputField:
    def __init__(
        self, 
        surface: Surface, 
        on_text_change: Callable[[str], None] | None,
        on_submit: Callable[[], None] | None,
        placeholder_color: tuple[int, int, int],
        background_color: tuple[int, int, int],
        border_color: tuple[int, int, int],
        field_dimensions: tuple[int, int],
        text_color: tuple[int, int, int],
        field_position: tuple[int, int],
        text_padding_left: int,
        border_width: int,
        placeholder: str,
        max_length: int,
        font_size: int,
    ) -> None:
        self.placeholder_color = placeholder_color
        self.text_padding_left = text_padding_left
        self.background_color = background_color
        self.on_text_change = on_text_change
        self.border_color = border_color
        self.border_width = border_width
        self.placeholder = placeholder
        self.text_color = text_color
        self.max_length = max_length
        self.on_submit = on_submit
        self.surface = surface
        self.cursor_pos = 0
        self.active = False
        self.text = ""

        width, height = field_dimensions
        x, y = field_position
        self.rect = Rect(x, y, width, height)

        self.font = font.Font(None, font_size)

    def draw(self) -> None:
        self.draw_field()
        self.draw_border()
        self.draw_text()
        self.draw_cursor()

    def draw_field(self) -> None:
        pygame_draw.rect(self.surface, self.background_color, self.rect)

    def draw_border(self) -> None:
        pygame_draw.rect(self.surface, self.border_color, self.rect, self.border_width)
    
    def draw_text(self) -> None:
        text = self.text if self.text else self.placeholder
        text_color = self.text_color if self.text else self.placeholder_color

        text_surface = self.font.render(text, True, text_color)
        
        text_rect = text_surface.get_rect()
        text_rect.centery = self.rect.centery
        text_rect.x = self.rect.x + self.text_padding_left

        self.surface.blit(text_surface, text_rect)

    def draw_cursor(self) -> None:
        if not self.active:
            return None

        text_before_cursor = self.text[:self.cursor_pos]

        cursor_x = self.rect.x + self.text_padding_left + self.font.size(text_before_cursor)[0]
        cursor_rect = Rect(cursor_x, self.rect.y + (self.text_padding_left / 2), 2, self.rect.height - self.text_padding_left)

        pygame_draw.rect(self.surface, self.text_color, cursor_rect)

    def set_focus(self, focused: bool) -> None:
        self.active = focused 

    def set_cursor_where_clicked(self, click_x: int) -> None:
        """ Finds and sets the cursor position based on the click location """
        relative_x = click_x - self.rect.x - self.text_padding_left

        best_pos = 0
        for i in range(len(self.text) + 1):
            text_before_cursor = self.text[:i]
            text_width = self.font.size(text_before_cursor)[0]
            
            if text_width > relative_x:
                break
            
            best_pos = i

        self.set_cursor_position(best_pos)

    def move_cursor(self, direction: int) -> None:
        new_pos = self.cursor_pos + direction
        self.set_cursor_position(max(0, min(len(self.text), new_pos)))

    def insert_char_at_cursor_position(self, char: str) -> None:
        self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
        self.cursor_pos += 1
        self.notify_text_change()

    def handle_backspace(self) -> None:
        if self.cursor_pos <= 0:
            return None

        self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
        self.cursor_pos -= 1
        self.notify_text_change()

    def notify_text_change(self) -> None:
        if not self.on_text_change:
            return None

        self.on_text_change(self.text)

    def set_active(self, active: bool) -> None:
        self.active = active

    def get_active(self) -> bool:
        return self.active

    def set_text(self, text: str) -> None:
        self.text = text[:self.max_length]
        self.set_cursor_position_to_end()
        self.notify_text_change()

    def get_text(self) -> str:
        return self.text

    def clear(self) -> None:
        self.set_text("")

    def is_colliding(self, point: tuple[int, int]) -> bool:
        return self.rect.collidepoint(point)

    def set_cursor_position_to_end(self) -> None:
        self.set_cursor_position(len(self.text))

    def set_cursor_position(self, position: int) -> None:
        self.cursor_pos = position

    def text_length_exceeds_max_length(self) -> bool:
        return len(self.text) >= self.max_length