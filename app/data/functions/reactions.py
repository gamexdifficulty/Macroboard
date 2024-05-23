import os,json,pygame
import data.classes
from data.presets import *
from data.classes.text import Text
import data.views.macroview as macroview

def switch_language(engine,button):
    index = engine.text_language_options.index(engine.text_language)+1
    if index > len(engine.text_language_options)-1:
        index -= len(engine.text_language_options)
    engine.text_language = engine.text_language_options[index]
    for text in engine.texts:
        text.check()

    engine.save_manager.save("language",engine.text_language)
        
def switch_theme(engine,id):
    if engine.color_timer == 0:
        if engine.color_theme == "dark":
            engine.color_theme = "light"
            engine.color_bg_target = [235,245,255]
        else:
            engine.color_theme = "dark"
            engine.color_bg_target = [13,17,32]

        for i in range(len(engine.color_bg_diff)):
            engine.color_bg_diff[i] = engine.color_bg_target[i]-engine.color_bg[i]

        engine.save_manager.save("color_theme",engine.color_theme)
        engine.save_manager.save("color_bg",engine.color_bg_target)

##########################################################################################

def change_layer_name(engine,name):
    engine.config[engine.current_layer_selected]["name"] = name
    engine.save_manager.save("config",engine.config)

    options = []
    for config in engine.config:
        options.append(config["name"])

    engine.select_layer.set_options(options)

def change_color(engine,color):
    engine.config[engine.current_layer_selected]["color"] = color
    engine.save_manager.save("config",engine.config)

    engine.i += 1
    message = f"03{color[0]:>03}{color[1]:>03}{color[2]:>03}\r".encode()

def change_effect_type(engine,selected):
    engine.config[engine.current_layer_selected]["effect"] = engine.layer_effect_type_select.options[selected]
    engine.save_manager.save("config",engine.config)

def change_brightness(engine,percentage):
    engine.config[engine.current_layer_selected]["bri"] = percentage
    engine.save_manager.save("config",engine.config)
    message = f"01{round(percentage,3)}".encode()

def change_effect_speed(engine,percentage):
    engine.config[engine.current_layer_selected]["speed"] = percentage
    engine.save_manager.save("config",engine.config)

##########################################################################################

def add_layer(engine,button):
    layer = new_layer.copy()
    layer["name"] = engine.translate("new_layer")
    engine.config.append(layer)

    engine.save_manager.save("config",engine.config)

    options = []
    for config in engine.config:
        options.append(config["name"])

    engine.select_layer.set_options(options)

    set_select_layer(engine,len(engine.config)-1)

def delete_layer(engine,button):
    if len(engine.config) > 1:
        engine.config.pop(engine.current_layer_selected)
        engine.save_manager.save("config",engine.config)

        options = []
        for config in engine.config:
            options.append(config["name"])

        engine.select_layer.set_options(options)

        set_select_layer(engine,min(max(engine.current_layer_selected,0),len(engine.config)-1))

##########################################################################################

def layerchange(engine,selected):
    engine.details_state = "layer"
    for loop_button in engine.board_buttons:
        loop_button.selected = False
    set_select_layer(engine,selected)

def set_select_layer(engine,index:int):
    engine.current_layer_selected = index

    engine.layer_name_input.set_text(engine.config[index]["name"])
    engine.layer_color_select.set_color(engine.config[index]["color"])
    engine.layer_brightness_slider.set_value(engine.config[index]["bri"])
    engine.layer_effect_speed_slider.set_value(engine.config[index]["speed"])
    engine.layer_effect_type_select.set_selected(engine.config[index]["effect"])

    engine.select_layer.set_selected(engine.config[index]["name"])
    keylist = engine.config[engine.current_layer_selected]["keys"]
    for i,button in enumerate(engine.board_buttons):
        engine.board_buttons[i].text.text_id = keylist[str(i+1)]["name"]
        engine.board_buttons[i].text.check()

def board_button_click(engine,button):
    engine.details_state = "button"
    for loop_button in engine.board_buttons:
        loop_button.selected = False
    for loop_input in engine.inputs:
        loop_input.selected = False
    button.selected = True
    engine.board_button_name_input.set_text(engine.config[engine.current_layer_selected]["keys"][str(button.id)]["name"])
    engine.board_button_selected = button
    refresh_macro_views(engine)

##########################################################################################

def back_to_layer(engine,button):
    engine.details_state = "layer"
    for loop_button in engine.board_buttons:
        loop_button.selected = False

def add_macro(engine,button):
    engine.details_state = "macroselect"

##########################################################################################

def back_to_button(engine,button):
    engine.details_state = "button"

def change_button_name(engine,name):
    button_index = engine.board_buttons.index(engine.board_button_selected)
    engine.config[engine.current_layer_selected]["keys"][str(button_index+1)]["name"] = name
    engine.board_buttons[button_index].text.text_id = name
    engine.board_buttons[button_index].text.check()
    engine.save_manager.save("config",engine.config)

###########################################################################################

def back_to_macrotype(engine,button):
    if engine.edit_macro:
        engine.details_state = "button"
    else:
        engine.details_state = "macroselect"
    engine.edit_macro = False

def macro_key(engine,button):
    engine.details_state = "macrokey"
    engine.macro_create_key_type_select.set_selected("clicked")
    engine.pressed_keys = []
    engine.macro_create_key_input_text = Text(engine,"",engine.macro_create_keys_background,False)

def macro_text(engine,button):
    engine.details_state = "macrotext"

def macro_layer(engine,button):
    engine.details_state = "macrolayer"

def macro_button(engine,button):
    engine.details_state = "macrobutton"

def macro_pos(engine,button):
    engine.details_state = "macropos"

def macro_exe(engine,button):
    engine.details_state = "macroexe"

##############################################################################################

def refresh_macro_views(engine):
    engine.macro_views = []
    for i,macro in enumerate(engine.config[engine.current_layer_selected]["keys"][engine.board_button_selected.id]["macros"]):
        engine.macro_views.append(macroview.MacroView(engine,i+1,macro))

def create_key_macro(engine,button):
    if engine.pressed_keys != []:
        macro = new_macro.copy()
        macro["type"] = 0
        macro["trigger"] = engine.macro_create_key_type_select.selected
        macro["data"] = engine.pressed_keys
        button_index = engine.board_buttons.index(engine.board_button_selected)
        if engine.edit_macro:
            engine.config[engine.current_layer_selected]["keys"][str(button_index+1)]["macros"][engine.edit_macro_index] = macro
        else:
            engine.config[engine.current_layer_selected]["keys"][str(button_index+1)]["macros"].append(macro)
        engine.save_manager.save("config",engine.config)
        engine.details_state = "button"
        engine.edit_macro = False
        refresh_macro_views(engine)

def empty_keys(engine,button):
    engine.pressed_keys = []
    engine.macro_create_key_input_text = Text(engine,"",engine.macro_create_keys_background,False)

def create_text_macro(engine,button):
    engine.details_state = "button"

def create_layer_macro(engine,button):
    engine.details_state = "button"

def create_button_macro(engine,button):
    engine.details_state = "button"

def create_pos_macro(engine,button):
    engine.details_state = "button"

def create_exe_macro(engine,button):
    engine.details_state = "button"

def delete_macro(engine,button):
    engine.config[engine.current_layer_selected]["keys"][engine.board_button_selected.id]["macros"].pop(button.id-1)
    engine.save_manager.save("config",engine.config)
    refresh_macro_views(engine)

def edit_macro_key(engine,config,index):
    engine.edit_macro = True
    engine.edit_macro_index = index-1
    engine.details_state = "macrokey"
    engine.macro_create_key_type_select.set_selected(["clicked","pressed","released"][config["trigger"]])
    engine.pressed_keys = config["data"]
    engine.macro_create_key_input_text = Text(engine,"",engine.macro_create_keys_background,False)
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

        if engine.macro_create_key_input_text.text_id != "":
            text = " + "+text

        engine.macro_create_key_input_text = Text(engine,engine.macro_create_key_input_text.text_id+text,engine.macro_create_keys_background,False)