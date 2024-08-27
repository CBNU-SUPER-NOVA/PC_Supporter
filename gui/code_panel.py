import wx
import json
from gui.componets.CodeBox import CodeBox
from gui.componets.SVGButton import SVGButton
from gui.componets.RoundedPanel import RoundedPanel
from utils.code_handler import handle_code_blocks
from utils.code_executor import execute_code
from utils.db_handler import save_code_to_db, delete_code_from_db, update_code_order, get_code_blocks

# 임시데이터
json = [("ls -al", "bash"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!')", "python"),
        ("print('Hello, World!'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa)\npruint\n\n\nratasdf", "python"),
        ("print('Hello, World!')", "python")]


class CodePanel(wx.Panel):
    def __init__(self, parent, conversation_id):
        super(CodePanel, self).__init__(parent)
        self.SetSize(600, 800)
        self.SetBackgroundColour("white")
        self.conversation_id = conversation_id
        self.code_blocks = []  # 코드 블록 데이터를 저장할 리스트

        # 메인 Sizer 생성 (수직 배치)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # ScrolledWindow 생성 (수직 스크롤만 허용)
        self.scrolled_window = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scrolled_window.SetScrollRate(20, 20)  # 스크롤 속도 설정
        self.scrolled_window.SetBackgroundColour("white")

        # Sizer 생성
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.scrolled_window.SetSizer(self.sizer)

        # ScrolledWindow를 메인 Sizer에 추가
        main_sizer.Add(self.scrolled_window, 1, wx.EXPAND | wx.ALL, 5)

        # 독립적인 버튼 생성
        WorkflowRunButton = RoundedPanel(
            self, size=(300, 50), radius=25, alignment="center", texts="Workflow Run", color="#F7F7F8", hover_color="#C0C0C0")
        
        WorkflowRunButton.Bind(wx.EVT_LEFT_DOWN, self.workflowRun)  # 이벤트 핸들러로 수정
        main_sizer.Add(WorkflowRunButton, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(main_sizer)

        # 코드 블록들을 UI에 추가
        self.update_list(conversation_id)

        # 창 크기 조정 시 가로 크기를 다시 맞춤
        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_resize(self, event):
        self.GetSizer().Layout()
        self.scrolled_window.FitInside()  # 스크롤 윈도우 내부 크기 재조정
        event.Skip()

    def update_list(self, conversation_id):
        self.code_blocks = get_code_blocks(conversation_id)
        print("Fetched code blocks:", self.code_blocks)  # 디버깅 출력

        for child in self.sizer.GetChildren():
            child.GetWindow().Destroy()

        for code_block in self.code_blocks:
            code_id, code_type, code_data, order_num = code_block
            print(f"Adding CodeBox with data: {code_data}, type: {code_type}")  # 디버깅 출력
            code_box = CodeBox(self.scrolled_window, True, code_data, code_type, code_id=code_id)
            self.sizer.Add(code_box, 0, wx.ALL | wx.EXPAND, 10)

        self.sizer.Layout()
        self.scrolled_window.FitInside()


    def add_code_block_to_ui(self, code, language, order):
        # 코드 블록을 UI에 추가하는 메서드
        code_box = CodeBox(self.scrolled_window, True, code, language)
        code_box.delete_callback = lambda evt, cb=code_box: self.RemoveCodeBlock(
            cb)  # 삭제 콜백 설정
        code_box.up_callback = lambda evt, cb=code_box: self.move_code_block_up(
            cb)  # 위로 이동 콜백
        code_box.down_callback = lambda evt, cb=code_box: self.move_code_block_down(
            cb)  # 아래로 이동 콜백
        self.sizer.Add(code_box, 0, wx.ALL | wx.EXPAND, 10)
        self.code_blocks.append(
            {'data': code, 'language': language, 'order': order})  # 리스트에 추가
        save_code_to_db(self.conversation_id, code,
                        language, order)  # 데이터베이스에 저장

    def RemoveCodeBlock(self, code_box):
        # 'X' 버튼이 클릭된 CodeBox를 제거하는 메서드
        # UI에서 제거하는 방식이 아닌 없애고 새로 그리는 방식으로 구현
        self.code_blocks = [
            block for block in self.code_blocks if block['data'] != code_box.text]
        delete_code_from_db(code_box.text)  # 데이터베이스에서 코드 블록 삭제
        self.update_ui()

    def move_code_block_up(self, code_box):
        # 코드 블록을 위로 이동시키는 메서드
        index = self.sizer.GetChildren().index(code_box.GetContainingSizer())
        if index > 0:
            self.sizer.Remove(index)
            self.sizer.Insert(index - 1, code_box, 0, wx.ALL | wx.EXPAND, 10)
            self.update_code_order_in_db()
            self.update_ui()

    def move_code_block_down(self, code_box):
        # 코드 블록을 아래로 이동시키는 메서드
        index = self.sizer.GetChildren().index(code_box.GetContainingSizer())
        if index < len(self.sizer.GetChildren()) - 1:
            self.sizer.Remove(index)
            self.sizer.Insert(index + 1, code_box, 0, wx.ALL | wx.EXPAND, 10)
            self.update_code_order_in_db()
            self.update_ui()

    def update_code_order_in_db(self):
        # UI에서 코드 블록 순서가 변경될 때 데이터베이스의 순서를 업데이트하는 메서드
        for index, child in enumerate(self.sizer.GetChildren()):
            if child.IsWindow():
                code_box = child.GetWindow()
                update_code_order(code_box.text, index)

    def workflowRun(self, event=None):
        print("workflowRun 실행")

        # 동일한 유형의 코드 블록을 그룹화하여 저장할 변수들
        combined_code = []
        current_type = None
        
        # self.code_blocks 리스트의 코드 블록을 order_num 순서대로 실행
        for code_block in sorted(self.code_blocks, key=lambda x: x[3]):  # order_num을 기준으로 정렬
            code_id, code_type, code_data, order_num = code_block

            # 동일한 그룹의 코드 타입일 경우
            if current_type == code_type:
                combined_code.append(code_data)

            else:
                # 이전 코드 그룹을 실행하고 초기화
                if combined_code:
                    # 코드 블록을 합쳐서 실행
                    code_to_execute = ' && '.join(combined_code) if current_type in ['bash', 'zsh', 'cmd', 'shell'] else '\n'.join(combined_code)
                    output = execute_code(code_to_execute, current_type)
                    print(output)
                    combined_code = []

                # 새 그룹 시작
                combined_code.append(code_data)
                current_type = code_type

        # 마지막 그룹 실행
        if combined_code:
            code_to_execute = ' && '.join(combined_code) if current_type in ['bash', 'zsh', 'cmd', 'shell'] else '\n'.join(combined_code)
            output = execute_code(code_to_execute, current_type)
            print(output)

    
    def OnDragStart(self, event):
        self.dragging_item = event.GetEventObject().GetParent()
        self.dragging_item.Hide()
        event.Skip()

    def OnDrop(self, event):
        pos = event.GetPosition()
        target_item, index = self.FindTargetItem(pos)
        if target_item:
            self.sizer.Insert(index, self.dragging_item,
                              0, wx.ALL | wx.EXPAND, 10)
            self.dragging_item.Show()
            self.sizer.Layout()
            self.update_ui()

            # 순서 변경을 DB에 반영
            self.update_code_order_in_db()

        event.Skip()

    def FindTargetItem(self, pos):
        for index, item in enumerate(self.sizer.GetChildren()):
            if item.GetWindow().GetScreenRect().Contains(pos):
                return item.GetWindow(), index
        return None, -1

    def update_code_order_in_db(self):
        """
        DB의 코드 블록 순서를 업데이트하는 함수
        """
        for index, child in enumerate(self.sizer.GetChildren()):
            code_box = child.GetWindow()
            code_id = code_box.code_id  # 각 CodeBox에 code_id를 저장해야 합니다.
            update_code_order(code_id, index + 1)
