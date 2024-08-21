import wx


class CodeBox(wx.Panel):
    # Todo => drag and drop , UI 수정
    def __init__(self, parent, isWorkflow, texts, language="python"):
        super(CodeBox, self).__init__(parent)
        # 박스의 크기
        self.SetSize((540, 100))
        selfWidth, selfHeight = self.GetSize()
        print(selfWidth, selfHeight)
        self.SetBackgroundColour("blue")

        # 변수 내용 저장
        self.text = texts
        self.language = language

        # 코딩언어
        self.codeLanguage = wx.StaticText(
            self, label=self.language, pos=(20, 20))
        self.codeLanguage.SetBackgroundColour("white")
        self.codeLanguage.SetForegroundColour("black")
        self.codeLanguage.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.codeLanguage.Wrap(400)
        # 코드
        self.code = wx.TextCtrl(self, value=self.text, pos=(20, 40), size=(selfWidth - 40, selfHeight - 50),
                                style=wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_RICH2 | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.code.SetEditable(False)
        self.code.SetBackgroundColour("white")
        self.code.SetForegroundColour("black")
        self.code.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        # self.code.Wrap(400)

        # 버튼들 추가
        # codeRun , codeCopy , codeEdit , isWorkflow False => codeToWorkFlow , isWorkflow True => codeboxDelete
        self.runButton = wx.Button(
            self, label="Run", pos=(selfWidth - 20 - 70 * 4, 20))
        self.runButton.Bind(wx.EVT_BUTTON, self.on_run)

        self.copyButton = wx.Button(
            self, label="Copy", pos=(selfWidth - 20 - 70 * 3, 20))
        self.copyButton.Bind(wx.EVT_BUTTON, self.on_copy)

        self.editButton = wx.Button(
            self, label="Edit", pos=(selfWidth - 20 - 70 * 2, 20))
        self.editButton.Bind(wx.EVT_BUTTON, self.on_edit)

        if (isWorkflow):
            self.deleteButton = wx.Button(
                self, label="Delete", pos=(selfWidth - 20 - 70 * 1, 20))
            self.deleteButton.Bind(wx.EVT_BUTTON, self.on_delete)
        else:
            self.toWorkflowButton = wx.Button(
                self, label="toWorkflow", pos=(selfWidth - 20 - 70 * 1, 20))
            self.toWorkflowButton.Bind(wx.EVT_BUTTON, self.on_to_workflow)

    def on_run(self, event):
        wx.MessageBox("language = " + self.language + "   texts = " + self.text, "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_save(self, event):
        wx.MessageBox("Save Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_copy(self, event):
        wx.MessageBox("Copy Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_paste(self, event):
        wx.MessageBox("Paste Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_edit(self, event):
        if (self.code.IsEditable()):
            self.code.SetEditable(False)
        else:
            self.code.SetEditable(True)

    def on_delete(self, event):
        wx.MessageBox("Delete Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)

    def on_to_workflow(self, event):
        wx.MessageBox("toWorkflow Button Clicked!", "Info",
                      wx.OK | wx.ICON_INFORMATION)
