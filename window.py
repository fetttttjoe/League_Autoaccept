import win32gui
import win32con
class windowManager:

    #Constructor
    def __init__ (self,window_name,class_name=None):
        self.window_name=window_name
        
        self._handle=win32gui.FindWindowEx(None,None,class_name, window_name)
        
        
        self.window_size = win32gui.GetWindowRect(self._handle)
    def minimiseWindow(self):
        win32gui.ShowWindow(self._handle, win32con.SW_MINIMIZE)
        
        
    def getWindow(self):
        return self._handle
    def getWindowName(self):
        return self.window_name
    def getWindowSize(self):
        x=self.window_size[0]
        y=self.window_size[1]
        w=self.window_size[2]-x
        h=self.window_size[3]-y

        #print("Window %s"%self._handle)
        #print("Location: (%d,%d)" %(x,y))
        #print("Size: (width:%d height:%d)" %(w,h))
        return x,y,w,h

    #put the window in the foreground    
    def set_foreground(self):
        try:
            #max window (5 seems to be magic number)
            win32gui.ShowWindow(self._handle,5)
            
            #force window on top layer
            win32gui.SetForegroundWindow(self._handle)  
            
        except:
            print("The process is not running!")    
            return 0

