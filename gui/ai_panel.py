import wx
from gui.componets.SVGButton import SVGButton
from gui.componets.PromptInputPanel import PromptInputPanel
from gui.componets.AIChatBox import AIChatBox
from gui.componets.MyChatBox import MyChatBox


tempdata = [
    {"type": "AI", "data": "안녕하세요. PC지원팀입니다."},
    {"type": "AI", "data": "무엇을 도와드릴까요?"},
    {"type": "User", "data": "PC가 느려요."},
    {"type": "AI", "data": "PC가 언제부터 느려졌나요?"},
    {"type": "User", "data": "며칠 전부터요."},
    {"type": "AI", "data": "혹시 어떤 프로그램을 실행할 때 느려지나요?"},
    {"type": "User", "data": "특히 인터넷 브라우저를 사용할 때 느려져요."},
    {"type": "AI", "data": "인터넷 브라우저의 캐시를 삭제해 보셨나요?"},
    {"type": "User", "data": "아니요, 어떻게 하는지 잘 모르겠어요."},
    {"type": "AI", "data": "인터넷 브라우저에서 설정 메뉴로 가신 후, '기록' 또는 '캐시'를 삭제해 보세요."},
    {"type": "User", "data": "알겠습니다. 한 번 시도해 볼게요."},
    {"type": "AI", "data": "다른 질문이 있으신가요?"},
    {"type": "User", "data": "PC가 가끔씩 혼자 재부팅되는데, 이유가 뭘까요?"},
    {"type": "AI", "data": "PC가 과열되면 자동으로 재부팅될 수 있습니다. 최근에 PC가 뜨거워지지 않았나요?"},
    {"type": "User", "data": "네, 요즘 계속 뜨거운 것 같아요."},
    {"type": "AI", "data": "쿨러나 팬이 정상적으로 작동하는지 확인해 보셨나요?"},
    {"type": "User", "data": "아직 확인하지 않았어요. 어떻게 확인할 수 있죠?"},
    {"type": "AI", "data": "PC를 열고 팬이 정상적으로 회전하는지 확인해 보세요. 팬이 돌아가지 않으면 청소하거나 교체해야 할 수 있습니다."},
    {"type": "User", "data": "알겠습니다. 확인해 볼게요."},
    {"type": "AI", "data": "또 다른 문제가 있나요?"},
    {"type": "User", "data": "최근에 새로운 프로그램을 설치한 이후부터 문제가 생긴 것 같아요."},
    {"type": "AI", "data": "어떤 프로그램을 설치하셨나요?"},
    {"type": "User", "data": "새로운 게임을 설치했어요."},
    {"type": "AI", "data": "게임이 PC 사양을 초과하는 경우, 성능 저하가 발생할 수 있습니다. 시스템 요구 사항을 확인해 보셨나요?"},
    {"type": "User", "data": "아니요, 확인하지 않았어요."},
    {"type": "AI", "data": "게임의 시스템 요구 사항과 PC의 사양을 비교해 보세요. PC 사양이 부족하다면 설정을 낮추거나 다른 조치를 고려해 보셔야 합니다."},
    {"type": "User", "data": "네, 그렇게 해볼게요."},
    {"type": "AI", "data": "도움이 되셨길 바랍니다. 더 궁금한 사항이 있으면 언제든지 말씀해 주세요."},
    {"type": "User", "data": "감사합니다. 큰 도움이 되었어요."},
    {"type": "AI", "data": "천만에요! 좋은 하루 되세요."},
    {"type": "User", "data": "네, 감사합니다."},
    {"type": "AI", "data": "PC 관련해서 더 필요하신 사항이 있으면 언제든지 연락 주세요."},
    {"type": "User", "data": "알겠습니다. 감사합니다."},
    {"type": "AI", "data": "오늘도 좋은 하루 보내세요."},
    {"type": "User", "data": "네, 좋은 하루 보내세요."},
]


class AiPanel(wx.Panel):
    def __init__(self, parent):
        super(AiPanel, self).__init__(parent)
        self.SetBackgroundColour("#FFFFFF")

        # 더블 버퍼링 활성화
        self.SetDoubleBuffered(True)

        # main_sizer 생성
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 상단의 버튼들 박스사이저 생성
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 사이드바 버튼 생성
        self.SidebarButton = SVGButton(self, "gui/icons/SideBar.svg", 40)
        self.SidebarButton.set_on_click(self.SidebarButtonClick)
        top_sizer.Add(self.SidebarButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        # New chat 버튼 생성
        self.NewChatButton = SVGButton(self, "gui/icons/NewChat.svg", 40)
        self.NewChatButton.set_on_click(self.newChatButtonClick)
        top_sizer.Add(self.NewChatButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        main_sizer.Add(top_sizer, 0, wx.EXPAND | wx.TOP, 10)

        # 중단의 AI 생성한 코드 출력 창 생성 (스크롤 가능)
        self.middle_panel = wx.ScrolledWindow(
            self, style=wx.VSCROLL | wx.HSCROLL)
        self.middle_panel.SetScrollRate(5, 5)
        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        self.middle_panel.SetSizer(middle_sizer)

        # 임시 데이터 추가
        # for i in range(20):  # 20개의 임시 데이터를 추가
        #     label = wx.StaticText(self.middle_panel, label=f"임시 데이터 {i+1}")
        #     middle_sizer.Add(label, 0, wx.ALL, 5)
        for data in tempdata:
            if data["type"] == "AI":
                ai_chat = AIChatBox(self.middle_panel, data["data"])
                middle_sizer.Add(ai_chat, 0, wx.ALL, 5)
            elif data["type"] == "User":
                user_chat = MyChatBox(self.middle_panel, data["data"])
                middle_sizer.Add(user_chat, 0, wx.ALL, 5)

        main_sizer.Add(self.middle_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 하단의 프롬프트 입력 패널 추가
        self.prompt_panel = PromptInputPanel(self)
        main_sizer.Add(self.prompt_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main_sizer)
        self.Layout()

    def SidebarButtonClick(self, event):
        self.Parent.Parent.overlay_panel.Show()
        self.Enable(False)

    def newChatButtonClick(self, event):
        self.Parent.newChat()
