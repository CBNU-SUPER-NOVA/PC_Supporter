import wx
from gui.componets.SVGButton import SVGButton


class PromptInputPanel(wx.Panel):
    def __init__(self, parent):
        super(PromptInputPanel, self).__init__(parent)

        self.basecolor = "#F7F7F8"
        self.padding = 14  # 패딩 설정
        self.fixed_width = 400  # 고정된 너비 설정
        self.current_lines = 1  # 현재 라인 수를 추적
        self.initial_height = 26   # 초기 높이 설정

        # 배경 색상 설정
        self.SetBackgroundColour("white")

        # 입력창과 버튼을 위한 Sizer 생성
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 프롬프트 입력 창 생성
        self.prompt_input = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.BORDER_NONE | wx.TE_PROCESS_ENTER)
        self.prompt_input.SetHint("프롬프트를 작성해주세요")
        self.prompt_input.SetBackgroundColour(self.basecolor)

        # 폰트 크기 설정
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.prompt_input.SetFont(font)

        # 초기 입력 창 크기 설정
        self.prompt_input.SetMinSize(
            wx.Size(self.fixed_width, self.initial_height))
        self.prompt_input.SetSize(
            wx.Size(self.fixed_width, self.initial_height))

        # 초기 최대 높이 설정 (이 높이까지는 스크롤 없이 확장됨)
        self.max_height = self.initial_height * 5

        sizer.Add(self.prompt_input, 1, wx.EXPAND | wx.ALL, self.padding)

        # 전송 버튼 생성
        self.send_button = SVGButton(self, "gui/icons/Arrow.svg", 30)
        self.send_button.SetBackgroundColour(self.basecolor)
        self.send_button.set_on_click(self.send_prompt)
        sizer.Add(self.send_button, 0, wx.ALIGN_CENTER_VERTICAL |
                  wx.RIGHT, self.padding)

        # 엔터키로 전송
        self.prompt_input.Bind(wx.EVT_TEXT_ENTER, self.send_prompt)

        # 텍스트 크기 변경 이벤트 연결
        self.prompt_input.Bind(wx.EVT_TEXT, self.on_text_change)

        self.SetSizer(sizer)
        self.Layout()

        # 페인팅 이벤트 연결
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        # 배경색 설정
        gc.SetBrush(wx.Brush(self.basecolor))  # 배경색을 지정된 색으로 설정
        # 둥근 모서리 그리기
        rect = self.GetClientRect()
        radius = 25
        gc.DrawRoundedRectangle(
            rect.x, rect.y, rect.width, rect.height, radius)

    def on_text_change(self, event):
        # 현재 텍스트에서 라인의 수를 계산
        lines = self.prompt_input.GetNumberOfLines()

        # 라인이 변경된 경우에만 리렌더링
        if lines != self.current_lines:
            self.current_lines = lines

            # 텍스트 높이 측정
            text_height = self.prompt_input.GetCharHeight() * lines

            # 창의 높이 설정 (최대 높이까지 증가)
            new_height = min(text_height + self.padding, self.max_height)

            self.prompt_input.SetMinSize(wx.Size(self.fixed_width, new_height))
            self.prompt_input.SetSize(wx.Size(self.fixed_width, new_height))

            # 패널의 크기 업데이트 및 레이아웃 재조정
            self.SetMinSize(
                wx.Size(self.fixed_width, new_height + self.padding))
            self.Layout()
            self.Fit()

            # 부모 패널 (AiPanel)의 레이아웃 재조정
            if self.Parent:
                self.Parent.Layout()

            self.Refresh()

    def clear_prompt(self):
        self.prompt_input.Clear()
        self.current_lines = 1  # 라인 수를 초기 상태로 복원
        self.Layout()
        self.Fit()

        # 부모 패널 (AiPanel)의 레이아웃 재조정
        if self.Parent:
            self.Parent.Layout()

        self.Refresh()

    def send_prompt(self, event=None):
        prompt_text = self.prompt_input.GetValue()
        self.clear_prompt()
        if prompt_text.strip():  # 공백이 아닌 경우에만 전송
            # 추가적인 전송 로직 작성
            from gpt_api.api import send_to_gpt
            json = send_to_gpt(prompt_text)
            print(json)
