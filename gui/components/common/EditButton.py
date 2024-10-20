import wx
import wx.svg


class EditButton(wx.Panel):
    def __init__(self, parent, URL, size, corner_radius=10, hover_color="#F7F7F8", active_color="#D0D0D0"):
        super(EditButton, self).__init__(parent)
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
        self.is_active = False  # 버튼이 눌려진 상태인지 여부
        self.hover_color = hover_color  # 호버 시 배경색
        self.active_color = active_color  # 활성화 상태의 배경색
        self.corner_radius = corner_radius  # 둥근 모서리 반경

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        # 활성화 상태일 때 배경 그리기
        if self.is_active:
            gc.SetBrush(wx.Brush(self.active_color))
            gc.SetPen(wx.Pen(self.active_color))
        elif self.is_hovered:
            gc.SetBrush(wx.Brush(self.hover_color))
            gc.SetPen(wx.Pen(self.hover_color))
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

    def on_enter(self, event):
        self.is_hovered = True
        self.Refresh()

    def on_leave(self, event):
        self.is_hovered = False
        self.Refresh()

    def pos(self, x, y):
        self.SetPosition((x, y))
        self.Refresh()

    def set_on_click(self, on_click):
        self.Bind(wx.EVT_LEFT_DOWN, on_click)
