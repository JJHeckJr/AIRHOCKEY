import pygame 

from constants import *
from local_game import LocalGame
from local_menu import LocalMenu
from menu import Menu
from practice import Practice


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Air Hockey')

clock = pygame.time.Clock()

game_state = MENU
menu = Menu(window)
practice = Practice(window)
local_game = LocalGame(window)
local_menu = LocalMenu(window, local_game)

screens = {
    MENU: menu,
    PRACTICE: practice,
    LOCAL_MENU: local_menu,
    LOCAL: local_game,
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

    window.fill(BLACK)
    screen = screens.get(game_state)
    if screen is not None:
        screen.update()
        screen.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

        