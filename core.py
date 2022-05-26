from typing import List
import pygame
import os
from dotenv import load_dotenv
from os.path import join, dirname

from player import Player


class Core:
    def __init__(self) -> None:
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        self.running = False
        self.clock = pygame.time.Clock()


    def init(self) -> None:
        self.running = True
        dotenv_path = join(dirname(__file__), 'config.env')
        load_dotenv(dotenv_path)
        self.bg = pygame.image.load(os.getenv('BG'), "Background")
        self.display = pygame.display.set_mode((self.bg.get_width(), self.bg.get_height()), pygame.DOUBLEBUF | pygame.HWACCEL)
        self.bg = self.bg.convert()
        self.first_bg_pos = 0
        self.second_bg_pos = self.bg.get_width()
        self.fps = int(os.getenv('FPS'))
        self.player = Player(self.load_player())    
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.ground = 266
        self.jump_height = 366


    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_SPACE:
                self.player_jump()


    def update(self, delta_time) -> None:
        self.move_bg()
        self.player_group.update(delta_time)


    def render(self) -> None:
        self.display.blit(self.bg, (self.first_bg_pos,0))
        self.display.blit(self.bg, (self.second_bg_pos,0))
        self.player_group.draw(self.display)
        pygame.display.update()

    
    def cleanup(self) -> None:
        pygame.quit()


    def run(self) -> None:
        self.init()
        while self.running:
            delta_time = self.clock.tick(self.fps)
            for event in pygame.event.get():
                self.event(event)
            self.update(delta_time)
            self.render()
        self.cleanup()
    

    def move_bg(self) -> None:
        self.first_bg_pos -= self.player.player_speed
        self.second_bg_pos -= self.player.player_speed
        if self.first_bg_pos < self.bg.get_width() * -1:
            self.first_bg_pos = self.bg.get_width()
        if self.second_bg_pos < self.bg.get_width() * -1:
            self.second_bg_pos = self.bg.get_width()
    

    def load_player(self) -> List:
        images = []
        for i in reversed(range(1,10)):
            image = pygame.image.load(os.getenv(f'PLAYER_SPRITE{i}'), f'Player{i}').convert()
            image.set_colorkey('WHITE')
            images.append(image)
        return images


    def player_jump(self) -> None:
        self.player.rect.move_ip([50, 366])
