from typing import List
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, player_images: List) -> None:
        super().__init__()
        self.player_pos = pygame.Vector2(50, 266)
        self.images = player_images
        self.image_index = 0
        self.image = player_images[self.image_index]
        self.player_speed = 3.7
        self.rect = self.image.get_rect(topleft=self.player_pos)
        self.animation_time = 30
        self.current_time = 0
        self.diry = 0


    def update(self, delta_time):
        self.current_time += delta_time
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

