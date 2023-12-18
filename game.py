import pygame
import sys
from database_data import DatabaseData
from renderer import Renderer
from board import Board
from player import Player


DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 900
DISPLAY_COLOR = (255, 255, 255)


class Game:
    # Initializing the game, connecting to the database, creating the game board and players
    def __init__(self):
        pygame.init()
        self.database_data = DatabaseData()
        self.renderer = Renderer(DISPLAY_WIDTH, DISPLAY_HEIGHT, self.database_data, self)
        cell_size, margin = self.renderer.main_screen()
        edge_width = cell_size // 10
        dot_size = edge_width * 1.2
        margin = 100
        self.board = Board(self.renderer, DISPLAY_WIDTH, DISPLAY_HEIGHT, cell_size, edge_width, dot_size, margin)
        self.players = [Player("Player 1", (255, 0, 0), (255, 90, 90)), Player("Player 2", (0, 0, 255), (90, 90, 255))]
        self.current_player_index = 0
    
    # Methods to change the current player and check if the game is over
    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    # Methods to change the current player and check if the game is over
    def is_game_over(self): 
        return all(cell.filled_player for cell in self.board.cells)
    
    # The main game loop, handling mouse events, drawing the board, checking the end of the game and displaying the winner.This code allows players to play the game "Dots and Boxes" on the game board of their choice and save the game history in the database
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked_edge = self.board.get_edge_at_pos(pos)
                    if clicked_edge and not clicked_edge.is_colored:
                        current_player = self.players[self.current_player_index]
                        clicked_edge.set_color(current_player.main_color)
                        if not self.board.check_squares(current_player, clicked_edge):
                            self.switch_player()

            self.board.draw()
            self.renderer.display_current_player(self.players[self.current_player_index])
            self.renderer.update_display()

            if self.is_game_over():
                winner = max(self.players, key=lambda player: player.score)
                self.renderer.display_winner(winner, self.players)
                self.__init__()
