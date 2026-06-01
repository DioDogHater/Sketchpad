from __future__ import annotations

import evdev
from evdev import InputDevice, categorize, ecodes

from config import Config
from vector import Vec2

from threading import Thread

class Touchpad:
    __instance : Touchpad | None = None
    __thread : Thread | None = None

    def __start(self):
        self.__device : InputDevice = InputDevice(Config().touchpad)
        self.__device.grab()
        self.__grabbing : bool = True
        self.__last_pos : Vec2 = Vec2()
        self.__positions : list[Vec2] = []
        self.__first_update : bool = False
        self.__just_pressed : bool = False
        self.__keys : dict[str, bool] = {"BTN_TOUCH" : False, "BTN_TOOL_DOUBLETAP" : False, "BTN_TOOL_TRIPLETAP" : False}

    def __loop(self):
        # Code from stackoverflow
        # Loop to continuously read touchpad events
        for event in self.__device.read_loop():
            if event.type == ecodes.EV_ABS:
                # Handle absolute axis events
                abs_event : evdev.AbsEvent = categorize(event)
                if abs_event.event.code == ecodes.ABS_X:
                    self.__last_pos = Vec2(abs_event.event.value, self.__last_pos.y)
                    if not self.__first_update:
                        self.__positions.append(self.__last_pos)
                elif abs_event.event.code == ecodes.ABS_Y:
                    self.__last_pos = Vec2(self.__last_pos.x, abs_event.event.value)
                    if not self.__first_update:
                        self.__positions.append(self.__last_pos)
                self.__first_update = False
            elif event.type == ecodes.EV_KEY:
                # Handle key events (like tapping)
                key_event : evdev.KeyEvent = categorize(event)
                self.__keys[key_event.keycode] = (key_event.keystate == 1)
                if key_event.keycode == "BTN_TOUCH" and key_event.keystate == 1:
                    self.__first_update = True
                    self.__just_pressed = True

    @property
    def last_pos(self) -> Vec2:
        return self.__last_pos

    @property
    def positions(self) -> list[Vec2]:
        return self.__positions

    @property
    def keys(self) -> dict[str, bool]:
        return self.__keys

    @property
    def just_pressed(self) -> bool:
        return self.__just_pressed

    @just_pressed.setter
    def just_pressed(self, value : bool):
        if not isinstance(value, bool):
            raise TypeError("value must be a bool")
        self.__just_pressed = value

    @property
    def grabbing(self) -> bool:
        return self.__grabbing

    @grabbing.setter
    def grabbing(self, value : bool):
        if not isinstance(value, bool):
            raise TypeError("value must be a bool")
        self.__grabbing = value
        if value:
            print("grab")
            self.__device.grab()
        else:
            print("ungrab")
            self.__device.ungrab()

    def __new__(cls) -> Touchpad:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__start()
            cls.__thread = Thread(target=cls.__instance.__loop, daemon=True)
            cls.__thread.start()
        return cls.__instance
