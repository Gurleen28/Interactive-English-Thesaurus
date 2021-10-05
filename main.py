import wx
import GUI

app = wx.App()
myFrame = GUI.AppFrame(None, 1, "Interactive English Thesaurus")
myFrame.Show(True)
app.MainLoop()
