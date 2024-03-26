import pygame

class Text:
    def __init__(self,engine,text_id,rect,highlight=False) -> None:
        self.engine = engine
        self.text_id = text_id
        self.text = self.engine.translate(self.text_id)
        self.sprite = self.engine.text_font.render(self.text, True, self.engine.color_text)
        self.highlight_sprite = self.engine.text_font.render(self.text, True, self.engine.color_highlight)
        self.rect = rect
        self.text_rect = self.sprite.get_rect()
        if self.rect.w != 0 and self.rect.h != 0:
            self.pos = [self.rect.x+self.rect.w/2-self.text_rect.w/2,self.rect.y+self.rect.h/2-self.text_rect.h/2]
        else:
            self.pos = [self.rect.x,self.rect.y]
        self.highlight = highlight

        self.engine.texts.append(self)

    def reposition(self):
        if self.rect.w != 0 and self.rect.h != 0:
            self.pos = [self.rect.x+self.rect.w/2-self.text_rect.w/2+self.engine.window_offset[0],self.rect.y+self.rect.h/2-self.text_rect.h/2+self.engine.window_offset[1]]
        else:
            self.pos = [self.rect.x+self.engine.window_offset[0],self.rect.y+self.engine.window_offset[1]]

    def check(self):
        self.text = self.engine.translate(self.text_id)
        self.sprite = self.engine.text_font.render(self.text, True, self.engine.color_text)
        self.highlight_sprite = self.engine.text_font.render(self.text, True, self.engine.color_highlight)
        self.text_rect = self.sprite.get_rect()
        self.reposition()
        
    def draw(self):
        if self.highlight:
            self.engine.window.render(self.highlight_sprite,self.pos)
        else:
            self.engine.window.render(self.sprite,self.pos)