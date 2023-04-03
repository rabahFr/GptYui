from wx import Frame, Panel, BoxSizer, ALL, EXPAND, BITMAP_TYPE_JPEG, Icon, HORIZONTAL
from ui.chat_message_grid import ChatMessageGrid

class ChatPanel(Frame):
    def __init__(self, title):
        super().__init__(parent=None, title=title)
        panel = Panel(self)

        hbox = BoxSizer(HORIZONTAL)

        chatGrid = ChatMessageGrid(panel)

        hbox.Add(chatGrid, proportion=1, flag=ALL | EXPAND, border=15)
        panel.SetSizer(hbox)

        loc = Icon(r"assets/logo.jpg", BITMAP_TYPE_JPEG)
        self.SetIcon(Icon(loc))
        self.Centre()
        self.SetSize((800, 600))
        self.Show()