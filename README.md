## Clippin – Clipboard Image → OBS Source

This script watches for **Ctrl+V** and, when your clipboard contains an image, sends that image to OBS as an `image_source` in the current scene.

### Requirements

- **Python**: 3.9 or newer
- **OBS Studio** with the **WebSocket server enabled**
  - OBS 28+ has WebSocket built-in (check `Tools → WebSocket Server Settings`)
  - Note the **port** and **password**
- **Packages** (installed via `requirements.txt`):
  - `Pillow`
  - `obsws-python`
  - `keyboard`

On **macOS**, you may need to grant your terminal / Python:

- **Accessibility** permission (for global hotkeys via `keyboard`)
- **Screen Recording** / **Screen Capture** permission (for `ImageGrab`)

You will be prompted by macOS the first time, or you can adjust these under **System Settings → Privacy & Security**.

### Installation

From the `Clippin` folder:

```bash
# (optional) create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

### OBS Configuration

1. Open OBS.
2. Go to `Tools → WebSocket Server Settings`.
3. Ensure the server is **enabled**.
4. Note the **port** (default `4455`) and **password**.

Then, in `main.py`, update:

- `OBS_HOST` (usually `"localhost"`)
- `OBS_PORT` (e.g. `4455`)
- `OBS_PW` (set this to your OBS WebSocket password)

You can also change:

- `SAVE_PATH`: where the temporary `pasted_image.png` file is stored
- `SOURCE_NAME`: the OBS source name to create/update (default `Clipboard_Paste`)

### Running the Script

From the `Clippin` folder (and with your virtual environment activated, if you use one):

```bash
python main.py
```

You should see log messages like:

- Connecting to OBS
- Whether the connection succeeded
- Instructions about pressing **Ctrl+V**

Leave the script running in the terminal.

### Using It

1. Make sure **OBS is running** and connected (no error in the script output).
2. Copy an **image** to your clipboard (for example, take a screenshot or copy an image from a browser).
3. Press **Ctrl+V** anywhere.
4. The script will:
   - Read the clipboard
   - If it finds an image, save it to `pasted_image.png`
   - Create or update an OBS `image_source` named `Clipboard_Paste` in the current scene

If the clipboard does **not** contain an image, the script will log that and do nothing.

### Stopping the Script

In the terminal where it is running, press:

- **Ctrl+C**

This will stop the hotkey listener and exit the script.

### Troubleshooting

- **Cannot connect to OBS WebSocket**
  - Verify OBS is running.
  - Check that WebSocket server is enabled and the port/password match the values in `main.py`.
  - Ensure no firewall is blocking the port (default `4455`).
- **Ctrl+V does nothing**
  - Make sure the terminal/Python process has **Accessibility** permissions (macOS).
  - Confirm that the clipboard actually contains an image (not text).
- **No image appears in OBS**
  - Check the script output for errors.
  - Confirm you are looking at the **current program scene** in OBS.
  - Look for the `Clipboard_Paste` source in the scene and ensure it is visible.

