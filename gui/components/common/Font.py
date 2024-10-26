import wx


class Font():
    @staticmethod
    def default(size=16):
        font = wx.Font(size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        font.SetPixelSize(wx.Size(0, size))  # 높이 16픽셀로 설정 (폭은 0으로 자동 설정)
        return font

    @staticmethod
    def bold(size=16):
        font = wx.Font(size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        font.SetPixelSize(wx.Size(0, size))  # 높이 16픽셀로 설정 (폭은 0으로 자동 설정)
        return font
