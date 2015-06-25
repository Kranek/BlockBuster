"""
The main file of the BlockBuster. Run it to play and have fun!
"""
from gamedata import Assets
from gameclock import GameClock
from pygame import init
from pygame.display import set_caption, set_icon, set_mode, get_surface, flip
from pygame.event import get
from constants import LEVEL_WIDTH, LEVEL_HEIGHT
from GameStateMenu import GameStateMenu
import Tkinter as Tk

if __name__ == '__main__':
    ROOT = Tk.Tk()
    ROOT.withdraw()

    init()

    Assets.load_images()
    GAME_ICON = Assets.gameIcon
    set_caption('BlockBuster')
    set_icon(GAME_ICON)
    # WINDOW = set_mode((LEVEL_WIDTH, LEVEL_HEIGHT))
    set_mode((LEVEL_WIDTH, LEVEL_HEIGHT))

    SCREEN = get_surface()
    flip()

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
        events = get()
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
        flip()

    CLOCK = GameClock(max_ups=60, max_fps=60, update_callback=_update, frame_callback=_draw)

    while True:
        CLOCK.tick()
