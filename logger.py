class ConsoleLogger:
    """A simple logger to prevent spamming the console with repeated messages."""
    def __init__(self):
        self.last_message = ""
        self.repeat_count = 0

    def log(self, message: str):
        """Logs a status message, adding a counter if it's repeated."""
        if message == self.last_message:
            self.repeat_count += 1
            # Use carriage return to print on the same line, clearing extra space
            print(f"{message} (x{self.repeat_count}){' ' * 10}", end='\r', flush=True)
        else:
            # If there was a previous status message, print a newline to finalize it
            if self.last_message:
                print()
            self.last_message = message
            self.repeat_count = 1
            print(message, end='\r', flush=True)

    def log_event(self, message: str):
        """Logs a one-time event message on a new line."""
        # Finalize any previous status line
        if self.last_message:
            print()
        print(message, flush=True)
        # Reset the status so the next log starts fresh
        self.last_message = ""
        self.repeat_count = 0