# @author Gurleen Kour
# Permission to copy and modify all files if author is credited
# email: gurleenkour2800@gmail.com

import sys
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

