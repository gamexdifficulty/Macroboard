import pygame
from data.classes.text import *

class Input:
    def __init__(self,engine,pos,size,text) -> None:
        self.engine = engine

        self.pos = pos
        self.size = size

        self.percentage = 0

        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.rect_small = pygame.Rect(self.rect.x+4,self.rect.y+4,self.rect.w-8,self.rect.h-8)

        self.selected = False

        self.text_id = text
        self.text = Text(self.engine,self.text_id,pygame.Rect(self.rect.x,self.rect.y,self.rect.w,self.rect.h))

        self.engine.inputs.append(self)

    def reposition(self):
        self.rect = pygame.Rect(self.pos[0]+self.engine.window_offset[0],self.pos[1]+self.engine.window_offset[1],self.size[0],self.size[1])
        self.rect_small = pygame.Rect(self.rect.x+4,self.rect.y+4,self.rect.w-8,self.rect.h-8)
        self.text.reposition()

    def update(self):
        if self.engine.input.get("accept"):
            if self.rect.collidepoint(self.engine.input.mouse.get_pos()):
                if self.engine.select_overlay != None:
                    if not(self.engine.select_overlay.select_rect.collidepoint(self.engine.input.mouse.get_pos())):
                        self.selected = True
                        self.engine.input_text = self.text.text
                else:
                    self.selected = True
                    self.engine.input_text = self.text.text

        if self.selected:
            self.text = Text(self.engine,self.engine.input_text,pygame.Rect(self.rect.x,self.rect.y,self.rect.w,self.rect.h))
            if self.engine.input.get("accept") and not self.rect.collidepoint(self.engine.input.mouse.get_pos()):
                self.selected = False

    def draw(self):
        if self.selected:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect,border_radius=8)
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect_small,border_radius=4)
        else:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect,border_radius=8)
        self.text.draw()