from src.types.main import ColorFunction, SelectorFunction
from src.menu.config import COLORS
from pygame import (
    Surface, font, Rect
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
