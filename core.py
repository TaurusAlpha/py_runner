import pygame
import os
from dotenv import load_dotenv
from os.path import join, dirname
import time
from player import Player
import logging
from debug import debug as dbg


class Core():
    def __init__(self) -> None:
        self.logger = logging.getLogger()
        self.load_env()

        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(eval(os.getenv('SCREEN_RES')), pygame.DOUBLEBUF | pygame.HWACCEL)

        self.bg = self.init_bg()
        self.level_pos_start = 0
        self.level_pos_end = self.screen.get_width()
        
        self.fps = int(os.getenv('FPS'))
        self.speed = int(os.getenv('SPEED'))
        self.ground = 600

        self.player = Player(self.dotenv_path, self.speed, self.ground)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.running = True

 
    def init_bg(self) -> pygame.surface.Surface:
        if os.getenv('BG'):
            bg = pygame.image.load(os.getenv('BG'), 'Background').convert_alpha()
            bg = pygame.transform.scale(bg, (self.screen.get_width(), self.screen.get_height()))
            return bg
        else:
            self.logger.error('BG variable not found in config.env')
            self.cleanup()


    def load_env(self):
        self.dotenv_path = join(dirname(__file__), 'config.env')
        if not load_dotenv(self.dotenv_path):
            self.logger.error('config.env file not found')
            self.cleanup()


    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.VIDEORESIZE:
            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            self.bg = pygame.transform.scale(self.bg, (self.screen.get_width(), self.screen.get_height()))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_SPACE:
                self.player.jump()


    def update(self, delta_time) -> None:
        pygame.display.update()
        self.player_group.update(delta_time)


    def render(self) -> None:
        self.bg_scroll()
        self.screen.blit(self.bg, (self.level_pos_start, 0))
        self.screen.blit(self.bg, (self.level_pos_end, 0))
        self.player_group.draw(self.screen)

    
    def bg_scroll(self) -> None:
        self.level_pos_start -= self.speed
        self.level_pos_end -= self.speed
        if self.level_pos_start <= -self.screen.get_width():
            self.level_pos_start = self.screen.get_width()
        if self.level_pos_end <= -self.screen.get_width():
            self.level_pos_end = self.screen.get_width()
        

    def cleanup(self) -> None:
        self.running = False
        pygame.quit()


    def run(self) -> None:
        prev_time = time.time()
        while self.running:
            delta_time = (time.time() - prev_time)*100
            prev_time = time.time()
            for event in pygame.event.get():
                self.event(event)            
            self.render()
            dbg(self.player.gravity)
            dbg((self.player.rect.bottom, self.player.rect.bottomright, self.ground), y=40)
            self.update(delta_time)
            self.clock.tick(self.fps)
        self.cleanup() 
