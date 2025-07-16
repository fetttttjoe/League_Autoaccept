from app import AutoAcceptApp
import sys

def main():
    """
    The main entry point for the application.
    Initializes and runs the Auto-Accept tool.
    """
    try:
        app = AutoAcceptApp()
        app.run()
    except Exception as e:
        print(f"\n[FATAL ERROR] An unrecoverable error occurred: {e}")
        print("Please check your configuration and ensure all files are in place.")
        input("Press Enter to exit.")
        sys.exit(1)

if __name__ == "__main__":
    main()