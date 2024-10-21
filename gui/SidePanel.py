import wx
from gui.components import SVGButton, ConversationPanel, Settings, Information
from gpt_api.api import validate_openai_api_key, validate_gemini_api_key
from utils.db_handler import get_conversation_names, save_prompt_setting, load_prompt_setting, save_api_key


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
        self.sidebar_button = SVGButton(self, "gui/icons/SideBar.svg", 40, self.sidebar_button_Click, hover_color="#AAAAAA")
        top_sizer.Add(self.sidebar_button, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        # 새 채팅 추가 버튼
        self.new_chat_button = SVGButton(
            self, "gui/icons/NewChat.svg", 40, self.new_chat_button_Click, hover_color="#AAAAAA")
        top_sizer.Add(self.new_chat_button, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        # 중간 공간 추가하여 버튼들을 우측으로 밀어내기
        top_sizer.AddStretchSpacer(1)

        # 세팅 버튼 생성
        self.setting_button = SVGButton(
            self, "gui/icons/Setting.svg", 40, hover_color="#AAAAAA")
        top_sizer.Add(self.setting_button, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        self.setting_button.set_on_click(self.on_open_settings)

        # prompt setting button
        self.prompt_setting_button = SVGButton(
            self, "gui/icons/promptsetting.svg", 40, self.prompt_setting_button_click, hover_color="#AAAAAA")
        top_sizer.Add(self.prompt_setting_button, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)

        # informaiton button 생성
        self.information_button = SVGButton(
            self, "gui/icons/info.svg", 40, self.information_button_click, hover_color="#AAAAAA")
        top_sizer.Add(self.information_button, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)

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

    def sidebar_button_Click(self, event):
        wx.GetTopLevelParent(self).aiPanel.Enable(True)
        self.Hide()

    def new_chat_button_Click(self, event):
        # AI 패널의 새 채팅 버튼 클릭과 동일한 동작 수행
        wx.GetTopLevelParent(self).aiPanel.new_chat_button_click(event)

    def prompt_setting_button_click(self, event):
        """
        사용자가 프롬프트 설정 버튼을 클릭했을 때 호출되는 함수.
        입력된 프롬프트를 DB에 저장하고 모든 대화에 적용합니다.
        """
        
        # 프롬프트 입력을 위한 다이얼로그 생성
        prompt_dialog = wx.TextEntryDialog(self, "AI가 더 나은 응답을 제공해 드리기 위해 사용자님에 대해 알아두어야 할 것이 있다면 무엇인가요?")

        if prompt_dialog.ShowModal() == wx.ID_OK:
            user_prompt = prompt_dialog.GetValue().strip()
            if user_prompt:
                # 프롬프트를 DB에 저장
                save_prompt_setting(user_prompt)

                # 저장 성공 메시지
                wx.MessageBox("Prompt has been saved to the database.", "Success", wx.OK | wx.ICON_INFORMATION)
        prompt_dialog.Destroy()


    def on_workflow_click(self, event):
        self.sidebar_button_Click(event)
        clicked_panel = event.GetEventObject()
        conversation_id = clicked_panel.conversation_id  # 여기서 conversation_id를 올바르게 가져옴
        # 대화 ID를 이용해 다음 단계로 연결하는 로직 추가
        wx.GetTopLevelParent(self).refresh_data(conversation_id)

    def update_list(self):
        """
        대화 목록을 업데이트하는 메서드.
        """
        # 기존 목록 삭제
        for child in self.workflow_sizer.GetChildren():
            child.GetWindow().Destroy()

        # 대화 목록 가져오기
        conversation_names = get_conversation_names()

        # 대화 목록 UI에 추가
        for conversation in conversation_names:
            workflow_panel = ConversationPanel(
                self.scroll_panel, size=(340, 40), radius=20, texts=conversation[1], alignment="left",
                color=self.background_color
            )
            workflow_panel.conversation_id = conversation[0]
            self.workflow_sizer.Add(workflow_panel, 0, wx.ALL | wx.EXPAND, 5)

        self.workflow_sizer.Layout()
        self.scroll_panel.FitInside()
    
    def apply_saved_prompt(self):
        """
        저장된 프롬프트를 모든 대화에 적용합니다.
        """
        saved_prompt = load_prompt_setting()
        if saved_prompt:
            # 모든 대화에 프롬프트 적용
            ai_panel = wx.GetTopLevelParent(self).aiPanel
            if hasattr(ai_panel, 'prompt_panel'):
                ai_panel.prompt_panel.set_saved_prompt(saved_prompt)

    def on_open_settings(self, event):
        """설정 창 열기 및 API 키 처리"""
        dialog = Settings(self)

        if dialog.ShowModal() == wx.ID_OK:
            selected_option = dialog.get_selection()
            wx.MessageBox(f"Selected: {selected_option}", "Settings", wx.OK | wx.ICON_INFORMATION)

            wx.GetTopLevelParent(self).aiPanel.prompt_panel.use_api = selected_option

            gpt_key = dialog.gpt_api_input.GetValue().strip()
            gemini_key = dialog.gemini_api_input.GetValue().strip()

            # GPT API 키 검증 및 저장
            if gpt_key and validate_openai_api_key(gpt_key):
                save_api_key("Chat GPT", gpt_key)
                wx.MessageBox("GPT API 키가 유효하고 저장되었습니다.", "성공", wx.OK | wx.ICON_INFORMATION)
            elif gpt_key:
                wx.MessageBox("GPT API 키가 유효하지 않습니다.", "오류", wx.OK | wx.ICON_ERROR)

            # Gemini API 키 검증 및 저장
            if gemini_key and validate_gemini_api_key(gemini_key):
                save_api_key("Gemini", gemini_key)
                wx.MessageBox("Gemini API 키가 유효하고 저장되었습니다.", "성공", wx.OK | wx.ICON_INFORMATION)
            elif gemini_key:
                wx.MessageBox("Gemini API 키가 유효하지 않습니다.", "오류", wx.OK | wx.ICON_ERROR)

        dialog.Destroy()


    def information_button_click(self, event):
        dialog = Information(self)
        dialog.ShowModal()
        dialog.Destroy()
