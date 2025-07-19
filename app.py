import pyautogui
import keyboard
import time
import os
from pathlib import Path
import configparser
from PIL import Image, ImageDraw
import sys # <--- ADDED: Import sys for PyInstaller path handling

# Import our custom modules
import window
import file_handler
from logger import ConsoleLogger

class AutoAcceptApp:
    """
    Encapsulates the entire logic for the League Auto-Accept tool.
    """
    def __init__(self):
        """Initializes the application, loading configuration and setting up components."""
        self.logger = ConsoleLogger()
        self.load_config()
        self.setup_paths()

    def _get_base_path(self) -> Path:
        """
        Determines the correct base path for accessing data files,
        whether running in a PyInstaller bundle or in development.
        """
        if getattr(sys, 'frozen', False):
            # We are running in a PyInstaller bundle, sys._MEIPASS points to the
            # temporary directory where bundled files are extracted.
            return Path(sys._MEIPASS)  # type: ignore
        else:
            # We are running in a normal Python environment, so the current
            # working directory is the base.
            return Path.cwd()

    def load_config(self):
        """
        Loads all settings from the config.ini file.
        Includes extensive debugging to check file paths and loaded values.
        """
        config = configparser.ConfigParser()
        base_path = self._get_base_path()
        config_path = base_path / 'config.ini'

        # --- DEBUGGING START ---
        self.logger.log_event(f"DEBUG: Running in frozen environment: {getattr(sys, 'frozen', False)}")
        self.logger.log_event(f"DEBUG: Determined base path: {base_path}")
        self.logger.log_event(f"DEBUG: Attempting to read config.ini from: {config_path}")
        # --- DEBUGGING END ---

        # Attempt to read the config.ini file using the determined path.
        # config.read() returns a list of successfully read files.
        if not config.read(config_path): # <--- MODIFIED: Use the full determined path
            self.logger.log_event("!! WARNING: config.ini not found or could not be read. Using fallback values.")
            self.logger.log_event(f"DEBUG: Current working directory (CWD) was: {Path.cwd()}") # Add CWD for context
        else:
            self.logger.log_event("config.ini found and read successfully.")
            self.logger.log_event(f"Sections found in config.ini: {config.sections()}")

        # Safely get all settings with fallbacks
        self.game_window_title = config.get('Settings', 'game_window_title', fallback='League of Legends')
        self.quit_key = config.get('Settings', 'quit_key', fallback='end')
        self.accept_button_image_name = config.get('Settings', 'accept_button_image', fallback='accept_button.png')

        self.client_check_interval = config.getfloat('Timings', 'client_check_interval_seconds', fallback=0.5)
        self.in_game_sleep_time = config.getfloat('Timings', 'in_game_sleep_seconds', fallback=15.0)

        self.confidence_level = config.getfloat('ImageSearch', 'confidence', fallback=0.9)
        self.use_grayscale = config.getboolean('ImageSearch', 'grayscale_search', fallback=True)

        # Retrieve search area values with fallbacks
        self.rel_center_x = config.getfloat('SearchArea', 'relative_center_x', fallback=0.5)
        self.rel_center_y = config.getfloat('SearchArea', 'relative_center_y', fallback=0.45)
        self.rel_width = config.getfloat('SearchArea', 'relative_width', fallback=0.4)
        self.rel_height = config.getfloat('SearchArea', 'relative_height', fallback=0.5)

        # --- DEBUGGING START ---
        self.logger.log_event(f"DEBUG_CONFIG: rel_center_x = {self.rel_center_x}")
        self.logger.log_event(f"DEBUG_CONFIG: rel_center_y = {self.rel_center_y}")
        self.logger.log_event(f"DEBUG_CONFIG: rel_width = {self.rel_width}")
        self.logger.log_event(f"DEBUG_CONFIG: rel_height = {self.rel_height}")
        # --- DEBUGGING END ---

        self.save_debug_image = config.getboolean('Debug', 'save_debug_image_on_fail', fallback=True)

    def setup_paths(self):
        """Sets up the required file paths, using the correct base path."""
        base_path = self._get_base_path()
        self.pic_folder = base_path / "pic" # <--- MODIFIED: Use base_path for pic folder

        # IMPORTANT: Do NOT call file_handler.setup_directories here if 'pic' is a bundled, read-only resource.
        # file_handler.setup_directories is for creating *writable* directories (e.g., for logs or user data).
        # Bundled files are in a read-only temporary location.
        # If you intend for users to place their *own* accept_button.png, you'd need a separate, writable
        # user data directory (e.g., in AppData on Windows) and copy the example there on first run.
        # For now, we assume 'pic' is a bundled resource.
        # file_handler.setup_directories(self.pic_folder.name) # REMOVED/COMMENTED OUT THIS LINE

        self.accept_button_path = self.pic_folder / self.accept_button_image_name

    def run(self):
        """Starts the main application loop."""
        self.print_header()
        if not self.pre_run_check():
            input("Press Enter to exit.")
            return

        while not keyboard.is_pressed(self.quit_key):
            self.process_loop_tick()

        print(f"\n\n'{self.quit_key.upper()}' key pressed. Exiting script. Goodbye!")

    def print_header(self):
        """Prints the initial welcome header."""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.logger.log_event("--- League of Legends Auto-Accept Tool ---")
        self.logger.log_event(f"Press and hold the '{self.quit_key.upper()}' key to exit the script.")
        self.logger.log_event(f"Debug mode is {'ON' if self.save_debug_image else 'OFF'}.")
        self.logger.log_event("-" * 42)

    def pre_run_check(self):
        """Checks if the necessary files (e.g., accept button image) exist."""
        if not file_handler.check_image_exists(self.accept_button_path):
            self.logger.log_event(f"!! IMPORTANT: Image file not found at '{self.accept_button_path}'")
            if not getattr(sys, 'frozen', False):
                # Only download example if NOT running in a frozen (bundled) environment.
                # In a bundled app, you cannot write to sys._MEIPASS.
                self.logger.log_event("-> Attempting to download example image (development mode)...")
                file_handler.download_example_image(self.pic_folder)
            else:
                self.logger.log_event("!! In bundled app, 'accept_button.png' not found at expected path.")
                self.logger.log_event("!! Ensure 'accept_button.png' is correctly bundled with the application.")
            return False
        return True

    def process_loop_tick(self):
        """A single iteration of the main processing loop."""
        try:
            lol_window = window.WindowManager(self.game_window_title)

            if lol_window.is_in_game():
                self.logger.log(f"[INFO] In-game state detected. Checking again in {self.in_game_sleep_time}s...")
                time.sleep(self.in_game_sleep_time)
                return

            self.logger.log("[INFO] Game client found. Monitoring for 'Accept' button...")
            self.find_and_click_accept(lol_window)

        except FileNotFoundError:
            # This is the main way we detect if the window is closed.
            self.logger.log(f"[INFO] '{self.game_window_title}' is not running. Waiting...")
            time.sleep(5)
        except pyautogui.PyAutoGUIException as e:
            self.handle_image_not_found(e)
        except Exception as e:
            self.logger.log_event(f"[ERROR] An unexpected error occurred: {type(e).__name__}: {e}")
            self.logger.log_event(f"[INFO] Restarting check in {self.client_check_interval} seconds.")
            time.sleep(self.client_check_interval)

    def find_and_click_accept(self, lol_window):
        """Calculates search area and attempts to find and click the button."""
        window_rect = lol_window.get_window_rect()
        win_x, win_y, win_width, win_height = window_rect

        if win_width <= 0 or win_height <= 0:
            self.logger.log("[INFO] Game client is minimized. Checking again in 5s...")
            time.sleep(5)
            return

        search_region = self.calculate_search_region(window_rect)

        accept_button_location = pyautogui.locateOnScreen(
            str(self.accept_button_path),
            region=search_region,
            confidence=self.confidence_level,
            grayscale=self.use_grayscale
        )

        if accept_button_location:
            self.logger.log_event(f"[SUCCESS] Accept button found at {accept_button_location}!")
            lol_window.set_foreground()
            time.sleep(0.2)
            pyautogui.click(pyautogui.center(accept_button_location))
            self.logger.log_event(f"[ACTION] Clicked 'Accept'. Pausing for {self.in_game_sleep_time}s...")
            time.sleep(self.in_game_sleep_time)
        else:
            # This is the normal "not found yet" case.
            time.sleep(self.client_check_interval)

    def calculate_search_region(self, window_rect):
        """Calculates the absolute pixel values for the smaller search area."""
        win_x, win_y, win_width, win_height = window_rect

        search_width = int(win_width * self.rel_width)
        search_height = int(win_height * self.rel_height)
        search_center_x = win_x + int(win_width * self.rel_center_x)
        search_center_y = win_y + int(win_height * self.rel_center_y)

        search_x = search_center_x - (search_width // 2)
        search_y = search_center_y - (search_height // 2)

        return (search_x, search_y, search_width, search_height)

    def handle_image_not_found(self, e):
        """Handles the ImageNotFoundException with detailed debug steps."""
        self.logger.log_event(f"[ERROR] A screen search error occurred: {type(e).__name__}")

        # Attempt to get window and search region for debug image
        try:
            lol_window = window.WindowManager(self.game_window_title)
            window_rect = lol_window.get_window_rect()
            search_region = self.calculate_search_region(window_rect)

            if self.save_debug_image:
                debug_file = self.save_debug_screenshot(window_rect, search_region)
                if debug_file:
                    self.logger.log_event(f"  > A debug image was saved to '{debug_file}'.")
                    self.logger.log_event("  > Check this image to see the red box where the script is searching.")
        except Exception as debug_e:
            self.logger.log_event(f"[DEBUG ERROR] Could not create debug image: {debug_e}")

        self.logger.log_event("  Troubleshooting steps:")
        self.logger.log_event("  1. Look at 'debug_search_area.png'. Is the red box in the right place?")
        self.logger.log_event("  2. If not, adjust the 'SearchArea' values in config.ini.")
        self.logger.log_event("  3. If the box is correct, retake your 'accept_button.png' screenshot.")
        self.logger.log_event("\n[INFO] Restarting check in 5 seconds.")
        time.sleep(5)

    def save_debug_screenshot(self, window_region, search_region):
        """Saves a screenshot of the window with the search area drawn on it."""
        try:
            screenshot = pyautogui.screenshot(region=window_region)
            draw = ImageDraw.Draw(screenshot)

            win_x, win_y, _, _ = window_region
            search_x, search_y, search_width, search_height = search_region

            local_x1 = search_x - win_x
            local_y1 = search_y - win_y
            local_x2 = local_x1 + search_width
            local_y2 = local_y1 + search_height

            draw.rectangle([local_x1, local_y1, local_x2, local_y2], outline="red", width=3)

            debug_file = "debug_search_area.png"
            screenshot.save(debug_file)
            return debug_file
        except Exception as e:
            self.logger.log_event(f"\n[DEBUG ERROR] Could not save debug image: {e}")
            return None
