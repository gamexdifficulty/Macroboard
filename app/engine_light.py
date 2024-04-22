import os
import sys
import json
import glob
import time
import pygame
import shutil
import datetime
import argparse
from cryptography.fernet import Fernet

class Builder:
    def __init__(self,engine) -> None:

        """
        Initialise the engines input system.

        The build system packs the engine files if a release is planed and converts the app to an exe file.

        Args:
        
        - engine (Engine): The engine to access specific variables.

        !!!This is only used internally by the engine and should not be called in an app!!!
        """

        # Engine variable
        self._engine = engine

    def _setup(self,name:str=""):

        """
        Created the initial app folder structure

        Args:

        - name (str): Not implemented yet, for naming the app files

        !!!This is only used internally by the engine and should not be called in an app!!!
        """

        # Create engine tree
        directories_created = 0
        files_created = 0
        directories_to_create = ["data",os.path.join("data","classes"),os.path.join("data","saves"),os.path.join("data","saves","backup"),os.path.join("data","sprites")]

        # Creating directories
        for directory in directories_to_create:
            try:
                os.mkdir(directory)
                directories_created += 1
            except FileExistsError:
                self._engine.logger.warning(f"Skipping creation of directory {directory}, it already exist.")

        # Create main code file
        if not os.path.exists("main.py"):
            with open("main.py","+wt") as file:
                file.write("from engine_light import *\n")
                file.write("\n")
                file.write("class App(Engine):\n")
                file.write("    def __init__(self):\n")
                file.write("        super().__init__() # Engine options go here\n")
                file.write("\n")
                file.write("    def update(self):\n")
                file.write('        if self.app_state == "menu":\n')
                file.write("            pass\n")
                file.write("\n")
                file.write("    def draw(self):\n")
                file.write('        if self.app_state == "menu":\n')
                file.write("            pass\n")
                file.write("\n")
                file.write("\n")
                file.write('if __name__ == "__main__":\n')
                file.write("    app = App()\n")
                file.write("    app.run()\n")
            files_created += 1
        else:
            self._engine.logger.warning("Skipping creation of main file, already exist.")

        # Log creation process
        if files_created == 0 and directories_created == 0:
            self._engine.logger.info("No new files or directories where created.")
        else:
            self._engine.logger.info(f"Created app files structure with {files_created} files and {directories_created} directories")

    def _create_exe(self,name:str="app"):

        """
        Builds the app into exe file and zips all dependencies

        Args:

        - name (str): Not implemented yet, for naming the app files

        !!!This is only used internally by the engine and should not be called in an app!!!
        """

        # Import Modules
        import subprocess
        import shutil
        import sys

        # Install pyinstaller
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            import PyInstaller.__main__
        except:
            print("Pyinstaller cannot be installed!")
        else:

            # Packing app in exe
            PyInstaller.__main__.run([
                'main.py',
                '--onefile',
                '--noconsole',
                '--clean'
            ])

            # Removing build files
            if os.path.isfile("main.spec"):
                os.remove("main.spec")
            if os.path.isdir("build"):
                shutil.rmtree("build")
            if os.path.isdir("dist"):
                if os.path.isdir("export"):
                    shutil.rmtree("export")
                os.rename("dist","export")

            # Create Export DIR
            if os.path.isdir("data"):
                shutil.copytree("data",os.path.join("export","data"))
            if os.path.isdir("screenshots"):
                shutil.copytree("screenshots",os.path.join("export","screenshots"))

            # Zip Export
            if os.path.isdir("export"):
                shutil.make_archive("export","zip","export")
                shutil.rmtree("export")

    def _pack_release(self):

        """
        Packs engine for release into single file

        Args:

        - no args are required

        !!!This is only used internally by the engine and should not be called in an app!!!
        """

        # Relevent paths
        class_path = "./classes"
        export_file = "engine_export.py"
        main_file = "engine_light.py"
        imported_modules = []
        class_contents = []
        within_class = False

        # Read class folder 
        for pathname, _, files in os.walk(class_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(pathname, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        for line in content.split("\n"):
                            unstriped_line = line
                            line = line.strip()
                            if unstriped_line.startswith("class "):
                                within_class = True
                            elif unstriped_line and not unstriped_line.startswith(" ") and within_class:
                                within_class = False
                            if (line.startswith("import ") or line.startswith("from "))  and not "PyInstaller.__main__" in line and not within_class:
                                if not line.startswith("from classes."):
                                    imported_modules.append(line)
                                    content = content.replace(unstriped_line, "",1)
                        class_contents.append(content)

        imported_modules = sorted(set(imported_modules),key=len)

        # Read main file
        with open(main_file, "r", encoding="utf-8") as main_handle:
            main_content = main_handle.read()
            for line in main_content.split("\n"):
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    if not line.startswith("from classes."):
                        imported_modules.append(line)

        imported_modules = sorted(set(imported_modules),key=len)

        # Creating export file
        with open(export_file, "w", encoding="utf-8") as f:
            # write imports
            for importlines in imported_modules:
                f.write(f"{importlines}\n")
            f.write("\n")

            # Write classes content
            for content in class_contents:
                content = "\n".join(line for line in content.split("\n") if not line.strip().startswith("from classes."))
                f.write(content.strip())
                f.write("\n\n")

            # Write main content
            main_content = "\n".join(line for line in main_content.split("\n") if not line.strip().startswith("from classes.") and not line.strip().startswith("import "))
            f.write(main_content)

# Input types
_KEYBOARD = 0
_MOUSE = 1

# Input method
CLICKED = 0
PRESSED = 1
RELEASE = 2

# Keyboard input index
KEY_A = [pygame.K_a,_KEYBOARD]
KEY_B = [pygame.K_b,_KEYBOARD]
KEY_C = [pygame.K_c,_KEYBOARD]
KEY_D = [pygame.K_d,_KEYBOARD]
KEY_E = [pygame.K_e,_KEYBOARD]
KEY_F = [pygame.K_f,_KEYBOARD]
KEY_G = [pygame.K_g,_KEYBOARD]
KEY_H = [pygame.K_h,_KEYBOARD]
KEY_I = [pygame.K_i,_KEYBOARD]
KEY_J = [pygame.K_j,_KEYBOARD]
KEY_K = [pygame.K_k,_KEYBOARD]
KEY_L = [pygame.K_l,_KEYBOARD]
KEY_M = [pygame.K_m,_KEYBOARD]
KEY_N = [pygame.K_n,_KEYBOARD]
KEY_O = [pygame.K_o,_KEYBOARD]
KEY_P = [pygame.K_p,_KEYBOARD]
KEY_Q = [pygame.K_q,_KEYBOARD]
KEY_R = [pygame.K_r,_KEYBOARD]
KEY_S = [pygame.K_s,_KEYBOARD]
KEY_T = [pygame.K_t,_KEYBOARD]
KEY_U = [pygame.K_u,_KEYBOARD]
KEY_V = [pygame.K_v,_KEYBOARD]
KEY_W = [pygame.K_w,_KEYBOARD]
KEY_X = [pygame.K_x,_KEYBOARD]
KEY_Y = [pygame.K_y,_KEYBOARD]
KEY_Z = [pygame.K_z,_KEYBOARD]
KEY_0 = [pygame.K_0,_KEYBOARD]
KEY_1 = [pygame.K_1,_KEYBOARD]
KEY_2 = [pygame.K_2,_KEYBOARD]
KEY_3 = [pygame.K_3,_KEYBOARD]
KEY_4 = [pygame.K_4,_KEYBOARD]
KEY_5 = [pygame.K_5,_KEYBOARD]
KEY_6 = [pygame.K_6,_KEYBOARD]
KEY_7 = [pygame.K_7,_KEYBOARD]
KEY_8 = [pygame.K_8,_KEYBOARD]
KEY_9 = [pygame.K_9,_KEYBOARD]
KEY_F1 = [pygame.K_F1,_KEYBOARD]
KEY_F2 = [pygame.K_F2,_KEYBOARD]
KEY_F3 = [pygame.K_F3,_KEYBOARD]
KEY_F4 = [pygame.K_F4,_KEYBOARD]
KEY_F5 = [pygame.K_F5,_KEYBOARD]
KEY_F6 = [pygame.K_F6,_KEYBOARD]
KEY_F7 = [pygame.K_F7,_KEYBOARD]
KEY_F8 = [pygame.K_F8,_KEYBOARD]
KEY_F9 = [pygame.K_F9,_KEYBOARD]
KEY_F10 = [pygame.K_F10,_KEYBOARD]
KEY_F11 = [pygame.K_F11,_KEYBOARD]
KEY_F12 = [pygame.K_F12,_KEYBOARD]
KEY_LCTRL = [pygame.K_LCTRL,_KEYBOARD]
KEY_RCTRL = [pygame.K_RCTRL,_KEYBOARD]
KEY_LSHIFT = [pygame.K_LSHIFT,_KEYBOARD]
KEY_RSHIFT = [pygame.K_RSHIFT,_KEYBOARD]
KEY_RETURN = [pygame.K_RETURN,_KEYBOARD]
KEY_SPACE = [pygame.K_SPACE,_KEYBOARD]
KEY_ESCAPE = [pygame.K_ESCAPE,_KEYBOARD]
KEY_BACKSPACE = [pygame.K_BACKSPACE,_KEYBOARD]
KEY_DELETE = [pygame.K_DELETE,_KEYBOARD]
KEY_TAB = [pygame.K_TAB,_KEYBOARD]
KEY_HOME = [pygame.K_HOME,_KEYBOARD]
KEY_ARROW_LEFT = [pygame.K_LEFT,_KEYBOARD]
KEY_ARROW_RIGHT = [pygame.K_RIGHT,_KEYBOARD]
KEY_ARROW_UP = [pygame.K_UP,_KEYBOARD]
KEY_ARROW_DOWN = [pygame.K_DOWN,_KEYBOARD]

# Mouse input index
MOUSE_LEFTCLICK = [0,_MOUSE]
MOUSE_MIDDLECLICK = [1,_MOUSE]
MOUSE_RIGHTCLICK = [2,_MOUSE]

class Input:
    def __init__(self, engine) -> None:

        """
        Initialise the engines input system.

        The input system should help collect and read out many inputs by a specified key.

        Args:

        - engine (Engine): The engine to access specific variables.

        !!!This is only used internally by the engine and should not be called in an app!!!
        """

        # Engine variable
        self._engine = engine

        # Mouse variables        
        self.mouse = self._Mouse()

        # Keyboard variables
        self._keys = {}
        self._reset_keys = []

        # Input variables
        self.autosave = True
        self.save_path = os.path.join("data","saves","input")
        self._registered_input = {
            "accept":[[MOUSE_LEFTCLICK,CLICKED]],
            "cancel":[[KEY_ESCAPE,CLICKED]],
        }

        # Setting default value for keys
        for i in self._registered_input:
            for key in self._registered_input[i]:
                if key[0][1] == _KEYBOARD:
                    self._keys[key[0][0]] = [False,False,False]

    def new(self, name:str, key:list[int,int], method:int=1) -> bool:

        """
        Register or add a new input for read out later.

        Args:
        - name (str): The name of the input to register.
        - key: The input key which will be monitored.
        - method: The way the input is pressed: [CLICKED, PRESSED, RELEASE].

        Returns:
        - True if registration was successful.
        - False if input is already registered or something went wrong.

        If the variable autosave is True the new input is automatically saved and loaded.

        Example:
        ```
        self.input.new("move_left",KEY_ARROW_LEFT,PRESSED)
        ```
        """

        # Register/add new input
        try:
            if name not in self._registered_input:
                self._registered_input[name] = [[key,method]]
            else:
                if [key,method] not in self.registered_input[name]:
                    self._registered_input[name].append([key,method])
                else:
                    return False

            self._keys[key[0]] = [False,False,False]
            if self.autosave:
                self.save()
                self.load()
            return True
        except:
            return False

        
    def remove(self, inputname:str) -> bool:

        """ 
        Removes registered input.

        Args:
        - inputname (str): the name of the registered input to remove.

        Returns:
        - True if removal was successful.
        - False if something went wrong.

        If the variable autosave is True the removal of the input is automatically saved.

        Example:

        ```
        self.input.remove("move_left")
        ```
        registered inputs 

        - before removal:
        {"accept","cancel","right","left","up","down","screenshot","move_left"}

        - after removal:
        {"accept","cancel","right","left","up","down","screenshot"}
        """

        # Remove registered input
        try:
            del self._registered_input[inputname]
            if self.autosave:
                self.save()
                self.load()
            return True
        except:
            return False

    def reset(self, name:str, controller_index:int=-1):

        """
        Resets input to default value.

        Args:
        - name (str): The name of the input value to reset.
        - controller_index (int): Index or joystick id of the controller to reset.

        Returns:
        - True if reset was successful.
        - False if controller_index is out of range or something went wrong.

        Example:

        ```
        print(self.input.get("move_left"))
        >>> 1
        self.input.reset("move_left")
        print(self.input.get("move_left"))
        >>> 0
        ```
        """

        # Resets value of registered input to default

        try:
            for key in self._registered_input[name]:
                if key[0][1] == _KEYBOARD:
                    self._keys[key[0][0]] = [False,False,False]
                    
                # Mouse values
                elif key[0][1] == _MOUSE:
                    self.mouse.buttons[key[0][0]] = [False,False,False]

            return True
        except:
            return False

    def get(self, name:str, controller_index:int=-1) -> int|float:

        """
        Gets value of registered input.

        Args:
        - name (str): The name of the registered input to get a value from.
        - controller_index (int): Index or joystick id of the controller to get a value from.
        
        Returns:
        - Axis return value between -1.0 and 1.0.
        - Keys and buttons return either 0 or 1.
        - If return is 0 either the inputname or joystick dose not exist or input is on default value.

        Example:

        ```
        print(self.input.get("move_left"))
        >>> 1
        ```
        """

        # Get input value from registered input
        try:
            for key in self._registered_input[name]:

                # Keyboard values
                if key[0][1] == _KEYBOARD:
                    if self._keys[key[0][0]][key[1]]:
                        return 1

                # Mouse values
                elif key[0][1] == _MOUSE:
                    if self.mouse.buttons[key[0][0]][key[1]]:
                        return 1
        except:
            return 0

        return 0
    
    def set(self, name:str, keys:list[int,int]):

        """
        Register or add a new input to read out later.

        Args:
        - name (str): The name of the input to overwrite.
        - keys (list): Is a list of [key, method].
        - method: The way the input is pressed: [CLICKED, PRESSED, RELEASE].

        Returns:
        - True if registration was successful.
        - False if something went wrong.

        If the variable autosave is True the new input is automatically saved and loaded.

        Example:
        ```
        self.input.set("move_left",[[KEY_D,PRESSED],[KEY_ARROW_LEFT,PRESSED]])
        ```
        """

        # Sets key to new inputs
        try:
            self._registered_input[name] = key
            for key in self._registered_input[name]:
                if key[0][1] == _KEYBOARD:
                    self._keys[key[0][0]] = [False,False,False]

            if self.autosave:
                self.save()
                self.load()

            return True
        except:
            return False

    def save(self):

        """
        Saves registered inputs to file.

        Args:
        - no args are required.

        Returns:
        - True if save was successful.
        - False if something went wrong.

        Example:
        ```
        self.input.save()
        ```
        """

        # Save registered input in file
        try:
            with open(self.save_path,"w+") as f:
                json.dump(self._registered_input,f)
            return True
        except:
            return False

    def load(self):

        """
        Load registered inputs from file.

        Args:
        - no args are required.

        Returns:
        - True if load was successful.
        - False if something went wrong.

        Example:
        ```
        self.input.load()
        ```
        """

        # Load registered input in file
        try:
            with open(self.save_path,"r+") as f:
                self._registered_input = json.load(f)

                # Setting default value for keys
                for i in self._registered_input:
                    for key in self._registered_input[i]:
                        if key[0][1] == _KEYBOARD:
                            self._keys[key[0][0]] = [False,False,False]
            return True
        except:
            return False

    def _update(self) -> None:

        # Update all input devices
        for key in self._reset_keys.copy():
            self._keys[key][0] = False
            self._keys[key][2] = False
            self._reset_keys.remove(key)

        self.mouse._update()

    def _handle_key_event(self, event:pygame.Event):

        # Handel joystick button down event
        if event.type == pygame.KEYDOWN:
            self._keys[event.key] = [True,True,False]
            self._reset_keys.append(event.key)

        # Handel mouse button release event
        elif event.type == pygame.KEYUP:
            self._keys[event.key] = [False,False,True]
            self._reset_keys.append(event.key)

    def _handle_mouse_event(self, event:pygame.Event):
        # Handel joystick button down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse.buttons[event.button-1] = [True,True,False]

        # Handel mouse button release event
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse.buttons[event.button-1] = [False,False,True]

    class _Mouse:
        def __init__(self) -> None:

            # Mouse variables
            self.position = [0,0]
            self.buttons = [
                [False,False,False],
                [False,False,False],
                [False,False,False],
                [False,False,False],
                [False,False,False]
            ]

        def _update(self) -> None:

            # Reset mouse input values
            self.buttons[0][0] = False
            self.buttons[0][2] = False
            self.buttons[1][0] = False
            self.buttons[1][2] = False
            self.buttons[2][0] = False
            self.buttons[2][2] = False

            # Get mouse values
            self.position = [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
            mouse_pressed = pygame.mouse.get_pressed()
            self.buttons[0][1] = mouse_pressed[0]
            self.buttons[1][1] = mouse_pressed[1]
            self.buttons[2][1] = mouse_pressed[2]

        def get_pos(self) -> list[int,int]:

            """
            Returns mouse position relative to main window.

            Args:
            - no args are required.

            Returns:
            - List of [x mouse position (int), y mouse position (int)].

            Example:
            ```
            mouse_pos = self.input.mouse.get_pos()
            ```
            """

            # Getting mouse position
            return self.position

class Logger:
    def __init__(self,engine,delete_old_logs:bool=False) -> None:

        """
        Initialise the engines logging system.

        The logging system helps to log important information and collects error messages.

        Args:
        
        - engine (Engine): The engine to access specific variables.
        - delete_old_logs (bool)=False: If true there will only be the newest logfile.

        !!!This is only used internally by the engine and should not be called in an app!!!
        """

        # Engine variable
        self.engine = engine

        # Setting starting variables
        self.logpath = os.path.join("logs",f"{datetime.datetime.now().strftime('%d.%m.%y %H-%M-%S')}.log")
        self.last_logged_second = 0
        self.last_logged_message = ""
        self.repeat_log_times = 1
        self.time_format = "%d.%m.%y %H:%M:%S:%f"
        if delete_old_logs:
            self.logpath = os.path.join("logs","latest.log")

        if self.engine.logging:
            # Trying to create logfile
            try:

                # Create empty file
                if not os.path.exists(self.logpath):
                    if not os.path.exists("logs"):
                        os.mkdir("logs")
                    if delete_old_logs:
                        for filename in glob.glob("logs/*.log"):
                            os.remove(filename)
                    with open(self.logpath,"+w") as file:
                        file.write("")
            except Exception as e:

                # Creating logfile failed, printing instead
                print(f"[Engine {datetime.datetime.now().strftime(self.time_format)[:-4]}]: Could not create logfile ({e})")

    # Different log variants
    def error(self,message:str):

        """
        Logs an error.

        Args:

        - message (str): Content to log.

        Mostly used by the engine internally but can also be used for logging other error messages

        Example:
        ```
        self.logger.error("The Exception")
        ```
        """

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        self._log("Error",f"{message} in [{fname} line: {exc_tb.tb_lineno}]")

    def warning(self,message:str):

        """
        Logs a warning.

        Args:

        - message (str): Content to log.

        Example:
        ```
        self.logger.warning("Memory almost 80% filled!")
        ```
        """

        self._log("Warning",str(message))

    def info(self,message:str):

        """
        Logs an info.

        Args:

        - message (str): Content to log.

        Example:
        ```
        self.logger.info("I am a duck)
        ```
        """

        self._log("Info",str(message))

    def _log(self,prefix:str,message:str):

        """
        Writes logged content to file.

        Args:

        - prefix (str): Importance of content 
        - message (str): Content to write to logfile.

        !!!This is only used internally by the engine and should not be called in an app!!!
        """

        if self.engine.logging:
            caller = "Engine"
            try:
                if self.last_logged_message == message:

                    # Message is repeating
                    if self.last_logged_second != datetime.datetime.now().second:
                        self.last_logged_second = datetime.datetime.now().second

                        # Writing to logfile: caller + time + repeating count + log type + message
                        with open(self.logpath,"+at") as file:
                            self.repeat_log_times += 1
                            file.write(f"[{caller} {datetime.datetime.now().strftime(self.time_format)[:-4]}]: {prefix} | x{self.repeat_log_times} | {message}\n")
                else:

                    # Storing last message and timestamp
                    self.last_logged_second = datetime.datetime.now().second
                    self.last_logged_message = message
                    self.repeat_log_times = 1

                    # Writing to logfile: caller + time + log type + message
                    with open(self.logpath,"+at") as file:
                        file.write(f"[{caller} {datetime.datetime.now().strftime(self.time_format)[:-4]}]: {prefix} | {message}\n")
            except Exception as e:
                print(f"[Engine {datetime.datetime.now().strftime(self.file_name_option)[:-4]}]: Could not log message ({message}) | ({e})")

class SaveManager():

    """A class for managing encrypted storage data."""

    def __init__(self,engine,path="data/saves/save") -> None:

        """
        Initialize the SaveManager object.

        Args:

        - engine: Engine instance.
        - path (str): Path to the file to be managed. Defaults to "data/saves/save".
        """

        self.engine = engine
        self.path = path
        self.encryption_key = b"z8IwBgA-gFs66DrrM7JHtXe0fl9OVtL3A8Q-xU1nmAA="

    def set_encryption_key(self,encryption_key:bytes) -> None:

        """
        Set the encryption key for the SaveManager.

        Args:

        - encryption_key (bytes): New encryption key to be set.
        """

        self.encryption_key = encryption_key

    def generate_encryption_key(self) -> bytes:

        """
        Generate a new encryption key using Fernet.

        Returns:

        - bytes: Generated encryption key.
        """

        return Fernet.generate_key()

    def set_save_path(self,path:str) -> None:

        """
        Set the save path for the SaveManager.

        Args:

        - path (str): New path to be set for saving data.
        """

        self.path = path

    def _encrypt(self,data:dict) -> bool:

        """
        !Used for internal functionality!
        Encrypt the provided data using Fernet encryption.

        Args:

        - data (dict): Data to be encrypted (as a dictionary).

        Returns:

        - bool: True if encryption is successful, False otherwise.
        """

        try:
            fernet = Fernet(self.encryption_key)
            encrypted_data = fernet.encrypt(bytes(json.dumps(data,ensure_ascii=True).encode("utf-8")))

            with open(self.path, 'wb') as file:
                file.write(encrypted_data)
        except Exception as e:
            self.engine.logger.error(e)

    def _decrypt(self) -> bool|dict:

        """
        !Used for internal functionality!
        Decrypt the data in the file specified by the path using Fernet decryption.

        Returns:

        - bool | dict: Decrypted data as a dictionary if successful, False otherwise.
        """

        try:
            with open(self.path, 'rb') as file:
                data = file.read()
            if data != b'':
                fernet = Fernet(self.encryption_key)
                return json.loads(fernet.decrypt(data))
            
        except Exception as e:
            self.engine.logger.error(e)

        return False

    def save(self,key,value) -> bool:

        """
        Save data to the file using a specified key-value pair.

        Args:

        - key: Key for the data.
        - value: Value to be saved corresponding to the key.

        Returns:

        - bool: True if saving is successful, False otherwise.
        """

        try:
            data = self._decrypt()
            if data != False:
                data[key] = value
            else:
                data = {}
            self._encrypt(data)
            return True
        except Exception as e:
            self.engine.logger.error(e)

        return False

    def load(self,key,default=None) -> any:

        """
        Load data from the file using the specified key.

        Args:

        - key: Key to retrieve data.
        - default: If key is not found, default will be returned instead.

        Returns:

        - any: Retrieved value corresponding to the key, or default value if not found.
        """

        if os.path.exists(self.path):
            try:
                data = self._decrypt()
                if data != False:
                    if key in data:
                        return data[key]
                    else:
                        return default
            except Exception as e:
                self.engine.logger.error(e)
        else:
            return default

    def backup(self,backup_path:str="data/saves/backup"):

        """
        Create a backup of the current save file.

        Args:

        - backup_path (str): Path to store the backup file. Defaults to "data/saves/backup".
        """

        shutil.copyfile(
            self.path,
            os.path.join(backup_path,f'{os.path.split(self.path)[-1]}-{datetime.datetime.now().strftime("%d.%m.%y %H-%M-%S")}')
            )

class Window:
    def __init__(self,engine,set_window_size=None,fullscreen=False,resizable=True,windowless=False,window_centered=True,vsync=False,window_name="Frostlight Engine",mouse_visible=True,color_depth=24) -> None:

        """
        Initialise the engines window system.

        The window system manages all window events and rendering.

        Args:

        - engine (Engine): The engine to access specific variables.
        - set_window_size (list)=None: Size of window.
        - fullscreen (bool)=False: Sets windows fullscreen mode.
        - resizable (bool)=True: Sets windows resizability.
        - windowless (bool)=False: Removes window interaction menu at the top.
        - window_centered (bool)=True: Sets window centered state.
        - vsync (bool)=False: Sets vsync state.
        - window_name (str)="Frostlight Engine": Default name to display.
        - mouse_visible (bool)=True: mouses visibility state.
        - color_depth (int)=24: Window color depth.

        !!!This is only used internally by the engine and should not be called in an app!!!
        """

        # Engine Variable
        self.engine = engine

        # Setting startup variables
        self.windowless = windowless
        self.window_centered = window_centered
        self.vsync = vsync
        self.color_depth = color_depth
        self.fullscreen = fullscreen
        self.window_name = window_name
        self.mouse_visible = mouse_visible
        self.window_size = set_window_size
        self.resizable = resizable
        self.icon = None

    def _create(self):

        """
        Creates main window instance.

        Args:

        - no args are required.

        !!!This is only used internally by the engine and should not be called in an app!!!
        """

        if not self.windowless:
            pygame.display.init()

            # Center window
            if self.window_centered:
                os.environ['SDL_VIDEO_CENTERED'] = '1'
            else:
                os.environ['SDL_VIDEO_CENTERED'] = '0'

            # Create window
            display_size = [int(pygame.display.Info().current_w),int(pygame.display.Info().current_h)]
            if self.fullscreen: 

                # Fullscreen window
                self.main_surface = pygame.display.set_mode(display_size,pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN,vsync=self.vsync,depth=self.color_depth)
            else:

                # Calculate fitting window size
                if self.window_size == None:
                    self.window_size = [display_size[0],display_size[1]*0.94]

                if self.resizable:

                    # Resizable window
                    self.main_surface = pygame.display.set_mode(self.window_size,pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,vsync=self.vsync,depth=self.color_depth)
                else: 

                    # Fixed size window
                    self.main_surface = pygame.display.set_mode(self.window_size,pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME,vsync=self.vsync,depth=self.color_depth)

            # Change window attributes
            pygame.display.set_caption(self.window_name)
            pygame.mouse.set_visible(self.mouse_visible)
            if self.icon != None:
                pygame.display.set_icon(self.icon)

    def render(self,sprite:pygame.Surface,pos:list[int,int] | pygame.Rect):

        """
        Renders a sprite to the main window.

        Args:

        - sprite (pygame.Surface): The sprite to render.
        - pos (list[int,int]): The position to render the sprite to.

        Example:
        ```
        self.window.render(player_sprite,player_pos)
        ```
        """

        # Renders sprite to main window
        self.main_surface.blit(sprite,pos)

    def resize(self,new_window_size:list[int,int]):

        """
        Resizes the main window.

        Args:

        - new_window_size (list[int,int]): The new window size.

        Example:
        ```
        self.window.resize([600,600])
        ```
        """

        # Resize window to specified size        
        self.window_size = new_window_size

        if self.resizable:

            # Resizable window 
            self.main_surface = pygame.display.set_mode(self.window_size,pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE,vsync=self.vsync,depth=self.color_depth)
        else: 

            # Fixed size window
            self.main_surface = pygame.display.set_mode(self.window_size,pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME,vsync=self.vsync,depth=self.color_depth)

    def set_fullscreen(self,fullscreen:bool):

        """
        Changes window fullscreen state.

        Args:

        - fullscreen (bool): Fullscreen state.

        Example:
        ```
        self.window.set_fullscreen(True)
        ```
        """

        # Set fullscreen variable
        self.fullscreen = fullscreen
        pygame.display.quit()
        self._create()

    def toggle_fullscreen(self):

        """
        Toggles window fullscreen state.

        Args:

        - no args are required.

        Example:
        ```
        self.window.toggle_fullscreen()
        ```
        """

        # Set Fullscreen variable to opposite truth value
        self.set_fullscreen(not(self.fullscreen))

    def set_name(self,name:str="") -> None:

        """
        Set a window name.

        Args:

        - name (str)="": New window name.

        Example:
        ```
        self.window.set_name("new app")
        ```
        """

        # Renaming the displayed window title
        pygame.display.set_caption(str(name))

    def get_fps(self) -> int:

        """
        Returns apps fps value.

        Args:

        - no args are required.

        Returns:

        - FPS value as integer.

        Example:
        ```
        self.window.set_name(self.window.get_fps())
        ```
        """

        # Returning frames per second as integer
        return int(min(self.engine.clock.get_fps(),99999999))
    
    def fill(self,color:list[int,int,int]) -> None:

        """
        Fills window with a color.

        Args:

        - color (list[int,int,int]): Color the window is filled with.

        Example:
        ```
        self.window.fill([3,13,36])
        ```
        """

        # Fills the screen with a solid color
        self.main_surface.fill(color)
    
    def get_size(self) -> list[int,int]:

        """
        Returns window size as list.

        Args:

        - no args are required.

        Returns:

        - Window size as list of integers.

        Example:
        ```
        print(self.window.get_size())
        ```
        """

        # Returning window size as a list of integers
        return self.window_size

    def set_icon(self,icon:pygame.Surface):
        self.icon = icon
        pygame.display.set_icon(self.icon)

class Engine:
    def __init__(self,
                 catch_error:bool=True,
                 color_depth:int=16,
                 delete_old_logs:bool=False,
                 fps:int=0,
                 fullscreen:bool=False,
                 app_version:str="1.0",
                 language:str="en",
                 logging:bool=True,
                 mouse_visible:bool=True,
                 nowindow:bool=False,
                 resizable:bool=True,
                 sounds:bool=True,
                 vsync:bool=False,
                 window_centered:bool=True,
                 window_name:str="New app",
                 window_size:list=None):

        # initialize all modules
        pygame.init()
        pygame.joystick.init()
        if sounds:
            pygame.mixer.pre_init(44100,-16,2,512)

        # Boolean variables go here
        self.catch_error = catch_error
        self.logging = logging
        self.run_app = True
        self.sounds = sounds

        # Integer and float variables go here
        self.fps = fps
        self.delta_time = 1
        self.last_time = time.time()

        # String variables go here
        self.engine_version = "1.1.0"
        self.app_state = "intro"
        self.app_version = app_version
        self.language = language

        # List variables go here
        self.display_update_rects = []

        # Object variables go here
        self.clock = pygame.time.Clock()
        self._builder = Builder(self)
        self.logger = Logger(self,delete_old_logs)
        self.input = Input(self)
        self.save_manager = SaveManager(self,os.path.join("data","saves","save"))
        self.window = Window(self,window_size,fullscreen,resizable,nowindow,window_centered,vsync,window_name,mouse_visible,color_depth)

        # Object processing go here
        self.window._create()
        pygame.event.set_allowed([pygame.QUIT,
                                  pygame.WINDOWMOVED, 
                                  pygame.VIDEORESIZE, 
                                  pygame.KEYDOWN,
                                  pygame.KEYUP,
                                  pygame.MOUSEBUTTONDOWN,
                                  pygame.MOUSEBUTTONUP])

    def _get_events(self):
        self.clock.tick(self.fps)
        self.input._update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event_quit()
                self.quit()

            # Window events
            elif event.type == pygame.WINDOWMOVED:
                self.last_time = time.time()
                self.delta_time = 0
                self.event_window_move([event.x,event.y])

            elif event.type == pygame.VIDEORESIZE:
                if not self.window.fullscreen:
                    self.last_time = time.time()
                    self.delta_time = 0
                    self.window.resize([event.w,event.h])
                    self.event_window_resize([event.w,event.h])

            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                self.input._handle_key_event(event)
                if event.key == pygame.K_F11:
                    self.window.toggle_fullscreen()
                self.event_keydown(event.key,event.unicode)

            elif event.type == pygame.KEYUP:
                self.input._handle_key_event(event)
                self.event_keyup(event.key,event.unicode)

            # Mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.input._handle_mouse_event(event)
                self.event_mouse_buttondown(event.button,event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.input._handle_mouse_event(event)
                self.event_mouse_buttonup(event.button,event.pos)

    def event_quit(self):

        # Event function to overwrite on quit
        """
        This function can be overwritten to react to the app quit event.
        Event is called before the app closes.

        Args:

        - No args are required.

        Example:
        ```
        def event_quit(self):
            print("app end")
        ```
        """

    def event_window_move(self,position:list[int,int]):

        # Event function to overwrite on window move
        """
        This function can be overwritten to react to the window move event.
        Event is called after the window moved.

        Args:

        - position (list[int,int]): Monitor position to where to window moved.

        Example:
        ```
        def event_window_move(self,position:list[int,int]):
            print(f"The window moved to: {position}")
        ```
        """

    def event_window_resize(self,size:list[int,int]):

        # Event function to overwrite on window resize
        """
        This function can be overwritten to react to the window resize event.
        Event is called after the window is resized.

        Args:

        - size (list[int,int]): New window size.

        Example:
        ```
        def event_window_resize(self,size:list[int,int]):
            print(f"The window was resized to: {size}")
        ```
        """

    def event_keydown(self,key:int,unicode:str):

        # Event function to overwrite on keypress
        """
        This function can be overwritten to react to the keypress event.
        Event is called after a key is pressed.

        Args:

        - key (int): Index of pressed key.
        - unicode (str): Displayable unicode of key.

        Example:
        ```
        def event_keydown(self,key:int,unicode:str):
            print(f"Key {unicode} with id {key} was pressed")
        ```
        """

    def event_keyup(self,key:int,unicode:str):

        # Event function to overwrite on key release
        """
        This function can be overwritten to react to the key release event.
        Event is called after a key is released.

        Args:
        
        - key (int): Index of released key.
        - unicode (str): Displayable unicode of key.

        Example:
        ```
        def event_keyup(self,key:int,unicode:str):
            print(f"Key {unicode} with id {key} was released")
        ```
        """

    def event_mouse_buttondown(sefl,button:int,position:list[int,int]):

        # Event function to overwrite on mouse click
        """
        This function can be overwritten to react to a mouse click.
        Event is called after the mouse is clicked.

        Args:

        - button (int): Index of clicked button.
        - position (list[int,int]): Position the mouse was on when clicked.

        Example:
        ```
        def event_mouse_buttondown(sefl,button:int,position:list[int,int]):
            print(f"Mouse button {button} was pressed at position {position}}")
        ```
        """

    def event_mouse_buttonup(sefl,button:int,position:list[int,int]):

        # Event function to overwrite on mouse release
        """
        This function can be overwritten to react to a mouse button release.
        Event is called after the mouse button is released.

        Args:

        - button (int): Index of released button.
        - position (list[int,int]): Position the mouse was on when released.

        Example:
        ```
        def event_mouse_buttonup(sefl,button:int,position:list[int,int]):
            print(f"Mouse button {button} was released at position {position}}")
        ```
        """

    def _engine_update(self):

        # Update that runs before normal update
        self.delta_time = time.time()-self.last_time
        self.last_time = time.time()

    def _engine_draw(self):

        # Draw that runs after normal draw
        pygame.display.update()

    def run(self):

        """
        This function starts the main app loop

        Args:

        - No args are required.

        Example:
        ```
        if __name__ == "__main__"
            app = app()
            app.run()
        ```
        """

        # Starting app engine
        self.logger.info(f"Starting [Engine version {self.engine_version} | app version {self.app_version}]")
        if self.catch_error:
            while self.run_app:

                # Main loop
                try:
                    self._get_events()
                    self._engine_update()
                    self.update()
                    self.draw()
                    self._engine_draw()
                except Exception as e:

                    # Error logging and catching
                    self.logger.error(e)
        else:
            while self.run_app:

                # Main loop
                self._get_events()
                self._engine_update()
                self.update()
                self.draw()
                self._engine_draw()

        # Ending app
        self.logger.info("Closed app")

    def quit(self):

        """
        This function closes the app loop

        Args:

        - No args are required.

        Example:
        ```
        i = 0
        while True:
            i += 1
            if i == 10:
                self.quit()
        ```
        """

        # Quit app loop
        self.run_app = False

if __name__ == "__main__":

    # Parser arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pack", action="store_true")
    parser.add_argument("-b", "--build", action="store_true")
    parser.add_argument("-n", "--name", action="store_true")
    args = parser.parse_args()

    if args.pack:

        # Pack Engine for release
        engine = Engine(nowindow=True)
        engine._builder._pack_release()

    elif args.build:

        # Build app to EXE
        engine = Engine(nowindow=True)
        engine._builder._setup()
        engine._builder._create_exe()

    elif args.name: 

        # Setup new Project with name
        engine = Engine(nowindow=True)
        engine._builder._setup(args.name)

    else:

        # Setup new no name Project
        engine = Engine(nowindow=True)
        engine._builder._setup()