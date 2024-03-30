import os
import pygame
from data.classes.text import *

class Color:
    def __init__(self,engine,pos,size) -> None:
        self.engine = engine

        self.pos = pos
        self.size = size

        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.rect_small = pygame.Rect(self.rect.x+4,self.rect.y+4,self.rect.w-8,self.rect.h-8)

        self.color_sprite = pygame.Surface((self.rect.w, self.rect.h))
        self.color_sprite.fill((255, 255, 255))
        self.pwidth = self.rect.w
        for i in range(self.pwidth):
            color = pygame.Color(0)
            color.hsla = (int(360*i/self.pwidth), 100, 50, 100)
            pygame.draw.rect(self.color_sprite, color, (i, 0, 1, self.rect.h))

        self.round_sprite = pygame.Surface((self.rect.w,self.rect.h)).convert_alpha()
        self.round_sprite.fill((0,0,0))
        pygame.draw.rect(self.round_sprite,(255,255,255),pygame.Rect(0,0,self.rect.w,self.rect.h),border_radius=8)
        self.round_sprite.set_colorkey((255,255,255))
        self.color_sprite.blit(self.round_sprite,(0,0))
        self.color_sprite.set_colorkey((0,0,0))
        self.p = 0
        self.color = [0,0,0]
        self.last_message = ""

        self.selected = False

    def reposition(self):
        self.rect = pygame.Rect(self.pos[0]+self.engine.window_offset[0],self.pos[1]+self.engine.window_offset[1],self.size[0],self.size[1])
        self.rect_small = pygame.Rect(self.pos[0]+self.engine.window_offset[0]+4,self.pos[1]+self.engine.window_offset[1]+4,self.size[0]-8,self.size[1]-8)

    def update(self):
        if self.engine.input.get("released"):
            self.selected = False
        elif self.engine.input.get("accept"):
            if self.rect.collidepoint(self.engine.input.mouse.get_pos()):
                if self.engine.select_overlay != None:
                    if not(self.engine.select_overlay.select_rect.collidepoint(self.engine.input.mouse.get_pos())):
                        self.selected = True
                else:
                    self.selected = True

        if self.selected:
            self.p = (self.engine.input.mouse.get_pos()[0] - self.rect.x) / self.pwidth
            self.p = (max(0, min(self.p, 1)))
            color = pygame.Color(0)
            color.hsla = (int(self.p * 360), 100, 50, 100)
            self.color = [color.r,color.g,color.b]

    def draw(self):
        self.engine.window.render(self.color_sprite,[self.rect.x,self.rect.y])
        if self.selected:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,pygame.Rect(self.rect.x+self.p*self.rect.w-16-4,self.rect.y-4-4,32+8,self.rect.h+8+8),border_radius=4)
            pygame.draw.rect(self.engine.window.main_surface,self.color,pygame.Rect(self.rect.x+self.p*self.rect.w-16,self.rect.y-4,32,self.rect.h+8),border_radius=2)
        else:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,pygame.Rect(self.rect.x+self.p*self.rect.w-16-4,self.rect.y-4-4,32+8,self.rect.h+8+8),border_radius=4)
            pygame.draw.rect(self.engine.window.main_surface,self.color,pygame.Rect(self.rect.x+self.p*self.rect.w-16-4,self.rect.y-4-4,32+8,self.rect.h+8+8),border_radius=2)