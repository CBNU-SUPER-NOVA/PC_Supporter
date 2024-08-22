import wx


class CodeBox(wx.Panel):
    def __init__(self, parent, isWorkflow, texts, language="python"):
        super(CodeBox, self).__init__(parent)
        self.SetBackgroundColour("#FFFFFF")
        self.SetSize(400, 400)

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

        # 코딩언어 라벨 (좌측)
        self.codeLanguage = wx.StaticText(top_panel, label=self.language)
        self.codeLanguage.SetBackgroundColour("#1E1E1E")
        self.codeLanguage.SetForegroundColour("#FFFFFF")
        self.codeLanguage.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.codeLanguage.Wrap(400)

        top_sizer.Add(self.codeLanguage, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)

        # 버튼들 추가 (우측)
        self.runButton = wx.Button(top_panel, label="Run")
        self.runButton.Bind(wx.EVT_BUTTON, self.on_run)
        top_sizer.Add(self.runButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        self.copyButton = wx.Button(top_panel, label="Copy")
        self.copyButton.Bind(wx.EVT_BUTTON, self.on_copy)
        top_sizer.Add(self.copyButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        self.editButton = wx.Button(top_panel, label="Edit")
        self.editButton.Bind(wx.EVT_BUTTON, self.on_edit)
        top_sizer.Add(self.editButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        if isWorkflow:
            self.deleteButton = wx.Button(top_panel, label="Delete")
            self.deleteButton.Bind(wx.EVT_BUTTON, self.on_delete)
            top_sizer.Add(self.deleteButton, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        else:
            self.toWorkflowButton = wx.Button(top_panel, label="toWorkflow")
            self.toWorkflowButton.Bind(wx.EVT_BUTTON, self.on_to_workflow)
            top_sizer.Add(self.toWorkflowButton, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

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

        # 더블 버퍼링을 위한 장치 맥락 생성
        dc = wx.BufferedPaintDC(self)
        dc.Clear()

        # 그래픽 컨텍스트 생성
        gc = wx.GraphicsContext.Create(dc)

        # 둥근 사각형 그리기
        path = gc.CreatePath()
        path.AddRoundedRectangle(0, 0, width, height, 15)

        gc.SetBrush(wx.Brush("#000000"))
        gc.SetPen(wx.Pen("#000000", 4))
        gc.DrawPath(path)

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
