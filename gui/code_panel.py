import wx
from componets.CodeBox import CodeBox


class CodePanel(wx.Panel):
    def __init__(self, parent):
        super(CodePanel, self).__init__(parent)
        self.SetBackgroundColour("white")

        # 기본 텍스트 추가
        self.text = wx.StaticText(
            self, label="Middle Panel is visible.", pos=(20, 20))

        self.CodeBox = CodeBox(self, "print('Hello, World!')", "python")

        self.CodeBox.SetPosition((20, 50))

    def update_text(self, message):
        self.text.SetLabel(message)
