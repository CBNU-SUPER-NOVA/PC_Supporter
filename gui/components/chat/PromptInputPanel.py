import wx
from gui.components import SVGButton, Font
from gpt_api.api import send_to_llm
from utils.code_extractor import extract_code
from utils.db_handler import save_message_to_db, get_conversation_model, load_prompt_setting


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
        self.prompt_input.SetFont(Font.bold(16))

        # 초기 입력 창 크기 설정
        self.prompt_input.SetMinSize(
            wx.Size(self.fixed_width, self.initial_height))
        self.prompt_input.SetSize(
            wx.Size(self.fixed_width, self.initial_height))

        # 초기 최대 높이 설정 (이 높이까지는 스크롤 없이 확장됨)
        self.max_height = self.initial_height * 5

        sizer.Add(self.prompt_input, 1, wx.EXPAND | wx.ALL, self.padding)

        # 전송 버튼 생성
        self.send_button = SVGButton(self, "gui/icons/Arrow.svg", 30, self.send_prompt, hover_color="#AAAAAA")
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

        self.saved_prompt = load_prompt_setting()

        if prompt_text:
            # 1. 사용자가 입력한 프롬프트에 사전에 저장된 프롬프트 결합
            if self.saved_prompt:
                combined_prompt = f"{self.saved_prompt}\n{prompt_text}"
            else:
                combined_prompt = prompt_text

            # 2. 유저 메시지를 DB에 추가 및 새로고침
            save_message_to_db(self.Parent.conversation_id,
                               "user", "text", prompt_text)
            self.Parent.update_list()

            # 3. LLM(GPT 또는 Gemini) API로 프롬프트 전송 및 응답 수신

            # 사용할 API 선택
            ai_model = get_conversation_model(self.Parent.conversation_id)

            raw_response = send_to_llm(combined_prompt, ai_model)

            print(raw_response)
            # 4. 응답 정제
            response = extract_code(raw_response)

            # 5. 정제된 응답 DB에 추가 및 새로고침
            self.add_response_to_DB(response)
            self.Parent.update_list()

    def add_response_to_DB(self, response):
        """정제된 응답을 GUI에 추가하는 메서드"""
        for item in response:
            # AI 응답이 텍스트일 경우
            if item["type"] == "text":
                save_message_to_db(self.Parent.conversation_id,
                                   "ai", "text", item["data"])
            # AI 응답이 코드 블럭일 경우
            elif item["type"] in ["python", "bash"]:
                save_message_to_db(self.Parent.conversation_id, "ai",
                                   item["type"], item["data"])
