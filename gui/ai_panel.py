import wx
from gui.componets.SVGButton import SVGButton
from gui.componets.PromptInputPanel import PromptInputPanel
from gui.componets.AIChatBox import AIChatBox
from gui.componets.MyChatBox import MyChatBox
from gui.tempchatData import tempdata


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
        self.SidebarButton = SVGButton(
            self, "gui/icons/SideBar.svg", 40, hover_color="#AAAAAA")
        self.SidebarButton.set_on_click(self.SidebarButtonClick)
        top_sizer.Add(self.SidebarButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        # New chat 버튼 생성
        self.NewChatButton = SVGButton(
            self, "gui/icons/NewChat.svg", 40, hover_color="#AAAAAA")
        self.NewChatButton.set_on_click(self.newChatButtonClick)
        top_sizer.Add(self.NewChatButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        main_sizer.Add(top_sizer, 0, wx.EXPAND | wx.TOP, 10)

        # 중단의 AI 생성한 코드 출력 창 생성 (스크롤 가능)
        self.middle_panel = wx.ScrolledWindow(
            self, style=wx.VSCROLL | wx.HSCROLL)
        self.middle_panel.SetScrollRate(35, 35)
        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        self.middle_panel.SetSizer(middle_sizer)

        # 임시 데이터 추가
        for data in tempdata:
            if data["type"] == "AI":
                ai_chat = AIChatBox(self.middle_panel, data["data"])
                middle_sizer.Add(ai_chat, 0, wx.ALL | wx.EXPAND, 5)
            elif data["type"] == "User":
                user_chat = MyChatBox(self.middle_panel, data["data"])
                middle_sizer.Add(user_chat, 0, wx.ALL | wx.EXPAND, 5)

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
