import pygame
import sys
import logging
from game import Game

logging.basicConfig(filename='game_log.log', level=logging.INFO)

if __name__ == "__main__":
    pygame.init()
    
    try:
        logging.info("Game started!")
        game = Game()
        game.run()
    except Exception as e:
        logging.exception("An exception occurred:")
        pygame.quit()
        sys.exit()
