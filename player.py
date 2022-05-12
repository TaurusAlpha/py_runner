from email.mime import image
from typing import List
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, player_images: List) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.player_pos = pygame.Vector2(50, 266)
        self.images = player_images
        self.image_index = 0
        self.image = player_images[self.image_index]
        self.image_size = (self.image.get_width(), self.image.get_height())
        self.player_speed = 3.7
        self.rect = pygame.Rect(self.player_pos, self.image_size)
        self.animation_time = 0.05
        self.current_time = 0


    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

        #self.rect.move_ip(self.player_speed,0)


    def update(self, dt):
        # Switch between the two update methods by commenting/uncommenting.
        self.update_time_dependent(dt)
