# MIT License
# Copyright (c) 2024 CBNU-SUPER-NOVA
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import wx
from gui import AiPanel, CodePanel, SidePanel
from utils.db_handler import init_db, get_conversation_names, create_conversation


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.SetSize((1200, 800))
        self.SetTitle("PCSupporter")
        # 스플릿 패널 추가
        self.splitter = wx.SplitterWindow(self)

        # 메인 패널 생성 및 추가
        self.aiPanel = AiPanel(self.splitter)

        # 코드 패널 생성 및 추가
        self.codePanel = CodePanel(self.splitter)

        # 스플릿 패널 속성
        self.splitter.SetMinimumPaneSize(600)
        self.splitter.SplitVertically(self.aiPanel, self.codePanel)

        # 오버레이 패널 생성 및 추가
        self.sidePanel = SidePanel(self.splitter)

        # 데이터를 새로고침
        self.refresh_data(init_Conversation())

    def refresh_data(self, conversation_id):
        # 데이터를 새로고침하는 메서드
        self.conversation_id = conversation_id  # 대화 ID 저장
        self.aiPanel.conversation_id = conversation_id
        self.codePanel.conversation_id = conversation_id
        self.aiPanel.update_list()
        self.codePanel.update_list()


def main():
    init_db()
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()


def init_Conversation():
    # DB 에서 대화이름들을 가져옴
    conversation_names = get_conversation_names()
    # 대화 목록이 없을경우 MyConversation으로 하나 생성하고 지정함
    if not conversation_names:
        conversation_name = "MyConversation"
        conversation_id = create_conversation(conversation_name)
        return conversation_id
    else:
        conversation_id = conversation_names[0][0]
        return conversation_id


if __name__ == "__main__":
    main()
