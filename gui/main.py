import wx
from gui.ai_panel import AiPanel
from gui.side_panel import SidePanel
from gui.code_panel import CodePanel
from utils.db_handler import init_db


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.SetSize((1200, 800))
        self.SetTitle("PCSupporter")

        # 스플릿 패널 추가
        self.splitter = wx.SplitterWindow(self)

        # 메인 패널 생성 및 추가
        self.main_panel = AiPanel(self.splitter)

        # 코드 패널 생성 및 추가
        # 'conversation_id=None' 명시적으로 추가
        self.code_panel = CodePanel(self.splitter, conversation_id=None)

        # 스플릿 패널 속성
        self.splitter.SetMinimumPaneSize(600)
        self.splitter.SplitVertically(self.main_panel, self.code_panel)

        # 오버레이 패널 생성 및 추가
        self.overlay_panel = SidePanel(self.splitter)

    def refresh_data(self, conversation_id):
        # 데이터를 새로고침하는 메서드
        # self.main_panel.Refresh() <- 이부분은 생성되면 추가
        self.code_panel.update_list(conversation_id)
        self.overlay_panel.update_list


def main():
    init_db()
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    main()
