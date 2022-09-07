# @author Gurleen Kour
# Permission to copy and modify all files if author is credited
# email: gurleenkour2800@gmail.com

import wx


class ChoiceDialog(wx.Dialog):

    def __init__(
            self, parent, matches
    ):
        wx.Dialog.__init__(self, parent, id=5, title="Choose word", pos=wx.DefaultPosition, size=wx.Size(300, 150),
                           style=wx.DEFAULT_DIALOG_STYLE, name="choose word dialog")
        self.parent = parent

        self.SetFont(wx.Font(wx.FontInfo(12).FaceName("Lucida Sans Unicode")))
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        vbox.Add(wx.StaticText(self, 1, "Did you mean one of these words?", wx.DefaultPosition, wx.DefaultSize, 0,
                               "text"))
        self.SetSizer(vbox)
        self.buttons = []
        self.matches = matches
        for i in range(0, len(matches)):
            button = wx.RadioButton(self, 1, matches[i], wx.DefaultPosition,
                                    wx.DefaultSize, 0, wx.DefaultValidator,
                                    "button")
            self.buttons.append(button)
            vbox.Add(button)
        okbutton = wx.Button(self, 5, "Ok", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE,
                             wx.DefaultValidator, "ok button")
        self.Bind(wx.EVT_BUTTON, self.OnOk, okbutton)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        vbox.Add(okbutton, flag=wx.ALIGN_CENTRE)

        # change color based on theme
        if self.GetParent().theme == "red":
            self.SetBackgroundColour((255, 204, 204, 255))
            okbutton.SetBackgroundColour((255, 153, 153, 255))
        elif self.GetParent().theme == "green":
            self.SetBackgroundColour((204, 255, 229, 255))
            okbutton.SetBackgroundColour((102, 255, 178, 255))
        elif self.GetParent().theme == "purple":
            self.SetBackgroundColour((229, 204, 255, 255))
            okbutton.SetBackgroundColour((204, 153, 255, 255))

        self.Centre()
        self.Show()

    def OnOk(self, event):
        for i in range(0, len(self.buttons)):
            if self.buttons[i].GetValue():
                definitions = self.parent.logic.searchWord(self.matches[i])
                self.GetParent().definition.SetLabel(definitions)
                self.GetParent().definition.Show(True)
                self.GetParent().textbox.Clear()
                self.GetParent().textbox.SetInsertionPoint(0)
                self.GetParent().textbox.WriteText(self.matches[i])
        self.Destroy()

    def OnClose(self, event):
        self.GetParent().definition.SetLabel("No word found.")
        self.Destroy()


