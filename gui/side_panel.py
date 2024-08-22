import wx
import wx.svg
from gui.componets.SVGButton import SVGButton
from gui.componets.RoundedPanel import RoundedPanel

string_array = ["apple", "banana", "cherry", "date",
                "나는 문어", "꿈을 꾸는 문어", " 꿈속에서는 무엇이든지 할수있어", " 으아악ㅇㄱㅇ각"]


class SidePanel(wx.Panel):
    def __init__(self, parent):
        super(SidePanel, self).__init__(
            parent, size=(400, 800))
        self.SetBackgroundColour("#D0D0D0")

        # 더블 버퍼링 활성화
        self.SetDoubleBuffered(True)

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

        # workflow들 출력
        for index, workflow in enumerate(string_array):
            self.workflow = RoundedPanel(self, (360, 40), 20, workflow)
            self.workflow.SetPosition((20, 60 + 60 * index))

        # 초기에는 숨김
        self.Hide()

    def sideBarButtonClick(self, event):
        self.Hide()
        self.Parent.SidebarButton.Show()
        self.Parent.NewChatButton.Show()

    def settingButtonClick(self, event):
        print("Setting Button Clicked")

    def newChatButtonClick(self, event):
        self.Parent.Parent.newChat()

    def promptSettingButtonClick(self, event):
        print("Prompt Setting Button Clicked")
