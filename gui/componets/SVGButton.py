import wx
import wx.svg


class SVGButton(wx.Panel):
    def __init__(self, parent, URL, size):
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

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        # SVG 이미지 로드 기본적으로 512* 512임.
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
