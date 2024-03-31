import json
from engine_light import *
from data.classes.button import *
from data.classes.select import *
from data.classes.slider import *
from data.classes.color import *
from data.classes.input import *

class App(Engine):
    def __init__(self):
        super().__init__(delete_old_logs=True,nowindow=False,window_size=[1270,720],window_name="Macroboard",catch_error=False)
        self.window.set_icon(pygame.image.load(os.path.join("data","sprites","icon.png")).convert_alpha())

        self.first_boot = self.save_manager.load("first_boot",True)
        
        self.input.load()

        self.color_theme = self.save_manager.load("color_theme","dark")
        self.color_bg = self.save_manager.load("color_bg",[13,17,32])
        self.color_element = self.save_manager.load("color_element",[37,44,62])
        self.color_text = self.save_manager.load("color_text",[235,245,255])
        self.color_highlight = self.save_manager.load("color_highlight",[7,132,227])
        self.color_attention = self.save_manager.load("color_highlight",[242,8,7])

        self.color_bg_target = self.color_bg.copy()
        self.color_text_target = self.color_text.copy()

        self.select_overlay = None
        
        self.color_timer = 0
        self.color_bg_diff = [0,0,0]
        self.color_text_diff = [0,0,0]

        self.buttons = []
        self.selects = []
        self.sliders = []
        self.colors = []
        self.inputs = []
        self.texts = []

        self.app_state = "full_view"
        self.details_state = "layer"

        self.window_offset = [0,0]

        self.text_font = pygame.font.Font(os.path.join("data","font.TTF"), 24)
        self.text_language = self.save_manager.load("language","en")
        self.language_options = ["en","de"]
        self.text_translation = {}

        self.theme_light_icon = pygame.image.load(os.path.join("data","sprites","sun.png")).convert_alpha()
        self.theme_dark_icon = pygame.image.load(os.path.join("data","sprites","moon.png")).convert_alpha()
        self.add_layer_icon = pygame.image.load(os.path.join("data","sprites","new_layer.png")).convert_alpha()

        self.board_border = pygame.Rect(32,176,512,512)
        self.board_separator = pygame.Rect(576,32,16,656)
        self.board_buttons = [
            Button(self,[57,201],[96,96],self.board_button_click,"1","ABC"),
            Button(self,[178,201],[96,96],self.board_button_click,"2"),
            Button(self,[299,201],[96,96],self.board_button_click,"3"),
            Button(self,[420,201],[96,96],self.board_button_click,"4"),
            Button(self,[57,322],[96,96],self.board_button_click,"5"),
            Button(self,[178,322],[96,96],self.board_button_click,"6"),
            Button(self,[299,322],[96,96],self.board_button_click,"7"),
            Button(self,[420,322],[96,96],self.board_button_click,"8"),
            Button(self,[57,443],[96,96],self.board_button_click,"9"),
            Button(self,[178,443],[96,96],self.board_button_click,"10"),
            Button(self,[299,443],[96,96],self.board_button_click,"11"),
            Button(self,[420,443],[96,96],self.board_button_click,"12"),
            Button(self,[57,567],[96,96],self.board_button_click,"13"),
            Button(self,[178,567],[96,96],self.board_button_click,"14"),
            Button(self,[299,567],[96,96],self.board_button_click,"15"),
            Button(self,[420,567],[96,96],self.board_button_click,"16"),
        ]

        self.layer_lable = Text(self,"layer",pygame.Rect(96,32,448,48),True)
        self.layer_text = [
            Text(self,"layerview",pygame.Rect(622,32,648,24),True),
            Text(self,"name",pygame.Rect(622,112,0,0),True),
            Text(self,"color",pygame.Rect(622,192,0,0),True),
            Text(self,"brightness",pygame.Rect(622,288,0,0),True),
            Text(self,"effectspeed",pygame.Rect(622,384,0,0),True),
            Text(self,"effecttype",pygame.Rect(622,480,0,0),True),
        ]

        self.layer_name_input = Input(self,[814,104],[424,48],"Main")
        self.layer_brightness_slider = Slider(self,[814,280],[424,48])
        self.layer_effect_type_select = Select(self,[814,472],[424,48],["static","breath","colorwheel","rainbow"])
        self.layer_color_select = Color(self,[814,184],[424,48])
        self.layer_effect_speed_slider = Slider(self,[814,376],[424,48])

        self.layer_new_button = Button(self,[628,592],[288,96],self.board_button_click,"new_layer","new_layer",flag=1)
        self.layer_delate_button = Button(self,[950,592],[288,96],self.board_button_click,"delete","delete",flag=2)

        self.select_layer = Select(self,[96,96],[336+96+16,48],["Main","x","X","X"])
        self.theme_switch_button = Button(self,[32,32],[48,48],self.switch_theme,"theme")
        self.language_switch_button = Button(self,[32,96],[48,48],self.switch_language,"language","language_id")

    def event_window_resize(self, size: list[int]):
        if self.app_state == "full_view":
            self.window_offset = [size[0]/2-635,size[1]/2-360]

            self.board_border = pygame.Rect(32+self.window_offset[0],176+self.window_offset[1],self.board_border.w,self.board_border.h)
            self.board_separator = pygame.Rect(576+self.window_offset[0],32+self.window_offset[1],self.board_separator.w,self.board_separator.h)
            
            for button in self.buttons:
                button.reposition()

            for select in self.selects:
                select.reposition()

            for slider in self.sliders:
                slider.reposition()

            for color in self.colors:
                color.reposition()

            for text in self.texts:
                text.reposition()

            for text_input in self.inputs:
                text_input.reposition()

    def update(self):
        if self.app_state == "full_view":
            self.update_colors()

            self.select_layer.update()
            self.theme_switch_button.update()
            self.language_switch_button.update()

            for button in self.board_buttons:
                button.update()

            if self.details_state == "layer":
                self.layer_name_input.update()
                self.layer_color_select.update()
                self.layer_brightness_slider.update()
                self.layer_effect_type_select.update()
                self.layer_effect_speed_slider.update()
                self.layer_new_button.update()
                self.layer_delate_button.update()
    
    def draw(self):
        if self.app_state == "full_view":
            self.window.fill(self.color_bg)

            pygame.draw.rect(self.window.main_surface,self.color_element,self.board_separator,border_radius=32)
            pygame.draw.rect(self.window.main_surface,self.color_element,self.board_border,16,32)

            self.theme_switch_button.draw()
            self.language_switch_button.draw()

            self.layer_lable.draw()
            self.select_layer.draw()

            if self.color_theme == "light":
                self.window.render(self.theme_dark_icon,[self.theme_switch_button.rect.x,self.theme_switch_button.rect.y])
            else:
                self.window.render(self.theme_light_icon,[self.theme_switch_button.rect.x,self.theme_switch_button.rect.y])

            for button in self.board_buttons:
                button.draw()

            if self.details_state == "layer":
                for text in self.layer_text:
                    text.draw()

                self.layer_name_input.draw()
                self.layer_color_select.draw()
                self.layer_brightness_slider.draw()
                self.layer_effect_type_select.draw()
                self.layer_effect_speed_slider.draw()
                self.layer_new_button.draw()
                self.layer_delate_button.draw()

            if self.select_overlay != None:
                self.select_overlay.draw_select()

    def board_button_click(self,button):
        button.selected = True

    def add_layer(self,button):
        pass

    def translate(self,text_id):
        with open(os.path.join("data","language.json"),"r+",encoding="UTF-8") as f:
            self.text_translation = json.load(f)
            if text_id in self.text_translation[self.text_language]:
                return self.text_translation[self.text_language][text_id]
            else:
                return text_id
            
    def switch_language(self,button):
        index = self.language_options.index(self.text_language)+1
        if index > len(self.language_options)-1:
            index -= len(self.language_options)
        self.text_language = self.language_options[index]
        for text in self.texts:
            text.check()

        self.save_manager.save("language",self.text_language)
            
    def switch_theme(self,id):
        if self.color_timer == 0:
            if self.color_theme == "dark":
                self.color_theme = "light"
                self.color_bg_target = [235,245,255]
            else:
                self.color_theme = "dark"
                self.color_bg_target = [13,17,32]

            for i in range(len(self.color_bg_diff)):
                self.color_bg_diff[i] = self.color_bg_target[i]-self.color_bg[i]

            self.save_manager.save("color_theme",self.color_theme)
            self.save_manager.save("color_bg",self.color_bg_target)

    def update_colors(self):
        if self.color_bg != self.color_bg_target:
            self.color_timer = min(self.color_timer+self.delta_time,0.5)
            for i in range(len(self.color_bg)):
                self.color_bg[i] = self.color_bg_target[i]-self.color_bg_diff[i]*(0.5-self.color_timer)*2

            if self.color_timer == 0.5:
                self.color_timer = 0
                self.color_bg = self.color_bg_target.copy()
                self.color_text = self.color_text_target.copy()

if __name__ == "__main__":
    app = App()
    app.run()
