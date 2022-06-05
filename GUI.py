import wx
from logic import Logic


# custom Frame
class AppFrame(wx.Frame):
    def __init__(
            self, parent
    ):
        wx.Frame.__init__(self, parent)
        self.SetSize(500, 500)
        self.SetTitle("Interactive Dictionary")
        self.SetFont(wx.Font(wx.FontInfo(10).FaceName("Lucida Sans Unicode")))
        self.logic = Logic()

        # frame gets a panel
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour((255, 204, 204, 255))

        displaytext = wx.StaticText(self.panel, label="Please enter a word:")
        self.button = wx.Button(self.panel, id=wx.ID_ANY, label="Search Word", pos=wx.DefaultPosition,
                                size=wx.DefaultSize, style=wx.BORDER_NONE, validator=wx.DefaultValidator,
                                name="button")
        self.button.SetBackgroundColour((255, 153, 153, 255))
        self.Bind(wx.EVT_BUTTON, self.OnSearchWord, self.button)
        self.textbox = wx.TextCtrl(self.panel, 1, "", wx.DefaultPosition,
                                   wx.DefaultSize, wx.TE_PROCESS_ENTER, wx.DefaultValidator, "text")
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSearchWord, self.textbox)
        self.definition = wx.StaticText(self.panel, size=(300, 500), style=wx.ST_NO_AUTORESIZE)
        self.theme = "red"

        # organize panel items in a sizer box
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        vbox.Add((0, 50), 0)
        vbox.Add(displaytext, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(30)
        vbox.Add(self.textbox, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(30)
        vbox.Add(self.button, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(50)
        vbox.Add(self.definition, flag=wx.ALIGN_CENTER | wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        vbox.AddStretchSpacer(prop=1)
        self.definition.Show(False)
        self.panel.SetSizer(vbox)

        # add a menu bar
        menu_bar = wx.MenuBar()
        menu = wx.Menu()
        about_item = wx.MenuItem(menu, 5, text="About")
        help_item = wx.MenuItem(menu, 6, text="Help")
        menu.Append(about_item)
        menu.Append(help_item)
        menu_bar.Append(menu, "Menu")
        self.Bind(wx.EVT_MENU, self.OpenAbout, about_item)
        self.Bind(wx.EVT_MENU, self.OpenHelp, help_item)
        self.SetMenuBar(menu_bar)

        # add a toolbar
        self.toolbar = self.CreateToolBar(style=wx.TB_DEFAULT_STYLE, id=wx.ID_ANY, name="toolbar")
        self.toolbar.SetBackgroundColour((255, 153, 153, 255))

        # add radio buttons for color theme
        redtool = self.toolbar.AddRadioTool(1, "Red", wx.Bitmap('icons/red.png'),
                                            bmpDisabled=wx.NullBitmap, shortHelp="",
                                            longHelp="", clientData=None)
        greentool = self.toolbar.AddRadioTool(2, "Green", wx.Bitmap('icons/green.png'),
                                              bmpDisabled=wx.NullBitmap, shortHelp="",
                                              longHelp="", clientData=None)
        purpletool = self.toolbar.AddRadioTool(3, "Purple", wx.Bitmap('icons/purple.png'),
                                               bmpDisabled=wx.NullBitmap,
                                               shortHelp="", longHelp="", clientData=None)
        # add functionality for radio buttons
        self.Bind(wx.EVT_TOOL, self.ChangeThemeRed, redtool)
        self.Bind(wx.EVT_TOOL, self.ChangeThemeGreen, greentool)
        self.Bind(wx.EVT_TOOL, self.ChangeThemePurple, purpletool)

        # realize toolbar
        self.toolbar.Realize()

        self.panel.SetAutoLayout(True)
        vbox.Fit(self.panel)
        self.Center()
        self.Show()

    def OnSearchWord(self, event):
        word = self.textbox.GetLineText(0)
        definitions = self.logic.searchWord(word)
        if definitions:
            self.definition.SetLabel(str(definitions))
            self.definition.Show(True)
        else:
            matches = self.logic.getCloseMatches(word)
            if not matches:
                self.definition.SetLabel("Word not found.")
                self.definition.Show(True)
            else:
                ChoiceDialog(self, matches)

    def OpenAbout(self, event):
        wx.MessageBox('This program was created by Gurleen Kour.', 'About',
                      style=wx.OK | wx.CLOSE | wx.CENTRE, parent=self)

    def OpenHelp(self, event):
        wx.MessageBox('Enter a word and press Search word to look up its definition.',
                      'Help', style=wx.OK | wx.CLOSE | wx.CENTRE, parent=self)

    def ChangeThemeRed(self, event):
        self.theme = "red"
        self.panel.SetBackgroundColour((255, 204, 204, 255))
        self.button.SetBackgroundColour((255, 153, 153, 255))
        self.toolbar.SetBackgroundColour((255, 153, 153, 255))
        self.Refresh()
        self.toolbar.Realize()

    def ChangeThemeGreen(self, event):
        self.theme = "green"
        self.panel.SetBackgroundColour((204, 255, 229, 255))
        self.button.SetBackgroundColour((102, 255, 178, 255))
        self.toolbar.SetBackgroundColour((102, 255, 178, 255))
        self.Refresh()
        self.toolbar.Realize()

    def ChangeThemePurple(self, event):
        self.theme = "purple"
        self.panel.SetBackgroundColour((229, 204, 255, 255))
        self.button.SetBackgroundColour((204, 153, 255, 255))
        self.toolbar.SetBackgroundColour((204, 153, 255, 255))
        self.Refresh()
        self.toolbar.Realize()


class ChoiceDialog(wx.Dialog):

    def __init__(
            self, parent, matches
    ):
        wx.Dialog.__init__(self, parent, id=5, title="Choose word", pos=wx.DefaultPosition, size=wx.Size(300, 150),
                           style=wx.DEFAULT_DIALOG_STYLE, name="choose word dialog")
        self.parent = parent

        self.SetFont(wx.Font(wx.FontInfo(10).FaceName("Lucida Sans Unicode")))
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
                definition = self.parent.logic.searchWord(self.matches[i])
                self.GetParent().definition.SetLabel(str(definition))
                self.GetParent().definition.Show(True)
                self.GetParent().textbox.Clear()
                self.GetParent().textbox.SetInsertionPoint(0)
                self.GetParent().textbox.WriteText(self.matches[i])
        self.Destroy()

    def OnClose(self, event):
        self.GetParent().definition.SetLabel("No word found.")
        self.Destroy()
