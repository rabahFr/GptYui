import wx
import wx.richtext as rt
from service.api_client import ApiClient
from utils.utils import model_choices
import threading

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


class ChatMessageGrid(wx.FlexGridSizer):
    def __init__(self, panel):
        super().__init__(6, 2, 9, 25)
        
        chatMessageApiKeyLabel = wx.StaticText(panel, label="API key")
        chatMessageApiKeyInput = wx.TextCtrl(panel)

        chatMessageHistoricLabel = wx.StaticText(panel, label="Chat", pos=(1, 0))
        chatMessageHistoricInput = rt.RichTextCtrl(panel, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)

        chatMessageSystemLabel = wx.StaticText(panel, label="System")
        chatMessageSystemInput = wx.TextCtrl(panel)

        chatMessageLabel = wx.StaticText(panel, label="your message")
        chatMessageText = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        chatMessageButton = wx.Button(panel, label="send")

        modelChoiceLabel = wx.StaticText(panel, label="model")
        modelChoiceBox = wx.ComboBox(panel, value="gpt-4", choices=model_choices)

        self.AddMany(
            [
                (chatMessageApiKeyLabel),
                (chatMessageApiKeyInput, 1, wx.EXPAND),
                (chatMessageSystemLabel),
                (chatMessageSystemInput, 1, wx.EXPAND),
                (chatMessageHistoricLabel, 1, wx.EXPAND),
                (chatMessageHistoricInput, 1, wx.EXPAND),
                (chatMessageLabel, wx.EXPAND),
                (chatMessageText, 1, wx.EXPAND),
                (modelChoiceLabel, wx.EXPAND),
                (modelChoiceBox, wx.EXPAND),
                (chatMessageButton, wx.EXPAND),
            ]
        )

        self.AddGrowableRow(2, 1)
        self.AddGrowableRow(3, 1)
        self.AddGrowableCol(1, 1)

        chatMessageButton.Bind(
            wx.EVT_BUTTON,
            lambda event: self.onClick(
                event,
                chatMessageSystemInput,
                chatMessageApiKeyInput,
                chatMessageHistoricInput,
                chatMessageText,
                modelChoiceBox,
                chatMessageButton
            ),
        )
        
    def completeRequest(self, messages, model, apiKey, chatMessageHistoricInput, message, button):
        # call the service
        client = ApiClient(apiKey)
        answer = client.complete(messages, model=model)

        messages.append({"role": "assistant", "content": answer})

        blue_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        blue_text_attr = rt.RichTextAttr()
        blue_text_attr.SetTextColour(wx.BLUE)
        blue_text_attr.SetFont(blue_font)
        
        red_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        red_text_attr = rt.RichTextAttr()
        red_text_attr.SetTextColour(wx.RED)
        red_text_attr.SetFont(red_font)
        
        # update the UI
        wx.CallAfter(chatMessageHistoricInput.BeginStyle, blue_text_attr)
        wx.CallAfter(chatMessageHistoricInput.WriteText, "User: " + message + "\n")
        wx.CallAfter(chatMessageHistoricInput.EndStyle)
        
        wx.CallAfter(chatMessageHistoricInput.BeginStyle, red_text_attr)
        wx.CallAfter(chatMessageHistoricInput.WriteText, "Assistant: " + answer + "\n")
        wx.CallAfter(chatMessageHistoricInput.EndStyle)
        wx.CallAfter(chatMessageHistoricInput.ShowPosition, chatMessageHistoricInput.GetLastPosition())
        
        button.Enable()

    def onClick(
        self,
        event,
        chatMessageSystemInput: wx.TextCtrl,
        chatMessageApiKeyInput: wx.TextCtrl,
        chatMessageHistoricInput: rt.RichTextCtrl,
        chatMessageText: wx.TextCtrl,
        modelChoiceBox: wx.ComboBox,
        button: wx.Button
    ):
        if not len(chatMessageApiKeyInput.GetValue().strip()):
            wx.MessageBox("API key is empty!", "Error", wx.OK | wx.ICON_ERROR)
        elif not len(chatMessageText.GetValue().strip()):
            wx.MessageBox("type something please!", "Error", wx.OK | wx.ICON_ERROR)
        else:
            apiKey = chatMessageApiKeyInput.GetValue().strip()
            message = chatMessageText.GetValue().strip()

            messages = [
                {
                    "role": "system",
                    "content": chatMessageSystemInput.GetValue().strip(),
                },
            ]
            messages.append({"role": "user", "content": message})


            button.Disable()

            # create a thread to run the API call
            t = threading.Thread(target=self.completeRequest, args=(messages, modelChoiceBox.GetValue(), apiKey, chatMessageHistoricInput, message, button))
            t.start()


            


if __name__ == "__main__":
    app = wx.App()
    frame = ChatPanel("AI Chat")
    app.MainLoop()
