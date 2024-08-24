import wx

from .SVGButton import SVGButton


class AIChatBox(wx.Panel):
    def __init__(self, parent, message, max_width=550):
        super(AIChatBox, self).__init__(parent)

        # 더블 버퍼링 활성화
        self.SetDoubleBuffered(True)

        # 패널의 최대 너비 설정 (높이는 제한하지 않음)
        self.SetMaxSize((max_width, -1))

        # 메인 사이저 생성
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # AI SVG 이미지 버튼 생성
        SVG_sizer = wx.BoxSizer(wx.VERTICAL)
        self.ai_icon = SVGButton(self, "gui/icons/AI.svg", 30)
        SVG_sizer.Add(self.ai_icon, 0, wx.ALL | wx.TOP, 10)

        # 공백 추가해서 밀어내기
        SVG_sizer.AddStretchSpacer(1)
        main_sizer.Add(SVG_sizer, 0, wx.ALL, 0)

        # 텍스트 사이저 추가
        text_sizer = wx.BoxSizer(wx.VERTICAL)

        # 배경 색상 및 텍스트 색상 설정
        self.bg_color = wx.Colour("white")  # 흰색 배경
        self.text_color = wx.Colour("#000000")  # 검은색 텍스트

        # 메시지 레이블 생성
        message_label = wx.StaticText(
            self, label=message, style=wx.ALIGN_LEFT)
        # 메시지 줄바꿈 설정
        message_label.Wrap(max_width - 100)  # 최대 너비 설정
        # 텍스트 사이저에 메시지 레이블 추가
        text_sizer.Add(message_label, 0, wx.ALL | wx.EXPAND, 3)

        # 메인 사이저에 텍스트 사이저 추가
        main_sizer.Add(text_sizer, 1, wx.EXPAND | wx.ALL, 10)

        # 패널에 메인 사이저 설정
        self.SetSizer(main_sizer)

        # 패널 크기를 내용물에 맞게 조정
        self.Fit()

        self.Layout()

    def message(self, message):
        message_label = wx.StaticText(
            self, label=message, style=wx.ALIGN_LEFT)
        message_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                      wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        message_label.SetForegroundColour(self.text_color)
