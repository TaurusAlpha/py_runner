import pygame

pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, x = 10, y = 10) -> None:
    debug_display = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'Black')
    debug_rect = debug_display.get_rect(topleft = (x,y))
    debug_display.blit(debug_surf,debug_rect)
