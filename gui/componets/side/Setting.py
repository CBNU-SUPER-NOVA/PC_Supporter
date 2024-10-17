import wx

# 설정 다이얼로그
# TODO : 실제 API 키 인증 로직 추가


class Settings(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="API Key 입력", size=(600, 250))

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

        # Todo : 실제 db상에 값이 있을경우 저장된값으로 넣어주기
        self.chatgpt_api_input.SetValue("Chat GPT API Key")
        self.gemini_api_input.SetValue("Gemini API Key")
        # Todo : 실제 db상에 선택되어져있는 모델로 라디오버튼 선택하기
        setradio = 2
        if(setradio == 1):
            self.chatgpt_radio.SetValue(True)
        elif(setradio == 2):
            self.gemini_radio.SetValue(True)

    def on_check_chatgpt_api(self, event):
        api_key = self.chatgpt_api_input.GetValue()
        # 여기에서 실제 API 키 인증 확인 로직을 추가할 수 있습니다.
        if api_key:  # 단순히 입력이 있으면 인증된다고 가정
            api_key_test = True
            if(api_key_test):
                wx.MessageBox("Chat GPT API 키가 인증되었습니다!", "확인", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("잘못된 Chat GPT API 키입니다.", "확인", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Chat GPT API 키를 입력하세요.", "경고", wx.OK | wx.ICON_WARNING)

    def on_check_gemini_api(self, event):
        api_key = self.gemini_api_input.GetValue()
        # 여기에서도 실제 API 키 인증 확인 로직을 추가할 수 있습니다.
        if api_key:
            api_key_test = True
            if(api_key_test):
                wx.MessageBox("Chat GPT API 키가 인증되었습니다!", "확인", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("잘못된 Chat GPT API 키입니다.", "확인", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Gemini API 키를 입력하세요.", "경고", wx.OK | wx.ICON_WARNING)

    def on_ok(self, event):
        # 현재 선택된 라디오 버튼과 입력된 API 키 값 확인
        selected_model = "Chat GPT" if self.chatgpt_radio.GetValue() else "Gemini"
        api_key = self.chatgpt_api_input.GetValue() if selected_model == "Chat GPT" else self.gemini_api_input.GetValue()

        # 현재 선택된 라디오 값과 입력된 api키 값 확인해서 문제있으면 경고창 띄우기
        if selected_model == "Chat GPT" and not api_key:
            # 키가 없을경우 경고창 띄우기
            wx.MessageBox("Chat GPT API 키를 입력하세요.", "경고", wx.OK | wx.ICON_WARNING)
            # db상의 키값이 맞지 않을경우 경고창 띄우기
        elif selected_model == "Gemini" and not api_key:
            wx.MessageBox("Gemini API 키를 입력하세요.", "경고", wx.OK | wx.ICON_WARNING)
        else:
            # 전부다 괜찮을경우 모달창 닫기
            self.EndModal(wx.ID_OK)
        # 간단한 출력 테스트

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
