import json
from engine_light import *
from data.classes.button import *

class App(Engine):
    def __init__(self):
        super().__init__(delete_old_logs=True,window_size=[1270,720],window_name="Macroboard",catch_error=False)
        pygame.display.set_icon(pygame.image.load(os.path.join("data","sprites","icon.png")).convert_alpha())

        self.first_boot = self.save_manager.load("first_boot",True)

        self.color_theme = self.save_manager.load("color_theme","dark")
        self.color_bg = self.save_manager.load("color_bg",[13,17,32])
        self.color_element = self.save_manager.load("color_element",[37,44,62])
        self.color_text = self.save_manager.load("color_text",[235,245,255])
        self.color_highlight = self.save_manager.load("color_highlight",[7,132,227])
        self.color_timer = 0
        self.color_bg_diff = [0,0,0]
        self.color_text_diff = [0,0,0]

        self.app_state = "full_view"
    def update(self):
        if self.app_state == "overlay":
            self.update_colors()
        if self.app_state == "full_view":
            self.update_colors()
    def draw(self):
        if self.app_state == "full_view":
            self.window.fill(self.color_bg)
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
