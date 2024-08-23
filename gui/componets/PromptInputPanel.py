import wx
from gui.componets.SVGButton import SVGButton


class PromptInputPanel(wx.Panel):
    def __init__(self, parent):
        super(PromptInputPanel, self).__init__(parent)

        self.basecolor = "#DDDDDD"

        # 배경 색상 설정 (올바르게 메서드를 호출하여 배경색 설정)
        self.SetBackgroundColour("white")

        # 입력창과 버튼을 위한 Sizer 생성
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 프롬프트 입력 창 생성 (wx.TE_PROCESS_ENTER 플래그 추가)
        self.prompt_input = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.BORDER_NONE | wx.TE_PROCESS_ENTER)
        self.prompt_input.SetHint("프롬프트를 작성해주세요")  # 힌트 텍스트 추가
        self.prompt_input.SetBackgroundColour(self.basecolor)  # 입력창의 배경색 설정

        # 폰트 크기 설정 (10포인트로 설정)
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.prompt_input.SetFont(font)

        # 입력 창 크기 고정
        self.prompt_input.SetMinSize(wx.Size(400, 20))  # 원하는 크기로 설정
        self.prompt_input.SetSize(wx.Size(400, 20))     # 크기 설정

        sizer.Add(self.prompt_input, 1, wx.EXPAND | wx.ALL, 10)

        # 전송 버튼 생성
        self.send_button = SVGButton(self, "gui/icons/Arrow.svg", 40)
        self.send_button.SetBackgroundColour(self.basecolor)
        self.send_button.set_on_click(self.send_Prompt)
        sizer.Add(self.send_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)

        # 엔터키로 전송
        self.prompt_input.Bind(wx.EVT_TEXT_ENTER, self.send_Prompt)

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
        radius = 20
        gc.DrawRoundedRectangle(
            rect.x, rect.y, rect.width, rect.height, radius)

    def get_prompt_text(self):
        return self.prompt_input.GetValue()

    def clear_prompt(self):
        self.prompt_input.Clear()

    def send_Prompt(self, event=None):
        print("프롬프트가 전송되었습니다.")
        self.clear_prompt()
        # 추가적인 전송 로직 작성
