import wx
from .SVGButton import SVGButton


class CodeBox(wx.Panel):
    def __init__(self, parent, isWorkflow, texts, language="python"):
        super(CodeBox, self).__init__(parent)

        # 변수 내용 저장
        self.text = texts
        self.language = language

        # 메인 수직 박스 사이저 생성 (위아래 배치용)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 상단 부분을 감싸는 패널 생성 및 배경색 지정
        top_panel = wx.Panel(self)
        top_panel.SetBackgroundColour("#1E1E1E")  # 원하는 배경색 지정

        # 첫 번째 수평 박스 사이저 생성 (좌우 배치용)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 코딩언어 라벨 (좌측 정렬)
        self.codeLanguage = wx.StaticText(top_panel, label=self.language)
        self.codeLanguage.SetBackgroundColour("#1E1E1E")
        self.codeLanguage.SetForegroundColour("#FFFFFF")
        self.codeLanguage.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.codeLanguage.Wrap(400)

        # 좌측 정렬
        top_sizer.Add(self.codeLanguage, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 0)
        # 중간 공간 추가하여 버튼들을 우측으로 밀어내기
        top_sizer.AddStretchSpacer(1)

        # 버튼들 추가 (우측 정렬을 위한 공간 추가)
        self.codePlayButton = SVGButton(top_panel, "gui/icons/CodePlay.svg", 20)
        self.codePlayButton.set_on_click(self.on_run)
        top_sizer.Add(self.codePlayButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        self.copyButton = SVGButton(top_panel, "gui/icons/Copy.svg", 20)
        self.copyButton.set_on_click(self.on_copy)
        top_sizer.Add(self.copyButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        self.editButton = SVGButton(top_panel, "gui/icons/Edit.svg", 20)
        self.editButton.set_on_click(self.on_edit)
        top_sizer.Add(self.editButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        if isWorkflow:
            self.deleteButton = SVGButton(top_panel, "gui/icons/Delete.svg", 20)
            self.deleteButton.set_on_click(self.on_delete)
            top_sizer.Add(self.deleteButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        else:
            self.toWorkflowButton = SVGButton(top_panel, "gui/icons/ToWorkflow.svg", 20)
            self.toWorkflowButton.set_on_click(self.on_to_workflow)
            top_sizer.Add(self.toWorkflowButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        # 패널에 수평 박스 사이저 설정
        top_panel.SetSizer(top_sizer)

        # 수평 박스 사이저를 포함한 패널을 메인 수직 박스 사이저에 추가
        main_sizer.Add(top_panel, 0, wx.EXPAND | wx.ALL, 10)

        # 코드 입력 상자 (아래쪽)
        self.code = wx.TextCtrl(self, value=self.text, style=wx.NO_BORDER | wx.TE_MULTILINE |
                                wx.TE_NO_VSCROLL | wx.TE_RICH2 | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.code.SetEditable(False)
        self.code.SetBackgroundColour("#000000")
        self.code.SetForegroundColour("#FFFFFF")
        self.code.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.code.SetStyle(0, self.code.GetLastPosition(),
                           wx.TextAttr(wx.Colour(255, 255, 255)))  # 흰색 텍스트

        # 코드 입력 상자를 메인 수직 박스 사이저에 추가
        main_sizer.Add(self.code, 1, wx.EXPAND | wx.ALL, 10)

        # 메인 수직 박스 사이저를 패널에 설정
        self.SetSizer(main_sizer)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnPaint(self, event):
        width, height = self.GetSize()
        radius = 15  # 둥근 모서리의 반지름 설정

        # 더블 버퍼링을 위한 장치 맥락 생성
        dc = wx.BufferedPaintDC(self)
        dc.Clear()

        # 그래픽 컨텍스트 생성
        gc = wx.GraphicsContext.Create(dc)

        # 위쪽 모서리만 둥근 사각형 그리기 (path_top)
        path_top = gc.CreatePath()
        path_top.MoveToPoint(radius, 0)
        path_top.AddLineToPoint(width - radius, 0)
        path_top.AddArcToPoint(width, 0, width, radius, radius)  # 오른쪽 위 둥근 모서리
        path_top.AddLineToPoint(width, 40)
        path_top.AddLineToPoint(0, 40)
        path_top.AddLineToPoint(0, radius)
        path_top.AddArcToPoint(0, 0, radius, 0, radius)  # 왼쪽 위 둥근 모서리
        path_top.CloseSubpath()
        gc.SetBrush(wx.Brush("#1E1E1E"))  # 원하는 색상으로 변경
        gc.SetPen(wx.Pen("#1E1E1E", 0))
        gc.DrawPath(path_top)

        # 아래쪽 모서리만 둥근 사각형 그리기 (path_bottom)
        path_bottom = gc.CreatePath()
        path_bottom.MoveToPoint(0, 40)
        path_bottom.AddLineToPoint(0, height - radius)
        path_bottom.AddArcToPoint(0, height, radius, height, radius)  # 왼쪽 아래 둥근 모서리
        path_bottom.AddLineToPoint(width - radius, height)
        path_bottom.AddArcToPoint(width, height, width, height - radius, radius)  # 오른쪽 아래 둥근 모서리
        path_bottom.AddLineToPoint(width, 40)
        path_bottom.AddLineToPoint(0, 40)
        path_bottom.CloseSubpath()
        gc.SetBrush(wx.Brush("#000000"))
        gc.SetPen(wx.Pen("#000000", 0))
        gc.DrawPath(path_bottom)

    def OnResize(self, event):
        # 리사이즈 시 다시 그리기
        self.Refresh()
        event.Skip()

    def on_run(self, event):
        wx.MessageBox("language = " + self.language + "   texts = " + self.text, "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_copy(self, event):
        wx.MessageBox("Copy Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_edit(self, event):
        if self.code.IsEditable():
            self.code.SetEditable(False)
        else:
            self.code.SetEditable(True)

    def on_delete(self, event):
        wx.MessageBox("Delete Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_to_workflow(self, event):
        wx.MessageBox("toWorkflow Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)
