import wx
import wx.svg


class SVGButton(wx.Panel):
    def __init__(self, parent, URL, size, corner_radius=10):
        super(SVGButton, self).__init__(parent)
        self.SetMinSize((size, size))  # 최소 크기 설정
        self.SetSizeHints(size, size)  # 크기 힌트 설정
        self.SetBackgroundColour(
            self.Parent.GetBackgroundColour())  # 부모 배경색으로 설정
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.SetSize(size, size)
        self.svg_image = wx.svg.SVGimage.CreateFromFile(URL)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)

        self.is_hovered = False
        self.hover_color = "#F7F7F8"  # 호버 시 배경색
        self.corner_radius = corner_radius  # 둥근 모서리 반경

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        # 호버 상태일 때 둥근 사각형 그리기
        if self.is_hovered:
            gc.SetBrush(wx.Brush(self.hover_color))
            gc.SetPen(wx.Pen(self.hover_color))
            gc.DrawRoundedRectangle(
                0, 0, self.Size.width, self.Size.height, self.corner_radius)
        else:
            gc.SetBrush(wx.Brush(self.GetBackgroundColour()))
            gc.SetPen(wx.Pen(self.GetBackgroundColour()))
            gc.DrawRoundedRectangle(
                0, 0, self.Size.width, self.Size.height, self.corner_radius)

        # SVG 이미지 로드 기본적으로 512 * 512임.
        scale = self.Size.width / 512
        # SVG 이미지를 그대로 렌더링
        if self.svg_image:
            self.svg_image.RenderToGC(gc, scale)

    # 마우스 hover
    def on_enter(self, event):
        self.is_hovered = True
        self.Refresh()

    # 마우스 hover에서 벗어날 경우
    def on_leave(self, event):
        self.is_hovered = False
        self.Refresh()

    def pos(self, x, y):
        self.SetPosition((x, y))
        self.Refresh()

    def set_on_click(self, on_click):
        self.Bind(wx.EVT_LEFT_DOWN, on_click)
