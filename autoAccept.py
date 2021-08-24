from pythoncom import pywintypes
import window as w
import pyautogui
from pathlib import Path
import keyboard
import fileHandler as fH

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
def autoAccept(window,window_size,quit_key,game_name):
    file_name="accept_button.png"
    while True and not keyboard.is_pressed(quit_key) and getWindow(game_name)!=0:
        print("----------------------------------")
        print(f"hold {quit_key} for at least 5 sek to end script")
        window=getWindow(game_name) 
        if window==0:
            return 0 
        new_window_size=window.getWindowSize() 
        if(new_window_size[2]!=window_size[2]):
            pyautogui.sleep(10)
            print("Skipped, you are ingame!")
        else:
            #print(window.getWindowName())

            window_size=window.getWindowSize()
            print("Currently in Lobby, waiting for match")
            
            p_filePath = getPictureFilePath(file_name)
            p_filePath=Path(f'{p_filePath}/pic/{file_name}').resolve()
            print(f"inside else {window_size} {pyautogui.locateOnScreen(f'{p_filePath}',region=(window_size[0],window_size[1],window_size[2], window_size[3]),confidence=0.9)} ")
            if pyautogui.locateOnScreen(f'{p_filePath}',region=(window_size[0],window_size[1],window_size[2], window_size[3]),confidence=0.85) != None:
                window.set_foreground()
                accept_Box = pyautogui.locateOnScreen(f'{p_filePath}',region=(window_size[0],window_size[1],window_size[2], window_size[3]),confidence=0.85)
                print(f"accept found in Box {accept_Box}")

              

                pyautogui.click(pyautogui.center(accept_Box))
            pyautogui.sleep(3)
    if getWindow(game_name)==0:
        return 0     
    return 1
def getPictureFilePath(file_name):
    
    p_filePath = Path(__file__).parent.resolve()
    #creates folder if doesnt exist
    Path(f"{p_filePath}/pic").mkdir(parents=True, exist_ok=True)

    if Path(f"{p_filePath}/pic/{file_name}").exists():
        return p_filePath
    else:
        fH.download_file("accept_Button.png","https://www.dropbox.com/s/ozcn8fpdfs0q8gg/accept_button.png?dl=1")
        return p_filePath
    
def main():
    enter=1
    game_name="League of Legends"
    quit=0
    quit_key=input("Please choose Key to quit script (in case you dont find it anymore): ")   
    while quit==0:
        if getWindow(game_name)==0:
            print(f"{game_name} is not running, Pls start game first")
            pyautogui.sleep(10)
         
        while enter==1 and getWindow(game_name)!=0:

            window=getWindow(game_name)  
            window_size=window.getWindowSize() 
            enter=input(f"Hit Enter to start Autoaccept if this is your Client size: {window_size[2],window_size[3]}")

            if enter=='':
                quit=autoAccept(window,window_size,quit_key,game_name)
            else:
                enter=1

    print("script endet")

        
        
        
if __name__ == "__main__":
    main()
    