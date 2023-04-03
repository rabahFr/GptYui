import wx
from ui.chat_message_grid import ChatMessageGrid

class ChatPanel(wx.Frame):
    def __init__(self, title):
        super().__init__(parent=None, title=title)
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        chatGrid = ChatMessageGrid(panel)

        hbox.Add(chatGrid, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        panel.SetSizer(hbox)

        loc = wx.Icon(r"assets/logo.jpg", wx.BITMAP_TYPE_JPEG)
        self.SetIcon(wx.Icon(loc))
        self.Centre()
        self.SetSize((800, 600))
        self.Show()