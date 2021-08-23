import requests
from pathlib import Path
import shutil
def download_file(filename, url):
    """
    Download an URL to a file
    """
    with open(filename, 'wb') as fout:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        # Write response data to file
        for block in response.iter_content(4096):
            fout.write(block)
    file_path=Path(f'{filename}').parent.resolve()
    print(file_path)
    shutil.copy(f"{file_path}/{filename}",(f'{file_path}/pic/{filename}'))
def download_if_not_exists(filename, url):
    """
    Download a URL to a file if the file
    does not exist already.
    Returns
    -------
    True if the file was downloaded,
    False if it already existed
    """
    if not Path(f'{filename}/pic/accept_button.png').exitst():
        download_file(filename, url)
        return True
    return False