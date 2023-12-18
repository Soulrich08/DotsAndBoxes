from cell import Cell
from edge import Edge


class Board:
    # Initializing the game board with cells, edges, and points
    def __init__(self, renderer, width, height, cell_size, edge_width, dot_size, margin):
        self.renderer = renderer
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.edge_width = edge_width
        self.dot_size = dot_size
        self.margin = margin
        self.edges = []
        self.cells = []
        for x in range(self.margin, self.width - self.margin, self.cell_size):
            for y in range(self.margin, self.height - self.margin, self.cell_size):
                top = self.define_edge(Edge(x, y, x + self.cell_size, y, self.cell_size))
                right = self.define_edge(Edge(x + self.cell_size, y, x + self.cell_size, y + self.cell_size, self.cell_size))
                bottom = self.define_edge(Edge(x, y + self.cell_size, x + self.cell_size, y + self.cell_size, self.cell_size))
                left = self.define_edge(Edge(x, y, x, y + self.cell_size, self.cell_size))

                self.cells.append(Cell(top, right, bottom, left))

    # Define the edges of the game board
    def define_edge(self, edge):
        if edge not in self.edges:
            self.edges.append(edge)
        else:
            edge = self.edges[self.edges.index(edge)]
        return edge

    # Checking for filled squares when setting a line
    def check_squares(self, player, clicked_line):
        affected_cells = []
        for cell in self.cells:
            if clicked_line in cell.edges.values():
                affected_cells.append(cell)

        filled_any_cell = False
        for cell in affected_cells:
            if cell.check_is_filled(player):
                filled_any_cell = True
                player.score += 1
                print(f'{player.name} score: {player.score}')
        return filled_any_cell
    
    # Drawing points and cells on the game board
    def draw_dots(self, dot_radius):
        for x in range(self.margin, self.width - self.margin, self.cell_size):
            for y in range(self.margin, self.height - self.margin, self.cell_size):
                self.renderer.draw_dot(x, y, dot_radius)
                self.renderer.draw_dot(x + self.cell_size, y, dot_radius)
                self.renderer.draw_dot(x, y + self.cell_size, dot_radius)
                self.renderer.draw_dot(x + self.cell_size, y + self.cell_size, dot_radius)
    
    # Drawing points and cells on the game board
    def draw(self):
        for cell in self.cells:
            cell.draw(self.renderer)
        for line in self.edges:
            line.draw(self.renderer, self.edge_width)
        self.draw_dots(self.dot_size)
        self.renderer.update_display()

    # Retrieving the edge that was clicked on
    def get_edge_at_pos(self, pos):
        for edge in self.edges:
            if edge.is_clicked(pos):
                return edge
        return None