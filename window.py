import win32gui
import win32con
from typing import Optional

class WindowManager:
    """
    A class to manage interactions with a specific window, such as finding it,
    getting its size and position, and bringing it to the foreground.
    """

    def __init__(self, window_name: str, class_name: Optional[str] = None):
        """
        Initializes the WindowManager and finds the window handle using FindWindowEx
        for potentially better compatibility with some applications like game clients.

        Args:
            window_name (str): The title of the window to find.
            class_name (str, optional): The class name of the window. Defaults to None.
        """
        self.window_name = window_name
        # Using FindWindowEx as it can be more reliable for certain window hierarchies.
        # Searching from the desktop level (parent=None).
        self._handle = win32gui.FindWindowEx(None, None, class_name, window_name)

        if self._handle == 0:
            # Raise an exception if the window is not found.
            raise FileNotFoundError(f"Window '{self.window_name}' not found.")

    def get_handle(self):
        """Returns the window handle."""
        return self._handle

    def get_window_rect(self) -> tuple[int, int, int, int]:
        """
        Gets the window's rectangle coordinates (left, top, right, bottom)
        and returns them as (x, y, width, height).

        Returns:
            tuple[int, int, int, int]: A tuple containing the x, y of the top-left
                                      corner and the width and height of the window.
        """
        rect = win32gui.GetWindowRect(self._handle)
        x = rect[0]
        y = rect[1]
        width = rect[2] - x
        height = rect[3] - y
        return x, y, width, height

    def set_foreground(self):
        """
        Brings the window to the foreground, making it the active window.
        This is necessary for sending clicks or key presses to it.
        """
        try:
            # The combination of these two calls is a reliable way to bring
            # a window to the front.
            win32gui.ShowWindow(self._handle, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self._handle)
        except Exception as e:
            # win32gui functions can raise pywintypes.error
            print(f"\n[ERROR] Could not bring window to foreground: {e}")

    def is_in_game(self) -> bool:
        """
        Determines if the user is likely in a game based on window aspect ratio.
        The League of Legends client has a fixed 16:9 aspect ratio (approx 1.777).
        When in-game, the window can be resized freely, changing the ratio.
        This is a simple but effective heuristic.

        Returns:
            bool: True if the aspect ratio is not close to 16:9, suggesting an in-game state.
                  False otherwise.
        """
        _, _, width, height = self.get_window_rect()
        if height == 0 or width == 0:
            return False

        # The client has a very specific aspect ratio.
        # If it deviates significantly, we assume the user is in the game itself.
        aspect_ratio = width / height
        # LoL client is 1280x720 or 1024x576, both are 1.777...
        return not (1.77 < aspect_ratio < 1.78)