import wx


class AiPanel(wx.Panel):
    def __init__(self, parent):
        super(AiPanel, self).__init__(parent)
        self.SetBackgroundColour("light gray")

        # 패널에 버튼 추가
        self.toggle_button = wx.Button(
            self, label="Toggle Overlay", pos=(20, 20))

    def bind_toggle_button(self, handler):
        # 외부에서 이벤트 핸들러를 바인딩할 수 있도록 메서드 추가
        self.toggle_button.Bind(wx.EVT_BUTTON, handler)
