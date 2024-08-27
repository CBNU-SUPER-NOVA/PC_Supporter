from utils.code_extractor import extract_code
from gui.componets.CodeBox import CodeBox
import wx
from gui.componets.SVGButton import SVGButton
from gui.componets.AIChatBox import AIChatBox  # AIChatBox 모듈이 아닌 클래스 임포트
from gui.componets.MyChatBox import MyChatBox  # MyChatBox를 명확하게 임포트
from gpt_api.api import send_to_gpt
from utils.db_handler import create_conversation, save_code_to_db


class PromptInputPanel(wx.Panel):
    def __init__(self, parent):
        super(PromptInputPanel, self).__init__(parent)

        self.basecolor = "#F7F7F8"
        self.padding = 14
        self.fixed_width = 400
        self.current_lines = 1
        self.initial_height = 26
        self.conversation_id = None  # 대화 ID를 저장

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
        lines = self.prompt_input.GetNumberOfLines()

        if lines != self.current_lines:
            self.current_lines = lines
            text_height = self.prompt_input.GetCharHeight() * lines
            new_height = min(text_height + self.padding, self.max_height)

            self.prompt_input.SetMinSize(wx.Size(self.fixed_width, new_height))
            self.prompt_input.SetSize(wx.Size(self.fixed_width, new_height))
            self.SetMinSize(
                wx.Size(self.fixed_width, new_height + self.padding))
            self.Layout()
            self.Fit()

            if self.Parent:
                self.Parent.Layout()

            self.Refresh()

    def clear_prompt(self):
        self.prompt_input.Clear()
        self.current_lines = 1  # 라인 수를 초기 상태로 복원
        self.Layout()
        self.Fit()

        if self.Parent:
            self.Parent.Layout()

        self.Refresh()

    def send_prompt(self, event=None):
        prompt_text = self.prompt_input.GetValue().strip()
        self.clear_prompt()

        if prompt_text:
            # 1. 유저 메시지를 GUI에 추가
            user_chat = MyChatBox(self.Parent.middle_panel, prompt_text)
            self.Parent.middle_panel.GetSizer().Add(user_chat, 0, wx.ALL | wx.EXPAND, 5)

            # 2. GPT API로 프롬프트 전송 및 응답 수신
            raw_response = send_to_gpt(prompt_text)

            # 3. 응답 정제
            response = extract_code(raw_response)

            # 4. 정제된 응답 GUI 추가
            self._add_response_to_gui(response)

            # 5. 레이아웃 갱신 및 화면 새로고침
            self._refresh_layout()

    def _add_response_to_gui(self, response):
        """정제된 응답을 GUI에 추가하는 메서드"""
        for item in response:
            if item["type"] == "text":
                ai_chat = AIChatBox(self.Parent.middle_panel, item["data"])
                self.Parent.middle_panel.GetSizer().Add(ai_chat, 0, wx.ALL | wx.EXPAND, 5)
            elif item["type"] in ["python", "bash"]:
                # CodeBox 생성 및 추가
                code_box = CodeBox(self.Parent.middle_panel, isWorkflow=False,
                                texts=item["data"], language=item["type"])
                self.Parent.middle_panel.GetSizer().Add(code_box, 0, wx.ALL | wx.EXPAND, 5)

                # 강제로 레이아웃과 크기 갱신
                code_box.update_size()  # 강제로 크기 업데이트 호출
                code_box.Layout()
                code_box.Refresh()

        # 전체 레이아웃 갱신
        self.Parent.middle_panel.GetSizer().Layout()
        self.Parent.middle_panel.FitInside()
        self.Parent.middle_panel.Scroll(
            0, self.Parent.middle_panel.GetScrollRange(wx.VERTICAL))
        self.Parent.middle_panel.Refresh()
        
    def _refresh_layout(self):
        """레이아웃을 갱신하고 화면을 새로고침하는 메서드"""
        self.Parent.middle_panel.GetSizer().Layout()
        self.Parent.middle_panel.FitInside()
        self.Parent.middle_panel.Scroll(
            0, self.Parent.middle_panel.GetScrollRange(wx.VERTICAL))
        self.Parent.middle_panel.Refresh()

    def handle_chat(self, tempdata):
        """채팅 데이터를 처리하여 GUI에 추가하는 메서드"""
        for data in tempdata:
            if data["type"] == "User":
                user_chat = MyChatBox(self.middle_panel, data["data"])
                self.middle_sizer.Add(user_chat, 0, wx.ALL | wx.EXPAND, 5)
            elif data["type"] == "AI":
                self._add_response_to_gui(data["data"])  # 정제된 응답을 처리
        self._refresh_layout()  # 레이아웃 갱신

    def clear_prompt(self):
        self.prompt_input.Clear()
        self.current_lines = 1
        self.Layout()
        self.Fit()
