from typing import List
import pygame
from dotenv import load_dotenv
import os
import logging


class Player(pygame.sprite.Sprite):
    def __init__(self, player_frames: str, speed: int, ground: int) -> None:
        super().__init__()
        self.logger = logging.getLogger()
        load_dotenv(player_frames)

        self.frames = self.load_player()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.jump_up = pygame.transform.rotate(self.frames[len(self.frames)-1], 30.0).convert_alpha()
        self.jump_air = self.frames[len(self.frames)-1].convert_alpha()
        self.jump_down = pygame.transform.rotate(self.frames[len(self.frames)-1], -30.0).convert_alpha()

        self.player_pos = pygame.Vector2(50, ground)
        self.rect = pygame.Surface.get_rect(self.image, bottomleft=self.player_pos)
        self.animation_time = 30
        self.current_time = 0
        self.running = True
        self.speed = speed
        self.ground = ground
        self.gravity = 0
        self.air_time = 0


    def update(self, delta_time) -> None:
        self.__animation_state(delta_time)


    def __animation_state(self, dt) -> None:
        if self.rect.bottom < self.ground:
            if self.gravity < 0:
                self.image = self.jump_up
                self.gravity += 1
            elif self.gravity == 0 and self.air_time > 0:
                self.image = self.jump_air
                self.air_time -= dt
            else:
                self.image = self.jump_down
                self.gravity += 1
            self.rect = self.rect.move(0, self.gravity)
        else:
            self.current_time += dt*self.speed
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]


    def load_player(self) -> List:
        images = []
        for i in reversed(range(1,10)):
            image = pygame.image.load(os.getenv(f'PLAYER_SPRITE{i}'), f'Player_Sprite_{i}').convert_alpha()
            image.set_colorkey('WHITE')
            images.append(image)
        return images


    def isRunning(self) -> bool:
        return self.running
     

    def set_speed(self, speed) -> None:
        self.speed = speed


    def jump(self):
        self.gravity = -20
        self.air_time = 20
        self.rect.bottom = self.ground-1
