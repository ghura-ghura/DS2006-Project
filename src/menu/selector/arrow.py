from pygame import Surface, draw

class ArrowSelector:
    def __init__(self, surface: Surface, size: int, offset: int, color: tuple[int, int, int]) -> None:
        self.arrow_offset = offset
        self.arrow_color = color
        self.surface = surface
        self.arrow_size = size
        
    def draw(self, index: int, title_position: tuple[int, int], margin_top: int, gap: int) -> None:
        arrow_position = self.calculate_arrow_position(index, title_position, margin_top, gap)
        self.draw_arrow(arrow_position)
    
    def draw_arrow(self, position: tuple[int, int]) -> None:
        x, y = position

        right_tip = (x + self.arrow_size // 2, y)
        top_left = (x - self.arrow_size // 2, y - self.arrow_size // 2)
        bottom_left = (x - self.arrow_size // 2, y + self.arrow_size // 2)

        points = [right_tip, top_left, bottom_left]
        
        draw.polygon(self.surface, self.arrow_color, points)

    def calculate_arrow_position(self, index: int, title_position: tuple[int, int], margin_top: int, gap: int) -> tuple[int, int]:
        title_x, title_y = title_position
        option_y = title_y + margin_top + (index * gap)
        
        arrow_x = title_x - self.arrow_offset
        
        return (arrow_x, option_y)