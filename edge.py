import math


class Edge:
    # Initializes the edge of the game board, specifying coordinates, color, and distance to handle mouse clicks
    def __init__(self, x1, y1, x2, y2, cell_size):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.distance_multiplier = 1.33
        self.distance_to_click = cell_size / self.distance_multiplier
        self.color = (169,169,169)
        self.is_colored = False
    
    # Removing duplicate lines
    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2
        return False
    
    # Methods to draw an edge
    def draw(self, renderer, width=1):
        renderer.draw_line(self, width)
    
    # Methods to check if the edge is clicked
    def is_clicked(self, pos):
        mid_x = (self.x1 + self.x2) // 2
        mid_y = (self.y1 + self.y2) // 2

        distance = math.sqrt((pos[0] - mid_x)**2 + (pos[1] - mid_y)**2)

        return distance <= 0.5 * self.distance_to_click
    
    # Methods to set the color of the edge
    def set_color(self, color):
        if not self.is_colored:
            self.color = color
            self.is_colored = True
