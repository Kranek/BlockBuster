"""
The main file of the BlockBuster. Run it to play and have fun!
"""
from gamedata import Assets
from gameclock import GameClock
import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from GameStateMenu import GameStateMenu
import Tkinter as Tk

if __name__ == '__main__':
    ROOT = Tk.Tk()
    ROOT.withdraw()

    pygame.init()

    Assets.load_images()
    GAME_ICON = Assets.gameIcon
    pygame.display.set_caption('BlockBuster')
    pygame.display.set_icon(GAME_ICON)
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH/2, WINDOW_HEIGHT))

    SCREEN = pygame.display.get_surface()
    pygame.display.flip()

    CONTEXT = dict()
    GAMESTATE = GameStateMenu(CONTEXT, SCREEN)
    CONTEXT["gamestate"] = GAMESTATE

    # noinspection PyUnusedLocal
    def _update(_):
        """
        Pump events to the current GameState and tell its objects to update
        :param _: unused dt provided by GameClock
        :return:
        """
        events = pygame.event.get()
        CONTEXT["gamestate"].handle_input(events)
        CONTEXT["gamestate"].update()
        # gamestate.handle_input(events)
        # gamestate.update()


    # noinspection PyUnusedLocal
    def _draw(_):
        """
        Ask the current GameState to redraw itself
        :param _: unused interp provided by GameClock
        :return:
        """
        # gamestate.draw()
        CONTEXT["gamestate"].draw()
        pygame.display.flip()

    CLOCK = GameClock(max_ups=60, max_fps=60, update_callback=_update, frame_callback=_draw)

    while True:
        CLOCK.tick()
