import wx
from gui.componets.CodeBox import CodeBox
from gui.componets.SVGButton import SVGButton

# 임시데이터
json = [("ls -al", "bash"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')\npruint\n\n\nratasdf", "python"),
        ("print('Hello, World!')", "python")]


class CodePanel(wx.Panel):
    def __init__(self, parent):
        super(CodePanel, self).__init__(parent)
        self.SetSize(600, 800)
        self.SetBackgroundColour("white")

        # 메인 Sizer 생성 (수직 배치)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # ScrolledWindow 생성 (수직 스크롤만 허용)
        scrolled_window = wx.ScrolledWindow(self, style=wx.VSCROLL)
        scrolled_window.SetScrollRate(20, 20)  # 스크롤 속도 설정
        scrolled_window.SetBackgroundColour("white")

        # Sizer 생성
        sizer = wx.BoxSizer(wx.VERTICAL)
        scrolled_window.SetSizer(sizer)

        # sizer에 코드박스 추가
        for i, code_info in enumerate(json):
            code_box = CodeBox(scrolled_window, True,
                               code_info[0], code_info[1])
            sizer.Add(code_box, 0, wx.ALL | wx.EXPAND, 10)

        # 내부 위젯의 크기에 맞게 ScrolledWindow 크기를 조정
        sizer.Fit(scrolled_window)

        # 가로 크기를 패널의 가로 크기로 고정하고 세로만 가상 크기 설정
        scrolled_window.SetVirtualSize(
            (self.GetClientSize().GetWidth(), sizer.GetMinSize().GetHeight()))
        scrolled_window.SetMinSize(
            (self.GetClientSize().GetWidth(), sizer.GetMinSize().GetHeight()))

        # ScrolledWindow를 메인 Sizer에 추가
        main_sizer.Add(scrolled_window, 1, wx.EXPAND | wx.ALL, 5)

        # 독립적인 버튼 생성
        runButton = wx.Button(self, label="Workflow Run")
        runButton.Bind(wx.EVT_BUTTON, self.workflowRun)
        main_sizer.Add(runButton, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(main_sizer)

        # 창 크기 조정 시 가로 크기를 다시 맞춤
        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_resize(self, event):
        self.GetSizer().Layout()
        event.Skip()

    def workflowRun(self, code):
        print("workflowRun")
