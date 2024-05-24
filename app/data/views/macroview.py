import os
import json
import pygame
from data.classes.text import Text
from data.classes.button import Button
from data.functions.reactions import delete_macro,edit_macro_key

class MacroView:
    def __init__(self,engine,index,config) -> None:
        self.engine = engine
        self.index = index
        self.type = config["type"]
        self.trigger = config["trigger"]
        self.data = config["data"] 
        self.rect = pygame.Rect(694,128+72*index-1,472,64)
        self.pos = [self.rect.x,self.rect.y]
        self.index_text = Text(self.engine,str(self.index)+".",pygame.Rect(630,128+72*index-1,48,64),True,False)
        self.delete_button = Button(self.engine,[630+64+512+32-64,128+72*self.index-1],[64,64],delete_macro,index,flag=2)
        self.delete_sprite = pygame.image.load(os.path.join("data","sprites","delete.png")).convert_alpha()
        self.type_sprite = self.engine.typeicon_sprites[self.type]
        self.drag_rect = pygame.Rect(self.rect.x+408,self.rect.y,64,64)
        self.drag_sprite = pygame.image.load(os.path.join("data","sprites","move.png")).convert_alpha()
        if self.type == 0:
            keytext = ""
            for key in config["data"]:
                text = ""
                if key <= 0x10ffff:
                    if not chr(key).isspace():
                        text = chr(key)
                    else:
                        text = pygame.key.name(key)
                else:
                    text = pygame.key.name(key)

                if text.isspace() or text == "":
                    with open(os.path.join("data","keycodes.json"),"r+",encoding="UTF-8") as f:
                        keycodes = json.load(f)
                        if str(key) not in keycodes:
                            text = "???"
                        else:
                            text = keycodes[str(key)]

                if keytext != "":
                    text = " + "+text

                keytext += text
            if len(keytext) > 32:
                keytext = keytext[:32]+"..."
            self.previewtext = Text(self.engine,keytext,pygame.Rect(630+160+16,128+72*index-1,256,64),translate=False)
        self.reposition()

    def reposition(self):
        self.rect = pygame.Rect(self.pos[0]+self.engine.window_offset[0],self.pos[1]+self.engine.window_offset[1],self.rect.w,self.rect.h)
        self.drag_rect = pygame.Rect(self.pos[0]+self.engine.window_offset[0]+408,self.pos[1]+self.engine.window_offset[1],self.rect.w,self.rect.h)

    def update(self):
        self.delete_button.update()
        if self.engine.input.get("accept") and self.rect.collidepoint(self.engine.input.mouse.get_pos()) and not self.drag_rect.collidepoint(self.engine.input.mouse.get_pos()):
            edit_macro_key(self.engine,{"trigger":self.trigger,"data":self.data},self.index)

    def draw(self):
        self.index_text.draw()
        pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect,border_radius=8)
        self.engine.window.render(self.type_sprite,(self.rect.x+8,self.rect.y))
        self.previewtext.draw()
        self.engine.window.render(self.drag_sprite,(self.drag_rect.x,self.drag_rect.y))
        self.delete_button.draw()
        self.engine.window.render(self.delete_sprite,(self.rect.x+self.rect.w+8,self.rect.y))
        if self.rect.collidepoint(self.engine.input.mouse.get_pos()):
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect,4,8)