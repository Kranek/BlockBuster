"""
This file contains the Running GameState Multi
"""
import sys
from pygame import Surface
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_LEFT, K_UP, K_RIGHT, K_a, K_w, K_d, K_RETURN
from pygame.display import set_mode
from gamedata import Assets
from levels import LevelMulti
from GameStatePauseMenu import GameStatePauseMenu
from constants import LEVEL_WIDTH, LEVEL_HEIGHT, update_level_count


class GameStateRunningMulti(object):
    """
    Multiplayer Running GameState. Contains some of the gameplay logic and a Level,
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
        self.levels = (
            LevelMulti(screen, (0, 0), (K_a, K_w, K_d), 0, self.finish_game, self.disturb_player),
            LevelMulti(screen, (LEVEL_WIDTH, 0), (K_LEFT, K_UP, K_RIGHT), 1, self.finish_game,
                       self.disturb_player)
        )
        set_mode((LEVEL_WIDTH * 2, LEVEL_HEIGHT))
        self.game_finished = False
        self.end_labels = None

    def restart_level(self):
        """
        Helper function that allows to restart level of each of the players
        :return:
        """
        for level in self.levels:
            level.start_level(level.level_number)

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
                                                                       self, LEVEL_WIDTH * 2)
            elif event.type == KEYUP and event.key == K_RETURN:
                set_mode((LEVEL_WIDTH, LEVEL_HEIGHT))
                self.context["gamestate"] = self.prev_state

        if not self.game_finished:
            for level in self.levels:
                level.handle_input(events)

    def disturb_player(self, function, player, level=False):
        """
        Method used to disturb other player game by certain power ups
        :return:
        """
        if level:
            if player == 0:
                function(self.levels[1])
            else:
                function(self.levels[0])
        else:
            if player == 0:
                function(self.levels[1].paddle)
            else:
                function(self.levels[0].paddle)

    def finish_game(self):
        """
        Function triggered on the game end, passed to the Level
        :return:
        """
        self.game_finished = True
        self.end_labels = []
        player1score = self.levels[0].player.score
        player2score = self.levels[1].player.score
        if player1score > player2score:
            self.end_labels.append(Assets.menu_font.render("Player 1 wins!", 1, (255, 255, 255)))
        elif player1score < player2score:
            self.end_labels.append(Assets.menu_font.render("Player 2 wins!", 1, (255, 255, 255)))
        else:
            self.end_labels.append(Assets.menu_font.render("Draw!", 1, (255, 255, 255)))
        self.end_labels.append(Assets.font.render("Player 1 score: " + str(player1score), 1,
                                                  (255, 255, 255)))
        self.end_labels.append(Assets.font.render("Player 2 score: " + str(player2score), 1,
                                                  (255, 255, 255)))
        self.end_labels.append(Assets.font.render("Press enter to return to menu", 1,
                                                  (255, 255, 255)))

        overlay = Surface((LEVEL_WIDTH * 2, LEVEL_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        y = LEVEL_HEIGHT / 2 - sum([label.get_rect().height / 2 for label in self.end_labels])
        offset = 0
        for label in self.end_labels:
            self.screen.blit(label, (LEVEL_WIDTH - label.get_rect().width / 2, y + offset))
            offset = offset + label.get_rect().height

    def draw(self):
        """
        Method called each frame to (re)draw the objects and UI
        :return:
        """
        if not self.game_finished:
            for level in self.levels:
                level.draw()

    def update(self):
        """
        Method called each frame, to update the state of entities based on input events and
        previous state of the game
        :return:
        """
        if not self.game_finished:
            for level in self.levels:
                level.update()

