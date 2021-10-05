import wx
import logic


# custom Frame
class AppFrame(wx.Frame):
    def __init__(
            self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.Size(500, 500), style=wx.DEFAULT_FRAME_STYLE
    ):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        panel = wx.Panel(self, -1)  # frame gets a panel
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        displaytext = wx.StaticText(panel, label="Please enter a word:", pos=wx.Point(140, 50))
        button = wx.Button(panel, 1003, "Search word")
        button.SetPosition((150, 150))
        self.Bind(wx.EVT_BUTTON, self.OnSearchWord, button)
        self.textbox = wx.TextCtrl(panel)
        self.textbox.SetPosition(wx.Point(140, 100))
        self.definition = wx.StaticText(panel, pos=wx.Point(50, 200))
        self.definition.SetSize(wx.Size(300, 500))
        self.definition.SetWindowStyle(wx.ST_NO_AUTORESIZE)
        self.definition.Show(False)
        menubar = wx.MenuBar()
        menu = wx.Menu()
        aboutitem = wx.MenuItem(menu, 5, text="About")
        menu.Append(aboutitem)
        helpitem = wx.MenuItem(menu, 6, text="Help")
        menu.Append(helpitem)
        menubar.Append(menu, "Menu")
        self.Bind(wx.EVT_MENU, self.OpenAbout, aboutitem)
        self.Bind(wx.EVT_MENU, self.OpenHelp, helpitem)
        self.SetMenuBar(menubar)

        # add all elements to sizer
        vbox.Add(displaytext, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        vbox.Add(self.textbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        vbox.Add(button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        vbox.Add(self.definition, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        panel.SetSizer(vbox)

    def OnSearchWord(self, event):
        word = self.textbox.GetLineText(0)
        print(word)
        definition = str(logic.searchWord(word))
        print(definition)
        self.definition.SetLabel(definition)
        self.definition.Show(True)

    def OpenAbout(self, event):
        aboutmessage = wx.MessageBox('This program was created by Gurleen Kour.',
                                     'About', style=wx.OK | wx.CLOSE | wx.CENTRE, parent=self)

    def OpenHelp(self, event):
        helpmessage = wx.MessageBox('Enter a word and press Search word to look up its definition.',
                                    'Help', style=wx.OK | wx.CLOSE | wx.CENTRE, parent=self)
