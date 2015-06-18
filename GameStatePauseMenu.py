"""
This file contains the Pause Menu GameState
"""
import sys
import pygame
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_UP, K_DOWN, K_RETURN, K_ESCAPE
from gamedata import Assets
from constants import MENU_COLORS, MENU_PADDING, LEVEL_WIDTH, LEVEL_HEIGHT


class GameStatePauseMenu(object):
    """
    Pause Menu GameState. Available in Running GameState by pressing Esc
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
        self.context = context
        self.screen = screen
        self.menu_option = 0
        self.menu_options = []
        self.font = Assets.menu_font
        self.menu_options.append(self.font.render("RESUME GAME", 1, (255, 255, 255)))
        self.menu_options.append(self.font.render("RESTART LEVEL", 1, (255, 255, 255)))
        self.menu_options.append(self.font.render("EXIT TO MENU", 1, (255, 255, 255)))
        self.overlay_drawn = False
        self.prev_state = prev_state

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
                        self.context["gamestate"] = self.prev_state
                    elif self.menu_option == 1:
                        self.prev_state.start_level(self.prev_state.level_number)
                        self.context["gamestate"] = self.prev_state
                    elif self.menu_option == 2:
                        self.context["gamestate"] = self.prev_state.prev_state

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.context["gamestate"] = self.prev_state

    def draw(self):
        """
        Method called each frame to (re)draw the objects and UI
        :return:
        """
        if not self.overlay_drawn:
            overlay = pygame.Surface((LEVEL_WIDTH, LEVEL_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.overlay_drawn = True
            self.screen.blit(overlay, (0, 0))

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
            pygame.draw.rect(self.screen, used_color, (x, y + counter * height, width, height), 0)
            option_x = x + MENU_PADDING[0] + (o_max_width - option.get_rect().width) / 2
            self.screen.blit(option, (option_x, y + height * counter + MENU_PADDING[1]))
            counter += 1

    def update(self):
        """
        This state does not really need to update any objects, because it operates
        solely on the input events
        :return:
        """
        pass
