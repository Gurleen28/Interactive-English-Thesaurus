# @author Gurleen Kour
# Permission to copy and modify all files if author is credited
# email: gurleenkour2800@gmail.com

import sys
import wx


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

