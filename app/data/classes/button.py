import pygame
from data.classes.text import *

class Button:
    def __init__(self,engine,pos,size,function,id,text="",flag=None) -> None:
        self.engine = engine
        self.pos = pos
        self.size = size
        self.function = function
        self.id = id
        self.flag = flag
        self.rect = pygame.Rect(self.pos[0]+self.engine.window_offset[0],self.pos[1]+self.engine.window_offset[1],self.size[0],self.size[1])
        self.rect_small = pygame.Rect(self.rect.x+4,self.rect.y+4,self.rect.w-8,self.rect.h-8)
        self.text = Text(self.engine,text,self.rect)
        self.engine.buttons.append(self)

    def reposition(self):
        self.rect = pygame.Rect(self.pos[0]+self.engine.window_offset[0],self.pos[1]+self.engine.window_offset[1],self.size[0],self.size[1])
        self.rect_small = pygame.Rect(self.pos[0]+self.engine.window_offset[0]+4,self.pos[1]+self.engine.window_offset[1]+4,self.size[0]-8,self.size[1]-8)
        self.text.reposition()

    def update(self):
        if self.rect.collidepoint(self.engine.input.mouse.get_pos()):
            if self.engine.input.get("accept"):
                if self.engine.select_overlay == None:
                    self.function(self.id)
                elif not(self.engine.select_overlay.select_rect.collidepoint(self.engine.input.mouse.get_pos())):
                    self.function(self.id)

    def draw(self):
        if self.flag == 1:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect,border_radius=8)
        else:
            if self.rect.collidepoint(self.engine.input.mouse.get_pos()):
                if self.engine.select_overlay == None:
                    pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect,border_radius=8)
                    pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect_small,border_radius=4)
                elif not(self.engine.select_overlay.select_rect.collidepoint(self.engine.input.mouse.get_pos())):
                    pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect,border_radius=8)
                    pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect_small,border_radius=4)
                else:
                    pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect,border_radius=8)
            else:
                pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect,border_radius=8)
        self.text.draw()