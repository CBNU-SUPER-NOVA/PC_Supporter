import wx
from utils.db_handler import save_prompt_setting

# TODO : DB에 저장된 프롬프트를 불러와 텍스트 필드에 표시하는 기능 구현


class PromptSetting(wx.Dialog):
    def __init__(self, parent):
        super(PromptSetting, self).__init__(parent, title="Prompt Setting", size=(600, 150))

        # 레이아웃 구성
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 설명 텍스트 (부모 크기에 맞춰 확장)
        label = wx.StaticText(self, label="AI가 더 나은 응답을 제공해 드리기 위해 사용자님에 대해 알아두어야 할 것이 있다면 무엇인가요?")
        vbox.Add(label, flag=wx.ALL | wx.EXPAND, proportion=1, border=10)

        # 텍스트 입력 필드
        self.prompt_text_ctrl = wx.TextCtrl(self)
        vbox.Add(self.prompt_text_ctrl, flag=wx.ALL | wx.EXPAND, border=5)

        # 저장 버튼과 취소 버튼을 가로로 배치할 사이저
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # 저장 버튼
        save_button = wx.Button(self, label="Save")
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        hbox.Add(save_button, flag=wx.RIGHT, border=10)

        # 취소 버튼
        cancel_button = wx.Button(self, label="Cancel")
        cancel_button.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CANCEL))
        hbox.Add(cancel_button, flag=wx.LEFT, border=10)

        # hbox를 vbox에 추가하여 버튼을 가로로 정렬
        vbox.Add(hbox, flag=wx.ALL | wx.ALIGN_CENTER, border=10)

        self.SetSizer(vbox)

    def on_save(self, event):
        """
        Save 버튼 클릭 시 프롬프트를 DB에 저장하고 성공 메시지를 보여줍니다.
        """
        user_prompt = self.prompt_text_ctrl.GetValue().strip()
        if user_prompt:
            save_prompt_setting(user_prompt)  # 프롬프트를 DB에 저장
            wx.MessageBox("Prompt has been saved to the database.", "Success", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox("Prompt cannot be empty.", "Warning", wx.OK | wx.ICON_WARNING)
