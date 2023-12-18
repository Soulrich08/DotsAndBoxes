import pygame
import sys


class Renderer:

    screen_color = (255, 255, 255)
    dot_color = (28, 28, 28)
    
    # Initializing the object to draw the game screen, initial fill with color, and call the update_display method
    def __init__(self, width, height, database_data, game):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.database_data = database_data
        self.game = game
        self.screen.fill(self.screen_color)
        self.update_display()
    
    # Clearing the screen
    def clear_screen(self):
        self.screen.fill((0, 0, 0))
    
    # Drawing a line
    def draw_line(self, edge, width=1):
        pygame.draw.line(self.screen, edge.color, (edge.x1, edge.y1), (edge.x2, edge.y2), width)
    
    # Drawing a dot
    def draw_dot(self, x, y, radius):
        pygame.draw.circle(self.screen, self.dot_color, (x, y), radius)
    
    # Drawing a rectangle
    def draw_rect(self, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height))
    
    # Display the main screen with "Play" and "History" buttons
    def main_screen(self):
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Main Screen")
    
        font = pygame.font.Font(None, 36)
        play_button = pygame.Rect(self.width // 2 - 50, self.height // 2 - 25, 100, 50)
        
        # Define history button below the play button
        history_button = pygame.Rect(self.width // 2 - 50, self.height // 2 + 30, 100, 50)
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_button.collidepoint(event.pos):
                        return self.board_size_screen()
                    elif history_button.collidepoint(event.pos):
                        self.show_history()
    
            window.fill(self.screen_color)
    
            # Draw play button
            pygame.draw.rect(window, (0, 0, 0), play_button, 2)
            text = font.render("Play", True, (0, 0, 0))
            window.blit(text, (play_button.x + play_button.width // 2 - text.get_width() // 2,
                               play_button.y + play_button.height // 2 - text.get_height() // 2))
    
            # Draw history button
            pygame.draw.rect(window, (0, 0, 0), history_button, 2)
            text = font.render("History", True, (0, 0, 0))
            window.blit(text, (history_button.x + history_button.width // 2 - text.get_width() // 2,
                               history_button.y + history_button.height // 2 - text.get_height() // 2))
    
            pygame.display.flip()

    # Display the game history screen
    def show_history(self):
        # Open a new window for game history
        history_window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game History")
        history_window.fill(self.screen_color)

        font = pygame.font.Font(None, 32)
        y_offset = 50

        history = self.database_data.get_database()

        # Display game history on the window
        for record in history:
            history_text = font.render(f"Time: {record[1]} Winner: {record[2]}, Player 1 Score: {record[3]}, Player 2 Score: {record[4]}", True, (0, 0, 0))
            history_window.blit(history_text, (10, y_offset))
            y_offset += 40

        pygame.display.flip()
        waiting_for_close = True
        while waiting_for_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    waiting_for_close = False

    # Display a screen for selecting the size of the game board
    def board_size_screen(self):
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Choose Board Size")

        font = pygame.font.Font(None, 36)
        buttons = {
            "5x5": pygame.Rect(self.width // 2 - 50, self.height // 2 - 100, 100, 50),
            "7x7": pygame.Rect(self.width // 2 - 50, self.height // 2, 100, 50),
            "9x9": pygame.Rect(self.width // 2 - 50, self.height // 2 + 100, 100, 50),
        }

        game_started = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for size, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            if size == "5x5":
                                cell_size = 140
                                margin = 100
                                window.fill(self.screen_color)
                                return cell_size, margin
                            elif size == "7x7":
                                cell_size = 100
                                margin = 100
                                window.fill((self.screen_color))
                                return cell_size, margin
                            elif size == "9x9":
                                cell_size = 78
                                margin = 100
                                window.fill(self.screen_color)
                                return cell_size, margin
                            game_started = True
                            return

            window.fill(self.screen_color)
            if not game_started:
                for size, rect in buttons.items():
                    pygame.draw.rect(window, (0, 0, 0), rect, 2)
                    text = font.render(size, True, (0, 0, 0))
                    window.blit(text, (rect.x + rect.width // 2 - text.get_width() // 2, rect.y + rect.height // 2 - text.get_height() // 2))

            pygame.display.flip()
    
    # Displays information about the current player
    def display_current_player(self, player):
        pygame.font.init()
        font = pygame.font.Font(None, 32)
        text = font.render(f"Current Player: {player.name}", True, player.main_color)
    
        # Clear the area where the player's name is displayed
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(10, 10, text.get_width(), text.get_height()))
    
        self.screen.blit(text, (10, 10))  # Adjust the position as needed
        pygame.display.flip()

    # Display information about the winner of the game and process the "Back to menu" button
    def display_winner(self, winner, players):
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        text_winner = font.render("The winner is: ", True, (28, 28, 28))
        text_winner_name = font.render(winner.name, True, winner.main_color)

        scores_text = [font.render(f"{player.name}: {player.score}", True, player.main_color) for player in players]

        window_width, window_height = self.width, self.height
        window = pygame.display.set_mode((window_width, window_height))
        window.fill((255, 255, 255))

        x_offset = window_width // 2 - text_winner.get_width() // 2
        y_offset = 20

        window.blit(text_winner, (x_offset, y_offset))
        window.blit(text_winner_name, (x_offset + text_winner.get_width(), y_offset))

        y_offset += 60

        for score_text in scores_text:
            y_offset += 40
            window.blit(score_text, (x_offset, y_offset))
        
        button_back_to_menu = pygame.Rect(window_width // 2 - 100, window_height - 100, 200, 50)
        button_back_to_menu.x = (window_width - button_back_to_menu.width) // 2
        button_back_to_menu.y = (window_height - button_back_to_menu.height) // 2

        button_surface = pygame.Surface(button_back_to_menu.size)
        button_surface.fill((169,169,169))
        text_button = font.render("Back to menu", True, (255, 255, 255))
        button_surface.blit(text_button, (button_surface.get_width() // 2 - text_button.get_width() // 2, button_surface.get_height() // 2 - text_button.get_height() // 2))

        window.blit(button_surface, button_back_to_menu)

        self.database_data.insert_to_database(winner, players)
        self.database_data.insert_to_cloud_database(winner, players)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                   if button_back_to_menu.collidepoint(event.pos):
                    return

            pygame.display.flip()

    # Updates the screen       
    def update_display(self):
        pygame.display.flip()
