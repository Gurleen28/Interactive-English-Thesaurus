# @author Gurleen Kour
# Permission to copy and modify all files if author is credited
# email: gurleenkour2800@gmail.com

import os
import sys
import wx
from wx.lib.scrolledpanel import ScrolledPanel
from logic import Logic


# custom Frame
class AppFrame(wx.Frame):
    def __init__(
            self, parent
    ):
        wx.Frame.__init__(self, parent)
        self.SetSize(500, 500)
        self.SetTitle("Interactive English Thesaurus")
        self.SetFont(wx.Font(wx.FontInfo(12).FaceName("Lucida Sans Unicode")))
        self.currentdir = os.getcwd()
        self.SetIcon(wx.Icon(self.currentdir + '/icons/flag_icon.png'))

        # frame gets a panel
        self.panel = ScrolledPanel(self, size=wx.Size(500, 500), style=wx.CLIP_CHILDREN)
        self.panel.SetAutoLayout(True)
        self.panel.SetupScrolling()
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
        redtool = self.toolbar.AddRadioTool(1, "Red", wx.Bitmap(self.currentdir + '/icons/red.png'),
                                            bmpDisabled=wx.NullBitmap, shortHelp="",
                                            longHelp="", clientData=None)
        greentool = self.toolbar.AddRadioTool(2, "Green", wx.Bitmap(self.currentdir + '/icons/green.png'),
                                              bmpDisabled=wx.NullBitmap, shortHelp="",
                                              longHelp="", clientData=None)
        purpletool = self.toolbar.AddRadioTool(3, "Purple", wx.Bitmap(self.currentdir + '/icons/purple.png'),
                                               bmpDisabled=wx.NullBitmap,
                                               shortHelp="", longHelp="", clientData=None)
        # add functionality for radio buttons
        self.Bind(wx.EVT_TOOL, self.ChangeThemeRed, redtool)
        self.Bind(wx.EVT_TOOL, self.ChangeThemeGreen, greentool)
        self.Bind(wx.EVT_TOOL, self.ChangeThemePurple, purpletool)

        # realize toolbar
        self.toolbar.Realize()
        self.Center()
        self.Show()
        LoginDialog(self)
        self.logic = Logic()

    def OnSearchWord(self, event):
        word = self.textbox.GetLineText(0)
        definitions = self.logic.searchWord(word)
        if definitions:
            self.definition.SetLabel(definitions)
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


class LoginDialog(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Log in to PostgreSQL", style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        panel = wx.Panel(self)
        self.SetFont(wx.Font(wx.FontInfo(12).FaceName("Lucida Sans Unicode")))
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        vbox.Add(wx.StaticText(panel, label="Please enter your PostgreSQL Login credentials."), flag=wx.ALIGN_CENTRE |
                 wx.ALL, border=20)

        hbox1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(panel, label="Username"))
        hbox1.AddSpacer(20)
        self.username_field = wx.TextCtrl(panel, value='postgres')
        hbox1.Add(self.username_field)

        hbox2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(panel, label="Password"))
        hbox2.AddSpacer(20)
        self.password_field = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD)
        hbox2.Add(self.password_field)

        self.login_button = wx.Button(panel, label="Log In")

        vbox.Add(hbox1, flag=wx.ALIGN_CENTRE)
        vbox.AddSpacer(20)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTRE)
        vbox.AddSpacer(20)
        vbox.Add(self.login_button, flag=wx.ALIGN_CENTRE)
        vbox.AddSpacer(20)

        # bind all elements to their handler
        self.Bind(wx.EVT_TEXT_ENTER, self.OnLogin, self.password_field)
        self.Bind(wx.EVT_BUTTON, self.OnLogin, self.login_button)
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)

        panel.SetSizer(vbox)
        panel.Fit()
        self.Fit()
        self.CenterOnParent()
        self.Show()

    def OnLogin(self, event):
        username = self.username_field.GetLineText(0)
        password = self.password_field.GetLineText(0)
        login = self.GetParent().logic.setupDatabase(username, password)
        if not login:
            dialog = wx.MessageDialog(self, "Your username or password are incorrect. Please try again.",
                                      style=wx.OK)
            dialog.ShowModal()
        else:
            self.Destroy()

    def OnClose(self, event):
        dialog = wx.MessageDialog(self, "You have to log in to use the application. Do you want to close the "
                                        "application?", style=wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT)
        answer = dialog.ShowModal()

        if answer == wx.ID_YES:
            sys.exit("Login interrupted")

