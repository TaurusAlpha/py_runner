import pygame
from dotenv import load_dotenv
import os
import logging

class Level(pygame.sprite.Sprite):
    def __init__(self, level_path: str):
        super().__init__()
        self.logger = logging.getLogger()
        self.level = self.init_level()
        # self.bg = self.bg.convert()
        self.level_pos_start = 0
        self.level_pos_end = self.level.get_width()


    def get_level(self):
        return [self.level_pos_start, self.level_pos_end]
    

    def get_level_size(self):
        return pygame.Surface.get_rect(self.level)
    

    def init_level(self) -> pygame.Surface:
        if os.getenv('BG'):
            return pygame.image.load(os.getenv('BG'), 'Background').convert_alpha()
        else:
            self.logger.error('BG variable not found in config.env')
            return pygame.Surface((0,0), masks="BLACK")

    
    def move(self, speed: int) -> None:
        self.level_pos_start -= speed
        self.level_pos_end -= speed
        if self.level_pos_start < self.level.get_width() * -1:
            self.level_pos_start = self.level.get_width()
        if self.level_pos_end < self.level.get_width() * -1:
            self.level_pos_end = self.level.get_width()
