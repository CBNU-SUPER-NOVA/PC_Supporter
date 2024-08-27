import wx
from gui.componets.SVGButton import SVGButton
from gui.componets.RoundedPanel import RoundedPanel
from utils.db_handler import get_conversation_names


class SidePanel(wx.Panel):
    def __init__(self, parent):
        super(SidePanel, self).__init__(parent, size=(
            400, parent.GetClientSize().GetHeight()))

        # 컬러 설정
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
        self.scroll_panel = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scroll_panel.SetBackgroundColour(self.background_color)
        self.scroll_panel.SetScrollRate(20, 20)

        # 대화 목록을 출력할 sizer 생성
        self.workflow_sizer = wx.BoxSizer(wx.VERTICAL)
        self.scroll_panel.SetSizer(self.workflow_sizer)

        main_sizer.Add(self.scroll_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 메인 사이저 설정
        self.SetSizer(main_sizer)
        self.Layout()  # 초기 레이아웃 설정

        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_SHOW, self.on_show)  # 패널이 보일 때 크기를 조정

        #  처음생성시 대화 목록 업데이트
        self.update_list()

        # 초기에는 숨김
        self.Hide()

    def on_resize(self, event):
        self.SetSize((self.GetSize().GetWidth(),
                     self.Parent.GetClientSize().GetHeight()))
        self.Layout()  # 레이아웃 갱신
        event.Skip()

    def on_show(self, event):
        if event.IsShown():
            self.SetSize((self.GetSize().GetWidth(),
                         self.Parent.GetClientSize().GetHeight()))
            self.Layout()

    def sideBarButtonClick(self, event):
        self.Parent.Parent.main_panel.Enable(True)
        self.Hide()

    def settingButtonClick(self, event):
        print("Setting Button Clicked")

    def newChatButtonClick(self, event):
        # AI 패널의 새 채팅 버튼 클릭과 동일한 동작 수행
        self.Parent.Parent.main_panel.newChatButtonClick(event)

    def promptSettingButtonClick(self, event):
        print("Prompt Setting Button Clicked")

    def on_workflow_click(self, event):
        clicked_panel = event.GetEventObject()
        conversation_id = clicked_panel.conversation_id  # 여기서 conversation_id를 올바르게 가져옴
        print(f"Clicked conversation ID: {conversation_id}")
        # 대화 ID를 이용해 다음 단계로 연결하는 로직 추가

    def update_list(self):
        """
        대화 목록을 업데이트하는 메서드
        """
        # 기존 목록 삭제
        for child in self.workflow_sizer.GetChildren():
            child.GetWindow().Destroy()

        # 새로운 대화 목록을 DB에서 가져오기
        conversation_names = get_conversation_names()

        # 새로운 대화 목록을 UI에 추가
        for conversation in conversation_names:
            # 각 RoundedPanel에 conversation_id 저장
            workflow_panel = RoundedPanel(
                self.scroll_panel, size=(340, 40), radius=20, texts=conversation[1], alignment="left", color=self.background_color)
            workflow_panel.SetBackgroundColour(self.background_color)
            workflow_panel.conversation_id = conversation[0]  # 대화 ID 저장
            self.workflow_sizer.Add(workflow_panel, 0, wx.ALL | wx.EXPAND, 5)
            workflow_panel.Bind(
                wx.EVT_LEFT_UP, self.on_workflow_click)  # 이벤트 바인딩

        # 레이아웃 업데이트
        self.workflow_sizer.Layout()
        self.scroll_panel.FitInside()
