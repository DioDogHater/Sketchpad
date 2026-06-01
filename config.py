from __future__ import annotations
from os import path
import json

from vector import Vec2

class Config:
    """Singleton in charge of reading configuration."""
    __instance : Config | None = None
    __path : str = path.join(path.dirname(__file__), "config.json")

    def __get_entry(self, entry : str, expected_type : type | tuple[type, ...], default_val = None):
        """Checks the validity of the entry and returns its value.
        Args:
            entry (str) : the key of the entry.
            expected_type (type | tuple[type, ...]) : the expected type of the value in the entry.
            default_val (Any | None) : default value of the entry.
        Returns:
            Any : returns the value of the entry or default_val if default_val != None.
        Raises:
            KeyError : if the entry is not in config.json and there is no default value.
            TypeError : if the entry value is not of the expected type."""
        val = self.__data.get(entry, default_val)
        if val is None:
            raise KeyError(f"Missing '{entry}' entry in config.json")
        if not isinstance(val, expected_type):
            raise TypeError(f"Entry '{entry}' in config.json must be type {expected_type}, got {type(val)} instead.")
        return val

    def __read(self):
        """Reads the config data from config.json."""
        with open(Config.__path, "r") as f:
            self.__data : dict = json.load(f)
        self.__touchpad : str = self.__get_entry("touchpad", str)
        self.__input_scale : Vec2 = Vec2(self.__get_entry("x_scale", (int, float), 1.0), self.__get_entry("y_scale", (int, float), 1.0))
        self.__canvas_size : Vec2 = Vec2(self.__get_entry("canvas_width", int, 1100), self.__get_entry("canvas_height", int, 700))
        self.__window_size : Vec2 = Vec2(self.__get_entry("window_width", int, 1100), self.__get_entry("window_height", int, 700))
        if self.__canvas_size.x <= 0 or self.__canvas_size.y <= 0:
            raise ValueError(f"Canvas dimensions {self.__canvas_size} in config.json are invalid")
        if self.__window_size.x <= 0 or self.__window_size.y <= 0:
            raise ValueError(f"Window dimensions {self.__window_size} in config.json are invalid")
        self.__save_dir : str = self.__get_entry("save_directory", str)

    def __write(self):
        """Writes the config data to config.json."""
        with open(Config.__path, "w") as f:
            json.dump(self.__data, f)

    def __new__(cls) -> Config:
        """Creates the singleton or returns its instance.
        Returns:
            Config : the config Singleton instance."""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__read()
        return cls.__instance

    @property
    def touchpad(self) -> str:
        """Path to the touchpad event."""
        return self.__touchpad

    @touchpad.setter
    def touchpad(self, value : str):
        if not isinstance(value, str):
            raise TypeError(f"value must be of type str, got {type(value)} instead.")
        self.__data["touchpad"] = self.__touchpad = value
        self.__write()

    @property
    def input_scale(self) -> Vec2:
        return self.__input_scale

    @input_scale.setter
    def input_scale(self, value : Vec2):
        if not isinstance(value, Vec2):
            raise TypeError(f"value must be of type str, got {type(value)} instead.")
        self.__input_scale = value
        self.__data["x_scale"] = value.x
        self.__data["y_scale"] = value.y
        self.__write()

    @property
    def canvas_size(self) -> Vec2:
        """Size of the drawing canvas."""
        return self.__canvas_size

    @canvas_size.setter
    def canvas_size(self, value : Vec2):
        if not isinstance(value, Vec2):
            raise TypeError(f"value must be of type Vec2, got {type(value)} instead.")
        self.__canvas_size = value
        self.__data["canvas_width"] = value.x
        self.__data["canvas_height"] = value.y
        self.__write()

    @property
    def window_size(self) -> Vec2:
        """Size of the window."""
        return self.__window_size

    @window_size.setter
    def window_size(self, value : Vec2):
        if not isinstance(value, Vec2):
            raise TypeError(f"value must be of type Vec2, got {type(value)} instead.")
        self.__window_size = value
        self.__data["window_width"] = value.x
        self.__data["window_height"] = value.y
        self.__write()

    @property
    def save_dir(self) -> str:
        """Save directory for images."""
        return self.__save_dir

    @save_dir.setter
    def save_dir(self, value : str):
        if not isinstance(value, str):
            raise TypeError(f"value must be of type str, got {type(value)} instead.")
        self.__save_dir = value
        self.__data["save_dir"] = value
        self.__write()
