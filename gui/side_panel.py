import wx
from gui.componets.SVGButton import SVGButton
from gui.componets.RoundedPanel import RoundedPanel

string_array = ["apple", "banana", "cherry", "date",
                "나는 문어", "꿈을 꾸는 문어", " 꿈속에서는 무엇이든지 할수있어", " 으아악ㅇㄱㅇ각",
                "나는 문어", "꿈을 꾸는 문어", " 꿈속에서는 무엇이든지 할수있어", " 으아악ㅇㄱㅇ각",
                "나는 문어", "꿈을 꾸는 문어", " 꿈속에서는 무엇이든지 할수있어", " 으아악ㅇㄱㅇ각",
                "나는 문어", "꿈을 꾸는 문어", " 꿈속에서는 무엇이든지 할수있어", " 으아악ㅇㄱㅇ각",
                "나는 문어", "꿈을 꾸는 문어", " 꿈속에서는 무엇이든지 할수있어", " 으아악ㅇㄱㅇ각"]


class SidePanel(wx.Panel):
    def __init__(self, parent):
        super(SidePanel, self).__init__(parent, size=(400, 800))

        # 컬러 설정
        # GPT 추천 컬러 => E5E5E5
        self.background_color = "#F7F7F8"
        self.text_color = "#000000"

        # 배경색 설정
        self.SetBackgroundColour(self.background_color)

        # 더블 버퍼링 활성화
        self.SetDoubleBuffered(True)

        # 상단 버튼들의 박스사이저 생성
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 사이드바 버튼 생성
        self.sideBarButton = SVGButton(
            self, "gui/icons/SideBar.svg", 40, hover_color="#AAAAAA")
        self.sideBarButton.SetBackgroundColour(self.background_color)
        top_sizer.Add(self.sideBarButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        self.sideBarButton.set_on_click(self.sideBarButtonClick)

        # 새 채팅 추가 버튼
        self.newChatButton = SVGButton(
            self, "gui/icons/NewChat.svg", 40, hover_color="#AAAAAA")
        self.newChatButton.SetBackgroundColour(self.background_color)
        top_sizer.Add(self.newChatButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        self.newChatButton.set_on_click(self.newChatButtonClick)

        # 중간 공간 추가하여 버튼들을 우측으로 밀어내기
        top_sizer.AddStretchSpacer(1)

        # 세팅 버튼 생성
        self.settingButton = SVGButton(
            self, "gui/icons/Setting.svg", 40, hover_color="#AAAAAA")
        self.settingButton.SetBackgroundColour(self.background_color)
        top_sizer.Add(self.settingButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        self.settingButton.set_on_click(self.settingButtonClick)

        # prompt setting button
        self.promptSettingButton = SVGButton(
            self, "gui/icons/PromptSetting.svg", 40, hover_color="#AAAAAA")
        self.promptSettingButton.SetBackgroundColour(self.background_color)
        top_sizer.Add(self.promptSettingButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        self.promptSettingButton.set_on_click(self.promptSettingButtonClick)

        # main_sizer 생성
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(top_sizer, 0, wx.EXPAND | wx.TOP, 10)

        # 스크롤 가능한 영역 생성
        scroll_panel = wx.ScrolledWindow(self, style=wx.VSCROLL)
        scroll_panel.SetBackgroundColour(self.background_color)
        scroll_panel.SetScrollRate(20, 20)

        # workflow들을 출력할 sizer 생성
        workflow_sizer = wx.BoxSizer(wx.VERTICAL)
        for workflow in string_array:
            workflow_panel = RoundedPanel(
                scroll_panel, size=(340, 40), radius=20, texts=workflow, alignment="left", color=self.background_color)
            workflow_panel.SetBackgroundColour(self.background_color)
            workflow_sizer.Add(workflow_panel, 0, wx.ALL | wx.EXPAND, 5)
            workflow_panel.on_click(self.on_workflow_click)

        scroll_panel.SetSizer(workflow_sizer)
        workflow_sizer.Fit(scroll_panel)

        main_sizer.Add(scroll_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 메인 사이저 설정
        self.SetSizer(main_sizer)
        self.Layout()  # 초기 레이아웃 설정

        self.Bind(wx.EVT_SIZE, self.on_resize)

        # 초기에는 숨김
        self.Hide()

    def on_resize(self, event):
        self.Layout()  # 레이아웃 갱신
        event.Skip()

    def sideBarButtonClick(self, event):
        self.Parent.Parent.main_panel.Enable(True)
        self.Hide()

    def settingButtonClick(self, event):
        print("Setting Button Clicked")

    def newChatButtonClick(self, event):
        self.Parent.Parent.newChat()

    def promptSettingButtonClick(self, event):
        print("Prompt Setting Button Clicked")

    def on_workflow_click(self, event):
        print("Workflow Clicked")
