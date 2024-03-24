import pygame

class Text:
    def __init__(self,engine,text_id,rect) -> None:
        self.engine = engine
        self.text = self.engine.translate(text_id)
        self.sprite = self.engine.text_font.render(self.text, True, self.engine.color_text)
        self.rect = rect
        self.text_rect = self.sprite.get_rect()
        self.pos = [self.rect.x+self.rect.w/2-self.text_rect.w/2,self.rect.y+self.rect.h/2-self.text_rect.h/2]

    def reposition(self):
        self.pos = [self.rect.x+self.rect.w/2-self.text_rect.w/2+self.engine.window_offset[0],self.rect.y+self.rect.h/2-self.text_rect.h/2+self.engine.window_offset[1]]

    def draw(self):
        self.engine.window.render(self.sprite,self.pos)