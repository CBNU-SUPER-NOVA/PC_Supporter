import wx
from gui.componets.CodeBox import CodeBox
from gui.componets.SVGButton import SVGButton
from gui.componets.RoundedPanel import RoundedPanel

# 임시데이터
json = [("ls -al", "bash"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa)\npruint\n\n\nratasdf", "python"),
        ("print('Hello, World!')", "python")]


class CodePanel(wx.Panel):
    def __init__(self, parent):
        super(CodePanel, self).__init__(parent)
        self.SetSize(600, 800)
        self.SetBackgroundColour("white")

        # 메인 Sizer 생성 (수직 배치)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # ScrolledWindow 생성 (수직 스크롤만 허용)
        self.scrolled_window = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scrolled_window.SetScrollRate(20, 20)  # 스크롤 속도 설정
        self.scrolled_window.SetBackgroundColour("white")

        # Sizer 생성
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.scrolled_window.SetSizer(self.sizer)

        # sizer에 코드박스 추가
        for i, code_info in enumerate(json):
            code_box = CodeBox(self.scrolled_window, True,
                               code_info[0], code_info[1])
            self.sizer.Add(code_box, 0, wx.ALL | wx.EXPAND, 10)

        # ScrolledWindow를 메인 Sizer에 추가
        main_sizer.Add(self.scrolled_window, 1, wx.EXPAND | wx.ALL, 5)

        # 독립적인 버튼 생성
        WorkflowRunButton = RoundedPanel(
            self, size=(300, 50), radius=25, alignment="center", texts="Workflow Run", color="#F7F7F8", hover_color="#C0C0C0")
        WorkflowRunButton.on_click(self.workflowRun)
        main_sizer.Add(WorkflowRunButton, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(main_sizer)

        # 창 크기 조정 시 가로 크기를 다시 맞춤
        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_resize(self, event):
        self.GetSizer().Layout()
        self.scrolled_window.FitInside()  # 스크롤 윈도우 내부 크기 재조정
        event.Skip()

    def workflowRun(self, code):
        print("workflowRun")
