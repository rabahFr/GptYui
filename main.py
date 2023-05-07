import wx
from ui.ai_chat_ui_main import ChatPanel

if __name__ == "__main__":
    app = wx.App()
    frame = ChatPanel("AI Chat")
    app.MainLoop() 