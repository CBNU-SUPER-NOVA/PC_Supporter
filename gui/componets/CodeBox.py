import wx


class CodeBox(wx.Panel):
    def __init__(self, parent, texts, language="python"):
        super(CodeBox, self).__init__(parent)

        self.texts = wx.StaticText(self, label=texts, pos=(20, 50))
        self.language = wx.StaticText(self, label=language, pos=(20, 20))
        self.texts.SetBackgroundColour("white")
        self.language.SetBackgroundColour("white")
        self.texts.SetForegroundColour("black")
        self.language.SetForegroundColour("black")
        self.texts.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                   wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.language.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                      wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.texts.Wrap(400)
        self.language.Wrap(400)
        self.SetBackgroundColour("blue")
        self.SetSize(400, 100)
        self.SetPosition((20, 20))
        # 버튼들 추가
        self.button1 = wx.Button(self, label="Run", pos=(20, 70))
        self.button2 = wx.Button(self, label="Save", pos=(100, 70))
        self.button3 = wx.Button(self, label="Copy", pos=(180, 70))
        self.button4 = wx.Button(self, label="Paste", pos=(260, 70))

        # 버튼 이벤트 바인딩
        self.button1.Bind(wx.EVT_BUTTON, self.on_run)
        self.button2.Bind(wx.EVT_BUTTON, self.on_save)
        self.button3.Bind(wx.EVT_BUTTON, self.on_copy)
        self.button4.Bind(wx.EVT_BUTTON, self.on_paste)

    def on_run(self, event):
        wx.MessageBox("Run Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_save(self, event):
        wx.MessageBox("Save Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_copy(self, event):
        wx.MessageBox("Copy Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_paste(self, event):
        wx.MessageBox("Paste Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)
