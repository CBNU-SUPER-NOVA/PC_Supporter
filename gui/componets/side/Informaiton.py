import wx


class Information(wx.Dialog):
    def __init__(self, parent, title="Information", message="This is an information dialog."):
        super().__init__(parent, title=title, size=(300, 200))
        self.message = message

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        message_text = wx.StaticText(panel, label=self.message)
        vbox.Add(message_text, flag=wx.ALL | wx.CENTER, border=10)

        ok_button = wx.Button(panel, label='OK')
        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        vbox.Add(ok_button, flag=wx.ALL | wx.CENTER, border=10)

        panel.SetSizer(vbox)

    def on_ok(self, event):
        self.Close()
