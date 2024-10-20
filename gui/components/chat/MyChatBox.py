import wx


class MyChatBox(wx.Panel):
    def __init__(self, parent, message, text_color="#000000", font_size=10, font_family=wx.FONTFAMILY_DEFAULT):
        super(MyChatBox, self).__init__(parent)
        self.color = "#F7F7F8"
        self.text_color = text_color
        self.font_size = font_size
        self.font_family = font_family

        # 메인 사이저 생성 (수평 정렬)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 둥근 박스를 그리기 위해 별도의 패널 생성
        rounded_panel = wx.Panel(self)
        rounded_panel.SetBackgroundColour(self.color)

        # 메시지 레이블 생성
        message_label = wx.StaticText(rounded_panel, label=message)
        message_label.Wrap(300)  # 너비 제한 설정

        # 텍스트 색상 설정
        message_label.SetForegroundColour(self.text_color)

        # 폰트 설정
        font = wx.Font(self.font_size, self.font_family,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        message_label.SetFont(font)

        # 둥근 박스 안에 레이블을 포함하는 사이저 생성
        rounded_sizer = wx.BoxSizer(wx.HORIZONTAL)
        rounded_sizer.Add(message_label, 0, wx.ALL, 10)
        rounded_panel.SetSizer(rounded_sizer)

        # 둥근 모서리를 적용하기 위해 Paint 이벤트 처리
        rounded_panel.Bind(wx.EVT_PAINT, self.on_paint)

        # 오른쪽 정렬을 위해 왼쪽에 스페이서를 추가
        main_sizer.AddStretchSpacer(1)
        main_sizer.Add(rounded_panel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        # 패널에 메인 사이저 설정
        self.SetSizer(main_sizer)
        self.Fit()
        self.Layout()

        # 부모 패널에 맞게 크기 조정
        parent.Layout()

    def on_paint(self, event):
        panel = event.GetEventObject()  # 이벤트가 발생한 패널을 얻음
        dc = wx.GCDC(wx.BufferedPaintDC(panel))
        dc.Clear()

        # 둥근 사각형 그리기
        width, height = panel.GetSize()
        dc.SetBrush(wx.Brush(self.color))
        dc.SetPen(wx.Pen(self.color))

        radius = 15  # 둥근 모서리의 반경
        dc.DrawRoundedRectangle(0, 0, width, height, radius)
