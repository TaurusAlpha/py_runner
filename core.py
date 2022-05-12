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
        self.dt = 0
        dotenv_path = join(dirname(__file__), 'config.env')
        load_dotenv(dotenv_path)
        self.bg = pygame.image.load(os.getenv('BG'), "Background")
        self.display = pygame.display.set_mode((self.bg.get_width(), self.bg.get_height()), pygame.DOUBLEBUF | pygame.HWACCEL)
        self.bg = self.bg.convert()
        self.bgX = 0
        self.bgY = self.bg.get_width()
        self.fps = int(os.getenv('FPS'))
        self.player = Player(self.load_player())    
        self.player_group = pygame.sprite.Group(self.player)

    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False


    def update(self) -> None:
        self.move_bg()
        self.dt = self.clock.tick(self.fps) / 1000
        self.player_group.update(self.dt)
        self.clock.tick(self.fps)


    def render(self) -> None:
        self.display.blit(self.bg, (self.bgX,0))
        self.display.blit(self.bg,(self.bgY,0))
        self.player_group.draw(self.display)
        pygame.display.update()

    
    def cleanup(self) -> None:
        pygame.quit()


    def run(self) -> None:
        self.init()
        while self.running:
            for event in pygame.event.get():
                self.event(event)
            self.update()
            self.render()
        self.cleanup()
    

    def move_bg(self) -> None:
        self.bgX -= self.player.player_speed
        self.bgY -= self.player.player_speed
        if self.bgX < self.bg.get_width() * -1:
            self.bgX = self.bg.get_width()
        if self.bgY < self.bg.get_width() * -1:
            self.bgY = self.bg.get_width()
    

    def load_player(self) -> List:
        images = []
        for i in reversed(range(1,10)):
            image = pygame.image.load(os.getenv(f'PLAYER_SPRITE{i}'), f'Player{i}').convert()
            image.set_colorkey('WHITE')
            images.append(image)
        return images
