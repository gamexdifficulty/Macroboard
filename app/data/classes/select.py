import os
import pygame
from data.classes.text import *

class Select:
    def __init__(self,engine,pos,size,options=[""],flag=None,selected=0) -> None:
        self.engine = engine
        self.pos = pos
        self.size = size
        self.flag = flag
        self.options = options
        self.selected = selected
        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.rect_small = pygame.Rect(self.rect.x+4,self.rect.y+4,self.rect.w-8,self.rect.h-8)
        self.select_rect = pygame.Rect(self.rect.x,self.rect.y+self.rect.h,self.rect.w,(self.rect.h-16)*len(self.options))
        self.select_rect_small = pygame.Rect(self.select_rect.x+4,self.select_rect.y+4,self.select_rect.w-8,self.select_rect.h-8)
        self.select_sprite = pygame.image.load(os.path.join("data","sprites","select.png")).convert_alpha()
        self.sprite_pos = [pos[0]+self.size[0]-48,pos[1]]
        self.color = [200,34,234]
        self.color_rect = pygame.Rect(self.rect.x+8,self.rect.y+8,self.rect.w-16,self.rect.h-16)
        self.text = Text(self.engine,self.options[self.selected],pygame.Rect(self.rect.x,self.rect.y,self.rect.w-32,self.rect.h))
        self.open = False
        self.options_texts = []
        for y,option in enumerate(self.options):
            self.options_texts.append(Text(self.engine,option,pygame.Rect(self.rect.x,self.rect.y+self.rect.h+self.rect.y/len(self.options)*y,self.rect.w-32,self.rect.h)))
        self.engine.switches.append(self)
        if len(self.options) > 1:
            self.open = True

    def reposition(self):
        self.rect = pygame.Rect(self.pos[0]+self.engine.window_offset[0],self.pos[1]+self.engine.window_offset[1],self.size[0],self.size[1])
        self.rect_small = pygame.Rect(self.pos[0]+self.engine.window_offset[0]+4,self.pos[1]+self.engine.window_offset[1]+4,self.size[0]-8,self.size[1]-8)
        self.text.reposition()

    def update(self):
        if self.engine.input.get("accept"):
            if self.rect.collidepoint(self.engine.input.mouse.get_pos()):
                self.open = not self.open
            elif self.select_rect.collidepoint(self.engine.input.mouse.get_pos()):
                for y,option in enumerate(self.options):
                    if pygame.Rect(self.rect.x,self.rect.y+self.rect.h+self.rect.y/len(self.options)*y,self.rect.w-32,self.rect.h).collidepoint(self.engine.input.mouse.get_pos()):
                        self.selected = y
                        self.text = self.text = Text(self.engine,self.options[self.selected],pygame.Rect(self.rect.x,self.rect.y,self.rect.w-32,self.rect.h))
                        self.open = False
            else:
                self.open = False

    def draw(self):
        if self.open:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect,border_top_left_radius=8,border_top_right_radius=8)
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.select_rect,border_bottom_left_radius=8,border_bottom_right_radius=8)
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.select_rect_small,border_bottom_left_radius=4,border_bottom_right_radius=4)
            if self.flag == None:
                self.engine.window.render(pygame.transform.rotate(self.select_sprite,180),self.sprite_pos)
            if self.flag == 1:
                pygame.draw.rect(self.engine.window.main_surface,self.color,self.color_rect,border_radius=4)
            for text in self.options_texts:
                text.draw()
        else:
            if self.rect.collidepoint(self.engine.input.mouse.get_pos()):
                pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect,border_radius=8)
                pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect_small,border_radius=4)
            else:
                pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect,border_radius=8)
            if self.flag == None:
                self.engine.window.render(self.select_sprite,self.sprite_pos)
            if self.flag == 1:
                pygame.draw.rect(self.engine.window.main_surface,self.color,self.color_rect,border_radius=4)
        self.text.draw()