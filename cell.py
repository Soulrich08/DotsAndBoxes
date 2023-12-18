class Cell:
    # Initialization of a game board cell with edges and fill
    def __init__(self, top, right, bottom, left):
        self.edges = {'top': top, 'right': right, 'bottom': bottom, 'left': left}
        self.filled_player = None
    
    # Checking if the cell is filled 
    def check_is_filled(self, player):
        if not self.filled_player:
            if all(edge.is_colored for edge in self.edges.values()):
                self.filled_player = player
                print(f'{player.name} filled a square')
                return True
        return False
    
    # Checking if drawing a filled cell
    def draw(self, renderer):
        if self.filled_player:
            x = min(self.edges['left'].x1, self.edges['right'].x1)
            y = min(self.edges['top'].y1, self.edges['bottom'].y1)
            width = abs(self.edges['left'].x1 - self.edges['right'].x1)
            height = abs(self.edges['top'].y1 - self.edges['bottom'].y1)
            renderer.draw_rect(x, y, width, height, self.filled_player.cell_color)