import pygame as pg
from pygame import Color

from os import path
from random import randint

from vector import Vec2
from config import Config
from touchpad import Touchpad
from brushes import *
from line_cleaner import cleanup_line

pg.init()
clock = pg.time.Clock()

canvas = Config().canvas_size
window = Config().window_size

win = pg.display.set_mode((window.x, window.y))
pg.display.set_caption("Sketchpad with touchpad")

font : pg.font.Font = pg.font.SysFont("monospace", 20)

tp : Touchpad = Touchpad()

drawing : pg.Surface = pg.surface.Surface((canvas.x, canvas.y))
drawing.fill(Color(0, 0, 0))
drawing_pos : Vec2 = Vec2()
drawing_zoom : float = 1.0

last_point : Vec2 | None = None
ignore : bool = False
moving : bool = False
hover : bool = True

# Extra modes
adjusting : bool = False
editing_text : bool = False
input_text : str = ""

brushes : list[Brush] = [PaintBrush(), Eraser()]
width_vel : float = 1.0
curr_brush : int = 0

MAX_UNDO : int = 32
undo_buffer : list[pg.Surface] = []
redo_buffer : list[pg.Surface] = []

def add_undo():
    global undo_buffer
    undo_buffer.append(drawing.copy())
    undo_buffer = undo_buffer[-MAX_UNDO:]

def add_redo():
    global redo_buffer
    redo_buffer.append(drawing.copy())
    redo_buffer = redo_buffer[-MAX_UNDO:]

def reset_brush():
    global last_point, tp, ignore
    add_undo()
    redo_buffer.clear()
    last_point = None
    tp.just_pressed = False
    ignore = False

def input_field(event):
    global input_text, editing_text, drawing
    if event.type == pg.TEXTINPUT:
        input_text += event.text
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_BACKSPACE:
            input_text = input_text[:-1]
        elif event.key == pg.K_RETURN:
            editing_text = False
            pg.key.stop_text_input()
            pg.image.save(drawing, path.join(path.dirname(__file__), Config().save_dir, input_text))
        elif event.key == pg.K_ESCAPE:
            editing_text = False
            pg.key.stop_text_input()

def controls(key, down : bool = False):
    global tp, ignore, hover, moving, brushes, curr_brush, drawing, undo_buffer, redo_buffer, width_vel, drawing_zoom, editing_text, input_text, adjusting
    if key == pg.K_ESCAPE and down:
        pg.quit()
        exit()
    elif key == pg.K_z and undo_buffer and down:
        add_redo()
        drawing = undo_buffer.pop()
        ignore = True
    elif key == pg.K_y and redo_buffer and down:
        add_undo()
        drawing = redo_buffer.pop()
        ignore = True
    elif key == pg.K_x and down:
        curr_brush = (curr_brush + 1) % len(brushes)
        ignore = True
    elif key == pg.K_UP:
        width_vel = 1.025 if down else 1.0
    elif key == pg.K_DOWN:
        width_vel = 0.975 if down else 1.0
    elif key == pg.K_SPACE and not moving:
        if hover:
            reset_brush()
        hover = not hover
    elif key == pg.K_f and down and not moving:
        if hover:
            reset_brush()
        hover = not hover
    elif key == pg.K_g and down:
        tp.grabbing = not tp.grabbing
    elif key == pg.K_EQUALS or key == pg.K_PLUS and down:
        drawing_zoom = min(1.05 * drawing_zoom, 2.0)
    elif key == pg.K_MINUS or key == pg.K_UNDERSCORE and down:
        drawing_zoom = max(0.95 * drawing_zoom, 0.25)
    elif key == pg.K_s and down and adjust_step == 0:
        input_text = ""
        editing_text = True
        pg.key.start_text_input()
    elif key == pg.K_a and down:
        adjusting = True

def transform(p : Vec2):
    global window, drawing_zoom, drawing_pos
    return (p * Config().input_scale - drawing_pos) / drawing_zoom

while True:
    if not hover and tp.just_pressed:
        reset_brush()

    points : list[tuple[int, int]] = [transform(last_point)] if last_point else []
    points.extend([transform(p) for p in tp.positions])

    if len(tp.positions) > 0:
        if not ignore and not hover:
            brushes[curr_brush].apply(drawing, points)
        if moving:
            if tp.just_pressed:
                last_point = None
                tp.just_pressed = False
            if last_point:
                drawing_pos += tp.positions[-1] - last_point
        last_point = tp.positions[-1]
        tp.positions.clear()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if not editing_text and not adjusting and (event.type == pg.KEYDOWN or event.type == pg.KEYUP):
            controls(event.key, event.type == pg.KEYDOWN)
        elif editing_text and (event.type == pg.TEXTINPUT or event.type == pg.KEYDOWN):
            input_field(event)
        elif adjusting and (event.type == pg.KEYDOWN):
            if event.key == pg.K_RETURN and last_point != None:
                Config().input_scale = window / last_point
                adjusting = False

    if tp.keys["BTN_TOOL_DOUBLETAP"] and hover:
        moving = not moving
        tp.keys["BTN_TOOL_DOUBLETAP"] = False

    brushes[curr_brush].width *= width_vel

    win.fill(Color(0, 0, 0))

    drawing_rect = (int(drawing_pos.x), int(drawing_pos.y), int(canvas.x * drawing_zoom), int(canvas.y * drawing_zoom))
    win.blit(pg.transform.scale(drawing, drawing_rect[2:]), drawing_rect)
    pg.draw.rect(win, Color(125,125,255), drawing_rect, width=1)

    if last_point:
        brushes[curr_brush].display(win, last_point * Config().input_scale, drawing_zoom)

    if adjusting:
        text : pg.Surface = font.render(
            "Touch bottom right corner of touchpad, then press ENTER",
            True, Color(255, 0, 0)
        )
        win.blit(text, (window.x / 2 - text.get_width() / 2, window.y / 2 - 12))

    if editing_text:
        text : pg.Surface = font.render(input_text, True, Color(100, 0, 200))
        pg.draw.rect(win, Color(150, 150, 150), (window.x / 3, window.y / 2 - 12, window.x / 3, 24))
        pg.draw.rect(win, Color(200, 0, 0), (window.x / 3, window.y / 2 - 12, window.x / 3, 24), width=4)
        win.blit(text, (window.x / 3 + 5, window.y / 2 - 12))

    pg.display.update()
    clock.tick(60)
