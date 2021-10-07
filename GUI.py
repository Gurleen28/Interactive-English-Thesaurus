import wx
import logic


# custom Frame
class AppFrame(wx.Frame):
    def __init__(
            self, parent
    ):
        wx.Frame.__init__(self, parent)
        self.SetTitle("Interactive English Thesaurus")
        self.SetFont(wx.Font(wx.FontInfo(10).FaceName("Lucida Sans Unicode")))

        # frame gets a panel
        panel = wx.Panel(self)
        panel.SetBackgroundColour((229, 204, 255, 255))

        displaytext = wx.StaticText(panel, label="Please enter a word:")
        button = wx.Button(panel, id=wx.ID_ANY, label="Search Word", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.BORDER_NONE, validator=wx.DefaultValidator,
                           name="button")
        button.SetBackgroundColour((204, 0, 204, 255))
        self.Bind(wx.EVT_BUTTON, self.OnSearchWord, button)
        self.textbox = wx.TextCtrl(panel)
        self.definition = wx.StaticText(panel, size=(300, 500), style=wx.ST_NO_AUTORESIZE)

        # organize panel items in a sizer box
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        vbox.Add((0, 50), 0)
        vbox.Add(displaytext, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(50)
        vbox.Add(self.textbox, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(20)
        vbox.Add(button, flag=wx.ALIGN_CENTER)
        vbox.AddSpacer(50)
        vbox.Add(self.definition, flag=wx.ALIGN_CENTER | wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        vbox.AddStretchSpacer(prop=1)
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

        # add a toolbar
        toolbar = self.CreateToolBar(style=wx.TB_DEFAULT_STYLE, id=wx.ID_ANY, name="toolbar")
        toolbar.SetBackgroundColour((204, 0, 204, 255))
        # toolbar.AddTool(wx.ID_ANY, "Leaf", bitmap, shortHelp=””, kind = ITEM_NORMAL)
        # toolbar.AddTool(wx.ID_ANY, "Sunflower", bitmap, shortHelp=””, kind = ITEM_NORMAL)
        # toolbar.AddTool(wx.ID_ANY, "Tulip", bitmap, shortHelp=””, kind = ITEM_NORMAL)

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
        wx.MessageBox('This program was created by Gurleen Kour.', 'About',
                      style=wx.OK | wx.CLOSE | wx.CENTRE, parent=self)

    def OpenHelp(self, event):
        wx.MessageBox('Enter a word and press Search word to look up its definition.',
                      'Help', style=wx.OK | wx.CLOSE | wx.CENTRE, parent=self)
