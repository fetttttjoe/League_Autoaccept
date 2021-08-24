from pythoncom import pywintypes
import window as w
import pyautogui
from pathlib import Path
import keyboard
import fileHandler as fH
import cv2
import gc
def getWindow(game_name,class_name=None):
    
    try: 
        window = w.windowManager(game_name,class_name)
        size=window.getWindowSize()
        #print(f'your window size is: {size}')
        window.getWindow()
        return window
    except pywintypes.error as error:
        #print(error)
        return 0
def autoAccept(window_size,quit_key,game_name):
    file_name="accept_button.png"
    window=0
    
    while not keyboard.is_pressed(quit_key) and getWindow(game_name)!=0:
        print("----------------------------------")
        print(f"hold {quit_key} for at least 5 sek to end script")
        window=getWindow(game_name) 
        
        new_window_size=window.getWindowSize() 
        if(new_window_size[2]!=window_size[2]):
            pyautogui.sleep(10)
            print("Skipped, you are ingame!")
            del window
            gc.collect()
        else:
            #print(window.getWindowName())

            window_size=window.getWindowSize()
            print("Currently in Client, waiting for Accept screen")
            
            p_filePath = getPictureFilePath(file_name)
            p_filePath=Path(f'{p_filePath}/pic/{file_name}').resolve()
            #print(f"inside else {window_size} {pyautogui.locateOnScreen(f'{p_filePath}',region=(window_size[0],window_size[1],window_size[2], window_size[3]),confidence=0.85)} ")
            window.set_foreground()
            if pyautogui.locateOnScreen(f'{p_filePath}',region=(window_size[0],window_size[1],window_size[2], window_size[3]),confidence=0.85) != None:
                window.set_foreground()
                print(p_filePath)
                accept_Box = pyautogui.locateOnScreen(f'{p_filePath}',region=(window_size[0],window_size[1],window_size[2], window_size[3]),confidence=0.85)
                print(f"accept found in Box {accept_Box}")
                pyautogui.click(pyautogui.center(accept_Box))
            pyautogui.sleep(3)
            del window
            gc.collect()
    if keyboard.is_pressed(quit_key):
        del window
        gc.collect()
        return 1 
    
    
    return 0

def getPictureFilePath(file_name):
    
    p_filePath = Path(__file__).parent.resolve()
    #creates folder if doesnt exist
    Path(f"{p_filePath}/pic").mkdir(parents=True, exist_ok=True)

    if Path(f"{p_filePath}/pic/{file_name}").exists():
        return p_filePath
    else:
        fH.download_file("accept_Button_example.png","https://www.dropbox.com/s/ozcn8fpdfs0q8gg/accept_button_example.png?dl=1")
        while not Path(f"{p_filePath}/pic/{file_name}").exists():
            print(f"Pls overwrite the example screenshot in folder {p_filePath}/pic and remove _example in file name")
            pyautogui.sleep(10)
        return p_filePath
def main():
    enter=1
    quit=0
    game_name="League of Legends"
    quit_key=input("Please choose Key to quit script (in case you dont find it anymore): ")   
    
    while quit==0:
        while enter == 1 and getWindow(game_name) != 0:

            window=getWindow(game_name)  
            window_size=window.getWindowSize() 
            enter=input(f"Hit Enter until your Client size matches: {window_size[2],window_size[3]}, maybe shake windows a bit. Hit random button if match:")
            if enter=='':
                enter=1
            else:
                quit=autoAccept(window_size,quit_key,game_name)
            del window
            gc.collect()
        print(f"{game_name} is not running, Pls start game first and log into Client")
        enter=1
        pyautogui.sleep(10)
        
    print("script endet")

        
        
        
if __name__ == "__main__":
    main()
    