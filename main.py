import time
import os
import sys

from PIL import ImageGrab
import obsws_python as obs
import keyboard

# --- CONFIGURATION ---

OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PW = "your_password_here"  # Change this to your OBS WebSocket password

SAVE_PATH = os.path.join(os.getcwd(), "pasted_image.png")
SOURCE_NAME = "Clipboard_Paste"

# ---------------------


def make_obs_client():
    """Create an OBS WebSocket client with simple, clear error messages."""
    try:
        print(f"[INFO] Connecting to OBS at {OBS_HOST}:{OBS_PORT} ...")
        client = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PW, timeout=5)
        # Simple test call to verify connection
        _ = client.get_version()
        print("[OK] Connected to OBS WebSocket successfully.")
        return client
    except Exception as e:
        print("\n[ERROR] Could not connect to OBS WebSocket.")
        print("Common causes:")
        print("  - OBS is not running.")
        print("  - WebSocket server is not enabled in OBS (Tools → WebSocket Server Settings).")
        print("  - The password or port in this script does not match OBS settings.")
        print(f"Details: {e}\n")
        return None


def update_obs_image(client, path):
    """Create or update the image source in OBS."""
    if client is None:
        print("[ERROR] No OBS connection; cannot update image.")
        return

    try:
        scene = client.get_current_program_scene().scene_name
        print(f"[INFO] Using current scene: {scene}")

        # Check if the source already exists to avoid duplicates
        items = client.get_scene_item_list(scene).scene_items

        # obsws-python returns scene_items as a list of dict-like objects
        exists = any(item.get("sourceName") == SOURCE_NAME for item in items)

        if not exists:
            print(f"[INFO] Source '{SOURCE_NAME}' not found. Creating it...")
            client.create_input(
                scene_name=scene,
                input_name=SOURCE_NAME,
                input_kind="image_source",
                input_settings={"file": path},
                scene_item_enabled=True,
            )
            print(f"[OK] Source '{SOURCE_NAME}' created and image set to: {path}")
        else:
            print(f"[INFO] Source '{SOURCE_NAME}' exists. Updating image file...")
            client.set_input_settings(SOURCE_NAME, {"file": path}, True)
            print(f"[OK] Source '{SOURCE_NAME}' updated with image: {path}")

    except Exception as e:
        print("\n[ERROR] Problem while talking to OBS.")
        print("This might mean the scene changed, or OBS blocked the request.")
        print(f"Details: {e}\n")


def handle_paste(client):
    """Handler called when Ctrl+V is pressed."""
    img = ImageGrab.grabclipboard()

    if img is None:
        print("[INFO] Ctrl+V pressed, but clipboard does not contain an image.")
        return

    try:
        img.save(SAVE_PATH, "PNG")
        print(f"[OK] Ctrl+V: saved clipboard image to: {SAVE_PATH}")
        update_obs_image(client, SAVE_PATH)
    except Exception as e:
        print("\n[ERROR] Could not save or send the image after Ctrl+V.")
        print("Is the disk full or is the path writable?")
        print(f"Details: {e}\n")


def run_with_hotkey():
    print("=================================================")
    print(" Clipboard → OBS Image Script")
    print("=================================================")
    print("What this does:")
    print("  - Waits for you to press Ctrl+V.")
    print("  - When you press Ctrl+V, it reads the clipboard.")
    print("  - If the clipboard has an IMAGE, it appears in OBS")
    print(f"    as a source named '{SOURCE_NAME}'.")
    print()
    print("How to stop it: press Ctrl + C in this window.")
    print("=================================================\n")

    client = make_obs_client()
    if client is None:
        print("[FATAL] Exiting because we could not connect to OBS.")
        sys.exit(1)

    print("[INFO] Waiting for Ctrl+V. Make sure this script is running,")
    print("       then copy an image and press Ctrl+V in any app.")
    print("       (On macOS you may need to grant Accessibility permissions.)\n")

    # Register hotkey: when Ctrl+V is pressed, call handle_paste
    keyboard.add_hotkey("ctrl+v", lambda: handle_paste(client))

    try:
        keyboard.wait()  # Wait indefinitely until interrupted
    except KeyboardInterrupt:
        print("\n[INFO] Stopping script because you pressed Ctrl + C.")
    except Exception as e:
        print("\n[ERROR] Unexpected error while waiting for Ctrl+V.")
        print(f"Details: {e}\n")


if __name__ == "__main__":
    run_with_hotkey()


