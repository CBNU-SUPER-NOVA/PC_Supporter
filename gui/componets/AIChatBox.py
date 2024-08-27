import wx
from .SVGButton import SVGButton


class AIChatBox(wx.Panel):
    def __init__(self, parent, message, max_width=550, text_color="#000000", font_size=10, font_family=wx.FONTFAMILY_DEFAULT, bg_color="#FFFFFF", text_bg_color="#FFFFFF"):
        super(AIChatBox, self).__init__(parent)

        # 배경 색상 설정 (패널과 텍스트 배경 색상 통일)
        self.bg_color = wx.Colour(bg_color)
        self.text_bg_color = wx.Colour(text_bg_color)
        self.SetBackgroundColour(self.bg_color)

        # 텍스트 색상 및 폰트 설정
        self.text_color = wx.Colour(text_color)
        self.font_size = font_size
        self.font_family = font_family

        # 패널의 최대 너비 설정 (높이는 제한하지 않음)
        self.SetMaxSize((max_width, -1))

        # 메인 사이저 생성
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # AI SVG 이미지 버튼 생성
        SVG_sizer = wx.BoxSizer(wx.VERTICAL)
        self.ai_icon = SVGButton(self, "gui/icons/AI.svg", 30)
        self.ai_icon.SetBackgroundColour(self.bg_color)
        SVG_sizer.Add(self.ai_icon, 0, wx.ALL | wx.TOP, 10)

        # 공백 추가해서 밀어내기
        SVG_sizer.AddStretchSpacer(1)
        main_sizer.Add(SVG_sizer, 0, wx.ALL, 0)

        # 텍스트 사이저 추가
        text_sizer = wx.BoxSizer(wx.VERTICAL)

        # 메시지 처리
        self.add_message(message, text_sizer, max_width)

        # 메인 사이저에 텍스트 사이저 추가
        main_sizer.Add(text_sizer, 1, wx.EXPAND | wx.ALL, 10)

        # 패널에 메인 사이저 설정
        self.SetSizer(main_sizer)

        # 패널 크기를 내용물에 맞게 조정
        self.Fit()
        self.Layout()

    def add_message(self, message, text_sizer, max_width):
        """메시지를 텍스트 또는 코드로 처리하여 사이저에 추가"""
        if isinstance(message, list):
            for item in message:
                if item["subtype"] == "text":
                    # 텍스트 메시지일 경우
                    message_label = wx.StaticText(
                        self, label=item["data"], style=wx.ALIGN_LEFT)
                    message_label.Wrap(max_width - 100)  # 최대 너비 설정
                    # 텍스트 색상 및 폰트 설정
                    message_label.SetForegroundColour(self.text_color)
                    message_label.SetBackgroundColour(self.text_bg_color)
                    message_label.SetFont(wx.Font(self.font_size, self.font_family,
                                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                    text_sizer.Add(message_label, 0, wx.ALL | wx.EXPAND, 3)
                elif item["subtype"] in ["python", "bash"]:
                    # 지연 임포트 방식으로 CodeBox 불러오기
                    from .CodeBox import CodeBox
                    # 코드일 경우 CodeBox 사용
                    code_box = CodeBox(
                        self, isWorkflow=False, texts=item["data"], language=item["subtype"])
                    text_sizer.Add(code_box, 0, wx.ALL | wx.EXPAND, 5)
        else:
            # 단일 텍스트 메시지일 경우
            message_label = wx.StaticText(
                self, label=message, style=wx.ALIGN_LEFT)
            message_label.Wrap(max_width - 100)  # 최대 너비 설정
            # 텍스트 색상 및 폰트 설정
            message_label.SetForegroundColour(self.text_color)
            message_label.SetBackgroundColour(self.text_bg_color)
            message_label.SetFont(wx.Font(self.font_size, self.font_family,
                                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            text_sizer.Add(message_label, 0, wx.ALL | wx.EXPAND, 3)
