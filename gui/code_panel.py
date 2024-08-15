import wx


class RightPanel(wx.Panel):
    def __init__(self, parent):
        super(RightPanel, self).__init__(parent)
        self.SetBackgroundColour("white")

        # 기본 텍스트 추가
        self.text = wx.StaticText(
            self, label="Middle Panel is visible.", pos=(20, 20))

    def update_text(self, message):
        self.text.SetLabel(message)
