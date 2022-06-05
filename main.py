from wx import App
from GUI import AppFrame

app = App()
myFrame = AppFrame(None)
myFrame.Show()
app.MainLoop()

