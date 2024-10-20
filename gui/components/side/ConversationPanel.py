import wx
from gui.components import RoundedPanel
from utils.db_handler import update_conversation_name, delete_conversation_and_related_data


class ConversationPanel(RoundedPanel):
    def __init__(self, parent, size, radius, texts, alignment="center", color="#D0D0D0", hover_color="#C0C0C0"):
        super(ConversationPanel, self).__init__(parent, size, radius, texts, alignment, color, hover_color)

        # 우클릭 이벤트 바인딩
        self.Bind(wx.EVT_RIGHT_DOWN, self.show_context_menu)

    def show_context_menu(self, event):
        # 팝업 메뉴 생성
        menu = wx.Menu()

        # 메뉴 항목 생성
        edit_item = menu.Append(wx.ID_EDIT, "Edit")
        delete_item = menu.Append(wx.ID_DELETE, "Delete")

        # 메뉴 항목에 이벤트 핸들러 연결
        self.Bind(wx.EVT_MENU, self.on_edit, edit_item)
        self.Bind(wx.EVT_MENU, self.on_delete, delete_item)

        # 마우스 포인터 위치에서 메뉴를 팝업
        self.PopupMenu(menu, event.GetPosition())

        # 메뉴 삭제 (메모리 관리)
        menu.Destroy()

    # Edit 메뉴 항목 선택 시 호출되는 함수
    def on_edit(self, event):
        # 텍스트 입력을 받는 다이얼로그 생성
        dialog = wx.TextEntryDialog(self, "Edit conversation name:", "Edit", self.texts)
        # 다이얼로그가 확인 버튼을 눌러서 종료되었을 때
        if dialog.ShowModal() == wx.ID_OK:
            new_text = dialog.GetValue()  # 입력된 새 텍스트를 가져옴
            self.texts = new_text  # 텍스트 업데이트
            update_conversation_name(self.conversation_id, new_text)  # 대화 이름 업데이트 함수 호출
            self.Refresh()  # UI 갱신 (화면을 다시 그림)
        dialog.Destroy()

    # Delete 메뉴 항목 선택 시 호출되는 함수
    def on_delete(self, event):
        # 대화 삭제 함수 호출
        delete_conversation_and_related_data(self.conversation_id)
        wx.MessageBox(f"{self.texts} is being deleted!", "Delete", wx.OK | wx.ICON_INFORMATION)
        # 대화 목록 업데이트
        wx.GetTopLevelParent(self).sidePanel.update_list()
