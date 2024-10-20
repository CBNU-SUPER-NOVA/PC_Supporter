import wx
from gui.components import CodeBox, SVGButton, PromptInputPanel, AIChatBox, MyChatBox
from utils.db_handler import create_conversation, get_code_blocks, get_messages


class AiPanel(wx.Panel):
    def __init__(self, parent):
        super(AiPanel, self).__init__(parent)
        self.SetBackgroundColour("#FFFFFF")

        self.conversation_id = None  # 초기화

        # 더블 버퍼링 활성화
        self.SetDoubleBuffered(True)

        # main_sizer 생성
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 상단의 버튼들 박스사이저 생성
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 사이드바 버튼 생성
        self.sidebar_button = SVGButton(
            self, "gui/icons/SideBar.svg", 40, self.sidebar_button_click, hover_color="#AAAAAA")
        top_sizer.Add(self.sidebar_button, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        # New chat 버튼 생성
        self.new_chat_button = SVGButton(
            self, "gui/icons/NewChat.svg", 40, self.new_chat_button_click, hover_color="#AAAAAA")
        top_sizer.Add(self.new_chat_button, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        main_sizer.Add(top_sizer, 0, wx.EXPAND | wx.TOP, 10)

        # 중단의 AI 생성한 코드 출력 창 생성 (스크롤 가능)
        self.middle_panel = wx.ScrolledWindow(
            self, style=wx.VSCROLL | wx.HSCROLL)
        self.middle_panel.SetScrollRate(35, 35)
        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        self.middle_panel.SetSizer(middle_sizer)

        main_sizer.Add(self.middle_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 하단의 프롬프트 입력 패널 추가
        self.prompt_panel = PromptInputPanel(self)
        main_sizer.Add(self.prompt_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main_sizer)
        self.Layout()

    def sidebar_button_click(self, event):
        wx.GetTopLevelParent(self).sidePanel.Show()
        self.Enable(False)

    def update_list(self):
        # 대화 목록 초기화
        for child in self.middle_panel.GetChildren():
            child.Destroy()

        # 대화 목록을 데이터베이스에서 불러와 생성
        conversations = get_messages(self.conversation_id)
        for conversation in conversations:
            if conversation[0] == "user":
                chat_box = MyChatBox(self.middle_panel, conversation[2])
            else:
                chat_box = AIChatBox(
                    self.middle_panel, conversation[1], conversation[2], conversation_id=self.conversation_id)
            self.middle_panel.GetSizer().Add(chat_box, 0, wx.ALL | wx.EXPAND, 10)

        self.middle_panel.GetSizer().Layout()
        self.middle_panel.FitInside()

    def new_chat_button_click(self, event):
        # 기존의 함수에 대화 생성 로직 추가
        dialog = wx.TextEntryDialog(
            self, 'Enter the conversation name :', 'New Conversation')
        if dialog.ShowModal() == wx.ID_OK:
            conversation_name = dialog.GetValue()
            # 데이터베이스에 새로운 대화 생성
            conversation_id = create_conversation(conversation_name)
            wx.MessageBox(f'Conversation "{conversation_name}" created with ID {conversation_id}', 'Info', wx.OK | wx.ICON_INFORMATION)

            # 새로운 대화 생성 후 사이드 패널 업데이트 호출
            wx.GetTopLevelParent(self).sidePanel.update_list()

        dialog.Destroy()

    def refresh_data(self, conversation_id):
        """
        주어진 대화 ID에 해당하는 데이터를 가져와 UI에 출력합니다.
        """
        # 기존 대화 데이터를 초기화
        self.middle_panel.GetSizer().Clear(True)

        # DB에서 대화 ID에 해당하는 메시지와 코드 블록을 가져옴
        messages = get_messages(conversation_id)
        code_blocks = get_code_blocks(conversation_id)

        # 메시지를 UI에 추가
        for message in messages:
            if message['sender_type'] == 'user':
                user_chat = MyChatBox(self.middle_panel, message['content'])
                self.middle_panel.GetSizer().Add(user_chat, 0, wx.ALL | wx.EXPAND, 5)
            else:
                ai_chat = AIChatBox(self.middle_panel, message['content'])
                self.middle_panel.GetSizer().Add(ai_chat, 0, wx.ALL | wx.EXPAND, 5)

        # 코드 블록을 UI에 추가
        for code_block in code_blocks:
            code_box = CodeBox(self.middle_panel, True,
                               code_block['code_data'], code_block['code_type'])
            self.middle_panel.GetSizer().Add(code_box, 0, wx.ALL | wx.EXPAND, 5)

        # 레이아웃 갱신
        self.middle_panel.GetSizer().Layout()
        self.middle_panel.FitInside()

    def set_conversation_id(self, conversation_id):
        """SidePanel에서 선택된 conversation_id를 설정"""
        self.conversation_id = conversation_id
        self.prompt_panel.conversation_id = conversation_id  # PromptInputPanel에도 설정
