import wx


class AIChatBox(wx.Panel):
    def __init__(self, parent, message):
        super(AIChatBox, self).__init__(parent)

        self.SetBackgroundColour("#f0f0f0")
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # AI의 메시지 레이블 생성
        ai_label = wx.StaticText(self, label="AI", style=wx.ALIGN_LEFT)
        ai_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                         wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        # 메시지 레이블 생성
        message_label = wx.StaticText(self, label=message, style=wx.ALIGN_LEFT)

        sizer.Add(ai_label, 0, wx.ALL, 5)
        sizer.Add(message_label, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()
