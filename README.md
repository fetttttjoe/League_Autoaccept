# League Auto-Accept Tool v3

A modular and efficient tool that automatically accepts "League of Legends" matches for you. It features robust error handling and a powerful debug mode to help you get it running perfectly.

## Features

* **Modular Codebase:** The project is broken down into logical modules (`app`, `logger`, `window`) for easy maintenance and understanding.
* **Automatic Match Acceptance:** Detects the "accept" button within a defined search area and clicks it for you.
* **Efficient State Detection:** Uses different check intervals depending on whether you are in the client or in-game, saving system resources.
* **Powerful Debug Mode:** If the script can't find the accept button, it will save a `debug_search_area.png` image with a red box showing exactly where it was looking.
* **Clean Console Output:** A custom logger prevents the console from being spammed with repetitive status messages.

## Setup

1.  **Install Python:** If you don't have Python installed, download and install the latest version from [python.org](https://www.python.org/downloads/).

2.  **Download Files:** Place all the project files (`main.py`, `app.py`, `logger.py`, `window.py`, `file_handler.py`, `config.ini`, `requirements.txt`) into a single folder.

3.  **Install Dependencies:** Open a terminal or command prompt, navigate to the folder where you saved the files, and run the following command:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create Your "Accept" Button Image:**
    * Run the script once (`python main.py`). It will detect that `accept_button.png` is missing and download a high-quality example into a `pic` folder.
    * Take a very small, tight screenshot of **only the "ACCEPT!" button** in your League of Legends client.
    * Save this screenshot inside the `pic` folder with the exact filename: `accept_button.png`.

## How to Use

1.  **Run the script:** Open a terminal or command prompt, navigate to the tool's folder, and run:
    ```bash
    python main.py
    ```
2.  **Let it Run:** The script will now run in the background. To stop the script at any time, press and hold the `quit_key` (default is `end`) for a moment.

## Troubleshooting

If the script fails to find the button, it will create a `debug_search_area.png` file.
1.  Open this file. It shows a snapshot of your client with a red box.
2.  **Is the red box in the wrong place?** Adjust the `[SearchArea]` values in `config.ini`.
3.  **Is the red box in the right place but it still fails?** Your `accept_button.png` is not a good match. Retake your screenshot, making sure it's a clean crop. You can also try lowering the `confidence` value in `config.ini`.