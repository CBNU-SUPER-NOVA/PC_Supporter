import wx
from gui.componets.common.SVGButton import SVGButton
from gui.componets.side.ConversationPanel import ConversationPanel
from gui.componets.side.Setting import Settings
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
        self.settingButton.set_on_click(self.on_open_settings)

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
        self.Parent.Parent.aiPanel.Enable(True)
        self.Hide()

    def newChatButtonClick(self, event):
        # AI 패널의 새 채팅 버튼 클릭과 동일한 동작 수행
        self.Parent.Parent.aiPanel.newChatButtonClick(event)

    def promptSettingButtonClick(self, event):
        """
        사용자가 프롬프트 설정 버튼을 클릭했을 때 호출되는 함수.
        여기서는 프롬프트를 입력받아 저장해둡니다.
        """
        # 프롬프트 입력을 위한 다이얼로그 생성
        prompt_dialog = wx.TextEntryDialog(self, "Enter the default prompt to use in future:", "Prompt Setting")

        # 사용자가 OK를 눌렀을 때만 동작
        if prompt_dialog.ShowModal() == wx.ID_OK:
            user_prompt = prompt_dialog.GetValue()  # 입력된 프롬프트 가져오기
            if user_prompt.strip():  # 공백이 아닌 경우에만 처리
                # AiPanel의 prompt_panel에 접근하여 프롬프트 저장
                ai_panel = self.Parent.Parent.aiPanel  # AiPanel에 접근
                if hasattr(ai_panel, 'prompt_panel'):
                    ai_panel.prompt_panel.set_saved_prompt(user_prompt)  # 프롬프트를 저장

                    # 저장 성공 메시지 출력
                    wx.MessageBox("Prompt has been saved.", "Success", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("Prompt input panel not found!", "Error", wx.OK | wx.ICON_ERROR)

        # 다이얼로그 닫기
        prompt_dialog.Destroy()

    def on_workflow_click(self, event):
        self.sideBarButtonClick(event)
        clicked_panel = event.GetEventObject()
        conversation_id = clicked_panel.conversation_id  # 여기서 conversation_id를 올바르게 가져옴
        # 대화 ID를 이용해 다음 단계로 연결하는 로직 추가
        self.Parent.Parent.refresh_data(conversation_id)

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
            # 각 converastionPanel에 conversation_id 저장
            workflow_panel = ConversationPanel(
                self.scroll_panel, size=(340, 40), radius=20, texts=conversation[1], alignment="left", color=self.background_color)
            workflow_panel.SetBackgroundColour(self.background_color)
            workflow_panel.conversation_id = conversation[0]  # 대화 ID 저장
            self.workflow_sizer.Add(workflow_panel, 0, wx.ALL | wx.EXPAND, 5)
            workflow_panel.on_click(self.on_workflow_click)

        # 레이아웃 업데이트
        self.workflow_sizer.Layout()
        self.scroll_panel.FitInside()

    def on_open_settings(self, event):
        """설정 창 열기"""
        dialog = Settings(self)
        if dialog.ShowModal() == wx.ID_OK:
            selected_option = dialog.get_selection()  # 선택된 옵션 가져오기
            wx.MessageBox(f"Selected: {selected_option}", "Settings", wx.OK | wx.ICON_INFORMATION)

        self.Parent.Parent.aiPanel.prompt_panel.use_api = selected_option

        dialog.Destroy()
