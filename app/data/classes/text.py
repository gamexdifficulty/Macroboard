import pygame

class Text:
    def __init__(self,engine,text_id,rect,highlight=False,translate=True) -> None:
        self.engine = engine
        self.text_id = text_id
        self.translate = translate
        if self.translate:
            self.text = self.engine.translate(self.text_id)
        else:
            self.text = text_id
        self.sprite = self.engine.text_font.render(self.text, True, self.engine.color_text)
        self.highlight_sprite = self.engine.text_font.render(self.text, True, self.engine.color_highlight)
        self.rect = rect
        self.text_rect = self.sprite.get_rect()
        if self.rect.w != 0 and self.rect.h != 0:
            self.pos = [self.rect.x+self.rect.w/2-self.text_rect.w/2,self.rect.y+self.rect.h/2-self.text_rect.h/2]
        else:
            self.pos = [self.rect.x,self.rect.y]
        self.highlight = highlight

        self.letter_rects = []

        self.engine.texts.append(self)
        self.create_letter_rects()

    def reposition(self):
        if self.rect.w != 0 and self.rect.h != 0:
            self.pos = [self.rect.x+self.rect.w/2-self.text_rect.w/2+self.engine.window_offset[0],self.rect.y+self.rect.h/2-self.text_rect.h/2+self.engine.window_offset[1]]
        else:
            self.pos = [self.rect.x+self.engine.window_offset[0],self.rect.y+self.engine.window_offset[1]]

    def create_letter_rects(self):
        self.letter_rects = []
        self.sprite = self.engine.text_font.render(self.text, True, self.engine.color_text)
        self.text_rect = self.sprite.get_rect()
        if self.rect.w != 0 and self.rect.h != 0:
            self.pos = [self.rect.x+self.rect.w/2-self.text_rect.w/2,self.rect.y+self.rect.h/2-self.text_rect.h/2]
        else:
            self.pos = [self.rect.x,self.rect.y]

        word = ""
        for letter in self.text:
            word += letter
            sprite = self.engine.text_font.render(word, True, self.engine.color_text)
            rect = sprite.get_rect()
            rect.x += self.pos[0]
            rect.y += self.pos[1]
            self.letter_rects.append(rect)

    def check(self):
        if self.translate:
            self.text = self.engine.translate(self.text_id)
        else:
            self.text = self.text
        self.sprite = self.engine.text_font.render(self.text, True, self.engine.color_text)
        self.highlight_sprite = self.engine.text_font.render(self.text, True, self.engine.color_highlight)
        self.text_rect = self.sprite.get_rect()
        self.reposition()
        self.create_letter_rects()
        
    def draw(self):
        if self.highlight:
            self.engine.window.render(self.highlight_sprite,self.pos)
        else:
            self.engine.window.render(self.sprite,self.pos)