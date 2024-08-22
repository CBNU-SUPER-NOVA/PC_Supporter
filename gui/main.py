import wx
from gui.ai_panel import AiPanel
from gui.side_panel import SidePanel
from gui.code_panel import CodePanel


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.SetSize((1200, 800))
        self.SetTitle("PCSupporter")

        # 스플릿 패널 추가
        splitter = wx.SplitterWindow(self)

        # 메인 패널 생성 및 추가
        self.main_panel = AiPanel(splitter)

        # 코드 패널 생성 및 추가
        self.code_panel = CodePanel(splitter)

        # 스플릿 패널 속성
        splitter.SetMinimumPaneSize(600)
        splitter.SplitVertically(self.main_panel, self.code_panel)

        # 오버레이 패널 생성 및 추가
        self.overlay_panel = SidePanel(self.main_panel)

        # 버튼 이벤트 핸들러 바인딩
        self.main_panel.bindSideBarButton(self.on_toggle_overlay)

    def on_toggle_overlay(self, event):
        if self.overlay_panel.IsShown():
            self.overlay_panel.Hide()  # 오버레이 패널 숨기기
        else:
            self.overlay_panel.Show()  # 오버레이 패널 보이기
        self.main_panel.Refresh()  # 화면 갱신

    def newChat(self):
        print("newChat created")


def main():
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    main()
