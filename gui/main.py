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
        self.code_panel = CodePanel(self.splitter, conversation_id=None)  # 'conversation_id=None' 명시적으로 추가

        # 스플릿 패널 속성
        self.splitter.SetMinimumPaneSize(600)
        self.splitter.SplitVertically(self.main_panel, self.code_panel)

        # 오버레이 패널 생성 및 추가
        self.overlay_panel = SidePanel(self.splitter)

        # 메인 패널과 코드 패널의 상호작용 설정
        self.main_panel.code_panel = self.code_panel
        self.main_panel.on_new_conversation = self.update_code_panel  # 새로운 대화 생성 시 호출될 메서드 설정

    def update_code_panel(self, conversation_id):
        """
        새로운 대화가 생성될 때 코드 패널을 업데이트하는 메서드
        """
        self.code_panel.update_conversation(conversation_id)
    
    def update_side_panel(self, conversation_id):
        """
        새로운 대화가 생성될 때 사이드 패널을 업데이트하는 메서드
        """
        self.overlay_panel.update_conversation_list()

def main():
    init_db()
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    main()
