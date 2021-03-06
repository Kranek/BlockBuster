"""
This file contains the Main Menu GameState
"""
import sys
from pygame import draw
from pygame.locals import QUIT, KEYUP, K_UP, K_DOWN, K_RETURN
from gamedata import Assets
from GameStateRunning import GameStateRunning
from GameStateEditor import GameStateEditor
from GameStateRunningMulti import GameStateRunningMulti
from constants import MENU_COLORS, MENU_PADDING, LEVEL_WIDTH, LEVEL_HEIGHT


class GameStateMenu(object):
    """
    Main Menu GameState, the first state in the main application. Allows to run the game,
    level editor, or to quit the game.
    """
    def __init__(self, context, screen):
        """
        Init with context and a main PyGame surface. Note that, unlike in other states, this one
        does not take the previous state as a parameter.
        :param context: The field in the main application which contains the current GameState.
        Current GameState has input events pumped into it, is updated and then drawn on the screen.
        Used by the current state to switch to the other GameState
        :param screen: Main PyGame surface to draw the objects/UI on
        :return:
        """
        self.context = context
        self.screen = screen
        self.background = Assets.background
        self.menu_option = 0
        self.menu_options = []
        self.font = Assets.menu_font  # trust me, it's in here
        self.menu_options.append(self.font.render("NEW GAME", 1, (255, 255, 255)))
        self.menu_options.append(self.font.render("MULTIPLAYER", 1, (255, 255, 255)))
        self.menu_options.append(self.font.render("EDITOR", 1, (255, 255, 255)))
        self.menu_options.append(self.font.render("EXIT", 1, (255, 255, 255)))
        self.title = Assets.title_font.render("BlockBuster", 1, (255, 255, 255))
        self.authors = Assets.font.render("Authors: Kranek, RavMahov", 1, (255, 255, 255))

    def handle_input(self, events):
        """
        Handles incoming input events
        :param events: input events from the main app
        :return:
        """
        for event in events:
            if event.type == QUIT:
                sys.exit(0)

            elif event.type == KEYUP:
                if event.key == K_UP:
                    if self.menu_option <= 0:
                        self.menu_option = len(self.menu_options) - 1
                    else:
                        self.menu_option -= 1
                elif event.key == K_DOWN:
                    if self.menu_option >= len(self.menu_options) - 1:
                        self.menu_option = 0
                    else:
                        self.menu_option += 1
                elif event.key == K_RETURN:
                    if self.menu_option == 0:
                        # pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                        # self.parent.gamestate = GameStateRunning(self.parent)
                        # control_set = (K_a, K_w, K_d)
                        # control_set = (K_LEFT, K_UP, K_RIGHT)
                        self.context["gamestate"] = GameStateRunning(self.context, self.screen, self)
                    elif self.menu_option == 1:
                        self.context["gamestate"] = GameStateRunningMulti(self.context, self.screen, self)
                    elif self.menu_option == 2:
                        self.context["gamestate"] = GameStateEditor(self.context, self.screen, self)
                    elif self.menu_option == 3:
                        sys.exit(0)
                    else:
                        pass

    def draw(self):
        """
        Method called each frame to (re)draw UI
        :return:
        """
        self.screen.blit(Assets.background, (0, 0))
        self.screen.blit(self.title, (LEVEL_WIDTH / 2 - self.title.get_rect().width / 2, 30))

        o_max_width = max([option.get_rect().width for option in self.menu_options])
        width = o_max_width + MENU_PADDING[0] * 2
        height = self.menu_options[0].get_rect().height + MENU_PADDING[1] * 2
        x = LEVEL_WIDTH / 2 - width / 2
        y = LEVEL_HEIGHT / 2 - (height * len(self.menu_options)) / 2
        counter = 0
        for option in self.menu_options:
            if counter == self.menu_option:
                used_color = MENU_COLORS[1]
            else:
                used_color = MENU_COLORS[0]
            draw.rect(self.screen, used_color, (x, y + counter * height, width, height), 0)
            option_x = x + MENU_PADDING[0] + (o_max_width - option.get_rect().width) / 2
            self.screen.blit(option, (option_x, y + height * counter + MENU_PADDING[1]))
            counter += 1

        authors_rect = self.authors.get_rect()
        self.screen.blit(self.authors, (LEVEL_WIDTH - authors_rect.width,
                                        LEVEL_HEIGHT - authors_rect.height))

    def update(self):
        """
        This state does not really need to update any objects, because it operates
        solely on the input events
        :return:
        """
        pass
