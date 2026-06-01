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
- Edit `config.json` and put replace `/dev/input/eventX` with what you got
- Run using `sudo python3 main.py`

## Important notice
There are times where after restarting your computer, the event used by your
touchpad changes. **Please check every first time you use the program if the**
**event has changed since last session.**
