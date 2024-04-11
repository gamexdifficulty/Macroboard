import os
import pygame
from data.classes.text import *

class Color:
    def __init__(self,engine,pos,size,function,color=[0,0,0]) -> None:
        self.engine = engine

        self.pos = pos
        self.size = size

        self.percentage = 0

        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])

        self.rect_slider_outline = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-20,self.rect.w-40),0),self.rect.y-8,40,self.rect.h+16)
        self.rect_slider_fill = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-16,self.rect.w-36),4),self.rect.y-4,32,self.rect.h+8)

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
        self.color = color
        self.last_color = color
        self.last_message = ""
        
        self.function = function

        self.selected = False

        self.engine.colors.append(self)

    def reposition(self):
        self.rect = pygame.Rect(self.pos[0]+self.engine.window_offset[0],self.pos[1]+self.engine.window_offset[1],self.size[0],self.size[1])
        self.rect_slider_outline = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-20,self.rect.w-40),0),self.rect.y-8,40,self.rect.h+16)
        self.rect_slider_fill = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-16,self.rect.w-36),4),self.rect.y-4,32,self.rect.h+8)
    
    def set_color(self,color:list):
        self.percentage = (max(0, min(pygame.Color(color[0],color[1],color[2]).hsla[0]/360, 1)))
        color = pygame.Color(0)
        color.hsla = (int(self.percentage * 360), 100, 50, 100)
        self.color = [color.r,color.g,color.b]
        self.rect_slider_outline = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-20,self.rect.w-40),0),self.rect.y-8,40,self.rect.h+16)
        self.rect_slider_fill = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-16,self.rect.w-36),4),self.rect.y-4,32,self.rect.h+8)

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
            self.percentage = (self.engine.input.mouse.get_pos()[0] - self.rect.x) / self.pwidth
            self.percentage = (max(0, min(self.percentage, 1)))
            color = pygame.Color(0)
            color.hsla = (int(self.percentage * 360), 100, 50, 100)
            self.color = [color.r,color.g,color.b]
            self.rect_slider_outline = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-20,self.rect.w-40),0),self.rect.y-8,40,self.rect.h+16)
            self.rect_slider_fill = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-16,self.rect.w-36),4),self.rect.y-4,32,self.rect.h+8)
            if self.color != self.last_color:
                self.function(self.engine,self.color)
                self.last_color = self.color

    def draw(self):
        self.engine.window.render(self.color_sprite,[self.rect.x,self.rect.y])
        if self.selected:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect_slider_outline,border_radius=4)
            pygame.draw.rect(self.engine.window.main_surface,self.color,self.rect_slider_fill,border_radius=2)
        else:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect_slider_outline,border_radius=4)
            pygame.draw.rect(self.engine.window.main_surface,self.color,self.rect_slider_fill,border_radius=2)