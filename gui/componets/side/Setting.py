import wx

# 설정 모달 다이얼로그 클래스


class Settings(wx.Dialog):
    def __init__(self, parent):
        super(Settings, self).__init__(parent, title="Settings", size=(300, 200))

        # 패널 생성
        panel = wx.Panel(self)

        # 라디오 버튼 그룹
        self.gemini_radio = wx.RadioButton(panel, label="Use GEMINI", style=wx.RB_GROUP)
        self.chatgpt_radio = wx.RadioButton(panel, label="Use ChatGPT")

        # 버튼 생성 (확인 및 취소)
        ok_button = wx.Button(panel, wx.ID_OK, "OK")
        cancel_button = wx.Button(panel, wx.ID_CANCEL, "Cancel")

        # 레이아웃 설정
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.gemini_radio, flag=wx.ALL, border=15)
        vbox.Add(self.chatgpt_radio, flag=wx.ALL, border=15)
        # ok_button, cancel_button을 수평으로 정렬
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(ok_button, flag=wx.ALL, border=10)
        hbox.Add(cancel_button, flag=wx.ALL, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER)

        # 패널에 sizer 설정
        panel.SetSizer(vbox)

    def get_selection(self):
        """사용자가 선택한 옵션을 반환"""
        if self.gemini_radio.GetValue():
            return "GEMINI"
        elif self.chatgpt_radio.GetValue():
            return "ChatGPT"
