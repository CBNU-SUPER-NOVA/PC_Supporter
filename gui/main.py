import wx
from ai_panel import AiPanel
from side_panel import OverlayPanel


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        # 메인 패널 생성 및 추가
        self.main_panel = AiPanel(self)

        # 오버레이 패널 생성 및 추가
        self.overlay_panel = OverlayPanel(self.main_panel)

        # 버튼 이벤트 핸들러 바인딩
        self.main_panel.bind_toggle_button(self.on_toggle_overlay)

        self.SetSize((1200, 800))
        self.SetTitle("Panel Management Example")

    def on_toggle_overlay(self, event):
        if self.overlay_panel.IsShown():
            self.overlay_panel.Hide()  # 오버레이 패널 숨기기
        else:
            self.overlay_panel.Show()  # 오버레이 패널 보이기
        self.main_panel.Refresh()  # 화면 갱신


def main():
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    main()
