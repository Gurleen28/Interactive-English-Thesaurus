import wx
import GUI
import logic
import database

engDict = logic.generateDictLists()

# database.createTable("english")
# database.insertElements("english", engDict)

app = wx.App()
myFrame = GUI.AppFrame(None)
myFrame.Show()
app.MainLoop()

