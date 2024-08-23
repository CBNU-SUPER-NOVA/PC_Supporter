import wx
from gui.componets.SVGButton import SVGButton
from gui.componets.PromptInputPanel import PromptInputPanel


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

        # 중단의 AI 생성한 코드 출력 창 생성
        self.AiOutput = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        main_sizer.Add(self.AiOutput, 1, wx.EXPAND | wx.ALL, 10)

        # 하단의 프롬프트 입력 패널 추가
        print("promp generated")
        self.prompt_panel = PromptInputPanel(self)
        main_sizer.Add(self.prompt_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main_sizer)
        self.Layout()

    def SidebarButtonClick(self, event):
        self.Parent.Parent.overlay_panel.Show()
        self.Enable(False)

    def newChatButtonClick(self, event):
        self.Parent.newChat()

    def sendButtonClick(self, event):
        textvalue = self.prompt_panel.get_prompt_text()
        self.prompt_panel.clear_prompt()
        from gpt_api.api import send_to_gpt
        json = send_to_gpt(textvalue)
        print(json)
