from gamedata import Assets
from gameclock import GameClock
# from constants import
import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from GameStateMenu import GameStateMenu
import Tkinter as Tk


if __name__ == '__main__':
    root = Tk.Tk()
    root.withdraw()

    pygame.init()

    Assets.load_images()
    game_icon = Assets.gameIcon
    pygame.display.set_caption('BlockBuster')
    pygame.display.set_icon(game_icon)
    window = pygame.display.set_mode((WINDOW_WIDTH/2, WINDOW_HEIGHT))

    screen = pygame.display.get_surface()
    pygame.display.flip()

    context = dict()
    gamestate = GameStateMenu(context, screen)
    context["gamestate"] = gamestate

    # noinspection PyUnusedLocal
    def _update(dt):
        events = pygame.event.get()
        context["gamestate"].handle_input(events)
        context["gamestate"].update()
        # gamestate.handle_input(events)
        # gamestate.update()


    # noinspection PyUnusedLocal
    def _draw(interp):
        # gamestate.draw()
        context["gamestate"].draw()
        pygame.display.flip()

    clock = GameClock(max_ups=60, max_fps=60, update_callback=_update, frame_callback=_draw)

    while True:
        clock.tick()