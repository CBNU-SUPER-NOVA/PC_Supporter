import wx
from componets.SVGButton import SVGButton


class AiPanel(wx.Panel):
    def __init__(self, parent):
        super(AiPanel, self).__init__(parent)
        self.SetBackgroundColour("white")
        # 사이드바 버튼 생성
        self.SidebarButton = SVGButton(self, "gui/icons/SideBar.svg", 40)
        self.SidebarButton.pos(10, 10)
        # New chat 버튼 생성
        self.NewChatButton = SVGButton(self, "gui/icons/NewChat.svg", 40)
        self.NewChatButton.pos(60, 10)
        self.NewChatButton.set_on_click(self.newChatButtonClick)

    def bindSideBarButton(self, handler):
        def wrapped_handler(event):
            handler(event)
            self.SidebarButton.Hide()
            self.NewChatButton.Hide()
        # 외부에서 이벤트 핸들러를 바인딩할 수 있도록 메서드 추가
        self.SidebarButton.set_on_click(wrapped_handler)

    def newChatButtonClick(self, event):
        self.Parent.newChat()
