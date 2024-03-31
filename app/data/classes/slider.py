import pygame
from data.classes.text import *

class Slider:
    def __init__(self,engine,pos,size) -> None:
        self.engine = engine

        self.pos = pos
        self.size = size

        self.percentage = 0

        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.rect_slider_outline = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-20,self.rect.w-40),0),self.rect.y-8,40,self.rect.h+16)
        self.rect_slider_fill = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-16,self.rect.w-36),4),self.rect.y-4,32,self.rect.h+8)

        self.selected = False

        self.engine.sliders.append(self)

    def reposition(self):
        self.rect = pygame.Rect(self.pos[0]+self.engine.window_offset[0],self.pos[1]+self.engine.window_offset[1],self.size[0],self.size[1])
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
            self.percentage = (self.engine.input.mouse.get_pos()[0] - self.rect.x) / self.rect.w
            self.percentage = (max(0, min(self.percentage, 1)))
            self.rect_slider_outline = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-20,self.rect.w-40),0),self.rect.y-8,40,self.rect.h+16)
            self.rect_slider_fill = pygame.Rect(self.rect.x+max(min(self.percentage*self.rect.w-16,self.rect.w-36),4),self.rect.y-4,32,self.rect.h+8)

    def draw(self):
        pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect,border_radius=8)
        if self.selected:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect_slider_outline,border_radius=4)
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect_slider_fill,border_radius=2)
        else:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect_slider_outline,border_radius=4)
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect_slider_fill,border_radius=2)