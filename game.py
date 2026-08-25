import pygame 

from constants import *
from local_game import LocalGame
from local_menu import LocalMenu
from menu import Menu
from practice import Practice
from settings import GameSettings, SettingsMenu


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Air Hockey')

clock = pygame.time.Clock()
game_settings = GameSettings()
game_state = MENU
menu = Menu(window)
practice = Practice(window)
local_game = LocalGame(window, game_settings)
local_menu = LocalMenu(window, local_game)
settings_menu = SettingsMenu(window, game_settings)

screens = {
    MENU: menu,
    PRACTICE: practice,
    LOCAL_MENU: local_menu,
    LOCAL: local_game,
    SETTINGS: settings_menu
}

is_running = True

#can be converted to event dictionary types
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        screen = screens.get(game_state)
        if screen is not None:
            next_state = screen.handle_ui_events(event)
            if next_state is not None:
                game_state = next_state

                if game_state == PRACTICE:
                    practice.reset_match()
                elif game_state == LOCAL:
                    local_game.reset_match()

    window.fill(BLACK)
    screen = screens.get(game_state)
    if screen is not None:
        screen.update()
        screen.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

        