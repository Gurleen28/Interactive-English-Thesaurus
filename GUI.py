import wx
import logic


# custom Frame
class AppFrame(wx.Frame):
    def __init__(
            self, parent
    ):
        wx.Frame.__init__(self, parent)

        # frame gets a panel
        panel = wx.Panel(self)
        panel.SetBackgroundColour("purple")

        displaytext = wx.StaticText(panel, label="Please enter a word:")
        button = wx.Button(panel, label="Search word")
        self.Bind(wx.EVT_BUTTON, self.OnSearchWord, button)
        self.textbox = wx.TextCtrl(panel)
        self.definition = wx.StaticText(panel, size=(300,500), style=wx.ST_NO_AUTORESIZE)

        # organize panel items in a sizer box
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        vbox.Add(displaytext, flag=wx.ALIGN_CENTER)
        vbox.Add(self.textbox, flag=wx.ALIGN_CENTER)
        vbox.Add(button, flag=wx.ALIGN_CENTER)
        vbox.Add(self.definition, flag=wx.ALIGN_CENTER | wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        self.definition.Show(False)
        panel.SetSizer(vbox)

        # add a menu bar
        menu_bar = wx.MenuBar()
        menu = wx.Menu()
        about_item = wx.MenuItem(menu, 5, text="About")
        menu.Append(about_item)
        help_item = wx.MenuItem(menu, 6, text="Help")
        menu.Append(help_item)
        menu_bar.Append(menu, "Menu")
        self.Bind(wx.EVT_MENU, self.OpenAbout, about_item)
        self.Bind(wx.EVT_MENU, self.OpenHelp, help_item)
        self.SetMenuBar(menu_bar)

        panel.SetAutoLayout(True)
        vbox.Fit(panel)
        self.Center()
        self.Show()

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
