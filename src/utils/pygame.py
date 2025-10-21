from src.types.main import ColorFunction, SelectorFunction, PyGameEventFunction
from src.menu.config import COLORS
from sys import exit
from pygame import (
    Surface, font, Rect, quit as pygame_quit,
    QUIT, KEYDOWN, MOUSEBUTTONDOWN,
    event as pygame_event,
)

def draw_options(surface: Surface, options: list[str], title_position: tuple[int, int], font: font.Font, margin_top: int, gap: int, alpha: int | None = None, color_fn: ColorFunction | None = None, selector_fn: SelectorFunction | None = None) -> None:
    """
    Summary: 
    
    Draws a list of menu options on a pygame surface. Optionally sets transparency and custom colors/selectors for each option.
    
    Args:
        - surface: The surface to draw the options on.
        - options: List of option text strings to render.
        - title_position: The center position (x, y) of the title above the options.
        - font: The font to use for rendering the options.
        - margin_top: The vertical margin from the title to the first option.
        - gap: The vertical gap between each individual option.
        - alpha: The transparency of the options.
        - color_fn: A function that takes an option's index and returns an RGB color tuple for that option.
        - selector_fn: A function that takes an option's index and draws a selector for that option.
    
    Returns:
        - None
    """
    for i, option in enumerate(options):
        if color_fn is None:
            color = COLORS["WHITE"]
        else:
            color = color_fn(i)
        
        option_surface = font.render(option, True, color)
        if alpha:
            option_surface.set_alpha(alpha)

        # Evenly space out the menu options with consideration to the title
        title_x, title_y = title_position
        y_position = title_y + margin_top + (i * gap)
        option_rect = option_surface.get_rect(center=(title_x, y_position))
        surface.blit(option_surface, option_rect)

        if selector_fn is not None:
            selector_fn(i)

def draw_title(surface: Surface, title: str, font: font.Font, color: tuple[int, int, int], position: tuple[int, int], alpha: int | None = None) -> None:
    """
    Summary: 
    
    Draws a title on a pygame surface. Optionally sets the transparency of the rendered text.
    
    Args:
        - surface: The surface to draw the title on.
        - title: The text to render.
        - font: The font to use for rendering the title.
        - color: The color of the title.
        - position: The center position (x, y) of the title
        - alpha: The transparency of the title.
    
    Returns:
        - None
    """
    title_surface: Surface = font.render(title, True, color)

    if alpha:
        title_surface.set_alpha(alpha)

    title_rect: Rect = title_surface.get_rect(center=position)
    surface.blit(title_surface, title_rect)

def handle_event(on_key_down: PyGameEventFunction, on_mouse_down: PyGameEventFunction) -> None:
    """
    Summary:
    
    Handles the events and calls the appropriate functions.
    
    Args:
        - on_key_down: The function to call when a key is pressed.
        - on_mouse_down: The function to call when a mouse button is pressed.
    
    Returns:
        - None
    """
    for event in pygame_event.get():
        if event.type == QUIT:
            quit_program()
        elif event.type == KEYDOWN:
            if on_key_down(event):
                continue
        elif event.type == MOUSEBUTTONDOWN:
            if on_mouse_down(event):
                continue

def quit_program(status: int = 0) -> None:
    """
    Summary:
    
    Quits the program and exits with the given status.
    
    Args:
        - status: The status to exit with.
    
    Returns:
        - None
    """
    pygame_quit()
    exit(status)

def get_back_instruction_rect(text: str, color: tuple[int, int, int], position: tuple[int, int], back_font: font.Font, surface: Surface) -> Rect:
    """
    Summary:
    
    Gets the rectangle of the back instruction.
    
    Args:
        - text: The text to render.
        - color: The color of the back instruction.
        - position: The center position (x, y) of the back instruction.
        - back_font: The font to use for rendering the text.
        - surface: The surface to draw the back instruction on.
    
    Returns:
        - The rectangle of the back instruction surface.
    """
    back_surface = back_font.render(text, True, color)
    back_rect = back_surface.get_rect(center=position)
    surface.blit(back_surface, back_rect)
    return back_rect

def is_back_instruction_clicked(mouse_position: tuple[int, int], back_rect: Rect) -> bool:
    """
    Summary:
    
    Checks if the back instruction is clicked.
    
    Args:
        - mouse_position: The position of the mouse.
        - back_rect: The rectangle of the back instruction.
    
    Returns:
        - True if the back instruction is clicked, False otherwise.
    """ 
    return back_rect.collidepoint(mouse_position)