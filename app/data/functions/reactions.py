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

    engine.pyserial.flushInput()
    engine.pyserial.write(message)

def change_effect_type(engine,selected):
    engine.config[engine.current_layer_selected]["effect"] = engine.layer_effect_type_select.options[selected]
    engine.save_manager.save("config",engine.config)

def change_brightness(engine,percentage):
    engine.config[engine.current_layer_selected]["bri"] = percentage
    engine.save_manager.save("config",engine.config)

    message = f"01{round(percentage,3)}".encode()
    engine.pyserial.flushInput()
    print(message)
    engine.pyserial.write(message)

def layerchange(engine,selected):
    set_select_layer(engine,selected)

def change_effect_speed(engine,percentage):
    engine.config[engine.current_layer_selected]["speed"] = percentage
    engine.save_manager.save("config",engine.config)

def set_select_layer(engine,index:int):
    engine.current_layer_selected = index

    engine.layer_name_input.set_text(engine.config[index]["name"])
    engine.layer_color_select.set_color(engine.config[index]["color"])
    engine.layer_brightness_slider.set_value(engine.config[index]["bri"])
    engine.layer_effect_speed_slider.set_value(engine.config[index]["speed"])
    engine.layer_effect_type_select.set_selected(engine.config[index]["effect"])

    engine.select_layer.set_selected(engine.config[index]["name"])

def delete_layer(engine,button):
    if len(engine.config) > 1:
        engine.config.pop(engine.current_layer_selected)
        engine.save_manager.save("config",engine.config)

        options = []
        for config in engine.config:
            options.append(config["name"])

        engine.select_layer.set_options(options)

        set_select_layer(engine,min(max(engine.current_layer_selected,0),len(engine.config)-1))

def add_layer(engine,button):
    engine.config.append({
        "name":engine.translate("new_layer"),
        "bri":1.0,
        "speed":0.5,
        "color":[0,0,255],
        "effect":"static",
        "keys":{1:None,2:None,3:None,4:None,5:None,6:None,7:None,8:None,9:None,10:None,11:None,12:None,13:None,14:None,15:None,16:None,}
    })

    engine.save_manager.save("config",engine.config)

    options = []
    for config in engine.config:
        options.append(config["name"])

    engine.select_layer.set_options(options)

    set_select_layer(engine,len(engine.config)-1)

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