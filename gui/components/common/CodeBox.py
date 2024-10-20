import wx
from gui.components import SVGButton, EditButton
from utils.db_handler import save_code_to_db, update_code_data
from utils.code_executor import execute_code


class CodeBox(wx.Panel):
    def __init__(self, parent, isWorkflow, texts, language="python", fixed_width=400, code_id=None, conversation_id=None):
        super(CodeBox, self).__init__(parent)
        self.SetBackgroundColour("white")  # 배경색 설정
        # 변수 내용 저장
        self.text = texts
        self.language = language
        self.fixed_width = fixed_width  # 좌우 길이를 고정
        self.current_lines = 1  # 현재 라인 수를 추적
        self.padding = 10  # 패딩 설정
        self.initial_height = 24  # 초기 높이 설정
        self.min_height = 24  # 텍스트 부분의 최소 높이 설정
        self.code_id = code_id  # 각 CodeBox에 고유한 code_id 부여
        self.conversation_id = conversation_id  # conversation_id 저장

        # 메인 수직 박스 사이저 생성 (위아래 배치용)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 상단 부분을 감싸는 패널 생성 및 배경색 지정
        top_panel = wx.Panel(self)
        top_panel.SetBackgroundColour("#1E1E1E")  # 원하는 배경색 지정

        # 첫 번째 수평 박스 사이저 생성 (좌우 배치용)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 코딩언어 라벨 (좌측 정렬)
        self.codeLanguage = wx.StaticText(top_panel, label=self.language)
        self.codeLanguage.SetBackgroundColour("#1E1E1E")
        self.codeLanguage.SetForegroundColour("#FFFFFF")
        self.codeLanguage.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.codeLanguage.Wrap(400)

        # 좌측 정렬
        top_sizer.Add(self.codeLanguage, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 0)
        # 중간 공간 추가하여 버튼들을 우측으로 밀어내기
        top_sizer.AddStretchSpacer(1)

        # 버튼들 추가 (우측 정렬을 위한 공간 추가)
        self.codePlayButton = SVGButton(
            top_panel, "gui/icons/CodePlay.svg", 20, self.on_run)
        top_sizer.Add(self.codePlayButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        self.copyButton = SVGButton(top_panel, "gui/icons/Copy.svg", 20, self.on_copy)
        top_sizer.Add(self.copyButton, 0,
                      wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        if isWorkflow:
            # EditButton 추가
            self.editButton = EditButton(top_panel, "gui/icons/Edit.svg", 20)
            self.editButton.set_on_click(self.on_edit)
            top_sizer.Add(self.editButton, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
            # DeleteButton 추가
            self.deleteButton = SVGButton(
                top_panel, "gui/icons/Delete.svg", 20, self.on_delete)
            top_sizer.Add(self.deleteButton, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        else:
            # toWorkflowButton 추가
            self.toWorkflowButton = SVGButton(
                top_panel, "gui/icons/ToWorkflow.svg", 20, self.on_to_workflow)
            top_sizer.Add(self.toWorkflowButton, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        # 패널에 수평 박스 사이저 설정
        top_panel.SetSizer(top_sizer)

        # 수평 박스 사이저를 포함한 패널을 메인 수직 박스 사이저에 추가
        main_sizer.Add(top_panel, 0, wx.EXPAND | wx.ALL, 10)

        # 코드 입력 상자 (아래쪽)
        self.code = wx.TextCtrl(self, value=self.text, style=wx.NO_BORDER | wx.TE_MULTILINE |
                                wx.TE_NO_VSCROLL | wx.TE_RICH2 | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.code.SetEditable(False)
        self.code.SetBackgroundColour("#000000")
        self.code.SetForegroundColour("#FFFFFF")
        self.code.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.code.SetStyle(0, self.code.GetLastPosition(),
                           wx.TextAttr(wx.Colour(255, 255, 255)))  # 흰색 텍스트

        # 고정된 너비와 기본 높이 설정
        self.code.SetMinSize(wx.Size(self.fixed_width, self.min_height))
        self.code.SetSize(wx.Size(self.fixed_width, self.initial_height))

        # 텍스트가 변경될 때 이벤트 바인딩
        self.code.Bind(wx.EVT_TEXT, self.OnTextChange)

        # 코드 입력 상자를 메인 수직 박스 사이저에 추가
        main_sizer.Add(self.code, 1, wx.EXPAND | wx.ALL, self.padding)

        # 메인 수직 박스 사이저를 패널에 설정
        self.SetSizer(main_sizer)

        # 초기 텍스트 줄 수에 따라 크기 조정
        self.update_size(initial=True)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnPaint(self, event):
        width, height = self.GetSize()
        radius = 15  # 둥근 모서리의 반지름 설정

        # 더블 버퍼링을 위한 장치 맥락 생성
        dc = wx.BufferedPaintDC(self)
        dc.Clear()

        # 그래픽 컨텍스트 생성
        gc = wx.GraphicsContext.Create(dc)

        # 위쪽 모서리만 둥근 사각형 그리기 (path_top)
        path_top = gc.CreatePath()
        path_top.MoveToPoint(radius, 0)
        path_top.AddLineToPoint(width - radius, 0)
        path_top.AddArcToPoint(width, 0, width, radius, radius)  # 오른쪽 위 둥근 모서리
        path_top.AddLineToPoint(width, 40)
        path_top.AddLineToPoint(0, 40)
        path_top.AddLineToPoint(0, radius)
        path_top.AddArcToPoint(0, 0, radius, 0, radius)  # 왼쪽 위 둥근 모서리
        path_top.CloseSubpath()
        gc.SetBrush(wx.Brush("#1E1E1E"))  # 원하는 색상으로 변경
        gc.SetPen(wx.Pen("#1E1E1E", 0))
        gc.DrawPath(path_top)

        # 아래쪽 모서리만 둥근 사각형 그리기 (path_bottom)
        path_bottom = gc.CreatePath()
        path_bottom.MoveToPoint(0, 40)
        path_bottom.AddLineToPoint(0, height - radius)
        path_bottom.AddArcToPoint(
            0, height, radius, height, radius)  # 왼쪽 아래 둥근 모서리
        path_bottom.AddLineToPoint(width - radius, height)
        path_bottom.AddArcToPoint(
            width, height, width, height - radius, radius)  # 오른쪽 아래 둥근 모서리
        path_bottom.AddLineToPoint(width, 40)
        path_bottom.AddLineToPoint(0, 40)
        path_bottom.CloseSubpath()
        gc.SetBrush(wx.Brush("#000000"))
        gc.SetPen(wx.Pen("#000000", 0))
        gc.DrawPath(path_bottom)

    def OnResize(self, event):
        # 리사이즈 시 다시 그리기
        self.Refresh()
        event.Skip()

    def OnTextChange(self, event):
        self.update_size()

    def update_size(self, initial=False):
        # 현재 텍스트에서 라인의 수를 계산
        lines = self.code.GetNumberOfLines()

        # 초기 렌더링 시에도 크기 조정
        if initial or lines != self.current_lines:
            self.current_lines = lines
            # 텍스트 높이 측정
            text_height = self.code.GetCharHeight() * lines

            # 창의 높이 설정 (최소 높이만 고려)
            new_height = max(text_height + self.padding + 40,  # 40 추가
                             self.min_height)

            self.code.SetMinSize(wx.Size(self.fixed_width, new_height))
            self.code.SetSize(wx.Size(self.fixed_width, new_height))

            # 패널의 크기 업데이트 및 레이아웃 재조정
            self.SetMinSize(
                wx.Size(self.fixed_width, new_height + self.padding))
            self.Layout()
            self.Fit()

            # 부모 패널의 레이아웃 재조정 (새로 추가된 부분)
            if self.Parent:
                self.Parent.Layout()
                self.Parent.FitInside()  # 부모 패널의 크기를 업데이트

            self.Refresh()

    def on_run(self, event):
        # 실행할 코드와 언어를 정의
        code = self.code.GetValue()
        language = self.language

        # 코드 실행
        output = execute_code(code, language)

        # 결과를 메시지 박스로 표시
        wx.MessageBox(f"language = {language}\ntexts = {code}\n\nOutput:\n{output}", "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_copy(self, event):
        # 클립보드에 텍스트 복사
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.code.GetValue()))
            wx.TheClipboard.Close()
            wx.MessageBox("텍스트가 클립보드에 복사되었습니다.", "Info",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("클립보드에 접근할 수 없습니다.", "Error", wx.OK | wx.ICON_ERROR)

    def on_edit(self, event):
        if self.code.IsEditable():
            self.code.SetEditable(False)
            self.editButton.is_active = False  # 활성화 해제
            # 코드 블록을 데이터베이스에 업데이트
            update_code_data(self.code_id, self.code.GetValue())
            # 메시지 박스로 편집 완료 메시지 표시
            wx.MessageBox("코드가 편집되었습니다.", "Info", wx.OK | wx.ICON_INFORMATION)

        else:
            self.code.SetEditable(True)
            self.editButton.is_active = True  # 활성화 상태로 설정

        self.editButton.Refresh()  # 버튼 상태 업데이트

    def on_delete(self, event):
        # 삭제 버튼 클릭 시 이벤트 처리
        parent = self.GetParent()  # ScrolledWindow
        grandparent = parent.GetParent()  # CodePanel

        if hasattr(grandparent, 'RemoveCodeBlock'):
            grandparent.RemoveCodeBlock(self)
        else:
            wx.MessageBox("코드 블록을 제거할 수 없습니다.", "Error", wx.OK | wx.ICON_ERROR)

    def on_to_workflow(self, event):
        """
        워크플로우로 전환 이벤트 처리
        워크플로우로 전환된 코드 블록을 DB에 저장합니다.
        """
        # 대화 ID가 None인지 확인
        if not hasattr(self.Parent.Parent.Parent, 'conversation_id'):
            wx.MessageBox("대화가 존재하지 않습니다. 대화를 먼저 생성하세요.",
                          "Error", wx.OK | wx.ICON_ERROR)
            return

        # 대화 ID 가져오기
        conversation_id = self.Parent.Parent.Parent.conversation_id

        # 코드 블록을 데이터베이스에 저장
        # order_num은 실제 순서에 맞게 처리 가능
        save_code_to_db(conversation_id, self.language,
                        self.text, order_num=1)
        wx.MessageBox("Code block successfully added to workflow!",
                      "Info", wx.OK | wx.ICON_INFORMATION)
        self.Parent.Parent.Parent.Parent.Parent.codePanel.update_list()
