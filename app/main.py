import json
from engine_light import *

from data.presets import *

from data.classes.button import *
from data.classes.select import *
from data.classes.slider import *
from data.classes.color import *
from data.classes.input import *
from data.views.macroview import *

from data.functions.reactions import *

class App(Engine):
    def __init__(self):
        super().__init__(delete_old_logs=True,nowindow=False,window_size=[1270,720],window_name="Macroboard",catch_error=False)
        self.window.set_icon(pygame.image.load(os.path.join("data","sprites","icon.svg")).convert_alpha())

        self.first_boot = self.save_manager.load("first_boot",True)
        self.save_manager.load("first_boot",False)
        
        self.input.load()

        self.app_state = "full_view"
        self.details_state = "layer"

        self.select_overlay = None
        
        self.current_layer_selected = 0

        self.color_theme = self.save_manager.load("color_theme","dark")
        self.color_bg = self.save_manager.load("color_bg",[13,17,32])
        self.color_element = self.save_manager.load("color_element",[37,44,62])
        self.color_text = self.save_manager.load("color_text",[235,245,255])
        self.color_highlight = self.save_manager.load("color_highlight",[7,132,227])
        self.color_attention = self.save_manager.load("color_highlight",[242,8,7])

        self.color_bg_target = self.color_bg.copy()
        self.color_text_target = self.color_text.copy()

        self.color_timer = 0
        self.color_bg_diff = [0,0,0]
        self.color_text_diff = [0,0,0]

        self.input_current = None
        self.input_text = ""
        self.input_max_length = 20
        
        self.buttons = []
        self.selects = []
        self.sliders = []
        self.colors = []
        self.inputs = []
        self.texts = []
        self.macro_views = []

        self.window_offset = [0,0]

        self.text_font = pygame.font.Font(os.path.join("data","font.TTF"), 24)
        self.text_language = self.save_manager.load("language","en")
        self.text_language_options = ["en","de"]
        self.text_translation = {}

        self.icon_theme_light = pygame.image.load(os.path.join("data","sprites","sun.png")).convert_alpha()
        self.icon_theme_dark = pygame.image.load(os.path.join("data","sprites","moon.png")).convert_alpha()

        self.board_border = pygame.Rect(32,176,512,512)
        self.board_separator = pygame.Rect(576,32,16,656)
        self.board_buttons = [
            Button(self,[57,201],[96,96],board_button_click,"1",""),
            Button(self,[178,201],[96,96],board_button_click,"2",""),
            Button(self,[299,201],[96,96],board_button_click,"3",""),
            Button(self,[420,201],[96,96],board_button_click,"4",""),
            Button(self,[57,322],[96,96],board_button_click,"5",""),
            Button(self,[178,322],[96,96],board_button_click,"6",""),
            Button(self,[299,322],[96,96],board_button_click,"7",""),
            Button(self,[420,322],[96,96],board_button_click,"8",""),
            Button(self,[57,443],[96,96],board_button_click,"9",""),
            Button(self,[178,443],[96,96],board_button_click,"10",""),
            Button(self,[299,443],[96,96],board_button_click,"11",""),
            Button(self,[420,443],[96,96],board_button_click,"12",""),
            Button(self,[57,567],[96,96],board_button_click,"13",""),
            Button(self,[178,567],[96,96],board_button_click,"14",""),
            Button(self,[299,567],[96,96],board_button_click,"15",""),
            Button(self,[420,567],[96,96],board_button_click,"16",""),
        ]

        self.board_back_button = Button(self,[622,32],[128,48],back_to_layer,"","back")
        self.board_button_view = Text(self,"buttonview",pygame.Rect(750,32,520,48),True)
        self.board_button_name_text = Text(self,"name",pygame.Rect(622,112,0,0),True)
        self.board_button_name_input = Input(self,[814,104],[424,48],"ABC",change_button_name)
        self.board_button_new_button = Button(self,[628,592],[610,96],add_macro,"new_macro","new_macro",flag=1)
        self.board_button_no_macro_text = Text(self,"no_macro",pygame.Rect(622,112,648,512),True)

        self.macrotype_back_button = Button(self,[622,32],[128,48],back_to_button,"","back")
        self.macrotype_button_view_text = Text(self,"macrotype",pygame.Rect(750,32,520,48),True)
        self.macrotype_key_button = Button(self,[622,184],[299,128],macro_key,"")
        self.macrotype_key_text = Text(self,"key_combinations",pygame.Rect(622,248,299,64))
        self.macrotype_text_button = Button(self,[937,184],[299,128],macro_text,"")
        self.macrotype_text_text = Text(self,"text_input",pygame.Rect(937,248,299,64))
        self.macrotype_layer_button = Button(self,[622,328],[299,128],macro_layer,"")
        self.macrotype_layer_text = Text(self,"layer_change",pygame.Rect(622,392,299,64))
        self.macrotype_mousebutton_button = Button(self,[937,328],[299,128],macro_button,"")
        self.macrotype_mousebutton_text = Text(self,"mouse_button",pygame.Rect(937,392,299,64))
        self.macrotype_mousepos_button = Button(self,[622,472],[299,128],macro_pos,"")
        self.macrotype_mousepos_text = Text(self,"mouse_movement",pygame.Rect(622,538,299,64))
        self.macrotype_execapp_button = Button(self,[937,472],[299,128],macro_exe,"")
        self.macrotype_execapp_text = Text(self,"app_execution",pygame.Rect(937,538,299,64))

        self.typeicon_sprites = [
            pygame.image.load(os.path.join("data","sprites","key.png")).convert_alpha(),
            pygame.image.load(os.path.join("data","sprites","text.png")).convert_alpha(),
            pygame.image.load(os.path.join("data","sprites","layer.png")).convert_alpha(),
            pygame.image.load(os.path.join("data","sprites","mouse.png")).convert_alpha(),
            pygame.image.load(os.path.join("data","sprites","mouse_move.png")).convert_alpha(),
            pygame.image.load(os.path.join("data","sprites","app.png")).convert_alpha()
        ]

        self.back_to_macrotype_button = Button(self,[622,32],[128,48],back_to_macrotype,"","back")

        self.macro_create_key_text = Text(self,"key_macro",pygame.Rect(750,32,520,48),True)
        self.macro_create_key_type_text = Text(self,"execute_on",pygame.Rect(628,136,0,0),True)
        self.macro_create_key_type_select = Select(self,[814,128],[424,48],change_effect_type,["clicked","pressed","released"])
        self.macro_create_key_combination_text = Text(self,"key_combination",pygame.Rect(628,176+32,512+96,48),True)
        self.macro_create_key_press_combination_text = Text(self,"presskeycombination",pygame.Rect(628,176+96,512+96,512-128-96),False)
        self.macro_create_keys_background = pygame.Rect(628,176+96,512+96,512-128-96)
        self.macro_create_key_input_text = Text(self,"",pygame.Rect(628,176+96,512+96,512-128-96),False)
        self.macro_create_key_button = Button(self,[628,592],[288,96],create_key_macro,"create_key_macro","save",flag=1)
        self.macro_empty_key_combination_button = Button(self,[950,592],[288,96],empty_keys,"empty_keys","empty_keys",flag=2)

        self.macro_create_text_button = Button(self,[628,592],[610,96],create_text_macro,"create_text_macro","save_macro",flag=1)
        self.macro_create_layer_button = Button(self,[628,592],[610,96],create_layer_macro,"create_layer_macro","save_macro",flag=1)
        self.macro_create_button_button = Button(self,[628,592],[610,96],create_button_macro,"create_button_macro","save_macro",flag=1)
        self.macro_create_pos_button = Button(self,[628,592],[610,96],create_pos_macro,"create_pos_macro","save_macro",flag=1)
        self.macro_create_exe_button = Button(self,[628,592],[610,96],create_exe_macro,"create_exe_macro","save_macro",flag=1)

        self.board_button_selected = None

        self.layer_lable = Text(self,"layer",pygame.Rect(96,32,448,48),True)
        self.layer_text = [
            Text(self,"layerview",pygame.Rect(622,32,648,24),True),
            Text(self,"name",pygame.Rect(622,112,0,0),True),
            Text(self,"color",pygame.Rect(622,192,0,0),True),
            Text(self,"brightness",pygame.Rect(622,288,0,0),True),
            Text(self,"effectspeed",pygame.Rect(622,384,0,0),True),
            Text(self,"effecttype",pygame.Rect(622,480,0,0),True),
        ]

        self.layer_name_input = Input(self,[814,104],[424,48],"Main",change_layer_name)
        self.layer_brightness_slider = Slider(self,[814,280],[424,48],change_brightness)
        self.layer_effect_type_select = Select(self,[814,472],[424,48],change_effect_type,["static","breath","colorwheel","rainbow"])
        self.layer_color_select = Color(self,[814,184],[424,48],change_color)
        self.layer_effect_speed_slider = Slider(self,[814,376],[424,48],change_effect_speed)

        self.layer_new_button = Button(self,[628,592],[288,96],add_layer,"new_layer","new_layer",flag=1)
        self.layer_delate_button = Button(self,[950,592],[288,96],delete_layer,"delete","delete",flag=2)

        self.select_layer = Select(self,[96,96],[336+96+16,48],layerchange)
        self.theme_switch_button = Button(self,[32,32],[48,48],switch_theme,"theme")
        self.language_switch_button = Button(self,[32,96],[48,48],switch_language,"language","language_id")

        self.config = self.save_manager.load("config",[])
        if self.config == []:
            self.config = [new_layer.copy()]
            self.save_manager.save("config",self.config)

        options = []
        for config in self.config:
            options.append(config["name"])

        self.select_layer.set_options(options)
        set_select_layer(self,self.current_layer_selected)

        self.edit_macro = False
        self.edit_macro_index = 0

        self.pressed_keys = []
        self.pressed_keys_focused = False

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

    def event_keydown(self, key: int, unicode: str):
        if self.details_state == "macrokey" and self.pressed_keys_focused:
            if key not in self.pressed_keys:
                self.pressed_keys.append(key)
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

                if len(self.pressed_keys) != 1:
                    text = " + "+text

                self.macro_create_key_input_text = Text(self,self.macro_create_key_input_text.text_id+text,self.macro_create_keys_background,False)
        else:
            if self.input_current != None:
                if key == KEY_BACKSPACE[0] and self.input_current.text_position != 0:
                    self.input_text = self.input_text[:self.input_current.text_position-1] + self.input_text[self.input_current.text_position:]
                    self.input_current.text_position = max(self.input_current.text_position-1,0)
                if key == KEY_DELETE[0] and self.input_current.text_position != len(self.input_current.text.letter_rects):
                    self.input_text = self.input_text[:self.input_current.text_position] + self.input_text[self.input_current.text_position+1:]
                elif unicode.isalpha() or unicode.isalnum() or key == KEY_SPACE[0]:
                    if len(self.input_text) < self.input_max_length and self.input_current:
                        self.input_text = self.input_text[:self.input_current.text_position] + unicode + self.input_text[self.input_current.text_position:]
                        self.input_current.text_position += 1

        if key == KEY_ARROW_LEFT[0]:
            if self.input_current:
                self.input_current.text_position = max(self.input_current.text_position-1,0) 
        elif key == KEY_ARROW_RIGHT[0]:
            if self.input_current:
                self.input_current.text_position = min(self.input_current.text_position+1,len(self.input_current.text.text)) 

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

            if self.details_state == "button":
                self.board_back_button.update()
                self.board_button_name_input.update()
                self.board_button_new_button.update()
                for view in self.macro_views:
                    view.update()

            if self.details_state == "macroselect":
                self.macrotype_back_button.update()
                self.macrotype_key_button.update()
                self.macrotype_text_button.update()
                self.macrotype_layer_button.update()
                self.macrotype_mousebutton_button.update()
                self.macrotype_mousepos_button.update()
                self.macrotype_execapp_button.update()

            if self.details_state == "macrokey":
                self.back_to_macrotype_button.update()
                self.macro_empty_key_combination_button.update()
                self.macro_create_key_button.update()
                self.macro_create_key_type_select.update()
                if self.input.get("accept"):
                    if self.macro_create_keys_background.collidepoint(self.input.mouse.get_pos()):
                        self.pressed_keys_focused = True
                    else:
                        self.pressed_keys_focused = False
            if self.details_state == "macrotext":
                self.back_to_macrotype_button.update()
                self.macro_create_text_button.update()

            if self.details_state == "macrolayer":
                self.back_to_macrotype_button.update()
                self.macro_create_layer_button.update()

            if self.details_state == "macrobutton":
                self.back_to_macrotype_button.update()
                self.macro_create_button_button.update()

            if self.details_state == "macropos":
                self.back_to_macrotype_button.update()
                self.macro_create_pos_button.update()

            if self.details_state == "macroexe":
                self.back_to_macrotype_button.update()
                self.macro_create_exe_button.update()

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
                self.window.render(self.icon_theme_dark,[self.theme_switch_button.rect.x,self.theme_switch_button.rect.y])
            else:
                self.window.render(self.icon_theme_light,[self.theme_switch_button.rect.x,self.theme_switch_button.rect.y])

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

            if self.details_state == "button":
                self.board_back_button.draw()
                self.board_button_view.draw()
                self.board_button_name_text.draw()
                self.board_button_name_input.draw()
                self.board_button_new_button.draw()
                if self.config[self.current_layer_selected]["keys"][self.board_button_selected.id]["macros"] == []:
                    self.board_button_no_macro_text.draw()

                for view in self.macro_views:
                    view.draw()

            if self.details_state == "macroselect":
                self.macrotype_back_button.draw()
                self.macrotype_button_view_text.draw()
                self.macrotype_key_button.draw()
                self.window.render(self.typeicon_sprites[0],(739,200))
                self.macrotype_key_text.draw()
                self.macrotype_text_button.draw()
                self.window.render(self.typeicon_sprites[1],(1054,200))
                self.macrotype_text_text.draw()
                self.macrotype_layer_button.draw()
                self.window.render(self.typeicon_sprites[2],(739,344))
                self.macrotype_layer_text.draw()
                self.macrotype_mousebutton_button.draw()
                self.window.render(self.typeicon_sprites[3],(1054,344))
                self.macrotype_mousebutton_text.draw()
                self.macrotype_mousepos_button.draw()
                self.window.render(self.typeicon_sprites[4],(739,488))
                self.macrotype_mousepos_text.draw()
                self.macrotype_execapp_button.draw()
                self.window.render(self.typeicon_sprites[5],(1054,488))
                self.macrotype_execapp_text.draw()

            if self.details_state == "macrokey":
                self.back_to_macrotype_button.draw()
                self.macro_create_key_button.draw()
                self.macro_create_key_text.draw()
                self.macro_create_key_type_select.draw()
                self.macro_create_key_type_text.draw()
                pygame.draw.rect(self.window.main_surface,self.color_element,self.macro_create_keys_background,border_radius=8)
                if self.pressed_keys_focused:
                    pygame.draw.rect(self.window.main_surface,self.color_highlight,self.macro_create_keys_background,width=4,border_radius=8)
                self.macro_create_key_combination_text.draw()
                if self.pressed_keys == []:
                    self.macro_create_key_press_combination_text.draw()
                else:
                    self.macro_create_key_input_text.draw()
                self.macro_empty_key_combination_button.draw()

            if self.details_state == "macrotext":
                self.back_to_macrotype_button.draw()
                self.macro_create_text_button.draw()

            if self.details_state == "macrolayer":
                self.back_to_macrotype_button.draw()
                self.macro_create_layer_button.draw()

            if self.details_state == "macrobutton":
                self.back_to_macrotype_button.draw()
                self.macro_create_button_button.draw()

            if self.details_state == "macropos":
                self.back_to_macrotype_button.draw()
                self.macro_create_pos_button.draw()

            if self.details_state == "macroexe":
                self.back_to_macrotype_button.draw()
                self.macro_create_exe_button.draw()

            if self.select_overlay != None:
                self.select_overlay.draw_select()

    def translate(self,text_id):
        with open(os.path.join("data","language.json"),"r+",encoding="UTF-8") as f:
            self.text_translation = json.load(f)
            if text_id in self.text_translation[self.text_language]:
                return self.text_translation[self.text_language][text_id]
            else:
                return text_id

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
