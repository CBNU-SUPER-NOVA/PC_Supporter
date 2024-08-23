import wx


class RoundedPanel(wx.Panel):
    def __init__(self, parent, size, radius, texts, alignment="center", color="#D0D0D0", hover_color="#C0C0C0"):
        super(RoundedPanel, self).__init__(parent, size=size)
        self.radius = radius
        self.texts = texts
        self.alignment = alignment.lower()  # 정렬 방식을 소문자로 변환하여 저장
        self.default_color = wx.Colour(color)
        self.hover_color = wx.Colour(hover_color)

        self.current_color = self.default_color  # 현재 색상 (초기값은 기본 색상)

        # 부모 창의 배경색을 패널 배경색과 일치
        self.SetBackgroundColour(self.GetParent().GetBackgroundColour())

        # 더블 버퍼링 사용
        self.SetDoubleBuffered(True)

        self.Bind(wx.EVT_PAINT, self.on_paint)

        # 마우스 이벤트 바인딩
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click)

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        # 배경 초기화
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        # 둥근 사각형 그리기
        pen = wx.Pen(self.current_color, width=1)
        gc.SetPen(pen)
        gc.SetBrush(wx.Brush(self.current_color))
        width, height = self.GetSize()
        gc.DrawRoundedRectangle(0, 0, width, height, self.radius)

        # 텍스트 그리기
        font = wx.Font(18, wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        gc.SetFont(font, wx.Colour("#000000"))

        # 텍스트 크기 측정
        text_width, text_height = gc.GetTextExtent(self.texts)

        # 텍스트 위치 계산 (가로 정렬)
        if self.alignment == "left":
            text_x = 10  # 좌측 정렬일 경우 좌측에서 약간의 여백(10픽셀)을 두고 그리기
        elif self.alignment == "center":
            text_x = (width - text_width) / 2  # 중앙 정렬일 경우
        elif self.alignment == "right":
            # 우측 정렬일 경우 우측에서 약간의 여백(10픽셀)을 두고 그리기
            text_x = width - text_width - 10
        else:
            text_x = (width - text_width) / 2  # 기본적으로 중앙 정렬

        # 텍스트 세로 중앙 정렬
        text_y = (height - text_height) / 2

        gc.DrawText(self.texts, text_x, text_y)

    # 호버링 이벤트
    def on_enter(self, event):
        self.current_color = self.hover_color
        self.Refresh()  # on_paint를 호출하여 다시 그림

    # 호버에서 벗어날때 이벤트
    def on_leave(self, event):
        self.current_color = self.default_color
        self.Refresh()  # on_paint를 호출하여 다시 그림

    # 패널 클릭 이벤트
    def on_click(self, on_click):
        self.Bind(wx.EVT_LEFT_DOWN, on_click)

    def on_right_click(self, event):
        wx.MessageBox(self.texts + " Panel Right clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)
        self.Refresh()
