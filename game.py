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
local_menu = LocalMenu(window)

is_running = True

#can be converted to event dictionary types
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if game_state == MENU:
            if menu.practice_button.is_clicked(event):
                game_state = PRACTICE
            elif menu.local_button.is_clicked(event):
                game_state = LOCAL_MENU
            elif menu.multiplayer_button.is_clicked(event):
                game_state = MULTIPLAYER

        elif game_state == PRACTICE:
            practice.handle_ui_events(event)
            if practice.menu_button.is_clicked(event):
                game_state = MENU
        elif game_state == LOCAL_MENU:
            if local_menu.back_button.is_clicked(event):
                game_state = MENU
            elif local_menu.user_button.is_clicked(event):
                local_game.set_vs_cpu(False)
                game_state = LOCAL
            elif local_menu.cpu_button.is_clicked(event):
                local_game.set_vs_cpu(True)
                game_state = LOCAL
        elif game_state == LOCAL:
            local_game.handle_ui_events(event)
            if local_game.menu_button.is_clicked(event):
                game_state = MENU
            elif local_game.timer.time_up and local_game.rematch_button.is_clicked(event):
                local_game.reset_match()
    
    window.fill(BLACK) #fills screen to after event loop
    
    if game_state == MENU:
        menu.draw_menu(window)
    elif game_state == PRACTICE:
        practice.update_practice()
        practice.draw(window)
    elif game_state == LOCAL_MENU:
        local_menu.draw_local_menu(window)
    elif game_state == LOCAL:
        local_game.update_local()
        local_game.draw_local(window)
    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


