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
        self.rect = pygame.Rect(630+64,128+72*index-1,512+32-64-8,64)
        self.index_text = Text(self.engine,str(self.index)+".",pygame.Rect(630,128+72*index-1,48,64),True,False)
        self.delete_button = Button(self.engine,[630+64+512+32-64,128+72*index-1,],[64,64],delete_macro,index,"X",flag=2)
        self.type_text = Text(self.engine,["Key","Text","Layer","Pos","Button","EXE"][self.type],pygame.Rect(630+64,128+72*index-1,96,64),translate=False)
        self.drag_rect = pygame.Rect(630+64+512+32-64-64-8,128+72*index-1,64,64)
        if self.type == 0:
            self.previewtext = Text(self.engine,engine.translate("key_combinations")+" "+str(len(self.data)),pygame.Rect(630+160,128+72*index-1,256,64),translate=False)

    def update(self):
        self.delete_button.update()
        if self.engine.input.get("accept") and self.rect.collidepoint(self.engine.input.mouse.get_pos()) and not self.drag_rect.collidepoint(self.engine.input.mouse.get_pos()):
            edit_macro_key(self.engine,{"trigger":self.trigger,"data":self.data},self.index)

    def draw(self):
        self.index_text.draw()
        pygame.draw.rect(self.engine.window.main_surface,self.engine.color_element,self.rect,border_radius=8)
        self.type_text.draw()
        self.previewtext.draw()
        pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.drag_rect,4,8)
        self.delete_button.draw()
        if self.rect.collidepoint(self.engine.input.mouse.get_pos()):
            pygame.draw.rect(self.engine.window.main_surface,self.engine.color_highlight,self.rect,4,8)