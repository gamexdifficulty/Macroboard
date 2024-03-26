import os
import pygame
from data.classes.text import *

class Select:
    def __init__(self,engine,pos,size,options=[""],flag=None,selected=0) -> None:
        self.engine = engine

        self.pos = pos
        self.size = size

        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.rect_small = pygame.Rect(self.rect.x+4,self.rect.y+4,self.rect.w-8,self.rect.h-8)

        self.options = options
        self.selected = selected
        
        self.select_rect = pygame.Rect(self.rect.x,self.rect.y+self.rect.h,self.rect.w,(self.rect.h-16)*len(self.options))
        self.select_rect_small = pygame.Rect(self.select_rect.x+4,self.select_rect.y+4,self.select_rect.w-8,self.select_rect.h-8)

        self.select_sprite = pygame.image.load(os.path.join("data","sprites","select.png")).convert_alpha()
        self.sprite_pos = [self.pos[0]+self.size[0]-48,self.pos[1]]

        self.text = Text(self.engine,self.options[self.selected],pygame.Rect(self.rect.x,self.rect.y,self.rect.w-32,self.rect.h))
        self.options_texts = []
        self.item_height = (self.select_rect.h-16)/len(self.options)
        for y,option in enumerate(self.options):
            self.options_texts.append(Text(self.engine,option,pygame.Rect(self.select_rect.x,self.select_rect.y+self.item_height*y+8,self.rect.w,self.item_height)))

        self.open = False
        self.flag = flag

        if self.flag == 1:
            self.select_rect = pygame.Rect(self.rect.x,self.rect.y+self.rect.h,256,48)
            self.color_size = [self.select_rect.w,self.select_rect.h]
            self.color_sprite = pygame.Surface((self.color_size[0], self.color_size[1]))
            self.color_sprite.fill((255, 255, 255))
            self.pwidth = self.color_size[0]
            for i in range(self.pwidth):
                color = pygame.Color(0)
                color.hsla = (int(360*i/self.pwidth), 100, 50, 100)
                pygame.draw.rect(self.color_sprite, color, (i, 0, 1, self.color_size[1]))
            self.p = 0
            self.color = [0,0,0]
        self.color_rect = pygame.Rect(self.rect.x+8,self.rect.y+8,self.rect.w-16,self.rect.h-16)

        self.engine.selects.append(self)

    def reposition(self):
        self.rect = pygame.Rect(self.pos[0]+self.engine.window_offset[0],self.pos[1]+self.engine.window_offset[1],self.size[0],self.size[1])
        self.rect_small = pygame.Rect(self.pos[0]+self.engine.window_offset[0]+4,self.pos[1]+self.engine.window_offset[1]+4,self.size[0]-8,self.size[1]-8)
        self.select_rect = pygame.Rect(self.rect.x,self.rect.y+self.rect.h,self.rect.w,(self.rect.h-16)*len(self.options))
        self.select_rect_small = pygame.Rect(self.select_rect.x+4,self.select_rect.y+4,self.select_rect.w-8,self.select_rect.h-8)
        self.sprite_pos = [self.pos[0]+self.size[0]-48+self.engine.window_offset[0],self.pos[1]+self.engine.window_offset[1]]
        self.color_rect = pygame.Rect(self.rect.x+8,self.rect.y+8,self.rect.w-16,self.rect.h-16)
        self.text.reposition()
        for text in self.options_texts:
            text.reposition()

    def update(self):
        if self.engine.input.get("accept"):
            if self.rect.collidepoint(self.engine.input.mouse.get_pos()):
                if self.engine.select_overlay == None:
                    self.open = not self.open
                elif not(self.engine.select_overlay.select_rect.collidepoint(self.engine.input.mouse.get_pos())):
                    self.open = not self.open
            elif self.select_rect.collidepoint(self.engine.input.mouse.get_pos()) and self.open:
                for y,text in enumerate(self.options_texts):
                    if self.flag == None:
                        if text.rect.collidepoint(self.engine.input.mouse.get_pos()):
                            self.selected = y
                            self.text = self.text = Text(self.engine,self.options[self.selected],pygame.Rect(self.rect.x,self.rect.y,self.rect.w-32,self.rect.h))
                            self.open = False
                    elif self.flag == 1:
                        self.p = (self.engine.input.mouse.get_pos()[0] - self.rect.x) / self.pwidth
                        print(self.p)
                        self.p = (max(0, min(self.p, 1)))
                        color = pygame.Color(0)
                        color.hsla = (int(self.p * 360), 100, 50, 100)
                        self.color = [color.r,color.g,color.b]
                    self.engine.input.reset("accept")
            else:
                self.open = False

            if self.open:
                self.engine.select_overlay = self
            else:
                if self.engine.select_overlay == self:
                    self.engine.select_overlay = None

        for y,text in enumerate(self.options_texts):
            if text.rect.collidepoint(self.engine.input.mouse.get_pos()):
                text.highlight = True
            else:
                text.highlight = False

    def draw(self):
        if self.open:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect,border_top_left_radius=8,border_top_right_radius=8)
            if self.flag == None:
                self.engine.window.render(pygame.transform.rotate(self.select_sprite,180),self.sprite_pos)
            if self.flag == 1:
                pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,[self.rect.x,self.rect.y+self.rect.h,self.color_size[0]+8,self.color_size[1]+8],border_bottom_left_radius=4,border_bottom_right_radius=4,border_top_right_radius=4)
                self.engine.window.render(self.color_sprite,[self.rect.x+4,self.rect.y+self.rect.h+4])
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
            if self.flag == None:
                self.engine.window.render(self.select_sprite,self.sprite_pos)
            if self.flag == 1:
                pygame.draw.rect(self.engine.window.main_surface,self.color,self.color_rect,border_radius=4)
        self.text.draw()

    def draw_select(self):
        if self.flag == None:
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.select_rect,border_bottom_left_radius=8,border_bottom_right_radius=8)
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.select_rect_small,border_radius=4)
        if self.flag == 1:
            pygame.draw.rect(self.engine.window.main_surface,self.color,self.color_rect,border_radius=4)
        for text in self.options_texts:
            text.draw()