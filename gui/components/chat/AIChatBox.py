import wx
from gui.components import SVGButton, Font


class AIChatBox(wx.Panel):
    def __init__(self, parent, type, message, conversation_id, max_width=480, text_color="#000000", font_size=12, bg_color="#FFFFFF", text_bg_color="#FFFFFF"):
        super(AIChatBox, self).__init__(parent)
        self.conversation_id = conversation_id

        # 배경 색상 설정 (패널과 텍스트 배경 색상 통일)
        self.bg_color = wx.Colour(bg_color)
        self.text_bg_color = wx.Colour(text_bg_color)
        self.SetBackgroundColour(self.bg_color)

        # 텍스트 색상 및 폰트 설정
        self.text_color = wx.Colour(text_color)
        self.font_size = font_size
        self.max_width = max_width  # 최대 너비 제한 설정

        # 메인 사이저 생성
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # AI SVG 이미지 버튼 생성
        SVG_sizer = wx.BoxSizer(wx.VERTICAL)
        self.ai_icon = SVGButton(self, "gui/icons/AI.svg", 30, self.on_click)
        SVG_sizer.Add(self.ai_icon, 0, wx.ALL | wx.TOP, 10)

        # 공백 추가해서 밀어내기
        SVG_sizer.AddStretchSpacer(1)
        main_sizer.Add(SVG_sizer, 0, wx.ALL, 0)

        # 텍스트 사이저 추가
        text_sizer = wx.BoxSizer(wx.VERTICAL)

        # 메시지 처리
        self.add_message(type, message, text_sizer)

        # 메인 사이저에 텍스트 사이저 추가 (wx.EXPAND를 사용하여 좌우로 확장 가능하게 설정)
        main_sizer.Add(text_sizer, 1, wx.EXPAND | wx.ALL, 10)

        # 패널에 메인 사이저 설정
        self.SetSizer(main_sizer)

        # 패널 크기를 내용물에 맞게 조정
        self.Fit()
        self.Layout()

    def add_message(self, type, message, text_sizer):
        """메시지를 텍스트 또는 코드로 처리하여 사이저에 추가"""
        if (type == "text"):
            # 텍스트 메시지일 경우
            message_label = wx.StaticText(
                self, label=message, style=wx.ALIGN_LEFT)
            message_label.Wrap(self.max_width - 100)  # 최대 너비에 따라 줄 바꿈
            # 텍스트 색상 및 폰트 설정
            message_label.SetForegroundColour(self.text_color)
            message_label.SetBackgroundColour(self.text_bg_color)
            message_label.SetFont(Font.bold(self.font_size))
            text_sizer.Add(message_label, 0, wx.ALL | wx.EXPAND, 3)
        else:
            from gui.components import CodeBox
            # 코드일 경우 CodeBox 사용
            code_box = CodeBox(
                self, isWorkflow=False, texts=message, language=type, conversation_id=self.conversation_id)
            text_sizer.Add(code_box, 0, wx.ALL | wx.EXPAND, 5)

    def on_click(self, event):
        print("AI chat box clicked")
        event.Skip()
