import wx


class OverlayPanel(wx.Panel):
    def __init__(self, parent):
        super(OverlayPanel, self).__init__(
            parent, pos=(50, 50), size=(200, 150))
        self.SetBackgroundColour("light blue")

        # 닫기 버튼 생성
        self.close_button = wx.Button(self, label="Close", pos=(50, 50))

        # 버튼 클릭 시 패널을 숨기도록 이벤트 핸들러 바인딩
        self.close_button.Bind(wx.EVT_BUTTON, self.on_close_button_click)

        # 초기에는 숨김
        self.Hide()

    def on_close_button_click(self, event):
        self.Hide()  # 이벤트 핸들러 내에서 패널 숨기기
