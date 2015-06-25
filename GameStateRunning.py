"""
This file contains the Running GameState
"""
import sys
from pygame import Surface
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_LEFT, K_UP, K_RIGHT, K_RETURN
from gamedata import Assets
from levels import Level
from constants import LEVEL_WIDTH, LEVEL_HEIGHT, update_level_count
from GameStatePauseMenu import GameStatePauseMenu


class GameStateRunning(object):
    """
    Running GameState. Contains some of the gameplay logic and a Level,
    handles some of the input events...
    """
    def __init__(self, context, screen, prev_state):
        """
        Init with context, main PyGame surface and the previous state
        if you want to be able to go back
        :param context: The field in the main application which contains the current GameState.
        Current GameState has input events pumped into it, is updated and then drawn on the screen.
        Used by the current state to switch to the other GameState
        :param screen: Main PyGame surface to draw the objects/UI on
        :param prev_state: The state to which we will return
        :return:
        """
        update_level_count()
        self.context = context
        self.screen = screen
        self.prev_state = prev_state
        self.level = Level(screen, (0, 0), (K_LEFT, K_UP, K_RIGHT), 0, self.finish_game)
        self.game_finished = False
        self.end_labels = None

    def restart_level(self):
        """
        Helper function that restarts the level (and gets overridden in GameStateRunningMulti
        :return:
        """
        self.level.start_level(self.level.level_number)

    def handle_input(self, events):
        """
        Handles incoming input events
        :param events: input events from the main app
        :return:
        """
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            if not self.game_finished:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.context["gamestate"] = GameStatePauseMenu(self.context, self.screen,
                                                                       self, LEVEL_WIDTH)
            elif event.type == KEYUP and event.key == K_RETURN:
                self.context["gamestate"] = self.prev_state

        if not self.game_finished:
            self.level.handle_input(events)

    def finish_game(self):
        """
        Function triggered on the game end, passed to the Level
        :return:
        """
        self.game_finished = True
        self.end_labels = (
            Assets.menu_font.render("Congratulations!", 1, (255, 255, 255)),
            Assets.font.render("Your final score: " + str(self.level.player.score), 1,
                               (255, 255, 255)),
            Assets.font.render("Press enter to return to menu", 1, (255, 255, 255))
        )

        overlay = Surface((LEVEL_WIDTH, LEVEL_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        y = LEVEL_HEIGHT / 2 - sum([label.get_rect().height / 2 for label in self.end_labels])
        offset = 0
        for label in self.end_labels:
            self.screen.blit(label, (LEVEL_WIDTH / 2 - label.get_rect().width / 2, y + offset))
            offset = offset + label.get_rect().height

    def draw(self):
        """
        Method called each frame to (re)draw the objects and UI
        :return:
        """
        if not self.game_finished:
            self.level.draw()

    def update(self):
        """
        Method called each frame, to update the state of entities based on input events and
        previous state of the game
        :return:
        """
        if not self.game_finished:
            self.level.update()

