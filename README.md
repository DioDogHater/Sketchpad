# Sketchpad
### Barebones paint program for the touchpad
Very useful to sketch easily by only drawing with your touchpad.
<br></br>

## Controls
- Enable / disable drawing using **SPACE** (hold) and **F** (toggle)
- Switch from brush / eraser with **X**
- Undo / redo with **Z** and **Y** respectively
- Move the canvas (when drawing is disabled) by **double tapping**, dragging, then **double tapping** again
- Zoom / unzoom with **+** and **-** respectively
- Increase / decrease brush size with **&uarr;** and **&darr;**
- Save with **S** by entering the filename (with extension) and pressing **Enter** or **Escape** to cancel
- Unlock mouse with **G**
- Quit with **Escape**
<br></br>

## Setup
- **Only Linux X11 desktops are supported**
- Python 3.13+ required
- `pip install evdev`
- Find touchpad's `/dev/input/eventX` by running `cat /proc/bus/input/devices`
- Edit `config.json` and put replace `/dev/input/event9` with what you got
- Run using `sudo python3 main.py`
