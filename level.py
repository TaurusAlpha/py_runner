from typing import List
import pygame
import os
import logging
from random import randint

class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger()
        self.ground = int(os.getenv('GROUND'))
        self.width = int(os.getenv('SCREEN_WIDTH'))
        self.speed = int(os.getenv('SPEED'))

        self.frames = self.init_level()
        self.image = self.frames[0]
        self.obstacle_pos = pygame.Vector2(self.width+300, self.ground)
        self.rect = pygame.Surface.get_rect(self.image, bottomleft=self.obstacle_pos)
        

    def init_level(self) -> List[pygame.surface.Surface]:
        images = []
        for i in range(1,12):
            image = pygame.image.load(os.getenv(f'LEVEL_OBSTACLE{i}'), f'Obstacle_Sprite_{i}').convert_alpha()
            image.set_colorkey('WHITE')
            images.append(image)
        return images


    def update(self, delta_time) -> None:
        if self.rect.right < 0:
            self.image = self.frames[randint(0, len(self.frames)-1)]
            self.rect = pygame.Surface.get_rect(self.image, bottomleft=self.obstacle_pos)
        self.rect = self.rect.move(-self.speed, 0)
