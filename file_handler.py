import requests
from pathlib import Path

def setup_directories(pic_folder_name: str = "pic"):
    """Ensures that the required directories exist."""
    Path(pic_folder_name).mkdir(parents=True, exist_ok=True)

def check_image_exists(image_path: Path) -> bool:
    """Checks if the specified image file exists."""
    return image_path.is_file()

def download_example_image(pic_folder: Path):
    """Downloads a high-quality example image to help the user."""
    # This URL points to the direct image, which is more reliable.
    url = "https://i.imgur.com/o72ThX1.png"
    example_filename = "accept_button_EXAMPLE.png"
    save_path = pic_folder / example_filename

    if save_path.exists():
        print(f"-> Example image '{example_filename}' already exists.")
        return

    # *** FIX: Add a User-Agent header to avoid being blocked by Imgur (HTTP 429 error) ***
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"-> Downloading example screenshot to '{save_path}'...")
    try:
        # Use a context manager for the request
        with requests.get(url, stream=True, headers=headers) as r:
            # Check if the request was successful
            r.raise_for_status()
            # Write the content to the file in chunks
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("-> Download complete. Please take your own screenshot and name it 'accept_button.png'.")
    except requests.exceptions.RequestException as e:
        # Print a more informative error message
        print(f"!! Could not download example image. Error: {e}")

