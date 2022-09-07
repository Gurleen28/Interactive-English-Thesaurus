# @author Gurleen Kour
# Permission to copy and modify all files if author is credited
# email: gurleenkour2800@gmail.com

from wx import App
from GUI.AppFrame import AppFrame

app = App()
myFrame = AppFrame(None)
myFrame.Show()
app.MainLoop()

