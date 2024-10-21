import wx

from gpt_api.api import validate_gemini_api_key, validate_openai_api_key
from utils.db_handler import load_api_key, save_api_key
# 설정 다이얼로그


class Settings(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Settings", size=(600, 250))

        panel = wx.Panel(self)

        # 사용 모델 레이블
        model_label = wx.StaticText(panel, label="사용 모델", pos=(20, 20))

        # 라디오 버튼 (Chat GPT, Gemini)
        self.chatgpt_radio = wx.RadioButton(panel, label="Chat GPT", pos=(20, 50), style=wx.RB_GROUP)
        self.gemini_radio = wx.RadioButton(panel, label="Gemini", pos=(20, 80))

        # Chat GPT API 키 입력란
        chatgpt_api_label = wx.StaticText(panel, label="Chat GPT API키:", pos=(130, 50))
        self.chatgpt_api_input = wx.TextCtrl(panel, pos=(230, 50), size=(240, 25), style=wx.TE_PASSWORD)

        # Chat GPT 인증키 확인 버튼
        self.chatgpt_check_button = wx.Button(panel, label="인증키 확인", pos=(480, 50))
        self.chatgpt_check_button.Bind(wx.EVT_BUTTON, self.on_check_chatgpt_api)

        # Gemini API 키 입력란
        gemini_api_label = wx.StaticText(panel, label="Gemini API키:", pos=(130, 80))
        self.gemini_api_input = wx.TextCtrl(panel, pos=(230, 80), size=(240, 25), style=wx.TE_PASSWORD)

        # 라디오 버튼 이벤트 핸들러
        self.chatgpt_radio.Bind(wx.EVT_RADIOBUTTON, self.on_radio_button_selected)
        self.gemini_radio.Bind(wx.EVT_RADIOBUTTON, self.on_radio_button_selected)

        # Gemini 인증키 확인 버튼
        self.gemini_check_button = wx.Button(panel, label="인증키 확인", pos=(480, 80))
        self.gemini_check_button.Bind(wx.EVT_BUTTON, self.on_check_gemini_api)

        # OK 버튼
        ok_button = wx.Button(panel, label="OK", pos=(250, 150))
        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)

        # DB에서 저장된 값 불러오기
        self.load_saved_values()

        # # Todo : 실제 db상에 값이 있을경우 저장된값으로 넣어주기
        # self.chatgpt_api_input.SetValue("Chat GPT API Key")
        # self.gemini_api_input.SetValue("Gemini API Key")
        # # Todo : 실제 db상에 선택되어져있는 모델로 라디오버튼 선택하기
        # setradio = 2
        # if(setradio == 1):
        #     self.chatgpt_radio.SetValue(True)
        # elif(setradio == 2):
        #     self.gemini_radio.SetValue(True)

    def load_saved_values(self):
        """DB에서 저장된 API 키와 모델을 불러와 필드에 반영합니다."""
        gpt_key = load_api_key("Chat GPT")
        gemini_key = load_api_key("Gemini")

        # API 키 필드에 저장된 값 반영
        if gpt_key:
            self.chatgpt_api_input.SetValue(gpt_key)
        if gemini_key:
            self.gemini_api_input.SetValue(gemini_key)

        # 기본 모델 선택 (DB에서 가져온 값으로 설정 가능)
        selected_model = "Gemini" if gemini_key else "Chat GPT"
        if selected_model == "Chat GPT":
            self.chatgpt_radio.SetValue(True)
        else:
            self.gemini_radio.SetValue(True)

    def on_check_chatgpt_api(self, event):
        """Chat GPT API 키 유효성 확인"""
        api_key = self.chatgpt_api_input.GetValue().strip()
        if api_key and validate_openai_api_key(api_key):
            wx.MessageBox("Chat GPT API 키가 인증되었습니다!", "확인", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("잘못된 Chat GPT API 키입니다.", "오류", wx.OK | wx.ICON_ERROR)

    def on_check_gemini_api(self, event):
        """Gemini API 키 유효성 확인"""
        api_key = self.gemini_api_input.GetValue().strip()
        if api_key and validate_gemini_api_key(api_key):
            wx.MessageBox("Gemini API 키가 인증되었습니다!", "확인", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("잘못된 Gemini API 키입니다.", "오류", wx.OK | wx.ICON_ERROR)

    def on_ok(self, event):
        """OK 버튼 클릭 시 API 키 저장 및 설정 적용"""
        selected_model = "Chat GPT" if self.chatgpt_radio.GetValue() else "Gemini"
        api_key = self.chatgpt_api_input.GetValue().strip() if selected_model == "Chat GPT" else self.gemini_api_input.GetValue().strip()

        if not api_key:
            wx.MessageBox(f"{selected_model} API 키를 입력하세요.", "경고", wx.OK | wx.ICON_WARNING)
            return

        # 유효한 키만 DB에 저장
        if selected_model == "Chat GPT" and validate_openai_api_key(api_key):
            save_api_key("Chat GPT", api_key)
            wx.MessageBox("Chat GPT API 키가 저장되었습니다.", "성공", wx.OK | wx.ICON_INFORMATION)
        elif selected_model == "Gemini" and validate_gemini_api_key(api_key):
            save_api_key("Gemini", api_key)
            wx.MessageBox("Gemini API 키가 저장되었습니다.", "성공", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("유효하지 않은 API 키입니다.", "오류", wx.OK | wx.ICON_ERROR)
            return

        # 설정이 완료되면 다이얼로그 닫기
        self.EndModal(wx.ID_OK)

    def get_selection(self):
        """사용자가 선택한 옵션을 반환"""
        if self.gemini_radio.GetValue():
            return "GEMINI"
        elif self.chatgpt_radio.GetValue():
            return "ChatGPT"

    def on_radio_button_selected(self, event):
        """라디오 버튼 선택시 이벤트 핸들러"""
        radio_selected = event.GetEventObject()
        if radio_selected == self.chatgpt_radio:
            print("Chat GPT 모델이 선택되었습니다.")
        elif radio_selected == self.gemini_radio:
            print("Gemini 모델이 선택되었습니다.")
        else:
            raise ValueError("올바르지 않은 라디오 버튼입니다.")
