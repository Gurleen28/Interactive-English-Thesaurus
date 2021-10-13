import wx
import GUI
import database

# database.createTable("english")
# engDict = logic.generateDictList("english")
# database.insertElements("english", engDict)
a = database.getDefinitions("english", "rain")
print(a)

# app = wx.App()
# myFrame = GUI.AppFrame(None)
# myFrame.Show()
# app.MainLoop()

