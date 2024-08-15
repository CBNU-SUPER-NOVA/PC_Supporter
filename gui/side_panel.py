import wx
import wx.svg
from componets.SVGButton import SVGButton


class SidePanel(wx.Panel):
    def __init__(self, parent):
        super(SidePanel, self).__init__(
            parent, size=(400, 800))
        self.SetBackgroundColour("light blue")

        # 사이드바 버튼 생성
        self.sideBarButton = SVGButton(self, "gui/icons/SideBar.svg", 40)
        self.sideBarButton.pos(10, 10)
        self.sideBarButton.set_on_click(self.sideBarButtonClick)
        # 새 채팅 추가 버튼
        self.newChatButton = SVGButton(self, "gui/icons/NewChat.svg", 40)
        self.newChatButton.pos(60, 10)
        self.newChatButton.set_on_click(self.newChatButtonClick)
        # 세팅 버튼 생성
        self.settingButton = SVGButton(self, "gui/icons/Setting.svg", 40)
        self.settingButton.pos(350, 10)
        self.settingButton.set_on_click(self.settingButtonClick)
        # prompt setting button
        self.promptSettingButton = SVGButton(
            self, "gui/icons/PromptSetting.svg", 40)
        self.promptSettingButton.pos(300, 10)
        self.promptSettingButton.set_on_click(self.settingButtonClick)

        # 임시 텍스트
        self.text = wx.StaticText(self, label="Overlay Panel", pos=(100, 200))
        self.text = wx.StaticText(self, label="Overlay Panel", pos=(100, 100))

        # 초기에는 숨김
        self.Hide()

    def sideBarButtonClick(self, event):
        self.Hide()
        self.Parent.SidebarButton.Show()

    def settingButtonClick(self, event):
        print("Setting Button Clicked")

    def newChatButtonClick(self, event):
        print("New Chat Button Clicked")

    def promptSettingButtonClick(self, event):
        print("Prompt Setting Button Clicked")
